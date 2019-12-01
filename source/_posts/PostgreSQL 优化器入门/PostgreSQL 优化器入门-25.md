---
title: PostgreSQL 优化器入门-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Greenplum 是脱胎于 PostgreSQL 的分布式数据库。既然是分布式数据库，原来 PostgreSQL 生成的基于单机数据库的执行计划显然就无法使用了。因此，本章要分析的是 Greenplum 如何改进 PostgreSQL 的执行计划，使其能够在分布式数据库中执行。</p>
<h3 id="">数据分布不同了</h3>
<p>Greenplum 中有多个结点，最主要的是划分成了 Master 结点和 Segment 结点。每个集群中只有一个 Master 结点，但是可以有多个 Segment 结点，Master 结点负责生成执行计划并协调执行计划的执行，而 Segment 结点负责保存数据。</p>
<p>分布式数据库的数据是分布在不同的结点之上的，PostgreSQL 数据库存在 3 种不同类型的表：</p>
<pre><code>-- 哈希分布表
shzhang=# CREATE TABLE TEST_A(a int, b int, c int, d int) DISTRIBUTED BY (a,b);
CREATE TABLE

-- 随机分布表
shzhang=# CREATE TABLE TEST_B(a int, b int, c int, d int) DISTRIBUTED RANDOMLY;
CREATE TABLE

-- 复制分布表
shzhang=# CREATE TABLE TEST_C(a int, b int, c int, d int) DISTRIBUTED REPLICATED;
CREATE TABLE
</code></pre>
<ul>
<li><p>哈希分布表: 按照指定的键值分布数据，比如在上面的示例中指定了以 (a,b) 作为键值进行分布数据。在向 TEST_A 中插入一条元组时，执行器会计算这个元组中对应的 (a,b) 所产生的整型的哈希值，并将这个哈希值映射到某个结点上（一般用取余数的方式，比如集群中有 3 个结点，通过 x%3 就能获得一个 0~2 之间的值）。在数据量比较大，数据比较“丰富”的情况下，这种方式能够比较好地分布数据，不会产生数据倾斜。但是如果 (a,b) 中的值比较单一，也有可能数据总是落在其中的一个结点上，这种情况会导致结点的读写压力比较大。另外，它带来的问题就是更新哈希键的时候会有一些麻烦，原因是更新哈希键可能导致本来在 0 号结点上的数据需要迁移到 1 号结点上，这和单机的更新差别较大。Greenplum 最新版本已经开始支持更新哈希键了。</p></li>
<li><p>随机分布表：随机分布数据，每条数据分布在哪个结点上并不是特别重要。随机作用导致数据在每个结点都差不多，不太可能产生数据倾斜，而且更新的时候也没有更新哈希键的苦恼。但这种方式也有个问题，就是“数据是没有特点的”。比如，对一个哈希分布的表，如果多个元组中的 (a,b) 相同，那么这些元组就都会落到同一个结点上，遇到 SQL 语句中包含等值约束条件的情况就可能比较有优势。但是随机分布的表不行，它的数据没有这些特点。</p></li>
<li><p>复制分布表：这种类型的表在每个结点上都有一份相同的数据拷贝。通常适用于表的数据量比较小的情况，是一种通过冗余数据优化数据库性能的方法。这种表的好处是，在做连接操作时经常需要在结点之间拷贝数据，有了复制表，就可以免于拷贝数据了。</p></li>
</ul>
<p>实际上还有一种类型的表，我们可以叫它 catalog 表，也就是 PostgreSQL 中对应的系统表。Greenplum 在每个结点上都保持了一份 catalog 表的副本，看上去和复制表有点像，它们之间的区别是 catalog 表在 Master 结点上也保有一份副本，而复制分布表只在 Segment 结点保存。</p>
<h3 id="motion">Motion 算子是个新成员</h3>
<p>在 PostgreSQL 中，虽然有并行执行计划，但是它们之间的通信还是在一个单机上的，通信的方法是使用共享内存的方式，而 Greenplum 则需要借助网络进行通信，在 Greenplum 内部实现了 Interconnect 组件负责通信的工作。</p>
<p>为了适应这种数据分布在不同的结点上的特点，Greenplum 对执行计划进行了分片，每一片叫一个 Slice。让我们先来看一个执行计划，TEST_A 是一个哈希分布表，它的数据分布在 3 个Segment 上，要扫描这个表的数据就需要在 3 个 Segment 上同时扫描，然后将数据汇总到一个结点上输出。通过示例可以看出，TableScan 是一个扫描算子，负责扫描 TEST_A 表，而 Gather Motion 则是负责汇总数据的算子，TableScan 扫描到的数据交给 Motion 算子传递上来。从执行计划可以看出，其中只有一个 Slice。</p>
<pre><code>shzhang=# EXPLAIN SELECT * FROM TEST_A;
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=0.00..431.00 rows=1 width=16)
   -&gt;  Table Scan on test_a  (cost=0.00..431.00 rows=1 width=16)
 Optimizer: PQO version 3.3.0
