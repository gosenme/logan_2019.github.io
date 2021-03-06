---
title: 案例上手 Python 数据可视化-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课将要介绍的关系图和回归图，与上一课中的分类特征统计图的不同之处在于，这两类图的目的是发现 X 和 Y 轴两个变量之间的可能关系。</p>
<h3 id="231">2.3.1 关系统计图</h3>
<p>如果要研究两个变量之间的可能函数关系，依据以往的经验，可以通过散点图进行探索——注意，这里所说的散点图，与上一课提到的“分类特征的散点图”是不同的。</p>
<p>还是看示例，来理解此处的散点图。</p>
<pre><code class="python language-python">%matplotlib inline
import seaborn as sns
sns.set(style='ticks')
tips = sns.load_dataset("tips")
tips.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FgXF6f6srrAhe00wpL0M5_qsynPf" alt="avatar" /></p>
<p>继续使用 tips 数据集。从结果中可以看到，特征 total_bill 和 tip 中的数值，都是浮点数（连续值），下面就分别以它们为坐标系的两个坐标轴，绘制散点图，试图找到这两个特征之间的关系——这就是“关系统计图”的目的。</p>
<pre><code class="python language-python">sns.relplot(x='total_bill', y='tip', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/799311d0-3e2e-11e9-acbf-6f04514d907d" alt="enter image description here" /></p>
<p>使用 sns.relplot 函数，所得到的图示与以往绘制散点图的效果差不多，如果看看这个函数完整参数列表，就能发现惊奇。</p>
<pre><code class="python language-python">seaborn.relplot(x=None, y=None, hue=None, size=None, style=None, data=None, row=None, col=None, col_wrap=None, row_order=None, col_order=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, markers=None, dashes=None, style_order=None, legend='brief', kind='scatter', height=5, aspect=1, facet_kws=None, **kwargs)
</code></pre>
<p>上一课学习了 sns.catplot 函数，此处 sns.relpot 的参数与之类似，只有很小的差异。</p>
<p>在 sns.relplot 的参数中，除了 x, y 两个参数之外，同样也有 hue，它与以往的含义一样。</p>
<pre><code class="python language-python">sns.relplot(x='total_bill', y='tip', hue='sex', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/ea74d0e0-3e2f-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>以 hue='sex'，在散点图中把 sex 特征所对应的数据区别开了。</p>
<p>此外，还有一个很熟悉的参数 kind，默认值是 'scatter'，就意味着默认是绘制散点图。除了这个值之外，还可以是别的值——类似 sns.catplot 中的 kind。</p>
<ul>
<li>kind='scatter'，默认值，等同函数 sns.scatterplot()。</li>
<li>kind='line'，等同函数 lineplot()。</li>
</ul>
<p>对应着参数 kind 不同的值，分别也有相应专有函数的情况。仍然与 sns.catplot 类似，相对于各个专用函数，sns.relplot 的优势还是在于绘制分区坐标图。</p>
<pre><code class="python language-python">g = sns.relplot(x="total_bill", y="tip", hue="time", 
                size="size", palette=["b", "r"], sizes=(10, 100), col="time", data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6607cb90-3e30-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>除了显示分区坐标系之外，还顺便对其他几个参数做了设置，请根据效果理解上述代码中的参数。</p>
<p>下面，还是按照原来的套路，通过对专有函数的介绍来进一步理解“关系统计图”的绘制。</p>
<p><strong>1. sns.scatterplot</strong></p>
<p>此函数的完整形式如下：</p>
<pre><code class="python language-python">seaborn.scatterplot(x=None, y=None, hue=None, style=None, size=None, data=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, markers=True, style_order=None, x_bins=None, y_bins=None, units=None, estimator=None, ci=95, n_boot=1000, alpha='auto', x_jitter=None, y_jitter=None, legend='brief', ax=None, **kwargs)
</code></pre>
<p>很多参数都是熟悉的了，这里不再一一解释了，下面通过举例了解其含义。</p>
<pre><code class="python language-python">ax = sns.scatterplot(x="total_bill", y="tip", hue="day", style="time", data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/96ed09a0-3e30-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>从效果上看，其实通过 style='time' 又引入了一个维度，即用不同的散点形状表示 time 特征下的数据。</p>
<p>此外，参数 size 可以用于设置点的大小。如果将它指定为某个分类特征，那么也就相当于用散点的大小表示了该特征不同值，相当于又在坐标系中叠加了一个维度。</p>
<pre><code class="python language-python">sns.scatterplot(x='total_bill', y='tip', hue='day', size='smoker', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b88b25b0-3e30-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>并且，参数 sizes（注意写法，是复数形式了）能够规定参数 size 中划分的不同特征的“散点”大小。</p>
<pre><code class="python language-python">sns.scatterplot(x='total_bill', y='tip', hue='day', 
                size='smoker', sizes=(50, 150), data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d3cbc550-3e30-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<p>了解了 sns.scatterplot 的使用方法之后，再研习 sns.relplot 的参数 kind='line' 时的等同函数 sns.lineplot。</p>
<p><strong>2. sns.lineplot</strong></p>
<p>用这个函数，能够根据 x 轴和 y 轴的数值，直接画出反映了两个变量关系的曲线。</p>
<pre><code class="python language-python">sns.lineplot(x='total_bill', y='tip', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/27164000-3e31-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<p>很显然，tips 中的这两个特征的数据，不适合用这种方式呈现它们的关系——这点请特别注意，什么数据用什么图像表示，是有讲究的，不能乱来。</p>
<pre><code class="python language-python">fmri = sns.load_dataset("fmri")
fmri.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FuV4LlMpiDmw4vArTm7VaFEKcPii" alt="avatar" /></p>
<p>换一个数据集，使用 fmri 引用的数据集中的 timepoint 和 signal 两个连续特征的数据。</p>
<pre><code class="python language-python">sns.lineplot(x="timepoint", y="signal", data=fmri)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5d6d6c90-3e32-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>用 sns.lineplot 绘制的图，并不是一条“线”，严格地说，是一条“带”，在曲线（图中实线）两侧还有一个范围，这是告诉我们，数据点基本上落在了这个区域，如果要抽象为一个函数，其曲线大致在这个范围内。这其实是自动完成了线性拟合。</p>
<p>可以看一下散点图，对比之后，就理解上图表示的“可能规律”含义。</p>
<pre><code class="python language-python">sns.scatterplot(x='timepoint', y='signal', data=fmri)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7d07a250-3e32-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>两者比较，不难发现，“带”状图比下面的散点图更抽象，更趋向于把数据之间的关系表达了出来——这也就是 sns.lineplot 相对于 sns.scatterplot 的区别。</p>
<p>照例，依然要呈现此函数的全貌：</p>
<pre><code class="python language-python">seaborn.lineplot(x=None, y=None, hue=None, size=None, style=None, data=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, dashes=True, markers=None, style_order=None, units=None, estimator='mean', ci=95, n_boot=1000, sort=True, err_style='band', err_kws=None, legend='brief', ax=None, **kwargs)
</code></pre>
<p>再演示一个示例，说明几个函数的基本作用，其他更多的函数，应该在用到的时候查看帮助文档了（不要忘记这种反复提及的方法）。</p>
<pre><code class="python language-python">sns.lineplot(x='timepoint', y='signal', data=fmri, 
             hue='event', style='event', markers=True, dashes=False)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9ce067b0-3e32-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>需要特别说明的是参数 err_style，默认值为 'band'，显然这就是得到“带状”的原因，如果像下面一样，显示效果就不同了。</p>
<pre><code class="python language-python">sns.lineplot(x='timepoint', y='signal', data=fmri, 
             hue='event', style='event', markers=True, dashes=False, err_style='bars')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/cf2f6ef0-3e32-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<p>是不是用 sns.lineplot 绘制的图都有“误差”呢？这要看你的数据了。</p>
<pre><code class="python language-python">import numpy as np
X = np.linspace(0, 100, 100)
y = np.sin(X) + np.random.random(100)
sns.lineplot(x=X, y=y)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/ef48e6d0-3e32-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>这就实现了以前绘制曲线图的效果。</p>
<p>总而言之，不论是 sns.relplot，还是两个专有函数 sns.scatterplot 和 sns.lineplot，都是以可视化的方式展示了两个连续变量之间可能存在的关系。</p>
<h3 id="232">2.3.2 回归统计图</h3>
<p>在前面散点图的基础上，并且利用 tips 数据集中的 total_bill 和 tip 两个特征的数据训练了机器学习中的线性回归模型，再将这个模型绘制到散点图中，就可以比较直观地观察到模型表达的规律以及与数据之间的关系。Seaborn 中的回归统计图，就是将上述过程合并起来，一气呵成地完成绘图过程。</p>
<pre><code class="python language-python">sns.lmplot(x='total_bill', y='tip', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/30b87540-3e33-11e9-acbf-6f04514d907d" alt="enter image description here" /></p>
<p>就是这么简单。</p>
<p>除了 sns.lmplot 之外，还有 sns.regplot 函数，也能实现同样的功能（此处演示从略），不过，这两个函数也是有区别的。</p>
<p>找区别的最好方式是看两个函数参数列表：</p>
<pre><code class="python language-python">seaborn.lmplot(x, y, data, hue=None, col=None, row=None, palette=None, col_wrap=None, height=5, aspect=1, markers='o', sharex=True, sharey=True, hue_order=None, col_order=None, row_order=None, legend=True, legend_out=True, x_estimator=None, x_bins=None, x_ci='ci', scatter=True, fit_reg=True, ci=95, n_boot=1000, units=None, order=1, logistic=False, lowess=False, robust=False, logx=False, x_partial=None, y_partial=None, truncate=False, x_jitter=None, y_jitter=None, scatter_kws=None, line_kws=None, size=None)
</code></pre>
<pre><code class="python language-python">seaborn.regplot(x, y, data=None, x_estimator=None, x_bins=None, x_ci='ci', scatter=True, fit_reg=True, ci=95, n_boot=1000, units=None, order=1, logistic=False, lowess=False, robust=False, logx=False, x_partial=None, y_partial=None, truncate=False, dropna=True, x_jitter=None, y_jitter=None, label=None, color=None, marker='o', scatter_kws=None, line_kws=None, ax=None)
</code></pre>
<p>认真比较，不难发现，在 sns.lmplot 中有的几个参数如 hue=None、col=None、row=None、palette=None、col_wrap=None 等，在 sns.regplot 中没有。这说明什么？根据以前学习过的参数特点，不难知晓。</p>
<p>再看 sns.regplot 函数，也有几个属于自己的参数，比如 dropna=True、label=None、color=None、marker='o'。因此，可以认为 sns.regplot 专注于一个坐标系的绘图。</p>
<pre><code class="python language-python">sns.regplot(x='total_bill', y='tip', data=tips, color='g', marker='+')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/fa92a700-3e33-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>不仅仅在于修改图中的某些元素的显示模式，回归还可以适用于非连续的特征。</p>
<pre><code class="python language-python">sns.regplot(x="size", y="total_bill", data=tips, x_jitter=.1)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0f8d97f0-3e34-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>其实，从统计的角度看，这个回归图有一些缺陷，每个分类数据都对应着若干个 y 轴的数据，那么回归的直线是根据这些数据的什么量绘制的呢？为了解决这个疑惑，最好使用下面的方式：</p>
<pre><code class="python language-python">sns.regplot(x='size', y='total_bill', data=tips, x_estimator=np.mean)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/2eb1b350-3e34-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<p>回归线是按照参数 x_estimator=np.mean 所设定的值得到的，并且，图中分别用线段显示出了各个分类的的置信区间。</p>
<p>前面已经说过了，sns.regplot 和 sns.lmplot 是基本相似的，除了提到的那些参数，特别是在 sns.lmplot 中，因为多出来的那些参数，使得它的独特之处在于分区和引入类别维度。</p>
<pre><code class="python language-python">sns.lmplot(x="total_bill", y="tip", hue="smoker", data=tips, markers=["o", "x"])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/59fc76d0-3e34-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>在 sns.lmplot 的参数中，这里使用了 hue='smoker', markers=['o', 'x']，从而实现了从不同分类的数据中得到了各自的回归直线。</p>
<p>进一步，还可以这样做：</p>
<pre><code class="python language-python">sns.lmplot(x="total_bill", y="tip", col="day", hue="day", data=tips, col_wrap=2)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6feb64b0-3e34-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<p>以上就是回归统计图的两个函数使用方法。</p>
<h3 id="">总结</h3>
<p>本课首先学习了关系统计图——通常研究两个连续特征的关系，基本的函数模式依然是有一个一般性的函数 sns.relplot，当然这个函数的参数中要有 kind，根据此参数的不同值，还有专门的函数，分别如下所示：</p>
<ul>
<li>kind='scatter'，默认值，等同函数 sns.scatterplot()</li>
<li>kind='line'，等同函数 lineplot()</li>
</ul>
<p>在关系统计图基础上，研习了回归统计图，这种统计图实现了数据点绘图和回归曲线的结合，常用的是两个功能相似的函数 sns.regplot 和 sns.lmplot——它们的区别，通过参数对比，也是显而易见的。</p>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>