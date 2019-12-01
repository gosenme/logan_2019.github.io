---
title: PostgreSQL 优化器入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>外连接是查询优化中的搅屎棍，在查询优化器的实现过程中，很多时间都消耗在和外连接做斗争。我们从《第4课：谓词下推》和《第5课：连接顺序交换规则》可以看出，外连接的出现对提高优化器的实现难度“功不可没”。例如，对约束条件进行下推（谓词下推）时，如果连接操作是外连接，那么有些约束条件下推就可能会受到阻碍。在连接顺序交换时，内连接的表之间的连接顺序交换比较灵活，而外连接不能随意地交换连接表的顺序。因此，如果能将外连接转换成内连接，查询优化的过程就会大大地简化。</p>
<h3 id="">外连接消除示例</h3>
<p>在介绍怎样才能消除一个外连接之前，让我们先来看一下内连接和外连接的区别。例如，两个表 STUDENT 和 SCORE 的数据如下，其中有一个学生 lisi 没有成绩。</p>
<pre><code>postgres=# SELECT * FROM STUDENT;
 sno     |  sname    | ssex
-----+----------+------
   1     | zhangsan  |    1
   2     | lisi      |    1
(2 rows)

postgres=# SELECT * FROM SCORE;
 sno     | cno   | degree
-----+-----+--------
   1     |   1   |     36
(1 row)
</code></pre>
<p>如果要查询学生的姓名和成绩，可以对 STUDENT 和 SCORE 做连接。从查询结果可以看出，内连接只显示了有成绩的学生，而外连接则对没有成绩的学生补了 NULL 值，也就是说这个外连接是不能转换成内连接的。</p>
<pre><code>postgres=# SELECT * FROM STUDENT LEFT JOIN SCORE ON STUDENT.sno = SCORE.sno;
 sno     |  sname    | ssex | sno    | cno   | degree
-----+----------    +------+-----+-----+--------
   1     | zhangsan  |    1  |   1   |   1   |     36
   2     | lisi      |    1  |       |       |
(2 rows)

postgres=# SELECT * FROM STUDENT INNER JOIN SCORE ON STUDENT.sno = SCORE.sno;
 sno     |  sname    | ssex  | sno | cno | degree
-----+----------    +-----  +-----+-----+--------
   1     | zhangsan  |    1  |   1   |   1   |     36
(1 row)
</code></pre>
<p>假如我们再增加一个 WHERE 条件，形成下面这样的语句，内连接的查询结果就和外连接的查询结果相同了。</p>
<pre><code>postgres=# SELECT * FROM STUDENT LEFT JOIN SCORE ON STUDENT.sno = SCORE.sno WHERE cno IS NOT NULL;
 sno     |  sname    | ssex  | sno | cno     | degree
-----+----------+------+-----+-----    +--------
   1     | zhangsan  |    1  |   1   |   1   |     36
(1 row)

postgres=# SELECT * FROM STUDENT INNER JOIN SCORE ON STUDENT.sno = SCORE.sno WHERE cno IS NOT NULL;
 sno     |  sname    | ssex  | sno | cno     | degree
-----+----------+------+-----+-----    +--------
   1     | zhangsan  |    1  |   1   |   1   |     36
