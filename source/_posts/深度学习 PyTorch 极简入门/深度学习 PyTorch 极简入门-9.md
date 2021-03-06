---
title: 深度学习 PyTorch 极简入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇，我们主要介绍了深层神经网络模型的结构和常用的标记方法，详细推导了深层神经网络模型的正向传播和反向传播过程，并在最后介绍了多分类 Softmax 模型。</p>
<p>本文我将带领大家通过搭建一个较深层的神经网络来解决一个猫、狗的分类问题。这是一个典型的二分类问题。输入是一张图片，我们会把 3 通道的 RGB 图片拉伸为一维数据作为神经网络的输入层。神经网络的输出层包含一个神经元，经过 Softmax 输出概率值 $P$，若 $P&gt;0.5$，则判断为猫（正类），若 $P\leq 0.5$，则判断为非猫（负类）。</p>
<p>对于整个神经网络模型，我们可以选择使用不同层数，以此来比较模型分类的性能，从而得到较深的神经网络及分类效果更好的结论。但这也不是绝对的，并不是说网络层数越多越好。接下来，我就带大家一步步构建神经网络模型。</p>
<h3 id="">导入数据集</h3>
<p>首先，我们导入构建模型所需的数据集。</p>
<p>该数据集分为训练（Train）集和测试（Test）集，训练集共有 250 张猫的图片和 250 张狗的图片，测试集共有 100 张猫的图片和 100 张狗的图片。我们需要训练神经网络模型来识别图片是否为猫类，最终模型在测试集上进行正确率的验证。</p>
<blockquote>
  <p>说明：本文所有代码均在 Jupyter Notebook 中编写实现。</p>
</blockquote>
<p>首先导入数据集：</p>
<pre><code>import skimage.io as io
import numpy as np

# 训练样本
file='./data/train/*.jpg'
coll = io.ImageCollection(file)

# 500 个训练样本，250 个猫图片，250 个非猫图片
X_train = np.asarray(coll)     
# 输出标签 
y_train = np.hstack((np.ones(250),np.zeros(250)))            

# 测试样本
file='./data/test/*.jpg'
coll = io.ImageCollection(file)
# 200 个训练样本，100 个猫图片，100 个非猫图片
X_test = np.asarray(coll)  
# 输出标签 
y_test = np.hstack((np.ones(100),np.zeros(100)))            

m_train = X_train.shape[0]
m_test = X_test.shape[0]
w, h, d = X_train.shape[1], X_train.shape[2], X_train.shape[3]

print('训练样本数量：%d' % m_train)
print('测试样本数量：%d' % m_test)
print('每张图片的维度：(%d, %d, %d)' % (w, h, d))
</code></pre>
<p>上述代码主要来导入数据训练集和测试集。训练样本放在 GitHub 路径 <code>./data/train/</code> 目录下，测试样本放在 GitHub 路径 <code>./data/test/</code> 目录下。训练样本共有 500 个，其中猫 250 个，非猫 250 个，正负样本各占一半。测试样本共有 200 个，其中猫 100 个，非猫 100 个，正负样本各占一半。每张图片的维度是 <code>64x64x3</code>，其中 3 表示 RGB 三通道。</p>
<p>运行以上程序，输出结果为：</p>
<blockquote>
  <p>训练样本数量：500</p>
  <p>测试样本数量：200</p>
  <p>每张图片的维度：(64, 64, 3)</p>
</blockquote>
<p>接下来，我们从训练样本中随机选择 10 张图片显示，并识别其是否为猫类图片。结果 y = 1 表示是猫类图片；y = 0 表示非猫类图片。测试代码如下：</p>
<pre><code>import matplotlib.pyplot as plt

idx = [np.random.choice(m_train) for _ in range(10)]  # 随机选择 10 张图片
label = y_train[idx]
for i in range(2):
    for j in range(5):
        plt.subplot(2, 5, 5*i+j+1)
        plt.imshow(X_train[idx[5*i+j]])
        plt.title("y="+str(label[5*i+j]))
        plt.axis('off')
