---
title: 案例上手 Python 数据可视化-27
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>经过我们前面的讲解，已经基本展示了 Bokeh 的应用。但是，或许也留下了一个不太好的印象，似乎这个东西的功能也没有什么太特别的，尤其是针对某些常用统计图而言，缺少以往工具的那种更直接的方法。对于 Bokeh 而言，我认为它并非是为绘制统计图而生，而是为多样化的、更灵活的数据可视化而生，特别是在交互性上，它的特色就非常鲜明了。</p>
<p>首先，要确定已经把安装的 Bokeh 设置了环境变量。例如我在自己的计算机中完成了如下操作：</p>
<pre><code class="bash language-bash">ln -s /Library/Frameworks/Python.framework/Versions/3.7/bin/bokeh /usr/local/bin/bokeh
</code></pre>
<p>完成了这个软连接的操作之后，就能够在任何地方执行 bokeh xxxx 的操作了。</p>
<p>以上准备工作结束，就打开本地的代码编辑器，输入如下代码（来自 Bokeh 官方示例）：</p>
<pre><code class="python language-python">import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b
    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
</code></pre>
<p>将文件保存到某个目录中，并命名为 inter_sin.py。</p>
<p>然后进入到该目录，执行如下指令：</p>
<pre><code class="bash language-bash">$ bokeh serve --show inter_sin.py
</code></pre>
<p>上述指令执行之后，会看到类似下面的信息：</p>
<pre><code class="bash language-bash">2019-01-31 13:26:32,754 Starting Bokeh server version 1.0.4 (running on Tornado 5.1.1)
2019-01-31 13:26:32,759 Bokeh app running at: http://localhost:5006/inter_sin
2019-01-31 13:26:32,759 Starting Bokeh server with process id: 37729
2019-01-31 13:26:33,441 200 GET /inter_sin (::1) 108.82ms
2019-01-31 13:26:33,607 101 GET /inter_sin/ws?bokeh-protocol-version=1.0&amp;bokeh-session-id=26KlDWgq2snZshJoVWCemP9aKvlUHmWsBogrA0WKgeLB (::1) 0.71ms
2019-01-31 13:26:33,607 WebSocket connection opened
2019-01-31 13:26:33,607 ServerConnection created
</code></pre>
<p>并且会自动打开一个页面，这个页面的地址是 http://localhost:5006/inter_sin，页面的内容如下图所示。</p>
<p><img src="https://images.gitbook.cn/93ee8a80-4ac4-11e9-816f-a94bb1ffd325" width = "70%" /></p>
<p>在网页中，可以拖动正弦曲线图左侧的各个滑块，即修改正弦函数的有关参数，可以观察到函数曲线的实时变化。</p>
<p>这就是 Bokeh 给我们带来的交互性，正是它的特色。</p>
<p>在上一部分中，我们曾经介绍了如何在 Django 项目中发布 pyecharts 的制图结果，所有的 Web 项目都要有一个服务器，Django 项目中使用的是 Django 的服务。但是在这里，我们使用的是 Bokeh 的服务，也就是 Bokeh 自带服务器。</p>
<p>Bokeh 的<a href="https://bokeh.pydata.org/en/latest/docs/user_guide/server.html">官方详细说明</a>中非常详细地介绍了自身的服务器，基本结构如下图所示（图示源自官方网站）。</p>
<p><img src="https://images.gitbook.cn/c5b30500-4ac4-11e9-95d4-c9806df1e112" width = "60%" /></p>
<p>对照前面的示例，其中的文件 inter_sin.py 就是图中的“App Code”，执行指令 bokeh serve --show inter_sin.py，启动服务器。运行 App，创建上图中的 Document，从而对客户端的请求做出相应，然后在客户端浏览器呈现图示。</p>
<p>Bokeh 为 App 提供了如下模式。</p>
<ul>
<li>单组件模式：即只有一个“.py”文件，如上例所示。</li>
<li>目录模式：即有一个目录，在目录中可以有一个或者多个“.py”文件，以及其他有关的文件或者目录。</li>
</ul>
<p>此外，Bokeh 服务器还可以与其他服务器协同工作，比如嵌入到 Tornado 框架的 Web 中，或者用 Nginx 反向代理等。本课在这里不对这些内容做更多介绍，请你参阅官方文档。下面仅就“单组件模式”的“.py”文件中的有关代码给予说明，因为这是最基本的。</p>
<p><a href="http://xn--points-9v7is7c8ynsrll5br45b5otcz5ffx7b.py/">在编辑器中创建文件 points.py</a>，其代码如下：</p>
<pre><code class="python language-python">from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from numpy.random import random

N = 300
source = ColumnDataSource(data={'x': random(N), 'y': random(N)})    # ①

plot = figure()
plot.circle(x='x', y='y', source=source)

slider = Slider(start=100, end=1000, value=N, step=10, title='Number of points')    # ②

def callback(attr, old,  new):    # ③
    N = slider.value    # ④
    source.data = {'x': random(N), 'y': random(N)}    # ⑤

slider.on_change('value', callback)    # ⑥

