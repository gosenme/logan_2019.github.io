---
title: 高可用 Elasticsearch 集群 21 讲-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用 Elasticsearch 过程中，你会发现你偶尔需要将一个集群的数据迁移到另一个集群，或者把索引的数据迁移到另一个具有不同 mapping 或者分片数的索引。本章总结常见的迁移场景和迁移方法。</p>
<h3 id="1">1. 数据迁移场景</h3>
<p><strong>(1) mapping 发生了改变</strong></p>
<p>Elasticsearch 的 scheme 十分灵活，支持给类型动态添加新的字段， <strong>6.x</strong> 之前的版本支持给索引动态的添加新的类型。但是不支持修改已有的字段的类型，也不能使用新的分词器对已有的字段进行分析，因未这会影响到已有数据的搜索。</p>
<p>所以，如果业务中 mapping 发生了变化，而你又必须保留历史数据，最简单和直接的办法就是根据新的 mapping 创建好新索引，然后降历史数据从历史索引迁移到新索引。</p>
<p><strong>(2) 调整分片数</strong></p>
<p>默认情况下，Elasticsearch 创建的索引分片数为 5 个。或许你在创建索引初期也评估了分片数的设置，但是后期仍然需要调大索引的分片数，如果您使用的是 6.1 之后的版本，那可以采用 shard split 功能。否则只能按照合理的分片数，建立好目标索引，然后降索引数据从历史索引迁移到新索引。</p>
<p><strong>(3) 拆分索引</strong></p>
<p>随着业务的发展，前期的设计无法满足目前的性能要求和业务场景。比如索引需要按天划分而不是按月或按周。索引需要按类型划分而不是降多个类型存储到单个索引中等，需要按照合理的方式拆分好目标索引，并将数据从历史索引迁移到新索引</p>
<p><strong>(4) 机房变化</strong></p>
<p>由于某种原因，数据从一个数据中心迁移到另一个数据中心。涉及集群数据的整体搬迁。</p>
<h3 id="2">2. 迁移前需要考虑的问题</h3>
<p><strong>(1) <code>_source</code>是否启用？</strong></p>
<p>Elasticsearch 默认启用 <code>\_source</code>字段，<code>\_source</code>字段存储了原始 json 文档，<code>\_source</code>并不会被索引，它主要用于查询结果展示。Elasticsearch 的 reindex api依赖该字段；而且在没有原始数据的情况下，如果_source没有启用，有些场景的迁移无法完成。</p>
<p><strong>(2) 版本兼容情况</strong></p>
<p>Elasticsearch 不支持加载跨版本的索引数据，比如 6.x 可以加载 5.x 的索引文件，但是不能加载 1.x 及 2.x 的索引文件。snapshot/restore 功能也是如此，不支持跨版本的备份和恢复。</p>
<p>所以，在跨集群迁移数据前要明确目标集群和源集群的 Elasticsearch 版本。如果包含跨越大版本的索引，这部分索引只能通过 reindex 来迁移。</p>
<h3 id="3">3. 迁移方法</h3>
<h4 id="31snapshotrestore">3.1 snapshot/restore</h4>
<p>snapshot/restore 是 Elasticsearch 用于对数据进行备份和恢复的一组 api 接口，可以通过 snapshot/restore 接口进行跨集群的数据迁移，该方法支持索引级、集群级的 snapshot/restore。</p>
<p><strong>(1) 前提条件</strong></p>
<p>目的集群的 Elasticsearch 版本号要大于等于源端集群索引版本号且不能跨越大版本。</p>
<p><strong>(2) 操作步骤</strong></p>
<ul>
<li>源集群配置仓库路径
修改源集群中 Elasticsearch 的配置文件，<code>elasticsearch.yml</code>，添加如下配置：</li>
</ul>
<pre><code>path.repo: ["/data/to/backup/location"]
</code></pre>
<ul>
<li>源集群中创建仓库</li>
</ul>
<pre><code> curl -XPUT "http://[source_cluster]:[source_port]/_snapshot/backup"  -d '{
     "type": "fs",
     "settings": {
         "location": "/data/to/backup/location" 
         "compress": true
     }
 }'
