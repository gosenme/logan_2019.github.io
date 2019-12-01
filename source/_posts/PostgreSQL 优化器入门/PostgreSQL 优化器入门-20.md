---
title: PostgreSQL 优化器入门-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>接下来我们会分别介绍 3 种物理路径的代价计算方法，这样读者就能跟着这种计算的过程了解代价计算的流程。需要注意的是读者朋友们可以不用过度关注计算的准确性，而是把注意力集中在 PostgreSQL 代价模型的思想上。</p>
<p>由于 SQL 是描述性语言，所以它只需要告诉我们执行结果，它不关心执行的过程。假如有很多可以获得执行结果的手段，那么我们当然是想获得一个效率最高的——也就是说条条大路通罗马，但我们一定要选一个最短的路来走。在 PostgreSQL 数据库中也把这些数据的访问方法称为“路径”（Path)，物理优化的过程就是从众多路径中选择最优路径的过程。</p>
<p>比如要访问 STUDENT 表，向这个表写入 10000 行数据：</p>
<pre><code>INSERT INTO STUDENT SELECT i, repeat('A', i%5 + 1), i%2 FROM GENERATE_SERIES(1,10000) i;
ANALYZE STUDENT;
</code></pre>
<p>目前已知：</p>
<ul>
<li>STUDENT 表有 10000 条数据</li>
<li>STUDENT 表在 sno 上有一个主键索引</li>
</ul>
<h3 id="">顺序扫描代价</h3>
<p>像 STUDENT 这样的堆表，最通用的办法是把它的数据全部访问一遍，所以就可以考虑顺序扫描（SeqScan）的方式来访问这个表：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT;
                          QUERY PLAN
--------------------------------------------------------------
 Seq Scan on student  (cost=0.00..155.00 rows=10000 width=12)
(1 row)
</code></pre>
<p>那么顺序扫描的代价是怎么计算出来的呢？我们来看一下计算顺序扫描的已知信息：</p>
<pre><code>--顺序扫描读取一个页面的代价
postgres=# SHOW SEQ_PAGE_COST;
 seq_page_cost
---------------
 1
(1 row)

--提取一条元组的代价
postgres=# SHOW CPU_TUPLE_COST;
 cpu_tuple_cost
----------------
 0.01
(1 row)

-- STUDENT 表占用的页面数，以及 STUDENT 表上的元组数
postgres=# SELECT RELPAGES, RELTUPLES FROM PG_CLASS WHERE RELNAME='student';
 relpages | reltuples
----------+-----------
       55 |     10000
(1 row)
</code></pre>
<p>我们可以把代价分成两部分：</p>
<pre><code>    整体代价 = IO 代价 + CPU 代价
</code></pre>
<p>IO 代价通常是和页面相关的代价，PostgreSQL 的数据是保存在页面里的，每个页面默认是 8k，所以 IO 代价通常和一个表所占的页面数量有关。CPU 代价是对元组进行处理的代价，一个页面上会保存多个元组，在拿到其中一个元组之后，要对这个元组进行表达式计算，这部分代价主要是 CPU 代价。下面分别计算 SeqScan 的IO 代价和 CPU 代价，最终获得 SeqScan 的整体代价：</p>
<pre><code>IO 代价 = 55 个页面 * SEQ_PAGE_COST = 55
CPU 代价 = 10000 条元组 * CPU_TUPLE_COST = 100
整体代价 = IO 代价 + CPU 代价 = 155
</code></pre>
<p>这个代价和我们在执行计划中看到的代价完全一致，说明我们的计算是正确的（或者说是符合 PostgreSQL 代价模型的）。</p>
<p>虽然 STUDENT 表上有主键索引，但是上面的查询没有选择索引扫描的方式，而是选择了顺序扫描的方式。简单来看，由于要访问全表的数据，O(N) 的时间复杂度是逃不过去的，因而还不如直接访问数据来得痛快——索引扫描需要首先扫描索引项，然后再由索引项去访问数据，这种代价就比较高了。</p>
<p>在数据库中建索引，本质上是对数据的预处理，是一种空间换时间的概念。新建的索引需要占用磁盘空间，还需要在用户写入数据的时候保证索引的数据和表中的数据一致，维护的代价也是很高的。但是它能提高查询的效率，尤其是在查询中含有约束条件的时候。</p>
<p>约束条件本质上是对数据的过滤，由于索引是“预处理”过的数据，它的分布符合一定的规则，加上约束条件就可能用的上了。但是，也并非有约束条件就会进行索引扫描，例如下面的语句中虽然有约束条件，但是执行计划中仍然是顺序扫描：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 0;
                          QUERY PLAN
