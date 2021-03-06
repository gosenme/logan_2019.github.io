---
title: Deeplearning4j 快速入门-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课将为大家介绍如何基于 GPU 加速 Deeplearning4j 的建模过程。首先我们将为大家介绍异构计算的基本框架和原理，包括主流的 GPU 供应商英伟达各系列显卡的相关情况；接着，结合 Deeplearning4j 的具体情况，我们将讲解如何在使用单 GPU 和多 GPU 情况下加速训练过程的相似步骤；最后，我们会介绍一些调优的手段并对本节课做下总结。本节课核心内容包括：</p>
<ul>
<li>异构计算框架加速深度学习</li>
<li>Deeplearning4j 对 GPU 的支持</li>
<li>Deeplearning4j 在多 GPU 环境下训练</li>
</ul>
<h3 id="151">15.1 异构计算框架加速深度学习</h3>
<p>我们日常接触的开发工作其实都是对 CPU 进行编程。应当说在过去的几十年，在摩尔定律还比较有效的时期内，大家将提升计算速度的注意力集中在 CPU 的工艺和晶体管的集成度上——高主频的 CPU 以及多核 CPU 相继面世，可以说，以英特尔为代表的 CPU 厂商长期占据着高性能计算服务的制高点。</p>
<p>但是，CPU 作为计算机系统的大脑所承担的控制和计算任务非常繁重，再加上近几年晶体管工艺的瓶颈逐渐显现，CPU 性能提升放缓，因此在面对现在庞大数据的计算和优化迭代任务时，往往显得力不从心。</p>
<p>与之相比的 GPU，本身就作为显示计算的器件存在，功能相对单一和独立，擅长大规模的矩阵/张量计算，因此目前很多主流的深度学习框架都支持基于 GPU 的加速模型训练。</p>
<p>以英伟达为代表的 GPU 厂商积极推动 GPU 工艺和计算能力的提升，先后推出了特斯拉、费米、开普勒、麦克斯韦、帕斯卡、伏特架构的高性能 GPU 计算卡。另外面向不同需求人群，英伟达的显卡又可以分为 GeForce、Tegra、ION、Quadro、Tesla 几个产品系列。目前面向企业 HPC 的主要产品是 Tesla 系列的显卡，下面给出的案例也会以 Tesla K80/P40 显卡为基础硬件（下面截图是 Tesla V100）。</p>
<p><img src="https://images.gitbook.cn/0a6d7690-fbd2-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>GPU 相比 CPU 拥有更多的核心数量，更多的计算单元。CPU 芯片上的很大一部分面积用于做 Cache，而 GPU 则不然。从工艺和晶体管数量看，在 2000 年前后 GPU 的晶体管集成度已经超越 CPU，它的并行处理能力不断增强。鉴于上面的诸多原因，GPU 拥有的强劲计算能力更适合科学计算。</p>
<p>但是早期，对 GPU 编程并不是一件容易的事情。调用诸如 OpenGL 的接口实现 GPU 编程成为早期的一种主要手段，但是并不方便，门槛也相对较高，因此 GPU 的潜力很大但一直未能被很好地挖掘。</p>
<p>英伟达推出的统一异构计算框架 CUDA（Compute Unified Device Architecture）较好地解决了这一问题，使得对 GPU 编程变得容易和高效了起来。CUDA 支持诸如 C/C++/Fortran 等高级编程语言，从开发者的角度来看，基于 CUDA 的编程逐渐变得和对 CPU 编程一样容易。虽然通过调用几个 CUDA 函数就可以使数据在 GPU 上跑起来，但是我们必须了解底层的一些机制，方便开发者进一步调优。</p>
<p>GPU 运算所需要的数据，都是直接或间接地来源于主机内存/CPU 内存。换句话说，当我们需要对一批数据进行科学计算时，我们依然需要先读取到 CPU 内存，然后通过 PCI-E 总线传输到 GPU 上，之后才可以对这些数据进行相应的计算。</p>
<p>数据传输/拷贝的过程是非常耗时的，其中涉及的每一个硬件环节都可能成为瓶颈，这也就是为什么有时候我们觉得 GPU 并没有那么快的原因。其实并非 GPU 慢了，而是慢在了其他环节。这一系列的复杂动作中，寻址的操作非常重要。</p>
<p>由于 CPU 和 GPU 拥有独立的地址空间，因此最传统的数据传输操作就是显示的拷贝，这是 CUDA 1.0 版本的做法。但这样的操作非常低效，如果有什么方式可以使 GPU “直接”访问 CPU 内存，那么数据传输的操作会高效得多。</p>
<p>从 CUDA 2.0 开始，映射锁页内存的支持使得被锁页的 CPU 内存映射到 GPU 的地址空间。这样 GPU 就可以直接读入这部分数据，即 DMA 方式，但是此时 CPU 和 GPU 的地址仍是不同的。</p>
<p>从 CUDA 4.0 开始支持统一寻址的方式，即将映射锁页内存的虚拟地址空间进行了统一，进一步提升了数据传输效率。值得一提的是，在多 GPU 环境下，除了以上的几种内存拷贝方式外，还可以有点对点（P2P）方式，即 GPU 之间的数据直接拷贝。</p>
<p>从硬件架构上，流处理器簇（Streaming Multiprocessor，SM）以及构成 SM 的流处理器（Streaming Processor，SP）是 GPU 并行计算的基础组件。流处理器，也就是我们通常意义上说的核心，决定了该卡的并行计算能力。当然目前的英伟达显卡集成了越来越多的 CUDA Core，计算能力当然也越来越强。另一方面，从软件架构上说，英伟达 GPU 的内核启动是以一个网格的形式（Grid）。网格包含了多个线程块，也就是我们常说的 Block，当然每个线程块是由具体的线程（Thread）构成的。线程块会驻留在 SM 当中，因此当内核将存储分配给 SM 中的线程后即可进行调度和计算。这里我们给出一张费米架构显卡的官网架构图：</p>
<p><img src="https://images.gitbook.cn/a28ac790-fbd5-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>从库应用来讲，CUDA 本身支持多种计算工具。例如，实现了快速傅立叶算法（FFT）的 cuFFT 模块，实现了标准线代操作的 cuBLAS，以及为深度学习定制的 cuDNN。CUDA 作为英伟达 GPU 编程者的重要开发套件，提供了友好的上层接口，使得开发者对 GPU 编程变得和 CPU 编程一样方便。</p>
<p>值得一提的是，异构计算框架加速建模并非只有 CPU + GPU 这唯一一种方案。除了 GPU，可编程门阵列也就是 FPGA 也同样得到了很大的关注。FPGA 相比于 GPU 拥有很低的数据延迟，并且不像 CPU 和 GPU 拥有固定的架构，FPGA 的架构是可变的，这样为开发者带来的灵活性是不言而喻的。目前，CPU + FPGA 的异构计算框架已经有许多工作和成果，有兴趣的同学可以查阅相关论文及产品。下面截图是 Xilinx 的 FPGA。</p>
<p><img src="https://images.gitbook.cn/ee814ec0-3105-11e9-b327-73590015031f" alt="enter image description here" /></p>
<h3 id="152deeplearning4jgpu">15.2 Deeplearning4j 对 GPU 的支持</h3>
<h4 id="1521">15.2.1 参数配置</h4>
<p>Deeplearning4j 支持大部分英伟达的 GPU 产品，包括 Tesla 和 GeForce 系列。其中，对 CUDA 的调用是通过 JavaCPP 技术实现的。JavaCPP 是一种 JNI 技术，目前已经对很多提供 C/C++ 接口项目的支持，比如：OpenCV、FFmpeg 以及 Caffe、TensorFlow 等深度学习项目。更多的信息可以参考 JavaCPP-Presets 的 <a href="https://github.com/bytedeco/javacpp-presets">GitHub 主页</a>相关信息。</p>
<p>在 Deeplearning4j 使用 GPU 训练模型，只需要声明一个 CUDA 实例就可以了。ND4J 的后台检测逻辑会自动检查平台所配置的相关 GPU 信息。我们来看一个实例：</p>
<pre><code>CudaEnvironment.getInstance().getConfiguration()
                .allowMultiGPU(true)
                .setMaximumDeviceCache(11L * 1024L * 1024L * 1024L)
                .allowCrossDeviceAccess(true);
