---
title: 深度学习 PyTorch 极简入门-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇给出了构建神经网络模型时的一些实用建议，涉及到评估模型、训练/验证/测试集、贝叶斯最优误差和人类表现水平、错误分析等内容。掌握这些知识对优化神经网络模型非常有用。</p>
<p>本文将继续使用第9课中的项目，带领大家使用一些梯度优化技巧和正则化技术搭建一个更好的神经网络来解决猫、狗图片分类问题。这是一个典型的二分类问题。输入是一张图片，我们会把三通道的 RGB 图片拉伸为一维数据作为神经网络的输入层。神经网络的输出层包含一个神经元，经过 Sigmoid 函数输出概率值 $P$，若 $P&gt;0.5$，则判断为猫（正类），若 $P\leq 0.5$，则判断为非猫（负类）。</p>
<p>本项目中，我们主要通过以下技巧来优化神经网络模型：</p>
<ul>
<li>网络输入标准化；</li>
<li>权重 W 初始化技巧；</li>
<li>L2 正则化和 Dropout 技巧；</li>
<li>梯度优化技巧 SGD、Momentum、Adam。</li>
</ul>
<h3 id="">导入数据集</h3>
<p>首先，我们导入构建模型所需的数据集。</p>
<p>该数据集分为训练（Train）集和测试（Test）集，训练集共有 250 张猫的图片和 250 张狗的图片，测试集共有 100 张猫的图片和 100 张狗的图片。我们需要训练神经网络模型来识别图片是否为猫类，最终模型在测试集上进行正确率的验证。</p>
<blockquote>
  <p>说明：本文所有代码均在 Jupyter Notebook 中编写实现。</p>
</blockquote>
<p>首先导入数据集，代码如下：</p>
<pre><code>import skimage.io as io
import numpy as np
import math

%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 6.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# 训练样本
file='./data/train/*.jpg'
coll = io.ImageCollection(file)
X_train = np.asarray(coll)                                   # 500 个训练样本，250 个猫图片，250 个非猫图片
y_train = np.hstack((np.ones(250),np.zeros(250)))            # 输出标签 
y_train = y_train.reshape((1, 500))

# 测试样本
file='./data/test/*.jpg'
coll = io.ImageCollection(file)
X_test = np.asarray(coll)                                   # 200 个训练样本，100 个猫图片，100 个非猫图片
y_test = np.hstack((np.ones(100),np.zeros(100)))            # 输出标签 
y_test = y_test.reshape((1, 200))

m_train = X_train.shape[0]
m_test = X_test.shape[0]
w, h, d = X_train.shape[1], X_train.shape[2], X_train.shape[3]

print('训练样本数量：%d' % m_train)
print('测试样本数量：%d' % m_test)
print('每张图片的维度：(%d, %d, %d)' % (w, h, d))
</code></pre>
<p>上述代码用来导出数据训练集和测试集。训练样本放在课程 GitHub 项目的 <code>./data/train/</code> 目录下，测试样本放在 <code>./data/test/</code> 目录下。训练样本共有 500 个，其中猫图片 250 个，非猫图片 250 个，正负样本各占一半。测试样本共有 200 个，正负样本各占 100 个。每张图片的维度是 64x64x3，其中 3 表示 RGB 三通道。</p>
<p>运行以上程序，输出结果为：</p>
<blockquote>
  <p>训练样本数量：500</p>
  <p>测试样本数量：200</p>
  <p>每张图片的维度：(64, 64, 3)</p>
</blockquote>
<p>接下来，我们从训练样本中随机选择 10 张图片显示，并识别其是否为猫类图片。结果 y = 1 表示是猫类图片；y = 0 表示非猫类图片。测试代码如下：</p>
<pre><code>import matplotlib.pyplot as plt

idx = [np.random.choice(m_train) for _ in range(10)]  # 随机选择 10 张图片
label = y_train[0,idx]
for i in range(2):
    for j in range(5):
        plt.subplot(2, 5, 5*i+j+1)
        plt.imshow(X_train[idx[5*i+j]])
        plt.title("y="+str(label[5*i+j]))
        plt.axis('off')
