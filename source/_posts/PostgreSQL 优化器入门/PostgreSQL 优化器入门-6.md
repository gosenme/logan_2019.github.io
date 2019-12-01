---
title: PostgreSQL 优化器入门-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过 EXPLAIN 查看了具体的执行计划之后，我们还能尝试影响优化器，让优化器生成我们想要的执行计划。不过，PostgreSQL 没有像 Oracle 那样通过在 SQL 语句中增加 HINT 信息的方式来影响执行计划的生成。但它也提供了一系列的 GUC 参数，比如在前面的课程中曾使用 enable_material 参数来尝试禁用 material，而且确实达到了禁用的效果。PostgreSQL 针对大部分算子都给出了具体的 GUC 参数，下面先把这些 GUC 参数列出来：</p>
<ul>
<li>enable_bitmapscan</li>
<li>enable_gathermerge</li>
<li>enable_hashagg </li>
<li>enable_hashjoin </li>
<li>enable_indexonlyscan </li>
<li>enable_indexscan </li>
<li>enable_material </li>
<li>enable_mergejoin </li>
<li>enable_nestloop </li>
<li>enable_parallel_append </li>
<li>enable_parallel_hash </li>
<li>enable_partitionwise_join </li>
<li>enable_seqscan </li>
<li>enable_sort </li>
<li>enable_tidscan </li>
</ul>
<p>每个 GUC 参数都可以通过下面的方式来设置：</p>
<pre><code>SET GUC_NAME = ON/OFF;
</code></pre>
<h3 id="">扫描路径的调整</h3>
<p>可以先来看一个最简单的情况：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &gt; 1000;
                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on student  (cost=0.00..180.00 rows=9000 width=12)
   Filter: (sno &gt; 1000)
(2 rows)

postgres=# set enable_seqscan = off;
SET

postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &gt; 1000;
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..318.79 rows=9000 width=12)
   Index Cond: (sno &gt; 1000)
(2 rows)
</code></pre>
<p>从执行计划可以看出，在禁止掉 Seq Scan 之后，优化器选择了通过索引扫描（Index Scan）来对数据进行访问。从两个执行算子的代价来看，索引扫描的代价确实要大于顺序扫描的代价，也就是说在没有禁用 Seq Scan 的时候，优化器对这两种路径是进行过对比的，最终选择了代价低的顺序扫描。</p>
<p>那么如果把索引扫描也禁用掉会如何呢？还可以通过位图扫描的方式来对数据进行访问，通过对比执行计划的代价，发现目前位图扫描的代价“高达” 345.53，在目前已经展示出来的扫描算子中是最高的。因此，如果不禁用 Seq Scan 和 Index Scan，优化器在面对 Bitmap Scan 时“虽然脸上笑嘻嘻，但心里 mmp”，是不可能选择位图扫描的。</p>
<pre><code>postgres=# set enable_indexscan = off;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &gt; 1000;
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Bitmap Heap Scan on student  (cost=178.03..345.53 rows=9000 width=12)
   Recheck Cond: (sno &gt; 1000)
   -&gt;  Bitmap Index Scan on student_pkey  (cost=0.00..175.78 rows=9000 width=0)
         Index Cond: (sno &gt; 1000)
(4 rows)
</code></pre>
<p>我们进一步追问，如果我们把位图扫描也禁用掉呢？从示例中可以看到，位图扫描关闭之后，执行计划最终又选择回了顺序扫描。</p>
<pre><code>postgres=# set enable_bitmapscan = off;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &gt; 1000;
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Seq Scan on student  (cost=10000000000.00..10000000180.00 rows=9000 width=12)
   Filter: (sno &gt; 1000)
(2 rows)
</code></pre>
<p>虽然我们关闭了顺序扫描，但 PostgreSQL 中的“关闭”（off）并不是真的把这种执行算子给禁止掉，而是选择在优化器内部进行代价估算的时候，提高这种类型执行算子的代价值，这样就能让优化器把这种类型的执行算子筛掉。PostgreSQL 对一个表的扫描路径通常只有 3 种类型——顺序扫描、索引扫描、位图扫描。如果我们把这些路径都完全禁止掉，那优化器就束手无策了，执行计划就生成不出来了。因此，通过增加代价值让优化器对执行路径进行筛选，一方面可以筛掉被禁用的路径，另一方面也可以让优化器在无路可走时柳暗花明。</p>
<h3 id="-1">连接路径的调整</h3>
<p>除了扫描算子，在优化器中还有很重要的 3 种连接算子，我们一一来看一下。首先看一下两个表做连接的情况，从示例中很容易看出，两个表选择了最通用的嵌套循环连接方法。这个示例我们在前面的课程中也使用 enable_material 进行调整过，通过禁用 Materialize 方法，可以产生两个表直接进行嵌套循环连接的执行计划。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT, SCORE;
                               QUERY PLAN
