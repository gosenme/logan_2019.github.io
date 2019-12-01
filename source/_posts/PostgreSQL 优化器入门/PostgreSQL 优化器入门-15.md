---
title: PostgreSQL 优化器入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从这一节课开始就进入了物理优化的部分。所谓物理优化就是通过计算代价的方式来对多种可能的方法进行筛选，优胜劣汰。那么什么是代价呢？代价就是一个执行计划在执行过程中所带来的消耗。既然是数据库，数据都保存在磁盘上，那么就免不了读取磁盘带来的消耗，这种消耗可以称为 <strong>IO 代价</strong>。在 SQL 语句中需要执行各种表之间做逻辑运算，看到“运算”两个字就很容易想到 CPU，因为 CPU 是中央处理单元，所以执行计划还要考虑 <strong>CPU 代价</strong>。由于分布式计划（或者并行执行计划）对数据进行了切分，导致在执行计划之间需要传递数据，因此还需要考虑<strong>通信代价</strong>。</p>
<p>那么问题来了，这些代价如何计算呢？当然可以采用最简单的“拍脑袋大法”，比如在路径选择的时候我们就喜欢记住这样的模糊的概念：<strong>通过建索引的方式可以提高查询速度</strong>。基于此，在打算提高查询性能的时候，一拍脑袋就在一个表上建上百个索引，美其名曰用空间换时间，除了更新和插入的速度慢一点，简直没毛病。</p>
<p>但优化器的代价模型不满足于这种含糊其辞式概念，需要做“精确”的计算，于是就需要如下几个方面的信息。</p>
<ul>
<li>数据到底是什么情况？也就是说数据的分布情况，比如它占了多少个页面，有多少个元组，元组的宽度是多少，每一列里有没有 NULL 值，有没有那种重复度特别高的列（比如性别）等。</li>
<li>如何量化 IO 和 CPU 的消耗？我们都知道“距离 = 速度 × 时间”，数据分布就好比是速度，那么量化的 IO 和 CPU 消耗就好像是时间，数据分布和量化的 IO 和 CPU 消耗相乘，才能获得代价。</li>
<li>执行计划是如何执行的？假设我们知道读取一个页面需要的 IO 消耗是 1，一个表有 1000 个页面，此时执行计划选择了通过索引读取结果，很可能有一些页面就被跳过了，因此还需要知道执行计划是如何执行的才能计算代价。</li>
</ul>
<p>这节课的主要内容是介绍如何统计数据的分布情况。</p>
<h3 id="">数据分布的分类</h3>
<p>PostgreSQL 数据库最早只支持单列的统计信息，也就是说我们对一个表执行 ANALYZE 之后，它会针对这个表的每一列建立一组统计信息，这组统计信息包括如下类型。</p>
<ul>
<li><p>高频值（常见值），在一个列里出现最频繁的值，按照出现的频率进行排序，并且生成一个一一对应的频率数组，这样就能知道一个列中有哪些高频值，这些高频值的频率是多少。</p></li>
<li><p>直方图，PostgreSQL 数据库使用等频直方图来描述一个列中的数据的分布，高频值不会出现在直方图中，这就保证了数据的分布是相对平坦的。</p></li>
<li><p>相关系数，相关系数记录的是当前列未排序的数据分布和排序后的数据分布的相关性，这个值通常在索引扫描时用来估计代价。假设一个列未排序和排序之后的相关性是 0，也就是完全不相关，那么索引扫描的代价就会高一些。</p></li>
<li><p>数组高频值（常见值），用于数组类型或者一些其他类型，PostgreSQL 数据库提供了 ts_typanalyze 系统函数来负责生成这种类型的统计信息。</p></li>
<li><p>数组类型直方图，用于给数组类型生成直方图。PostgreSQL 数据库提供了 array_typanalyze 系统函数来负责生成这种类型的统计信息。</p></li>
<li><p>为 Range 类型生成一个基于长度的直方图统计信息，用户可以自定义 Range 类型，例如 CREATE TYPE floatrange AS RANGE (subtype = float8, subtype_diff = float8mi)，PostgreSQL 数据库提供了 range_typanalyze 系统函数负责生成这种类型的统计信息。</p></li>
<li><p>为 Range 类型生成一个基于边界的直方图，这种类型的直方图也通过 range_typanalyze 系统函数来进行统计；</p></li>
</ul>
<pre><code>注：高频值（MCV)、直方图、相关系数是统计模块常用的 3 种统计方式，其他统计方式和这 3 种统计方式大致上类似，但是针对的是一些特殊的类型，所以我们主要还是针对这 3 种类型进行说明。
</code></pre>
<p>PostgreSQL 除了支持单列的统计信息之外，还支持了多列的统计信息用来计算各个列之间的依赖度，它主要包括以下两种形式。</p>
<ul>
<li><p>去重统计信息，和单列统计信息中的 stadistinct 是类似的，stadistinct 中记录的是单列中去掉 NULL 值和消重之后的数据量或者比例。STATS_EXT_NDISTINCT 类型的统计信息则记录的是基于多列的消重之后的数据量。</p></li>
<li><p>依赖统计信息，计算各个列之间的函数依赖度，通过函数依赖度计算各个列之间的依赖关系，从而得到准确的统计信息。</p></li>
</ul>
<p>另外，PostgreSQL 数据库在 PG_CLASS 系统表中会保存两个统计信息，分别是 relpages 和 reltuples。relpages 记录了当前表占用了多少个页面，reltuples 记录了当前表共有多少条元组。relpages 中记录的值是一个精确值，也就是说统计信息生成的时候会真的统计这个表所占的页面数量，而元组数则是一个估计值，通常采用 EMA（指数平均数指标）方法来对表中元组的密度（每个页面有多少元组）进行估计，最终获得最新的元组密度（updated_density）。</p>
<pre><code>old_density = old_rel_tuples / old_rel_pages;
new_density = scanned_tuples / scanned_pages;
multiplier = (double) scanned_pages / (double) total_pages;
updated_density = old_density + (new_density - old_density) * multiplier;
</code></pre>
<p>那么为什么页面数是精确值而元组数量为估计值呢？这是因为 PostgreSQL 中每个表的数据都保存在一个文件里，而文件又是由页面组织起来的。每个页面的大小是固定的，默认是 8K，这样就能根据文件大小和页面大小快速得到一个表有多少个页面。而元组数就不同了，元组的长度是不确定的（可能有变长的列，比如 Varchar）。即使元组的长度是确定的，也不行，因为不是每个页面中都放满元组，我们删除元组的时候可能会使一个页面中出现“空洞”，也就是说没有办法直接计算精确的元组数量。当然，如果我们一条一条地统计也是能得到页面中的元组数量的，但是这需要的代价偏高，对于数据量小的表还好，数据量很大就需要非常多时间。因此，可以估计一个页面内的元组密度，这个密度是一个平均值，通过密度和页面数量估算出元组的数量。</p>
<h3 id="-1">统计信息示例</h3>
<p>统计信息的生成是通过采样数据来生成的，也就是从一个表中抽样出来一部分数据作为样本，样本是否显著就决定了统计信息是否准确。PostgreSQL 使用了两阶段采样，第一个阶段是对页面进行采样。因为页面的数量是精确的，所以采用随机的方法采样就可以了。第二个阶段是从获得的采样页面中再次采样元组。由于元组的数量是不精确的，因而采用的是蓄水池算法进行采样。无论采用什么样的采样算法，总会有统计的偏差存在，通常我们可以通过调整 default_statistics_target 参数来设定样本的容量。</p>
<p>如果用户要给某一个表生成统计信息，可以使用 ANALYZE 语句对一个表进行统计分析，这样就能给这个表生成统计信息并且保存在 PG_STATISTIC 系统表中。</p>
<p>下面主要看一下 PG_STATISTIC 系统表的统计信息的组织形式。以 STUDENT 表为例，我们向 STUDENT 表插入一些数据，然后对 STUDENT 表执行 ANALYZE 操作。由于 STUDENT 表有 3 个列属性，因此执行 ANALYZE 操作之后会在 PG_STATISTIC 系统表中给 STUDENT 表生成 3 行统计信息。</p>
<pre><code>--向 STUDENT 表插入一些数据
insert into student values(1, 'zs', 1);
insert into student values(2, 'ls', 1);
insert into student values(3, 'ww', 1);
insert into student values(4, 'zl', 1);
insert into student values(5, 'zs', 2);
insert into student values(6, 'ls', 2);
insert into student values(7, null, null);

