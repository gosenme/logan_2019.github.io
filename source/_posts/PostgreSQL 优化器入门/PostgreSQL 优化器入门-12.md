---
title: PostgreSQL 优化器入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在 SQL 语句中，经常会有 A=B 这样的约束条件，它的操作符是等值操作符。我们将这种等值约束条件称为“等价条件”，而基于多个等价条件进行推理而获得的等价属性的集合就是“等价类”。</p>
<h3 id="">含有常量的等价推理</h3>
<p>假如等价约束条件中的一端是常量，这种等价的推理就会显得更有意义。假如有两个约束条件 A=B 和 B=5，从谓词下推的角度来看，A=B 肯定只能作为一个连接条件。只有在连接操作做完之后，A=B 这样的约束条件才能获得约束条件两端的值。因此，这个约束条件是没有办法下推的，对于 B=5 这样的约束条件呢？如果是内连接的话，通常而言它是能下推的。</p>
<p>如果能通过 A=B 和 B=5 这样的两个约束条件推理出一个新的 A=5 的约束条件，由于 A=5 这样的单属性（只涉及一个表）约束条件或许能够下推到单表上，这样就可以在对表进行扫描的时候把没用的元组过滤掉，从而提高执行的效率。</p>
<p>例如 SQL 语句 SELECT * FROM TEST_A a,TEST_B b WHERE a.a = b.a AND  b.a = 5，本来只能在连接结果产生之后使用 a.a = b.a 对连接结果进行过滤。但是如果推理出 b.a = 5 这样一个过滤条件，那么就能把这个过滤的操作下推到对 TEST_A 表的扫描上。如下面的示例所示，的确产生了新的约束条件 a.a = 5。</p>
<p>从执行计划中还可以看出，a.a = b.a 这个约束条件也被消除掉了，这是因为做扫描操作的时候已经把不等于 5 的数据过滤掉了，只有等于 5 的数据才能被返回给嵌套循环连接结点。由此，在嵌套循环连接结点再做一次 a.a = b.a 就显得有点多余了。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a,TEST_B b WHERE a.a = b.a AND  b.a = 5;
                          QUERY PLAN
---------------------------------------------------------------
 Nested Loop  (cost=0.00..3.38 rows=1 width=32)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.25 rows=1 width=16)
         Filter: (a = 5)
   -&gt;  Seq Scan on test_b b  (cost=0.00..1.12 rows=1 width=16)
         Filter: (a = 5)
(5 rows)
</code></pre>
<h3 id="-1">产生新的连接条件</h3>
<p>假如有两个约束条件分别是 A=B 和 B=C，根据等值传递的特性很容易推出 A=C，这时候就可以说 {A,B,C} 构成一个等价类，因此我们可以隐式地构建一个 A = C 的约束条件。</p>
<p>从示例可以看出，SQL 语句中本来是没有 a.a = c.a 这样的约束条件的，在执行计划中却出现了这样的约束条件。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a,TEST_B b, TEST_C c WHERE a.a = b.a AND b.a = c.a;
                                QUERY PLAN
