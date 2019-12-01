---
title: 案例上手 Python 数据可视化-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面学习的可视化工具，所绘制的图都是发布到本地的。如果别人想看，有两种方法：一种是跑到自己的计算机这边来看；另一种是导出图片发给对方。在当今网络如此发达的时代，还用这种古代的方式传播信息，的确有点太不上档次了。</p>
<p>如果读者在这之前已经意识到问题了，说明你是一个善于发现问题的人。但这还不够，还要善于解决问题。当然，这个问题也不是今天才发现的，比如 Alex Johnson、Jack Parmer、Chris Parmer 和 Matthew Sundquist，他们早在大约 2013 年就意识到了，并且动手解决，于是 Plotly 诞生了（参考：<a href="https://en.wikipedia.org/wiki/Plotly">维基百科</a>）。</p>
<p>Plotly 解决了数据可视化作品的在线分享问题，这就是它的独特之处。</p>
<h3 id="411">4.1.1 初始化</h3>
<p>Plotly 的底层是 plotly.js，plotly.js 基于 D3.js、stack.gl 和 SVG，能够用 JS 在网页上实现类似 Matlab 和 Matplotlib 的图形。Plotly 提供了 Python、Matlab、R 语言等 API。</p>
<p>Plotly 原本是收费的，自 2016 年 6 月开始，提供免费的社区版。</p>
<p>如果要使用它，首先要在网站官方网站 <a href="https://plot.ly/">https://plot.ly/</a> 注册账号，然后就可以在线发布绘制的图示了。</p>
<p><img src="https://images.gitbook.cn/26bd0c20-4637-11e9-a3cb-3f7f3cd145c5" alt="enter image description here" /></p>
<p>登录网站之后，在用户个人信息中的下拉菜单选择“setting”项目，进入下面的界面。</p>
<p><img src="https://images.gitbook.cn/31f47240-4637-11e9-a7f8-09d27c9861c8" width = "70%" /></p>
<p>记录下自己的 Username 和 API KEY（可以重置），这样就做好了在线账号设置工作。</p>
<p>下一步就是要在本地安装 Plotly，在本课程第 0-3 课中已经介绍过，如果尚未安装，请用如下指令：</p>
<pre><code>pip3 install plotly
</code></pre>
<p>安装完毕，进行在线账号初始化。</p>
<pre><code class="python language-python">import plotly
plotly.tools.set_credentials_file(username="your_username", api_key='your_apikey')
</code></pre>
<p>这步操作如果成功，则不返回任何结果。初始化的结果是在本地生成了 ~/.plotly/.credentials 文件。</p>
<h3 id="412">4.1.2 三种模式</h3>
<p>完成初始化之后，就可以进行绘图，并实现在线分享。</p>
<pre><code class="python language-python">import plotly.plotly as py
import plotly.graph_objs as go

t0 = go.Scatter(x = [1, 2, 3, 4],
                y = [10, 15, 13, 17])
t1 = go.Scatter(x = [1, 2, 3, 4],
                y = [16, 18, 13, 17])
data = [t0, t1]
py.plot(data, filename="example_image")    #①
</code></pre>
<p>执行上述代码之后，会输出一个 URL：'https://plot.ly/~qiwsir/12'（每个人的 URL 会有所不同）。同时，会自动打开浏览器一个新标签，在那里会展现这个 URL 的页面内容，就是上述程序所绘制的图形。如果没有自动打开，可以把返回的 URL 复制到地址栏中访问此页面。</p>
<p><img src="https://images.gitbook.cn/1e64c9c0-463a-11e9-a3cb-3f7f3cd145c5" width = "70%" /></p>
<p>如果看到了此页面，就可以把 URL 分享给任何人，他们都能打开网页看到同样的图像。而且，因为这张图是基于 JavaScript 的，在手机那种小屏幕上看，也一样能够自适应。</p>
<p><strong>惊喜还不止这些。</strong> 如果用鼠标点击图例，就会发现可以选择要显示的图线。另外，上面还有放大、截图、移动、下载、分享多个小工具等。</p>
<p>我们可以把 Plotly 的官方网站看做免费公开图示的托管网站，在里面可以看到很多高手发布的精美图示。每个用户在这里都有个人作品的专有页面，比如本教程作者的个人作品集：<a href="https://plot.ly/~qiwsir#/">https://plot.ly/~qiwsir#/</a>，打开之后会看到我个人发布的图示（很抱歉，没有好东西）。</p>
<p><img src="https://images.gitbook.cn/773377e0-463a-11e9-991a-8dc936640e58" alt="enter image description here" /></p>
<p>图中标示了 filename，它所显示的就是 py.plot(data, filename="example_image") 中所设置的图示文件名称。</p>
<p>刚才生成的图示，直接发布到 plot.ly 上，把这种方式称为“在线模式”。与之相对，还有另外一种模式，不发布到该网站上，而是在本地生成一个 HTML 文件，并将图示置于其中，这种模式称为“离线模式”。操作如下：</p>
<pre><code class="python language-python">import plotly
import plotly.graph_objs as go

