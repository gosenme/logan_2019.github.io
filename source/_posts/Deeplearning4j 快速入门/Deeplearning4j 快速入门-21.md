---
title: Deeplearning4j 快速入门-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本节课开始，我们将介绍 Deeplearning4j 的一些扩展特性。首先在本次课程中，我们将为大家介绍 Deeplearning4j 对 Keras 和 TensorFlow 的支持情况，以及如何将这两个框架下训练好的模型导入到 Deeplearning4j 中。</p>
<p>在系列课程的第一课中，我们就谈到 Deeplearning4j 可以通过 Keras 这样的胶水框架来提供对诸如 Caffe、Theano 等深度学习框架的支持。对于 Theano 而言，它自身可以作为 Keras 的 backend 计算框架，因此 Deeplearning4j 间接支持了 Theano。对于 Caffe 而言，我们可以通过一些第三方工具来支持。因此，本次课程我们将重点介绍 Deeplearning4 就对 Keras 和 TensorFlow 这两个框架的支持情况。首先我们来看 Keras。本节课核心内容包括：</p>
<ul>
<li>Deeplearning4j + Keras</li>
<li>Deeplearning4j + TensorFlow</li>
</ul>
<h3 id="191deeplearning4jkeras">19.1 Deeplearning4j + Keras</h3>
<p>Keras（<a href="https://keras.io/">https://keras.io/</a>）是一个基于 Layer 建模的开源深度学习框架。主要使用的 Python 编程。Keras 的后台可以在 Theano、TensorFlow 和 CNTK 等多种开源框架之间切换，因此 Keras 的开发核心旨在快速的原型验证和落地。目前 Keras 已经推出了 2.x 的版本，相较于 1.x 的版本在接口层面有着一些变化，但支持的模型结构等方便逐渐变得完善和强大。Keras 早在 2017 年间就被 TensorFlow 社区接纳并支持为默认的高级建模 API，这使得越来越多的工程师投入到 Keras 的开发和使用中。</p>
<p>在系列课程的第一课中，我们在介绍 Deeplearning4j 建模案例的时候就给出过 Keras 的例子来做对比，这里我将那段逻辑再次解释一下：</p>
<pre><code>model = Sequential()
model.add(Convolution2D(nb_filters, (kernel_size[0], kernel_size[1]))) #卷积层  
model.add(Activation('relu')) #非线性变换  
model.add(MaxPooling2D(pool_size=pool_size)) #池化层  
</code></pre>
<p>如果大家有仔细看过前面介绍卷积神经网络课程的话，这段建模逻辑相信是非常好理解的。同样是基于 Layer 的建模，我们将卷积 + 池化的 CNN 常用结构通过 Keras 实现了一遍。唯一不同的地方在于激活函数的使用在 Deeplearning4j 中是和 Layer 封装在一起的。下面我们使用 Keras 1.2 的版本对 MNIST 分类问题进行建模。首先我们在线安装 Keras 库，安装完毕后验证下版本。</p>
<pre><code>$ pip install keras==1.2.2
$ import keras
$ print keras.__version_
</code></pre>
<p><img src="https://images.gitbook.cn/35ab2420-4b86-11e9-96f1-356961e976e6" alt="enter image description here" /></p>
<p>从截图可以看到，我们成功安装 1.2.2 的 Keras 库并且使用的默认运行的后台 Theano。下面我们介绍了通过建立多层感知机模型来完成 MNIST 分类问题。</p>
<pre><code>#label为 0~9 共 10 个类别，Keras 要求形式为 binary class matrices，转化一下，直接调用 Keras 提供的这个函数
nb_class = 10
label = np_utils.to_categorical(label, nb_class)

#定义多层感知机
def MLP():
    model = Sequential()   
    model.add(Dense(input_dim=784,output_dim=500, init='glorot_uniform')) 
    model.add(Activation('relu'))  

    model.add(Dense(input_dim=500,output_dim=500,init='glorot_uniform')) 
    model.add(Activation('relu'))   
    model.add(Dropout(0.5))  

    model.add(Dense(input_dim=500,output_dim=10,init='glorot_uniform'))  
    model.add(Activation('softmax')) 

    return model

#############
#开始训练模型
##############
model = MLP()
sgd = SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

