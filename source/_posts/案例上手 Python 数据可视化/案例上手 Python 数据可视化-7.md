---
title: 案例上手 Python 数据可视化-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在图纸上绘图，有时候整张图纸只绘制一幅图，有时候要绘制多幅图。在 Matplotlib 中要实现这种功能，可以使用 plt.subplots，前面已经用过此函数，此处要深入理解它的特点。</p>
<p>首先，要引用 Matplotlib 的模块。</p>
<pre><code class="python language-python">%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
</code></pre>
<h3 id="131">1.3.1 分区</h3>
<p>在前面编写可视化代码的时候，plt.subplots() 已经出现过了，它返回了一个图像对象和一个坐标系对象。但是，在以往调用的时候，没有向函数提供任何参数。如果像下面代码这样，就不会只返回一个坐标系对象了。</p>
<pre><code class="python language-python">fig, ax = plt.subplots(3, 3, sharex='col', sharey='row')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/74732580-3359-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>从输出结果中可知，现在得到了 3 × 3 = 9 个坐标，即在一张图中得到了 9 个坐标系。</p>
<pre><code class="python language-python">ax
#Out:
array([[&lt;matplotlib.axes._subplots.AxesSubplot object at 0x118bb3470&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x118ba69b0&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x11ac36e48&gt;],
       [&lt;matplotlib.axes._subplots.AxesSubplot object at 0x11ac652b0&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x11ac8c6d8&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x11acb49b0&gt;],
       [&lt;matplotlib.axes._subplots.AxesSubplot object at 0x11acdcc88&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x11ad0c0b8&gt;,
        &lt;matplotlib.axes._subplots.AxesSubplot object at 0x11ad333c8&gt;]],
      dtype=object)
</code></pre>
<p>变量 ax 其实引用了一个数组对象，其形状是 3 × 3 的，每个元素是一个坐标系对象。于是乎就可以通过类似 ax[1, 2] 的方式得到某一个坐标系对象，然后对该坐标系对象实施有关操作，比如设置属性，或者调用方法，在上一课中有一个绘制脸谱的例子，就是这个道理的具体应用。</p>
<p>作为复习，可以看下面的代码，目的是依次在每个坐标系内标注上行列。</p>
<pre><code class="python language-python">fig, ax = plt.subplots(3, 3, sharex='col', sharey='row')
for i in range(3):
    for j in range(3):
        ax[i, j].text(0.5, 0.5, str((i, j)), fontsize=18, ha='center')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/add42c20-3359-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>显然，以上功能的实现，就在于 plt.subplots 函数。为了深入理解此函数，可以先浏览它的完整参数。</p>
<pre><code class="python language-python">plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True, subplot_kw=None, gridspec_kw=None, **fig_kw)
</code></pre>
<p>结合之前展示的 Matplotlib 中函数（方法）的参数，会发现不仅参数个数比较多，而且还通过 *<em>fig_kw、</em>arg 等方式，许可传入更多的参数。这就说明，它们提供了非常灵活的功能。但是，记忆就麻烦了。而实际上，不用刻意记忆，因为通过官方文档或者在 Jupyter 中使用查看帮助文档的智力，能够查看到对所有参数解释说明。</p>
<p>选择几个常用的参数给予说明：</p>
<ul>
<li>nrows 和 ncols，必须是整数，分别设置了行（nrows）和列（ncols）的坐标系分区数量；</li>
<li>sharex 和 shapey，布尔值，或者选择 'none'、'all'、'row'、'col' 中的某个字符串，默认是 False。</li>
</ul>
<blockquote>
  <p>注意观察上面的代码，已经分别设置了两个参数的值。为了对比，如果不设置，即默认值 False，会是什么效果？</p>
</blockquote>
<pre><code class="python language-python">fig, ax = plt.subplots(3, 3)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5d0458f0-335a-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>将此处的结果图示和前面的对比，发现此图示中，每个坐标系的坐标轴都标明了横纵坐标的刻度。这就是 sharex 和 sharey 的作用效果。</p>
<p>其他参数，就请读者自己查看帮助文档了。</p>
<p>以上解释了 plt.subplots，它返回两个对象，除了 ax，还有一个 fig，那么如何理解 fig 呢？</p>
<p>其实，fig 是在坐标系之上的对象，称之为“图像”（figure）。创建这个图像对象的基本方式是 fig = plt.figure()，而后所建立的坐标系对象，其实是由图像对象生成的。</p>
<pre><code class="python language-python">fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e41c3d80-335a-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>如果还对第1-1课的内容有印象，对于这个结果就不陌生了。在这里，首先创建了图像对象，然后使用图像对象的方法创建了此图像中的一个坐标系对象。</p>
<blockquote>
  <p>注意，fig.add_axes([0.1, 0.1, 0.8, 0.8]) 中的参数，是按照 [left, bottom, width, height] 的顺序，设置坐标系相对于图像对象的位置以及坐标系对象的长宽（其数值是相对于图像对象长宽的比例，width=0.8 意味着坐标系对象的宽度是图像对象宽度的 80%）。</p>
