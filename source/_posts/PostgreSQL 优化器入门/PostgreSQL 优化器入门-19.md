---
title: PostgreSQL 优化器入门-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>PostgreSQL 数据库分别采用了动态规划方法和遗传算法来选择最优的执行计划。动态规划方法需要遍历全部的解空间（有优化），它一定能够获得最优解，因此是我们首选的方法。遗传算法则只能尝试从局部最优解向全局最优解不断逼近，但由于遗传代际的数量的限制，最终可能产生的是局部最优解。这种方法在表比较多的时候被采用，因为在表比较多的时候，动态规划的解空间快速地膨胀，可能会导致查询性能的下降，遗传算法的复杂度则可以限制在一定的范围内。</p>
<h3 id="">动态规划方法</h3>
<p>我们先来看一下 PostgreSQL 数据库是如何使用动态规划方法来选择最优解的，假设参与连接的有 3 个表以及它们上面分别有索引：</p>
<pre><code>CREATE TABLE TEST_A(A INT, B INT, C INT, D INT);
CREATE TABLE TEST_B(A INT, B INT, C INT, D INT);
CREATE TABLE TEST_C(A INT, B INT, C INT, D INT);

INSERT INTO TEST_A SELECT I, I+100, I+200, I+300 FROM GENERATE_SERIES(1,100) i;
INSERT INTO TEST_B SELECT I, I+100, I+200, I+300 FROM GENERATE_SERIES(1,100) i;
INSERT INTO TEST_C SELECT I, I+100, I+200, I+300 FROM GENERATE_SERIES(1,100) i;

CREATE INDEX TEST_A_IDX ON TEST_A(A);
CREATE INDEX TEST_B_IDX ON TEST_B(A,B);

ANALYZE TEST_A;
ANALYZE TEST_B;
ANALYZE TEST_C;
</code></pre>
<p>我们来看这样一个示例的动态规划的过程：</p>
<pre><code>TEST_A LEFT JOIN TEST_B 
    ON TEST_A.A = TEST_B.A 
LEFT JOIN TEST_C 
    ON TEST_A.B = TEST_C.B
</code></pre>
<p>在进入动态规划之前，我们会先建立每个表的扫描路径。对于 TEST_A 而言，由于语句中有约束条件 "TEST_A.A = TEST_B.A"，这种约束条件可能用来做 MergeJoin，而 MergeJoin 需要对参与连接的表进行排序，而恰好 TEST_A.A 上有一种情况是有序的，那就是对 TEST_A_IDX(A) 进行扫描，这个索引是 B 树索引，因此这个扫描路径产生的结果是有序的。因此，对 TEST_A 的扫描会考虑两种路径：</p>
<pre><code>SeqScan(TEST_A);
IndexScan(TEST_A);
</code></pre>
<p>TEST_B 和 TEST_A 类似，因此它也可以用下面两种路径：</p>
<pre><code>SeqScan(TEST_B);
IndexScan(TEST_B);
</code></pre>
<p>如果仔细观察 "TEST_A LEFT JOIN TEST_B ON TEST_A.A = TEST_B.A" 这部分，我们可以发现一个问题——假如我们把 "TEST_A.A = TEST_B.A" 中的 TEST_A.A 看成常量，这个语句就变成了 "CONST = TEST_B.A"，也就是 "TEST_B.B = CONST" 这种形式。这种形式的约束条件是能下推的，可以变成 "TEST_A LEFT JOIN (SELECT * FROM TEST_B WHERE TEST_B.A = CONST) ON TRUE"，而 "TEST_B.A = CONST" 这样的约束条件用来生成索引扫描再合适不过了。</p>
<p>但 TEST_A.A 并不是常量，所以我们要想办法让他变成常量。我们可以把这种情况变成 "TEST_B.A = [PARAM]"，在执行器进行连接操作的时候就可以先获得 TEST_A.A 的值，然后替换到 "TEST_B.A = [PARAM]" 中，这样就能使用索引扫描了，因此对 TEST_B，我们还能生成一种参数化索引扫描路径：</p>
<pre><code>IndexScan(TEST_B) PARAM WITH TEST_A.A
</code></pre>
<p>对于 TEST_C 而言，这个表上没有索引，因此只能使用 SeqScan 的方式进行扫描：</p>
<pre><code>SeqScan(TEST_C)
</code></pre>
<p>有了这些扫描路径之后，就好像大厦打好了地基，就可以考试考虑连接操作了。我们先来生成两个表和两个表之间的连接，比如我们可以先生成 TEST_A 和 TEST_B 之间的连接路径。那么，我们可以有几种选择呢？首先 TEST_A 上有两个扫描路径待选，TEST_B 上有 3 个扫描路径待选，这样就有 2 * 3 共 6 种情况：</p>
<pre><code>1.SeqScan(TEST_A)
  SeqScan(TEST_B)

