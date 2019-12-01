---
title: PostgreSQL 优化器入门-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>子查询和子连接不同，它不是“表达式”，它是“表”。因此，优化器把子查询当做表来对待，从而针对子查询产生的是一个扫描路径，也就是 SubQueryScan。</p>
<h3 id="simple">SIMPLE 子查询的提升</h3>
<p>如果把子查询看做一个表，我们可以叫它“子查询表”，这个子查询表和其他表在做连接（Join）操作。子查询如果被提升，会转换成子查询中的表直接与与上层的表做连接操作。查询优化模块对表之间的连接操作的优化做了很多工作，因此可能获得更好的执行计划。PostgreSQL 提升了 3 种类型的子查询：SIMPLE 子查询、VALUES 子查询和 UNION 子查询，我们分别来看一下这 3 种子查询的提升。</p>
<p>所谓 SIMPLE 子查询，实际上就是经典的子查询。对于 SIMPLE 子查询，我们先看一下它的提升条件。首先要求子查询的类型是真的“简单”（simple）的。所谓的简单，需要满足如下条件：不能包含聚集操作、窗口函数、GROUP 操作等。在子连接提升的时候我们已经见过类似的条件，下面的例子中子查询中包含了聚集函数 avg，不能提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, (SELECT avg(a) FROM TEST_B) b;
                             QUERY PLAN
--------------------------------------------------------------------
 Nested Loop  (cost=2.25..5.27 rows=100 width=48)
   -&gt;  Aggregate  (cost=2.25..2.26 rows=1 width=32)
         -&gt;  Seq Scan on test_b  (cost=0.00..2.00 rows=100 width=4)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
(4 rows)
</code></pre>
<p>你是否感觉有点怪怪的，这个执行计划中找不到任何子查询的“标识“，那我们如何知道它没有提升呢？实际上，如果子查询没有提升，在物理优化阶段是会生成 SubqueryScan 路径的。虽然示例的执行计划中没有 SubqueryScan 这个执行路径，实际上这个物理路径是生成了的，只不过在查询优化的最后阶段——清理执行计划时又优化掉了。上面语句在物理优化阶段生成的执行计划是这样的：</p>
<pre><code>Nested Loop Join
    -&gt; SubQuery Scan
        -&gt; Aggregate
            -&gt; Seq Scan on test_b
    -&gt; Seq Scan on test_a
</code></pre>
<p>这个 SubQueryScan 在执行计划中起到什么作用呢？它的作用就是把聚集函数生成的结果“转交”给上层结点，也就是“中介”的作用。优化器痛恨这种什么都不干只收中介费的黑中介，于是在生成执行计划的最后阶段把它干掉了。所以虽然子查询没有提升，但我们也看不到子查询对应的计算结点。</p>
<p>子查询树不能是集合操作。需要注意的是，UNION ALL 操作可以当做 UNION 类型的子查询来处理，但如果是其他类型的集合操作，那就只能和提升 say goodbye 了。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, (SELECT * FROM TEST_B UNION SELECT * FROM TEST_C) bc;
                                   QUERY PLAN
---------------------------------------------------------------------------------
 Nested Loop  (cost=14.64..271.39 rows=20000 width=32)
   -&gt;  Unique  (cost=14.64..17.14 rows=200 width=16)
         -&gt;  Sort  (cost=14.64..15.14 rows=200 width=16)
               Sort Key: test_b.a, test_b.b, test_b.c, test_b.d
               -&gt;  Append  (cost=0.00..7.00 rows=200 width=16)
                     -&gt;  Seq Scan on test_b  (cost=0.00..2.00 rows=100 width=16)
                     -&gt;  Seq Scan on test_c  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=0.00..2.50 rows=100 width=16)
         -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
