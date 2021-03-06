---
title: Deeplearning4j 快速入门-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本节课开始，我们将陆续为大家介绍在工业界使用较多的几种神经网络结构。首先介绍的是卷积神经网络（Convolution Neural Network，CNN）。本节课核心内容包括：</p>
<ul>
<li>卷积神经网络发展历史回顾</li>
<li>卷积与池化</li>
<li>卷积神经网络的应用（图像分类）</li>
</ul>
<p>卷积一词来源于信号处理领域。以 1D 信号为例，$f(x)$ 和 $g(x)$ 分别代表两个信号源输出的信号，则 $f(x)$ 和 $g(x)$ 的卷积可以表示为：</p>
<div style="text-align:center"><img src="https://images.gitbook.cn/f71bab20-fe29-11e8-9206-ebae2af18c23" width="70%" /></div>
<p></br></p>
<p>卷积的数学含义可以认为是两个函数重叠部分的面积（其中一个函数需要做反褶操作）。现实生活中很多信号也可以认为是两个信号卷积的结果，例如：</p>
<blockquote>
  <p>回声就可以认为是声源发出的信号与反射信号的卷积。</p>
</blockquote>
<p>在实际应用中，卷积/解卷积操作可用于信号的平滑、滤波等场景，而这次介绍的卷积神经网络也同样基于卷积操作。在介绍卷积神经网络的细节之前，我们先回顾下它的发展历史。</p>
<h3 id="51">5.1 卷积神经网络发展历史回顾</h3>
<p>现在卷积神经网络具有代表性的工作，可以追溯到 20 世纪 90 年代 Yann LeCun 提出的 LeNet-5。事实上，后期的 AlexNet、VGG 系列、GoogLeNet 等卷积网络结构，都或多或少地借鉴了 LeCun 的工作，只不过网络的整体结构变得更深更广，或者与其他神经网络结构（如 RNN）结合使用。</p>
<p>LeNet-5 的结构示意图如下：</p>
<p><img src="https://images.gitbook.cn/8cf670f0-f860-11e8-9a64-877e724fe46d" alt="enter image description here" />
图片来源：<em>Gradient-Based Learning Applied to Document Recognition</em> (Proc. IEEE 1998)，<a href="https://ieeexplore.ieee.org/document/726791">论文下载链接</a></p>
<p>LeNet-5 受限于当时硬件的计算能力，对于小规模的机器视觉问题，如 MNIST 分类问题，可以达到很高的准确率，但对于更大型的问题则显得力不从心。这一局面直到 2012 年 Hinton 以及他的学生 Alex Krizhesky 凭借 AlexNet 夺得 ImageNet 比赛冠军后才被打破。自此，卷积神经网络甚至整个神经网络领域再度受到工业界和学术界的关注，深度神经网络以及深度学习的概念也逐渐被大家所知晓。</p>
<p>AlexNet 其实是一种更为深刻的 LeNet。此外非线性变换函数、防止过拟合的 Dropout 等 trick 也都在后来深度学习的发展中扮演着重要的角色。此后，卷积神经网络沿着更深更广的趋势继续发展。下面是一个简单的发展历程图：</p>
<p><img src="https://images.gitbook.cn/95b1ceb0-f9cd-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>接着，我们介绍下在卷积神经网络中常见的卷积、池化操作的一些细节。</p>
<h3 id="52">5.2 卷积与池化</h3>
<p>在卷积神经网络中，卷积操作的目的是用于提取局部特征。参与卷积操作的信号是两个矩阵，其中一个是人为设置大小的（例如 3x3、5x5）通常被称作是卷积核或者滤波器的矩阵，另一个则是图像原始输入的像素矩阵，或上一轮卷积操作后输出的 Feature Map。我们结合 Standford 机器学习课程中关于卷积神经网络的一个动态 Demo 来直观了解下卷积的过程。下图的源地址：<a href="https://cs231n.github.io/assets/conv-demo/index.html">https://cs231n.github.io/assets/conv-demo/index.html</a>。</p>
<p><img src="https://images.gitbook.cn/f65847c0-f9ce-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>截图中左侧第一列的三个矩阵可以认为是图片的 R、G、B 三个通道。原始的像素矩阵其实是 5x5 的大小。由于使用的卷积核尺寸是 3x3，并且卷积核在像素矩阵上每次移动 2 个像素，因此需要在外围补充一些像素点，也就是灰色且像素值都是 0 的那些点。截图的例子中选取了两个卷积核，因此输出的 Feature Map（图中最右侧的绿色的矩阵）也是两个。每个卷积核其实是一个 3x3x3 的三维张量，每个 3x3 的切面则用于在原始三个通道的像素矩阵中提取一些特征。当然，每个切面内部的值是可以不同的。 </p>
<p>卷积核从像素矩阵最左上角的像素点开始进行自左向右、自上而下的滑动（例子中滑动过 2 个像素点）。在滑动的过程中，对应位置的矩阵中的值相乘（Hadmard 乘积）并线性叠加。</p>
<p>需要注意的是，卷积核并不需要做像刚才介绍的一维信号那样的反褶操作（其实反褶操作可以通过初始化不同的矩阵元素的值来实现，效果是一样的）。 </p>
<p>卷积操作结束后，我们可以将输出的 Feature Map 通过非线性激活函数来获取非线性特征。我们将经过非线性处理后的结果称为 Activation Map。 </p>
<p>在获取 Activation Map 之后，我们可以选择添加一次池化或者说下采样的操作（注意：池化操作不是必须，连续卷积操作也是可以的）。池化操作有一些具体的选择，比如说最大池化、平均池化等。我们同样以 Standford 课程中的示例图为例，解释下最大池化的概念。下图的源地址：<a href="https://cs231n.github.io/convolutional-networks/">https://cs231n.github.io/convolutional-networks/</a></p>
<p><img src="https://images.gitbook.cn/1518d040-f9d8-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>在池化操作中，我们同样需要类似卷积核或者说滤波器的介入。只不过滤波器在这里的作用并不是做 Hadmard 乘积，而是在过滤的像素区域内根据一定的规则（如最大数值、加权平均）输出，即为<strong>池化</strong>。从截图中我们可以看到，当我们的滤波器设置成 2x2，每次滑动 2 个像素点时，就可以把 Activation Map 中 4 个区域的最大值输出成为新的 Feature Map，即为<strong>最大池化</strong>。类似地，平均池化则是求取了均值。 </p>
<p>池化的好处有两个：</p>
<ol>
<li>显著缩小了输出矩阵的大小，起到了降维的作用；</li>
<li>可以按照需要选择更有代表性的特征，比如最大池化，就可以认为是选择了一定区域内最有代表性的特征，起到了特征选择的作用。 </li>
</ol>
<p>卷积 + 池化的结构成为卷积神经网络的一种常用的搭配，但并非在所有网络中都采用这样的结构，读者在这里需要参考相关论文和著述并结合自身的实际情况进行选择。 </p>
<p>下面我们分别介绍卷积神经网络在图像分类和目标检测任务中的应用。</p>
<h3 id="53">5.3 卷积神经网络的应用</h3>
<p>卷积神经网络目前广泛应用于语音、机器视觉及文本处理的算法任务中。这里我们选择机器视觉中常见的分类和目标检测任务，对如何基于 Deeplearning4j 构建 CNN 网络的应用进行详细分析。</p>
<h4 id="531">5.3.1 图像分类</h4>
<p>传统的图像分类往往分为特征提取和分类器构建两个阶段。特征提取常用的算法有 SIFT、SURF、HOG 等。分类器的选择集中在 SVM、基于 Boosting/Bagging 的集成学习算法。在深度学习大规模应用前，类似 SIFT 等设计精良的特征提取方式基本决定了应用的实际效果。但是不可否认的是，现实应用问题往往十分复杂，特征组合的应用非常常见，这不仅增加了工程师的工作量，最重要的是无论如何组合特征实际效果不一定有保证。</p>
<p>卷积神经网络的兴起在一定程度上解决了传统算法的问题。在我们使用卷积神经网络做图像分类时，并不需要设计特征算法，特征的提取和分类已嵌入到了整个神经网络中。事实上这种 end-to-end 的做法对于工程师来讲只需要将图像的原始信号（也就是像素矩阵）输入到模型，输出就是分类结果，至于神经网络在训练过程中提取了什么特征做分类，其实并不完全可见或者可理解（卷积神经网络的可视化分析可以参考：<a href="https://cs231n.github.io/understanding-cnn/">https://cs231n.github.io/understanding-cnn/</a>）。</p>
<p>下面我们使用 Deeplearning4j 对 Fashion-MNIST 数据集进行分类建模。</p>
<p>Fashion-MNIST 数据集（<a href="https://github.com/zalandoresearch/fashion-mnist">https://github.com/zalandoresearch/fashion-mnist</a>）是类似 MNIST 手写体数字数据集的一组开源的服装数据集。它除了图片内容和 MNIST 不同外，其他诸如标签数量、图片尺寸、训练/测试图片数量，甚至二进制文件名称和 MNIST 均完全一致。以下是 Fashion-MNIST 的部分截图：</p>
<p><img src="https://images.gitbook.cn/ccc28640-f9d9-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>我们用类似 LeNet-5 的结构，即两组 Conv+MaxPooling 构建卷积神经网络模型。</p>
<pre><code>public static MultiLayerNetwork getModel(){
        MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                        .seed(12345)
                        .iterations(1)
                        .learningRate(0.01)
                        .learningRateScoreBasedDecayRate(0.5)
                        .weightInit(WeightInit.XAVIER)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .updater(Updater.ADAM)
                        .list()
                        .layer(0, new ConvolutionLayer.Builder(5, 5)
                                .nIn(1)
                                .stride(1, 1)
                                .nOut(32)
                                .activation(Activation.LEAKYRELU)
                                .build())
                        .layer(1, new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
                                .kernelSize(2,2)
                                .stride(2,2)
                                .build())
                        .layer(2, new ConvolutionLayer.Builder(5, 5)
                                .stride(1, 1)
                                .nOut(64)
                                .activation(Activation.LEAKYRELU)
                                .build())
                        .layer(3, new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
                                .kernelSize(2,2)
                                .stride(2,2)
                                .build())
                        .layer(4, new DenseLayer.Builder().activation(Activation.LEAKYRELU)
                                .nOut(500).build())
                        .layer(5, new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                                .nOut(10)
                                .activation(Activation.SOFTMAX)
                                .build())
                        .backprop(true).pretrain(false)
                        .setInputType(InputType.convolutionalFlat(28, 28, 1));
        MultiLayerConfiguration conf = builder.build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        return model; 
}
</code></pre>
<p>我们结合上述逻辑解释下，在 Deeplearning4j 中卷积神经网络的建模过程。</p>
<p>首先我们需要声明一个 MultiLayerConfiguration，即多层网络的配置对象。</p>
<blockquote>
  <p>注意：Deeplearning4j 同时支持 MultiLayerConfiguration 和 ComputationGraphConfiguration，对于无法清晰划分为多层结构的神经网络，可以考虑使用 ComputationGraphConfiguration。</p>
