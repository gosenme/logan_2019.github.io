---
title: 案例上手 Python 数据可视化-26
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Bokeh 与以往的绘图工具类似，不同之处在于，前面的工具都是以绘制统计图，通常会直接提供专门绘制统计图的函数，但是 Bokeh 中提供的图线模型，是以常见的几何图形或者曲线为主，同时能够用它们绘制常见的统计图。从这点来说，Bokeh 更捉住了数据可视化的未来发展——不局限于统计图范畴。</p>
<p>下面就列举几种图形或曲线的绘制方法（这些方法在<a href="https://bokeh.pydata.org/en/latest/docs/reference/plotting.html">官方文档</a>中都有详细说明），读者可以从中体会 Bokeh 的特点。</p>
<p>为了将图形插入到 Jupyter 浏览器中，先执行下述代码：</p>
<pre><code class="python language-python">from bokeh.plotting import output_notebook
output_notebook()
</code></pre>
<p>这样做便于调试和学习，而在以后的商业项目中是否如此操作，要看具体要求。</p>
<h3 id="621">6.2.1 饼图</h3>
<p>饼图，是常见的一种统计图，很多工具都提供了专用方法，如 pyecharts 中的 Pie 类，但是在 Bokeh 中没有专门方法或类。</p>
<p>如果把饼图看做“圆形”，倒是 Bokeh 中有相应的基本模型。</p>
<pre><code class="python language-python">from bokeh.plotting import figure, show

fig = figure(plot_width = 500, plot_height = 300)
fig.circle(x = [1, 2, 3, 4, 5],
           y = [1, 2, 3, 4, 5],
           size = 20,
           #angle = 45,
           fill_color = 'yellow',
          )
show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c3ac3220-4abc-11e9-9c67-45765652785b" width = "70%" /></p>
<p>fig.circle 方法是以指定的坐标点为圆心，绘制圆（fill_color='white'）或者圆面。此方法适合于对各个坐标点以圆（面）表示，但不能用它来画出包含不同比例的扇形图。</p>
<p>跟 fig.circle 类似的还有好几个，如 circle_cross、circle_x、cross 等。下面要演示的 fig.annulus，是专门用来绘制圆环图形的，可以实现类似上图的效果，也可以绘制一个圆环。</p>
<pre><code class="python language-python">fig = figure(plot_width = 500, plot_height = 300)
fig.annulus(x=[3], y=[3], color='green', inner_radius=0.2, outer_radius=0.6)
show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e5b285e0-4abc-11e9-b468-dd988901e5fa" width = "70%" /></p>
<p>当然，对于此图而言，如果不想显示坐标轴和坐标网格，可以通过对 figure 函数的参数设置实现。请学习者自行阅读文档并完成。</p>
<p>至此，还没有找到绘制饼图的方法，继续找。</p>
<p>有一个名为 wedge 的方法，从名称上看，wedge 有“楔形”的含义。饼图中的每个扇形图，也就是“楔形”，因此这个方法值得研究—— Python 中的函数、变量、类的命名原则是“望文生义”，寻找实现某个功能的函数 / 方法，一定要将“名称”作为重要线索。</p>
<p>如果把 wedge 列为疑似对象，就应该仔细审查一下它，看看它的参数。或许读者已经敏锐地捕捉到两个以往没有出现的参数 <strong>start_angle、end_angle</strong>，那就来试一试。</p>
<pre><code class="python language-python">import numpy as np

fig = figure(plot_width = 500, plot_height = 300)
fig.wedge(x=[3,], y=[3,], 
          radius=80, 
          start_angle=0, 
          end_angle=np.pi/2, 
          radius_units="screen", 
          color="#2b8cbe")
show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/44860920-4abd-11e9-b468-dd988901e5fa" width = "70%" /></p>
<p>参数 start_angle 和 end_angle 分别是扇面的起、止半径线段相对水平方向的角度，并且默认是逆时针旋转。</p>
<p>这里绘制了一个扇形，按理说，能绘制一个，就能绘制另外一个，这样组合而成，就是可以分别用不同扇形表示不同比例了。</p>
<pre><code class="python language-python"># 定义每个扇形的起止半径相对水平线的角度
percents = [0, 0.3, 0.4, 0.6, 0.9, 1]
starts = [p*2*np.pi for p in percents[:-1]]
ends = [p*2*np.pi for p in percents[1:]]

# 每个扇形的色彩
colors = ["red", "green", "blue", "orange", "yellow"]

