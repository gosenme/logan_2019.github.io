---
title: 高可用 Elasticsearch 集群 21 讲-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>一个 shard 本质上就是一个 Lucene 索引，也是 Elasticsearch 分布式化 Lucene 的关键抽象，是 Elasticsearch 管理 Lucene 文件的最小单位。</p>
<p>所以，Elasticsearch 提供了大量的接口，可以对集群内的 shard 进行管理。</p>
<h3 id="1shardrestapi">1 常用 shard 级 REST API 操作</h3>
<h4 id="11shard">1.1 shard 移动</h4>
<p>将分片从一个节点移动到另一个节点，在使用 Elasticsearch 中，鲜有需要使用该接口去移动分片，更多的是使用 AllocationDecider 参数以及平衡参数去自动调整 shard 的位置。 </p>
<p>在一些特别的情况下，例如发现大部分热点数据集中在几个节点，可以考虑手工 move 一下。</p>
<pre><code>curl -XPOST 'localhost:9200/_cluster/reroute' -d '{
    "commands" : [ {
        "move" :
            {
              "index" : "test", "shard" : 0,
              "from_node" : "node1", "to_node" : "node2"
            }
        }
    ]
}'
</code></pre>
<h4 id="12explainapi">1.2 explain api</h4>
<p>explain api 是 Elasticsearch 5.x 以后加入的非常实用的运维接口，可以用来诊断 shard 为什么没有分配，以及 shard 为什么分配在某个节点。</p>
<pre><code>    curl -XGET "http://localhost:9200/_cluster/allocation/explain
      {
          "index": "myindex",
          "shard": 0,
          "primary": true
      }
</code></pre>
<p>如果不提供参数调用该 api，Elasticsearch 返回第一个 unassigned shard 未分配的原因。</p>
<pre><code>    GET /_cluster/allocation/explain
</code></pre>
<h4 id="13stale">1.3 分配 stale 分片</h4>
<p>在索引过程中，Elasticsearch 首先在 primary shard 上执行索引操作，之后将操作发送到 replica shards 执行，通过这种方式使 primary 和 replica 数据同步。</p>
<p>对于同一个分片的所有 replicas，Elasticsearch 在集群的全局状态里保存所有处于同步状态的分片，称为 in-sync copies。</p>
<p>如果修改操作在 primary shard 执行成功，在 replica 上执行失败，则 primary 和 replica 数据就不在同步，这时 Elasticsearch 会将修改操作失败的 replica 标记为 stale，并更新到集群状态里。</p>
<p>当由于某种原因，对于某个 shard 集群中可用数据只剩 stale 分片时，集群会处于 red 状态，并不会主动将 stale shard 提升为 primary shard，因为该 shard 的数据不是最新的。这时如果不得不将 stale shard 提升为主分片，需要人工介入：</p>
<pre><code>curl -XPOST "http://localhost:9200/_cluster/reroute" -d '{
        "commands":[{
            "allocate_stale_primary":{
                "index":"my_index",
                "shard":"10",
                "node":"node_id",
                "accept_data_loss":true
            }
        }]
    }'
</code></pre>
<h4 id="14empty">1.4 分配 empty 分片</h4>
<p>当由于 lucene index 损坏或者磁盘故障导致某个分片的主副本都丢失时，为了能使集群恢复 green 状态，最后的唯一方法是划分一个空 shard。</p>
<pre><code>curl -XPOST "http://localhost:9200/_cluster/reroute" -d '{
        "commands":[{
            "allocate_empty_primary":{
                "index":"my_index",
                "shard":"10",
                "node":"node_id",
                "accept_data_loss":true
            }
        }]
    }'