</blockquote>
<p>在理解了上面的绘图原理之后，就可以进一步，做出这样的结果了：</p>
<pre><code class="python language-python">fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax2 = fig.add_axes([0.6, 0.5, 0.2, 0.3])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/18320590-335c-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>这就是面向对象思想的魅力。</p>
<p>诚然，图像对象还有很多属性和方法，当以后作图的时候如果用到，再进一步研习。</p>
<p>在同一个图像对象上，设置不同大小的坐标系分区，还可以使用 GridSpec 实现。</p>
<pre><code class="python language-python">from matplotlib.gridspec import GridSpec    #①

fig = plt.figure()
fig.suptitle("划分不同大小的坐标系分区")    #②

gs = GridSpec(3, 3, figure=fig)    #③
ax1 = fig.add_subplot(gs[0, :])    #④
ax2 = fig.add_subplot(gs[1, :-1])
ax3 = fig.add_subplot(gs[1:, -1])
ax4 = fig.add_subplot(gs[-1, 0])
ax5 = fig.add_subplot(gs[-1, -2])

def format_axes(fig):    
    for i, ax in enumerate(fig.axes):    #⑤
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

format_axes(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/399c6770-335c-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>在上述示例中，使用 GridSpec 类，实现了最终图示的结果。下面依次解释程序中的某些语句：</p>
<ul>
<li>① 引入 GridSpec，注意它不在 plt 下面；</li>
<li>② 使用图像对象的方法设置本图像的标题；</li>
<li>③ 建立了 GridSpec 的实例。</li>
</ul>
<p>下面列出这个类的完整参数：</p>
<pre><code class="python language-python">GridSpec(nrows, ncols, figure=None, left=None, bottom=None, right=None, top=None, wspace=None, hspace=None, width_ratios=None, height_ratios=None)
</code></pre>
<p>根据望文生义的原则，基本上能够猜测到这些参数的含义，况且，很多参数跟以往遇到的含义基本一致，实在不行还可以查看帮助文档。因此，此处就不再赘述各个参数的含义了。</p>
<p>gs 实例对象的建立，就相当于在图像对象 fig 的图层上创建了网格（3 × 3 的网格）。</p>
<ul>
<li>④ 中的 fig.add_subplot 方法旨在创建一个坐标系分区，其效果与 add_axes 方法相仿。注意 add_subplot 的参数，是以 gs 的网格来说明这个坐标系分区所覆盖的网格区域。可以把 gs 对象的网格看做一个二维的数组（3 × 3），gs[0, :] 就是获得数组的切片。可以用下图依次表示各部分切片或者索引得到的结果。</li>
</ul>
<p><img src="https://images.gitbook.cn/83b58530-335c-11e9-ae61-ab46ecd2ee1c" width = "70%" /></p>
<p>如此，就在所规定的网格范围上建立了相应的坐标系对象，即为 ④ 和后面各句的效果。</p>
<ul>
<li>⑤ 中的 fig.axes 是通过图像对象的属性 axes 得到该图像中的所有坐标系对象，然后依次调用每个坐标系对象，使用坐标系对象的属性和方法。</li>
</ul>
<p>通过上述各项操作，已经基本感受到了如何实现坐标系分区的操作，下面就开始在坐标系中绘图。</p>
<h3 id="132">1.3.2 曲线</h3>
<p>在本课中，凡是依据某个函数关系在坐标系中绘制的图像，都泛称为曲线，尽管有的分明是直的。下面要演示的是在同一个坐标系中绘制多条曲线。</p>
<pre><code class="python language-python">import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), color='blue')
ax.plot(x, np.sin(x-np.pi/3), color='r', linestyle='-.')
ax.plot(x, np.sin(x-2*np.pi/3), color='#A52A2A', linewidth=3)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0a9a24c0-335d-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>如果在一个坐标系中绘制一条曲线，只需要调用一次 ax.plot()；如果要绘制多条曲线，就调用多次。</p>
<p>下面，要了解的就是 ax.plot 的多种多样的使用方法，上面的程序中，已经分别用不同的参数显示了对曲线的控制。</p>
<pre><code class="python language-python">plot([x], y, [fmt], data=None, **kwargs)
</code></pre>
<ul>
<li>x，y：表示横纵坐标的数据集。</li>
<li>fmt：可以在这里设置很多关于曲线的属性，比如前面程序中设置过线的颜色、线型、宽度等。有一部分可以用缩写的方式表示，比如 color='r'。关于颜色及其符号表示、线型及其符号表示，在前几课中已经列出了，请参考。</li>
</ul>
<p>还有一个参数，上面的示例中没有显示，名为 marker，它能够指定表示坐标（点）的图形。例如：</p>
<pre><code class="python language-python">plt.plot([1,2,3], [3,8,5], marker='o')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/467e2cc0-335d-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>这里使用 marker='o' 对坐标点指定了显示图形。marker 还可以取其他值，下表列出了可选值及其含义。</p>
<table>
<thead>
<tr>
<th>符号</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>'.'</td>
<td>实心小点</td>
</tr>
<tr>
<td>','</td>
<td>一个像素，其实就是什么也没显示</td>
</tr>
<tr>
<td>'o'</td>
<td>实心圆点</td>
</tr>
<tr>
<td>'v'</td>
<td>一个角指向下的三角形</td>
</tr>
<tr>
<td>'^'</td>
<td>一个角指向上的三角形</td>
</tr>
<tr>
<td>'&lt;'</td>
<td>一个角指向左的三角形</td>
</tr>
<tr>
<td>'&gt;'</td>
<td>一个角指向右的三角形</td>
</tr>
<tr>
<td>'1'</td>
<td>一个棱指向下的三棱形</td>
</tr>
<tr>
<td>'2'</td>
<td>一个棱指向上的三棱形</td>
</tr>
<tr>
<td>'3'</td>
<td>一个棱指向左的三棱形</td>
</tr>
<tr>
<td>'4'</td>
<td>一个棱指向右的三棱形</td>
</tr>
<tr>
<td>'s'</td>
<td>正方形</td>
</tr>
<tr>
<td>'p'</td>
<td>五边形</td>
</tr>
<tr>
<td>'*'</td>
<td>星形</td>
</tr>
<tr>
<td>'h'</td>
<td>六边形</td>
</tr>
<tr>
<td>'H'</td>
<td>六边形</td>
</tr>
<tr>
<td>'+'</td>
<td>加号 ＋ 形</td>
</tr>
<tr>
<td>'x'</td>
<td>乘号 × 形</td>
</tr>
<tr>
<td>'D'</td>
<td>菱形（对角线相等）</td>
</tr>
<tr>
<td>'d'</td>
<td>菱形（水平对角线较短）</td>
</tr>
<tr>
<td>'</td>
<td>'</td>
</tr>
<tr>
<td>'_'</td>
<td>横线符号</td>
</tr>
</tbody>
</table>
<p>以下几个参数也是跟上述图形设置有关的：</p>
<ul>
<li>markersize，设置大小</li>
<li>markerfacecolor，设置颜色</li>
<li>markevery，指定所要设置的坐标点</li>
</ul>
<p>以下面的程序为例，显示上述设置效果：</p>
<pre><code class="python language-python">    plt.plot([3,8,5,2,9],
             marker='d', 
             markerfacecolor='yellow', 
             markersize=10, 
             markevery=[1,2,4])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/ec14f690-335e-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>对照图示结果，体会上述几个参数的效果，特别是 markevery，它是按照点的顺序指定坐标点的，如上即为第 1 个、第 2 个和第 4 个点，还要注意，计数是从 0 开始的。</p>
