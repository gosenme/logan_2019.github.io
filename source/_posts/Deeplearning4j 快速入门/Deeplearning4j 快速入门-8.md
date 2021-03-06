---
title: Deeplearning4j 快速入门-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一节课中，我们介绍了卷积神经网络发展的历史以及图像分类的应用。本节课的内容将在上一节课的基础上，为大家介绍机器视觉中另一类经典案例——目标检测。本节课核心内容包括：</p>
<ul>
<li>卷积神经网络的应用：图像目标检测</li>
<li>滑动窗口算法</li>
<li>基于卷积神经网络的算法</li>
</ul>
<p>目前基于深度神经网络的目标检测模型有：YOLO 系列、SSD、R-CNN 系列等。本节课我们将为大家介绍这些算法的基本原理并结合目前 Deeplearning4j 中直接支持的 YOLOv2 来构建目标检测的模型。在文章的最后，我们将为大家附上模型在图片和视频文件中的检测效果。</p>
<h3 id="61">6.1 卷积神经网络的应用：图像目标检测</h3>
<p>图像的目标检测问题不同于上面介绍的图像分类。图像分类无需具体定位图像中实物的具体位置，只需要完成对整体内容的识别；而目标检测需要检测出一个或者多个目标区域，通常我们用 Bounding Box（由中心坐标 [x,y]、矩形框宽 width 、矩形框高 height 来确定）来框选目标区域。</p>
<p>首先我们来回顾下目标检测的几种经典算法。</p>
<h4 id="611">6.1.1 滑动窗口算法</h4>
<p>滑动窗口的做法的核心思想是利用不同尺寸的矩阵窗口在图像中左右滑动，提取特征并用分类器进行识别。这里特征的选择和分类器可以有多种组合，例如：</p>
<ul>
<li>HOG+SVM 可用于检测行人或其他常见物体</li>
<li>Harr+AdaBoost/SVM 常用于检测人脸</li>
</ul>
<p>当然我们也可以使用深度学习的方式直接预测，即 HOG+SVM 或 Harr+AdaBoost 的组合，用 VGG-16 或其他网络整体替换。</p>
<p>滑动窗口思想非常直接，通过扫描整张图片来确定目标区域。但是它的缺点也非常明显，即计算的速度比较慢。我们需要对窗口内的区域不断地做分类，也就是说每滑动一次就预测一次。这样的结果就是，对整张图片的局部区域做了多次的分类预测，导致性能的急剧下降。下图是滑动窗口的一个示例：</p>
<p><img src="https://images.gitbook.cn/3ccb6c50-f9ed-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>我们可以看到，如果基于滑动窗口算法检测图中“飞机”这个目标的话，红色的窗口需要不断移动并且不断预测，速度非常慢。</p>
<h4 id="612">6.1.2 基于卷积神经网络的算法</h4>
<p>基于卷积神经网络的算法大致可以分为两类。一类是以 YOLO 、SSD 为代表的，可以一次性输出目标区域和识别结果的算法；另一类则是以 R-CNN 家族为代表的，将目标检测分为区域位置检测和内容识别两个阶段的算法。首先我们介绍 R-CNN 家族算法。</p>
<h5 id="rcnn"><strong>R-CNN家族系列介绍</strong></h5>
<p>对于 R-CNN 算法而言，第一阶段的工作是枚举图像的候选框（一般候选框的数量在 2K 左右，使用 Selective Search 算法实现）并将根据候选框提取的区域输入到一个卷积神经网络中，得到输出的特征向量。第二阶段的工作是将第一阶段输出的特征向量进行分类，并且利用回归模型修正目标区域使之更加精准。</p>
<p><img src="https://images.gitbook.cn/79055c80-f9ed-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>R-CNN 算法的显著缺点在于速度慢，大量的候选框提取的区域都需要输入到 CNN 中，导致计算量很大。针对这个问题，在改进版的 Fast R-CNN 中将分类和回归两个问题进行合并，即将两个任务的损失函数线性加权，做成多任务模型。另外借鉴 SPP-Net 的做法，Fast R-CNN 使用 ROI Pooling Layer 来适应不同尺寸的候选区域，使得整图的特征候选区域的特征可以输出到一个全连接网络中。这主要的两个改进，使得其无需像 R-CNN 对候选区域分别做分类和回归，因此提升了速度。 </p>
<p>Fast R-CNN 一定程度上提升了预测速度，并且提出多任务损失函数来提高精度，但使用 Selective Search 算法提取候选框的做法没有改变，依然存在很大的速度瓶颈。</p>
<p>这个问题在 Faster R-CNN 中进行解决。Faster R-CNN 提出使用 RPN 网络来代替 Selective Search 算法提取候选框，换句话说候选区域的选择也由神经网络来完成，预测速度得到进一步的提升。</p>
<h5 id="yolo"><strong>YOLO 家族系列介绍</strong></h5>
<p>YOLO（You Only Look Once）算法在 2015 提出，此后有 YOLOv2 和 YOLOv3。YOLO 的思想是将目标检测做成一个彻底的端到端的问题。YOLO 不同于 R-CNN 家族算法需要提取不同尺寸的候选区域，而是直接用整图作为唯一输入，来直接获取最终的目标区域和分类结果。</p>
<p><img src="https://images.gitbook.cn/82f845a0-f9f6-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>YOLO 的基本思想是将图片划分成 SxS（如 13X13）个格子，每一个格子会负责给出各个类别的概率，还有该区域内可能的 Bounding Box 数量、置信度以及坐标。预测的结果被编码成 SxSx(Bx5+C) 的向量输出。</p>
<p>YOLO 的损失函数分成 3 个部分（<strong>坐标误差、IOU 误差、分类误差</strong>）线性加权。换句话说，和 Fast R-CNN 模型类似，YOLO 同样将目标检测做成一个多任务的模型，有关的损失信息都通过线性加权的方式进行集成。</p>
<p>YOLOv1 的问题在于小物体检测不是很准确，检测精度不够。YOLOv2 在 v1 的基础上做出了一系列的改进。</p>
<p>首先，v2 借鉴了 Faster R-CNN 的思路，引入 Anchor Box 的理念并使用 K-Means 进行聚类来自动预测最合理的 Bounding Box。</p>
<blockquote>
  <p>论文中对预设值的 Anchor Box 数量进行的讨论，有兴趣的同学可以阅读原文的分析结果。</p>
