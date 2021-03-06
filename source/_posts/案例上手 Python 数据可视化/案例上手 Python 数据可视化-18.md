---
title: 案例上手 Python 数据可视化-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在 Plotnine 官方网站中，提供了一些比较经典的案例，如果能够将这些案例分析清楚，对提高 Plotnine 的应用技能大有裨益。本课就选择两个案例抛砖引玉，供参考。</p>
<h3 id="331">3.3.1 柱形图及坐标轴设置</h3>
<p>本案例是关于柱形图和对其坐标轴设置，案例中核心类为 plotnine.geoms.geom_col（<a href="https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_col.html#two-variable-bar-plot">点击这里详见官方地址</a>）。</p>
<p>还是先创建数据集：</p>
<pre><code>import pandas as pd
import numpy as np
from plotnine import *

df = pd.DataFrame({
    'variable': ['gender', 'gender', 'age', 'age', 'age', 'income', 'income', 'income', 'income'],
    'category': ['Female', 'Male', '1-24', '25-54', '55+', 'Lo', 'Lo-Med', 'Med', 'High'],
    'value': [60, 40, 50, 30, 20, 10, 25, 25, 40],
    })
df['variable'] = pd.Categorical(df['variable'], categories=['gender', 'age', 'income'])
df
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>variable</th>
<th>category</th>
<th>value</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>gender</td>
<td>Female</td>
<td>60</td>
</tr>
<tr>
<td>1</td>
<td>gender</td>
<td>Male</td>
<td>40</td>
</tr>
<tr>
<td>2</td>
<td>age</td>
<td>1-24</td>
<td>50</td>
</tr>
<tr>
<td>3</td>
<td>age</td>
<td>25-54</td>
<td>30</td>
</tr>
<tr>
<td>4</td>
<td>age</td>
<td>55+</td>
<td>20</td>
</tr>
<tr>
<td>5</td>
<td>income</td>
<td>Lo</td>
<td>10</td>
</tr>
<tr>
<td>6</td>
<td>income</td>
<td>Lo-Med</td>
<td>25</td>
</tr>
<tr>
<td>7</td>
<td>income</td>
<td>Med</td>
<td>25</td>
</tr>
<tr>
<td>8</td>
<td>income</td>
<td>High</td>
<td>40</td>
</tr>
</tbody>
</table>
<p>然后绘制柱形图：</p>
<pre><code class="python language-python">(ggplot(df, aes(x='variable', y='value', fill='category'))
 + geom_col()
)
</code></pre>
<p><img src="https://images.gitbook.cn/4414e150-459a-11e9-81d0-97204205141b" width = "80%" /></p>
<p>代码比较简单，但是因为特征 variable 的每个值所对应的 value 特征值自动成为一个柱子，而该柱子又是根据 fill='category' 填充（即柱子本身根据特征 category 的值划分为若干部分），图显得有点乱，不如绘制簇状柱形图清晰。</p>
<pre><code class="python language-python">(ggplot(df, aes(x='variable', y='value', fill='category'))
 + geom_col(stat='identity', position='dodge')    #①
)
</code></pre>
<p><img src="https://images.gitbook.cn/da9b8560-45a0-11e9-81d0-97204205141b" width = "80%" /></p>
<p><strong>① 增加了两个参数，就改为簇状柱形图了。</strong></p>
<ul>
<li>stat：默认为 'identity'，表示对本图层数据进行统计变换。当然，这不是出现“簇”的决定参数。</li>
<li>position：默认为 'stack'，表示堆叠的柱形图。如果设置为 'dodge'，就出现簇了。</li>
</ul>
<p>旁边虽然有图例，可以对应看到每种颜色的柱状图所表示的 category 值，但是，不如直接在柱形图上标示更清晰。为此可以进行如下修改：</p>
<pre><code class="python language-python">dodge_text = position_dodge(width=0.9)                              # ②