plt.show()
</code></pre>
<p>以上代码从训练数据中随机选择了 10 张图片并显示出来，显示图片的同时也显示图片对应的标签 Label。</p>
<p>10 张图片的输出结果，如下图所示：</p>
<p><img src="https://images.gitbook.cn/09e58e60-9ad9-11e8-831e-0180aea56660" alt="enter image description here" /></p>
<h3 id="-1">预处理</h3>
<p>导入数据之后，我们需要对图片进行一些预处理操作。首先，每张图片由 R、G、B 三通道组成，要把每个图片矩阵转化为一维向量，方便神经网络输入层输入数据。然后，对每张图片的像素值归一化到 [0,1] 之间，这样做的原因是方便神经网络的训练，是图片处理常用的预处理操作。代码如下：</p>
<pre><code># 图片矩阵转化为一维向量
X_train = X_train.reshape(m_train, -1).T
X_test = X_test.reshape(m_test, -1).T

print('训练样本维度：' + str(X_train.shape))
print('测试样本维度：' + str(X_test.shape))

# 图片像素归一化到 [0,1] 之间
X_train = X_train / 255
X_test = X_test / 255
</code></pre>
<p>上述代码中，reshape 作用就是将图片尺寸调整为一维数组。</p>
<p>输出结果为：</p>
<blockquote>
  <p>训练样本维度：(12288, 500)</p>
  <p>测试样本维度：(12288, 200)</p>
</blockquote>
<h3 id="wb">初始化参数 W 和 b</h3>
<p>接下来需要对神经网络参数 W 和 b 进行初始化操作。</p>
<p>上一篇，我们介绍过深层神经网络一些常用的标记。在命名习惯上，我们把输入层称之为第 0 层，输出层称之为第 L 层。$l$ 表示第几层，$l=0,1,\cdots,L$。$n^{[l]}$ 表示第 $l$ 层神经元个数。第 $l$ 层的线性输出用 $z^{[l]}$ 表示，第 $l$ 层神经元的输出（非线性输出）用 $a^{[l]}$ 表示。一般把输入 $x$ 记为 $a^{[0]}$，把输出 $\hat y$ 记为 $a^{[L]}$。神经网络第 $l$ 层的参数分别用 $W^{[l]}$ 和 $b^{[l]}$ 来表示。第 $l$ 层的激活函数用 $g^{[l]}(\cdot)$ 表示。</p>
<p>首先，我们定义 <code>layer_dims</code>，用来存储神经网络各层数的列表，使用 parameters 字典存储各层参数 W 和 b，定义过程如下：</p>
<pre><code>def initialize_parameters(layer_dims):

    parameters = {}          # 存储参数 W 和 b 的字典
    L = len(layer_dims)      # 神经网络的层数，包含输入层

    for l in range(1, L):
        parameters['W' + str(l)] = np.random.randn(layer_dims[l],layer_dims[l-1]) * 0.1
        parameters['b' + str(l)] = np.zeros((layer_dims[l],1))

    return parameters
</code></pre>
<p>以上代码将 W 初始化为均值 0，方差为 0.1 的服从高斯分布随机值，将 b 全部初始化为 0。需要注意 W 和 b 的维度不要写错。</p>
<h3 id="-2">正向传播单层神经元</h3>
<p>神经网络正向传播过程中，单个神经元的运算包括两个步骤：线性运算和激活函数，而激活函数又根据所在的网络层，选择 Sigmoid 或者 ReLU。首先来定义单个神经元的运算函数：</p>
<pre><code># sigmoid 函数
def sigmoid(Z):

    A = 1/(1+np.exp(-Z))

    return A

# relu 函数
def relu(Z):

    A = np.maximum(0,Z)

    return A

# 单个神经元运算单元
def linear_activation_forward(A_prev, W, b, activation):

    Z = np.dot(W, A_prev) + b        # 线性输出
    if activation == "sigmoid":
        A = sigmoid(Z)
    elif activation == "relu":
        A = relu(Z)

    cache = (A_prev, W, b, Z)

    return A, cache
