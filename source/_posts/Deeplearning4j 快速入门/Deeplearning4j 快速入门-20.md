---
title: Deeplearning4j 快速入门-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本次的课程主要介绍模型的部署上线。Deeplearning4j 支持将模型持久化后结合诸如 Spark Streaming、Flink 等流式计算框架提供实时或者准实时的预测服务，也可以和 Java Web 技术整合通过 Web 容器对外提供服务。这几种方式在实际的生产环境中都有比较广泛的使用，一般都根据实际的技术和业务背景来做选择。课程中我们将分别就这两种上线方式给出具体的案例。另外，对于离线的批量预测这部分，Deeplearning4j 是通过结合 Spark 来实现的，这在前面 Spark 的课程中已经有所提及，这里就不再多赘述了。下面我们首先来看第一种对外提供服务的方式。本节课核心内容包括：</p>
<ul>
<li>Deeplearning4j + Spring + JSP</li>
<li>Deeplearning4j + Apache Flink</li>
</ul>
<h3 id="181deeplearning4jspringjsp">18.1 Deeplearning4j + Spring + JSP</h3>
<p>第一种模型上线的方式是结合 Spring 通过对外提供 Web 服务来实现的，容器我们用 Tomcat。我们选择的案例是之前课程提到过的 Fashion-MNIST 数据集的分类问题，我们的目标是，通过已经训练好的卷积神经网络对用户上传的服装类图片进行识别。前端交互我们用 JSP 来实现。</p>
<p>我们假设 CNN 网络已经构建完毕，因此我们将重点集中在前后台的交互逻辑上。下面首先是整个 Java Web 工程结构图。</p>
<p><img src="https://images.gitbook.cn/6e7d7ff0-43de-11e9-a8b3-9f9f13f626ac" alt="enter image description here" /></p>
<p>前台的主要逻辑集中在 picture.jsp 中，后台的核心处理集中的 PictureUploadService 这个类中。页面中的主要功能是支持用户图片的上传、分类预测结果的展示。这里我们用表单来实现。</p>
<pre><code>&lt;!--图片上传--&gt;
&lt;form action="/DL-Web/upload" method="post" enctype="multipart/form-data"&gt; 
Please Upload Picture:
&lt;input type="file" name="uploadFile"/&gt;
&lt;input type="submit" value="Upload"/&gt; 
&lt;/form&gt;
&lt;!--分类结果--&gt; 
&lt;p&gt;Predict Result：${label}&lt;/p&gt;
&lt;!--临时文件引用--&gt; 
&lt;img src="${pageContext.request.contextPath}/imgs/temp${timestamp}.jpg"/&gt;
</code></pre>
<p>JSP 中的逻辑是比较清晰的，我们也相应做了注释。分类结果的变量值会从后台传到前端。下面我们重点看下后台逻辑：</p>
<pre><code>@Service
public class PictureUploadService implements InitializingBean{
    private static final Logger LOG = LoggerFactory.getLogger(PictureUploadService.class);
    private MultiLayerNetwork model;
    private NativeImageLoader imageloader;
    private Map&lt;Integer,String&gt; map;

    @Override
    public void afterPropertiesSet() throws Exception {
        //加载训练好的模型
        model = ModelSerializer.restoreMultiLayerNetwork("fashionmnist/model.mod");
        //声明图片加载器
        imageloader = new NativeImageLoader(28, 28, 1);
        //声明分类标签的映射关系
        map = new HashMap&lt;Integer,String&gt;(){{put(0,"T-shirt");put(1,"Trouser");
                                            put(2,"Pullover");put(3,"Dress");
                                            put(4,"Coat");put(5,"Sandal");
                                            put(6,"Shirt");put(7,"Sneaker");
                                            put(8,"Bag");put(9,"Ankle boot");}};
        LOG.info("Finish Loading Model");
    }

