---
title: PostgreSQL 优化器入门-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过统计信息，代价估算系统就可以了解一个表有多少行数据、用了多少个数据页面、某个值出现的频率等，然后根据这些信息计算出一个约束条件能过滤掉多少数据，这种约束条件过滤出的数据占总数据量的比例称为“选择率”。</p>
<pre><code>选择率 = 筛选之后所剩的元组数量 / 筛选之前的元组数量
</code></pre>
<h3 id="io">选择率与随机 IO 的关系</h3>
<p>获得了统计信息之后，在代价估算的时候就可以利用这些统计信息进行计算，比如可以借用统计信息计算约束条件的选择率：</p>
<pre><code>--STUDENT 表中需要多些数据
DELETE FROM STUDENT;
INSERT INTO STUDENT SELECT GENERATE_SERIES(1,10000), LEFT(RANDOM()::TEXT, 10), 1;
ANALYZE STUDENT;

--选择率高，采用顺序扫描的方法获取数据
postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &gt; 2;
                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on student  (cost=0.00..224.00 rows=9999 width=10)
   Filter: (sno &gt; 2)
(2 rows)

--选择率低，采用索引扫描的方法获取数据
postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sno &lt; 2;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 Index Scan using student_pkey on student  (cost=0.29..8.30 rows=1 width=10)
   Index Cond: (sno &lt; 2)
(2 rows)
</code></pre>
<p>通过示例可以看出，在选择率高的情况下查询路径选择了顺序扫描（SeqScan）的方式，在选择率低的情况下查询路径选择了索引扫描（IndexScan）。这是因为对于索引扫描而言，它产生了“随机读”，PostgreSQL 数据库中堆表的数据是无序的，而主键索引则以 B 树的方式进行存储。B 树的叶子结点是有序的，如果通过顺序扫描（SeqScan）的方式对 STUDENT 表进行遍历，则需要对每一个 STUDENT 表中的元组应用约束条件，筛选出符合约束条件的元组作为结果。如果通过索引扫描的方式，则可以借助 B 树索引的有序性，快速定位索引项的位置，每一个索引项都有一个堆元组的“地址”，这个“地址”指向了该索引项对应的 STUDENT 表中的元组。因为索引项是有序的，而 STUDENT 表中的元组是无序的，所以这时就产生了随机读。</p>
<div style="text-align:center">
<img src="http://file.ituring.com.cn/Original/1810b30e63aa1f10ff3d" width="500px" /></div>
<p></br></p>
<p>而在 PostgreSQL 数据库中对于顺序读和随机读定义了不同的代价。</p>
<pre><code>SEQ_PAGE_COST  1.0       //顺序读的单页代价
RANDOM_PAGE_COST  4.0    //随机读的单页代价
</code></pre>
<p>如果选择率比较高，那么随机读的代价累计起来就很可观了。因此在选择率高的情况下会选择顺序扫描，而当选择率比较低时，顺序扫描仍然要把整个表的数据过滤一遍。索引扫描的单个随机读代价虽然高，但总量远远小于顺序读的数据量，因此顺序读的累计的代价就会超过索引扫描的代价，这时就会选择索引扫描作为执行路径。</p>
<h3 id="">选择率计算的示例</h3>
<p>古人云“兵马未动，粮草先行”，统计信息和选择率都是代价估算过程中的“粮草”，在开始物理优化的源代码分析之前，我们先来分析一下统计信息的获取过程和选择率的计算过程。</p>
<p>选择率是通过约束条件过滤之后保留的元组数占约束条件过滤之前的元组数的比例，选择率的估计需要借助于统计信息，对统计信息我们已经进行了介绍，它包括直方图、高频值、NULL 值率等，我们可以根据这些特征来估算选择率，比如我们先看一个执行计划：</p>
<pre><code>postgres=# INSERT INTO TEST_A SELECT I,I,I,I FROM GENERATE_SERIES(1,10000) I;
INSERT 0 10000

postgres=# ANALYZE TEST_A;
ANALYZE

postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 5500;
                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..180.00 rows=4500 width=16)
   Filter: (a &gt; 5500)
