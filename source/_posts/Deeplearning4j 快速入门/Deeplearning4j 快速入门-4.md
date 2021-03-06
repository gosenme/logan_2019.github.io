---
title: Deeplearning4j 快速入门-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面的课程介绍了在 Windows、Mac OS X 和 Linux 系统下，Deeplearning4j 开发环境的搭建。在此基础上，我们将进一步介绍 Deeplearning4j 开发的基本流程。本节课核心内容包括：</p>
<ul>
<li>单 CPU 环境</li>
<li>多 CPU 环境</li>
<li>分布式 Spark 环境</li>
</ul>
<p>对于机器学习应用来说，数据预处理、模型的训练和验证、模型的部署上线是几个标准的流程，Deeplearning4j 框架的开发流程同样遵循这几个步骤。由于 Deeplearning4j 本身支持在 CPU/GPU 环境下的单机/并行/分布式建模，并且在不同环境下建模的细节略有不同，因此本次课程将着重介绍在单 CPU、多 CPU 及 Spark 集群上建模的步骤。至于在 GPU 环境的开发细节，将在后续课程中单独进行介绍。 </p>
<h3 id="21cpu">2.1 单 CPU 环境</h3>
<p>单 CPU 环境常常用于原型验证，尤其对于 Deeplearning4j 来讲，在单 CPU 环境下验证通过后的逻辑可以很方便地移植到其他环境中。下面我们分四个环节介绍在单 CPU 环境下的建模步骤。</p>
<h4 id="211">2.1.1 构建训练数据</h4>
<p>数据集的构建是建模的基础。Deeplearning4j 用内置类：DataSet 对训练数据进行封装（PS：DataSet 对象不仅可以封装单条训练数据，也可以封装一个 Mini-batch 的训练数据）。每一次迭代其实是用一个 DataSet 去更新神经网络中的参数。因此在 Deeplearning4j 中构建训练数据集的最终目的是生成一个 DataSet 迭代器或者 DataSet 序列。  </p>
<p>首先使用 Deeplearning4j 中的子项目：DataVec 来构建 DataSetIterator。训练用例是鸢尾花分类问题的开源数据集，<a href="http://archive.ics.uci.edu/ml/datasets/Iris" title="IrisDataSet">具体详见这里</a>。 </p>
<pre><code>public static DataSetIterator loadIrisIter(File file) throws IOException, InterruptedException {

     RecordReader recordReader = new CSVRecordReader();
     recordReader.initialize(new FileSplit(file));
     DataSetIterator iterator = new RecordReaderDataSetIterator(recordReader, batchSize, labelColIndex, numClasses);

     return iterator;
}
</code></pre>
<p>这里对上述代码做下说明。batchSize 是每个批次的训练数据大小。labelColIndex 是“指定 CSV 文件中第几列是标注”。numClasses 是分类的类别数目。</p>
<blockquote>
  <p>需要注意的是，鸢尾花的原始数据集中的标注使用的是文字，事先我已经替换为数字，否则程序会报错。</p>
