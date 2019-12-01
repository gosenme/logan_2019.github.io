---
title: 高可用 Elasticsearch 集群 21 讲-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在业务上线之前，压力测试是一个十分重要的环节，他不仅能让你了解集群能够支撑多大的请求量，以便在业务增长过程中提前扩容，同时在压力场景下也能提前发现以下不常见的问题。</p>
<p>由于业务数据的千差万别，除了参考 Elasticsearch 集群的基准测试指标，每个业务都应该使用自己的数据进行全链路的压力测试。</p>
<p>你可以使用很多工具进行压力测试，例如编写 shell 脚本使用 curl、ab 等命令行工具，也可以自己开发压测工具或者使用 Jmeter 进行压测，在此我们建议使用官方的压测工具：esrally 。官方也是使用这个工具进行压力测试的， 使用 esrally 可以做到：</p>
<ul>
<li>得到读写能力，读写 QPS 能达到多少？</li>
<li>对压测结果进行对比，例如不同版本，不同数据，不同索引设置下的性能差异，例如关闭 <code>_all</code> 之后写入性能可以提高多少？</li>
<li>同时监控 JVM 信息，可以观察 GC 等指标是否存在异常。</li>
</ul>
<h3 id="1esrally">1 esrally 的安装和配置</h3>
<p>esrally 是 Elastic 的开源项目，由 python3 编写，安装 esrally 的系统环境需求如下：</p>
<ul>
<li>为了避免多个客户端从磁盘数据成为性能瓶颈，最好使用 SSD；</li>
<li>操作系统支持 Linux 以及 MacOS，不支持 Windows；</li>
<li>Python 3.4 及以上；</li>
<li>Python3 头文件；</li>
<li>pip3；</li>
<li>git 1.9 及以上；</li>
<li>JDK 8，并且正确设置了 JAVA_HOME 环境变量；</li>
</ul>
<p>当上述环境准备就绪后，可以通过 pip3 简单安装：</p>
<pre><code>pip3 install esrally
</code></pre>
<p>安装完毕后，esrally 所需的配置文件等已经被安装到默认位置，你可以运行下面的命令重新生成这些默认配置：</p>
<pre><code>esrally configure
</code></pre>
<p>如果想要修改默认的配置文件路径，可以运行下面的命令进行高级设置：</p>
<pre><code>esrally configure --advanced-config
</code></pre>
<h3 id="2">2 基本概念</h3>
<p>压测工具引用了很多汽车拉力赛中的概念，要学会使用 esrally 必须理解这些术语。</p>
<p><strong>track</strong>
赛道，在 esrally 中指测试数据以及对这些测试数据执行哪些操作，esrally 自带了一些测试数据，执行：</p>
<pre><code>esrally list tracks
</code></pre>
<p>命令可以查看目前都有哪些 track</p>
<p>我们以 <code>geonames/track.json</code> 为例看看一个 trace 都包含了哪些东西：</p>
<p><img src="https://images.gitbook.cn/FtBTfIxIHySOmu43rLuTIMEjY0SI" alt="avatar" /></p>
<p>在这一堆信息中只需要重点关注几个字段：
indices：描述了测试时数据写入到哪个索引，以及测试数据的 json 文件名称
challenges：描述了测试过程中都要执行哪些操作</p>
<p><strong>challenge</strong>
在赛道上执行哪些挑战。此处只对数据执行哪些压测操作。这些操作的部分截图如下：</p>
<p><img src="https://images.gitbook.cn/FsWSS6AxypPrH1ED-aolYcqlzSCe" alt="avatar" /></p>
<p>可以看到先执行删除索引，然后创建索引，检查集群健康，然后执行索引写入操作。</p>
<p><strong>car</strong>
赛车，这里待测试的指 Elasticsearch实例，可以为每个实例进行不同的配置。通过下面的命令查看都有哪些自带的 car</p>
<pre><code>esrally list cars
</code></pre>
<p><strong>race</strong>
进行一次比赛，此处指进行一次压测，进行一次比赛要指定赛道，赛车，进行什么挑战。此处需要指定 track，challenge，car。通过下面的命令可以查看已经执行过的压测：</p>
<pre><code>esrally list races
</code></pre>
<p><strong>Tournament</strong>
锦标赛，由多次 race 组成一个</p>
<h3 id="3">3 执行压测</h3>
<p>esrally 可以自行下载指定版本的 Elasticsearch进 行测试，也可以对已有集群进行测试。如果想要对比不同版本，不同 Elasticsearch 配置，开启<code>_all</code> 与否等性能差异，那么建议使用 esrally 管理的 Elasticsearch 实例。</p>
<p>如果只想验证一下读写吞吐量，可以使用外部集群，运行 esrally 的服务器与 Elasticsearch 集群独立部署也可以让测试结果更准确。现在我们先使用 esrally 自己管理的 Elasticsearch 实例快速执行一个简单的压测：</p>
<pre><code>esrally --distribution-version=6.5.1   --track=geonames  --challenge=append-no-conflicts --car="4gheap"  --test-mode --user-tag="demo:test"
</code></pre>
<p><strong><code>--distribution-version</code></strong></p>
<p>esrally 会下载 6.5.1 版本的 Elasticsearch</p>
<p><strong><code>--track</code></strong></p>
<p>使用 geonames 这个数据集</p>
<p><strong><code>--challenge</code></strong></p>
<p>执行 append-no-conflicts 操作序列</p>
<p><strong><code>--car</code></strong>
使用 Elasticsearch 实例配置为 4gheap</p>
<p><strong><code>--test-mode</code></strong></p>
<p>由于这个数据集比较大，我们为了快速完成压测示例，通过此参数只使用 1000 条数据进行压测。</p>
<p><strong><code>--user-tag</code></strong></p>
<p>参数为本次压测指定一个标签，便于在多次压测之间进行区分。</p>
<p>压测开始运行后，正常情况下其输出信息如下：</p>
<p><img src="https://images.gitbook.cn/FiELHU3CZpfCOGJVyunCQ0mcrkO8" alt="avatar" /></p>
<p>压测完成后会产生详细的压测结果信息，部分结果如下：</p>
<p><img src="https://images.gitbook.cn/Fq4vOkKbMkxI4kJXFGavxEk_3M67" alt="avatar" /></p>
<p>这些结果包括索引写入速度，写入延迟，以及 JVM 的 GC 情况等我们关心的指标。你可以在运行压测时指定 <code>--report-file=xx</code> 来将压测结果单独保存到一个文件中。</p>
<p>如果使用相同的数据集对外部已有集群进行压测，则对应的命令如下：</p>
<pre><code>esrally  --pipeline=benchmark-only --target-hosts=hostname:9200 --client-options="basic_auth_user:'elastic',basic_auth_password:'xxxxxx'" --track=geonames  --challenge=append-no-conflicts   --test-mode --user-tag="demo:mycluster"
</code></pre>
<p><strong><code>--pipeline</code></strong>
简单的理解就是带测试的 Elasticsearch 集群来着哪里，包括直接下载发行版，从源码编译，或者使用外部集群，要对外部已有集群进行压测，此处需要设置为 benchmark-only </p>
<p><strong><code>--client-options</code></strong>
指定客户端附加选项，这些选项会设置到发送到 Elasticsearch 集群的请求中，如果目标集群开启了安全认证，我们需要在此处指定用户名和密码。</p>
<p>启动压测后，esrally 会弹出如下警告，测试外部集群时，esrally 无法收集目标主机的 CPU 利用率等信息，对这个警告不必紧张。</p>
<p><img src="https://images.gitbook.cn/FjiEpjhK8e8wSvLzHqyG-KEtdeXA" alt="avatar" /></p>
<h3 id="4">4 对比压测结果</h3>
<p>现在，我们进行了两次压测，可以将两次压测结果进行对比，先执行下面的命令列出我们执行过的 race：</p>
<pre><code>esrally list races
</code></pre>
<p>输出信息如下：</p>
<pre><code>Recent races:

