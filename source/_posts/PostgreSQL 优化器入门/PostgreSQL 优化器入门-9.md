---
title: PostgreSQL 优化器入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>PostgreSQL 数据库区分了子查询和子连接，我们先来看一下子查询和子连接的区别。</p>
<h3 id="">子连接和子查询的区别</h3>
<p>PostgreSQL 数据库基于子查询所在的位置和作用的不同，将子查询细分成了两类，一类称为子连接（SubLink），另一类称为子查询（SubQuery）。那么如何来区分子查询和子连接呢？通常而言，如果它是以“表”的方式存在的，那么就称为<strong>子查询</strong>，例如下面的示例语句中是以一个表的方式存在的:</p>
<pre><code>SELECT * FROM TEST_A, (SELECT * FROM TEST_B) as b;
注：可以把 (SELECT * FROM TEST_B) as b 看做是一个表
</code></pre>
<p>如果它以表达式的方式存在，那么就称为<strong>子连接</strong>，例如下面的标量子查询，它是一个表达式类型的子连接，它是投影中的一个表达式。</p>
<pre><code>SELECT (SELECT AVG(a) FROM TEST_A), a FROM TEST_B;
SELECT * FROM TEST_A WHERE TEST_A.a &gt; ANY(SELECT a FROM TEST_B);
注：我们可以把目标列、约束条件都可以看成表达式
</code></pre>
<p>在实际应用中可以通过子句所处的位置来区分子连接和子查询，<strong>出现在 FROM 关键字后的子句是子查询语句，出现在 WHERE/ON 等约束条件中或投影中的子句是子连接语句</strong>。</p>
<p>子查询固然从语句的逻辑层次上是清晰的，但是使用的方法不同，它的效率有高有低。通常而言，相关子查询是值得提升的，因为其执行结果和父查询相关，也就是说父查询的每一条元组都对应着子查询的重新求值；而非相关子查询则可以不提升，因为可以一次求值多次使用，但是在实际应用中还需要具体情况具体分析。</p>
<h3 id="-1">相关子连接和非相关子连接</h3>
<p>从相关性上而言，PostgreSQL 把子连接又分为相关子连接和非相关子连接。</p>
<p><strong>相关子连接</strong>：指在子查询语句中引用了外层表的列属性，这就导致外层表每获得一个元组，子查询就需要重新执行一次。</p>
<pre><code>SELECT * FROM TEST_A WHERE EXISTS (SELECT a FROM TEST_B WHERE TEST_A.a = TEST_B.a);
注：子连接中包含 TEST_A.a ，证明这是一个相关子连接
</code></pre>
<p><strong>非相关子连接</strong>：指子查询语句是独立的，和外层的表没有直接的关联，子查询可以单独执行一次，外层表可以重复利用子查询的执行结果。</p>
<pre><code>SELECT * FROM TEST_A WHERE EXISTS (SELECT a FROM TEST_B WHERE TEST_B.a = 1);
注：子连接中没有包含 TEST_A 上的任何属性，所以这是一个非相关子连接
</code></pre>
<p>PostgreSQL 函数目前只处理了 EXISTS 类型的子连接和 ANY 类型的子连接，比如对于 ALL 类型的子连接它是不能提升的：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; ALL ( SELECT a FROM TEST_B);
                             QUERY PLAN
---------------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..61.00 rows=50 width=16)
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=4)
           -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=4)
(5 rows)
</code></pre>
<h3 id="exists">EXISTS 类型的子连接是怎么提升的</h3>
<p>例如下面的 SQL 语句，它是一个 EXISTS 类型的相关子连接，由执行计划可以看出，子连接已经被提升了。提升之后的逻辑运算符是 Semi Join，物理运算符是 Hash Join（逻辑运算符是指我们在 SQL 语句中指定的连接方法，而物理运算符是指执行器用什么样的方法来实现这个逻辑运算符）。提升之后通过将内表哈希化，降低了算法的复杂度，避免了重复多次执行子查询的问题。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE EXISTS (SELECT a FROM TEST_B WHERE TEST_A.a = TEST_B.a);
                            QUERY PLAN
