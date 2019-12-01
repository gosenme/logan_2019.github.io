---
title: 案例上手 Python 数据可视化-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课将继续学习其他类型的统计图，有了上一课的基础，学习下面的内容就比较容易了。不同类型的统计图，只是生成 Trace 对象的类的名称变化一下，其参数的调用方式大同小异。因此，当本课介绍几种统计图时，可能就不如以往那么细致，如果读者想要详细了解某些细节，就需要亲自阅读文档——这种方法是必须要掌握的。</p>
<h3 id="431">4.3.1 饼图</h3>
<p>继续使用上一课的数据集。</p>
<pre><code class="python language-python">import pandas as pd
import plotly as py
import plotly.graph_objs as go
py.offline.init_notebook_mode(connected=True)
df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/universityrank/timesData.csv")
</code></pre>
<p>用饼图统计入榜的中国大学 Top5。</p>
<pre><code class="python language-python">dfcn = df[df['country']=='China']
dfcn5 = dfcn.iloc[:5, :]
dfcn5
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>world_rank</th>
<th>university_name</th>
<th>country</th>
<th>teaching</th>
<th>international</th>
<th>research</th>
<th>citations</th>
<th>income</th>
<th>total_score</th>
<th>num_students</th>
<th>student_staff_ratio</th>
<th>international_students</th>
<th>female_male_ratio</th>
<th>year</th>
</tr>
</thead>
<tbody>
<tr>
<td>36</td>
<td>37</td>
<td>Peking University</td>
<td>China</td>
<td>76.4</td>
<td>68.6</td>
<td>61.3</td>
<td>72.2</td>
<td>98.6</td>
<td>70.7</td>
<td>40,148</td>
<td>8.3</td>
<td>14%</td>
<td>NaN</td>
<td>2011</td>
</tr>
<tr>
<td>49</td>
<td>49</td>
<td>University of Science and Technology of China</td>
<td>China</td>
<td>57.5</td>
<td>-</td>
<td>48.6</td>
<td>92.7</td>
<td>30.3</td>
<td>66.0</td>
<td>14,290</td>
<td>7.9</td>
<td>2%</td>
<td>NaN</td>
<td>2011</td>
</tr>
<tr>
<td>57</td>
<td>58</td>
<td>Tsinghua University</td>
<td>China</td>
<td>74.9</td>
<td>43.0</td>
<td>66.6</td>
<td>52.7</td>
<td>97.8</td>
<td>64.2</td>
<td>39,763</td>
<td>13.7</td>
<td>10%</td>
<td>32 : 68</td>
<td>2011</td>
</tr>
<tr>
<td>119</td>
<td>120</td>
<td>Nanjing University</td>
<td>China</td>
<td>52.2</td>
<td>50.2</td>
<td>46.2</td>
<td>66.0</td>
<td>43.4</td>
<td>54.6</td>
<td>29,743</td>
<td>13.3</td>
<td>10%</td>
<td>46 : 54</td>
<td>2011</td>
</tr>
<tr>
<td>170</td>
<td>171</td>
<td>Sun Yat-sen University</td>
<td>China</td>
<td>46.2</td>
<td>29.3</td>
<td>34.7</td>
<td>70.2</td>
<td>41.2</td>
<td>49.6</td>
<td>51,351</td>
<td>16.6</td>
<td>8%</td>
<td>51 : 49</td>
<td>2011</td>
</tr>
</tbody>
</table>
<p>我们计划统计各个学校在校生相对比例，但是，会发现“num_students”特征中的数据是字符串，不是数字。因此，需要对其进行转换。</p>
<pre><code class="python language-python">dfcn5['num_students']=dfcn5['num_students'].apply(lambda value: float(value.replace(",", "")))
dfcn5['num_students']

# out
36     40148.0
49     14290.0
57     39763.0
119    29743.0
170    51351.0
Name: num_students, dtype: float64
</code></pre>
<p>之后创建 go.Pie 的 Trace 实例对象，并绘制饼图。</p>
<pre><code class="python language-python">trace = go.Pie(values = dfcn5['num_students'],
               labels = dfcn5['university_name'],
               domain = {'x':[0, .5]},
               name = 'Number of Students Rates',
               hoverinfo = 'label + percent + name',
               hole = .3,
              )
layout = go.Layout(title = "Universities Number of Students Rates",
                   annotations = [
                       {'font':{'size':20},
                        'showarrow':False,
                        "text": "Number of Students",
                        'x':0.20,
                        'y':1
                       },
                   ]
                  )