<ul>
<li>data：用这个参数可以声明数据来源，也就是可以这样作图。</li>
</ul>
<pre><code class="python language-python">  import pandas as pd
  df = pd.DataFrame({"col1":[1,2,3,4,5,6], 'col2':[9,3,8,1,5,3], 'col3':[10,8,1,5,7,3]})
  plt.plot('col1', 'col2', data=df, marker='D')    #⑥
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0f31ea70-335f-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>语句 ⑥ plt 的参数中，分别用字符串 'col1' 和 'col2' 表示坐标系中的 x 和 y 轴数据集，而它们是数据集 df 的两个特征。数据来源，则用 data 参数指明（data=df）。这充分显示了 Pandas 和 Matplotlib 的融洽，如果没有理解 Pandas，请参阅《跟老齐学Python：数据分析》，里面有深入浅出地讲解。</p>
<p>而事实上，Pandas 的数据对象也有绘图方法。</p>
<pre><code class="python language-python">df.plot('col1', 'col2')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5801bf50-335f-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>对于 Pandas 对象的绘图方法，与前面的使用方式基本一样，只不过是某个 Pandas 的方法罢了，这里不重复说明。</p>
<p>如果注意观察上图，发现它比以往的图多了一个东西，右上角的那个。</p>
<h3 id="133">1.3.3 图例</h3>
<p>在可视化的图示中，把类似上图右上角的那个东西，称为图例。比如，在地图中，图例就非常清楚地标明了图中表示首都、城市、公路、铁路等各用什么符号。</p>
<p>使用 Pandas 对象的绘图方法，会自动生成图例，这是非常友好的，再体会一番。</p>
<pre><code class="python language-python">df = pd.DataFrame({"col1":[1,2,3,4,5,6], 'col2':[9,3,8,1,5,3], 'col3':[10,8,1,5,7,3]})
df.plot()
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7b136890-335f-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>如果不用这种自动的方式，就要使用 plt.legend 生成图例。</p>
<pre><code class="python language-python">a = np.arange(0, 3, .02)
b = np.arange(0, 3, .02)
c = np.exp(a)
d = c[: : -1]
plt.plot(a, c, 'k--', label="Model")
plt.plot(a, d, 'r:', label="Data")
plt.plot(a, c+d, 'b-', label="Total")
plt.legend(loc='upper right')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/8f3389e0-335f-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>这次不仅用 plt.legend 函数生成了图例，还给函数提供了参数 loc='upper right'，通过它指定了图例的位置。在图像中，图例的位置有如下几种，并且每种位置都有相应的数字表示，在使用的时候，可以用“名称”字符串，也可以用“编号”整数。</p>
<table>
<thead>
<tr>
<th>名称</th>
<th>编号</th>
<th>名称</th>
<th>编号</th>
</tr>
</thead>
<tbody>
<tr>
<td>best</td>
<td>0</td>
<td>center   left</td>
<td>6</td>
</tr>
<tr>
<td>upper   right</td>
<td>1</td>
<td>center   right</td>
<td>7</td>
</tr>
<tr>
<td>upper   left</td>
<td>2</td>
<td>lower   center</td>
<td>8</td>
</tr>
<tr>
<td>lower   left</td>
<td>3</td>
<td>upper   center</td>
<td>9</td>
</tr>
<tr>
<td>lower   right</td>
<td>4</td>
<td>center</td>
<td>10</td>
</tr>
<tr>
<td>right</td>
<td>5</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>如果 loc=0，Matplotlib 会自动根据情况找到最佳的图例位置。</p>
<p>在刚才的程序中，不知不觉就使用了另外一种绘图方式，没有面向对象，目的是要提醒注意，这种方式也要熟悉哦。</p>
<p>图例在坐标系围成的图像之内，这是通常情况。有些特殊情况下，可能要求图例放在其他位置，甚至排列方式也可以变化（默认都是纵向排列的）。</p>
<pre><code class="python language-python">plt.plot([0,1,2,3,4,5], label="positive")
plt.plot([5,4,3,2,1,0], label="negative")
plt.legend(bbox_to_anchor=(0, 1), loc=3, ncol=2)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b4ecd380-335f-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>因此，有时间还是要了解 plt.legend 的其他参数，<a href="https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html">更多内容可以阅读这里</a>。</p>
<p>阅读材料的确不少，这都在说明 Matplotlib 博大精深，值得学习。虽然很多阅读材料都是英文的，并且充满了专业术语，刚开始会有些不熟练，只要持之以恒，就不会感到困难了。</p>
<h3 id="134">1.3.4 移动坐标轴</h3>
<p>先看下面的程序，“温故”和“知新”同时具有：</p>
<pre><code class="python language-python">X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-")
plt.plot(X, S, color="green", linewidth=1.0, linestyle="-.")
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], 
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])    #⑦
plt.yticks([-1, 0, +1], [r'$-1$', r'$0$', r'$+1$'])
plt.tick_params(axis='both', labelsize=18, colors='red')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e22c3b10-335f-11e9-b3a9-4f8760d3237f" width = "50%" /></p>
<p>语句 ⑦ 貌似用了新的函数 plt.xticks，其实不然，以前用过 ax.set_xticks 方法，两者是在不同应用模式下的同一个功能。只不过在 ⑦ 中，除了规定横坐标的主刻线位置（[-np.pi, -np.pi/2, 0, np.pi/2, np.pi]）之外，还规定了主刻线的标示显示方式（[r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$']）。plt.yticks 与此同样含义。</p>
<p>看着这张图，其实并不能满足需要，因为从数学的习惯而言，我们希望坐标原点应该在图像中间，即 x=0 和 y=0 的交点为坐标原点。</p>
<pre><code class="python language-python">X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-")
plt.plot(X, S, color="green", linewidth=1.0, linestyle="-.")
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], 
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([-1, 0, +1], [r'$-1$', r'$0$', r'$+1$'])
plt.tick_params(axis='both', labelsize=18, colors='red')