-------------------------------------------------------------------
 Hash Semi Join  (cost=54.05..112.30 rows=2 width=16)
   Hash Cond: (test_a.a = test_b.a)
   -&gt;  Seq Scan on test_a  (cost=0.00..57.56 rows=256 width=16)
   -&gt;  Hash  (cost=54.02..54.02 rows=2 width=4)
         -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=4)
(5 rows) 
</code></pre>
<p>再看一个 EXISTS 类型的非相关子连接的例子。从执行计划可以看出，子连接形成了一个单独的子执行计划，查询执行器会对这个子执行计划进行单独求解，求解的结果则作为一个 One-Time Filter 来决定是否对 TEST_A 表进行扫描，这里虽然没有做到“一次求解多次使用”，但是做到了“一次求解决定全局”。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE EXISTS (SELECT a FROM TEST_B);
                           QUERY PLAN
-----------------------------------------------------------------
 Result  (cost=27.01..84.57 rows=256 width=16)
   One-Time Filter: $0
   InitPlan 1 (returns $0)
     -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=0)
   -&gt;  Seq Scan on test_a  (cost=27.01..84.57 rows=256 width=16)
(5 rows)
</code></pre>
<p>由此可以记住一个大的原则：<strong>EXISTS 类型的相关子连接会被提升，非相关子连接会形成子执行计划单独求解。</strong>需要注意的是，还需要保证 EXISTS 类型的相关子连接是“简单”的才能被提升。例如在下面的示例中，由于投影中含有聚集函数，导致了这个 EXISTS 类型的相关子连接也不能提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE EXISTS (SELECT SUM(a) FROM TEST_B WHERE TEST_A.a = TEST_B.a);
                             QUERY PLAN
---------------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..13891.80 rows=128 width=16)
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Aggregate  (cost=54.03..54.04 rows=1 width=8)
           -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=4)
                 Filter: (test_a.a = a)
(6 rows)
</code></pre>
<h3 id="any">ANY 类型的子连接是怎么提升的</h3>
<p>如下面的示例所示，PostgreSQL 数据库对 ANY 类型的非相关子连接进行了提升。虽然这个 SQL 语句看上去是非相关子连接，但是它的约束条件中的 a 作为 ‘&gt;’ 操作符的左值，和这个子连接有很大的关系，也就是说它可以形成一个相关的约束条件。从执行计划可以看出，提升之后它们有了一个约束条件 TEST_A.a &gt; TEST_B.a，也就是说 ANY 类型的子连接天然带有“相关”的特性。另外从执行计划也可以看出，子连接被提升之后变成了对 TEST_B 表的扫描，并且对扫描之后的表进行了物化，物化的主要作用就是“一次扫描，多次使用”，因此这种提升是可以带来收益的。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; ANY (SELECT a FROM TEST_B);
                            QUERY PLAN
-------------------------------------------------------------------
 Nested Loop Semi Join  (cost=0.00..118.41 rows=85 width=16)
   Join Filter: (test_a.a &gt; test_b.a)
   -&gt;  Seq Scan on test_a  (cost=0.00..57.56 rows=256 width=16)
   -&gt;  Materialize  (cost=0.00..54.03 rows=2 width=4)
         -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=4)
(5 rows)
</code></pre>
<p>假如我们把这种相关性打破，它就不会再提升了，我们把约束条件中的左操作数换成常量，打破相关性，示例如下：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE 1 &gt; ANY (SELECT a FROM TEST_B);
                              QUERY PLAN
----------------------------------------------------------------------
 Result  (cost=1.38..3.38 rows=100 width=16)
   One-Time Filter: (SubPlan 1)
   -&gt;  Seq Scan on test_a  (cost=1.38..3.38 rows=100 width=16)
   SubPlan 1
     -&gt;  Materialize  (cost=0.00..2.50 rows=100 width=4)
           -&gt;  Seq Scan on test_b  (cost=0.00..2.00 rows=100 width=4)
