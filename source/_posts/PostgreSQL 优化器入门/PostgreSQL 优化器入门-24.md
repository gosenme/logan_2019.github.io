---
title: PostgreSQL 优化器入门-24
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>PostgreSQL 中除了 SPJ(SELECT、PROJECT、JOIN) 之外，还有大量的聚合和分组操作，比如下面示例中的语句，其中有聚集操作  avg(a) 和分组操作 GROUP BY b。顾名思义，聚集操作就是一个合并的过程，而分组操作则是对数据的归类。</p>
<pre><code>postgres=# EXPLAIN SELECT avg(a) FROM TEST_A GROUP BY b;
                          QUERY PLAN
--------------------------------------------------------------
 HashAggregate  (cost=2.50..3.75 rows=100 width=36)
   Group Key: b
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=8)
(3 rows)
</code></pre>
<h3 id="">简单的聚集操作</h3>
<p>简单来说，聚集操作分成 3 个步骤。</p>
<ul>
<li>初始阶段：初始化一个初值，比如对于 avg 操作来说，它的初值是 0。</li>
<li>中间阶段：向初值中不断累加值，并记载累加了多少条记录。比如要对 TEST_A.a 做 avg 聚集操作，就需要先把 TEST_A.a 中的所有列值累加起来，并且同时统计 TEST_A.a 中有多少条数据。</li>
<li>结束阶段：对累加的数据做最后的处理，比如对 avg 聚集来说，在<strong>中间阶段</strong>已经累加了所有的值和数量，求平均值就只需要做一次除法就可以了。</li>
</ul>
<p>这样看起来还是蛮容易的，如果我们自己去算一个平均数，也都是这样做的。但是 avg 是函数的形态，PostgreSQL 怎么区分函数是否是聚集函数呢？在语义分析阶段，PostgreSQL 根据 PG_PROC 表中的信息就能知道这个函数是一个聚集函数：</p>
<pre><code>postgres=# SELECT oid, proname, proargtypes, prokind, prosrc FROM PG_PROC WHERE proname='avg';
 oid  | proname | proargtypes | prokind |     prosrc
------+---------+-------------+---------+-----------------
 2100 | avg     | 20          | a       | aggregate_dummy
 2101 | avg     | 23          | a       | aggregate_dummy
 2102 | avg     | 21          | a       | aggregate_dummy
 2103 | avg     | 1700        | a       | aggregate_dummy
 2104 | avg     | 700         | a       | aggregate_dummy
 2105 | avg     | 701         | a       | aggregate_dummy
 2106 | avg     | 1186        | a       | aggregate_dummy
(7 rows)

注：针对每种类型都生成一个对应的 avg 聚集函数
</code></pre>
<p>所以在语义分析阶段一旦发现这个函数是聚集函数，那么就会记录它的信息，并且从 PG_AGGREGATE 系统表中找到这个函数对应的三个阶段：</p>
<pre><code>postgres=# SELECT aggfnoid, aggtransfn, aggfinalfn, agginitval FROM PG_AGGREGATE WHERE aggfnoid=2101;
    aggfnoid    |   aggtransfn   | aggfinalfn | agginitval
----------------+----------------+------------+------------
 pg_catalog.avg | int4_avg_accum | int8_avg   | {0,0}
(1 row)

* 初始化阶段用的是 agginitval 中的初值
* 中间阶段用的是 int4_avg_accum 中的函数进行累加
* 最终阶段用 int8_avg 中的函数做一个触发操作
</code></pre>
<p>在很长一段时间里，这就是 PostgreSQL 执行一个聚集函数的经典方法。它的问题是性能差了一点，因为在累加的时候它是单线程的，无法充分利用 CPU，而且每次只能累加一条元组。PostgreSQL 针对每条元组都要调用一次累加函数，这个开销也不能简单地忽略掉。为了提高 CPU 的利用率，PostgreSQL 增加了并行的聚集操作（为了减少一次一元组的开销，还可以考虑在执行器的阶段引入向量化执行。目前 PostgreSQL 还没有相关的功能，但是源自 PostgreSQL 的 HAWQ 数据库已经实现了部分向量化执行的功能，性能也获得了大幅提升）。</p>
<p>并行聚集的执行计划是什么样的呢？来看一个执行计划的示例：</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT SUM(a) FROM TEST_A;
                                           QUERY PLAN
