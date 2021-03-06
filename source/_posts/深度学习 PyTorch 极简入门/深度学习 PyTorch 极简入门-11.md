---
title: 深度学习 PyTorch 极简入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇，我们主要介绍了在神经网络模型中如何防止出现过拟合问题。常用的方法是 L1、L2 正则化，Dropout 正则化，Data Augmentation，Early Stopping 等。本文将重点介绍如何使用梯度优化来使神经网络训练更快更有效率。</p>
<h3 id="minibatch"><code>Mini-Batch</code> 梯度下降</h3>
<p>神经网络反向传播的过程需要使用梯度下降算法来优化网络参数，迭代更新。我们之前介绍的梯度下降算法做法是每次训练都使用全部 m 个训练样本（称为 Batch）。该做法的缺点是当 m 很大的时候，例如百万数量级（这在大型的深度学习神经网络里是比较常见的），会影响运算速度，增加模型的训练时间。</p>
<p>为了解决这一问题，我们可以将 m 个样本均匀分割成若干个子集，每个子集包含较少的样本数量。一般子集包含的样本数量为 64、128、256 等，较常使用 2 的幂数。计算机存储数据一般是 2 的幂，这样设置可以提高运算速度。然后，对每个子集依次进行训练。所有的子集都训练完成之后，可以说一次训练就完成了，我们称之为一次 epoch。这就是 <code>Mini-Batch</code> 梯度下降算法。</p>
<p>例如总的训练样本数量 m = 320000，拆分成 T=5000 个子集，每个 <code>Mini-Batch</code> 包含样本的个数是 64。我们将每个 <code>Mini-Batch</code> 的输入记为 $X^{\{t\}}$，输出记为 $Y^{\{t\}}$，$t=1,2,\cdots,T$。</p>
<p>这里总结下神经网络参数标记中各个上标一般表示的含义：</p>
<ul>
<li><p><strong>$X^{(i)}$ ：第 $i$ 个样本</strong>；</p></li>
<li><p><strong>$Z^{[l]}$：神经网络第 $l$ 层网络的线性输出</strong>；</p></li>
<li><p><strong>$X^{\{t\}},Y^{\{t\}}$：第 $t$ 组 <code>Mini-Batch</code></strong>。</p></li>
</ul>
<p>使用 <code>Mini-Batch</code> 梯度下降算法单次 epoch 的训练过程如下：</p>
<p>$for\ \ t=1,\cdots,T$</p>
<p>$\{$</p>
<p>$\ \ \ \ Forward\ Propagation$</p>
<p>$\ \ \ \ Compute\ Cost\ Function$</p>
<p>$\ \ \ \ Backward\ Propagation$</p>
<p>$\ \ \ \ W:=W-\alpha\cdot dW$</p>
<p>$\ \ \ \ b:=b-\alpha\cdot db$</p>
<p>$\}$</p>
<p>值得一提的是，我们常说的迭代训练 N 次，是指包含 N 次 epoch。每次 epoch 又进行 T 次 <code>Mini-Batch</code> 梯度下降。也就是说每次 epoch 都会把所有 m 个训练样本训练完毕，之后再进入第二次 epoch。对于 <code>Mini-Batch</code> 梯度下降，每次 epoch 最好是随机打乱所有训练样本，再重新随机均匀分成 T 个 <code>Mini-Batch</code>。这样更有利于神经网络进行准确的训练。</p>
<p>我们来比较一下 Batch 梯度下降和 <code>Mini-Batch</code> 梯度下降的性能。</p>
<p><img src="https://images.gitbook.cn/64443890-a0fe-11e8-adf5-590019ab5349" alt="enter image description here" /></p>
<p>上图显示的是 Batch 梯度下降和 <code>Mini-Batch</code> 梯度下降损失函数 cost 的变化趋势。一般来说，Batch 梯度下降损失函数的下降过程是比较平滑的，但是 <code>Mini-Batch</code> 梯度下降损失函数略有震荡，但也是整体下降的。这是因为，<code>Mini-Batch</code> 梯度下降每次更新都使用不同的 <code>Mini-Batch</code>，模型有可能出现不同的表现，这也是正常的。</p>
<p>说个极端的情况，当 T=m，即每个 <code>Mini-Batch</code> 包含的样本数为 1 的时候，就成为了随机梯度下降算法（Stachastic Gradient Descent，SGD）。根据 T 的取值不同，就形成了 Batch 梯度下降、<code>Mini-Batch</code> 梯度下降、随机梯度下降三种不同的算法。</p>
<p>下面我们来比较一下这三种算法的梯度下降曲线。</p>
<p><img src="https://images.gitbook.cn/9d974000-a0ff-11e8-adf5-590019ab5349" alt="enter image description here" /></p>
<p>上图中，蓝色代表是 Batch 梯度下降的优化路径，绿色代表的 <code>Mini-Batch</code> 梯度下降的优化路径，紫色代表的是随机梯度下降的优化路径。Batch 梯度下降会比较平稳地接近全局最小值，但因为使用了所有 m 个样本，每次前进的速度有些慢、时间也有些长。随机梯度下降每次前进速度很快，但是路线曲折，有较大的振荡，最终会在最小值附近来回波动，难以真正达到全局最优值。而 <code>Mini-Batch</code> 梯度下降每次前进速度较快，且振荡较小，基本能接近全局最优值。</p>
<p>实际应用时，如果样本数量不是太大，例如 <code>m&lt;2000</code>，则三种梯度下降算法差别不大，可以直接使用 Batch 梯度下降。若样本数量很大时，则一般使用 <code>Mini-Batch</code> 梯度下降。每个 Batch 的 Size 可根据实际情况而定，一般不要太大也不要太小。</p>
<h3 id="momentumgd">动量梯度下降（Momentum GD）</h3>
<p>动量梯度下降算法是在每次训练时，对梯度进行指数加权平均处理，然后用得到的梯度值更新权重 W 和常数项 b。它的速度要比传统的梯度下降算法快。</p>
<p>该算法的关键是对梯度进行了指数加权，权重 W 和常数项 b 的指数加权平均表达式如下：</p>
<p>$$V_{dW}=\beta\cdot V_{dW}+(1-\beta)\cdot dW$$</p>
<p>$$V_{db}=\beta\cdot V_{db}+(1-\beta)\cdot db$$</p>
<p>上式中，$dW$ 和 $db$ 分别为本次迭代训练计算中的 W 和 b 的梯度。$V_{dW}$ 和 $V_{db}$ 分别表示加权修正的 $dW$ 和 $db$。$V_{dW}$ 和 $V_{db}$ 的初始值为 0，每次迭代训练后，其值由上一次的 $V_{dW}$ 和 $V_{db}$ 以及 $dW$ 和 $db$ 共同决定并更新。$\beta$ 是加权系数，取值范围为 [0,1]，一般取 0.8 或 0.9 不等。</p>
<p>在其它文献资料中，动量梯度下降还有另外一种比较常见的写法：</p>
<p>$$V_{dW}=\beta V_{dW}+dW$$</p>
<p>$$V_{db}=\beta V_{db}+db$$</p>
<p>可见，$V_{dW}$ 和 $V_{db}$ 由之前 W 和 b 的梯度和当前 W 和 b 的梯度共同决定，是一种加权平均的形式。这样有什么好处呢？滑动平均能让 $V_{dW}$ 和 $V_{db}$ 每次更新不会有太大的振荡。而且，$\beta$ 越接近 1，滑动平均的效果越明显，振荡越小。也就是说，当前的速度是渐变的，而不是瞬变的，这保证了梯度下降的平稳性和准确性，减少振荡，较快地达到最小值处。</p>
<p>然后，每次迭代训练后就会使用 $V_{dW}$ 和 $V_{db}$ 来更新 W 和 b：</p>
<p>$$W = W-\alpha\cdot V_{dW}$$</p>
<p>$$b=b-\alpha\cdot V_{db}$$</p>
<p>下面来比较一下传统梯度下降与动量梯度下降算法的实际训练效果。</p>
<p><img src="https://images.gitbook.cn/eaa31ca0-a11a-11e8-a81f-49efe4a8d273" alt="enter image description here" /></p>
<p>如上图所示，蓝色表示的是传统的梯度下降，红色表示的是动量梯度下降算法。显然，传统的梯度下降优化路径是比较曲折的，振荡较大，尤其在 W、b 之间数值范围差别较大的情况下。每一点处的梯度只与当前方向有关，产生类似折线的效果，前进缓慢，达到全局最优解的耗时更多。而动量梯度下降算法对梯度进行指数加权平均，这样使当前梯度不仅与当前方向有关，还与之前的方向有关，这样的处理使梯度前进方向更加平滑，减少振荡，能够更快地到达最小值处。</p>
<p>用 Python 实现动量梯度下降算法，代码示例如下：</p>
<pre><code>dW = compute_gradient(W)
db = compute_gradient(b)
Vdw = beta*Vdw + dW
Vdb = beta*Vdb + db
W -= alpha*Vdw
b -= alpha*Vdb
</code></pre>
<h3 id="nesterovmomentum">Nesterov Momentum</h3>
<p>Nesterov Momentum 是 Momentum GD 的变种，与 Momentum GD 唯一区别就是，计算梯度的不同。Nesterov Momentum 先用当前的 $V$ 更新一遍参数，再用更新的临时参数计算新的梯度，相当于添加了矫正因子的 Momentum GD。Nesterov Momentum 可以防止优化算法走得太快错过极小值，使其对变动的反应更灵敏。</p>
<p>相应的表达式如下：</p>
<p>$$dW=\nabla J(W+\beta V_{dW})$$</p>
<p>$$db=\nabla J(b+\beta V_{db})$$</p>
<p>$$V_{dW}=\beta\cdot V_{dW}-\alpha\cdot dW$$</p>
<p>$$V_{db}=\beta\cdot V_{db}-\alpha\cdot db$$</p>
<p>$$W = W+V_{dW}$$</p>
<p>$$b=b+V_{db}$$</p>
<p>下面这张图展示了 Momentum GD 与 Nesterov Momentum 更新的不同之处。</p>
<p><img src="https://images.gitbook.cn/8b9e1a10-a765-11e8-9a80-ff5f9b540635" alt="enter image description here" /></p>
<p>SGD、Momentum GD、Nesterov Momentum 的实际训练效果对比结果，如下图所示：</p>
<p><img src="https://images.gitbook.cn/006a7640-a766-11e8-8e69-83a537438da3" alt="enter image description here" /></p>
<p>显然，Nesterov Momentum 除了速度较快之外，振荡也更小一些。</p>
<p>Nesterov Momentum 相应的 Python 示例代码如下：</p>
<pre><code>dW = compute_gradient(W)
db = compute_gradient(b)
Vdw = beta*Vdw - alpha*dW
Vdb = beta*Vdb - alpha*db
W += Vdw
b += Vdb
</code></pre>
<h3 id="adagrad">AdaGrad</h3>
<p>上述优化算法，对每一个参数 W 和 b 的训练都使用了相同的学习因子 $\alpha$。AdaGrad 能够在训练中自动的对 $\alpha$ 进行调整，对于出现频率较低参数采用较大的更新；相反，对于出现频率较高的参数采用较小的更新。因此，AdaGrad 非常适合处理稀疏数据。</p>
<p>AdaGrad 的做法是对从开始到当前迭代训练的所有参数进行平方和累计，设当前迭代次数为 t，则梯度的平方和为：</p>
<p>$$SdW=\sum_{i=1}^tdW^2$$</p>
<p>$$Sdb=\sum_{i=1}^tdb^2$$</p>
<p>这样，随着迭代次数 t 的增加，$SdW$ 和 $Sdb$ 都有不同程度的增加。然后，使用参数更新公式：</p>
<p>$$W = W - \alpha \frac{dW}{\sqrt{SdW+\epsilon}}$$</p>
<p>$$b = b - \alpha \frac{db}{\sqrt{Sdb+\epsilon}}$$</p>
<p>其中，$\epsilon$ 是常数，一般取 1e-7，主要作用是防止分母为零。</p>
<p>AdaGrad 的 Python 示例代码为：</p>
<pre><code>dW = compute_gradient(W)
db = compute_gradient(b)
dW_squared += dW*dW
db_squared += db*db
W -= alpha*dW/(np.sqrt(dW_squared)+1e-7)
b -= alpha*db/(np.sqrt(db_squared)+1e-7)
</code></pre>
<h3 id="rmsprop">RMSprop</h3>
<p>RMSprop 是 Geoff Hinton 提出的一种自适应学习率方法。AdaGrad 会累加之前所有的梯度平方，而 RMSprop 仅仅是计算对应的平均值，因此可缓解 AdaGrad 算法学习率下降较快的问题。 每次迭代训练过程中，其权重 W 和常数项 b 的更新表达式为：</p>
<p>$$S_{dW}=\beta S_{dW}+(1-\beta)dW^2$$</p>
<p>$$S_{db}=\beta S_{db}+(1-\beta)db^2$$</p>
<p>$$W=W-\alpha \frac{dW}{\sqrt{S_{dW}+\epsilon}}$$</p>
<p>$$b=b-\alpha \frac{db}{\sqrt{S_{db}+\epsilon}}$$</p>
<p>下面简单解释一下 RMSprop 算法的原理，如下图所示，令水平方向为 W 的方向，垂直方向为 b 的方向。</p>
<p><img src="https://images.gitbook.cn/11c1cbe0-a76c-11e8-9a80-ff5f9b540635" alt="enter image description here" /></p>
<p>从图中蓝色折线可以明显看出，水平方向振荡较小，而垂直方向振荡较大，也就是说 db 要比 dW 大。在 W 和 b 的更新公式里，由于分母的存在，会消除彼此的这种差异性，从而减小振荡，实现快速梯度下降算法，其梯度下降过程如绿色折线所示。总得来说，就是如果哪个方向振荡大，就减小该方向的更新速度。</p>
<p>SGD、Momentum GD、RMSprop 的实际训练效果对比结果如下图所示：</p>
<p><img src="https://images.gitbook.cn/de889640-a76c-11e8-b38e-d3cdf982a441" alt="enter image description here" /></p>
<p>RMSprop 相应的 Python 示例代码为：</p>
<pre><code>dW = compute_gradient(W)
db = compute_gradient(b)
Sdw = beta*Sdw + (1-beta)*dW*dW
Sdb = beta*Sdb + (1-beta)*db*db
W -= alpha*dW / (np.sqrt(Sdw)+1e-7)
b -= alpha*db / (np.sqrt(Sdb)+1e-7)
</code></pre>
<h3 id="adam">Adam</h3>
<p>Adam（Adaptive Moment Estimation） 是另一种自适应学习率的方法。它利用梯度的一阶矩估计和二阶矩估计动态调整每个参数的学习率。Adam 的优点主要在于经过偏置校正后，每一次迭代学习率都有个确定范围，使得参数比较平稳。相应的公式如下：</p>
<p>$$V_{dW}=\beta_1V_{dW}+(1-\beta_1)dW,\ V_{db}=\beta_1V_{db}+(1-\beta_1)db$$</p>
<p>$$S_{dW}=\beta_2S_{dW}+(1-\beta_2)dW^2,\ S_{db}=\beta_2S_{db}+(1-\beta_2)db^2$$</p>
<p>$$V_{dW}^{corrected}=\frac{V_{dW}}{1-\beta_1^t},\ V_{db}^{corrected}=\frac{V_{db}}{1-\beta_1^t}$$</p>
<p>$$S_{dW}^{corrected}=\frac{S_{dW}}{1-\beta_2^t},\ S_{db}^{corrected}=\frac{S_{db}}{1-\beta_2^t}$$</p>
<p>$$W:=W-\alpha\frac{V_{dW}^{corrected}}{\sqrt{S_{dW}^{corrected}+\varepsilon}},\ b:=b-\alpha\frac{V_{db}^{corrected}}{\sqrt{S_{db}^{corrected}+\varepsilon}}$$</p>
<p>其中，t 是当前迭代次数。Adam 算法包含了几个超参数，分别是：$\alpha、\beta_1、\beta_2、\varepsilon$。其中，$\beta_1$ 通常设置为0.9，$\beta_2$ 通常设置为0.999，$\varepsilon$ 通常设置为$10^{-7}$。一般只需要对 $\beta_1$ 和 $\beta_2$ 进行调试。</p>
<p>实际应用中，Adam 算法结合了动量梯度下降和 RMSprop 各自的优点，使得神经网络训练速度大大提高。</p>
<p>SGD、Momentum GD、RMSprop、Adam 的实际训练效果对比结果如下图所示：</p>
<p><img src="https://images.gitbook.cn/044497a0-a770-11e8-8e69-83a537438da3" alt="enter image description here" /></p>
<p>Adam 相应的 Python 示例代码为：</p>
<pre><code>dW = compute_gradient(W)
db = compute_gradient(b)
Vdw = beta1*Vdw + (1-beat1)*dW
Vdb = beta1*Vdb + (1-beta1)*db
Sdw = beta2*Sdw + (1-beta2)*dW*dW
Sdb = beta2*Sdb + (1-beta2)*db*db
Vdw_corrected = Vdw / (1 - beta1**t)
Vdb_corrected = Vdb / (1 - beta1**t)
Sdw_corrected = Sdw / (1 - beta2**t)
Sdb_corrected = Sdb / (1 - beta2**t)
W -= alpha*Vdw_corrected / np.sqrt(Sdw_corrected+1e-7)
b -= alpha*Vdb_corrected / np.sqrt(Sdb_corrected+1e-7)
</code></pre>
<h3 id="">降低学习因子</h3>
<p>学习因子 $\alpha$ 决定了梯度下降每次更新参数的尺度大小，俗称步进长度。学习因子过大或过小，都会严重影响神经网络的训练效果。</p>
<p><img src="https://images.gitbook.cn/b0247610-a772-11e8-8e69-83a537438da3" alt="enter image description here" /></p>
<p>那么，如何选择合适的学习因子呢？在神经网络整个训练过程中，使用固定大小的学习因子往往效果不好，一般的原则是随着迭代次数增加，学习因子 $\alpha$ 应该逐渐减小。这种方法被称为 Learning Rate Decay。</p>
<p>下面讨论一下使用 Learning Rate Decay 的原因。如下图所示，蓝色折线表示使用恒定的学习因子 $\alpha$，由于每次训练 $\alpha$ 相同，在接近最优值处的振荡也大，在最优值附近较大范围内振荡，与最优值距离比较远。绿色折线表示使用不断减小的 $\alpha$，随着训练次数增加， $\alpha$ 逐渐减小，步进长度减小，使得能够在最优值处较小范围内微弱振荡，不断逼近最优值。</p>
<p><img src="https://images.gitbook.cn/45e8c340-a773-11e8-b38e-d3cdf982a441" alt="enter image description here" /></p>
<p>Learning Rate Decay 有两种常用形式，第一种是 Exponential Decay，相应的表达式如下所示：</p>
<p>$$\alpha=\alpha_0e^{-kt}$$</p>
<p>其中，k 为可调参数，t 为当前迭代次数。学习因子 $\alpha$ 呈指数衰减。</p>
<p>第二种是 1/t Decay，相应的表达式如下所示：</p>
<p>$$\alpha=\alpha_0/(1+kt)$$</p>
<p>其中，k 为可调参数，t 为当前迭代次数。</p>
<p>使用 Learning Rate Decay，损失函数 Loss 的趋势变化情况与下图所示近似：</p>
<p><img src="https://images.gitbook.cn/8a3404f0-a774-11e8-bd23-ab73edb1c5ff" alt="enter image description here" /></p>
<h3 id="-1">总结</h3>
<p>本文主要介绍了神经网络中几种常见的梯度下降优化算法，包括 <code>Mini-Batch</code>、Momentum、Nesterov Momentum、AdaGrad、RMSprop、Adam、Learning Rate Decay ，并对各自特点进行了说明和对比。实际应用中应该根据具体情况选择合适的优化算法。</p>
<h3 id="-2">参考文献：</h3>
<ul>
<li>斯坦福 CS231n 课程</li>
</ul></div></article>