</code></pre>
<p>使用 GPU 加速 Deeplearning4j 建模的步骤非常简单，只需要声明这样一个 CUDA 实例，设置一些必要的参数，ND4J 就会自动检测 
Backend 是 CPU 还是 GPU，如果是 CPU 默认就调用 OpenBLAS 进行张量计算，如果是 GPU，就调用 cuBLAS 以及 cuDNN 等进行相关的计算。我们看下 CUDA 实例可以设置的参数：</p>
<pre><code>.allowMultiGPU(boolean reallyAllow)                                //是否允许多GPU模式

.allowPreallocation(boolean reallyAllow)                        //是否允许预先分配存储空间

.allowCrossDeviceAccess(boolean reallyAllow)                    //是否允许点对点进行显卡间的数据读取

.banDevice(@NonNull Integer deviceId)                            //禁止使用某个设备/某张显卡

.setAllocationModel(@NonNull AllocationModel allocationModel)    //其中AllocationModel是枚举类型，可以取DIRECT, CACHE_HOST, CACHE_ALL三种模式。DIRECT表示无论主存还是显存都直接释放使用完的存储空间，CACHE_HOST则只在内存中缓存，CACHE_ALL表示内存和显存中都缓存。默认是最后一种。

.setExecutionModel(@NonNull ExecutionModel executionModel)        //张量运算的模式。ExecutionModel是一个枚举类型，支持SEQUENTIAL、ASYNCHRONOUS两种模式。