fig = figure(title='Pie Chart', x_range=(-1,1), y_range=(-1,1))
fig.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)
show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/242a29b0-4ac0-11e9-9c67-45765652785b" width = "55%" /></p>
<p>此图，就是我们所要的饼图。当然，如果要在上面标示有关说明，可以通过其他方式进行。原理上来说，这样就实现了饼图。</p>
<p>看到这里，肯定会觉得用 Bokeh 绘制饼图太麻烦了。因此，就不要用 Bokeh 绘制饼图了，用 pyecharts 吧。这说明，不同工具有不同的优势，有不同的主攻方向。就如同吃饭用具一样，筷子是能做不少事情，但是并不是什么地方都能做得最好。因此，有必要多学一些工具——这也是本课的目的，才能临阵不乱，从容选择最适合的。</p>
<h3 id="622">6.2.2 多边形</h3>
<p>在 Bokeh 中不缺乏绘制多边形的方法，如不规则多边形、四边形、三角形等。</p>
<p>先看比较简单的三角形，而且是正三角形。</p>
<pre><code class="python language-python">from bokeh.plotting import figure, show

fig = figure(plot_width=300, plot_height=300)
fig.triangle(x=[3], y=[3], size=[100],
              color="#666666", line_width=2)

show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c5550350-4ac0-11e9-816f-a94bb1ffd325" alt="enter image description here" /></p>
<p>虽然这样绘制了正三角形，其实，fig.triangle 是标记坐标点的符号，跟前面用过的 fig.circle 等是一样的，只不过在上面的例子中只给了一个点 [3, 3] 罢了，如果是下面这样，就熟悉了。</p>
<pre><code class="python language-python">from bokeh.plotting import figure, show

fig = figure(plot_width=300, plot_height=300)
fig.triangle(x=[1, 2, 3], y=[1, 2, 3], size=[10, 30, 20],
              color="#666666", line_width=2)
fig.line(x=[1,2,3], y=[1,2,3])
show(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/dac7bc50-4ac0-11e9-816f-a94bb1ffd325" alt="enter image description here" /></p>
<p>除了绘制正三角形（符号）之外，还有绘制倒三角形的函数 inverted_triangle，使用方法与上述相同。</p>
<p>如果要自定义绘制图形，可以使用 patch 方法。</p>
<pre><code class="python language-python">from bokeh.plotting import figure, show
p = figure(plot_width=300, plot_height=300)
p.patch(x=[1, 3, 2], y=[1, 2, 3], color="#090909")
show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e821b450-4ac0-11e9-95d4-c9806df1e112" alt="enter image description here" /></p>
<p>这里得到了一个锐角三角形，三角形的三个顶点坐标分别是 (1, 1)、(3, 2)、(2, 3)。p.patch 方法的参数 x、y 分别对象三角形顶点坐标的 X 轴和 Y 轴的值。与此类似，如果确定了平面直角坐标系中任意一个多边形的各个顶点坐标，就可以绘制出相应的多边形，如下所示。</p>
<pre><code class="python language-python">p = figure(plot_width=300, plot_height=300)
p.patch(x=[1, 1, 1.5, 3, 2.5], y=[1, 2, 2, 3,2], color="red")
show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/001dfe60-4ac1-11e9-9c67-45765652785b" alt="enter image description here" /></p>
<p>与 patch 类似的另外一个方法名为 patches，它是复数形式，我们推测是不是可以绘制多个图形。</p>
<p>正解！</p>
<pre><code class="python language-python">p = figure(plot_width=300, plot_height=300)
p.patches(xs=[[1,1,3],[1,3,5,3]], 
          ys=[[1,2,1],[2,2,4,4]],
          color=["gray", "#010199"])
show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0c5129a0-4ac1-11e9-95d4-c9806df1e112" alt="enter image description here" /></p>
<p>请仔细观察 p.patches 方法的参数，跟前面的 p.patch 有所不同，这里使用的是 xs、ys，意即可以通过这两个参数向 p.patches 提供多个不同多边形的顶点。注意观察上述代码，参数的值是嵌套列表。</p>
<p>虽然 patch 和 patches 能够绘制任何多边形，但是某些特殊多边形，因其常用，Bokeh 又提供了单独的方法，比如上面的正三角形，还有下面要演示的矩形。</p>
<pre><code class="python language-python">plot = figure(plot_width=300, plot_height=300)
plot.quad(top=[2, 3, 4], bottom=[1, 2, 3], left=[1, 2, 3],
          right=[1.2, 2.5, 3.7], color="#B3DE69")
show(plot)
</code></pre>
<p><img src="https://images.gitbook.cn/1be45350-4ac2-11e9-9c67-45765652785b" alt="enter image description here" /></p>
<p>在 quad 方法中，参数 top、bottom、right、left 分别为该矩形的“上、下、右、左”的边界位置。例如 top=[2, 3, 4]，其含义是：</p>
<ul>
<li>第一个矩形的上边界是 y=2 的直线；</li>
<li>第二个矩形的上边界是 y=3 的直线；</li>
<li>第三个矩形的上边界是 y=4 的直线。</li>
</ul>
<p>如此，通过设置每个矩形的四边界限（分界“线”），最终确定了一个矩形。</p>
<p>quad 方法除了可以绘制如上面那样的矩形之外，还有另外一个用途——Bokeh 必须如此，那就是绘制表示数据分布的直方图——再次提醒，直方图和柱形图是完全不同的。前面介绍的其他制图工具，有的提供了专门绘制直方图的方法（函数），例如 Seaborn 中的 sns.distplot。但是 Bokeh 中没有专门函数，不得不使用 quad 实现直方图。</p>
<pre><code class="python language-python">mu = 0
sigma = 0.5
measured = np.random.normal(mu, sigma, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)    # ①

p = figure(title='直方图')
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],     # ②
       fill_color='navy', line_color='white', alpha=0.5)