(6 rows)
</code></pre>
<p>PostgreSQL 数据库对 ANY 类型的相关子连接没有进行提升。从下面的示例可以看出，子连接形成了一个单独的子执行计划。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; ANY (SELECT a FROM TEST_B WHERE TEST_A.b = TEST_B.b);
                          QUERY PLAN
---------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..6974.04 rows=128 width=16)
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Seq Scan on test_b  (cost=0.00..54.02 rows=2 width=4)
           Filter: (test_a.b = b)
(5 rows)
</code></pre>
<p>这里需要说明的是，实际上面示例的相关子连接应该也是能够提升的，例如 Oracle 数据库对这种情况就进行了提升，它的执行计划如下：</p>
<pre><code>SQL&gt; explain plan for SELECT * FROM TEST_A WHERE a &gt; ANY (SELECT a FROM TEST_B WHERE TEST_A.b = TEST_B.b);
| Id  | Operation                | Name      | Rows  | Bytes | Cost (%CPU)| Time  
-------------------------------------------------------------------------
|   0 | SELECT STATEMENT       |           |     1 |    26 |     4   (0)| 00:00:01 
|*  1 |  HASH JOIN SEMI         |           |     1 |    26 |     4   (0)| 00:00:01 
|   2 |   TABLE ACCESS FULL    | TEST_A    |     1 |    13 |     2   (0)| 00:00:01 
|   3 |   TABLE ACCESS FULL    | TEST_B    |     1 |    13 |     2   (0)| 00:00:01 

Predicate Information (identified by operation id):
---------------------------------------------------
   1 - access("TEST_A"."B"="TEST_B"."B")
       filter("A"&gt;"A")
</code></pre>
<p>PostgreSQL 没有将这种子连接提升是由于 ANY 类型的子连接提升分成了两个步骤，第一个步骤是将子连接提升成子查询，第二个步骤则进行子查询提升。对于 ANY 类型的相关子连接在提升成子查询之后会形成如下形式的语句：</p>
<pre><code>SELECT * FROM TEST_A SEMI JOIN (SELECT a FROM TEST_B WHERE TEST_A.b = TEST_B.b) AS b WHERE TEST_A.a &gt; TEST_B.a;
</code></pre>
<p>这个 SQL 语句中的子查询中引用了父查询的属性 TEST_A.b，这种情况 PostgreSQL 数据库在语法上是不支持的，自然在源代码中也没有支持这种逻辑。当然，PostgreSQL 数据库在 9.3 版本之后支持了 Lateral 语义，可以通过 Lateral 关键字来支持子查询引用父查询的属性，但 PostgreSQL 数据库目前还没有支持这种 ANY 类型的相关子连接的提升。</p>
<p>由此对于 ANY 类型的子连接我们也可以得到一个感性的原则：<strong>ANY 类型的非相关子连接可以提升（仍然需要是“简单”的子连接），并且可以通过物化的方式进行优化，而 ANY 类型的相关子连接目前还不能提升</strong>。</p>
<h3 id="-2">不能提升的子连接示例</h3>
<p>子连接形成的表达式中如果含有易失性函数子连接不能提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE random() &gt; ANY (SELECT a FROM TEST_B);
                              QUERY PLAN
----------------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..140.25 rows=50 width=16)
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Materialize  (cost=0.00..2.50 rows=100 width=4)
           -&gt;  Seq Scan on test_b  (cost=0.00..2.00 rows=100 width=4)
(5 rows)


注：PostgreSQL 数据库中的函数有三种稳定性级别：VOLATILE、STABLE 和 IMMUTABLE，其中 VOLATILE 函数输入同样的参数会返回不同的结果，查询优化模块通常不对含有 VOLATILE 函数的表达式进行优化，用户可以通过 PG_PROC 系统表中的 provolatile 列来查询一个函数的稳定性级别。

