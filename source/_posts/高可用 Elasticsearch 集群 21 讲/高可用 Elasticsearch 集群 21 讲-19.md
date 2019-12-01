---
title: 高可用 Elasticsearch 集群 21 讲-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>当你已经熟悉系统原理，在集群遇到故障的时候仍然需要花一些时间进行定位，在我们处理过的问题中，有很多是重复性的问题，我们将这些问题进行了汇总，目的是让运维同学可以根据错误类型找到现有的解决方案，快速解决问题。</p>
<p>因此本文分享在我们运维过程中遇到的一些比较通用的问题，希望可以给读者借鉴和参考。</p>
<h3 id="1">1. 原理与诊断</h3>
<p>集群 RED 和 YELLOW 是 Elasticsearch 集群最常见的问题之一，无论 RED 还是 YELLOW，原因只有一个：有部分分片没有分配。</p>
<p>如果有一个以上的主分片没有被分配，集群以及相关索引被标记为 RED 状态，如果所有主分片都已成功分配，有部分副分片没有被分配，集群以及相关索引被标记为 YELLOW 状态。</p>
<p>对于集群 RED 或 YELLOW 的问题诊断推荐使用 Cluster Allocation Explain API，该 API 可以给出造成分片未分配的具体原因。例如，如下请求可以返回第一个未分配的分片的具体原因：</p>
<pre><code>GET /_cluster/allocation/explain
</code></pre>
<p>也可以只查看特定分片未分配的原因：</p>
<pre><code>GET /_cluster/allocation/explain
{
  "index": "myindex",
  "shard": 0,
  "primary": true
}
</code></pre>
<p>引用一个官网的例子，API 的返回信息如下：</p>
<pre><code>{
  "index" : "idx",
  "shard" : 0,
  "primary" : true,
  "current_state" : "unassigned",                 
  "unassigned_info" : {
    "reason" : "INDEX_CREATED",                   
    "at" : "2017-01-04T18:08:16.600Z",
    "last_allocation_status" : "no"
  },
  "can_allocate" : "no",                          
  "allocate_explanation" : "cannot allocate because allocation is not permitted to any of the nodes",
  "node_allocation_decisions" : [
    {
      "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
      "node_name" : "node-0",
      "transport_address" : "127.0.0.1:9401",
      "node_attributes" : {},
      "node_decision" : "no",                     
      "weight_ranking" : 1,
      "deciders" : [
        {
          "decider" : "filter",                   
          "decision" : "NO",
          "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"non_existent_node\"]"  
        }
      ]
    }
  ]
}
</code></pre>
<p>在返回结果中给出了导致分片未分配的详细信息，<code>reason</code> 给出了分片最初未分配的原因，可以理解成 unassigned 是什么操作触发的；<code>allocate_explanation</code>则进一步的说明，该分片无法被分配到任何节点，而无法分配的具体原因在 deciders 的 <code>explanation</code> 信息中详细描述。这些信息足够我们诊断问题。</p>
<p><strong>分片没有被分配的最初原因有下列类型：</strong></p>
<p><strong>1. <code>INDEX_CREATED</code></strong></p>
<p>由于 create index api 创建索引导致，索引创建过程中，把索引的全部分片分配完毕需要一个过程，在全部分片分配完毕之前，该索引会处于短暂的 RED 或 YELLOW 状态。因此监控系统如果发现集群 RED，不一定代表出现了故障。</p>
<p><strong>2. <code>CLUSTER_RECOVERED</code></strong></p>
<p>集群完全重启时，所有分片都被标记为未分配状态，因此在集群完全重启时的启动阶段，reason属于此种类型。</p>
<p><strong>3. <code>INDEX_REOPENED</code></strong></p>
<p>open 一个之前 close 的索引， reopen 操作会将索引分配重新分配。</p>
<p><strong>4. <code>DANGLING_INDEX_IMPORTED</code></strong></p>
<p>正在导入一个 dangling index，什么是 dangling index？</p>
<p>磁盘中存在，而集群状态中不存在的索引称为 dangling index，例如从别的集群拷贝了一个索引的数据目录到当前集群，Elasticsearch 会将这个索引加载到集群中，因此会涉及到为 dangling index 分配分片的过程。</p>
<p><strong>5. <code>NEW_INDEX_RESTORED</code></strong></p>
<p>从快照恢复到一个新索引。</p>
<p><strong>6. <code>EXISTING_INDEX_RESTORED</code></strong>,</p>
<p>从快照恢复到一个关闭状态的索引。</p>
<p><strong>7. <code>REPLICA_ADDED</code></strong></p>
<p>增加分片副本。</p>
<p><strong>8. <code>ALLOCATION_FAILED</code></strong></p>
<p>由于分配失败导致。</p>
<p><strong>9. <code>NODE_LEFT</code></strong></p>
<p>由于节点离线。</p>
<p><strong>10. <code>REROUTE_CANCELLED</code></strong></p>
<p>由于显式的cancel reroute命令。</p>
<p><strong>11. <code>REINITIALIZED</code></strong></p>
<p>由于分片从 started 状态转换到 initializing 状态。</p>
<p><strong>12. <code>REALLOCATED_REPLICA</code></strong></p>
<p>由于迁移分片副本。</p>
<p><strong>13. <code>PRIMARY_FAILED</code></strong></p>
<p>初始化副分片时，主分片失效。</p>
<p><strong>14. <code>FORCED_EMPTY_PRIMARY</code></strong></p>
<p>强制分配一个空的主分片。</p>
<p><strong>15. <code>MANUAL_ALLOCATION</code></strong></p>
<p>手工强制分配分片。</p>
<h3 id="2">2. 解决方式</h3>
<p>对于不同原因导致的未分配要采取对应的处理措施，因此需要具体问题具体分析。需要注意的是每个索引也有 GREEN，YELLOW，RED 状态，只有全部索引都 GREEN 时集群才 GREEN，只要有一个索引 RED 或 YELLOW，集群就会处于 RED 或 YELLOW。如果是一些测试索引导致的 RED，你直接简单地删除这个索引。</p>
<p>因此单个的未分配分片就会导致集群 RED 或 YELLOW，一些常见的未分配原因如下：</p>
<ul>
<li>由于配置问题导致的，需要修正相应的配置</li>
<li>由于节点离线导致的，需要重启离线的节点</li>
<li>由于分片规则限制的，例如 total<em>shards</em>per_node，或磁盘剩余空间限制等，需要调整相应的规则</li>
<li>分配主分片时，由于找不到最新的分片数据，导致主分片未分配，这种要观察是否有节点离线，极端情况下只能手工分片陈旧的分片为主分片，这会导致丢失一些新入库的数据。</li>
</ul>
<p>集群 RED 或 YELLOW 时，一般我们首先需要看一下是否有节点离线，对于节点无法启动或无法加入集群的问题我们单独讨论。下面我们分享一些 RED 与 YELLOW 的案例及相应的处理方式。</p>
<h3 id="3">3. 案例分析</h3>
<h4 id="a">【案例A】</h4>
<p><strong>1. 故障诊断</strong></p>
<p>首先大致看一下分片未分配原因：</p>
<pre><code>curl -sXGET "localhost:9200/_cat/shards?h=index,shard,prirep,state,unassigned.*&amp;pretty"|grep UNASSIGNED
</code></pre>
<p>结果显示分片大都是因为 node_left 导致未分配，然后通过 explain API 查看分片 myindex[3]不自动分配的具体原因：</p>
<pre><code>curl -sXGET localhost:9200/_cluster/allocation/explain?pretty -d '{"index":"myindex","shard":3,"primary":true}' 
</code></pre>
<p>我们在 explain api 中指定了只显示 分片 myindex[3] 的信息，诊断结果的主要信息如下：</p>
<pre><code> "can_allocate" : "no_valid_shard_copy",
  "allocate_explanation" : "cannot allocate because all found copies of the shard are either stale or corrupt",
