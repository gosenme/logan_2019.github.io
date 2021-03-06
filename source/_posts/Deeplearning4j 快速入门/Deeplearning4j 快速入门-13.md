---
title: Deeplearning4j 快速入门-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>下面两节课我将为大家介绍，如何基于 Deeplearning4j 的框架来实现词和句子的分布式/向量化建模。目前 Deeplearning4j 支持对词建模的 word2vec、GloVe，对文档建模的 doc2vec/paragraph2vec，以及对图结构进行建模的 DeepWalk 算法。在具体介绍这些建模工具之前，我们首先回顾下对文本建模的一些手段。本节课核心内容包括：</p>
<ul>
<li>文本建模的词袋和词嵌入模型</li>
<li>word2vec 的原理与建模</li>
<li>GloVe 的原理与建模</li>
</ul>
<h3 id="111">11.1 文本建模的词袋和词嵌入模型</h3>
<p>文本由很多的段落和很多的句子构成，同时，每个句子又由若干个词构成。因此在早期对文本建模时，很容易想到将一段文本表示成词的集合，也就是我们在 NLP 问题经常讲到的词袋模型（Bag of Words）。具体落地的时候，我们用一个很长的向量来表示这个词袋。向量中的每个索引位置即代表文本当中的词。那么每个位置的具体值可以看情况而定，我们可以直接用 0/1 来表示该词是否出现，也可以用 TF-IDF 的值来填充。</p>
<p><strong>词袋模型</strong>是经典的文本特征表示方法。直到现在，基于词袋模型对长文本进行特征表示依然会取得非常好的效果。它的表示方法简单、直接、易于理解。但它的缺点其实也是很突出的，就是向量的维度很高，且容易忽略上下文的信息（可以基于一些如 N-Gram 的语言模型进行补充调整，但会加重高维的问题）。当然对于这些问题我们有些手段可以处理，例如对于高维灾难的问题可以借助于 PCA/SVD 进行降维，或者基于统计的一些方法进行特征抽取，这些在这里就不展开讨论了。</p>
<p><strong>词的分布式表达/词嵌入</strong>是从另外一个角度来表示词或者文本，即对于每个词都用一个稠密向量来表示。这个稠密向量不再是 One-Hot 的稀疏表达形式，而是一个经由神经网络训练出来的，可以代表词本身物理含义的向量。单个词向量的维度一般可以设置成 64/128/256 等，但总的来说相比于词袋模型维度大大降低了。目前词向量的实现方式主要有：</p>
<blockquote>
  <p>word2vec</p>
  <ul>
  <li><a href="https://arxiv.org/pdf/1301.3781.pdf"><em>Efficient Estimation of Word Representations in Vector Space</em></a></li>
  <li><a href="https://arxiv.org/pdf/1310.4546.pdf"><em>Distributed Representations of Words and Phrases and their Compositionality</em></a></li>
  </ul>
  <p>GloVe</p>
  <ul>
  <li><a href="https://nlp.stanford.edu/pubs/glove.pdf"><em>GloVe: Global Vectors for Word Representation</em></a></li>
  </ul>