---------------------------------------------------------------------------------------
 Finalize Aggregate  (cost=7793.55..7793.56 rows=1 width=8)
   Output: sum(a)
   -&gt;  Gather  (cost=7793.33..7793.54 rows=2 width=8)
         Output: (PARTIAL sum(a))
         Workers Planned: 2
         -&gt;  Partial Aggregate  (cost=6793.33..6793.34 rows=1 width=8)
               Output: PARTIAL sum(a)
               -&gt;  Parallel Seq Scan on public.test_a
                     Output: a
(9 rows)
</code></pre>
<p>那么 PostgreSQL 如何并行地执行聚集函数呢？当然，对于不同的函数有不同的处理方法，还是以 avg 聚集函数为例。由于引入了并行，因此它增加了这么几个函数：</p>
<pre><code>postgres=# SELECT aggfnoid, aggcombinefn, aggserialfn, aggdeserialfn FROM PG_AGGREGATE WHERE aggfnoid = 2101;
    aggfnoid    |   aggcombinefn   | aggserialfn | aggdeserialfn
----------------+------------------+-------------+---------------
 pg_catalog.avg | int4_avg_combine | -           | -
(1 row)
</code></pre>
<p>显然，并行的聚集需要在不同的进程间进行通信，也就是下层结点需要把自己聚集产生的结果传输给上层结点。有些数据类型很方便地就能进行直接的传输了，而有些类型属于 internal 类型，这种类型就没那么容易传输了。因此，需要增加序列化和反序列化函数，比如上面示例中的 int 类型，它的传输是比较容易的，所以示例中没有提供序列化和反序列化函数。PostgreSQL 清楚地知道如何对一个 int 进行序列化，针对 “internal” 类型的函数，必须要借用序列化和反序列化函数，例如对于 int8 类型的聚集函数，就需要借助序列化函数：</p>
<pre><code>-- int8 对应的 OID 是 20
postgres=# SELECT oid, typname FROM PG_TYPE WHERE typname='int8';
 oid | typname
-----+---------
  20 | int8
(1 row)

-- int8 对应的聚集函数的 OID 是 2100
postgres=# SELECT oid, proname, proargtypes, prokind, prosrc FROM PG_PROC WHERE proname='avg' AND proargtypes = '20';
 oid  | proname | proargtypes | prokind |     prosrc
------+---------+-------------+---------+-----------------
 2100 | avg     | 20          | a       | aggregate_dummy
(1 row)

-- int8 对应的序列化函数和反序列化函数是存在的，因为负责传输中间结果的数据类型是 “internal”
postgres=# SELECT aggfnoid, aggcombinefn, aggserialfn, aggdeserialfn, aggtranstype FROM PG_AGGREGATE WHERE aggfnoid = 2100;
    aggfnoid    |   aggcombinefn   |    aggserialfn     |    aggdeserialfn     | aggtranstype
----------------+------------------+--------------------+----------------------+--------------
 pg_catalog.avg | int8_avg_combine | int8_avg_serialize | int8_avg_deserialize |         2281
(1 row)

-- 实践证明， aggtranstype 对应的数据类型是 “internal”
postgres=# SELECT typname FROM PG_TYPE WHERE oid = 2281;
 typname
----------
 internal
(1 row)
</code></pre>
<p>除了序列化和反序列化函数，还有一个 combine 函数。这个函数很容易理解，并行聚集总是需要汇总结果的，combine 的作用就是汇总结果，在此就不赘述了。</p>
<h3 id="-1">复杂的聚集操作</h3>
<p>目前看上去一切完美，这是因为我们还没有把 PG_AGGREGATE 系统表分析透彻，不信你看下面几个函数，就让人觉得难以理解：</p>
<pre><code>postgres=# SELECT aggfnoid, aggmtransfn, aggminvtransfn, aggmfinalfn FROM PG_AGGREGATE WHERE aggfnoid = 2101;
    aggfnoid    |  aggmtransfn   |   aggminvtransfn   | aggmfinalfn
