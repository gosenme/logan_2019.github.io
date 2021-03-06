---
title: Deeplearning4j 快速入门-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一次的课程中，我们为大家介绍了词嵌入的两种算法：word2vec 和 GloVe。我们以实例的方式给出了 Deeplearning4j 的应用构建方式及部分实验结果。本次课程我们将以同样的方式为大家介绍句向量的建模工具——doc2vec/paragraph2vec，以及图嵌入的算法 DeepWalk。首先我们来看下doc2vec的原理和实例构建方式。本节课核心内容包括：</p>
<ul>
<li>doc2vec 的原理与建模</li>
<li>DeepWalk 的原理与建模</li>
</ul>
<h3 id="121doc2vec">12.1 doc2vec 的原理与建模</h3>
<p>上节课两个部分介绍的都是词维度的向量表示方法，其实在很多时候整个序列或文本段落的向量表达是更加重要和有意义的。这里给大家介绍的就是 Deeplearning4j 实现的 doc2vec 模型。</p>
<p>doc2vec，或者更准确地说，在 Deeplearning4j 中叫做 ParagraphVectors 类的实现，可以实现文本段落的向量化表示。其实在介绍完上面的词向量后，文本段落向量的表达就可以基于词向量来做。比如，将一段文本序列中所有词向量进行累和求平均就是一种很常用的策略。当然，也可以将这些具有相同维度的向量拼接成一个矩阵，这些都可以作为序列或者说文本段落向量的表示方式。那么另一种方式，其实就是直接构建一个模型来获取段落向量的表示。</p>
<p>Deeplearning4j 的 ParagraphVectors 是基于 word2vec 的作者 Mikolov 的另一篇论文 <a href="https://cs.stanford.edu/~quocle/paragraph_vector.pdf"><em>Distributed Representations of Sentences and Documents</em></a> 来实现的。在这篇文章中，作者大量借鉴了 word2vec 的建模思想，提出了 PV-DM 和 DBOW 两种模型。</p>
<p>下面先看下从原论文中截取的示意图：</p>
<p><strong>PV-DM（Distributed Memory Model of Paragraph Vectors）：</strong></p>
<p><img src="https://images.gitbook.cn/FjasNmXEoNNlBOnUIhwiYx0Mhrt-" alt="avatar" /></p>
<p><strong>DBOW（paragraph vector with distributed bag of words）：</strong></p>
<p><img src="https://images.gitbook.cn/ba708df0-1b46-11e9-8448-3921c043358a" alt="enter image description here" /></p>
<p>PV-DM 的思想是将段落向量和词向量通过某种方式拼接后预测句子中的某个词，而 DBOW 的思想则是更加的直接，将段落向量作为输入直接连接到分类器进行各个词的预测。应该说前者比较接近与 word2vec 中的 CBOW，而后者则是更加接近与 Skip-Gram。实现的思想并不复杂，那么下面我们就来看下基于 Deeplearning4j 是如何建模的。首先看下如下建模逻辑：</p>
<pre><code>ParagraphVectors vec = new ParagraphVectors.Builder()
                .minWordFrequency(1)
                .iterations(20)
                .epochs(1)
                .layerSize(128)
                .learningRate(0.01)
                .labelsSource(source)
                .windowSize(8)
                .workers(8)
                .iterate(iter)
                .useAdaGrad(true)
                .sequenceLearningAlgorithm(new DBOW&lt;VocabWord&gt;())
                .negativeSample(1.0)
                .trainWordVectors(false)
                .trainSequencesRepresentation(true)
                .vocabCache(cache)
                .tokenizerFactory(t)
                .sampling(0)
                .build();