plt.show()
</code></pre>
<p>以上代码就是从训练数据中随机选择了 10 张图片并显示出来，显示图片的同时也显示图片对应的标签 Label。</p>
<p>10 张图片的输出结果，如下图所示：</p>
<p><img src="https://images.gitbook.cn/2d44c900-afee-11e8-9e72-c76ef41e3edd" alt="enter image description here" /></p>
<h3 id="-1">预处理</h3>
<p>导入数据之后，我们需要对图片进行一些预处理操作。每张图片由 R、G、B 三通道组成，要把每个图片矩阵转化为一维向量，方便神经网络输入层输入数据。代码如下：</p>
<pre><code># 图片矩阵转化为一维向量
X_train = X_train.reshape(m_train, -1).T
X_test = X_test.reshape(m_test, -1).T

print('训练样本维度：' + str(X_train.shape))
print('测试样本维度：' + str(X_test.shape))
</code></pre>
<p>上述代码中，reshape 函数的作用就是将图片尺寸调整为一维数组。</p>
<p>输出结果为：</p>
<blockquote>
  <p>训练样本维度：(12288, 500)</p>
  <p>测试样本维度：(12288, 200)</p>
</blockquote>
<h3 id="-2">网络输入标准化</h3>
<p>我们知道对网络输入进行标准化很有必要，可以防止在训练过程中发生振荡，以加快训练速度。标准化的做法很简单，直接减去各输入特征的均值，再除以各自特征的标准差即可。相应的代码如下：</p>
<pre><code># 首先计算均值和标准差
mean_image = np.mean(X_train, axis=1)
std_image = np.std(X_train, axis=1)
# 然后标准化
X_train = X_train.astype(float)
X_test = X_test.astype(float)
X_train -= mean_image.reshape(12288, 1)
X_train /= std_image.reshape(12288, 1)
X_test -= mean_image.reshape(12288, 1)
X_test /= std_image.reshape(12288, 1)
</code></pre>
<h3 id="minibatch">划分 <code>Mini-Batch</code></h3>
<p>将样本集分割成 <code>Mini-batch</code> 有利于提高神经网络模型训练速度。因此，我们首先定义划分样本集为 Mini-batch 的函数：</p>
<pre><code>def random_mini_batches(X, Y, mini_batch_size = 64):

    m = X.shape[1]                  # 训练样本数据
    mini_batches = []

    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((1,m))

    num_complete_minibatches = math.floor(m/mini_batch_size) # mini-batch 的个数
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size : (k+1) * mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size : (k+1) * mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    # 多出的被 mini_batch_size 除不尽的一些样本再组成一个 mini-batch
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, mini_batch_size * math.floor(m/mini_batch_size) : m]
        mini_batch_Y = shuffled_Y[:, mini_batch_size * math.floor(m/mini_batch_size) : m]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches
</code></pre>
<p>注意，如果总的样本个数不是 <code>mini_batch_size</code> 的整数倍，则最后一个 <code>mini_batch</code> 包含的样本数将少于 <code>mini_batch_size</code>。例如总的样本数为 650，<code>mini_batch_size=64</code>，则总共有 11 个 <code>mini_batch</code>，最后一个 <code>mini_batch</code> 包含的样本数为 10。</p>
<h3 id="wb">初始化 W 和 b</h3>
<p>我们之前说过，一般可以将 W 初始化为均值 0，方差为 0.01 的服从高斯分布随机值，将 b 全部初始化为 0。但遇到网络层数较多的情况，这种对权重 W 的简单初始化容易造成梯度消失或者梯度爆炸。也就是说在进行神经网络反向传播梯度计算的时候，可能会引起梯度呈现指数型增大或减小。梯度过大会造成损失函数曲线振荡，无法准确进行训练；梯度过小会造成损失函数曲线近乎水平，训练缓慢或基本没有效果，这些都会严重影响神经网络训练。</p>
<p>因此，我们需要对权重 W 采用一些初始化技巧，即让权重 W 的方差为 $\frac2n$，参数 b 仍初始化为 0 即可。相应的代码如下：</p>
<pre><code>def initialize_parameters(layers_dims):

    parameters = {}
    L = len(layers_dims) - 1 # 网络层数

    for l in range(1, L + 1):
        parameters['W' + str(l)] = np.random.randn(layers_dims[l],layers_dims[l-1]) * np.sqrt(2/layers_dims[l-1])
        parameters['b' + str(l)] = np.zeros((layers_dims[l],1))

    return parameters