2.SeqScan(TEST_A)
  IndexScan(TEST_B);

3.SeqScan(TEST_A)
  IndexScan(TEST_B) PARAM WITH TEST_A.A

4.IndexScan(TEST_A)
  SeqScan(TEST_B)

5.IndexScan(TEST_A)
  IndexScan(TEST_B);

6.IndexScan(TEST_A)
  IndexScan(TEST_B) PARAM WITH TEST_A.A
</code></pre>
<p>同时我们又知道连接操作有 3 种方法来实现，分别是嵌套循环连接、哈希连接、归并连接，因此上面的 6 种情况的每一种又可以扩展为 6 * 3 = 18 种连接路径，例如：</p>
<pre><code>1.1 Merge Join
        SeqScan(TEST_A)
           SeqScan(TEST_B)

1.2 Hash Join
        SeqScan(TEST_A)
           SeqScan(TEST_B)

1.3 Nestlooped Join
        SeqScan(TEST_A)
           SeqScan(TEST_B)

2.1 Merge Join
        SeqScan(TEST_A)
           IndexScan(TEST_B)

2.2 Hash Join
        SeqScan(TEST_A)
           IndexScan(TEST_B)

2.3 Nestlooped Join
        SeqScan(TEST_A)
           IndexScan(TEST_B)

………………
</code></pre>
<p>上面的情况只考虑了 TEST_A LEFT JOIN TEST_B 的情况，但实际上我们还要考虑 TEST_B RIGHT JOIN TEST_A 的情况，因为这两种情况是等价的，因此两个表连接的方法就更多了。</p>
<p>当然，有些连接路径是生成不出来的，比如：</p>
<pre><code>3.1 Merge Join
        SeqScan(TEST_A)
           IndexScan(TEST_B) PARAM WITH TEST_A.A

5.1 Hash Join
        SeqScan(TEST_A)
           IndexScan(TEST_B) PARAM WITH TEST_A.A
</code></pre>
<p>这种参数化路径只能支持嵌套循环连接的形式，对于哈希连接和归并连接是不支持的，因此这种路径是生成不出来的。</p>
<p>生成这么多的路径显然有些是不需要的，这就要采用一些淘汰机制。假如一个连接路径没有什么优势，那就没有必要建立了，因此 PostgreSQL 提供了一个预检机制，我们给一个简单的例子：</p>
<pre><code>3.1 Merge Join
        SeqScan(TEST_A)
           SeqScan(TEST_B)

3.2 Merge Join
        IndexScan(TEST_A)
           IndexScan(TEST_B)
</code></pre>
<p>同样是 Merge Join，但是如果下层选用了 SeqScan，就需要再增加一层排序结点：</p>
<pre><code>3.1 Merge Join
        Sort(TEST_A.A)
            SeqScan(TEST_A)
        Sort(TEST_B.A)
               SeqScan(TEST_B)
</code></pre>
<p>而如果下层使用的是 IndexScan，由于 TEST_A_IDX 在 TEST_A.A 上有序，TEST_B_IDX 在 TEST_B.A 上有序，因而就可以不用再进行排序了。这也就免掉了排序的代价，所以像 3.1 那样的连接路径，就可能没什么优势了，也就可以不用创建了。</p>
<p>上面只考虑了 TEST_A 和 TEST_B 的情况，我们还需要考虑 TEST<em>A 和 TEST</em>C 的情况以及 TEST<em>B 和 TEST</em>C 的情况，结合连接顺序交换规则：</p>
<pre><code>等式1.2： (A leftjoin B on (Pab)) leftjoin C on (Pac)
       = (A leftjoin C on (Pac)) leftjoin B on (Pab)
