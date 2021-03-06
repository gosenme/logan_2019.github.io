---
title: 案例上手 Python 数据可视化-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Plotly 的内容非常多，不过，本着“弱水三千、只取一瓢饮”的原则，本达人课仅详细介绍一些基本知识，并借着这些知识向读者说明掌握 Plotly 制图的基本方法，特别是本达人课中反复强调过的方法——阅读文档。理解和使用这些方法，才是将来在项目实践中所向无敌的保证。</p>
<p>本课会再选几个示例展示一些高级的制图方法。</p>
<h3 id="441">4.4.1 地理信息可视化</h3>
<p>地理信息可视化是数据可视化中一个非常重要的分支。前面若干课的工具都能实现地理信息可视化，但是此前并没有介绍，因为还要安装很多别的东西，比较麻烦。其实 Plotly 提供了比较简单的实现方式，因为它整合了 Mapbox。</p>
<blockquote>
  <p>Mapbox，官方网站：<a href="http://www.mapbox.com/">www.mapbox.com</a>，是一家向移动端和 Web 应用提供地图数据的服务商。</p>
</blockquote>
<p>首先，要到 Mapbox 官方网站注册，然后取得 token；接下来就能做地理信息可视化了。</p>
<pre><code class="python language-python">import plotly
import plotly.graph_objs as go

mapbox_access_token = "your_mapbox_access_token"

data = [go.Scattermapbox(lat = ['31.3'],
                         lon = ['120.7'],
                         mode = 'markers',
                         marker = dict(size = 20, colo r= 'red'),
                         text=['Soochow'],
                        )]
layout = go.Layout(autosize = True, 
                   hovermode = 'closest',
                   mapbox = dict(accesstoken = mapbox_access_token,
                                 bearing = 0,
                                 center = dict(lat = 31.3, lon = 120.7),
                                 pitch = 0,
                                 zoom=10
                                ),
                  )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='Soochow')
</code></pre>
<p><img src="https://images.gitbook.cn/8cc23690-46f9-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>这里的截图仅是部分界面，看到图中的红点了吧，那个就是上面的程序中要在地图上标记的点。下面就看看是如何实现这种效果的。</p>
<p>跟前面各节绘制的图示一样，地理信息的图示在 Plotly 中也是一种 Trace 对象，它由 plotly.graph_objs.Scattermapbox 生成。</p>
<pre><code class="python language-python">go.Scattermapbox(arg=None, connectgaps=None, customdata=None, customdatasrc=None, fill=None, fillcolor=None, hoverinfo=None, hoverinfosrc=None, hoverlabel=None, hovertext=None, hovertextsrc=None, ids=None, idssrc=None, lat=None, latsrc=None, legendgroup=None, line=None, lon=None, lonsrc=None, marker=None, mode=None, name=None, opacity=None, selected=None, selectedpoints=None, showlegend=None, stream=None, subplot=None, text=None, textfont=None, textposition=None, textsrc=None, uid=None, unselected=None, visible=None, **kwargs)
</code></pre>
<p>在本例中，使用了部分参数，具体如下。</p>
<ul>
<li>lat = ['31.3']：所标记地点的纬度，以北纬为正数。</li>
<li>lon = ['120.7']：所标记地点的经度，以东经为正数。注意，lat 和 lon 两个参数的值都是列表，也就意味着还可以标记多个地点，只是本例中只标记了一个地点。</li>
<li>mode='markers'：所标记地点在图上显示符号。</li>
<li>marker=dict(size=20,color='red')：对标记符号的大小、颜色等属性的设置。</li>
<li>text=['Soochow']：标记点的文本显示。当鼠标移动到该点时会显示此列表中的元素。</li>
</ul>
<p>只有 Trace 对象，最终还不能得到图示结果。Trace 对象仅是地理信息，其背景图应该是地图，这就要在 go.Layout 中指定要读入的地图了。在以往的示例中，虽然也多次应用它，但是所使用的参数与本示例有差别，毕竟这里要用地图作为布局了。</p>
<ul>
<li>autosize = True：确定图示自动适应页面大小。</li>
<li><strong>hovermode</strong>：设置鼠标悬停的交互操作，通常与之配套操作的还有参数 clickmode。默认值为 'closest'，意即鼠标靠近标记对象实现交互操作。</li>
<li><strong>mapbox</strong>：这是实现地图作为背景的关键参数。它的值是以字典形式提供的跟地图有关的属性映射。<ul>
<li><strong>accesstoken</strong>：前文已经提到过的 Mapbox，此键的值就是在 Mapbox 上注册后获得的 token。</li>
<li><strong>bearing</strong>：默认值为 0。用于设置地图上的方位角。</li>
<li><strong>center</strong>：以 {'lon': number, 'lat': number} 的形式设置最终图示中心的经纬度位置。</li>
<li><strong>pitch</strong>：设置观察地图的角度（以度为单位），即俯视角度。默认值为 0 度，表示垂直于地图表面观察。</li>
<li><strong>zoom</strong>：所显示的地图的层级，数量越大，显示的范围越小。若为 0，则显示的是世界地图；本例中使用了 zoom=10，显示了我朝的“街道”和“镇”这一级的地图。当然，因为在网页中呈现的地图是具有交互性的，还可以通过扩大、缩小操作，实现呈现地图范围的变化。</li></ul></li>
</ul>
<p>在上述基础上，再用<a href="https://github.com/qiwsir/DataSet/tree/master/jiangsu">江苏省各城市数据</a>，标记出各个城市的位置。</p>
<pre><code class="python language-python">import pandas as pd