Race Timestamp    Track     Track Parameters    Challenge            Car       User Tags
----------------  --------  ------------------  -------------------  --------  -----------------------------
20190212T102025Z  geonames                      append-no-conflicts  external  demo=mycluster
20190212T095938Z  geonames                      append-no-conflicts  4gheap    demo=test
</code></pre>
<p>User Tags 列可以让我们容易区分两次 race，现在我们以 demo=test 为基准测试，对比  demo=mycluster 的测试结果。在进行对比时，需要指定 race 的时间戳，也就是上面结果中的第一列：</p>
<pre><code>esrally compare --baseline=20190212T095938Z --contender=20190212T102025Z
</code></pre>
<p>输出信息的前几列如下：</p>
<p><img src="https://images.gitbook.cn/FnxKBcFVp2Z9SWfjaz3PkzA4VGSD" alt="avatar" /></p>
<p>对比结果给出了每个指标相对于基准测试的 diff 量，可以非常方便地看到压测结果之间的差异。</p>
<h3 id="5track">5 自定义 track</h3>
<p>我们通常需要使用自己的数据进行测试，这就需要自己定义 track。esrally 自带的 track 默认存储在 <code>~/.rally/benchmarks/tracks/default</code> 目录下，我们自己定义的 track 可以放在这个目录下也可以放到其他目录，使用的时候通过 <code>--track-path=</code> 参数指定存储目录。下面我们来定义一个名为 demo 的最简单 track。</p>
<p><strong>1. 准备样本数据</strong></p>
<p>先创建用于存储 track 相关文件的目录，目录名就是未来的 trace 名称：</p>
<pre><code>mkdir ~/test/demo
</code></pre>
<p>track 所需的样本数据为 json 格式，结构与 bulk 所需的类似，在最简单的例子中，我们在 documents.json 中写入1000行相同的内容：</p>
<pre><code>cat documents.json |head -n 3
{"name":"zhangchao"}
{"name":"zhangchao"}
{"name":"zhangchao"}
</code></pre>
<p><strong>2. 定义索引映射</strong></p>
<p>样本数据准备好之后，我们需要为其配置索引映射和设置信息，我们建立 <code>index.json</code> 文件，写入如下内容：</p>
<pre><code>{
    "settings": {
        "index.refresh_interval": "120s",
        "index.translog.durability" : "async",
        "index.translog.flush_threshold_size" : "5000mb",
        "index.translog.sync_interval" : "120s",
        "index.number_of_replicas": 0,
        "index.number_of_shards": 8
    },
    "mappings": {
        "doc": {
            "dynamic": false,
            "properties": {
                "name":{"type":"keyword"}
            }
        }
    }
}
</code></pre>
<p>在  index.json 中添加你自己的索引设置，并在 mappings 中描述字段类型等信息。</p>
<p><strong>3. 编写 track.json 文件</strong></p>
<p>该配置文件是 track 的核心配置文件，本例中，编写内容如下：</p>
<pre><code>{% import "rally.helpers" as rally %}
{
  "version": 2,
  "description": "Demo benchmark for Rally",
  "indices": [
    {
      "name": "demo",
      "body": "index.json",
      "types": [ "doc" ]
    }
  ],
  "corpora": [
    {
      "name": "rally-demo",
      "documents": [
        {
          "source-file": "documents.json",
          "document-count": 1000,
          "uncompressed-bytes": 21000
        }
      ]
    }
  ],
"operations": [
    {{ rally.collect(parts="operations/*.json") }}
  ],
  "challenges": [
    {{ rally.collect(parts="challenges/*.json") }}
  ]
}
</code></pre>
<ul>
<li><p><strong>description</strong></p>
<p>此处的描述是 <code>esrally list tracks</code> 命令输出的 tracks 描述信息。</p></li>
<li><p><strong>indices</strong></p>
<p>写入 Elasticsearch 集群时目标索引信息。
name：索引名称；
body：索引设置信息文件名；
types：索引的 type；</p></li>
<li><p><strong>corpora</strong></p>
<p>指定样本数据文件及文件信息。
source-file：样本数据文件名
document-count：样本数据文件行数，必须与实际文件严格一致，可以通过 <code>wc -l documents.json</code> 命令来计算。
uncompressed-bytes：样本数据文件字节数，必须与实际文件严格一致，可以通过 <code>ls -l documents.json</code> 命令来计算。</p></li>
<li><p><strong>operations</strong></p>
<p>用来自定义 operation 名称，此处我们放到 operations 目录下独立的 json 文件中。</p></li>
<li><p><strong>challenges</strong></p>
<p>描述自定义的 challenges 要执行哪些操作，此处我们放到 challenges 目录下的独立文件中。</p></li>
</ul>
<p><strong>4. 自定义 operations</strong></p>
<p>这里自定义某个操作应该如何执行，在我们的例子中，我们定义索引文档操作以及两种查询请求要执行的操作：</p>
<pre><code> {
      "name": "index-append",
      "operation-type": "bulk",
      "bulk-size": {{bulk_size | default(5000)}},
      "ingest-percentage": {{ingest_percentage | default(100)}}
},
{
      "name": "default",
      "operation-type": "search",
      "body": {
        "query": {
          "match_all": {}
        }
      }
    },
    {
      "name": "term",
      "operation-type": "search",
      "body": {
        "query": {
          "term": {
            "method": "GET"
          }
        }
      }
    },