(ggplot(df, aes(x='variable', y='value', fill='category'))
 + geom_bar(stat='identity', position='dodge', show_legend=False)   # ③
 + geom_text(aes(y=-.5, label='category'),                          # ④
             position=dodge_text,
             color='gray', size=8, angle=45, va='top')
 + lims(y=(-5, 60))                                                 # ⑤
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0ba3dbd0-45a1-11e9-81d0-97204205141b" width = "80%" /></p>
<p>比较本图和上面的图，虽然去掉了图例，但是在每个柱子下面非常清楚地标明了来自于特征 category 的值。下面通过阅读代码，研习实现方式。</p>
<ul>
<li>图中的每个“簇”只有一个“中心”，对该“簇”的标示，就显示在中心刻线处。但是，如果这样，就不能对每簇的多个柱子标示了。因为效果必将是标示不同柱子文字（category，特征的数据）重叠起来，并位于中心刻线处。为此，就要设置各数据的显示距离。这就是 ② 的作用，其应用见 ④ 中的参数 position。</li>
<li>③ 相对原来的 ① 修改了类名称，这里使用了 geom_bar，它与 geom_col 没有什么区别，重点在于 show_legend=False，这个参数用于将图例关闭。</li>
<li>④ 是新增的图层，用它来展示 category 特征的值——对应相应的柱子。<ul>
<li>geom_text 专用于控制文本图层的类（<a href="https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_text.html?highlight=geom_text">点击这里查看官方文档</a>）。跟设置其他图层对象一样，也有参数 mapping，在 ④ 中其值为 aes(y=-.5, label='category')，“y=-.5” 表示这个文本图层对象 Y 轴的映射为常数，即规定了文本对象在 Y 轴方向的位置。</li>
<li>position 的值为 ② 中得到的对象。</li>
<li>angle=45，文字逆时针旋转的角度。</li>
<li>在 ④ 中所规定的美学映射中，没有规定 X 轴，则会继承在 ① 中设定的美学映射值。</li></ul></li>
<li>⑤ 的作用是要扩展 Y 轴的范围，默认是从 0 开始的。</li>
</ul>
<p>柱形图的一个缺陷在于不能很精确地显示某项的数值，它擅长的是显示各个不同项之间的相对大小。但是，如果在每个柱子上标示出相应的值，不就能克服这个缺陷了吗？</p>
<p>不错的想法。</p>
<p>标示数值，也是文本对象，因此只需要增加 geom_text 图层对象即可，不过要注意参数配置，才能正好显示在每个柱子的顶部。</p>
<pre><code class="python language-python">dodge_text = position_dodge(width=0.9)

(ggplot(df, aes(x='variable', y='value', fill='category'))
 + geom_bar(stat='identity', position='dodge', show_legend=False)
 + geom_text(aes(y=-.5, label='category'),
             position=dodge_text,
             color='gray', size=8, angle=45, va='top')
 + geom_text(aes(label='value'),                     # ⑥
             position=dodge_text,
             size=8, va='bottom', format_string='{}%')
 + lims(y=(-5, 60))
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5a7837b0-45a1-11e9-aea4-95aeabea01e4" width = "80%" /></p>
<p>⑥ 是新增的图层，用于显示柱子顶部的数值。在 geom_text 中所设置的美学映射为 aes(label='value')，没有在这里设置 X 和 Y 轴的映射数据，如前所述，它会继承来自 ① 的相应映射（包括 ① 中的参数 fill='category'）。因此，相应的数字才能知道自己的所在位置。</p>
<p>在本案例的最后，通过设置主题，将图示美化了一番。</p>
<pre><code class="python language-python">dodge_text = position_dodge(width=0.9)
ccolor = '#555555'

(ggplot(df, aes(x='variable', y='value', fill='category'))
 + geom_bar(stat='identity', position='dodge', show_legend=False)
 + geom_text(aes(y=-.5, label='category'),
             position=dodge_text,
             color=ccolor, size=8, angle=45, va='top')              # ⑦
 + geom_text(aes(label='value'),
             position=dodge_text,
             size=8, va='bottom', format_string='{}%')
 + lims(y=(-5, 60))
 + theme(panel_background=element_rect(fill='white'),               # ⑧
         axis_title_y=element_blank(),
         axis_line_x=element_line(color='black'),
         axis_line_y=element_blank(),
         axis_text_y=element_blank(),
         axis_text_x=element_text(color=ccolor),
         axis_ticks_major_y=element_blank(),
         panel_grid=element_blank(),
         panel_border=element_blank())
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/a45604b0-45a2-11e9-b5ba-8f1c1da573a0" width = "80%" /></p>
<p>⑦ 中更换了参数 color 的值，别的没有变化，重点看 ⑧，增加了主题层对象。</p>
<ul>
<li>panel_background=element_rect(fill='white')，图像背景设置为白色。</li>
<li>axis_title_y=element_blank(),，Y 轴的标题设置为空，即不显示。</li>
<li>axis_line_x=element_line(color='black'),，X 轴的直线颜色设置为黑色。</li>
<li>axis_line_y=element_blank(),，Y 轴的直线设置为空，即不显示。</li>
<li>axis_text_y=element_blank(),，Y 轴的标示设置为空，即不显示。</li>
<li>axis_text_x=element_text(color=ccolor),，X 轴的标示颜色设置。</li>
<li>axis_ticks_major_y=element_blank(),，Y 轴主刻线设置为空，即不显示。</li>
<li>panel_grid=element_blank(),，图示的网格设置为空，即不显示。</li>
<li>panel_border=element_blank())，图示的边框设置为空，即不显示。</li>
</ul>
<p>从 ⑧ 的各个参数设置不难看出，每个参数的值都使用了 element_* 的类。</p>
<h3 id="332">3.3.2 化学元素周期表</h3>
<p>Plotnine 中的化学元素周期表，是一个非常经典的案例，可以说搞懂了这个案例，Plotnine 技能就掌握得差不多了。</p>
<p>本例所用化学元素数据下载地址：</p>
<blockquote>
  <p><a href="https://github.com/qiwsir/DataSet/tree/master/elemanets">https://github.com/qiwsir/DataSet/tree/master/elemanets</a></p>
</blockquote>
<p>下图显示的就是本例的最终目标。</p>
<p><img src="https://images.gitbook.cn/1bce4a30-45a7-11e9-aea4-95aeabea01e4" alt="enter image description here" /></p>
<p>根据<a href="https://zh.wikipedia.org/wiki/%E5%85%83%E7%B4%A0%E5%91%A8%E6%9C%9F%E8%A1%A8">维基百科的元素周期表词条</a>可知，元素周期表基本构成如下。</p>
<ul>
<li>族：表中的每一列就是一族，从左向右依次为 1、2……18 族。</li>
<li>周期：表中的行。</li>
<li>元素：每个方框表示一个元素，其中包括元素符号、名称、原子序数、原子量。</li>
<li>在主表下面还有镧系元素和锕系元素表。</li>
<li>用颜色区分金属、非金属等常见的物质状态。</li>
</ul>
<p>本例正是演示如何一步一步绘制这幅图示（元素周期表不仅仅是这一种形状，只不过这是最常见的。<a href="https://www.zhihu.com/question/28828049%EF%BC%89">其他形状的周期表</a>）。</p>
<p>首先，要读入数据集，并对数据做适当处理：</p>
<pre><code class="python language-python">import pandas as pd
import numpy as np
from plotnine import *

elements = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/elemanets/elements.csv")
elements.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FoYUyO8B09m17DxlvfPvqOzX3ONv" alt="avatar" /></p>
<p>5 rows × 21 columns</p>
<p>本例的数据集来源依然要参考本书的数据集仓库。</p>
<pre><code class="python language-python">elements.info()

#out
&lt;class 'pandas.core.frame.DataFrame'&gt;
RangeIndex: 118 entries, 0 to 117
Data columns (total 21 columns):
atomic number               118 non-null int64
symbol                      118 non-null object
name                        118 non-null object
atomic mass                 118 non-null object
CPK                         118 non-null object
electronic configuration    118 non-null object
electronegativity           97 non-null float64
atomic radius               71 non-null float64
ion radius                  92 non-null object
van der Waals radius        38 non-null float64
IE-1                        102 non-null float64
EA                          85 non-null float64
standard state              99 non-null object
bonding type                98 non-null object
melting point               101 non-null float64
boiling point               94 non-null float64
density                     96 non-null float64
metal                       118 non-null object
year discovered             118 non-null object
group                       118 non-null object
period                      118 non-null int64
dtypes: float64(8), int64(2), object(11)
memory usage: 19.4+ KB
</code></pre>
<p>特征 group 就是该元素所在的族，但是，如果用 elements['group'] 查看所有内容，会发现有的记录中用 '-' 标记，说明它不属于任何族，说明它们应该是镧系元素或者锕系元素。根据数据分析的通常要求，'-' 符号最好用数字表示，这里用 ﹣1。</p>
<pre><code class="python language-python">elements['group'] = [-1 if g == '-' else int(g) for g in elements.group]
</code></pre>
<p>这是官方示例中的写法，其实，如果让我来写，我会用 np.where 实现上面的条件判断和赋值。</p>
<p>特征 bonding type、metal 都是分类数据，因此在类型上进行转化。</p>
<pre><code class="python language-python">elements['bonding type'] = elements['bonding type'].astype('category')
elements['metal'] = elements['metal'].astype('category')
</code></pre>
<p>为了显示方便，将原本是整数型的 atomic number 特征，转化为字符串类型。</p>
<pre><code class="python language-python">elements['atomic_number'] = elements['atomic number'].astype(str)
</code></pre>
<p>前面已经说过，元素周期表有两部分，上面的一部分每个元素是属于某一个族的，即 group 特征中的 1-18。而对于值是 ﹣1 的则表示这些元素应该在下面的镧系或者锕系元素表中。下面分别用 top 变量和 bottom 变量引用这两部分元素集合。</p>
<pre><code class="python language-python">top = elements.query('group != -1').copy()
bottom = elements.query('group == -1').copy()
</code></pre>
<p>元素周期表中横向表示的是族（group），纵向表示的是周期（period），用下面的方式在 top 中创建两个特征，分别为“族”和“周期”的值。</p>
<pre><code class="python language-python">top['x'] = top.group
top['y'] = top.period
</code></pre>
<p>除了上面的部分之外，下面的锕系和镧系元素也要做类似的配置。不过，横坐标不能用 group 特征的值，因为前面设置为 ﹣1。</p>
<pre><code class="python language-python">nrows = 2
hshift = 3.5
vshift = 3
bottom['x'] = np.tile(np.arange(len(bottom)//nrows), nrows) + hshift
bottom['y'] = bottom.period + vshift
</code></pre>
<p>hshift 和 vshift 分别表示横、纵间距，这样就为每个锕系和镧系元素增加了横纵坐标值。</p>
<p>每个元素占有一个小矩形，这个小矩形的大小要设置一下。</p>
<pre><code class="python language-python">tile_width = 0.95
tile_height = 0.95
</code></pre>
<p>准备工作已经完成，开始画图。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))                                          #⑨
 + geom_tile(top, aes(width=tile_width, height=tile_height))    #⑩
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c4197b10-45a7-11e9-aea4-95aeabea01e4" width = "80%" /></p>
<p>⑨ 只有美学映射，没有传入数据集，不用担心，因为在下面的图层对象中，要传入不同的数据集。前面已经把元素分为了两类 top 表示主表中的，bottom 表示下面的锕、镧系元素。⑩ 使用 geom_title 绘制安放元素的小矩形图层，并且使用 top 数据集。下面再引入一个图层，绘制 bottom 对应的图层。</p>
<p>但是，Y 轴方向上跟周期表反了，因此再用 scale_y_reverse() 实现坐标轴翻转。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + scale_y_reverse() # new
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e0f728e0-45a7-11e9-913c-5b7dceba72f4" width = "80%" /></p>
<p>基本样式已经有了。</p>
<p>前面已经把特征“metal”的数据转换为分类数据，下面用这些数据对不同元素的小矩形（以后简称“元素块”）上色。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')  # new
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + scale_y_reverse()
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f1fb6430-45a7-11e9-b5ba-8f1c1da573a0" alt="enter image description here" /></p>
<p>接下来的工作比较麻烦，要把化学元素的有关信息写到这些元素块上。在本例中，要将如下信息写到元素块上：</p>
<ul>
<li>原子序数，对应着数据集中的特征是“atomic number”；</li>
<li>元素符号，对应着数据集中的特征是“symbol”；</li>
<li>元素名称，对应着数据集中的特征是“name”；</li>
<li>原子量，对应着数据集中的特征是“automic mass”。</li>
</ul>
<p>上一节中已经介绍过，Plotnine 中用 geom_text 创建文字图层对象，现在我们要绘制 4 个图层，每个图层对应上面的一个特征，并且每个图层的位置、字号大小等都不同。为此，写一个函数来实现此功能。</p>
<pre><code class="python language-python">def inner_text(data):
    layers = [geom_text(data, aes(label='atomic_number'), 
                        nudge_x=-0.40, nudge_y=0.40,
                        ha='left', va='top', fontweight='normal', size=6),
              geom_text(data, aes(label='symbol'), 
                         nudge_y=.1, size=9),
              geom_text(data, aes(label='name'), 
                        nudge_y=-0.125, fontweight='normal', size=4.5),
              geom_text(data, aes(label='atomic mass'), 
                         nudge_y=-.3, fontweight='normal', size=4.5)]
    return layers
</code></pre>
<p>除了用 aes 中的 label 参数确定前述各个特征之外，其他参数都是用于规定文本位置、字号等。</p>
<ul>
<li>nudge_x：文本在水平方向上的相对位置。</li>
<li>nudge_y：文本在竖直方向上的相对位置。</li>
<li>ha：可选 'left'、'center'、'right'，表示水平方向的对齐方式。</li>
<li>va：可选 'top'、'center'、'bottom'，表示竖直方向的对齐方式。</li>
<li>size：字号大小。</li>
<li>fontweight：字族中的字体粗细。</li>
</ul>
<p>将函数 inner_text 应用到绘图流程中：</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)    # new
 + inner_text(bottom) # new
 + scale_y_reverse()
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/543bac90-45a8-11e9-913c-5b7dceba72f4" alt="enter image description here" /></p>
<p>因为有 top 和 bottom 两个数据，所以要调用两次，才能在上下两部分的元素块中叠加上文本图层。</p>
<p>不过，大小还没有调整好。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)
 + inner_text(bottom)
 + scale_y_reverse()
 + coord_equal(expand=False)   # new
 + theme(figure_size=(12, 6))  # new
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/62c8cd60-45a8-11e9-aea4-95aeabea01e4" alt="enter image description here" /></p>
<p>这里又新增了两个图层对象：</p>
<ul>
<li>在默认的主题中，横纵坐标的图上长度相等，也就是图像是呈现在一张正方形的图纸上，coord_equal 的作用就是设置坐标系的横轴和纵轴，它与 coord_fixed 是完全等效的，能够改变图纸的大小和长宽比例。参数 expand 的值是布尔值，如果为 False，则意味着坐标系的大小（即图纸的大小）由制图所用数据决定。</li>
<li>新增的第二个图层对象是一个新的主题，在其中规定了图纸的尺寸。</li>
</ul>
<p>在元素周期表中，Lu 和 Lr 两个元素比较特殊，其实它们不是单独的元素，而是对应着下面两行的，因此要对这两个进行处理，以区分出与其他元素的不同。处理方法就是将它们的元素块“分为两半”，怎么分为两半呢？再做一个图层，覆盖到 Lu 和 Lr 元素块上，不过这个图层仅是原来的元素块的一般，这样看起来就分为两半了。</p>
<pre><code class="python language-python">split_df = pd.DataFrame({
    'x': 3-tile_width/4,
    'y': [6, 7],
    'metal': pd.Categorical(['lanthanoid', 'actinoid'])
})
</code></pre>
<p>split_df 是绘制新元素块所需要的数据集。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(split_df, aes(width=tile_width/2, height=tile_height))  # ⑪
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)
 + inner_text(bottom)
 + scale_y_reverse()
 + coord_equal(expand=False)
 + theme(figure_size=(12, 6))
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/7e1e5490-45a8-11e9-913c-5b7dceba72f4" alt="enter image description here" /></p>
<p>⑪ 就是专门对 Lu 和 Lr 元素块再增加的一个图层，最终显示为将其分为两半。</p>
<p>至此，最基本的已经绘制完工，然后做的就是让它的显示更美观，比如在填充色和主题上变换一下。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(split_df, aes(width=tile_width/2, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)
 + inner_text(bottom)
 + scale_y_reverse()
 + scale_fill_brewer(type='qual', palette=3)         # ⑫
 + coord_equal(expand=False)
 + theme_void()                                      # ⑬
 + theme(figure_size=(12, 6),
         plot_background=element_rect(fill='white')) # ⑭

)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/88859970-45a8-11e9-913c-5b7dceba72f4" alt="enter image description here" /></p>
<p>⑫ 对元素块的填充色进行转换。</p>
<p>⑬ 增加了一个经典的主题图层对象。</p>
<p>⑭ 增加一个主题图层，并且设置了该图层的尺寸和背景色 plot_background=element_rect(fill='white')。</p>
<p>最后要解决的问题是为主表中的元素表上族和周期。</p>
<p>观察主表中每一列——注意我们已经把 Y 轴映射反序了，如果在 H 元素的元素块上面标注族的序号“1”，那么这个“1”的 Y 轴坐标应该是 y=1，同样，在 Sc 元素块上标注族的序号“3”，那么“3”的 Y 轴坐标应该是 y=4。因此，我们就可以创建每列（即：族，编号为 1~18）及其对应的 Y 轴坐标。</p>
<pre><code class="python language-python">groupdf = pd.DataFrame({
    'group': range(1, 19),
    'y': np.repeat([1, 2, 4, 2, 1], [1, 1, 10, 5, 1])})
