---
title: 高可用 Elasticsearch 集群 21 讲-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Elasticsearch 高效运行依赖于内存的合理分配，包括堆内内存和堆外内存。无论堆内内存不足、还是堆外内存不足，都会影响运行效率，甚至是节点的稳定性。</p>
<p>在安装 Elasticsearch 前进行内存分配时，我们一般把可用内存的一半分配给 JVM，剩余一半留给操作系统缓存索引文件。本课主要关注由于 JVM 内存问题引起的长时间 GC，从而导致的节点响应缓慢问题。</p>
<h3 id="1">1. 原理与诊断</h3>
<h4 id="11">1.1 原理</h4>
<p>当集群出现响应缓慢时，在排除掉硬件资源不足的因素后，接下来就要重点分析节点的 GC 情况了。ES 内部占用内存较多的数据结构主要包括如下几个部分：</p>
<ul>
<li><p><strong>Lucene segments</strong></p>
<p>Elasticsearch 底层依赖于 Lucene 全文索引库，为了提供快速的检索服务，需要把 Lucene 的特定数据结构加载到内存，集群内的数据量越大，需要加载到内存的信息越多。</p></li>
<li><p><strong>Query Cache</strong></p>
<p>Elasticsearch 集群中的每个节点包含一个 Node Query Cache，由该节点的所有 shard 共享。该 Cache 采用 LRU 算法，Node Query Cache 只缓存 filter 的查询结果。默认大小为堆内存的 10%。</p></li>
<li><p><strong>Fielddata</strong></p>
<p>Elasticsearch 从 2.0 开始，默认在非 text 字段开启 <code>doc_values</code>，基于 <code>doc_values</code> 做排序和聚合，可以极大降低节点的内存消耗，减少节点 OOM 的概率，性能上损失却不多。</p>
<p>5.0开始，text 字段默认关闭了 Fielddata 功能，由于 text 字段是经过分词的，在其上进行排序和聚合通常得不到预期的结果。所以我们建议 Fielddata Cache 应当只用于 global ordinals。Fielddata 占用内存大小由 <code>indices.fielddata.cache.size</code> 控制，默认不限制大小。</p></li>
<li><p><strong>Index Buffer</strong></p>
<p>在索引过程中，新索引的数据首先会被放入缓存，并在合适的时机将缓存的数据刷入磁盘，这个缓存就是 Index Buffer。默认值为堆内存的 10%。</p></li>
<li><p><strong>查询</strong></p></li>
</ul>
<p>在执行查询过程中，尤其聚合查询，中间数据存储也会占用很大的内存空间。</p>
<ul>
<li><strong>其他</strong></li>
</ul>
<p>除了上面个提到的几个部分外，transport、集群状态，索引和分片管理等也会占用一部分内存。</p>
<h4 id="12">1.2 诊断</h4>
<p><strong>查看堆内内存状态</strong></p>
<p>执行下面的命令可以查看各个节点的内存状态：</p>
<pre><code>curl -sXGET "http://localhost:9200/_cat/nodes?v"
</code></pre>
<p>该命令后输出如下(本文中命令的输出会隐去节点 ip，name 等信息）</p>
<pre><code> heap.percent ram.percent cpu load_1m load_5m load_15m node.role master
           36          94   7    2.65    2.79     3.06 di        -     
           57          99  15   11.37    6.58     4.75 di        -     
           40          96   6    1.58    2.12     2.39 mdi       -     
           38         100   7    2.35    2.38     2.32 di        -     
           57          95   8    2.89    3.29     3.76 mdi       -     
           60          95   7    2.98    3.51     4.14 di        -     
           60          99   7    2.18    2.60     2.65 di        -     
           52          95   7    2.98    3.51     4.14 mdi       -     
           63          99   7    2.18    2.60     2.65 mdi       -     
           48          94   7    2.65    2.79     3.06 mdi       -     
           50          95   8    2.89    3.29     3.76 di        -     
           53          98   7    2.80    2.63     2.67 mdi       -     
           59          96   6    1.58    2.12     2.39 di        -     
           60          98   7    2.80    2.63     2.67 di        -     
           55          96   8    4.74    3.53     3.29 mdi       -     
           49          97  12    3.79    4.00     3.31 di        -     
           47          96   8    4.74    3.53     3.29 di        -     
           71          99  15   11.37    6.58     4.75 mdi       -     
           51         100   7    2.35    2.38     2.32 mdi       *     
           56          97  12    3.79    4.00     3.31 mdi       -     
</code></pre>
<p><strong>查看 GC 状态</strong></p>
<pre><code>$JAVA_HOME/bin/jstat -gc $pid
</code></pre>
<p>执行该命令后输出如下：</p>
<pre><code> S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT
1083456.0 1083456.0  0.0   391740.9 8668032.0 7715466.1 21670912.0 15789191.1 86684.0 80325.8 10908.0 9375.5 290445 24067.090 3920  14579.724 38646.814
1083456.0 1083456.0  0.0   391740.9 8668032.0 8000968.4 21670912.0 15789191.1 86684.0 80325.8 10908.0 9375.5 290445 24067.090 3920  14579.724 38646.814
1083456.0 1083456.0  0.0   391740.9 8668032.0 8230172.2 21670912.0 15789191.1 86684.0 80325.8 10908.0 9375.5 290445 24067.090 3920  14579.724 38646.814
1083456.0 1083456.0 268584.8 391740.9 8668032.0 8667696.3 21670912.0 15789440.7 86684.0 80325.8 10908.0 9375.5 290446 24067.090 3920  14579.724 38646.814
1083456.0 1083456.0 412489.4  0.0   8668032.0 1049588.2 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 2169211.9 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 3077474.4 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 4109532.1 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 5050874.2 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 5497027.7 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
1083456.0 1083456.0 412489.4  0.0   8668032.0 5850000.6 21670912.0 15790123.0 86684.0 80325.8 10908.0 9375.5 290446 24067.147 3920  14579.724 38646.872
</code></pre>
<p><strong>Elasticsearch 内部内存使用状况</strong></p>
<pre><code>curl -sXGET "http://localhost:9200/_cat/nodes?h=name,port,segments.memory,segments.index_writer_memory,fielddata.memory_size,query_cache.memory_size,request_cache.memory_size&amp;v"
</code></pre>
<p>执行该命令后输出如下：</p>
<pre><code>port segments.memory segments.index_writer_memory fielddata.memory_size query_cache.memory_size request_cache.memory_size
9301           2.1gb                      112.9mb               193.1mb                 362.2mb                    52.7mb
9301           2.7gb                        162mb               191.7mb                 372.8mb                      48mb
9300           2.4gb                        182mb                 191mb                 350.7mb                    35.7mb
9301           2.4gb                      165.6mb                 2.9mb                 264.6mb                    72.9mb
9300           3.2gb                      329.7mb               192.7mb                 402.4mb                    40.6mb
9300           2.6gb                      116.3mb                   4mb                 334.5mb                    36.8mb
9300           2.3gb                      164.8mb                 2.7mb                 210.2mb                    64.4mb
9300             3gb                      152.7mb                 3.4mb                 369.9mb                    37.3mb
9301             3gb                      153.7mb                 4.3mb                   364mb                    44.6mb
9300           2.3gb                        151mb                 3.3mb                 300.4mb                    40.1mb
9301           2.1gb                      113.6mb               190.9mb                 379.7mb                    30.6mb
9300           2.3gb                      176.9mb                 192mb                 329.2mb                    40.5mb
9301           2.8gb                      136.9mb                 3.1mb                   341mb                    27.2mb
9301           3.1gb                      137.5mb                 193mb                 370.6mb                    42.1mb
9301           4.1gb                      165.4mb                 4.2mb                 356.1mb                    52.8mb
9300           3.2gb                      140.4mb               194.8mb                   566mb                      28mb
9301           3.2gb                      153.2mb                 4.1mb                 363.9mb                    55.8mb
9300           2.4gb                      147.8mb               191.3mb                   371mb                    45.3mb
9300           2.5gb                        150mb                 3.9mb                 414.2mb                      44mb
9301           2.8gb                      140.3mb               194.6mb                 552.7mb                    48.4mb
</code></pre>
<h3 id="2">2. 案例分析</h3>
<p>下面提供我们遇到的一些关于 GC 问题导致集群响应缓慢的案例。大部分都是通过导出堆，加载到 MAT 中进行分析定位的。希望遇到相似问题的同学不用再导出堆重复分析。</p>
<h4 id="21a">2.1 案例 A</h4>
<p><strong>分段过多导致 GC</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，也没有大量的入库和查询操作。通过查看节点 GC 状态，发现节点在持续进行 FullGC。</p></li>
<li><p><strong>分析：</strong>通过 REST 接口查看 Elasticsearch 进程内存使用状况，发现 <code>segments.memory</code> 占用了很大的空间。</p></li>
<li><p><strong>解决方案：</strong>对索引进行 forcemerge 操作，将 segment 合并成一个段。随着 merge 的进行，进程堆内内存逐步降下来。</p></li>
<li><p><strong>总结：</strong>对于不再写入和更新的索引，尽量通过 forcemerge api 将其 merge 为一个单一的段。 如果在把段 merge 完后，<code>segments.memory</code> 仍然占用很大的空间，则需要考虑扩容来解决。</p></li>
</ul>
<h4 id="22b">2.2 案例 B</h4>
<p><strong>fieldata 导致 gc[1]</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，也没有大量的入库和查询操作。通过查看节点 gc 状态，发现节点在持续进行 FullGC。</p></li>
<li><p><strong>分析：</strong>查看 Elasticsearch 进程内存使用状况，发现 <code>fielddata.memory_size</code> 占用了很大的空间。业务中对 keyword 类型字段进行排序或者聚合，如果 shard 包含多个段， Elasticsearch 需要构建 global_ordinals 数据结构，会占用比较大的内存。对于 merge 成一个段的shard，则不需要构建。</p></li>
<li><p><strong>解决方案：</strong>对索引进行 forcemerge 操作，将 segment 合并成一个段。随着 merge 的进行，进程堆内内存逐步降下来。</p></li>
<li><p><strong>总结：</strong>对于不再写入和更新的索引，尽量通过 forcemerge api 将其 merge 为一个段。通过【案例A】和【案例 B】我们可以明确，段要及时合并，可以减少节点内存压力，提高节点稳定性。同时在搜索过程中，可以减少磁盘随机 IO。</p></li>
</ul>
<p><strong>fieldata 导致 gc[2]</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，也没有大量的入库和查询操作。通过查看节点 GC 状态，发现节点在持续进行 FullGC。</p></li>
<li><p><strong>分析：</strong>查看 Elasticsearch 进程内存使用状况，发现 <code>fielddata.memory_size</code> 占用了很大的空间。同时，数据不写入和更新的索引，segment 都已经做过 merge。这种情况，一般是 <code>indices.fielddata.cache.size</code> 参数没有做限制导致的。</p></li>
<li><p><strong>解决方案：</strong>将 <code>indices.fielddata.cache.size</code> 设置降低，重启集群，节点堆内内存恢复正常。</p></li>
<li><p><strong>总结：</strong>由于 Fielddata cache 构建是一个比较重的操作，如果在  <code>indices.fielddata.cache.size</code> 设置的范围内，Elasticsearch 并不会主动释放，所以需要把该值设置的保守一些。如果业务确实需要比较大的值，则需要增加节点内存，或者添加节点进行水平扩容来解决。</p></li>
</ul>
<h4 id="23c">2.3 案例 C</h4>
<p><strong>bulk queue 过大 gc</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，此时系统 cpu 利用率处于 80% 以上，通过查看节点 GC 状态，发现节点在持续进行 FullGC 。</p></li>
<li><p><strong>分析：</strong>查看 Elasticsearch 进程内存使用状况，并没有发现占用内存不正常的情况。登陆服务器，通过如下命令，查看 <code>thread_pool</code> 使用情况：</p></li>
</ul>
<pre><code>curl -sXGET "http://localhost:9200/_cat/thread_pool?v"
</code></pre>
<p>发现全部入库线程都处于 Active 状态，且出现了大量的拒绝操作。之后导出堆进行分析，发现堆内有大量的 IndexRequest，如下图所示：</p>
<pre><code>![](media/15569515713986/15569531048045.jpg)
</code></pre>
<p>由此可以确定 FullGC 的原因是入库资源不足且 bulk queue 过大导致的。</p>
<ul>
<li><p><strong>解决方案：</strong>降低 bulk queue 大小，从500降低到官方的默认值 50。</p></li>
<li><p><strong>总结：</strong>bulk queue 不建议设置的特别大，如果设置的特别大，且每次bulk的数据条数很多，一旦出现资源不够导致数据进入 bulk queue，说明系统资源已经利用很充分，大量数据滞留在队列内，很可能导致节点频繁 FullGC，引起节点响应慢，甚至离线。</p></li>
</ul>
<h4 id="24d">2.4 案例 D</h4>
<p><strong>嵌套聚合导致 GC</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，通过查看节点 GC 状态，发现节点在持续进行 FullGC。</p></li>
<li><p><strong>分析：</strong>查看 Elasticsearch 进程内存使用状况，发现各个内存项都比较正常。导出堆分析，发现内存中有大量的 bucket 对象。初步推测是聚合导致了 GC 问题。通过搜索 Elasticsearch 日志，发现每次执行完一个查询语句后，就开始有大量的 GC 日志打印出来。发现那是在一个 10 亿+ 的索引上执行了4层聚合。</p></li>
<li><p><strong>解决方案：</strong>业务方去掉了这个功能，以其他的方式实现。</p></li>
<li><p><strong>总结：</strong>对于在大数据集上进行的嵌套聚合，需要很大的堆内内存来完成。如果业务场景确实无法以其他方式实现，也只能增加更多的硬件，分配更多的堆内内存给 Elasticsearch 进程。</p></li>
</ul>
<h4 id="25f">2.5 案例 F</h4>
<p><strong>更新导致 GC</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，也没有大量的入库和查询操作。通过查看节点 GC 状态，发现节点在持续进行FullGC。</p></li>
<li><p><strong>分析：</strong>查看 Elasticsearch 进程内存使用状况，并没有发现内存占用异常的情况。不写入的索引的 segment 也进行了 merge。此种情况，除了分析堆，没有更好的办法了。经过分析，发现有大量的 PerThreadIDAndVersionLookup 占用大量的内存，如下图所示：
<img src="media/15569515713986/15569516098070.jpg" alt="" />
而且该对象都跟几个正在写入和更新的索引有关。通过查看 Lucene 代码，发现如果在索引过程中是采用自定义 id 而非自动生成 id，每个入库线程对每个 segment 会持有一个 PerThreadIDAndVersionLookup 对象。查看这几个索引的 segment 数量，都在2万+以上。</p></li>
<li><p><strong>解决方案：</strong>由于索引持续有写入和更新，定时对这类型的索引进行适当的 merge，不强制merge成一个段，以免对业务产生比较大的影响。之后观察几天，节点 GC 情况正常。</p></li>
<li><p><strong>总结：</strong>对于索引数据持续发生变化，且 ID 是业务自定义的索引，要定期将其段的数量 merge 到一个比较小数量，以免发生 FullGC 的问题。</p></li>
</ul>
<h4 id="26g">2.6 案例 G</h4>
<p><strong>堆外内存不足导致 GC</strong></p>
<ul>
<li><p><strong>现象：</strong>节点响应缓慢，也没有大量的入库和查询操作。通过查看节点 GC 状态，发现节点在持续进行 FullGC，但是与前面案例不同的是，在发生 FullGC 时，Java 进程的 old 区使用不足 50%。</p></li>
<li><p><strong>分析：</strong>由于old区还有很多剩余空间，则应该不是堆内内存问题。查看 Elasticsearch 进程内存使用状况，果然一切正常。随即怀疑是堆外内存导致。查看进程的启动参数，发现有 <code>-XX:MaxDirectMemorySize=2048m</code>，由于 Elasticsearch 底层采用 netty 作为通信框架， netty 为了提高效率，很多地方采用了堆外内存，很可能是该参数配置过小导致频繁的 GC。</p></li>
<li><p><strong>解决方案：</strong>去掉 <code>-XX:MaxDirectMemorySize=2048m</code> 启动参数，重启进程，GC 恢复正常。</p></li>
<li><p><strong>总结：</strong>不要在线上系统随意添加优化参数，需要经过充分的测试验证。</p></li>
</ul>
<h3 id="">总结</h3>
<p>本文介绍了 Elasticsearch 内部的内存分布，以及我们在使用过程中因为 GC 问题引起的节点相应缓慢问题的案例分析方法和解决方案。</p>
<p>节点 GC 情况对节点稳定性和请求延迟密切相关，保证 GC 时长在一个合理的时间范围至关重要。</p>
<p>下一节我们介绍下一些其他比较通用的问题。</p></div></article>