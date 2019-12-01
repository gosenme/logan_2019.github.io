---
title: 案例上手 Python 数据可视化-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Plotly 的 plotly.graph_objs 库提供了很多种绘图类，涵盖了常用的统计图表，并且还有所拓展。不过，为了对类的理解更深刻，以下讲述将按照对象进行，不同的统计图依据相应的参数来实现。</p>
<h3 id="421scatter">4.2.1 Scatter 类——绘制直线图、散点图</h3>
<p>在 plotly.graph_objs 中的 Scatter 类，功能比较多，用它能够绘制直线图、散点图等。</p>
<p>根据经验，可以在 Jupyter 中输入了 go.Scatter，然后按下 TAB 键，查看到不仅仅是 Scatter，还包含其他以 Scatter 开头的家族成员（如下图所示）。</p>
<p><img src="https://images.gitbook.cn/9852caf0-46d2-11e9-80be-3f0f855ff29d" width = "50%" /></p>
<p>不过在这里，我们仅关注 go.Scatter，其他对象暂时不研究。</p>
<pre><code class="python language-python">go.Scatter(arg=None, cliponaxis=None, connectgaps=None, customdata=None, customdatasrc=None, dx=None, dy=None, error_x=None, error_y=None, fill=None, fillcolor=None, groupnorm=None, hoverinfo=None, hoverinfosrc=None, hoverlabel=None, hoveron=None, hovertext=None, hovertextsrc=None, ids=None, idssrc=None, legendgroup=None, line=None, marker=None, mode=None, name=None, opacity=None, orientation=None, r=None, rsrc=None, selected=None, selectedpoints=None, showlegend=None, stackgaps=None, stackgroup=None, stream=None, t=None, text=None, textfont=None, textposition=None, textpositionsrc=None, textsrc=None, tsrc=None, uid=None, unselected=None, visible=None, x=None, x0=None, xaxis=None, xcalendar=None, xsrc=None, y=None, y0=None, yaxis=None, ycalendar=None, ysrc=None, **kwargs)
</code></pre>
<p>面对这么多参数，不要惊慌，前面学习过程中，也不是没有见过这种阵势。参数多，说明它的功能比较全。如果有兴趣，可以根据官方文档的说明，将每个参数的含义通读一遍。若暂时没兴趣或没时间，就到用的时候再去看吧。</p>
<p>下面就用一些示例来说明某些参数的含义（示例中的数据来自：<a href="https://github.com/qiwsir/DataSet/tree/master/universityrank">https://github.com/qiwsir/DataSet/tree/master/universityrank</a>）。</p>
<pre><code class="python language-python">import pandas as pd
import plotly
import plotly.graph_objs as go