postgres=# SELECT proname, provolatile FROM PG_PROC WHERE proname = 'random';
 proname | provolatile
---------+-------------
 random  | v
(1 row)
</code></pre>
<p>另外，我们说 EXISTS 类型的子连接必须是“简单”的才能提升，那么怎么才是简单的子句呢？首先，子句中如果包含通用表达式（CTE），子连接不能提升。</p>
<p>其次，如果子句中包含集合操作、聚集操作、HAVING 子句等，子连接不能提升，否则子连接中的子句进行简化。所谓简化，是指结合 EXISTS 的语义，“存在即可”，因此子连接中的结果是否排序，是否有 LIMIT 限制，投影的数量，都没什么用，可以简化掉。从下面的示例可以看出，两个执行计划完全相同，说明这些因素确实被简化掉了。</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT * FROM TEST_A WHERE EXISTS (SELECT a FROM TEST_B);
                              QUERY PLAN
-----------------------------------------------------------------------
 Result  (cost=0.02..2.02 rows=100 width=16)
   Output: test_a.a, test_a.b, test_a.c, test_a.d
   One-Time Filter: $0
   InitPlan 1 (returns $0)
     -&gt;  Seq Scan on public.test_b  (cost=0.00..2.00 rows=100 width=0)
   -&gt;  Seq Scan on public.test_a  (cost=0.02..2.02 rows=100 width=16)
         Output: test_a.a, test_a.b, test_a.c, test_a.d
(7 rows)

postgres=# EXPLAIN VERBOSE  SELECT * FROM TEST_A WHERE EXISTS (SELECT distinct a, b, c FROM TEST_B ORDER BY c LIMIT 10);
                              QUERY PLAN
-----------------------------------------------------------------------
 Result  (cost=0.02..2.02 rows=100 width=16)
   Output: test_a.a, test_a.b, test_a.c, test_a.d
   One-Time Filter: $0
   InitPlan 1 (returns $0)
     -&gt;  Seq Scan on public.test_b  (cost=0.00..2.00 rows=100 width=0)
   -&gt;  Seq Scan on public.test_a  (cost=0.02..2.02 rows=100 width=16)
         Output: test_a.a, test_a.b, test_a.c, test_a.d
(7 rows)
</code></pre>
<p>EXISTS 类型的子连接的约束条件（Whereclause）中如果含有易失性函数，子连接不能提升。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE EXISTS ( SELECT a FROM TEST_B WHERE TEST_A.a = random());
                          QUERY PLAN
--------------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..119.50 rows=50 width=16)
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Seq Scan on test_b  (cost=0.00..1.18 rows=1 width=0)
           Filter: ((test_a.a)::double precision = random())
(5 rows)
</code></pre>
<h3 id="-3">不提升的子连接怎么执行</h3>
<p>下面的示例中，在投影中有一个子连接，在子连接提升的过程中没有处理这种情况。从执行计划来看，它生成了一个 InitPlan（虽然这个执行计划可以生成，但是语句却不一定能执行，因为投影中的子连接的结果必须是标量）：</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT (SELECT A FROM TEST_B),* FROM TEST_A;
                             QUERY PLAN
---------------------------------------------------------------------
 Seq Scan on public.test_a  (cost=1.03..2.06 rows=3 width=20)
   Output: $0, test_a.a, test_a.b, test_a.c, test_a.d
   InitPlan 1 (returns $0)
     -&gt;  Seq Scan on public.test_b  (cost=0.00..1.03 rows=3 width=4)
           Output: test_b.a
(5 rows)
</code></pre>
<p>在来看一个非相关 EXISTS 子连接的例子，这时候这个子连接仍然生成了一个 InitPlan：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE EXISTS (SELECT A FROM TEST_B);
                          QUERY PLAN