(1 row)
</code></pre>
<h3 id="-1">严格的表达式</h3>
<p>“WHERE cno IS NOT NULL” 这样的条件可以让外连接和内连接的结果相同，因为这个约束条件是“严格”（strict）的。“严格”的精确定义是，对于一个表达式，如果输入参数是 NULL 值，那么输出也一定是 NULL 值，就可以说这个表达式是严格的。</p>
<p>从 SQL 语义的角度出发，对于一个表达式，如果输入参数是 NULL 值，输出结果是 NULL 值或者 FALSE，那么就可以认为这个表达式是严格的。如果在约束条件里有这种严格的表达式，由于输入是 NULL 值，输出是 NULL 值或者 FALSE，那么含有 NULL 值的元组就会被过滤掉。</p>
<p>可以通过如下方法来判断一个表达式是否严格：</p>
<ul>
<li>对于函数而言，在 PG_PROC 系统表中的 proisstrict 列属性代表了当前函数是否严格；</li>
<li>如果是操作符表达式，在 PostgreSQL 数据库中操作符实际都转成了对应的函数，因此也可以用 proisstrict 来表示是否严格；</li>
<li>对基于 IS [NOT] NULL 产生的 NullTest 表达式需要单独处理，其中 IS NOT NULL 是严格的，IS NULL 是不严格的。</li>
</ul>
<p>给定一个表达式，可以对表达式进行递归遍历。如果满足上面的 3 种情况，那么这个表达式也是严格的，例如我们常见的约束条件 a &gt; 1，它实际上就是一个表达式，那么这个表达式是否严格呢？我们可以先看一下 "&gt;" 这个操作符对应的是哪个函数，这个函数是否是严格的：</p>
<pre><code>postgres=# SELECT oid, typname FROM PG_TYPE WHERE typname='int4';
 oid | typname
-----+---------
  23 | int4
(1 row)

postgres=# SELECT oprname, oprcode FROM PG_OPERATOR WHERE oprname = '&gt;' AND oprright = 23 AND oprleft = 23;;
 oprname | oprcode
---------+---------
 &gt;       | int4gt
(1 row)

postgres=# SELECT proname, proisstrict FROM PG_PROC WHERE proname = 'int4gt';
 proname | proisstrict
---------+-------------
 int4gt  | t
(1 row)

注：proisstrict 是 true， 代表这个表达式是严格的
</code></pre>
<h3 id="-2">外连接的消除</h3>
<p>“WHERE cno IS NOT NULL” 这样的约束条件，如果输入的 cno 是 NULL 值，这个约束条件返回的是 FALSE，也满足了广义的“严格”定义。而且 cno 又处于左连接的 Nullable-side，所以对于补充的 NULL 值又能起到过滤的作用，因此它可以使内连接和外连接的查询结果相同。根据这一点，我们可以得到一个外连接消除的必要条件：</p>
<ul>
<li>上层有“严格”的约束条件</li>
<li>约束条件中引用了 Nullable-side 的表</li>
</ul>
<p>需要注意“上层”两个字，所谓的上层是指这个约束条件不是当前的连接条件，而是上层的连接条件或者过滤条件，例如有 SQL 语句：</p>
<pre><code>SELECT * FROM STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) ON COURSE.cno IS NOT NULL，
</code></pre>
<p>其中约束条件（或者连接条件）“ON COURSE.cno IS NOT NULL” 处在 (SCORE LEFT JOIN COURSE ON TRUE) 的上层，它能对 (SCORE LEFT JOIN COURSE ON TRUE) 这个外连接的消除起作用，但是不能对 STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) 的消除起到作用。它们的层次下图所示，例句的执行计划如下：</p>
<div style="text-align:center">
<img src="http://file.ituring.com.cn/Original/18100374966db1844b6c" width="500px" /></div>
<p></br></p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) ON COURSE.cno IS NOT NULL;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..132.48 rows=7658 width=69)
   -&gt;  Seq Scan on student  (cost=0.00..1.07 rows=7 width=11)
   -&gt;  Materialize  (cost=0.00..38.42 rows=1094 width=58)
         -&gt;  Nested Loop  (cost=0.00..32.95 rows=1094 width=58)
               -&gt;  Seq Scan on score  (cost=0.00..1.01 rows=1 width=12)
               -&gt;  Seq Scan on course  (cost=0.00..21.00 rows=1094 width=46)
                     Filter: (cno IS NOT NULL)