----------------+----------------+--------------------+-------------
 pg_catalog.avg | int4_avg_accum | int4_avg_accum_inv | int8_avg
(1 row)
</code></pre>
<p>不妨让我们来看这么一个例子：</p>
<pre><code>postgres=# SELECT avg(b) OVER (ORDER BY a ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) FROM (VALUES (1, 1),(2, 2),(3,3),(4,4),(5,5)) AS T(a,b);
        avg
--------------------
 2.0000000000000000
 3.0000000000000000
 4.0000000000000000
 4.5000000000000000
 5.0000000000000000
(5 rows)
</code></pre>
<p>这个函数的意思就滚动向下累加求平均值。累加我们已经说过了，所以你看上面示例中的 aggmtransfn 和 aggtransfn 是一样的，都是 int4<em>avg</em>accum，但是除了累加之外还要剔除前面的值，因为我们的“滑动的小窗口”是 3 ，所以这里的 aggminvtransfn 就负责不断剔除值。至于汇总函数，最后还提供了一个汇总结果。</p>
<h3 id="-2">分组操作</h3>
<p>分组操作经常会和聚集一起使用，但是我们也能单独使用分组方法对数据进行归类。如果只对一列数据进行分组，其实和去重操作就差不多：</p>
<pre><code>-- 去重操作
postgres=# EXPLAIN SELECT distinct a FROM TEST_A;
                          QUERY PLAN
--------------------------------------------------------------
 HashAggregate  (cost=2.25..3.25 rows=100 width=4)
   Group Key: a
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=4)
(3 rows)

-- 分组操作
postgres=# EXPLAIN SELECT a FROM TEST_A GROUP BY a;
                          QUERY PLAN
--------------------------------------------------------------
 HashAggregate  (cost=2.25..3.25 rows=100 width=4)
   Group Key: a
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=4)
(3 rows)
</code></pre>
<p>对于去重，通常需要借助两个方法：排序和哈希。</p>
<p>如果对一组数据进行排序，那么那些相同的数据就会“挨”在一起，这样就很容易找到重复数据并把重复数据去掉。如果对一组数据进行哈希，那么相同的数据肯定会进入同一个哈希桶中，如果我们发现桶中已经有了这个数据，那么就不把它插入桶中了，这样也能去重。既然去重和分组有相似之处，所以 PostgreSQL 也采用了排序和哈希的方法来进行分组。在上面示例的执行计划中我们总可以看到 HashAggregate 的身影，这就是采用哈希的方法来进行分组。如果禁用哈希方法，就会采用排序的方法进行分组(从执行计划可以看出，采用排序进行分组的代价高一些，所以需要禁用哈希分组方法才能启用)：</p>
<pre><code>postgres=# SET ENABLE_HASHAGG = OFF;
SET
postgres=# EXPLAIN SELECT a FROM TEST_A GROUP BY a;
                             QUERY PLAN
--------------------------------------------------------------------
 Group  (cost=5.32..5.82 rows=100 width=4)
   Group Key: a
   -&gt;  Sort  (cost=5.32..5.57 rows=100 width=4)
         Sort Key: a
         -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=4)
(5 rows)
</code></pre>
<h3 id="-3">小结</h3>
<p>这一节课主要介绍了聚集和分组的操作实现。目前 PostgreSQL 已经实现了并行的聚集，并行的聚集需要更多聚集方法的支持，因为要将各个进程的数据汇总到一起。对于窗口函数中的聚集，不但需要提供用来汇总数据的函数，还需要提供剔除数据的函数。</p>
<p>分组主要采用了两种方法——哈希方法和排序的方法。PostgreSQL 通常会采用哈希方法，但是用户也应该尝试禁用哈希方法，这往往会带来惊喜。</p></div></article>