.setFirstMemory(@NonNull AllocationStatus initialMemory)
//这个参数决定了初始的训练数据存储的位置，是内存还是显存。AllocationStatus是一个枚举类型，支持HOST、DEVICE、DELAYED三种模式。HOST和DEVICE分别表示存储在内存和显存上。DELAYED表示首先存储在内存中，一旦使用就会进入显存。

.setMaximumBlockSize(int blockDim)/.setMinimumBlockSize(int blockDim)    //设置最大/最小线程块的数量

.setMaximumDeviceCacheableLength(long maxLen)                    //设置单个内存块的最大容量

.setMaximumDeviceMemoryUsed(double percentage)                     //设置显存使用的最大比例

.setMaximumGridSize(int gridDim)                                //通过设置网格总数来限制线程总量

.setMaximumZeroAllocation(long max)                                //最大主机内存

.setMaximumDeviceCache(long maxCache)                            //设置最大显存使用（字节为单位）
</code></pre>
<p>以上是 Deeplearning4j 中 CUDA 实例可以设置的一些常用参数，主要围绕着内存和显存的大小还有存储方式进行。这些配置项大部分都有默认的设置，在大部分情况下采用默认配置就可以满足需求。而一些需要根据显卡进行具体设置的包括：最大显存设置、是否允许多卡运行，以及多卡间的点对点数据拷贝等。如果用户希望用 cuDNN 进一步加速，可以参考如下示例：</p>
<pre><code>.layer(0, new ConvolutionLayer.Builder(5, 5)
            .nIn(nChannels)
            .stride(1, 1)
            .nOut(20)
            .activation(Activation.IDENTITY)
            .cudnnAlgoMode(AlgoMode.NO_WORKSPACE)    //cuDNN 设置
            .build())