--对 STUDENT 表做统计
ANALYZE STUDENT;

--查询 STUDENT 表的 relpages 和 reltuples 信息
--可以看出占用了 1 个页面，该表共有 7 条元组
postgres=# ANALYZE student;
ANALYZE
postgres=# SELECT relname, relpages, reltuples FROM PG_CLASS WHERE relname = 'student';
 relname | relpages | reltuples
---------+----------+-----------
 student |        1 |         7
(1 row)

--查询 PG_STATISTIC 表中和 STUDENT 表相关的统计信息，其中 24587 是 STUDENT 表的 OID
--staattnum 中的 1、2、3 分别对应 STUDENT 表中的 3 个列
postgres=# SELECT relname, staattnum, stanullfrac, stawidth, stadistinct  FROM PG_STATISTIC, PG_CLASS WHERE starelid = 'student'::regclass AND starelid = PG_CLASS.oid;
 relname | staattnum | stanullfrac | stawidth | stadistinct
---------+-----------+-------------+----------+-------------
 student |         1 |           0 |        4 |          -1
 student |         2 |    0.142857 |        3 |   -0.571429
 student |         3 |    0.142857 |        4 |   -0.285714
(3 rows)
</code></pre>
<p><strong>starelid/staattnum</strong>：对应的表的 OID（来自 PG_CLASS）和列的编号（来自 PG_ATTRIBUTES），其中 sno、sname、ssex 这 3 个属性的编号分别是 1、2、3。</p>
<p><strong>stanullfrac</strong>：NULL 值率，表示一个属性（列）里 NULL 值所占的比例，如示例所示，STUDENT 表的sname 和 ssex 两个列中各有一个 NULL 值，因此它们 NULL 值率都是 1/7 = 0.142857。</p>
<p><strong>stawidth</strong>：计算该属性（列）的平均宽度，STUDENT 表的第一个属性 sno 是 INT 类型。INT 类型是定长类型，它的宽度是 4；而 STUDENT 表的第二个属性 sname 是变长的类型，它的宽度是所有值的平均宽度。虽然 sname 的类型是 VARCHAR(10)，但是实际上我们插入的值全部长度都是 2，再加上 VARCHAR 类型的 Header 的 1 个字节的长度，可以获得它的平均宽度是 3。</p>
<p><strong>stadistinct</strong>：计算该属性消重之后的数据的个数或比例，stadistinct 的取值有 3 种情况：</p>
<ul>
<li>= 0，代表未知或者未计算的情况</li>
<li>> 0，代表消除重复值之后的个数，不常使用这种情况</li>
<li>&lt; 0，其绝对值是去重之后的属性个数占总个数的比例，通常使用这种情况</li>
</ul>
<p>STUDENT 表的第二列共有 7 个值，去掉 NULL 值，去掉重复值后还剩 4 个值（zs, ls, ww, zl），因此stadistinct = 4/7 = 0.571429。</p>
<p>PostgreSQL 数据库对每一个属性（列）的统计目前最多只能应用 5 种方法，因此在 PG_STATISTIC 中会有 stakind(1-5)、staop(1-5)、stanumbers[1](1-5)、stavalues(1-5)，分别是 5 个槽位。如果 stakind 不为 0，那么表明这个槽位有统计信息。第一个统计方法统计的信息首先会记录到第一个槽位（stakind1、staop1、stanumbers1[1]、stavalues1），第二个统计方法的统计信息会记录到第二个槽位（stakind2、staop2、stanumbers2[1]、stavalues2），以此类推。</p>
<p>stakind：统计信息的的形式，它的定义如下：</p>
<pre><code>STATISTIC_KIND_MCV              1  //高频值
STATISTIC_KIND_HISTOGRAM        2  //直方图
STATISTIC_KIND_CORRELATION      3  //相关系数
STATISTIC_KIND_MCELEM           4 
STATISTIC_KIND_DECHIST          5 
STATISTIC_KIND_RANGE_LENGTH_HISTOGRAM    6 
STATISTIC_KIND_BOUNDS_HISTOGRAM          7
</code></pre>
<p>在对 STUDENT 表做完统计后，STUDENT 的每个行的槽位情况如下：</p>
<pre><code>--查询STUDENT表中的每个属性所应用的方法
--STUDENT(sno)应用了2个方法，占2个槽位，分别是直方图（2）和相关系数（3）
--STUDENT(sname)应用了3个方法，占3个槽位，分别是常见值（1）、直方图（2）和相关系数（3）
--STUDENT(ssex)应用了2个方法，占2个槽位，分别是常见值（2）和相关系数（3）
postgres=# SELECT relname, staattnum, stakind1, stakind2, stakind3, stakind4, stakind5 FROM PG_STATISTIC, PG_CLASS WHERE starelid = 'student'::regclass AND starelid = PG_CLASS.oid;
 relname | staattnum | stakind1 | stakind2 | stakind3 | stakind4 | stakind5
