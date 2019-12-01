---
title: 深度学习 PyTorch 极简入门-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇我们主要介绍了最简单的二层神经网络模型，详细推导其正向传播过程和反向传播过程，对整个神经网络的模型结构和数学理论推导过程有了清晰的认识和掌握。本文将带大家使用 Python 搭建一个神经网络模型来解决实际的分类问题。</p>
<h3 id="">导入数据集</h3>
<p>为了简化操作，我们直接构造一批数据集。</p>
<blockquote>
  <p>说明：本文所有代码均在 Jupyter Notebook 中编写实现。</p>
</blockquote>
<pre><code>import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline

r = np.random.randn(200)*0.8
x1 = np.linspace(-3, 1, 200)
x2 = np.linspace(-1, 3, 200)
y1 = x1*x1 + 2*x1 - 2 + r
y2 = -x2*x2 + 2*x2 + 2 + r

X = np.hstack(([x1, y1],[x2, y2]))                     # 输入样本 X，维度：2 x 400
Y = np.hstack((np.zeros((1,200)),np.ones((1,200))))    # 输出标签 Y
</code></pre>
<p>输入样本 X 的特征维度为 2，样本个数为 400，输出标签 Y 包含 0 和 1 类别各 200 个。将数据集在二维平面上显示。</p>
<pre><code>plt.scatter(X[0, :], X[1, :], c=Y, s=40, cmap=plt.cm.Spectral)
</code></pre>
<p><img src="https://images.gitbook.cn/75fa28e0-9593-11e8-b8b3-690dce6077c1" alt="enter image description here" /></p>
<p>从正负样本的分布来看，使用简单的逻辑回归进行分类效果肯定不会太好，因为数据集不是线性可分的。下面，我将带大家一步一步搭建一个简单的神经网络模型来解决这个分类问题。</p>
<h3 id="-1">定义神经网络输入层、隐藏层、输出层神经元个数</h3>
<p>我们使用的简单神经网络，只包含一层隐藏层。首先，我们需要定义神经网络输入层、隐藏层、输出层的神经元个数。</p>
<p><img src="https://images.gitbook.cn/369bea10-959a-11e8-a745-212b93fdcf52" alt="enter image description here" /></p>
<pre><code>m = X.shape[1]      # 样本个数
n_x = X.shape[0]    # 输入层神经元个数
n_h = 3             # 隐藏层神经元个数
n_y = Y.shape[0]    # 输出层神经元个数
</code></pre>
<h3 id="wb">网络参数 W 和 b 初始化</h3>
<p>在上一篇中我们说过神经网络模型在开始训练时需要对各层权重系数 W 和常数项 b 进行初始化赋值。初始化赋值时，b 一般全部初始化为 0 即可，但是 W 不能全部初始化为 0。初始化代码如下：</p>
<pre><code>W1 = np.random.randn(n_h,n_x)*0.01
b1 = np.zeros((n_h,1))
W2 = np.random.randn(n_y,n_h)*0.01
b2 = np.zeros((n_y,1))


assert (W1.shape == (n_h, n_x))
assert (b1.shape == (n_h, 1))
assert (W2.shape == (n_y, n_h))
assert (b2.shape == (n_y, 1))

parameters = {"W1": W1,
              "b1": b1,
              "W2": W2,
              "b2": b2}
</code></pre>
<p>其中，assert 语句对向量或者数组维度进行判断。如果与给定的维度不同，则程序在此处停止运行。assert 的灵活使用可以帮助我们及时检查神经网络模型中参数的维度是否正确。</p>
<h3 id="-2">正向传播过程</h3>
<p>正向传播过程，包含了 $Z^{[1]}，A^{[1]}，Z^{[2]}，A^{[2]}$ 的计算，根据上一篇的详细推导结果：</p>
<p>$$Z^{[1]}=W^{[1]}X+b^{[1]}$$</p>
<p>$$A^{[1]}=g(Z^{[1]})$$</p>
<p>$$Z^{[2]}=W^{[2]}A^{[1]}+b^{[2]}$$</p>
<p>$$A^{[2]}=g(Z^{[2]})$$</p>
<p>其中，隐藏层的激活函数 $g(\cdot)$ 选择使用 tanh 函数，输出层的激活函数 $g(\cdot)$ 选择使用 sigmoid 函数。</p>
<pre><code>def sigmoid(x):
    """
    Compute the sigmoid of x
    """
    s = 1/(1+np.exp(-x))
    return s

