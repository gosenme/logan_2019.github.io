---
title: 案例上手 Python 数据可视化-24
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一课中，我们已经介绍过使用 Plotly 实现地理信息可视化的方法。但是，那个工具对我们不是很友好，特别是由于某种不可抗力的存在，可能根本无法调试。</p>
<p>不过，pyecharts 的确在地理信息可视化上做得不错——如果仅做国内地图，特别推荐使用，还是通过示例来说明吧。</p>
<p>首先，要安装地图文件，安装方法如下：</p>
<pre><code class="bash language-bash">$ pip install echarts-countries-pypkg         # 全球国家地图
$ pip install echarts-china-provinces-pypkg   # 中国省级地图
$ pip install echarts-china-cities-pypkg      # 中国市级地图
$ pip install echarts-china-counties-pypkg    # 中国县区地图
$ pip install echarts-china-misc-pypkg        # 中国区域地图
</code></pre>
<p>不仅可以安装上述官方提供的地图文件，还能够自己制作个性化的地图扩展，<a href="http://pyecharts.org/#/zh-cn/customize_map">具体请点击这里参阅</a>。</p>
<blockquote>
  <p>注意：上述文件安装完毕，要重新启动 jupyter notebook。</p>
</blockquote>
<h3 id="521">5.2.1 地图上的散点图</h3>
<p>有了上述基础，就可以进行地理信息可视化了（以下示例的数据源，<a href="https://github.com/qiwsir/DataSet/tree/master/pm25%EF%BC%89">请点击这里查看</a>）。</p>
<pre><code class="python language-python">import pandas as pd
from pyecharts import Geo

df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/pm25/pm2.csv")
city = df['CITY_NAME']
value = df['Exposed days']

geo = Geo("主要城市空气质量", "pm2.5", title_color = "#666666", title_pos = "center", 
          width=800, height=600, background_color = "#404a59")
geo.add("PM2.5", city, value, visual_range=[0, 300], visual_text_color='#fff', symbol_size=16, is_visualmap=True)
geo
</code></pre>
<p><img src="https://images.gitbook.cn/f7e6ada0-4967-11e9-9675-055a4c4b91fa" width = "70%" /></p>
<p>实现上述效果的类是 Geo，默认情况下绘制散点图，此外可以实现 type='effectScatter'（闪耀的散点图）和 type='heatmap'（热图）。</p>
<p>此图也是动态交互的，通过左侧图例选择不同数值范围，相应地会显示该范围内的数据。</p>
<p>如果按照前面所述安装了各种地图文件，还可以在 geo.add 方法中规定地理范围。</p>
<pre><code class="python language-python">df.sample(3)
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>RANK</th>
<th>CITY_ID</th>
<th>CITY_NAME</th>
<th>Exposed days</th>
</tr>
</thead>
<tbody>
<tr>
<td>115</td>
<td>127</td>
<td>97</td>
<td>阜新</td>
<td>91</td>
</tr>
<tr>
<td>40</td>
<td>45</td>
<td>88</td>
<td>丹东</td>
<td>49</td>
</tr>
<tr>
<td>71</td>
<td>79</td>
<td>55</td>
<td>吕梁</td>
<td>69</td>
</tr>
</tbody>
</table>
<p>在 pyecharts 地图中认可的城市名称都如同上述结果显示的那样，例如“阜新”，不要写成“阜新市”。</p>
<pre><code class="python language-python">js = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/jiangsu/city_population.csv")
js_cities = [name[:-1] for name in js.name]
js_cities

# out
['南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁']
</code></pre>
<p>下面就绘制江苏省的空气质量分布图。</p>
<pre><code class="python language-python">jspm = df[df['CITY_NAME'].isin(js_cities)]

geo = Geo(
    "江苏城市空气质量",
    "",
    title_color="#202020",
    title_pos="center",
    width=800,
    height=600,
    background_color="#666666",
)