---------+-----------+----------+----------+----------+----------+----------
 student |         1 |        2 |        3 |        0 |        0 |        0
 student |         2 |        1 |        2 |        3 |        0 |        0
 student |         3 |        1 |        3 |        0 |        0 |        0
(3 rows)
</code></pre>
<p><strong>staop</strong>：统计过程中涉及的操作符。</p>
<p><strong>stanumbers</strong>：存放统计信息的高频值数组或者存放相关系数，例如 stakind1 保存的统计信息类型是STATISTIC_KIND_MCV，那么在 stanumbers1 中保存的就是高频值数组，数组中记录的是每个高频值所占的频率值。再例如 stakind3 中保存的统计信息类型是 STATISTIC_KIND_CORRELATION，那么在stanumbers3 中保存的就是相关系数。</p>
<p><strong>stavalues</strong>：统计值的数组，如果 stakind1 保存的统计信息类型是 STATISTIC_KIND_MCV，那么在 stavalues 中保存的就是高频值对应的值，它和 stanumbers 中的高频值数组的频率值一一对应。如果stakind1 保存的统计信息类型是 STATISTIC_KIND_HISTOGRAM，那么在 stanumbers1 中保存的是直方图中的桶的信息。由于直方图是等频直方图，因此只要记录了每个桶的边界值，就可以获得每个桶的平均比例。
通过示例可以看出，不同的列使用的槽数是不同的，例如 STUDENT.sno 列和 STUDENT.ssex 列都使用了 2 个槽，而 STUDENT.sname 列则使用了 3 个槽。</p>
<p>下面可以通过查看每个槽的信息，来分析一下 STUDENT 表的数据分布情况。</p>
<p>STUDENT.sno 属性在第一个槽中保存的是直方图信息，因为 STUDENT.sno 上面有主键索引，因此它的直方图的每个桶的边界值都是平坦的。</p>
<p>STUDENT.sname 属性和 STUDENT.ssex 属性在第一个槽中保存的是 STATISTIC_KIND_MCV 形式的统计信息，以 STUDENT.sname 为例，{ls, zs} 表示在 STUDENT.sname 中这两个值出现的频率比较高，{0.285714, 0.285714} 和 {ls, zs} 一一对应，表示的是每个高频值的频率。</p>
<pre><code>--第一个槽的统计信息
postgres=# SELECT relname, staattnum, stakind1, staop1, stanumbers1, stavalues1 FROM PG_STATISTIC, PG_CLASS WHERE starelid =  'student'::regclass AND starelid = PG_CLASS.oid;
 relname | staattnum | stakind1 | staop1 |     stanumbers1     |   stavalues1