figure = go.Figure(data=[trace], layout=layout)
py.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/3b287d50-46f2-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>go.Pie 也是有很多参数的，这里仅对上面用到的几个参数简要说明一下，其他的参数，可以参阅<a href="https://plot.ly/python/reference/#pie">官方网站的说明</a>。</p>
<ul>
<li><strong>values</strong>：用于绘制饼图的数据。</li>
<li><strong>labels</strong>：与上述数据项对应的标示。</li>
<li><strong>domain</strong>：从单词含义上看，它的意思是“领域”；其实，是当前的饼图所占据的“领域”。通常可以为 {'x': [0,1], 'y': [0, 1]}，表示当前图示分别在横、纵两个方向上相对图示默认坐标的范围分布，例如本例中以 domain = {'x':[0, .5]} 表示当前图示（即 Trace 对象）在图示坐标横轴上的范围是：从 0 开始，到最大刻度的 50% 止。</li>
<li><strong>name</strong>：当前 Trace 对象（图示）的名称。</li>
<li><strong>hoverinfo</strong>：当鼠标移动到每个扇区的时候，会显示相应的说明文字，就是这个参数确定的。</li>
<li><strong>hole</strong>：如果仔细观察上图，其实它不是真正意义的饼图，严谨地说，这张图应该名曰“环形图”，因为中间有一个洞（hole），这个洞就让“饼”变成“环”了。参数 hole 就是控制这个洞大小的，其值为浮点数，表示洞的半径相对饼半径的大小。如果将 hole 参数去掉，或者 hole=0，那么得到的才是真正意义的“饼图”，如下图所示。</li>
</ul>
<p><img src="https://images.gitbook.cn/74688e70-46f2-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>本来，如果创建了 go.Pie 的 Trace 对象，然后就执行语句 py.offline.iplot([trace])，就能够得到饼图（环形图）了。但是，有时候我们还需要对输出的结果在布局上进行设置，因此常常再使用 go.Layout 创建一个专门的实例对象。并且在上面的示例中，使用了 go.Layout 类中的参数 annotations，代表了标注图示文本的有关属性。</p>
<pre><code class="python language-python">colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1', '##CD5C5C']
trace = go.Pie(values = dfcn5['num_students'],
               labels = dfcn5['university_name'],
               rotation = 45,
               opacity = 0.5,
               showlegend = False,
               pull = [0.1, 0, 0, 0, 0],
               hoverinfo = 'label + percent',
               textinfo = 'value',
               textfont = dict(size=20, color='white'),
               marker = dict(colors = colors,
                             line = dict(color="#333333", width=2)
                            )
              )
py.offline.iplot([trace])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1ad95a00-46f3-11e9-babb-79877ea49803" width = "60%" /></p>
<p>这次得到的饼图跟前面的稍有不同，其变化之因皆由 go.Pie 中引入的几个新参数而来。</p>
<ul>
<li><strong>rotation</strong>：默认状态，饼图的开始是从 12 点钟位置，通过此函数，将饼图进行旋转。</li>
<li><strong>opacity</strong>：设置显示图的透明度。</li>
<li><strong>showlegend</strong>：控制是否显示图例。</li>
<li><strong>pull</strong>：以列表形式显示每个扇形区是否突出出来，列表中的“0.1”表示第一个扇区突出，并用数值表示分离的相对距离（相对半径长度）。</li>
<li><strong>textinfo</strong>：设置每个扇区上显示数值（'value'）还是百分比（'percent'）。</li>
<li><strong>marker</strong>：设置每个扇形的属性，比如颜色、线条的颜色和宽度等。</li>
</ul>
<p>在同一个 Data 中，也可以集成多个 go.Pie 的 Trace 对象，并且通过对布局的设置，能够满足更多的显示需要。下面的示例是对前述所学内容的综合展示，请认真品读。</p>
<pre><code class="python language-python"># 获取数据集中美国的 TOP 5 学校
dfusa = df[df['country']=='United States of America']
dfusa5 = dfusa.iloc[:5, :]
dfusa5['num_students'] = dfusa5['num_students'].apply(lambda value: float(value.replace(",", "")))    # 将字符串转化为浮点数

trace0 = go.Pie(values = dfcn5['num_students'],
                labels = dfcn5['university_name'],
                domain = dict(x=[0, .45]),
                name = 'China Top5',
                showlegend = False,
                hoverinfo = 'label + percent + name',
                textinfo = 'percent',
                hole = 0.4
              )