model.fit(data, label, batch_size=128,nb_epoch=10)
classes = model.predict_classes(test_data)
acc = np_utils.accuracy(classes, test_label)
print('Test accuracy:', acc)
##保存模型信息和 weight
json_string = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(json_string)
model.save_weights('model_weights.h5')
</code></pre>
<p>简单解释下上面这部分的建模逻辑。</p>
<p>在 MLP 函数中我们声明了一个三层的全连接网络。由于 MNIST 是 28x28 的灰度图，因此第一层的输入维度即为 28x28=784。对于输出我们用了 500 个神经元，包括隐藏层的神经元数量也是 500。这几个超参数开发人员可以自行调优，并不一定需要完全按照我们给出的例子来。输出层同样是一个全连接层，我们用 softmax 作为输出层的激活函数。我们使用梯度下降作为优化算法和交差熵作为损失函数。在 fit 接口中我们定义了 batchSize 等超参数。在训练完毕后我们将模型保存成 h5 文件。以上逻辑定义可以完成基于多层感知机的 MNIST 分类问题。训练过程可以得到类似下面的截图：</p>
<p><img src="https://images.gitbook.cn/3f0da330-4b86-11e9-96f1-356961e976e6" alt="enter image description here" /></p>
<p>下面我们需要将训练好的 Keras 模型导入到 Deeplearning4j 中并在 MNIST 验证集上做出预测与刚才 Keras 建模后验证的效果进行比较。我们来看下相关的逻辑：</p>
<pre><code>List&lt;DataSet&gt; testData = new ArrayList&lt;DataSet&gt;();
final ImageLoader imageLoader = new ImageLoader(28, 28, 1);   
File dir = new File("mnist_small");
if( !dir.isDirectory() ){
        System.err.println("Not A Directory");
        return;
}
File[] pics = dir.listFiles();
System.out.println("Total Test Image: " + pics.length);
for( File pic : pics ){
        INDArray features = imageLoader.asRowVector(pic);
        String picName = pic.getName();
        INDArray labels = Nd4j.zeros(10);
        String label = picName.split("\\.")[0];
        int intLabel = Integer.parseInt(label);
        labels.putScalar(0, intLabel, 1.0);
        DataSet test = new DataSet(features, labels);
        testData.add(test);
}
//加载Keras模型
MultiLayerNetwork model = KerasModelImport.importKerasSequentialModelAndWeights("keras_model/model.json", "keras_model/model_weights.h5");
    Evaluation eval = new Evaluation(10);
    for( DataSet ds : testData ){
        INDArray output = model.output(ds.getFeatureMatrix(), false);
        eval.eval(ds.getLabels(), output);
    }
    System.out.println(eval.stats());
</code></pre>
<p>我们直接来看下结果：</p>
<p><img src="https://images.gitbook.cn/5be42510-4b86-11e9-8269-8dda0475a431" alt="enter image description here" /></p>
<p>从最后的验证结果来看，无论是 Keras 还是 Deeplearning4j 的在验证集上都可以达到 96% 左右的分类准确率。这也直接证明了导入到 Deeplearning4j 中的 Keras 模型并没有在网络结构或者参数上存在一些不兼容的问题。</p>
<p>对于上面 Deeplearning4j 的验证逻辑我们在这里作为解释。首先是验证数据集构建的过程。我们直接从磁盘上读取验证集中的图片，将灰度图以及标注向量化后贮存在内存中。接着我们将之前训练好的 Keras 模型通过 KerasModelImport 工具类的相关接口加载到内存中，读取相关的网络结构和参数并随后在验证集上进行模型的评估，最终得到分类的结果。</p>
<h3 id="192deeplearning4jtensorflow">19.2 Deeplearning4j + TensorFlow</h3>
<p>在上面一个部分中，我们介绍了基于 Keras 的建模和导入到 Deeplearning4j 中的基本流程。这个部分我们为大家介绍直接导入 TensorFlow 模型的过程。</p>
<p>首先，Keras 本身就是 TensorFlow 官方接纳的高级建模工具，其后台是可以跑在 TensorFlow 的计算图上的。但这里给大家介绍的是使用原生的 TensorFlow API 建模并保存成 PB 文件后，使用 ND4j 中的 SameDiff 加载使用的实例。SameDiff 作为 Deeplearning4j 官方支持的自动微分的主要工具类，从 0.9.x 版本之后开始全面支持，因此在开发的时候建议将 Deeplearning4j 的版本切换到最新的版本上。这里我们使用最新的 1.0.0-beta3 的版本。下面我们先给出 TensorFlow 建模的核心逻辑（本次课程中我们使用的 TensorFlow 是 1.6.0 的版本）：</p>
<pre><code>mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
input_units = 784  # 输入节点数
hidden_units = 500  # 隐含层节点数
output_units = 10 #输出节点的数目
batch_size = 128 #batch size
num_steps = 1001;

W1 = tf.Variable(tf.truncated_normal([input_units, hidden_units], stddev=0.1))
b1 = tf.Variable(tf.zeros([hidden_units]))
W2 = tf.Variable(tf.zeros([hidden_units, output_units]))
b2 = tf.Variable(tf.zeros([output_units]))
X = tf.placeholder(tf.float32, [None, input_units], name='input')

# 全连接模型
H1 = tf.nn.relu(tf.matmul(X, W1) + b1)
Y = tf.nn.softmax(tf.matmul(H1, W2) + b2 , name='output') #输出需要定义name

# 模型训练部分
Y_ = tf.placeholder(tf.float32, [None, output_units])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y_ * tf.log(Y), reduction_indices=[1]))
train_step = tf.train.AdagradOptimizer(0.3).minimize(cross_entropy)