df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/jiangsu/city_population.csv")

mapbox_token = "your_mapbox_access_token"

lat = df.latd    # 经度(Longitude) 纬度(Latitude)
lon = df.longd
locations_name = df.name   # 城市名称

data = [
    go.Scattermapbox(
        lat = lat,
        lon = lon,
        mode = "markers",
        marker = dict(size=17, 
                      color='rgb(255, 0, 0)', 
                      opacity=0.7),  
        text = locations_name,
        hoverinfo = 'text',
    ),
    go.Scattermapbox(
        lat = lat,
        lon = lon,
        mode = "markers",
        marker = dict(size=8, 
                      color='rgb(242, 177, 172)', 
                      opacity=0.7),
        text = locations_name,
        hoverinfo = 'text'
    )
]

layout = go.Layout(
    title = "The City of Jiangsu",
    autosize = True,
    hovermode = "closest",
    showlegend = False,
    mapbox = dict(accesstoken=mapbox_token, 
                  bearing=0, 
                  center=dict(lat=31,lon=120),
                  pitch=0,
                  zoom=5,
                  style='light'),
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename="jiangsu_city_map")
</code></pre>
<p>输出结果局部效果：</p>
<p><img src="https://images.gitbook.cn/bcfdbb90-4703-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<h3 id="442">4.4.2 金融数据可视化</h3>
<p>金融领域对数据可视化有着非常迫切的需要，比如股票市场，常以多种可视化方式表示不同类别的数据，而这些数据通常都有一个重要的维度：时间——严格讲是时刻，只不过是不同单位罢了。</p>
<p>先看下面的示例（数据来源：<a href="https://github.com/qiwsir/DataSet/tree/master/appl%EF%BC%89">https://github.com/qiwsir/DataSet/tree/master/appl</a>）。</p>
<pre><code class="python language-python">appl_df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/appl/appl.csv", 
                      index_col=['date'], parse_dates=['date'])
appl_df.head()
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>close</th>
<th>volume</th>
<th>open</th>
<th>high</th>
<th>low</th>
</tr>
</thead>
<tbody>
<tr>
<td>date</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>2018-10-17</td>
<td>221.19</td>
<td>22692880</td>
<td>222.30</td>
<td>222.64</td>
<td>219.3400</td>
</tr>
<tr>
<td>2018-10-16</td>
<td>222.15</td>
<td>28802550</td>
<td>218.93</td>
<td>222.99</td>
<td>216.7627</td>
</tr>
<tr>
<td>2018-10-15</td>
<td>217.36</td>
<td>30280450</td>
<td>221.16</td>
<td>221.83</td>
<td>217.2700</td>
</tr>
<tr>
<td>2018-10-12</td>
<td>222.11</td>
<td>39494770</td>
<td>220.42</td>
<td>222.88</td>
<td>216.8400</td>
</tr>
<tr>
<td>2018-10-11</td>
<td>214.45</td>
<td>52902320</td>
<td>214.52</td>
<td>219.50</td>
<td>212.3200</td>
</tr>
</tbody>
</table>
<p>读入数据的同时将“date”列指定为 DataFrame 的索引，并转化为日期类型。在输出结果中可以看到该数据的各个特征，且索引是按照日期“从大到小”排列的。</p>
<pre><code class="python language-python">data = [go.Scatter(x=appl_df.index, y=appl_df['high'])]