--------------------------------------------------------------
 Seq Scan on student  (cost=0.00..180.00 rows=10000 width=11)
   Filter: (sno &gt; 0)
(2 rows)
</code></pre>
<p>显然，加上了约束条件之后上面的查询仍然没有用上索引扫描，最终还是选择使用 SeqScan，这是因为 SNO &gt; 0 这个约束条件的<strong>选择率</strong>太高了，我们看一下符合 SNO &gt; 0 的约束条件有多少条，我们在表中插入的 10000 条数据全部满足 SNO &gt; 0，也就是选择率是 100%。</p>
<p>这个约束条件有和没有一个样，它一条元组都没筛选掉，优化器仍然会选择 SeqScan。但需要注意的是，代价变高了，加上约束条件之后，执行计划的代价变成了 180，这是因为约束条件在执行时也需要代价，已知：</p>
<pre><code>postgres=# SHOW CPU_OPERATOR_COST;
 cpu_operator_cost
-------------------
 0.0025
(1 row)

postgres=# SELECT proname, procost FROM PG_PROC WHERE proname = 'int4gt';
 proname | procost
---------+---------
 int4gt  |       1
(1 row)
</code></pre>
<p>SNO &gt; 0 对应的应该是一个操作符，对应到函数应该是 int4gt 函数。每个数据库的系统函数都保存在 PG_PROC 系统表中，PG_PROC 系统表中的 procost 列是用来调节这个函数的执行代价的。 CPU_OPERATOR_COST 是表达式执行的基准代价，而不同的函数可能执行的代价不同，就需要借用 procost 来表示这个函数执行需要“多少个基准代价”来表示。</p>
<pre><code>int4gt 函数针对每个元组的代价 = CPU_OPERATOR_COST * procost = 0.0025
所有的元组都要执行 int4gt 函数的代价 = 10000 * 0.0025 = 25

顺序扫描 + 约束条件执行的总代价 = 155 + 25 = 180
</code></pre>
<p>为了能让优化器选择索引扫描，我们尝试一个比较低的选择率尝试一下：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 9999;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..8.30 rows=1 width=11)
   Index Cond: (sno &gt; 9999)
(2 rows)
</code></pre>
<p>SNO 属性的最大值是 10000，那么 SNO &gt; 9999 就是一个非常低的选择率了，也就是万分之一的选择率。因此这时候就会执行索引扫描了，试着对比一下 SNO &gt; 9999 的情况下选择 SeqScan 和 IndexScan 的不同：</p>
<ul>
<li>如果选择了 SeqScan，扫描 STUDENT 表上所有的元组，看一下每条元组中的 SNO 是否大于 9999，时间复杂度是 O(N)；</li>
<li>如果选择了 IndexScan，通过 B 树索引来查找 SNO &gt; 9999 的元组，时间复杂度和 SNO &gt; 9999 的选择率有关。</li>
</ul>
<p>通过二分法很容易就能找到所谓的临界点：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 5032;
                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on student  (cost=0.00..180.00 rows=4968 width=11)
   Filter: (sno &gt; 5032)
(2 rows)

postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 5033;
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..178.21 rows=4967 width=11)
   Index Cond: (sno &gt; 5033)
(2 rows)
</code></pre>
<p>那么为什么会有这样的临界点呢？这是因为顺序扫描使用的是 SEQ_PAGE_COST 来计算 IO 代价，而索引扫描采用的是 RANDOM_PAGE_COST 来计算 IO 代价：</p>
<pre><code>postgres=# SHOW RANDOM_PAGE_COST;
 random_page_cost
------------------
 4
