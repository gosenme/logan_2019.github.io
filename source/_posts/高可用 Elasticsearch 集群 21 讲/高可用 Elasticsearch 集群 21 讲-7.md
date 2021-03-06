---
title: 高可用 Elasticsearch 集群 21 讲-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>当新文档被索引到 Elasticsearch，他们被暂存到索引缓冲中。当索引缓冲达到 flush 条件时，缓冲中的数据被刷到磁盘，这在 Elasticsearch 称为 refresh，refresh 会产生一个新的 Lucene 分段，这个分段会包含一系列的记录正排和倒排数据的文件。</p>
<p>当他们还在索引缓冲，没有被 refresh 到磁盘的时候，是无法被搜索到的。因此为了保证较高的搜索可见性，默认情况下，每1秒钟会执行一次 refresh。</p>
<p>因此这会频繁地产生 Lucene 段文件，为了降低需要打开的 fd 的数量，优化查询速度，需要将这些较小的 Lucene 分段合并成较大的段，引用一张官网的示意图如下：</p>
<p><img src="https://images.gitbook.cn/FsziqJaho_e2aQYv6APf4sy0kCGK" alt="avatar" /></p>
<p>在段合并之前，有四个较小的分段对搜索可见，段合并过程选择了其中三个分段进行合并，当合并完成之后，老的段被删除：</p>
<p><img src="https://images.gitbook.cn/Fk7gDD8YDlbU8YuhK_Xt_zP1LuFR" alt="avatar" /></p>
<p>在段合并（也可以称为 merge）的过程中，此前被标记为删除的文档被彻底删除。因此 merge 过程是必要的，但是进行段合并耗费的资源比较高，他不能仅仅进行 io 的读写操作就完成合并过程，而是需要大量的计算，因此数据入库过程中有可能会因为 merge 操作占用了大量 CPU 资源。进而影响了入库速度。我们可以通过 <code>_nodes/hot_threads</code> 接口查看节点有多少个线程在执行 merge。</p>
<p><code>hot_threads</code> 接口返回每个节点，或者指定节点的热点线程，对于 merge 来说，他的堆栈长成下面这个样子：</p>
<p><img src="https://images.gitbook.cn/FuX5iCYIzPTx432Xeh9N8JF9-o-D" alt="avatar" /></p>
<p>可以通过红色框中标记出来的文字来找到 merge 线程。</p>
<h3 id="1merge">1 merge 优化</h3>
<p>很多时候我们希望降低 merge 操作对系统的影响，通常从以下几个方面入手：</p>
<ul>
<li>降低分段产生的数量和频率，少生成一些分段，自然就可以少执行一些 merge 操作</li>
<li>降低最大分段大小，达到我们指定的大小后，不再进行段合并操作。这可以让较大的段不再参与 merge，节省大量资源，但最终分段数会更多一些</li>
</ul>
<p>具体来说可以执行以下调整：</p>
<p><strong>1. <code>refresh</code></strong></p>
<p>最简单的是增大 refresh 间隔时间，可以动态的调整索引级别的 <code>refresh_interval</code> 参数，-1 代表关闭自动刷新。</p>
<p>具体取值应该参考业务对搜索可见性的要求。在搜索可见性要求不高的业务上，我们将此值设置为分钟级。</p>
<p><strong>2. <code>indices.memory.index_buffer_size</code></strong></p>
<p>索引缓冲用于存储刚刚被索引的文档，当缓冲满的时候，这些数据被刷到磁盘产生新的分段。默认值为整个堆内存的10%，可以适当提高此值，例如调整到30%。该参数不支持动态调整。</p>
<p><strong>3. 避免更新操作</strong></p>
<p>尽量避免更新文档，也就是说，尽量避免使用同一个 docid 进行文档更新。</p>
<p>对文档的 update 需要先执行 Get 操作，再执行 Index 操作，执行 Get 操作时，realtime 参数被设置为 true，在 Elasticsearch 5.x 及以后之后的版本中，这会导致一个对索引的 refresh 操作。</p>
<p>同理，Get 操作默认是实时的，应该尽量避免客户端直接发起的 Get 操作，或者将 Get 操作的请求中将 <code>realtime</code> 参数设置为 false。</p>
<p><strong>4. 调整 merge 线程数</strong></p>
<p>执行 merge 操作的线程池由 Lucene 创建，其最大线程池数由以下公式计算：</p>
<pre><code>Math.max(1, Math.min(4, Runtime.getRuntime().availableProcessors() / 2))
</code></pre>
<p>你可以通过以下配置项来调整：</p>
<pre><code>index.merge.scheduler.max_thread_count
</code></pre>
<p><strong>5. 调整段合并策略</strong></p>
<p>Lucene 内置的段合并策略有三种，默认为分层的合并策略：tiered。对于这种策略，我们可以调整下面两个值，来降低段合并次数。</p>
<pre><code>index.merge.policy.segments_per_tier
</code></pre>
<p>该参数设置每层允许存在的分段数量，值越小，就需要更多的合并操作，但是最终分段数越少。默认为10，可以适当增加此值，我们设置为24。</p>
<p>注意该值必须大于等于 <code>index.merge.policy.max_merge_at_once</code>(默认为10)。</p>
<pre><code>index.merge.policy.max_merged_segment
</code></pre>
<p>当分段达到此参数配置的大小后，不再参与后续的段合并操作。默认为 5Gb，可以适当降低此值，我们使用 2Gb，但是索引最终会产生相对更多一些的分段，对搜索速度有些影响。</p>
<h3 id="2forcemerge">2 force merge 成几个？</h3>
<p>在理想情况下，我们应该对不再会有新数据写入的索引执行 force merge，force merge 最大的好处是可以提升查询速度，并在一定情况下降低内存占用。</p>
<p>未进行 force merge 的时候，对分片的查询需要遍历查询所有的分段，很明显，在一次查询中会涉及到很多文件的随机 io，force merge 降低分段数量大大降低了所需随机 io 的数量，带来查询性能的提升。</p>
<p>但是对一个分片来说， force merge 成几个分段比较合适？这没有明确的建议值，我们的经验是，维护分片下的分段数量越少越好，理想情况下，你可以 force merge 成一个，但是 merge 过程占用大量的网络、io、以及计算资源。</p>
<p>如果在业务底峰期开始执行的 force merge 到了业务高峰期还没执行完，已经影响到集群的性能，就应该增加 force merge 最终的分段数量。</p>
<p>目前我们让分段合并到 2GB 就不再合并，因此 force merge 的数量为：<strong>分片大小/2GB</strong></p>
<h3 id="3flushmerge">3 flush 和 merge 的其他问题</h3>
<p>我们总结一下关于 flush 和 merge 的一些原理，这是一些新同学学习 Elasticsearch 过程中的常见问题。</p>
<ul>
<li><p>从索引缓冲刷到磁盘的 refresh 过程是同步执行的。</p>
<p>像 hbase 这种从缓冲刷到磁盘的时候是异步的，hbase 会开辟一个新的缓冲去写新数据。但同步执行不意味着这是耗时很久的 io 操作，因为数据会被先写入到系统 cache，因此通常情况下这不会产生磁盘 io，很快就会执行完成。</p>
<p>但是这个过程中操作系统会判断 page cache 的脏数据是否需要进行落盘，如果需要进行落盘，他先执行异步落盘，如果异步的落盘来不及，此时会阻塞写入操作，执行同步落盘。</p>
<p>因此在 io 比较密集的系统上，refresh 有可能会产生阻塞时间较长的情况，这种情况下可以调节操作系统内核参数，让脏数据尽早落盘，需要同时调整异步和同步落盘的阈值，具体可以参考《Elasticsearch 源码解析与优化实战》 21.3.3 章节。</p></li>
<li><p>merge 策略和具体的执行过程，以及merge 过程所用的线程池是 Lucene 维护的，而不是在 Elasticsearch 中。</p></li>
<li><p>merge 过程是异步执行的，也就是说，refresh 过程中判断是否需要执行 merge，如果需要执行 merge，merge 不会阻塞 refresh 操作。</p></li>
<li><p>很多同学对 Elasticsearch 的刷盘与 Lucene 的 commit 之间的关系容易搞混乱，我们在此用一句话总结两者之间概念的关系： Elasticsearch 的 refresh 调用 Lucene 的 flush；Elasticsearch 的 flush 调用 Lucene 的 commit。</p></li>
</ul>
<h3 id="">总结</h3>
<p>本章介绍了分段合并的原理及实际使用过程中常见问题，以及应对方法，段合并是必要的，但是堆栈中如果出现过多的 merge 线程，并且在长时间周期内占据堆栈，则需要注意一下，可能需要一些调整，在调整之前，应该首先排查一下如此多的 merge 是什么原因产生的。</p>
<p>第二部分的这两节课程我们深入介绍了 Elasticsearch 分片及分段在实际应用时的原则和注意事项，下一节我们将介绍一些 Elasticsearch 的 Cache 机制和实际应用。</p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>