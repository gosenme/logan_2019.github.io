---
title: 案例上手 Python 数据可视化-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一课介绍了柱形图和条形图，本课将介绍另外几种统计图表。</p>
<h3 id="161">1.6.1 箱线图</h3>
<p>Box Plot 有多种翻译，盒须图、盒式图、盒状图或箱线图、箱形图等，不管什么名称，它的基本结构是这样的：</p>
<p><img src="https://images.gitbook.cn/aec6fa90-3a3e-11e9-b08a-999f0282aa3d" width = "70%" /></p>
<p>这种图是由美国著名统计学家约翰·图基（John Tukey）于 1977 年发明的，它能显示出一组数据的上限、下限、中位数及上下四分位数。</p>
<ul>
<li>中位数：由矩形箱子中的线表示。中位数常用于度量数据的中心，一半观测值小于等于该值，而另一半则大于等于该值。</li>
<li>四分位间距框：四分位间距框表示中间 50% 的数据，即上图中的矩形框，它的上下边之间的距离表示“上四分位数 Q3”和“下四分位数 Q1”的差（Q3-Q1）。</li>
<li>须和上限、下限：由矩形框向两侧延伸的线段，线段的终点分别称为“上限”和“下限”。</li>
<li>异常值：超出“上限”和“下限”范围的值。</li>
</ul>
<p>为了更深入理解箱线图的含义，假设有这样一组数据：[1, 3, 5, 8, 10,11, 16, 98 ]，共有 8 个数字。</p>
<p>首先要计算箱线图中的“四分位数”，注意不是 4 个数：</p>
<ul>
<li>Q1 = 第 1 四分位数、下四分位数，即第 25 百分位数，Q1 的位置 = $\frac{n+1}{4}$ = $\frac{8+1}{4}$ = 2.25</li>
<li>Q2 = 第 2 四分位数、中位数，即第 50 百分位数，Q2 的位置 = $2\frac{n+1}{4}$ = $\frac{2(8+1)}{4}$ = 4.5</li>
<li>Q3 = 第 3 四分位数、上四分位数，即第 75 百分位数，Q3 的位置 = $3\frac{n+1}{4}$ = $\frac{3(8+1)}{4}$ = 6.75</li>
</ul>
<p>对于已经排序的数据 [1, 3, 5, 8, 10,11, 16, 98 ]，下四分位数（Q1）的位置是数列中从小到大第 2.25 个数，当然是不存在这个数字的——如果是第 2 个或者第 3 个，则存在。但是，可以用下面的原则，计算出此位置的数值。</p>
<p><strong>四分位数等于与该位置两侧的两个整数的加权平均数，此权重取决于相对两侧整数的距离远近，距离越近，权重越大，距离越远，权重越小，权数之和等于 1。</strong></p>
<p>根据这个原则，可以分别计算本例中数列的 3 个四分位数。</p>
<p><img src="https://images.gitbook.cn/385b87d0-3a53-11e9-a141-299b97b53ca8" width = "70%" /></p>
<ul>
<li>Q1 = 3 × 0.75 + 5 × 0.25 = 3.5</li>
<li>Q2 = 8 × 0.5 + 10 × 0.5 = 9</li>
<li>Q3 = 11 × 0.25 + 16 × 0.75 = 14.75</li>
</ul>
<p>在此计算基础上，还可以进一步计算四分位间距和上限、下限的数值。</p>
<ul>
<li>四分位间距：IQR = Q3 － Q1 = 11.25</li>
<li>上限 = Q3 + 1.5 × IQR = 14.75 + 1.5 × 11.25 = 31.625</li>
<li>下限 = Q1 － 1.5 × IQR = 3.3 － 1.5 × 11.25 = ﹣13.375</li>
</ul>
<blockquote>
  <p>注意：凡是落在上下限以外的数据，都是离群值。上述计算中，并没有把离群值剔除，因此导致下限出现了负数。下面我们要使用 Matplotlib 中的专有方法绘制箱线图，该方法会把离群值剔除之后计算。</p>
</blockquote>
<p>先看一个简单示例，了解基本的流程。</p>
<pre><code class="python language-python">%matplotlib inline
import matplotlib.pyplot as plt

