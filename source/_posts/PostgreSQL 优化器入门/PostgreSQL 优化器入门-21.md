---
title: PostgreSQL 优化器入门-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在介绍具体的代价计算之前，我们先来认识一下启动代价和整体代价。</p>
<h3 id="">启动代价和整体代价</h3>
<p>我们在前面的课程已经简要介绍了启动代价，那为什么要区分启动代价和整体代价呢？我们通过一个示例来说明。</p>
<pre><code>postgres=# CREATE INDEX TEST_A_A_IDX ON TEST_A(a);
CREATE INDEX

postgres=# INSERT INTO TEST_A SELECT GENERATE_SERIES(1,10000),FLOOR(RANDOM()*100), FLOOR(RANDOM()*100), FLOOR(RANDOM()*100);
INSERT 0 10000

postgres=# ANALYZE TEST_A;
ANALYZE

postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 1 ORDER BY a;
                            QUERY PLAN
-------------------------------------------------------------------
 Sort  (cost=844.39..869.39 rows=10000 width=16)
   Sort Key: a
   -&gt;  Seq Scan on test_a  (cost=0.00..180.00 rows=10000 width=16)
         Filter: (a &gt; 1)
(4 rows)
</code></pre>
<p>从示例 SQL 语句可以看出，SQL 语句要求查询的结果有序（ORDER BY a）。我们已知属性 a 上有 B 树索引，而 B 树索引是有序的，所以索引扫描（IndexScan）是一个好选择。但是从示例的查询计划可以看出它没有选择 IndexScan，反而选择了顺序扫描（SeqScan）+ 排序（Sort）的方式，这是由于 a &gt; 1 的选择率比较高，导致索引扫描（IndexScan）产生的随机读比较多，页面的 IO 代价中随机 IO 的代价远高于顺序 IO 的代价。</p>
<pre><code>--禁用 SeqScan
postgres=# SET ENABLE_SEQSCAN=FALSE;
SET
postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 1 ORDER BY A;
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Index Scan using test_a_a_idx on test_a  (cost=0.29..7373.28 rows=10000 width=16)
   Index Cond: (a &gt; 1)
(2 rows)
</code></pre>
<p>从示例的执行计划可以看出，禁用 SeqScan 扫描之后，执行计划变成了对 B 树索引进行扫描，索引扫描的代价是 7373.28。而顺序扫描（SeqScan）+ 排序（Sort）方式的总代价是 869.39，因此我们说查询优化器的选择是正确的。同时还注意到，顺序扫描（SeqScan）+ 排序（Sort）的方式的启动代价是 844.39，而 IndexScan 的启动代价是 0.29，也就是说 SeqScan + Sort 方式的启动代价高于 IndexScan。</p>
<p>如果给 SQL 语句增加 LIMIT 子句：</p>
<pre><code>SELECT * FROM TEST_A WHERE a &gt; 1 ORDER BY a LIMIT 1;
</code></pre>
<p>这时就会出现一个问题，LIMIT 子句处在执行计划的上层，优化器在对顺序扫描/索引扫描进行代价估算的时候，是不知道上层有没有 LIMIT 结点的。假如查询优化器仍然会选择 SeqScan + Sort 这样的启动代价比较高的路径作为子路径，然后形成 SeqScan + Sort + Limit 这样的路径，这就不合理了。由于子句 LIMIT 1 的出现，之前放弃的 IndexScan 就有了优势。虽然 IndexScan 会出现大量的随机 IO，但是 LIMIT 1 子句限制了随机 IO 的数量，IndexScan 不用再扫描整个索引了，只需要从索引获取一条元组，也就是说这时候随机 IO 只有一次。这时候，IndexScan 这种启动代价比较低的路径的优势就凸显出来了。下面来分别看一下加上 Limit 子句之后，两种执行计划的表现。</p>
<pre><code>postgres=# SET ENABLE_SEQSCAN=TRUE;
SET
postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 1 ORDER BY a LIMIT 1;
                                       QUERY PLAN
-------------------------------------------------------------------------
 Limit  (cost=0.29..0.32 rows=1 width=16)
   -&gt;  Index Scan using test_a_a_idx on test_a  
         Index Cond: (a &gt; 1)
(3 rows)

postgres=# SET ENABLE_INDEXSCAN=FALSE;
SET
postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 1 ORDER BY a LIMIT 1;
                               QUERY PLAN
-------------------------------------------------------------------------
 Limit  (cost=230.00..230.00 rows=1 width=16)
   -&gt;  Sort  (cost=230.00..255.00 rows=10000 width=16)
         Sort Key: a
         -&gt;  Seq Scan on test_a  (cost=0.00..180.00 rows=10000 width=16)
               Filter: (a &gt; 1)
