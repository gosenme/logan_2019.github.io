---
title: Deeplearning4j 快速入门-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课我们将介绍如何使用神经网络对数据进行降维和特征提取，主要采用的方案是基于自监督学习的 AutoEncoder。本节课核心内容包括：</p>
<ul>
<li>降噪自编码器（DAE）</li>
<li>基于深度信念网络的自编码器</li>
<li>变分自编码器</li>
</ul>
<p>自编码器的用途比较广泛，比如：数据的压缩、检索、高效传输、深层网络的预训练等。由于 AutoEncoder 的具体实现方式很多，限于篇幅，我们介绍最常用的三种自编码器：变分自编码器、降噪自编码器、基于深度信念网络的自编码器。</p>
<p>其实抛开上述的这些具体实现，在理想情况下，自编码器的输出和输入是一致的。换句话说，通过压缩数据获取更为抽象的特征后，我们希望用这些更为抽象，同时也更为简洁的特征来表示原数据的分布。</p>
<p>这次我们使用的数据集是手写体数字 MNIST 数据集（<a href="http://yann.lecun.com/exdb/mnist/">http://yann.lecun.com/exdb/mnist/</a>）。</p>
<blockquote>
  <p>MNIST 数据集是 28*28 的灰度图，由 60000 张训练图片和 10000 张验证图片构成，是入门深度学习最常用的开源数据集之一。MNIST 数据集的内容是 0~9 的手写的数字。下面的截图即是部分的 MNIST 数据集：</p>