------------------------------------------------------------------------
 Nested Loop  (cost=0.00..1250335.00 rows=100000000 width=24)
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
   -&gt;  Materialize  (cost=0.00..205.00 rows=10000 width=12)
         -&gt;  Seq Scan on score  (cost=0.00..155.00 rows=10000 width=12)
(4 rows)
</code></pre>
<p>如果我们把嵌套循环连接方法禁用掉，优化器想必会选择哈希连接或归并连接中的一种吧？</p>
<pre><code>postgres=# set enable_nestloop = off;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT, SCORE;
                                 QUERY PLAN
----------------------------------------------------------------------------
 Nested Loop  (cost=10000000000.00..10001250335.00 rows=100000000 width=24)
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
   -&gt;  Materialize  (cost=0.00..205.00 rows=10000 width=12)
         -&gt;  Seq Scan on score  (cost=0.00..155.00 rows=10000 width=12)
(4 rows)
</code></pre>
<p>结果事与愿违，优化器还是执着地选择了嵌套循环连接，尽管目前嵌套循环连接的执行代价已经非常大了。这是因为：PostgreSQL 要想生成哈希连接或者归并连接，需要有匹配的约束条件才行，显然我们的示例中是没有约束条件的，那么我们不妨加上约束条件：</p>
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
<p>加上约束条件，优化器会去识别这个约束条件是否符合做哈希连接的需要，从执行计划可以看出，优化器选择了 st.sno = sc.sno 作为 Hash Cond。</p>
<p>如果继续关闭哈希连接，优化器就会倾向于选择归并连接了，从归并连接的执行计划中可以看出，这次 st.sno = sc.sno 又变成了 Merge Cond：</p>
<pre><code>postgres=# set enable_hashjoin = off;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT st, SCORE sc WHERE st.sno = sc.sno;
                                         QUERY PLAN
--------------------------------------------------------------------------------------------
 Merge Join  (cost=819.68..1322.67 rows=10000 width=24)
   Merge Cond: (st.sno = sc.sno)
   -&gt;  Index Scan using student_pkey on student st  (cost=0.29..328.29 rows=10000 width=12)
   -&gt;  Sort  (cost=819.39..844.39 rows=10000 width=12)
         Sort Key: sc.sno
         -&gt;  Seq Scan on score sc  (cost=0.00..155.00 rows=10000 width=12)
(6 rows)
</code></pre>
<p>这里有一点需要说明的是，归并连接这种需要排序的执行算子是 B 树索引扫描的“真爱粉”，因为 student_pkey 这样的 B 树索引具有有序的特点。通过这种索引扫描出来的数据天然就是有序的，而归并连接最喜欢的就是有序的数据，这样它就能避免对这份数据再进行显式地排序了。从执行计划可以看出，SCORE 表上就没有索引，所以显式地加上了 Sort 结点，而 STUDENT 表的扫描则借助了索引的有序性，没有显式地增加 Sort 结点。</p>
<p>我们在这里继续禁用 Sort 方法，结果执行计划又出现了走投无路的情况，从执行计划的代价可以看出，这次的 Sort 结点的排序代价是一个“超大值”。</p>
<pre><code>postgres=# set enable_sort = off;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT st, SCORE sc WHERE st.sno = sc.sno;
                                         QUERY PLAN
--------------------------------------------------------------------------------------------
 Merge Join  (cost=10000000819.68..10000001322.67 rows=10000 width=24)
   Merge Cond: (st.sno = sc.sno)
   -&gt;  Index Scan using student_pkey on student st  (cost=0.29..328.29 rows=10000 width=12)
   -&gt;  Sort  (cost=10000000819.39..10000000844.39 rows=10000 width=12)
         Sort Key: sc.sno
         -&gt;  Seq Scan on score sc  (cost=0.00..155.00 rows=10000 width=12)
(6 rows)
</code></pre>
<h3 id="-2">聚集与分组的执行计划调整</h3>
<p>PostgreSQL 中提供了两种对数据进行分组的方法，一种是哈希聚集（Hash Cluster），另一种是顺序聚集（Sort Cluster），但是 PostgreSQL 只提供了对 Hash 聚集的禁用方法，却没有提供对 Sort 聚集的禁用方法。实际上 Hash 聚集的这个功能在 PostgreSQL 中实现得比较晚，也就是说在很长一段时间 PostgreSQL 只有 Sort 聚集一种分组方法。</p>
<pre><code>postgres=# EXPLAIN SELECT MAX(DEGREE) FROM SCORE GROUP BY CNO;;
                           QUERY PLAN