</blockquote>
<p>此外，v2 还引入了 Batch Normalization 等 trick，一定程度上提升了模型的效果。 </p>
<p>YOLOv2 在 v1 的基础上做了很多改进，使得目标检测的速度和准确性都有了比较大的提升。但 v2 对于一些难点，如距离接近的物体、非常小的物体，并没有很好地解决。</p>
<p>v3 针对这些问题做了一些改进。</p>
<ul>
<li>用 Logistic Loss 替换 Softmax Loss</li>
<li>v2 中依赖的卷积网络 Darknet-19 升级成 Darknet-53</li>
<li>Anchor Box 由 v2 中的默认 5 个升级成 9 个</li>
</ul>
<p>在下面的部分中，我们将基于 Deeplearning4j 1.0-apha 版本实现图像和视频中人脸检测的应用。</p>
<h4 id="613yolo">6.1.3 YOLO 实现人脸检测</h4>
<p>人脸识别是当前机器视觉应用中比较成功的一个领域。包括付款、安保、罪犯追踪等实际场景中都有人脸识别不同程度的落地工作。人脸识别通常分为人脸检测和识别两个环节，这里我们将讨论用 YOLO 来实现第一个环节。</p>
<p>首先我们需要收集一些人脸的数据并且打上标注。人脸的数据这里我们用的是开源的 LFW 数据集（<a href="http://vis-www.cs.umass.edu/lfw/">http://vis-www.cs.umass.edu/lfw/</a>），以及部分苏宁易购服装类图片。我们利用目标检测的打标工具 LabelImg（<a href="https://github.com/tzutalin/labelImg">https://github.com/tzutalin/labelImg</a>）进行人脸的标注。</p>
<blockquote>
  <p>LabelImg 工具是基于 Python 的可视化目标检测打标工具，可以批量选择图片进行区域的框选，并且自动生成 VOC 格式的标注文件。</p>
</blockquote>
<p>下面是这个工具的使用截图：</p>
<p><img src="https://images.gitbook.cn/e7883210-f9f0-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>在利用 LabelImg 标注完相应的图片后，VOC 格式的标注文件会自动生成在 Annotations 的目录下（该子目录一般需要用户事先手动创建），每一张图片对应一个 XML 标注文件。</p>
<p>以下是其中一份 XML 文件的内容截图：</p>
<p><img src="https://images.gitbook.cn/02e1ff00-f9f1-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>从 XML 文件中可以直观地看出标注的内容，包括图片的大小、目标的数量和名称的坐标。在最新版的 DataVec 中支持直接读取 VOC 格式的标注数据，VocLabelProvider 这个工具类实现了对 VOC 标注文件的解析。以下是读取标注数据的逻辑：</p>
<pre><code>final int width = 416;
final int height = 416;
final int nChannels = 3;
final int gridWidth = 13;
final int gridHeight = 13;
...此处省略部分参数

