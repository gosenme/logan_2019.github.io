---
title: 深度学习 PyTorch 极简入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>之前的课程中，我们介绍的都是传统神经网络结构，也称为全连接层神经网络。传统神经网络在许多应用中都有着不错的表现和性能。但是在某些领域问题中，其性能受限，表现却并不完美。因此，本文我们将讨论一种新的神经网络结构：卷积神经网络（Convolutional Neural Networks，CNN）。</p>
<h3 id="cnn">为什么选择 CNN</h3>
<p>在机器视觉（Computer Vision，CV）、图像识别领域，传统神经网络结构存在两个缺点：</p>
<ul>
<li><p>输入层维度过大。例如一张 64x64 的三通道图片，神经网络输入层的维度为 12288。如果图片尺寸较大，是 1000x1000 的三通道图片，神经网络输入层的维度将达到三百万，使网络权重 W 数值非常庞大。这样会造成两个后果，一是神经网络结构复杂，样本训练集不够，容易出现过拟合；二是训练网络所需的内存和计算量都十分庞大，模型训练更加困难。</p></li>
<li><p>不符合图像特征提取的机制。我们知道传统神经网络是将二维或者三维（包含 RGB 三通道）图片拉伸成一维特征，作为神经网络的输入层。这种操作实际上是将图片的各个像素点独立开来，忽略了各个像素点之间的区域性联系。而我们知道，图片是以区域特征为基础的，比如图片的这块区域组成了眼睛，那块区域组成了鼻子。人脸的视觉机制也是从边缘、轮廓、局部特征等等来捕获图片信息的。传统神经网络结构并不具备这样的功能，因此在性能上不会表现得特别突出。</p></li>
</ul>
<p>基于传统神经网络的这两个缺点，一种新的神经网络结构：卷积神经网络应运而生。接下来我们就开始详细介绍 CNN。</p>
<h3 id="">边缘检测</h3>
<p>在介绍 CNN 之前，我们先来了解一下图片的边缘检测。</p>
<p>图片的边缘检测是图像处理中最常用的算法之一，其目的是检测图片中包含的边缘信息，例如水平边缘、垂直边缘等轮廓信息。效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/81179ca0-b4c7-11e8-a745-899a3978c7b7" alt="enter image description here" /></p>
<p>其实边缘检测算法原理非常简单，只需将图片与相应的边缘检测算子进行卷积操作即可。举例来说，垂直边缘检测和水平边缘检测的滤波器算子如下所示：</p>
<p><img src="https://images.gitbook.cn/a00f5b60-b4c8-11e8-a745-899a3978c7b7" alt="enter image description here" /></p>
<p>然后，就可以将图片与相应的滤波器算子进行卷积操作，以水平边缘检测为例：</p>
<p><img src="https://images.gitbook.cn/d98a0480-b4c8-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p>注意，CNN 中的卷积并不是真正意义上的卷积操作。实际上，真正的卷积运算会先将滤波器算子绕其中心旋转 180 度，然后再在原始图片上进行滑动计算。旋转过程如下所示：</p>
<p><img src="https://images.gitbook.cn/9f6ff1a0-b4c9-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p>为了简化计算，我们一般会对 CNN 中的卷积运算进行简化。之所以可以这么做，是因为滤波器算子一般水平或垂直对称，180 度旋转对其影响不大，而且最终滤波器算子需要通过 CNN 网络梯度下降算法计算得到，旋转过程可以看作已包含在 CNN 模型算法中。总的来说，忽略旋转运算可以大大提高 CNN 网络运算速度，而且不影响模型性能。</p>
<h4 id="padding">padding</h4>
<p>根据上面讲解得图片卷积，如果原始图片尺寸为 n x n，滤波器算子大小为 f x f，则卷积后的图片尺寸为 (n-f+1) x (n-f+1)，注意 f 一般为奇数。这样会带来两个问题：</p>
<ol>
<li>卷积运算后，输出图片尺寸缩小；</li>
<li>原始图片边缘信息对输出贡献少，输出图片丢失边缘信息。</li>
</ol>
<p>为了解决图片缩小的问题，可以使用 padding 方法，即把原始图片尺寸进行扩展，扩展区域补零，用 p 来表示每个方向扩展的宽度。</p>
<p><img src="https://images.gitbook.cn/c5fe08b0-b4cf-11e8-8cec-e73b093e0df7" alt="enter image description here" /></p>
<p>经过 padding 之后，原始图片尺寸为 (n+2p) x (n+2p)，滤波器算子尺寸为 f x f，则卷积后的图片尺寸为 (n+2p-f+1) x (n+2p-f+1)。若要保证卷积前后图片尺寸不变，则 p 应满足：</p>
<p>$$p=\frac{f-1}{2}$$</p>
<h4 id="stride">Stride</h4>
<p>Stride 表示滤波器算子每次在原图片中水平方向和垂直方向的步进长度。之前我们默认 stride=1。若 stride=2，则表示滤波器算子每次步进长度为 2，即隔一点移动一次。</p>
<p><img src="https://images.gitbook.cn/9529ec30-b4d0-11e8-a745-899a3978c7b7" alt="enter image description here" /></p>
<p>我们用 s 表示 stride 长度，用 p 表示 padding 长度，如果原始图片尺寸为 n x n，滤波器算子尺寸为 f x f，则卷积后的图片尺寸为：</p>
<p>$$\lfloor\frac{n+2p-f}{s}+1\rfloor\ X\ \lfloor\frac{n+2p-f}{s}+1\rfloor$$</p>
<p>上式中，$\lfloor\cdots\rfloor$表示向下取整。</p>
<h3 id="cnn-1">CNN 结构</h3>
<p>好了，介绍完边缘检测和图片的卷积运算之后，我们重点来查下 CNN 的模型结构。</p>
<p>首先，图片是三通道的情况下，其卷积过程如下图所示：</p>
<p><img src="https://images.gitbook.cn/df7c9b10-b4d1-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p>上图中，左边的图片由 RGB 三个通道组成，分别对应着红绿蓝三种颜色。黄色部分表示滤波器算子，尺寸大小是 3x3，每个滤波器算子包含 3 个滤波器，分别对应原图片中的三通道。卷积运算时，各个通道分别与其对应的滤波器算子进行卷积运算，各个通道得到的结果求和作为相应位置的输出。本例中，s=1，p=0，n=6，f=3，则卷积后的图片尺寸为：</p>
<p>$$\lfloor\frac{n+2p-f}{s}+1\rfloor=\frac{6+2\cdot 0-3}{1}+1=4$$</p>
<p>即 4x4。</p>
<p>知道了基本的卷积运算之后，我们就来看一个最简单的不包含激活层 1-Layer 的卷积神经网络结构。</p>
<p><img src="https://images.gitbook.cn/2cce1590-b4d4-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p>其实，这张图跟上面那张图唯一的差别就是包含了两组滤波器算子。其原理是为了进行多个卷积运算，实现更多边缘检测，可以增加更多的滤波器组。例如设置第一个滤波器组实现垂直边缘检测，第二个滤波器组实现水平边缘检测。这样，不同滤波器组卷积就得到不同的输出。最后的输出维度由滤波器组的个数决定。</p>
<p>若输入图片的尺寸为 n x n x $n_c$，滤波器组的尺寸为 f x f x $n_c$，则卷积后的图片尺寸为 (n-f+1) x (n-f+1) x $n_c'$。其中，$n_c$ 为图片通道数目，$n_c'$ 为滤波器组个数。</p>
<p>接着，再复杂一些，加上激活层，1-Layer 的 CNN 结构如下图所示：</p>
<p><img src="https://images.gitbook.cn/61a09df0-b4d5-11e8-a745-899a3978c7b7" alt="enter image description here" /></p>
<p>在卷积运算之后，会对结果加上偏移常数 b，再进行激活函数的非线性运算。此过程与标准的神经网络单层结构非常类似：</p>
<p>$$Z^{[l]}=W^{[l]}A^{[l-1]}+b$$</p>
<p>$$A^{[l]}=g^{[l]}(Z^{[l]})$$</p>
<p>卷积运算对应着上式中的乘积运算，滤波器组数值对应着权重 $W^{[l]}$，所选的激活函数为 ReLU。</p>
<p>我们来计算下上图中所有参数的数量：每个滤波器组有 3x3x3=27 个参数，还有 1 个偏移量 b，则每个滤波器组有 27+1=28 个参数，两个滤波器组总共包含 28x2=56 个参数。我们发现，选定滤波器组后，参数数量与输入图片尺寸大小无关。所以就避免了由于图片尺寸过大，造成参数过多的情况发生。这样大大简化了模型的复杂度，提高了模型的运算速度和性能。</p>
<p>下面，我们总结下 CNN 单层结构的标记符号。</p>
<ul>
<li>输入维度为：$n_H^{[l-1]}$ x $n_W^{[l-1]}$ x $n_c^{[l-1]}$</li>
<li>每个滤波器组维度为：$f^{[l]}$ x $f^{[l]}$ x $n_c^{[l-1]}$</li>
<li>权重维度为：$f^{[l]}$ x $f^{[l]}$ x $n_c^{[l-1]}$ x $n_c^{[l]}$</li>
<li>偏置维度为：1 x 1 x 1 x $n_c^{[l]}$</li>
<li>输出维度为：$n_H^{[l]}$ x $n_W^{[l]}$ x $n_c^{[l]}$</li>
</ul>
<p>其中：</p>
<p>$$n_H^{[l]}=\lfloor \frac{n_H^{[l-1]}+2p^{[l]}-f^{[l]}}{s^{[l]}}+1 \rfloor$$</p>
<p>$$n_W^{[l]}=\lfloor \frac{n_W^{[l-1]}+2p^{[l]}-f^{[l]}}{s^{[l]}}+1 \rfloor$$</p>
<p>$l$ 为当前网络层数，$n_c^{[l-1]}$ 表示上一层滤波器组个数（或图片的通道数），$n_c^{[l]}$ 表示该层滤波器组个数。</p>
<p>这样，我们就能得到一个简单的 CNN 模型：</p>
<p><img src="https://images.gitbook.cn/f7460690-b4d7-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p>需要注意的是，$a^{[3]}$ 的维度是 7 x 7 x 40，最后将 $a^{[3]}$ 拉伸展开成一维向量，维度为 1960 x 1，然后连接最后一级输出层。输出层可以是一个神经元，即二元分类（Logistic）；也可以是多个神经元，即多元分类（Softmax）。最后得到预测输出 $\hat y$。</p>
<p>上面的 CNN 结构都只包含卷积层。除了卷积层之外，还有另外两种结构：池化层（Pooling Layer，POOL） 和全连接层（Fully Connect Layer，FC），下面分别介绍。</p>
<h4 id="pool">池化层 POOL</h4>
<p>在 CNN 中，池化层用来减小尺寸、提高运算速度，同样还能减小噪声的影响，让各特征更具有健壮性。池化层的做法比卷积层简单许多，没有卷积运算，最常用的做法是在滤波器算子滑动区域内取最大值，即 Max Pooling。具体做法如下图所示：</p>
<p><img src="https://images.gitbook.cn/6ee14f80-b4ff-11e8-ba91-df426e0e62ac" alt="enter image description here" /></p>
<p>Max Pooling 的好处是只保留区域内的最大值（特征），忽略其它值，减小噪声的影响，提高模型健壮性，而且计算量很小。值得注意的是，对于多通道，每个通道应该单独进行 Max Pooling 操作。</p>
<p>池化层的另一种做法是 Average Pooling。顾名思义，就是在滤波器算子滑动区域计算平均值。具体做法如下图所示：</p>
<p><img src="https://images.gitbook.cn/16bea360-b500-11e8-8cec-e73b093e0df7" alt="enter image description here" /></p>
<h4 id="fc">全连接层 FC</h4>
<p>全连接层更加简单易懂，就是将卷积层维度拉伸成一维向量。例如当前卷积层的维度是 20x20x10，则拉伸为全连接层的维度就是 4000。全连接层实际上就是 CNN 中的标准神经网络结构，一般出现在 CNN 末端，Softmax 层之前。</p>
<p>介绍完 POOL 和 FC 之后，我们来构造一个完整的 CNN 模型：</p>
<p><img src="https://images.gitbook.cn/e656c0c0-b501-11e8-ba91-df426e0e62ac" alt="enter image description here" /></p>
<p>上图中，CONV 层后面紧接一个 POOL 层，习惯性地将卷积层和后面的池化层称为一层，即 CONV1 和 POOL1 构成第一层，CONV2 和 POOL2 构成第二层。FC1、FC2、FC3 和 FC4 为全连接层，它跟标准的神经网络结构一致。最后是 Softmax 层，输出 $\hat y$。</p>
<h3 id="cnn-2">CNN 模型如何训练</h3>
<p>知道了 CNN 模型的基本结构之后，我们再来看看它是如何训练的。</p>
<p>CNN 模型的训练过程与标准神经网络的训练过程近乎一致，都是基于梯度优化的。开始训练时，CNN 中每一层的滤波器组包括的 FC 层各项参数都是随机初始化的。然后进行正向传播，计算模型的损失函数，再使用梯度下降算法及各种优化算法进行反向传播，更新各个滤波器组和 FC 层各项参数。经过多次迭代训练之后，各滤波器组和 FC 层各项参数都已训练完成，可使模型拥有较高的准确率。</p>
<p>CNN 模型的结构相对来说比较复杂，训练过程涉及复杂的计算，如果完全使用手动搭建的方式效率会很低。因此，建议使用各种成熟的深度学习框架来搭建 CNN 模型，例如 PyTorch。下一篇我们就将使用 PyTorch 搭建一个 CNN 模型，以解决图片识别的问题。</p>
<p>有一个问题，较其他模型，为什么 CNN 模型在图片识别上性能表现更优？首先，CNN 参数数目要少得多。一方面特征检测器（例如垂直边缘检测）对图片某块区域有用，同时也可能作用在图片其它区域；另一方面因为滤波器算子尺寸限制，每一层的每个输出只与输入部分区域内有关。其次，由于 CNN 参数数目较小，所需的训练样本也相对较少，在一定程度上不容易发生过拟合现象。而且，CNN 比较擅长捕捉区域位置偏移，也就是说 CNN 进行物体检测时，不太受物体所处图片位置的影响，增加了检测的准确性和系统的健壮性。</p>
<h3 id="cnnlenet5alexnetvgg">几个常用的 CNN 模型：LeNet-5、AlexNet、VGG</h3>
<p>接下来介绍几个常用的 CNN 模型。</p>
<h4 id="lenet5">LeNet-5</h4>
<p>LeNet-5 模型是 Yann LeCun 于1998年提出来的，它是第一个成功应用于数字识别问题的卷积神经网络。在 MNIST 数据中，它的准确率达到大约 99.2%。典型的 LeNet-5 结构包含 CONV layer、POOL layer 和 FC layer，顺序一般是 CONV layer -&gt; POOL layer -&gt; CONV layer -&gt; POOL layer -&gt; FC layer -&gt; FC layer -&gt; Output layer。上文介绍的 CNN 模型就是 LeNet-5：</p>
<p><img src="https://images.gitbook.cn/e91b2930-b507-11e8-ba91-df426e0e62ac" alt="enter image description here" /></p>
<p><strong>AlexNet</strong></p>
<p>AlexNet 模型是由 Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 共同提出的，其结构如下所示：</p>
<p><img src="https://images.gitbook.cn/8172cb70-b508-11e8-ba74-87184af855a0" alt="enter image description here" /></p>
<p><strong>VGG</strong></p>
<p>VGG-16 模型更加复杂一些，结构如下所示：</p>
<p><img src="https://images.gitbook.cn/a180f8b0-b508-11e8-a745-899a3978c7b7" alt="enter image description here" /></p>
<h3 id="-1">总结</h3>
<p>本文主要介绍了卷积神经网络模型 CNN 的基本结构以及使用 CNN 的原因，同时详细解释了边缘检测、padding、Stride 等基本概念。此外，由简单到复杂，推导了基本 CNN 的结构，包括池化层和全连接层。最后介绍了几种常见的 CNN 模型：LeNet-5、AlexNet、VGG。</p></div></article>