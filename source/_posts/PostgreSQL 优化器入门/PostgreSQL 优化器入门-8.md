---
title: PostgreSQL 优化器入门-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>没有规矩，不成方圆。我们在编写 SQL 语句的时候，通常都会绞尽脑汁地想写出一个性能比较好的语句。对于如何安排表之间的连接顺序，也都是经过深思熟虑的。但是人脑毕竟不是电脑，我们在安排表之间的连接顺序时，能够考虑到的因素也有限。而且，数据库内的数据情况瞬息万变，在不同的时间节点，同样的连接顺序可能需要消耗不同数量的资源。因此，对表的连接顺序进行重新排列是一个非常重要的优化过程。</p>
<p>请看下面示例中的 SQL 语句，如果从连接条件下推的角度来看，TEST_B.a = TEST_C.a 是无法下推的，因为它引用了 Nonnullable-side 的表（这里把 TEST_A LEFT JOIN TEST_B ON TRUE 看做一个整体）。但是通过查看下面 SQL 语句的执行计划会发现执行计划改变了表之间的连接顺序，由原来的 (TEST_A LEFT JOIN TEST_B ON TRUE) LEFT JOIN TEST_C ON TEST_B.a = TEST_C.a 变成了 TEST_A LEFT JOIN (TEST_B LEFT JOIN TEST_C ON TEST_B.a = TEST_C.a) ON TRUE，使得连接条件同样地下降了一层。 </p>
<pre><code>-- ( A LEFT JOIN B ) LEFT JOIN C
postgres=# EXPLAIN SELECT * FROM (TEST_A LEFT JOIN TEST_B ON TRUE) LEFT JOIN TEST_C ON TEST_B.a = TEST_C.a;
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..16.82 rows=1000 width=48)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=1.11..2.35 rows=10 width=32)
         -&gt;  Hash Left Join  (cost=1.11..2.30 rows=10 width=32)
               Hash Cond: (test_b.a = test_c.a)
               -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
               -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
                     -&gt;  Seq Scan on test_c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)
</code></pre>
<p>SQL语句中会指定表的具体顺序，有一些简单的情况，通过观察就能看出交换顺序之后仍然等价，例如：</p>
<ul>
<li><strong>内连接</strong> 交换内连接的两个表的连接顺序，通常而言不会影响执行结果</li>
<li><strong>左外连接</strong> 交换左外连接的两个表的连接顺序而且把左外连接改变成右外连接，那么也不会影响执行结果</li>
</ul>
<p>但如果有更多的表呢？是否存在一种“结合律”，把不同的表进行结合同样存在着等价的执行结果？查询优化器在尝试生成连接路径的时候会尝试交换基表之间的连接顺序，这样就带来了更多的可能性，也就有更大的概率选出更优的路径。但是，连接顺序的交换也会受到一些限制，PostgreSQL 数据库定制了一些交换规则：</p>
<pre><code>假设 A、B、C 为参与连接的基表，Pab 代表引用了 A 表和 B 表上的列的谓词（连接条件）。

和 LEFT JOIN 相关的连接顺序交换等式：

    等式 1.1： (A leftjoin B on (Pab)) innerjoin C on (Pac)
           = (A innerjoin C on (Pac)) leftjoin B on (Pab)
    等式 1.2： (A leftjoin B on (Pab)) leftjoin C on (Pac)
           = (A leftjoin C on (Pac)) leftjoin B on (Pab)
    等式 1.3： (A leftjoin B on (Pab)) leftjoin C on (Pbc)
           = A leftjoin (B leftjoin C on (Pbc)) on (Pab)
              &amp;Pbc must be strict

和 Semi Join 有关的连接顺序交换等式：

    等式 2：(A semijoin B ON Pab) innerjoin/leftjoin/semijoin/antijoin C ON Pac
          = (A innerjoin/leftjoin/semijoin/antijoin C ON Pac) semijoin B ON Pab