</code></pre>
<ul>
<li>源集群创建 snapshot</li>
</ul>
<pre><code> curl -XPUT http://[source_cluster]:[source_port]/_snapshot/backup/indices_snapshot_1?wait_for_completion=true
</code></pre>
<ul>
<li>目标集群配置和创建仓库</li>
</ul>
<p>该步骤与源集群中步骤类似, 不再赘述。</p>
<ul>
<li><p>将 snapshot 从源集群仓库移动到目的集群仓库</p></li>
<li><p>目的集群执行 restore</p></li>
</ul>
<pre><code>curl -XPUT "http://[dest_cluster]:[dest_port]/_snapshot/backup/indices_snapshot/_restore"
</code></pre>
<ul>
<li>检查恢复状态</li>
</ul>
<pre><code> curl -sXGET "http://[dest_cluster]:[dest_port]/_snapshot/_status"
</code></pre>
<p><strong>(3) 适用场景</strong></p>
<p>该迁移方式适合大量数据的迁移，支持增量迁移，但是需要比较大的存储空间来存放 snapshot。</p>
<h4 id="32reindex">3.2 reindex</h4>
<p>reindex 支持集群内和集群间的索引数据迁移。</p>
<p><strong>(1) 前提条件</strong></p>
<p>源端索引要启用 <code>\_source</code>字段, 如果没有则不能进行 reindex；reindex 需要事先在目标集群(源集群和目标集群可以是同一个集群)按照要求建立好目标索引，reindex 过程并不会自动降源端索引的设置拷贝到目标索引，否则 reindex 就失去了意义。所以在 reindex 前，要设置好目标索引的 mapping、分片数。</p>
<p><strong>(2) 集群内 reindex</strong></p>
<p>集群内 reindex 比较简单，按照新的需求创建好目标索引后，执行如下命令即可：</p>
<pre><code>POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter"
  }
}
</code></pre>
<p><strong>(3) 跨集群 reindex</strong></p>
<p>跨集群 reindex 与集群内 reindex 的主要区别是源端集群的信息需要配置到目标集群的 Elasticsearch 配置文件里，例如：</p>
<pre><code>reindex.remote.whitelist: "otherhost:9200, another:9200"
</code></pre>
<p>由于这是静态配置，配置完成后需要重启节点。之后可以通过如下命令进行数据迁移：</p>
<pre><code>POST _reindex
{
  "source": {
    "remote": {
      "host": "http://otherhost:9200",
      "username": "user",
      "password": "pass"
    },
    "index": "source",
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "dest"
  }
}
</code></pre>
<p><strong>(4) 控制参数</strong></p>
<p>reindex 提供了很多控制参数，下面介绍几个常用的配置：</p>
<ul>
<li><code>size</code></li>
</ul>
<p>指定迁移的数据条数。</p>
<ul>
<li><code>_source</code></li>
</ul>
<p>指定需要迁移数据中的哪些字段。</p>
<ul>
<li><code>size in source</code></li>
</ul>
<p>可以指定一次 scroll 的数据条数，用来控制 reindex 对源、目的集群资源消耗压力。 默认值为 1000。由于 index 过程比较消耗 cpu 资源，所以需要根据硬件环境合理配置，可以先配置一个较小的值，如果资源压力不大，逐步加大到合适的值，然后重新启动 reindex 过程。</p>
<ul>
<li><code>connect_timeout</code></li>
</ul>
<p>跨集群 reindex 时，远端集群连接超时时间，可以根据网络情况进行调整。默认值时 30s。</p>
<ul>
<li><code>socket_timeout</code></li>
</ul>
<p>跨集群 reindex 时，远端集群的读超时时间，可以根据网络情况进行调整。默认值是 30s。</p>
<ul>
<li><code>slices</code></li>
</ul>
<p>可以控制 reindex 的并发度。应用官方文档的例子：</p>
<pre><code>POST _reindex?slices=5&amp;refresh
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter"
  }
}
</code></pre>
<blockquote>
  <p>注意：较大的值会对源端和目的端带来资源压力。需要逐步加大，观察源集群和目的集群的资源适用情况。</p>
