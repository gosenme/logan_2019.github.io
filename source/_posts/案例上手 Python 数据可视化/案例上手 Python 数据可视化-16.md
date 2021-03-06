---
title: 案例上手 Python 数据可视化-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面两课分别介绍了 Matplotlib 和 Seaborn，其基本的绘图思想是一样的：面向对象修改或添加对象的属性。本课要介绍的 Plotnine，看标题就明白，它必然有不同以往之处，也的确与 Matplotlib 体系有所不同。</p>
<p>Plotnine 在绘图上，引入了“图层”的概念——如果熟悉美工妹妹的工作，这个概念就不难理解。它不是师承于 Matplotlib，而是基于 ggplot2。</p>
<h3 id="311">3.1.1 渊源和特点</h3>
<p>能够用于数据科学的语言不只是 Python，还有很多其他语言，比如 R ——一个具有一定历史并且目前也被很多人使用的语言。</p>
<blockquote>
  <p>R 语言，主要用于统计分析、绘图、数据挖掘，由新西兰奥克兰大学的罗斯·伊哈卡和罗伯特·杰特曼发明。</p>
</blockquote>
<p>那么，支持 R 语言绘图的工具之一就是 ggplot2（官网：<a href="https://ggplot2.tidyverse.org/">https://ggplot2.tidyverse.org/</a>），它由 Hadley Wickham 创建，其绘图基本思想是（以下是基本概念介绍，参考了 <a href="http://www.sthda.com/english/wiki/be-awesome-in-ggplot2-a-practical-guide-to-be-highly-effective-r-software-and-data-visualization">STHDA</a> 的有关内容）：</p>
<blockquote>
  <p>Plot（图）= Data（数据集）+ Aesthetics（美学映射）+ Geometry（几何对象）</p>
</blockquote>
<p>这种制度的基本规则来自于 <a href="https://www.amazon.com/Grammar-Graphics-Statistics-Computing/dp/0387245448/ref=as_li_ss_tl?ie=UTF8&qid=1477928463&sr=8-1&keywords=the+grammar+of+graphics&linkCode=sl1&tag=ggplot2-20&linkId=f0130e557161b83fbe97ba0e9175c431">The Grammar of Graphics</a> 一书中的规定，各项的含义如下：</p>
<ul>
<li>Data，数据集；</li>
<li>Aesthetics，美学映射，比如将变量映射给 X、Y 坐标轴，或者映射给颜色、大小、形状等图形属性；</li>
<li>Geometry，几何对象，比如柱形图、直方图、散点图、线图、密度图等。</li>
</ul>
<p>在 ggplot2 中有两个主要绘图函数：</p>
<ul>
<li>qplot，快速绘图；</li>
<li>ggplot，此函数是 ggplot2 的精髓，远比 qplot() 强大，可以绘制复杂的图形。</li>
</ul>
<p>在 ggplot2 中有几个基本概念，需要了解一下。</p>
<ul>
<li>图层（Layer）：一个图层好比是一张“透明纸”，包含有各种图形元素，可以分别建立不同的图层，然后叠放在一起，组合成图形的最终效果。</li>
<li>标度（Scale）：标度控制了数学空间到图形元素空间的映射。一组连续数据可以映射到 X 轴坐标，也可以映射到一组连续的渐变色彩；一组分类数据可以映射成为不同的形状，也可以映射成为不同的大小。</li>
<li>坐标系（Coordinate）：坐标系控制了图形的坐标轴并影响所有图形元素，最常用的是直角坐标轴。坐标轴可以进行变换以满足不同的需要，如对数坐标，其他可选的还有极坐标。</li>
<li>位面、组图、分面（Facet）：很多时候需要将数据按某种方法分组，分别进行绘图。facet 就是控制分组绘图的方法和排列形式。（注意，将 facet 翻译为“位面”，有时候会造成误解，因为 planes 也翻译为“位面”）。</li>
</ul>
<p>这是 R 的 ggplot2 的概念，Python 要挑战 R 语言，那么它有的 Python 就要有了，这样，我们在 Python 中也能使某些绘图工具，实现上述的绘图思想。比较常用的有：</p>
<ul>
<li>ggplot，官网：<a href="http://ggplot.yhathq.com/">http://ggplot.yhathq.com/</a></li>
<li>Plotnine，官网：<a href="https://plotnine.readthedocs.io/en/stable/about-plotnine.html">https://plotnine.readthedocs.io/en/stable/about-plotnine.html</a></li>
</ul>
<p>Plotnine 因为继承了 R 语言的 ggplot2 的绘图思想，因此，图层概念就是它的核心。</p>
<p>Plotnine 的安装应该已经在第 0-3 课中完成了，如果尚未安装，请参考之。</p>
<h3 id="312">3.1.2 理解图层含义</h3>
<p>先用一个示例体会一下“分层绘图—图层”的思想和操作流程。</p>
<p>在 Plotnine 中，也有类似 Seaborn 那样集成的数据集。</p>
<pre><code class="python language-python">%matplotlib inline
import plotnine as p9
from plotnine import data
mg = data.mpg
mg.head()
</code></pre>
<p><img src="https://images.gitbook.cn/Fpo3ovuJZrpERL6lUO3QPTcI-EXH" alt="avatar" /></p>
<pre><code class="python language-python">mg.info()