</blockquote>
<p><img src="https://images.gitbook.cn/210e6380-f3c8-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<h3 id="41dae">4.1 降噪自编码器（DAE）</h3>
<p>在介绍 DAE 之前，我们可以试想下，如何基于上节课介绍的多层感知机构建自编码器。由于自编码器的特点是输入和输出的维度一致，因此只需要在中间的隐藏层配置较少的神经元数量即可降维。我们可以很容易地设计出如下结构的全连接神经网络：</p>
<p><img src="https://images.gitbook.cn/7b4764a0-fc5b-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>图中省略了神经元间的连接。</p>
<p>下面我们结合 MNIST 数据集，尝试将 28*28 的灰度图压缩到 250 维的向量。网络结构的配置如下：</p>
<pre><code>private static MultiLayerNetwork mlp(){
        MultiLayerConfiguration conf = new NeuralNetConfiguration.Builder()
                        .seed(12345L)
                        .iterations(1)
                        .learningRate(0.01)
                        .learningRateScoreBasedDecayRate(0.5)
                        .weightInit(WeightInit.XAVIER)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .updater(Updater.ADAM)
                        .list()
                        .layer(0, new DenseLayer.Builder().activation(Activation.RELU)
                                        .nIn(28*28).nOut(1000).build())
                        .layer(1, new DenseLayer.Builder().activation(Activation.RELU)
                                        .nIn(1000).nOut(500).build())
                        .layer(2, new DenseLayer.Builder().activation(Activation.RELU)
                                        .nIn(500).nOut(250).build())
                        .layer(3, new DenseLayer.Builder().activation(Activation.RELU)
                                        .nIn(250).nOut(500).build())
                        .layer(4, new DenseLayer.Builder().activation(Activation.RELU)
                                        .nIn(500).nOut(1000).build())
                        .layer(5, new OutputLayer.Builder(LossFunctions.LossFunction.MSE)  
                                        .nIn(1000)  
                                        .nOut(28*28)  
                                        .activation(Activation.RELU)  
                                        .build())
                        .backprop(true).pretrain(false)
                        .build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        return model;
}
</code></pre>
<p>网络的结构实际上是：784(28*28) –&gt; 1000 –&gt; 500 –&gt; 250 –&gt; 500 –&gt; 1000 -&gt; 784(28*28)。输出的张量和输入的张量维度相同，目的也是希望有一个重建的过程。需要注意的是，神经网络的第二层含有 1000 个神经元，其目的是希望将 MNIST 数据集先映射成相对高维的向量后再降维。当然读者也可以直接对 MNIST 进行降维，效果可以自行验证。损失函数在这里我直接使用均方误差来做约束。训练的逻辑和之前课程中类似，这里我们训练的轮次为 50 个 Epoch，batchSize 是 32。我们看下部分原始图片和压缩还原后图片的对比情况：</p>
<p><img src="https://images.gitbook.cn/95b94310-f3ca-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>截图中以 reconstruct.jpg 结尾的图片就是根据之前训练好的基于 MLP 的自编码器重构原图后的结果。红色框框选的几组图片是我任意选择的一些原图和原图的重构图。可以看到，重构图基本上可以还原出原图的有用信息，但也不排除一些重构图非常模糊，质量较差。对以上的网络结构其实很很多可以改进的地方，比如损失函数、压缩的比例等。这些可以调整的信息留给有兴趣的同学自行尝试。</p>
<p><strong>接下来我们介绍降噪自编码器（Denoising AutoEncoder）</strong>。</p>
<p>降噪自编码器顾名思义是在网络中人为添加一些噪声分布，常见的比如高斯白噪声，然后让模型在噪声环境中进行训练，由于模型需要摒除噪声对数据进行重建，从而可以获取更为有代表性的特征。在 Deeplearning4j 中，内置的 AutoEncoder 类已经封装了以上功能，因此我们可以直接堆叠 AutoEncoder 实例来实现降噪自编码器。我们先看下基于 Deeplearning4j 中的 AutoEncoder 来构建降噪自编码器。</p>
<pre><code>private static MultiLayerNetwork dae(){
        MultiLayerConfiguration conf = new NeuralNetConfiguration.Builder()
                        .learningRate(0.01)
                        .learningRateScoreBasedDecayRate(0.5)
                        .seed(12345)
                        .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                        .updater(Updater.ADAM)
                        .list()
                        .layer(0, new AutoEncoder.Builder().nIn(28 * 28).nOut(1000)
                                .activation(Activation.RELU)
                                .weightInit(WeightInit.XAVIER)
                                .lossFunction(LossFunction.KL_DIVERGENCE)
                                .corruptionLevel(0.3)
                                .build())
                        .layer(1, new AutoEncoder.Builder().nIn(1000).nOut(500)
                                     .activation(Activation.RELU)
                                     .weightInit(WeightInit.XAVIER)
                                     .lossFunction(LossFunction.KL_DIVERGENCE)
                                     .corruptionLevel(0.3)
                                     .build())
                        .layer(2, new AutoEncoder.Builder().nIn(500).nOut(250)
                                        .activation(Activation.RELU)
                                        .weightInit(WeightInit.XAVIER)
                                        .lossFunction(LossFunction.KL_DIVERGENCE)
                                        .corruptionLevel(0.3)
                                        .build())
                        .layer(3, new AutoEncoder.Builder().nIn(250).nOut(500)
                                        .activation(Activation.RELU)
                                        .weightInit(WeightInit.XAVIER)
                                        .lossFunction(LossFunction.KL_DIVERGENCE)
                                        .corruptionLevel(0.3)
                                        .build())
                        .layer(4, new AutoEncoder.Builder().nIn(500).nOut(1000)
                                        .activation(Activation.RELU)
                                        .weightInit(WeightInit.XAVIER)
                                        .lossFunction(LossFunction.KL_DIVERGENCE)
                                        .corruptionLevel(0.3)
                                        .build())
                        .layer(5, new OutputLayer.Builder(LossFunctions.LossFunction.MSE)
                                     .nIn(1000)
                                     .nOut(28 * 28)
                                     .activation(Activation.RELU)
                                     .build())
                        .pretrain(false).backprop(true)
                        .build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        return model;
}
</code></pre>
<p>这里我们做下解释。首先与基于 MLP 的自编码器相比，每一层我们使用 AutoEncoder 代替，并且每一层的噪声比例使用 .corruptionLevel 声明。在上面的逻辑中，高斯噪声的比例设为 0.3。其余的网络配置和 MLP 类似。下面我们来看下 MNIST 数据集基于降噪自编码器重构后的结果：</p>
<p><img src="https://images.gitbook.cn/06e016e0-f3cb-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>截图中，以 dae_gauss.jpg 结尾的图片是基于降噪编码器重构出来的结果。从图中可以看出，对比直接使用基于 MLP 的自编码器的结果，加入高斯噪声的降噪自编码器效果略差，部分重构内容不够准确。</p>
<blockquote>
  <p>注意：由于作者在验证不同编码器的顺序不同，所以截图中已经有了基于 RBM 的结果，这里读者可以先忽略。</p>
