---
title: 高可用 Elasticsearch 集群 21 讲-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>随着时间的推移、业务的发展，你存入 Elasticsearch 的数据会越来越多；随着用户量的增加，系统响应时间增加。</p>
<p>总有一天，初始安装的集群规模无法满足日益增长的需求，这时需要考虑对现有的 Elasticsearch 集群进行扩容。</p>
<h3 id="1">1 扩容方式</h3>
<p>为了提高系统的处理能力，包括增加系统的 cpu、内存、存储等资源，通常有两种扩容方式：垂直扩容和水平扩容。</p>
<h4 id="11">1.1 垂直扩容</h4>
<p>增加单机处理能力，如购买更好的 cpu，增加 cpu 核心数；将机械硬盘换成 SSD，提高 IO 能力；购买更大容量的内存条，提高内存容量满足计算需求；升级万兆网卡，提高网络带宽等。</p>
<h4 id="12">1.2 水平扩容</h4>
<p>通过增加服务器的数量，将服务器形成分布式的集群，以提高整个系统的计算、存储、IO 能力，满足业务的需求。水平扩容通常需要软件在架构层面上的支持。</p>
<h3 id="2">2 定位硬件瓶颈</h3>
<p>我们现在集群的处理能力能够满足业务需求吗？何时需要扩容？你肯定不希望你的线上业务由于硬件资源不够挂掉。为了解答这些问题，我们首先要定位出当前的硬件资源是否存在瓶颈。下面列出我们常用的定位 Elasticsearch 存在硬件资源瓶颈的一些办法。</p>
<h4 id="21cpu">2.1 <strong>cpu</strong></h4>
<p>Elasticsearch 索引和查询过程都是 cpu 密集型的操作，如果 cpu 存在瓶颈，系统性能会受到很大影响。那采用什么指标来定位 cpu 瓶颈呢？我们一般通过如下几个方法来定位：</p>
<ul>
<li><p><strong>通过操作系统的监控命令</strong></p>
<p><code>sar</code> 命令</p></li>
</ul>
<pre><code>bash-4.2$ sar -u
</code></pre>
<p>执行该命令后，输出如下：</p>
<pre><code>    07:44:02 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
    07:46:01 PM     all     11.39      0.00      1.64      0.21      0.00     86.76
    07:48:01 PM     all     10.40      0.00      1.50      0.07      0.00     88.03
    07:50:01 PM     all      9.37      0.00      1.34      0.07      0.00     89.23
    07:52:01 PM     all     12.01      0.00      1.55      0.05      0.00     86.40
    07:54:01 PM     all      9.58      0.00      1.41      0.02      0.00     88.98
    07:56:01 PM     all     10.16      0.00      1.49      0.15      0.00     88.20
    07:58:01 PM     all     10.04      0.00      1.44      0.02      0.00     88.50
    08:00:01 PM     all     10.39      0.00      1.51      0.03      0.00     88.07
    08:02:01 PM     all     10.90      0.00      1.55      0.05      0.00     87.50
    08:04:01 PM     all      9.29      0.00      1.43      0.02      0.00     89.26
    08:06:01 PM     all      9.91      0.00      1.40      0.05      0.00     88.64
    08:08:01 PM     all     10.56      0.00      1.53      0.08      0.00     87.84