</blockquote>
<p>另外，我们也可以直接使用 CSVRecordReader 读取训练数据。除了 CSVRecordReader，DataVec 项目中还提供了许多有用的实现：</p>
<p><img src="https://images.gitbook.cn/33b06ef0-f389-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p>构建 DataSetIterator 是 Deeplearning4j 官网推荐的用法，即通过构建 RecordReader 和 DataSetIterator 来生成训练数据。但其实也可以不依赖 DataVec，自行构建 DataSet 序列。具体示例如下：</p>
<pre><code>public static List&lt;DataSet&gt; loadIrisSeq(File file) throws IOException {
     BufferedReader br = new BufferedReader(new FileReader(file));
     String line = null;
     List&lt;DataSet&gt; trainDataSetList = new LinkedList&lt;DataSet&gt;();
     while( (line = br.readLine()) != null ){
          String[] token = line.split(",");
          double[] featureArray = new double[token.length - 1];
          double[] labelArray = new double[numClasses];
          for( int i = 0; i &lt; token.length - 1; ++i ){
              featureArray[i] = Double.parseDouble(token[i]);
          }
          labelArray[Integer.parseInt(token[token.length - 1])] = 1.0;
          //
          INDArray featureNDArray = Nd4j.create(featureArray);
          INDArray labelNDArray = Nd4j.create(labelArray);
          trainDataSetList.add(new DataSet(featureNDArray, labelNDArray));
     }
     br.close();
     return trainDataSetList;
}
</code></pre>
<p>以上是通过调用 Java 的原生态接口生成的训练数据。需要注意的是，上述例子中一个 DataSet 对象里只封装了一条训练数据。如果直接把生成的 DataSet 序列喂给模型，相当于 Mini-batch 等于 1。如果需要进一步处理成任意大小的 Mini-batch 的形式，可以做如下处理：  </p>
<pre><code>public static List&lt;DataSet&gt; merge(List&lt;DataSet&gt; seq, int batchSize){
     int count = 0;
     List&lt;DataSet&gt; miniBatchSeq = new LinkedList&lt;DataSet&gt;();
     List&lt;DataSet&gt; tempSeq = new LinkedList&lt;DataSet&gt;();
     for( DataSet ds : seq ){
         if( count == batchSize ){
             miniBatchSeq.add(DataSet.merge(tempSeq));
             tempSeq.clear();
             count = 0;
         }
         tempSeq.add(ds);
         ++count;
     }
     if( !tempSeq.isEmpty() ){
         miniBatchSeq.add(DataSet.merge(tempSeq));
     }
     return miniBatchSeq;
}
</code></pre>
<p>经过上述逻辑的处理，DataSet 序列中对象将包含一组 Mini-batch 的数据。虽然使用 Java 原生接口要比直接使用 DataVec 中的工具类来得繁琐一些，但更符合普通 Java 开发者的习惯。</p>
<h4 id="212">2.1.2 超参数的配置</h4>
<p>比如，我们配置如下图的全连接神经网络：</p>
<p><img src="https://images.gitbook.cn/6399d470-fc27-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>从图中可以看到，这是一个仅含有一层隐藏层的全连接神经网络，其中输入层有三个神经元，隐藏层含有四个神经元，输出层有两个神经元。我们用 Deeplearning4j 中的 MultiLayerConfiguration 对这类可以明确分层的神经网络进行建模：  </p>
<pre><code>public static MultiLayerNetwork model(){
     MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                     .seed(12345)
                     .iterations(1)
                     .learningRate(0.01)
                     .weightInit(WeightInit.XAVIER)
                     .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                     .updater(Updater.ADAM)
                     .list()
                     .layer(0, new DenseLayer.Builder().activation(Activation.RELU)
                         .nIn(3).nOut(4).build())
                     .layer(1, new OutputLayer.Builder(LossFunctions.LossFunction.MCXENT)
                              .activation(Activation.SOFTMAX)
                         .nIn(4).nOut(2).build())
                     .backprop(true).pretrain(false);
     MultiLayerConfiguration conf = builder.build();
     MultiLayerNetwork model = new MultiLayerNetwork(conf);
     return model;      
}
</code></pre>
<p>以上逻辑定义了一个和截图中结构相吻合的全连接神经网络。此外，我们还定义了很多超参数，如学习率、参数的初始分布、优化算法及优化器、激活函数，默认使用 BP 反向传播算法等。这些超参数对最后网络参数的收敛有直接影响，具体在后续的课程中会有详细讨论，这里不再赘述。 </p>
<h4 id="213">2.1.3 训练和保存模型</h4>
<p>对于这一部分，我们先来看下具体的逻辑：  </p>
<pre><code>MultiLayerNetwork mlp = model();
        mlp.setListeners(new ScoreIterationListener(1));    //损失函数监听器
        for( int i = 0; i &lt; 20; ++i ){    //训练 20 轮
            mlp.fit(iter);
            iter.reset();
            Evaluation eval = mlp.evaluate(iter);
            System.out.println(eval.stats());
            iter.reset();
        }
