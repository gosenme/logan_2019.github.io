---
title: 案例上手 Python 数据可视化-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一课，已经了解了基本的绘图方法，特别是熟悉了如何对坐标系做各种各样的设置，那是可视化的基础。本课要在上一课内容的基础上，进一步丰富坐标系内图像的设置。</p>
<blockquote>
  <p>注意，没有使用曲线这个词，显然包括但不限于曲线。</p>
</blockquote>
<h3 id="141">1.4.1 标注</h3>
<p>如果在坐标系中绘制了多条曲线，会用图例表示出每条曲线的含义，这是一种区分方式；另外一种方式是直接对每条曲线进行标注，或许这样更直接明了。此外，有时候对于坐标系中某些特殊点也会进行标注。</p>
<pre><code class="python language-python">%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 10, 0.005)
y = np.exp(-x/2) * np.sin(2*np.pi*x)

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position('zero')

#以下标注
x1 = 1.25
y1 = np.exp(-x1/2) * np.sin(2*np.pi*x1)
ax.scatter([x1,], [y1,], 50, color='blue')    #①
ax.plot([x1, x1], [0, y1], color='blue', linewidth=2.5, linestyle="--")    #②
ax.plot([0, x1], [y1, y1], color='blue', linewidth=2.5, linestyle='--')    #③

ax.annotate(r'$e^{-\frac{x}{2}}sin(2\pi{x}), x=1.25$',     
             xy=(x1, y1), xycoords='data',  
             xytext=(+30, +0.6), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="-&gt;", connectionstyle="arc3,rad=.2"))    #④
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/930186c0-33ec-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>先看输出的结果，相比以往绘制的类似图，此处做了两处改变，一处是坐标系，现在把 x 轴设置到了 y=0 的位置，这种设置方法的解释请参考上一课的内容；另外一处是增加了标注，即图中看到的，除了曲线和坐标轴之外，都属于标注的部分。这些内容是通过代码中写有注释的那一行以下的代码实现的，一共4行，下面逐一进行解释。</p>
<p>① 的目的在于呈现图中的坐标点，即那个蓝色的圆点。scatter 是实现散点图的方法（函数），后面会对此进行详细讲解。请注意这里的参数 [x1,], [y1,]。如果用数学方式表示，应该画出的点是 (x1, y1)，这是一个坐标点。scatter 方法的参数跟以前学习过的 plot 一样，都要输入表示横轴的数据集和表示纵轴的数据集，那么，就要把 x1 和 y1 分别放到两个序列中，于是就有了参数 [x1,], [y1,]。</p>
<p>② 和 ③ 的作用就从坐标点 (x1, y1) 分别向 x 轴、y 轴画出垂直的虚线。</p>
<p>④ 是标注文字说明，此处使用 ax.annotate 方法，也可以用 plt.annotate 函数。</p>
<ul>
<li>r'$e^{-\frac{x}{2}}sin(2\pi{x}), x=1.25$'：这是所显示的内容，在 Matplolib 中，支持 LaTex 编辑显示公式。</li>
<li>xy=(x1, y1)：说明被标注点的坐标。</li>
<li>xycoords='data'：标注内容指向的点，默认值是 'data'，也可以选其他值，<a href="https://matplotlib.org/api/_as_gen/matplotlib.pyplot.annotate.html">更多内容请阅读这里</a>。</li>
<li>xytext=(+30, +0.6)：上述文本内容的显示位置。</li>
<li>arrowprops=dict(arrowstyle="-&gt;", connectionstyle="arc3,rad=.2")：箭头的设置。</li>
</ul>
<p>在坐标系内能够绘制的图像，除了曲线之外，还有很多其他类型的图像，如散点图。</p>
<h3 id="142">1.4.2 散点图</h3>
<p>散点图很重要，是因为在科学研究中，特别是规律探索的过程中，散点图是一种常用的图像。通常发现科学规律的过程是这样进行的：</p>
<ul>
<li>设计实验，通过实验测量得到数据；</li>
<li>将数据在坐标系内做散点图；</li>
<li>观察散点图的特点，推断可能的函数关系，即规律；</li>
<li>再用实验验证规律是否正确，也包括理论上的检验，总之，只要没有发现不符合上述规律的实验数据，就姑且认为该规律是成立的。</li>
</ul>
<p>当然，上面的过程是以得到一个函数为例说明，有时候画出散点图，或许也不是为了得到某一个函数。</p>
<p>那么，散点图怎么画？</p>
<p>前面已经剧透过了，scatter 就是用来画散点图的方法。</p>
<pre><code class="python language-python">n = 1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0,1,n)
plt.scatter(X,Y)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7a63e1b0-33ee-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>X、Y 是符合高斯分布的数据（np.random.normal() 随机生成符合高斯分布的数字集），然后用 plt.scatter() 做散点图，从图中可以直观地看到数据的分布，这正是高斯分布的特点。</p>
<pre><code class="python language-python">plt.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, edgecolors=None, *, data=None, **kwargs)
</code></pre>
<p>scatter 的参数中除了 x，y 必不可少的之外，还有其他很多参数，在后面的绘图中，会用到一些。</p>
<pre><code class="python language-python">import pandas as pd
cities = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/jiangsu/city_population.csv")
cities