show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7283ec70-4ac2-11e9-95d4-c9806df1e112" width = "70%" /></p>
<p>虽然 Bokeh 中没有专门的直方图方法，借助 np.histogram（①）函数——返回每个小矩形的高度和左右边界值，即 hist、bin_edges ——依然能绘制直方图。</p>
<p>于是，② 中 quad 的参数 top 的值当然为 hist。由于每个小矩形的底部都是从 y=0 开始，因此 bottom = 0。需要留心的是 left 和 right，edges 是从左向右每个小矩形的边界，所以 left = edges[:-1]，同理设置 right = edges[1:]。</p>
<p>如果将上述程序再延伸，还可以画出正态分布的核函数。</p>
<pre><code class="python language-python">mu = 0
sigma = 0.5

measured = np.random.normal(mu, sigma, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)

p = figure(title='直方图')
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], 
       fill_color='navy', line_color='white', alpha=0.5)

x = np.linspace(-2, 2, 1000)
pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7)

show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9e83cf20-4ac2-11e9-816f-a94bb1ffd325" width = "70%" /></p>
<p>如果研究 Bokeh 的<a href="https://bokeh.pydata.org/en/latest/docs/reference/plotting.html">官方文档</a>，我们还能找到一个绘制矩形的方法—— rect。</p>
<pre><code class="python language-python">plot = figure(plot_width=300, plot_height=300)
plot.rect(x=[3, 5], 
          y=[3, 15], 
          width=100, 
          height=20, 
          fill_color='white', 
          color=['red', 'blue'])
show(plot)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b04dcb70-4ac2-11e9-b468-dd988901e5fa" alt="enter image description here" /></p>
<p>在 plot.rect 中，以参数 x、y 规定了每个矩形的中心，然后参数 width、height 分别设置矩形的长宽（高）。显然这个方法适合于绘制某些矩形，而不适合于绘制诸如上面的直方图那样的矩形。</p>
<p>通过上述的讲解，对 Bokeh 的制图方法已经有了比较完整的理解，当然，还有很多函数此处没有介绍，但使用方法都大同小异。</p>
<h3 id="623">6.2.3 分析民航的数据</h3>
<p>本示例的数据来源：</p>
<blockquote>
  <p><a href="https://github.com/qiwsir/DataSet/tree/master/flights/nycflights.csv">https://github.com/qiwsir/DataSet/tree/master/flights/nycflights.csv</a></p>
</blockquote>
<p>此数据集包含航班的记录（<a href="https://towardsdatascience.com/data-visualization-with-bokeh-in-python-part-one-getting-started-a11655a467d4">以下示例可点击这里参考</a>）。</p>
<pre><code class="python language-python">import pandas as pd
flights = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/flights/nycflights.csv", index_col=0)
flights.info()

# output
&lt;class 'pandas.core.frame.DataFrame'&gt;
Int64Index: 336776 entries, 0 to 336775
Data columns (total 20 columns):
year              336776 non-null int64
month             336776 non-null int64
day               336776 non-null int64
dep_time          328521 non-null float64
sched_dep_time    336776 non-null int64
dep_delay         328521 non-null float64
arr_time          328063 non-null float64
sched_arr_time    336776 non-null int64
arr_delay         327346 non-null float64
carrier           336776 non-null object
flight            336776 non-null int64
tailnum           334264 non-null object
origin            336776 non-null object
dest              336776 non-null object
air_time          327346 non-null float64
distance          336776 non-null int64
hour              336776 non-null int64
minute            336776 non-null int64
time_hour         336776 non-null object
name              336776 non-null object
dtypes: float64(5), int64(9), object(6)
memory usage: 54.0+ MB
</code></pre>
<p>此处，我们重点研究的是航班的延迟情况，即特征“arr_delay”的数据。</p>
<pre><code class="python language-python">flights['arr_delay'].describe()

