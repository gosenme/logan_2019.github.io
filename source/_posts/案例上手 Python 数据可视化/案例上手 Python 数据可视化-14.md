---
title: 案例上手 Python 数据可视化-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课将继续介绍 Seaborn 中的统计图。一定要牢记，Seaborn 是对 Matplotlib 的高级封装，它优化了很多古老的做图过程，因此才会看到一个函数解决问题的局面。</p>
<h3 id="241">2.4.1 数据分布统计图</h3>
<p>在统计学中，研究数据的分布情况，也是一个重要的工作，比如某些数据是否为正态分布——某些机器学习模型很在意数据的分布情况。</p>
<p>在 Matplotlib 中，可以通过绘制直方图将数据的分布情况可视化。在 Seaborn 中，也提供了绘制直方图的函数。</p>
<pre><code class="python language-python">%matplotlib inline
import seaborn as sns
import numpy as np
sns.set()
np.random.seed(0)
x = np.random.randn(100)
ax = sns.distplot(x)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/339865e0-3e42-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>sns.distplot 函数即实现了直方图，还顺带把曲线画出来了——曲线其实代表了 KDE。</p>
<pre><code class="python language-python">seaborn.distplot(a, bins=None, hist=True, kde=True, rug=False, fit=None, hist_kws=None, kde_kws=None, rug_kws=None, fit_kws=None, color=None, vertical=False, norm_hist=False, axlabel=None, label=None, ax=None)
</code></pre>
<p>除了 sns.distplot 之外，在 Seaborn 中还有另外一个常用的绘制数据分布的函数 sns.kdeplot，它们的使用方法类似。</p>
<h3 id="242">2.4.2 联合统计图</h3>
<p>首先看这样一个示例。</p>
<pre><code class="python language-python">sns.set(rc={'axes.facecolor':'cornflowerblue', 'figure.facecolor':'cornflowerblue'})    #①
tips = sns.load_dataset("tips")
jg = sns.JointGrid(x='total_bill', y='tip', data=tips)    #②
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/593044d0-3e42-11e9-acbf-6f04514d907d" width = "50%" /></p>
<p>① 的作用是设置所得图示的背景颜色，这样做的目的是让下面的 ② 绘制的图像显示更清晰，如果不设置 ①，在显示的图示中看到的就是白底图像，有的部分看不出来。</p>
<p>② 最终得到的是坐标网格，而且在图中分为三部分，如下图所示。</p>
<p><img src="https://images.gitbook.cn/a3c26320-3e42-11e9-a98d-5dc2d0f56a42" width = "50%" /></p>
<p>相对于以往的坐标网格，多出了 B 和 C 两个部分。也就是说，不仅可以在 A 部分绘制某种统计图，在 B 和 C 部分也可以绘制。</p>
<p>继续操作：</p>
<pre><code class="python language-python">jg = sns.JointGrid(x='total_bill', y='tip', data=tips)
jg.plot(sns.regplot, sns.distplot)    #③
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/bce83910-3e42-11e9-a98d-5dc2d0f56a42" width = "50%" /></p>
<p>语句 ③ 实现了在坐标网格中绘制统计图的效果，jp.plot 方法以两个绘图函数为参数，分别在 A 部分绘制了回归统计图，在 B 和 C 部分绘制了直方图，而且直方图分别表示了对应坐标轴数据的分布，即：</p>
<ul>
<li>A 部分表示的是两个特征之间的关系；</li>
<li>B 和 C 部分分别表示某一个特征的数据分布。</li>
</ul>
<p>我们把有语句 ② 和 ③ 共同实现的统计图，称为联合统计图。除了用 ② ③ 两句可以绘制这种图之外，还有一个函数也能够“两步并作一步”，具体如下：</p>
<pre><code class="python language-python">seaborn.jointplot(x, y, data=None, kind='scatter', stat_func=None, color=None, height=6, ratio=5, space=0.2, dropna=True, xlim=None, ylim=None, joint_kws=None, marginal_kws=None, annot_kws=None, **kwargs)
</code></pre>
<blockquote>
  <p>注意，参数 kind 的取值只能是“scatter”、“reg”、“resid”、“kde”、“hex”中的一个，这就规定了在 A 区中所显示的统计图的种类。</p>
