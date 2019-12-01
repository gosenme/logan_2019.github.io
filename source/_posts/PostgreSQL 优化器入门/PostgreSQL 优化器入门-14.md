---
title: PostgreSQL 优化器入门-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>目前已经比较着重地介绍过子连接和子查询的提升、表达式的规范化、外连接的消除、等价推理、连接顺序交换、谓词下推等逻辑优化方法，实际上，PostgreSQL 还做了很多逻辑优化，我们把这些优化在这一课做一个汇总。</p>
<h3 id="having">Having 子句的优化</h3>
<p>在 Having 子句中，有些约束条件是可以转变为过滤条件的。这里对 Having 子句中的约束条件进行了拆分，从下面的示例可以看出，c &gt; 0 这个约束条件已经变成了 TEST_A 表扫描路径上的过滤条件，而 SUM(a) &gt; 100 这个约束条件则保留在了原来的位置。</p>
<pre><code>postgres=# EXPLAIN SELECT SUM(a),b,c FROM TEST_A WHERE b &gt; 0 GROUP BY b,c HAVING SUM(a) &gt; 100 AND c &gt; 0;
                          QUERY PLAN
---------------------------------------------------------------
 HashAggregate  (cost=3.50..4.75 rows=33 width=16)
   Group Key: b, c
   Filter: (sum(a) &gt; 100)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.50 rows=100 width=12)
         Filter: ((b &gt; 0) AND (c &gt; 0))
(5 rows)
</code></pre>
<h3 id="groupby">Group By 键值化简</h3>
<p>Group By 子句的实现需要借助排序或者哈希来实现，如果能减少 Group By 后面的字段，就能降低排序或者哈希带来的损耗。</p>
<p>对于一个有主键（Primary Key）的表，如果 Group By 的字段包含了主键的所有键值，实际上这个主键已经能够表示当前的结果就是符合分组的，因此可以将主键之外的字段去掉。例如，对于 SQL 语句：SELECT * FROM STUDENT GROUP BY sno, sname,ssex，因为 sno 属性上有一个主键索引，所以 Group By 子句中的 sname 和 ssex 可以被去除掉。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT GROUP BY sno, sname, ssex;
                          QUERY PLAN
--------------------------------------------------------------
 HashAggregate  (cost=1.09..1.16 rows=7 width=11)
   Group Key: sno
   -&gt;  Seq Scan on student  (cost=0.00..1.07 rows=7 width=11)
(3 rows)
</code></pre>
<p>上面的示例是单表的扫描路径，连接路径也可以用同样的方式简化 Group By 子句。无论是连接操作的 LHS 还是 RHS，只要 Group By 包含了表上的全部主键，那么主键键值之外的 Group By 字段就能被消除掉。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT LEFT JOIN COURSE ON TRUE GROUP BY sno,sname,ssex,cno,cname;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 HashAggregate  (cost=159.57..236.57 rows=7700 width=57)
   Group Key: student.sno, course.cno
   -&gt;  Nested Loop Left Join  (cost=0.00..121.07 rows=7700 width=57)
         -&gt;  Seq Scan on student  (cost=0.00..1.07 rows=7 width=11)
         -&gt;  Materialize  (cost=0.00..26.50 rows=1100 width=46)
               -&gt;  Seq Scan on course  (cost=0.00..21.00 rows=1100 width=46)
(6 rows)
</code></pre>
<h3 id="">无用连接项消除</h3>
<p>数据库在生成连接路径的时候，需要考虑所有的表之间的连接路径。如果能消除掉其中的一些表，那么势必能够降低物理路径的搜索空间，从而提高查询优化的运行效率。例如，有这样一种情况：</p>
<pre><code>postgres=# CREATE UNIQUE INDEX TEST_B_U_IDX ON TEST_B(a);
CREATE INDEX
postgres=# EXPLAIN SELECT TEST_A.a FROM TEST_A LEFT JOIN TEST_B ON TEST_A.a = TEST_B.a;
                       QUERY PLAN
