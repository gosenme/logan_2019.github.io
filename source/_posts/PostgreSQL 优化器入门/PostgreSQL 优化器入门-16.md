---
title: PostgreSQL 优化器入门-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>如果有这样一条 SQL 语句：</p>
<pre><code>SELECT * FROM STUDENT, COURSE WHERE (sno =1 AND cname=’math’) OR (sno = 2 AND cname = ‘physics’)，
</code></pre>
<p>在对谓词做表达式预处理的时候，我们对这种类型的约束条件无从下手。我们知道 PostgreSQL 的约束条件的顶层是合取范式（或者说是“与”的方式），但这里的顶层是一个析取范式，这样的约束条件也只能应用到 STUDENT 表和 COURSE 表的连接结果上，对连接操作产生的结果进行过滤。如果有办法对其中的一些条件提取出来，并且下推到基表上，那么就会降低连接操作的计算量。</p>
<h3 id="">拆分约束条件</h3>
<p>通过分析 (sno =1 AND cname='math') OR (sno = 2 AND cname = 'physics') 这个约束条件就会发现，它是 OR 谓词连接起来的两个合取范式： (sno =1 AND cname='math') 和 (sno = 2 AND cname = 'physics') ，这样的连接条件产生的结果有什么特点呢？</p>
<p>对于 STUDENT 表而言，能够顺利通过这两个合取范式过滤的元组，一定具有这样的特征：sno = 1 或 sno = 2。同理，对于 COURSE 表而言，也能够得到一个类似的特征：cname = 'math' 或 cname = 'physics'。</p>
<p>结合之前提到过的谓词下推，会发现 sno = 1 或 sno = 2 这样的约束条件是能下推的。如果先把这两个约束条件应用（下推）到基表（STUDENT 表）上，显然就能实现我们降低计算量的目标（连接操作的计算量大大降低）。想到不如做到，PostgreSQL 于是就根据初始的约束条件 (sno =1 AND cname='math') OR (sno = 2 AND cname = 'physics') 进行推理，生成下面这样的执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT, COURSE WHERE (sno=1 AND cname='math') OR (sno=2 AND cname='physics');
                                                                     QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------
 Nested Loop  (cost=8.87..17.99 rows=3 width=65)
   Join Filter: (((student.sno = 1) AND ((course.cname)::text = 'math'::text)) OR ((student.sno = 2) AND ((course.cname)::text = 'physics'::text)))
   -&gt;  Bitmap Heap Scan on student  (cost=8.87..16.86 rows=2 width=19)
         Recheck Cond: ((sno = 1) OR (sno = 2))
         -&gt;  BitmapOr  (cost=8.87..8.87 rows=2 width=0)
               -&gt;  Bitmap Index Scan on student_pkey  (cost=0.00..4.44 rows=1 width=0)
                     Index Cond: (sno = 1)
               -&gt;  Bitmap Index Scan on student_pkey  (cost=0.00..4.44 rows=1 width=0)
                     Index Cond: (sno = 2)
   -&gt;  Materialize  (cost=0.00..1.04 rows=2 width=46)
         -&gt;  Seq Scan on course  (cost=0.00..1.03 rows=2 width=46)
               Filter: (((cname)::text = 'math'::text) OR ((cname)::text = 'physics'::text))
(12 rows)
</code></pre>
<p>从执行计划可以看出 sno = 1 OR sno = 2 和 cname = 'math' OR cname = 'physics' 都应用到了基表上，形成了过滤条件，这样的结果虽然完美，但是我们不能如此轻易满足，比如谓词已经下推，那么原来的 (sno=1 AND cname='math') OR (sno=2 AND cname='physics') 这个整体条件是否能消除掉呢？答案是不能，我们借用一点小学的知识把这个约束条件展开如下：</p>
<pre><code> (sno=1 AND cname='math') OR (sno=2 AND cname='physics')
= (sno=1 OR (sno=2 AND cname='physics)) AND (cname='math' OR (sno=2 AND cname=physics))
= (sno = 1 OR sno = 2) AND (sno=1 OR cname='physics) AND (cname='math' OR sno = 2) AND (cname='math' OR cname='physics')
</code></pre>
<p>我们下推的是其中的 (sno = 1 OR sno = 2) 和 (cname='math' OR cname='physics')，但连接条件中还应该有 (sno=1 OR cname='physics) AND (cname='math' OR sno = 2) 才能保持等价。这里 PostgreSQL 没有展开，只是保留了原来的条件，虽然有点冗余，但正确性是没有问题的。</p>
<h3 id="-1">提取表达式需要满足什么条件</h3>
<p>由于我们已经默认约束条件的顶层是一个合取范式，合取范式的下一层子句可能就是析取范式。这些析取范式如果是基于 OR 谓词的，就有可能提取出新的约束条件，例如对于约束条件 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) AND sname='JIM'，显然这个约束条件是析取范式 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) 和单个子句 sname='JIM' 形成的一个合取范式。其中析取范式 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) 是 OR 谓词连接的，就有可能提取出新的约束条件。</p>
<p>提取新的约束条件还需要满足析取范式中的每个子句（也就是 OR 谓词连接起来的每个下层的子约束条件）都同时引用了同一个表，也就是说 (sno=1 AND cname='math') 中被引用的 sno 是 STUDENT 表的属性，(sno=2 AND cname='physics') 中被引用的 sno 也是 STUDENT 表的属性，约束条件 sno = 1 OR sno = 2 才能被提取出来，否则就无法提取出新的约束条件。例如，对于 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics') OR sname = 'TOM'，由于 sname = 'TOM' 的存在，就无法提取出新的约束条件。</p>
<p>提取新的约束条件的时候还需要满足谓词下推的规则，这样新生成的约束条件才可以被认为是过滤条件而下推给表。 例如，对于一个左连接 SQL 语句，即使我们可以生成一个约束条件 sno = 1 OR sno = 2，但是这时它是一个连接条件，而属性 sno 所在的 STUDENT 表是在左连接的 Nonnullable-side，这样的连接条件不能下推给基表，因此生成这样的连接条件是没用的。从下面的示例中也可以看出并没有生成 sno = 1 OR sno = 2 这样的连接条件。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT LEFT JOIN COURSE ON (sno=1 AND cname='math') OR (sno=2 AND cname='physics');
                                                                     QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..119286.58 rows=1289119 width=65)
   Join Filter: (((student.sno = 1) AND ((course.cname)::text = 'math'::text)) OR ((student.sno = 2) AND ((course.cname)::text = 'physics'::text)))
   -&gt;  Seq Scan on student  (cost=0.00..61275.19 rows=1289119 width=19)
   -&gt;  Materialize  (cost=0.00..1.04 rows=2 width=46)
         -&gt;  Seq Scan on course  (cost=0.00..1.03 rows=2 width=46)
               Filter: (((cname)::text = 'math'::text) OR ((cname)::text = 'physics'::text))
