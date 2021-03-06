---
title: Deeplearning4j 快速入门-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本节课开始，我们将逐一介绍 Deeplearning4j 基于主流神经网络结构在分类、回归等机器问题上的实例应用。这一课将介绍多层感知机（MLP）在结构化数据集上构建分类和回归模型的例子。在给出具体的实例之前，先简单介绍下多层感知机的相关信息及特点。本节课核心内容包括：</p>
<ul>
<li>MLP 在分类问题中的应用</li>
<li>MLP 在回归问题中的应用</li>
</ul>
<h3 id="31">3.1 简介</h3>
<p>如果回顾神经网络的发展历史，早期的神经网络其实是没有隐藏层的（因此也更加谈不上什么深度神经网络或者深度学习），比如我们熟悉的感知机模型。1969 年，人工智能之父 Marvin Minsky 在其出版的《感知机》一书中以 XOR 问题为例谈到了这个浅层模型的局限性，即只能做线性的分类问题。虽然这一判断多少影响了 AI 的发展，但在另一方面上也促进了后期的包括神经网络、支持向量机等理论的不断完善。从神经网络这一分支来说，增加隐藏层以及非线性变换，成了解决感知机局限性的有效手段。此后，多层感知机逐渐进入大众的视野。</p>
<p>多层感知机（Multi-Layer Perceptron，MLP）或者说全连接网络（Full-Connected Network，FCN），通常是输入层、隐藏层、输出层的三层神经网络结构。相对于早期的感知机模型，隐藏层的引入（更本质的，其实是非线性变换的引入）可以不局限于线性分类问题，在理论上可以拟合任意的函数分布。MLP 中相邻两层神经元之间互相连接，网络结构清晰，易于理解。我们可以利用一些非线性激活函数（比如早期的 Sigmoid 和现在比较流行的 ReLU 等）对隐藏层输出进行非线性变换，以此提升模型抽象特征的能力。</p>
<p>目前神经网络的训练和预测主要依赖反向传播算法（BP 算法）和前向传播算法。MLP 同样可以采用这些算法（目前除了 MLP 以外，CNN、RNN 等网络均可采用 BP 算法或其变种，如 BPTT）进行训练和预测（在早期，当网络结构比较简单的时候，是可以通过人工调整参数进行训练的。不过，目前是绝对不会采用这样的方法，所以不做介绍了）。下面的部分我们将 MLP 分别应用到分类（<strong>Iris 鸢尾花分类问题</strong>）和回归（<strong>波士顿房价预测问题</strong>）两类机器学习问题中。</p>
<h3 id="32mlp">3.2 MLP 在分类问题中的应用</h3>
<p>分类问题是机器学习中的一类典型问题，基于分类的思想我们可以简化一些复杂的业务场景。例如，图像检索中图像分类可以帮助减少全量索引的扫描；自动对话系统中的文本分类可以明确对话所处的场景等。这里我们对经典的鸢尾花分类问题基于多层感知机进行建模。首先来介绍一些鸢尾花分类问题。</p>
<h4 id="321">3.2.1 鸢尾花数据集简介</h4>
<p>鸢尾花是广泛分布于温带的一种植物，在中国国内也种植有大量的鸢尾花，据<a href="https://baike.baidu.com/item/%E9%B8%A2%E5%B0%BE%E5%B1%9E/3459868?fr=aladdin&fromid=1401&fromtitle=%E9%B8%A2%E5%B0%BE%E8%8A%B1">百度百科——鸢尾花词条</a>中记录的信息表明，鸢尾花的种类有 13 种之多。</p>
<p><a href="https://archive.ics.uci.edu/ml/datasets/iris">鸢尾花数据集</a>是由 R. A. Fisher 收集的关于 3 种鸢尾花的开源数据集（Iris Setosa、Iris Versicolour 和 Iris Virginica），且每一个种类有 50 条记录。</p>
<p><img src="https://images.gitbook.cn/c5509240-f3a7-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" />
<img src="https://images.gitbook.cn/dcbb4ab0-f3a7-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" />
<img src="https://images.gitbook.cn/f1328cb0-f3a7-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>数据集中的每条记录共包含 4 个维度（萼片长度、萼片宽度、花瓣长度和花瓣宽度），部分数据集的截图如下：</p>
<p><img src="https://images.gitbook.cn/08619bb0-f3a8-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>需要注意的是，最后一列表示鸢尾花类别的例子是由文本写成的，因此为了方便之后训练数据集的构建，我们将最后一列统一替换成数字（用数字 0、1、2 分别标识三种类别的鸢尾花）。</p>
<p>在详细了解了鸢尾花数据集的相关信息后，就可以依据上一节课程中建议的步骤进行建模。</p>
<h4 id="322">3.2.2 鸢尾花数据集的读取</h4>
<p>在上一节课程中我们已经以鸢尾花分类问题为例，给出两种读取的方法。这里我直接采用“自行构建 DataSet 序列”的方案读取鸢尾花数据集（相关逻辑请参考上一节课程中的代码示例），然后将数据集切分成训练和验证数据集。</p>
<pre><code>/*--------------超参数常量声明------------------*/
final int batchSize = 3;
final long SEED = 1234L;
final int trainSize = 120;
/*--------------数据集构建------------------*/
List&lt;DataSet&gt; irisList = loadIrisSeq(new File("Iris-data-num.csv"));//该方法参考上一节课程的实现
DataSet allData = DataSet.merge(irisList);
allData.shuffle(SEED);
SplitTestAndTrain split = allData.splitTestAndTrain(trainSize);
DataSet dsTrain = split.getTrain();
DataSet dsTest = split.getTest();
DataSetIterator trainIter = new ListDataSetIterator(dsTrain.asList() , batchSize);
DataSetIterator testIter = new ListDataSetIterator(dsTest.asList() , batchSize);
</code></pre>
<p>简单解释一下上面的逻辑：</p>
<ul>
<li>首先从 CSV 文件中读取一共 150 条记录的鸢尾花数据集，将这些数据合并到一个 DataSet 中并且随机打乱顺序；</li>
<li>接着，我们利用内置的切分接口将全部数据切分成训练数据集和验证数据集（这里将 120 条数据作为训练数据，剩余的 30 条数据作为验证数据）；</li>
<li>最后，分别构建训练和验证数据集的迭代器对象。</li>
</ul>
<p>到此，数据的准备就完成了。</p>
<p>需要注意的是，由于鸢尾花数据集（包括接下来用到的波士顿房价数据集）的数据量很小，因此很多的操作（如数据集的读取、打乱、切分、重构）都可以在内存/显存上进行。当训练数据集量很大的时候，这样的操作其实是不合适的，容易导致存储溢出。</p>
<p>对于这个问题，我们可以采用内置的 AsyncDataSetIterator 进行处理，即数据是全量放在其他存储介质上，内存/显存里仅存储若干个 batchSize 的训练数据。当需要训练下一个批次的时候，从内存/显存中去取，同时以异步的方式再从存储介质上加载后续批次的数据，这样可以将有限的内存/显存用于参数的训练，而不是数据的存储。当然，这样做也有弊端，即每次从存储介质加载数据会不可避免地导致磁盘 I/O 或者网络 I/O，训练速度会有影响。</p>
<h4 id="323">3.2.3 鸢尾花数据集的建模与训练</h4>
<p>我们构建一个 4-2-3 结构的多层感知机网络对鸢尾花数据集进行建模。即输入层有 4 个神经元，代表鸢尾花 4 个维度的特征；隐藏层有 2 个神经元，代表非线性变换后实际用于分类的 high-level 的特征；输出层有 3 个神经元，代表共 3 种鸢尾花的分类类别。建模逻辑如下：</p>
<pre><code>public static MultiLayerNetwork model(){
        MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                        .seed(12345)
                        .iterations(1) // 如上所述训练迭代
                        .learningRate(0.01)
                        .weightInit(WeightInit.XAVIER)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .updater(Updater.ADAM)
                        .list()
                        .layer(0, new DenseLayer.Builder().activation(Activation.LEAKYRELU)
                                        .nIn(4).nOut(2).build())
                        .layer(1, new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                                            .activation(Activation.SOFTMAX)
                                        .nIn(2).nOut(3).build())
                        .backprop(true).pretrain(false);
        MultiLayerConfiguration conf = builder.build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        model.init();
        return model;      
}  
</code></pre>
<p>这里解释下里面的一些超参数。</p>
<table>
<thead>
<tr>
<th>超参数</th>
<th>物理含义</th>
</tr>
</thead>
<tbody>
<tr>
<td>.learningRate(0.01)</td>
<td>学习率</td>
</tr>
<tr>
<td>.weightInit(WeightInit.XAVIER)</td>
<td>神经网络权重初始化服从 XAVIER 分布</td>
</tr>
<tr>
<td>.optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)</td>
<td>优化算法使用随机梯度下降法</td>
</tr>
<tr>
<td>.updater(Updater.ADAM)</td>
<td>动量机制 ADAM</td>
</tr>
<tr>
<td>.iterations(1)</td>
<td>每一个 batch 迭代的次数</td>
</tr>
</tbody>
</table>
<p>表格里的这些参数都是针对整个网络而不仅仅是某一层，其中学习率参数可以根据需要设置成可变/可衰减。权重的初始化 Xavier 是比较常用的一种分布，当然其他诸如均匀分布的也可以选择。优化算法这里选用了 SGD，不过 Deeplearning4j 也提供了二阶的算法 L-BFGS 供开发者选择。动量的更新机制会帮助模型加快收敛速度，除了 Adam 还可以选择 AdaDelta、Nesterov、Adagrad、RMSProp 等。需要注意的是，在 Layer-0 中我们使用了 Leaky-ReLU 的激活函数，Leaky-ReLU 的函数形式： </p>
<p>$$f(x) = max(0, x) + alpha * min(0, x)$$</p>
<p><img src="https://images.gitbook.cn/3126f330-f3b0-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>在设置完超参数之后，建模这部分就基本完成了。接着，将之前已经读取的训练数据喂到模型中进行训练，具体逻辑如下：</p>
<pre><code>MultiLayerNetwork mlp = model();
mlp.setListeners(new ScoreIterationListener(1));    //loss score 监听器
for( int i = 0; i &lt; 20; ++i ){
     mlp.fit(trainIter);    //训练模型
     trainIter.reset();
     Evaluation eval = mlp.evaluate(testIter);    //在验证集上进行准确性测试
     System.out.println(eval.stats());
     testIter.reset();
}
</code></pre>
<p>训练这部分的逻辑比较简单。一般为了观察模型的收敛情况，我们会声明一个损失函数的监听器，用于在每次迭代后直观地显示当前损失函数的收敛情况。另外，在每一轮训练过后（示例代码中一共训练 20 轮），我们将会在验证集上测试当前轮次训练完后的模型分类准确率。</p>
<p><strong>Loss Score：</strong></p>
<p><img src="https://images.gitbook.cn/9fb73da0-f3b0-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p><strong>验证集上分类准确率评估：</strong></p>
<p><img src="https://images.gitbook.cn/b62e6e50-f3b0-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>如果觉得这样的方式还不够直观，我们可以使用 Deeplearning4j 内置的 UI 页面进行观察。<strong>将 JDK 版本切换到 1.8 并且加入如下逻辑</strong>：</p>
<pre><code>UIServer uiServer = UIServer.getInstance();
StatsStorage statsStorage = new InMemoryStatsStorage();
uiServer.attach(statsStorage);
mlp.setListeners(new StatsListener(statsStorage));
</code></pre>
<p>当开始训练后，我们在浏览器中键入 http://localhost:9000/train/overview，即可看到当前训练的情况。</p>
<p><img src="https://images.gitbook.cn/161b77e0-f3b1-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>到此，基于多层感知机的鸢尾花数据集的分类问题就算基本解决了。我们将原始的 150 条数据切分成 120:30 的训练和验证数据集，并最终在验证集上达到了 93% 左右的分类准确率。我们通过直接打印 Loss Score 和 UI 两种方式观察模型的收敛情况，尤其从 UI 页面上可以看到损失函数是一个振荡下降的走势，并逐步收敛。</p>
<h3 id="33mlp">3.3 MLP 在回归问题中的应用</h3>
<p>在这个部分中，我们将讨论基于多层感知机解决回归分析的问题，使用到的是<a href="http://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html">波士顿房价数据集</a>。首先介绍下这个数据集的相关信息。</p>
<h4 id="331">3.3.1 波士顿房价数据集简介</h4>
<p>波士顿房价数据集采集于 1970 年，主要记录的是波士顿郊区城镇的房价。全部数据集共 506 条记录，每条记录含有 14 个字段，每个字段的含义如下：</p>
<table>
<thead>
<tr>
<th>字段名称</th>
<th>物理含义</th>
</tr>
</thead>
<tbody>
<tr>
<td>CRIM</td>
<td>小镇人均犯罪率</td>
</tr>
<tr>
<td>ZN</td>
<td>面积超过 25000 平方英尺的住宅用地比例</td>
</tr>
<tr>
<td>INDUS</td>
<td>每个小镇上非零售/商业用地的比例</td>
</tr>
<tr>
<td>CHAS</td>
<td>查尔斯河虚拟变量（如果河流管制，则为 1；否则为 0）</td>
</tr>
<tr>
<td>NOX</td>
<td>一氧化碳指标（每千万英尺）</td>
</tr>
<tr>
<td>RM</td>
<td>每一栋房子的房间数</td>
</tr>
<tr>
<td>AGE</td>
<td>1940 年以前建造的自住单位比例</td>
</tr>
<tr>
<td>DIS</td>
<td>到波士顿五个就业中心的加权距离</td>
</tr>
<tr>
<td>RAD</td>
<td>距离高速公路的方便指数</td>
</tr>
<tr>
<td>TAX</td>
<td>每 10000 美元的财产税率</td>
</tr>
<tr>
<td>PTRATIO</td>
<td>城镇上的师生比例</td>
</tr>
<tr>
<td>B</td>
<td>1000*(Bk-0.63)^2，其中 Bk 指代城镇中黑人的比例</td>
</tr>
<tr>
<td>LSTAT</td>
<td>人口减少的百分比</td>
</tr>
<tr>
<td>MEDV</td>
<td>自住房的中位数房价，以千美元计</td>
</tr>
</tbody>
</table>
<p>一般地，我们将最后一个变量（MEDV）作为预测的对象，即前面 13 个字段构成特征。需要注意的是，对于 MEDV 字段的值等于 50 的记录，我们将作为异常值先行剔除（由于所有记录中最高的值就是 50，明显高于其他记录该字段的值并且重复出现了 16 次之多，很有可能是异常数据，因此我们将这 16 条记录剔除）。因此实际使用训练数据为 490 条记录，其中 400 条作为训练数据，90 条作为验证数据。</p>
<h4 id="332">3.3.2 波士顿房价数据集的读取</h4>
<p>首先和之前分类的例子类似，我们先从文本文件中读取训练和验证数据集并构建迭代器。</p>
<pre><code>public static List&lt;DataSet&gt; loadHousePrice(File file) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line = null;
        List&lt;DataSet&gt; totalDataSetList = new LinkedList&lt;DataSet&gt;();
        while( (line = br.readLine()) != null ){
            String[] token = line.split(",");
            double[] featureArray = new double[token.length - 1];
            double[] labelArray = new double[1];
            for( int i = 0; i &lt; token.length - 1; ++i ){
                featureArray[i] = Double.parseDouble(token[i]);
            }
            labelArray[0] = Double.parseDouble(token[token.length - 1]);
            //
            INDArray featureNDArray = Nd4j.create(featureArray);
            INDArray labelNDArray = Nd4j.create(labelArray);
            totalDataSetList.add(new DataSet(featureNDArray, labelNDArray));
        }
        br.close();
        return totalDataSetList;
}
</code></pre>
<p>简单做一下解释：我们还是按行读取记录并且将最后一列特征，也就是 MEDV 作为预测标签，其余的 13 列数据作为特征。我们为每条训练数据构建一个 DataSet 并将总共 490 条数据放入一个链表中。需要注意的是，这个案例我们做的是回归问题，因此预测的值是连续的。</p>
<h4 id="333">3.3.3 波士顿房价预测问题的建模</h4>
<p>我们先给出神经网络建模的逻辑：</p>
<pre><code>public static MultiLayerNetwork model(){
        MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                        .seed(12345L)
                        .iterations(1) 
                        .updater(Updater.ADAM)
                        .weightInit(WeightInit.XAVIER)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .list()
                        .layer(0, new DenseLayer.Builder().activation(Activation.LEAKYRELU)
                                        .nIn(13).nOut(10).build())
                        .layer(1, new OutputLayer.Builder(LossFunctions.LossFunction.MEAN_SQUARED_LOGARITHMIC_ERROR)
                                        .activation(Activation.IDENTITY)
                                        .nIn(10).nOut(1).build())
                        .backprop(true).pretrain(false);
        MultiLayerConfiguration conf = builder.build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        model.init();
        return model;      
}
</code></pre>
<p>这里依然基于多层感知机建模并且构建了一个三层（仅含有一层隐藏层）的网络，超参数的物理含义在上面分类的问题中已经做了解释，这里不再赘述。需要注意的是，输出层我们配置单个神经元用于预测房价的具体数值，请大家注意和分类模型的差别，另外损失函数我们使用了 MEAN_SQUARED_LOGARITHMIC_ERROR（MSLE，均方对数误差）。具体的损失函数的定义为：</p>
<p>$$L = 1/N sum_i (log(1+predicted_i) - log(1+actual_i))^2$$</p>
<p>其中，$N$ 为所有记录的数量，对所有的记录预测值取对数，并与真实值的对数值的差值取平方后累加，最后再平均误差。此外，同样可以选择其他的损失函数，比如 Mean Squared Error（MSE）、Mean Absolute Error（MAE）等，具体的内容读者可以自行查询相关资料并做实际尝试。</p>
<p>与之前的分类模型类似，我们将全量的记录分为 400 条训练数据集和 90 条验证数据集。先来看下完整的训练和预测逻辑。</p>
<pre><code>final int batchSize = 4;
final long SEED = 1234L;
final int trainSize = 400;
List&lt;DataSet&gt; housePriceList = loadHousePrice(new File("house_price.csv"));
//获取全部数据并且打乱顺序
DataSet allData = DataSet.merge(housePriceList);
allData.shuffle(SEED);
//划分训练集和验证集
SplitTestAndTrain split = allData.splitTestAndTrain(trainSize);
DataSet dsTrain = split.getTrain();
DataSet dsTest = split.getTest();
DataSetIterator trainIter = new ListDataSetIterator(dsTrain.asList() , batchSize);
DataSetIterator testIter = new ListDataSetIterator(dsTest.asList() , batchSize);
//归一化处理
DataNormalization scaler = new NormalizerMinMaxScaler(0,1);
scaler.fit(trainIter);
scaler.fit(testIter);
trainIter.setPreProcessor(scaler);
testIter.setPreProcessor(scaler);
//声明多层感知机
MultiLayerNetwork mlp = model();
mlp.setListeners(new ScoreIterationListener(1));
//训练 200 个 Epoch
for( int i = 0; i &lt; 200; ++i ){
    mlp.fit(trainIter);
    trainIter.reset();
}
//利用 Deeplearning4j 内置的回归模型分析器进行模型评估
RegressionEvaluation eval = mlp.evaluateRegression(testIter);
System.out.println(eval.stats());
testIter.reset();
//输出验证集的真实值和预测值
System.out.println(testIter.next(testIter.totalExamples()).getLabels());
System.out.println();
testIter.reset();
System.out.println(mlp.output(testIter));
testIter.reset();
</code></pre>
<p>这里有两点需要注意：</p>
<ol>
<li>我们使用了 DataVec 内置的归一化工具对特征数据进行了预处理；</li>
<li>评估回归模型的方法和分类是不同的，具体这里，我们需要调用 evaluateRegression 这个方法。</li>
</ol>
<p>在正常完成训练的前提下，会得到类似如下结果：</p>
<p><img src="https://images.gitbook.cn/79e7e910-f3b2-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>截图中上面几行是 Loss 值的一些信息，最后一行则是我们调用 evaluateRegression 的评估方法获得的验证集在不同评估指标下的平均值。另外将最后一部分，也就是打印验证集合的预测值和真实值的结果在 Excel 里绘图进行直观呈现：</p>
<p><img src="https://images.gitbook.cn/2dc34990-fc26-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>可以看到一共 90 条验证数据，预测值基本可以反映真实数据的变化趋势，但是拟合的程度还有待进一步调优，个别预测值和真实值还有较大的差别。</p>
<h3 id="34">3.4 小结</h3>
<p>最后，对本节课涉及的内容做个简单的小结。本次课程的内容主要是基于多层感知机/全连接网络构建分类和回归模型，分别采用了鸢尾花数据集和波士顿房价数据集。我们尽量采用 Java 原生态的语言特性对数据进行预处理以及数据集的构建，当然依赖于 DataVec 里的工具会更加方便。比如，在鸢尾花数据集的获取中，其实可以直接使用 Deeplearning4j 内置的 IrisDataSetIterator 或者 CSVRecordReader 来对数据集进行处理，但无论采用哪种方式，只要可以直观并正确地构建数据集就可以了。</p>
<p>对于分类问题，在后续的课程会多次遇到（如图像和文本的分类），除了多层感知机，我们可以采用更加复杂的网络结构来达到这一目的，而对于回归问题同样不仅限于 MLP 这一种结构。</p>
<p>对于多层感知机本身，它的优点在于结构简单、清晰、易于理解。但缺点也有很多，比如全连接的特性往往导致参数量会很大，另外 MLP 无法很好地获取空间以及时序的特征也局限了它的应用场景，当然这在后续卷积神经网络（CNN）和循环神经网络（RNN）的课程中会加以讨论和解决。总的来说，全连接网络依然是一种非常经典的神经网络结构，很多应用场景中也都可以使用得到。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://baike.baidu.com/item/%E9%B8%A2%E5%B0%BE%E5%B1%9E/3459868?fr=aladdin&fromid=1401&fromtitle=%E9%B8%A2%E5%B0%BE%E8%8A%B1">百度百科——鸢尾花词条</a></li>
<li><a href="https://archive.ics.uci.edu/ml/datasets/iris">鸢尾花数据集</a></li>
<li><a href="http://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html">波士顿房价数据集</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>