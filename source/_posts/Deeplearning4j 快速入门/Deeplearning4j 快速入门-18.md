---
title: Deeplearning4j 快速入门-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本次课程我们为大家介绍一种新的构建模型方式——迁移学习（Transfer Learning）。迁移学习是解决标注数据缺失、从已有模型快速构建新应用的有效手段。迁移学习旨在于不同领域之间进行经验、知识、技能的转移，无需每次都从头学习全新的知识。目前，基于神经网络的迁移学习已经在图像、文本等领域取得了很多的研究成果，在工业界也有落地，本次课程我们在介绍迁移学习相关理论的基础上，结合 Deeplearning4j 对迁移学习的支持场景给出在图像分类问题中的实例。本节课核心内容包括：</p>
<ul>
<li>迁移学习简介</li>
<li>为什么要做迁移学习</li>
<li>基于 Deeplearning4j 的迁移学习</li>
</ul>
<p>首先我们来看下迁移学习的相关介绍。</p>
<h3 id="161">16.1 迁移学习简介</h3>
<p>在现实生活中，我们经常需要通过类比的手段，根据已经掌握的技能来学习新的知识。举些具体的例子，会打乒乓球的人通过简单的学习，就可以比较快地掌握网球的打法，会编写 C++ 程序的程序员可能在一周以内就可以掌握 Java 的基本语法。</p>
<p><img src="https://images.gitbook.cn/631d99a0-38ae-11e9-b713-3b5d5fbed932" alt="enter image description here" /></p>
<p>诸如此类的案例不胜枚举。它们的一个共同点就是借助了知识或者技能迁移的手段。乒乓球和网球不仅是在英文表达上只差了一个 table 单词，更多的是在它们的击球节奏、球的弹跳规律、运动场地和击球工具等多项关键细节上都有些相似。而不论是 Java 还是 C++，面向对象、基本数据类型等语言特性都非常相像，因此知识的迁移就很自然了。</p>
<p>在人工智能领域，我们希望也可以借鉴人类的学习方式，以某种手段完成从源领域（Source Domain）到目标领域（Target Domain）的迁移学习。比如用户评价的情感识别，我们可以从电商领域迁移到视频、文字阅读等其他领域；机器翻译系统，我们可以从英语/德语这个领域迁移到法语/英语等其他领域。</p>
<p>目前迁移学习的实现方法主要有四种：</p>
<ul>
<li>样本迁移</li>
<li>特征迁移</li>
<li>模型迁移</li>
<li>关系迁移</li>
</ul>
<p>样本迁移的核心在于源领域的样本复用，即源领域和目标领域有部分相似或者说源领域可做迁移的样本，这些样本在目标领域的建模中得到复用。</p>
<p>特征迁移的思想在于找到可以共享于源领域和目标领域的特征。</p>
<p>模型迁移，同时也可以称作是参数迁移的核心思想，在目标领域建模的过程中不需要从头训练所有参数，而是从源领域中迁移部分已经训练好的超参数过来，目标领域只训练部分新的参数。模型迁移其实是目前深度神经网络中使用较多的一种迁移学习方式，具体实现的时候，工程师只需要“冻结”大部分神经网络层的参数并且只训练小部分参数即可。</p>
<p>最后一种，相关性迁移或者说关系迁移旨在不同领域之间迁移关系的内容，典型的是社交网络关系的迁移。</p>
<h3 id="162">16.2 为什么要做迁移学习</h3>
<p>第一部分我们简单介绍了迁移学习的基本内容和定义，在这一部分我们将讨论为什么要进行迁移学习，或者说迁移学习的价值所在。</p>
<p><strong>首先，迁移学习可以比较有效地解决标注数据缺失的问题。</strong>目前，很大一部分工业界的算法产品必须依赖监督学习进行。换句话说，样本的标注至关重要。样本的标注可以结合业务、算法等多种手段进行，但为了保证标注的质量，人工的介入依然是不可缺少的。可是，大量样本的人工标注所消耗的人力、物力成本极高，并且如果每一个项目都这样标注的话，时间成本也是很大的。因此，是否可以在较小的样本集上同样构建一个产品级的应用，从而降低各种成本和风险，这成为算法工程师研究和追求的新领域。</p>
<p>迁移学习提供了这样一种解决方案。举例来说，我们可以将很多在大数据集上预训练好的模型通过模型迁移的手段，使其适用于我们自身的业务。例如在 ImageNet 数据集上预先训练好的 VGG 网络，虽然无法直接应用于具体的业务场景上，但我们通过少量标注样本重新训练模型的部分参数，从而将模型迁移到具体的业务中。从这个角度来说，我们只需要标注业务中的少量样本并且训练 VGG 模型中的部分参数即可完成业务建模。无论是标注样本的数量，还是需要训练的参数量都大大减少。这便是迁移学习所带来的快速建模的好处。</p>
<p><strong>其次，迁移学习可以比较有效地解决冷启动问题和个性化问题。</strong>从本质上说，这两个问题依然可以归为数据缺失的问题中。对于诸如推荐中的冷启动问题，即完全没有行为记录的一些用户，我们可以通过样本迁移、关系迁移等手段，为其在其他领域找到可以描述该用户的行为特征，并迁移到当前推荐的实际场景中，从而在一定程度上解决冷启动问题。</p>
<p>需要指出的是，迁移学习目前确实可以在一定程度上解决诸如标注数据缺失所带来的问题，但是依赖迁移学习建模的应用和基于完全标注样本训练的模型相比，在各项模型的评估指标上还是可能会存在一些差距，甚至出现<strong>负迁移</strong>（Negative Transfer）的问题。负迁移指的是，在完成某种形式的迁移学习后，目标领域的建模效果并没有达到预期，甚至在各项指标上远低于完全标注样本训练的模型。从本质上讲，负迁移的出现很可能是源领域和目标领域的样本数据并未服从同一分布，换句话说是两个相关程度并不高的任务。例如，乒乓球的运动经验可以迁移到网球，但是篮球的技术很难迁移到网球。而在实际应用的过程中，如何事先通过一些手段评估迁移的有效性，将成为迁移学习是否成功的决定性因素，而不是等完成模型的迁移后再来评估。目前，很多迁移学习的任务依然依赖于人的经验和一些简单的数据统计，因此如何有效迁移将成为迁移学习的研究和应用重点。</p>
<p>下面的部分我们将基于 Deeplearning4j 给出深度学习在迁移学习方面的一个实例。</p>
<h3 id="163deeplearning4j">16.3 基于 Deeplearning4j 的迁移学习</h3>
<p>Deeplearning4j 从 0.8.0 版本开始支持迁移学习。在这个部分，我们尝试加载已经在 ImageNet 数据集上预训练好的 VGG-16 模型并尝试迁移到特定的 5 种花卉（daisy、dandelion、roses、sunflowers、tulips）分类问题上。数据集链接地址如下：</p>
<blockquote>
  <p><a href="http://download.tensorflow.org/example_images/flower_photos.tgz">http://download.tensorflow.org/example_images/flower_photos.tgz</a></p>
