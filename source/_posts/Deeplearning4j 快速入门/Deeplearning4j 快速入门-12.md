---
title: Deeplearning4j 快速入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一节课我们介绍了 Many-to-Many 在序列标注问题中的应用，在 RNN 部分的最后一节课中，我们来介绍另一种 Many-to-Many 的架构。本节课核心内容包括：</p>
<ul>
<li>基于 Many-to-Many 架构的机器翻译应用</li>
</ul>
<h3 id="101manytomany">10.1 基于 Many-to-Many 架构的机器翻译应用</h3>
<p>Many-to-Many 结构的输出具有一定的滞后性，常用于机器翻译、QA 问答模型之中。比较典型的就是 Sequence-to-Sequence。下面我们先看下这种架构的示意图：</p>
<p><img src="https://images.gitbook.cn/72d63c80-fc31-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>对比在第三部分介绍的 Many-to-Many 架构会发现，当前的这种架构的输出并非是从第一个 RNN Cell 开始，而是当整个序列输入完毕之后才开始预测第一个输出，并不断循环输出至最后。这种架构比较适合机器翻译的应用场景，下面我们就结合 seq2seq 来介绍如何基于 Deeplearning4j 来搭建这样的 RNN 架构。</p>
<p>首先我们看下建模的逻辑：</p>
<pre><code>public static ComputationGraphConfiguration getSMTModel(){
        ComputationGraphConfiguration configuration = new NeuralNetConfiguration.Builder()
            .regularization(true)
            .seed(123456L)
            .l2(0.0001)
            .weightInit(WeightInit.XAVIER)
            .learningRateScoreBasedDecayRate(0.5)
            .learningRate(learningrate)
            .updater(Updater.RMSPROP)
            .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
            .iterations(1)
            .graphBuilder()
            .addInputs("inputLine", "decoderInput")
            .setInputTypes(InputType.recurrent(VOCAB_ENCODER_SIZE), InputType.recurrent(VOCAB_DECODER_SIZE))
            //
            .addLayer("embeddingEncoder",new EmbeddingLayer.Builder().nIn(VOCAB_ENCODER_SIZE + 1).nOut(256).build(),"inputLine")
            .addLayer("encoder",new GravesLSTM.Builder().nIn(256).nOut(256).activation(Activation.SOFTSIGN).build(),"embeddingEncoder")
            .addVertex("thoughtVector", new LastTimeStepVertex("inputLine"), "encoder")
            .addVertex("dup", new DuplicateToTimeSeriesVertex("decoderInput"), "thoughtVector")
            //
            .addLayer("embeddingDecoder", new EmbeddingLayer.Builder().nIn(VOCAB_DECODER_SIZE + 1).nOut(256).activation(Activation.IDENTITY).build(),"decoderInput")
            .addVertex("embeddingDecoderSeq", new PreprocessorVertex(new FeedForwardToRnnPreProcessor()), "embeddingDecoder")
            //
            .addVertex("merge", new MergeVertex(), "embeddingDecoderSeq", "dup")
            .addLayer("decoder",new GravesLSTM.Builder().nIn(256 + 256).nOut(256).activation(Activation.SOFTSIGN).build(),"merge")
            .addLayer("output",new RnnOutputLayer.Builder().nIn(256).nOut(VOCAB_DECODER_SIZE + 1).activation(Activation.SOFTMAX).build(),"decoder")
            .setOutputs("output")
            .pretrain(false).backprop(true)
            .build();
        return configuration;
}
</code></pre>
<p>这个模型相对比较复杂，我们来解释下它的构成。首先配置的一些如 SGD、学习率等参数，和之前所有介绍的模型是一致的。模型的第一个部分是输入并编码的部分，我们使用了 Embedding + LSTM 的组合对输入进行编码。需要注意的是，紧接着在后面我们添加了两个存储中间状态的节点：lastTimeStep 和 duplicateTimeStep。</p>
<p>lastTimeStep 在网络结构上的作用可以将一个三维张量的数据转换成一个二维数据，目的是提取出最后一个 RNN Cell 的输出值。从物理含义上讲，最后一个 RNN Cell 的输出值是整个输入序列的语义表达。对于 seq2seq 来说，我们需要将整个输入序列的语义表达作为编码层的输入，从而预测下一个以及后面的输出。因此在提取完最后一个 Encoder 层的 RNN Cell 的输出值后，我们需要将数据通过复制的形式还原成三维的数据，也就是 duplicateTimeStep 的作用。</p>
<p>在 Decoder 层，我们将原始输入序列的语义结果和输出结果 Embedding 后的结果同时作为解码器的输入并输出解码后的结果。需要注意的是，在训练阶段，解码后的结果其实是作为其中一个“输入”使用的。而在预测阶段，也需要两个输入，即用户键入的待预测的序列和已经预测出来的结果序列，作为另一个输入来预测接下来的结果。</p>
<p>我们这里使用的是从英文翻译到法文的例子。因此建模中的命名也是根据这个问题场景而定制的。例如：“inEn”和“inFr”就分别代表英文和法文的输入。下面我们看下构建数据的逻辑。</p>
<pre><code>@Override
public MultiDataSet next(int num) {
       // 此处逻辑和 Many-to-One 部分类似，限于篇幅进行省略
       /*--------------------------------------*/
       // 这里有两个输入，分别代表翻译前后的序列，一个输出代表翻译后的序列
       // 第一个输入序列是由序列中词的下标构成
       // 第二个序列类似，但有一个单独的“go”符号作为起始标识位
       // 输出序列也是由词的索引构成，并带有“stop”这样的结束标识位
       // 以上序列都需要通过设置掩码来标识有效位置上的数据

       INDArray in1 = Nd4j.create(numExamples, 1, in1Length);  
       INDArray in1Mask = Nd4j.ones(numExamples, in1Length);   

       int[] arr1 = new int[3];
       int[] arr2 = new int[2];
       for (int i = 0; i &lt; numExamples; i++) {
           List&lt;VocabWord&gt; list = iter1List.get(i);
           arr1[0] = i;        // 张量的第一维标识语料的批次
           arr2[0] = i;

           int j = 0;                          // 词集中的词在序列中的位置
           for (VocabWord vw : list) {         // 遍历语料数据并将词的索引值进行填充
               arr1[2] = j++;
               in1.putScalar(arr1, vw.getIndex());
           }
           for (; j &lt; in1Length; j++) {
               arr2[1] = j;
               in1Mask.putScalar(arr2, 0.0);
           }
       }
       /* 和输入的第一个序列类似，不同之处在于：
       *1. 第二个输入序列的第一个元素是一个标识位，一般用一个较大的索引值标识，这里我直接用词集的 size 作为值
       *2. 掩码的最后一个元素是 1.0
       */
       INDArray in2 = Nd4j.create(numExamples, 1, in2Length + 1);
       INDArray in2Mask = Nd4j.ones(numExamples, in2Length + 1);
       for (int i = 0; i &lt; numExamples; i++) {
           List&lt;VocabWord&gt; list = iter2List.get(i);
           arr1[0] = i;
           arr2[0] = i;

           // 如上面注释所示，go 这个标识的实际值用词集的 size 填充
           arr1[2] = 0;
           in2.putScalar(arr1, vocabSize);

           int j = 1;
           for (VocabWord vw : list) {
               arr1[2] = j++;
               in2.putScalar(arr1, vw.getIndex());
           }
           for (; j &lt; in2Length; j++) {
               arr2[1] = j;
               in2Mask.putScalar(arr2, 0.0);
           }
       }

       // 输出序列只有一个，直接用 One-Hot 编码
       INDArray out = Nd4j.create(numExamples, vocabSize + 1, in2Length + 1);
       INDArray outMask = Nd4j.ones(numExamples, in2Length + 1);

       for (int i = 0; i &lt; numExamples; i++) {
           List&lt;VocabWord&gt; list = iter2List.get(i);
           arr1[0] = i;
           arr2[0] = i;

           int j = 0;
           for (VocabWord vw : list) {
               arr1[1] = vw.getIndex();
               arr1[2] = j++;
               out.putScalar(arr1, 1.0);   // One-Hot 编码
           }

           // 注意下最后的结束标识位，也就是上面注释中提到的 stop，这里也用词集的 size 作为值进行填充，当然也可以换作一个更大的值
           arr1[1] = vocabSize;
           arr1[2] = j++;
           out.putScalar(arr1, 1.0);

           for (; j &lt; in2Length; j++) {
               arr2[1] = j;
               outMask.putScalar(arr2, 0.0);
           }
       }

       INDArray[] inputs = new INDArray[]{in1, in2};
       INDArray[] inputMasks = new INDArray[]{in1Mask, in2Mask};
       INDArray[] labels = new INDArray[]{out};
       INDArray[] labelMasks = new INDArray[]{outMask};

       return new org.nd4j.linalg.dataset.MultiDataSet(inputs, labels, inputMasks, labelMasks);
}
</code></pre>
<p>首先我们需要明确在 seq2seq 的模型中，输入有两个。在当前翻译问题场景下，一个是英文序列，另一个是法文序列。在训练时，两个序列其实都是已知的，因此可以直接构建数据。当预测的时候，需要将英文序列预测出的法文序列和原始英文序列，同时作为输入的两个部分进行后续法文序列的结果，这个在上面已经讲述过类似的问题，就不再多描述了。</p>
<p>构建数据这部分的逻辑总体和前面是类似的，但是需要注意两个地方。</p>
<ul>
<li>第一，由于是有多个输入，因此需要用 MultiDataSet 来存储训练和标注数据。</li>
<li>第二，对于法文序列作为第二个输入，我们需要来标识它的起始和结束。这个我们先看下 <em>Sequence to Sequence Learning with Neural Network</em> 论文中的图：</li>
</ul>
<p><img src="https://images.gitbook.cn/3be90eb0-fa05-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>论文中使用 <code>&lt;EOS&gt;</code> 来标识预测序列的起始和结束位置的。在我们的逻辑里，使用 vocabSize 的具体值来代替。</p>
<p>训练的逻辑这里不再赘述了，和之前其他模型的训练过程是一样。我们直接看下准备的语料数据和预测结果。</p>
<p>英文语料：</p>
<p><img src="https://images.gitbook.cn/55810760-fa05-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>法文语料：</p>
<p><img src="https://images.gitbook.cn/6240bb30-fa05-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/739364a0-fa05-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><strong>我们预测的英文串是：</strong></p>
<blockquote>
  <p>Barack Obama becomes the fourth American president to receive the Nobel Peace Prize</p>