</blockquote>
<p>这些在 Deeplearning4j 中已经直接支持。下面我们首先来介绍下word2vec 的原理以及建模过程。</p>
<h3 id="112word2vec">11.2 word2vec 的原理与建模</h3>
<p>word2vec 是由 Google 研究员 Tomas Mikolov 等人在 2013 年左右提出的，可以说是神经网络在 NLP 领域的一大突破。正如它的名字那样，这个研究的目的就是将海量语料中的词进行向量化。word2vec 的训练本身是无监督的，也正是因为这样它的价值在某种程度上比基于监督学习获得词向量更能代表词的物理含义。对于它的用途，最直接的就是可以衡量词之间的相似度，通过模型可以召回一些具有相似语义的词。这在搜索的 Query 分析与改写和推荐场景中有着一定的价值。下面我们来简单看下它的实现。</p>
<p>word2vec 本身可以基于 CBOW 和 Skip-Gram 两种方式进行，而每一种方式又可以基于 Hierarchial Softmax 或 NCE（严格来讲是 Negative Sampling）两种框架实现。CBOW 或者说连续窗口模型是基于上下文来预测词，而 Skip-Gram 正相反，它是用某个词串中的中心词来预测整个上下文。如果我们基于 Hierarchial Softmax 的框架来构建 word2vec 的模型，那么 CBOW 和 Skip-Gram 的方式大致如下：</p>
<p><img src="https://images.gitbook.cn/26ff25a0-fc32-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>上面的左图是 CBOW + Hierarchial Softmax 来实现 word2vec，而右图则是 Skip-Gram + Hierarchial Softmax。CBOW 的输入是整个窗口中的上下文词集，而 Skip-Gram 则正好相反。模型的输出是一棵 Huffman 树，其中每个叶子节点代表词集中的某个具体的词。这样每个词就可以得到一个唯一的二进制编码。Hierarchial Softmax 的目的是将默认的 Softmax 以树结构来替代，从根节点到叶子节点的路径中，每经过一个内部结构即做一次 Logistic 二分类，因此原来的 Softmax 近似成多次 Logistic 回归。</p>
<p>上面描述的是 Hierarchial Softmax 结构做为模型输出。另外一种做法是使用 Negative Sampling，即使用随机负采样的方式替代输出 Huffman 编码树。Negative Sampling/NCE 的主要难点在于词集的采样高效性和均衡性。</p>
<p>以 CBOW 为例，对于一组固定训练样本并基于上下文预测单个词时，除了该词自身作为正样本，其余的词都可以作为负样本，优化目标也是尽量使得模型可以预测出正样本，因此随机负采样的过程非常重要。这里存在一个和词频相关的通识，具体来说对于高频词被采样的概率会高于低频词，因此这些词被采样作为负样本的概率会大很多。具体实现的时候，可以将所有词的归一化频率拼接成一个长度为 1 的线段，并且将这个线段等分成很多段（源码中取值为 $10^8$）。采样的时候，随机数发生器生成一组随机数，然后落在线段哪个范围内即取那个词，如果是需要被优化的词本身则直接跳过。</p>
<p>严格来说，word2vec 并不是算是深度学习，从示意图中我们看到，它其实是一个连隐藏层都可以去掉的二层神经网络结构。但是，基于 CBOW 或 Skip-Gram 的假设，再加上高效的训练方式，使得 word2vec 可以在短时间内训练出大量词集语料的词向量。目前，我们选择的主要方式是 Skip-Gram + Negtive Sampling 的实现方式，从实践的效果看，这样的实现方式在大语料下的效果要优于其他训练的方式。</p>
<p>下面我们以 Deeplearning4j 中的建模为例，来尝试构建 word2vec 模型。我们先看下下面的建模逻辑：</p>
<pre><code>import org.deeplearning4j.models.embeddings.learning.impl.elements.SkipGram;
import org.deeplearning4j.models.word2vec.VocabWord;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.BasicLineIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.List;

//省略声明部分
log.info("Building model....");
Word2Vec vec = new Word2Vec.Builder()
            .useHierarchicSoftmax(false)
            .negativeSample(1.0)
            .minWordFrequency(5)
            .elementsLearningAlgorithm(new SkipGram&lt;VocabWord&gt;())
            .stopWords(stopWords)
            .iterations(10)
            .layerSize(128)
            .seed(42)
            .windowSize(5)
            .iterate(iter)
            .tokenizerFactory(t)
            .build();