layout = column(slider, plot)    # ⑦

curdoc().add_root(layout)    # ⑧
</code></pre>
<p>在保存此文件的目录中，执行 bokeh serve --show points.py，会在浏览器中看到如下效果的页面。</p>
<p><img src="https://images.gitbook.cn/fff2f9f0-4ac4-11e9-816f-a94bb1ffd325" width = "60%" /></p>
<p>拖动上面的滑块，概念数量，图中的点的个数也同时变化。再看看代码，两厢对照理解。</p>
<p>利用 Bokeh 制图，其所需要的数据可以有两类提供方式。<strong>一类是直接提供类列表数据</strong>，例如列表、数组等，另外一类是 Bokeh 中规定的<strong>专用数据类型</strong>，即 ColumnDataSource，这种类型的数据便于在多个图示或者交互工具中共享，可以把它理解为类似 Pandas 中的 DataFrame。</p>
<p>① 就是创建了一个 ColumnDataSource 类的实例对象，也可以说是 ColumnDataSource 类型的对象。这种类型的对象，通常用于图示对象的绘图方法的参数 source 的值。例如上述代码中的 plot.circle(x='x', y='y', source=source)，其含义即为绘制圆点的数据来源为 source=source —— 变量 source 引用的就是刚才定义的 ColumnDataSource 对象，x='x', y='y' 分别规定了坐标点的值来自 ColumnDataSource 对象的 'x', 'y' 两个键的值。</p>
<p>关于 ColumnDataSource 更多的资料，请阅读<a href="https://bokeh.pydata.org/en/latest/docs/user_guide/data.html#columndatasource">官方文档</a>。</p>
<p>② 的 Slider 类，是用于创建一个滑块对象，它可以用 from bokeh.models import Slider 的方式引入，也可以使用高级接口 from bokeh.models.widgets import Slider 的方式引入。不论哪种方式，都是来自于 bokeh.models，这个类是 Bokeh 制图的根本类。官方网站为此提供了一张图，如果结合上述程序示例，能够更好地理解 Bokeh 绘制图示的基本思想。</p>
<p><img src="https://images.gitbook.cn/49ce2450-4ac5-11e9-816f-a94bb1ffd325" width = "60%" /></p>
<p>在本例中，就包含了两部分：一部分是图示（即 GlyphRenderer），另外一部分是小工具（Widgets），分别用 plot = figure() 和 ② 创建了实例。</p>
<p>如何将两个对象组合？这就是 ⑦ 的作用，使用 bokeh.layouts.column。bokeh.layouts 提供了多种布局函数，具体参阅<a href="https://bokeh.pydata.org/en/latest/docs/reference/layouts.html">官方文档</a>。此处使用的 column 实现各个对象的竖直排列布局。</p>
<p>② 创建了滑块，如果拖动，会看到数值的变化，即 Slider 类的实例的属性 slider.value 的值会随着滑块的移动而变化。若要实现此值变化的同时，图示中的点也变化，就必须要修改 ① 所创建的实例的数据变化。为此要完成 ③ 到 ⑥ 的操作。</p>
<p>③ 是一个函数，因为这个函数被用在了 ⑥，所以也称为“回调函数”。③ 的作用是根据 slider.value 的值（见 ④）修改 source.data 的值（见 ⑤）。</p>
<p>为了实现滑块数值与 source 值同步，还需要 ⑥，通过 slider.on_change 方法，实现了滑块数值变化，同时修改 source 实例的值。</p>
<p>程序都写好了。当通过 Bokeh 服务器加载此程序的时候，要能够返回文件，以供客户端访问，并将此程序的内容返给客户端。这就要在程序的最后必须写上 ⑧。curdoc() 的作用就是范围当前的文件，并且将 ⑦ 最终封装的对象加载，从而实现客户端请求后返回 BokehJS 到浏览器，并生成所看到的结果。其实，在前面也用过类似的，只不过是生成单独的 HTML 文件，即 output_file，也可以通过 from bokeh.io import output_file 方式引入。</p>
<p>从上述示例可以看出，实现什么样的交互，其关键是看 Bokeh 中提供了什么类型的工具（Widget），在官方文档对列出了如下工具（类）：</p>
<pre><code class="python language-python">from bokeh.models.widgets import Button, 
                                 CheckboxButtonGroup, 
                                 CheckboxGroup, 
                                 DataTable, 
                                 Dropdown,
                                 MultiSelect，
                                 RadioButtonGroup,
                                 RadioGroup,
                                 Select,
                                 Slider,
                                 RangeSlider,
                                 Panel, 
                                 Tabs,
                                 TextInput,
                                 Toggle,
                                 Div,
                                 Paragraph,
                                 PreText
</code></pre>
<p><a href="https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html">官方文档</a>对这些工具有完整的阐述，请参阅，此处不一一赘述，其使用方法与本节的示例雷同。</p>
<h3 id="">本节总结</h3>
<p>本节通过对 Bokeh 中的小工具介绍，突出了 Bokeh 在交互性上的特点，并且它支持服务器模式，更拓展了 Bokeh 的应用领域。</p>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>