geo.add(
    "",
    jspm['CITY_NAME'],
    jspm['Exposed days'],
    maptype="江苏",
    type="effectScatter",
    is_random=True,
    effect_scale=5,
    is_legend_show=False,
)
geo
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5ccd36d0-4968-11e9-9f9a-07ff224f37b2" width = "70%" /></p>
<p>这里的 geo.add 参数与前面的不同，导致了展示效果的差异。</p>
<h3 id="522">5.2.2 地图上的热图</h3>
<p>一直以来，房价都是人们关注的话题，下面就用可视化的方式研究一下近十年（2009—2018 年）全国部分城市平均房价（数据源：<a href="https://github.com/qiwsir/DataSet/tree/master/house%EF%BC%89%E3%80%82">https://github.com/qiwsir/DataSet/tree/master/house</a>）。</p>
<pre><code class="python language-python">hp = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/house/houseprice.csv")
hp['mean'] = hp.mean(axis=1)
hp.drop(index=46, inplace=True)    # 有城市在默认安装的地图文件中没有，将其删除
geo = Geo("主要城市房产均价", "", title_color='#111111', width=800, height=600)
geo.add('PRICE', hp['city_name'], hp['mean'], 
        visual_range=[2000, 40000], symbol_size=20, 
        is_visualmap=True, type="heatmap")
geo
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9360c590-4968-11e9-9675-055a4c4b91fa" width = "70%" /></p>
<p>在热图查看房价的基础上，为了更准确查看某些城市的房价走向，可以使用折线图看看趋势，例如下列几个城市。</p>
<pre><code class="python language-python">some_cities = hp[hp['city_name'].isin(['上海', '苏州', "北京", "南京", '杭州', '广州'])]

from pyecharts import Line
years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
line = Line('选择几个城市的房价', width=800, height=600)
for city in some_cities['city_name']:
    line.add(city, years, some_cities[some_cities['city_name']==city][years].values[0])
line
</code></pre>
<p><img src="https://images.gitbook.cn/9fbd71d0-4968-11e9-99d4-dfadbb5b8dbf" width = "70%" /></p>
<p>请注意，这里使用循环语句在同一个坐标系中绘制多个折线图。</p>
<h3 id="523">5.2.3 地理坐标系线图</h3>
<p>如果在地图上表示各地之间关系，可以使用 GeoLines 类，即地理坐标系线图。</p>
<pre><code class="python language-python">from pyecharts import GeoLines, Style

style = Style(title_color="#fff", title_pos="center", 
              width=800, height=600, background_color="#404a59")

data = [
    ["北京", "苏州"],
    ["北京", "哈尔滨"],
    ["北京", "呼和浩特"],
    ["北京", "乌鲁木齐"],
    ["北京", "西安"],
    ["北京", "广州"],
    ["北京", "贵州"],
    ["北京", "拉萨"]
]

geolines = GeoLines("直线图", **style.init_style)    #style.init_style表示使用前述style中的配置
geolines.add("BEIJING TO", data, is_legend_show=False)
geolines
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/acfcdcf0-4968-11e9-9675-055a4c4b91fa" width = "70%" /></p>
<p>类 Style 用于规定图示的风格，用它创建一个风格实例，此实例就可以多个图示，从而使不同图示的风格一致。而且调用方便，只需要在创建图示实例的时候，增加参数 **style.init_style 即可。</p>
<p>默认情况下，geolines.add 的参数中没有对图示中的线型做任何说明，就用有向直线表示。可以在原有的 style 实例基础上，增加一些关于风格的配置内容。</p>
<pre><code class="python language-python">geolines_style = style.add(
    is_label_show = True,
    line_curve = 0.3,    # 设置线的弧度
    line_opacity = 0.6,
    legend_text_color = "#eee",
    legend_pos = "right",
    geo_effect_symbol = "plane",    # 线端的形状
    geo_effect_symbolsize = 16,
    label_color = ['#a6c84c', '#ffa022', '#46bee9'],
    label_pos = "right",
    label_formatter = "{b}",
    label_text_color = "#eee",
)
</code></pre>
<p>geolines_style 是在 style 基础上配置完成的，也就包含了 style 的属性，当然，也可以利用 Style 类重新创建这个风格实例。上述的注释中说明了线型的两处设置，使得这次所得线型是曲线。</p>
<p>然后把 geolines_style 应用于 add 方法之中。</p>
<pre><code class="python language-python">geolines = GeoLines("曲线", **style.init_style)
geolines.add("Beijing To", data, **geolines_style)
geolines
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/dcb66c40-4968-11e9-a9ef-73aa0bf0b745" width = "70%" /></p>
<p>上面这个示例就来自于 pyecharts 的官网网站，因此，还是鼓励读者多去看官网。</p>
<h3 id="524">5.2.4 极坐标</h3>
<p>pyecharts 真心是一个好工具，只要发挥聪明才智，你就能够绘制出很多酷炫的图。</p>
<p>下面以极坐标绘制花瓣图案的示例为引子，希望能对读者有所启发。</p>
<pre><code class="python language-python">import math
from pyecharts import Polar