</code></pre>
<p>参数看似很多，但是实际很多是默认的，我们可以不设置。这里主要解释几个重要的参数。</p>
<pre><code>.sequenceLearningAlgorithm(SequenceLearningAlgorithm&lt;VocabWord&gt; algorithm)    //选择 PV-DM 还是 DBOW 作为实现的算法，一般来讲 DBOW 的效果较好
.sampling(double sampling)    //这个参数如果大于 0，则会采用抽样的形式抽取词，等于 0 则不会
.labelsSource(LabelsSource source)    //段落标记的实例对象作为入参。实际建模时，我们会给每个段落文本分配一个 id，相关的信息则存储在 LabelsSource 的实例对象中
.trainWordVectors(boolean trainElements)
.trainSequencesRepresentation(boolean trainSequences)    //这两个参数可以根据实际情况设置，如果你需要训练句子向量，则后者一定要设置成 true
</code></pre>
<p>我们仍然对于《平凡的世界》这本书的文字进行建模。只不过这次我们关注的是句子/段落向量的表达。</p>
<pre><code>File file = new File("corpus.txt");
        SentenceIterator iter = new BasicLineIterator(file);

        AbstractCache&lt;VocabWord&gt; cache = new AbstractCache&lt;&gt;();

        TokenizerFactory t = new DefaultTokenizerFactory();
        t.setTokenPreProcessor(new CommonPreprocessor());

        LabelsSource source = new LabelsSource("DOC_");
        //同上面的建模逻辑
        //...
        vec.fit();  //vec由上面逻辑声明
        Collection&lt;String&gt; docs = vec.nearestLabels("李向前  闭住  眼睛  ，  让  汹涌  的  泪水  在  脸颊  上  溪流  般地  纵情  流淌 ", 5);

        for( String doc : docs ){
            final int docID = Integer.parseInt(doc.split("_")[1]);
            int id = 0;
            LabelAwareIterator labelIter = vec.getLabelAwareIterator();
            labelIter.reset();
            while( labelIter.hasNextDocument() ){
                LabelledDocument next = labelIter.nextDocument();
                if( id == docID  ){
                    System.out.println("similar sentence: ");
                    System.out.println(next.getContent());
                    break;
                }else{
                    ++id;
                }
            }
}
</code></pre>
<p>首先我们读取语料，并且将每一行的文本/句子作为一个 document。我们声明一个 LabelsSource 的实例，作用是给每个句子一个 id 表示。训练的逻辑很简单，就不多描述了。最后我们做了一个应用，就是根据训练好的模型，召回和示例句子相似语义的 5 个句子。我们先来看下结果：</p>
<p><img src="https://images.gitbook.cn/158782f0-fbcd-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>我们一定召回了 5 个和待预测句子语义相近的句子。从这些句子的含义可以相对直观地看到，这些句子基本都表达着类似的心情，也就是说它们的语义层面的含义比较接近。这是一个比较有意思的应用，可以召回一些句意相近的文本，这和 word2vec 可以召回相似词的应用其实是类似的。</p>
<p>最后我解释下预测的那段逻辑。</p>
<p>首先我们使用接口 nearestLabels 返回相似句子的 id，遍历这个 id 集合，从字符串中截取数值 id，之后从句子迭代器中获取对应数字 id 的文本，然后打印到控制台。整个过程不是非常直接，尤其需要注意的是，nearestLabels 返回的是相似句子的 id，而不是直接的文本结果。另外很多时候，我们需要从模型中获取句子的向量表达式，可以调用 inferVector 接口来实现。具体就不在这里展开了。</p>
<h3 id="122deepwalk">12.2 DeepWalk 的原理与建模</h3>
<p>最后一个小部分给大家介绍下 Graph Embedding 的一种实现方式：DeepWalk。</p>
<p>DeepWalk 的核心思想是基于 Random Walk 算法，从以图结构存储的数据中发现与某节点有关系的其他节点，并以此作为上下文数据放到 Skip-Gram 的框架中，从而可以达到对节点编码的目的。一旦节点可以用低维度向量表示后，那么更多应用都可以基于此进行展开，图的关系得到高效转化。</p>
<p>需要注意的是，使用 Deeplearning4j 中的 DeepWalk 算法需要引入相关依赖：</p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
    &lt;artifactId&gt;deeplearning4j-graph&lt;/artifactId&gt;
    &lt;version&gt;${dl4j.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>基于图的挖掘有很多典型的应用，比如社交网络中的链路预测、好友推荐等。这里我们给出一个基于 Deeplearning4j 内置 DeepWalk 算法的好友推荐的简单应用。</p>
<p>我们先看下这份数据：</p>
<p><img src="https://images.gitbook.cn/e4229820-fbcd-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>这是一份我为自己造的篮球运动员的关联图结构数据。注意，我这里并没有涉及权重，只涉及节点。这个对最终好友推荐是有影响的，有兴趣的同学可以添加上权重后再测试。</p>
<p>这份数据一共分为两列，From/To 分别代表发射节点和接收节点。由于一共有 11 个不同的人名，所以转换成图结构后就一共有 11 个不同节点。我们的目的是为其中一个运动员推荐认识其他的运动员。</p>
<p>我们首先做数据的预处理，将人名转化成数字。需要注意的是，转化后代表人名的数字索引是从 0 开始的。大概逻辑可以参考如下：</p>
<pre><code>private static final String delim = "\t";
private static String format = "%s:%s\n";

public static BiMap&lt;String,Integer&gt; constructGraph(String fileName) throws FileNotFoundException, IOException{
        BiMap&lt;String,Integer&gt; vertextId = HashBiMap.create();
        int idx = -1;
        List&lt;String&gt; numFromTos = new ArrayList&lt;&gt;();
        try(BufferedReader br = new BufferedReader(new FileReader(new File(fileName)))){
            String line;
            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(delim);
                String from = tokens[0];
                String to = tokens[1];
                if( !vertextId.containsKey(from) )vertextId.put(from, ++idx);
                if( !vertextId.containsKey(to) )vertextId.put(to, ++idx);
                String numFromTo = vertextId.get(from) + delim + vertextId.get(to);
                numFromTos.add(numFromTo);
            }
        }
        //
        try(PrintWriter pw = new PrintWriter("graphNum.txt")){
            for( String fromto : numFromTos )pw.println(fromto);
        }
        //
        return vertextId;
}
</code></pre>
<p>这段逻辑比较清晰，主要是为人名创建了一个对应数字索引的映射，并且用了 Guava 里的 BiMap，这样方便以后根据数字索引取出中文人名。然后重要的一步是，将原来用人名构成的文件，转换成数字索引表示的文件。这些预处理工作完成后，我们就可以开始训练 DeepWalk 的模型。</p>
<pre><code>public static void main(String[] args) throws IOException {
        BiMap&lt;String,Integer&gt; bimapNameId = constructGraph("graph.txt");
        //
        Graph&lt;String, String&gt; graph = GraphLoader.loadUndirectedGraphEdgeListFile("graphNum.txt",bimapNameId.size(),delim);
        DeepWalk&lt;String,String&gt; dw = new DeepWalk.Builder&lt;String,String&gt;()
                                                .learningRate(0.01)
                                                .vectorSize(64)
                                                .windowSize(4)
                                                .build();
        dw.fit(graph, 3);
        //
        int[] num = dw.verticesNearest(bimapNameId.get("姚明"), 3);
        for( int n : num ){
            System.out.printf(format, bimapNameId.inverse().get(n), dw.similarity(1, n));
        }
}
</code></pre>
<p>我们利用 GraphLoader 这个工具类中的静态方法加载那个数字索引的图文件，然后声明 DeepWalk 的实例，并设置相应的参数，就可以训练模型了。我们最后为“姚明”推荐了三个可能的好友，并且打印出相似度到控制台。看下结果：</p>
<p><img src="https://images.gitbook.cn/75e3fab0-fbce-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>在结果里，王治郅和孙悦是已经在原始数据中存在的好友，但是马布里是新好友。当然实际应用中，我们可以有更多的后续处理工作，但这个案例基本实现了一个简单的基于图嵌入的好友推荐。</p>
<p>最后需要说明的是，另一种图嵌入的算法 node2vec 也已经在实现中，和 DeepWalk 的思想基本类似，但在游移算法上有区别，有兴趣的同学可以关注 Deeplearning4j 每次的版本更新。</p>
<h3 id="123">12.3 总结</h3>
<p>这两节课主要介绍了词/句的分布式表达及向量化表示的一些经典算法和案例。我们从基本原理到基于 Deeplearning4j 框架建模进行了比较详细的描述，希望可以对有需要借助于这些算法的同学有所启发。除了可以基于框架来完成实例构建外，我们需要对 Embedding 的思想有进一步的了解，以及在什么场景适用 Embedding、什么场景不适用都要有比较清晰的认识。</p>
<p>对于文本的向量化表示其实由来已久，但是早期的特征构建都比较简单粗暴，并且有高维灾难、上下文信息缺失等问题。向量化表示可以有效降低特征维度，并且由于这些向量表示了文本潜在的语义，因此基于这些信息构建其他应用将十分有用。但也必须指出的是在工业界落地的时候，我们不能仅通过优化算法的方式来提升产品的各项指标，在很多时候数据的质量可能会更为重要些，因此当有同学遇到在实际工程中上述某种算法效果不好的时候，不要着急更换算法和模型，而是应该冷静分析各种方面的原因，避免在算法选择上做无用功。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://cs.stanford.edu/~quocle/paragraph_vector.pdf"><em>Distributed Representations of Sentences and Documents</em></a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>