plotly.offline.plot({"data": [go.Scatter(x=[1,2,3,4], y=[6,7,8,9])],
                     "layout": go.Layout(title="laoqi_third_image")}, 
                     auto_open = True)
</code></pre>
<p>执行之后，会返回 HTML 文件的地址，例如：'file:///Users/qiwsir/Documents/Projects/gitchat/data-visual/temp-plot.html'，并且同时在浏览器中打开这个文件 auto_open = True。</p>
<p>在线模式或离线模式，都是要在新的浏览器地址打开。如果觉得这样的方式不方便调试，还可以使用第三种模式——嵌入模式。</p>
<pre><code class="python language-python">plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({
    "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": go.Layout(title="hello world")
})
</code></pre>
<p>执行之后，在当前代码的下面会插入下图所示（因为不同计算机的计算能力差异，有时候可能需要等几秒钟才能呈现图示）：</p>
<p><img src="https://images.gitbook.cn/cca69ef0-463a-11e9-ba92-49a75a13a563" width = "70%" /></p>
<p>效果貌似跟前面使用 Matplotlib 等差不多，但是这里插入的不是一张静态图片，而是跟“在线模式”或者“离线模式”一样的 H 前段代码（HTML + JS），同样具有交互功能。只不过，这种模式对于调试更便捷。</p>
<h3 id="413">4.1.3 基本结构</h3>
<p>在上述的制图代码中，主要是用 Plotly 提供的一些 API 完成绘图，这一点与以往的工具是一样的。区别就在于，这里还提供了一些基于网站 plot.ly 的 API，从而能够实现在线模式的制图。</p>
<p>如果对绘制图示的过程进行分析，可以将其概括为如下几部分。</p>
<p><strong>1. API 函数</strong></p>
<p>基于 Plotly 制图，不论是最后生成在线的还是本地的图示，都是按照如下流程。</p>
<ul>
<li>向服务器的 API 提交数据和有关参数配置——以 JSON 格式。如果是生成本地图示，就提交给本地的 Plotly 程序并生成 HTML 文件；如果是生成在线图示，就是向 Plotly 服务器提交，并返回网址。</li>
<li>服务器接收到信息，验证正确后生成图示。</li>
<li>返回地址（可以是在线的 URL，也可以是本地 HTML 文件地址，或者插入到当前浏览器）。</li>
</ul>
<p>以在线模式为例：</p>
<pre><code class="python language-python">import plotly.plotly as py
</code></pre>
<p>用这种方式引入了 plotly.plotly 库，并更名为 py。这个库包含了与 Plotly 官方服务器相连接的函数，例如在线模式中的 ①（py.plot(data, filename="example_image")）所使用的函数 py.plot，其作用就是向 Plotly 官网提交有关绘图的数据，以及对图示的各种配置信息。服务器接受之后，会创建一个在线图示（唯一的一个 URL），默认自动打开。</p>
<pre><code class="python language-python">plot(figure_or_data, validate=True, **plot_options)
</code></pre>
<p>常用参数见下。</p>
<ul>
<li><strong>figure_or_data</strong>：向 Plotly 官方网站提交的数据，通常以 JSON 组成的列表形式提交。</li>
<li><strong>filename</strong>：图示的名称。</li>
<li><strong>fileopt</strong>：文件保存模式，可选的模式（字符串）有以下几个选项。<ul>
<li><strong>new</strong>：新创建一个 URL。</li>
<li><strong>overwrite</strong>：覆盖原有的同 filename 的图示。</li>
<li><strong>extend</strong>：对已有图示的 traces 增加数据—— traces 是什么？继续阅读就能明白。</li>
<li><strong>append</strong>：对已有图示的数据列表中追加 traces ——跟 extend 不同。假设已有图示的数据列表是 [trace1, trace2]，append 的作用就是向这个列表中追加 trace，使其变成 [trace1, trace2, trace3]。</li></ul></li>
<li><strong>auto_open</strong>：默认 auto_open = True，即自动打开 URL。</li>
<li><strong>sharing</strong>：设置 URL 的访问权限，可选值有以下几个。<ul>
<li>'public'：任何人都可以访问，并且显示在个人页面，允许 Plotly 搜索。</li>
<li>'private'：只有发布者个人用户可以访问。</li>
<li>'secret'：拥有此链接的人能够访问，但 Plotly 网站上不会展示，也不搜索此图。</li></ul></li>
</ul>
<p>除了此函数之外，类似的还有 plotly.offline.plot 和 plotly.offline.iplot，不同之处在于向本地的 Plotly 服务提交有关数据和图示的参数设置等。而后根据设置生成图示。</p>
<p><strong>2. JSON 格式的数据</strong></p>
<p>通过 Plotly 的 API 所提交的数据，可以有多种类型（对象）。</p>
<p><strong>列表中的字典。</strong> 例如（使用嵌入模式，后续不特别说明，都以这种模式演示）：</p>
<pre><code class="python language-python">import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({"data": [{'x': [1, 2, 3],
                                    'y': [4, 5, 6],
                                    'name': 'a trace',
                                    "text":['one', 'two', 'three'],
                                    "mode": "markers+lines",
                                    "marker":{'color':'red', 'symbol': 104}
                                   },
                                   {'x': [3, 2, 1],
                                    'y': [4, 4.5, 5],
                                    'name': 'a trace',
                                    "text":['FIRST', 'SECOND', 'THIRD'],
                                    "marker":{'color':'black',}
           }
     ],
})
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b21910c0-463c-11e9-991a-8dc936640e58" width = "70%" /></p>
<p>如果在本地也生成了图中所示结果，在解释“数据”之前，可以先用鼠标指向某个点，然后对照数据中的配置看看效果，并且再次体会，所得到图示中的交互性，这也是 Plotly 的显著特点，此前的工具都不具有此功能——这是基于 JS 生成图示的特征。</p>
<p>下面来看 iplot 的参数。iplot 是以 data 为键的一个字典，这个字典的值就是向 Plotly 的 API 所提交的数据。值是一个列表，列表中的元素为字典——这里是两个字典。每个字典以键值对的方式说明所要绘图示的属性：</p>
<ul>
<li>'x'—— X 轴的数据；</li>
<li>'y'—— Y 轴的数据；</li>
<li>'name'——每条曲线的名称；</li>
<li>'marker'——点的颜色和形状。</li>
</ul>
<p>显然，每个字典所包含的不仅仅是“数据”，还包含了关于图形的有关设置。</p>
<p><strong>Trace 对象</strong></p>
<p>Plotly 还提供了另外一个库，就是前面已经引入的 plotly.graph_objs，即：</p>
<pre><code class="python language-python">import plotly.graph_objs as go
</code></pre>
<p>这个库中提供了一些用于生成图示对象的函数，Trace 对象就是其一。</p>
<p>Trace，我没有找到太适合的翻译词语，有的资料翻译为“数据”，但是与通常所说的“数据”有混淆。因为 Trace 包含的不仅仅是绘制图像的“数据”——上图中对应 X、Y 轴的数据（我们通常说的“数据”）——还包括对图线属性的设置。因此，在找到适合的词语之前，先直接使用 Trace 说明这个对象。</p>
<p>plotly.graph_objs 中有专门用于生成 Trace 对象的类，这些类中包括数据，还包括对图线的配置。例如：</p>
<pre><code class="python language-python">t0 = go.Scatter(x=[1,2,3], 
                y=[4,5,6], 
                marker={'color':'red', 'size':10}, 
                text=['one', 'two', 'three'])