</code></pre>
<p>我们可以发现 TEST_B 和 TEST_C 如果进行连接是不行的，也就是说:</p>
<pre><code>  (A leftjoin B on (Pab)) leftjoin C on (Pac)
≠ A leftjoin （B LEFT JOIN C ON TRUE) on (Pab) and P(ac)
</code></pre>
<p>因此产生 TEST_B 和 TEST_C 这样的连接是没有价值的，所以 PostgreSQL 也不会产生这种类型的连接路径，总之连接路径的生成需要基于几个基本规则：</p>
<ul>
<li>连接路径是合理合法的</li>
<li>连接路径和已经存在的连接路径相比，必须有优势</li>
</ul>
<p>综合上面的示例，在两个表进行连接的阶段，我们只生成了 TEST_A 和 TEST_B 的连接路径、TEST_A 和TEST_C 的连接路径，然后我们就进入到第三个步骤，生成 3 个表的连接路径，也就是：</p>
<ul>
<li>TEST_A 和 TEST_B 的连接路径 + TEST_C 的扫描路径</li>
<li>TEST_A 和 TEST_C 的连接路径 + TEST_B 的扫描路径</li>
</ul>
<p>我们以 "TEST_A和TEST_B的连接路径 + TEST_C的扫描路径" 的情况为例，实际上我们可以把 "TEST_A和TEST_B 的连接路径" 看成是一个表，这样就能把这 3 个表的连接抽象成仍然是两个表的连接，因此它又能生成 3 种连接路径：</p>
<pre><code>1.1.1 Merge Join
            MergeJoin
                SeqScan(TEST_A)
                   SeqScan(TEST_B)
               SeqScan(TEST_C)

1.1.2 Hash Join
            MergeJoin
                SeqScan(TEST_A)
                   SeqScan(TEST_B)
               SeqScan(TEST_C)

1.1.3 Nestlooped Join
            MergeJoin
                SeqScan(TEST_A)
                   SeqScan(TEST_B)
               SeqScan(TEST_C)

………………
</code></pre>
<p>我们把 3 个表的情况抽象成了两个表的情况，因此它的连接路径的生成原则和两个表的也是一样的，我们就不再赘述了。</p>
<p>3 个表的情况还算比较简单，我们这里还只是考虑了左深树的情况，实际上还应该考虑一下浓密树的情况。生成浓密树则抛开了扫描路径，它将各个层次的连接路径尝试进行连接，例如将第 N−2 层连接路径和第 2 层的连接路径进行连接，以此类推出（2，N−2）、(3，N−3)、 (4, N−4)等多种情况，比如有 A、B、C、D 共 4 个表，那么浓密树还要考虑的是：</p>
<ul>
<li>A 和 B 产生的连接路径 + C 和 D 产生的连接路径</li>
<li>A 和 C 产生的连接路径 + B 和 D 产生的连接路径</li>
<li>......</li>
</ul>
<p>在具体的使用过程中，我们把 "A 和 B 产生的连接路径" 和 "C 和 D 产生的连接路径" 分别看成两个表，这样就能继续采用连接路径的方法来生成新的连接路径。</p>
<p>采用上面这样的方法，我们就能“无限的递归”下去，生成无数表的连接路径，但是从路径的数量来看，也就像“宇宙大爆炸”一样的快速攀升了，表的数量越多，路径的数量也就越多。这时候，我们可以开始考虑另一件事，换一种路径的搜索方法——采用遗传算法来进行路径的搜索。</p>
<h3 id="-1">遗传算法</h3>
<p>物竞天择，适者生存，这是大自然的普遍规律。PostgreSQL 把这种普遍的方法借用到连接路径搜索中，一方面是借助了随机的威力，另一方面是借助了遗传的特点。</p>
<p>我们常说进行连接操作的表超过 12 个就可能会通过遗传算法来进行最优路径的筛选工作，但实际上这个值是受 GUC 参数 geqo_threshold 控制的，这个 GUC 参数的默认值是 12。</p>
<p>不过即使参与连接的表达到了 geqo_threshold 的要求，PostgreSQL 也不会轻易选择遗传算法，还需要通过另一个 GUC 参数 geqo 打开遗传算法。也就是说要想启用遗传算法，必须满足：</p>
<pre><code>geqo = true 且 表的数量 &gt; geqo_threshold
</code></pre>
<p>假设有 TEST_A、TEST_B、TEST_C、TEST_D 共 4 个表做连接操作（PostgreSQL 对 4 个表的情况不会启用遗传算法，但我们这里使用较少的表是为了简化说明的复杂度）。第一步把每个表看做一个基因，然后借助随机的威力来生成一个种群，每个种群是由多个染色体组成的，实际上一个染色体就对应一种执行计划。为了简化，我们看一个有 3 条染色体的种群：</p>
<pre><code>染色体1：TEST_A,TEST_B,TEST_C,TEST_D
染色体2：TEST_B,TEST_C_TEST_A,TEST_D
染色体3：TEST_D,TEST_A,TEST_B,TEST_C
</code></pre>
<p>种群中的每个染色体实际上就是 TEST_A、TEST_B、TEST_C、TEST_D 这 4 个表的一种排列，如果是 4 个表最多能生成 4！=24 种染色体，表的数量超过 12 个，穷举就会产生 479001600 种可能的染色体。这就有点过分了，实际上，种群的数量也是受到限制的。通过 GUC 参数 geqo_pool_size 可以控制种群的大小，不过，通常我们不这样做，而是借助另一个 GUC 参数 geqo_effort 来控制种群的大小。</p>
<p>只有 geqo_pool_size 参数没有设置的情况下，geqo_effort 参数才有效果，geqo_effort 的默认值是 5，让我们看看怎么用它来获得种群的数量：</p>
<pre><code>n = 参与连接的表的数量
种群初值 = 2 ^ (n + 1)
种群上限 = geqo_effort * 50
种群下限 = geqo_effort * 10