data = []
for i in range(361):
    t = i / 180 * math.pi
    r = math.sin(2 * t) * math.cos(2 * t)
    data.append([r, i])
polar = Polar("极坐标", width=800, height=600)
polar.add("Flower", data, start_angle=0, symbol=None, axis_range=[0, None])
polar
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f8b2e1d0-4968-11e9-9675-055a4c4b91fa" width = "70%" /></p>
<p>当然，这类图已经不是统计图了。数据可视化，不仅是绘制统计图表，也应该利用想象力，利用创新的方式表达数据，pyecharts 为此提供了可能。</p>
<h3 id="525django">5.2.5 在 Django 项目中发布可视化图像</h3>
<p>此前，所有的制图结果，要么是嵌入到 Jupyter 的浏览器中，要么是生成一个静态的 HTML 文件。那么，这些可视化的结果是否可以直接发布到 Web 项目中呢？</p>
<p><strong>可以。</strong> </p>
<p>此处就简要说明如何在 Django 项目中发布 pyecharts 的可视化图像，其实上一课中的 Plotly 也能实现类似功能。</p>
<blockquote>
  <p>注意：Django 是一个使用非常广泛的 Web 开发框架，完整内容请参阅拙作《跟老齐学 Python：Django 实战》（各大网店有售）。</p>
</blockquote>
<p>为本项目创建一个目录，并进入该目录，执行如下操作：</p>
<pre><code class="bash language-bash">promote:data-visual qiwsir$ cd django-pyecharts/    # 进入到项目目录
promote:django-pyecharts qiwsir$ django-admin startproject myecharts .    # 创建 Django 项目
promote:django-pyecharts qiwsir$ ls   # 在此目录中自动生成如下内容
manage.py    myecharts
</code></pre>
<p>注意，django-admin startproject myecharts . 的写法，不要丢掉最后的英文句点，表示要将此项目创建在当前目录中。</p>
<p>如此创建了一个基于 Django 框架的网站项目，然后在这个项目创建一个应用，并在这个应用中发布利用 pyecharts 创建的可视化结果。</p>
<p>在当前目录中继续执行如下操作，旨在创建一个名为 visualdata 的应用。</p>
<pre><code class="bash language-bash">promote:django-pyecharts qiwsir$ python3 manage.py startapp visualdata
promote:django-pyecharts qiwsir$ tree    # 此时的目录结构
.
├── manage.py
├── myecharts
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-37.pyc
│   │   └── settings.cpython-37.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── visualdata
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py

4 directories, 14 files
</code></pre>
<p>进入到 myecharts 目录，并编辑其中的 settings.py 文件，找到下面所示的部分代码，并按照注释中的说明增加新的应用。</p>
<pre><code class="python language-python">INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'visualdata',     # 新创建的应用名称
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],    # 设置模板目录
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
</code></pre>
<p>再编辑 ./myecharts 目录中的 urls.py 文件。</p>
<pre><code class="python language-python">from django.contrib import admin
from django.urls import path, include    # 比原来多引入了 include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('visualdata/', include('visualdata.urls', namespace='visualdata')),    # 新增
]
</code></pre>
<p>以上两个文件编辑完毕，进入到所创建的应用的目录，即项目根目录下的 ./visualdata 中，<a href="http://xn--urls-zf5fr5b75ii8n3qq2gbc95b9na.py/">并在其中新建文件 urls.py</a>，在此文件中写入如下代码：</p>
<pre><code class="python language-python">from django.urls import path
from . import views