</code></pre>
<p>这部分的逻辑主要是，在声明一个 word2vec 的实例对象和设置各种参数。结合我们在上面讲到的理论部分，这些参数的设置就很好理解。</p>
<pre><code>.useHierarchicSoftmax(boolean reallyUse)    //是否采用 Hierarchic Softmax，布尔类型入参
.negativeSample(double negtive)    //当入参大于 0 的时候，采用 Negtive Sampling，否则不采用
.minWordFrequency(int minWordFrequency)    //词频下限参数，即语料中低于该词频出现的词不会参与建模
.elementsLearningAlgorithm(ElementsLearningAlgorithm&lt;VocabWord&gt; algorithm)    //选择采用 Skip-Gram 还是 CBOW。笔者这里采用的是 Skip-Gram
.stopWords(List&lt;String&gt; stopList)    //停用词
.layerSize(int layerSize)    //词向量长度
.windowSize(int windowSize)    //上下文窗口长度
</code></pre>
<p>以上是模型主要参数的一些解释。可以看出，我们可以使用 Skip-Gram + Negtive Sampling 的方式来建模。接下来，我们尝试基于一段分好词的语料来训练该模型。我们使用的语料是路遥的小说《平凡的世界》全文，分词使用的是 jieba。训练语料的构建可以参考一下逻辑（事先我们已经基于 jieba 分词以空格为分隔符构建了语料）。</p>
<pre><code>String filePath = "corpus.txt";
log.info("Load &amp; Vectorize Sentences....");
SentenceIterator iter = new BasicLineIterator(filePath);
TokenizerFactory t = new DefaultTokenizerFactory();
t.setTokenPreProcessor(new CommonPreprocessor());
</code></pre>
<p>我们将语料存储在 corpus.txt 这样的一个以 UTF-8 编码的文本文件中，然后调用 Deeplearning4j 内置的一些文本预处理类来读入语料，其中默认的切词接口就是按照空格来切词。</p>
<p>训练模型的方式就是调用 fit 接口即可。</p>
<pre><code>log.info("Fitting Word2Vec model....");
vec.fit();
</code></pre>
<p>另外，模型的保存和读取可以调用 WordVectorSerializer 这个工具类中的静态方法来完成。这里不再详述。</p>
<p>在训练完模型后，我们抽几个词来看下效果：</p>
<pre><code>log.info(“Closest Words:”);
System.out.println(vec.wordsNearestSum(“孙少平”, 5));
System.out.println(vec.wordsNearestSum(“孙少安”, 5));
System.out.println(vec.wordsNearestSum(“田晓霞”, 5));
System.out.println(vec.wordsNearestSum(“田润叶”, 5));
System.out.println(vec.wordsNearestSum(“白面”, 5));
</code></pre>
<p>这里的目的是，在构建完模型后，基于模型来获取这些词的相似词（这些词大部分是小说中主人公的名字）。得到的结果如下图：</p>
<p><img src="https://images.gitbook.cn/61e04cf0-fbcc-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>从截图中我们可以看到，大部分的人名和与其交集较多的人与事互为相似词。熟悉这部小说情节的同学应该知道，这样的结果总体是可以反映它们的相近程度的。但是需要注意的是，相似结果或词并不能完全替代原词，因此使用的时候也需要注意。如果读者需要从模型中再度获得词的词向量的话，也可以通过接口 getWordVector 来获取。</p>
<p>最后我们总结下这部分的内容。在本次课程的第一个部分中，我们介绍了 word2vec 的基本原理和几种实现方式，并基于 Deeplearning4j 框架实践了一个简单的应用，使得大家对 word2vec 模型有了感性的认识。应当说，word2vec 模型的效果不仅和我们上面介绍的参数有关，同时和数据预处理的质量也大有关系。尤其对于中文而言，分词、停用词的构建对最终的 word2vec 也有很大的影响。因此，word2vec 在实际使用时，需要结合自身的业务做更多细致的规划。</p>
<h3 id="113glove">11.3 GloVe 的原理与建模</h3>
<p>GloVe（<a href="https://nlp.stanford.edu/pubs/glove.pdf">Global Vectors for Word Representation</a>）是 2014 斯坦福大学提出的，一种基于全局和局部语料单词共现频率来计算词向量的一种模型。不同于上面介绍的 word2vec，GloVe 本身并不是基于神经网络实现的，并且 word2vec 更多关注的是行级别的词信息，而 GloVe 是兼顾全局和局部词信息的一种模型。在原文中，作者举了如下截图的例子，我们先来看下：</p>
<p><img src="https://images.gitbook.cn/6ead6e40-fbcc-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>截图所想表达的意思用一句话概括就是，词的相关与否可以用改词与其他词的共现比率来表示。根据截图中的例子，k 代表的是四种具体的词，分别和 ice 还有 steam 两个词，其中一个相关、两个都相关或两个都无关的场景。具体来说，根据语料，我们可以非常容易获得诸如 P(k|some word) 这样的统计信息。但是该后验概率的绝对大小并不能直接使用，因此作者想到了使用比率的大小，即后验概率之比来表征相关性信息。</p>
<p>比如图中的 water 还有 fashion，它们对于 ice 和 steam 的后验概率之比接近于 1，那么它们就是都相关或都不相关。而 solid 这个词明显和 ice 更加相关，gas 和 steam 更加相关。这个假设在一定程度上是合理的，尤其从全局语料信息来看，相关性的共现次数肯定会比较高。那么基于这个假设，作者将词共现信息和词向量的信息进行统一建模，即可获取基于统计信息的词向量信息。原文的理论推导比较详细，有兴趣的同学可以直接参考原文，这里限于篇幅就不再展开了。下面，我们看下如何基于 Deeplearning4j 构建 GloVe 模型。首先看下模型构建逻辑还有必要的参数设置：</p>
<pre><code>Glove glove = new Glove.Builder()
            .layerSize(512)
                .iterate(iter)
                .iterations(1)
                .tokenizerFactory(t)
                .alpha(0.75)
                .learningRate(0.1)
                .minWordFrequency(5)
                .stopWords(stopWords)
                .useAdaGrad(true)
                .workers(8)
                .epochs(10)
                .xMax(100)
                .batchSize(1000)
                .shuffle(true)
                .symmetric(true)
                .build();