---------+-----------+----------+--------+---------------------+-----------------
 student |         1 |        2 |     97 |                     | {1,2,3,4,5,6,7}
 student |         2 |        1 |     98 | {0.285714,0.285714} | {ls,zs}
 student |         3 |        1 |     96 | {0.571429,0.285714} | {1,2}
(3 rows)
</code></pre>
<p>STUDENT.sname 属性在第二个槽中保存的是直方图信息，STUDENT.sno 和 STUDENT.ssex 属性在第二个槽中保存的是相关系数，从示例可以看出它们的相关系数都是 1，也就是说数据的分布和排序后的数据分布完全正相关，这是因为 STUDENT 表中的数据写入后没有进行过更新操作，目前在堆中保存的顺序和插入数据时的顺序是一致的，而插入数据时这两个列的数据是有序的。</p>
<pre><code>--第二个槽的统计信息
postgres=# SELECT relname, staattnum, stakind2, staop2, stanumbers2, stavalues2 FROM PG_STATISTIC, PG_CLASS WHERE starelid =  'student'::regclass AND starelid = PG_CLASS.oid;
 relname | staattnum | stakind2 | staop2 | stanumbers2 | stavalues2
---------+-----------+----------+--------+-------------+------------
 student |         1 |        3 |     97 | {1}         |
 student |         2 |        2 |    664 |             | {ww,zl}
 student |         3 |        3 |     97 | {1}         |
(3 rows)
</code></pre>
<p>STUDENT.sname 属性在第三个槽中保存的是相关系数信息，可以看出 STUDENT.sname 中的堆数据的顺序和排序后的顺序的相关系数是 0.0285714。</p>
<pre><code>--第三个槽
postgres=# SELECT relname, staattnum, stakind3, staop3, stanumbers3, stavalues3 FROM PG_STATISTIC, PG_CLASS WHERE starelid =  'student'::regclass AND starelid = PG_CLASS.oid;
 starelid | staattnum | stakind3 | staop3 | stanumbers3 | stavalues3