def forward_propagation(X, parameters):

    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    Z1 = np.dot(W1,X) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2,A1) + b2
    A2 = sigmoid(Z2)

    assert(A2.shape == (1, X.shape[1]))

    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}

    return A2, cache
</code></pre>
<h3 id="-3">损失函数</h3>
<p>m 个样本的损失函数为：</p>
<p>$$J=-\frac{1}{m}\sum_{i=1}^my^{(i)}log\hat y^{(i)}+(1-y^{(i)})log(1-\hat y^{(i)})$$</p>
<pre><code>def compute_cost(A2, Y, parameters):

    m = Y.shape[1] # number of example

    # 计算交叉熵损失函数
    logprobs = np.multiply(np.log(A2),Y)+np.multiply(np.log(1-A2),(1-Y))
    cost = - 1/m * np.sum(logprobs)

    cost = np.squeeze(cost)     

    return cost
</code></pre>
<h3 id="-4">反向传播过程</h3>
<p>反向传播过程需要计算损失函数 $J$ 对各个变量 $A^{[2]}$，$Z^{[2]}$，$W^{[2]}$，$b^{[2]}$，$A^{[1]}$，$Z^{[1]}$，$W^{[1]}$，$b^{[1]}$ 的偏导数。根据上一篇的详细推导结果：</p>
<p>$$dZ^{[2]}=A^{[2]}-Y$$</p>
<p>$$dW^{[2]}=\frac1mdZ^{[2]}A^{[1]T}$$</p>
<p>$$db^{[2]}=\frac1mnp.sum(dZ^{[2]},axis=1)$$</p>
<p>$$dZ^{[1]}=W^{[2]T}dZ^{[2]}\ast g'(Z^{[1]})$$</p>
<p>$$dW^{[1]}=\frac1mdZ^{[1]}X^T$$</p>
<p>$$db^{[1]}=\frac1mnp.sum(dZ^{[1]},axis=1)$$</p>
<p>反向传播函数定义为：</p>
<pre><code>def backward_propagation(parameters, cache, X, Y):

    m = X.shape[1]

    W1 = parameters["W1"]
    W2 = parameters["W2"]

    A1 = cache["A1"]
    A2 = cache["A2"]

    # 反向求导
    dZ2 = A2 - Y
    dW2 = 1/m*np.dot(dZ2,A1.T)
    db2 = 1/m*np.sum(dZ2,axis=1,keepdims=True)
    dZ1 = np.dot(W2.T,dZ2)*(1 - np.power(A1, 2))
    dW1 = 1/m*np.dot(dZ1,X.T)
    db1 = 1/m*np.sum(dZ1,axis=1,keepdims=True)

    # 存储各个梯度值
    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}

    return grads
</code></pre>
<h3 id="-5">网络参数更新</h3>
<p>根据梯度下降算法，对网络参数 W 和 b 进行更新，并将新的网络参数存储在字典里。</p>
<pre><code>def update_parameters(parameters, grads, learning_rate = 0.1):

    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]

    W1 = W1 - learning_rate*dW1
    b1 = b1 - learning_rate*db1
    W2 = W2 - learning_rate*dW2
    b2 = b2 - learning_rate*db2

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters
</code></pre>
<h3 id="-6">搭建整个神经网络模型</h3>
<p>各个模块已经写好，接下来要做的就是将各个模块组合起来，搭建整个神经网络模型。</p>
<pre><code>def nn_model(X, Y, n_h = 3, num_iterations = 10000, print_cost=False):

    m = X.shape[1]      # 样本个数
    n_x = X.shape[0]    # 输入层神经元个数
    n_y = Y.shape[0]    # 输出层神经元个数

    W1 = np.random.randn(n_h,n_x)*0.01
    b1 = np.zeros((n_h,1))
    W2 = np.random.randn(n_y,n_h)*0.01
    b2 = np.zeros((n_y,1))

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    # 迭代训练
    J = []     # 存储损失函数
    for i in range(0, num_iterations):

        A2, cache = forward_propagation(X, parameters)            # 正向传播
        cost = compute_cost(A2, Y, parameters)                    # 计算损失函数
        grads = backward_propagation(parameters, cache, X, Y)     # 反向传播
        parameters = update_parameters(parameters, grads)         # 更新权重
        J.append(cost)

        # 每隔 1000 次训练，打印 cost
        if print_cost and i % 1000 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))

    return parameters
