---
title: Deeplearning4j 快速入门-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在之前的课程中，我们为大家先后介绍了 MLP、DBN、CNN、RNN 等网络结构的建模，我们的网络输入也从结构化数据拓展到图片、文本等复杂的非结构化数据。其实现实应用中的很多问题，往往不会从单一维度进行建模，很多时候我们需要同时考虑视觉、听觉等多维度的信息特征甚至基于这些信息同时完成多个目标的学习，而非单一目标。这些应用场景相对于之前我们介绍的问题会复杂一些，使用 Deeplearning4j 落地的时候会使用到一些相对高级的特性，这里我们就集中对部分高级特性做一些介绍。本节课核心内容包括：</p>
<ul>
<li>多模态（Multi-modal）建模</li>
<li>多任务（Multi-task）建模</li>
</ul>
<h3 id="201multimodal">20.1 多模态（Multi-modal）建模</h3>
<p>在本课的引言中我们谈到的视觉、听觉等都可以认为是一种独立的模态。当然模态的定义可以有很多不同的理解，比如信息采集的来源不同我们也可以认为是两种独立的模态。作为信息的载体，图像、文字等同样可以认为是不同的模态。在这个部分中，我们为大家介绍同时基于文本和图像的分类问题的建模。</p>
<p>之前的课程我们也介绍了很多的分类问题，如：图像和文本的分类。当然从模态的角度去看，之前的分类问题都是单模态的建模，输入全部都是图像或者文本。很多时候，单模态的建模虽然也会达到一定的应用效果，但是毫无疑问地，有用信息越多对于目标的优化肯定越有利，因此多模态的建模就变得非常有意义了。我们首先看下面这张图：</p>
<p><img src="https://images.gitbook.cn/3122f6f0-55d9-11e9-8bca-0bef6cecda97" alt="enter image description here" /></p>
<p>从图中可以看到，从图片或者文字单一模态我们已经可以在一定程度上解决商品类目预测的问题，但是如果可以将两者结合，具体来说就是将图片和文字同时作为网络的两个输入，那么对于该问题的优化效果可能会得到进一步的提升，分类的准确性可能会提高。我们在这里给出建模的网络结构：</p>
<pre><code>private static ComputationGraph getModel(final int VOCAB_SIZE){
    ComputationGraphConfiguration conf = new NeuralNetConfiguration.Builder()
                .updater(Updater.ADAM)
                .graphBuilder()
                .addInputs("input1", "input2")
                .addLayer("embedding", new EmbeddingLayer.Builder()
                                              .nIn(VOCAB_SIZE+1)
                                              .nOut(128)
                                              .activation(Activation.IDENTITY)
                                              .build(),"input1")
                .addLayer("encoder", new GravesLSTM.Builder()
                                            .nIn(128)
                                            .nOut(128)
                                            .activation(Activation.SOFTSIGN)
                                            .build(),"embedding")
                .addLayer("L1", new DenseLayer.Builder().nOut(64).build(), "encoder")
                //
                .addLayer("conv", new ConvolutionLayer.Builder(5, 5)
                                .nIn(3)
                                .stride(3, 3)
                                .nOut(32)
                                .activation(Activation.LEAKYRELU)
                                .build(),"input2")
                .addLayer("pooling", new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
                                .kernelSize(2,2)
                                .stride(2,2)
                                .activation(Activation.IDENTITY)
                                .build(),"conv")
                .addLayer("L2", new DenseLayer.Builder().nOut(64).build(), "pooling")
                .addVertex("merge", new MergeVertex(), "L1", "L2")
                .addLayer("out", new OutputLayer.Builder().nIn(64 + 64).nOut(3).build(), "merge")
                .inputPreProcessor("L1", new RnnToFeedForwardPreProcessor())
                .inputPreProcessor("L2", new CnnToFeedForwardPreProcessor(8, 8, 32))
                .setInputTypes(InputType.recurrent(VOCAB_SIZE + 1), InputType.convolutionalFlat(50, 50, 3))
                .setOutputs("out")
                .build();
    return new ComputationGraph(conf);
}
</code></pre>
<p>我们来看下上面给出的多模态建模的网络结构。首先我们需要使用 ComputationGraph 来容纳多个输入，也就是 .addInputs (“input1”, “input2”) 中的 input1 和 input2。具体来说，input1 是商品的文本信息，input2 是商品的图片信息。对于文本信息，我们通过 embedding+lstm 的结构来抽取相关的特征，而对于图片我们则用标准的 conv+pooling 结构来提取图片的 high-level 特征。为了方便将文本和图片的特征进行 merge，我们需要在提取高维抽象特征后接一个全连接网络层将特征进行平展并且在 .addVertex (“merge”, new MergeVertex (), “L1”, “L2”) 这个 merge 层进行特征的拼接。拼接后的组合特征其实是文本和图像的高维特征组合，我们以组合特征作为分类的基础特征后接一个全连接层进行多分类。到此基于文本和图片的多模态分类建模网络就搭建完成了。下面是 UI 页面的示意图：</p>
<p><img src="https://images.gitbook.cn/40a79720-55d9-11e9-92da-05f89e75a7eb" alt="enter image description here" /></p>
<p>从 UI 图中我们可以更加清晰地看到图像和文本同时作为两个输入。
最后我们给出训练数据的处理过程。</p>
<pre><code>    final int VOCAB_SIZE = 10;
    ComputationGraph network = getModel(VOCAB_SIZE);
    //
    final String fileName = "手电筒.jpg";
    File file = new File(fileName);
    NativeImageLoader imageLoader = new NativeImageLoader(50, 50, 3);
    INDArray imageFeature = imageLoader.asRowVector(file);  //图像特征
    //
    final String word = StringUtils.split(fileName, ".")[0];
    INDArray inEmbedding = Nd4j.create(1, 1, 1);
    inEmbedding.putScalar(new int[]{0, 0, 0}, wordIndex.get(word));           //文本特征
    //
    double[] labelArray = new double[]{0.0,1.0,0.0};
    INDArray label = Nd4j.create(labelArray);               //标注
    //UI 配置
    UIServer uiServer = UIServer.getInstance();
    StatsStorage statsStorage = new InMemoryStatsStorage();
    uiServer.attach(statsStorage);
    network.setListeners(new StatsListener(statsStorage));
    //
    //模型训练
    network.fit(new INDArray[]{inEmbedding,imageFeature}, new INDArray[]{label} );