</code></pre>
<h3 id="l2">L2 正则化</h3>
<p>神经网络模型容易发生过拟合，即模型对训练样本拟合得较好，但是对测试样本效果较差，模型的泛化能力不强。通常来说，为了避免发生过拟合，需要一些正则化技巧提高模型的泛化能力。</p>
<p>神经网络 L2 正则化是指在损失函数中增加 $||w||^2$ 项，表达式如下：</p>
<p>$$J(w^{[1]},b^{[1]},\cdots,w^{[L]},b^{[L]})=\frac1m\sum_{i=1}^mL(\hat y^{(i)},y^{(i)})+\frac{\lambda}{2m}\sum_{l=1}^L||w^{[l]}||^2$$</p>
<p>$$||w^{[l]}||^2=\sum_{i=1}^{n^{[l]}}\sum_{j=1}^{n^{[l-1]}}(w_{ij}^{[l]})^2$$</p>
<p>其中，$l$ 表示当前神经网络层数，$n^{[l]}$ 为当前神经网络层包含的神经元个数。</p>
<p>因此，我们要在原来的损失函数 Loss 基础上加上 L2 正则项。引入 L2 正则化后的正向传播写成 Python 代码如下：</p>
<pre><code>def compute_cost_with_regularization(A3, Y, parameters, lambd):

    m = Y.shape[1]
    W1 = parameters["W1"]
    W2 = parameters["W2"]
    W3 = parameters["W3"]

    cross_entropy_cost = compute_cost(A3, Y) # 损失函数交叉熵

    L2_regularization_cost = lambd/(2*m)*(np.sum(np.square(W1)) + np.sum(np.square(W2)) + np.sum(np.square(W3))) # 正则化项

    cost = cross_entropy_cost + L2_regularization_cost

    return cost
</code></pre>
<p>反向传播相应的 Python 代码为：</p>
<pre><code>def backward_propagation_with_regularization(X, Y, cache, lambd):

    m = X.shape[1]
    (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3) = cache

    dZ3 = A3 - Y

    dW3 = 1./m * np.dot(dZ3, A2.T) + lambd/m*W3
    db3 = 1./m * np.sum(dZ3, axis=1, keepdims = True)

    dA2 = np.dot(W3.T, dZ3)
    dZ2 = np.multiply(dA2, np.int64(A2 &gt; 0))
    dW2 = 1./m * np.dot(dZ2, A1.T) + lambd/m*W2
    db2 = 1./m * np.sum(dZ2, axis=1, keepdims = True)

    dA1 = np.dot(W2.T, dZ2)
    dZ1 = np.multiply(dA1, np.int64(A1 &gt; 0))
    dW1 = 1./m * np.dot(dZ1, X.T) + lambd/m*W1
    db1 = 1./m * np.sum(dZ1, axis=1, keepdims = True)

    gradients = {"dZ3": dZ3, "dW3": dW3, "db3": db3,"dA2": dA2,
                 "dZ2": dZ2, "dW2": dW2, "db2": db2, "dA1": dA1, 
                 "dZ1": dZ1, "dW1": dW1, "db1": db1}

    return gradients