(6 rows)
</code></pre>
<p>如果约束条件中引用了下层的子外连接的 Nullable-side 的表，这种约束条件也不能应用于提取新的约束条件。例如 SQL 语句： EXPLAIN SELECT * FROM SCORE LEFT JOIN (STUDENT FULL JOIN COURSE ON TRUE) sc ON (SCORE.sno = 1 AND sc.sno = 1) OR (SCORE.sno = 2 AND sc.sno = 2) AND sc.sname IS NULL AND sc.cname IS NULL。</p>
<h3 id="-2">选择率需要修正</h3>
<p>这里我们要讨论一些“超纲”的知识，因为我们还没有完整地介绍过选择率，读者可以先去查阅《第14课：选择率》，然后再返回来看这部分内容。</p>
<p>约束条件改变，选择率的估算就会发生变化，但这种变化显然是没有“道理”的，因为我们新添加的约束条件是从原来的约束条件中衍生出来的。例如，对于约束条件 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics'))，它本来是应用在 STUDENT 表和 COURSE 表的连接结果之上的，对于这样一个约束条件的选择率是 P((sno=1 AND cname='math') OR (sno=2 AND cname='physics'))。</p>
<p>这个选择率的都是基于 STUDENT 表的统计信息和 COURSE 表的统计信息进行计算的，而这些统计信息又是基于整个表的数据经过采样和统计分析获得的，也就是说，上面的选择率计算是基于 STUDENT 表和 COURSE 表的全体数据进行的。</p>
<p>假如这时候提取出新的约束条件 sno = 1 OR sno = 2，这个约束条件就会先对 STUDENT 表进行一次过滤，过滤产生的结果用于和 COURSE 表做连接，那么 P((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) 中基于 STUDENT 全部数据计算的选择率就不再准确了（因为过滤导致 STUDENT 表变小了），这时候就需要调整 P((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) 的选择率。</p>
<p>假设基表 STUDENT 中有 m 条数据，基表 COURSE 中有 n 条数据，那么在没有增加新的约束条件时，估算最终产生的结果数量为：</p>
<pre><code>m × n × P((sno=1 AND cname='math') OR (sno=2 AND cname='physics'))
</code></pre>
<p>STUDENT 表经过约束条件 sno = 1 OR sno = 2 过滤后产生的结果数量为：</p>
<pre><code>m × P(sno = 1 OR sno = 2)
</code></pre>
<p>如果我们不对选择率修正，新加约束条件之后，连接产生的结果数量为：</p>
<pre><code>m × P(sno = 1 OR sno = 2) × n × P((sno=1 AND cname='math') OR (sno=2 AND cname='physics'))
</code></pre>
<p>那么我们可以在新增加约束条件之后做如下修正：</p>
<pre><code>m × P(sno = 1 OR sno = 2) × n × [P((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) / P(sno = 1 OR sno = 2)]
</code></pre>
<p>也就是说在增加新的约束条件之后，约束条件 ((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) 的选择率应该修正为：</p>
<pre><code>P((sno=1 AND cname='math') OR (sno=2 AND cname='physics')) / P(sno = 1 OR sno = 2)
</code></pre>
<h3 id="-3">小结</h3>
<p>在 PostgreSQL 早期的版本中，对于合取范式和析取范式的处理还是比较多的，但后来发现处理半天浪费时间却收效甚微，后来经过一次比较大的改动之后，对表达式的处理就简化了。因此，PostgreSQL 目前对表达式的优化偏弱，这是需要改进的地方。</p></div></article>