</blockquote>
<pre><code class="python language-python">sns.set()
sns.jointplot(x="total_bill", y="tip", kind='reg', data=tips)    #④
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f31e8ca0-3e42-11e9-a98d-5dc2d0f56a42" width = "50%" /></p>
<p>④ 的结果与前述 ② 和 ③ 的结果一样——只是因为 sns.set()，背景发生了变化。</p>
<h3 id="243">2.4.3 坐标网格关系图</h3>
<p>对于一个数据集中，通常有多个特征，此时会有一种需要，研究一下任何两个特征之间的关系——是否相关、是否线性相关等。如果根据排列组合方式，两两特征绘图，未免太麻烦了。Seaborn 中有一个函数，可以直接生成两两特征关系图。</p>
<pre><code class="python language-python">seaborn.pairplot(data, hue=None, hue_order=None, palette=None, vars=None, x_vars=None, y_vars=None, kind='scatter', diag_kind='auto', markers=None, height=2.5, aspect=1, dropna=True, plot_kws=None, diag_kws=None, grid_kws=None, size=None)
</code></pre>
<p>其中参数 kind 表示可以绘制的关系图类型，默认为 'scatter'，还可以选择 'reg'——回归统计图。</p>
<pre><code class="python language-python">sns.set(style='ticks')
iris = sns.load_dataset("iris")
sns.pairplot(iris)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1e8b7e20-3e43-11e9-a7c2-ef0a2addb332" width = "50%" /></p>
<p>参数 hue，意思是许可引入另外一个维度，在 iris 数据集中，有名为 species 的特征，标记了每个记录是什么种类的鸢尾花。</p>
<pre><code class="python language-python">sns.pairplot(iris, hue='species')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5cc1da90-3e43-11e9-a7c2-ef0a2addb332" width = "50%" /></p>
<p>其他参数，读者可以自行尝试，基本使用方法跟以往遇到过的函数类似。</p>
<h3 id="244">2.4.4 热图</h3>
<p>热图是通过色彩变化来显示的数据。例如：</p>
<pre><code class="python language-python">data = np.random.rand(10, 12)
sns.heatmap(data)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/8180bea0-3e43-11e9-a7c2-ef0a2addb332" width = "50%" /></p>
<p>绘制热图的函数完整形式是：</p>
<pre><code class="python language-python">seaborn.heatmap(data, vmin=None, vmax=None, cmap=None, center=None, robust=False, annot=None, fmt='.2g', annot_kws=None, linewidths=0, linecolor='white', cbar=True, cbar_kws=None, cbar_ax=None, square=False, xticklabels='auto', yticklabels='auto', mask=None, ax=None, **kwargs)
</code></pre>
<p>除了此类热图，还有一种能够表示分层聚类的热图。</p>
<pre><code class="python language-python">species = iris.pop("species")
sns.clustermap(iris)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/95302750-3e44-11e9-9475-090a8c8aed3a" width = "50%" /></p>
<p>sns.clustermap 的完整形式是：</p>
<pre><code class="python language-python">seaborn.clustermap(data, pivot_kws=None, method='average', metric='euclidean', z_score=None, standard_scale=None, figsize=None, cbar_kws=None, row_cluster=True, col_cluster=True, row_linkage=None, col_linkage=None, row_colors=None, col_colors=None, mask=None, **kwargs)
</code></pre>
<p>对于此处的两个绘制热图的函数，如果要深入了解，建议阅读官方文档中对各个参数项的说明。此处仅以上述两个示例简要演示，在后续的学习内容中，还会遇到热图，只不过是用另外的方式绘制。</p>
<p>Seaborn 中的函数还有很多，不仅仅达人课所介绍的这些，此处重点在于理解最基本的方法。在官方网站中，对各种 API 都有完善的说明，因此，当学完本达人课的基础知识之后，就要结合具体项目实践，并且使用官方文档，才能全面而深入地掌握 Seaborn 更多技能。</p>
<h3 id="">总结</h3>
<p>本课依次介绍了如下内容：</p>
<ul>
<li>数据分布图，sns.distplot</li>
<li>联合统计图，sns.JointGrid、jg.plot、sns.jointplot</li>
<li>坐标网格关系图，sns.pairplot</li>
<li>热图，sns.heatmap</li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>