groupdf
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>group</th>
<th>y</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>1</td>
<td>2</td>
<td>2</td>
</tr>
<tr>
<td>2</td>
<td>3</td>
<td>4</td>
</tr>
<tr>
<td>3</td>
<td>4</td>
<td>4</td>
</tr>
<tr>
<td>4</td>
<td>5</td>
<td>4</td>
</tr>
<tr>
<td>5</td>
<td>6</td>
<td>4</td>
</tr>
<tr>
<td>6</td>
<td>7</td>
<td>4</td>
</tr>
<tr>
<td>7</td>
<td>8</td>
<td>4</td>
</tr>
<tr>
<td>8</td>
<td>9</td>
<td>4</td>
</tr>
<tr>
<td>9</td>
<td>10</td>
<td>4</td>
</tr>
<tr>
<td>10</td>
<td>11</td>
<td>4</td>
</tr>
<tr>
<td>11</td>
<td>12</td>
<td>4</td>
</tr>
<tr>
<td>12</td>
<td>13</td>
<td>2</td>
</tr>
<tr>
<td>13</td>
<td>14</td>
<td>2</td>
</tr>
<tr>
<td>14</td>
<td>15</td>
<td>2</td>
</tr>
<tr>
<td>15</td>
<td>16</td>
<td>2</td>
</tr>
<tr>
<td>16</td>
<td>17</td>
<td>2</td>
</tr>
<tr>
<td>17</td>
<td>18</td>
<td>1</td>
</tr>
</tbody>
</table>
<p>当然，标注族的序号，也是一个文本图层，还要使用 geom_text。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))    # ⑯
 + aes(fill='metal')      # ⑰
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(split_df, aes(width=tile_width/2, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)
 + inner_text(bottom)
 + geom_text(groupdf, aes('group', 'y', label='group'), 
             color='gray', nudge_y=.525, va='bottom',
             fontweight='normal', size=9, inherit_aes=False)    # ⑮
 + scale_y_reverse()                    
 + scale_fill_brewer(type='qual', palette=3)
 + coord_equal(expand=False)
 + theme_void()
 + theme(figure_size=(12, 6),
         plot_background=element_rect(fill='white'),)
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/aa1a1890-45a8-11e9-913c-5b7dceba72f4" alt="enter image description here" /></p>
<p>⑮ 即为标注每一列族序号的文本图层。此处的众多参数，有一项需要特别关注，inherit_aes=False，前面曾经提过，如果在各项几何对象之前设置了美学映射和数据，那么，在没有特别重写之前，后续的几何对象中会继承这些设置。在本程序中，前面已经在 ⑯ 和 ⑰ 初已经有了美学映射，在 ⑮ 的 geom_text 中，aes('group', 'y', label='group') 重写了 ⑯ 中对 X 轴和 Y 轴的映射，但是 ⑰ 的映射，在这里没有重写。但是，此处不想继承这个映射配置，于是乎就使用参数 inherit_aes=False 实现这个目的。</p>
<p><strong>元素的族标注完毕，接下来标注周期。</strong></p>
<p>因为周期是对每一行的标注，一共 7 行。因为标注在左侧，可以把它看做是左侧的 Y 轴标示，那么，就可以在图层上通过对 Y 轴标示的设置完成周期的标注。</p>
<pre><code class="python language-python">(ggplot(aes('x', 'y'))
 + aes(fill='metal')
 + geom_tile(top, aes(width=tile_width, height=tile_height))
 + geom_tile(split_df, aes(width=tile_width/2, height=tile_height))
 + geom_tile(bottom, aes(width=tile_width, height=tile_height))
 + inner_text(top)
 + inner_text(bottom)
 + geom_text(groupdf, aes('group', 'y', label='group'), color='gray', nudge_y=.525,
             va='bottom',fontweight='normal', size=9, inherit_aes=False)    
 + scale_y_reverse(breaks=range(1, 8), limits=(0, 10.5))                    # ⑱
 + scale_fill_brewer(type='qual', palette=3)
 + coord_equal(expand=False)
 + theme_void()
 + theme(figure_size=(12, 6),
         plot_background=element_rect(fill='white'),
         axis_text_y=element_text(margin={'r': 5}, color='gray', size=9)    # ⑲
         )
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c080a770-45a8-11e9-81d0-97204205141b" alt="enter image description here" /></p>
<p>⑱ 和 ⑲ 是在原来语句上修改的。</p>
<ul>
<li>⑱ 增加了纵坐标主刻度标示数字。</li>
<li>⑲ 增加了参数 axis_text_y，对 Y 轴标示的显示格式进行了设置。</li>
</ul>
<p>至此，一张元素周期表绘制完毕。</p>
<p>请再次重复上述流程，以便有所感悟。</p>
<h3 id="333">3.3.3 小结</h3>
<p>本课研习了 Plotnine 官方提供的两个案例，目的在于通过剖析案例，深刻理解 Plotnine 的多种应用技能。如果有时间，请学习者耐心地把其他的案例也研读一番，虽然官方网站上解释很好，不妨仿照本课所述的方式，解剖每个示例，从而管窥 Plotnine 的妙处。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>