trace1 = go.Pie(values = dfusa5['num_students'],
                labels = dfusa5['university_name'],
                domain = dict(x=[0.55, 1]),
                name = 'USA Top5',
                showlegend = False,
                hoverinfo = 'label + percent + name',
                textinfo = 'percent',
                hole = 0.4
              )

data = go.Data([trace0, trace1])

layout = go.Layout(title="TOP5 of China and USA",
                   annotations = [dict(font={"size":20}, # 文字大小
                                      showarrow=False,
                                      text='China',    # 显示在环形图中央的文本
                                      x=0.18,          # 文本的显示位置
                                      y=0.5,
                                     ),
                                  dict(font={'size':20},
                                       showarrow=False,
                                       text='USA',
                                       x=0.81,
                                       y=0.5
                                      )]
                  )
figure = go.Figure(data=data, layout=layout)
py.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5ea63960-46f3-11e9-80be-3f0f855ff29d" width = "80%" /></p>
<p>对于上述程序，所用参数多数在前面已经介绍，请对照注释自行理解。</p>
<h3 id="432">4.3.2 直方图</h3>
<p>Plotly 中提供了绘制直方图的类 go.Histogram，用它创建 Trace 实例对象，并提交到 API 之后，即可得到直方图。</p>
<pre><code class="python language-python">go.Histogram(arg=None, autobinx=None, autobiny=None, cumulative=None, customdata=None, customdatasrc=None, error_x=None, error_y=None, histfunc=None, histnorm=None, hoverinfo=None, hoverinfosrc=None, hoverlabel=None, ids=None, idssrc=None, legendgroup=None, marker=None, name=None, nbinsx=None, nbinsy=None, opacity=None, orientation=None, selected=None, selectedpoints=None, showlegend=None, stream=None, text=None, textsrc=None, uid=None, unselected=None, visible=None, x=None, xaxis=None, xbins=None, xcalendar=None, xsrc=None, y=None, yaxis=None, ybins=None, ycalendar=None, ysrc=None, **kwargs)
</code></pre>
<p>本来，这些参数已经不需要说明了，因为学习本课程内容至此，读者应该已经初步习得了“阅读文档的功夫”。但是，参数 histnorm 仍有必要强调一下——它规定了直方图中表示的是样本数量还是样本频率，默认值为 None，其他取值如下：</p>
<ul>
<li>空（None），则为样本数量的直方图。</li>
<li>'percent' 或者 'probability'，则为样本频率的直方图。</li>
<li>'density'，则为样本数量密度的直方图。</li>
<li>'probability density'，则为样本频率密度的直方图。</li>
</ul>
<pre><code class="python language-python">import plotly as py
import plotly.graph_objs as go
import numpy as np

x = np.random.randn(500)
data = [go.Histogram(x=x, histnorm='probability')]
py.offline.iplot(data, filename='normalized histogram')
</code></pre>
<p><img src="https://images.gitbook.cn/9722ac60-46f3-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>此直方图表示的是样本频率分布情况。建议在这个基础上，将 histnorm 的值修改为 None，观察所制的图与此有何差别，从而深入理解直方图的含义。</p>
<p>再看一个稍微综合的示例，理解更多样化的直方图绘制方法。</p>
<pre><code class="python language-python">x2011 = df.student_staff_ratio[df.year == 2011]
x2012 = df.student_staff_ratio[df.year == 2012]

trace1 = go.Histogram(
    x=x2011,
    opacity=0.75,
    name = "2011",
    marker=dict(color='rgba(171, 50, 96, 0.6)'))
trace2 = go.Histogram(
    x=x2012,
    opacity=0.75,
    name = "2012",
    marker=dict(color='rgba(12, 50, 196, 0.6)'))