(9 rows)
</code></pre>
<p>如果子查询中没有指定具体的表，那么在无约束条件或者满足删除条件或者不是外连接的情况下才能提升，这是因为在物理优化阶段优化器会针对所有的表建立一个“内部的描述符”。如果它是一个子查询，我们也可以把这个子查询当成一个表，建立一个“子查询类型的内部结构“来代表它。但如果将空子查询提升上来，那么就没有合适的“内部描述符“来表示它了。下面是子查询没有指定表的例子，从执行计划可以看出，这个子查询转变成了一个 Result 结点。</p>
<pre><code>-- 有约束条件的例子，假如提升上来，不知道该如何安置这个约束条件
postgres=# EXPLAIN SELECT * FROM TEST_A, LATERAL  (SELECT 1 AS b WHERE TEST_A.A &gt; 0) bb;
                          QUERY PLAN
---------------------------------------------------------------
 Nested Loop  (cost=0.00..5.25 rows=100 width=20)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Result  (cost=0.00..0.01 rows=1 width=4)
         One-Time Filter: (test_a.a &gt; 0)
</code></pre>
<p>Lateral 语义支持在子查询中引用上一层的表。但是如果引用的是更上层的表，可能会出现问题。例如下面的语句中，如果子查询提升，TEST_A.a &gt; 1 这个约束条件的提升可能会改变查询结果。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN (TEST_B LEFT JOIN LATERAL (SELECT * FROM TEST_C WHERE TEST_A.a &gt; 1) AS c ON TRUE) ON TRUE;
                                      QUERY PLAN
-------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..809535.32 rows=5120000 width=48)
   -&gt;  Seq Scan on test_a  (cost=0.00..57.56 rows=256 width=16)
   -&gt;  Nested Loop Left Join  (cost=0.00..2962.02 rows=20000 width=32)
         -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=16)
         -&gt;  Materialize  (cost=0.00..2683.00 rows=10000 width=16)
               -&gt;  Result  (cost=0.00..2533.00 rows=10000 width=16)
                     One-Time Filter: (test_a.a &gt; 1)
                     -&gt;  Seq Scan on test_c  (cost=0.00..2533.00 rows=10000 width=16)
(8 rows)
</code></pre>
<p>另外，如果子查询的投影中包含了上层外连接的列属性，子查询也不能提升，例如下面的 SQL 语句中子查询就没有提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN (TEST_B LEFT JOIN LATERAL (SELECT *,TEST_A.a FROM TEST_C) AS c ON TRUE) ON TRUE;
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..809534.68 rows=5120000 width=52)
   -&gt;  Seq Scan on test_a  (cost=0.00..57.56 rows=256 width=16)
   -&gt;  Nested Loop Left Join  (cost=0.00..2962.02 rows=20000 width=36)
         -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=16)
         -&gt;  Materialize  (cost=0.00..2683.00 rows=10000 width=20)
               -&gt;  Seq Scan on test_c  (cost=0.00..2533.00 rows=10000 width=20)
(6 rows)
</code></pre>
<p>另外包含易失性函数之后也不能提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, (SELECT A, random() FROM TEST_B) b;
                             QUERY PLAN
---------------------------------------------------------------------
 Nested Loop  (cost=0.00..130.50 rows=10000 width=28)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=0.00..3.75 rows=100 width=12)
         -&gt;  Seq Scan on test_b  (cost=0.00..2.25 rows=100 width=12)
(4 rows)
</code></pre>
<p>上面看了很多不能提升的例子，下面我们看一个能够提升的例子：</p>
<pre><code>SELECT * FROM TEST_A a, (SELECT * FROM TEST_B b WHERE a &gt; 10) b WHERE a.a = b.a;
</code></pre>
<p>我们可以直观地判断这是一个简单的子查询：</p>
<ul>
<li>子查询中没有集合操作（如果有集合操作应该进行 UNION 子查询的提升）</li>
<li>子查询中没有聚集函数等</li>
<li>子查询中指定了具体的表</li>
<li>也没有易失性函数</li>
</ul>
<p>下面是这个 SQL 语句的执行计划：</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT * FROM TEST_A a, (SELECT * FROM TEST_B b WHERE a &gt; 10) b WHERE a.a = b.a;
                                 QUERY PLAN