-----------------------------------------------------------------
 HashAggregate  (cost=205.00..205.05 rows=5 width=8)
   Group Key: cno
   -&gt;  Seq Scan on score  (cost=0.00..155.00 rows=10000 width=8)
(3 rows)

postgres=# set enable_hashagg = off;
SET
postgres=# EXPLAIN SELECT MAX(DEGREE) FROM SCORE GROUP BY CNO;;
                              QUERY PLAN
-----------------------------------------------------------------------
 GroupAggregate  (cost=819.39..894.44 rows=5 width=8)
   Group Key: cno
   -&gt;  Sort  (cost=819.39..844.39 rows=10000 width=8)
         Sort Key: cno
         -&gt;  Seq Scan on score  (cost=0.00..155.00 rows=10000 width=8)
(5 rows)
</code></pre>
<h3 id="-3">简单调整并行执行计划</h3>
<p>所谓并行度就是一个任务同时需要几个并行的后台进程进行处理，用户可以在创建表的时候指定 parallel_workers 参数，例如有 SQL 语句：</p>
<pre><code>CREATE TABLE TEST_A(a INT) WITH (PARALLEL_WORKERS=100);
</code></pre>
<p>就可以指定一个并行度是 100 的表，但这并不代表对这个表进行扫描的时候一定会产生一个并行度是 100 的并行扫描路径。一方面非并行路径代价可能低于并行路径的代价，这时就会选择非并行路径；另一方面 PostgreSQL 数据库对并行度也进行了限制，每个查询都有过大的并行度对数据库的整体性能也会带来不利影响。</p>
<p>PostgreSQL 会自适应地计算一个查询需要多少个 worker 来同时工作，它综合考虑了一个表进行顺序扫描所需要的页面数（heap_pages）、进行索引扫描所需要的页面数（index_pages）。另外，PostgreSQL 数据库还增加了几个 GUC 参数来提高并行度设置的灵活性，这样用户就可以自己调节这些参数，根据当前的硬件环境来配置自己的并行度。</p>
<table border="0" style="width:1000px;font-size:6px;">
  <tr>
    <th width="100px">参数名</th>
    <th width="40px">参数类型</th>
    <th >描述</th>
  </tr>
<tr>
<td> min_parallel_table_scan_size</td>
<td width="40px">int</td>
<td> 启用并行表扫描的最小页面数，
也就是说表扫描的页面数小于
min_parallel_table_scan_size，
不会启用并行扫描</td>
</tr>

<tr>
<td>min_parallel_index_scan_size</td>
<td width="40px">int</td>
<td>启用并行索引扫描的最小页面数，
也就是说索引扫描的页面数小于
min_parallel_index_scan_size，
不会启用并行扫描</td>
</tr>

<tr>
<td>max_parallel_workers_per_gather</td>
<td width="40px">int</td>
<td>每个 gather 下的最大并行度，
在同一个执行计划里，
gather 路径是并行的最上层子路径，
它用来对并行的后台线程的执行结果进行合并，
一个执行计划里可能有多个 gather 路径</td>
</tr>
</table>
<p>如果对一个表进行扫描，如果 heap_pages &lt; min_parallel_table_scan_size 或者 index_pages &lt; min_parallel_index_scan_size，就不启用并行查询。</p>
<p>另外基于 min_parallel_table_scan_size 和 min_parallel_index_scan_size 可以获得一个并行度的参考值：</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/30538c30-cdd5-11e8-8458-03f9794b87bd"  /></div>
<p></br></p>
<p>当然，这个并行度还不能超过 max_parallel_workers_per_gather 参数设置的值，如果超过了 max_parallel_workers_per_gather，那么就取 max_parallel_workers_per_gather 的值作为并行度。</p>
<p>另外还有一个 max_parallel_workers 参数，用来控制在同一时间最多有多少并行的进程。</p>
<p>因为我们目前的示例中的数据量都比较小，所以都没有出现并行执行计划的情况，当然 PostgreSQL 也给我们提供了 GUC 参数 force_parallel_mode 来强制增加一个 gather 结点：</p>
<pre><code>postgres=# set force_parallel_mode = on;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT;
                             QUERY PLAN
--------------------------------------------------------------------
 Gather  (cost=1000.00..2155.00 rows=10000 width=12)
   Workers Planned: 1
   Single Copy: true
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
(4 rows)
</code></pre>
<h3 id="-4">小结</h3>
<p>了解 SQL 语句的执行过程，能够对执行计划进行解读、数量的调整，是学习优化器的基本要素之一，也是最常用的基本内容。通过这些内容可以反向地理解 PostgreSQL 优化器的实现。实际上，大部分数据库的优化器实现都大同小异，理解 PostgreSQL 的优化器之后，期待读者朋友能举一反三、触类旁通，那么就不虚此行了。</p></div></article>