data = [trace1, trace2]
layout = go.Layout(barmode='overlay',
                   title=' students-staff ratio in 2011 and 2012',
                   xaxis=dict(title='students-staff ratio'),
                   yaxis=dict(title='Count'),
)
fig = go.Figure(data=data, layout=layout)
py.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/adf06180-46f3-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>x2011 和 x2012 所引用的数据对象，来自本课开始就创建的数据集（关于大学的统计）中的特征“student_staff_ratio”，而后将这两组数据分别用于两个 Trace 对象 trace1 和 trace2。</p>
<p>将两个 Trace 对象绘制到一个坐标系中。在上一课，我们学习 go.Bar 的时候也遇到过类似的情况，我们使用 go.Layout 中的参数 barmode 控制不同的状态，这里依然。</p>
<ul>
<li>barmode = 'overlay'：表示两个直方图重叠。</li>
<li>barmode = 'stack'：表示两个直方图堆叠（层叠）。</li>
</ul>
<p>对直方图的介绍先这些，因为它的基本用法与其他的差不多。</p>
<h3 id="433">4.3.3 箱线图</h3>
<p>利用 Plotly 绘制箱线图，所使用的对象是 go.Box，如下示例说明绘制箱线图的基本方法。</p>
<pre><code class="python language-python">trace = go.Box(
    y=df.head(100).research,
    name = 'research of top 100 universities ',
    marker = dict(
        color = 'rgb(12, 128, 128)',
    )
)
data = [trace]
py.offline.iplot(data)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/319629c0-46f4-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>因为图示是具有交互性的，鼠标移动到箱线图上，就能看到图中显示的数据。</p>
<p>关于 go.Box 的详细信息，可以查看其官方文档，此处不赘述了，跟前面的各个方法类似。但是，这里要借着箱线图的阐述，介绍另外一种被称之为“矩阵分布图”的图示，即可视化描述有关特征之间关系的图。</p>
<pre><code class="python language-python">df2015 = df[df['year'] == 2015].loc[:, ['research', 'international', 'total_score']]
df2015.sample(5)
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>research</th>
<th>international</th>
<th>total_score</th>
</tr>
</thead>
<tbody>
<tr>
<td>1691</td>
<td>22.2</td>
<td>70.8</td>
<td>-</td>
</tr>
<tr>
<td>1490</td>
<td>41.7</td>
<td>56.1</td>
<td>56.4</td>
</tr>
<tr>
<td>1451</td>
<td>77.1</td>
<td>30.3</td>
<td>64.8</td>
</tr>
<tr>
<td>1581</td>
<td>19.7</td>
<td>67.4</td>
<td>47.0</td>
</tr>
<tr>
<td>1752</td>
<td>33.1</td>
<td>21.5</td>
<td>-</td>
</tr>
</tbody>
</table>
<p>从前面已经创建的 df 数据集中取一部分，并且只研究三个特征之间的关系。</p>
<pre><code class="python language-python">df2015["index"] = np.arange(1,len(df2015)+1)    # 对已得到数据增加一个特征，表示当前的顺序。

import plotly.figure_factory as ff
fig = ff.create_scatterplotmatrix(df2015, diag='box', index='index', 
                                  colormap='Portland',
                                  colormap_type='cat',
                                  height=700, width=700)
py.offline.iplot(fig)
</code></pre>
<p><img src="https://images.gitbook.cn/48283570-46f4-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>这里使用 plotly.figure_factory 中的 create_scatterplotmatrix 实现了上述图示效果，此函数是用散点图表示两个不同变量之间的关系。简单解释本例中用到的几个参数。</p>
<ul>
<li><strong>diag</strong>：确定主对角线上的图示类型，可选值有 'scatter'、'histogram'、'box'。</li>
<li><strong>colormap</strong>：设置图示中色彩光谱的名称，在 Plotly 中提供了一些内置的色彩谱，如 'Greys'、'YlGnBu'、'Greens'、'YlOrRd'、'Bluered'、'RdBu'、'Reds'、'Blues'、'Picnic'、'Rainbow'、'Portland'、'Jet'、'Hot'、'Blackbody'、'Earth'、'Electric'、'Viridis'、'Cividis'。此参数的值也可以是用 'rgb(x, y, z)' 表示的单一颜色。</li>
<li><strong>colormap_type</strong>：可选值为 'seq'（sequential）和 'cat'（categorical）。</li>
</ul>
<h3 id="434">4.3.4 统计图的布局</h3>
<p>上面介绍了绘制常规统计图的通常方法，另外，这些统计图在布局上，可能会有所变化——重点就是 go.Layout 如何实例化，特别是针对多个统计图（即多个 Trace 对象）的时候，布局更要有讲究了。虽然前面已经对 go.Layout 有了介绍，但为了深化理解，下面再演示两个示例。</p>
<p><strong>1. 嵌入式</strong></p>
<p>所谓嵌入式，是在某一个统计图的内部，嵌入了另外一个统计图，当然不会干扰作为主体的统计图的展现——至少看起来像是嵌入了一个小图。</p>
<pre><code class="python language-python">df100 = df.iloc[:100, :]    # 前 100 所学校
# 主图 Trace 对象
trace0 = go.Scatter(x = df100['world_rank'],
                    y = df100['teaching'],
                    name = "teaching",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                   )