# 定义一个InteractiveSession会话并初始化全部变量
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
correct_prediction = tf.equal(tf.arg_max(Y, 1), tf.arg_max(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
for i in range(num_steps):
    batch_xs, batch_ys = mnist.train.next_batch(batch_size)
    train_step.run({X: batch_xs, Y_: batch_ys})
    if i % 100 == 0:
        print(i, 'current arruracy:', accuracy.eval({X: mnist.test.images, Y_: mnist.test.labels}))
print('accuracy:', accuracy.eval({X: mnist.test.images, Y_: mnist.test.labels}))

# 保存模型成 PB 格式
constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ['input','output'])
with tf.gfile.FastGFile('mnist.pb', mode='wb') as f:
    f.write(constant_graph.SerializeToString())
</code></pre>
<p>整体的建模、训练和保存模型的逻辑都在上面的代码片段中。我们首先定义了一些超参数，包括输出层、隐藏层还有输出层的神经元的数量等等。接着我们定义网络权重和偏置变量，这也是需要训练的参数。在模型定义的部分，我们基于 matmul 算子构建全连接的网络结构，并且需要注意的是对于输出结果变量我们需要定义它的名称。在模型训练部分，我们使用交差熵作为损失函数，以及 Adagrad 作为优化器。每间隔 100 步我们就评估下模型在验证集上准确率。最后我们将模型以 PB 格式进行保存。训练过程的截图如下：</p>
<p><img src="https://images.gitbook.cn/651a3cf0-4b86-11e9-8269-8dda0475a431" alt="enter image description here" /></p>
<p>接着，我们通过 ND4J 中的 SameDiff 工具来加载之前保存的 PB 模型并且对单张图片进行预测。</p>
<pre><code>public class LoadMnistPB {
    private static NativeImageLoader imageLoder = new NativeImageLoader();
    public static void main(String[] args) throws IOException {
        INDArray f1 = imageLoder.asRowVector(new File("0.png"));
        double[] featureArray = f1.toDoubleVector();
        SameDiff sd = TFGraphMapper.getInstance().importGraph(new File("mnist.pb"));    //加载 PB 文件到内存中
        INDArray feature = Nd4j.create(featureArray);
        sd.associateArrayWithVariable(feature, "input");
        System.out.println(sd.execAndEndResult());
    }
}
</code></pre>
<p>整个逻辑其实是比较清晰的。首先我们使用图片加载的工具类 NativeImageLoader 从磁盘加载任意一张手写体数字的图片，接着我们基于 TFGraphMapper 的实例加载 PB 的模型文件。在加载完 TensorFlow 的模型文件后，我们需要通过 associateArrayWithVariable 关联特征向量和变量。输入变量名称在之前的 TensorFlow 建模代码中已经有过定义，这里需要显示指定，最后我们在 JVM 的环境中执行整个图计算并得到最终的结果。</p>
<p><img src="https://images.gitbook.cn/6c501800-4b86-11e9-8269-8dda0475a431" alt="enter image description here" /></p>
<p>上图是单张需要预测的图片，很明显结果是数字 7。</p>
<p><img src="https://images.gitbook.cn/71f9adc0-4b86-11e9-82cc-693784eb80d2" alt="enter image description here" /></p>
<p>从截图中我们可以看到。execAndEndResult 执行了整个预测过程并且得到了分类的结果，这个和图片本身的信息的符合的。需要指出的是，SameDiff 在最新的版本中已经不仅仅可以支持 TensorFlow 模型的导入，同样可以支持网络结构导入后模型的训练以及批量的评估。</p>
<h3 id="193">19.3 小结</h3>
<p>本次课程我们为大家介绍了 Deeplerning4j 对 Keras 和 TensorFlow 这两个 Python 框架的支持情况。我们分别将训练好的 Keras 和 TensorFlow 模型导入到 Deeplearning4j 中进行预测并取得了几乎和原始模型一样的准确率。目前对于 Keras 1.x 和 2.x 版本，Deeplearning4j 都给予了支持。对于 TensorFlow 而言，Deeplearning4j 主要通过 Nd4J 中 SameDiff 的自动微分机制来支持。最新版本的 Deeplearning4j 并仅仅支持导入训练完成的模型，通常可以支持导入有 TensorFlow 框架定义的模型结构并在 Java 环境下进行训练。需要指出的是，Deeplearning4j 对于 TensorFlow 的支持并不是完美的，还有很多的 Op 暂时并不支持，因此在使用的时候请大家自行查阅相关文档来确定具体版本的支持情况。</p>
<p>当前深度学习框架越来越多，在一个团队中每一位工程师都可能有自己较为熟悉和擅长的框架，因此对其他框架的兼容将非常有利于团队工作的开展。值得一提的是，ONNX（Open Neural Network Exchange）标准的制定将进一步满足不同深度学习框架间的通信，目前诸如 Caffe、TensorFlow 社区都在不同程度上支持了 ONNX 的交换标准，Deeplearning4j 社区同样也在不断跟进这一标准，因此在未来的两到三年时间，通过 ONNX 格式进行模型复用将会成为另一种主流的方式。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>