</blockquote>
<h3 id="42">4.2 基于深度信念网络的自编码器</h3>
<p>深度信念网络（Deep Belief Network，DBN）是由一系列受限玻尔兹曼机（Restricted Boltzmann Machine，RBM）堆叠而成的一种神经网络。这里我们先简单介绍下受限玻尔兹曼机。</p>
<p>受限玻尔兹曼机源于玻尔兹曼机（Boltzmann Machine，BM）。BM 的网络拓扑结构可见如下示意图：</p>
<p><img src="https://images.gitbook.cn/c154d240-f9f7-11e8-98b8-21d1b727d9e8" alt="enter image description here" /></p>
<p>BM 拓扑中所有单元/神经元相互连接，往往可以分为可见单元层和隐藏单元层。在上面的截图中即含有 3 个可见单元和 4 个隐藏单元。</p>
<p>将玻尔兹曼机同层单元间的连接去除后就形成了受限玻尔兹曼机的拓扑，这也是其所谓“受限”的地方。</p>
<p><img src="https://images.gitbook.cn/adffa0b0-fc29-11e8-8576-39c4102c68fe" alt="enter image description here" /></p>
<p>下面介绍下基于受限玻尔兹曼机重构数据的原理（这里引用下 Deeplearning4j 官网的图解：<a href="https://skymind.ai/wiki/restricted-boltzmann-machine">https://skymind.ai/wiki/restricted-boltzmann-machine</a>）。</p>
<p><img src="https://images.gitbook.cn/725ac0d0-fe27-11e8-9206-ebae2af18c23" alt="enter image description here" /></p>
<p>如上图，输入向量经过可视层（Visible Layer）进入到神经网络中，并和全连接网络一样向前传播，通过隐藏层（Hidden Layer）。如果有多个受限玻尔兹曼机堆叠，则前一层隐藏层的输出会作为下一层可视层的输入。下面我们看下反向传播的场景：</p>
<p><img src="https://images.gitbook.cn/085e12d0-fe28-11e8-9206-ebae2af18c23" alt="enter image description here" /></p>
<p>当数据一层一层地反向传播到第一层的 RBM 时，此时输入是从原先定义的隐藏层输入，从可视层输出。可视层的输出就是所谓重建后的数据。需要注意的是，RBM 可视层和隐藏层之间的权值在前向和后向传播是是同一组。最后介绍下损失函数，对于重构数据，一般我们使用 KL 散度/相对熵作为损失函数。下面分别是 KL 散度的数学函数式和实例图：</p>
<div style="text-align:center"><img src="https://images.gitbook.cn/eb64f850-fe28-11e8-9206-ebae2af18c23" width="70%" /></div>
<p></br></p>
<p><img src="https://images.gitbook.cn/1f7c3c70-fe29-11e8-9206-ebae2af18c23" alt="enter image description here" /></p>
<p>通俗地讲，KL 散度（KL-divergence）是用于衡量两个函数分布的相近程度。对于重构问题来说，图中的 $p(x)$ 和 $q(x)$ 可以认为是原始输入和输出的重构。它们各自服从某种函数分布。当两个分布逐渐趋同，即重构的数据越准确，隐藏层的输出结果也即压缩/降维结果越具信息量。</p>
<p>下面我们尝试用堆叠的 RBM 即深度信念网络压缩 MNIST 数据集。网络的定义如下：</p>
<pre><code>private static MultiLayerNetwork DBN(){
        MultiLayerConfiguration conf = new NeuralNetConfiguration.Builder()
                        .learningRate(0.01)
                        .learningRateScoreBasedDecayRate(0.5)
                        .seed(12345L)
                        .optimizationAlgo(OptimizationAlgorithm.LINE_GRADIENT_DESCENT)
                        .updater(Updater.ADAM).adamMeanDecay(0.9).adamVarDecay(0.999)
                        .list()
                        .layer(0, new RBM.Builder().nIn(28 * 28).nOut(1000).hiddenUnit(HiddenUnit.IDENTITY).visibleUnit(VisibleUnit.IDENTITY)
                                       .activation(Activation.RELU).lossFunction(LossFunctions.LossFunction.KL_DIVERGENCE).build())
                        .layer(1, new RBM.Builder().nIn(1000).nOut(500).hiddenUnit(HiddenUnit.IDENTITY).visibleUnit(VisibleUnit.IDENTITY)
                                        .activation(Activation.RELU).lossFunction(LossFunctions.LossFunction.KL_DIVERGENCE).build())
                        .layer(2, new RBM.Builder().nIn(500).nOut(250).hiddenUnit(HiddenUnit.IDENTITY).visibleUnit(VisibleUnit.IDENTITY)
                                        .activation(Activation.RELU).lossFunction(LossFunctions.LossFunction.KL_DIVERGENCE).build())
                        .layer(3, new RBM.Builder().nIn(250).nOut(500).hiddenUnit(HiddenUnit.IDENTITY).visibleUnit(VisibleUnit.IDENTITY)
                                        .activation(Activation.RELU).lossFunction(LossFunctions.LossFunction.KL_DIVERGENCE).build())
                        .layer(4, new RBM.Builder().nIn(500).nOut(1000).hiddenUnit(HiddenUnit.IDENTITY).visibleUnit(VisibleUnit.IDENTITY)
                                        .activation(Activation.RELU).lossFunction(LossFunctions.LossFunction.KL_DIVERGENCE).build())
                        .layer(5, new OutputLayer.Builder(LossFunctions.LossFunction.MSE).activation(Activation.RELU).nIn(1000).nOut(28*28).build())
                        .pretrain(true).backprop(true)
                        .build();
        MultiLayerNetwork model = new MultiLayerNetwork(conf);
        return model;
}
</code></pre>
<p>这里对上述网络的定义做些解释。我们共定义了 5 层的网络，每一层都是单独的一层 RBM 网络。RBM 的网络的可视层和隐藏层都使用了线性激活函数，读者可以根据需要选择伯努力、高斯等激活策略。由于每一层的 RBM 都有重构输出，因此我们在每一层都定义一下损失函数。在输出层，我们使用 MSE 作为 fine-tune（微调）整个网络的损失函数。另外数据的读取和之前描述的基于多层感知机压缩的逻辑是一样的，这里就不再赘述了。训练参数同样是 50 个 epoch 和 batchSize 等于 32。下面我们看下结果的截图：</p>
<p><img src="https://images.gitbook.cn/66cf0a50-f3cd-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>在截图中，文件名以 dae_rbm.jpg 结尾的图片是用 DBN 重构的图片。通过和原图包括基于 MLP 重构的图片比较，和原图还是有一定的差别，但和 MLP 重构出来的图片质量相当。</p>
<h3 id="43">4.3 变分自编码器</h3>
<p>变分自编码器（Variational AutoEncoder）也是一种生成式模型。VAE 同样分为 Encoder 层和 Decoder 层（这在下面 Deeplearning4j 代码的截图中也可以看到）。和上面介绍的自编码器不同的是，VAE 中编码出的高维空间特征向量服从高斯分布，而传统编码器则没有这个约束。也正是因为这样 VAE 中 Encoder 层的作用是计算输入的均值和方差，而不是得到特征向量的分布。换句话说，从 Decoder 层的角度去看，输出/重构的数据是从对服从高斯分布的数据进行采样后，输出到解码器中得到的。但也正是由于特征向量的元素是从高斯分布中采样的，因此会引入噪声。VAE 希望的其实也是在引入噪声的基础上将信息尽可能准确还原，起到降噪的作用。</p>
<p>下面看下建模逻辑：</p>
<pre><code>private static MultiLayerNetwork VAE(){
        MultiLayerConfiguration conf = new NeuralNetConfiguration.Builder()
                        .seed(1234)
                        .learningRate(0.01)
                        .learningRateScoreBasedDecayRate(0.5)
                        .updater(Updater.ADAM)
                        .weightInit(WeightInit.XAVIER)
                        .list()
                        .layer(0, new VariationalAutoencoder.Builder()
                            .activation(Activation.LEAKYRELU)
                            .encoderLayerSizes(1000, 500)        
                            .decoderLayerSizes(500, 1000)        
                            .pzxActivationFunction(Activation.IDENTITY) 
                            .reconstructionDistribution(new BernoulliReconstructionDistribution(Activation.SIGMOID.getActivationFunction())) 
                            .nIn(28 * 28)              
                            .nOut(250)                            
                            .build())
                        .pretrain(true).backprop(false).build();

                    MultiLayerNetwork net = new MultiLayerNetwork(conf);
                    net.init();
        return net;
}
</code></pre>
<p>这里解释下上面的建模逻辑。和之前的网络类似，我们配置一个多层的网络，其中第一层即是 VAE 层。encoderLayerSizes 和 decoderLayerSizes 用来配置编解码的神经元的数量。reconstructionDistribution 用来指定高维空间特征向量服从的分布，目前 Deeplearning4j 可以支持高斯分布、伯努力分布等。训练部分的逻辑和之前的类似，我们直接看下重构的逻辑。</p>
<pre><code>org.deeplearning4j.nn.layers.variational.VariationalAutoencoder vae
      = (org.deeplearning4j.nn.layers.variational.VariationalAutoencoder) trainedModel.getLayer(0);
