---
title: 案例上手 Python 数据可视化-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一课已经体验到了 Seaborn 相对 Matplotlib 的优势，本课将要介绍的是 Seaborn 对分类数据的统计，也是它的长项。</p>
<p>针对分类数据的统计图，可以使用 sns.catplot 绘制，其完整参数如下：</p>
<pre><code class="python language-python">seaborn.catplot(x=None, y=None, hue=None, data=None, row=None, col=None, col_wrap=None, estimator=&lt;function mean&gt;, ci=95, n_boot=1000, units=None, order=None, hue_order=None, row_order=None, col_order=None, kind='strip', height=5, aspect=1, orient=None, color=None, palette=None, legend=True, legend_out=True, sharex=True, sharey=True, margin_titles=False, facet_kws=None, **kwargs)
</code></pre>
<p>本课使用演绎的方式来学习，首先理解这个函数的基本使用方法，重点是常用参数的含义。</p>
<ul>
<li>x，y，hue：参数 data 所设置的数据集中的特征，其中 hue 是嵌入到坐标系中的分类特征，x, y 分别是数据集中作为横纵轴的特征。</li>
<li>data：一个 DataFrame 对象，即数据集。</li>
<li>row，col：如果要绘制分区坐标系，用这两个参数分别设置了“坐标矩阵”的行列。例如，指定 col 的值为某一个分类特征，就会按照该分类特征数据属性，划分不同坐标系分区。</li>
<li>order，hue_order：字符串组成的列表，指定分类特征显示的顺序。</li>
<li>kind：这个参数很重要，默认值是 'strip'，其他取值还可以是：“point”、“bar”、“swarm”、“box”、“violin”or“boxen”，每个值都对应着一种专门的分类统计图，并且也对应着专有的函数，这是本课要重点阐述的。</li>
<li>palette：设置色彩方案。</li>
</ul>
<p>其他的参数，根据名称也能基本理解。</p>
<p>下面就依据 kind 参数的不同取值，分门别类地介绍各种不同类型的分类统计图。</p>
<h3 id="221">2.2.1 分类特征的散点图</h3>
<ul>
<li>kind = 'strip'，默认值，等同函数 sns.stripplot。</li>
<li>kind = 'swarm'，等同函数 sns.swarmplot。</li>
</ul>
<p>读入数据集：</p>
<pre><code class="python language-python">import seaborn as sns
sns.set(style="whitegrid")

