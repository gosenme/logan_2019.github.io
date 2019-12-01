---
title: PostgreSQL 优化器入门-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我们写一个查询语句，语句中会有投影和约束条件，这些都需要在执行器中进行计算之后才能获得它们的值，这些就是我们所说的表达式，比如：</p>
<pre><code>SELECT a, b+c FROM TEST_A WHERE d &gt; 0;
</code></pre>
<p>这样的一个语句中我们说有 3 个表达式：</p>
<pre><code>* 对 a 进行求值的表达式
* 对 b+c 进行求值的表达式
* 对 d &gt; 0 进行求值的表达式
</code></pre>
<p>执行器通过 Seq Scan on test_a 表来获得一条元组之后，由于我们已经记录了 a、b、c、d 这些列的编号（也就是它们是表的第几列），因而可以从获得的元组中把 a、b、c、d 对应的值取出来，然后用这些值进行计划，这就是表达式计算的过程。</p>
<p>也就是说每次从 TEST_A 表中取到一条元组，都需要执行一次表达式，它需要先计算 d &gt; 0，如果该元组的确满足 d &gt; 0 的约束条件，然后就需要计算投影，从元组中取出 a 的值作为投影，从元组中取出b、c的值开始计算 b+c 的值来作为投影，如果 TEST_A 表中有 10000 条元组，那么像 d&gt;0 这样的表达式就需要执行 10000 次，而投影中的表达式执行的次数取决于 d&gt;0 这个约束条件的选择率。</p>
<p>在约束条件中，优化器尝试将约束条件进行规范化，主要包括 3 个功能：</p>
<ul>
<li>简化约束条件；</li>
<li>对树状的约束条件拉平，将形如 A OR (B OR C) 形式的约束条件转换为 OR(A,B,C) 形式；</li>
<li>提取公共项，将形如 (A AND B) OR (A AND C) 转换为 A AND (B OR C) 。</li>
</ul>
<h3 id="">简化约束条件</h3>
<p>例如，有这样一个 SQL 语句：</p>
<pre><code>SELECT * FROM TEST_A WHERE NULL OR FALSE OR a = 1;
</code></pre>
<p>由于是 OR 操作，约束条件中的 NULL 和 FALSE 是可以忽略掉的，我们看一下执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE NULL OR FALSE OR a = 1;
                      QUERY PLAN
-------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..2.25 rows=1 width=16)
   Filter: (a = 1)
(2 rows)
</code></pre>
<p>对于 AND 操作，如果涉及了 NULL 或 FALSE，则实际上代表整个约束条件可以规约为 FALSE，例如对于 SQL 语句:</p>
<pre><code>SELECT * FROM TEST_A WHERE NULL AND FALSE AND a = 1;
</code></pre>
<p>约束条件 NULL AND FALSE AND sno = 1 的值最终是 FALSE，从下面的执行计划可以看出，对 TEST_A 表的扫描已经被省略掉了。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE NULL AND FALSE AND a = 1;
                QUERY PLAN
-------------------------------------------
 Result  (cost=0.00..0.00 rows=0 width=16)
   One-Time Filter: false
(2 rows)
</code></pre>
<h3 id="-1">拉平约束条件</h3>
<p>先来看一下约束条件在查询树的表现形式，例如有 SQL 语句：SELECT * FROM TEST_A WHERE a=1 OR (a=2 OR (a=3 OR a=4))，它的约束条件的组织形式是一个树状结构，谓词规范需要将这个约束条件拉平，我们来看一下这个语句的执行计划：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE a=1 OR (a=2 OR (a=3 OR a=4));
                      QUERY PLAN
-------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..3.00 rows=4 width=16)
   Filter: ((a = 1) OR (a = 2) OR (a = 3) OR (a = 4))