----------+-----------+----------+--------+-------------+------------
    24587 |         1 |        0 |      0 |             |
    24587 |         2 |        3 |    664 | {0.0285714} |
    24587 |         3 |        0 |      0 |             |
(3 rows)
</code></pre>
<p>PG_STATISTIC_EXT 系统表保存的是多列的统计信息，用户需要显式地使用 CREATE STATISTICS 语句对一个表创建多列统计信息，例如：</p>
<pre><code>postgres=# CREATE STATISTICS STATEXT_STUDENT ON sno, sname, ssex FROM STUDENT;
CREATE STATISTICS
postgres=# SELECT * FROM PG_STATISTIC_EXT WHERE stxname='statext_student';
 stxrelid |     stxname     | stxnamespace | stxowner | stxkeys | stxkind | stxndistinct | stxdependencies
----------+-----------------+--------------+----------+---------+---------+--------------+-----------------
    24587 | statext_student |         2200 |       10 | 1 2 3   | {d,f}   |              |
(1 row)
</code></pre>
<p>通过 CREATE STATISTICS 语句创建统计信息之后只是在 PG_STATISTIC_EXT 系统表中增加了一个统计信息项，这时候并没有真正对指定表上的属性去做统计分析，只有在用户对表再次执行 ANALYZE 的时候，而且 ANALYZE 的表的属性满足了多列统计信息的要求，才会生成多列统计信息。</p>
<pre><code>-- ANALYZE 语句中指定的属性和多列统计信息项 STATEXT_STUDENT 中要求的不一致
postgres=# ANALYZE STUDENT(sno, sname);
WARNING:  statistics object "public.statext_student" could not be computed for relation "public.student"
ANALYZE
-- ANALYZE 语句中指定的属性和多列统计信息项 STATEXT_STUDENT 中要求的一致
postgres=# ANALYZE STUDENT(sno, sname, ssex);
ANALYZE

postgres=# SELECT * FROM PG_STATISTIC_EXT WHERE stxname='statext_student';
 stxrelid |     stxname     | stxnamespace | stxowner | stxkeys | stxkind |                  stxndistinct                   |                                                                                        stxdependencies
----------+-----------------+--------------+----------+---------+---------+-------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    24587 | statext_student |         2200 |       10 | 1 2 3   | {d,f}   | {"1, 2": 7, "1, 3": 7, "2, 3": 7, "1, 2, 3": 7} | {"1 =&gt; 2": 1.000000, "1 =&gt; 3": 1.000000, "2 =&gt; 1": 0.500000, "2 =&gt; 3": 0.500000, "3 =&gt; 1": 0.250000, "3 =&gt; 2": 0.250000, "1, 2 =&gt; 3": 1.000000, "1, 3 =&gt; 2": 1.000000, "2, 3 =&gt; 1": 1.000000}
(1 row)
</code></pre>
<p>PG_STATISTIC_EXT 系统表中的每个属性的说明如下所示。</p>
<p><strong>stxrelid</strong>：统计信息属于哪个表</p>
<p><strong>stxname</strong>：统计信息的名字</p>
<p><strong>stxnamespace</strong>：统计信息的命名空间</p>
<p><strong>stxowner</strong>：统计信息的创建者</p>
<p><strong>stxkeys</strong>：统计哪些列</p>
<p><strong>stxkind</strong>：多列统计的类型，目前支持两种类型：</p>
<pre><code>    STATS_EXT_NDISTINCT         'd'
    STATS_EXT_DEPENDENCIES      'f'
</code></pre>
<p><strong>stxndistinct</strong>：STATS_EXT_NDISTINCT 类型的统计信息</p>
<p><strong>stxdependencies</strong>：STATS_EXT_DEPENDENCIES 类型的统计信息</p>
<h3 id="-2">小结</h3>
<p>统计信息中除了常规的高频值、直方图和相关系数之外，还有 NULL 值率，去重率等，它们主要用在计算选择率上。在 SQL 语句中经常会有诸如 “a &gt; 10” 这样的约束条件，有了 a 列的统计信息，有了表中的元组数，就能计算出这个约束条件可以过滤掉多少数据，这样就能在保留的数据上计算代价了。PostgreSQL 在频繁的增删改操作之后，会自动更新统计信息，但是，我们还是应该注意统计信息的准确性。因此，掌握解读统计信息的含义就非常重要了。</p></div></article>