fig,ax = plt.subplots(1, 2)
data = [1, 5, 9, 2]
ax[0].boxplot([data]) 
ax[0].grid(True)
ax[1].boxplot([data], showmeans=True)    # 显示平均值
ax[1].grid(True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/76aaad50-3a5c-11e9-8072-7365783b1b78" width = "70%" /></p>
<p>这里绘制了两张箱线图，一张没有显示平均值，另外一张显示了平均值，所使用的方法就是 boxplot，其完整参数列表为：</p>
<pre><code class="python language-python">plt.boxplot(x, notch=None, sym=None, vert=None, whis=None, positions=None, widths=None, patch_artist=None, bootstrap=None, usermedians=None, conf_intervals=None, meanline=None, showmeans=None, showcaps=None, showbox=None, showfliers=None, boxprops=None, labels=None, flierprops=None, medianprops=None, meanprops=None, capprops=None, whiskerprops=None, manage_xticks=True, autorange=False, zorder=None, *, data=None)
</code></pre>
<p>参数很多，不要担心记忆问题，更别担心理解问题。首先很多参数都是可以“望文生义”的，再有，与以前所使用的其他方法（函数）的参数含义也大同小异。</p>
<ul>
<li>notch：默认为 None，如果为 True，则意味着绘制有凹槽的箱线图。</li>
</ul>
<pre><code class="python language-python">  plt.boxplot([2,4,6,8,10], notch=True)
  plt.grid(1)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f127a420-3a5c-11e9-94ba-95207c5914bd" width = "70%" /></p>
<p>所谓的“凹槽”，不是简单形状的改变，左右折线的上限区间表示了数据分布的置信区间，横线依然是上限和下限。</p>
<ul>
<li>vert：设置箱线图是竖直还是水平，默认为 True，如果设置为 False，则水平。</li>
<li>bootstrap：这个参数与前面的 notch 配合，用于设置置信区间。</li>
</ul>
<p>姑且简单解释几个，因为太多，还是要通过一些具体的例子，理解箱线图在实际问题的应用方式，特别是参数的作用。</p>
<p>为了制图需要，先创建一个数据集。</p>
<pre><code class="python language-python">import numpy as np
np.random.seed(10)
collectn_1 = np.random.normal(100, 10, 200)
collectn_2 = np.random.normal(80, 30, 200)
collectn_3 = np.random.normal(90, 20, 200)
collectn_4 = np.random.normal(70, 25, 200)   
data = [collectn_1, collectn_2, collectn_3, collectn_4]
</code></pre>
<p>然后利用 data 数据集，绘制箱线图——注意，里面有 4 个维度。</p>
<pre><code class="python language-python">fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(data, patch_artist=True)    #①
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/2ff621e0-3a5d-11e9-938f-ff5cd0ffb5a9" width = "70%" /></p>
<p>语句 ① 中使用了参数 patch_artist=True，它控制的是矩形框是否填充。另外，因为数据集是二维数据，那么就会按照每个维度（特征）的数值分别画出该维度（特征）的箱线图。</p>
<p>还要注意，图中已经显示出来了每个维度中的离群值——这种方法会常用于数据清洗之中判断某个特征中是否有离群值。</p>
<p>① 中，用变量 bp 得到了 ax.boxplot 方法的返回对象，该对象包含了如下内容：</p>
<pre><code class="python language-python">bp

#output
{'whiskers': [&lt;matplotlib.lines.Line2D at 0x11deab2b0&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dea7710&gt;,
  &lt;matplotlib.lines.Line2D at 0x11deb7940&gt;,
  &lt;matplotlib.lines.Line2D at 0x11deb7d30&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dec1fd0&gt;,
  &lt;matplotlib.lines.Line2D at 0x11decb400&gt;,
  &lt;matplotlib.lines.Line2D at 0x11ded36a0&gt;,
  &lt;matplotlib.lines.Line2D at 0x11ded3a90&gt;],
 'caps': [&lt;matplotlib.lines.Line2D at 0x11deab9e8&gt;,
  &lt;matplotlib.lines.Line2D at 0x11deabd30&gt;,
  &lt;matplotlib.lines.Line2D at 0x11deb7e10&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dec1400&gt;,
  &lt;matplotlib.lines.Line2D at 0x11decb748&gt;,
  &lt;matplotlib.lines.Line2D at 0x11decba90&gt;,
  &lt;matplotlib.lines.Line2D at 0x11ded3dd8&gt;,
  &lt;matplotlib.lines.Line2D at 0x11ded3eb8&gt;],
 'boxes': [&lt;matplotlib.patches.PathPatch at 0x11deab080&gt;,
  &lt;matplotlib.patches.PathPatch at 0x11deb7710&gt;,
  &lt;matplotlib.patches.PathPatch at 0x11dec1da0&gt;,
  &lt;matplotlib.patches.PathPatch at 0x11ded3470&gt;],
 'medians': [&lt;matplotlib.lines.Line2D at 0x11deabe10&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dec1748&gt;,
  &lt;matplotlib.lines.Line2D at 0x11decbdd8&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dedd4a8&gt;],
 'fliers': [&lt;matplotlib.lines.Line2D at 0x11deb7400&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dec1a90&gt;,
  &lt;matplotlib.lines.Line2D at 0x11decbeb8&gt;,
  &lt;matplotlib.lines.Line2D at 0x11dedd7f0&gt;],
 'means': []}
</code></pre>
<p>这些其实都是箱线图的各个组成部分，每一部分都可以看做对象，于是可以对各个部分给予进一步的修饰。</p>
<pre><code class="python language-python">fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(data, patch_artist=True)
# 修改矩形框内的填充色和矩形框的边线
for box in bp['boxes']:
    box.set( color='#7570b3', linewidth=2)    # 矩形框边线颜色和粗细
    box.set( facecolor = '#1b9e77' )    # 填充色

# 须线的粗细和颜色
for whisker in bp['whiskers']:
    whisker.set(color='red', linewidth=2)

# 表示上下限的线的颜色和粗细
for cap in bp['caps']:
    cap.set(color='black', linewidth=2)

# 表示中位数的的线的颜色和粗细
for median in bp['medians']:
    median.set(color='#b2df8a', linewidth=4)

# 表示离群值的符号设置
for flier in bp['fliers']:
    flier.set(marker='*', color='#e7298a', alpha=0.5)

# 设置坐标轴
ax.set_xticklabels(['Sample1', 'Sample2', 'Sample3', 'Sample4'])
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5ea40d90-3a5d-11e9-938f-ff5cd0ffb5a9" width = "70%" /></p>
<p>变量 bp 引用的对象是字典对象，其中包含（以下各项其实都是对象）：</p>
<ul>
<li>boxes，箱线图的矩形框</li>
<li>whiskers，箱线图的须线，即从矩形框开始向两侧延伸的线段</li>
<li>medians，表示中位数的线段</li>
<li>caps，表示上、下限的线段</li>
<li>fliers，表示离群值的符号</li>
<li>means，表示平均值的符号</li>
</ul>
<p>在此程序的最后，对坐标系的坐标轴做了设置，与以往学习过的内容一样，那就请读者自行理解它们吧。</p>
<p>类似于以往的制图方法，在 DataFrame 对象中，也有绘制箱线图的方法。</p>
<pre><code class="python language-python">import pandas as pd
import numpy as np
data = np.random.randn(25, 4)
df = pd.DataFrame(data, columns=list('ABCD'))
df.head()

#out
           A            B          C           D
0    0.456884    -0.242716   0.889094    -0.535021
1    1.427260    -0.515891   -0.913880   0.997063
2    0.470586    -0.874625   0.162060    0.370161
3    -0.756437   -0.528706   0.160920    0.863682
4    0.402548    0.902117    0.415504    1.492799
</code></pre>
<p>df 有 4 个特征，每个特征下是随机生成的浮点数。</p>
<pre><code class="python language-python">ax = df.plot.box()
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/edb88db0-3a5f-11e9-a141-299b97b53ca8" width = "70%" /></p>
<p>箱线图暂时这么多，下面看饼图。</p>
<h3 id="162">1.6.2 饼图</h3>
<p>饼图是用来表示数据中各项的代销占总数的比例。在 Matplotlib 中，pie 是用来绘制饼图的方法（函数）。</p>
<pre><code class="python language-python">plt.pie(x, explode=None, labels=None, colors=None, autopct=None, pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=None, radius=None, counterclock=True, wedgeprops=None, textprops=None, center=(0, 0), frame=False, rotatelabels=False, *, data=None)
</code></pre>
<p>这里列出了 pie 的完整参数——有时间和耐心的话，可以通过阅读官方文档，详细了解。我们还是在下面的实践中理解其含义。</p>
<pre><code class="python language-python">x = [2, 4, 6 ,8]
fig, ax = plt.subplots()
labels = ['A', 'B', 'C', 'D']
colors = ['red', 'yellow', 'blue', 'green']
explode = (0, 0.1, 0, 0)
ax.pie(x, explode=explode, labels=labels, 
       colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, radius=1.2) 
ax.set(aspect="equal", title='Pie')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f5383db0-3bf9-11e9-945f-355129fe08bb" alt="enter image description here" /></p>
<p>画出了一张漂亮的饼图，依次解释此代码中 ax.pie 的各个参数。</p>
<ul>
<li>x：毫无疑问，是数据。</li>
<li>explode：“扇面”的偏离。饼图一个“圆饼”，被分成了 4 个“扇面”，explode 中第二个数 0.1，对应 B“扇面”偏离 0.1，其他为零，即不偏离。</li>
<li>labels：为每个“扇面”设置标示。</li>
<li>colors：为每个“扇面”设置颜色。</li>
<li>autopct：按照规定格式在每个“扇面”上显示百分比。</li>
<li>shadow：是否有阴影。</li>
<li>startangle：第一个“扇形”开始的角度，然后默认依逆时针旋转。</li>
<li>radius：半径大小。</li>
</ul>
<p>饼图的绘制过程比较简单，为了巩固已学过的知识，借此机会完成一个示例。<a href="https://github.com/qiwsir/DataSet/tree/master/bra">数据来源请点击这里查看</a>，该数据是从某东网站上爬下来的某商品的部分评论数据。</p>
<pre><code class="python language-python">df = pd.read_csv("/Users/qiwsir/Documents/Codes/Dataset/bra/colors.csv")
colors = pd.DataFrame({'productColor':df.values[0:,1], 'color':df.values[0:,2]})
colors.head()

#out
    productColor    color
0    22咖啡色   棕色
1    02粉色    粉色
2    071蓝色   蓝色
3    071黑色   黑色
4    071肤色   肤色
</code></pre>
<p>从这个数据集中，估计也猜不出是什么商品。下面还要读取另外一个 CSV 文档，然后两个合并，就能猜出是什么商品了。</p>
<pre><code class="python language-python">df2 = pd.read_csv("/Users/qiwsir/Documents/Codes/Dataset/bra/bra.csv")
cbras = pd.merge(df2, colors, on="productColor", how="left")
cbras.head()

#out
        creationTime    productColor    productSize color
0    2016-06-08 17:17:00 22咖啡色               75C 棕色
1    2017-04-07 19:34:25 22咖啡色               80B 棕色
2    2016-06-18 19:44:56 02粉色                80C 粉色
3    2017-08-03 20:39:18 22咖啡色               80B 棕色
4    2016-07-06 14:02:08 22咖啡色               75B 棕色
</code></pre>
<p>以上数据其实是经过整理之后的，不是从网页上得到的原始数据。</p>
<p>首先用柱形图比较不同的“color”特征值的记录数量。</p>
<pre><code class="python language-python">color_count = cbras.groupby('color').count()    # ②
datas = color_count['productColor']
labels = datas.index
position = range(len(datas.index))

plt.bar(x=position, height=datas.values, width=0.6, tick_label=labels)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/23614850-3c02-11e9-945f-355129fe08bb" alt="enter image description here" /></p>
<p>② 使用了 pandas 中的分组统计——按照“color”特征的值（颜色）统计每种颜色的记录数量，然后将统计结果在柱状图中显示。</p>
<blockquote>
  <p>注意，横轴的标示是汉字，如果在调试的时候，看到的是方框，说明本地的计算机没有设置显示汉字的功能，可以到网上搜索一下，关于汉字在 Matplotlib 中显示问题的资料有很多。</p>
</blockquote>
<p>特征“productSize”中的数据不利于统计，需要对其进行再处理，即所谓的“数进行清洗”。</p>
<pre><code class="python language-python"># 对 df2 中的 productSize 特征的数值进行清洗
bras2 = df2['productSize'].str.upper()
cup = bras2.str.findall("[a-zA-Z]+").str[0]    #用正则表达式进行初步清洗
cup2 = cup.str.replace('M', 'B')    #将其他型号归类为A-E
cup3 = cup2.str.replace('L', 'C')
cup4 = cup3.str.replace('XC', 'D')
cup5 = cup4.str.replace('AB', 'B')
df2['cup'] = cup5

# 数据清洗完毕，进行分组统计，并用饼图表现结果
cup_count = df2.groupby('cup').count()
labels = ['A', 'B', 'C', 'D', 'E']
fig, ax = plt.subplots()
explode = (0, 0.1, 0, 0, 0)
ax.pie(cup_count['productColor'], explode=explode, labels=labels, autopct='%1.1f%%', radius=1.2, startangle=0)
ax.set(aspect='equal')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/61d45fa0-3c02-11e9-bf74-1fbe0a2767fa" alt="enter image description here" /></p>
<p>此处的统计结果显示，网上的那么多“波涛汹涌”的图片多数是 PS 过的——这不是重点，重点是上面的程序，特别是使用 pie 方法绘制饼图。</p>
<p>顺便告知，DataFrame 对象也有 pie 方法，使用很简单，可以尝试，此处从略。</p>
<h3 id="163">1.6.3 直方图</h3>
<p>先提醒：直方图，跟“柱形图”有很大区别。</p>
<p>在这里借用《概率论与数理统计》（盛骤等编著，浙江大学出版社 2008 年 6 月第 4 版第 1 次印刷）图书里面的一个例题（题目的解会根据本达人课的语言风格需要做适当修改），通过该例题理解“直方图”含义，以及与“柱形图”的区别。</p>
<p>题目：下面列出了 84 个伊特拉斯坎（Etruscan）人男子头颅的最大宽度（mm），现在来画这些数据的“频率直方图”。</p>
<p>141, 148, 132, 138, 154, 142, 150, 146, 155, 158, 150, 140, 147, 148, 144, 150, 149, 145, 149, 158, 143, 141, 144, 144, 126, 140, 144, 142, 141, 140, 145, 135, 147, 146, 141, 136, 140, 146, 142, 137, 148, 154, 137, 139, 143, 140, 131, 143, 141, 149, 148, 135, 148, 152, 143, 144, 141, 143, 147, 146, 150, 132, 142, 142, 143, 153, 149, 146, 149, 138, 142, 149, 142, 137, 134, 144, 146, 147, 140, 142, 140, 137, 152, 145</p>
<p>解：以上数据最小值、最大值分别为 126、158，所有数据都落在区间 [126, 158] 上。那么，如果设定一个区间 [124.5, 159.5]，则所有的数据也在此区间内——没有什么理由，区间大点，略有冗余，这是画直方图的通常做法。</p>
<p>将区间 [124.5, 159.5] 划分为 7 小段（原书称为“小区间”），每小段的长度用希腊字母 Δ 表示，则 Δ=（159.5－124.5）/ 7 = 5。给Δ一个文雅的名称，叫做“组距”，即将区间 [124.5, 159.5] 划分为 7 个组，每组的组距为 5（如图下所示），每组的两端（如 124.5、129.5）称为“组限”。</p>
<p><img src="https://images.gitbook.cn/de59d0a0-3c02-11e9-b0f8-41432cc061d0" alt="enter image description here" /></p>
<p>数一数落在各个组内的数据个数——严格的概念曰“频数”，用 f 表示。各组的频数与总数据量（84）的比值称为“频率”，即 f / n，如下表所示。</p>
<p><img src="https://images.gitbook.cn/FncXOyZ0N0JMfoJjZvG8kVaQWVV8" alt="avatar" /></p>
<p>以上图的每一小段（如 124.5 到 129.5 之间的线段）为宽：</p>
<p>（1）若以频数 f 为高，绘制小矩形，得到如下“频数直方图”：</p>
<p><img src="https://images.gitbook.cn/70784c40-3c90-11e9-820f-71e8e54c16d2" width = "70%" /></p>
<p>（2）若以 f/(nΔ) 的值为高，画出一系列的小矩形，得到如下“频率直方图”：</p>
<p><img src="https://images.gitbook.cn/c49503b0-3c93-11e9-bea2-69276fa17a9f" width = "70%" /></p>
<p>这样就理解了直方图与柱形图的区别了，那么，用 Matplotlib 如何画出直方图？</p>
<pre><code class="python language-python">import matplotlib 
matplotlib.rcParams['axes.unicode_minus']=False # ③

data = np.random.randn(10000)    # ④
plt.hist(data, bins=40, density=True, facecolor="blue", edgecolor="black", alpha=0.7) 
plt.xlabel("区间") 
plt.ylabel("频率") 
plt.title("频数/频率分布直方图")
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f64c85e0-3c93-11e9-8dd5-1b4e2ffa509f" alt="enter image description here" /></p>
<p>语句 ③ 是前文已经介绍过的内容，其作用是显示横轴中的负数。</p>
<p>语句 ④ 生成了服从正态分布的一些数据，然后用这些数据绘制直方图。</p>
<p>plt.hist 语句中的参数含义如下。</p>
<ul>
<li>data：必选参数，绘图数据。</li>
<li>bins：这个参数的赋值比较多样化。<ul>
<li>如果是整数，则表示直方图中矩形数目，即组距（小区间）的数目。</li>
<li>如果是数列，比如 [1,2,3,4,5]，则表示直方图中矩形左右边界（即组距的左右边界，组限）是 [1, 2), [2, 3), [3, 4), [4, 5]，即组距数目为 4（矩形数量为 4）。</li></ul></li>
<li>density=True：本例中如此设置，则所得直方图表示的归一化后的频率（概率密度），即直方图下的面积总和为 1；如果不设置，则显示的是频数，没有归一化。</li>
<li>facecolor：直方图中矩形的颜色。</li>
<li>edgecolor：矩形边的颜色。</li>
<li>alpha：图像透明度。</li>
</ul>
<p>如果查看 plt.hist 的文档，会发现它还有很多参数，这跟以往的类似函数差不多的，我们的做法还是“在战争中学习打仗”，通常只有在有意愿的时候，才可能耐心阅读帮助文档。</p>
<p>另外，plt.hist 函数也有返回值，可惜文档中只说它要返回 n、bins、patches，对这些返回值的含义没有解释，这里给予简要说明。</p>
<ul>
<li>n：表示直方图中每个“组距”（小区间，或小矩形）中的频数或者频率。</li>
<li>bins：表示直方图中组距（小区间、小矩形）的左边界数值（最后一个数字是最后的组距右边界）。</li>
<li>patches：组成直方图的小矩形对象的集合。</li>
</ul>
<p>网上很少有资料对 patches 进行详细说明，甚至有的资料说“不用管它”。这里我们就管管它，理解它是什么东西——东西就是对象。</p>
<pre><code class="python language-python">x = np.random.normal(size=100)
n, bins, patches = plt.hist(x)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9260c580-3c95-11e9-8dd5-1b4e2ffa509f" width = "70%" /></p>
<p>这个直方图没有太多修饰，是很朴素的，默认情况下，bins=10。根据上面对三个返回值的阐述，n 应该对应着一个数组，这个数组中有 10 个数值，这十个数值分别表示分布在每个小矩形中的随机数（来自于 x 所引用的数据集）的数量，即 n 表示的是频数。</p>
<pre><code class="python language-python">n

#out
array([ 3.,  3., 14., 15., 21., 22., 12.,  6.,  1.,  3.])
</code></pre>
<p>将结果与图示对照——总坐标表示频数，是吻合的。</p>
<p>再来看 bins：</p>
<pre><code class="python language-python">bins

#out
array([-2.28899862, -1.82261866, -1.3562387 , -0.88985873, -0.42347877,
        0.04290119,  0.50928116,  0.97566112,  1.44204108,  1.90842105,
        2.37480101])
</code></pre>
<p>这里一共有 11 个数，分别构成了每个小矩形的左右边界数值。</p>
<p>最后看 patches。</p>
<pre><code class="python language-python">patches

#out
&lt;a list of 10 Patch objects&gt;
</code></pre>
<p>返回的是 10 个小矩形的对象集合。为了深入理解对象集合的概念，对上面绘制直方图的程序稍加改进。</p>
<pre><code class="python language-python">x = np.random.normal(size=100)
n, bins, patches = plt.hist(x)
plt.setp(patches[0], 'facecolor', 'g')    # ⑤
max_index = np.where(n==np.max(n))[0][0]    # ⑥
plt.setp(patches[max_index], facecolor='red')    # ⑦
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/2dd33c50-3c96-11e9-bea2-69276fa17a9f" width = "70%" /></p>
<p>语句 ⑤ 就是要对 patches 对象集合中索引是 0，即第 1 个小矩形进行属性设置，plt.setp 函数的作用是对某对象的属性进行设置，即 set property；语句 ⑥ 则是获得变量 n 中最大的数值——频数最高——所对应的索引——也是小矩形在 patches 中的索引，然后在 ⑦ 中对该小矩形的填充颜色设置为红色，最终得到了图示效果。</p>
<p>至此，已经理解了直方图的基本含义。既然它表达的是数值的分布情况，根据统计学知识得知，概率分布的具体形态有多种，下面列举一二。</p>
<p>高斯分布是最常见的，比如智商，通常认为符合这种分布。</p>
<pre><code class="python language-python">np.random.seed(19680801)

mu, sigma = 100, 15    # 分别表示平均数和标准差
x = mu + sigma * np.random.randn(10000)

# 绘制直方图，并得到返回值
n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)    # ⑧