--------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=4)
(1 row)
</code></pre>
<p>SQL 语句中原本是针对 TEST_A 表和 TEST_B 表的外连接，在示例的执行计划中却显示只有一个扫描路径，其中的连接项 TEST_B 被消除掉了。那么，什么样的连接项才能被消除掉呢？它需要满足以下几个条件：</p>
<ul>
<li>必须是左连接（注意这时候已经没有右连接了，在消除外连接的时候把所有的右连接已经转换成了左连接），且内表是普通的表</li>
<li>除了当前连接中，其他位置不能出现内表的任何列</li>
<li>连接条件中内表的列具有唯一性</li>
</ul>
<p>分析示例中的 SQL 语句可以发现，TEST_A 表和 TEST_B 表需要做左连接操作。除了连接条件 TEST_A.a = TEST_B.a 之外，语句的其他地方没有引用 TEST_B 表中的任何列，连接条件中的 TEST_B.a 上有唯一索引，具有唯一性，而且 TEST_B.a 是内表的列，因此 TEST_B 表作为无用的连接项被消除掉了。</p>
<h3 id="-1">半连接消除</h3>
<p>半连接的本质是对于外表（也就是 LHS）的每一条元组，如果在内表（也就是 RHS）的表中找到一条符合连接条件的元组，就表示连接成功，即使内表中有多个符合连接条件的元组，也只匹配一条。</p>
<p>如果内表能保证唯一性，半连接的连接结果就可以和内连接相同了。这种情况下，可以将半连接消除，转换为内连接。例如，对于具有 DISTINCT 属性的内表，就可以将半连接转换为内连接。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a = ANY (SELECT DISTINCT a FROM TEST_B);
                                 QUERY PLAN
----------------------------------------------------------------------------
 Hash Join  (cost=93.25..145.10 rows=1850 width=16)
   Hash Cond: (test_a.a = test_b.a)
   -&gt;  Seq Scan on test_a  (cost=0.00..28.50 rows=1850 width=16)
   -&gt;  Hash  (cost=70.13..70.13 rows=1850 width=4)
         -&gt;  HashAggregate  (cost=33.13..51.63 rows=1850 width=4)
               Group Key: test_b.a
               -&gt;  Seq Scan on test_b  (cost=0.00..28.50 rows=1850 width=4)
(7 rows)
</code></pre>
<h3 id="minmax">MIN/MAX 优化</h3>
<p>因为 B 树索引是有序的，如果要获取某一列的最大值或者最小值，同时这一列是 B 树索引的键值，那么可以借用索引来获取最大值，例如：</p>
<pre><code>postgres=# CREATE INDEX TEST_A_A_IDX ON TEST_A(a);
postgres=# CREATE INDEX TEST_A_B_IDX ON TEST_A(b);
postgres=# EXPLAIN SELECT MAX(a), MIN(b) FROM TEST_A WHERE c &gt; 1;
                                              QUERY PLAN
------------------------------------------------------------------------------------
 Result  (cost=0.66..0.67 rows=1 width=8)
   InitPlan 1 (returns $0)
     -&gt;  Limit  (cost=0.29..0.32 rows=1 width=4)
           -&gt;  Index Scan Backward using test_a_a_idx on test_a  
                 Index Cond: (a IS NOT NULL)
                 Filter: (c &gt; 1)
   InitPlan 2 (returns $1)
     -&gt;  Limit  (cost=0.29..0.34 rows=1 width=4)
           -&gt;  Index Scan using test_a_b_idx on test_a test_a_1  
                 Index Cond: (b IS NOT NULL)
                 Filter: (c &gt; 1)
(11 rows)
</code></pre>
<p>从执行计划可以看出针对每个 MAX/MIN 聚集函数增加了一个对应的子 Plan，这个子 Plan 是在 build_minmax_path 函数中创建的，子 Plan 是基于如下 SQL 语句生成的：</p>
<pre><code>SELECT col FROM tab
    WHERE col IS NOT NULL AND existing-quals
    ORDER BY col ASC/DESC
    LIMIT 1;