INDArray latent = vae.activate(features,false);
INDArray recontruct = vae.generateAtMeanGivenZ(latent);
recontruct = recontruct.mul(255);
//...省略保存图片的逻辑
</code></pre>
<p>在上述的重构逻辑中，trainedModel 是我们加载的之前训练好的 VAE 模型。我们取出第一层的网络也就是 VAE 自身，在一次强制类型转换后，获取 VAE 的对象引用。features 是向量形式的图片数据，并直接调用激励函数方法 activate 获得高维特征向量，也就是逻辑中的 latent 对象。最后我们调用 generateAtMeanGivenZ 接口获得重构后的图像数据。下面我们看下重构的结果截图：</p>
<p><img src="https://images.gitbook.cn/bd51d730-f3ce-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/d0106cb0-f3ce-11e8-b6c3-2b03a92d8fdd" alt="enter image description here" /></p>
<p>截图中以 vae.jpg 结尾是基于 VAE 重构出来的结果。从我们用红框框选出来的结果来看，VAE 的重构结果总体比较模糊，甚至还有像最后一张“9”的图重构出来的结果很像是“3”。对于 VAE 的使用这里只给出简单的例子，更多调参和使用，读者可以在本次课程的基础上进一步做研究。</p>
<h3 id="44">4.4 小结</h3>
<p>本次课程主要介绍了基于多层感知机、受限玻尔兹曼机还有变分自编码器，对 MNIST 数据集进行压缩并重构的结果。对于以上这些自编码器的形式，Deeplearning4j 都提供了直接的支持。不过需要注意的是，在最新版本的 Deeplearning4j 中，受限玻尔兹曼机已经被移除，因此如果需要继续使用 RBM 或者 DBN 的话，需要使用相对老版本的 Deeplearning4j。</p>
<p>自编码器的使用场景很多，尤其在缺少标注的场景中，自编码器可以获取数据潜在的语义信息，并用于后期的检索或分类，一定程度上省去了特征工程的部分工作。</p>
<p>另外值得一提的是对于另一种生成模型——对抗生成网络（Generative Adversarial Network，GAN）在 1.0.0-alpha/beta 版本中因为引入了解卷积和上采样而可以直接支持，并且在Model Zoo 中已经在开发相关内容（<a href="https://github.com/deeplearning4j/deeplearning4j/issues/5005">https://github.com/deeplearning4j/deeplearning4j/issues/5005</a>）。如果读者着急使用的话，还可以通过导入 Keras 的模型来实现（导入 Keras 模型的工作在后面的课程中会专门介绍）。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="http://yann.lecun.com/exdb/mnist/">手写体数字 MNIST 数据集</a></li>
<li><a href="https://skymind.ai/wiki/restricted-boltzmann-machine">基于受限玻尔兹曼机重构数据的原理图解</a></li>
<li><a href="https://github.com/deeplearning4j/deeplearning4j/issues/5005">对抗生成网络（Generative Adversarial Network，GAN）的支持</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>