(2 rows)
</code></pre>
<p>通过 INSERT 语句可以知道我们向 TEST_A 表插入了 10000 行数据，从 SELECT 语句可以看到它有一个过滤条件是 a &gt; 5500，从执行计划可以看出经过筛选之后获得的元组数量是 4500，恰好是我们所想要的，也就是说 a &gt; 5500 的选择率是 0.45。</p>
<p>之所以能如此精确地计算出选择率，一方面是因为我们在插入数据之后，马上进行了 ANALYZE，也就是刷新了 TEST_A 表的统计信息，另一方面是因为我们这个表的数据比较“简单”，易于统计。</p>
<p>我们通过统计信息看一下 TEST_A 表的 a 列的分布情况：</p>
<pre><code>postgres=# select * from pg_statistic where starelid = (select oid from pg_class where relname = 'test_a') and staattnum = 1;
 starelid | staattnum | stainherit | stanullfrac | stawidth | stadistinct | stakind1 | stakind2 | stakind3 | stakind4 | stakind5 | staop1 | staop2 | staop3 | staop4 | staop5 | stanumbers1 | stanumbers2 | stanumbers3 | stanumbers4 | stanumbers5 |                                                                                                                                                                                                                                                   stavalues1                                                                                                                                                                                                                                                    | stavalues2 | stavalues3 | stavalues4 | stavalues5
----------+-----------+------------+-------------+----------+-------------+----------+----------+----------+----------+----------+--------+--------+--------+--------+--------+-------------+-------------+-------------+-------------+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+------------+------------+------------
    16403 |         1 | f          |           0 |        4 |          -1 |        2 |        3 |        0 |        0 |        0 |     97 |     97 |      0 |      0 |      0 |             | {1}         |             |             |             | {1,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,4500,4600,4700,4800,4900,5000,5100,5200,5300,5400,5500,5600,5700,5800,5900,6000,6100,6200,6300,6400,6500,6600,6700,6800,6900,7000,7100,7200,7300,7400,7500,7600,7700,7800,7900,8000,8100,8200,8300,8400,8500,8600,8700,8800,8900,9000,9100,9200,9300,9400,9500,9600,9700,9800,9900,10000} |            |            |            |
