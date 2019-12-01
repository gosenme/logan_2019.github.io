---
title: Deeplearning4j 快速入门-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一课中总体介绍了开源深度学习框架 Deeplearning4j 的相关内容，从本节课开始，我们将逐步讨论 Deeplearning4j 的使用，先来介绍如何在 Windows、Mac OS X 和 Linux 上搭建相应的开发环境。本节课核心内容包括：</p>
<ul>
<li>Deeplearning4j on Windows</li>
<li>Deeplearning4j on Mac OS X</li>
<li>Deeplearning4j on Linux</li>
</ul>
<p>首先，在 Windows/Linux/Mac 系统上，操作系统需要 64 位的（早期的版本支持 32 位，但由于训练深度神经网络需要大量内存，而 32 位系统访问内存有限，因此后期的版本只支持 64 位系统）。</p>
<p>其次，由于 Deeplearning4j 是基于 JVM 的框架，因此 JDK 必须安装，JDK 版本推荐 1.7 以上。由于篇幅关系，这里不再赘述 JDK 的相关安装，请读者自行阅读 Oracle 相关文档进行 JDK 的安装和相关环境变量的设置。</p>
<p>再者，Deeplearning4j 依赖以及间接依赖的库很多，比如 JavaCPP、JavaCV、Guava、Spark 等。所以我们需要用类似 Maven 的 JAR 包管理工具进行依赖的引入。下面就详细介绍如何在 Windows、Mac OS X 和 Linux 上搭建开发环境。</p>
<h3 id="11deeplearning4jonwindows">1.1 Deeplearning4j on Windows</h3>
<p>首先介绍在 Windows 系统下的环境搭建（笔者的系统是 Win7，IDE 环境是 Eclipse）。  </p>
<ul>
<li>Step1：新建 Maven 工程，并配置 JDK 版本在 1.7 以上。</li>
<li>Step2：POM 配置文件添加 Deeplearning4j 的相关依赖，笔者这里选择的 0.8.0 版本，读者可以结合自身的使用情况选择相应的版本。</li>
<li>Step3：使用 ND4J 创建并操作简单的张量运算，验证环境是否配置正确。  </li>
</ul>
<h4 id="111">1.1.1 基本依赖</h4>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.nd4j&lt;/groupId&gt;
    &lt;artifactId&gt;nd4j-native&lt;/artifactId&gt;
    &lt;version&gt;${nd4j.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
    &lt;artifactId&gt;deeplearning4j-core&lt;/artifactId&gt;
    &lt;version&gt;${dl4j.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>以上分别为 ND4J 和 Deeplearning4j 的 Maven 依赖，也是最基本的依赖。其中，ND4J 会根据系统的不同下载相应的 Java 本地库。如果开发人员希望下载所有系统的本地库，可以把依赖改成 nd4j-native-platform。</p>
<p>Deeplearning4j 的 Maven 的依赖<a href="https://github.com/deeplearning4j/deeplearning4j/tree/master">请参考这里</a>，还有其相关依赖库的编译后的 JAR，里面包含了各种神经网络结构的实现、训练和预测模块。</p>
<h4 id="112spark">1.1.2 Spark 依赖</h4>
<p>如果读者希望在 Apache Spark 建模，那么需要添加一下 dl4j-spark 的依赖库：  </p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
    &lt;artifactId&gt;dl4j-spark_${scala.binary.version}&lt;/artifactId&gt;
    &lt;version&gt;${dl4j.version}_spark_{spark.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.nd4j&lt;/groupId&gt;
    &lt;artifactId&gt;nd4j-kryo_${scala.binary.version}&lt;/artifactId&gt;
    &lt;version&gt;${nd4j.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>研发人员不需要额外添加 Spark 的依赖，因为 dl4j-spark 会间接依赖到 Spark 相关的 JAR 包，dl4j-spark 的依赖需要注意 Scala 和 Spark 的版本。由于 Deeplearning4j 同时支持 1.5.x/1.6.x 和 2.x 的 Spark，所以需要根据实际情况指定 Scala 和 Spark 的版本。而其中 nd4j-kryo 的依赖则是 ND4J 在不同版本下支持的 Kryo 序列化格式。</p>
<blockquote>
  <p>注意：在 0.6.0 之前的版本中，可以用 Java 默认的序列化格式；但在 0.8.0 之后会强制使用 Kryo 的序列化格式，不然会运行报错。</p>
</blockquote>
<p>以下是 Maven 中心仓库的截图：</p>
<p><img src="https://images.gitbook.cn/21b62b60-f2fb-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<h4 id="113gpu">1.1.3 GPU 依赖</h4>
<p>如果读者希望在 GPU 环境下进行建模，那么可以添加以下配置：</p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.nd4j&lt;/groupId&gt;
    &lt;artifactId&gt;nd4j-cuda-8.0&lt;/artifactId&gt;
    &lt;version&gt;${nd4j.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>笔者自身使用的 CUDA 版本是 8.0，并且 Deeplearning4j 在 0.9.0 后同时支持 CUDA 8.0/9.0 的版本（7.0 不再支持），因此推荐读者安装 8.0 以后的 CUDA 版本。</p>
<h4 id="114">1.1.4 数据预处理的依赖（非必须）</h4>
<p>最后，如果需要使用 DataVec 相关的功能（不是必须），那么可以添加如下依赖：  </p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.datavec&lt;/groupId&gt;
    &lt;artifactId&gt;datavec-api&lt;/artifactId&gt;
    &lt;version&gt;${datavec.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.datavec&lt;/groupId&gt;
    &lt;artifactId&gt;datavec-data-image&lt;/artifactId&gt;
    &lt;version&gt;${datavec.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.datavec&lt;/groupId&gt;
    &lt;artifactId&gt;datavec-data-audio&lt;/artifactId&gt;
    &lt;version&gt;${datavec.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.datavec&lt;/groupId&gt;
    &lt;artifactId&gt;datavec-spark_${scala.binary.version}&lt;/artifactId&gt;
    &lt;version&gt;${dl4j.version}_spark_{spark.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>其中，datavec-data-image/datavec-data-audio 中封装了对图像和音频的相关预处理的模块，而 <code>datavec-spark_${scala.binary.version}</code> 封装了很多在 Spark 集群上预处理数据的功能。此外，还有单独为 NLP 封装的组件，这在后面的内容中会逐步提到，这里就不再详述。</p>
<h4 id="115">1.1.5 开发环境测试</h4>
<p>根据之前的介绍，在选择适当的开发环境（CPU/GPU/单机/分布式）并引入对应的依赖之后，我们需要写个简单的程序来验证开发环境是否搭建成功。我们以本地单机为例，添加最基本也是最必要的 ND4J 和 Deeplearning4j 的依赖，并测试 ND4J 的相关代码：</p>
<pre><code>import java.io.IOException;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

public class ND4j_create {
    public static void main(String[] args) throws IOException{
        System.out.println(Nd4j.getBackend());
        INDArray tensor1 = Nd4j.create(new double[]{1,2,3});
        INDArray tensor2 = Nd4j.create(new double[]{10.0,20.0,30.0});
        System.out.println(tensor1.add(tensor2));
    }
}
</code></pre>
<p>这个简单的张量相加的例子是为了测试之前的安装是否成功，同时通过这个例子也可以了解 ND4J 的基本使用。测试结果如下：</p>
<p><img src="https://images.gitbook.cn/591b93a0-f2fc-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p>上面介绍了在 Windows 上搭建环境的流程，以及不同环境下对应的 Maven 依赖。读者需要注意的是，这里我们并没有介绍在 Windows 系统上编译源码，有两个原因：</p>
<ul>
<li>第一，Windows 上编译源码较为复杂，一般需要安装 MinGW 或者 MSYS2，并且按照 LibND4J → ND4J → DataVec → Deeplearning4j 的编译顺序挨个编译，步骤比较繁琐容易出错；</li>
<li>第二，官方目前并不建议用户自己编译源码，尤其在 Windows 平台上，一般搭建 Maven 工程就行了；但在 Linux 上，官方提供了一栈式的脚本进行编译。</li>
</ul>
<h3 id="12deeplearning4jonmacosx">1.2 Deeplearning4j on Mac OS X</h3>
<p>在 Mac 系统上搭建 Deeplearning4j 的步骤和 Windows 类似，需要预先安装好 JDK 1.7 以上版本，以及 Eclipse 或 IntelliJ IDEA 等 IDE 开发环境。在新建完 Maven 工程后，将 1.1 部分提到的 Maven 依赖添加到 pom.xml 文件中，Deeplearning4j 的相关依赖就可以自动下载下来，完成 Mac 上开发环境的配置。</p>
<p>下面是一张参考的截图：</p>
<p><img src="https://images.gitbook.cn/2bf6ed40-fe03-11e8-b003-8d9a607f51c2" alt="enter image description here" /></p>
<p>截图中的示例即为 1.1 中 ND4J 运算例子在 Mac OS X 系统上的运行结果。由于和 Windows 上开发的过程一致，这里就不再赘述了。</p>
<h3 id="13deeplearning4jonlinux">1.3 Deeplearning4j on Linux</h3>
<p>下面简单介绍下在 Linux 环境中，对 Deeplearning4j 的源码进行编译和环境搭建的过程。</p>
<ul>
<li>Step0：安装 JDK 1.8 以上以及 Maven（安装完成后通过 <code>java -version</code> 和 <code>mvn -v</code> 进行版本验证）。</li>
<li>Step1：将 master 分支和 examples 的代码克隆到本地。</li>
<li>Step2：<code>cd</code> 到源码根目录下，并执行脚本 build-dl4j-stack.sh，接下来会根据脚本依次编译 Deeplearning4j 的各个模块并生成本地代码库。</li>
<li>Step3：如果 Step2 顺利完成，则 <code>cd</code> 到 examples 的根目录下，编译各个子目录下的代码，并执行 MNIST 数据集的例子做相关验证。</li>
</ul>
<h4 id="131">1.3.1 源码编译</h4>
<pre><code>$ git clone https://github.com/deeplearning4j/deeplearning4j.git
$ cd deeplearning4j/
$ sudo ./build-dl4j-stack.sh
</code></pre>
<p>需要注意的是，在编译最新的 master 分支的代码时，Deeplearning4j 所依赖的库 LibND4J 需要 GCC 4.9 及 CMake 3.6 以上版本支持，ND4J 需要依赖 JDK 1.8 以上版本支持，否则会提示错误。如果出现版本低的错误提示，请读者先自行升级 JDK、GCC 和 CMake。  </p>
<p>另外笔者选择的各软件版本如下。</p>
<ul>
<li>JDK：1.8.0_131</li>
<li>GCC/G++：5.3.0</li>
<li>CMake：3.6.0</li>
</ul>
<p><strong>ND4J 编译的截图</strong>：</p>
<p><img src="https://images.gitbook.cn/4babb7c0-f2fe-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p><strong>Deeplearning4j 编译的截图</strong>：</p>
<p><img src="https://images.gitbook.cn/65c7fba0-f2fe-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p>整个工程的编译时间较长，一般需要若干个小时。更多有关本地编译的信息可以参考链接，<a href="https://deeplearning4j.org/buildinglocally">详见这里</a>。</p>
<p>当成功编译完源码后，我们将官网的 examples 克隆至本地，并运行其中 MNIST 数据集的例子。</p>
<h4 id="132">1.3.2 示例测试</h4>
<pre><code>$ git clone https://github.com/deeplearning4j/dl4j-examples.git
$ cd dl4j-examples/
$ mvn clean install 
</code></pre>
<p>dl4j-examples 成功编译完后，我们运行一下根目录下的脚本程序 runexamples.sh，运行该脚本会给出样例库中的所有例子，并且每一个例子有对应的编号，我们只需要输入例子的编号即可运行其中的样例。</p>
<p><strong>首先是编译 examples 成功后的截图</strong>：</p>
<p><img src="https://images.gitbook.cn/bf023cd0-f2fe-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p><strong>其次是运行样例执行脚本后的选择页面</strong>：</p>
<p><img src="https://images.gitbook.cn/d2757c50-f2fe-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p><strong>我们选择其中利用多层感知机进行 MNIST 分类的例子</strong>：</p>
<p><img src="https://images.gitbook.cn/ecd64340-f2fe-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p><strong>最终运行以及评估的结果</strong>：</p>
<p><img src="https://images.gitbook.cn/03e87b70-f2ff-11e8-8d28-f50de28a2376" alt="enter image description here" /></p>
<p>这里对上述基于 MLP 的 MNIST 分类例子进行说明。</p>
<blockquote>
  <p>首先，<a href="http://yann.lecun.com/exdb/mnist/">MNIST 数据集</a> 是一个手写体数字 0~9 的灰度图，且大小为 28*28 的开源数据集。我们可以基于不同的模型对这 10 类图片进行分类建模，那么上面跑的例子，是基于多层感知机的传统神经网络模型进行的建模、训练和评估。</p>
</blockquote>
<p>在这里，主要的任务是跑通示例，对其中的网络结构、超参数配置不做过多的说明。在今后的课程中，尤其是在卷积神经网络使用的课程中，我们会进一步对该数据集，以及另一个类似的数据集 Fashion-MNIST 进行一些对比和探讨，同时我们会比较 MLP 和 CNN 在这些数据集上的表现。</p>
<h3 id="14">1.4 小结</h3>
<p>以上是 Deeplearning4j 在 Windows、Mac OS X 和 Linux 上的环境搭建过程，由于编译所有分支源码非常耗时，因此官网不建议直接编译源码，一般搭建环境只需要在配置好 Java 和 Maven 的环境下进行开发即可。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://github.com/deeplearning4j/deeplearning4j/tree/master">Deeplearning4j 的 Maven 的依赖</a></li>
<li><a href="http://yann.lecun.com/exdb/mnist/">MNIST 数据集</a></li>
<li><a href="https://github.com/AllenWGX/CSDN-GitChat-DL4j-Course">课程源码下载</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>