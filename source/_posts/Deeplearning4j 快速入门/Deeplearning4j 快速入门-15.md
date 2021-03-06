---
title: Deeplearning4j 快速入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课程为大家介绍 Deeplearning4j 在 Apache Spark 上构建分布式深度学习模型的方式与底层机制。本节课的核心内容包括：</p>
<ul>
<li>Apache Spark 简介</li>
<li>深度学习的并行与分布式建模</li>
</ul>
<p>Deeplearning4j 是原生支持在 Spark 上建模的开源库之一，同样原生支持的还有 Intel BigDL、SparkNet、H2O 等。像 Caffe 和 TensorFlow 则可以借助第三方的项目，如 CaffeOnSpark 和 TensorFlowOnSpark 来完成基于 Spark 的分布式建模。</p>
<p>从具体开发的角度上讲，基于 Deeplearning4j 进行分布式建模和运行一个普通的 Spark 应用是相似的，因此熟练 Spark 应用开发是必须的基础，在下面的课程中我们也会抽出一些篇幅来做介绍。</p>
<p>在本次课程的第二个部分，我们将为大家介绍参数服务器（Parameter Server）和异步梯度共享（Gradient Sharing）的原理，这也是 Deeplearning4j 构建分布式神经网络的底层机制。</p>
<p>在下一节课程中，我们将结合之前介绍过的 Fashion-MNIST 数据集的分类应用来介绍一个完整的分布式建模案例。从读取数据、训练、评估和部署等环节介绍完整的流程。在下半部分课程中我们还会介绍下内存调优的一些机制。由于 ND4J 的底层其实是通过 JavaCPP 的方式调用了诸如 OpenBLAS/MKL 的张量运算库，因此 off-heap memory 的设置是否合理非常重要，在这一部分我们会介绍调优的细节还有常见的一些问题。下面我们首先给出原理部分的内容。</p>
<h3 id="131apachespark">13.1 Apache Spark 简介</h3>
<blockquote>
  <p><a href="http://spark.apache.org/">Apache Spark</a> 最早是 UC Berkeley 的 AMP 实验室用于构建分布式机器学习算法的一个研究项目，机器学习往往需要多次迭代，但使用类似 Hadoop 框架会因受制于 Shuffle 操作而低效，因此产生了后来对业界影响很大的弹性分布式存储的内存机制。Spark 于 2014 年成为 Apache 基金会的顶级项目，成为继 Hadoop 之后又一个备受瞩目的分布式计算框架。除了机器学习以外，Spark 陆续支持了流式计算（Spark Streaming）、图计算（GraphX）等模块，大大强化了 Spark 的功能和应用领域。目前 Spark 已经来到了 2.x 版本，其中 ML/MLlib 库中集成了常见的分类、回归、聚类算法，可以说 Spark 机器学习库是使用最广泛的分布式机器学习算法库之一。</p>