</code></pre>
<h3 id="-7">模型训练</h3>
<p>接下来，就可以使用样本数据，对模型进行训练。</p>
<pre><code>parameters = nn_model(X, Y, n_h = 3, num_iterations = 10000, print_cost=True)
</code></pre>
<p>从 print 的结果看，损失函数是逐渐下降的。</p>
<blockquote>
  <p>Cost after iteration 0: 0.693142</p>
  <p>Cost after iteration 1000: 0.035742</p>
  <p>Cost after iteration 2000: 0.016065</p>
  <p>Cost after iteration 3000: 0.013651</p>
  <p>Cost after iteration 4000: 0.012505</p>
  <p>Cost after iteration 5000: 0.011774</p>
  <p>Cost after iteration 6000: 0.011240</p>
  <p>Cost after iteration 7000: 0.010816</p>
  <p>Cost after iteration 8000: 0.010457</p>
  <p>Cost after iteration 9000: 0.010137</p>
</blockquote>
<h3 id="-8">模型预测</h3>
<p>模型搭建完毕之后，就可以使用训练好的模型对新样本进行预测。</p>
<pre><code>def predict(parameters, X):

    A2, cache = forward_propagation(X, parameters)
    predictions = A2 &gt; 0.5

    return predictions
</code></pre>
<pre><code>y_pred = predict(parameters,X)
accuracy = np.mean(y_pred == Y)
print(accuracy)
</code></pre>
<blockquote>
  <p>0.9825</p>
</blockquote>
<p>得到的预测准确率达到了 98.25%。</p>
<p>最后，为了更直观地查看分类曲线和分类效果，我们绘制分类界限。</p>
<pre><code>def plot_decision_boundary(model, X, y):

    x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
    y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
    h = 0.01

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = model(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[0, :], X[1, :], c=y, cmap=plt.cm.Spectral)
</code></pre>
<pre><code>plot_decision_boundary(lambda x: predict(parameters, x.T), X, Y)
plt.title("Decision Boundary, hidden layers = 5")
plt.show()
</code></pre>
<p><img src="https://images.gitbook.cn/5423ffe0-9622-11e8-bd60-15398afc36e1" alt="enter image description here" /></p>
<h3 id="-9">隐藏层神经元个数对分类效果的影响</h3>
<p>下面，分别设置隐藏层神经元个数 n_h = 2、3、4、6，看看分类效果如何。</p>
<p>当 n_h = 2 时，测得准确率为 88.25%。</p>
<p><img src="https://images.gitbook.cn/616ae510-9622-11e8-9c35-b59aad3fef8b" alt="enter image description here" /></p>
<p>当 n_h = 4 时，测得准确率为 98.5%。</p>
<p><img src="https://images.gitbook.cn/81020d90-9622-11e8-bee3-b1dbef72ca56" alt="enter image description here" /></p>
<p>可见，当 n_4 = 4 时，分类准确率最高。一般情况下，神经元个数越多，模型的分类准确率越高。但是，根据问题的复杂程度，一味地增加神经元个数不一定总会提高准确率，准确率可能会达到饱和状态。另外，神经元个数过多也容易造成过拟合。实际应用中，神经元个数一般可以通过交叉验证选择最佳个数。</p>
<p>包含本文完整代码的 <code>.ipynb</code> 文件，我已经放在了 GitHub 上。附上地址：</p>
<ul>
<li><a href="https://github.com/RedstoneWill/gitchat_dl">第07课 <code>.ipynb</code> 文件获取地址</a> </li>
</ul></div></article>