plotly.offline.init_notebook_mode(connected=True)
plotly.offline.iplot(data)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0ec84d00-4704-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>这是用 go.Scatter 绘制的折线图，但是 Plotly 在处理 X 轴数据的时候很聪明，并没有按照 appl_df 中索引顺序直接在坐标系绘图（按照时间“从大到小”），而是自动进行翻转，按照时间“从小到大”的自然顺序绘制了每日的股票交易最高价折线图。为了观察到时间跨度更小的某个范围的价格变化，可以利用交互功能中的“放大”操作工具。</p>
<p>从 appl_df 的数据集中可知，股票数据中还有 close、open、low 等交易数值。要把这些也在图中表示出来，可以创建相应的 Trace 对象——这是以前讲过的方法。Plotly 中提供了专门用户绘制股票交易数据的类（也是 Trace 对象）。</p>
<pre><code class="python language-python">trace = go.Ohlc(
    x = appl_df.index,
    open = appl_df.open,
    high = appl_df.high,
    low = appl_df.low,
    close = appl_df.close,
)

plotly.offline.iplot([trace])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/655ff6e0-4704-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>这里使用了一个新的 Trace 类 go.Ohlc，其作用就是绘制股票的开盘价（open）、最高价（high）、最低价（low）和收盘价（close）——简称“ohlc”。</p>
<p>注意观察图示：</p>
<ul>
<li>图示中的线不是折线（貌似是因为数据量比较大的缘故）——后续会换一种数据研究图线。</li>
<li>在 X 轴下面有专门的时间控件，通过它可以选择显示任意时间间隔内的统计图。而且，这个时间空间是自动生成的。</li>
</ul>
<p>为了便于研究图线，取少量数据，还是绘制 OHLC 图。</p>
<pre><code class="python language-python">df30 = appl_df.head(30)

trace = go.Ohlc(x = df30.index,
                open = df30.open,
                high = df30.high,
                low = df30.low,
                close = df30.close,
               )

plotly.offline.iplot([trace])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/bfa147d0-4704-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>现在看清楚图线了，以线的长度表示出最高、最低价，以左侧短线表示开盘价，右侧短线表示收盘价，而且不同颜色分别表示收盘价相对开盘价高还是低。</p>
<p>在金融领域，除了 OHLC 图之外，还有一种被称为蜡烛图的可视化方式。相对于 OHLC 图的做法，只需要修改 go.Ohlc 为 go.Candlestick 即可。</p>
<pre><code class="python language-python">trace = go.Candlestick(    #只需修改函数名称
    x = df30.index,
    open = df30.open,
    high = df30.high,
    low = df30.low,
    close = df30.close,
)

plotly.offline.iplot([trace])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d323c990-4704-11e9-81c1-6b54ce939752" alt="enter image description here" /></p>
<p>其实 go.Candlestick 和 go.Ohlc 表达的是同样的含义，只是样式有所差别。</p>
<p>如果仔细观察 appl_df 的索引，会发现其日期并不是一天一天都连续的，而是每隔 5 天，就缺少 2 天，是因为那两天没有交易——当然，也有的遇到美国的法定假日没有交易。</p>
<p>而横坐标轴则不然，是按照每天绘制的，只不过在没有交易的时候，不画图线罢了（如下图所示），这就导致有的地方空隙较大。</p>
<p><img src="https://images.gitbook.cn/ecc670a0-4704-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>因此，需要将程序优化，去除横轴上不交易日期。</p>
<pre><code class="python language-python">df = appl_df.head(50)

trace = go.Candlestick(x = df.index,
                       open = df.open,
                       high = df.high,
                       low = df.low,
                       close = df.close,
                      )

layout =go.Layout(xaxis = dict(autorange = True,
                               mirror = 'all',
                               gridcolor = 'rgb(180, 180, 180)',
                               showline = True,
                               showgrid = True,
                               tickangle = -60,
                               type = 'category',   # ①
                               categoryorder = 'category ascending',    # ②
                              ),
                  yaxis = dict(autorange = True,
                               gridcolor = '#3d3d4f',
                              )
                 )