#在前面已有代码基础上增加下面的内容
ax = plt.gca()  # ⑧
ax.spines['right'].set_color('none')    #⑨
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')    #⑩
ax.spines['bottom'].set_position(('data',0))    #⑪
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))    #⑫
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/595d6240-3360-11e9-ae61-ab46ecd2ee1c" width = "50%" /></p>
<p>对这个结果还是相当满意的。不能满足于此，还要知其所以然。</p>
<p>⑧ 中的 plt.gca 函数的作用是获得当前的坐标系对象。在此语句之前，没有创建坐标系对象，是通过执行 plt 的函数完成各种操作。后面要用坐标系对象的方法和属性完成各种操作了，就要获得当前的坐标系对象。“gca”的含义就是“get current axis”。</p>
<p>⑨ 中的 ax.spines 是坐标系对象四周的边线。</p>
<pre><code class="python language-python">ax.spines

# out
OrderedDict([('left', &lt;matplotlib.spines.Spine at 0x11ff95780&gt;),
             ('right', &lt;matplotlib.spines.Spine at 0x11ff95ef0&gt;),
             ('bottom', &lt;matplotlib.spines.Spine at 0x11ff95518&gt;),
             ('top', &lt;matplotlib.spines.Spine at 0x11f7f7b38&gt;)])