(1 row)
</code></pre>
<p>我们把 SEQ_PAGE_COST 称为顺序 IO，把 RANDOM_PAGE_COST 称为随机 IO，“顺序IO”和“随机IO”是相对应的，从基准代价的定义可以看到这二者之间相差 4 倍，造成这种差距主要有如下两个原因。</p>
<ul>
<li>目前的存储介质大部分仍然是机械硬盘，机械硬盘的磁头在获得数据库的时候需要付出寻道时间。如果要读写的是一串在磁盘上连续的数据，就可以节省寻道时间，提高 IO 性能；而如果随机读写磁盘上任意扇区的数据，那么会有大量的时间浪费在寻道上。</li>
<li>大部分磁盘本身带有缓存，这就形成了主存→磁盘缓存→磁盘的三级结构。在将磁盘内容加载到内存的时候，考虑到磁盘的 IO 性能，磁盘会进行数据的预读，把预读到的数据保存在磁盘的缓存中。也就是说如果用户只打算从磁盘读取 100 字节的数据，磁盘可能会连续读取磁盘中的 512 字节（不同的磁盘预读的数量可能不同），并将其保存到磁盘缓存。如果下一次是顺序读取 100 字节之后的内容，那么预读的 512 字节的数据就会发挥作用，性能会大大地增加。而如果读取的内容超出了 512 字节的范围，那么预读的数据就没有发挥作用，磁盘的 IO 性能就会下降。</li>
</ul>
<p>寻道时间和预读是否命中对查询的性能影响还是非常大的，最明显的对比就是顺序扫描（SeqScan）和索引扫描（IndexScan）这两种路径，SeqScan 是对数据从头至尾地遍历。PostgreSQL 数据库的表的数据以堆的方式存储，可以假设这个表的数据在磁盘上是连续的，因此顺序扫描的 IO 代价是 SEQ_PAGE_COST。而索引扫描则不然，以 B 树索引为例，B 树上的叶子结点保存了表中每个元组的 ItemId。我们在索引扫描时是对 B 树的叶子结点进行顺序扫描，但是我们每获得一个叶子结点，都要去读取叶子结点中的 ItemId 对应的元组，这个操作是一个随机 IO 操作，因此索引扫描在代价计算的时候需要考虑 RANDOM_PAGE_COST。</p>
<p>顺序 IO 和随机 IO 的值并非一成不变。例如固态硬盘正在逐步取代机械硬盘，那么顺序 IO 的代价和随机 IO 的代价是否还有 4 倍的差距就值得商榷了，这就需要数据库的使用者根据硬件环境来灵活地调整这些基础的代价值，我们尝试把 SEQ_PAGE_COST 的值调整成 10000，然后再来查看执行计划：</p>
<pre><code>postgres=# SET SEQ_PAGE_COST = 10000;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 0;
                                      QUERY PLAN
--------------------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..540403.29 rows=10000 width=12)
   Index Cond: (sno &gt; 0)
(2 rows)

postgres=# EXPLAIN SELECT * FROM STUDENT;
                           QUERY PLAN
-----------------------------------------------------------------
 Seq Scan on student  (cost=0.00..550100.00 rows=10000 width=12)
(1 row)
</code></pre>
<p>从上面的执行计划可以看出，即使 SEQ_PAGE_COST 调整成了非常大的值，但是在没有约束条件的情况下（或者说没有和索引匹配的约束条件）也不会选择索引扫描路径，这是因为优化器在生成索引扫描路径的时候必须先要验证有没有和索引匹配的约束条件。比如 STUDENT 表上有 SNO &gt; 0 这样的约束条件，同时也有STUDENT_PKEY(SNO) 这样的主键索引，这样的约束条件和索引就是匹配的。</p>
<p>我们知道可以强制给执行计划加上 Gather 结点，由此我们也可以看一下和并行相关的代价计算，通过force_parallel_mode 参数强制加 Gather 结点之后，执行计划改变如下：</p>
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
<p>用户可以调整和并行相关的代价基准因子来调整并行代价的计算：</p>
<pre><code>postgres=# show parallel_setup_cost;
 parallel_setup_cost
---------------------
 1000
(1 row)

postgres=# show parallel_tuple_cost;
 parallel_tuple_cost
---------------------
 0.1
(1 row)
</code></pre>
<p>那么 Gather 结点的代价 2155.00 的计算方法就是：</p>
<pre><code>扫描的代价 = 155.00
启动并行进程并通信的代价 = 1000
每条元组的通信及处理代价 = 0.1
要处理的元组数 = 10000

