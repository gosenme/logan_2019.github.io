---
title: Deeplearning4j 快速入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课我们介绍另一种常用的神经网络结果——循环神经网络（Recurrent Neural Network，RNN）。需要注意的是，RNN 可以是两种神经网络的缩写，一种是本次课程讨论的 Recurrrent Neural Network，另一种则是 Recursive Neural Network，也称递归神经网络。前者是时间递归的神经网络，而后者是结构递归。在下文中，如果不特别说明，RNN 都代表 Recurrent Neural Network。有关递归神经网络的更多信息，读者可以自行查阅相关资料，这里不再赘述。本节课核心内容包括：</p>
<ul>
<li>基于 Many-to-One 架构的文本分类应用</li>
</ul>
<p>在实际问题中，视频、文本、语音都具有时序性。虽然上一节课中介绍的卷积神经网络可以针对单一图像进行目标检测和识别，但是并不擅长处理时序问题，而这些问题用循环神经网络处理起来就自然许多。我们先结合下面两张图来看下循环神经网络的原理。</p>
<p><img src="https://images.gitbook.cn/f05172d0-f9fa-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/f9b77450-f9fa-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>第一张图从宏观上解释了循环神经网络结构递归的本质。从第一张图可以看出，循环神经网络的总体结构和之前介绍的全连接网络是类似的，但在中间的隐藏层神经元之间是有状态的连续传递。通常我们都会用第一张图右侧的简略图来表示循环神经网络。</p>
<p>第二张 GIF 图则是对第一张图中隐藏层结构展开的动态效果的展示。从 GIF 动图中我们可以看到，循环神经网络每个神经元接收了一个输入（这个输入可以是一个特征向量，比如 Word Embedding 后的词向量），然后经过激活函数等操作，可以得到当前神经元的输出。同时该输出继续传递至下一个神经元，作为输入的一部分参与后面神经元的输出。<strong>这便是循环神经网络的基本原理。</strong></p>
<p>从上面介绍的内容可以看出，循环神经网络的关键在于，可以将过去的信息传递到未来。试想，我们的输入是一个文字序列或视频帧序列，那么循环神经网络可以将第一个文字或第一帧图像中抽取的特征向前传递，在获取每个时间状态下数据特征的同时，最后可以获取整个序列数据的特征内容。<strong>如果说卷积神经网络擅于获取空间特征，那么循环神经网络则擅于提取时间维度的特征。</strong></p>
<p>循环神经网络虽然在理论上具备了很好地提取时间维度特征的办法，但是当输入序列过长时，容易出现序列头部状态信息丢失的情况。正是因为这个问题，循环神经网络的理论虽然很早就被提出，但是受限于这个缺点及硬件计算能力，所以其无法在工业界大规模落地。直到 LSTM（Long Short-Term Memory）的出现，循环神经网络及其变种才得到进一步的落地和发展，在包括机器翻译、QA 系统、语音识别、文本分类等问题上取得了很好的效果。</p>
<p><img src="https://images.gitbook.cn/eab71cc0-0365-11e9-8cdc-69881fcac255" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/16f4a4b0-0366-11e9-8cdc-69881fcac255" alt="enter image description here" /></p>
<p>上面两张截图是传统 RNN 和 LSTM 的内部逻辑示意图。可以看出在第一张图中，RNN Cell 内部结构非常简单，直接将上一个神经元传递过来的信息，和当前神经元的输入信息一并送入激活函数中，得到输出并传到下一个神经元。</p>
<p>而相对地，LSTM Cell 中逻辑则复杂很多，但主要可以划分为输入门、遗忘门和输出门三个部分。遗忘门顾名思义是会选择性地记忆前面神经元传递过来的一些信息，输入门则是对新输入的信息进行过滤，输出门控制遗忘门和输入门过滤出的信息，并进一步做选择性输出。这是 LSTM Cell 具有长期记忆原理的简单描述，更多详细信息读者可以参考 <a href="https://www.researchgate.net/publication/13853244_Long_Short-term_Memory">LSTM 的论文</a>进行研读。</p>
<p>另一种和 LSTM 类似的结构是 GRU（Gated Recurrent Unit）。GRU 相比 LSTM 少了一个门，结构更加简单，实际使用的效果和 LSTM 差不多，这里就不多做说明了。</p>
<p>循环神经网络及其变种的训练依赖于 BP 算法，具体来说有 BPTT（Back Propagation Through Time，即 Full-BPTT）和 Truncated-BPTT（T-BPTT）。传统循环神经网络可能会出现梯度弥散（Gradient Vanishing）和梯度爆炸（Gradient Explosion）的问题。一般地，梯度爆炸的问题可以通过梯度剪裁的方法解决，但梯度弥散的问题则不是那么容易处理。现在 LSTM 中的具体实现采用累加的形式计算状态，而不是累乘，这在一定程度上缓解了梯度弥散的问题。</p>
<p>在 Deeplearning4j 中，支持传统 RNN 以及 LSTM 和 Bi-LSTM。在官方给出的示例中，也给出了常用的文本生成、Sequence-to-Sequence 等应用。总的来说，常见循环神经网络的应用可以归为 3 类：One-to-Many、Many-to-One、Many-to-Many。</p>
<p>下面几课我就分别结合文本生成、文本分类、序列标注和机器翻译这几个实际应用来详细描述上面的这几类问题。</p>
<h3 id="71manytoone">7.1 基于 Many-to-One 架构的文本分类应用</h3>
<p>Many-to-One 的架构指的是，对于输入序列只输出一个结果（一般在最后一个神经元输出）。这样的架构比较适合用于序列的分类问题，我们先看下 Many-to-One 的示意图。</p>
<p><img src="https://images.gitbook.cn/a0445960-fc2a-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>截图中红色 X 序列代表输入，绿色的 Y 则表示输出。对于文本分类问题而言，X 序列可以代表 Embedding 的词向量序列，而 Y 则代表分类的结果。</p>
<p>下面我们看一下基于 Deeplearning4j 中的 LSTM 实现文本分类的一个具体问题：情感识别。这个应用的数据来源于 <a href="https://spaces.ac.cn/archives/3414">https://spaces.ac.cn/archives/3414</a> 这个博客作者分享的评价数据。该数据语料主要分为正、反两方面的评价文本，以 Excel 表的形式存储。对于这些语料，我先用了 jieba 分词进行处理。分完词之后的结果，词与词之间用空格进行分隔。部分数据可见下图：</p>
<p><img src="https://images.gitbook.cn/4b4267e0-f9ff-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/573fdd20-f9ff-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>截图中每一行数据都表示一条语料。标注用中文表示（正面、负面）。</p>
<p>下面我们看下如何用 Deeplearning4j 构建这样的分类模型。</p>
<pre><code>public static MultiLayerNetwork textClassifyModel(){
        MultiLayerConfiguration netconf = new NeuralNetConfiguration.Builder()
                .seed(1234)
                .iterations(1)
                .learningRate(0.01)
                .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                .regularization(true)
                .l2(5 * 1e-4) 
                .updater(Updater.ADAM)
                .list()
                .layer(0, new EmbeddingLayer.Builder().nIn(VOCAB_SIZE).nOut(100).activation(Activation.IDENTITY).build())
                .layer(1, new GravesLSTM.Builder().nIn(100).nOut(100).activation(Activation.SOFTSIGN).build())
                .layer(2, new RnnOutputLayer.Builder(LossFunctions.LossFunction.MCXENT)
                        .activation(Activation.SOFTMAX).nIn(100).nOut(2).build())
                .pretrain(false).backprop(true)
                .setInputType(InputType.recurrent(VOCAB_SIZE))
                .build();

        MultiLayerNetwork net = new MultiLayerNetwork(netconf);
        return net;
}
</code></pre>
<p>我们分析下上面的建模配置。整个神经网络的结构共可以分为三层，<strong>第一层是 Embedding，第二层是 LSTM，第三层是针对 RNN 的输出层。</strong>Embedding 的作用是将输入的词映射成词向量，而 LSTM 是基于了 Many-to-One 的架构，对于输入的词向量序列输出一个分类结果。这里 LSTM 层的神经元数量用户可以根据自己的需要去设计，这里我们设置了 100 个 Cell。EmbeddingLayer 的输入是语料中涉及到不重复词的数量，输出的是词向量的维度。需要注意的是，当用户使用 RNN 或 LSTM 时，需要使用 RnnOutputLayer 作为输出层。</p>
<p>下面我们介绍下 Deeplearining4j 中序列问题的训练数据集构建方法，以及涉及到的掩码（Mask Array）技术。官网的介绍地址是：<a href="https://deeplearning4j.org/usingrnns">https://deeplearning4j.org/usingrnns</a>。</p>
<p>首先，输入循环神经网络的其实是一个三维的数据：[batchSize,sequenceLength,sequenceValuePerTimeStep]。如果我们将 batchSize 设置为 1，那么实际的数据结构将更为清晰，即只包含该条训练数据中每一个时刻的特征值。在实际问题中，序列的长度并不是固定的，如果要在一个 batch 里同时支持处理不同长度的序列，那么最简单直接的办法就是，将所有序列统一成一样的长度（一般以当前 batch 下面最长的那个序列长度为准），这里 Deeplearning4j 通过引入掩码的方式来支持。</p>
<p>掩码（Mask Array）的作用是，在不同长度的序列中，用一个新的二进制序列来表示原序列中哪些位置是真实有值的，哪些是为了统一长度而额外添加的。其中真实有值的位置在掩码序列中用 1 来表示，额外添加的用 0 表示。下面是 Many-to-One 结构下的掩码的示意图：</p>
<p><img src="https://images.gitbook.cn/8efcb430-fa00-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>截图中红色框的就是掩码序列。由于对于 Many-to-One 的结构来说，在输出层，我们只关心最后一个 RNN Cell 的输出，所以其余的 RNN Cell 虽然有输出，但我们并不需要，那么就可以用输出的掩码 0 来表示。同样，如果需要在输入层用掩码来表示的也类似。下面我们来看下具体落地的代码逻辑：</p>
<pre><code>private static class SegmentIterator implements DataSetIterator {

        private static final long serialVersionUID = -649505930720554358L;

        private int batchSize;
        private int vocabSize;
        private int maxLength;
        private SequenceIterator&lt;VocabWord&gt; iter1;
        private SequenceIterator&lt;VocabWord&gt; iter2;
        private AbstractCache&lt;VocabWord&gt; vocabCache1;
        private AbstractCache&lt;VocabWord&gt; vocabCache2;

        private boolean toTestSet;

        public SegmentIterator(int batchSize, int vocabSize, SequenceIterator&lt;VocabWord&gt; iter1, SequenceIterator&lt;VocabWord&gt; iter2,
                                          AbstractCache&lt;VocabWord&gt; vocabCache1, AbstractCache&lt;VocabWord&gt; vocabCache2) {
            this.batchSize = batchSize;
            this.vocabSize = vocabSize;
            this.iter1 = iter1;
            this.iter2 = iter2;
            this.vocabCache1 = vocabCache1;
            this.vocabCache2 = vocabCache2;

        }

        public AbstractCache&lt;VocabWord&gt; getVocabCache1() {
            return vocabCache1;
        }

        public AbstractCache&lt;VocabWord&gt; getVocabCache2() {
            return vocabCache2;
        }

        public int getMaxLen(){
            return maxLength;
        }

        @Override
        public DataSet next(int num) {

            if( toTestSet ){
                reset();
                batchSize = num;
            }

            /*--构建输入序列--*/
            List&lt;List&lt;VocabWord&gt;&gt; iter1List = new ArrayList&lt;&gt;(batchSize);       

            for (int i = 0; i &lt; batchSize &amp;&amp; iter1.hasMoreSequences(); i++) {
                iter1List.add(iter1.nextSequence().getElements());
            }
            /*--构建输入序列结束--*/
            /*-------------------------------------*/
            /*--构建输出序列--*/
            List&lt;List&lt;VocabWord&gt;&gt; iter2List = new ArrayList&lt;&gt;(batchSize);
            for (int i = 0; i &lt; batchSize &amp;&amp; iter2.hasMoreSequences(); i++) {
                iter2List.add(iter2.nextSequence().getElements());
            }
            /*--输出序列构建完毕--*/
            /*--------------------------------------*/
            int numExamples = Math.min(iter1List.size(), iter2List.size());     //保证语料及标注在数量上的一致性
            int in1Length = 0;
            int in2Length = 0;
            /*以下部分针对输入/输出序列长度，以当前 batch 里最长序列的长度作为全部序列的长度，以此兼容变长的场景*/
            for (int i = 0; i &lt; numExamples; i++) {
                in1Length = Math.max(in1Length, iter1List.get(i).size());
            }
            for (int i = 0; i &lt; numExamples; i++) {
                in2Length = Math.max(in2Length, iter2List.get(i).size());
            }
            maxLength = Math.max(in1Length, in2Length);
            /*完成输入/输出变长的支持*/
            /*--------------------------------------*/


            INDArray features = Nd4j.create(numExamples, 1, maxLength);  //当  batchSize=32，maxLength=39，则每条语料由每个词的哈夫曼编码构成，如：283.0，128.0，10.0，0.0，0.0……

            INDArray labels = Nd4j.create(numExamples, 2, maxLength);   //2 这里代表分类的类别数目
            //
            INDArray featuresMask = Nd4j.zeros(numExamples, maxLength);
            INDArray labelsMask = Nd4j.zeros(numExamples, maxLength);

            int[] origin = new int[3];
            int[] mask = new int[2];
            for (int i = 0; i &lt; numExamples; i++) {
                List&lt;VocabWord&gt; list = iter1List.get(i);
                origin[0] = i;                        //三维数组 origin 中，下标为 0 存储语料的批次（batch index）
                mask[0] = i;

                int j = 0;                          //每条语料中词的位置索引
                for (VocabWord vw : list) {         //遍历整条语料
                    origin[2] = j;
                    features.putScalar(origin, vw.getIndex());
                    //
                    mask[1] = j;
                    featuresMask.putScalar(mask, 1.0);  //对于掩码序列，如果当前位置有词出现，则为 1.0，否则为 0.0
                    ++j;
                }
                //
                int idx = iter2List.get(i).get(0).getIndex();
                int lastIdx = list.size();
                labels.putScalar(new int[]{i,idx,lastIdx-1},1.0);   //设置标注信息，[1.0] 为正例，[0.1] 为负例
                labelsMask.putScalar(new int[]{i,lastIdx-1},1.0);   //标注序列掩码保证只在最后一个 RNN Cell 输出标注信息，其余掩码都为 0.0
            }

            return new DataSet(features, labels, featuresMask, labelsMask);
        }


        @Override
        public void reset() {
            iter1.reset();
            iter2.reset();
        }

        @Override
        public boolean hasNext() {
            return iter1.hasMoreSequences() &amp;&amp; iter2.hasMoreSequences();
        }

        @Override
        public DataSet next() {
            return next(batchSize);
        }

        //此处省略一些需要实现的父类以及接口的未实现的方法
}
</code></pre>
<p>这里详细解释下上面的训练数据生成的逻辑。我们生成的是一个 batch 的训练数据并且封装在一个 DataSet 中。在实际的迭代过程中，每一次的迭代都会消费一个 DataSet 中整个批次的训练数据来更新模型参数。</p>
<p>首先，我们通过实现 DataSetIterator 接口来构造一个符合自己业务需求的类 SegmentIterator。在该类的构造函数当中，我们接收 6 个参数：</p>
<ul>
<li><code>int batchSize</code>：批量训练的数据量</li>
<li><code>int vocabSize</code>：语料中词库的维度（可不传）</li>
<li><code>SequenceIterator&lt;VocabWord&gt; iter1</code>：语料/文字序列迭代器</li>
<li><code>SequenceIterator&lt;VocabWord&gt; iter2</code>：标注序列迭代器</li>
<li><code>AbstractCache&lt;VocabWord&gt; vocabCache1</code>：语料涉及的词集</li>
<li><code>AbstractCache&lt;VocabWord&gt; vocabCache2</code>：标注涉及的词集</li>
</ul>
<p>所有的语料和标注数据都存储在了 <code>SequenceIterator&lt;VocabWord&gt;</code> 的实例对象当中。VocabWord 是 Deeplearning4j 针对序列数据，尤其是文本数据封装的一个类，里面包含了某个词的具体内容、索引、词频等相关信息。对于文本序列来说，实际构成数据的是词序列，所以利用 <code>SequenceIterator&lt;VocabWord&gt;</code> 来封装语料是比较直观的一种方式。另外，标注的序列（在这个案例中，也就是由“正面”、“负面”两个词构成序列）同样由 <code>SequenceIterator&lt;VocabWord&gt;</code> 进行封装。接下来看下具体的构造逻辑，也就是 next 方法里的具体实现。</p>
<p>首先我们将文字序列迭代器和标注序列迭代器中的数据根据 batchSize 的大小取出一部分，分别放到两个对象当中。同时为了确保两个序列的长度一致，我们做一些校验的工作（一般情况下，只要语料和标注一一对应，以上校验将不起实质性作用）。接下来，利用 ND4J 工具类的静态方法，创建三维的张量训练数据包括标注，另外还有对应的掩码数据。</p>
<pre><code>INDArray features = Nd4j.create(numExamples, 1, maxLength);                                                     
INDArray labels = Nd4j.create(numExamples, 2, maxLength);   
INDArray featuresMask = Nd4j.zeros(numExamples, maxLength);
INDArray labelsMask = Nd4j.zeros(numExamples, maxLength);
</code></pre>
<p>其中 numExamples 就是 batchSize。掩码（Mask Array）序列的初始值全部设置为 0。maxLength 是当前 batch 下最长的那个序列的长度，目的是解决不同长度序列的统一问题。需要注意的是，labels 这个对象第二个维度的值是 2，代表只有两种分类，如果是 multiclass 的场景，用户可以自行修改。下面需要给这些对象赋值。</p>
<pre><code>int[] origin = new int[3];
int[] mask = new int[2];
for (int i = 0; i &lt; numExamples; i++) {
                List&lt;VocabWord&gt; list = iter1List.get(i);
                origin[0] = i;   //三维数组 origin 中，下标为 0 存储语料的批次（batch index）
                mask[0] = i;

                int j = 0;            //每条语料中词的位置索引
                for (VocabWord vw : list) {  
                //遍历整条语料
                    origin[2] = j;
                    features.putScalar(origin, vw.getIndex());
                    //
                    mask[1] = j;
                    featuresMask.putScalar(mask, 1.0);  
                    ++j;
                }
                //
                int idx = iter2List.get(i).get(0).getIndex();
                int lastIdx = list.size();
                //设置标注信息，[1.0] 为正例，[0.1] 为负例
                labels.putScalar(new int[]{i,idx,lastIdx-1},1.0);   
                //标注序列掩码保证只在最后一个 RNN Cell 输出标注信息，其余掩码都为 0.0
                labelsMask.putScalar(new int[]{i,lastIdx-1},1.0);   

}
</code></pre>
<p>我们分别定义了一个二维和三维的数组。三维数组的元素值用于表征每条训练中的每个词在整个 batch 中的位置。二维数组则表征掩码数据的位置。我们遍历当前 batch 中的所有数据，按顺序将每条数据中的每个词的索引填充到之前声明的 features 对象中，同时对于掩码数据，根据词的有效性进行 0 或 1 的标识。</p>
<p>以上是对于文本序列数据的构建。对于相应的标注结果，和构建文字序列类似，只不过是在序列输出的最后一个 RNN Cell 的位置才有输出，掩码的标识也和文字序列类似。那么到此，构建训练数据的工作就基本完成了。</p>
<p>下面和之前提到的所有训练逻辑一样，训练若干个 Epoch，将模型保存后评估下准确率。目前我在单机场景下训练 10 轮左右，可以达到 90% 的准确率。具体可以请读者自行验证。</p>
<h3 id="72">7.2 小结</h3>
<p>在本次课程中我们首先介绍了循环神经网络（Recurrent Neural Network）的基本结构和原理，随后讨论了如何基于 Deeplearning4j 构建基于 RNN/LSTM 的文本分类模型。</p>
<p>需要指出的是，我并没有刻意加深循环神经网络的层数以及 LSTM Cell 的数量，需要在此基础上进一步优化分类准确率等指标的朋友，可以考虑从 Embedding Size、LSTM Cell 数量、LSTM Layer 的层数等方面来进一步调优这个模型。但在实际使用中，将模型复杂化的同时也必须考虑在 Inference 阶段的响应时效问题，否则得不偿失。</p>
<p>另外由于循环神经网络结构的特点，并行化计算不如卷积神经网络那么方便，因而 RNN/LSTM Cell 数量等因素必须要进行考虑。在接下来的课程中，我将介绍循环神经网络在文本生成中的应用。</p>
<p><strong>相关资料</strong></p>
<ul>
<li><a href="https://deeplearning4j.org/usingrnns">Deeplearining4j 中序列问题的训练数据集构建方法</a></li>
<li><a href="https://www.researchgate.net/publication/13853244_Long_Short-term_Memory">LSTM 论文：<em>Long Short-term Memory</em></a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>