    /***
     *  图片分类的主逻辑 
     */
    public String fashionReco(File pic) throws IOException{
        INDArray feature = imageloader.asRowVector(pic);
        feature = feature.div(255.0).rsub(1.0); //归一化
        int label = model.predict(feature)[0];
        return map.get(label);
    }
}
</code></pre>
<p>后台的核心处理就在于这个 Service 中。我们通过助记符 @Service 声明一个内部服务，并在容器启动的时候，从磁盘加载已经训练好的卷积神经网络模型。另外，我们通过声明 NativeImageLoader 对象来构建图片加载器。其中构造函数涉及的三个参数主要是围绕图片本身的属性而言（Fashion-MNIST 是 28x28 的灰度图，因此 channel 数是 1，宽高都是 28）。最后我们为了方便预测结果的展示，将数字标签和文字标签建立映射关系。在用户上传一张服饰类图片之后，我们会调用 fashionReco 方法来对图片做分类预测。首先我们用图片加载器来读取图片，对像素值做归一后，调用模型的预测接口将第一个分类结果（默认也是概率最大的结果）返回给前端。</p>
<p>前台页面的效果如下：</p>
<p><img src="https://images.gitbook.cn/d89d8280-43df-11e9-ae1b-cbdd9b69dbba" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/e3cd6e90-43df-11e9-bd5e-8f4912d4bd5f" alt="enter image description here" /></p>
<p>这些图片大多是苏宁易购网站上的图片，我们随机挑选了一些。可以看到，虽然我们用的训练数据集 Fashion-MNIST 只是尺寸很小的灰度图，但对于较大的彩色图片依然可以做出还算准确的预测。值得一提的是，我们用于测试的服饰类图片经过图片加载器读取后会自动转成 28x28x1 的灰度图，无需手动转换。这里我选择的都是相对干净的白底图，图片中也都只有一个主体，因此不需要目标检测技术的介入，可以直接预测分类。当然，在实际生产环境中，我们会将实际商品图片作为训练集来建模，而不会仅仅依赖开源数据集。</p>
<p>以上是通过 Web 容器对外提供服务的简单案例。由于 Deeplearning4j 是基于 JVM 的开源框架，因此和 Java EE 项目的整合非常方便，所有的预测逻辑相当于提供一种内部的服务，完全在内存中展开，无需单独部署，整体逻辑可以和其他业务代码保持一定的耦合但同时又保持相对独立。需要注意的是，当使用 Wildfly 作为容器时，可能会出现 jar 包冲突的问题，需要适当排包。</p>
<h3 id="182deeplearning4japacheflink">18.2 Deeplearning4j + Apache Flink</h3>
<p>在这个部分我们为大家介绍基于分布式流式计算框架 Apache Flink 的模型部署过程。首先我们简单介绍下 Flink 的相关信息。</p>
<p><img src="https://i.imgur.com/Ezv6lsj.png" alt="" /></p>
<p>Apache Flink（<a href="https://flink.apache.org/">https://flink.apache.org/</a>）是新一代兼容批处理和流式处理的分布式计算框架，和 Spark 一样也是基于内存的。事实上目前在开源项目中，Spark 是解决批处理的首选，Storm 是流式计算引擎中的佼佼者。在实际开发的过程中，对于同样的业务场景我们很有可能需要兼顾全量和增量的数据处理，通常的做法是借助批处理和流处理的框架来分别完成上述的需求。但这样一来需要维护两套的处理逻辑，如果实时性要求不是很高，可以考虑使用 Spark Streaming 这种 mini-batch 来近似模拟流处理。</p>
<p>实际情况是，工程师往往希望有一个更好的兼容两种计算的框架，那么 Flink 就是一个比较好的选择。我们在这里和之前介绍 Spark 一样，首先给出一个 Flink 的流式计算案例供大家参考。</p>
<p>我们首先添加 Flink 项目的相关依赖（注意：这里笔者用 Java 来开发 Flink 应用，如果使用 Scala 的话，依赖会有所不同）。</p>
<pre><code>&lt;properties&gt;
    &lt;flink.version&gt;1.5.4&lt;/flink.version&gt;