df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/universityrank/timesData.csv")
df.head()
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
<td>0</td>
<td>1</td>
<td>Harvard University</td>
<td>United States of America</td>
<td>99.7</td>
<td>72.4</td>
<td>98.7</td>
<td>98.8</td>
<td>34.5</td>
<td>96.1</td>
<td>20,152</td>
<td>8.9</td>
<td>25%</td>
<td>NaN</td>
<td>2011</td>
</tr>
<tr>
<td>1</td>
<td>2</td>
<td>California Institute of Technology</td>
<td>United States of America</td>
<td>97.7</td>
<td>54.6</td>
<td>98.0</td>
<td>99.9</td>
<td>83.7</td>
<td>96.0</td>
<td>2,243</td>
<td>6.9</td>
<td>27%</td>
<td>33 : 67</td>
<td>2011</td>
</tr>
<tr>
<td>2</td>
<td>3</td>
<td>Massachusetts Institute of Technology</td>
<td>United States of America</td>
<td>97.8</td>
<td>82.3</td>
<td>91.4</td>
<td>99.9</td>
<td>87.5</td>
<td>95.6</td>
<td>11,074</td>
<td>9.0</td>
<td>33%</td>
<td>37 : 63</td>
<td>2011</td>
</tr>
<tr>
<td>3</td>
<td>4</td>
<td>Stanford University</td>
<td>United States of America</td>
<td>98.3</td>
<td>29.5</td>
<td>98.1</td>
<td>99.2</td>
<td>64.3</td>
<td>94.3</td>
<td>15,596</td>
<td>7.8</td>
<td>22%</td>
<td>42 : 58</td>
<td>2011</td>
</tr>
<tr>
<td>4</td>
<td>5</td>
<td>Princeton University</td>
<td>United States of America</td>
<td>90.9</td>
<td>70.3</td>
<td>95.4</td>
<td>99.9</td>
<td>-</td>
<td>94.2</td>
<td>7,929</td>
<td>8.4</td>
<td>27%</td>
<td>45 : 55</td>
<td>2011</td>
</tr>
</tbody>
</table>
<p>现在读入的数据集是世界各大学排名，在后续示例中，只取其中的前一百所大学。</p>
<pre><code class="python language-python">df100 = df.iloc[:100, :]
</code></pre>
<p>首先要做的，就是利用 go.Scatter 创建 Trace 对象，将此对象提交给 Plotly 的 API 之后，Plotly 服务器就能根据此 Trace 对象的有关配置，返回相应的图线，即可得到所要绘制的图示。</p>
<pre><code class="python language-python">trace1 = go.Scatter(x = df100['world_rank'],    # 世界排名
                    y = df100['citations'],        # 被引用次数
                    mode = 'lines',
                    name = 'citations', 
                    marker = dict(color='rgba(16, 112, 2, 0.8)'),
                    text = df100['university_name']
                   )
trace2 = go.Scatter(x = df100['world_rank'],
                    y = df100['teaching'],
                    mode = 'lines+markers',
                    name = 'teaching',
                    marker = dict(color='rgba(80, 26, 80, 0.8)'),
                    text = df100['university_name']
                   )
trace3 = go.Scatter(x = df100['world_rank'],
                    y = df100['research'],
                    mode = 'markers',
                    name = 'research',
                    marker = dict(color='rgba(40, 66, 120, 0.8)'),
                    text = df100['university_name']
                   )
data = [trace1, trace2, trace3]
layout = dict(title = "Citation Research and Teaching VS World Rank of Top100 Universities",
              xaxis = dict(title='Wrold Rank', ticklen=5, zeroline=False)
             )
fig = dict(data=data, layout=layout)

plotly.offline.init_notebook_mode(connected=True)
plotly.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6bcd19a0-46d6-11e9-8b24-eb95978a8837" alt="enter image description here" /></p>
<p>在这里绘制的是三种图，控制不同类型图的参数是 go.Scatter 中的 mode，它的值可以是：</p>
<ul>
<li>'lines'，折线图，没有标记坐标点；</li>
<li>'lines + markers'，折线图，标记坐标点；</li>
<li>'markers'，散点图，没有各点之间的连线。</li>
</ul>
<p>如果觉得观察起来有点乱，可以通过图示的交互功能，比如选择图例，显示指定的图线。</p>
<p>另外几个参数的含义，也简要解释一下：</p>
<ul>
<li>'name'，每个图线的名称，对应着会在图例中显示；</li>
<li>'marker'，数据点的样式，包括大小、颜色、格式等，如果没有用另外一个参数 'line' 设置图线的颜色，则图线颜色与 'marker' 中设置的数据点颜色一样；</li>
<li>'text'，与数据点关联的文本内容。</li>
</ul>
<p><strong>特别提醒</strong>，如果使用嵌入模式，plotly.offline.init_notebook_mode(connected=True) 是不可缺少的。</p>
<p>上述方式除了绘制散点图之外，还可以绘制如下的点状图：依次对每个点进行渲染，有资料称之为“气泡图”。</p>
<pre><code class="python language-python">dfcn = df100[df100['country']=='China']
t = go.Scatter(x = dfcn['world_rank'],
               y = dfcn['citations'],
               mode = 'markers',
               marker = dict(size=[80, 60, 40], color=['yellow', 'red', 'blue']),
               text = dfcn['university_name'],
              )
