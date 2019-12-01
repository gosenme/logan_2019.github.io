---
title: PostgreSQL 优化器入门-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>所谓“出名要趁早”，谓词下推就是基于这一原则（这里所说的谓词就是常用的那些约束条件）。如果一个谓词在执行计划中即使处在不同的位置也不改变执行结果，那么我们就尽量把它保持在下层，因为它有“过滤”的作用。在下层结点把数据过滤掉，有助于降低上层结点的计算量。当然对于一些比较执着的谓词，SQL 的书写者把它安排在了上层，我们在生成执行计划的时候就可以考虑是否能把它推下去。这就需要进行甄别，哪些谓词是可以推下去的，而哪些谓词是无法推下去的。为了把谓词下推的过程说清楚，我们把约束条件做个分类，它主要可以分成过滤条件和连接条件。</p>
<h3 id="">过滤条件和连接条件</h3>
<p>从过滤条件的名字就能看出，它强调的是对查询结果的过滤作用。对这种情况，下面给出了一个示例，示例表中有 100 条数据，SQL 的语句是从这个表中选择出大于 10 的数据，从执行计划可以看出，这个约束条件的描述方式是 “Filter: (a &gt; 10)”，也就是说它起的是过滤作用，本来表中有 100 条数据，经过 a &gt; 10 的过滤之后，一共查找出来 91 条数据。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a &gt; 10;
                       QUERY PLAN
--------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..2.25 rows=91 width=16)
   Filter: (a &gt; 10)
(2 rows)
</code></pre>
<p>仔细观察上面执行的 SQL 语句不难发现，这个过滤条件是处在 <strong>WHERE</strong> 关键字后面的，那么这是不是过滤条件的标志呢？我们再来看一个示例：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = b.a;
                              QUERY PLAN