(1 row)
</code></pre>
<p>可以看到里面有两种类型的统计信息，一种统计信息是相关系数，这种统计信息在计算选择率的时候没什么用；另一种统计信息是直方图，由于我们插入的数据既均衡又平坦，所以这个直方图能很好地表现出现有的数据分布，因此通过直方图获得的选择率也非常准确。</p>
<p>这里只是一个比较简单的情况，我们看一个稍稍复杂一些的情况，比如约束条件中包含多个子约束条件的情况，则需要借助概率的方法，已知基于独立事件的概率的加法和乘法的公式为：</p>
<pre><code>P(A + B) = P(A) + P(B) − P(AB)
P(AB) = P(A) × P(B)
</code></pre>
<p>假设我们有一个 STUDENT 表，向表中写入如下的数据：</p>
<pre><code>--向 STUDENT 表插入一些数据
insert into student values(1, 'zs', 1);
insert into student values(2, 'ls', 1);
insert into student values(3, 'ww', 1);
insert into student values(4, 'zl', 1);
insert into student values(5, 'zs', 2);
insert into student values(6, 'ls', 2);
insert into student values(7, null, null);
</code></pre>
<p>再假如执行 SQL 语句 SELECT * FROM STUDENT WHERE sname = 'ww' AND (ssex IS NOT NULL OR sno &gt; 5)，其中 sname = 'ww' AND (ssex IS NOT NULL OR sno &gt; 5) 是由 3 个子约束条件拼接起来的一个完整的约束条件。对于这个约束条件，会分别计算 （sname = 'ww'）、（ssex IS NOT NULL）、（sno &gt; 5） 三个子约束条件的选择率，然后根据其中的 AND 运算符和 OR 运算符再计算总的选择率。
其中 （sname = 'ww'） 的选择率的计算过程如下所示。</p>
<ul>
<li>获得 sname 列对应的 stanullfrac = 0.142857。</li>
<li>获得高频值数组 {0.285714,0.285714}，计算高频值的总比例 = 0.285714＋0.285714 = 0.571428。</li>
<li>因为 sname='ww' 既不是高频值，也不是 NULL 值，所有的元组的总比例是 1，因此可以先去除 NULL 值和高频值，计算其余的元组所占的比例 = 1 − 0.142857 − 0.571428 = 0.285714。</li>
<li>计算除了NULL值和高频值，剩下还有几个值：其中元组数量 = 7，stadistinct = −0.571429，可以获得去除 NULL 值并消重之后，还剩 7×0.571429 = 4 个元组，这 4 个元组中还有两个高频值，从 4 个元组中去掉两个高频值，也就是说还有 2 个值。</li>
<li>假设两个值平均分配选择率，可以获得 sname = 'ww' 的选择率是 0.285714/2 = 0.142857。</li>
</ul>
<p>其中（ssex IS NOT NULL）的选择率的计算过程如下所示。</p>
<ul>
<li>获得 ssex 列对应的 stanullfrac = 0.142857，这些对应的是 NULL 值的选择率。</li>
<li>非 NULL 值的选择率即为 1 − stanullfrac = 1 − 0.142857 = 0.857142。</li>
</ul>
<p>其中（sno &gt; 5）的选择率计算过程如下所示。</p>
<ul>
<li>根据 sno 属性的直方图 {1,2,3,4,5,6,7} 计算 sno &lt;= 5 的选择率，直方图是左闭右开区间，即 [1，2)，[2，3)… 因此 sno &lt;5 共占了 4 个桶，共有 6 个桶，选择率是 0.6666666666666666。虽然 sno=5 则位于 [5，6) 这个桶内（也就是说位于第 5 个桶），但由于 5 是边界值，所以这部分选择率没有被计算入内。</li>
<li>根据 sno <= 5 的选择率计算 sno > 5 的选择率 = 1 – 0.6666666666666666 = 0.3333333333333333。</li>
</ul>
<p>在计算了每个子约束条件独立的选择率之后，就可以根据 AND 运算符和 OR 运算符计算它们的综合的选择率。 AND 运算符和 OR 运算符的选择率计算是基于概率的，已知基于独立事件的概率的加法和乘法的公式为：</p>
<p>可以首先获得约束条件 (ssex IS NOT NULL OR sno &gt; 5) 的选择率为：</p>
<pre><code>P(ssex IS NOT NULL OR sno &gt; 5) 
  = P(ssex IS NOT NULL) + P(sno &gt; 5) – P(ssex IS NOT NULL AND sno &gt; 5)
  = P(ssex IS NOT NULL) + P(sno &gt; 5) – P(ssex IS NOT NULL) × P(no &gt; 5)
  = 0.857142 + 0.333333 − 0.857142 × 0.333333
  = 0.90476
</code></pre>
<p>然后可以获得 sname = 'ww' AND (ssex IS NOT NULL OR sno &gt; 5) 的总的选择率为：</p>
<pre><code>P(sname = 'ww' AND (ssex IS NOT NULL OR sno &gt; 5))
  = P(sname = 'ww') × P(ssex IS NOT NULL OR sno &gt; 5) 
  = 0.142857 × 0.90476
  = 0.129252
</code></pre>
<p>因为 STUDENT 表中目前有 7 个元组，因此这个查询最终可能获得的结果集有 7 × 0.129252 ≈ 1 条元组，通过执行计划也可以看出的确是 1 条元组：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM STUDENT WHERE sname = 'ww' AND (ssex IS NOT NULL OR sno &gt; 5);
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Seq Scan on student  (cost=0.00..55.10 rows=1 width=11)
   Filter: (((ssex IS NOT NULL) OR (sno &gt; 5)) AND ((sname)::text = 'ww'::text))