</code></pre>
<p>上面代码定义了激活函数 Sigmoid 和 ReLU。 </p>
<h3 id="l">正向传播 L 层神经元</h3>
<p>对于 L 层神经网络，它是由单层神经网络组成的，第 $l$ 层的正向传输过程表示如下：</p>
<p>$$Z^{[l]}=W^{[l]}A^{[l-1]}+b^{[l]}$$</p>
<p>$$A^{[l]}=g^{[l]}(Z^{[l]})$$</p>
<p>前 L-1 层使用的激活函数是 ReLU，最后一层使用的激活函数是 Sigmoid。可以使用 for 循环来构建整个正向传播过程：</p>
<pre><code>def model_forward(X, parameters):

    caches = []
    A = X
    L = len(parameters) // 2                  # 神经网络层数 L

    # L-1 层使用 ReLU
    for l in range(1, L):
        A_prev = A 
        A, cache = linear_activation_forward(A_prev, parameters['W' + str(l)], parameters['b' + str(l)], "relu")
        caches.append(cache)

    # L 层使用 Sigmoid
    AL, cache = linear_activation_forward(A, parameters['W' + str(L)], parameters['b' + str(L)], "sigmoid")
    caches.append(cache)

    return AL, caches
</code></pre>
<h3 id="-3">损失函数</h3>
<p>对于 m 个样本的损失函数为：</p>
<p>$$J=-\frac{1}{m}\sum_{i=1}^my^{(i)}log\hat y^{(i)}+(1-y^{(i)})log(1-\hat y^{(i)})$$</p>
<p>计算损失函数的代码如下：</p>
<pre><code>def compute_cost(AL, Y):

    m = AL.shape[1]

    cost = -1/m*np.sum(Y*np.log(AL)+(1-Y)*np.log(1-AL))

    cost = np.squeeze(cost)      # 压缩维度，保证损失函数值维度正确，例如 [[10]] -&gt; 10

    return cost
</code></pre>
<h3 id="-4">反向传播单层神经元</h3>
<p>从神经网络单层神经元来看，需要求解 $dZ^{[l]}$，$dW^{[l]}$，$db^{[l]}$，$dA^{[l-1]}$。公式如下：</p>
<p>$$dZ^{[l]}=dA^{[l]}*g^{[l]'}(Z^{[l]})$$</p>
<p>$$dW^{[l]}=\frac1mdZ^{[l]}\cdot A^{[l-1]T}$$</p>
<p>$$db^{[l]}=\frac1mnp.sum(dZ^{l]},axis=1)$$</p>
<p>$$dA^{[l-1]}=W^{[l]T}\cdot dZ^{[l]}$$</p>
<p>首先需要定义 ReLU 的求导函数，代码如下：</p>
<pre><code>def relu_backward(dA, Z):

    dZ = np.array(dA, copy=True)  
    dZ[Z &lt;= 0] = 0

    return dZ
</code></pre>
<p>然后需要定义 Sigmoid 的求导函数：</p>
<pre><code>def sigmoid_backward(dA, Z):

    s = 1/(1+np.exp(-Z))
    dZ = dA * s * (1-s)

    return dZ
</code></pre>
<p>接下来是定义单层神经元反向传播函数：</p>
<pre><code>def linear_activation_backward(dA, cache, activation):

    A_prev, W, b, Z = cache

    if activation == "relu":
        dZ = relu_backward(dA, Z)
    elif activation == 'sigmoid':
        dZ = sigmoid_backward(dA, Z)

    m = dA.shape[1]
    dW = 1/m*np.dot(dZ,A_prev.T)
    db = 1/m*np.sum(dZ,axis=1,keepdims=True)
    dA_prev = np.dot(W.T,dZ)

    return dA_prev, dW, db
