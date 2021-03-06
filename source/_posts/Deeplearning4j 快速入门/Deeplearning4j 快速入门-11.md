---
title: Deeplearning4j 快速入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在前两节课的内容中，我们介绍了循环神经网络及变种的基本原理，并介绍了 Many-to-One 和 One-to-Many 两种架构下，如何基于 Deeplearning4j 进行文本分类和文本生成的应用。</p>
<p>本节课开始，我们将继续为大家介绍另外一种架构，Many-to-Many 在序列标注和机器翻译问题中的应用。这两类问题是 NLP 中的经典问题。尤其对于序列标注问题来说，分词、实体识别、句法分析都可以基于序列标注进行。这里介绍的也是平时企业中最常见的问题——分词。本节课核心内容包括：</p>
<ul>
<li>基于 Many-to-Many 架构的序列标注应用</li>
</ul>
<h3 id="91manytomany">9.1 基于 Many-to-Many 架构的序列标注应用</h3>
<p>序列标注是自然语言处理应用中常见的问题。基于序列标注的思想，我们可以解决分词、实体识别、浅层句法分析等实际应用。序列标注在以往一般会依赖于 HMM、CRF 等模型来实现，并且已经可以达到产品级别的准确率。基于神经网络的方法目前也有很多工作和研究成果，虽然在准确性上不一定有质的飞跃，但端到端的思想可以体现得更为彻底，毕竟类似 CRF 的模型设计特征模版需要做比较大量的预研工作。</p>
<p>下面我们就详细介绍下如何基于 Deeplearning4j 中的 LSTM 结构来实现分词的问题。使用的架构是 Many-to-Many。我们先来看下示意图。</p>
<p><img src="https://images.gitbook.cn/aa498440-fc2e-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>从截图中我们可以清楚地看到，每一个 RNN Cell 输出的结果即为我们的标注序列。和之前讲述的 Many-to-One/One-to-Many 不同，在 Many-to-Many 架构中，输出和输出的序列都是我们关心的。在分词的场景中，我们可以用最简单的 BESM 标注法来为单个字进行标注：<strong>即对应截图中的 Y 序列其实是一组 BESM 序列。</strong></p>
<p>下面我们来看下如何基于单层单向 LSTM 进行 BESM 序列的标注。首先看建模逻辑：</p>
<pre><code>public static MultiLayerNetwork getSegModel(){
          MultiLayerConfiguration netconf = new NeuralNetConfiguration.Builder()
                .seed(1234)
                .iterations(1)
                .learningRate(0.01)
                .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT) 
                .updater(Updater.ADAM)
                .list()
                .layer(0, new EmbeddingLayer.Builder().nIn(VOCAB_SIZE).nOut(256).activation("identity").build())
                .layer(1, new GravesLSTM.Builder().nIn(256).nOut(256).activation("softsign").build())
                .layer(2, new RnnOutputLayer.Builder().nIn(256).nOut(4).activation("softmax").build())
                .pretrain(false).backprop(true)
                .setInputType(InputType.recurrent(VOCAB_SIZE))
                .build();

        MultiLayerNetwork net = new MultiLayerNetwork(netconf);
        net.init();
        return net;
}
</code></pre>
<p>建模的逻辑和之前的 Many-to-One 的结构类似。由于我们使用的是 BESM 标注法来标注单个字，因此在输出层 nOut 的入参值设置成 4。接下来我们重点看下构建训练数据集的逻辑。</p>
<pre><code>@Override
public DataSet next(int num) { 
            //此处逻辑和 Many-to-One 部分类似，限于篇幅进行省略...
            /*--------------------------------------*/
            INDArray featureTensor = Nd4j.create(numExamples, 1, wordIterMaxLength);
            int[] loc = new int[3];
            for (int i = 0; i &lt; numExamples; i++) {
                List&lt;VocabWord&gt; list = wordIterList.get(i);
                loc[0] = i;                        //arr(0) store the index of batch sentence

                int j = 0;                          //index of the word in the sentence
                for (VocabWord vw : list) {         //traverse the list which store an entire sentence
                    loc[2] = j++;
                    featureTensor.putScalar(loc, vw.getIndex());
                }
            }

            //Using a one-hot representation here. Can't use indexes line for input
            INDArray taggingTensor = Nd4j.create(numExamples, 4, taggingIterMaxLength);
            for (int i = 0; i &lt; numExamples; i++) {
                List&lt;VocabWord&gt; list = taggingIterList.get(i);
                loc[0] = i;

                int j = 0;
                for (VocabWord vw : list) {
                    loc[1] = vw.getIndex();
                    loc[2] = j++;
                    taggingTensor.putScalar(loc, 1.0);   //one hot representation
                }
            }
            return new DataSet(featureTensor, taggingTensor);
}
</code></pre>
<p>这部分用于构建 DataSet 的逻辑总体和 Many-to-One 架构中的对应逻辑相类似。唯一不同的地方在于，在这个应用中，我们不需要构建掩码序列，因为每个 RNN Cell 的输出都是输出序列的一个部分，都是我们关心的。</p>
<p>最后补充一下语料的格式。由于时间仓促，因此这个应用我并没有在大规模的开源数据集上进行测试，只是自己补充了一些带有标注的语料供大家参考：</p>
<p><img src="https://images.gitbook.cn/9118d610-fa03-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/9a6d9980-fa03-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>以上两条语料分别存储在两个文本文件里。字与字之间、标注与标注之前用空格隔开。读者可以根据自己需要，添加自己的语料和标注来验证课程中的逻辑。下面我们给出训练后测试的结果。</p>
<p><img src="https://images.gitbook.cn/ac9c7220-fa03-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>截图中最后一行是分词的实际结果，可以看出预测的结果符合我们的预期。重点需要解释下分词结果串上面的那个三维张量。</p>
<p>从截图中我们可以看出，待分词的文字串共含有 12 个字，换句话说预测出来的序列也是一个包含 12 个标注的序列。由于我们使用 BESM 标注法共含有 4 种可能的标注，因此实际有意义的内容是一个 4*12 的二维矩阵，即每个字输出的标注可能含有 4 种状态，并且概率大小不一。当对每个字输出的标注取概率最大的那个时，就构成了最终的结果（当然对于概率接近的结果，可以另做细致的处理，这里不再赘述）。</p>
<p>从截图中看到，头两个字“中国”对应输出的结果中，“中”对应第一行概率最大，“国”对应第二行概率最大，因此它们的标注就分别为“B”和“E”。以此类推，后面文字的标注也都可以获得，并且得到最终整个文本序列的分词结果。下面补充下预测的逻辑：</p>
<pre><code>/***
*单条语料的预测
*/
private static List&lt;String&gt; predict(String sentence, MultiLayerNetwork net,
                    AbstractCache&lt;VocabWord&gt; wordVocabulary,
                    AbstractCache&lt;VocabWord&gt; taggingVocabulary){
        char[] charArray = sentence.toCharArray();
        double[] wordIndices = new double[charArray.length];
        for(int idx = 0; idx &lt; charArray.length; ++idx){
            int wordIndex = wordVocabulary.indexOf(String.valueOf(charArray[idx]));
            wordIndices[idx] = wordIndex;
        }
        INDArray featureTensor = Nd4j.create(1, 1, charArray.length);
        featureTensor.put(new INDArrayIndex[] {NDArrayIndex.point(0), NDArrayIndex.interval(0, charArray.length)}, Nd4j.create(wordIndices));
        INDArray out = net.output(featureTensor,false);
        System.out.println("Test");
        System.out.println(out);
        INDArray argMax = Nd4j.argMax(out, 1);
        StringBuilder labels = new StringBuilder();
        for( int col = 0; col &lt; argMax.columns(); ++col ){
            double labelIndex = argMax.getDouble(col);
            String labelWord = taggingVocabulary.wordAtIndex((int)labelIndex);
            labels.append(labelWord);
        }
        String labelStr = labels.toString();
        List&lt;String&gt; result = new ArrayList&lt;&gt;();
        for( int index = 0; index &lt; sentence.length();  ){
            if( labelStr.charAt(index) == 's'){
                result.add(Character.toString(sentence.charAt(index)));
                ++index;
            }else if( labelStr.charAt(index) == 'b' ){
                StringBuilder tempWord = new StringBuilder();
                do{
                    tempWord.append(Character.toString(sentence.charAt(index)));
                    ++index;
                }while( (  index &lt; sentence.length() &amp;&amp; labelStr.charAt(index) != 'e') );
                tempWord.append(Character.toString(sentence.charAt(index)));
                ++index;
                result.add(tempWord.toString());
            }
        }
        return result;
}
</code></pre>
<p>以上预测逻辑是针对单条文本进行分词的逻辑，结构总体比较清晰。这里我就不再详细解释了。最后做一下简单的讨论，即<strong>基于 LSTM 的 Many-to-Many 框架进行分词可能有什么样的缺陷。</strong></p>
<p>首先，我们在这个案例中讨论的 LSTM 是单向的 LSTM。语义信息从第一个 LSTM Cell 逐渐传递后最后一个 LSTM Cell，越往后，信息越丰富，理论上越是后面的预测结果越可靠，因为传递到后面的信息几乎包含了整个文本的上下文信息。而相对靠前的输出则显得不那么靠谱了。这相对于 CRF 等其他可以做序列标注的模型来说，是一个潜在的劣势。</p>
<p>但我们其实也有方案，就是可以基于 Bi-LSTM 替换单向的 LSTM 进行建模。理论上双向的 LSTM 可以弥补单向 LSTM 的不足，但相应的预测时间会比较长。目前 Deeplearning4j 已经支持了双向 LSTM，所以读者可以自行尝试，这里不再深究了。</p>
<h3 id="92">9.2 小结</h3>
<p>本节课我们讨论了，基于 Many-to-Many 的框架进行分词应用开发的简单案例，采用的序列标注手段也是经典的 BESM 标注法。在正文中我们给出的是单向 LSTM 的方案，但实际我们同样可以采用双向 LSTM 来解决这个问题，但需要考虑预测阶段的速度。</p>
<p>由于序列标注本身在实际生产开发中应用得非常广泛，因此针对于这一类问题的研究有利于产品的落地。当然我们并非一定要采用神经网络的解决方案，传统的一些浅层网络模型如 CRF 同样可以很好地解决这一类问题。</p>
<p>目前也有基于 LSTM + CRF 来做序列标注问题的，这无疑可以把 LSTM 构成的神经网络，看作是 CRF 特征模版的自动学习工具。有兴趣的读者也可以尝试，可以和使用纯神经网络的解决方案进行对比。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>