</code></pre>
<p>AlgoMode 同样是个枚举类型，可以选择 PREFER_FASTEST 和 NO_WORKSPACE 两种值。它们分别代表不同的存储使用策略，后者的存储消耗会小于前者，而前者相较于后者会更加快速。</p>
<p>目前 Deeplearning4j 支持的 CUDA 版本从 7.0-&gt;10.0(snapshot) 都已经支持，用户可以根据实际情况进行选择。值得说明的是，由于 CUDA 版本和 cuDNN 的版本并不是一一对应的，所以用户可以人为指定版本的细节。具体的内容可以参考官网的相关文档：<a href="https://deeplearning4j.org/docs/latest/deeplearning4j-config-cudnn">https://deeplearning4j.org/docs/latest/deeplearning4j-config-cudnn</a>。</p>
<h4 id="1522">15.2.2 并行配置</h4>
<p>在多 GPU 环境下对 Deeplearning4j 进行建模也是非常容易。除了一样需要声明一个 CUDA 实例，还额外需要声明一个参数服务器。我们来看下下面的逻辑。</p>
<pre><code>DataTypeUtil.setDTypeForContext(DataBuffer.Type.FLOAT);    //FP Setting，HALF/FLOAT/DOUBLE

CudaEnvironment.getInstance().getConfiguration()
                        .allowMultiGPU(true)
                        .setMaximumDeviceCache(11L * 1024L * 1024L * 1024L)
                        .allowCrossDeviceAccess(true);
        //....
        //参数服务器实例声明以及参数配置
        ParallelWrapper wrapper = new ParallelWrapper.Builder(net)
                    .prefetchBuffer(numGPU * 8)
                    .workers(numGPU * 2)
                    .averagingFrequency(3)
                    .reportScoreAfterAveraging(true)
                    .useLegacyAveraging(true)
                    .build();
        //...
        wrapper.fit(trainDataSet);
</code></pre>
<p>我们首先对运算精度进行设置。目前市场上主流的 GPU 卡支持 FP16/FP32/FP64 的运算，即半精度/单精度/双精度的浮点运算。最常用的应当属 FP32 和 FP16。Deeplearning4j 通过 DataTypeUtil 或者 ND4J 中的静态方法可以设置浮点运算的精度，上面的案例中我们设置的是单精度。</p>
<p>随后我们声明了一个 CUDA 实例。对于该实例，我们配置了最大显存（字节为单位）容量，以及多 GPU 所需要的一些基本选项。这些在第一部分中都已经涉及并做出了解释，这里就不再赘述了。</p>
<p>最后一个部分是声明一个参数服务器实例。对于该实例，我们配置了一些常用的参数，例如：worker 的数量、预取的训练数据的数量和参数平均的频率。一般地，预先读取的训练数据数量和 worker 节点的数量是可以成比例于 GPU 卡数量的。worker 的数量一般设置在 GPU 卡的一到两倍，而预先读取的训练数据数量可以达到 8 倍或 16 倍。在最后的一小部分逻辑中，我们就可以用参数服务器实例来并行训练模型。</p>
<h3 id="153deeplearning4jgpu">15.3 Deeplearning4j 在多 GPU 环境下训练</h3>
<p>在这个部分我们以 MNIST 数据集分类应用为例，介绍如何通过 GPU 加速建模。我们的软硬件配置如下：</p>
<ol>
<li>Tesla P40 x2</li>
<li>CUDA 8.0</li>
<li>OpenJDK 1.8 64bit</li>
<li>Deeplearning4j/ND4J 0.8.0</li>
</ol>
<p>在配置完硬件和安装好 CUDA 的基础上，我们先用 <code>nvidia-smi</code> 命令来看下安装是否正确。<code>nvidia-smi</code> 命令可以返回自身机器上英伟达系列显卡的安装情况，我们看下如下截图：</p>
<p><img src="https://images.gitbook.cn/91f4cc80-fbd7-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>这是执行 <code>nvidia-smi</code> 命令后系统返回的 GPU 相关信息。从图中我们可以清晰地看到 Tesla P40 的相关信息，包括 GPU 使用率、显存的大小/使用率的情况。由于这是在没有跑任何任务时的截图，因此现在 GPU 处于空闲的状态。</p>
<p>接着，我们在 Maven 工程中添加 Deeplearning4j 对 GPU 的相关依赖。</p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.nd4j&lt;/groupId&gt;
    &lt;artifactId&gt;nd4j-cuda-8.0-platform&lt;/artifactId&gt;
    &lt;version&gt;${nd4j.version}&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
    &lt;artifactId&gt;deeplearning4j-parallel-wrapper_${scala.binary.version}&lt;/artifactId&gt;
    &lt;version&gt;${dl4j.version}&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>我们的机器安装的是 CUDA 8.0，因此需要引入 ND4J 的 CUDA 8.0 的依赖。另外，由于我们需要在多 GPU 环境下进行建模，因此我们需要引入参数服务器的相关依赖，也就是 deeplearning4j-parallel-wrapper。这部分在第二次课程中也有提及，相关内容也可以参考下那次的课程。</p>