和 Anti Join 有关的连接顺序交换等式：

    等式 3：(A antijoin B ON Pab) innerjoin/leftjoin/semijoin/antijoin C ON Pac
          = (A innerjoin/leftjoin/semijoin/antijoin C ON Pac) antijoin B ON Pab
</code></pre>
<p>在这些等式里，没有考虑右外连接，这是因为右外连接可以直接变成左外连接，然后按照左外连接的等式进行等价变换：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM (TEST_A RIGHT JOIN TEST_B ON TRUE) LEFT JOIN TEST_C ON TEST_A.a = TEST_C.a;
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..17.39 rows=1000 width=48)
   -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
   -&gt;  Materialize  (cost=1.11..4.04 rows=100 width=32)
         -&gt;  Hash Left Join  (cost=1.11..3.54 rows=100 width=32)
               Hash Cond: (test_a.a = test_c.a)
               -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
               -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
                     -&gt;  Seq Scan on test_c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)

注：右外连接转换成了左外连接
</code></pre>
<p>在这些等式里也没有考虑全连接（Full Join）的情况，这是因为PostgreSQL 没有对全连接的情况进行优化，也就是说一旦发现两个表之间的连接关系是全连接，那么不会再和其他表交换连接顺序：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM (TEST_A LEFT JOIN TEST_B ON TRUE) FULL JOIN TEST_C ON TEST_B.a = TEST_C.a;
                                QUERY PLAN
--------------------------------------------------------------------------
 Hash Full Join  (cost=1.11..25.49 rows=1000 width=48)
   Hash Cond: (test_b.a = test_c.a)
   -&gt;  Nested Loop Left Join  (cost=0.00..15.62 rows=1000 width=32)
         -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=16)
               -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
   -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
         -&gt;  Seq Scan on test_c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)

注： 全连接没有交换连接顺序
</code></pre>
<h3 id="">和左外连接相关的连接顺序交换示例</h3>
<p>在上面已经给出了等式 1.3 的示例，下面给出等式 1.1 和等式 1.2 的示例：</p>
<pre><code>-- 等式 1.1
postgres=# EXPLAIN SELECT * FROM (TEST_A LEFT JOIN TEST_B ON TRUE) INNER JOIN TEST_C ON TEST_A.a = TEST_C.a;
                               QUERY PLAN
-------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..5.29 rows=50 width=48)
   -&gt;  Hash Join  (cost=1.11..3.54 rows=5 width=32)
         Hash Cond: (test_a.a = test_c.a)
         -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
               -&gt;  Seq Scan on test_c  (cost=0.00..1.05 rows=5 width=16)
   -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=16)
         -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
(8 rows)

-- 等式 1.2
postgres=# EXPLAIN SELECT * FROM (TEST_A LEFT JOIN TEST_B ON TRUE) LEFT JOIN TEST_C ON TEST_A.a = TEST_C.a;
                               QUERY PLAN
-------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..17.16 rows=1000 width=48)
   -&gt;  Hash Left Join  (cost=1.11..3.54 rows=100 width=32)
         Hash Cond: (test_a.a = test_c.a)
         -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
               -&gt;  Seq Scan on test_c  (cost=0.00..1.05 rows=5 width=16)
   -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=16)
         -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
(8 rows)
</code></pre>
<h3 id="semijoin">和 Semi Join 相关的连接顺序交换示例</h3>
<p>对于半连接（Semi Join）的情况，PostgreSQL 数据库的注释文档中指出：</p>
<pre><code>SEMI joins work a little bit differently.  A semijoin can be reassociated into or out of the lefthand side of another semijoin, left join, or antijoin, but not into or out of the righthand side.  Likewise, an inner join, left join, or antijoin can be reassociated into or out of the lefthand side of a semijoin, but not into or out of the righthand side.
</code></pre>
<p>我们以 (A semijoin B ON Pab) leftjoin C ON Pac 为例来查看一下执行计划。</p>
<pre><code>// (A semijoin B ON Pab) leftjoin C ON Pac
postgres=# EXPLAIN SELECT * FROM (SELECT * FROM TEST_A a WHERE a.a &gt; ANY (SELECT a FROM TEST_B b)) ab LEFT JOIN TEST_C c ON ab.a = c.a;
                                QUERY PLAN