</blockquote>
<p>网络的第一层，是一个卷积层：</p>
<pre><code>.layer(0, new ConvolutionLayer.Builder(5, 5)    //卷积核大小
         .nIn(1)        //输入原始图片的通道数
         .stride(1, 1)    //步长大小
         .nOut(32)        //输出 Feature Map 的数量
         .activation(Activation.LEAKYRELU)    //非线性激活函数
         .build())
</code></pre>
<ul>
<li>由于 Fashion-MNIST 数据集是灰度图，因此通道数为 1。如果是 RGB 彩色图片，则通道数等于 3。</li>
<li>卷积核的大小可以通过构造参数传入，也可以用 .kernelSize 来定义。</li>
<li>输出的 Feature Map 的数量这里等于 32，这个数量用户可以自定义。</li>
</ul>
<p>网络的第二层，是一个最大池化层：</p>
<pre><code>.layer(1, new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
         .kernelSize(2,2)
         .stride(2,2)
         .build())
</code></pre>
<ul>
<li>构建器传入的参数用于定义池化的类型，池化的类型常用的有最大池化、平均池化、求和池化等。这些方式在 Deeplearning4j 都支持。</li>
<li>kernelSize(2,2) 是卷积核/滤波器的尺寸大小。</li>
<li>stride(2,2) 和上面卷积层的参数概念一样，是步长。步长越大，输出的 Feature Map 的尺寸也就越小了。</li>
</ul>
<p>网络的第五层，是一个全连阶层：</p>
<pre><code>.layer(4, new DenseLayer.Builder().activation(Activation.LEAKYRELU)
         .nOut(500).build())