# 嵌入的附图 Trace 对象
trace1 = go.Scatter(x = df['world_rank'],
                    y = df['income'],
                    xaxis = 'x2',    # 附图坐标名称
                    yaxis = 'y2',
                    name = "income",
                    marker = dict(color = 'rgba(6, 6, 6, 0.8)'),
                   )
data = go.Data([trace0, trace1])
layout = go.Layout(xaxis2=dict(domain=[0.6, 0.95],    # ① 设置附图 X 轴位置
                               anchor='y2',),
                   yaxis2=dict(domain=[0.6, 0.95],    # ② 设置附图 Y 轴位置
                               anchor='x2',),
                   title = 'Income and Teaching vs World Rank of Universities'
                  )

fig = go.Figure(data=data, layout=layout)
py.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/affd4120-46f6-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>从代码中可知，实现在主图中嵌入一个附图，关键在于 go.Layout 中对附图坐标的设置，即 xaxis2 和 yaxis2。</p>
<p><strong>2. 分区</strong></p>
<p>除了嵌入，还能够实现在一张视图上划分若干区域，每个区域是一个坐标系，分别在不同坐标系中实现某种指定的制图。</p>
<pre><code class="python language-python">trace1 = go.Scatter(x = df100.world_rank,
                    y = df100.research,
                    name = "research"
                   )
trace2 = go.Scatter(x = df100.world_rank,
                    y = df100.citations,
                    xaxis = 'x2',
                    yaxis = 'y2',
                    name = "citations"
                   )
trace3 = go.Scatter(x = df.world_rank,
                    y = df.income,
                    xaxis = 'x3',
                    yaxis = 'y3',
                    name = "income"
                   )
trace4 = go.Scatter(x = df.world_rank,
                    y = df.total_score,
                    xaxis = 'x4',
                    yaxis = 'y4',
                    name = "total_score"
                   )
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(xaxis = dict(domain=[0, 0.45]),    # ③
                   yaxis = dict(domain=[0, 0.45]),    # ④
                   xaxis2 = dict(domain=[0.55, 1]),   # ⑤
                   xaxis3 = dict(domain=[0, 0.45],    # ⑥
                               anchor='y3'),
                   xaxis4 = dict(domain=[0.55, 1],
                               anchor='y4'),
                   yaxis2 = dict(domain=[0, 0.45],    # ⑦
                               anchor='x2'),
                   yaxis3 = dict(domain=[0.55, 1]),
                   yaxis4 = dict(domain=[0.55, 1],
                               anchor='x4'),
                   title = 'Research, citation, income and total score VS World Rank of Universities'
                  )
fig = go.Figure(data=data, layout=layout)
py.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f096e1f0-46f6-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>大家记得吗？上一课用过的 plotly.tools.make_subplots，再结合这里的示例，那么应该可以理解，本示例是提供了另外一种绘制分区图的方法。两种方法，请君自选。</p>
<p>上述两个示例，其实本质方法是一样的，即通过 go.Layout 实现对坐标系的设置。③ 和 ④ 设置了 trace1 所在的图示坐标系，可以视为基础坐标系，后续其他的坐标系都是相对于此坐标系设置的。正如前一个示例中的嵌入图示的坐标系，也是相对于基础坐标系设置了坐标轴的位置。只不过在前一个示例中，基础坐标系就是默认的——以左下为坐标原点，本示例的基础坐标系也是以左下为坐标原点。③ 和 ④ 分别设置了坐标轴起点和终点相对整个视图长宽比例，例如 ③ 表示该坐标轴的起点从左下原点开始，至视图宽度的 45% 处止。</p>
<p>⑤ 设置了第二个图示（trace2 对象）的 X 轴起止位置。注意这个坐标轴和基础坐标轴在同一水平线上。</p>
<p>⑥ 设置了第三个图示（trace3 对象）的 X 轴起止位置。但是，在 Y 方向上，因为已经有基础坐标系（trace1 对象图示），所以还必须要声明与此 X 轴配对的 Y 轴，否则，就会使用该方向上已有的坐标轴了，这就是为什么在 ⑥ 的值中又增加了 anchor='y3' 的原因。同样的理由，在前一个示例中的 ① 和 ②，也都声明了配对的坐标轴。</p>
<p>⑦ 规定的是第二个图示的 Y 轴，基于上述同样的原因，也要声明它对应的 X 轴。</p>
<h3 id="435">4.3.5 小结</h3>
<p>本课继续介绍了三种常规统计图：饼图（含环形图）、直方图和箱线图，并且以示例展示另外一种绘制分区图的方法，也包括嵌入图示的绘制方法。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>