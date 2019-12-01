---
title: PostgreSQL 优化器入门-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在谓词下推的过程中，对于 …FROM A JOIN B ON A.a = B.b 这种类型的约束条件肯定是不能下推的。原因是 A.a = B.b 这样的约束条件既引用了 LHS 表的列属性，又引用了 RHS 表的列属性，必须在获得两个表的元组之后才能应用这样的约束条件。现在假如在 B.b 属性上有一个索引 B_b_index，但没有能够匹配索引的约束条件，索引扫描路径或者不会被采纳，或者采纳为对整个索引进行扫描（例如 Fast Index Scan，这时候将索引视为一个表，实际上和 SeqScan 类似），发挥不了索引对数据筛选的作用。</p>
<h3 id="">借用参数来产生索引扫描路径</h3>
<p>PostgreSQL 优化器最大的优势是“没有困难，制造困难也要上”。在没有办法使用索引扫描的情况下，制造办法使用索引扫描，也是一种能力......</p>
<p>假设 …FROM A JOIN B ON A.a = B.b 生成的执行计划是嵌套循环连接，A 表作为外表做 SeqScan，B 表作为内表也做 SeqScan。</p>
<pre><code>Nestloop Join (JoinCluase: A.a = B.b)
    -&gt;SeqScan (A)
    -&gt;SeqScan (B)

它的执行过程应该是这样的：
1)    从 A 表取出一条元组
2)    如果 A 表已经扫描完毕，执行结束
3)    从 B 表取出一条元组
4)    如果 B 表已经扫描完毕，跳转到步骤 1)
5)    对两个元组应用 A.a = B.b 的约束条件
6)    如果符合 A.a = B.b 的约束条件，则返回连接结果，下一次执行跳转到步骤 3)
7)    如果不符合 A.a = B.b 的约束条件，则直接跳转到步骤 3)
</code></pre>
<p>通过这些执行步骤可以看出，步骤 1) 从 A 表取出一条元组之后，还需要扫描整个 B 表来匹配 A.a = B.b 这样的约束条件。而实际上在步骤 1)获得了 A 表的元组之后，A.a 的值已经确定了。假如我们把这个值从 A 表的元组中取出来作为一个常量，这时候约束条件就可以转换成 B.b = Const（交换 Const = B.b 的顺序）这样一个约束条件，这种只引用了连接操作一端的表的约束条件，大部分情况下是能够下推的。如果在 B.b 上有索引，那么 B.b = Const 这样的约束条件可以让索引变得有用了，索引扫描可以避免扫描整个 B 表。这时候执行计划就变成了：</p>
<pre><code>Nestloop Join
    -&gt;SeqScan (A) (Extract A.a to Const)
    -&gt;IndexScan (B_b_index) (Filter: B.b = Const)
