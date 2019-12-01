---
title: 机器学习极简入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="yabx">y = a + bx 的目标函数</h3>
<p>上一篇文章，我们解释了线性，本文我们回到求解线性回归目标函数的问题上。前面已知，线性回归的<strong>目标函数</strong>为：</p>
<p>$J(a,b) = \frac{1}{2m}\sum_{i=1}^{m}(a + bx^{(i)} - y^{(i)})^2$</p>
<p>J(a,b) 是一个二元函数。我们要求的是：两个参数 a 和 b 的值。要满足的条件是：a 和 b 取这个值的时候，J(a,b) 的值达到最小。</p>
<p>我们现在就来用之前讲过的算法：梯度下降法，来对其进行求解。</p>
<h3 id="">斜率、导数和偏微分</h3>
<p>梯度下降法我们前面也讲过步骤，<strong>总结</strong>起来就是：从任意点开始，在该点对目标函数求导，沿着导数方向（梯度）“走”（下降）一个给定步长，如此循环迭代，直至“走”到导数为0的位置，则达到极小值。</p>
<p>为什么要求导呢？从下图可以看到：曲线表示一个函数，它在一个点处的导数值就是经过这个点的函数曲线切线的斜率。</p>
<p><img src="http://images.gitbook.cn/83e1ab10-3731-11e8-9e5f-49e3de6d39b3" alt="enter image description here" /></p>
<p><strong>导数</strong>表现的是函数 f(x) 在 x 轴上某一点 $x_0$ 处，沿着 x 轴正方向的变化率/变化趋势，记作 $f’(x_0)$。</p>
<p>在 x 轴上某一点处，如果 $f’(x_0)&gt;0$ ，说明 f(x) 的函数值在 $x_0$ 点沿 x 轴正方向是趋于增加的；如果 $f’(x_0)&lt;0$，说明 f(x) 的函数值在 $x_0$ 点沿 x 轴正方向是趋于减少的。</p>
<p>一元函数在某一点处沿 x 轴正方向的变化率称为导数。但如果是二元或更多元的函数（自变量维度 &gt;=2），则某一点处沿某一维度坐标轴正方向的变化率称为<strong>偏导数</strong>。</p>
<p>导数/偏导数表现的是变化率，而变化本身，用另一个概念来表示，这个概念就是<strong>微分</strong>（对应偏导数，二元及以上函数有<strong>偏微分</strong>）。</p>
<p><strong>（偏）导数</strong>是针对函数上的一个点而言的，<strong>是一个值</strong>。而<strong>（偏）微分</strong>则<strong>是一个函数</strong>，其中的每个点表达的是原函数上各点沿着（偏）导数方向的变化。</p>
<p>直观而不严格的来说，（偏）微分就是沿着（偏）导数的方向，产生了一个无穷小的增量。</p>
<p>想想我们的梯度下降算法，我们要做的不就是在一个个点上（沿着导数方向）向前走一小步吗？</p>
<p><strong>当我们求出了一个函数的（偏）微分函数后，将某个变量带入其中，得出的（偏）微分函数对应的函数值，就是原函数在该点处，对该自变量求导的导数值。</strong></p>
<p>所以，只要我们求出了目标函数的（偏）微分函数，那么目标函数自变量值域内每一点的导数值也就都可以求了。</p>
<p>如何求一个函数的（偏）微分函数呢？这个我们只需要记住最基本的求导规则就好，函数（整体，而非在一个点处）求导的结果，就是微分函数了。</p>
<p>本文会用到的仅仅是常用规则中最常用的几条：</p>
<blockquote>
  <ol>
  <li>常数的导数是零：(c)' = 0；</li>
  <li>x 的 n 次幂的导数是 n 倍的 x 的 n-1 次幂：$(x^n)' = nx^{n-1}$；</li>
  <li>对常数乘以函数求导，结果等于该常数乘以函数的导数：(cf)' = cf'；</li>
  <li>两个函数 f 和 g 的和的导数为：(f+g)' = f' + g'；</li>
  <li>两个函数 f 和 g 的积的导数为：(fg)' = f'g + fg'。</li>
  </ol>
</blockquote>
<h3 id="-1">梯度下降求解目标函数</h3>
<p>对于 J(a,b) 而言，有两个参数 a 和 b，函数 J 分别对自变量 a 和 b 取偏微分的结果是：</p>
<p>$ \frac{\partial{J(a,b)}}{\partial{a}} = \frac{1}{(m)}\sum_{i=1}^{m}((a+bx^{(i)}) - y^{(i)}) $</p>
<p>$ \frac{\partial{J(a,b)}}{\partial{b}} = \frac{1}{(m)}\sum_{i=1}^{m}x^{(i)}((a+bx^{(i)}) - y^{(i)}) $</p>
<p>所以我们要做得是：</p>
<p>Step 1：任意给定 a 和 b 的初值。</p>
<blockquote>
  <p>a = 0; b = 0;</p>