//读取训练和测试数据集
FileSplit trainData = new FileSplit(new File(inputPath), NativeImageLoader.ALLOWED_FORMATS, rng);
FileSplit testData = new FileSplit(new File(inputTestPath), NativeImageLoader.ALLOWED_FORMATS, rng);

//读取 VOC 格式的标注数据
ObjectDetectionRecordReader recordReaderTrain = new ObjectDetectionRecordReader(height, width, nChannels,
        gridHeight, gridWidth, new VocLabelProvider(inputPath));
recordReaderTrain.initialize(trainData);

ObjectDetectionRecordReader recordReaderTest = new ObjectDetectionRecordReader(height, width, nChannels,
        gridHeight, gridWidth, new VocLabelProvider(inputTestPath));
recordReaderTest.initialize(testData);

//归一化处理
RecordReaderDataSetIterator train = new RecordReaderDataSetIterator(recordReaderTrain, batchSize, 1, 1, true);
train.setPreProcessor(new ImagePreProcessingScaler(0, 1));

RecordReaderDataSetIterator test = new RecordReaderDataSetIterator(recordReaderTest, 1, 1, 1, true);
test.setPreProcessor(new ImagePreProcessingScaler(0, 1));
</code></pre>
<p>上述逻辑分为三个主要部分：</p>
<ul>
<li>读取图片文件</li>
<li>读取 VOC 格式标注数据 </li>
<li>预处理</li>
</ul>
<p>DataVec 对目标检测的数据格式进行了高度封装，只需要传入图片文件相关的参数即可生成训练数据。接下来我们基于 YOLO 建模。如下逻辑：</p>
<pre><code>int nClasses = 1;
int nBoxes = 5;
double lambdaNoObj = 0.5;
double lambdaCoord = 1.0;
double[][] priorBoxes = {{1.08, 1.19}, {3.42, 4.41}, {6.63, 11.38}, {9.42, 5.11}, {16.62, 10.52}};    
//...以下省略部分逻辑代码

public static ComputationGraph tinyYOLO(int nBoxes, int numLabels, INDArray priors, double lambdaNoObj, double lambdaCoord){
        GraphBuilder graphBuilder = new NeuralNetConfiguration.Builder()
                        .seed(123456L)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .gradientNormalization(GradientNormalization.RenormalizeL2PerLayer)
                        .gradientNormalizationThreshold(1.0)
                        .updater(new Adam.Builder().learningRate(1e-3).build())
                        //.l2(0.00001)
                        .activation(Activation.IDENTITY)
                        .trainingWorkspaceMode(WorkspaceMode.SEPARATE)
                        .inferenceWorkspaceMode(WorkspaceMode.SEPARATE)
                        .cudnnAlgoMode(ConvolutionLayer.AlgoMode.NO_WORKSPACE)
                        .graphBuilder()
                        .addInputs("input")
                        .setInputTypes(InputType.convolutional(416, 416, 3));
                addLayers(graphBuilder, 1, 3, 3, 16, 2, 2);
                addLayers(graphBuilder, 2, 3, 16, 32, 2, 2);
                addLayers(graphBuilder, 3, 3, 32, 64, 2, 2);
                addLayers(graphBuilder, 4, 3, 64, 128, 2, 2);
                addLayers(graphBuilder, 5, 3, 128, 256, 2, 2);
                addLayers(graphBuilder, 6, 3, 256, 512, 2, 1);
                addLayers(graphBuilder, 7, 3, 512, 1024, 0, 0);
                addLayers(graphBuilder, 8, 3, 1024, 1024, 0, 0);

                int layerNumber = 9;
                graphBuilder
                        .addLayer("convolution2d_" + layerNumber,
                                new ConvolutionLayer.Builder(1,1)
                                        .nIn(1024)
                                        .nOut(nBoxes * (5 + numLabels))
                                        .weightInit(WeightInit.XAVIER)
                                        .stride(1,1)
                                        .convolutionMode(ConvolutionMode.Same)
                                        .weightInit(WeightInit.RELU)
                                        .activation(Activation.IDENTITY)
                                        .build(),
                                "activation_" + (layerNumber - 1))
                        .addLayer("outputs",
                                new Yolo2OutputLayer.Builder()
                                        .lambbaNoObj(lambdaNoObj)
                                        .lambdaCoord(lambdaCoord)
                                        .boundingBoxPriors(priors)
                                        .build(),
                                "convolution2d_" + layerNumber)
                        .setOutputs("outputs").backprop(true).pretrain(false);
        ComputationGraphConfiguration conf = graphBuilder.build();
        ComputationGraph net = new ComputationGraph(conf);
        return net;
}
</code></pre>
<p>这里我们使用了 Tiny YOLO。</p>
<blockquote>
  <p>Tiny YOLO 是 YOLO 的简化版本，用于目标检测的卷积网络层数更少、训练时间更短、检测速度更快，但准确率相对较低。作为验证 YOLO 功能的模型，非常适合作为入门的模型案例。 </p>
