---
title: 案例上手 Python 数据可视化-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从上一课的初步体验中，我们已经获悉，只要加载了数据，并创建了“美学映射”之后，也就有了绘图的基础，然后要思考的就是：做什么形状的图，是散点图，还是箱线图？这些图就是所谓的“几何对象”，每个几何对象都是一个图层——也可以看做一个对象。正是基于这个认识，p9.geom_* 等这些几何对象才都是类，每个图层也就是某个类的实例。</p>
<h3 id="321">3.2.1 几何对象</h3>
<p>原来曾经写过的：</p>
<pre><code class="python language-python">(p9.ggplot(mg)    
 + p9.aes(x='displ', y='hwy', color='factor(cyl)')    
 + p9.geom_point()
)
</code></pre>
<p>还可以用下面的方式写：</p>
<pre><code class="python language-python">%matplotlib inline
import plotnine as p9
from plotnine import data

base_plot = p9.ggplot(data.mpg, p9.aes(x='displ', y='hwy', color='factor(cyl)'))    #①
base_plot + p9.geom_point()    #②
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6a8c3320-453f-11e9-9b40-8d81bb51beff" width = "70%" /></p>
<p>① 的 p9.ggplot 返回的是一个图层对象，其中包含了数据和美学映射关系，而后这个对象与一个几何对象（图层）相加（② 所示），就相当于图层叠加，最终得到了上述结果。</p>
<p>我曾在 Python 基础课程中很明确地讨论过“+”的运算（参见《跟老齐学 Python：轻松入门》），能够参与“+”运算的，都是 Python 中的对象——内置对象（如整数、浮点数、字符串、列表等）或者自定义的对象——注意都是对象，或者说只有对象才能参与此运算。② 实现增加图层，因为图层是对象，也就意味着最终的图示就是多个图层对象相加。</p>
<p>既然如此，那么每个图层对象都有自己的属性，通过对本图层的设置，会让可视化控制更灵活。</p>
<pre><code class="python language-python">(p9.ggplot(data.mpg)    
 + p9.aes(x='displ', y='hwy')    #③
 + p9.geom_point(p9.aes(color='factor(cyl)'))    #④
 + p9.geom_smooth()
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/667212d0-4546-11e9-955a-05e47ab35196" width = "70%" /></p>
<p>如果与上一节的类似图示进行比较，那条代表回归规律的曲线有了变化，现在没有再被颜色分为若干部分了，而是统一的一条线（下图是上一节得到的图示）。</p>
<p><img src="https://images.gitbook.cn/75035250-4546-11e9-955a-05e47ab35196" width = "70%" /></p>
<p>之所以有这样的变化，是因为 ③ 创建美学映射图层——这个图层被后续图层使用——没有了 color='factor(cyl)'，而是将这种映射移到了 ④，也就是专门对 ④ 创建的图层对象配置了 p9.aes(color='factor(cyl)')，其他层就没有这种映射关系了。</p>
<p>以下是 geom_point 的参数：</p>
<pre><code class="python language-python">geom_point(mapping=None, data=None, stat='identity', position='identity',
           na_rm=False, inherit_aes=True, show_legend=None, **kwargs)
</code></pre>
<p>其他的类都与此差不多。从这里可以看出，每个图层对象，都可以为该层设置数据、映射关系等属性，如果该图层对象的属性与 p9.ggplot 中设置的重名，则不再调用 p9.ggplot 中的值。</p>
<h3 id="322">3.2.2 美学映射</h3>
<p>虽然前面已经多少了解了“美学映射”—— 其实就是 “映射”，加上 “美学”，更显得是一个独特的专有名词 —— 但是对它的领悟，恐怕还要继续。</p>
<pre><code class="python language-python">(p9.ggplot(data.mpg)    
 + p9.aes(x='displ', y='hwy')    
 + p9.geom_point(p9.aes(color='factor(cyl)',size='hwy'))
 + p9.geom_smooth(color='red')
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e9194c40-4545-11e9-9142-110b45dd2fac" width = "70%" /></p>
<p>观察图示结果，丰富了各个图层的属性。凝视此图，对 “美学映射” 会有所悟，即将数据集中的某个特征与可视化的图示中某个图像元素（图对象属性）建立映射关系，将该特征的数据用可视化的美学方式表示出来。比如，在上述例子中：</p>
<ul>
<li>将数据集中的 “displ” 特征与坐标系的 X 轴建立映射关系，即用 X 轴的点表示此特征中的数据；</li>
<li>将数据集中的 “hwy” 特征与图示中点的直径尺寸建立映射关系，即用不同大小的点表示此特征的数据——此特征数据是分类数据。</li>
</ul>
<p>并且，每个图层对象中都可以创建各自的映射，如果本图层没有特别给 mapping 参数赋值，将继承 p9.ggplot 所创建的映射关系。</p>
<pre><code class="python language-python">(p9.ggplot(data.mpg)    
 + p9.aes(x='displ', y='hwy')    
 + p9.geom_point(p9.aes(color='factor(cyl)',size='hwy'))
 + p9.geom_smooth(color='red')
 + p9.xlab("engine displacement(L)")    #⑤
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d8dca6b0-4545-11e9-9b40-8d81bb51beff" width = "70%" /></p>
<p>这次增加的图层对象是 ⑤，它的作用就是设置坐标轴的注释。</p>
<p>其他的几何对象类，<a href="https://plotnine.readthedocs.io/en/stable/api.html#geoms">可点击这里参考官方网站提供的 API 说明</a>。</p>
<p>前面曾经提到了对“美学映射”的理解，即 plotnine.aes 类所创建的对象。</p>
<p>但是，在实际的制图业务中，除了需要将数据集的特征与图中的元素建立映射关系之外，还可能需要对数据进行某种变换。比如将某个特征的数据进行对数转换之后，再映射到 Y 轴。实现这种操作的最基本方法是使用 Pandas 等工具，为数据集增加一个特征保存转换之后的数据——这是数据清洗应完成的工作。如果使用 Plotnine，会发现它部分地解决这个问题（有的变换能够自动完成，有的还是需要通过数据清洗解决），无需提前运算，只需要使用 Plotnine 中提供的名为“标度”（Scale）的类（官方文档<a href="https://plotnine.readthedocs.io/en/stable/api.html#scales%EF%BC%89%E3%80%82">请点击这里</a>）。</p>
<pre><code class="python language-python">(p9.ggplot(data.mpg)    
 + p9.aes(x='displ', y='hwy')    
 + p9.geom_point(p9.aes(color='factor(cyl)',size='hwy'))
 + p9.geom_smooth(color='red')
 + p9.xlab("engine displacement(L)")
 + p9.scale_x_reverse()    #⑥
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/13a8f290-4545-11e9-9b40-8d81bb51beff" width = "70%" /></p>
<p>此图与前述不同之原因就是 ⑥，将映射到 X 轴的数据进行了转换——翻转。其实，依然可以把 ⑥ 看做一个图层，这个新的图层覆盖了原来的 X 轴的设置。</p>
<p>另外，在 Plotnine 中，还有 Coordinate（坐标系）和 Facet（位面、组图、分面），秉承着前面的方法，对它们的应用并不难，可以依据官方文档使用。在这里对这部分内容从略，在后续的示例中，会将它们的应用融汇其中。</p>
<h3 id="323">3.2.3 解析一个示例</h3>
<p>下面解析一个官方网站的示例（<a href="https://plotnine.readthedocs.io/en/stable/generated/plotnine.scales.scale_x_continuous.html#guitar-neck">官方示例地址</a>，本课程将此示例做了适当简化），通过这个解析过程，不仅进一步理解 Plotnine 的制图基本思想，顺便还了解一些前面没有介绍过的内容。</p>
<p>先创建数据集 c_chord 和 markings。</p>
<pre><code class="python language-python">import pandas as pd
c_chord = pd.DataFrame({
    'Fret':   [0, 2.5, 1.5, 0, 0.5, 0],
    'String': [1, 2, 3, 4, 5, 6]
})

c_chord['Sequence'] = list(range(1, 1+len(c_chord['Fret'])))
c_chord
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>Fret</th>
<th>String</th>
<th>Sequence</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>0.0</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>1</td>
<td>2.5</td>
<td>2</td>
<td>2</td>
</tr>
<tr>
<td>2</td>
<td>1.5</td>
<td>3</td>
<td>3</td>
</tr>
<tr>
<td>3</td>
<td>0.0</td>
<td>4</td>
<td>4</td>
</tr>
<tr>
<td>4</td>
<td>0.5</td>
<td>5</td>
<td>5</td>
</tr>
<tr>
<td>5</td>
<td>0.0</td>
<td>6</td>
<td>6</td>
</tr>
</tbody>
</table>
<pre><code class="python language-python">markings = pd.DataFrame({
    'Fret':   [2.5, 4.5, 6.5, 8.5, 11.5, 11.5, 14.5, 16.5, 18.5, 20.5],
    'String': [3.5, 3.5, 3.5, 3.5, 2, 5, 3.5, 3.5, 3.5, 3.5]
})
markings
</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>Fret</th>
<th>String</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>2.5</td>
<td>3.5</td>
</tr>
<tr>
<td>1</td>
<td>4.5</td>
<td>3.5</td>
</tr>
<tr>
<td>2</td>
<td>6.5</td>
<td>3.5</td>
</tr>
<tr>
<td>3</td>
<td>8.5</td>
<td>3.5</td>
</tr>
<tr>
<td>4</td>
<td>11.5</td>
<td>2.0</td>
</tr>
<tr>
<td>5</td>
<td>11.5</td>
<td>5.0</td>
</tr>
<tr>
<td>6</td>
<td>14.5</td>
<td>3.5</td>
</tr>
<tr>
<td>7</td>
<td>16.5</td>
<td>3.5</td>
</tr>
<tr>
<td>8</td>
<td>18.5</td>
<td>3.5</td>
</tr>
<tr>
<td>9</td>
<td>20.5</td>
<td>3.5</td>
</tr>
</tbody>
</table>
<p>还是按照以前的思路，加载数据集，并创建映射关系。</p>
<pre><code class="python language-python">(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d87500b0-4544-11e9-b363-c7a998ed42df" width = "70%" /></p>
<p>这个结果不足为奇，但是距离官方示例所要的图相差太远，根源在于目前采用的是默认的主题。在 Plotnine 中，有专门定义主题的类 p9.theme，更多相关内容请参阅：</p>
<blockquote>
  <p><a href="https://plotnine.readthedocs.io/en/stable/api.html#themes">https://plotnine.readthedocs.io/en/stable/api.html#themes</a></p>
</blockquote>
<p>于是乎，就自定义一个主题。</p>
<pre><code class="python language-python">neck_color = '#FFDDCC'
fret_color = '#998888'
string_color = '#AA9944'

neck_theme = p9.theme(
    figure_size = (10, 2),    #⑦
    panel_background = p9.element_rect(fill=neck_color),    #⑧
    panel_grid_major_y = p9.element_line(color=string_color, size=2.2),    #⑨
    panel_grid_major_x = p9.element_line(color=fret_color, size=2.2),
    panel_grid_minor_x = p9.element_line(color=fret_color, size=1)
)

(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
  + neck_theme    #⑩
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b4a844d0-4544-11e9-9b40-8d81bb51beff" alt="enter image description here" /></p>
<p>nect_theme 是自定义的主题。在自定义主题中，通常要规定图的大小、背景、网格线的粗细和颜色，以及文本的字号和颜色等。p9.theme 的各个参数，就是从上述角度定义了一个新的主题。</p>
<ul>
<li>⑦ 定义了图的大小。</li>
<li>⑧ 定义了图的颜色。这里使用了 p9.element_rect 类。因为所有图都是矩形的，可以通过此类对矩形的背景颜色（fill=neck_color）进行设置。</li>
<li>⑨ 定义了 Y 轴主刻度网格线。使用了 p9.element_line，其中 color=string_color 定义了颜色，size=2.2 定义了粗细。同样，下面也定义了 X 轴主刻度网格线和副刻度网格线。对于 Y 轴副刻度网格线没有定义，则用默认值。</li>
</ul>
<p>新的主题定义好之后，把它当做一个对象（图层），即 ⑩，于是得到了上图显示结果。</p>
<p>然后根据 p9.ggplot(c_chord, p9.aes('Fret', 'String')) 的设置，绘制散点图。</p>
<pre><code class="python language-python">neck_color = '#FFDDCC'
fret_color = '#998888'
string_color = '#AA9944'

neck_theme = p9.theme(
    figure_size=(10, 2),
    panel_background=p9.element_rect(fill=neck_color),
    panel_grid_major_y=p9.element_line(color=string_color, size=2.2),
    panel_grid_major_x=p9.element_line(color=fret_color, size=2.2),
    panel_grid_minor_x=p9.element_line(color=fret_color, size=1)
)

(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
 + neck_theme
 + p9.geom_point(p9.aes(color='Sequence'), fill='#FFFFFF', size=3)    #⑪
 + p9.geom_path(p9.aes(color='Sequence'), size=3)    #⑫
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/bec9a710-4544-11e9-b363-c7a998ed42df" alt="enter image description here" /></p>
<p>⑪ 绘制的就是散点图；⑫ 中的 p9.geom_path 的作用则是将各个散点图用折线连接起来。</p>
<p>还是在这张图上，再绘制数据集 markings 的散点图，那就是增加一个图层，并且在该图层中声明这个数据集。</p>
<pre><code class="python language-python">neck_color = '#FFDDCC'
fret_color = '#998888'
string_color = '#AA9944'

neck_theme = p9.theme(
    figure_size=(10, 2),
    panel_background=p9.element_rect(fill=neck_color),
    panel_grid_major_y=p9.element_line(color=string_color, size=2.2),
    panel_grid_major_x=p9.element_line(color=fret_color, size=2.2),
    panel_grid_minor_x=p9.element_line(color=fret_color, size=1)
)

(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
 + neck_theme
 + p9.geom_point(p9.aes(color='Sequence'), fill='#FFFFFF', size=3)
 + p9.geom_path(p9.aes(color='Sequence'), size=3)
 + p9.geom_point(data=markings, fill='#000000', size=4)    #⑬
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9b2ffe90-4543-11e9-955a-05e47ab35196" alt="enter image description here" /></p>
<p>⑬ 的效果就是增加了另外一个数据集的散点图。注意对比本图和上面的图，横坐标的范围已经变化了，这是因为 markings 数据集中“Fret”特征中的数据与 c_chord 中同名特征的数据分布不同。因为两个数据集中有两个同名特征，并且它们都是要映射到 X 轴和 Y 轴，⑬ 就无需再次设置美学映射，而是采用前面设置的即可。</p>
<p>如果观察两个数据集，它们的不同之处还表现在“String”特征的数据。为了更准确地显示，需要将图中的 Y 轴主刻度重新设置。</p>
<pre><code class="python language-python">neck_color = '#FFDDCC'
fret_color = '#998888'
string_color = '#AA9944'

neck_theme = p9.theme(
    figure_size=(10, 2),
    panel_background=p9.element_rect(fill=neck_color),
    panel_grid_major_y=p9.element_line(color=string_color, size=2.2),
    panel_grid_major_x=p9.element_line(color=fret_color, size=2.2),
    panel_grid_minor_x=p9.element_line(color=fret_color, size=1)
)

(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
 + neck_theme
 + p9.geom_point(p9.aes(color='Sequence'), fill='#FFFFFF', size=3)
 + p9.geom_path(p9.aes(color='Sequence'), size=3)
 + p9.geom_point(data=markings, fill='#000000', size=4)   
 + p9.scale_y_continuous(breaks=range(0, 7), minor_breaks=[])    #⑭
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/8d6bd310-4543-11e9-9b40-8d81bb51beff" alt="enter image description here" /></p>
<p>注意观察 Y 轴的变化。</p>
<p>p9.scale_y_continuous 的详细内容请阅读<a href="https://plotnine.readthedocs.io/en/stable/generated/plotnine.scales.scale_y_continuous.html#plotnine.scales.scale_y_continuous">官方文档</a>，⑭ 中使用的参数 breaks=range(0, 7)，表示设置主刻度的位置；minor_breaks=[] 表示副刻度的位置，但是这里是空列表，意思就是不显示副刻度。</p>
<pre><code class="python language-python">neck_color = '#FFDDCC'
fret_color = '#998888'
string_color = '#AA9944'

neck_theme = p9.theme(
    figure_size=(10, 2),
    panel_background=p9.element_rect(fill=neck_color),
    panel_grid_major_y=p9.element_line(color=string_color, size=2.2),
    panel_grid_major_x=p9.element_line(color=fret_color, size=2.2),
    panel_grid_minor_x=p9.element_line(color=fret_color, size=1)
)

(p9.ggplot(c_chord, p9.aes('Fret', 'String'))
 + neck_theme
 + p9.geom_point(p9.aes(color='Sequence'), fill='#FFFFFF', size=3)
 + p9.geom_path(p9.aes(color='Sequence'), size=3)
 + p9.geom_point(data=markings, fill='#000000', size=4)   
 + p9.scale_y_continuous(breaks=range(0, 7), minor_breaks=[])    
 + p9.guides(color=False)    #⑮
)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/47254120-4543-11e9-9142-110b45dd2fac" alt="enter image description here" /></p>
<p>很明显，⑮ 的作用就是去掉了右边的数据光谱。</p>
<p>至此，所绘制的图已经跟官方示例的相差无几——差别在于 X 轴。这个工作交给读者，通过阅读官方文档中的代码，看是否能够理解其对横轴的处理。</p>
<h3 id="324">3.2.4 小结</h3>
<p>本课进一步理解了 Plotnine 中的几何对象和美学映射的含义，并且通过一个示例，扩展了知识技能。Plotnine 提供了很多灵活多样的 API，在具体业务中，可以根据需要查阅相应的 API。当然，为了能够实现此操作，需要开发者在学习阶段多练习，通过练习熟悉 API 的应用。</p>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>