</code></pre>
<p>判断 MIN/MAX 优化能否适用的条件是比较严格的，主要有如下几个：</p>
<ul>
<li>只能包含 MIN/MAX 聚集函数，语句中不能有其他聚集函数；</li>
<li>如果是多个表连接的情况，不适用 MIM/MAX 优化；</li>
<li>查询中不能包含 Group By 子句，因为创建了分组之后就无法借用索引获得 MIN/MAX 值；</li>
<li>语句中不能包含 CTE 表达式；</li>
<li>如果 MIN/MAX 对应的列上没有 B 树索引，也不适用这种优化方式。</li>
</ul>
<h3 id="-2">子执行计划剪枝</h3>
<p>我们已经知道执行计划是一棵二叉树，在这个二叉树中，一旦其中的一个结点已经确定不会返回任何结果，那么实际上就可以考虑将这个子树剪掉。</p>
<p>如果连接方式是内连接（Inner Join），并且内表、外表或者约束条件中有常量 false，则连接子树可以被剪枝。从示例的执行计划可以看出，这个语句由于子查询中有一个“2&gt;3”的约束条件，导致连接的 LHS 端不可能有结果，也就导致了整个执行计划都不会产生执行结果。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM (SELECT * FROM TEST_A WHERE 2&gt;3) ta INNER JOIN TEST_B ON TRUE;
                QUERY PLAN
-------------------------------------------
 Result  (cost=0.00..0.00 rows=0 width=32)
   One-Time Filter: false
(2 rows)
</code></pre>
<p>如果连接方式是左连接（Left Join），并且外表有常量 false 的约束条件，整个连接子树可以被剪枝。从执行计划可以看出，不但子查询被剪掉，它的内表 TEST_B 也被剪掉了：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM (SELECT * FROM TEST_A WHERE 2&gt;3) ta LEFT JOIN TEST_B ON TRUE;
                QUERY PLAN
-------------------------------------------
 Result  (cost=0.00..0.00 rows=0 width=32)
   One-Time Filter: false
(2 rows)
</code></pre>
<p>另外，如果左连接的内表是虚表或者有常量 false 的约束条件，可以将内表进行剪枝，但是外表必须保留：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN (SELECT * FROM TEST_B WHERE 2&gt;3) tb ON TRUE;
                              QUERY PLAN
----------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..19979.64 rows=786432 width=16)
   -&gt;  Seq Scan on test_a  (cost=0.00..12115.32 rows=786432 width=16)
   -&gt;  Result  (cost=0.00..0.00 rows=0 width=0)
         One-Time Filter: false
(4 rows)
</code></pre>
<p>如果连接方式是全连接（Full Join），且全连接两端的子查询都可以被剪枝，则整个全连接就可以被剪枝：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM (SELECT * FROM TEST_A WHERE 2&gt;3) ta FULL JOIN (SELECT * FROM TEST_B WHERE 3 &gt;4) tb ON TRUE;
                QUERY PLAN
-------------------------------------------
 Result  (cost=0.00..0.00 rows=0 width=32)
   One-Time Filter: false
(2 rows)
</code></pre>
<p>如果连接方式是半连接（Semi Join），这种情况和内连接相似：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE (a,0) IN (SELECT a,2 FROM TEST_B);
                QUERY PLAN
-------------------------------------------
 Result  (cost=0.00..0.00 rows=0 width=16)
   One-Time Filter: false
(2 rows)
</code></pre>
<p>如果连接方式是反连接（Anti Join），这种情况和左连接相似：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE NOT EXISTS (SELECT a FROM TEST_B WHERE TEST_A.a &gt; TEST_B.a AND 2 &gt; 3);
                              QUERY PLAN
----------------------------------------------------------------------
 Nested Loop Anti Join  (cost=0.00..19979.64 rows=786432 width=16)
   Join Filter: false
   -&gt;  Seq Scan on test_a  (cost=0.00..12115.32 rows=786432 width=16)
   -&gt;  Result  (cost=0.00..0.00 rows=0 width=0)
         One-Time Filter: false
(5 rows)
</code></pre>
<h3 id="-3">小结</h3>
<p>到此为止，基于规则的优化（逻辑优化）就告一段落了。逻辑优化的部分实际上还有一些小优化，比如 UNION ALL 的拉平、连接 Var 的溯源等，这里就不再一一赘述了。在逻辑优化之后，就开始进入一个新的篇章——基于代价的优化（物理优化）。这部分优化主要是建立代价模型，从不同的角度尝试还原执行计划的执行步骤，按照执行步骤计算执行消耗，这样就可以在多个计划之间进行筛选。那么，现在就让我们去领略物理优化的精彩吧！</p></div></article>