type(t0)

# out
plotly.graph_objs._scatter.Scatter
</code></pre>
<p>这里得到的 t0 就是一种 Trace 对象，这个 Scatter 类的 Trace 对象，是专门用于绘制各类点状图的。其实，在这个 Trace 对象中所规定的，跟前面字典中规定的意义相当，都是将最终要显示的图示中的某些元素，与相应的值建立映射关系。因此，Trace 对象可以这样来应用：</p>
<pre><code class="python language-python">plotly.offline.iplot([t0])    # ②

# 或者用下面的方式
# plotly.offline.iplot({"data":[t0]})    # ③
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d79813b0-4640-11e9-a3cb-3f7f3cd145c5" width = "70%" /></p>
<p>上面显示了 ② 和 ③ 两种写法，如果只有 data 参数，可以使用 ②。特别注意观察，这里是把 Trace 对象放到列表里面，跟前面字典放到列表中一样。不管是 Trace 对象还是字典，其作用都是，把即将创建的图示中的各个元素与某些值建立关系，并通过函数以 JSON 的方式把这个关系提交给 Plotly 服务器（或本地程序），然后就返回了制图。</p>
<p>如果有多个 Trace，可以利用 go.Data，将多个 Trace 对象封装为一个 Data 对象。go.Data 与 go.Scatter 类似之处在于，它们都是 Plotly 提供的数据对象，最终 Plotly 会根据所得到的 Trace 对象类型，生成相应的图示，也就是 go.XXXXX 类，是生成各种统计图的关键，如 go.Bar、go.Box、go.Heatmap 等。</p>
<pre><code class="python language-python">t1 = go.Scatter(x=[3, 2, 1],
                y=[4, 4.5, 5],
                name='black trace',
                text=['FIRST', 'SECOND', 'THIRD'],
                marker={'color':'black'})