<p>MNIST 数据集的分类问题和 Fashion-MNIST 是几乎一样的，这在之前已经有过比较详细的讨论，详情可以参考第六次的课程。这里只需要在那次分类建模的逻辑上再添加上本次课程 10.2.2 部分的相关内容即可。当执行 JAR 时，我们同样可以用 <code>watch -n 1 nvidia-smi</code> 每隔 1 秒来观察 GPU 的使用情况。以下便是正常运行起来的截图。</p>
<p><img src="https://images.gitbook.cn/02e96cc0-fbd8-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>这是我们使用单张卡时运行的情况。注意，单 GPU 运行时不需要声明参数服务器的实例。由于我没有指定具体的 GPU 卡号，所以两张卡都有显存的占用情况。如果需要只使用其中的一张卡，那么可以执行下这个命令：</p>
<pre><code>export CUDA_VISIBLE_DEVICES=0
</code></pre>
<p>这样第二张卡就不会出现占用的情况。接下来我们来看下并行的情况：</p>
<p><img src="https://images.gitbook.cn/236a5900-fbd8-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<p>这个截图是我们在两张卡上并行建模，具体的逻辑也是声明一个参数服务器实例来进行。从这张截图中我们可以看出，两张卡都有一定的 GPU 使用率，并行建模正在正常执行。最后我们给出一张执行时间的比较图供大家参考。</p>
<p><img src="https://images.gitbook.cn/336a6ac0-fbd8-11e8-a127-a5ca6ce9be36" alt="enter image description here" /></p>
<h3 id="154">15.4 小结</h3>
<p>本节课我们主要介绍了 GPU 加速深度学习建模的一些基本概念和原理，以及如何基于 Deeplearning4j 来实现多 GPU 环境下的并行建模，最后给出了 MNIST 数据集下的训练时间的比较。</p>
<p>在没有细致调优的情况下，应该说 GPU 加速以及并行加速的效果还是比较明显的。但是需要注意的是，由于 MNIST 数据集相对较小，对存储的要求不高，因此可以直接全部放在显存中。如果遇到大规模的数据训练，则可以采用异步的方式，读取若干 batch 的数据训练，同步异步线程从磁盘或者其他介质加载后续的数据。</p>
<p>另外，限于环境因素，本次课程并没有介绍在 GPU 集群上建模的方式。GPU 集群的建模需要结合 Spark 的框架，而大多数情况下多 GPU 建模已经可以较好地满足需要，有条件的同学可以自行搭建相应的开发环境进行尝试，这里不再多做介绍。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://github.com/bytedeco/javacpp-presets">JavaCPP 介绍</a></li>
<li><a href="https://deeplearning4j.org/docs/latest/deeplearning4j-config-cudnn">Deeplearning4j 有关 cuDNN 的版本设置</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>