(7 rows)
</code></pre>
<p>从执行计划可以看出 (SCORE LEFT JOIN COURSE ON TRUE) 的左连接已经被消除了，但是 STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) 的左连接仍然存在。</p>
<p>再看另一个例句：</p>
<pre><code>SELECT * FROM STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) ON TRUE WHERE COURSE.cno IS NOT NULL;
</code></pre>
<div style="text-align:center">
<img src="http://file.ituring.com.cn/Original/1810a652072e312f6e26" width="500px" /></div>
<p></br></p>
<p>它的结构图如上图所示，可以看到约束条件（或者过滤条件）“WHERE COURSE.cno IS NOT NULL”可以作用于顶层的连接，查看它的查询计划可以看出，语句中的左外连接被消除了。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT LEFT JOIN (SCORE LEFT JOIN COURSE ON TRUE) ON TRUE WHERE COURSE.cno IS NOT NULL;
                                QUERY PLAN
--------------------------------------------------------------------------
 Nested Loop  (cost=0.00..118.89 rows=7658 width=69)
   -&gt;  Seq Scan on course  (cost=0.00..21.00 rows=1094 width=46)
         Filter: (cno IS NOT NULL)
   -&gt;  Materialize  (cost=0.00..2.19 rows=7 width=23)
         -&gt;  Nested Loop  (cost=0.00..2.15 rows=7 width=23)
               -&gt;  Seq Scan on score  (cost=0.00..1.01 rows=1 width=12)
               -&gt;  Seq Scan on student  (cost=0.00..1.07 rows=7 width=11)
(7 rows)
</code></pre>
<h3 id="-3">左外连接等价变换为反连接</h3>
<p>而 IS NULL 这样不严格的表达式对我们也是有用的。例如，对于左连接而言，Nonnullable-side 没有连接上的元组会在 Nullable-side 补 NULL 值显示出来。而所谓的“没有连接上的元组”，恰好是 AntiJoin 所需要的，因此就带来了将左连接（LeftJoin）转换成反连接（AntiJoin）的可能性，这种可能性的前提是：</p>
<ul>
<li>当前层次的连接条件必须是严格的；</li>
<li>上层的约束条件和当前层的连接条件都引用了 Nullable-side 表的同一列；</li>
<li>上层的约束条件强制 Nullable-side 产生的结果必须是 NULL。</li>
</ul>
<p>来看一个这样的示例：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT LEFT JOIN SCORE ON STUDENT.sno = SCORE.sno WHERE SCORE.sno IS NULL;
                            QUERY PLAN
------------------------------------------------------------------
 Nested Loop Anti Join  (cost=0.00..2.19 rows=6 width=23)
   Join Filter: (student.sno = score.sno)
   -&gt;  Seq Scan on student  (cost=0.00..1.07 rows=7 width=11)
   -&gt;  Materialize  (cost=0.00..1.01 rows=1 width=12)
         -&gt;  Seq Scan on score  (cost=0.00..1.01 rows=1 width=12)
(5 rows) 
</code></pre>
<p>从示例中可以看出，左连接被转换成了反连接，这是因为：连接条件 STUDENT.sno = SCORE.sno 是严格的。这保证了在 Nullable-side 的表中如果本身就含有 NULL 值，这些元组会被连接条件筛选掉。另外，约束条件 SCORE.sno IS NULL 是上层的不严格的约束条件，这就保证了在外连接操作之后，约束条件 SCORE.sno IS NULL 会把 Nullable-side 补的 NULL 值的元组保留下来。这样的操作结果和 Anti Join 的结果应该是一致的，也就是说通过连接条件 STUDENT.sno = SCORE.sno 筛选掉了表中本来就有的 NULL 值，通过 SCORE.sno IS NULL 保留了外连接补的 NULL 值。</p>
<h3 id="-4">小结</h3>
<p>外连接消除共做了 3 件事：</p>
<ul>
<li>将外连接等价转换为内连接</li>
<li>将外连接等价转换为反连接</li>
<li>将逻辑的右外连接转换为逻辑的左外连接，也就是交换顺序</li>
</ul></div></article>