(3 rows)
</code></pre>
<p>在 SQL 语句中有连接操作的情况下，Motion 的作用就更大了。下面的执行计划是 TEST_A 和 TEST_B 进行连接的执行计划，TEST_A 是一个哈希分布表，TEST_B 是一个随机分布表。执行计划中分成了 2 个 Slice，其中一个 Slice 是将 TEST_B 做广播，把它广播到其他 3 个结点上，广播之后每个结点上就都有了一个 TEST_B 的副本，然后 TEST_A 和这个副本在第二个 Slice 里做连接操作。</p>
<pre><code>shzhang=# EXPLAIN SELECT * FROM TEST_A, TEST_B;
                                          QUERY PLAN
----------------------------------------------------------------------------------------------
 Gather Motion 3:1  (slice2; segments: 3)  (cost=0.00..1324032.39 rows=1 width=32)
   -&gt;  Nested Loop  (cost=0.00..1324032.39 rows=1 width=32)
         Join Filter: true
         -&gt;  Broadcast Motion 3:3  (slice1; segments: 3)  (cost=0.00..431.00 rows=1 width=16)
               -&gt;  Table Scan on test_b  (cost=0.00..431.00 rows=1 width=16)
         -&gt;  Table Scan on test_a  (cost=0.00..431.00 rows=1 width=16)
 Optimizer: PQO version 3.3.0
(7 rows)

其中Slice 1：
         -&gt;  Broadcast Motion 3:3  (slice1; segments: 3)  (cost=0.00..431.00 rows=1 width=16)
               -&gt;  Table Scan on test_b  (cost=0.00..431.00 rows=1 width=16)

其中Slice 2：
Gather Motion 3:1  (slice2; segments: 3)  (cost=0.00..1324032.39 rows=1 width=32)
   -&gt;  Nested Loop  (cost=0.00..1324032.39 rows=1 width=32)
         Join Filter: true
         -&gt;  Slice 1 的广播结果
         -&gt;  Table Scan on test_a  (cost=0.00..431.00 rows=1 width=16)
</code></pre>
<p>上面之所以将 TEST_B 做广播是因为它想借用 TEST_A 的哈希分布的特点，也就是：</p>
<pre><code>  A × B
= (A1 ∪ A2 ∪ A3) × B
= (A1 × B) ∪ (A2 × B) ∪ (A3 × B)
</code></pre>
<p>对于上面的例子，如果 TEST_B 是一个复制分布，那么就可以免掉一次广播，这就是复制分布表锁带来的好处：</p>
<pre><code>shzhang=# EXPLAIN SELECT * FROM TEST_A, TEST_C;
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=0.00..1324032.13 rows=1 width=32)
   -&gt;  Nested Loop  (cost=0.00..1324032.13 rows=1 width=32)
         Join Filter: true
         -&gt;  Table Scan on test_a  (cost=0.00..431.00 rows=1 width=16)
         -&gt;  Table Scan on test_c  (cost=0.00..431.00 rows=1 width=16)
 Optimizer: PQO version 3.3.0
(6 rows)
注：TEST_C 是复制分布表
</code></pre>
<p>再来看一个新的例子：</p>
<pre><code>shzhang=# EXPLAIN SELECT * FROM TEST_B bx, TEST_B by WHERE bx.a = by.a;
                                              QUERY PLAN