&lt;/properties&gt;

&lt;dependency&gt;
    &lt;groupId&gt;org.apache.flink&lt;/groupId&gt;
    &lt;artifactId&gt;flink-java&lt;/artifactId&gt;
    &lt;version&gt;${flink.version}&lt;/version&gt;
    &lt;scope&gt;provided&lt;/scope&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.apache.flink&lt;/groupId&gt;
    &lt;artifactId&gt;flink-streaming-java_2.11&lt;/artifactId&gt;
    &lt;version&gt;${flink.version}&lt;/version&gt;
    &lt;scope&gt;provided&lt;/scope&gt;
&lt;/dependency&gt;
</code></pre>
<p>我们这里使用 1.5.4 版本的相关依赖。下面是一个入门的例子：</p>
<pre><code>public class FlinkDemo {

public static void main(String[] args) throws Exception {
    //流式计算上下文
    final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    DataStream&lt;Integer&gt; streamInt = env.addSource(new UDFSource())  //Source
                                        .map(new AddFunction());

    //Sink
    streamInt.print();
    //执行流式任务
    env.execute("Demo Job");

}

//业务处理，对于 Source 生成的整数累加一个数值
private static final class AddFunction extends RichMapFunction&lt;Integer, Integer&gt;{

    private static final long serialVersionUID = -5798871261779071742L;
    private int addNumber;

    @Override
    public void open(Configuration parameters) throws Exception {
        addNumber = 100;
    }

    @Override
    public Integer map(Integer value) throws Exception {
        return value + addNumber;
    }

}

//自定义 Source，不断发送 0~10 的整数
private static final class UDFSource implements SourceFunction&lt;Integer&gt;{

    private static final long serialVersionUID = 5953310342004876373L;
    private int count = 0;
    private volatile boolean isRunning = true;

    @Override
    public void run(SourceContext&lt;Integer&gt; ctx) throws Exception {
        while (isRunning) { 
             synchronized (ctx.getCheckpointLock()) {
                   ctx.collect(count);
                   if( ++count &gt;= 10 )count = 0;
             }
        }
    }

    @Override
    public void cancel() {
        isRunning = false;
    }

}

}
</code></pre>
<p>Flink 的编程模型需要定义 Source 和 Sink，我们一般可以认为是上游数据源（如 Kafka 等）和推送的下游数据媒介（如 Hbase 等）。在这里我们为了方便测试，自定义了一个 Source，作用是不断生成 0~10 之间的整数。AddFunction 是继承了 RichMapFunction 的一个子类，其中的 open 方法定义了任务执行之前所需要的一些预处理操作，而 map 方法则是具体的处理逻辑。由于只是一个演示的例子，在 map 方法中我们只是把 Source 生成的数据加上一个固定数值并打印到控制台。需要注意的是，Flink 的 RichFunction 接口中（RichMapFunction 实现了该接口）定义了 open 和 close 两个方法，主要用来在对象初始化和实例销毁时候做一些预加载和数据释放的动作。当然，如果开发人员认为不需要这样的事先和事后处理，那么直接使用 MapFunction 也是可以的。</p>
<p>以上逻辑在我本地 4 核 CPU 的台式机上执行结果如下：</p>
<p><img src="https://images.gitbook.cn/1688ce60-43ef-11e9-a8b3-9f9f13f626ac" alt="enter image description here" /></p>
<p>结果和我们的预期一致，0~10 之间的整数加上固定值 100 之后被打印到控制台。由于是 4 核的机器，因此实际在本地执行的时候会有 4 个线程来模型集群进行并行计算，这也是输出的前缀有 2、3、4 的标识。</p>
<p>我们同样可以将以上逻辑编译成 JAR 包后上传到集群上运行。</p>
<pre><code>./bin/flink run -m yarn-cluster -c cn.live.wangongxi.FlinkDemo Demo.jar
</code></pre>
<p>通过以上命令我们可以将 Flink 任务提交到 Yarn 集群上运行。这里我们并没有执行 TaskManager 的数量和内存，如果需要自定义的话可以查询 <a href="https://ci.apache.org/projects/flink/flink-docs-release-1.7/ops/deployment/yarn_setup.html#run-a-flink-job-on-yarn">Flink 官网</a> 相关资料进行设置。当任务运行起来后，我们可以通过 Flink Dashboard 查看任务的进展情况。</p>
<p><img src="https://images.gitbook.cn/860d15c0-43ef-11e9-bd5e-8f4912d4bd5f" alt="enter image description here" /></p>
<p>下面我们开始进行 Flink 和 Deeplearning4j 的整合。由于我们只是考虑将训练好的神经网络部署在流式框架上，而不考虑 On-line Training 的场景，因此实际上只需要将模型文件当作一般的数据文件随 JAR 包上传集群后自动分发到每个节点，保证每个节点都持有一份模型的副本就可以做出实时的预测。这就是我们将 Deeplearning4j 与 Flink 联合部署在线预测应用的基本思想。我们在 RichMapFunction 实例的 open 方法中加载 JAR 包中的神经网络模型并生成实例，在 map 方法中完成在线预测逻辑：</p>
<pre><code>@Override
public String map(String jsonString) throws Exception {
        double[] featuresDouble = new double[numFeatures];
        //此处省略json格式数据的转换
        //... ...
        INDArray features = Nd4j.create(featuresDouble);
        int label = model.predict(features)[0];
        return String.valueOf(label);
    }