----------------------------------------------------------------------
 Hash Left Join  (cost=1.23..3.70 rows=100 width=32)
   Hash Cond: (a.a = b.a)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Hash  (cost=1.10..1.10 rows=10 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(5 rows)
</code></pre>
<p>这个示例中的约束条件处在 ON 关键词的后面，它一方面对连接（JOIN）的结果有过滤的作用，另一方面也强调的是连接操作的计算过程。由于左外连接会对没有连接上的内表元组补 NULL 值，因而对于 a.a = b.a 这样的连接条件产生出来的连接结果不一定满足 a.a == b.a，有可能产生出来的是 a.a 和 NULL，我们把这种约束条件称做连接条件。执行计划也可以看出，这个条件是一个 “Hash Cond”，实际上准确地说它是一个<strong>哈希连接条件</strong>（Hash Join Condition）。</p>
<p>于是我们可以得到一个比较粗略的结论：<strong>处在 ON 关键字后面的约束条件是连接条件，处在 WHERE 关键字后面的约束条件是过滤条件。</strong></p>
<p>在同一个语句中，我们即可以包含 ON 关键字，同时也能包含 WHERE 关键字，我们再来看一个示例：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = b.a WHERE a.b = b.b;
                              QUERY PLAN
----------------------------------------------------------------------
 Hash Join  (cost=1.25..4.01 rows=1 width=32)
   Hash Cond: ((a.a = b.a) AND (a.b = b.b))
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Hash  (cost=1.10..1.10 rows=10 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(5 rows)
</code></pre>
<p>是不是有点惊喜，处在 WHERE 关键字后面的过滤条件竟然跑到了 “Hash Cond” 中，这是为什么呢？答案是请再次仔细观察示例中的执行计划，你是否发现 SQL 语句中明明指定的是两个表做左外连接，但是在执行计划中两个表的连接关系变成了内连接，这是典型的<strong>外连接消除</strong>优化（外连接消除优化在后面的课程中会进行讲解，我们先不关心它，我们把目光继续转向约束条件）。</p>
<p>这个示例告诉我们，如果两个表要做的是内连接，实际上它是无需区分连接条件还是过滤条件的。因为即使是处在 ON 关键字后面的连接条件，也只有过滤的作用，内连接不会去补 NULL 值，所以在内连接的时候过滤条件和连接条件是等价的。</p>
<p>我们之所以要区分过滤条件和连接条件，是因为在谓词下推时这两种谓词是有区别的。下面就来看一下谓词下推的三个规则。</p>
<h3 id="-1">谓词下推之后的转化</h3>
<p>对连接条件而言，如果只有内连接，连接条件下推的过程就变得简单了，连接条件可以直接下推到自己所涉及的基表上。例如下面的示例中的约束条件 a.a = 1，细分的话它是一个连接条件，因为它处在 ON 关键字的后面。由于这个连接条件只涉及了TEST_A表，因此它可以被下推到了 TEST_A 表的扫描路径上，变成一个过滤条件，描述的方法是 “Filter: (a = 1)”。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a INNER JOIN TEST_B b ON a.a = 1;
                           QUERY PLAN
----------------------------------------------------------------
 Nested Loop  (cost=0.00..3.45 rows=10 width=32)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.25 rows=1 width=16)
         Filter: (a = 1)
   -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(4 rows)

注：下推的好处显而易见，这样就在对 TEST_A表扫描之后，扫描结果就只有1条元组了，这样就能降低连接操作的代价，下面看一下计算量的差别：

如果谓词下推：

Nested Loop 计算 1 * 10 = 10次
    -&gt;SeqScan 计算100次（TEST_A表中有100行数据）
        -计算100次，但只有1条符合条件
    -&gt;SeqScan 计算10次（TEST_B表中有10条数据）

如果谓词不下推：

Nested Loop 计算 100 * 10 = 1000次
    Join Cond: 计算100 * 10次 = 1000次
    -&gt;SeqScan 计算100次（TEST_A表中有100行数据）
    -&gt;SeqScan 计算10次（TEST_B表中有10条数据）
</code></pre>
<p>需要注意的是，这个连接条件下推之后不再是一个连接条件，变成了一个过滤条件（Filter），过滤条件主要起到信息筛选的作用，我们可以把它引申成一个结论。</p>
<p><strong>规则 1：连接条件下推之后会变成过滤条件，过滤条件下推之后仍然是过滤条件。</strong></p>
<p>上面的示例是两个表做内连接的情况，假如引入了外连接和（反）半连接之后，情况就变得复杂起来。不同的连接类型给连接操作符两端的表赋予了不同的属性：Nonnullable-side 和  Nullable-side。通常来说在外连接中 Nonnullable-side 的表没匹配上连接条件的元组也会显示出来，并在表 Nullable-side 补 NULL 值。</p>
<p>以左外连接为例，处于 LHS 的表是 Nonnullable-side，因为它不符合连接条件的元组也会被投影出来，而处于 RHS 的表是 Nullable-side，Nonnullable-side 不符合连接条件的元组投影时，对应 Nullable-side 的部分投影的是 NULL 值。</p>
<p>下表总结了各种连接类型对应的 Nullable-side 和 Nonnullable-size（对于 Nullable-side 和 Nonnullable-side 在不同的位置它们的含义可能略有不同）。</p>
<table border="0" style="width:1000px;font-size:6px;">
  <tr>
    <th width="180px">连接类型</th>
    <th >Nonnullable</th>
    <th >Nullable</th>
  </tr>
<tr>
<td> A LEFT JOIN B</td>
<td >A</td>
<td> B</td>
</tr>

<tr>
<td> A RIGHT JOIN B</td>
<td >B</td>
<td> A</td>
</tr>

<tr>
<td> A FULL JOIN B</td>
<td >A  B</td>
<td> A  B</td>
</tr>

<tr>
<td> A SEMI JOIN B</td>
<td >A  B</td>
<td> </td>
</tr>

<tr>
<td>A ANTI JOIN B </td>
<td >A</td>
<td> B</td>
</tr>
</table>
<h3 id="-2">连接条件下推的规则</h3>
<p>由于外连接的 Nullable-side 一端可能要补 NULL 值，连接条件的下推就会受到阻碍。如果连接条件引用了 Nullable-side 的表，连接条件是可以下推变成过滤条件的；如果连接条件引用了 Nonnullable-side 的表，那么这个连接条件无法下推，仍然是一个连接条件，如下面的示例:</p>
<pre><code>--例句是左外连接，连接条件没能下推，仍然是连接条件
--连接条件未能下推是因为其引用了 Nonnullable-side 的表
postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = 1;
                              QUERY PLAN
----------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..18.12 rows=100 width=32)
   Join Filter: (a.a = 1)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=16)
         -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
(5 rows)


--例句是右外连接，连接条件可以下推，变成了过滤条件
--连接条件能够下推的原因是其引用的是 Nullable-side 的表
postgres=# EXPLAIN SELECT * FROM TEST_A a RIGHT JOIN TEST_B b ON a.a = 1;
                             QUERY PLAN