# 设置坐标系
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0b555cb0-3c98-11e9-8dd5-1b4e2ffa509f" alt="enter image description here" /></p>
<p>再制作一张反映拉普拉斯分布的。</p>
<pre><code class="python language-python">np.random.seed(444)
d = np.random.laplace(loc=15, scale=3, size=500)
n, bins, patches = plt.hist(x=d, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)

plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('My Very Own Histogram')
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
plt.ylim(top=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/211942f0-3c98-11e9-820f-71e8e54c16d2" alt="enter image description here" /></p>
<p>直方图能够将数值的分布——包括频率和频数分布——以可视化的方式表达出来，但这不是最终目的，最终是要得到“概率密度函数”（一般以大写“PDF”（Probability Density Function）表示），为此要用到被称为“核密度估计”（Kernel Density Estimation，简称 KDE）的算法。KDE 属于非参数检验方法之一，由 Rosenblatt（1955）和 Emanuel Parzen（1962）提出，又名 Parzen 窗（Parzen Window）。</p>
<p>在 Matplotlib 中有专门的函数，实现 KDE 的可视化工作。</p>
<pre><code class="python language-python">means = 10, 20
stdevs = 4, 2
dist = pd.DataFrame(np.random.normal(loc=means, scale=stdevs, size=(1000, 2)), columns=['a', 'b'])
dist.agg(['min', 'max', 'mean', 'std']).round(decimals=2)

#out
          a     b
min      -2.93     14.40
max      22.58     27.08
mean    9.58    19.93
std        4.18    1.92
</code></pre>
<p>这里创建了具有两个特征的数据集，每个特征下的数值都是根据高斯分布生成的。</p>
<p>然后使用 DataFrame 对象中的 DataFrame.plot.kde 实现 KDE，并绘制相应的 PDF 曲线。</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
dist.plot.hist(density=True, ax=ax)    # ⑨
dist.plot.kde(ax=ax, legend=False, title='Histogram: A vs. B')    # ⑩

ax.set_ylabel('Probability')
ax.grid(axis='y')
ax.set_facecolor('#d8dcd6')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/605ddb10-3c98-11e9-8dd5-1b4e2ffa509f" alt="enter image description here" /></p>
<p>⑨ 绘制直方图，使用的是 DataFrame 对象的方法 plot.hist，其中参数 ax = ax，旨在说明当前直方图所在的坐标系。如果没有特别指定，默认 bings=10，这样就得到了两个特征的直方图。</p>
<p>⑩ 就是实现 KDE，并同时作图。DataFrame.plot.kde 使用的是高斯核函数。当然，如果再进一步，可以检验 KDE 结果与 PDF 曲线之间的差异，即在同一个坐标系中绘制相应曲线。对此有兴趣的可以进一步研究。</p>
<h3 id="">总结</h3>
<p>本课继续学习如何使用 Matplotlib 绘制常用的统计图，主要包括箱线图、饼图和直方图。以下内容是读者应该掌握的：</p>
<ul>
<li>绘制每种统计图所用的函数（方法），以及常用参数含义</li>
<li>每种统计图的含义和应用场景</li>
</ul>
<p>至此，我们已经将常用的 Matplotlib 绘图方法讲述完毕，当然，使用 Matplotlib 所能够绘制的图，远不止这几课所介绍的。但是，基础是最重要的，其他的更多花样的图，都是基于基本知识和基本方法而发展出来的。</p>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>