# output
count    327346.000000
mean          6.895377
std          44.633292
min         -86.000000
25%         -17.000000
50%          -5.000000
75%          14.000000
max        1272.000000
Name: arr_delay, dtype: float64
</code></pre>
<p>航班延迟的最小值是 ﹣86 分钟，意味着提前到了。最大值是 1272 分钟，即 21.2 小时——乘此航班，需要准备充足。</p>
<p>如果认为迟到时间太长的为离群值，那么可以用箱线图比较直观地看看这个特征下离群值的分布。但是 Bokeh 中也没有直接绘制箱线图的方法，显然不如前面介绍的工具方便。那么，是否我们非要用 Bokeh 实现箱线图呢？非也。我的建议是，要用适合的工具。既然 Bokeh 没有，我就用适合绘制箱线图的工具——没有必要钻牛角尖。</p>
<pre><code class="python language-python">%matplotlib inline
import seaborn as sns
sns.boxplot(y="arr_delay", data=flights,)
</code></pre>
<p><img src="https://images.gitbook.cn/1643efe0-4ac3-11e9-95d4-c9806df1e112" alt="enter image description here" /></p>
<p>这个结果说明，离群值很多哦。如果注意分析前面的描述性统计发现，下四分位（75%）的值是 14 分钟。</p>
<p>如果仿照前面的直方图，看看这些数据的基本分布，从而更清楚迟到时间的概况。</p>
<pre><code class="python language-python">hist, edges = np.histogram(flights['arr_delay'], bins=int(180/5), range=[-60, 300])
p = figure(plot_height=600, plot_width=600, 
           title="arrive delays", 
           x_axis_label='Delay(min)',
           y_axis_label='Number of Flights'
          )
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
       fill_color='red', line_color='black',
      )
show(p)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/21134560-4ac3-11e9-816f-a94bb1ffd325" width = "60%" /></p>
<p>这个图显示了一种“长尾效果”，从中可以看到飞机到达的时间分布。</p>
<p>回到上述操作中，似乎并没有觉得 Bokeh 有什么优势，它似乎是一个鸡肋。如果仅仅从本例绘制的统计图，的确有如此感觉。在直接绘制这些常规统计图上，用以往的工具都可以完成，而且更直接。既然如此，<strong>Bokeh 的特色在哪里？它存在的理由是什么？</strong></p>
<p>请继续往下看。</p>
<pre><code class="python language-python">from bokeh.models import ColumnDataSource, HoverTool

hist, edges = np.histogram(flights['arr_delay'], bins=int(180/5), range=[-60, 300])

delays = pd.DataFrame({'flights': hist, 
                       'left': edges[:-1], 
                       'right': edges[1:]})
delays['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(delays['left'], delays['right'])]
delays['f_flights'] = hist
src = ColumnDataSource(delays)

p = figure(plot_height=600, plot_width=600, 
           title="arrive delays", 
           x_axis_label='Delay(min)',
           y_axis_label='Number of Flights'
          )
p.quad(source=src, bottom=0, top='flights', left='left', right='right',
       fill_color='red', line_color='blue',
       hover_fill_alpha = 1.0,
       hover_fill_color = 'navy',
      )
hover = HoverTool(tooltips=[('Delay', '@f_interval'),
                            ('Num of Flights', '@f_flights')
                           ])
p.add_tools(hover)
show(p)
</code></pre>
<p>输出结果：（鼠标移动到任何一个小矩形上）</p>
<p><img src="https://images.gitbook.cn/5418a450-4ac3-11e9-816f-a94bb1ffd325" width = "60%" /></p>
<p>这才是 Bokeh 的特色——<strong>交互性</strong>。</p>
<p>对上述程序的理解，建议参照官方文档——下一课重点介绍交互性操作。</p>
<h3 id="624">6.2.4 小结</h3>
<p>本课介绍了 Bokeh 的常规绘图方法，特别是 bokeh.plotting 提供的各种绘图接口（方法），是实现常规作图的基本模型——比以往的工具更灵活。当然，这不是重点，重点是要学会根据需要选工具。最后我们对 Bokeh 的交互性特色进行了解释。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>