---------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..3.48 rows=10 width=32)
   -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
   -&gt;  Materialize  (cost=0.00..2.25 rows=1 width=16)
         -&gt;  Seq Scan on test_a a  (cost=0.00..2.25 rows=1 width=16)
               Filter: (a = 1)
(5 rows)
</code></pre>
<p>那么如果“强制”下推引用了 Nonnullable-side 的连接条件会有什么后果呢？答案是会导致外连接的语义发生改变，也就产生了“非等价变换”，例如我们对 SQL 语句：</p>
<pre><code>SELECT * FROM TEST_A a LEFT JOIN TEST_B b ON a.a = 1;
</code></pre>
<p>把连接条件 a.a = 1 强制下推，那么转换成的等价SQL语句是：</p>
<pre><code>SELECT * FROM (SELECT * FROM TEST_A a WHERE a.a = 1) AS aa LEFT JOIN TEST_B b ON TRUE;
</code></pre>
<p>按照左连接的语义，Nonnullable-side 表中的所有元组都应该被投影出来，而“强制”下推连接条件后，对 Nonnullable-side 表中的元组（也就是 TEST_A 表中的元组）进行了过滤，导致 TEST_A 表中可能有部分元组无法显示出来，因此这种“强制”下推是错误的。</p>
<p>由此，我们可以引申出一个新的结论。</p>
<p><strong>规则 2：如果连接条件引用了 Nonnullable-side 的表，那么连接条件不能下推；如果连接条件只引用了 Nullable-side 的表，那么连接条件可以下推。</strong></p>
<p>目前示例中的连接条件只考虑了“列属性 = 常量”这种情况，而对于“列属性 = 列属性”、“列属性 Op 列属性 = 列属性”、“Func(列属性) = 列属性”等情况都没有验证。但是我们只需要把握一个原则，就是如果连接条件中引用了 Nonnullable-side 的表，那么这个连接条件就不能下推，用户可以尝试构建用例来对这个结论进行验证。</p>
<p>另外，目前只考虑了两个表的情况，《道德经》中有“一生二，二生三，三生万物”的说法，我们尝试用 3 个表来代表普遍的情况，看一个包含 3 个表连接的 SQL 语句：</p>
<pre><code>SELECT * FROM TEST_A a LEFT JOIN (TEST_B b LEFT JOIN TEST_C c ON TRUE) ON a.a = 1;
</code></pre>
<p>如果我们把其中的 (TEST_B b LEFT JOIN TEST_C c ON TRUE) 看成一个整体，那么顶层左连接的 Nullable-side 就是 (TEST_B b LEFT JOIN TEST_C c ON TRUE)，顶层左连接的 Nonnullable-side 就是 TEST_A 表，因为 a.a = 1 引用了 TEST_A 表中的列（也就是引用了 Nonnullable-side 的表的列），因此 a.a = 1 不能被下推。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN (TEST_B b LEFT JOIN TEST_C c ON TRUE) ON a.a = 1;
                                   QUERY PLAN
---------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..79.91 rows=100 width=48)
   Join Filter: (a.a = 1)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=0.00..3.04 rows=50 width=32)
         -&gt;  Nested Loop Left Join  (cost=0.00..2.79 rows=50 width=32)
               -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
               -&gt;  Materialize  (cost=0.00..1.07 rows=5 width=16)
                     -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)
</code></pre>
<p>我们再来看一个语句：</p>
<pre><code>SELECT * FROM TEST_A a LEFT JOIN (TEST_B b LEFT JOIN TEST_C c ON TRUE) ON b.a = c.a;
</code></pre>
<p>连接条件所引用的表都在 (TEST_B b LEFT JOIN TEST_C c ON TRUE) 中，我们如果把 (TEST_B b LEFT JOIN TEST_C c ON TRUE) 看成一个整体，那么它就处于顶层左连接的 Nullable-side，也就是说连接条件是能下降的，结合规则 1 和规则 2，它们下降之后会等价于下面的 SQL 语句：</p>
<pre><code>SELECT * FROM TEST_A a LEFT JOIN (SELECT * FROM TEST_B b LEFT JOIN TEST_C c ON TRUE WHERE b.a = c.a) ON TRUE;
</code></pre>
<p>从查询计划也可以看出，连接条件下推之后和下推之前它们的执行计划是相同的：</p>
<pre><code>--显然，两个执行计划是相同的
postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN (TEST_B b LEFT JOIN TEST_C c ON TRUE) ON b.a = c.a;
                                   QUERY PLAN