</code></pre>
<p>这部分的逻辑主要集中在图像和文本的特征数据的准备上。我们以图片文件的名称作为该图片的文本信息，图片本身的像素矩阵作为神经网络输入的原始信息。同之前课程中介绍的读取图片文件的方式类似，我们使用 NativeImageLoader 工具实例读取图片文件。同时将图片文件的文件名称在 wordIndex 映射中找到对应词的索引并生成文本特征向量。标注信息在这里是我们自己定义的，并不代表在某种具体的场景中使用。最后是 UI 配置和模型训练的逻辑。需要注意的是，由于我们的输出是多个，因此需要将之前生成好的图片和文本的特征向量放在 INDArray 数组中共同作为输入。</p>
<p>以上便是基于图像和文本多模态建模的基本过程。</p>
<h3 id="202multitask">20.2 多任务（Multi-task）建模</h3>
<p>我们在之前介绍的一些问题中，不管输入有几个，优化的目标始终都是只有一个。从优化目标的数量来说，这些都是单任务的建模，而相对地，我们可以同时优化多个目标，也就是所谓的多任务学习。有别于单任务学习，多任务学习的过程中特征空间其实是共享的而非独立的，换句话说，如果需要优化的多个目标之间具有比较高的关联性，同时优化这些目标所得到的特征空间将是通用的。从这个意义上讲，多任务优化出来的特征空间将会有更好的泛化能力。我们来看下多任务的示意图：</p>
<p><img src="https://images.gitbook.cn/4bec43b0-55d9-11e9-bfba-c73f51f2799b" alt="enter image description here" /></p>
<p>示意图中的网络结构仅含有一个输入（也可以修改成我们上述的多个输入或者多模态的输入）但是含有多个输出。这就是多任务建模的基本示意图。下面我们给出多任务的一个建模实例。</p>
<pre><code> private static ComputationGraph getMultiTaskModel(){
    ComputationGraphConfiguration conf = new NeuralNetConfiguration.Builder()
                    .updater(Updater.ADAM)
                    .graphBuilder()
                    .addInputs("input")
                    .addLayer("dense-1", new DenseLayer.Builder().nIn(3).nOut(4).build(), "input")
                    .addLayer("dense-2", new DenseLayer.Builder().nIn(4).nOut(4).build(), "dense-1")
                    .addLayer("out1", new OutputLayer.Builder()
                            .lossFunction(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                            .nIn(4).nOut(2).build(), "dense-2")
                    .addLayer("out2", new OutputLayer.Builder()
                            .lossFunction(LossFunctions.LossFunction.MSE)
                            .nIn(4).nOut(1).build(), "dense-2")
                    .setOutputs("out1","out2")
                    .build();
    return new ComputationGraph(conf);
}
</code></pre>
<p><img src="https://images.gitbook.cn/7f955cb0-55d9-11e9-bfba-c73f51f2799b" alt="enter image description here" /></p>
<p>上面的逻辑中输入这块比较容易理解，就是一个全连接层的结构并且是一个输入层为 3 个神经元的结构。我们重点看下输出这块。名称为 out1 的是第一个输出层，其损失函数是交差熵。名称为 out2 的是第二个输出层，损失函数是均方误差。该网络同时优化两个损失函数，从实际物理含义上讲，我们在同时优化一个分类问题和一个回归问题。当然在理论上我们可以同时优化任意多个的目标函数，但实际的场景中同时优化两个目标函数可能是最为常见的。比如在推荐算法领域，我们可以同时优化 CTR 和 CVR 两个指标就可以借助这种多任务的神经网络结构来实现。从 Deeplearning4j 自带的 UI 页面上，我们也可以清楚地看到整个网络的结构是带有两个输出的。最后我们给出数据预处理部分的逻辑供大家参考：</p>
<pre><code>    double[][] features = new double[][]{{0.9,0.7,0.6},{0.9,0.7,0.6},{0.9,0.7,0.6},{0.9,0.7,0.6}};
    double[][] labels1 = new double[][]{{1.0,0.0},{0.0,1.0},{1.0,0.0},{0.0,1.0}};
    double[][] labels2 = new double[][]{{0.8},{0.8},{0.8},{0.8}};
    //
    INDArray featuresND = Nd4j.create(features);
    INDArray labelND1 = Nd4j.create(labels1);
    INDArray labelND2 = Nd4j.create(labels2);
    //...
    //训练部分
    model.fit(new INDArray[]{featuresND}, new INDArray[]{labelND1, labelND2});
</code></pre>
<p>我们简单解释下这部分的逻辑。</p>
<p>首先这些数据都是伪造的并非某个具体场景下的真实数据。我们的目的是验证在多任务场景下训练数据的格式是否正确。从上述逻辑中可以看出，我们共有 4 条训练数据，由于输入层包含有 3 个神经元，所以每条记录就含有三个浮点数值作为输入的特征。到目前位置和我们之前在讲述多层感知机课程中的相关内容是一样的。我们重点来看下输出这部分的数据准备。由于具有两个输出，第一个输出含有两个神经元，因此 labels1 这个二维数组中的每条记录都将包含两个元素。同理 labels2 中每条记录只包含一个元素对应 out2 这一层网络的输出神经元只有一个。</p>
<p>接着，我们将原始的二维数组的格式通过 ND4J 工具类转换成 NDArray 的对象形式。请注意，在训练部分由于是具有两个输出，因此需要声明一个 INDArray 数组将两者进行封装。那么到此，基本的训练数据和训练逻辑就是这样。在真实场景下，数据的存储可以千变万化，但是最终的形式和我们这个简单的例子是一致的，大家可以作为基本案例进行使用。</p>
<h3 id="203">20.3 小结</h3>
<p>在本次课程中，我们为大家介绍了如何基于 DL4j 进行多模态和多任务建模的方式。在之前的课程中我们大多使用的都是 MultiLayerNetwork 来建模，这对于单模态输入的模型或者单一优化目标的任务来说已经可以比较好的支持，但是对于诸如多模态或者多任务的问题来说，图结构的神经网络是更为合适的，因此在本次课程的实例中我们全部采用的是 ComputationGraph 来建模。</p>
<p>多模态和多任务的场景在实际应用中不如单一模态和单一目标优化那么得多，但是这两种建模方式可以作为提升模型效果的手段加以探索和利用。尤其对于情感识别等需要从多维度综合建模的问题而言，多模态将会是一种比较常见的建模手段。对于多任务问题而言，相比于单一任务它可以得到一组泛化能力较好的模型参数。从本质上说，由于需要同时考虑或者说优化多个目标，那么陷入单一目标的局部极值点的问题将会得到有效缓解，这也是提升泛化能力的一个主要原因。当然需要指出的是，多任务由于是共享特征空间的，因此被同时优化的几个任务需要保持一定的关联性，否则最终模型将很难收敛。</p>
<p>除了上述介绍的这些特性以外，Deeplearning4j 还支持自定义网络结构、激活函数和损失函数等。这些特性在实际开发中用得较少，但是对于希望复现最新成果的开发人员来说是非常有用的。在 Deeplearning4j 的 GitHub 主页的例子中已经给出了以上三种特性实现的具体案例，这里我们就不再详细介绍了，有需要的同学可以到相关主页上去参考。</p>
<ul>
<li><a href="https://github.com/deeplearning4j/dl4j-examples/tree/master/dl4j-examples/src/main/java/org/deeplearning4j/examples/misc/activationfunctions">自定义激活函数</a></li>
<li><a href="https://github.com/deeplearning4j/dl4j-examples/tree/master/dl4j-examples/src/main/java/org/deeplearning4j/examples/misc/customlayers">自定义网络结构</a></li>
<li><a href="https://github.com/deeplearning4j/dl4j-examples/tree/master/dl4j-examples/src/main/java/org/deeplearning4j/examples/misc/lossfunctions">自定义损失函数</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>