</code></pre>
<p>ax.spines 的值是一个类字典对象，通过类似 ax.spines['right'] 的样式得到相应的边线对象。⑨ 的含义就是将右边的边线颜色设置为 'none'，即没有颜色，不显示了。同理也设置了上面的边线为不显示。</p>
<p>⑩ 中的 ax.xaxis 显然是获得x轴，前面已经明确过了，坐标轴上有刻度（包含刻线和标示）。接下来的 set_ticks_position 方法就是设置表示刻度的位置，对于 x 轴而言，参数可选值为：{'top', 'bottom', 'both', 'default', 'none'}。这里使用了 'bottom'，显然是要把刻度置于底端。其实，如果没有 ⑩，那么刻度会位于默认值规定的位置，即刻线在上下边线，标示只在下边线。</p>
<p>⑪ 的作用就是要移动下边线（ax.spines['bottom']），把它作为 x 轴，移动到 y=0 的位置。set_position 用来确定移动的目标位置，注意它的参数，是用元组形式，基本格式为：(position type, amount)。其中 position type 的值有：</p>
<ul>
<li>'outward'，字符串，表示要将坐标轴移动到坐标系图形范围之外，ammount 规定移动的像素数；</li>
<li>'axes'，字符串，将坐标轴移动到 Y 轴指定的位置，amount 的取值范围为 0.0 ~ 1.0；</li>
<li>'data'，字符串，将坐标轴移动到由坐标指定的位置，amount 是具体的坐标位置。</li>
</ul>
<p>由此可知 ax.spines['bottom'].set_position(('data',0)) 的意思就是将下边线移动到 y=0 的位置。而当参数是 ('data', 0) 的时候，还可以用 'zero' 替代。于是乎 ⑫ 就这么做了。</p>
<p>如此，实现了坐标轴移动。</p>
<h3 id="">总结</h3>
<p>本课主要学习了如下内容：</p>
<ul>
<li>实现图像对象中的分区，subplots、fig.add_axes、GridSpec、fig.add_subplot；</li>
<li>对绘制的曲线进行多种属性配置，plt.plot、ax.plot；</li>
<li>图例的生成和位置控制，ax.legend；</li>
<li>坐标轴位置的设置，ax.spines、ax.spines['bottom'].set_position(('data',0))。</li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>