</code></pre>
<h3 id="l-1">反向传播 L 层神经元</h3>
<p>对于 L 层神经网络，它是由单层神经网络组成的，对于第 $l$ 层，已知 $dA^{[l]}$ 之后，就可以推导：</p>
<p>$$dZ^{[l]}=dA^{[l]}*g^{[l]'}(Z^{[l]})$$</p>
<p>$$dW^{[l]}=\frac1mdZ^{[l]}\cdot A^{[l-1]T}$$</p>
<p>$$db^{[l]}=\frac1mnp.sum(dZ^{l]},axis=1)$$</p>
<p>$$dA^{[l-1]}=W^{[l]T}\cdot dZ^{[l]}$$</p>
<p>前 L-1 层使用的激活函数是 ReLU，最后一层使用的激活函数是 Sigmoid。可以使用 for 循环来构建整个反向传播过程：</p>
<pre><code>def model_backward(AL, Y, caches):

    grads = {}
    L = len(caches)         # 神经网络层数，包括输入层
    m = AL.shape[1]         # 样本个数
    Y = Y.reshape(AL.shape) # 保证 Y 与 AL 维度一致

    # AL 值
    dAL = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

    # 第 L 层，激活函数是 Sigmoid
    current_cache = caches[L-1]
    grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache, activation = "sigmoid")

    # 前 L-1 层，激活函数是 ReLU
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 1)], current_cache, activation = "relu")
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads
</code></pre>
<h3 id="wb-1">更新网络参数 W 和 b</h3>
<p>计算完各层 $dW$ 和 $db$ 之后，利用梯度下降算法，更新 W 和 b：</p>
<p>$$W^{[1]}=W^{[1]}-\eta\cdot dW^{[1]}$$</p>
<p>$$b^{[1]}=b^{[1]}-\eta\cdot db^{[1]}$$</p>
<p>$$W^{[2]}=W^{[2]}-\eta\cdot dW^{[2]}$$</p>
<p>$$b^{[2]}=b^{[2]}-\eta\cdot db^{[2]}$$</p>
<p>其中，$\eta$ 是学习因子。</p>
<p>相应更新 W 和 b 的代码如下：</p>
<pre><code>def update_parameters(parameters, grads, learning_rate):

    L = len(parameters) // 2           # 神经网络层数，包括输入层

    for l in range(L):
        parameters["W" + str(l+1)] -=  learning_rate*grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] -=  learning_rate*grads["db" + str(l+1)]

    return parameters
</code></pre>
<h3 id="-5">整个神经网络模型</h3>
<p>讨论完正向传播、损失函数计算、反向传播、更新 W 和 b 之后，我们将所有的模块组合起来构成整个神经网络。整个模型定义如下：</p>
<pre><code>def nn_model(X, Y, layers_dims, learning_rate = 0.01, num_iterations = 3000, print_cost=False):

    np.random.seed(1)
    costs = []                         

    # 参数初始化
    parameters = initialize_parameters(layers_dims)

    # 迭代训练
    for i in range(0, num_iterations):

        # 正向传播
        AL, caches = model_forward(X, parameters)

        # 计算损失函数
        cost = compute_cost(AL, Y)

        # 反向传播
        grads = model_backward(AL, Y, caches)

        # 更新参数
        parameters = update_parameters(parameters, grads, learning_rate)

        # 每迭代 100 次，打印 cost
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # 绘制 cost 趋势图
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per hundred)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()

    return parameters
</code></pre>
<h3 id="-6">模型预测</h3>
<p>模型搭建完毕之后，就可以使用训练好的模型对新样本进行预测。</p>
<pre><code>def predict(X, y, parameters):

    m = X.shape[1]
    p = np.zeros((1,m))

    # 正向传播
    AL, caches = model_forward(X, parameters)
    predictions = AL &gt; 0.5

    accuracy = np.mean(predictions == y)

    print("Accuracy: %f" % accuracy)

    return predictions
</code></pre>
<p>神经网络输出层进行预测，若输出 $P&gt;0.5$，则判断为正类，若输出 $P\leq 0.5$，则判断为负类。predict 输出预测准确率。</p>
<h3 id="-7">训练模型</h3>
<p>下面开始训练神经网络模型，为了比较网络层数不同对准确率的影响，我们先设计一个简单的两层神经网络。</p>
<pre><code>layers_dims = [12288, 10, 1] #  2-layer model
parameters = nn_model(X_train, y_train, layers_dims, learning_rate = 0.01, num_iterations = 1500, print_cost = True)
</code></pre>
<p>print 函数输出如下内容：</p>
<blockquote>
  <p>Cost after iteration 0: 0.934291</p>
  <p>Cost after iteration 100: 0.654145</p>
  <p>Cost after iteration 200: 0.598071</p>
  <p>Cost after iteration 300: 0.491806</p>
  <p>Cost after iteration 400: 0.952094</p>
  <p>Cost after iteration 500: 0.426875</p>
  <p>Cost after iteration 600: 0.838886</p>
  <p>Cost after iteration 700: 0.832011</p>
  <p>Cost after iteration 800: 0.218174</p>
  <p>Cost after iteration 900: 0.190239</p>
  <p>Cost after iteration 1000: 0.424622</p>
  <p>Cost after iteration 1100: 0.181183</p>
  <p>Cost after iteration 1200: 0.243990</p>
  <p>Cost after iteration 1300: 0.125354</p>
  <p>Cost after iteration 1400: 0.179002</p>