</blockquote>
<p>根据第二部分中提到的迁移学习的几种方式，目前 Deeplearning4j 支持的是模型迁移，或者也可以称作为参数迁移。主要的 API 集中在下面截图中的三个工具类中：</p>
<p><img src="https://images.gitbook.cn/8af348b0-38b0-11e9-9be9-e5a41eccf0a0" alt="enter image description here" /></p>
<p>其中 FineTuneConfiguration 类用于配置迁移学习模型涉及的一些超参数配置，TransferLearningHelper 主要用于“记忆”部分网络层的输出并支持持久化到磁盘，TransferLearning 则作为迁移学习的主要工具类支持参数迁移后的模型训练和预测等工作。</p>
<p>在给出具体的案例之前，我们先给出迁移学习建模的主要步骤：</p>
<ul>
<li>读取预训练好的神经网络模型；</li>
<li>基于 FineTuneConfiguration 类实例化配置项参数，例如学习率和优化器等；</li>
<li>基于 TransferLearning 工具类声明迁移模型实例对象，并配置需要 Fine-tune 的网络层；</li>
<li>读取数据并且训练模型，此步骤和之前课程中介绍的模型训练步骤一致。</li>
</ul>
<p>需要指出的是，TransferLearningHelper 并不是必须的，实际的使用可以视具体情况而定。下面我们给出基于 VGG-16 网络从 ImageNet 数据集预训练的模型迁移到花卉分类问题上的实例。按照上面步骤，我们首先读取预训练好的 VGG 网络，并打印网络结构信息到控制台进行查看。</p>
<pre><code>import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
... ...
ComputationGraph vgg16 = KerasModelImport.importKerasModelAndWeights("VGG16.json", "vgg16_weights_th_dim_ordering_th_kernels.h5", false);
System.out.println(vgg16.summary());
</code></pre>
<p>通过控制台我们可以看到 VGG-16 的网络结构：</p>
<p><img src="https://images.gitbook.cn/c2f231d0-38b1-11e9-b713-3b5d5fbed932" alt="enter image description here" /></p>
<p><strong>这里我们解释下模型的读取过程。</strong>我们首先将 KerasModelImport 这个工具类引入，目的是将在 Keras 框架下已经训练好的 VGG-16 模型的结构和参数两个文件 load 到内存中。Deeplearning4j 支持导入 Keras、TensorFlow 框架下训练好的模型，这个在后面的课程中我们会单独进行讲解，这里我们直接导入 Keras 预训练好的 VGG-16 模型并打印网络结构和参数信息到控制台（注：上面逻辑中涉及到的 JSON 和 H5 文件的链接会附在最后，有需要的同学可以自行下载）。</p>
<p>在导入完模型之后，我们声明 FineTuneConfiguration 实例进行超参数的相关配置。具体逻辑如下：</p>
<pre><code>FineTuneConfiguration fineTuneConf = new FineTuneConfiguration.Builder()
                                                .learningRate(3e-5)
                                                .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                                                .updater(Updater.ADAM)
                                                .seed(seed)
                                                .build();