Gather 结点的代价 = 155 + 1000 + 10000*0.1 = 2155
</code></pre>
<p>用户可以通过降低 parallel 的基准代价来使数据库更倾向于选择并行计划：</p>
<pre><code>postgres=# set force_parallel_mode = off;
SET
postgres=# set parallel_setup_cost = 0;
SET
postgres=# set parallel_tuple_cost = 0;
SET
postgres=# EXPLAIN SELECT * FROM STUDENT;
                                QUERY PLAN
---------------------------------------------------------------------------
 Gather  (cost=0.00..96.67 rows=10000 width=12)
   Workers Planned: 2
   -&gt;  Parallel Seq Scan on student  (cost=0.00..96.67 rows=4167 width=12)
(3 rows)
</code></pre>
<h3 id="-1">索引扫描代价</h3>
<p>反过来我们再来看看索引扫描的代价计算过程，比如下面这个语句：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE SNO &gt; 7000;
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..140.78 rows=3000 width=12)
   Index Cond: (sno &gt; 7000)
(2 rows)
</code></pre>
<p>索引扫描的代价计算过程分成两部分：</p>
<ul>
<li>扫描索引项（索引元组）的代价</li>
<li>扫描堆表的代价</li>
</ul>
<p>由于 PostgreSQL 数据库提供了多种索引类型，因此不同类型的索引也提供了不同的扫描索引项的代价计算函数。在老版本的 PostgreSQL 中，这个接口是暴露出来的，但是新版本的 PostgreSQL 已经把这个版本收归己有了。当然我们也不关心这样的函数是怎么实现的，我们来看一下像主键索引——也就是 B 树索引是如何计算扫描索引项的代价的。</p>
<p>已知索引相关的内容如下：</p>
<pre><code>--索引的树高
postgres=# select level from bt_metap('student_pkey');
 level
-------
     1
(1 row)

postgres=# SHOW CPU_INDEX_TUPLE_COST;
 cpu_index_tuple_cost
----------------------
 0.005
(1 row)

postgres=# SHOW CPU_OPERATOR_COST;
 cpu_operator_cost
-------------------
 0.0025
(1 row)
</code></pre>
<p>如果要访问一个索引项，则需要首先在树上进行搜索，在树上进行搜索的过程就是将跟索引匹配的约束条件和 B 树上的页面结点中的索引项进行匹配的过程。如果索引上有 N 个元组，那么可以认为需要进行 Log(N)/Log(2) 次比较（也就是以 2 为底取 N 的对数）：</p>
<pre><code>N = 10000 条记录
比较的代价 = log(N)/log(2) * cpu_operator_cost = 0.035
</code></pre>
<p>另外，虽然通常假设 B 树的页面结点是不会产生磁盘 IO 的（因为使用频繁且数量少，可以假设这些页面一直在主存里），但是同一个索引在不同的时期所产生的扫描代价也不相同。经过长时间的蹂躏，索引中会出现很多半满的页面（甚至空页面），这些索引我们叫它“膨胀”的索引，这和新建的索引带来的消耗显然是不同的。“膨胀”索引的 B 树高度应该是高于“非膨胀”索引的，PostgreSQL 使用树高来计算读取页面产生的代价，这样就能区分膨胀的索引和非膨胀的索引在扫描时的代价误差。</p>
<pre><code>B 树页面的代价 = (level + 1) * 50 * cpu_operator_cost = 0.25
注：请不要问我 50 是什么意思，这是 PostgreSQL 拍脑袋定下来的
注：当前树的高度是 1，但是 PostgreSQL 在树的上面还有一层 root 结点，所以要 + 1
</code></pre>
<p>需要注意的是，上面计算的这两个代价都是在返回第一条元组之前的，所以它们属于启动代价。我们从执行计划里面也可以看到 0.25 + 0.035 = 0.285 ≈ 0.29，执行计划中的启动代价 0.29 是 0.285 做四舍五入的结果。</p>
<p>我们计算这些启动代价是基于 B 树的非叶子结点的，是查找 7000 这个学号的代价。一旦找到学号为 7000 的索引项，由于 PostgreSQL 的 B 树的叶子结点是链表结构，因而通过扫描叶子结点就可以获得 SNO &gt; 7000 的索引项，7000 之后共有 3000 个索引项，每个索引项实际上都是一个索引元组，这些索引元组的访问代价可以这样计算：</p>
<pre><code>每个索引元组的代价 = cpu_index_tuple_cost
每个元组应用约束条件的代价 = cpu_operator_cost（注：只有一个约束条件）
所有元组的处理的总代价 = （cpu_index_tuple_cost + cpu_operator_cost） * 3000
    = 0.0075 * 3000 = 22.5