</blockquote>
<p>Step 2：用梯度下降法求解 a 和 b，伪代码如下：</p>
<p>$  repeat \,\, until\,\,  convergence \{ $ 
$  \\    \hspace{1cm} a = a - \alpha  \frac{\partial{J(a,b)}}{\partial{a}} $</p>
<p>$      \hspace{1cm} b = b - \alpha  \frac{\partial{J(a,b)}}{\partial{b}} $<br />
$  \}$</p>
<p>当下降的高度小于某个指定的阈值（近似收敛至最优结果），则停止下降。</p>
<p>将上面展开的式子带入上面的代码，就是：</p>
<p>$  repeat \,\, until\,\, convergence \{ $<br />
$   \hspace{1cm}sumA = 0 $</p>
<p>$   \hspace{1cm}sumB = 0 $</p>
<p>$  \hspace{1cm}for\,\, i = 1\,\, to\,\, m \{$
$ \\  \hspace{2cm}sumA = sumA +  (a+bx^{(i)} - y^{(i)}) $
$  \hspace{2cm}sumB = sumB + x^{(i)}(a+bx^{(i)} - y^{(i)}) $
$  \hspace{1cm}\} $</p>
<p>$   \hspace{1cm}a = a - \alpha \frac{sumA}{m} $</p>
<p>$  \hspace{1cm} b = b - \alpha \frac{sumB}{m}  $</p>
<p>$  \}$</p>
<h3 id="-2">通用线性回归模型的目标函数求解</h3>
<p>y = a + bx 是一个线性回归模型，这个没问题。不过，反过来，线性回归模型只能是 y = a + bx 的形式吗？当然不是。</p>
<p>y = a + bx =&gt; f(x) = a + bx 实际上是线性回归模型的一个特例——自变量只有一个维度的特例，在这个模型中，自变量 x 是一个一维向量，可写作 [x]。</p>
<p>通用的线性回归模型，是接受 n 维自变量的，也就是说自变量可以写作 $[x_1, x_2, ..., x_n]$ 形式。于是，相应的模型函数写出来就是这样的：</p>
<p>$f(x_1, x_2, ..., x_n) = a + b_1 x_1 + b_2  x_2 + ... + b_n  x_n$</p>
<p>这样写参数有点混乱，我们用 $\theta_0 $ 来代替 a， 用 $\theta_1 $ 到 $\theta_n$ 来代替 $b_1$ 到 $b_n$，那么写出来就是这样的：</p>
<p>$f(1, x_1, x_2, ..., x_n) = \theta_0 + \theta_1 x_1 + \theta_2  x_2 + ... + \theta_n x_n$</p>
<p>我们设 $x_0 = 1$, 因此：</p>
<p>$f(x_0, x_1, x_2, ..., x_n) = \theta_0  x_0 + \theta_1  x_1 + \theta_2 x_2 + ... + \theta_n  x_n$</p>
<p>那么对应的，n 维自变量的线性回归模型对应的目标函数就是：</p>
<p>$  J(\theta_0,\theta_1, ..., \theta_n) = \frac{1}{(2m)}\sum_{i=1}^{m} (y'^{(i)}-y^{(i)})^{2} = \frac{1}{(2m)}\sum_{i=1}^{m}(\theta_0+\theta_1x_1^{(i)}+\theta_2x_2^{(i)} + ... + \theta_n x_n^{(i)} -y^{(i)})^{2}   $</p>
<p>再设：</p>
<p>$X=[x_0, x_1, x_2, ..., x_n] ，\Theta = [\theta_0, \theta_1, \theta_2, ..., \theta_n]$</p>
<p>然后将模型函数简写成：</p>
<p>$f(X) = \Theta^{T}  X$</p>
<p>根据习惯，我们在这里将 f(X) 写作 h(X)，因此，模型函数就成了：</p>
<p>$h(X) = \Theta^{T} X$</p>
<p>相应的目标函数就是：</p>
<p>$ J(\Theta) = \frac{1}{(2m)}\sum_{i=1}^{m}(h_\theta(X^{(i)})-y^{(i)})^{2}  $</p>
<p>同样应用梯度下降，实现的过程是：</p>
<p>$  repeat\,\, until\,\, convergence \{ $
$  \\    \hspace{1cm} \Theta \:= \Theta - \alpha  \frac{\partial{J(\Theta)}}{\partial{\Theta}} $<br />
$  \}$</p>
<p>细化为针对 theta_j 的形式就是：</p>
<p>$  repeat\,\, until\,\, convergence \{  $</p>
<p>$ \hspace{1cm}  for\,\, j = 1\,\, to\,\, n \{ $</p>
<p>$  \hspace{2cm} sum_j = 0 $</p>
<p>$ \hspace{2cm}for\,\, i = 1\,\, to\,\, m\{ $</p>
<p>$  \hspace{3cm}sum_j = sum_j +  (\theta_0 +\theta_1x_1^{(i)}+\theta_2x_2^{(i)}  + ... + \theta_nx_n^{(i)} -y^{(i)})x_j^{(i)}  $</p>
<p>$ \hspace{2cm}\}$</p>
<p>$  \hspace{2cm} \theta_j \:= \theta_j - \alpha  \frac{sum_j}{m} $</p>
<p>$  \hspace{1cm}\}     $</p>
<p>$  \}$</p>
<p>这就是梯度下降的通用形式。</p>
<h3 id="-3">线性回归的超参数</h3>
<p>作为一个线性回归模型，本身的参数是 $\Theta$，在开始训练之前，$\Theta$（无论是多少维），具体的数值都不知道，训练过程就是求解 $\Theta$ 中各维度数值的过程。</p>
<p>当我们使用梯度下降求解时，梯度下降算法中的步长参数：$\alpha$，就是训练线性回归模型的超参数。</p>
<p>训练程序通过梯度下降的计算，自动求出了 $\Theta$ 的值。而 $\alpha$ 却是无法求解的，必须手工指定。反之，如果没有指定 $\alpha$，梯度下降运算则根本无法进行。</p>
<ul>
<li>对于线性回归而言，<strong>只要用到梯度下降，就会有步长参数 alpha 这个超参数</strong>。</li>
</ul>
<p>如果训练结果偏差较大，可以尝试调小步长；如果模型质量不错但是训练效率太低，可以适当放大步长；也可以尝试使用动态步长，开始步长较大，随着梯度的缩小，步长同样缩小……</p>
<ul>
<li><p>如果训练程序是通过人工指定迭代次数来确定退出条件，则迭代次数也是一个超参数。</p></li>
<li><p>如果训练程序以模型结果与真实结果的整体差值小于某一个阈值为退出条件，则这个阈值就是超参数。</p></li>
</ul>
<p>在模型类型和训练数据确定的情况下，超参数的设置就成了影响模型最终质量的关键。</p>
<p>而往往一个模型会涉及多个超参数，如何制定策略在最少尝试的情况下让所有超参数设置的结果达到最佳，是一个在实践中非常重要又没有统一方法可以解决的问题。</p>
<p>在实际应用中，能够在调参方面有章法，而不是乱试一气，就有赖于大家对于模型原理和数据的掌握了。</p>
<h3 id="-4">编写线性回归训练/预测程序</h3>
<p>如果我们要用代码实现线性回归程序应该怎样做呢？当然，你可以按照上面的描述，自己从头用代码实现一遍。</p>
<p>不过，其实不必。因为我们已经有很多现成的方法库，可以直接调用了。</p>
<p>最常见的是 sklearn 库。下面的例子就对应最开始的经验和工资的问题。我们用前 7 个数据作为训练集，后面 4 个作为测试集，来看看结果：</p>
<pre><code>    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn import datasets, linear_model
    from sklearn.metrics import mean_squared_error, r2_score

    experiences = np.array([0,1,2,3,4,5,6,7,8,9,10])
    salaries = np.array([103100, 104900, 106800, 108700, 110400, 112300, 114200, 116100, 117800, 119700, 121600])

    # 将特征数据集分为训练集和测试集，除了最后 4 个作为测试用例，其他都用于训练
    X_train = experiences[:7]
    X_train = X_train.reshape(-1,1)
    X_test = experiences[7:]
    X_test = X_test.reshape(-1,1)

    # 把目标数据（特征对应的真实值）也分为训练集和测试集
    y_train = salaries[:7]
    y_test = salaries[7:]

    # 创建线性回归模型
    regr = linear_model.LinearRegression()

    # 用训练集训练模型——看就这么简单，一行搞定训练过程
    regr.fit(X_train, y_train)

    # 用训练得出的模型进行预测
    diabetes_y_pred = regr.predict(X_test)

    # 将测试结果以图标的方式显示出来
    plt.scatter(X_test, y_test,  color='black')
    plt.plot(X_test, diabetes_y_pred, color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()
</code></pre>
<p>最终结果是这个样子的：</p>
<p><img src="http://images.gitbook.cn/e234b7d0-37ee-11e8-9e5a-4da5a3d2cb23" alt="enter image description here" /></p></div></article>