----------------------------------------------------------------------------
 Hash Join  (cost=1.14..3.52 rows=1 width=32)
   Output: a.a, a.b, a.c, a.d, b.a, b.b, b.c, b.d
   Hash Cond: (a.a = b.a)
   -&gt;  Seq Scan on public.test_a a  (cost=0.00..2.00 rows=100 width=16)
         Output: a.a, a.b, a.c, a.d
   -&gt;  Hash  (cost=1.12..1.12 rows=1 width=16)
         Output: b.a, b.b, b.c, b.d
         -&gt;  Seq Scan on public.test_b b  (cost=0.00..1.12 rows=1 width=16)
               Output: b.a, b.b, b.c, b.d
               Filter: (b.a &gt; 10)
(10 rows)
</code></pre>
<p>通过观察执行计划可以看出，子查询中的表 TEST_B 提升上来和上层的表 TEST_A 做了嵌套循环连接，根据上面的执行计划可以推算等价的 SQL 语句。</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT * FROM TEST_A a, TEST_B b WHERE b.a &gt; 10 AND a.a = b.a;
                                 QUERY PLAN
----------------------------------------------------------------------------
 Hash Join  (cost=1.14..3.52 rows=1 width=32)
   Output: a.a, a.b, a.c, a.d, b.a, b.b, b.c, b.d
   Hash Cond: (a.a = b.a)
   -&gt;  Seq Scan on public.test_a a  (cost=0.00..2.00 rows=100 width=16)
         Output: a.a, a.b, a.c, a.d
   -&gt;  Hash  (cost=1.12..1.12 rows=1 width=16)
         Output: b.a, b.b, b.c, b.d
         -&gt;  Seq Scan on public.test_b b  (cost=0.00..1.12 rows=1 width=16)
               Output: b.a, b.b, b.c, b.d
               Filter: (b.a &gt; 10)
(10 rows)
</code></pre>
<p><strong>根据执行计划我们可以看出子查询的投影列和范围表都做了提升，投影列提升到上层做投影，范围表则提升到上层直接做连接操作。</strong></p>
<h3 id="simple-1">SIMPLE 子查询提升的小优化</h3>
<p>下面再看一个原来不能提升，后来又能提升的例子，假如有如下语句：</p>
<pre><code>SELECT * FROM STUDENT st LEFT JOIN (SELECT sno, COALESCE(degree,60) FROM SCORE) sc ON st.sno=sc.sno
</code></pre>
<p>假设 STUDENT 和 SCORE 表的数据如下：</p>
<pre><code>postgres=# SELECT sno, sname, ssex FROM STUDENT;
 sno     |  sname    | ssex
-----+----------+------
   1     | zhangsan  |    1
   2     | lisi      |    1
(2 rows)

postgres=# SELECT sno, cno, degree FROM SCORE;
 sno     | cno   | degree
-----+-----+--------
   1     |   1   |     36
(1 row)
</code></pre>
<p>它的执行情况如下：</p>
<pre><code>postgres=# SELECT * FROM STUDENT st LEFT JOIN (SELECT sno, COALESCE(degree,60) FROM SCORE) sc ON st.sno=sc.sno;
 sno     |  sname    | ssex  | sno   | coalesce
-----+----------+------+-----+----------
   1     | zhangsan  |    1  |   1   |       36
   2     | lisi      |    1  |       |
(2 rows)
</code></pre>
<p>用反证法，假设这个子查询是能提升的，对其进行强制提升，得到的查询结果如下：</p>
<pre><code>-- 强制提升
postgres=# SELECT st.sno, sname, ssex, sc.sno, COALESCE(degree,60) FROM STUDENT st LEFT JOIN SCORE sc ON st.sno=sc.sno;
 sno     |  sname    | ssex  | sno   | coalesce
-----+----------+------+-----+----------
   1     | zhangsan  |    1  |   1   |       36
   2     | lisi      |    1  |       |       60
