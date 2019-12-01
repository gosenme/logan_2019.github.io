---
title: PostgreSQL 优化器入门-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>选择执行计划之后，这个执行计划就可以开始执行了。PostgreSQL 数据库的执行器是一个流水线式的火山模型，“流水线”的意思是说它每次只处理一条元组，“火山模型”的意思是它是一个“拉取”式的模型，也就是对执行计划进行后序遍历。为了方便说明，我们来看一个例子。</p>
<p>假设有 2 个表，他们的数据分别如下：</p>
<p>TEST_A 表：</p>
<table>
<thead>
<tr>
<th>A</th>
<th>B</th>
<th>C</th>
<th>D</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>1</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>2</td>
<td>2</td>
<td>2</td>
<td>2</td>
</tr>
</tbody>
</table>
<p>TEST_B 表：</p>
<table>
<thead>
<tr>
<th>A</th>
<th>B</th>
<th>C</th>
<th>D</th>
</tr>
</thead>
<tbody>
<tr>
<td>2</td>
<td>2</td>
<td>2</td>
<td>2</td>
</tr>
<tr>
<td>3</td>
<td>3</td>
<td>3</td>
<td>3</td>
</tr>
</tbody>
</table>
<p>如果要对 TEST_A 进行扫描，它的执行计划应该是这样的：</p>
<pre><code>postgres=# EXPLAIN VERBOSE SELECT * FROM TEST_A WHERE A = 1;
                          QUERY PLAN
--------------------------------------------------------------
 Seq Scan on public.test_a  (cost=0.00..1.04 rows=1 width=16)
   Output: a, b, c, d
   Filter: (test_a.a = 1)
(3 rows)
</code></pre>
<p>这是一个普通的顺序扫描路径，它的主要作用就是对一个表进行全表扫描，PostgreSQL可以通过 shared_buffer 参数来控制缓冲区的大小。如果缓冲区足够大， 实际上大部分数据可能都已经被加载到缓存里了，对这些数据的读取就是直接从缓存中拿到页面，然后从页面中提取元组。</p>
<p>但也有的时候我们需要的某个元组（或者说元组所在的页面）没有在缓存中，而是在磁盘上，那么扫描路径不会去磁盘直接提取元组，而是先要把磁盘的页面加载到缓存中，这时候就可能产生换页。产生这种情况的原因是缓存中很可能没有空闲页面，把新的页面加载到缓存，必然就需要缓存中的一个页面写入磁盘，这样新页面才有缓存位置。</p>
<p>和扫描路径直接相关的是缓存地址。通常我们不直接去磁盘上拉取元组，一旦发现想要获取的元组不在缓存中，就需要将元组所在的磁盘页面加载到缓存，然后再从缓存中拉取对应的元组。</p>
<p>对于每个表，在 pg_class 中都会有一个元组与之对应，这个元组中包含一个 relfilenode 属性，其中的数字就是这个表的数据文件的文件名。在数据目录中搜索这个数组，就能找到对应表的数据文件，缓存就是从这个数据文件中加载数据页面的。</p>
<p>执行顺序扫描要有一个起始页面，那么，使用哪个页面作为起始页面呢？我们当然可以选择从第一个页面一直遍历到最后一个页面，但我们也可以优化一下。比如，现在有 10 个会话在同时查询这个表，它们都不停地向前读取页面，我们可以要求这些线程在向前读取页面的过程中，随时汇报它们已经读到了哪个页面。这样我们在开始扫描的时候，就可以采用它们最新汇报的那个页面作为开始页面，从而避免其他会话向后读取完一个页面之后，还要向前读取页面。在缓存较小很多页面在磁盘上的时候，这样的情况会有更明显的效果。</p>
<p>实际上，顺序扫描的路径并不是直接去磁盘上读取数据，PostgreSQL 还抽象出了存取层的概念，也就是说所有的扫描路径的执行都是基于在存取层之上的。存取层要做的事情就是屏蔽存取细节，无论我们要读取的是何种存储形式。比如对于 FunctionScan，它在执行的时候存取层会提供一个存取层函数，这个存取层函数负责不停地向 FunctionScan 返回元组，至于存取层函数是如何获取这个元组，扫描路径并不关心这些细节。对于顺序扫描而言，它需要借用顺序扫描的存取层函数，这个存取层函数的作用就是去缓存页面上读取元组，并且记录当前处理到了哪条元组的偏移量。要获得下一条元组，只需要修改这个偏移量即可。</p>
<p>下面通过一组图来看一下示例中的顺序扫描的执行过程。假设 TEST_A 表中的所有页面都已经加载到了缓存中，鉴于示例中的数据量比较小，无须考虑从哪个磁盘页面开始的问题，这样就可以直接从缓存中得到第一条元组。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/48b3a600-d679-11e8-be45-7958f66a47cf" width="350px" /></div>
<p></br></p>
<p>获得到对应的元组后，差不多每个执行算子都要做两件事：</p>
<ul>
<li>执行约束条件（表达式），对元组进行过滤，查看一下这条元组是否符合要求；</li>
<li>按照投影的要求生成新的元组，实际上投影的过程也是执行表达式的过程。</li>
</ul>
<p>"TEST_A.A = 1" 这样的约束条件，本质上是一个表达式，"TEST_A.A" 是 int 类型，“1”也是 int 类型，所以我们可以说这个表达式就是用于判断两个 int 是否相等的表达式。从 PG_OPERATOR 系统表中可以看到这个表达式，并且这个表达式最终映射到了系统函数 “int4eq” 上。</p>
<pre><code>postgres=# SELECT oid, typname FROM PG_TYPE WHERE typname='int4';
 oid | typname