public void open(Configuration parameters) throws Exception {
        synchronized(this){
            InputStream is = FlinkRealPredict.class.getClassLoader().getResourceAsStream("model.bin");
            model = ModelSerializer.restoreMultiLayerNetwork(is);
            LOGGER.info("Finish Loading Model");
    }
}
</code></pre>
<p>我们事先将训练好的模型打在 JAR 包里，当应用启动的时候，在 open 方法中加载模型到内存。模型的实时预测逻辑在 map 方法中进行，和之前提到的所有的 Deeplearning4j 的模型一样，我们将上游数据源推送的数据（案例中我们推送的是 JSON 格式数据）做一些预处理并生成 NDArray 对象后就可以调用 predict 或 output 方法进行模型预测。</p>
<p>需要注意的是，和之前在 Spark 集群上跑 Deeplearning4j 应用一样，我们需要构建一个 fat-jar 将 Deeplearning4j 的所有依赖打进去，使用的 Maven 插件和 Spark 课程提到的是一致的。</p>
<h3 id="183">18.3 总结</h3>
<p>本次课程我们介绍了 Deeplearning4j 模型上线部署的两种方式：Web 服务和依托流式计算框架。Web 服务我们可以用 Spring 框架来注册一个内部的服务，当容器启动时一次性加载模型到内存并实时对外提供服务。如果选择流式计算框架部署模型，同样需要加载模型到内存后随着每一次的流式计算处理提供模型的预测服务。这两种上线模型并没有绝对的好坏之分，主要根据工程师的技术储备和实际技术环境来进行选择，Deeplearning4j 都可以支持。</p>
<p>需要指出的是，我们在本次课程中的部署方式并不是仅有的两种方式。理论上所有 Java 生态圈的项目都可以和 Deeplearning4j 整合提供对外服务，这也是其区别于 Python 框架的一个主要特点。在实际的部署过程中很有可能会遇到 JAR 包冲突等问题，但就笔者的经验而言大部分的冲突问题经过精心的排包都可以解决。至于是否需要单独部署算法应用的集群来对外提供服务，这一点上并没有什么统一的答案。对于 Deeplearning4j 来讲，单独部署或者和其他业务逻辑耦合在一起都是可以的。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://ci.apache.org/projects/flink/flink-docs-release-1.7/ops/deployment/yarn_setup.html#run-a-flink-job-on-yarn">Flink 官网</a> </li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>