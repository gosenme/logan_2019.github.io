---
title: PostgreSQL 优化器入门-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通常，数据库就如同一个黑匣子，我们输入 SQL 语句给它，它负责反馈执行结果给我们。尤其是 SQL 又是一种入门极简单的语言，使用者只要能看懂英语就能熟练写出增删改查的简单语句，对于刚入门的用户来说肯定感觉是极好的。</p>
<p>在数据量比较少时，用户对数据库操作得比较随意，数据库也不会提出反对意见。但是随着数据量的增加，若是再胡乱地拼凑几个查询，并期望数据库给出一个完美的结果，那只能一首《凉凉》送给你——数据库罢工了。这时用户会查阅手册或者咨询一些资深的 DBA，期望得到一个“合理的解释”，但往往针对特定问题只能得到特定解决方案，下次遇到其他状况仍旧无从下手。</p>
<p>所谓求人不如求己，若用户对一个 SQL 语句进入数据库究竟经历了怎样的历程了如指掌，则可以在书写 SQL 的时候就避免 freestyle，即使遇到问题也能胸有成竹地解决。既然前景如此美好，让我们就从最简单的一个 SQL 语句开始看看，一个 SQL 语句在进入数据库之后，到底经历了什么。</p>
<h3 id="">语法分析</h3>
<p>要查询一个表中的一部分数据，用最简单的 SELECT 查询就可以了：</p>
<pre><code>SELECT * FROM TEST_A; 
</code></pre>
<p>这是一个单表查询语句，SELECT 告诉我们这是一个查询操作，FROM TEST_A 告诉我们 TEST_A 是要查询的表，而“*”则表示要输出的内容是 TEST_A 表的所有列的内容。</p>
<p>当用户将语句输入客户端工具（比如 psql）之后，客户端工具会将这个语句发送给数据库服务器，这时候 SQL 语句就进入了黑匣子里面，那么黑匣子如何处理它呢？</p>
<p>首先，黑匣子会通过 Lex 工具对 SQL 语句进行词法分析并产生 token，这些 token 都带有固定的词性，比如 token 可以是关键字、标识符、常量、运算符或边界符等。下面的内容展示了 SQL 语句被拆解成 token 之后的词性：</p>
<pre><code>c++
SELECT：    关键字
*：        常量
FROM：    关键字
TEST_A：    常量
; ：        边界符
</code></pre>
<p>语法分析器则接收词法分析产生的 token，并结合它的词性开始按照定义好的语法规则产生语法树。语法分析的规则在虽然算是内核中的源码，但是定义起来是非常简单的，这是因为语法分析使用的是 Yacc 工具。这个工具负责真正的语法分析，而使用者只需要定义语法规则即可，我们从中摘取一小部分语法规则来看一下：</p>
<pre><code>simple_select:
    SELECT opt_all_clause opt_target_list
    into_clause from_clause where_clause
    group_clause having_clause window_clause
    {
        SelectStmt *n = makeNode(SelectStmt);
        n-&gt;targetList = $3;
        n-&gt;intoClause = $4;
        n-&gt;fromClause = $5;
        n-&gt;whereClause = $6;
        n-&gt;groupClause = $7;
        n-&gt;havingClause = $8;
        n-&gt;windowClause = $9;
        $$ = (Node *)n;
    }
</code></pre>
<p>如果熟悉 SQL 语法的规则，那么很容易从上面的代码中看出各个部分的含义。Yacc 工具就结合上面的规则同时根据 token 的内容产生语法树，比如 Lex 交给 Yacc 一个 SELECT 关键字，Yacc 就可以找到上面的 simple_select 规则，并最终根据规则创建一个查询类型的语法树结点。</p>
<p>示例中的 SQL 语句中的投影列是“*”，也就是说要把 TEST_A 表中所有的列都投影出来，但 Yacc 工具并不了解这些，所以它直接把一个“*”保存成列信息。</p>
<p>经过语法分析，原来的 SQL 语句就转变成一棵语法树，这棵语法树包含下面的内容：</p>
<pre><code>是 SELECT 查询操作
    -&gt; 投影，目前的内容是 “*”
    -&gt; 要查询的表，目前的内容是表名 TEST_A