</code></pre>
<p>意味着 Elasticsearch 找到了这个分片在磁盘的数据，但是由于分片数据不是最新的，无法将其分配为主分片。</p>
<p>从多个副本中选择哪个分片作为主分片的策略在 2.x 及 6.x 中有较大变化，具体可以参阅《Elasticsearch 源码解析与优化实战》</p>
<p><strong>2. 解决方式</strong></p>
<p>如果有离线的节点，启动离线的节点可能会将该分片分配下去，在我们的例子中，所有节点都在线，且分片分配过程执行完成，原来拥有最新数据的主分片无法成功分配，例如坏盘的原因，可以将主分片分配到一个 stale 的节点上。这会导致丢失一些最新写入的数据。</p>
<p>首先记录一下 stale 分片所在的节点，这个信息也在 explain api 的返回信息中：</p>
<pre><code>"node_allocation_decisions" : [
    {
      "node_id" : "xxxxxx",
      "node_name" : "node2",
      "transport_address" : "127.0.0.1:9301",
      "node_decision" : "no",
      "store" : {
        "in_sync" : false,
        "allocation_id" : "HNeGpt5aS3W9it3a7tJusg"
      }
    }
  ]
</code></pre>
<p>分片所在节点为 node2，接下来将该 stale 分片分配为主分片：</p>
<pre><code>curl -sXPOST "http://localhost:9200/_cluster/reroute?pretty" -d '
{
    "commands" : [ {
        "allocate_stale_primary" : {
            "index" : "myindex",
            "shard" :3,
            "node" : "node2",
            "accept_data_loss" : true
        }
    }]
}'
</code></pre>
<h4 id="b">【案例 B】</h4>
<p><strong>1. 故障诊断</strong></p>
<p>分片分配失败，查看日志有如下报错：</p>
<pre><code>failed recovery, failure RecoveryFailedException[[log4a-20181026][2]: Recovery failed from {NSTDAT12.1}{fQM-UDjPSHu6-IMwuKg0nw}{7LNwMfeIT8uhPW8AUEPs-w}{NSTDAT12}{x.x.212.61:9301} into {NSTDAT12.0}{N8ubqgIxSvezL652baPT3w}{5uQzcvuwTOeV01_hnwipxQ}{NSTDAT12}{x.x.212.61:9300}]; nested: RemoteTransportException[[NSTDAT12.1][x.x.212.61:9301][internal:index/shard/recovery/start_recovery]]; nested: RecoveryEngineException[Phase[1] phase1 failed]; nested: RecoverFilesRecoveryException[Failed to transfer [0] files with total size of [0b]]; nested: IllegalStateException[try to recover [log4a-20181026][2] from primary shard with sync id but number of docs differ: 1483343 (NSTDAT12.1, primary) vs 1483167(NSTDAT12.0)]; 
</code></pre>
<p>产生该错误的原因是副分片与主分片 <code>sync_id</code> 相同，但是 doc 数量不一样，导致 recovery 失败。造成 <code>sync_id</code> 相同，但 doc 数量不同的原因可能有多种，例如下面的情况：</p>
<ol>
<li>写入过程使用自动生成 docid</li>
<li>主分片写 doc 完成，转发请求到副分片</li>
<li>在此期间，并行的一条 delete by query 删除了主分片上刚刚写完的 doc，同时副分片也执行了这个删除请求</li>
<li>主分片转发的索引请求到达副分片，由于是自动生成 id 的，副分片将直接写入该 doc，不做检查。最终导致副分片与主分片 doc 数量不一致。</li>
</ol>
<p>导致此类问题的一些 case 已经在 6.3.0 版本中修复，具体可以参考<a href="https://discuss.elastic.co/t/try-to-recover-test-20181128-2-from-primary-shard-with-sync-id-but-number-of-docs-differ-59432-10-1-1-189-primary-vs-60034-10-1-1-190/158983">此处</a></p>
<p><strong>2. 解决方式</strong></p>
<p>当出现线上出现这种故障时，解决这个问题也比较容易，先将分片副本数修改为 0</p>
<pre><code>curl -sXPUT "http://localhost:9200/log4a-20181026/_settings?pretty&amp;master_timeout=3m"  -d '{"index.number_of_replicas":0}}'
</code></pre>
<p>再将副本数恢复成原来的值，我们这里是 1：</p>
<pre><code>curl -sXPUT "http://localhost:9200/log4a-20181026/_settings?pretty&amp;master_timeout=3m"  -d '{"index.number_of_replicas":1}}'
</code></pre>
<p>这样重新分配副分片，副分片从主分片拉取数据进行恢复。</p>
<h3 id="">总结</h3>
<p>集群 RED 与 YELLOW 是运维过程中最常见的问题，除了集群故障，正常的创建索引，增加副分片数量等操作都会导致集群 RED 或 YELLOW，在这种情况下，短暂的 RED与 YELLOW 属于正常现象，如果你监控集群颜色，需要考虑到这一点，可以参考持续时间，Explain API的具体原因等因素制定报警规则。</p>
<p>集群颜色问题是最常见，也是最简单的问题，在我们处理过的其他问题中，大部分都是内存问题，下一节我们介绍下这部分内容。</p>
<h3 id="-1">参考</h3>
<p><a href="">https://www.elastic.co/guide/en/elasticsearch/reference/master/cluster-allocation-explain.html</a></p>
<hr />
<h3 id="-2">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>