</code></pre>
<h3 id="dropout">Dropout 正则化</h3>
<p>在第 10 课，我们已经介绍了 Dropout 正则化的基本原理，Inverted Dropout 在训练的时候，原神经元的输出直接乘以 $\frac1p$，以获得同样的期望值。举个例子来说明，假设第 $l$ 层神经元的输出是 $al$，保留神经元比例概率 keep_prob=0.8，即该层有 20% 的神经元停止工作。经过 Dropout 正则化作用，随机删减 20% 的神经元，只保留 80% 的神经元。最后，还要对 $al$ 进行 Scale Up 处理，即乘以 $\frac1p$。我们定义 Dropout 的正向传播函数为：</p>
<pre><code>def forward_propagation_with_dropout(X, parameters, keep_prob = 0.8):

    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    W3 = parameters["W3"]
    b3 = parameters["b3"]

    # LINEAR -&gt; RELU -&gt; LINEAR -&gt; RELU -&gt; LINEAR -&gt; SIGMOID
    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)

    D1 = np.random.rand(A1.shape[0],A1.shape[1])      # Step 1: 初始化掩模矩阵 D1
    D1 = D1 &lt; keep_prob                               # Step 2: D1 与阈值比较，0 or 1
    A1 = A1 * D1                                      # Step 3: 关闭一些神经元
    A1 = A1/keep_prob                                 # Step 4: scale up，保证期望值一致

    Z2 = np.dot(W2, A1) + b2
    A2 = relu(Z2)

    D2 = np.random.rand(A2.shape[0],A2.shape[1])      # Step 1: 初始化掩模矩阵 D1
    D2 = D2 &lt; keep_prob                               # Step 2: D1 与阈值比较，0 or 1
    A2 = A2 * D2                                      # Step 3: 关闭一些神经元
    A2 = A2/keep_prob                                 # Step 4: scale up，保证期望值一致

    Z3 = np.dot(W3, A2) + b3
    A3 = sigmoid(Z3)

    cache = (Z1, D1, A1, W1, b1, Z2, D2, A2, W2, b2, Z3, A3, W3, b3)

    return A3, cache
</code></pre>
<p>定义 Dropout 的反向传播函数为：</p>
<pre><code>def backward_propagation_with_dropout(X, Y, cache, keep_prob):

    m = X.shape[1]
    (Z1, D1, A1, W1, b1, Z2, D2, A2, W2, b2, Z3, A3, W3, b3) = cache

    dZ3 = A3 - Y
    dW3 = 1./m * np.dot(dZ3, A2.T)
    db3 = 1./m * np.sum(dZ3, axis=1, keepdims = True)
    dA2 = np.dot(W3.T, dZ3)

    dA2 = dA2 * D2              # Step 1: 关闭一些神经元
    dA2 = dA2/keep_prob         # Step 2: scale up，保证期望值一致

    dZ2 = np.multiply(dA2, np.int64(A2 &gt; 0))
    dW2 = 1./m * np.dot(dZ2, A1.T)
    db2 = 1./m * np.sum(dZ2, axis=1, keepdims = True)

    dA1 = np.dot(W2.T, dZ2)

    dA1 = dA1 * D1              # Step 1: 关闭一些神经元
    dA1 = dA1/keep_prob         # Step 2: scale up，保证期望值一致

    dZ1 = np.multiply(dA1, np.int64(A1 &gt; 0))
    dW1 = 1./m * np.dot(dZ1, X.T)
    db1 = 1./m * np.sum(dZ1, axis=1, keepdims = True)

    gradients = {"dZ3": dZ3, "dW3": dW3, "db3": db3,"dA2": dA2,
                 "dZ2": dZ2, "dW2": dW2, "db2": db2, "dA1": dA1, 
                 "dZ1": dZ1, "dW1": dW1, "db1": db1}

    return gradients
