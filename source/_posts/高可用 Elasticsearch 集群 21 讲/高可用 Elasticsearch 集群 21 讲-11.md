---
title: 高可用 Elasticsearch 集群 21 讲-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>为了能够提前发现问题，以及在出现故障后便于定位问题，我们需要对集群进行监控，对于一个完整的Elasticsearch 集群监控系统来说，需要的的指标非常多，这里我们列出一些比较重要的。</p>
<h3 id="1">1 集群级监控指标</h3>
<h4 id="11">1.1 集群健康</h4>
<p>集群健康是最基础的指标，他是快速衡量集群是否正常的依据，当集群 Yellow 的时候，代表有部分副分片尚未分配，导致未分配的原因很多。</p>
<p>例如节点离线等，从分布式系统的角度来说意味着数据缺少副本，系统会尝试将他自动补齐，因此可以不把 Yellow 作为一种报警状态。集群处于 Yellow 状态时也可以正常执行入库操作。</p>
<p>另外当创建新索引时，集群也可能会出现短暂的从 Red 到 Yellow 再到 Green 的状态，因为创建索引时，可能需要分配多个分片，在全部的分片分配完毕之前，该索引在集群状态中属于分片不完整的状态，因此短暂的 Red 也属于正常现象。</p>
<p>集群健康可以通过 <code>_cluster/health</code> 接口来查看。</p>
<h4 id="12qps">1.2 读写 QPS</h4>
<p>Elasticsearch 没有提供实时计算出好读写 QPS 值，实时计算这些值会对集群造成比较大的压力。</p>
<p>他提供了一个接口返回每个节点当前已处理的请求数量，你需要基于此进行计算：发送两次请求，中间间隔一段时间，用两次返回的请求数量做差值，得到间隔时间内的增量，再把每个节点的增量累加起来，除以两次请求的间隔时间，得到整个集群的 QPS。两次请求的间隔时间不要太短，建议在 10s 及以上。</p>
<p>节点的请求统计信息通过 <code>_nodes/stats</code> 接口获取，对于计算读写 QPS 来说，我们所需信息如下：</p>
<pre><code>"indexing" : {
  "index_total" : 141310,
}
"search" : {
  "query_total" : 5772,
},
</code></pre>
<p><strong>index_total：</strong>节点收到的索引请求总量;</p>
<p><strong>query_total：</strong>节点收到的查询请求总量;</p>
<p>通过这种方式计算出的 QPS 并非业务直接发起的读写请求 QPS，而是分片级别的。例如，只有一个索引，索引只有1个分片，那么我们计算出的 QPS 等于业务发起的请求 QPS，如果索引有5个分片，那么计算出的 QPS 等于业务发起的 QPS*5。因此，无论是查询还是索引请求：</p>
<p>计算出的 <code>QPS = 业务发起的 QPS * 分片数量</code></p>
<p>在 Kibana 的 Monitor 中看到的 Search Rate (/s) 与 Indexing Rate (/s) 的涵义与我们上面的描述相同。</p>
<h4 id="13">1.3 读写延迟</h4>
<p>与读写 QPS 类似，读取延迟也可以通过 <code>_nodes/stats</code> 接口返回的信息进行计算，对于读写延迟来说，所需信息如下：</p>
<pre><code>"indexing" : {
  "index_time_in_millis" : 54404,
}
"search" : {
  "query_time_in_millis" : 5347,
  "fetch_time_in_millis" : 1465,
},
</code></pre>
<p>查询由两个阶段完成，因此 query 耗时与 fetch 单独给出，对于整个搜索请求耗时来说需要把它加起来。由于这种方式计算出来的的采样周期内的平均值，因此只能给监控提供大致的参考，如果需要诊断慢请求需要参考慢查询或慢索引日志。</p>
<h4 id="14">1.4 分片信息</h4>
<p>我们还需要关注有多少分片处于异常在状态，这些信息都在 <code>_cluster/health</code> 的返回结果中，包括：</p>
<ul>
<li><p><strong><code>initializing_shards</code></strong></p>
<p>正在执行初始化的分片数量，当一个分片开始从 UNASSIGNED 状态变为 STARTED 时，从分片分配操作一开始，该分片被标记为 INITIALIZING 状态。例如创建新索引、恢复现有分片时，都会产生这个状态。</p></li>
<li><p><strong><code>unassigned_shards</code></strong></p>
<p>待分配的分片数量，包括主分片和副分片。</p></li>
<li><p><strong><code>delayed_unassigned_shards</code></strong></p>
<p>由于一些原因延迟分配的分片数量。例如配置了 <code>index.unassigned.node_left.delayed_timeout</code>，节点离线时会产生延迟分配的分片。</p></li>
</ul>
<h3 id="2">2 节点级别指标</h3>
<h4 id="21jvm">2.1 JVM 指标</h4>
<p>JVM 指标也在  <code>_nodes/stats</code> API 的返回结果中，每个节点的信息单独给出。需要重点关注的指标如下：</p>
<p><strong>1. 堆内存使用率</strong></p>
<p>字段 <code>heap_used_percent</code> 代表堆内存使用率百分比，如果堆内存长期居高则意味着集群可能需要扩容。</p>
<p>JVM 内存使用率过高，且无法 GC 掉时，集群处于比较危险的状态，当一个比较大的聚合请求过来，或者短期内读写压力增大时可能会导致节点 OOM。</p>
<p>如果 master 节点的堆内存使用率过高更需要警惕，当重启集群时，master 节点执行 gateway 及 recovery 都可能需要比较多的内存，这和分片数量有关，因此可能在重启集群的时候内存不足，有时需要关闭一些索引才能让集群启动成功。</p>
<p><strong>2. GC 次数和时长</strong></p>
<p>年轻代和老年代的回收次数与持续时间最好都被监控，如果年轻代 GC 频繁，可能意味着为年轻代分配的空间过小，如果老年代 GC 频繁，可能意味着需要进行扩容。</p>
<pre><code>"gc" : {
  "collectors" : {
    "young" : {
      "collection_count" : 44,
      "collection_time_in_millis" : 2678
    },
    "old" : {
      "collection_count" : 2,
      "collection_time_in_millis" : 493
    }
  }
},
</code></pre>
<p>正常情况下，通过 REST API 获取这些指标不是问题，但是当节点长时间 GC 时，接口无法返回结果，导致无法发现问题，因此建议使用 jstat 等外部工具对 JVM 进行监控。</p>
<h4 id="22">2.2 线程池</h4>
<p>关注线程池信息可以让我们了解到节点负载状态，有多少个线程正在干活，Elasticsearch 有很多线程池，一般我们可以重点关注执行搜索和索引的线程信息，可以通过 <code>_nodes/stats</code> API 或 <code>_cat/thread_pool</code> API 来获取线程池信息，建议使用 <code>_nodes/stats</code> API，你可以在一个请求的结果中得到很多监控指标，我们最好少发一些 stats 之类的请求到 Elasticsearch 集群。</p>
<pre><code>"bulk" : {
  "active" : 0,
  "rejected" : 0,
},
"search" : {
  "active" : 0,
  "rejected" : 0,
},
</code></pre>
<p><strong>active：</strong> 正在运行任务的线程个数;</p>
<p><strong>rejected：</strong> 由于线程池队列已满，拒绝的请求数量;</p>
<blockquote>
  <p>客户端对于被拒绝的请求应该执行延迟重试，更多信息可以参考《Elasticsearch 源码解析与优化实战》</p>