ModelSerializer.writeModel(mlp, new File("mlp.mod"), true);    //保存模型
</code></pre>
<p>在前两个步骤的基础上，可以获取一个初始化好的模型以及一组训练数据。为了观察损失函数的收敛情况，我们设置一下监听器：参数“1”表示每经过一次迭代，就记录当前损失函数的值。最后，设置了训练的总轮次（这里设置了 20 个 Epoch），并循环训练完所有的轮次。在每一轮次训练完后，评估下模型（这里因为不涉及具体的应用，因此直接拿训练数据评估模型，这在实际中没有太大意义，在这里仅仅作为参考）。在完成全部的训练后，保存模型到一个普通文件中。  </p>
<h4 id="214">2.1.4 加载并使用模型</h4>
<p>这部分的逻辑比较简单，重新加载模型并调用相关接口进行数据预测：    </p>
<pre><code>public static void loadModelAndPredict(INDArray feature) throws IOException{
        MultiLayerNetwork reloadModel = ModelSerializer.restoreMultiLayerNetwork(new File("mlp.mod"));
        reloadModel.predict(feature);
}
</code></pre>
<p>需要注意的是，predict/output 接口的入参可以是一个 DataSet 对象，也可以是一个 NDArray 形式的张量对象。</p>
<h3 id="22cpu">2.2 多 CPU 环境</h3>
<p>多 CPU 环境可以选择并行建模（当然也完全兼容上述的单机环境训练）。多 CPU 环境下的读取数据、模型的配置和最后模型的保存都可以参考单 CPU 环境的做法，不同的地方在于训练的过程中我们需要借助于参数服务器，下面具体看下逻辑。</p>
<p><strong>“构建训练数据”和“超参数的配置”请参考上面的内容，这里不再赘述。</strong></p>
<h4 id="221">2.2.1 训练和保存模型</h4>
<p>假设我们已经构建了数据集并配置了神经网络的超参数，并且需要并行训练模型，则添加以下逻辑：</p>
<pre><code>ParallelWrapper wrapper = new ParallelWrapper.Builder(model)
                        .prefetchBuffer(prefetchSize)
                        .workers(workers)
                        .averagingFrequency(averagingFrequency)
                        .reportScoreAfterAveraging(reportScore)
                        .useLegacyAveraging(legacyAveraging)
                        .build();
    for( int i = 0; i &lt; totalEpoch; ++i ){
        wrapper.fit(trainIter);
        trainIter.reset();
}
</code></pre>
<ul>
<li>ParallelWrapper 是数据并行化的封装类，支持在多 CPU/GPU 环境下进行并行建模。</li>
<li>ParallelWrapper 的主要工作是，将由各个线程针对各自数据分片计算出来的模型参数进行聚合处理，并将平均的结果更新到每个线程持有的模型参数，以此来完成参数的一次迭代。</li>
<li>ParallelWrapper 可以指定一些参数来优化迭代过程。比如，averagingFrequency 表示参数更新的频率，即多少次迭代后进行参数的平均；workers 表示工作的节点/线程数量。一般情况下，workers 的数量、prefetchBuffer 参数中预先存取的训练数据量，可以参考硬件的数量配置成一定比例。</li>
</ul>
<p>在生成 ParallelWrapper 的实例后，我们把训练数据喂到该实例中进行模型的训练。这部分和单 CPU 训练的逻辑类似。</p>
<p>最后，保存模型的逻辑也和单 CPU 的一致（需要注意的是，ParallelWrapper 持有的是神经网络模型的实例对象，更新的也是其中的参数，因此可以直接保存）。</p>
<p><strong>“加载并使用模型”请参考上面的内容，这里不再赘述。</strong></p>
<h4 id="222cpu">2.2.2 多 CPU 环境建模小结</h4>
<p>简单小结一下多 CPU 环境下的建模流程。目前多（核）CPU 具备更强的调度多线程的能力，因此利用硬件资源加快建模速度是一种高效可行的方案。Deeplearning4j 提供了数据并行化的工具类并且做了高度封装，用户只需要配置若干参数，就可以对模型进行并行建模。</p>
<h3 id="23spark">2.3 分布式 Spark 环境</h3>
<p>以上的第一、二部分都是围绕单机场景下的模型开发流程。由于单机的存储和计算能力有限，因此可以选择分布式集群计算框架扩展其建模能力，这个部分我们介绍基于 Apache Spark 的 Deeplearning4j 的建模流程。</p>
<p><a href="http://spark.apache.org/">Apache Spark</a> 是优秀的分布式计算框架，相比于 Hadoop 等上一代处理框架，Spark 提出的弹性分布式数据集（Resilient Distributed Datasets，RDD）可以高效地实现数据的共享，大大提高了迭代计算的效率。</p>
<p>Deeplearning4j 支持在 Spark 框架上进行分布式神经网络的建模。和本地多 CPU/GPU 类似，在 Spark 上的分布式建模需要构建数据并行化的实例，即参数服务器。</p>
<p>下面简要介绍下在 Spark 上建模的流程（PS：笔者所在的工作环境采用的是 Spark on Yarn 的部署模式，运行模式是 Yarn Cluster）。</p>
<h4 id="231">2.3.1 构建训练数据</h4>
<p>首先和所有的 Spark 应用一样，声明 Spark 上下文并配置相应的用户信息：</p>
<pre><code>SparkConf conf = new SparkConf()
               .set("spark.kryo.registrator", "org.nd4j.Nd4jRegistrator")  //ND4J 实例注册 Kryo 序列化
               .setAppName("Spark DL");