</blockquote>
<p><img src="https://images.gitbook.cn/f30ec3d0-1ef6-11e9-bcaf-e36575b0f413" alt="enter image description here" /></p>
<p>Spark 是由 Scala 编写的，可以说 Scala 函数式的编程思想使得很多应用开发变得高效和简洁，同样的逻辑使用 Java 语言如果在 150 行代码量的话，使用 Scala 可以控制在 100 行以内甚至更少。Scala 也是运行在 Java 虚拟机上的，因此 Spark 也往往被归为 Java 生态圈的项目。当然 Spark 也确实提供了 Java 的接口，方便广大 Java 程序员直接开发 Spark 应用。</p>
<p>数据模型 RDD（Resilient Distributed Dataset）是 Spark 的核心之一，这是一个可基于内存、支持分区和并行计算的存储框架。RDD 可以缓存在内存中，也可以落在磁盘上。如果 Cache 在内存中做迭代计算就非常高效，这也是很多分布式机器学习项目青睐 Spark 的原因。</p>
<p>在 Spark 1.6.0 及目前主流的 2.x 版本中，DataSet 作为新一代的数据模型被广泛应用于 Spark SQL 和 Spark ML 等模块中，DataSet 具备了 RDD 的大部分优点同时可以得到 Spark SQL 引擎的优化。DataSet 和 RDD 之间可以转化，从某种意义上说，DataSet 是就一种带有 Schema 的 RDD。</p>
<p>Spark 的运行模式大致可以分为 4 种：</p>
<ul>
<li>Local：Local 使用本地多线程的方式模拟集群。</li>
<li>Standalone：Standalone 是 Spark 自带的资源管理和任务调度框架，可以不依赖 Hadoop 在每个节点上单独部署 Spark 的 JAR 来完成 Standalone。</li>
<li>Hadoop-Yarn：Hadoop-Yarn 则是通过 Yarn 来统一调度和管理 MapReduce、Spark 等计算框架的任务。</li>
<li>Apache Mesos：基于 Mesos 的模式运行分布式 Spark 任务，指的是 Mesos Master 取代 Standalone 中的 Master，作为集群的管理者来进行 Task 分配等工作。</li>
</ul>
<p>目前我们采用的是 Hadoop-Yarn Cluster 的方式来运行 Spark 分布式任务，而本地调试的时候采用的就是 Local 模式。</p>
<p>在介绍了 Spark 的基本情况之后，我们给出一个 Spark 任务的具体实例并且结合该实例讲解下 Spark 任务开发的步骤。我们先来看下下面的这段 WordCount 的逻辑：</p>
<pre><code>import org.apache.spark.sql.SparkSession

class SparkWordCount {

}