</code></pre>
<h3 id="momentum">梯度优化之 Momentum</h3>
<p>Momentum 的关键是对梯度进行了指数加权，权重 W 和常数项 b 的指数加权平均表达式如下：</p>
<p>$$V_{dW}=\beta\cdot V_{dW}+(1-\beta)\cdot dW$$</p>
<p>$$V_{db}=\beta\cdot V_{db}+(1-\beta)\cdot db$$</p>
<p>上式中，$dW$ 和 $db$ 分别为本次迭代训练计算中 W 和 b 的梯度。$V_{dW}$ 和 $V_{db}$ 分别表示加权修正的 $dW$ 和 $db$。$V_{dW}$ 和 $V_{db}$ 的初始值为 0，每次迭代训练后，其值由上一次的 $V_{dW}$ 和 $V_{db}$ 以及 $dW$ 和 $db$ 共同决定并更新。$\beta$ 是加权系数，取值范围为 <code>[0,1]</code>，一般取 0.8 或 0.9 不等。</p>
<p>首先对 $V_{dw}$ 和 $V_{db}$ 进行初始化：</p>
<pre><code>def initialize_velocity(parameters):

    L = len(parameters) // 2 # 神经网络层数
    v = {}

    # 初始化 V
    for l in range(L):
        v["dW" + str(l+1)] = np.zeros(parameters['W' + str(l+1)].shape)
        v["db" + str(l+1)] = np.zeros(parameters['b' + str(l+1)].shape)

    return v