data = go.Data([t0, t1])
type(data)

# out
plotly.graph_objs._deprecations.Data
</code></pre>
<p>此处得到的 Data 对象，可以用下面的方式提交到 API：</p>
<pre><code class="python language-python">plotly.offline.iplot({"data":data})
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1db7bcb0-4641-11e9-ba92-49a75a13a563" width = "70%" /></p>
<p>效果与原来一样。</p>
<p><strong>布局（Layout 对象）</strong></p>
<p>前面所呈现的图示，是在提交给 API 的 Trace 对象中规定了跟图线有关的内容，而对于得到的图示的坐标系，无法在 Trace 对象中配置，只能在 go.Layout 类中设置。</p>
<pre><code class="python language-python">layout=go.Layout(title="First Plot", xaxis={'title':'x1'}, yaxis={'title':'x2'})
type(layout)

# out
plotly.graph_objs._layout.Layout
</code></pre>
<p>Layout 对象（翻译为：布局对象），此处所 Layoout 对象是 go.Layout 的实例，它规定了未来的图示中横轴和纵轴的说明，以及这个图示的标注。这个对象以 JSON 格式与前面所说的 Data 等一同提交。</p>
<pre><code class="python language-python">plotly.offline.iplot({"data":data, 'layout':layout})
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/3cf28270-4643-11e9-ba92-49a75a13a563" width = "70%" /></p>
<p>使用 Layout 对象的好处在于，可以随时调整布局的结构—— Layout 对象是类字典对象，可以仿照字典的操作。例如，增加对某个点的标注。</p>
<pre><code class="python language-python">layout.update(dict(annotations=[go.Annotation(text='Center Point',x=2,y=5)]))    # ④
plotly.offline.iplot({"data":data, 'layout':layout})
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/4971f8f0-4643-11e9-a3cb-3f7f3cd145c5" width = "70%" /></p>
<p>④ 完全使用了字典的方法，增加了 Layout 对象的元素，即 go.Annotation 类的实例——对某点的标注。</p>
<p><strong>Figure 对象</strong></p>
<p>在 plotly.graph_objs 中有一个 Figure 对象，前面所说的 Data、Layout 对象，都是 Figure 对象里的元素——数据、布局样式都是属于图纸的。因此可以这样做：</p>
<pre><code class="python language-python">figure = go.Figure(data=data, layout=layout)
type(figure)

# out
plotly.graph_objs._figure.Figure
</code></pre>
<p>显然，只要将 Figure 对象提交到 API 即可。</p>
<pre><code class="python language-python">plotly.offline.iplot(figure)
</code></pre>
<p>所得结果与上图一样，不再重复显示。</p>
<h3 id="414">4.1.4 小结</h3>
<p>本课对 Plotly 绘制统计图仅给予简单介绍，因为它是一种完全不同于以往的绘图工具。使用它的基本思路是：将对所要绘制图形的要求，以 JSON 格式经函数发送到 API，Plotly 网站根据信息返回图示。并且 plotly.graph_objs 中有各种统计图的 Trace 对象，Plotly 会根据这些对象返回相应的统计图。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>