exercise = sns.load_dataset("exercise")
exercise.sample(5)
</code></pre>
<p><img src="https://images.gitbook.cn/Fmqb4VLfZRZIUv54isut_XhzEQ5T" alt="avatar" /></p>
<p>然后用这个数据集制图，看看效果：</p>
<pre><code class="python language-python">%matplotlib inline
sns.catplot(x="time", y="pulse", hue="kind", data=exercise)    #①
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/3d2f2220-3d83-11e9-ab86-d9b554a5bb95" alt="enter image description here" /></p>
<p>毫无疑问，这里绘制的是散点图。但是，该散点图的横坐标是分类特征 time 中的三个值，并且用 hue='kind' 又将分类特征插入到图像中，即用不同颜色的的点代表又一个分类特征 kind 的值，最终得到这些类别组合下每个记录中的 pulse 特征值，并以上述图示表示出来。也可以理解为，x='time', hue='kind' 引入了图中的两个特征维度。</p>
<p>语句 ① 中，就没有特别声明参数 kind 的值，此时是使用默认值 'strip'。</p>
<p>与 ① 等效的还有另外一个对应函数 sns.stripplot。</p>
<pre><code class="python language-python">sns.stripplot(x="time", y="pulse", hue="kind", data=exercise)    #②
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/718013e0-3d83-11e9-ab86-d9b554a5bb95" alt="enter image description here" /></p>
<p>② 与 ① 的效果一样。</p>
<p>不过，在 sns.catplot 中的两个参数 row、col，在类似 sns.stripplot 这样的专有函数中是没有的。因此，下面的图，只有用 sns.catplot 才能简洁直观。</p>
<pre><code class="python language-python">sns.catplot(x='time', y='pulse', hue='kind', col='diet', data=exercise, kind='strip')    #③
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/83ba8540-3d83-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>不过，如果换一个叫角度来说，类似 sns.stripplot 这样的专有函数，表达简单，参数与 sns.catplot 相比，有所精简，使用起来更方便。</p>
<pre><code class="python language-python">seaborn.stripplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, jitter=True, dodge=False, orient=None, color=None, palette=None, size=5, edgecolor='gray', linewidth=0, ax=None, **kwargs)
</code></pre>
<p>仔细比较，sns.catplot 和 sns.stripplot 两者还是稍有区别的，虽然在一般情况下两者是通用的。</p>
<p>因此，不要追求某一个是万能的，各有各的用途，存在即合理。</p>
<p>不过，下面的声明请注意：<strong>如果没有非常的必要，比如绘制分区图，在本课中后续都演示如何使用专有名称的函数。</strong></p>
<h4 id="snsstripplot">sns.stripplot</h4>
<p>前面已经初步解释了这个函数，为了格式完整，这里再重复一下，即 sns.catplot 中参数 kind='strip'。</p>
<p>如果非要将此函数翻译为汉语，可以称之为“条状散点图”。以分类特征为一坐标轴，在另外一个坐标轴上，根据分类特征，将该分类特征数据所在记录中的连续值沿坐标轴描点。</p>
<p>从语句 ② 的结果图中可以看到，这些点虽然纵轴的数值有相同的，但是没有将它们重叠。因此，我们看到的好像是“一束”散点，实际上，所有点的横坐标都应该是相应特征分类数据，也不要把分类特征的值理解为一个范围，分散开仅仅是为了图示的视觉需要。</p>
<pre><code class="python language-python">ax = sns.stripplot(x="time", y="pulse", data=exercise, jitter=0)     #④
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/96b5ae90-3d83-11e9-bdc9-db211f1ca507" alt="enter image description here" /></p>
<p>④ 相对 ② 的图示，在于此时同一纵轴值的都重合了——本来它们的横轴值都是一样的。实现此效果的参数是 jitter=0，它可以表示点的“振动”，如果默认或者 jitter=True，意味着允许描点在某个范围振动——语句 ② 的效果；还可设置为某个 0 到 1 的浮点，表示许可振动的幅度。请对比下面的操作。</p>
<pre><code class="python language-python">ax = sns.stripplot(x="time", y="pulse", data=exercise, jitter=0.05)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/a8fd1840-3d83-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>语句 ② 中使用 hue='kind' 参数向图中提供了另外一个分类特征，但是，如果感觉图有点乱，还可以这样做：</p>
<pre><code class="python language-python">ax = sns.stripplot(x="time", y="pulse", data=exercise, hue='kind', 
                   dodge=True, palette='Set2')    #⑤
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/baa0a0d0-3d83-11e9-bdc9-db211f1ca507" alt="enter image description here" /></p>
<p>dodge=True 的作用就在于将 hue='kind' 所引入的特征数据分开，相对 ② 的效果有很大差异。</p>
<p>并且，在 ⑤ 中还使用了 paletter='Set2' 设置了色彩方案。</p>
<p>sns.stripplot 函数中的其他有关参数，请读者使用帮助文档了解。</p>
<h4 id="snsswarmplot">sns.swarmplot</h4>
<p>此函数即 sns.catplot 的参数 kind='swarm'。</p>
<pre><code class="python language-python">tips = sns.load_dataset("tips")
sns.swarmplot(x="day", y="total_bill", data=tips)
# 下面的语句，与之等效
# sns.catplot(x="day", y="total_bill", kind='swarm', data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d24702b0-3d83-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>再绘制一张简单的图，一遍研究这种图示的本质。</p>
<pre><code class="python language-python">sns.swarmplot(x=tips["total_bill"])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e5032730-3d83-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>此图只使用了一个特征的数据，简化表象，才能探究 sns.swarmplot 的本质。它同样是将该特征中的数据，依据其他特征的连续值在图中描点，并且所有点在默认情况下不彼此重叠——这方面与 sns.stripplot 一样。但是，与之不同的是，这些点不是随机分布的，它们经过调整之后，均匀对称分布在分类特征数值所在直线的两侧，这样能很好地表示数据的分布特点。但是，这种方式不适合“大数据”。</p>
<pre><code class="python language-python">seaborn.swarmplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, dodge=False, orient=None, color=None, palette=None, size=5, edgecolor='gray', linewidth=0, ax=None, **kwargs)
</code></pre>
<p>sns.swarmplot 的参数似乎也没有什么太特殊的。下面使用几个，熟悉一番基本操作。</p>
<p>在分类维度上还可以再引入一个维度，用不同颜色的点表示另外一种类别，即使用 hue 参数来实现。</p>
<pre><code class="python language-python">sns.swarmplot(x="day", y="total_bill", hue="smoker", data=tips, palette="Set2")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/09cf2aa0-3d84-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>这里用 hue = 'smoker' 参数又引入了一个分类特征，在图中用不同颜色来区分。</p>
<p>如果觉得会 smoker 特征的值都混在一起有点乱，还可以使用下面方式把他们分开——老调重弹。</p>
<pre><code class="pythn language-pythn">sns.swarmplot(x="day", y="total_bill", hue="smoker", data=tips, palette="Set2", dodge=True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1cdf3b80-3d84-11e9-ab86-d9b554a5bb95" alt="enter image description here" /></p>
<p>生成此效果的参数就是 dodge=True，它的作用就是当 hue 参数设置了特征之后，将 hue 的特征数据进行分类。</p>
<h3 id="222">2.2.2 分类特征的分布图</h3>
<p>sns.catplot 函数的参数 kind 可以有三个值，都是用于绘制分类的分布图：</p>
<ul>
<li>kind = 'box'，等同函数 sns.boxplot</li>
<li>kind = 'violin'，等同函数 sns.violinplot</li>
<li>kind = 'boxen'，等同函数 sns.boxenplot</li>
</ul>
<p>下面依次对这三个专有函数进行阐述。</p>
<h4 id="snsboxplot">sns.boxplot</h4>
<p>“望文生义”，此函数就是用来绘制箱线图的。我们已经知道，箱线图能够标明某特征中数据的基本分布（描述性统计）。</p>
<pre><code class="python language-python">sns.boxplot(x="day", y="total_bill", hue="smoker", data=tips, palette="Set3")
# 下面的与上面的等效
# sns.catplot(x="day", y="total_bill", hue="smoker", data=tips, kind='box', palette="Set3")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/4cc18880-3d84-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>基本参数跟前面的区别不大。</p>
<p>如果把箱线图和前面的散点图结合起来，或许能有更多维度来观察数据。</p>
<pre><code class="python language-python">ax = sns.boxplot(x="day", y="total_bill", data=tips)
ax = sns.swarmplot(x="day", y="total_bill", data=tips, color=".25")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6075efb0-3d84-11e9-bdc9-db211f1ca507" alt="enter image description here" /></p>
<p>最后，一定要呈现以下函数的完整参数列表。</p>
<pre><code class="python language-python"> seaborn.boxplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, orient=None, color=None, palette=None, saturation=0.75, width=0.8, dodge=True, fliersize=5, linewidth=None, whis=1.5, notch=False, ax=None, **kwargs)
</code></pre>
<h4 id="snsboxenplot">sns.boxenplot</h4>
<p>sns.boxenplot 是 sns.boxplot 的加强版，即 Draw an <strong>enhanced</strong> box plot for larger datasets。</p>
<pre><code class="python language-python">seaborn.boxenplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, orient=None, color=None, palette=None, saturation=0.75, width=0.8, dodge=True, k_depth='proportion', linewidth=None, scale='exponential', outlier_prop=None, ax=None, **kwargs)
</code></pre>
<p>将 sns.boxplot 和 sns.boxenplot 的参数对比，区别不大。</p>
<p>但是，这个函数可以用来应付“大数据”的箱线图——传统箱线图，在处理数据量很大的问题时，会力不从心。</p>
<pre><code class="python language-python">ax = sns.boxenplot(x="day", y="total_bill", data=tips)
ax = sns.stripplot(x="day", y="total_bill", data=tips, size=4, jitter=True, color="gray")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7d956170-3d84-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>因此，当用户绘制箱线图的数据是大数据时（没有绝对标准，你觉得大就大了），就要想到这个增强版的箱线图工具。</p>
<h4 id="snsviolinplot">sns.violinplot</h4>
<p>sns.violinplot 函数所绘制出的图像是以前没有遇到过的，它综合了箱线图和核密度估计，可以称为“提琴图”，其实样子也酷似。</p>
<pre><code class="python language-python">sns.violinplot(x="day", y="total_bill", data=tips)
# 上面的语句与下面的等效
# sns.catplot(x="day", y="total_bill", data=tips, kind='violin')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/93515870-3d84-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>这就是“提琴图”。图中反映的也是数据的分布，跟箱线图有类似的地方，不同地方在于，它的图形与真实的数据量分布对应，即纵坐标某位置数据量大，那么宽度就较大，反之较小。此外，“提琴图”的最终图形是以核密度估计为依据绘制的。</p>
<p>从图中还可以看出类似 sns.swarmplot 的一个特征，就是图形以特征值的直线为对称轴，左右对阵。那么，利用这个特征，就可以进一步做下面的操作。</p>
<p>与以往函数使用类似，可以用参数 hue='smoker' 设置图像中的分类——这一步请读者自行验证，这里再增加一个参数，从而得到一种新的效果。</p>
<pre><code class="python language-python">sns.violinplot(x="day", y="total_bill", hue="smoker", data=tips, palette="muted", split=True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/a661de80-3d84-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>这里因为增加了 split=True，实现了 hue='smoker' 中不同类别数据的对半显示，而不是分别画出两个。</p>
<p>sns.violinplot 的完整参数如下：</p>
<pre><code class="python language-python">seaborn.violinplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, bw='scott', cut=2, scale='area', scale_hue=True, gridsize=100, width=0.8, inner='box', split=False, dodge=True, orient=None, linewidth=None, color=None, palette=None, saturation=0.75, ax=None, **kwargs)
</code></pre>
<h3 id="223">2.2.3 分类特征的估计图</h3>
<p>实现分类特征估计图，依然可以通过定义 sns.catplot 函数中的 kind 参数，当然每个参数值还是会对应着某个单纯的函数：</p>
<ul>
<li>kind = 'point'，等同函数 sns.pointplot</li>
<li>kind = 'bar'，等同函数 sns.barplot</li>
<li>kind = 'count'，等同函数 sns.countplot</li>
</ul>
<h4 id="snsbarplot">sns.barplot</h4>
<p>sns.barplot 绘制的是柱形图，并且可以很容易地实现绘制簇状柱形图。</p>
<pre><code class="python language-python"># 载入泰坦尼克号的数据
titanic = sns.load_dataset("titanic")