</code></pre>
<p>大部分的参数信息和 word2vec 是类似的，比如 .layerSize(int layerSize) 都是表征词向量的维度，也都同样继承了 SequenceVectors 这个父类。其中，.alpah(double alpha) 和 .xMax(double xMax) 这两个参数取值是 0.75 和 100，这组数值参考了原论文中的结果，对应于原文公式中的 Xmax 和 alpha。</p>
<p><img src="https://images.gitbook.cn/1a68db90-13c7-11e9-a44b-95ffec9a2c37" alt="enter image description here" /></p>
<p>这个非线性变换函数是损失函数的一部分，不过根据论文中所描述的，整体模型效果对其依赖不是很大。我们也尝试过改变 alpha 和 Xmax，确实如原文中所说，模型输出基本不变。下面我们就训练一下 GloVe 模型并做一些测试：</p>
<pre><code>glove.fit();

System.out.println(glove.wordsNearest("孙少平", 5));
System.out.println(glove.wordsNearest("孙少安", 5));
System.out.println(glove.wordsNearest("田晓霞", 5));
</code></pre>
<p>模型输出的结果：</p>
<p><img src="https://images.gitbook.cn/aed0a690-fbcc-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>应该说，这个结果并不理想。和 word2vec 相比来看，还是有比较大的差别。很多词，如“门里门外”，在全文语料中出现的频次并不高。因此，想要得到更加合理的结果，除了参数调优以外，语料的预处理显得更加重要，有兴趣的同学可以自行调优模型结果。</p>
<h3 id="114">11.4 总结</h3>
<p>本次课程介绍了词分布式表达/词嵌入的两种实现算法 word2vec 和 GloVe。我们分别从原理和基于 Deeplearning4j 的实例构建两个方面来介绍这两种算法。需要指出的是，这两种算法都隶属于 Word Embedding 的范畴，但是 Word Embedding 并不等同于 word2vec 或者 GloVe 其中的一种或两种。Word Embedding 本身的实现方式可以非常多样化，基于监督学习和无监督学习都有相关的研究：监督学习的实现可以考虑全连接网络的方式，无监督学习则如本次课程介绍的两种方式，以及像 fastText 等相对较新的成果。在下一次的课程中，我们将会为大家介绍句的分布式表达建模工具，以及图嵌入（Graph Embedding）的一种实现算法。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://nlp.stanford.edu/pubs/glove.pdf">GloVe 介绍</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>