plotly.offline.iplot([t])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/532073e0-46ed-11e9-81c1-6b54ce939752" alt="enter image description here" /></p>
<p>对每个点的渲染，通过 marker = dict(size=[80, 60, 40], color=['yellow', 'red', 'blue']) 实现，其中 size 设置每个圆面的大小，color 设置颜色。</p>
<h3 id="422bar">4.2.2 Bar 类—— 绘制柱形图</h3>
<p>从名称上很容易得知，go.Bar 是专门用来绘制柱形图的类。</p>
<pre><code class="python language-python">trace1 = go.Bar(x = dfcn['university_name'],
                y = dfcn['citations'],
                name = 'citations',
                marker = dict(color='red', line=dict(color='rgb(0,0,0)', width=1.5)),
                text = dfcn['world_rank']
               )
trace2 = go.Bar(x = dfcn['university_name'],
                y = dfcn['teaching'],
                name = 'teaching',
                marker = dict(color='blue', line=dict(color='rgb(0,0,0)', width=1.5)),
                text = dfcn['world_rank']
               )
data = go.Data([trace1, trace2])
layout = go.Layout(barmode = 'group')
figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f1d32190-46ed-11e9-81c1-6b54ce939752" width = "70%" /></p>
<p>以 go.Bar 生成 Trace 对象，跟以前的方式类似，这里所使用的参数也不特别。最终能够生成如图所示的簇状柱形图，关键在于 go.Layout 的参数 barmode = 'group'，如果这个参数值换成 'stack'，就会看到下面的结果。</p>
<pre><code class="python language-python">layout = go.Layout(barmode='stack', 
                   xaxis=dict(title='top 3 universities'), 
                   title="citians and teaching of top3 universities of China")
figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/04ed6ba0-46ee-11e9-80be-3f0f855ff29d" width = "70%" /></p>
<p>还是继续研究 go.Bar 的参数。除了能够得到柱形图，通过参数的设置，还能得到水平的条形图。</p>
<pre><code class="python language-python">trace3 = go.Bar(x = dfcn['citations'],
                #y = dfcn['university_name'],
                y = ['北大', '科大', '清华'],
                name = 'citations',
                marker = dict(color='red', line=dict(color='rgb(0,0,0)', width=1.5)),
                text = dfcn['world_rank'],
                orientation = 'h'
               )
trace4 = go.Bar(x = dfcn['teaching'],
                #y = dfcn['university_name'],
                y = ['北大', '科大', '清华'],
                name = 'teaching',
                marker = dict(color='blue', line=dict(color='rgb(0,0,0)', width=1.5)),
                text = dfcn['world_rank'],
                orientation = 'h'
               )