(2 rows)
</code></pre>
<p>根据示例中计算出来的选择率可以估计出查询结果是一条元组，而实际情况确实只有一条元组。这样的结果虽然看上去令人欣喜，但是请保持冷静，这里示例只是一个特例。对这样的特例的结果并不能推演出一个普遍的结论，因此不能草率地说目前选择率的计算结果一定是准确的。需要谨记的是，选择率仍然是一个估计值，因为首先我们不能保证统计信息的准确性，统计信息是基于样本的（我们的示例过于简单，样本是整个表的数据，对于数据量比较大的表，样本只是表中的一部分数据），样本是否显著对统计信息的结果有很大的影响。对一个表进行更新之后，不会立即把所有的统计信息都同步更新一遍，这时选择率的计算还依赖于旧的统计信息。另外，基于概率的计算方法也不适用于所有的情况，例如对于这样一个 SQL 语句：</p>
<pre><code>SELECT * FROM STUDENT WHERE sno = 7 AND sname IS NULL AND ssex IS NULL;
</code></pre>
<p>通过统计信息可以快速地给出 （sno = 7 AND sname IS NULL AND ssex IS NULL） 的选择率：</p>
<pre><code>P(sno = 7) = 0.142857
P(sname IS NULL) = 0.142857
P(ssex IS NULL) = 0.142857

P(sno = 7 AND sname IS NULL AND ssex IS NULL)
   = P(sno = 7) × P(sname IS NULL) × P(ssex IS NULL) 
   = 0.142857× 0.142857 × 0.142857
             = 0.002915
</code></pre>
<p>计算获得的选择率为 0.002915，约为千分之三，这样的选择率显然不能代表语句的真实选择率。这时候如果 STUDENT 表上有多列统计信息，就有可能应用到这个选择率的计算上，可能结果会更准确一些。</p>
<p>这个示例虽然看上去已经有些复杂了，但实际上还属于比较简单的情况，只是在计算的过程中忽略了一些情况。例如对于既有高频值和直方图的统计信息的列，就需要同时考虑高频值和直方图。例子中的 sno &gt; 5 没有高频值信息，只有直方图信息，所以在计算的时候就直接使用直方图就可以了，但是在实际情况中，计算的过程会比示例中复杂一些。</p>
<h3 id="-1">选择率的默认值</h3>
<p>另外，统计信息也并不能覆盖选择率计算的所有情况，并不是所有的约束条件都能使用统计信息进行选择率计算。例如带有 Param 的约束条件，如果 Param 不是常量值，就没有计算选择率的依据，这时候只能设置一个默认值，PostgreSQL 数据库设定了大量的默认值。</p>
<p><strong>DEFAULT_EQ_SEL</strong>：默认值 0.005，等值约束条件的默认选择率，例如 A = 1。</p>
<p><strong>DEFAULT_INEQ_SEL</strong>：默认值 0.3333333333333333，不等值约束条件的默认选择率，例如 A &lt; b。</p>
<p><strong>DEFAULT_RANGE_INEQ_SEL</strong>：默认值 0.005，涉及同一个属性（列）的范围约束条件的默认选择率，例如 A &gt; b AND A &lt; c。</p>
<p><strong>DEFAULT_MATCH_SEL</strong>：默认值 0.005，基于模式匹配的约束条件的默认选择率，例如 LIKE。</p>
<p><strong>DEFAULT_NUM_DISTINCT</strong>：默认值 200，对一个属性消重（distinct）之后的值域中有多少个元素，通常和 DEFAULT_ EQ_SEL 互为倒数。</p>
<p><strong>DEFAULT_UNK_SEL</strong>：默认值 0.005，对 BoolTest 或 NullText 这种约束条件的默认选择率，例如 IS TRUE 或 IS NULL。</p>
<p><strong>DEFAULT_NOT_UNK_SEL</strong>：默认值是 (1.0 − DEFAULT_UNK_SEL)，对 BoolTest 或 NullText 这种约束条件的默认选择率，例如 IS NOT TRUE 或 IS NOT NULL。</p>
<h3 id="-2">小结</h3>
<p>上面给出的选择率的示例都比较简单，示例中的约束条件都是 “COL op CONST” 的形式。但生活并不能总是一帆风顺，比如在约到 “COL1 op COL2” 的情况时，估计选择率就遇到了一些困难。在 PostgreSQL 早期版本中，这种情况就直接使用默认值取代了，但是后来也做了一些改进。比如，假如 COL1 和 COL2 上都有统计信息，那么它们的高频值统计信息是否有交集呢？如果有交集那么就对估计选择率很有用，这个计算的方法就比较复杂了，这里就不再赘述了。</p></div></article>