-------------------------------------------------------------------------------------------------------
 Gather Motion 3:1  (slice3; segments: 3)  (cost=0.00..862.00 rows=1 width=32)
   -&gt;  Hash Join  (cost=0.00..862.00 rows=1 width=32)
         Hash Cond: (test_b.a = test_b_1.a)
         -&gt;  Redistribute Motion 3:3  (slice1; segments: 3)  (cost=0.00..431.00 rows=1 width=16)
               Hash Key: test_b.a
               -&gt;  Table Scan on test_b  (cost=0.00..431.00 rows=1 width=16)
         -&gt;  Hash  (cost=431.00..431.00 rows=1 width=16)
               -&gt;  Redistribute Motion 3:3  (slice2; segments: 3)  (cost=0.00..431.00 rows=1 width=16)
                     Hash Key: test_b_1.a
                     -&gt;  Table Scan on test_b test_b_1  (cost=0.00..431.00 rows=1 width=16)
 Optimizer: PQO version 3.3.0
(11 rows)
注： TEST_B 是随机分布表
</code></pre>
<p>从示例中可以看出执行计划被划分成了 3 个 Slice：Slice1 和 Slice2 是对 TEST_B 表做重分布，也就是说把 TEST_B 表按照 TEST_B.a 进行哈希分布，也可以理解成是新建一个哈希分布表，这个哈希分布表和 TEST_B 表的数据相同，只不过哈希分布表中的数据是按照 TEST_B.b 哈希分布在不同的 Segment 上的。</p>
<p>这种情况就是：</p>
<pre><code>  A × B
= (A1 ∪ A2 ∪ A3) × (B1 ∪ B2 ∪ B3)
= (A1 × B1) ∪ (A1 × B2) ∪ (A1 × B3) ∪ (A2 × B1) ∪ (A2 × B2) ∪ (A2 × B3) ∪ (A3 × B1) ∪ (A3 × B2) ∪ (A3 × B3)
注意，如果连接条件是等值连接，而我们又是按照等值连接条件中的列进行的哈希分布，也就代表着分布到不同结点的元组是不可能产生连接结果的。例如 A1 × B2 就不可能产生连接结果，因此：

= (A1 × B1) ∪ (A2 × B2) ∪ (A3 × B3)
</code></pre>
<p>既然随机分布表需要做哈希重分布，就说明哈希分布表是有价值的。下面的示例中 TEST_A 是按照 (a,b) 分布的哈希分布表：</p>
<pre><code>shzhang=# EXPLAIN SELECT * FROM TEST_A ax, TEST_A ay WHERE ax.a = ay.a AND ax.b = ay.b;
                                      QUERY PLAN
--------------------------------------------------------------------------------------
 Gather Motion 3:1  (slice1; segments: 3)  (cost=0.00..862.00 rows=1 width=32)
   -&gt;  Hash Join  (cost=0.00..862.00 rows=1 width=32)
         Hash Cond: ((test_a.a = test_a_1.a) AND (test_a.b = test_a_1.b))
         -&gt;  Table Scan on test_a  (cost=0.00..431.00 rows=1 width=16)
         -&gt;  Hash  (cost=431.00..431.00 rows=1 width=16)
               -&gt;  Table Scan on test_a test_a_1  (cost=0.00..431.00 rows=1 width=16)
 Optimizer: PQO version 3.3.0
(7 rows)
</code></pre>
<p>从上面的示例可以看出，哈希分布表、随机分布表、复制分布表各有各的优势，需要数据库管理员根据自己的应用情况调整不同表的分布方式。</p>
<h3 id="-1">小结</h3>
<p>将执行计划分布式化的过程就是强调数据迁移的过程，无论是小表广播还是将数据按照某个键值重分布，都需要在 Segment 之间传输数据。为了尽量减少数据的传输，就需要在生成执行计划的时候做出权衡，是使用广播的方式还是重分布的方式，或者借用原有的哈希分布表的特性、复制表的特性优化掉一些 Motion。</p>
<h3 id="-2">后记</h3>
<p>到此为止，《PostgreSQL 优化器入门》更新完毕了。这些内容基本涵盖了 PostgreSQL 优化器的所有部分，对于一些偏底层的方法，因为并未分析源代码，用文字的形式描述出来就比较困难，所以在理解上相对也有难度。欢迎读者朋友们在阅读课程期间随时提出疑问，我会在 GitChat 读者圈中回答大家提出的问题，并根据大家的意见持续地改进课程，谢谢大家！</p></div></article>