</blockquote>
<p>该模型，输入层神经元只包含了单隐藏层，隐藏层个数为 10，学习因子为 0.01，迭代训练 1500 次，每隔 100 次打印损失函数值。损失函数随迭代次数的变化趋势如下图所示，整体降低，但振荡较大。</p>
<p><img src="https://images.gitbook.cn/6e5afe90-9c3f-11e8-8519-414280066c63" alt="enter image description here" /></p>
<p>计算训练样本的准确率：</p>
<pre><code>pred_train = predict(X_train, y_train, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.984000</p>
</blockquote>
<p>测试样本的准确率：</p>
<pre><code>pred_test = predict(X_test, y_test, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.570000</p>
</blockquote>
<p>再设计一个较复杂的五层神经网络：</p>
<pre><code>layers_dims = [12288, 100, 50, 10, 4, 1] #  5-layer model
parameters = nn_model(X_train, y_train, layers_dims, learning_rate = 0.04, num_iterations = 1500, print_cost = True)
</code></pre>
<p>print 函数输出如下内容：</p>
<blockquote>
  <p>Cost after iteration 0: 0.693274</p>
  <p>Cost after iteration 100: 0.693000</p>
  <p>Cost after iteration 200: 0.692647</p>
  <p>Cost after iteration 300: 0.692013</p>
  <p>Cost after iteration 400: 0.690574</p>
  <p>Cost after iteration 500: 0.686974</p>
  <p>Cost after iteration 600: 0.675996</p>
  <p>Cost after iteration 700: 0.646076</p>
  <p>Cost after iteration 800: 0.626832</p>
  <p>Cost after iteration 900: 0.561664</p>
  <p>Cost after iteration 1000: 0.521846</p>
  <p>Cost after iteration 1100: 0.460633</p>
  <p>Cost after iteration 1200: 0.337490</p>
  <p>Cost after iteration 1300: 0.232980</p>
  <p>Cost after iteration 1400: 0.051204</p>
</blockquote>
<p>该模型，输入层神经元只包含了 4 层隐藏层，隐藏层个数分别为 100、50、10、4，学习因子为 0.04，迭代训练 1500 次，每隔 100 次打印损失函数值。损失函数随迭代次数的变化趋势如下图所示，整体降低，但振荡较小。</p>
<p><img src="https://images.gitbook.cn/bc46d9c0-9c40-11e8-8519-414280066c63" alt="enter image description here" /></p>
<p>训练样本的准确率：</p>
<pre><code>pred_train = predict(X_train, y_train, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.998000</p>
</blockquote>
<p>测试样本的准确率：</p>
<pre><code>pred_test = predict(X_test, y_test, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.625000</p>
</blockquote>
<p>通过对比能够看到，随着神经网络层数的加深，训练样本准确率和测试样本准确率与随之增加了，其实主要看的是测试样本准确率。事实上，测试样本的准确率并没有提高多少，原因是对于复杂图片的分类，单纯靠增加神经网络层数并不能有效提高模型的性能，还需要其它更高效的优化算法，包括梯度的优化算法、学习率的优化策略、权重初始化方法等等。关于神经网络各种常用的优化方法我们后面几课中将做详细介绍。</p>
<p>包含本文完整代码的 <code>.ipynb</code> 文件，我已经放在了 GitHub 上，大家可自行下载：</p>
<blockquote>
  <p><a href="https://github.com/RedstoneWill/gitchat_dl/tree/master/09%20chapter">第09课：项目实战——让你的神经网络模型越来越深</a></p>
</blockquote></div></article>