#out
    name    area    population  longd   latd
0    南京市 6582.31 8004680 118.78  32.04
1    无锡市 4787.61 6372624 120.29  31.59
2    徐州市 11764.88    8580500 117.20  34.26
3    常州市 4384.57 4591972 119.95  31.79
4    苏州市 8488.42 10465994    120.62  31.32
5    南通市 8001.00 7282835 120.86  32.01
6    连云港市    7615.29 4393914 119.16  34.59
7    淮安市 9949.97 4799889 119.15  33.50
8    盐城市 16972.42    7260240 120.13  33.38
9    扬州市 6591.21 4459760 119.42  32.39
10    镇江市 3840.32 3113384 119.44  32.20
11    泰州市 5787.26 4618558 119.90  32.49
12    宿迁市 8555.00 4715553 118.30  33.96
</code></pre>
<p>从数据集中读入上述数据，<a href="https://github.com/qiwsir/DataSet/blob/master/jiangsu/city_population.csv">可以点击这里下载</a>。</p>
<p>变量 cities 引用的数据集是江苏省各个城市的名称、人口、面积和经纬度数据。下面就要通过可视化的方式，把这些特征体现出来。</p>
<pre><code class="python language-python">lat = cities['latd']
lon = cities['longd']
population = cities['population'],
area = cities['area']

plt.scatter(lon, lat, label=None, c=np.log10(population)[0], cmap="viridis", s=area/10, linewidths=0, alpha=0.5)    
plt.axis(aspect='equal')
plt.xlabel("longitude")
plt.ylabel('latitude')
plt.colorbar(label='log$_{10}$(population)')    

for area in [10, 30, 50]:
    plt.scatter([], [], c='k', alpha=0.3, s=area, label=str(area) + ' km$^2$')

plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='City Area')
plt.title('江苏省各城市面积和人口')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/bc66d680-33ee-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>此处是按照经纬度来绘制散点图的，因此，各个城市在上图中的位置，应该跟实际地图中的位置一样的。为了对比，请看江苏省的地图。</p>
<p><img src="https://images.gitbook.cn/dac09d00-33ee-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>对比上下两张图，一定会为自己绘制的散点图所折服的。</p>
<p>在心理美滋滋之后，对关键语句进行介绍。</p>
<ul>
<li><p>plt.scatter(lon, lat, label=None, c=np.log10(population)[0], cmap="viridis", s=area/10, linewidths=0, alpha=0.5) ：这是绘制散点图的基本函数。scatter 参数众多，这里涉及一些，为了理解此行代码，适当解释几个参数。</p>
<ul>
<li>c：设置颜色。在此处使用的值是 np.log10(population)[0]，因为各个城市 population 数值较大，用对数对原值进行转换。注意，np.log10(population) 的结果是一个形状为 (13, 1) 的数组，因此要以 np.log10(population)[0] 的方式获得每个城市所对应的色彩，严格来讲只是建立了与色彩的映射关系，具体的色彩还要由 cmap 决定。</li>
<li>cmap：当用浮点数设置了参数 c 的值之后，就可以根据此处设置的色彩谱得到相应的色彩。</li>
<li>s：设置每个点的大小，还是考虑到 area 数值有点大，因此除以 10。</li>
<li>linewidths：设置每个点外周的线的粗细。</li></ul></li>
<li><p>plt.colorbar(label='log$_{10}$(population)')：这也是一个新面孔，它的作用是生成了图中右侧的数据光谱。</p></li>
</ul>
<p>对于散点图而言，其中的“点”，除了可以是圆点之外，还可以是别的形状的。比如，下面的代码来自于<a href="https://matplotlib.org/gallery/lines_bars_and_markers/scatter_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-symbol-py">官方网站的示例</a>。</p>
<pre><code class="python language-python">np.random.seed(19680801)

x = np.arange(0.0, 50.0, 2.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
s = np.random.rand(*x.shape) * 800 + 500

plt.scatter(x, y, s, c="g", alpha=0.5, marker=r'$\clubsuit$',
            label="Luck")
plt.xlabel("Leprechauns")
plt.ylabel("Gold")
plt.legend(loc='upper left')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/3b20dac0-33ef-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>原来的“点”变成了上图中的“树”，其原因就是 scatter 函数中的 maker 参数，通过设置其值，能够实现不同形状的“散点”。其他的值可以在官方网站的页面中得到，<a href="https://matplotlib.org/api/markers_api.html#module-matplotlib.markers">可点击这里获取</a>。</p>
<p>对于散点图而言，除了在正交的直角坐标系中绘制之外，可能有时候也会在极坐标系中绘制，其他图像也有此可能，但是因为不常用，因此在前面未提及。而散点图，对于极坐标系则是一种比较常见的需要。</p>
<pre><code class="python language-python">np.random.seed(19680801)

# 点的面积和色彩
N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2
colors = theta

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar') 
ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/80e14cc0-33ef-11e9-b59c-dfe60266e7ff" width = "70%" /></p>
<p>极坐标系是通过 fig.add_subplot(111, projection='polar') 里的参数 projection='polar' 建立的，其他方面则与之前的正交坐标系一致了。</p>
<p>虽然这里能够画出色彩斑斓的散点图了，但是，要注意，并不是什么时候都要这样画图的。为每个点或者某些点标明色彩，其实是为了分类，如果没有这种需要，并且是要处理大量数据，推荐使用另外一个——plt.plot。</p>
<p>前面用这个函数绘制的都是曲线，如何用它来绘制散点图？</p>
<pre><code class="python language-python">df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/xsin/xsin.csv")
plt.plot(df.x, df.y, 'Dr')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/adcfd530-33ef-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>本例中的数据集来自于：<a href="https://github.com/qiwsir/DataSet/tree/master/xsin/xsin.csv">https://github.com/qiwsir/DataSet/tree/master/xsin/xsin.csv</a>。</p>
<p>这样绘制出来的散点图，因为没有对各个点进行单独渲染，所以在处理大数据的时候，速度就快多了。</p>
<h3 id="">总结</h3>
<p>本课是在前一课的基础上，进一步丰富了在坐标系中绘制的图像。</p>
<ul>
<li>对曲线做标注：ax.annotate</li>
<li>绘制散点图：ax.scatter</li>
<li>创建极坐标系：fig.add_subplot(111, projection='polar') </li>
<li>用 plt.plot 针对大量数据做散点图</li>
</ul>
<blockquote>
  <p>特别提醒，因为每个函数都有很多参数，在使用的时候，一定要勤查阅官方文档，从中了解参数的控制对象和效果。</p>
</blockquote>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>