-----+---------
  23 | int4
(1 row)

postgres=# SELECT oid, typname FROM PG_TYPE WHERE typname='bool';
 oid | typname
-----+---------
  16 | bool
(1 row)

postgres=# SELECT oprname, oprleft, oprright, oprresult, oprcode FROM PG_OPERATOR WHERE oprname = '=' AND oprleft = 23 AND oprright = 23;
 oprname | oprleft | oprright | oprresult | oprcode
---------+---------+----------+-----------+---------
 =       |      23 |       23 |        16 | int4eq
(1 row)

postgres=# SELECT proname, prosrc, pronargs, proargtypes FROM PG_PROC WHERE proname='int4eq';
 proname | prosrc | pronargs | proargtypes
---------+--------+----------+-------------
 int4eq  | int4eq |        2 | 23 23
(1 row)
</code></pre>
<p>如果通过执行约束条件发现这个元组符合约束条件，那么就可以按照投影的要求生成投影，并且把元组发送给上层结点，最终发送到前端。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/ef133380-d679-11e8-be45-7958f66a47cf" width="350px" /></div>
<p></br></p>
<p>然后重新执行 SeqScan 结点，它会继续尝试获得新的元组。需要注意的是<strong>重新执行 SeqScan 结点</strong>这几个字，或许你以为我们是不停自动地发送元组给上层结点，但实际上 PostgreSQL 的执行器是一个拉取的模型，而且是“一次一元组”的形式，也就是说每获得一条元组，都要把执行计划重新执行一遍。SeqScan 结点也是在等上层结点的拉取，上层结点打算获得元组的时候，SeqScan 就把这个要求交给存取层。</p>
<p>这种一次一元组的形式要求每个执行算子都要记录自己的上下文信息，以便在下次执行的时候知道自己应该做些什么。对于存取层也是一样，上一次执行时元组的偏移量就是这种上下文信息，如果没有这种信息，存取层就没有办法知道自己应该去哪里读取下一条元组了。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/5c2da6d0-d67a-11e8-9d3a-e5c2f8f2166f" width="350px" /></div>
<p></br></p>
<p>但是如果获得的元组不满足约束条件，也就是说从存取层获得的元组不会返回给上层，那么 SeqScan 就直接再次调用存取层去获得下一条元组。也就是说，每个执行算子只有在拉取到符合约束条件的元组之后才会返回给上层。如果拉取到的元组不符合条件，也就是没有获得到符合条件的“一次一元组”，还需要去重新拿符合条件的元组，直到所有的元组处理完毕。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/acae5320-d67a-11e8-be45-7958f66a47cf" width="140px" /></div>
<p></br></p>
<p>当所有的元组都处理完毕，那么会从下至上地返回一个 NULL 元组，这就标志着下层已经没有元组给上层了，也就预示着查询需要结束了。</p>
<div style="text-align:center">
<img src="https://images.gitbook.cn/db815300-d67a-11e8-9d3a-e5c2f8f2166f" width="350px" /></div>
<p></br></p>
<h3 id="">小结</h3>
<p>上面提供的是顺序扫描路径的过程，由此及彼，索引扫描、位图扫描、Function 扫描、SubQueryScan 都有自己的存取层方法，它们的执行过程基本上是类似的。可以看出一个扫描结点在执行的过程中，它主要做了这么 3 件事：</p>
<ul>
<li>调用存取层方法获得下一条元组；</li>
<li>对元组进行过滤，看元组是否符合约束条件；</li>
<li>根据投影的要求，结合获得的元组计算新的投影。</li>
</ul></div></article>