fig = go.Figure(data=[trace], layout=layout)
plotly.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f5474240-4704-11e9-81c1-6b54ce939752" alt="enter image description here" /></p>
<p>跟前面的程序相比较，多了 go.Layout 的实例（即布局），特别是 ① 和 ②。</p>
<ul>
<li>① 的作用是将作为时间的横轴进行转化，不再是连续的时间，而是将数据集中时间索引的数据转换为分类数据，数据集中自然没有节假日，于是在图中横轴上节假日也就消失了。</li>
<li>但是，如果没有 ②，横轴的日期从左向右是按照日期“从大到小”排列的，这不符合习惯——虽然符合数据集中索引顺序。② 的作用就是将此顺序翻转。参数 categoryorder 的默认值是 trace，即按照 Trace 对象中规定的 X 轴显示，此处用 'category ascending' 为值，表示按照升序排列，反之则是降序 'category descending'。</li>
</ul>
<p>听说在股票上还有“5 日线”。其他 X 日线，画法相同。</p>
<pre><code class="python language-python">df['avg_5'] = df['close'].rolling(5).mean()    #计算5日收盘价的平均值，即五日平均价
five_line = go.Scatter(x = df.index,
                       y = df.avg_5,
                       name = '5 days mean',
                       line = dict(color='black')
                      )
fig = go.Figure(data=[trace, five_line], layout=layout)
plotly.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/fb482a50-4705-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>据传闻，炒股高手可以通过某些线占卜未来股价变化——恭喜发财。不过，码农还是热衷于敲代码，固然穷困潦倒，但也乐在其中——股市有风险，投资需谨慎。</p>
<h3 id="443">4.4.3 图表混合</h3>
<p>通常，图是定性的表达，在图中看到的是相对效果或者趋势。而如果要看准确的数据，就需要用表。Plotly 中也提供了生成表的方法。</p>
<p>下面演示如何绘制表及图表混合的图示（数据来源：<a href="https://github.com/qiwsir/DataSet/tree/master/school">https://github.com/qiwsir/DataSet/tree/master/school</a>）。</p>
<pre><code class="python language-python">stus = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/school/school.csv", 
                   index_col=['School'])
stus.head()
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>Women</th>
<th>Men</th>
<th>Gap</th>
</tr>
</thead>
<tbody>
<tr>
<td>School</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>MIT</td>
<td>94</td>
<td>152</td>
<td>58</td>
</tr>
<tr>
<td>Stanford</td>
<td>96</td>
<td>151</td>
<td>55</td>
</tr>
<tr>
<td>Harvard</td>
<td>112</td>
<td>165</td>
<td>53</td>
</tr>
<tr>
<td>U.Penn</td>
<td>92</td>
<td>141</td>
<td>49</td>
</tr>
<tr>
<td>Princeton</td>
<td>90</td>
<td>137</td>
<td>47</td>
</tr>
</tbody>
</table>
<p>在读入数据的时候，将原有 CSV 文件中的“School”列作为 DataFrame 的索引，然后用下面的程序绘制表格。</p>
<pre><code class="python language-python">import plotly.figure_factory as ff

table = ff.create_table(stus, index=True)
plotly.offline.iplot(table)    # ③
</code></pre>
<p><img src="https://images.gitbook.cn/5f59fe60-4706-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>这个表格不是普通的表格，它具有 Plotly 中前述各种图的交互功能，比如放大、缩小、移动等操作工具。换个角度，也可以直接把它看做以往制作的图示——一种表格类图示。</p>
<p>要特别注意 ③，对比前面绘制图示的时候多传入的参数，这个 table，其实已经不是 Trace 对象了（plotly.offline.iplot([trace])，这是 Trace 对象传入的方式），<strong>那么它是什么？</strong></p>
<pre><code class="python language-python">type(table)

# out
plotly.graph_objs._figure.Figure
</code></pre>
<p>这里的 table 其实是一个 Figure 对象，里面已经包含了 'data' 和 'layout' 两个键值对。</p>
<p>因此，在制作图表混合图的时候，要注意并利用这个特点。</p>
<pre><code class="python language-python">import plotly.figure_factory as ff
stus = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/school/school.csv").iloc[:10, :]

