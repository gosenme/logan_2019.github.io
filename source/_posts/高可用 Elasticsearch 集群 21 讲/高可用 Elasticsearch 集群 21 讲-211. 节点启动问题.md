---
title: 高可用 Elasticsearch 集群 21 讲-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="1">1. 节点启动问题</h3>
<p>节点启动问题主要是启动失败，可能的原因非常多，下面整理的是一些常见故障，大部分问题的详细信息可以在日志中找到。</p>
<h4 id="11a">1.1 案例 A</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>集群恢复到 90% 多后，节点频繁重启。查看节点日志，发现报错如下：</p>
<pre><code>exit due to io error
</code></pre>
<p>Elasticsearch 进程主动退出。同时日志中有大量的 <code>too many open files</code> 报错。</p>
<ul>
<li><strong>故障分析</strong></li>
</ul>
<p>通过 nodes stats API 可以查看节点打开的 fd 数量：</p>
<pre><code>curl -sXGET "localhost:9200/_nodes/stats/process?filter_path=**.max_file_descriptors,**.open_file_descriptors&amp;pretty"

{
  "nodes" : {
    "es.76.0" : {
      "process" : {
        "open_file_descriptors" : 65536,
        "max_file_descriptors" : 65536
      }
    },
    ...
}
</code></pre>
<p>该 API 返回每个节点的 fd 情况，其中 <code>open_file_descriptors</code> 代表进程当前打开的 fd 数量，<code>max_file_descriptors</code> 为最大可以打开的 fd 数量。该结果显示，节点打开的 fd 确实已达到 65536，怀疑索引 segment未 进行合并，查看节点是上 segment 的数量：</p>
<pre><code>curl -sXGET "localhost:9200/_nodes/stats/indices/segments?filter_path=**.count&amp;pretty"
</code></pre>
<p>发现非常多，大量的段文件是由于没有对冷索引执行 force merge 导致。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>该业务索引数据为日期轮转型，先关闭一批早期的索引，让节点正常启动，待集群 Green 后，对索引执行 force merge 操作，降低段文件数量。</p>
<h4 id="12b">1.2 案例 B</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>节点启动失败，查看日志输出有报错如下：</p>
<pre><code>Caused by: java.nio.file.FileAlreadyExistsException: /data01/es/nodes/0/indices/K1KZ1kgpRTCczI5rm03Q1g/1/.es_temp_file
</code></pre>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>Elasticsearch 节点启动过程中会尝试在分片目录下创建临时文件，如果文件已经存在就会启动失败，导致这个问题的原因可能是 Elasticsearch 进程在启动阶段被强制杀掉。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>Elasticsearch v5.6.0 以上的版本已经解决了这个问题，当低版本中出现时可以直接删除 <code>.es_temp_file</code> 这个临时文件。</p>
<h4 id="13c">1.3 案例 C</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>集群完全重启时，当全部节点加入集群后，master 节点开始频繁 fullgc，通过 jstat 命令观察 master 节点内存的 old 区持续增长，知道全部占满，节点停止响应</p>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>由于故障可以重现，因此重启 master 节点，当全部节点加入后，old 区开始快速增长期间，查看 master 节点的 <code>hot_threads</code> ：</p>
<pre><code>curl -X GET "localhost:9200/_nodes/master_node_name/hot_threads"
</code></pre>
<p><code>hot_threads</code> 结果显示 master 节点正在处理数据节点发送过来的集群状态，也就是说 master 当前处于 gateway 阶段，该阶段中，master 节点主动向每个具备 master 资格的节点索取集群状态，然后选举版本号最高的最为最终集群状态。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>猜测因为集群状态过大，master 索取各个节点的集群状态后 JVM 内存无法容纳。原集群没有做角色分离，每个节点都可以被选为主节点，因此调整集群结构，仅让 3 个节点具备 master 资格，重启集群后，集群正常启动。</p>
<h4 id="14d">1.4 案例 D</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>节点启动失败，查看日志文件，发现是由于 OOM 异常导致：</p>
<pre><code>unable to create new native thread
</code></pre>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>执行 <code>ulimit -u</code> 命令查看 es 用户的 max user processes，发现值为：1024，按照官网的意见，该值至少应该被设置为 2048.</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>修改 <code>/etc/security/limits.conf</code> 文件，将 nproc 值修改为 8192</p>
<pre><code>* - nproc 8192
</code></pre>
<h4 id="15e">1.5 案例 E</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>节点启动失败，查看日志文件，存在如下错误信息：</p>
<pre><code>failed to open a socket, too many open files
</code></pre>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>与案例 A 类似，先通过 nodes stats API 查看fd 数量，发现 <code>max_file_descriptors</code> 值为 1024，Elasticsearch 官方建议将 fd 的限制调整为 65536 </p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>修改 <code>/etc/security/limits.conf</code> 文件，将 nofile 值修改为 65536</p>
<pre><code>* - nofile 65536
</code></pre>
<h4 id="16f">1.6 案例 F</h4>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>节点启动失败，查看日志文件，存在如下错误信息：</p>
<pre><code>java.io.IOException: Input/output error
</code></pre>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>这日志一般意味着存在坏盘，坏盘有几种情况，一种是整块盘无法读写，还有一种是该盘的部分文件无法读写。存在坏盘的情况下，Elasticsearch 会中止启动过程，需要将坏盘的路径从配置文件的 <code>path.data</code> 中排除出去。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>从配置文件的 <code>path.data</code> 中删除坏盘的路径，重启节点。Elasticsearch 会自动补齐部分不足的数据。原来存在于坏盘上的主分片会被重新分配，分片数据不足的副分片会自动补齐。</p>
<p>但是假如仅存的一个主分片在坏盘上面，可以尝试将坏盘上的分片 数据拷贝出来，在命令行调用 Lucene 的 CheckIndex 尝试修复索引数据，修复完成后再拷贝到节点的数据目录下，Elasticsearch 自动将他加载。</p>
<h3 id="2recovery">2. Recovery 问题</h3>
<p>Elasticsearch 的 Recovery 发生在集群完全重启，以及 reopen 一个索引，增加副本等时机，执行 Recovery 的目的是：</p>
<ul>
<li>对于主分片来说，需要从事务日志恢复没有来得及刷盘的数据。</li>
<li>对于副分片来说，需要恢复成和主分片一致。</li>
</ul>
<p>在不同的大版本中，副分片执行 Recovery 的机制存在较大差异。</p>
<h4 id="21recovery">2.1 Recovery 慢</h4>
<p>为了不影响正常读写数据，索引恢复期间是有限速的，有时候我们希望集群尽快恢复，例如在集群完全重启阶段，一般会先停止入库操作。可以把默认的限速阈值增大。这些设置都可以动态调节，即时生效。</p>
<p>节点之间拷贝数据时的限速，默认为 40Mb，我们这里的网络环境为万兆，调整为 100Mb</p>
<pre><code>indices.recovery.max_bytes_per_sec
</code></pre>
<p>单个节点上执行副分片 Recovery 时的最大并发数量，默认值为 2，我们设置为 100</p>
<pre><code>cluster.routing.allocation.node_concurrent_recoveries
</code></pre>
<p>单个节点上执行主分片 Recovery 时的最大并发数量，默认值为 4，我们设置为 100</p>
<pre><code>cluster.routing.allocation.node_initial_primaries_recoveries
</code></pre>
<h3 id="3load">3. 系统 load 很高</h3>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>敲任何命令，操作系统响应都很慢，top 命令查看系统 load 很高，CPU 指标中的 sys 占用很大</p>
<ul>
<li><strong>故障分析</strong></li>
</ul>
<p>通过 <code>sar -B 1</code> 分析内存页面置换效率，发现 %vmeff 异常，该值正常情况下应该为 0 或接近 100 ，当该值异常低的时候代表页面置换效率存在问题，一般产生这种情况的原因与 NUMA 有关。关于该问题的更多分析可以参考<a href="https://elasticsearch.cn/article/348">这篇文章</a></p>
<p><img src="media/15529824334740/15532967575791.jpg" alt="" /></p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>查看内核参数的 <code>vm.zone_reclaim_mode</code> 值，发现该值为1：</p>
<pre><code>sysctl -A |grep vm.zone_reclaim_mode
</code></pre>
<p>该值在 CentOS7 系统下默认为 0，CentOS6 中默认为 1，将该值修改为 0，观察一段时间后，问题解决。编辑 <code>/etc/sysctl.conf</code>，添加 <code>vm.zone_reclaim_mode = 0</code>，然后执行 <code>sysctl -p</code> 参数立即生效，无需重启系统。对内核参数的临时性调整可以使用 <code>sysctl -w</code>，设置不会持久化，系统重启后会恢复原来的设置。</p>
<h3 id="4">4. 请求响应很慢</h3>
<ul>
<li><strong>故障现象</strong></li>
</ul>
<p>查询请求，以及 <code>_cat/thread_pool</code> 等请求长时间阻塞，平时可以秒内返回的查询请求都长时间没反应</p>
<ul>
<li><strong>故障诊断</strong></li>
</ul>
<p>产生故障之前该集群的数据总量比较高，JVM 内存使用率在 70% 以上，怀疑是节点 GC 停顿导致，由于此时 REST 接口的请求无法返回，因此通过</p>
<pre><code>jstack -gcutil es_pid
</code></pre>
<p>命令查看 Elasticsearch 各个节点的 GC 情况，发现有一个节点 JVM 利用率已经 100%，导致查询请求的协调节点再等待此节点返回数据，对于部分 _cat API 请求来说，主节点需要向各个节点抓取数据，因此一个 GC 异常的节点导致整个集群的响应都很缓慢</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>由于数据总量越大，JVM 常驻内存占用约高，根本解决方式需要对集群扩容，或者关闭、删除一些索引，临时解决方式就是观察故障节点的 GC 是否正常进行，可以重启节点。</p>
<h3 id="5">5. 入库慢</h3>
<p>导致写入速度慢的原因很多，我们有专门的一篇讨论入库速度的优化建议，现在我们分享一些运维过程中的实际案例。</p>
<h4 id="51a">5.1 案例 A</h4>
<ul>
<li><strong>故障分析</strong></li>
</ul>
<p>观察监控系统的 CPU 指标，发现只有个别节点 CPU 很高，查看热索引的分片在各个节点上的分布情况：</p>
<pre><code>curl -sXGET ‘http://localhost:9200/_cat/shards/$index/'
</code></pre>
<p>发现大部分分片分到了两个节点上，没有均匀地分配的整个集群，进一步发现没有限制索引分片在节点的数量。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>为了保证新建索引的分片在集群中均匀分配，我们调整索引的 <code>total_shards_per_node</code> 参数如下：</p>
<pre><code>curl -XPUT 'http://localhost:9200/$indices/_settings?pretty' -d '{"index.routing.allocation.total_shards_per_node":2}' 
</code></pre>
<p>将 <code>total_shards_per_node</code> 设置为 2，意味着索引在单个节点上最多只能否分片 2 个。我们的集群有10 个节点，索引主分片数为 5，副本数量为 1，如果均匀分布的话，每个节点应该有 (5×2)/10=1 个分片，考虑到节点离线等异常情况，将该值设置为 2，读者需要根据自己的实际情况进行调整。</p>
<h4 id="52b">5.2 案例 B</h4>
<ul>
<li><strong>故障分析</strong></li>
</ul>
<p>通过 <code>_cat/shards/$index</code> 发现分片在各个节点分布均匀，然后通过 <code>_nodes/hot_threads</code> 接口查看热点线程，发现有很多 merge 操作在 merge 前一天的索引。</p>
<p>我们会在每天凌晨开始 force merge 前一天索引，热点线程说明到了上午仍然没有 merge 完毕，ssh 到相关节点执行 <code>iostat -xd 1</code> 查看 utils，发现个别磁盘长期处于 100，通过 <code>_cat/indices/index</code> 查看前一天索引大小，发现索引大于 2TB，除以分片个数，单个分片大小为 200G  以上，而 force merge 的 <code>max_num_segments=1</code>，这种合并操作消耗的 CPU 和 IO 太高，导致和入库资源竞争。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>控制 force merge 后的分片数量，单个分段大小最好不要超过5G，我们将 <code>max_num_segments</code> 修改为 200/5 = 40，观察一段时间后问题得到缓解。</p>
<p>分段数量较多会对查询性能有负面影响，不过为了降低 merge 的影响，也可以将分段大小限制为 2G 或更小一点，这样 <code>max_num_segments</code> 可以设置为 100 左右。</p>
<h4 id="53c">5.3 案例 C</h4>
<ul>
<li><strong>故障分析</strong></li>
</ul>
<p>通过 <code>_nodes/hot_threads</code> 接口查看热点线程，发现很多 merge 操作，但并非 force merge 触发，而是正常的入库引起的。</p>
<p>分段合并是非常消耗 IO 和 CPU 的操作，对入库速度影响非常明显，默认情况下，入库引起的 merge 操作会将分段合并到 5G，超过5G 的不再合并。</p>
<ul>
<li><strong>解决方式</strong></li>
</ul>
<p>由于业务需要快速入库，避免数据堆积，因此调整 merge 策略，将目标最大分段大小由 5GB 修改为 500MB：</p>
<pre><code>curl -sXPUT "http://localhost:9200/*2019.01.31/_settings" -d '{"index.merge.policy.max_merged_segment":"500mb"}' 
</code></pre>
<p>并将 <code>segments_per_tier</code> 修改为 24</p>
<pre><code>curl -sXPUT "http://localhost:9200/*2019.01.31/_settings" -d '{"index.merge.policy.segments_per_tier":"24"}'
</code></pre>
<p>在分层的合并策略中，<code>segments_per_tier</code> 代表每层分段的数量，值越小则最终 segment 越少，因此需要 merge 的操作更多，默认为 10</p>
<p>这样修改后分片的最终分段较多，可以在业务低峰期的时候通过 force merge 来进一步合并。</p>
<h3 id="">总结</h3>
<p>到本节为止，本部分内容到此结束，在运维 Elasticsearch 集群的过程中，大部分问题的起因是比较简单，并且容易解决的，少数情况下需要分析内存，甚至阅读源码。</p>
<p>希望我们分享的这些案例可以给读者带来一些借鉴，并有所启发。</p></div></article>