object SparkWordCount {
  def main(args : Array[String]) : Unit = {
    val session = SparkSession.builder()
                  .appName("Word Count")
                  .master("local[*]")
                  .getOrCreate()
     //
     val nums = Array(0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9)
     val rdd = session.sparkContext.parallelize(nums);
     rdd.map((_, 1)).reduceByKey(_+_).collect().foreach(println)
     //
     session.stop()
  }
}
</code></pre>
<p>这段代码的逻辑是，统计数组中元素的出现次数。因为是介绍 Spark 的基本开发流程，这里不想给出过于复杂的逻辑，但该实例基本涵盖了 Spark 应用开发的所有要点。这里我直接用 Scala 来写，相比用 Java 来写会简单很多。</p>
<p>我们在这段逻辑里先声明了一个 SparkSession 实例，用于创建一个 Spark 的会话或者说上下文。在 Spark 1.x 的阶段，我们也可以直接声明 SparkContext。在会话实例中设置一些基本参数，如这里的应用名称、运行模型（这里是 Local）。随后我们随便创建了一个数组，里面会有一些我随意键入的数字。我们通过 parallelize 接口将本来在 driver 节点上的数据进行分布式存储，即放入一个 RDD 实例中。最后我们走一个标准的 map-reduce 流程，统计每个数字出现的次数，然后收集到 driver 节点上并遍历打印。</p>
<p>上述逻辑中我们设置了 Local 模式，所以会在本地多线程环境下对集群进行模拟，方便我们调试。虽然这里示例简单而且没什么实际价值，但是 Spark 应用的开发流程的各个主要环节已经都具备了。大致地，我们可以整理成以下几个步骤：</p>
<ol>
<li>创建 Spark 会话/上下文实例</li>
<li>业务数据 RDD/DataSet 建模</li>
<li>对于数据进行 transform/action 的操作</li>
<li>数据持久化</li>
<li>Spark 任务结束</li>
</ol>
<p>需要指出的是，像类似 map 这一类的 transform 操作是延迟的，也就是说不会立即执行，只有触发了类似 reduce/collect 等 action 操作的时候，所有 transform 和 action 操作才会被串起来执行。</p>
<h3 id="132">13.2 深度学习的并行与分布式建模</h3>
<p>在大数据技术成熟以前，数据的存储和计算面临着各种实际问题，纵然庞大的数据经过时间可以得到一定的积累，但是要想基于这些数据做些数据清洗和建模的工作非常麻烦，因此从实际应用角度上讲分布式的机器学习建模的需求并不是那么的急迫。随着 Google 发表了 Big Table 和 MapReduce 的理论，以及开源社区在这些理论基础上的贡献，诸如 Hadoop 生态圈这些项目后，算法工程师看到了在大规模高性能服务器集群上构建分布式机器学习工作的可行性和必要性，从基于 Hadoop 的 Mahout 再到基于 Spark 的 ML/MLlib，越来越多的成熟的分布式机器学习算法库在工业界得到了有效的实践和应用，分布式建模理论也逐渐受到业界的关注。</p>
<p>深度学习/深度神经网络作为当下人工智能最有效的解决方案之一，她的分布式解决方案也有很多理论研究和实际应用的成果。下面就为大家介绍下主要的几种分布式神经网络的建模方案，以及 Deeplearning4j 采用的方案。</p>
<p>深度神经网络分布式建模的方案，主要有模型并行化和数据并行化两个大类。</p>
<p><strong>模型并行化</strong>可以对多层神经网络进行分层训练，即每一层网络的参数或者若干层网络的部分参数集中在集群的一个节点上进行训练，整个集群需要一个调度器来调度各个节点之间参数的更新。模型并行化适合网络层次非常多的情况下的训练场景，由于每一个节点只训练网络的一小部分参数，因此可扩展性是比较好的。</p>
<p>另一种方式被称作<strong>数据并行化</strong>，这也是 Deeplearning4j 主要采用的解决方案。数据并行化的思想是在每个计算节点上保存一个网络的副本，并且各自训练各自的批量数据，然后再根据同步或异步的机制更新全局的网络参数。数据并行化的可扩展性并不如模型并行的方案，但相对容易实现。</p>
<p>Deeplearning4j 到目前为止支持以下两种数据并行化策略：</p>
<ul>
<li>参数服务器/参数同步平均方案（Parameter Averaging Implementation）</li>
<li>去中心化的梯度共享方案（Decentralized Asynchronous SGD/Gradient Sharing）</li>
</ul>
<p><strong>我们先来看第一种方案。</strong></p>
<p>参数服务器的是运行在 driver 节点上一个实例。它的作用是在收集了上一次迭代的各个节点的参数之后，做一次加权平均然后更新整个集群的网路参数。大概的示意图如下：</p>
<p><img src="https://images.gitbook.cn/222e1cb0-1efc-11e9-bcaf-e36575b0f413" alt="enter image description here" /></p>
<p>从图中可以看出，4 个节点将各自在本次迭代后的参数上传到参数服务器，参数服务器将拿到的各个节点的参数做完加权平均后，更新所有节点上的网络参数，然后进行下一轮的迭代。参数服务器的工作由每个 Spark 任务中的 driver 节点来做，而其他的则是 worker 节点来做。需要注意的是，Deeplearning4j 这里采用的是<strong>同步机制</strong>来更新网络参数，也就是说参数服务器会等到所有机器的最新参数都接收完后，再做加权平均，而不是收到一组或者几组参数就立即更新。</p>
<p>这样做的好处是不会出现参数延迟的情况（如：某些机器已经在做第 N+2 次迭代，而某些机器只在做第 N 次迭代），但是坏处也是非常明显，即会存在木桶效应，计算最慢的那台机器会成为整个集群计算的一个瓶颈。需要指出的是，参数服务器处理的可以是参数也可以是梯度，两种方案都是可以选择的，而 Deeplearning4j 选择的是参数的方案。</p>
<p><strong>接着我们看第二种方案。</strong></p>
<p>第二种方案是基于梯度共享的方式来做的，参考是 Amazon 的一篇论文：<em><a href="http://nikkostrom.com/publications/interspeech2015/strom_interspeech2015.pdf">Scalable Distributed DNN Training Using Commodity GPU Cloud Computing</a></em>。首先这是一种异步的梯度更新方案，着重解决的是分布式训练过程中的网络传输的瓶颈问题。由于神经网络每次迭代后参数或者梯度向量在数据量上都很可观，尤其需要通过网络进行向量数据传输的时候，网络带宽等因素会严重影响迭代的效率，这也是为什么很多并行方案会优先在单机多卡的环境下进行，可以有效避免网络 IO 的影响。</p>
<p>由于传输的数据量大，因此就自然得考虑对数据进行压缩处理。每一个节点计算的 Mini-batch 的梯度向量都是一个稀疏向量，换言之只有一小部分的参数需要更新，大部分更新的梯度接近于 0。因此这部分接近于 0 或者小于某一阈值的梯度更新可以被延迟。由此，论文中提出只对那些达到阈值要求的梯度更新进行传输，最简单就是构建一个 key-value 的映射关系（key 代表的是梯度向量的位置索引，value 代表的是更新的值）。进一步地，论文中提出可以对这组映射关系用一个 32 位的整型进一步压缩，其中的 31 位用来标识位置索引，而用 1 位来表示值。</p>
<p>下面的这张示意图可做参考：</p>
<p><img src="https://images.gitbook.cn/6f9c1fe0-1efe-11e9-ae28-d574dc548e53" alt="enter image description here" /></p>
<p>需要指出的是，在原论文中，节点间通信遵循 Peer-to-Peer 的模式。而在实际 Deeplearning4j 的实现中，并没有采用这样的方案，而是根据实际节点的数量可配置 Plain Mode 和 Mesh Mode 两种模式。另外，梯度的阈值在实际实现的时候也被设计成可变的形式。</p>
<p>更多有关 Deeplearning4j 具体落地的方案可参考链接：</p>
<blockquote>
  <p><a href="https://deeplearning4j.org/docs/latest/deeplearning4j-scaleout-technicalref#asgd">https://deeplearning4j.org/docs/latest/deeplearning4j-scaleout-technicalref#asgd</a> </p>