</code></pre>
<p>这个文件不必完全重写，我们可以从 esrally 自带的 track 目录中拷贝 <code>operations/default.json</code> 到自己的目录下进行修改。</p>
<p><strong>5. 自定义 challenges</strong></p>
<p>我们先定义一个写数据的 challenges，内容如下：</p>
<pre><code>cat challenges/index.json

{
  "name": "index",
  "default": false,
  "schedule": [
    {
      "operation": {
        "operation-type": "delete-index"
      }
    },
    {
      "operation": {
        "operation-type": "create-index"
      }
    },
    {
      "operation": {
        "operation-type": "cluster-health",
        "request-params": {
          "wait_for_status": "green"
        }
      }
    },
    {
          "operation": "index-append",
                "warmup-time-period": 120,
          "clients": {{bulk_indexing_clients | default(16)}}
    },
    {
      "operation": {
        "operation-type": "refresh"
      }
    },
    {
      "operation": {
        "operation-type": "force-merge"
      }
    }
  ]
}
</code></pre>
<p><strong>name</strong>
指定该 challenge 的名称，在运行 race 的时候， <code>--challenge</code> 参数 指定的就是这个名称</p>
<p><strong>schedule</strong>
指定要执行的操作序列。在我们的例子中，依次执行删除索引、创建索引、检查集群健康，写入数据，执行刷新、执行 force-merge</p>
<p>接下来，我们再创建一个执行查询的 challenge，内容如下：</p>
<pre><code>cat operations/default.json