#out
&lt;class 'pandas.core.frame.DataFrame'&gt;
RangeIndex: 234 entries, 0 to 233
Data columns (total 11 columns):
manufacturer    234 non-null category
model           234 non-null category
displ           234 non-null float64
year            234 non-null int64
cyl             234 non-null int64
trans           234 non-null category
drv             234 non-null category
cty             234 non-null int64
hwy             234 non-null int64
fl              234 non-null category
class           234 non-null category
dtypes: category(6), float64(1), int64(4)
memory usage: 13.9 KB
</code></pre>
<p>这个数据集中记录了一些跟汽车有关的数据，其中三个特征，是下面将要用到的：</p>
<ul>
<li>displ，发动机排气量；</li>
<li>hwy，高速公路上每加仑汽油能够行驶的路程；</li>
<li>cyl，汽缸数目。</li>
</ul>
<p>因为 Plotnine 继承了 ggplot2，本质上可以理解为就是要跟 R 语言争夺绘图领域的老大地位。那么如果读者是 Plotnine 的发明者，会如何命名自己的函数，才能更有利于把原来使用 ggplot2 的用户争取过来呢？</p>
<p><strong>当然是所有的函数和语法都要保持与 ggplot2 一样。</strong></p>
<p>英雄所见略同，都想到一起了。凡是在 ggplot2 中能够使用的函数，在 Plotnine 中几乎都有，而且使用方式也一样。因此，如果以前学过了 ggplot2，迁移过来丝毫不费力；如果没学过，那么当然就需要阅读本课程了。当然，如果在网上搜索到了 ggplot2 的方法，也可以直接拿到 Plotnine 中使用。</p>
<p>这招的确很绝妙，这就是所谓的后发优势。</p>
<p>那就先制作第一张图。</p>
<pre><code class="python language-python">p9.ggplot(mg, p9.aes('displ', 'hwy', color='factor(cyl)'))    #①