</code></pre>
<p>另外索引共用了 56 个页面：</p>
<pre><code>postgres=# SELECT RELPAGES, RELTUPLES FROM PG_CLASS WHERE RELNAME = 'student_pkey';
 relpages | reltuples
----------+-----------
       56 |     10000
(1 row)
</code></pre>
<p>按照选择率计算，访问索引需要处理的页面数为：</p>
<pre><code>56 * 3000 / 10000 = 17 个页面
访问索引页面的代价为 = 17 * random_page_cost = 68
访问索引的总代价 = 68 + 22.5 = 90.5
</code></pre>
<p>在计算完索引扫描的代价之后，就可以计算访问堆表部分的代价了，我们先来看一下访问堆表的 IO 代价。在介绍表的统计信息的时候，我们介绍了统计信息中有一个相关系数，相关系数记录了数据在堆表中的顺序和它排序之后的顺序之间的相关性。假如相关系数是 1，那么就是完全相关，这时候索引扫描访问堆表时就可以看做是顺序 IO，因为索引中的数据项的顺序和堆表上的元组的顺序完全一样。如果相关系数是 0，那么就是完全负相关，也就是说堆表的访问完全是随机 IO，因此 PostgreSQL 显式对堆表的扫描估计了“最大 IO”和“最小 IO”，然后综合相关系数进行计算。计算最大 IO 和最小 IO 需要回答下面几个问题：</p>
<pre><code>1. 索引扫描要访问多少堆上的页面呢？
    最大 IO 可以假设它要访问所有的堆页面（这里做了简化，PostgreSQL 采用了一些算法来计算，我们这里简单的假设采用所有的页面，比如极端情况下，每个堆页面里都有索引项对应的元组），也就是 55 个页面，而最小 IO 则可以假设数据是紧凑的，它只需要访问 30% 的页面，也就是 17 个页面。

2. 访问每个页面采用哪种基准代价呢？
    最大 IO 可以采用 random_page_cost，而最小 IO 的第一个页面使用 random_page_cost，其他的页面采用 seq_page_cost。

3.相关系数如何使用？
    PostgreSQL 使用了相关系数的平方，也就是判定系数来代表这种相关性，查询 PG_STATISTIC 表可以知道统计信息为 1（这是因为我们是用 generate_series 生成的数据，数据插入之后就没有做过更新，因此在磁盘上恰好是有序的）。
    postgres=# SELECT stakind2, stanumbers2 FROM PG_STATISTIC WHERE STARELID = (SELECT OID FROM PG_CLASS WHERE RELNAME = 'student') AND STAAT
     stakind2 | stanumbers2
    ----------+-------------
            3 | {1}
    (1 row)


因此：

最大 IO = 55 * random_page_cost = 220
最小 IO = random_page_cost + (17 - 1) * seq_page_cost = 20
判定系数 = 相关系数 * 相关系数 = 1

IO 代价 = 最大 IO + 判定系数 * （最小 IO - 最大 IO） = 20
</code></pre>
<p>CPU 代价的计算就比较简单了，因为选择率为 0.3，所以要处理的元组数是 3000 个，因此 CPU 代价是：</p>
<pre><code>CPU 代价 = 3000 个元组 * cpu_tuple_cost = 30
</code></pre>
<p>因此：</p>
<pre><code>执行计划的总代价 = 启动代价 + 扫描索引的代价 + 扫描堆表的代价 = 0.285 + 90.5 + 20 + 30 = 140.785
</code></pre>
<pre><code>    
</code></pre>
<h3 id="-2">小结</h3>
<p>PostgreSQL 的代价模型主要是 IO 代价和 CPU 代价，这两部分通常是分开计算的。IO 代价一般是基于页面计算的，页面是顺序 IO 还是随机 IO 往往决定了 IO 代价的大小。而CPU 代价是基于元组计算的，在不同的选择率之下，要进行表达式计算的元组数量不同，也就导致了 CPU 代价的不同。</p></div></article>