</code></pre>
<p>全连接这里的作用是将特征展开成一个 1x500 的向量。注意，输入的维度用户不一定要指定，Deeplearning4j 会根据前几层的网络输出自动计算。</p>
<p>网络的第六层，是一个输出层：</p>
<pre><code>.layer(5, new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                   .nOut(10)
                   .activation(Activation.SOFTMAX)
                   .build())
</code></pre>
<p>这一层主要用于定义输出标签的数量、损失函数等信息。由于输出有 10 个分类，我们用 Softmax 作为激活函数，损失函数使用交差熵。到此，一个卷积神经网络就基本定义好了。 </p>
<p>接下来，我们需要将数据喂到模型中进行训练。由于 Fashion-MNIST 数据集和手写体 MNIST 数据集在图片属性层面是完全一致的，因此我们可以直接用 Deeplearning4j 内置的工具类 MnistDataSetIterator 进行直接读取。</p>
<blockquote>
  <p>注意：如果使用该工具类读取 Fashion-MNIST 数据集，需要将 Fashion-MNIST 的二进制数据文件拷贝到当前用户根目录下的 MNIST 目录中，二进制数据文件可以从 GitHub 上下载。</p>
</blockquote>
<pre><code>DataSetIterator mnistTrain = new MnistDataSetIterator(batchSize, true, 12345);
DataSetIterator mnistTest = new MnistDataSetIterator(batchSize, false, 12345);
</code></pre>
<p>最后，我们需要编写训练模型的逻辑。这段逻辑和之前文章中提到训练逻辑是一致的。并在训练结束后，在验证集上进行准确率验证以及模型的保存。</p>
<pre><code>for( int i = 0; i &lt; numEpochs; ++i ){
    model.fit(mnistTrain);
}
Evaluation eval = model.evaluate(mnistTest);
System.out.println(eval.stats());
ModelSerializer.writeModel(model, modelSavePath, true);
</code></pre>
<p>我们共训练了 100 轮次，最终在验证集上的准确率仅在 90% 左右。</p>
<p><img src="https://images.gitbook.cn/17c39d90-f9db-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>此外，我们顺便给出 Fashion-MNIST 和 MNIST 数据集训练的比较结果。</p>
<p><img src="https://images.gitbook.cn/23f28310-f9db-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>从这张截图中，我们可以直观地看出，在使用同样网络的情况下，MNIST 数据集在第一轮训练结束后，就可以在验证集上达到 95% 左右的准确率。而反观 Fashion-MNIST 数据集，第一轮训练结束后仅仅达到 80% 左右的准确率，并且在最终的 100 轮训练完后，也只有 90% 的准确性。这说明 Fashion-MNIST 数据集的分类问题相较于 MNIST 而言更为复杂。</p>
<p>对于 Fashion-MNIST 数据集分类的探索，在它的 GitHub 主页上，有基于 CapsuleNet/Inception ResNet 等复杂网络结构下的分类结果，有兴趣的同学可以关注。</p>
<h3 id="54">5.4 小结</h3>
<p>本次课程主要介绍了卷积神经网络的原理，以及其在图像分类中的应用。我们首先回顾了卷积神经网络的历史，然后介绍了卷积神经网络中比较重要的两个概念，卷积 + 池化，随后我们基于 Deeplearning4j 的框架介绍如何构建分类模型。在下一课我们将继续围绕卷积神经网络，介绍基于 YOLO 的图像目标检测应用。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://cs231n.github.io/assets/conv-demo/index.html">Standford 机器学习课程中卷积神经网络 Demo</a></li>
<li><a href="https://cs231n.github.io/understanding-cnn">卷积神经网络的可视化分析</a></li>
<li><a href="https://github.com/zalandoresearch/fashion-mnist">Fashion-MNIST 数据集</a></li>
</ul></div></article>