</code></pre>
<div style="text-align:center">
<img src="https://images.gitbook.cn/0366f830-cdd8-11e8-8458-03f9794b87bd" width="200px" /></div>
<p></br></p>
<p>当然，如果用户在写 SQL 语句的时候显式地指定了具体的投影列，比如：</p>
<pre><code>SELECT a, b, c, d FROM ...
</code></pre>
<p>Yacc 就会用一个链表来表示需要进行投影的列，这个链表中有 4 个结点，这 4 个结点分别保存的是列名：a、b、c、d。</p>
<p>FROM 作为一个关键字，表示对 SQL 语句的解析进入了新的状态，FROM 后面接着的就是要查询的表——TEST_A，这时虽然语法分析器能知道 TEST_A 是一个表，但它对这个表掌握的信息也只有表名而已，我们在查询某个表的时候有时候还会指定这个表属于哪个 schema，这些和表名一样，统统都以记录名字的方式记录下来。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/195c75c0-cdd8-11e8-8458-03f9794b87bd" width="200px" /></div>
<p></br></p>
<h3 id="-1">语义分析</h3>
<p>语法分析器实际上是很懒的，它只专注于对 SQL 语句做解析，获得的信息也全部来源自 SQL 语句，其他的一概不管。比如在 SQL 语句中遇到要查询的表，就把表的名字记下来了，但是这个表是不是真的存在，它并不去检查。语法树生成之后，语法分析器就成功地把锅甩给了语义分析器。语义分析器接到这样一个“烂摊子”，就开始它的工作——<strong>检查和转换</strong>：</p>
<ul>
<li>先检查这些对象是不是真的存在，如果用户输入了错误的表名和列名，语义分析器的小拳拳就会锤你胸口——把错误从黑匣子中抛出来；</li>
<li>如果这些对象真的存在的话，就转换成内部形式来保存。</li>
</ul>
<p>要转成内部形式来保存的原因是，这个查询语句实在是太简单了，信息严重不足，要对一个表进行查询，至少要知道这个表的结构吧？比如它有几个列属性、每个属性是什么类型、它是一个什么类型的表、这个表上有没有索引之类的，上述这些信息在一个简单的 SQL 语句里都没有表达出来，这都依赖于语义分析器从数据库的<strong>元数据</strong>中读取。</p>
<p>PostgreSQL 有很多系统表来保存这些元数据信息，比如 PG_CLASS 系统表保存了所有表的描述信息，PG_ATTRIBUTES 系统表则用来保存每个表的所有的列属性信息，再比如 PG_INDEX 用来保存索引的信息等，所谓一方有难八方支援，当我们知道要查询一个表的名字的时候，我们需要把和这个表名相关的这些元数据组织起来。用有组织的元数据来代表这个表，这个过程就是语义分析。</p>
<p>在语法树中我们已经明确了每个对象的含义，因此可以借助遍历语法树来进行检查和转换的工作。</p>
<p>比如在语法树中遇到 TEST_A 就知道它是个表名而非列名，所以就可以去 PG_CLASS 里获取到这个表的基本信息，然后再根据 PG_CLASS 里的基本信息分别获取各种其他信息。通常数据库为了提高性能，会将这些表的信息缓存到主存里，所以每次获取表的元信息不一定都需要从磁盘上读取。</p>
<p>再比如在语法树的投影中遇到“*”，语义分析器就知道需要把它展开，这个展开的过程就需要去 PG_ATTRIBUTE 系统表中找到 TEST_A 表所对应的列属性的信息，用这些列属性信息把“*”替换掉。在 PG_ATTRIBUTE 表中记录了这些列的位置，也就是它们各自属于 TEST_A 的“第几列”。这个“第几列”就可以用来表示对应的列属性，而不再使用列名了。下面示例中的 attnum 就是表示列名对应的列是表的“第几列”（注：请忽略这些显示为负数的列，它们是“伪列”，如果不显式地在投影列中指定的话，是不会投影出来的）：</p>
<pre><code>postgres=# select attname, attnum  
from pg_attribute 
where attrelid = 
    (select oid 
     from pg_class
     where relname = 'test_a');
 attname  | attnum