---------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..10.56 rows=500 width=48)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=1.11..2.32 rows=5 width=32)
         -&gt;  Hash Join  (cost=1.11..2.30 rows=5 width=32)
               Hash Cond: (b.a = c.a)
               -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
               -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
                     -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)

postgres=# EXPLAIN SELECT * FROM TEST_A a LEFT JOIN (SELECT * FROM TEST_B b LEFT JOIN TEST_C c ON TRUE WHERE b.a = c.a) bc ON TRUE;
                                   QUERY PLAN
---------------------------------------------------------------------------------
 Nested Loop Left Join  (cost=1.11..10.56 rows=500 width=48)
   -&gt;  Seq Scan on test_a a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=1.11..2.32 rows=5 width=32)
         -&gt;  Hash Join  (cost=1.11..2.30 rows=5 width=32)
               Hash Cond: (b.a = c.a)
               -&gt;  Seq Scan on test_b b  (cost=0.00..1.10 rows=10 width=16)
               -&gt;  Hash  (cost=1.05..1.05 rows=5 width=16)
                     -&gt;  Seq Scan on test_c c  (cost=0.00..1.05 rows=5 width=16)
(8 rows)
</code></pre>
<p>规则 2 是给出了连接条件下推应该遵守的准则，接下来我们看一下过滤条件应该准守什么样的准则。</p>
<h3 id="-3">过滤条件下推的规则</h3>
<p>下面是两个带有过滤条件的语句，其中一个过滤条件涉及的是 Nullable-side 的表，另一个过滤条件涉及的是 Nonnullable-side 的表。</p>
<pre><code>SELECT * FROM TEST_A LEFT JOIN TEST_B ON TRUE WHERH TEST_A.a = 1;
SELECT * FROM TEST_A LEFT JOIN TEST_B ON TRUE WHERE TEST_B.a = 1;
</code></pre>
<p>我们来看一下这两个SQL语句的执行计划。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN TEST_B ON TRUE WHERE TEST_A.a = 1;
                          QUERY PLAN
--------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..3.45 rows=10 width=32)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.25 rows=1 width=16)
         Filter: (a = 1)
   -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
(4 rows)



postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN TEST_B ON TRUE WHERE TEST_B.a = 1;
                          QUERY PLAN
---------------------------------------------------------------
 Nested Loop  (cost=0.00..4.12 rows=100 width=32)
   -&gt;  Seq Scan on test_b  (cost=0.00..1.12 rows=1 width=16)
         Filter: (a = 1)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
(4 rows)
</code></pre>
<p>通过例子我们可以看出，如果过滤条件只引用了 Nonnullable-side 的表，那么这个过滤条件能够下推到 Nonnullable-side 的表上；如果过滤条件引用了 Nullable-side 的表且过滤条件是严格的（关于“严格”的解释可以参考《第 8 课 消除外连接》），那么会导致外连接消除变成内连接。在内连接的情况下，过滤条件显然也能下推到对应的表上，那么如果过滤条件引用了 Nullable-side 的表且过滤条件是不严格的，情况会怎样呢？如下面的示例所示，这种情况过滤条件是不能下推的。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A LEFT JOIN TEST_B ON TRUE WHERE TEST_B.a IS NULL;
                             QUERY PLAN
--------------------------------------------------------------------
 Nested Loop Left Join  (cost=0.00..15.62 rows=1 width=32)
   Filter: (test_b.a IS NULL)
   -&gt;  Seq Scan on test_a  (cost=0.00..2.00 rows=100 width=16)
   -&gt;  Materialize  (cost=0.00..1.15 rows=10 width=16)
         -&gt;  Seq Scan on test_b  (cost=0.00..1.10 rows=10 width=16)
(5 rows)
</code></pre>
<p>由此，我们得到一个新的结论。</p>
<p><strong>规则 3：如果过滤条件只引用了 Nonnullable-side 的表，那么这个过滤条件能够下推到表上；如果过滤条件引用了 Nullable-side 的表且过滤条件是严格的，那么会导致外连接消除，外连接消除之后变成内连接，过滤条件也是能下推的。</strong></p>
<h3 id="-4">小结</h3>
<p>谓词下推的规则主要是基于谓词下推的等价性。当读者对各种连接操作的语义都了如指掌之后，就可以在分析执行计划的时候快速了解谓词是否能下推，以及下推是否会产生语义的改变。而对于刚入门的读者，可以通过多分析执行计划强化记忆这些规则。在实践中，这种通过规则直接推到结论的方法会加快分析问题的速度。</p></div></article>