(2 rows)    
</code></pre>
<p>COALESCE 函数对 NULL 值做了处理，导致外连接补的 NULL 值也被处理了，所以强制提升之后两个查询就不再等价。</p>
<p>PostgreSQL 数据库在 8.4 之前的版本对这一类子查询是不能提升的，在 8.4 版本引入开始对这种类型的子查询也进行了提升，但是它只提升表，不提升投影中的表达式：</p>
<pre><code>-- 虽然子查询提升了，但是 COALESCE(score.degree, 60) 仍然是在对 SCORE 表扫描的时候进行计算
postgres=# EXPLAIN VERBOSE SELECT * FROM STUDENT st LEFT JOIN (SELECT sno, COALESCE(degree,60) FROM SCORE) sc ON st.sno=sc.sno;
                                  QUERY PLAN
------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..250.77 rows=71 width=19)
   Output: st.sno, st.sname, st.ssex, score.sno, (COALESCE(score.degree, 60))
   Join Filter: (st.sno = score.sno)
   -&gt;  Seq Scan on public.student st  (cost=0.00..1.07 rows=7 width=11)
         Output: st.sno, st.sname, st.ssex
   -&gt;  Materialize  (cost=0.00..40.60 rows=2040 width=8)
         Output: score.sno, (COALESCE(score.degree, 60))
         -&gt;  Seq Scan on public.score  (cost=0.00..30.40 rows=2040 width=8)
               Output: score.sno, COALESCE(score.degree, 60)
(9 rows)

-- 可以看到在对 SCORE 表进行扫描的时候，直接把投影列传递给了连接操作，
-- COALESCE(sc.degree, 60) 在连接操作之后进行计算
postgres=# EXPLAIN VERBOSE SELECT st.sno, sname, ssex, sc.sno, COALESCE(degree,6
0) FROM STUDENT st LEFT JOIN SCORE sc ON st.sno=sc.sno;
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..250.77 rows=71 width=19)
   Output: st.sno, st.sname, st.ssex, sc.sno, COALESCE(sc.degree, 60)
   Join Filter: (st.sno = sc.sno)
   -&gt;  Seq Scan on public.student st  (cost=0.00..1.07 rows=7 width=11)
         Output: st.sno, st.sname, st.ssex
   -&gt;  Materialize  (cost=0.00..40.60 rows=2040 width=8)
         Output: sc.sno, sc.degree
         -&gt;  Seq Scan on public.score sc  (cost=0.00..30.40 rows=2040 width=8)
               Output: sc.sno, sc.degree
(9 rows)    
</code></pre>
<h3 id="union">UNION 子查询的提升</h3>
<p>作为 UNION ALL 联合查询，它的效果和 PostgreSQL 数据库的继承表的效果是相似的：UNION ALL 联合查询是对两边的语句的结果集进行整合，继承表则是整合子表的查询结果。</p>
<pre><code>CREATE TABLE INH_P(a INT, b TEXT);
CREATE TABLE INH_C1() INHERITS(INH_P);
CREATE TABLE INH_C2() INHERITS(INH_P);

postgres=# EXPLAIN SELECT * FROM INH_P;
                           QUERY PLAN
-----------------------------------------------------------------
 Append  (cost=0.00..45.40 rows=2541 width=36)
   -&gt;  Seq Scan on inh_p  (cost=0.00..0.00 rows=1 width=36)
   -&gt;  Seq Scan on inh_c1  (cost=0.00..22.70 rows=1270 width=36)
   -&gt;  Seq Scan on inh_c2  (cost=0.00..22.70 rows=1270 width=36)
(4 rows)    
</code></pre>
<p>我们提升 UNION 类型的子查询的主要目的是将三个层次变成两个层次，第三个层次的“子子查询”以 Append 的形式提升一层，如下面的示例所示：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM SCORE sc, (SELECT * FROM STUDENT WHERE sno =1 UNION ALL SELECT * FROM STUDENT WHERE sno=2) st WHERE st.sno &gt; 0;
                                     QUERY PLAN
