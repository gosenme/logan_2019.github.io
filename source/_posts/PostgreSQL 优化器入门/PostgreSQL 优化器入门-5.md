---
title: PostgreSQL 优化器入门-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>SQL 语句在转换成查询树之后，就会进入优化器。优化器通过对查询树进行逻辑优化和物理优化后挑选出一个最优的执行计划，这个执行计划就会交给执行器来执行。因此，在使用 PostgreSQL 数据库的过程中，如果你在执行一个 SQL 语句时期望优化器给你带来的是卖家秀，结果实际上收到一个买家秀，那二话不说就先要看看这个 SQL 语句到底产生了一个什么样的执行计划，是不是因为优化器一时发昏选了一个比较“傻”的执行计划。</p>
<h3 id="">不同的执行算子示例</h3>
<p>执行计划是一个非完全的二叉树，每个父结点至少有一个子结点（叶子结点除外），最多有两个子结点。PostgreSQL 数据库的查询执行器通过对这个二叉树迭代执行来获得查询结果，它的执行过程我们通常叫它火山模型。</p>
<p>在 PostgreSQL 中，可以使用 EXPLAIN 语句来展示查询语句的执行计划，例如：</p>
<pre><code>INSERT INTO STUDENT SELECT i, repeat('A', i%5 + 1), i%2 FROM GENERATE_SERIES(1,10000) i;
ANALYZE STUDENT;

postgres=# EXPLAIN SELECT * FROM STUDENT;
                          QUERY PLAN
--------------------------------------------------------------
 Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
(1 row)
</code></pre>
<p>由于上面的示例是对 STUDENT 表进行查询，获取 STUDENT 表中的所有数据，因而就需要用一个 Seq Scan 就够了，它会把 STUDENT 表中的数据全部遍历一遍，但是假如要进行连接操作：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT, (SELECT * FROM SCORE) as sc;
                               QUERY PLAN
------------------------------------------------------------------------
 Nested Loop  (cost=0.00..1250335.00 rows=100000000 width=24)
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
   -&gt;  Materialize  (cost=0.00..205.00 rows=10000 width=12)
         -&gt;  Seq Scan on score  (cost=0.00..155.00 rows=10000 width=12)