</code></pre>
<p>一定要慎用该操作，会导致对应分片的数据完全清空。</p>
<h3 id="2shard">2 控制 shard 数量</h3>
<p>一般来说，增加主分片数量可以增加写入速度和查询速度，因为数据分布到了更多的节点，可以利用更多的计算和 IO 资源。增加副分片数量可以提升查询速度，并发的查询可以在多个分片之间轮询。</p>
<p>但是 shard 管理并不是 “免费” 的，shard 数量过多会消耗更多的 cpu、内存资源，引发一系列问题，主要包括如下几个方面。</p>
<h4 id="21shard">2.1 shard 过多问题</h4>
<ul>
<li><strong>引起 master 节点慢</strong></li>
</ul>
<p>任一时刻，一个集群中只有一个节点是 master 节点，master 节点负责维护集群的状态信息，而且状态的更新是在单线程中运行的，大量的 shard 会导致集群状态相关的修改操作缓慢，比如创建索引、删除索引，更新 setting 等。</p>
<p>单个集群 shard 超过 10 万，这些操作会明显变慢。集群在恢复过程中，会频繁更显状态，引起恢复过程漫长。</p>
<p>我们曾经在单个集群维护 30 多万分片，集群做一次完全重启有时候需要2-4个小时的时间，对于业务来说是难以忍受的。</p>
<ul>
<li><strong>查询慢</strong></li>
</ul>
<p>查询很多小分片会降低单个 shard 的查询时间，但是如果分片过多，会导致查询任务在队列中排队，最终可能会增加查询的整体时间消耗。</p>
<ul>
<li><strong>引起资源占用高</strong></li>
</ul>
<p>Elasticsearch 协调节点接收到查询后，会将查询分发到查询涉及的所有 shard 并行执行，之后协调节点对各个 shard 的查询结果进行归并。</p>
<p>如果有很多小分片，增加协调节点的内存压力，同时会增加整个集群的 cpu 压力，甚至发生拒绝查询的问题。因为我们经常会设置参与搜索操作的分片数上限，以保护集群资源和稳定性，分片数设置过大会更容易触发这个上限。 </p>
<h4 id="22shard">2.2 如何减少 shard</h4>
<ul>
<li><p><strong>设置合理的分片数</strong></p>
<p>创建索引时，可以指定 <code>number_of_shards</code>，默认值是 5，对于物理大小只有几个 GB 的索引，完全可以设置成更小的值。</p></li>
<li><p><strong>shard 合并</strong></p>
<p>如果集群中有大量的 MB、KB 级分片，可以通过 Elasticsearch 的 shard 合并功能，将索引的多个分片合并成 1 个分片。</p></li>
<li><p><strong>删除无用索引</strong>
根据业务场景，每个索引都有自己的生命周期。尤其对于日志型索引，超过一定时间周期后，业务就不再访问，应该及时从集群中删除。</p></li>
<li><p><strong>控制 replica 数量</strong></p>
<p>replica 可以提高数据安全性，并可以负载读请求，但是会增加写入时的资源消耗，同时使集群维护的分片数成倍的增长，引起上面提到的诸多问题。所以要尽量降低 replica 数量。</p></li>
</ul>
<h3 id="3shard">3 shard 分配</h3>
<p>Elasticsearch 通过 AllocationDecider 策略来控制 shard 在集群内节点上的分布。</p>
<h4 id="31allocationdeciders">3.1 allocation deciders</h4>
<ul>
<li><p><strong><code>same shard allocation decider</code></strong></p>
<p>控制一个 shard 的主副本不会分配到同一个节点，提高了数据的安全性。</p></li>
<li><p><strong><code>MaxRetryAllocationDecider</code></strong></p>
<p>该 Allocationdecider 防止 shard 分配失败一定次数后仍然继续尝试分配。可以通过 index.allocation.max_retries 参数设置重试次数。当重试次数达到后，可以通过手动方式重新进行分配。</p>
<pre><code>curl -XPOST "http://localhost:9200/_cluster/reroute?retry_failed"
</code></pre></li>
<li><p><strong><code>awareness allocation decider</code></strong></p>
<p>可以确保主分片及其副本分片分布在不同的物理服务器，机架或区域之间，以尽可能减少丢失所有分片副本的风险。</p></li>
<li><p><strong><code>filter allocation decider</code></strong></p>
<p>该 decider 提供了动态参数，可以明确指定分片可以分配到指定节点上。</p>
<pre><code>index.routing.allocation.include.{attribute}
index.routing.allocation.require.{attribute}
index.routing.allocation.exclude.{attribute}
</code></pre>
<p>require 表示必须分配到具有指定 attribute 的节点，include 表示可以分配到具有指定 attribute 的节点，exclude 表示不允许分配到具有指定 attribute 的节点。Elasticsearch 内置了多个 attribute，无需自己定义，包括 <code>_name</code>, <code>_host_ip</code>, <code>_publish_ip</code>, <code>_ip</code>, <code>_host</code>。attribute 可以自己定义到 Elasticsearch 的配置文件。</p></li>
<li><p><strong><code>disk threshold allocation decider</code></strong></p>
<p>根据磁盘空间来控制 shard 的分配，防止节点磁盘写满后，新分片还继续分配到该节点。启用该策略后，它有两个动态参数。</p>
<p><code>cluster.routing.allocation.disk.watermark.low</code>参数表示当磁盘空间达到该值后，新的分片不会继续分配到该节点，默认值是磁盘容量的 85%。</p>
<p><code>cluster.routing.allocation.disk.watermark.high</code>参数表示当磁盘使用空间达到该值后，集群会尝试将该节点上的分片移动到其他节点，默认值是磁盘容量的 90%。</p></li>
<li><p><strong><code>shards limit allocation decider</code></strong></p>
<p>通过两个动态参数，控制索引在节点上的分片数量。其中 <code>index.routing.allocation.total _ shards_per_node</code> 控制单个索引在一个节点上的最大分片数；</p>
<p><code>cluster.routing.allocation.total_shards_per_node</code> 控制一个节点上最多可以分配多少个分片。</p>
<p>应用中为了使索引的分片相对均衡的负载到集群内的节点，<code>index.routing.allocation.total_shards_per_node</code> 参数使用较多。</p></li>
</ul>
<h3 id="4shard">4 shard 平衡</h3>
<p>分片平衡对 Elasticsearch 稳定高效运行至关重要。下面介绍 Elasticsearch 提供的分片平衡参数。</p>
<h4 id="41elasticsearch">4.1 Elasticsearch 分片平衡参数</h4>
<ul>
<li><p><strong><code>cluster.routing.rebalance.enable</code></strong></p>
<p>控制是否可以对分片进行平衡，以及对何种类型的分片进行平衡。可取的值包括：<code>all</code>、<code>primaries</code>、<code>replicas</code>、<code>none</code>，默认值是<code>all</code>。</p>
<p><code>all</code> 是可以对所有的分片进行平衡；<code>primaries</code> 表示只能对主分片进行平衡；<code>replicas</code> 表示只能对副本进行平衡；<code>none</code>表示对任何分片都不能平衡，也就是禁用了平衡功能。该值一般不需要修改。</p></li>
<li><p><strong><code>cluster.routing.allocation.balance.shard</code></strong></p>
<p>控制各个节点分片数一致的权重，默认值是 0.45f。增大该值，分配 shard 时，Elasticsearch 在不违反 Allocation Decider 的情况下，尽量保证集群各个节点上的分片数是相近的。</p></li>
<li><p><strong><code>cluster.routing.allocation.balance.index</code></strong></p>
<p>控制单个索引在集群内的平衡权重，默认值是 0.55f。增大该值，分配 shard 时，Elasticsearch 在不违反 Allocation Decider 的情况下，尽量将该索引的分片平均的分布到集群内的节点。</p></li>
<li><p><strong><code>index.routing.allocation.total_shards_per_node</code></strong></p>
<p>控制单个索引在一个节点上的最大分片数，默认值是不限制。</p></li>
</ul>
<p>当使用<code>cluster.routing.allocation.balance.shard</code>和<code>index.routing.allocation.total_shards_per_node</code>不能使分片平衡时，就需要通过该参数来控制分片的分布。</p>
<p>所以，我们的经验是：<strong>创建索引时，尽量将该值设置的小一些，以使索引的 shard 比较平均的分布到集群内的所有节点。</strong></p>
<p>但是也要使个别节点离线时，分片能分配到在线节点，对于有 10 个几点的集群，如果单个索引的主副本分片总数为 10，如果将该参数设置成 1，当一个节点离线时，集群就无法恢复成 Green 状态了。</p>
<p>所以我们的建议一般是保证一个节点离线后，也可以使集群恢复到 Green 状态。</p>
<h4 id="42">4.2 关于磁盘平衡</h4>
<p>Elasticsearch 内部的平衡策略都是基于 shard 数量的，所以在运行一段时间后，如果不同索引的 shard 物理大小差距很大，最终会出现磁盘使用不平衡的情况。</p>
<p>所以，目前来说避免该问题的以办法是让集群内的 shard 物理大小尽量保持相近。</p>
<h3 id="">总结</h3>
<p>主节点对 shard 的管理是一种代价相对比较昂贵的操作，因此在满足需求的情况下建议尽量减少 shard 数量，将分片数量和分片大小控制在合理的范围内，可以避免很多问题。</p>
<p>下一节我们将介绍<strong>分片内部的段合并</strong>相关问题。</p>
<blockquote>
  <p>为了方便学习和技术交流，创建了高可用 Elasticsearch 集群的读者群，入群方式在第 1-3 课，欢迎已购课程的同学入群交流。</p>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5ce50135308dd66813d927a6&utm_source=ESzcsd001">点击了解《高可用 Elasticsearch 集群 21 讲》</a>。</p>
</blockquote></div></article>