</blockquote>
<p><strong>最理想的法文翻译结果是：</strong></p>
<blockquote>
  <p>Barack Obama sera le quatrième président américain à recevoir le prix Nobel de la Paix</p>
</blockquote>
<p>在训练过程中，每次训练完一轮，我们都预测一下第一句的英文翻译结果。可以看到，在刚开始的几轮中，预测的结果比较混乱，重复的词很多，整个翻译的结果完全是上下文逻辑不通顺的。但随着进一步的优化，到 10 轮之后，翻译的结果开始合理，前后语句的逻辑关系也开始通顺。由于时间原因，我们没有做非常大规模的机器翻译的建模及最后 BLEU 值的评估。有兴趣的读者可以自行下载开源数据集进行验证和模型进一步地调优。</p>
<p>本节课的 Many-to-Many 的框架和上一节课的框架，最重要的不同点在于，是否等待整个序列输入完毕后再输出。事实上，上节课的序列标注问题同样可以用本节课的框架来做，理论上会有更好的效果。但毫无疑问，本节课框架的实现难度和复杂度都要高于前面的三个框架，因此实际应用中我们可以分别作为 Baseline 来预研，最后看调优的结果再来决定究竟使用什么样的框架。</p>
<h3 id="102">10.2 小结</h3>
<p>这里对本次 RNN 部分的课程内容进行一个总结。</p>
<p>RNN 系列课程主要介绍了，如何基于 Deeplearning4j 提供的 RNN 结构（主要是 LSTM 结构），进行文本分类、文本生成、文本序列标注和机器翻译这些经典的 NLP 任务。由于时间的原因，部分应用没有在大规模语料场景下进行建模，但模型结构及构建的思路是一样的。</p>
<p>RNN 网络相比于先前的 CNN 网络更擅长于序列问题的处理，当然序列不仅限于文本。但 RNN 相对于 CNN 来说也有一些缺点，例如预测时间较长、并行困难等。所以上述的很多应用基本都有 CNN 的版本，有兴趣的读者可以自行尝试。但 RNN 网络对于深度学习开发者来讲，依然是必须了解和掌握的一种结构。</p>
<p>另外需要指出的是，在上述所有的 RNN 架构中，我们都可以尝试加入注意力模型（Attention）的机制，来进一步优化整个模型的预测效果。Attention 与 RNN 的结合可以较好地解决 LSTM 在长序列问题上信息遗失的问题。Deeplearning4j 目前还没有将 Attention 模型添加到主分支当中，但可以使用第三方开源的实现来补充，下图就是一个建模实例：</p>
<p><img src="https://images.gitbook.cn/059a4e10-0e72-11e9-9e38-15a2a3c596fe" alt="enter image description here" /></p>
<p>具体使用可以参考链接：<a href="https://github.com/treo/dl4j_attention">https://github.com/treo/dl4j_attention</a></p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>