(5 rows)
</code></pre>
<p>从示例中可以看出，加上了 LIMIT 1 子句之后，查询优化器选择了启动代价比较低的 IndexScan.IndexScan 的启动代价是 0.29，而 SeqScan+ Sort 的启动代价是 230.00（注意，如果没有 LIMIT 1 子句，SeqScan + Sort 的启动代价是 844.39。这个示例的启动代价是 230.00 的原因是：查询优化器在计算代价的时候对 LIMIT 1 这种情况做了优化，对于带有 LIMIT 子句的语句，它可能会采用基于 TOP-K 的堆排序，这样就能降低排序所带来的启动代价）。</p>
<h3 id="-1">连接操作的代价</h3>
<p>PostgreSQL 对连接操作提供了 3 种实现方法，分别是嵌套循环连接（Nested Loop Join）、哈希连接（Hash Join）、归并连接（Merge Join），这里我们以哈希连接为例来算一下代价。</p>
<p>假设有如下的表以及内容：</p>
<pre><code>CREATE TABLE STUDENT(sno INT PRIMARY KEY, sname VARCHAR(10), ssex INT);
CREATE TABLE SCORE(sno INT, cno INT, score INT);
INSERT INTO STUDENT SELECT i, repeat('A', i%5 + 1), i%2 FROM GENERATE_SERIES(1,10000) i;
ANALYZE STUDENT;
INSERT INTO SCORE SELECT i, i%5, RANDOM() * 100 FROM GENERATE_SERIES(1,10000) i;
ANALYZE SCORE;
</code></pre>
<p>结合上面的数据，会有下面的执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT st, SCORE sc WHERE st.sno = sc.sno;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 Hash Join  (cost=280.00..561.24 rows=10000 width=24)
   Hash Cond: (sc.sno = st.sno)
   -&gt;  Seq Scan on score sc  (cost=0.00..155.00 rows=10000 width=12)
   -&gt;  Hash  (cost=155.00..155.00 rows=10000 width=12)
         -&gt;  Seq Scan on student st  (cost=0.00..155.00 rows=10000 width=12)
(5 rows)
</code></pre>
<p>看到这个执行计划中的代价计算你是否会有一个疑问，创建 Hash 表的过程竟然没有计算代价，它的代价就是它的子结点 Seq Scan on student st 的代价：</p>
<pre><code>   -&gt;  Hash  (cost=155.00..155.00 rows=10000 width=12)
         -&gt;  Seq Scan on student st  (cost=0.00..155.00 rows=10000 width=12)
</code></pre>
<p>实际上这里的代价是不准的，当我们决定是否选择哈希连接这样的连接方法时，优化器认为这是一个路径，这个路径是成百上千路径中的一个：</p>
<pre><code>Hash Join Path
    -&gt; Seq Scan Path on score sc
    -&gt; Seq Scan Path on student st
</code></pre>
<p>如果最终发现这个哈希连接路径在成百上千的路径中代价最低，就确定选择这个路径了。然后就把路径转换成 Plan，在转换的过程中，就会在内表上增加一个建立哈希表的新结点：</p>
<pre><code>Hash Join Plan
    -&gt; Seq Scan Plan on score sc
    -&gt; Create Hash Table
        -&gt; Seq Scan Plan on student st
</code></pre>
<p>由于在挑选路径的时候把所有的代价都自 Hash Join Plan 里计算完了，但是没有做好区分，所以增加新的 Hash 表结点的时候就简单地把它的代价认为是下层的 Seq Scan on student st 的代价了。</p>
<p>对于执行计划中的两个 SeqScan 的代价，我们就不详细追究了，因为我们已经带领大家计算过 SeqScan 的代价，现在我们把目光转向哈希连接的代价计算。</p>
<p>我们先关注哈希连接中启动代价的计算，大家已经知道了启动代价是返回第一条元组之前的代价，那么哈希连接在返回第一条元组之前要干点啥呢？</p>
<pre><code>* 创建 Hash 表的代价一定是启动代价
* 因为 STUDENT 表的扫描在创建 Hash 表之前，所以也一定是启动代价 = 155
* SCORE 表的启动代价也应该算到 Hash Join 的启动代价里 = 0
</code></pre>
<p>我们分别来算一下这些代价：<br />
创建 Hash 表的过程是对内表的每条元组计算 Hash 值，然后插入到 Hash 表对应的桶中，那么：</p>
<pre><code>计算 Hash 的值使用的是 cpu_operator_cost = 0.0025
每个元组要插入到 Hash 表中的代价用 cpu_tuple_cost = 0.01 来计算
内表的元组一共有 10000 行