</code></pre>
<p>然后，定义 Momentum 梯度优化过程：</p>
<pre><code>def update_parameters_with_momentum(parameters, grads, v, beta, learning_rate):

    L = len(parameters) // 2     # 神经网络层数

    # Momentum 更新
    for l in range(L):
        # 计算 Vdw 和 Vdb
        v["dW" + str(l+1)] = beta * v["dW" + str(l+1)] + (1 - beta) * grads["dW" + str(l+1)]
        v["db" + str(l+1)] = beta * v["db" + str(l+1)] + (1 - beta) * grads["db" + str(l+1)]
        # 更新参数
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * v["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * v["db" + str(l+1)]

    return parameters, v
</code></pre>
<h3 id="adam">梯度优化之 Adam</h3>
<p>Adam（Adaptive Moment Estimation）是另一种自适应学习率的方法。它利用梯度的一阶矩估计和二阶矩估计动态调整每个参数的学习率。Adam 的优点主要在于经过偏置校正后，每一次迭代学习率都有个确定范围，使得参数比较平稳。相应的公式如下：</p>
<p>$$V_{dW}=\beta_1V_{dW}+(1-\beta_1)dW,\ V_{db}=\beta_1V_{db}+(1-\beta_1)db$$</p>
<p>$$S_{dW}=\beta_2S_{dW}+(1-\beta_2)dW^2,\ S_{db}=\beta_2S_{db}+(1-\beta_2)db^2$$</p>
<p>$$V_{dW}^{corrected}=\frac{V_{dW}}{1-\beta_1^t},\ V_{db}^{corrected}=\frac{V_{db}}{1-\beta_1^t}$$</p>
<p>$$S_{dW}^{corrected}=\frac{S_{dW}}{1-\beta_2^t},\ S_{db}^{corrected}=\frac{S_{db}}{1-\beta_2^t}$$</p>
<p>$$W:=W-\alpha\frac{V_{dW}^{corrected}}{\sqrt{S_{dW}^{corrected}+\varepsilon}},\ b:=b-\alpha\frac{V_{db}^{corrected}}{\sqrt{S_{db}^{corrected}+\varepsilon}}$$</p>
<p>其中，t 是当前迭代次数。Adam 算法包含了几个超参数，分别是：$\alpha、\beta_1、\beta_2、\varepsilon$。其中，$\beta_1$ 通常设置为0.9，$\beta_2$ 通常设置为0.999，$\varepsilon$ 通常设置为$10^{-7}$。一般只需要对 $\beta_1$ 和 $\beta_2$ 进行调试。</p>
<p>首先对 $V_{dw}$、$V_{db}$、$S_{dw}$、$S_{db}$ 进行初始化：</p>
<pre><code>def initialize_adam(parameters) :

    L = len(parameters) // 2     # 神经网络层数
    v = {}
    s = {}

    # 初始化
    for l in range(L):
        v["dW" + str(l+1)] = np.zeros(parameters["W" + str(l+1)].shape)
        v["db" + str(l+1)] = np.zeros(parameters["b" + str(l+1)].shape)
        s["dW" + str(l+1)] = np.zeros(parameters["W" + str(l+1)].shape)
        s["db" + str(l+1)] = np.zeros(parameters["b" + str(l+1)].shape)

    return v, s
</code></pre>
<p>然后，定义 Adam 梯度优化过程：</p>
<pre><code>def update_parameters_with_adam(parameters, grads, v, s, t, learning_rate = 0.01,
                                beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):

    L = len(parameters) // 2                 # 神经网络层数
    v_corrected = {}                         
    s_corrected = {}                         

    # Adam 更新
    for l in range(L):
        v["dW" + str(l+1)] = beta1 * v["dW" + str(l+1)] + (1 - beta1) * grads["dW" + str(l+1)]
        v["db" + str(l+1)] = beta1 * v["db" + str(l+1)] + (1 - beta1) * grads["db" + str(l+1)]

        v_corrected["dW" + str(l+1)] = v["dW" + str(l+1)]/(1 - np.power(beta1,t))
        v_corrected["db" + str(l+1)] = v["db" + str(l+1)]/(1 - np.power(beta1,t))

        s["dW" + str(l+1)] = beta2 * s["dW" + str(l+1)] + (1-beta2) * np.power(grads["dW" + str(l+1)],2)
        s["db" + str(l+1)] = beta2 * s["db" + str(l+1)] + (1-beta2) * np.power(grads["db" + str(l+1)],2)

        s_corrected["dW" + str(l+1)] = s["dW" + str(l+1)]/(1 - np.power(beta2,t))
        s_corrected["db" + str(l+1)] = s["db" + str(l+1)]/(1 - np.power(beta2,t))

        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * v_corrected["dW" + str(l+1)]/(np.sqrt(s_corrected["dW" + str(l+1)]) + epsilon)
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * v_corrected["db" + str(l+1)]/(np.sqrt(s_corrected["db" + str(l+1)]) + epsilon)

    return parameters, v, s
</code></pre>
<h3 id="model">构建整个模型 Model</h3>
<p>接下来，用我们已经写好的函数模块，构建整个神经网络模型。</p>
<pre><code>def model(X, Y, layers_dims, optimizer, lambd = 0, keep_prob = 1, learning_rate = 0.0007, mini_batch_size = 64, 
          beta = 0.9, beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8, num_epochs = 2000, print_cost = True):

    L = len(layers_dims)             # 神经网络层数，包括输入层
    costs = []                       # 损失函数列表
    t = 0                            # Adam 算法中的迭代次数

    # 初始化参数
    parameters = initialize_parameters(layers_dims)

    # 初始化优化器
    if optimizer == "gd":
        pass # 没有使用梯度优化算法
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    # 迭代训练
    for i in range(num_epochs):

        # mini-batch
        minibatches = random_mini_batches(X, Y, mini_batch_size)

        for minibatch in minibatches:

            # 选择一组 mini-batch
            (minibatch_X, minibatch_Y) = minibatch

            # 正向传播：LINEAR -&gt; RELU -&gt; LINEAR -&gt; RELU -&gt; LINEAR -&gt; SIGMOID
            if keep_prob == 1:
                A3, cache = forward_propagation(minibatch_X, parameters)
            elif keep_prob &lt; 1:
                A3, cache = forward_propagation_with_dropout(minibatch_X, parameters, keep_prob)

            # 计算 cost
            if lambd == 0:
                cost = compute_cost(A3, minibatch_Y)
            else:
                cost = compute_cost_with_regularization(A3, minibatch_Y, parameters, lambd)

            # 反向传播
            if lambd == 0 and keep_prob == 1:
                grads = backward_propagation(minibatch_X, minibatch_Y, cache)
            elif lambd != 0:
                grads = backward_propagation_with_regularization(minibatch_X, minibatch_Y, cache, lambd)
            elif keep_prob &lt; 1:
                grads = backward_propagation_with_dropout(minibatch_X, minibatch_Y, cache, keep_prob)

            # 更新参数
            if optimizer == "gd":
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(parameters, grads, v, beta, learning_rate)
            elif optimizer == "adam":
                t = t + 1 # 迭代次数 +1
                parameters, v, s = update_parameters_with_adam(parameters, grads, v, s,
                                                               t, learning_rate, beta1, beta2,  epsilon)

        # 每隔 1000 epoch，打印 cost
        if print_cost and i % 1000 == 0:
            print ("Cost after epoch %i: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # plot the cost
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('epochs (per 100)')
    plt.title("Learning rate = " + str(learning_rate))
    plt.show()

    return parameters
</code></pre>
<h3 id="-3">模型预测</h3>
<p>模型搭建完毕之后，就可以使用训练好的模型对新样本进行预测。</p>
<pre><code>def predict(X, y, parameters):

    m = X.shape[1]
    p = np.zeros((1,m), dtype = np.int)

    # 正向传播过程
    A3, caches = forward_propagation(X, parameters)

    for i in range(0, A3.shape[1]):
        if A3[0,i] &gt; 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0

    print("Accuracy: "  + str(np.mean((p[0,:] == y[0,:]))))

    return p
</code></pre>
<h3 id="-4">不使用正则化和梯度优化</h3>
<p>首先，我们来看一下不使用正则化和梯度优化的训练和测试结果：</p>
<pre><code># 训练 3-layer 神经网络
layers_dims = [X_train.shape[0], 20, 10, 1]
parameters = model(X_train, y_train, layers_dims, optimizer = "gd")
</code></pre>
<blockquote>
  <p>Cost after epoch 0: 0.719807</p>
  <p>Cost after epoch 200: 0.067682</p>
  <p>Cost after epoch 400: 0.040513</p>
  <p>Cost after epoch 600: 0.012301</p>
  <p>Cost after epoch 800: 0.009563</p>
  <p>Cost after epoch 1000: 0.005953</p>
  <p>Cost after epoch 1200: 0.004771</p>
  <p>Cost after epoch 1400: 0.004348</p>
  <p>Cost after epoch 1600: 0.003999</p>
  <p>Cost after epoch 1800: 0.003859</p>
  <p>Cost after epoch 2000: 0.002428</p>
  <p>Cost after epoch 2200: 0.001776</p>
  <p>Cost after epoch 2400: 0.002429</p>
  <p>Cost after epoch 2600: 0.001614</p>
  <p>Cost after epoch 2800: 0.001663</p>
</blockquote>
<p>随迭代次数的增加，损失函数的变化趋势如下图所示：</p>
<p><img src="https://images.gitbook.cn/f3e57ec0-b0ab-11e8-ac69-5fa26bfde8c1" alt="enter image description here" /></p>
<p>计算训练样本的准确率：</p>
<pre><code>predictions = predict(X_train, y_train, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.99</p>
</blockquote>
<p>测试样本的准确率：</p>
<pre><code>predictions = predict(X_test, y_test, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.525</p>
</blockquote>
<h3 id="l2adam">使用 L2 正则化，Adam 优化</h3>
<p>现在，使用 L2 正则化，Adam 优化对神经网络进行训练。</p>
<pre><code># 训练 3-layer 神经网络
layers_dims = [X_train.shape[0], 20, 10, 1]
parameters = model(X_train, y_train, layers_dims, lambd = 0.01, optimizer = "adam")
</code></pre>
<blockquote>
  <p>Cost after epoch 0: 1.097954</p>
  <p>Cost after epoch 200: 0.024345</p>
  <p>Cost after epoch 400: 0.036834</p>
  <p>Cost after epoch 600: 0.022035</p>
  <p>Cost after epoch 800: 0.070609</p>
  <p>Cost after epoch 1000: 0.022724</p>
  <p>Cost after epoch 1200: 0.104538</p>
  <p>Cost after epoch 1400: 0.021234</p>
  <p>Cost after epoch 1600: 0.088165</p>
  <p>Cost after epoch 1800: 0.021023</p>
  <p>Cost after epoch 2000: 0.026286</p>
  <p>Cost after epoch 2200: 0.015563</p>
  <p>Cost after epoch 2400: 0.025537</p>
  <p>Cost after epoch 2600: 0.050002</p>
  <p>Cost after epoch 2800: 0.047617</p>
</blockquote>
<p>随迭代次数的增加，损失函数的变化趋势如下图所示：</p>
<p><img src="https://images.gitbook.cn/4169db00-b0ac-11e8-ac69-5fa26bfde8c1" alt="enter image description here" /></p>
<p>计算训练样本的准确率：</p>
<pre><code>predictions = predict(X_train, y_train, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 1.0</p>
</blockquote>
<p>测试样本的准确率：</p>
<pre><code>predictions = predict(X_test, y_test, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.545</p>
</blockquote>
<h3 id="dropoutadam">使用 Dropout，Adam 优化</h3>
<p>现在，使用 Dropout，Adam 优化对神经网络进行训练。</p>
<pre><code># 训练 3-layer 神经网络
layers_dims = [X_train.shape[0], 20, 10, 1]
parameters = model(X_train, y_train, layers_dims, keep_prob = 0.6, optimizer = "adam")
</code></pre>
<blockquote>
  <p>Cost after epoch 0: 3.390538</p>
  <p>Cost after epoch 200: 0.070044</p>
  <p>Cost after epoch 400: 0.086490</p>
  <p>Cost after epoch 600: 0.093776</p>
  <p>Cost after epoch 800: 0.048461</p>
  <p>Cost after epoch 1000: 0.006210</p>
  <p>Cost after epoch 1200: 0.002600</p>
  <p>Cost after epoch 1400: 0.001356</p>
  <p>Cost after epoch 1600: 0.010101</p>
  <p>Cost after epoch 1800: 0.069984</p>
  <p>Cost after epoch 2000: 0.002017</p>
  <p>Cost after epoch 2200: 0.000373</p>
  <p>Cost after epoch 2400: 0.000551</p>
  <p>Cost after epoch 2600: 0.000583</p>
  <p>Cost after epoch 2800: 0.000180</p>
</blockquote>
<p>随迭代次数的增加，损失函数的变化趋势如下图所示：</p>
<p><img src="https://images.gitbook.cn/bd23e5b0-b0ac-11e8-ac69-5fa26bfde8c1" alt="enter image description here" /></p>
<p>计算训练样本的准确率：</p>
<pre><code>predictions = predict(X_train, y_train, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 1.0</p>
</blockquote>
<p>测试样本的准确率：</p>
<pre><code>predictions = predict(X_test, y_test, parameters)
</code></pre>
<p>执行结果如下：</p>
<blockquote>
  <p>Accuracy: 0.585</p>
</blockquote>
<p>通过对比能够看到，使用 L2 正则化、Dropout、梯度优化方法，测试样本准确率都有所提高。事实上，测试样本的准确率也并不是太高，原因是本项目中的图片来自于 Kaggle 竞赛，图片本身的识别本来就比较难。但是本项目中各种优化方法的代码是可行的。对于复杂的图片识别，想要获得更高的准确率，还需要使用卷积神经网络模型（CNN），在接下来的课程中，我们将会重点介绍。</p>
<p>包含本文完整代码的 <code>.ipynb</code> 文件，我已经放在了 GitHub 上，大家可自行下载：</p>
<blockquote>
  <p><a href="https://github.com/RedstoneWill/gitchat_dl/tree/master/14%20chapter">第14课：项目实战——深度优化你的神经网络模型</a></p>
</blockquote></div></article>