</blockquote>
<p>以上 Tiny YOLO 的配置来源于 deeplearning4j-zoo 中提供的版本。配置 Tiny YOLO 需要传入 5 个参数：</p>
<ul>
<li>nBoxes：Anchor Box 的数量</li>
<li>numLabels：训练全部涉及的标的分类数量</li>
<li>priors：Anchor Box 的具体配置/尺寸</li>
<li>lambdaNoObj：检测不到目标的置信度参数</li>
<li>lambdaCoord：坐标预测在损失函数中的权重</li>
</ul>
<p>需要注意的是在 Tiny YOLO/YOLOv2 的最后一层需要用 Yolo2OutputLayer 进行配置，Yolo2OutputLayer 已经实现了前述中的分类 + 回归的多任务损失函数。接下来看下训练模型的主逻辑：</p>
<pre><code>ComputationGraph model = tinyYOLO(nBoxes, numLabels, priors, lambdaNoObj, lambdaCoord)

log.info("Train model...");
model.setListeners(new ScoreIterationListener(1));
for (int i = 0; i &lt; nEpochs; i++) {
    train.reset();
    while (train.hasNext()) {
         model.fit(train.next());
    }
}
ModelSerializer.writeModel(model, modelFilename, true);
</code></pre>
<p>这部分逻辑和之前训练逻辑没什么太大的区别，因此就不再赘述了。</p>
<p>接下来我们选取一些有人脸的图像和视频进行测试。首先给出我们基于上述模型训练得出的测试效果：</p>
<p><img src="https://images.gitbook.cn/3e85e960-f9f4-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>测试集使用的是部分 LFW 的数据和苏宁易购服装的图片集。可以看出脸部区域已经被模型识别，包括有多个人脸的场景也可以进行识别。</p>
<blockquote>
  <p><strong>注意：由于标注的时候我们框选的区域大多包含头部区域，不仅限于脸部，因此预测出的区域也不仅限于脸部。如果要进行严格的人脸检测，可进行更为准确的标注。</strong></p>
</blockquote>
<p>下面这张 GIF 图是用模型检测视频中的人脸。由于我们的标注数据主要集中在正脸，因此大部分正脸都可以检测出来，但侧脸的效果会差很多。</p>
<p><img src="https://images.gitbook.cn/af44ac90-f9f4-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<h3 id="62">6.2 小结</h3>
<p>本次课程主要介绍了，基于 Deeplearning4j 框架，卷积神经网络在目标检测中的应用。</p>
<p>卷积神经网络可以在机器视觉领域（当然并不限于机器视觉问题，文本、语音的问题同样可以用 CNN）得到广泛应用的原因在于，<strong>它可以通过端到端的模型训练，学会如何在不同问题场景下获取有用的特征，</strong>而不是像传统的一些做法，单独提取特征再建模。</p>
<p>Deeplearning4j 目前支持大部分卷积神经网络的特性。包括一些诸如空洞卷积、上采样等有用的特性。在 Model Zoo 的子项目中，官网也给出了经典的卷积神经网络结构，如 AlexNet、GoogLeNet、VGG 系列、ResNet 等。有兴趣的同学可以结合自身业务需要进行使用。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="http://vis-www.cs.umass.edu/lfw/">LFW 数据集</a></li>
<li><a href="https://github.com/tzutalin/labelImg">目标检测的打标工具 LabelImg</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>