# 绘制反映不同等级船舱中不同性别人士获救比率的簇状柱形图
g = sns.catplot(x="class", y="survived", hue="sex", data=titanic, height=6, kind="bar", palette="muted")
g.despine(left=True)
g.set_ylabels("survival probability")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c201dc30-3d84-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>这里用我们熟悉的簇状柱形图表示了分类特征（不同等级的船舱和性别）的获救率。</p>
<p>在上图中，柱子的高度表示特征 survived 中根据特征 class 和 sex 分类的相关数的平均值——集中趋势估计。而每个柱子上面多了一条短线——用 Matplotlib 绘制柱状图的时候没有。对于这条短线，坊间的讹传很多，有人说是“误差”，有人说是“偏差”，<strong>这些都是错误的</strong>。短线表示的是：<strong>置信区间</strong>。</p>
<p>当然，如果不绘制簇状柱形图，也是可以实现的，不引入 hue='sex' 参数即可。</p>
<pre><code class="python language-python">ax = sns.barplot(x="day", y="tip", data=tips, capsize=.2)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d9d28260-3d84-11e9-ab86-d9b554a5bb95" alt="enter image description here" /></p>
<p>的确没有“簇”了，但是，好像又多了点东西，这是因为 capsize=.2 的原因，用它给置信区间的线段上下各加一个“帽子”，浮点数代表横线相对两个柱子中心线距离的比例。</p>
<p>默认情况下，柱状图的高度表示的是相关数据的平均值，既然说到了是默认，言下之意，就可以更改。的确如此，在 sns.boxplot 的参数列表中，有一个参数不可忽视——顺便读一读参数列表，对各种可能的绘图有个大概了解，在用到的时候，可以查阅帮助文档。</p>
<pre><code class="python language-python"> seaborn.barplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, estimator=&lt;function mean&gt;, ci=95, n_boot=1000, units=None, orient=None, color=None, palette=None, saturation=0.75, errcolor='.26', errwidth=None, capsize=None, dodge=True, ax=None, **kwargs)¶
</code></pre>
<p>注意参数列表中的 estimator，它就是用于指定一个统计函数的。例如：</p>
<pre><code class="python language-python">import numpy as np
sns.barplot(x="day", y="tip", data=tips, estimator=np.median)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f5a35410-3d84-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>此柱形图和前面的相比，发现柱子高度的数值不同了，因为这里使用了相关数据的中位数，即 np.median 来表示柱子高度了。</p>
<h4 id="snspointplot">sns.pointplot</h4>
<p>为了阅读方便，重复一下数据集 tips 的特征。</p>
<pre><code class="python language-python">tips.head()
</code></pre>
<p><img src="https://images.gitbook.cn/Fpm5lMFdGTSklnSh4Vj9ELlZ-WVH" alt="avatar" /></p>
<p>继续使用这个数据集。</p>
<pre><code class="python language-python">sns.pointplot(x="time", y="total_bill", data=tips)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0e0760a0-3d85-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>图中 Lunch 和 Dinner 两个分类特征的值所对应的竖直线段，分别表示记录中为该值的 total_bill 特征中的数据的<strong>置信区间</strong>，其中的圆点，表示相应数值的平均数——表示集中趋势的估计。</p>
<pre><code class="python language-python">sns.pointplot(x="time", y="total_bill", hue="smoker", data=tips, markers=["o", "x"], linestyles=["-", "--"])    #⑥
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/20f6f130-3d85-11e9-8c5c-8b54d319dad1" alt="enter image description here" /></p>
<p>⑥ 比前面对 sns.pointplot 函数的应用稍微复杂了一些，使用了更多的参数。再观察图示，就可以看出特征 smoker 中不同取值，在 time 特征中不同取值范畴上的 total_bill 特征数值集中趋势的差异。</p>
<p>这就是 sns.pointplot 的基本使用方法。当然还有更多的参数供使用，此处就不一一列举了，为了对此函数有全面了解，一定要读一读参数列表。</p>
<pre><code class="python language-python"> seaborn.pointplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, estimator=&lt;function mean&gt;, ci=95, n_boot=1000, units=None, markers='o', linestyles='-', dodge=False, join=True, scale=1, orient=None, color=None, palette=None, errwidth=None, capsize=None, ax=None, **kwargs)
</code></pre>
<h4 id="snscountplot">sns.countplot</h4>
<p>此函数也是绘制柱形图，只是它的柱子高度表示的是分类特征中某个值的记录数量。例如：</p>
<pre><code class="python language-python">sns.countplot(x="class", data=titanic)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f9386c40-3d85-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>柱形图中柱子的高度，表示了特征 class 中值为 First、Second、Third 的记录数量。</p>
<p>也可以绘制簇状柱形图，就需要引入 hue 参数——与以往一样。</p>
<pre><code class="python language-python">sns.countplot(x="class", hue="who", data=titanic)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/2515d2d0-3d86-11e9-9de9-d79e7402baad" alt="enter image description here" /></p>
<p>sns.countplot 的参数比以往的要简略一些：</p>
<pre><code class="python language-python">seaborn.countplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, orient=None, color=None, palette=None, saturation=0.75, dodge=True, ax=None, **kwargs)
</code></pre>
<p>以上，就将如何利用 Seaborn 绘制分类特征统计图介绍完毕了。</p>
<h3 id="">总结</h3>
<p>本课介绍的函数主要包括如下几个。</p>
<p>（1）通用性比较强的函数：sns.catplot，其参数 kind 来决定绘制什么类型的图。</p>
<p>（2）具体的专用函数：</p>
<ul>
<li>散点图</li>
<li>kind = 'strip'，默认值，等同函数 sns.stripplot</li>
<li>kind = 'swarm'，等同函数 sns.swarmplot</li>
<li>分布图</li>
<li>kind = 'box'，等同函数 sns.boxplot</li>
<li>kind = 'violin'，等同函数 sns.violinplot</li>
<li>kind = 'boxen'，等同函数 sns.boxenplot</li>
<li>估计图</li>
<li>kind = 'point'，等同函数 sns.pointplot</li>
<li>kind = 'bar'，等同函数 sns.barplot</li>
<li>kind = 'count'，等同函数 sns.countplot</li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>