</code></pre>
<p>使用 B.b = Const 这样的约束条件对索引进行扫描，扫描的效率远高于 SeqScan，显然这种方法是可取的。但随之带来的问题是：如何将从 A 元组中提取出来的常量值传递到 B 的扫描中呢？PostgreSQL 数据库选择了通过参数的方式进行传递，也就是生成参数化的路径。</p>
<p>PostgreSQL 中已经包含了使用参数的先例，对于没有提升的子连接，它就是通过传递参数的方式在父子执行计划之间传值，这时候我们是否能利用这个结构体为我们传递参数呢？通常，参数用来从执行计划外向执行计划内传递参数，比如 PBE（Prepare、Bind、Execute）中使用的参数。再比如父执行计划和子执行计划之间通过 Param 进行“通信”，可以是从父执行计划传递给子执行计划，也可以是子执行计划传递给父执行计划。这种情况参数值也是来自于执行计划外，而目前要用的参数是在执行计划内传递，从一个路径向另一个路径传递参数值，或者说是从外表向内表传递参数，和上面使用参数的方式有些区别。</p>
<p>PostgreSQL 借助上面的参数实现了在执行计划结点之间的参数传递，但对执行计划也提出了要求，那就是只能在嵌套循环连接情况下才能产生参数化路径。这是由于只有嵌套循环连接的两个表之间具有“驱动”关系，外表是“驱动表”，内表是“被驱动表”，而哈希连接虽然具有驱动关系，但其内表可以看做是一个哈希表，并非是直接驱动内表，而归并连接则不具有这样的驱动关系。</p>
<p>既然是从外表向内表传递参数，这就产生了一个限定条件：在生成执行路径的时候，如果要建立参数化路径，就需要考虑谁是内表或者谁是外表的问题——产生参数的一方必须是外表，而使用参数的一方就必须是内表，因此在生成连接路径的时候必须先获知连接的双方中谁是参数的生产者，谁是参数的使用者。生产者在“前”，使用者在“后”，我们在连接顺序交换的时候不但需要考虑基于关系代数的等价性，还需要考虑到参数化路径的等价性。</p>
<p>下面我们看一个参数化路径的例子：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, TEST_B WHERE TEST_A.a = TEST_B.a AND TEST_A.a &gt; 9000;
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Nested Loop  (cost=0.29..152931.52 rows=1 width=32)
   -&gt;  Seq Scan on test_a  (cost=0.00..152889.96 rows=5 width=16)
         Filter: (a &gt; 9000)
   -&gt;  Index Scan using test_b_a_idx on test_b  (cost=0.29..8.30 rows=1 width=16)
         Index Cond: (a = test_a.a)
(5 rows)
</code></pre>
<p>从例子中可以看出，对 TEST_B 表使用了索引扫描，约束条件 TEST_A.a = TEST_B.a 下推到了索引扫描上。虽然示例的执行计划中显式的约束条件是 a = test_a.a，但实际上在执行计划中这里的 test_a.a 是一个参数。</p>
<h3 id="lateral">Lateral 的实现也借用了参数化路径</h3>
<p>参数化路径的出现还能帮助我们实现一种之前 PostgreSQL 不支持的情况。之前有这样一个假设：所有的子查询（不包括子连接）都独立存在，不能互相引用属性，例如：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, (SELECT * FROM TEST_B LEFT JOIN (SELECT * FROM TEST_C WHERE TEST_A.A = TEST_C.A) C ON TRUE) B;
ERROR:  invalid reference to FROM-clause entry for table "test_a"
</code></pre>
<p>示例中子查询的投影列中引用了 TEST_A 表的属性，这导致了整个语句执行失败。如果打算执行这样的语句，就需要在子查询前面显式地指定 Lateral 关键字，这样 SQL 语句就能正常执行了：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A, LATERAL (SELECT * FROM TEST_B LEFT JOIN (SELECT * FROM TEST_C WHERE TEST_A.A = TEST_C.A) C ON TRUE) B;
                                QUERY PLAN
--------------------------------------------------------------------------
 Nested Loop  (cost=0.00..106.20 rows=81 width=48)
   -&gt;  Seq Scan on test_a  (cost=0.00..1.03 rows=3 width=16)
   -&gt;  Nested Loop Left Join  (cost=0.00..34.52 rows=27 width=32)
         -&gt;  Seq Scan on test_b  (cost=0.00..1.03 rows=3 width=16)
         -&gt;  Materialize  (cost=0.00..33.17 rows=9 width=16)
               -&gt;  Seq Scan on test_c  (cost=0.00..33.12 rows=9 width=16)
                     Filter: (test_a.a = a)
(7 rows)
</code></pre>
<p>我们从示例中可以看出，“Filter: (test_a.a = a)” 中包含了上层结点的属性，这里的 TEST_A.A 实际上是一个参数。</p>
<h3 id="-1">小结</h3>
<p>参数化路径需要注意以下三点：<br />
1.只能使用嵌套循环连接方法来实现参数的传递；<br />
2.假设连接条件的一端为 CONST 之后，这个连接条件需要满足谓词下推的规则；<br />
3.参数的生产者在前，消费者在后，也就是说连接顺序受到了限制。</p></div></article>