</blockquote>
<p><strong>(5) 适用场景</strong></p>
<p>该方法依赖源端索引启用 <code>_source</code> 字段，能够提供 query 来迁移索引的一部分数据。适用于迁移数据量和索引数都比较小的场景。</p>
<h4 id="33">3.3 拷贝索引文件</h4>
<p><strong>(1) 前提条件</strong></p>
<p>源端集群和目标集群索引版本兼容，该方法不适用于集群内迁移，也不能改变目标索引的相关设置。</p>
<p><strong>(2) 迁移步骤</strong></p>
<p>迁移步骤以单个索引为例。如果有多个，可以根据步骤实现自动化脚本来完成。</p>
<ul>
<li>禁止源集群中索引的分片移动</li>
</ul>
<pre><code>curl -XPUT "http://[source_cluster]:[source_port]/_cluster/settings" -d
'{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
  }
}'
</code></pre>
<ul>
<li>源集群停止写入、更新操作，并在源端集群执行执行 <code>sync_flush</code></li>
</ul>
<pre><code>curl -XPOST "http://[source_cluster]:[source_port]/$index/_flush/synced"
</code></pre>
<ul>
<li>查找主分片目录</li>
</ul>
<p>Elasticsearch 5.x 之前，索引数据是存放在以索引名为目录的文件夹下，5.x 起是存放在 uuid 目录下，索引首先确定源端索引的 uuid：</p>
<pre><code>curl -sXGET "http://[source_cluster]:[source_port]/_cat/indices/$index?v"
</code></pre>
<p>之后确定所有主分片所在节点：</p>
<pre><code>curl -sXGET "http://[source_cluster]:[source_port]/_cat/shards/$index" | grep " p "
</code></pre>
<p>最后一列为各个主分片所在的节点。这样就可以根据节点配置的 path.data 及索引的 uuid 找到索引存放的位置。</p>
<ul>
<li>将索引主分片的所有数据拷贝到目标集群。</li>
</ul>
<p>采用 rsync 方式，将索引文件从源集群数据目录拷贝到目的集群中的数据目录中。Elasticsearch 会加载拷贝的索引文件。</p>
<ul>
<li>检查迁移结果</li>
</ul>
<p>待目的集群将迁移过去的索引加载完成，集群状态恢复成 Green 后，检查目的集群中该索引的 doc 数是否与源集群中对应索引的 doc 数是否相等。</p>
<ul>
<li>打开副本</li>
</ul>
<p>迁移过程只迁移了主分片，如果索引在目的集群中有副本需求，需要根据需求设置合理的副本数量。一般保留一个副本即可：</p>
<pre><code>curl -XPUT "http://[dest_cluster]:[dest_port]/$index/_settings" -d '{"index.number_of_replicas": 1}'
</code></pre>
<p><strong>(3) 注意事项</strong></p>
<p>当删除一个索引时，Elasticsearch 会在集群状态里保存删除的索引的名称，防止被删除的索引被重新加载到集群，</p>
<p><code>cluster.indices.tombstones.size</code>, 默认值500。如果目标集群删除的索引列表中包含同名代迁移的索引，则拷贝的索引文件会出现不能加载的情况。检查方法</p>
<pre><code>curl -sXGET 'http://localhost:9200/_cluster/state/metadata?pretty'
</code></pre>
<p>执行以上命令，在 “index-graveyard” 部分查找是否有和要导入索引同名的索引。如果存在，可以减少 <code>cluster.indices.tombstones.size</code> 的配置，或者通过脚本创建删除索引使该索引名从 index graveyard 里移除，例如：</p>
<pre><code>for((i=0;i&lt;500;i++&gt;))
do
    curl -XPUT "http://localhost:9200/index_should_not_exists_$i";
    curl -XDELETE "http://localhost:9200/index_should_not_exists_$i;
done
</code></pre>
<p><strong>(4) 适用场景</strong></p>
<p>该方法采用直接拷贝索引文件的方式，迁移速度完全取决于带宽， 对带宽占用较高，对 cpu 和内存资源占用很低。适用于有大量数据需要迁移的场景。源端索引不需要启用 <code>\_source</code> 字段。我们做过多次数据迁移，优先都是采用此方式。</p>
<h3 id="">总结</h3>
<p>本课介绍了数据迁移的方法及不同方法适用的场景，希望可以帮助需要迁移数据的同学找到合适的迁移方法。</p>
<p>下一节我们介绍下常用的<strong>重要配置及注意事项。</strong></p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>