JavaSparkContext jsc = new JavaSparkContext(conf);
</code></pre>
<p>需要注意的是，我们为 ND4J 注册了 Kryo 的序列化方式。由于 Kryo 序列化算法比 Java 原生态序列化方式要高效得多，因此在 0.7.0 版本后，Deeplearning4j 会强制要求使用 Kryo 序列化方式，否则会报错。</p>
<p>接下来，构建训练和测试数据集：</p>
<pre><code>final String trainPath = "hdfs://..."
final String testPath = "hdfs://..."
//
JavaRDD&lt;DataSet&gt; javaRDDTrain = jsc.objectFile(trainPath); 
JavaRDD&lt;DataSet&gt; javaRDDTest = jsc.objectFile(testPath); 
</code></pre>
<p>这里构建训练和验证数据集的逻辑比较简单。假设在 HDFS 上已经存储了序列化好的 <code>JavaRDD&lt;DataSet&gt;</code> 对象，则可以直接用 JavaSparkContext 的接口 .objectFile 来进行反序列化。对于存储在其他数据源中的数据，则需要通过一系列的处理构建数据集，相应地会复杂一些。但最终我们的目标依然是构建 DataSet 的 JavaRDD 对象。</p>
<p><strong>“超参数的配置”请参考上面的内容，这里不再赘述。</strong></p>
<h4 id="232">2.3.2 训练和保存模型</h4>
<p>相比较于本地建模，在 Spark 上训练模型需要构建参数服务器和模型的 Spark 包装实例。我们先来看下以下具体的逻辑：</p>
<pre><code>//声明参数服务器
ParameterAveragingTrainingMaster trainMaster = new ParameterAveragingTrainingMaster.Builder(numBatch)   //weight average service
                .workerPrefetchNumBatches(0)
                .saveUpdater(true)
                .averagingFrequency(5)
                .batchSizePerWorker(numBatch)
                .build();
        //构建模型的 Spark 实例
        SparkDl4jMultiLayer sparkNetwork = new SparkDl4jMultiLayer(jsc, net, trainMaster);
        //Spark 上训练模型