data = go.Data([trace3, trace4])
layout = go.Layout(barmode = 'stack', yaxis={'tickangle': 45})
figure = go.Figure(data=data, layout=layout)
plotly.offline.iplot(figure)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/16cf5cc0-46ee-11e9-babb-79877ea49803" alt="enter image description here" /></p>
<p>生成条形图的关键参数就是 orientation = 'h'，其他部分与柱形图一样。</p>
<p><strong>还要注意观察纵轴显示的标示</strong>，因为在 go.Layout 中的设置了 yaxis={'tickangle': 45}，使得原本水平的标示顺时针转动 45 度。</p>
<p>对于 go.Bar 除了上面的参数设置之外，还有很多，下面是完整的参数列表。</p>
<pre><code class="python language-python">go.Bar(arg=None, base=None, basesrc=None, cliponaxis=None, constraintext=None, customdata=None, customdatasrc=None, dx=None, dy=None, error_x=None, error_y=None, hoverinfo=None, hoverinfosrc=None, hoverlabel=None, hovertext=None, hovertextsrc=None, ids=None, idssrc=None, insidetextfont=None, legendgroup=None, marker=None, name=None, offset=None, offsetsrc=None, opacity=None, orientation=None, outsidetextfont=None, r=None, rsrc=None, selected=None, selectedpoints=None, showlegend=None, stream=None, t=None, text=None, textfont=None, textposition=None, textpositionsrc=None, textsrc=None, tsrc=None, uid=None, unselected=None, visible=None, width=None, widthsrc=None, x=None, x0=None, xaxis=None, xcalendar=None, xsrc=None, y=None, y0=None, yaxis=None, ycalendar=None, ysrc=None, **kwargs)
</code></pre>
<p>老调重弹，我依然建议读者对这些参数在名称上姑且先有一个了解，而后如果将来用到了，可以通过查看文档了解每个参数的具体含义和使用方法。</p>
<h3 id="423">4.2.3 综合示例</h3>
<p>在一张图示中，可以单独是某一种统计图，也可以合并多个统计图。下面就用一个综合示例说明如何实现这种图示。</p>
<pre><code class="python language-python">df5 = df100.sample(5)    # 从 Top100 学校中抽样 5 所学校
trace0 = go.Bar(x = df5['teaching'],
                y = df5['university_name'],
                marker = dict(color = 'rgba(50, 171, 90, 0.8)',    # 水平条颜色
                             line = dict(color = 'rgba(50, 171, 90, 0.8)', 
                                         width = 1)    # 水平条的边框颜色和宽度
                            ), 
                name = "teaching",
                orientation = 'h'
               )
trace1 = go.Scatter(x = df5['citations'],
                    y = df5['university_name'],
                    mode = 'lines + markers', 
                    line = dict(color = 'rgb(128, 0, 128)'),    #折线颜色
                    name = 'citations'
                   )
layout = go.Layout(title="Teaching and Citations of University",
                   # 左侧图示的 Y 轴
                   yaxis1 = dict(showgrid = False,    # 不显示网格的水平线
                                 showline = False,    # 不显示Y轴
                                 showticklabels = True,    #  显示刻度的标示(即特征 'university_name' 的值)
                                 tickangle = 50
                                ),
                   # 右侧图示的 Y 轴
                   yaxis2 = dict(showgrid = False,
                                 showline = True,    #显示 Y 轴
                                 showticklabels = False,    # 不显示刻度标示
                                 linecolor ='rgba(102, 102, 102, 0.8)',    # Y 坐标轴的颜色
                                 linewidth = 2,
                                ),
                   # 左侧图示的 X 轴
                   xaxis1 = dict(zeroline = False,    # 不显示左侧 Y 轴线
                                 showline = False,    # 不显示下方 X 轴线
                                 showticklabels = True,
                                 showgrid = True
                                ),
                   # 右侧图示的 X 轴
                   xaxis2 = dict(zeroline = False,
                                 showline = False,
                                 showticklabels = True,
                                 showgrid = True,
                                 side = 'top',         # 将 X 轴的标示移到上面
                                ),

                  )

from plotly import tools
fig = tools.make_subplots(rows=1, cols=2, shared_xaxes = True, shared_yaxes = False)    # ①
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig['layout'].update(layout)
plotly.offline.iplot(fig)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7d23f4e0-46ee-11e9-80be-3f0f855ff29d" alt="enter image description here" /></p>
<p>请对照本例代码后面的注释，自行理解程序含义。</p>
<p>通过这个综合示例，我们应该重点理解的就是图示对象。如果按照面向对象的思想来理解 fig，就会发现通过 ①，fig 即为一个“容器”对象，向这个容器中增加 Trace 对象（注意指明位置）及布局（Layout），而后将此容器对象提交给 Plotly，即可得到图示。</p>
<h3 id="424">4.2.4 小结</h3>
<p>本课主要通过对 go.Bar 和 go.Scatter 两个创建 Trace 实例对象的类的理解，进一步研习如何创建散点图、折线图、柱形图和条形图，并在综合示例中展示了 Figure 容器对象的应用。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>