(2 rows)
</code></pre>
<div style="text-align:center">
<img src="https://images.gitbook.cn/f7cd2070-d1ed-11e8-b2d6-1188c7e0dd7e" width="200px" /></div>
<p></br></p>
<p>从执行计划可以看出，这个约束条件已经拉平了，所有的 OR 子句都是在同一个层次上。</p>
<h3 id="-2">提取公共表达式</h3>
<p>在约束条件被规约和拉平之后，可以尝试对形如（A AND B）OR (A AND C) 的约束条件进行优化，提取出 A 作为公共项。提取 A 的好处显而易见，对于（A AND B）OR (A AND C) 这样的约束条件，需要将条件涉及的所有表都做完连接之后，才能应用这个约束条件。而如果提取出 A 作为单独的约束条件，则 A 有可能下推到基表上（可以参考谓词下推的部分），从而提高执行效率，找公共项的过程如下。</p>
<p>首先，在约束条件中找到其中最短的子句。例如对于约束条件 (A AND B AND C) OR (A AND B) OR (A AND C AND D) ，OR 操作串联了 3 个子约束条件。可以先尝试找到其中最短的一个 (A AND B)，因为如果有公共因子，那么最短的那个也一定包含公共因子。找到最短的那个子句，在后面的操作里就能减少循环的次数。</p>
<p>然后，以最短的约束条件为依据，提取公共项，对于 (A AND B) 这样的最短项，可以先查看一下 3 个 AND 子句中是否都包含 A。</p>
<ul>
<li>(A AND B AND C)：包含 A</li>
<li>(A AND B)：包含 A</li>
<li>(A AND C AND D)：包含 A</li>
</ul>
<p>如果都包含 A，那么 A 就是公共项中的一员，再参照 3 个 AND 子句看是否都包含 B。</p>
<ul>
<li>(A AND B AND C) ：包含 B</li>
<li>(A AND B) ：包含 B</li>
<li>(A AND C AND D) ：不包含 B</li>
</ul>
<p>因为 (A AND C AND D) 不包含 B，所以 B 不是公共项中的一员，最终可以得出公共项为 A。</p>
<p>需要注意的是，对于 (A AND B) OR (A) 这样的约束条件可以规约成 (A)，同理，对于 (A AND B AND C) OR (A AND B) 这种类型的约束条件可以规约成 (A AND B)。</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A WHERE (a = 1 AND b = 2) OR a = 1;
                      QUERY PLAN
-------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..2.25 rows=1 width=16)
   Filter: (a = 1)
(2 rows)
</code></pre>
<h3 id="-3">表达式常量化简</h3>
<p>但是，无论是手写的 SQL 或者是通过应用框架拼出来的 SQL 语句，都可能出现一些带有常量的表达式。这些表达式计算之后的值是固定的，如果预先求解，那么就能避免在执行器中多次重复运算，因此优化器尝试对带有常量的表达式进行常量化简。</p>
<p>常量化简的主要的优化点有 3 个方面：参数常量化、函数常量化、约束条件常量化。参数的常量化是通过遍历参数的表达式实现的，如果发现参数表达式中全部为常量，则对参数执行预先求值。从下面的示例可以看出，原来的 MAX(a + (1+2)) 已经转变成了 MAX(a+3) 。</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT MAX(a + (1+2)) FROM TEST_A;
                             QUERY PLAN
---------------------------------------------------------------------
 Aggregate  (cost=2.50..2.51 rows=1 width=4)
   Output: max((a + 3))
   -&gt;  Seq Scan on public.test_a  (cost=0.00..2.00 rows=100 width=4)
         Output: a, b, c, d
(4 rows)
</code></pre>
<p>优化器如果发现所有的参数都是常量，则尝试预先获取函数的执行结果，并将结果常量化。从下面的示例可以看出，int4ge 函数是负责比较两个 int4 类型的，在执行计划里直接给出了 int4ge 函数的结果。</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT int4ge(1,3);
                QUERY PLAN
------------------------------------------
 Result  (cost=0.00..0.01 rows=1 width=1)
   Output: false
(2 rows)
</code></pre>
<p>实际上这里的常量化值进行了比较基础的分析，若是我们将参数的常量化略作调整，这种优化就无法进行了。如下面的示例所示，由于所有操作符是左结合的，因此导致投影表达式中的每个操作符都有非常量，这就导致了无法进行常量化。</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT MAX(a + 1 + 2) FROM TEST_A;
                             QUERY PLAN
---------------------------------------------------------------------
 Aggregate  (cost=2.75..2.76 rows=1 width=4)
   Output: max(((a + 1) + 2))
   -&gt;  Seq Scan on public.test_a  (cost=0.00..2.00 rows=100 width=4)
         Output: a, b, c, d
(4 rows)
</code></pre>
<h3 id="-4">小结</h3>
<p>本章的表达式规范化实际上是对表达式的整理，主要是为后续的优化工作做准备，优化器后面很多针对表达式的使用都是按照顶层是合取范式来做的。PostgreSQL 对表达式的调整比较少，不会对表达式进行深度展开以及变形，因为 PostgreSQL 发现即使进行了深度整理，在表达式上获得的收效甚微，反而浪费了生成执行计划的时间。</p></div></article>