for( int i = 0; i &lt; numEpochs; ++i ){
     sparkNetwork.fit(javaRDDTrain);
     Evaluation evalActual = sparkNetwork.evaluate(javaRDDTest);
     System.out.println(evalActual.stats());
}
</code></pre>
<p>参数服务器和本地并行建模的 ParallelWrapper 类似，都是基于数据并行化的工具类，将该工具类实例化并配置相应参数之后即可获取该实例对象。接着，需要声明模型配置信息的 Spark 实例对象，这里使用的是 SparkDl4jMultiLayer。SparkDl4jMultiLayer 是对 MultiLayerConfiguration 和 MultiLayerNetwork 的封装，主要用于保存模型的配置和相关参数。之后，只需要把训练数据喂给模型的 Spark 实例对象就可以了。</p>
<p>最后采用以下逻辑将模型保存到 HDFS 上：</p>
<pre><code>FileSystem hdfs = FileSystem.get(jsc.hadoopConfiguration());
Path hdfsPath = new Path(modelPath);
FSDataOutputStream outputStream = hdfs.create(hdfsPath);
MultiLayerNetwork trainedNet = sparkNetwork.getNetwork();
ModelSerializer.writeModel(trainedNet, outputStream, true);
</code></pre>
<p><strong>“加载并使用模型”请参考上面的内容，这里不再赘述。</strong></p>
<p>这一部分的应用和 Spark 平台已经基本解耦了。如果需要在集群上预测，那么从 HDFS 上加载模型及其参数即可；如果需要将模型移植到其他平台上进行预测的工作，则和一般本地单机的使用是一样的，这里就不再详述了。</p>
<h4 id="233spark">2.3.3 分布式 Spark 环境建模小结</h4>
<p>以上第三部分是基于 Spark 进行分布式建模的基本例子。和单机建模的差别在于，我们的数据是存储在 RDD 中的。因此在构建数据集的时候，需要从某个数据源（如 HDFS/HBase/Hive）构建 RDD 的实例对象。在实例中，我们直接从 HDFS 上反序列化 RDD 对象，但在实际的应用中，往往需要做更为复杂的预处理工作。另外，参数服务器的声明也是必需的。至于参数服务器的配置信息，可以<a href="https://deeplearning4j.org/docs/latest/deeplearning4j-scaleout-parameter-server">参考官网的文档</a>，里面有更为详细的描述。由于 Deeplearning4j 依赖的张量计算库 ND4J 大量使用了堆外内存，因此在 Spark 上训练的时候需要针对内存的使用进行调优，这在后面专门介绍 Spark 使用的课程中会进行讨论。</p>
<h3 id="24">2.4 小结</h3>
<p>下面对本次课程做一下总结，基于 Deeplearning4j 框架的开发流程大致可以分为四个步骤：</p>
<ol>
<li>构建训练数据（可依赖 DataVec）到内存/显存；</li>
<li>配置模型以及超参数，生成 Layer-Based 的模型实例；</li>
<li>训练并保存模型；</li>
<li>加载并使用模型。</li>
</ol>
<p>在不同开发环境下，主要的不同点在于数据处理、并行建模中参数服务器的实例声明这两个部分。尤其在 Spark 分布式计算环境下，我们需要加载数据到 RDD 中。在上述的建模过程中，我们并没有强调在 GPU 环境下的建模，这在后面的一节课程会有详细的介绍。另外需要注意的是，Deeplearning4j 在集群上进行分布式训练是需要依赖 Spark 框架的，Deeplearning4j 本身并不支持分布式计算，而对于希望使用 GPU 集群的开发人员来讲，除了需要依赖 Spark 以外，还需要 Node Label 技术的支持。</p>
<p>具体来说，如果 Spark 集群是一个异构计算框架（CPU + GPU），则需要通过 Node Label 技术将模型训练指定到那些拥有 GPU 的机器上，更多详细信息可以参考社区资料，<a href="https://deeplearning4j.org/spark#yarngpus">详见这里</a>。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="http://archive.ics.uci.edu/ml/datasets/Iris" title="IrisDataSet">鸢尾花分类问题的开源数据集</a></li>
<li><a href="http://spark.apache.org/">Apache Spark</a> </li>
<li><a href="https://deeplearning4j.org/docs/latest/deeplearning4j-scaleout-parameter-server">Spark 官网文档：参数服务器的配置信息</a></li>
<li><a href="https://deeplearning4j.org/spark#yarngpus">Deeplearning4j 社区：Spark 支持详细资料</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>