figure = ff.create_table(stus)    # ④

trace0 = go.Scatter(x = stus['School'],
                    y = stus['Women'],
                    marker = dict(color='#0099ff'), 
                    name = 'Women',
                    xaxis = 'x2',
                    yaxis = 'y2'
                   )
trace1 = go.Scatter(x = stus['School'],
                    y = stus['Men'],
                    marker = dict(color='#404040'),
                    name = 'Men',
                    xaxis = 'x2',
                    yaxis = 'y2'
                   )
data = go.Data([trace0, trace1])
figure.add_traces(data)    # ⑥

layout = go.Layout(xaxis = dict(domain=[0, 0.45]),
                   xaxis2 = dict(domain=[0.55, 1],),
                   yaxis2 = dict(anchor='x2'),
                   margin = go.layout.Margin(b=100, t=20),    # ⑦
                  )

figure['layout'].update(layout)    #⑧
plotly.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/8d4e8520-4706-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>这里得到的图示是“左表右图”的结构，跟以往一样，需要通过 go.Layout 设置布局。<strong>其中 ⑦ 是要特别说明的，以前没有出现过。</strong> 如果熟悉网页开发，就知道 margin 通常是用于设置单元对象周边的距离，它的完整形式应该是：</p>
<pre><code class="python language-python">go.layout.Margin(arg=None, autoexpand=None, b=None, l=None, pad=None, r=None, t=None, **kwargs)
</code></pre>
<p>在 ⑦ 中设置参数 b=100，表示相对底端的距离；t=20 设置了相对顶端的距离。</p>
<p>既然 ④ 得到的是 Figure 对象，如果向这个对象中的 data 键的值中增加元素（即所创建的 Trace 对象），现在已经不能使用某些资料中的 figure['data'].extend([trace0, trace1]) 方式——这种方法对比较早的版本适用，在 Plotly 3.0 之后的版本要用 ⑥ 的方式实现。</p>
<p>在 ④ 所得到的 Figure 对象中，也已经有了 Layout 键，因此，使用 ⑧ 可以继续为此键增加值。</p>
<p><strong>除了左右结构，图表混合的图示还可以实现上下结构。</strong></p>
<pre><code class="python language-python">figure = ff.create_table(stus)

trace0 = go.Bar(x = stus['School'],
                y = stus['Gap'],
                marker = dict(color='#0099ff'),
                name = 'Gap',
                xaxis = 'x2',
                yaxis = 'y2'
               )
trace1 = go.Bar(x = stus['School'],
                y = stus['Men'],
                marker = dict(color='#669900'),
                name = 'Men',
                xaxis = 'x2',
                yaxis = 'y2'
               )
trace2 = go.Bar(x = stus['School'],
                y = stus['Women'],
                marker = dict(color='#707070'),
                name = 'Women',
                xaxis = 'x2',
                yaxis = 'y2'
               )
figure.add_traces([trace0, trace1, trace2])

# 以下演示另外一种设置视图布局的方式
figure['layout']['xaxis2'] = {}
figure['layout']['yaxis2'] = {}

figure.layout.yaxis.update({'domain': [0, 0.45]})
figure.layout.yaxis2.update({'domain': [0.55, 1]})

figure.layout.yaxis2.update({'anchor': 'x2'})
figure.layout.xaxis2.update({'anchor': 'y2'})

figure.layout.margin.update({'t':75, 'l':50})
figure.layout.update({'height':800})

plotly.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e05232d0-4706-11e9-81c1-6b54ce939752" alt="enter image description here" /></p>
<p>此处实现了图表的上下结构。虽然在 Trace 对象的创建上没有什么特殊之处，但是在后面的布局设置上与以前的示例稍有区别。这里使用了字典对象的方法 update 增加 Layout 实例对象中的属性—— go.Figure 类的实例是类字典对象。</p>
<h3 id="444">4.4.4 小结</h3>
<p>回到本课开头所述，Plotly 中能够绘制的图示还很多，这里无法穷尽。但是，如果掌握了这些基本方法和思想，再结合官方文档，一定能解决项目实践中遇到的问题，绘出美图。</p>
<p>如果觉得本达人课中的这些案例还不过瘾，就请到官网欣赏更多精彩内容（<a href="https://plot.ly/python/">https://plot.ly/python/</a>）。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>