--------------------------------------------------------------
 Result  (cost=0.34..1.37 rows=3 width=16)
   One-Time Filter: $0
   InitPlan 1 (returns $0)
     -&gt;  Seq Scan on test_b  (cost=0.00..1.03 rows=3 width=0)
   -&gt;  Seq Scan on test_a  (cost=0.34..1.37 rows=3 width=16)
(5 rows)
</code></pre>
<p>这种 InitPlan 有一个共同的特点，那就是他们都是由非相关的子连接产生的。也就是说，它们都具有一个特点：只要执行一次，获得了结果之后就能反复地利用这个结果。</p>
<p>从执行计划中可以可出，对于在投影中的子连接，它执行之后获得了执行结果，这个执行结果就可以无数次地在投影（Output: $0, test_a.a, test_a.b, test_a.c, test_a.d）中使用。</p>
<p>而对于示例中的 EXISTS 类型的子连接，这个子连接是在约束条件（WHERE）中的。也就是说，这个子连接的结果起的是过滤的作用，只要这个子连接的结果为 TRUE，那么实际上 TEST_A 表的所有数据都能展示出来。而如果这个子连接的结果为 FALSE，那么 TEST_A 表的数据就没有展示的必要了。因此，执行计划中把这种子连接做成了一个 One-Time Filter，也就是先执行一次这个子连接来获得结果，再用这个结果来看是否还有扫描 TEST_A 的必要。</p>
<p>我们从执行计划中可以看到"$0"标识。这个标识实际上是一个参数，也就是说它把子连接的执行结果看做一个参数。当第一次要获得参数中的值的时候，就执行这个子连接来获得结果，并且把这个结果保存在参数中，当第二次以及之后再次要获得参数的值的时候，就无须再执行子连接了，只要将参数中已经保存好的结果直接返回就可以了。</p>
<p>另一种情况是，没有提升的相关子连接，这种类型的子连接产生的执行计划是这样的：</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT * FROM TEST_A WHERE A &gt; ANY(SELECT A FROM TEST_B WHERE TEST_A.B = TEST_B.B);
                             QUERY PLAN
---------------------------------------------------------------------
 Seq Scan on public.test_a  (cost=0.00..2.60 rows=2 width=16)
   Output: test_a.a, test_a.b, test_a.c, test_a.d
   Filter: (SubPlan 1)
   SubPlan 1
     -&gt;  Seq Scan on public.test_b  (cost=0.00..1.04 rows=1 width=4)
           Output: test_b.a
           Filter: (test_a.b = test_b.b)
(7 rows)
</code></pre>
<p>这种相关的子连接产生的执行计划是 SubPlan，它和产生 InitPlan 的子连接的执行方法是不同的，主要的区别在于，这个执行计划中隐含着两个参数：</p>
<ul>
<li>一个参数隐含在 “Filter: (SubPlan 1)” 中，这里实际上的形式应该是 “TEST_A.A &gt; Param” ，而 Param 就是所谓的参数，这个参数对应的是子连接的执行结果。从 SQL 的语义中也能看出来，子连接的执行结果和 TEST_A.A 构成了一个约束条件。</li>
<li>另一个参数隐含在 “Filter: (test_a.b = test_b.b)” 中，子连接中没有 TEST_A 表，这里的 TEST_A.b 应该是从父查询那里传递进来的，所以 TEST_A.b 实际上也是一个参数。</li>
</ul>
<p>这样的执行计划的流程是这样的：</p>
<pre><code>1.TEST_A 表获得一条元组
2.提取 TEST_A.B 的值，TEST_A.B 的值是子连接的参数
3.执行子连接，因为有了参数，所以子连接开始执行
4.子连接的执行结果保存到参数中
5.对 TEST_A 表的这条元组进行过滤，过滤时使用的参数是子连接的执行结果
</code></pre>
<p>虽然说<strong>相关的 Exists 类型的子连接</strong>是可以提升的，但这只是一个必要条件，而非充分条件。例如下面的这种情况，虽然是 EXISTS 类型的相关子连接，它仍然没有提升：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN TEST_C ON EXISTS (SELECT * FROM TEST_B WHERE TEST_A.A = TEST_B.A);
                              QUERY PLAN