----------+--------
 tableoid |     -7
 cmax     |     -6
 xmax     |     -5
 cmin     |     -4
 xmin     |     -3
 ctid     |     -1
 a        |      1
 b        |      2
 c        |      3
 d        |      4
(10 rows)
</code></pre>
<p>在经过语义分析之后，我们就可以获得一个查询树了，查询树和语法树本质上应该是等价的，但是他们表示信息的方式发生了变化：</p>
<pre><code>是 SELECT 查询操作
    -&gt; 投影，“*”已经被展开成为具体的列，
        不只记录列名，而是通过
        该列在所在表的“第几列”来表示
            -&gt;第 1 列是 a，第 2 列是 b，第 3 列是 c，第 4 列是 d
    -&gt; 要查询的表，通过表名找到该表的OID
        并且将表的所有信息组织成一个描述符
</code></pre>
<div style="text-align:center">
<img src="https://images.gitbook.cn/bca6dc30-ade8-11e8-96f9-9d9fc127863b" width="200px" /></div>
<p></br></p>
<h3 id="-2">查询重写</h3>
<p>在语义分析之后，还需要对查询树做一个重写（rewrite）操作，PostgreSQL 数据库可以让用户自己制定规则对查询树进行改写，不过最常用这种规则的还是对视图的改写，比如我们创建一个视图：</p>
<pre><code>CREATE VIEW TEST_A_VIEW AS SELECT * FROM TEST_A;
</code></pre>
<p>如果针对这个视图进行查询：</p>
<pre><code>SELECT * FROM TEST_A_VIEW;
</code></pre>
<p>虽然我们创建的视图也会在 PG_CLASS 系统表里建立一个“虚”的表，但是它没有存储结点，没有办法写入数据，也没有办法使用视图直接访问磁盘上的数据，所以最终还是要通过 TEST_A_VIEW 和 TEST_A 之间的映射关系把对视图的查询转化到对表的查询上。因此，创建视图的时候，同时创建了重写（rewrite）规则，这些规则保存在 PG_REWIRTE 系统表中，创建 TEST_A_VIEW 会在 PG_REWRITE 系统表中记录“SELECT * FROM TEST_A”的查询树，由于查询树的内容比较长，我们就不在这里展示了，读者可以通过下面的 SQL 语句来一睹查询树的芳容：</p>
<pre><code>SELECT * 
FROM PG_REWRITE 
WHERE EV_CLASS = 
    (SELECT OID 
     FROM PG_CLASS 
     WHERE RELNAME = 'TEST_A');
</code></pre>
<p>对查询树进行视图重写的过程就是将这棵查询树替换到“SELECT * FROM TEST_A_VIEW”产生的查询树中的过程，也就形成了类似下面的结构：</p>
<pre><code>SELECT 查询操作，针对 TEST_A_VIEW 视图
    -&gt; 投影，通过在视图中的“第几列”来表示
        -&gt;第 1 列是 a，第 2 列是 b，第 3 列是 c，第 4 列是 d
    -&gt; 要查询的视图
        -&gt; SELECT 查询操作，针对 TEST_A 表
            -&gt; 通过在表中的“第几列”表示
                -&gt; 第 1 列是 a，第 2 列是 b，第 3 列是 c，第 4 列是 d
            -&gt; 要查询的 TEST_A 表
</code></pre>
<div style="text-align:center">
<img src="https://images.gitbook.cn/cad4ed10-ade8-11e8-9cb7-a50d7ea43bbb" width="350px" /></div>
<p></br></p>
<p>实际上目前这棵查询树和下面的语句是等价的，视图相当于一个子查询：</p>
<pre><code>SELECT * FROM (SELECT * FROM TEST_A) ta;
</code></pre>
<p>查询树在经历了重写之后，语义分析器就举办一个简单的交接仪式，正式把查询树转交给优化器了。优化器对查询树先进行逻辑优化，也就是按照优化规则进行优化，这是一种精准的微整容，在优化的过程中它还保留查询树的基本样貌，只是垫垫鼻子，削削下巴，比如视图会被当做子查询放到查询树里，在逻辑优化阶段就会查看一下这个子查询是不是能提升，也就是说子查询能不能消除掉，比如我们这里的两个查询实际上是完全等价的：</p>
<pre><code>postgres=# EXPLAIN SELECT * FROM TEST_A;
                        QUERY PLAN