(4 rows)
</code></pre>
<p>我们从语句中可以看出这是一个单表和一个子查询进行连接，但是从执行计划可以看出，子查询已经没有了，而是直接变成了 STUDENT 表和 SCORE 的物化表的连接。这是因为优化器认为这里的子查询和直接使用 SCORE 表是等价的，这个执行计划对应的二叉树应该如下图所示：</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/477cc440-cdd4-11e8-8458-03f9794b87bd" width="150px" /></div>
<p></br></p>
<p>我们把每个结点的输出都可以看做是一个“临时表”，因此对于嵌套循环连接而言，它的左侧是对 STUDENT 表的顺序扫描，而右侧则可以看做是“临时表”的 Materialize 表，也就是说对于嵌套循环连接来说它的两个子结点“就是两个表”。</p>
<p>嵌套循环连接的执行流程是这样的：</p>
<pre><code>1.如果不存在外表元组，从外边获得一条元组；
2.如果外表元组是 NULL，连接操作结束；
3.从内表获得一条元组；
4.如果内表元组是 NULL，跳转到步骤 1；
5.外表和内表元组做连接，返回连接结果。
</code></pre>
<div style="text-align:center">
<img src="https://images.gitbook.cn/4199f4e0-d02b-11e8-a802-f373f137079f" width="400px"" /></div>
<p></br></p>
<p>嵌套循环连接的时间复杂度是一个 O(MN），所以它通常只适用于如下一些情况：</p>
<ul>
<li>没有什么可用的连接条件</li>
<li>内表有索引，可以通过索引扫描加速</li>
</ul>
<h3 id="explain">EXPLAIN 执行计划的解读</h3>
<p>执行计划中显示了优化器估算出来的两部分代价、行数和元组的宽度，例如，"(cost=0.00..1250335.00 rows=100000000 width=24)"，其中每一部分的含义如下：</p>
<table>
<thead>
<tr>
<th>name</th>
<th>descriptor</th>
</tr>
</thead>
<tbody>
<tr>
<td>cost</td>
<td>执行这一步骤的代价</td>
</tr>
<tr>
<td>rows</td>
<td>执行这一步骤会产生的元组数量</td>
</tr>
<tr>
<td>width</td>
<td>产生出的元组的平均字节数</td>
</tr>
</tbody>
</table>
<p>“cost=0.00..1250335.00”中的 0.00 代表的是启动代价，1250335.00 代表的是这个结点和它的子结点共同的整体代价。</p>
<p>启动代价是嵌套循环连接返回第一条元组前所消耗的代价。记录启动代价是有意义的，比如在执行计划中可能存在做“预处理”操作的结点，这些操作都会带来启动代价，因为它们要把全部元组预处理完才会返回第一条元组。比如排序操作，它需要把所有的元组都获取到，然后对元组排序，然后再返回第一条元组，所以获取第一条元组之前的排序时间就是启动代价：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT ORDER BY SNAME;
                             QUERY PLAN
--------------------------------------------------------------------
 Sort  (cost=819.39..844.39 rows=10000 width=12)
   Sort Key: sname
   -&gt;  Seq Scan on student  (cost=0.00..155.00 rows=10000 width=11)
(3 rows)
</code></pre>
<p>通过上面的示例可以看出来，Sort 结点——也就是排序操作的启动代价是 819.39，它的执行代价是844.39 − 819.39 = 25.00。因此，在优化器进行最优执行计划选择的时候，启动代价是一个很重要的参考指标。</p>
<p>执行计划中的 rows 代表的是当前结点所产生的结果元组数量，这是一个估计值，实际上每个表针对元组数量都会有一个估计值，它保存在 PG_CLASS 系统表中。从下面的示例可以看出 STUDENT 表中有 10000 条元组，这是符合我们预期的（但实际上这里应该是个估计值，这里的估计比较准确是因为我们还没有对这个表进行过多次的增删改查操作）。</p>
<pre><code>postgres=# select reltuples from pg_class where relname = 'student';
 reltuples
-----------
     10000
(1 row)
</code></pre>
<p>width 则是当前结点做投影的元组的平均宽度，STUDENT 表上的元组的平均宽度需要怎么计算呢？对于定长的属性，比如 INT 类型、BOOL 类型等，我们很容易知道它的长度，通过查询 PG_TYPE 系统表就能知道：</p>
<pre><code>postgres=# SELECT typname, typlen FROM PG_TYPE WHERE TYPNAME='int4';
 typname | typlen
---------+--------
 int4    |      4
(1 row)
</code></pre>
<p>对于非定长的，比如 Varchar 类型、TEXT 类型，它在 PG_TYPE 系统表中的长度是 -1，但是我们有办法获每一列的平均宽度（通过统计信息获得，后续课程会进行介绍），这里我们用一个聚集函数来看一下 sname 列的平均宽度：</p>
<pre><code>postgres=# SELECT AVG(LENGTH(sname)) FROM STUDENT;
        avg
--------------------
 3.0000000000000000
(1 row)
</code></pre>
<p>通过类型的长度以及通过聚集函数得到的平均宽度，我们可以计算得到元组的平均宽度是 4 + 3 + 4 = 11。可是我们从执行计划里看到的平均宽度是 12，这中间差的 1 个字节是搁哪来的呢？这是因为虽然我们用 avg 获得的 sname 的平均宽度是 3，但是在数据库内部，每个变长的数据类型会有一个头部（HEADER，头部的长度有可能是 1，也有可能是 4，取决于字符串具体的长度，我们示例中的字符串的长度都比较短，所以头部的长度是 1 字节）。它的形式是这样的，sname 除了内容的平均宽度是 3 之外，还有 1 个字节的 HEADER 信息，因此它的平均宽度是 4，也就获得了元组的平均宽度是 4 + 4 + 4 = 12。</p>
<h3 id="-1">物化结点的作用</h3>
<p>读者是否产生这样一个疑问，执行计划中的 Materialize 这一层是否属于画蛇添足呢？这里对 SCORE 表进行一次物化看上去并不能带来任何效率上的提升，反而因为做物化需要消耗资源把代价从 105 增加到了 255，PostgreSQL 为什么要增加这样的结点呢？我们尝试通过一个 GUC 参数来把物化结点去掉，看看没有物化的执行计划的代价是多少：</p>
<pre><code>postgres=# SET ENABLE_MATERIAL = OFF;

postgres=# EXPLAIN SELECT * FROM STUDENT st, SCORE sc;
                              QUERY PLAN
-----------------------------------------------------------------------
 Nested Loop  (cost=0.00..2550155.00 rows=100000000 width=24)
   -&gt;  Seq Scan on student st  (cost=0.00..155.00 rows=10000 width=12)
   -&gt;  Seq Scan on score sc  (cost=0.00..155.00 rows=10000 width=12)
(3 rows)

Time: 0.633 ms
</code></pre>
<p>有物化结点和没有物化结点的代价竟然相差这么多，没有物化结点的执行计划的总代价竟升高了足足有一倍，这其中的原因是 PostgreSQL 数据库的代价模型的计算方法的问题。</p>
<p>由于执行计划中的外表有 10000 条元组，在执行嵌套循环连接的时候，就需要对内表重复的扫描 10000 次。对一个表进行重复扫描的代价可能是不同的，比如第一次扫描的时候有些表的某些数据还在磁盘上，需要从磁盘加载到主存。但是在第二次扫描的时候，第一次加载到主存的数据就能够重复利用了，也就是说很可能第二次扫描的代价比第一次扫描的代价要低。</p>
<p>如果内表是 Seq Scan（没有物化的情况），它重复扫描的时候代价估算系统仍然认为代价是 155，也就是仍然按照需要读取磁盘的代价来进行计算。而 Materialize 就不同了，PostgreSQL 会计算物化之后的数据量的大小。如果物化之后的数据量能够完全放到内存里，在第二次扫描物化结点的时候，就可以假设这个结点是在内存里的，就不用考虑读磁盘带来的消耗了，这就是最终优化器认为加上 Materialize 的代价反而低的原因。</p>
<p>那么优化器是否可以考虑到各种情况呢? 假如把所有的因素都考虑到，那么生成执行计划的时候就会很长。如果生成执行计划要几个小时，即使选出的执行计划很优秀，也是不可接受的。因此，优化器中也需要权衡生成执行计划的时间和执行计划具体的执行时间。</p>
<h3 id="explain-1">EXPLAIN 语法说明</h3>
<p>我们实际地执行一下有 Materialize 结点和没有 Materialize 结点的这两种执行计划，看看是否真的如优化器所估算的那样有很大的差别。恰好 EXPLAIN 有一些 option 选项，我们尝试通过下面这些选项来分析问题。</p>
<pre><code>EXPLAIN [ ( _option_ [, ...] ) ] _statement_
</code></pre>
<p>其中的<code>_option_</code>可以是如下内容：</p>
<pre><code>ANALYZE [ _boolean_ ]
VERBOSE [ _boolean_ ]
COSTS [ _boolean_ ]
BUFFERS [ _boolean_ ]
TIMING [ _boolean_ ]
FORMAT { TEXT | XML | JSON | YAML }
</code></pre>
<p><strong>ANALYZE</strong>：通常通过 EXPLAIN 打印出的执行计划中的代价都是估计代价，如果增加上 ANALYZE 选项之后，还会在执行计划中打印实际的执行时间和实际的元组处理数量，也就是实际的代价。需要注意的是由于打印实际执行的代价也就意味着这个执行计划真正的执行了，而如果没有 ANALYZE 选项，执行计划不会实际地执行。</p>
<p><strong>VERBOSE</strong>：通常打印的执行计划更多的关注它的执行路径，对于投影之类的信息不会同时打印出来，增加上 VERBOSE 选项打印的信息会更丰富。</p>
<p><strong>COSTS</strong>：PostgreSQL 数据库默认打印代价，可以通过（COSTS OFF）关闭估计代价的打印。本选项默认是打开的，如果只是想看看执行路径，而不关系具体的估计代价，这个选项是可以关闭的。对于 PostgreSQL 数据库的内核开发者而言，这个选项经常用在写测试用例的时候。如果想测试一个语句的执行计划是否正确，自动化测试框架会通过 EXPLAIN 来查看该语句的执行计划。但自动化测试框架运行的主机不同，它产生的估计代价可能也不同，所以这时可以不打印代价的估计值。</p>
<p><strong>BUFFERS</strong>：需要和 ANALYZE 同时使用，因为它要打印缓冲区的命中率，而命中率只有实际执行过才知道。数据库为了提高性能，并不是每次读取数据都从磁盘读取，而是将大部分数据缓存在主存里。如果缓存的命中率很低，就要增加换页锁带来的消耗，所以可以通过 BUFFERS 来查看缓冲区的命中率。</p>
<p><strong>TIMING</strong>：需要和 ANALYZE 同时使用，ANALYZE 默认会统计各个结点的实际运行时间，通过 TIMING OFF，可以让 ANALYZE 不统计时间，只统计处理的元组的数量。</p>
<h3 id="-2">物化结点的代价模型的缺陷</h3>
<p>有了这些选项，我们再来看一下，有 Materialize 结点和没有 Materialize 结点的实际执行代价：</p>
<pre><code>postgres=# SET ENABLE_MATERIAL = ON;

postgres=# explain (analyze,buffers,costs off) SELECT * FROM STUDENT st, SCORE sc;
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Nested Loop (actual time=0.054..31231.428 rows=100000000 loops=1)
   Buffers: shared hit=110
   -&gt;  Seq Scan on student st (actual time=0.016..2.951 rows=10000 loops=1)
         Buffers: shared hit=55
   -&gt;  Materialize (actual time=0.000..0.883 rows=10000 loops=10000)
         Buffers: shared hit=55
         -&gt;  Seq Scan on score sc (actual time=0.020..1.778 rows=10000 loops=1)
               Buffers: shared hit=55
 Planning time: 0.130 ms
 Execution time: 38574.290 ms
(10 rows)

postgres=# SET ENABLE_MATERIAL = OFF;

postgres=# explain (analyze,buffers,costs off) SELECT * FROM STUDENT st, SCORE sc;
                                  QUERY PLAN
------------------------------------------------------------------------------
 Nested Loop (actual time=0.056..34717.028 rows=100000000 loops=1)
   Buffers: shared hit=550055
   -&gt;  Seq Scan on student st (actual time=0.031..1.845 rows=10000 loops=1)
         Buffers: shared hit=55
   -&gt;  Seq Scan on score sc (actual time=0.004..1.208 rows=10000 loops=10000)
         Buffers: shared hit=550000
 Planning time: 0.174 ms
 Execution time: 41996.891 ms
(8 rows)
</code></pre>
<p>通过对比发现：</p>
<table>
<thead>
<tr>
<th>Materialize</th>
<th>时间计算</th>
</tr>
</thead>
<tbody>
<tr>
<td>是</td>
<td>0.883 * 10000 次循环 = 8830 ms</td>
</tr>
<tr>
<td>否</td>
<td>1.208 * 10000 次循环 = 12080 ms</td>
</tr>
</tbody>
</table>
<p>对比总代价的时间差和结点的时间差可以看出的确 Materialize 节省了时间：</p>
<pre><code>估算的总时间差 = 2550155.00 - 1250335.00 = 1299820
实际执行总时间差 = 41996.891 - 38574.290 = 3422.601
实际执行对应结点的时间差 = 12080 - 8830 =  3250
</code></pre>
<p>实际执行时所节省的时间并没有优化器估算的那么大，这是因为 SCORE 表的体积并不大，在第一次读取之后，也能确保它的所有页面也已经加载到内存中了。从执行计划中也能看出，在没有 Materialize 结点的情况下，SCORE 表中页面在缓存中的命中率为 550000 次，而内表要重复扫描 10000 次。也就是说，平均每次循环命中 55 个页面，而实际上 SCORE 表目前也只有 55 个页面，也就证实了我们的猜想，页面已经全部被缓存。</p>
<pre><code>postgres=# SELECT RELPAGES FROM PG_CLASS WHERE RELNAME = 'score';
 relpages
----------
       55
(1 row)
</code></pre>
<h3 id="-3">小结</h3>
<p>执行计划的查看对 DBA 而言是非常重要的。如果一个查询语句执行得比较慢，这是最直接的查看手段，因此能够正确地阅读执行计划是所有 DBA 必须掌握的技能。如果通过查看执行计划发现了问题，进而想调整执行计划，PostgreSQL 也提供了相应的参数给我们来调整。</p></div></article>