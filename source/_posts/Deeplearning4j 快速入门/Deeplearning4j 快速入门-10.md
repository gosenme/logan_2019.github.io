---
title: Deeplearning4j 快速入门-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一节课的内容中，我们介绍了循环神经网络（Recurrent Neural Network）的相关内容，并根据 Many-to-One 的结构给出了基于 Deeplearning4j 的文本分类实例。本节课核心内容包括：</p>
<ul>
<li>基于 One-to-Many 架构的文本生成应用</li>
</ul>
<p>在本次的课程中，我们将介绍另外一种结构：One-to-Many，并且我们将基于这种结构给出文本自动生成的例子。下面我就将文本生成的相关背景知识及具体的建模工作做下介绍，和上一次课程类似，我们在第二部分对本次的课程做下小结。</p>
<h3 id="81onetomany">8.1 基于 One-to-Many 架构的文本生成应用</h3>
<p>这个部分我们介绍下 One-to-Many 架构。首先我们来看下示意图：</p>
<p><img src="https://images.gitbook.cn/22e5d100-fc2b-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>One-to-Many 的架构中输入序列往往只有一个元素，然后根据已经训练好的模型单步预测输出元素并循环往复最后得到一个完整的输出序列。这个应用在文本生成中比较常见。我们下面结合一个简单的例子来说明这种文本生成应用的具体做法。我们先看下应用的任务：</p>
<pre><code>private static final String[] stringArray = new String[]{"我","来自","苏宁","易购","。"};
</code></pre>
<p>第一个数组对象存储的是一个字符序列。一共由 4 个串构成。我们的目标是输入“我”这个字，把后面的三个词包括句号都预测出来。显然，这可以采用 One-to-Many 的架构进行。我们先看下建模的结构：</p>
<pre><code>    public static MultiLayerNetwork generateModel(LinkedHashSet&lt;String&gt; words){
        MultiLayerConfiguration netconf = new NeuralNetConfiguration.Builder()
                .seed(1234)
                .miniBatch(false)
                .iterations(1)
                .learningRate(0.01)
                .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                .updater(Updater.ADAM)
                .list()
                .layer(0, new GravesLSTM.Builder().nIn(words.size()).nOut(128).activation(Activation.TANH).build())
                .layer(1, new GravesLSTM.Builder().nIn(128).nOut(128).activation(Activation.TANH).build())
                .layer(2, new RnnOutputLayer.Builder(LossFunctions.LossFunction.MCXENT)
                        .activation(Activation.SOFTMAX).nIn(128).nOut(words.size()).build())
                .pretrain(false).backprop(true)
                .build();
        MultiLayerNetwork net = new MultiLayerNetwork(netconf);
        return net;
    }
</code></pre>
<p>入参其实是一个不含重复字符的，并且按照顺序存储的词的集合。由于只含有一条训练数据因此 .miniBatch(false) 这个参数需要设置下。在这个网络结构中，我们使用了两层的 LSTM 结构。需要注意的是，第一层 LSTM 的 nIn 入参还有输出层的 nOut 参数需要和词集的维度保持一致，因为我们的最终目的，是根据输入的一个词预测出一个词串。</p>
<p>下面我们看下数据构建、训练还有测试的逻辑。</p>
<pre><code>      public static void main(String[] args) {
        LinkedHashSet&lt;String&gt; vocabulary = new LinkedHashSet&lt;&gt;();
        for (String str : stringArray)
            vocabulary.add(str);
        allWords.addAll(vocabulary);
        //
        MultiLayerNetwork net = generateModel(vocabulary);
        net.setListeners(new ScoreIterationListener(1));
        //
        INDArray input = Nd4j.zeros(1, allWords.size(), stringArray.length);
        INDArray labels = Nd4j.zeros(1, allWords.size(), stringArray.length);

        int samplePos = 0;
        for (String currentWord : stringArray) {
            String nextWord = stringArray[(samplePos + 1) % (stringArray.length)];
            input.putScalar(new int[] { 0, allWords.indexOf(currentWord), samplePos }, 1);
            labels.putScalar(new int[] { 0, allWords.indexOf(nextWord), samplePos }, 1);
            samplePos++;
        }
        DataSet trainingData = new DataSet(input, labels);

        for (int epoch = 0; epoch &lt; 50; epoch++) {

            System.out.println("Epoch " + epoch);

            net.fit(trainingData);
            net.rnnClearPreviousState();

            INDArray testInit = Nd4j.zeros(allWords.size());
            testInit.putScalar(allWords.indexOf(stringArray[0]), 1);
            System.out.print(stringArray[0] + " ");

            INDArray output = net.rnnTimeStep(testInit);

            for (int step = 0; step &lt; 4; ++step ) {
                int sampledCharacterIdx = Nd4j.getExecutioner().exec(new IMax(output), 1).getInt(0);
                System.out.print(allWords.get(sampledCharacterIdx) + " ");
                INDArray nextInput = Nd4j.zeros(allWords.size());
                nextInput.putScalar(sampledCharacterIdx, 1);
                output = net.rnnTimeStep(nextInput);
            }
            System.out.print("\n");
        }
    }
</code></pre>
<p>以上是构建数据、训练和预测的完整逻辑。首先我们需要把所有不重复的词存储起来，然后利用上面的模型声明一个含有两层的 LSTM 神经网络。我们定义两个三维的张量，里面存储特征序列还有标注序列。</p>
<blockquote>
  <p>所谓特征序列其实就是 stringArray 对象中存储的每一个词，而标注序列则是特征序列位移一个词的结果。</p>
</blockquote>
<p>我们将该组数据封装在一个 DataSet 中，然后训练 50 个 Epoch。为了方便观察每一轮的训练效果，我们将预测的结果序列打印出来方便观察。下面是我在训练时候的截图：</p>
<p><img src="https://images.gitbook.cn/e4c870a0-fa02-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/f0f92ae0-fa02-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>从截图的预测结果来看，刚开始几轮训练的时候，模型还没有完全收敛，损失函数的值也比较高。预测的序列并不是成文的、可以理解的表达语句，重复的词出现比较多。</p>
<p>等到接近 50 轮后，一方面损失函数的值已经降得比较低，另一方面实际预测的结果也已经和训练数据完全一致了。不过，这个案例中有过拟合的可能性。</p>
<p>但抛开实际的应用效果来说，我们确实完成了一个简单的基于输入单个词来生成一段话的功能。有兴趣的读者可以根据自身的业务需求，生成一些语料来验证课程中提到的模型。</p>
<h3 id="82">8.2 小结</h3>
<p>本次课程主要对基于 RNN 的序列生成进行了讨论。虽然我们仅仅准备了一条语料来验证模型的功能，但从每一轮迭代后预测的文字序列，并且结合 Loss 值的下降情况，我们可以比较明显地看到 RNN 学习的过程。</p>
<p>随着模型逐渐得收敛，预测出来的文字序列的上下文也逐渐变得通顺和合理，形成了比较明显的语义。最后我们依然需要指出，本课程中涉及的数据是作者为了验证模型自己随意编造的，不具有落地意义。但涉及的 RNN 网络的架构则具有通用性，不仅可以由输入文字生成新的文字，也可以通过简单的改造和 CNN 结合，达到输入图片后输出文字序列的效果，具体的扩展和延伸工作请有兴趣的读者自行研究。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>