-----------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..28.50 rows=1850 width=16)
(1 row)

postgres=# EXPLAIN SELECT * FROM TEST_A_VIEW;
                        QUERY PLAN
-----------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..28.50 rows=1850 width=16)
(1 row)

postgres=# EXPLAIN SELECT * FROM (SELECT * FROM TEST_A) A;
                        QUERY PLAN
-----------------------------------------------------------
 Seq Scan on test_a  (cost=0.00..28.50 rows=1850 width=16)
(1 row)
</code></pre>
<p>逻辑优化就是做等价的逻辑变换，借由这种逻辑变换，将一棵低效的查询树转换成为一棵高效的查询树。逻辑优化之后就进入了物理优化阶段，它会生成很多的查询路径，比如顺序扫描、索引扫描之类的，并且计算这些路径的代价。</p>
<p>以对 TEST_A 表的查询为例，可以生成哪些查询路径呢？</p>
<ul>
<li>它可以生成一个顺序扫描路径，因为要返回 TEST_A 表的所有元组，所以把 TEST_A 表从头到尾扫描一遍是很合理的。</li>
<li>还可以生成一个索引扫描路径（假如 TEST_A 上有索引），借助索引间接进行数据访问。</li>
</ul>
<p>代价估算系统就可以根据上面两种路径（顺序扫描路径和索引扫描路径）对数据的访问方式，估计出来一个可比较的代价，这样优化器就可以和所有可能的执行路径一一确认眼神，终于遇见对的人，最后把最优路径转换成具体的执行计划。</p>
<h3 id="-3">打印执行计划的参数</h3>
<p>如果读者有兴趣，PostgreSQL 数据库也提供了 GUC 参数让我们查看查询树和执行计划树，通过打开这些参数，查询树和执行计划就能打印出来。但是查询树和执行计划树的具体结构是“偏内核”的，通常对于 PostgreSQL 的内核开发人员是比较有用的。我们这里只把这些参数简单列出来，至于查询树和执行计划树中每个结点的含义，则需要结合 PostgreSQL 源代码的分析才能说清楚，对源码分析有兴趣的读者可以查阅《PostgreSQL 技术内幕：查询优化深度探索》。</p>
<ul>
<li><strong>debug_pretty_print</strong>：打开该参数在打印查询树和执行计划时会以结构化的方式来展示，便于对查询树进行分析；</li>
<li><strong>debug_print_parse</strong>：打开该参数可以打印查询树；</li>
<li><strong>debug_print_rewritten</strong>：打开该参数可以打印重写（视图）之后的查询树；</li>
<li><strong>debug_print_plan</strong>：打开该参数可以打印执行计划。</li>
</ul>
<p>用户可以通过 SET 命令来指定这些参数：</p>
<pre><code>postgres=# SET DEBUG_PRINT_PLAN = ON;
SET
</code></pre>
<p>执行计划由执行器来执行。执行器实现了很多算子，比如我们刚才说的顺序扫描就有一个对应的顺序扫描算子，索引扫描也有一个对应的索引扫描算子。执行器根据执行计划选定的执行路径找到对应的执行算子进行数据的“计算”，我们就不再深究执行器是如何执行的了，但是我们接下来可以看看如何查看一个执行计划。</p>
<h3 id="-4">小结</h3>
<p>通过查看一个 SQL 语句的“一生”，有助于了解 SQL 语句在数据库内部的演变过程。不同的查询树产生不同的执行计划，但不同的查询树之间可能是等价的，也就代表着不同的执行计划之间也可能是等价的。因此，我们可以尝试等价地变化查询树，这就是逻辑优化（基于规则的优化）的主要工作。</p>
<p>读者可以尝试通过打开 GUC 参数的方式来查看数据库内部究竟是如何保存一个语法树、查询树和执行计划的，这将有助于提高对优化器的理解能力。</p></div></article>