---------------------------------------------------------------------------
 Hash Left Join  (cost=1.11..15.33 rows=33 width=32)
   Hash Cond: (a.a = c.a)
   -&gt;  Nested Loop Semi Join  (cost=0.00..14.07 rows=33 width=16)
         Join Filter: (a.a &gt; b.a)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=4)
               -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=4)
   -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
         -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
(9 rows)
</code></pre>
<p>分析执行计划可以发现，查询计划中并没有按照我们预想的进行顺序交换。这里没有交换的原因是根据代价计算，不交换的执行计划代价比较低。我们反向地看一下，如果 (A semijoin B ON Pab) leftjoin C ON Pac 等价于 (A leftjoin C ON Pac) semijoin B ON Pab，那么 (A leftjoin C ON Pac) semijoin B ON Pab 产生的执行计划应该与上面示例中的执行计划相同。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_C c ON a.a = c.a WHERE A.a &gt; ANY (SELECT a FROM TEST_B);
                               QUERY PLAN
-------------------------------------------------------------------------
 Hash Left Join  (cost=1.11..15.33 rows=33 width=32)
   Hash Cond: (a.a = c.a)
   -&gt;  Nested Loop Semi Join  (cost=0.00..14.07 rows=33 width=16)
         Join Filter: (a.a &gt; test_b.a)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=4)
               -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=4)
   -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
         -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
(9 rows)
</code></pre>
<p>通过示例可以看出查询优化器对 (A leftjoin C ON Pac) semijoin B ON Pab 产生的执行计划做了顺序交换，转变成了 (A semijoin B ON Pab) leftjoin C ON Pac 的形式。</p>
<h3 id="antijoin">Anti Join 的连接顺序交换示例</h3>
<p>下面是一个反半连接的例子:</p>
<pre><code>-- 直接用 (A leftjoin C ON Pac) antijoin B ON Pab 验证
postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = b.a WHERE NOT EXISTS (SELECT a FROM TEST_C c WHERE a.b = c.b);
                                QUERY PLAN
--------------------------------------------------------------------------
 Hash Left Join  (cost=2.34..6.01 rows=95 width=32)
   Hash Cond: (a.a = b.a)
   -&gt;  Hash Anti Join  (cost=1.11..4.33 rows=95 width=16)
         Hash Cond: (a.b = c.b)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Hash  (cost=1.05..1.05 rows=5 width=4)
               -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=4)
   -&gt;  Hash  (cost=1.10..1.10 rows=10 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(9 rows)
</code></pre>
<p>可以看出查询优化器对 (A leftjoin C ON Pac) antijoin B ON Pab 产生的执行计划做了顺序交换，转变成了 (A antijoin B ON Pab) leftjoin C ON Pac 的形式。</p>
<h3 id="-1">小结</h3>
<p>需要注意的是，连接顺序交换等价性的形式化证明并非易事，对于 PostgreSQL 数据库开发人员也是如此。而且即使能够证明其等价，通过清晰的代码来实现也有一定的难度。上面的 5 个等式可能并不全面，需要在分析查询优化的过程中根据不同的情况灵活地进行分析。不过，我们可以基于一个大的原则。SemiJoin 通常和 InnerJoin 具有一定的相似性，原因是可以把 SemiJoin 看做 “InnerJoin + 内表唯一化”的情况，因此，它本质上还是通过连接操作来产生结果的。AntiJoin 通常和 LeftJoin 具有一定的相似性，原因是 AntiJoin 需要的是和内表匹配不上，而 LeftJoin 恰好也把和内表匹配不上的数据显示出来，因此，它们两个都天然地含有“补 NULL”的逻辑。这种大的原则虽然不“精确”，但它是有用的，可以帮助我们在分析具体问题的时候更好地理清连接操作之间的逻辑关系。有了上面 3 个结论，读者不妨参照结论多构造一些执行计划进行练习，做到熟练掌握这些内容。</p></div></article>