</blockquote>
<p>限于篇幅就不再详细展开了。</p>
<p>我们需要指出的是，数据并行和模型并行是可以做成混合并行的解决方案。我们可以在模型并行的基础上使用部分数据训练分层后模型来达到混合并行的效果。或者也可以根据实际的网络情况，对部分网络采用数据并行，部分采用模型并行的方式。</p>
<p>目前 Deeplearning4j 支持的两种方案中，参数服务器的方案从 0.6.0 版本开始就已经支持，而去中心话的异步梯度更新机制则是在 1.0.0-beta 才开始支持，因此开发者使用的时候需要注意下版本。这两种方案有各自的优缺点，参数服务器在做同步参数更新的时候，不会存在延迟梯度数据的问题，但木板效应需要注意；而去中心化的异步梯度更新方案正好相反，由于采用了很多压缩的措施，使得通信效率大大提升，同时由于是异步的方案，因此更新机制更加灵活。</p>
<h3 id="133">13.3 小结</h3>
<p>本节课是 Deeplearning4j+Spark 应用介绍的上半部分内容，主要介绍了开源的分布式计算框架 Apache Spark 的相关信息以及 Deeplearning4j 在 Spark 上构建分布式神经网络模型的主要原理，即数据并行化的两种方式——参数服务器和去中心化的异步梯度更新机制。由于 Deeplearning4j 在 Spark 上建模的方式和一般的 Spark Job 没有本质的区别，因此我们在第一部分利用了一些篇幅给出了一个 Spark WordCount 的实例并做出了相关解释。Deeplearning4j 基于 Spark 建模的步骤也和 WordCount 的实例相似，具体建模实例会在下节课中给出。</p>
<p>另外值得说明的是，神经网络的并行或者分布式建模方案有很多可以选择，甚至可以将不同方案做整合后使用。Deeplearning4j 目前提供的只是对数据并行方案的支持，如果有对模型并行方案有需要的可以考虑自己进行二次开发或者直接提个 Issue 给官方开发团队。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="http://spark.apache.org/">Apache Spark 官网</a></li>
<li>异步梯度共享方案参考论文：<em><a href="http://nikkostrom.com/publications/interspeech2015/strom_interspeech2015.pdf">Scalable Distributed DNN Training Using Commodity GPU Cloud Computing</a></em></li>
<li><a href="https://deeplearning4j.org/docs/latest/deeplearning4j-scaleout-technicalref#asgd">更多的 Deeplearning4j 数据并行化策略具体落地方案</a> </li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>