-----------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..5861.66 rows=2775 width=32)
   Join Filter: (alternatives: SubPlan 1 or hashed SubPlan 2)
   -&gt;  Seq Scan on test_a  (cost=0.00..1.03 rows=3 width=16)
   -&gt;  Materialize  (cost=0.00..37.75 rows=1850 width=16)
         -&gt;  Seq Scan on test_c  (cost=0.00..28.50 rows=1850 width=16)
   SubPlan 1
     -&gt;  Seq Scan on test_b  (cost=0.00..1.04 rows=1 width=0)
           Filter: (test_a.a = a)
   SubPlan 2
     -&gt;  Seq Scan on test_b test_b_1  (cost=0.00..1.03 rows=3 width=4)
(10 rows)
</code></pre>
<p>子连接中涉及的 TEST_A.A 是父查询的 TEST_A LEFT JOIN TEST_C 的 Nonnullable 端的表，它如果提升上来，那么就先要和 TEST_A 表做连接，也就是说会形成 ((TEST_A SEMI JOIN TEST_B) LEFT JOIN TEST_C)，这种形式显然和原来的语义不等价。在原来的语义中，TEST_A 表的所有元组都会显示到最终结果中。而现在，经过 TEST_A SEMI JOIN TEST_B 的先期连接，很可能 TEST_A 表中的一些数据已经被丢弃了，所以执行结果就和原来的语义不相同了。</p>
<p>通过仔细观察还可以发现，这种情况中的子连接不但没有提升，它还生成了一种很奇怪的执行计划，<strong>一个子连接产生了两个 SubPlan</strong>，这是因为优化器想借助哈希表来优化这种执行计划。</p>
<p>先来看一下一个子连接要提升的原因和不能提升的原因：</p>
<pre><code>1. 相关子连接提升上来之后可以避免那种 O(N^2) 式的子计划的执行方式（参照上面的借助参数执行的情况），例如提升上来之后借助哈希表实现优化
2. 不能提升的一种情况是非相关子连接，因为只需要执行一次就能反复利用它的执行结果
3. 另一种不能提升的情况是对于外连接，它需要满足的是和 Nullable 端相关，而非和 Nonnullable 端相关
</code></pre>
<p>那么对于<strong>和 Nonnullable 端相关</strong>的<strong>相关子连接</strong>，虽然它不能提升，但是它仍然能借助哈希表进行优化。从 “Join Filter: (alternatives: SubPlan 1 or hashed SubPlan 2)” 中也可以看出，“SubPlan 1” 和 “SubPlan 2” 是<strong>或</strong>的关系，也就是说要么使用“常规模式”，要么还可以通过给 TEST_B 表中的数据创建一个哈希表，哈希查找的效率就高一些了。</p>
<p>但是，是常规的方式好还是借助哈希的方式好呢？在目前这个阶段（逻辑优化阶段）还不能准确判断。比如，如果 TEST_A 和 TEST_C 连接的结果很少，到 SubPlan 中去探测的数据就很少，那么，我们还要“辛苦”地去创建一个哈希表就不值得了。因此，在这里生成了一个 Alternative Plan，在进入执行器之后，执行器根据具体的执行情况，再来选择使用哪个 SubPlan。</p>
<p>当然还要满足一个条件就是 TEST_B 表必须哈希化之后是能保存在内存中的，也就是这个哈希表是无须物化的。</p>
<h3 id="-4">小结</h3>
<p>子连接提升是非常重要的一个优化手段，在 PostgreSQL 的优化器中也占有比较大的比重，这是因为一方面子连接的使用比较频繁，另一方面子连接提升之后带来的好处也比较明显。</p>
<p>读者朋友可以通过多构建一些子连接的情况来查看 PostgreSQL 的行为，通过反复练习来理解子连接提升的规则。</p></div></article>