</blockquote>
<h3 id="3">3 操作系统及硬件</h3>
<p>只监控 Elasticsearch 集群本身的指标是不够的，我们必须结合操作系统和硬件信息一起监控。这里只给出建议重点关注的指标，如何获取这些指标的方法很多，本文不再过多叙述。</p>
<h4 id="31">3.1 磁盘利用率</h4>
<p>这里的磁盘利用率不是指使用了多少空间，而是指 iostat 返回的 <code>%util</code>。服务器一般会挂载多个磁盘，你不比经常关心每个磁盘的 <code>%util</code> 有多少，但是需要注意下磁盘 util 长时间处于 100%， 尤其是只有个别磁盘的 util 长时间处于100%，这可能是分片不均或热点数据过于集中导致。</p>
<h4 id="32">3.2 坏盘</h4>
<p>目前 Elasticsearch 对磁盘的管理有些不足，因此我们需要外部手段检查、监控坏盘的产生并及时更换。坏盘对集群的稳定性有较大影响</p>
<h4 id="33">3.3 内存利用率</h4>
<p>一般不比对操作系统内存进行监控，Elasticsearch 会占用大量的 page cache，这些都存储在操作系统的物理内存中。因此发现操作系统的 free 内存很少不必紧张，特别注意不要手工回收 cache，这会对集群性能产生较严重影响。</p>
<h3 id="">总结</h3>
<p>本章从 Elasticsearch 集群角度和操作系统角度介绍了需要重点关注的监控项，在设计监控系统的时候，需要注意发起获取指标的请求频率不要太高，有些请求需要 master 节点到各个数据节点去收集，频繁的 <code>_cat/indices</code> 之类请求会对集群造成比较大的压力。</p>
<p>下一节课程我们介绍一下<strong>集群应该何时扩容，以及扩容注意事项</strong>。</p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>