{
  "name": "query",
  "default": true,
  "schedule": [
    {
      "operation": {
        "operation-type": "cluster-health",
        "request-params": {
          "wait_for_status": "green"
        }
      }
    },
    {
      "operation": "term",
      "clients": 8,
      "warmup-iterations": 1000,
      "iterations": 10
    },
    {
      "operation": "match",
      "clients": 8,
      "warmup-iterations": 1000,
      "iterations": 10
    }
  ]
}
</code></pre>
<p>该 challenge 同样先检查集群状态，然后依次执行我们预定义的 term 和 match 操作。</p>
<p>你也可以不将自定义 operations 放到单独目录中，而是在自定义 challenge 的时候直接合并在一起，但是分开来可以让自定义 challenge 的文件开起来更清晰一些。</p>
<p>同样，自定义的 operations 内容也可以直接写在 track.json 文件中，但是分开更清晰。</p>
<p>到此，我们自定义的 track 已经准备完毕，demo 目录下的文件结构如下：</p>
<pre><code>tree demo
demo
├── challenges
│   ├── index.json
│   └── query.json
├── documents.json
├── index.json
├── operations
│   └── default.json
└── track.json
</code></pre>
<p>执行下面的命令可以看到我们创建完毕的 track：</p>
<pre><code>esrally list tracks --track-path=~/test/demo
</code></pre>
<p>输出信息如下：</p>
<p><img src="https://images.gitbook.cn/Fv6twVgBp6ubVFWAHAM8333G4j8H" alt="avatar" /></p>
<p>现在，我们可以通过下面的命令使用刚刚创建的 track 进行测试：</p>
<pre><code>esrally  --track-path=/home/es/test/demo --pipeline=benchmark-only --target-hosts=hostname:9200 --client-options="basic_auth_user:'elastic',basic_auth_password:'xxxxxxx'"  --challenge=index    --user-tag="demo:mycluster_customtrack_index"
</code></pre>
<p>由于已经使用 <code>--track-path</code> 指定 track，因此不再使用 <code>--track</code> 来指定 track 名称。</p>
<h3 id="">总结</h3>
<p>使用 esrally 可以很方便的完成我们的压测需求，但是实际使用过程中可能会因为 python3 的环境遇到一些问题，因此也可以在 docker 中运行 esrally，将样本数据放在容器之外，然后将目录挂载到容器中，不会对性能测试产生多少影响。</p>
<p>现在已经有一些安装好 esrally 的 docker 镜像，可以通过 <code>docker search esrally</code> 命令来搜索可用镜像。</p>
<p>下一节我们介绍集群监控，Elasticsearch 的监控指标很多，我们将介绍一些需要重点关注的监控项。</p>
<h3 id="-1">参考</h3>
<p><a href="https://esrally.readthedocs.io/en/stable/#">官方的压测结果</a></p>
<p><a href="https://elasticsearch-benchmarks.elastic.co/#">esrally 手册</a></p>
<p><a href="https://esrally.readthedocs.io/en/latest/adding_tracks.html">Define Custom Workloads: Tracks</a></p>
<p><a href="https://github.com/elastic/rally-tracks">rally-tracks</a></p>
<p><a href="https://segmentfault.com/a/1190000011174694">Elasticsearch 压测方案之 esrally 简介</a></p>
<hr />
<h3 id="-2">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>