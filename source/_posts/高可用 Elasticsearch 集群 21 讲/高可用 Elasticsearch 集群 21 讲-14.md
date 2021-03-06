---
title: 高可用 Elasticsearch 集群 21 讲-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Elasticsearch 各个模块提供了很多配置参数，用来满足不同的业务场景。本篇我们结合我们的经验对参数进行归类介绍，方便读者进行配置。主要包括索引性能参数、查询参数、稳定性参数、数据安全参数、内存参数、allocation 参数、集群恢复参数。</p>
<h3 id="1">1. 索引性能参数</h3>
<p><strong>1. <code>index.translog.durability</code></strong></p>
<p>为了保证写入的可靠性，该值的默认参数值为 request，即，每一次 bulk、index、delete 请求都会执行 translog 的刷盘，会极大的影响整体入库性能。</p>
<p>如果在对入库性能要求较高的场景，系统可以接受一定几率的数据丢失，可以将该参数设置成 “async” 方式，并适当增加 translog 的刷盘周期。</p>
<p><strong>2. <code>index.refresh_interval</code></strong></p>
<p>数据索引到 Elasticsearch 集群中后，要经过 refresh 这个刷新过程才能被检索到。为了提供近实时搜索，默认情况下，该参数的值为 1 秒，没次 refresh 都会产生一个新的 Lucene segment，会导致后期索引过程中频繁的 merge。</p>
<p>对于入库性能要求较高，实时性要求不太高的业务场景，可以结合<code>indices.memory.index_buffer_size</code>参数的大小，适当增加该值。</p>
<p><strong>3. <code>index.merge.policy.max_merged_segment</code></strong></p>
<p>索引过程中，随着新数据不断加入，Lucene 会根据 merge 策略不断的对已产生的段进行 merge 操作。<code>index.merge.policy.max_merged_segment</code> 参数控制此 merge 过程中产生的最大的段的大小，默认值为 5gb。为了提高入库性能，可以适当降低配置的大小。</p>
<p><strong>4. <code>threadpool.write.queue_size</code></strong></p>
<p>index、bulk、delete、updaet 等操作的队列大小，默认值为 200。队列满时，说明已经没有足够的 CPU 资源做写入操作。加大配置并不能有效提高索引性能，但是会增加节点 OOM 的几率。</p>
<p>有一点要注意的是，Elasticsearch 首先在主分片上进行写入操作，然后同步到副本。为了保持主副本一致，在主分片写入后，副本并不会受该设置的限制，所以一个节点如果堆积了大量的副本写入操作，会增加节点 OOM 的几率。</p>
<h3 id="2">2. 查询参数</h3>
<p><strong>1. <code>threadpool.search.queue_size</code></strong></p>
<p>查询队列大小，默认值为1000。不建议将该值设置的过大，如果 search queue 持续有数据，需要通过其他策略提高集群的并发度，比如增加节点、同样的数据减少分片数等。</p>
<p><strong>2. <code>search.default_search_timeout</code></strong></p>
<p>控制全局查询超时时间，默认没有全局超时。可用通过 Cluster Update Settings 动态修改。在生产集群，建议设置该值防止耗时很长的查询语句长期占用集群资源，讲集群拖垮。</p>
<p><strong>3. <code>cluster.routing.use_adaptive_replica_selection</code></strong></p>
<p>在查询过程中，Elasticsearch 默认采用 round robin 方式查询同一个分片的多个副本，该参数可以考虑多种因素，将查发送到最合适的节点, 比如对于包含查询分片的多个节点，优先发送到查询队列较小的节点。生产环境中，建议打开该配置。</p>
<pre><code>PUT /_cluster/settings
{
    "transient": {
        "cluster.routing.use_adaptive_replica_selection": true
    }
} 
</code></pre>
<p><strong>4. <code>action.search.max_concurrent_shard_requests</code></strong></p>
<p>限制一个查询同时查询的分片数。防止一个查询占用整个集群的查询资源。该值需要根据业务场景进行合理设置。</p>
<p><strong>5. <code>search.low_level_cancellation</code></strong></p>
<p>Elasticsearch 支持结束正在执行的查询任务，但是在默认情况下，只在 segments 之间有是否结束查询的检查点。默认为 false。将该参数设置成 true 后，会在更多的位置进行是否结束的检查，这样会更快的结束查询。</p>
<p>如果集群中没有很多大的 segment，不建议修改该值的默认设置，设置后过多的检查任务是否停止会对查询性能有很大的影响。</p>
<p><strong>6. <code>execution_hint</code></strong></p>
<p>Elasticsearch 有两种方式执行 terms 聚合，默认会采用 <code>global_ordinals</code> 动态分配 bucket。大部分情况下，采用 <code>global_ordinals</code> 的方式是最快的。</p>
<p>但是对于查询命中结果数量比较小的时候，采用 map 方式会极大减少内存的占用。引用官方文档的例子，使用方式如下：</p>
<pre><code>GET /_search
{
    "aggs" : {
        "tags" : {
             "terms" : {
                 "field" : "tags",
                 "execution_hint": "map" 
             }
         }
    }
}
</code></pre>
<h3 id="3">3. 稳定性参数</h3>
<p><strong>1. <code>discovery.zen.minimum_master_nodes</code></strong></p>
<p>假设一个集群中的节点数为n，则至少要将该值设置为<code>n/2 + 1</code>，防止发生脑裂的现象。</p>
<p><strong>2. <code>index.max_result_window</code></strong></p>
<p>在查询过程中控制 from + size 的大小。查询过程消耗 CPU 和堆内内存。一个很大大值，比如 1000 万，很容易导致节点 OOM，默认值为 10000。</p>
<p><strong>3. <code>action.search.shard_count.limit</code></strong></p>
<p>用于限制一次操作过多的分片，防止过多的占用内存和 CPU 资源。建议合理设计分片和索引的大小。尽量查询少量的大的分片，有利于提高集群的并发吞吐量。</p>
<h3 id="4">4. 数据安全参数</h3>
<p><strong>1. <code>action.destructive_requires_name</code></strong></p>
<p>强烈建议在线上系统将该参数设置成 true，禁止对索引进行通配符和 _all 进行删除，目前 Elasticsearch 还不支持回收站功能，程序bug或者误操作很可能带来灾难性的结果——<strong>数据被清空</strong>！</p>
<p><strong>2. <code>index.translog.durability</code></strong></p>
<p>如果对数据的安全性要求高，则该值应该配置成 “request”，保证所有操作及时写入 translog。</p>
<h3 id="5">5. 内存参数</h3>
<p><strong>1. <code>indices.fielddata.cache.size</code></strong></p>
<p>限制 Field data 最大占用的内存，可以按百分比和绝对值进行设置，默认是不限制的, 也就是整个堆内存。 如果业务场景中持续有数据加载到 Fielddata Cache，很容易引起 OOM。所以我建议初始时将该值设置的比较保守一些，当遇到查询性能瓶颈时再结合软硬件资源调整。</p>
<p><strong>2. <code>indices.memory.index_buffer_size</code></strong></p>
<p>在索引过程中，新添加的文档会先写入索引缓冲区。默认值为堆内存的 10%。更大的 index buffer 通常会有更高的索引效率。</p>
<p>但是单个 shard的index buffer 超过 512M 以后，索引性能几乎就没有提升了。所以，如果为了提高索引性能，可以根据节点上执行索引操作的分片数来合理设置整个参数。</p>
<p><strong>3. <code>indices.breaker.total.limit</code></strong></p>
<p>父级断路器内存限制，默认值为堆内存的 70%。 对于内存比较小的集群，为了集群的稳定性，建议该值设置到 50% 以下。</p>
<p><strong>4. <code>indices.breaker.fielddata.limit</code></strong></p>
<p>防止过多的 Fielddata 加载导致节点 OOM，默认值为堆内存的 60%。 在生产集群，建议将该值设置成一个比较保守的值，比如 20%，在性能确实由于该值配置较小出现瓶颈时，合理考虑集群内存资源后，谨慎调大。</p>
<h3 id="6allocation">6. allocation 参数</h3>
<p><strong>1. <code>cluster.routing.allocation.disk.watermark.low</code></strong></p>
<p>该参数表示当磁盘使用空间达到该值后，新的分片不会继续分配到该节点，默认值是磁盘容量的 85%。</p>
<p><strong>2. <code>cluster.routing.allocation.disk.watermark.high</code></strong></p>
<p>参数表示当磁盘使用空间达到该值后，集群会尝试将该节点上的分片移动到其他节点，默认值是磁盘容量的90%。对于索引量比较大的场景，该值不宜设置的过高。可能会导致写入速度大于移动速度，使磁盘写满，引发入库失败、集群状态异常的问题。</p>
<p><code>index.routing.allocation.include.{attribute}；</code></p>
<p><code>index.routing.allocation.require.{attribute};</code></p>
<p><code>index.routing.allocation.exclude.{attribute} ;</code></p>
<ul>
<li>include 表示可以分配到具有指定 attribute 的节点；</li>
<li>require 表示必须分配到具有指定 attribute 的节点；</li>
<li>exclude 表示不允许分配到具有指定 attribute 的节点。</li>
</ul>
<p>Elasticsearch 内置了多个 attribute，无需自己定义，包括 <code>_name</code>,<code>_host_ip</code>,<code>_publish_ip</code>, <code>_ip</code>, <code>_host</code>。attribute 可以自己定义到 Elasticsearch 的配置文件。</p>
<p><strong>3. <code>total shards per node</code></strong></p>
<p>控制单个索引在一个节点上的最大分片数，默认值是不限制。我们的经验是，创建索引时，尽量将该值设置的小一些，以使索引的 shard 比较平均的分布到集群内的所有节点。</p>
<h3 id="7">7. 集群恢复参数</h3>
<p><strong>1. <code>indices.recovery.max_bytes_per_sec</code></strong></p>
<p>该参数控制恢复速度，默认值是 40MB。如果是集群重启阶段，可以将该值设置大一些。但是如果由于某些节点掉线，过大大值会占用大量的带宽北恢复占用，会影响集群的查询、索引及稳定性。</p>
<p><strong>2. <code>cluster.routing.allocation.enable</code></strong></p>
<p>控制是否可以对分片进行平衡，以及对何种类型的分片进行平衡。可取的值包括：all、primaries、replicas、none，默认值是 all。</p>
<ul>
<li>all 是可以对所有的分片进行平衡；</li>
<li>primaries 表示只能对主分片进行平衡；</li>
<li>replicas 表示只能对副本进行平衡；</li>
<li>none 表示对任何分片都不能平衡，也就是禁用了平衡功能。</li>
</ul>
<p>有一个小技巧是，在重启集群之前，可以将该参数设置成 <strong>primaries</strong>，由于主分片是从本地磁盘恢复数据，速度比较快，可以使集群迅速恢复到 Yellow 状态，之后设置成 <strong>all</strong>，开始恢复副本数据。</p>
<p><strong>3. <code>cluster.routing.allocation.node_concurrent_recoveries</code></strong></p>
<p>控制单个节点可以同时恢复的副本的数量，默认值为 2。副本恢复主要瓶颈在于网络，对于网络带宽不大的环境，不需要修改该值。</p>
<p><strong>4. <code>cluster.routing.allocation.node_initial_primaries_recoveries</code></strong></p>
<p>控制一个节点可以同时恢复的主分片个数，默认值为 4。由于主分片是从本地存储恢复，为了提高恢复速度，完全可以加大设置。</p>
<p><strong>5. <code>cluster.routing.allocation.cluster_concurrent_rebalance</code></strong></p>
<p>该参数控制在平衡过程中，同时移动的分片数，加大可以提高平衡的速度。一般在集群扩容节点、下线节点后，可以加大，使集群尽快的进行平衡。</p>
<h3 id="">总结</h3>
<p>本课主要把我们在实践中常用的参数进行了分类，并对结合我们的经验对参数的设置及影响做了说明。希望可以给读者提供一些设置参考。</p>
<p>这部分内容主要介绍在业务正式上线前如何压测，上线后对于分片和节点层面的管理工作，在集群运行过程中合适扩容等，第一部分和第二部分组合起来就是一个集群的生命周期。在此期间，“安全”是无法回避的话题，下一部分我们介绍下如何使用 X-Pack 进行安全防护。</p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>