如果种群初值介于上限和下限之间，则取种群初值
如果种群初值大于种群上限，则取种群上限值
如果种群初值小于种群下限，则去种群下限值
</code></pre>
<p>在种群初始化之后，其中的每个染色体代表一个执行计划，早期的 PostgreSQL 中，染色体 1 可以用一个左深树来表示。但是 PostgreSQL 发现，用左深树表示经常会产生一些不合法的路径（比如有些表必须出现在另一些表的前面，而种群初始化是随机产生的，根本不考虑这些），于是，后来 PostgreSQL 改进了这种情况，不再使用左深树了，而是尽量产生能够执行的路径（但是染色体中表的顺序仍然很重要）。如果实在不能产生执行计划，染色体的代价就设置成无限大，最终这个染色体就会被淘汰掉。</p>
<p>染色体的代价也就是染色体所代表的连接路径的代价，在遗传算法中，可以称其为适应度。种群中的染色体根据它的适应度进行排序，代价小的放到前面，代价大的放到后面。这么做有两个好处，一个是方便淘汰代价大的染色体，另一个是为了方便我们选择父母染色体。</p>
<p>种群中的染色体排序之后，我们还要继续对种群进行更新，也就是借助代际遗传的特点，把种群不断进行优化。我们随机的在种群中选择两个染色体进行杂交，虽然说是随机选择父母染色体，但是也并非平坦的随机，而是借助了概率随机的方法，在选择的过程中更倾向于选择排在前面的染色体，因为这些染色体“基因好”。这种随机的概率密度是符合一定分布的，我们可以用 geqo_selection_bias 这个 GUC 参数对随机概率的密度进行调整，概率密度函数为：</p>
<pre><code>f(x) = bias - 2(bias - 1)x
</code></pre>
<p>从函数的定义我们可以看出这是一个单调递减函数。在 [0,1] 的范围内，x 的值越是接近 0，对应的 f(x) 的值越大，正好符合了“借助了概率随机的方法，在选择的过程中更倾向于选择排在前面的染色体”这样的情况。</p>
<p>杂交的过程其实就是从父染色体和母染色体中选择基因的过程，这个过程可以多种多样，但是最终还是采用随机的方法，比如可以借用洗牌算法来实现。</p>
<p>杂交之后产生的染色体也放到种群里，由于种群中的染色体是已经排序的染色体，所以新染色体放到种群中之后仍然要保持种群的有序性。并且新染色体会排挤掉一个适应度差的染色体，也就是说排在队尾的染色体会被淘汰掉。</p>
<p>然后再重复地在种群中选择父母染色体，杂交，淘汰，那要重复多少次呢？这取决于用户有没有设置 geqo_generations 参数。通过设置 geqo_generations 可以指定遗传算法进行多少次遗传，如果用户没有指定 geqo_generations，则进行遗传的次数和种群池中染色体的数量相同。</p>
<p>另外，在上述的过程中，我们会大量用到随机数，这些随机数的 seed 也可以通过 GUC 参数来控制。这个参数是 geqo_seed，它是一个介于 0-1 之间的值，通过调整 seed 值，可以更好地利用随机特性来对染色体进行选择。</p>
<h3 id="-2">小结</h3>
<p>PostgreSQL 目前在生成物理路径之前都进行了预处理，也就是说对路径的搜索复杂度大大降低了，因此，可以适当放宽动态规划算法的表的个数，把 geqo_threshold 的值调大一些。</p></div></article>