</code></pre>
<p>这个部分和之前课程中的对网络超参数的设置是类似的，这里就不多做解释了，不明白的同学可以参考前面的课程。紧接着，我们声明迁移学习模型实例并做相关配置：</p>
<pre><code>ComputationGraph vgg16Transfer = new TransferLearning.GraphBuilder(vgg16)
                                                .fineTuneConfiguration(fineTuneConf)
                                                .setFeatureExtractor("fc2") 
                                                .removeVertexKeepConnections("predictions") 
                                                .addLayer("predictions",
                                                    new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                                                        .nIn(4096).nOut(5)
                                                        .weightInit(WeightInit.DISTRIBUTION)
                                                        .activation(Activation.SOFTMAX).build(),
                                                    "fc2")
                                                .build();
System.out.println(vgg16Transfer.summary());
</code></pre>
<p>我们先来看下控制台的输出结果，再对以上配置做解释。</p>
<p><img src="https://images.gitbook.cn/34df14c0-38b2-11e9-b713-3b5d5fbed932" alt="enter image description here" /></p>
<p>在这次的网络详情中，我们可以清楚地看到，除了 predictions 这层以外，其余所有的网络层都带上了 Frozen 的字样，即可以训练的其实只有 predictions 这一层，其余网络层的参数都被“冻结”了。可以被训练的参数是 4096*5=20485 个。</p>
<p>对比初始加载的 VGG-16 网络，最后一层的输出有 1000 个神经元，而为了适应新的分类场景，我们通过简单调整输出层的网络结构（主要是输出层的神经元个数），并重新训练这部分参数来达到模型迁移的目的。大部分的参数被冻结不需要被重新训练，这就是在第二部分中我们提到的，<strong>基于少量新的标注数据训练少量模型参数</strong>。</p>
<p>这个配置其实是基于 TransferLearning 这个工具类来实现的。通过 TransferLearning 构建 ComputationGraph 实例的过程中，我们将第一步导入的原始 VGG-16 实例和迁移配置参数，作为入参覆盖迁移模型的默认配置，并且通过 .setFeatureExtractor 接口来配置需要冻结的网络层。在实例中，我们设置“fc2”网络层以下的参数全部冻结，即从“input_2 -&gt; block1_conv1  -&gt; ...... -&gt; fc1”这些网络层参数不参与迁移学习的网络训练。</p>
<p>另外，为了适应新的分类场景，我们需要通过 .removeVertexKeepConnections 来移除输出层并且通过 .addLayer 添加符合新场景的输出层网络。到此，我们在 ImageNet 数据集预训练好的 VGG-16 网络上做了符合目标源的网络修改。</p>
<p>最后需要做的就是，在目标源的少量标注数据上训练这 20485 个参数，就完成了一个简单的迁移学习。我们同样也给出模型训练的逻辑：</p>
<pre><code class="     language-    ">int trainPerc = 60;
int batchSize = 8;
FlowerDataSetIterator.setup(batchSize,trainPerc);
DataSetIterator trainIter = FlowerDataSetIterator.trainIterator();
DataSetIterator testIter = FlowerDataSetIterator.testIterator();