--------------------------------------------------------------------------------
 Nested Loop  (cost=0.00..83.64 rows=4080 width=23)
   -&gt;  Seq Scan on score sc  (cost=0.00..30.40 rows=2040 width=12)
   -&gt;  Materialize  (cost=0.00..2.24 rows=2 width=11)
        -&gt;  Append  (cost=0.00..2.23 rows=2 width=11)
              -&gt;Seq Scan on student  (cost=0.00..1.11 rows=1 width=11)
                    Filter: ((sno &gt; 0) AND (sno = 1))
              -&gt;Seq Scan on student student_1(cost=0.00..1.11 rows=1 width=11)
                    Filter: ((sno &gt; 0) AND (sno = 2))
(8 rows) 
</code></pre>
<h3 id="values">VALUES 子查询的提升</h3>
<p>至于 VALUES 类型的子查询，它的提升分成了 2 个步骤，假设有一个 VALUES 类型的子查询语句如下：</p>
<pre><code>SELECT sname, sc.sno, sc.cno FROM STUDENT, (VALUES(1,2)) AS sc(sno, cno) WHERE sc.sno = STUDENT.sno;
</code></pre>
<p>第一个步骤是将 VALUES 转换成正式的子查询形式，而（1，2）则成了子查询的投影列：</p>
<pre><code>SELECT sname, sc.sno, sc.cno FROM STUDENT, (SELECT 1,2) AS sc(sno, cno) WHERE sc.sno = STUDENT.sno;
</code></pre>
<p>第二个步骤，这种子查询实际上就是没有指定具体表的 SIMPLE 类型的子查询。在介绍 SIMPLE 类型的子查询时，对没有指定具体表的子查询做了说明（需要子查询中没有约束条件，而且上层不能是外连接），当前示例中的子查询显然是能够提升的，它会转换成如下等价语句：</p>
<pre><code>SELECT sname, 1, 2 FROM STUDENT WHERE STUDENT.sno = 1;
</code></pre>
<p>这样经过两轮的转换，VALUES 类型的子查询也得到了提升。</p>
<h3 id="subqueryscan">带有 SubQueryScan 的执行计划</h3>
<p>虽然我们已经给出了子查询能够提升和不能提升的示例，但是实际上我们在那些示例中连 SubQueryScan 的“影”都没见着。原因是优化器认为如果一个SubQueryScan 只是一个“中介”，那么就应该把它干掉，但还是有必要给出一个带有 SubQueryScan 的示例：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, (SELECT MAX(A) A FROM TEST_B LIMIT 10) B WHERE B.A=10;;
                                  QUERY PLAN
------------------------------------------------------------------------------
 Nested Loop  (cost=1.04..2.12 rows=3 width=20)
   -&gt;  Subquery Scan on b  (cost=1.04..1.06 rows=1 width=4)
         Filter: (b.a = 10)
         -&gt;  Limit  (cost=1.04..1.05 rows=1 width=4)
               -&gt;  Aggregate  (cost=1.04..1.05 rows=1 width=4)
                     -&gt;  Seq Scan on test_b  (cost=0.00..1.03 rows=3 width=4)
   -&gt;  Seq Scan on test_a  (cost=0.00..1.03 rows=3 width=16)
(7 rows)
</code></pre>
<p>从示例中可以看出，这个 SubQueryScan 不仅仅是一个“中介”，它还对下层结点产生的结果具有过滤的作用（Filter: (b.a = 10)。</p>
<h3 id="">小结</h3>
<p>PostgreSQL 优化器对 3 种类型的子查询做了提升，分别是：SIMPLE 类型、UNION 类型、VALUES 类型。这种提升可以减少执行计划的层次。执行计划在执行的时候需要进行投影这样的表达式操作，这种操作往往带来“内存拷贝”的消耗，因此，减少执行计划的层次是有意义的。</p></div></article>