</code></pre>
<p>如果系统 cpu 使用率持续超过 60%，而且后期压力会随着业务的发展持续增加，就需要考虑扩容来减轻 cpu 的压力。</p>
<ul>
<li><strong>通过查看 Elasticsearch 的 Threadpool</strong></li>
</ul>
<pre><code>    curl -sXGET 'http://localhost:9200/_cat/thread_pool?v' | grep -E "node_name|search|bulk"
</code></pre>
<p>如果 active 一列在一段时间内持续达到了线程数的最大值，或者 rejected 不为 0，则意味着可能 cpu 资源不足，导致了请求拒绝。也可能瞬时写入并发过大，mapping 设置不合理等。</p>
<h4 id="22">2.2 <strong>内存</strong></h4>
<p>Elasticsearch 高效稳定的运行，十分依赖内存，包括 Java 进程占用的内存和操作系统 Cache Lucene 索引文件占用的内存。</p>
<ul>
<li><p>Java 堆内内存不足</p>
<p><strong>对于 Java 进程来说，我们一般从如下几个方面判断是否运行正常：</strong></p></li>
</ul>
<ol>
<li><p>minor gc 耗时超过 50ms</p></li>
<li><p>minor gc 执行很频繁，10s 以内会执行一次</p></li>
<li><p>minor gc 后 eden 还占用很大比例空间</p></li>
<li><p>minor gc 后，survior 容纳不下 eden 和另一个 survior 的存活对象，发生了过早提升</p></li>
<li><p>fullgc 平均执行时间超过1s</p></li>
<li><p>fullgc 10分钟以内会执行一次</p>
<p>如果调优 GC 参数后，gc 仍然存在问题，则需要适当增加 Java 进程的内存，但是单个节点的内存要小于 32G，继续观察，直到运行平稳。</p></li>
</ol>
<ul>
<li><p>操作系统 Cache 抖动</p>
<p>Elasticsearch 底层基于 Lucene，Lucene 的高效运行需要依赖操作系统 Cache，操作系统频繁发生换页，Cache 抖动严重，对运行速度会产生很大的影响，产生一系列的问题，导致内存使用效率降低，引发磁盘 IO 升高，cpu 的 IO Wait 增加，从而使系统的整体吞吐量和响应时间收到极大的影响。换页行为可以通过操作系统的 sar 命令来定位。</p>
<pre><code>sar -B 
</code></pre>
<p>执行该命令后，输入如下：</p>
<pre><code>07:44:01 PM  pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
07:46:01 PM  43267.29    389.22 293717.84      0.19  23414.69      0.00      0.00      0.00      0.00
07:48:01 PM  49302.07    982.05 305202.18      0.08  32241.47   3183.44     41.29   3223.85     99.97
07:50:01 PM  49409.41    524.31 297695.93      0.05  40182.40   8982.75    155.12   9126.79     99.88
07:52:01 PM  54349.32    432.02 309908.67      0.02  39272.66   9135.48    567.22   8363.67     86.20
07:54:01 PM  61406.73    348.05 326887.23      0.15  45224.42  20481.31   3296.59  15797.72     66.44
07:56:01 PM  58327.98    130.05 294911.57      0.12  41707.75  15614.09   1915.41  14558.13     83.05
07:58:01 PM  53790.35    442.78 293988.20      0.09  38539.34  13727.40   1719.69  13166.00     85.23
08:00:01 PM  59534.64    279.43 304241.40      0.03  41120.01  19764.74   1896.83  14958.18     69.05
08:02:01 PM  57026.47    204.59 292543.72      0.06  40701.89  18893.40   2479.08  14743.70     68.98
08:04:01 PM  39415.95    447.89 224081.73      0.07  36275.20  10158.59   1542.77  10016.37     85.60
08:06:01 PM  25112.09    668.31 204173.12      0.38  20699.20   3939.11   1371.64   5310.75    100.00
08:08:01 PM  24780.95    656.56 200126.48      0.02  54840.20   1024.04    213.75   1237.79    100.00
</code></pre>
<p>如果 <code>%vmeff</code> 一列持续低于 30，同时伴有比较高的 <code>pgpgin/s</code>、<code>pgpgout/s</code>、<code>pgscand/s</code>，说明系统内存很紧张了，如果通过优化配置无法有效降低该列的值，需要扩容来缓解系统内存不足的情况。</p></li>
</ul>
<h4 id="23">2.3 磁盘</h4>
<p>磁盘瓶颈一般分为两种:磁盘空间不足和磁盘读写压力大。</p>
<p><strong>磁盘空间</strong>
磁盘间不足，这很容易理解，现有硬件的磁盘容量已经无法满足业务的需求。</p>
<p><strong>读写压力大</strong>
磁盘 IO 读写压力比较大，磁盘使用率长期处于较高状态，导致系统的 IO Wait 增加，此时需要增加节点，将 shard 分布到更多的硬件磁盘上，以降低磁盘的 IO 压力。</p>
<h4 id="24">2.4 网络</h4>
<p>Elasticsearch 在运行过程中，很多操作都会占用很大的网络带宽，比如大批量的索引操作、scroll 查询拉取大量的结果、分片恢复拷贝索引文件、分片平衡操作。</p>
<p>如果网络存在瓶颈，不但会影响这些操作的执行效率，而且影响节点间的内部通信的稳定性，会使集群出现不稳定的情况，频繁发生节点离线的情况。网络瓶颈定位使用 <code>iftop</code>、<code>iptraf</code>、<code>sar</code> 命令。下面以 <code>sar</code> 命令为例：</p>
<pre><code>bash-4.2$ sar -n DEV
</code></pre>
<p>输出结果如下：</p>
<pre><code>07:12:01 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
07:14:01 AM      eth0   5130.99   8146.84   2933.22   7403.37      0.00      0.00      0.54
07:14:01 AM      eth1      0.00      0.00      0.00      0.00      0.00      0.00      0.00
07:14:01 AM        lo    296.09    296.09    121.74    121.74      0.00      0.00      0.00
07:16:01 AM      eth0   4240.99   7463.91   2490.03   7436.86      0.00      0.00      0.53
07:16:01 AM      eth1      0.00      0.00      0.00      0.00      0.00      0.00      0.00
07:16:01 AM        lo    300.13    300.13    129.30    129.30      0.00      0.00      0.00
07:18:01 AM      eth0   4529.47   7955.89   2639.50   7795.74      0.00      0.00      0.53
07:18:01 AM      eth1      0.00      0.00      0.00      0.00      0.00      0.00      0.00
07:18:01 AM        lo    303.97    303.97    123.36    123.36      0.00      0.00      0.00
</code></pre>
<p>重点关注 <code>rxkB/s</code>、<code>txkB/s</code> 两列，如果这两列的值持续接近网络带宽的极限，那就必须提升集群的网络配置，比如升级万兆网卡、交换机，如果集群跨机房，申请更多的跨机房带宽。</p>
<h3 id="3">3 扩容注意事项</h3>
<p>当新的服务器准备好之后，在新的 Elasticsearch 节点加入到集群之前，集群扩容的过程中有几点需要注意。</p>
<h4 id="31">3.1 调整最小主节点数</h4>
<p>最小主节点数的配置约束为多数，由于扩容后集群节点总数增加，有可能导致原来配置的最小主节点数不足多数，因此可能需要对该参数进行调整。</p>
<p>如果不进行调整，集群可能会脑裂，对该参数的调整非常重要。现在可以通过 REST API 来调整。</p>
<pre><code>PUT /_cluster/settings
{
    "persistent" : {
        "discovery.zen.minimum_master_nodes" : $X
    }
}
</code></pre>
<p>该配置会立即更新，并且持久化到集群状态中，此处的配置会优先于配置文件中的相同配置。也就是说如果配置文件中的值不同，最终会以 REST API 的设置为准。这样，你原来的集群就无需重启。</p>
<h4 id="32">3.2 调整节点分片总数</h4>
<p><code>total_shards_per_node</code> 用来限制某个索引的分片在单个节点上最多允许分配多少个。当集群扩容后，为了让分片分布到更多的节点，利用更多的资源，该值可能需要进行调整，可以通过 REST API 来动态调整。下列参数调整单个索引的配置。</p>
<pre><code>index.routing.allocation.total_shards_per_node
</code></pre>
<p>或者通过下列参数调整整个集群的配置，对所有的索引都生效：</p>
<pre><code>cluster.routing.allocation.total_shards_per_node
</code></pre>
<p>如果你原来的集群没有配置 <code>total_shards_per_node</code>，那么在扩容之前我们强烈建议你先计算好该值设置进去，因为 Elasticsearch 的分片分配策略下会尽量保证节点上的分片数大致相同，而扩容进来的新节点上还没有任何分片，这会导致新创建的索引集中在扩容进来的新节点，热点数据过于集中，产生性能问题。</p>
<h4 id="33">3.3 集群原有的分片会自动迁移到新节点吗？</h4>
<p>答案是会的，Elasticsearch 会把分片迁移到新增的节点上，最终让节点间的分片数量大致均衡，这个过程称为 rebalance 。默认情况下，执行 rebalance 的并发数为 2，可以通过下面的参数进行调整：</p>
<pre><code>cluster.routing.allocation.cluster_concurrent_rebalance
</code></pre>
<p>Elasticsearch 中，Peer recovery 负责副分片的数据恢复，增加副分片，以及 rebalance 等所有把数据从主分片拷贝到另一个节点的过程。因此 rebalance 期间的流量限速可以通过 Peer recovery 的限速开关进行调整：</p>
<pre><code>indices.recovery.max_bytes_per_sec
</code></pre>
<p>同理，你也可以使用 <code>_cat/recovery</code> API 查看数据迁移的状态和进度。</p>
<p>数据均衡策略并不会让节点间的分片数量分布完全一致，而是允许存在一定量的差异，有时候我们可能希望集群自己少做一些 rebalance 的操作，容忍节点间的分片数差异更多一点，可以通过调整一些权重值来实现：</p>
<ul>
<li><strong><code>cluster.routing.allocation.balance.shard</code></strong></li>
</ul>
<p>基于分片数量的权重因子，提高此值使集群中所有节点之间的分片数量更接近相等，默认值 0.45f</p>
<ul>
<li><strong><code>cluster.routing.allocation.balance.index</code></strong></li>
</ul>
<p>基于某个索引所有分片的权重因子，提高此值使集群中所有节点上某个索引的分片数量更接近相等，默认值0.55f</p>
<ul>
<li><strong><code>cluster.routing.allocation.balance.threshold</code></strong></li>
</ul>
<p>内部根据权重计算之后的值如果大于 threshold，就执行 rebalance，因此提高此值可以降低执行 rebalance 操作的积极性。</p>
<h3 id="">总结</h3>
<p>本课重点分析了定位系统硬件瓶颈的方法，当从软件层面不能有效改善系统运行性能时，可以采用本课提供的方式去分析是否存在硬件瓶颈。</p>
<p>对 Elasticsearch 集群的扩容是平滑的过程，期间不会影响业务使用，但是一定要注意到本文提及的几个事项，避免线上事故。下一节课我们介绍下集群数据迁移。</p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>