# 或者用下面的方式，也是可以的
#(p9.ggplot(mg, p9.aes('displ', 'hwy', color='factor(cyl)')))
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/07c439a0-453e-11e9-9b40-8d81bb51beff" width = "70%" /></p>
<p>Plotnine 的书写方式，看似与以往的 Matplotlib 不同——这是正常的，它继承自 ggplot2。不过，如果分解来看，就是按照“图层”在操作。</p>
<p>p9.ggplot 是 Plotnine 中绘图的类——这里命名上有点不完全合乎 Python 的习惯，类的名字用全小写的了。但说“类”是正确的，因为图形的每个组成部分其实就是一个对象——传入参数后就创建了一个该类的实例。</p>
<pre><code class="python language-python">p9.ggplot(mapping=None, data=None, environment=None)
</code></pre>
<ul>
<li>mapping：即所谓的美学映射（Aesthetics），除非专门对其隐藏，此映射会用于所有的层。</li>
<li>data：此次绘图所用的数据。如果某图层，没有特别声明自己的数据，都将使用这里的数据。</li>
</ul>
<p>语句 ① 如果按照这两个参数的意义来写，可以写成下面的形式：</p>
<pre><code class="python language-python">p9.ggplot(mapping=p9.aes('displ', 'hwy', color='factor(cyl)'), data=mg)
</code></pre>
<p>但是，这种写法没有明确显示出图层的含义。因此，通常更换一种书写格式，本质上跟 ① 是相同的。</p>
<pre><code class="python language-python">(p9.ggplot(mg)    #②
 + p9.aes(x='displ', y='hwy', color='factor(cyl)')    #③
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/07c439a0-453e-11e9-9b40-8d81bb51beff" width = "70%" /></p>
<p>这种写法的输出结果与 ① 完全一样。</p>
<ul>
<li>将 ② 和 ③ 分为两行，然后用 + 连接，并且它们都在一个最外层的括号里面，可以理解为它们都属于一张图。</li>
<li>② 是使用 p9.ggplot 加载数据，正如前面对参数解释的那样，通常将此处加载的数据用于所有图层。</li>
<li>③ 是一个图层，这个图层是用 p9.aes 类来实现的，其实就是建立了所谓的“美学映射”，即将 ② 中所加载的数据中的特征“displ”和特征“hwy”分别作为横纵坐标轴。这里的参数 color，请看后续讲述。美学映射这一层，可以应用到后面的所有图层，也就是说，后续的图层，都是在这个坐标系图层之上。</li>
</ul>
<p>到目前为止，还没有在坐标系中看到任何图像，也就是前面所说的 Geometry（几何对象）。</p>
<p>在 Plotnine 中有很多名字形式是 geom_* 的类，这些类都是用来绘制特定几何对象的，如下表列出的几个，请欣赏。</p>
<table>
<thead>
<tr>
<th>名称</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>geom_bar</td>
<td>柱形图</td>
</tr>
<tr>
<td>geom_boxplot</td>
<td>箱线图</td>
</tr>
<tr>
<td>geom_point</td>
<td>散点图</td>
</tr>
<tr>
<td>geom_violin</td>
<td>提琴图</td>
</tr>
</tbody>
</table>
<p>Plotnine 中能够绘制的几何对象还有很多，<a href="https://plotnine.readthedocs.io/en/stable/api.html#geoms%E3%80%82%E6%9C%AC%E4%B9%A6%E7%9A%84%E7%89%B9%E8%89%B2%E5%B0%B1%E6%98%AF%E6%80%BB%E5%9C%A8%E4%B8%8D%E5%8E%8C%E5%85%B6%E7%83%A6%E5%9C%B0%E6%8F%90%E7%A4%BA%E8%AF%BB%E8%80%85%EF%BC%8C%E8%A6%81%E5%AD%A6%E4%BC%9A%E7%9C%8B%E6%96%87%E6%A1%A3%E3%80%82">具体可以参考这里</a>。</p>
<blockquote>
  <p>本课程的特色就是总在不厌其烦地提示读者，要学会看文档。</p>
</blockquote>
<p>接下来，在 ② ③ 基础上，再增加一个图层，该图层就是一种几何对象：</p>
<pre><code class="python language-python">(p9.ggplot(mg)    
 + p9.aes(x='displ', y='hwy', color='factor(cyl)') 
 + p9.geom_point()    #④
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9dea55e0-453e-11e9-b363-c7a998ed42df" width = "80%" /></p>
<p>④ 就是增加的几何对象，将 ② 所载入的数据，根据 ③ 所确定的映射关系，绘制成 ④ 所规定的几何图像。</p>
<p>再看图像，④ 中的 geom_point 类表示要绘制的散点图。从图示结果中可看出，散点图点的颜色，根据数据集中的另外一个特征“cyl”进行了区分，这是因为在 ③ 美学映射中的参数 color='factor(cyl)'。</p>
<p>④ 仅仅是声明了几何对象，没有再对数据和美学映射做任何修改，因此，这些都使用了 ② 和 ③ 中的值。</p>
<p>依照上面的规则，还可以继续增加新的几何对象——新的图层。</p>
<pre><code class="python language-python">(p9.ggplot(mg)    
 + p9.aes(x='displ', y='hwy', color='factor(cyl)')    
 + p9.geom_point()
 + p9.geom_smooth()    #新增的图形，几何对象
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c514bbb0-453e-11e9-b363-c7a998ed42df" width = "80%" /></p>
<p>至此，我们已经对 Plotnine 的图层概念有了初步体验。当然，在具体的绘图过程中还有很多技巧，有待后续介绍。</p>
<h3 id="32">3.2 小结</h3>
<p>本课是利用 Plotnine 实现数据可视化的体验，关键是要理解“图层”的含义，基本的代码格式如下所示：</p>
<pre><code>(p9.ggplot(data)    # 加载数据
 + p9.aes()            # 美学映射层
 + p9.geom_*()      # 几何对象层
 + ...                     # 更多层
)
</code></pre>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>