---------------------------------------------------------------------------
 Hash Join  (cost=2.34..4.79 rows=1 width=48)
   Hash Cond: (a.a = b.a)
   -&gt;  Hash Join  (cost=1.11..3.54 rows=5 width=32)
         Hash Cond: (a.a = c.a)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
               -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
   -&gt;  Hash  (cost=1.10..1.10 rows=10 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(9 rows)
</code></pre>
<h3 id="-2">有序性的等价推理</h3>
<p>假如我们在 SQL 语句中发现一个约束条件为 A=B，那么通过这个约束条件而产生的连接结果中 A 和 B 一定是相等的（假设是内连接）。如果查询结果是按照 A 进行排序的，那么就可以得知查询结果也一定是按照 B 排序的，因为查询结果中的每一行都需要符合 A=B。例如，约束条件 A.a = B.a ORDER BY A.a，它的查询结果中的每一个元组都符合 A.a = B.a，因此 A.a 和 B.a 就构成一个等价类。虽然 ORDER BY 子句中显式指定的是按照 A.a 进行排序，但是对于等价类中的成员而言，只要其中的一个是有序的，那么在查询结果中它们就全部都是有序的。</p>
<p>下面来看一个示例，在示例 SQL 语句中用有 a.a = b.a ORDER BY b.a 这样的子句，也就是说 a.a 和 b.a 构成了一个等价类，且语句的执行结果是按照 b.a 排序的。可以推理出查询的执行结果也是按照 a.a 进行排序的。从执行计划中也可以看出，排序的依据是 “Sort Key: a.a”，这也印证了执行计划在生成的过程中确实进行了等价的推理。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a,TEST_B b WHERE a.a = b.a ORDER BY b.a;
                                 QUERY PLAN
----------------------------------------------------------------------------
 Sort  (cost=3.87..3.89 rows=10 width=32)
   Sort Key: a.a
   -&gt;  Hash Join  (cost=1.23..3.70 rows=10 width=32)
         Hash Cond: (a.a = b.a)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
         -&gt;  Hash  (cost=1.10..1.10 rows=10 width=16)
               -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(7 rows)
</code></pre>
<h3 id="-3">外连接中的小优化</h3>
<p>这种基于等价类的推理虽然能够帮助查询优化器产生更多的物理路径，但是同样需要注意，在引入了外连接（或半连接、反连接）之后情况就会变得复杂。例如在外连接中的 A=B 虽然是等值的连接条件，但这时我们不能草率地认为 A=B，外连接的查询结果对连接操作的 Nullable-side 可能会补 NULL 值，这时候 A 和 B 就不是相等的。对于大多数外连接的情况我们都无法生成等价类，但是其中也会有一些特例，我们可以在上面做做文章。</p>
<p>如果查询语句是左外连接，而且有这样一个等价类 {Nonnullable-side 表的列名, 常量}，也就是 {外表的列, 常量} 这样的等价类，另外连接条件中包含 "Nonullable-side 的列 = Nullable-side 的列" 的情况，那么就可以产生一个 "Nullable-side 的列 = 常量" 的过滤条件，下推到 Nullable-side 的表上，这里给出一个示例。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = b.a WHERE a.a = 5;
                          QUERY PLAN
---------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..3.39 rows=1 width=32)
   Join Filter: (a.a = b.a)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.25 rows=1 width=16)
         Filter: (a = 5)
   -&gt;  Seq Scan on test_b b  (cost=0.00..1.12 rows=1 width=16)
         Filter: (a = 5)
(6 rows)

注：
a.a = b.a 能满足 "Nonullable-side 的列 = Nullable-side 的列" 这个条件
a.a = 5 能满足 “Nonnullable-side 的列 = 常量” 这个条件
</code></pre>
<p>从上面示例的查询计划可以看出，在对 TEST_B 表进行扫描时增加了 TEST_B.a = 5 作为过滤条件。我们仔细分析这个语句发现，增加 TEST_B.a = 5 并不会改变原来语句的执行结果，原因如下：TEST_A.a = 5 作为过滤条件，能够在表扫描的过程中把 TEST_A 中所有 TEST_A.a != 5 的元组过滤掉（注意：TEST_A.a = 5 能够进行谓词下推，下推到 TEST_A 表上），因此扫描结果中的元组一定符合 TEST_A.a = 5。那么用这个扫描结果和 TEST_B 表做连接条件为 TEST_A.a = TEST_B.a 的左连接，TEST_B.a != 5 的元组就不可能连接上。因此增加新的过滤条件 TEST_B.a = 5 不会对连接结果产生影响。</p>
<p>再来看另一个小优化，如果语句中包含全连接（FULL JOIN）操作，如果有一个连接条件"左侧的列 = 右侧的列"，并且有一个过滤条件 "COALESCE(左侧的列, 右侧的列) = 常量"，这样就能构成两个过滤条件 "左侧的列 = 常量" 和 "右侧的列 = 常量" 分别下推到对应的表上。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a FULL JOIN TEST_B b ON a.a = b.a WHERE COALESCE(a.a, b.a) = 1;
                             QUERY PLAN
---------------------------------------------------------------------
 Hash Full Join  (cost=1.14..3.40 rows=1 width=32)
   Hash Cond: (a.a = b.a)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.25 rows=1 width=16)
         Filter: (a = 1)
   -&gt;  Hash  (cost=1.12..1.12 rows=1 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.12 rows=1 width=16)
               Filter: (a = 1)
(7 rows)
</code></pre>
<h3 id="-4">小结</h3>
<p>等价推理的主要目的还是为了增加可能性，总体而言，可能性越多生成更好的执行计划的可能性就越大。然而，可能性多也会带来问题，那就是生成执行计划的时间也会变长。PostgreSQL 在物理优化阶段做了一些优化，尽早淘汰掉了一些可能性。</p></div></article>