final int numEpoch = Integer.parseInt(args[0]);    //实际设置为50
for( int i = 0; i &lt; numEpoch; ++i ){
            vgg16Transfer.fit(trainIter);
            testIter.reset();
        }
Evaluation eval = vgg16Transfer.evaluate(testIter); 
System.out.println(eval.stats());
</code></pre>
<p>我们先给出最后的评估结果：</p>
<p><img src="https://images.gitbook.cn/10f12200-38c2-11e9-9be9-e5a41eccf0a0" alt="enter image description here" /></p>
<p>从截图中我们可以看出，准确率最后在 85% 左右（一共训练了 50 轮）并不是很高但也没有出现明显的负迁移。其实，如果想进一步提高分类的相关指标，我们可以从超参数、fine-tune 的网络结构等多方面进行调整。例如，目前我们只是对最后的输出层进行迁移，而从输入层到 fc2 这些网络层的参数都是冻结的，因此我们可以加大迁移的力度，换句话说增加重新训练的网络层数及参数。但这里我们需要注意的是，如果 fine-tune 的网络层过多，那么便失去了迁移的意义。</p>
<p>需要指出的是，迁移学习目前在工业界落地的案例仍然相对较少，原因在于，无论采取何种方式进行迁移，源领域和目标领域的相关性或者说可迁移性无法得到有效的、量化的证明。因此使用迁移学习之前，需要对源领域和目标领域的样本数据进行尽可能全面的分析，从而保证迁移学习的效果。</p>
<h3 id="164">16.4 小结</h3>
<p>本次课程我们介绍了当前关注度较高的一种人工智能技术——迁移学习。我们通过类比人类知识迁移、技能迁移的例子，给出了在机器学习问题中迁移学习的几种具体方式，并结合 Deeplearning4j 提供的迁移学习工具类完成了迁移学习的实例建模。在实例中，我们把在 ImageNet 数据集上预训练的 VGG 模型迁移到一个标签数目小得多的花卉分类问题上，经过 50 轮的训练后达到 85% 左右的分类准确率。我们对该指标进行了讨论，并且给出了提升模型的一些建议供大家参考。</p>
<p>迁移学习与深度学习的结合是当前可以快速落地的一种模型迁移方式。虽然对于迁移学习中的一些固有问题，比如负迁移等问题的论证和解决依然还需要做很多的工作，但是不可否认迁移学习将在未来不同场景下的快速建模、快速建立智能应用的需求中提供一个解决方案。最后我们在附录中给出文中参考的一些资料的来源。</p>
<p>相关资料：</p>
<ul>
<li><a href="https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf"><em>A Survey On Transfer Learning</em></a></li>
<li><a href="http://www.cse.ust.hk/~qyang/">杨强教授个人主页</a></li>
<li><a href="https://raw.githubusercontent.com/deeplearning4j/dl4j-examples/f9da30063c1636e1de515f2ac514e9a45c1b32cd/dl4j-examples/src/main/resources/trainedModels/VGG16.json">VGG-16 模型结构 JSON 格式文件</a></li>
<li><a href="https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_th_dim_ordering_th_kernels.h5">VGG-16 预训练模型参数文件</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>