postgres=# show cpu_operator_cost ;
 cpu_operator_cost
-------------------
 0.0025
(1 row)

postgres=# postgres=# sho_cost;
 cpu_tuple_cost
----------------
 0.01
(1 row)

建立 Hash 表的代价 =（0.0025 + 0.01 ）* 10000 = 125
</code></pre>
<p>因此执行计划的启动代价为 155 + 125 = 280。
注：这里的模型已经做了简化，例如上层如果有过滤条件，则需要计算过滤条件是否会产生启动代价，我们当前的示例中没有这种情况。</p>
<p>有了启动代价之后，我们来看一下哈希连接的执行代价：</p>
<pre><code>* 外表的每个元组都要去 hash 表做探测
    = cpu_operator_cost * 10000 = 25
* 外表的每个元组要有哈希条件的计算：
    = cpu_operator_cost * 10000 = 25
    但是这里只增加一半，也就是 12.5，原因是：
    假如有 n 个哈希条件，每个元组可能并不需要把所有的哈希条件都计算一次，
    如果在前面发现有不匹配的哈希条件，就终止计算了，
    所以 PostgreSQL 选择只计入一半的代价
* 通过 Hash 探测的元组我们仍然需要给他计算代价
    = cpu_tuple_cost * 10000 = 100
* 外表的扫描代价也是执行代价 = 155

因此执行代价 = 25 + 12.5 + 100 + 155 = 292.5

整个执行计划的总代价 = 292.5 + 280 = 582.5
</code></pre>
<p>你可能会发现我们计算的代价和执行计划中展示的有些差别：执行计划中哈希连接的代价是 561.24，这是因为我们采用的是常规的方法来计算 Hash 表执行的代价；但是如果内表是 STUDENT 的话，因为 STUDENT 表上有主键索引，而主键索引具有唯一性，这种唯一性的特点对代价计算具有提示作用，所以结合唯一性的特点计算的代价会小一些。</p>
<h3 id="nonspj">Non-SPJ 代价计算</h3>
<p>在 SQL 语句中，我们常常使用一些聚集函数，我们来看一个和聚集函数相关的执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT MAX(sno) FROM STUDENT;
                                                  QUERY PLAN
--------------------------------------------------------------------------------------------------------------
 Result  (cost=0.32..0.33 rows=1 width=4)
   InitPlan 1 (returns $0)
     -&gt;  Limit  (cost=0.29..0.32 rows=1 width=4)
           -&gt;  Index Only Scan Backward using student_pkey on student  (cost=0.29..353.29 rows=10000 width=4)
                 Index Cond: (sno IS NOT NULL)
(5 rows)
</code></pre>
<p>本来我们想查看和聚集相关的执行计划，但是优化器“自作聪明”地给我们做了优化，由于在 STUDENT.sno 这个列上有主键索引，而主键索引是基于 B 树实现的，因而可能很容易地从 B 树中找到 sno 的最大值，也就是说 PostgreSQL 的优化器把聚集函数等价变换成了：</p>
<pre><code>-- 由于 MAX 聚集函数要获得的是最大值，因此需要采用前向扫描
SELECT sno FROM STUDENT_PKEY LIMIT 1;
</code></pre>
<p>这种执行计划对我们计算聚集函数的代价没什么帮助，我们尝试把索引扫描给禁止掉，然后就获得了如下的执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT MAX(sno) FROM STUDENT;
                            QUERY PLAN
-------------------------------------------------------------------
 Aggregate  (cost=180.00..180.01 rows=1 width=4)
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=4)
(2 rows)
</code></pre>
<p>优化器会先生成 SeqScan 路径，然后在 SeqScan 路径的基础上再叠加上聚集操作，这种聚集函数的代价计算比较简单。需要注意的是它的启动代价实际上就是总代价，也就是说要返回第一条元组，必须在把所有的元组扫描一遍之后才能找到最大值。</p>
<pre><code>postgres=# show cpu_operator_cost ;
 cpu_operator_cost
-------------------
 0.0025
(1 row)

代价 = 0.0025 * 10000 条记录 = 25
总代价 = 155（扫描路径的代价） + 25 = 180
</code></pre>
<h3 id="-2">小结</h3>
<p>虽然我们分别尝试计算了各种物理路径的代价，但实际上这样计算代价并没有可实践性，如果换一个执行计划，我相信读者很难精准地计算出和执行计划一样的代价。但是通过分别计算这些代价，我们可以大概了解 PostgreSQL 的优化器是如何对一个执行算子计算代价的，并且可以对各种代价基准因子有一个比较深刻的认识，这样我们的目的就达到了。</p></div></article>