app_name = "visualdata"

urlpatterns = [
    path("", views.visual, name='visual'),
]
</code></pre>
<p>本项目中，将 Django 的静态页面写到指定的模板目录中，在 ./myecharts/settings.py 中已经规定了本项目的模板目录。进入到本项目的根目录，创建 templates 子目录，最终项目的目录结构为：</p>
<pre><code class="bash language-bash">promote:django-pyecharts qiwsir$ tree
.
├── manage.py
├── myecharts
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates    # 模板文件目录
└── visualdata    # 应用目录
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

8 directories, 16 files
</code></pre>
<p>基本结构部署完毕，就开始编写视图函数。编辑 ./visualdata/views.py 文件，代码如下：</p>
<pre><code class="python language-python">from django.shortcuts import render
from pyecharts import GeoLines, Style

# 绘制地图中直线图的函数
def geo_lines():    
    style = Style(title_color="#fff", title_pos="center", width=800, height=600, background_color="#404a59")
    data = [
        ["北京", "苏州"],
        ["北京", "哈尔滨"],
        ["北京", "呼和浩特"],
        ["北京", "乌鲁木齐"],
        ["北京", "西安"],
        ["北京", "广州"],
        ["北京", "贵州"],
        ["北京", "拉萨"]
        ]
    geolines = GeoLines("直线图", **style.init_style)
    geolines.add("BEIJING TO", data, is_legend_show=False)
    return geolines

# 视图函数
def visual(request):
    geolines = geo_lines()    
    geo = dict(
        echarts = geolines.render_embed(),
        script = geolines.get_js_dependencies()
    )
    return render(request, 'visualdata/visual.html', {'geo':geo})
</code></pre>
<p>然后编写模板文件。进入到 ./templates 目录中，创建子目录 visualdata，在此子目录中创建 visual.html 模板文件，即最终得到：./templates/visualdata/visual.html。模板文件的代码如下：</p>
<pre><code class="html language-html">&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="utf-8"&gt;
    &lt;title&gt;Geolines&lt;/title&gt;
    {% for jsfile_name in geo.script %}
        &lt;script src="https://pyecharts.github.io/assets/js/{{ jsfile_name }}.js"&gt;&lt;/script&gt;
    {% endfor %}
&lt;/head&gt;

&lt;body&gt;
&lt;h2&gt;FLY FORM BEIJING TO OTHERS CITIES&lt;/h2&gt;
  {{ geo.echarts|safe }}
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>这里简化了 JavaScript 脚本的引入，使用 pyecharts 官方提供的地址，也可以到 <a href="https://github.com/pyecharts/assets">https://github.com/pyecharts/assets</a> 下载 JS 库，部署到自己的项目中。</p>
<p>以上都完成，并保存文件之后，进入到项目根目录，执行如下指令：</p>
<pre><code class="bash language-bash">promote:django-pyecharts qiwsir$ python3 manage.py runserver

January 31, 2019 - 07:55:55
Django version 2.2, using settings 'myecharts.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
</code></pre>
<p>然后打开浏览器，在地址栏中输入：http://127.0.0.1:8000/visualdata/，如一切顺利，就能打开下图样式的页面。</p>
<p><img src="https://images.gitbook.cn/cf791ca0-496b-11e9-99d4-dfadbb5b8dbf" width = "70%" /></p>
<p>以上仅仅是非常简要地演示 pyecharts 如何在 Web 项目中发布，借鉴课程内容，你可以在网站项目中做出更复杂的页面。</p>
<h3 id="526">5.2.6 小结</h3>
<p>本课对 pyecharts 在地理数据可视化以及 Web 项目中如何发布可视化结果进行了介绍，还以简单的极坐标展示了多样化的作图方法。通过本课的学习，读者可以体会到，pyecharts 能够帮助我们完成很多可视化工作。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>