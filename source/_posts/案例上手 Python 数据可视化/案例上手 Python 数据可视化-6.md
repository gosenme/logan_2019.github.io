---
title: 案例上手 Python 数据可视化-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在数据可视化中，坐标系是最基本的。在一张图纸上，只要建立了坐标系，图中的任何一个点就可以用数学方式描述清楚了。</p>
<p>一般，小学学习了数轴，初中就开始学习了二维直角坐标系。但是，那仅仅是数学中的认识，现在要使用 Matplotlib 与已有的数学知识结合，对坐标系有新的认识。</p>
<p>要很耐心地阅读以下内容，即便是“温故”，目的还是“知新”。</p>
<p>通常所说的坐标系，也称为平面直角坐标系、正交坐标系、笛卡尔坐标系，英文：Cartesian coordinate system，形状如下图所示。</p>
<p><img src="https://images.gitbook.cn/9e3f40a0-334b-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>这种样式的坐标系，最早是由法国数学家勒内·笛卡尔（René Descartes）于 1637 年提出来的。它的组成部分包括以下几点。</p>
<ul>
<li><p>x 轴（x-axis）：水平的坐标轴，也称为“横轴”。这是条有方向的直线，箭头所指方向表示“正方向”，与之相反的为“负方向”。</p></li>
<li><p>y 轴（y-axis）：竖直的坐标轴，也称为“纵轴”。除了方向与 x 轴垂直之外，别的没有不同。</p></li>
<li><p>正方向：不论是 x 轴还是 y 轴，都是以箭头所指的方向为正方向。上图中所标示的正方向，是数学中的习惯。但是，在真实的问题中，可能会有变化。比如，在物理学中，会以物体的运动方向或者某个力的方向为其中一个坐标轴的正方向；在计算机图形中，还会以向下为 y 轴的正方向。</p></li>
<li><p>原点（origin）：x、y 轴的交点。通常用字母 O 标记，一般情况下，原点是数字 0。但在实际问题中，原点不一定都是从 0 开始的，有可能对于不同的坐标轴，值还不一样。</p></li>
<li><p>刻度：观察上面的图，坐标轴上有刻度，每个刻度，应该包含以下两部分。</p>
<ul>
<li>刻线：在坐标轴上的短线。</li>
<li>标示：刻线旁边的数字，表示该刻线的数量。但是，不是所有的刻线都必须有标示。上图中就显示出来了，每隔 5 个单位有一个标示。为了区分，还可以把这些有标示的刻线称为“主刻线”（此时的刻线和标示合称为“主刻度”），没有标示的刻线则称为“副刻线”。</li></ul></li>
<li><p>坐标：以 (x, y) 的方式表示坐标系中的一个点。例如，上图中点 P，坐标为 (3, 5)，即该点在 x 轴的投影点对应着 3，在 y 轴上的投影点对应着 5。</p></li>
</ul>
<p>对通常的坐标系有了认识之后，接下来，就是研习一番 Matplotlib 如何操控坐标系了。</p>
<h3 id="121">1.2.1 设置坐标网格</h3>
<p>坐标网格，是坐标系的辅助设备，主要是为了帮助人更直观地观察。</p>
<p><strong>注意</strong>：以下代码是在 Jupyter 中执行，没有在最后使用 plt.show()。如果使用其他编辑器，最终以程序方式执行，请读者自行增加此句。</p>
<pre><code class="python language-python">%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.02)
y = np.exp(-x) * np.cos(2*np.pi*x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.grid(color='blue')    # ①
</code></pre>
<p>运行结果：</p>
<p><img src="https://images.gitbook.cn/fb9b97c0-334c-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>在上述代码中，ax 引用了坐标系对象，它具有一个名为 grid 的方法，使用这个方法能够实现对坐标网格的设置。它的完整格式是：</p>
<pre><code class="python language-python">ax.grid(b=None, which='major', axis='both', **kwargs)
</code></pre>
<p>各个参数说明如下。</p>
<ul>
<li><p>b：布尔值或者 None，默认是 None。</p>
<ul>
<li>如果 b = True，则意味着显示坐标网格；如果 b = False，则意味着不显示。但是，如果将 ① 修改为 ax.grid(b = False, color='blue')，并不会让网格消失。之所以如此，是因为在代码示例中有一个很重要的参数 color = 'blue'，该参数被 kwargs 收集。也就是说，如果 kwargs 参数收集到了值，那么，b 这个参数对网格的控制将失效。</li>
<li>如果 b = None，并且 kwargs 参数也没有值，即 ax.grid()，Matplotlib 会默认显示坐标网格，并且以默认方式显示。</li></ul></li>
<li><p>which：默认值为 'major'。可选值为三个字符串：'major'、'minor'、'both'，指明要显示哪一个刻线的坐标网格。</p>
<ul>
<li>'major'：表示显示主刻线的坐标网格。</li>
<li>'minor'：表示显示副刻线的坐标网格。当然，对于上面的示例而言，只有主刻线。</li>
<li>'both'：以上都显示。</li></ul></li>
<li><p>axis：默认值为 'both'，可选值为三个字符串：'both'、'x'、'y'，规定显示哪个坐标轴上的网格。例如，将 ① 修改为：ax.grid(axis='x', color='blue')，则会显示下图效果。</p></li>
</ul>
<p><img src="https://images.gitbook.cn/a6c70530-334d-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<ul>
<li>**kwargs：这个是用来收集其他参数的。对于网格的设置，除了上面的三个，还有很多，比如线的色彩、宽度、样式等，都是用这个参数来收集的。因为太多，所以不能一一介绍，这里仅列举几个常用的。</li>
</ul>
<p>（1）color：设置颜色。在 Matplotlib 中，颜色可以用十六进制表示颜色，但实际上，数据可视化也不是美术作品，因此通常就几种色彩足够了。对于常用的几种色彩，可以使用相应单词拼写，也可以使用符号代替。如下表所示：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">颜色单词</th>
<th style="text-align:center;">符号</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">blue</td>
<td style="text-align:center;">b</td>
</tr>
<tr>
<td style="text-align:center;">green</td>
<td style="text-align:center;">g</td>
</tr>
<tr>
<td style="text-align:center;">red</td>
<td style="text-align:center;">r</td>
</tr>
<tr>
<td style="text-align:center;">cyan</td>
<td style="text-align:center;">c</td>
</tr>
<tr>
<td style="text-align:center;">magenta</td>
<td style="text-align:center;">m</td>
</tr>
<tr>
<td style="text-align:center;">yellow</td>
<td style="text-align:center;">y</td>
</tr>
<tr>
<td style="text-align:center;">black</td>
<td style="text-align:center;">b</td>
</tr>
<tr>
<td style="text-align:center;">white</td>
<td style="text-align:center;">w</td>
</tr>
</tbody>
</table>
<p>感觉上面的色彩不够用，比如体检中检验辨别色彩能力的图，还可以参阅：<a href="https://matplotlib.org/2.1.1/gallery/color/named_colors.html#visualizing-named-colors">Visualizing named colors</a>。</p>
<p>此处有一个重要提示，本达人课的宗旨是介绍数据可视化工具的基本应用方法，而非某个工具的文档翻译，因此，不会事无巨细地讲解。但是，为了便于读者学习，会在行文中提供一些参考资料，这些资料能够帮助读者对某个内容深化。如果有兴趣，可以深入阅读；也可以仅仅是浏览，先留有印象，待以后在项目中用到时晓得查阅。</p>
<p>（2）linestyle：设置线型，默认是实线。下表中是常用的线型。</p>
<table>
<thead>
<tr>
<th>可选值</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>-</td>
<td>实线</td>
</tr>
<tr>
<td>--</td>
<td>虚线</td>
</tr>
<tr>
<td>-.</td>
<td>点划线</td>
</tr>
<tr>
<td>:</td>
<td>点线</td>
</tr>
</tbody>
</table>
<p>例如，将网格的线型设置为虚线，ax.grid(axis='x', color='blue', linestyle="-.")，其效果如下图：</p>
<p><img src="https://images.gitbook.cn/5f8247b0-334e-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>（3）linewidth：从字面含义就能理解，该参数是规定线的粗细。例如，ax.grid(axis='x', color='blue', linestyle="-.", linewidth=8)，结果如下图所示：</p>
<p><img src="https://images.gitbook.cn/817d77e0-334e-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>对于 **kwargs 所能够收集的参数还很多，以上仅仅列举三个常用的。更多的参数，可以通过帮助文档阅读，即 ax.grid?。</p>
<p>继续提示读者，字里行间隐藏的学习方法很重要，比如此处提示<strong>要善于使用帮助文档，这可能会决定你的编程水平上限</strong>。在后续的内容中，这种提示还会经常出现，请读者特别注意体会，并按照要求操作。</p>
<h3 id="122">1.2.2 坐标轴的数值范围</h3>
<p>在数学上，坐标轴是没有范围的，但是在图示中显示，它必须有长度范围，即坐标轴上刻度的标示最大值和最小值。</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim((-2, 10))
</code></pre>
<p>输出结果：(-2, 10)</p>
<p><img src="https://images.gitbook.cn/28a81d90-334f-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>从美观角度来看，这个图的留白就太多了，之所以如此，就是因为在代码中使用 ax.set_xlim((-2, 10)) 修改了 x 轴的数值范围。如果要修改 y 轴的数值范围，可以使用类似的方法 ax.set_ylim()。</p>
<p>在上面的程序中，以元组 (-2, 10) 作为向 ax.set_xlim() 传入的参数，其含义是坐标轴上的刻度标示的最小值是 ﹣2，最大值是 10。同样的效果，也可以这样实现：ax.set_xlim(left=-2, right=10)。这里的 left 和 right 分别对应了坐标轴中显示的左右两端的值。如果这样提供参数，可以将其中某个设置为 None，那时就会按照默认情况处理。</p>
<p>但是，有一个问题请注意：通常 left 的值小于 right 的值，这意味着坐标轴方向是向右的。如果反过来，可以吗？</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(left=10, right=-2)    # 注意看这里的参数大小关系
</code></pre>
<p>输出结果：(10, -2)</p>
<p><img src="https://images.gitbook.cn/920dc640-334f-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>注意观察输出结果，当 left 的值大于 right 的值之后，其效果是相当于把 x 轴的方向调转了。</p>
<p>然而，上面两个图都有一个小瑕疵——观察要仔细哦，那就是代码中设置的“﹣2”，在图示中并没有显示出来，在应该显示“﹣2”的位置，显示的却是“2”，少了负号。</p>
<pre><code class="python language-python">import matplotlib    # 引入魔窟
matplotlib.rcParams['axes.unicode_minus'] = False    # 设置显示负号

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim((-2, 10))
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/753c1120-34d5-11e9-844c-bf355aeb03f4" alt="enter image description here" /></p>
<p>再次仔细地观察输出的图示，横轴和纵轴的负数显示问题都解决了。此次的示例只是解决方法之一，如果在网上搜索，还能找到其他解决方法。</p>
<p>仅仅设置了坐标轴的数值范围，而刻度还是按照默认情况分布的，总感觉上面函数图像中的刻度“精确度”有点低。比如还是将 x 轴的数值范围设置为 0 ~ 5，但是，最好能够以 0.5 为单位显示主刻线。这个如何实现？</p>
<p>看下面代码：</p>
<pre><code>fig, ax = plt.subplots()
ax.plot(x, y)

ax.set_xlim(left=0, right=5)
ax.set_ylim((-1, 1))

ax.set_xticks(np.linspace(0, 5, 11))
ax.set_yticks([-1, -0.4, -0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 1])
</code></pre>
<p>输出图像：</p>
<p><img src="https://images.gitbook.cn/524d5c80-3351-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>刻度的设置使用 ax.set_xticks() 来实现，不仅能够实现均匀分布的设置，如上图的 x 轴，还能实现非均匀分布设置，如上图的 y 轴。</p>
<p>Python 中的变量和函数等的命名通常都遵循着“望文生义”的原则，比如 set_xticks，字面含义就是“设置 x 轴的小棍子”。坐标轴上的那些刻度，可不就是“小棍子”吗？因此，学几个单词，还是大有裨益的。</p>
<h3 id="123">1.2.3 标记坐标轴</h3>
<p>在坐标轴附近显示一些文字，用以说明该坐标轴所表示的含义，这在通常的数据可视化中都是必不可少的。实现此操作可以使用 ax.set_xlabel() 和 ax.set_ylabel() 实现。</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(left=10, right=-2)
ax.set_xlabel("axis x")
ax.set_ylabel("axis y")
</code></pre>
<p>输出结果：Text(0, 0.5, 'axis y')</p>
<p><img src="https://images.gitbook.cn/c8e7e900-3351-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>看到上面的结果，在感到满意之余，可能还会有其他要求，比如字号能不能大点？</p>
<p>当然可以。</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(left=10, right=-2)
ax.set_xlabel("x轴", fontsize=20, color='red')    # 设置字号和字的颜色
ax.set_ylabel("y轴", fontsize='xx-large')    # 除了可以使用数字，还可使用这种方式
ax.set_title('The function', fontdict={'fontsize': 22, 'fontweight': 'medium'})
</code></pre>
<p>输出结果：Text(0, 0.5, 'y轴')</p>
<p><img src="https://images.gitbook.cn/e02a0ad0-3351-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>其实，对于这些文本的设计，不仅仅包含字号的大小，还包含其他内容，如字体、颜色等。从哪里可以知道这些文本的设置呢？请看官方文档的说明，<a href="https://matplotlib.org/api/text_api.html#matplotlib.text.Text">点击这里查看</a>，又出现推荐阅读资料，请按照前文提示方法处理。</p>
<p>在上面的代码中，还多了一句 ax.set_title('The function', fontdict={'fontsize': 22, 'fontweight': 'medium'})，它的作用是设置了坐标系上面的标题（看上图效果），并且使用了一个名为 fontdict 的参数，以字典的方式约定了文字的属性值。</p>
<p>以上还都比较简单，稍微复杂的是对刻度的操作。</p>
<h3 id="124">1.2.4 设置刻度</h3>
<p>前面已经明确说明，刻度包括刻线和标示两部分。在 Matplotlib 中，分别用这样两个单词对应：</p>
<ul>
<li>刻线，locator</li>
<li>标示，formatter</li>
</ul>
<p>在 Matplotlib 中，除了可以使用 ax.set_xticks() 对刻度的分布进行设置之外，还能够分别操作刻线和标示。</p>
<pre><code class="python language-python">fig, ax = plt.subplots()
ax.plot(x, y)
ax.yaxis.set_major_locator(plt.NullLocator())    # ②
ax.xaxis.set_major_formatter(plt.NullFormatter())    # ③
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1d422600-3352-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>仔细观察输出结果，纵轴上“刻线”和“标示”都没有了，横轴上只有“刻线”，没有“标示”。产生这种结果，就是因为在上面的代码中的 ②（ax.yaxis.set_major_locator(plt.NullLocator())）和③（ax.xaxis.set_major_formatter( plt.NullFormatter())）。下面对这两行中所涉及的内容进行详细解释。</p>
<ul>
<li>NullLocator：秉承着“望文生义”的原则，这是很重要的命名原则，估计已经猜测到这个函数的作用了。对的，它的作用就是让刻线消失，即返回无刻线对象；既然无刻线了，那么标示也就没有了，正所谓“皮之不存毛将焉附”。因此，这个函数的作用就在于，如果想要把某个坐标轴的刻度都取消了，可以用它的返回值为对象。</li>
<li>NullFormatter：对照着上面的，理解这个函数就比较简单了，它返回的是没有标示的对象。</li>
<li>set_major_locator：设置主刻度的刻线。</li>
<li>set_major_formatter：设置主刻度的标示。</li>
</ul>
<p>② 的作用效果就是将坐标系对象（ax）的 y 轴（yaxis）主刻线设置为无；③ 的作用效果是将 x 轴的标示设置为无，但是刻线还是存在的。</p>
<p>下面用一个具体的例子，来显示上面所学技能的应用。</p>
<p>此例将要显示一些头像。</p>
<pre><code class="python language-python">from sklearn.datasets import fetch_olivetti_faces

faces = fetch_olivetti_faces().images
fig, ax = plt.subplots(5, 5, figsize=(5, 5))
fig.subplots_adjust(hspace=0, wspace=0) 

for i in range(5):
    for j in range(5):
        ax[i, j].xaxis.set_major_locator(plt.NullLocator())
        ax[i, j].yaxis.set_major_locator(plt.NullLocator())
        ax[i, j].imshow(faces[10*i+j], cmap='bone')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b1438d80-3352-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>fig, ax = plt.subplots(5, 5, figsize=(5, 5)) 这句的作用是创建 5 × 5 分布的多个坐标系，然后用循环语句，对每个坐标系的坐标轴进行设置（ax[i, j].xaxis.set_major_locator(plt.NullLocator())），并最后将 faces = fetch_olivetti_faces().images 所得到的头像展示到每个坐标系中，即 ax[i, j].imshow(faces[10*i+j], cmap='bone')。</p>
<p>除了使用 set_major_locator 和 set_minor_formatter 设置主刻度之外，还可以使用 set_minor_locator 和 set_minor_formatter 设置副刻线。由于使用方法都是雷同的，就不重复演示了。</p>
<h3 id="125">1.2.5 两个纵轴</h3>
<p>到目前为止，已经对坐标轴上的有关项目设置有了初步了解。但是学习不能浅尝辄止，要不断深入。下面的示例既是前面知识的综合应用，又是理解和应用的深入。</p>
<p>在某种情况下，需要将两个坐标系重叠在一起，横轴是同一条，纵轴则是左右各一个，在中间区域显示图线。具体示例如下：</p>
<pre><code class="python language-python">import numpy as np
# 生成两组数据集：(x, y1) 和 (x, y2)
x = np.linspace(0, 10, 50)
y1 = np.exp(x)
y2 = np.sin(x)

# 绘制(x, y1)图像
fig, ax1 = plt.subplots()    # ④
ax1.plot(x, y1, "b")
ax1.set_xlabel('x axis')
ax1.set_ylabel("exp", color='blue')
ax1.tick_params(axis='y', which='major', colors='blue', width=4, length=9)    # ⑤

#绘制(x, y2)图像
ax2 = ax1.twinx()    # ⑥
ax2.plot(x, y2, color="red")
ax2.set_ylabel("sin", color="red")
ax2.tick_params(axis='y', colors='red', direction='inout')    # ⑦
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/89668ea0-3354-11e9-b59c-dfe60266e7ff" width = "80%" /></p>
<p>先观察结果，这就是本示例要得到的。再来看代码，是如何实现如此结果的。</p>
<p>语句 ④ 跟前面看到的一样，创建坐标系对象 ax1，然后在这个对象中绘制（x, y1）这组数据的图像，即结果中呈现的蓝色图线。</p>
<p>语句 ⑤ 是对 ax1 坐标系的 y 轴进行设置，此设置函数前面没有出现过，它的完整形式如下：</p>
<pre><code class="python language-python">ax1.tick_params(axis='both', **kwargs)
</code></pre>
<p>其作用是对坐标轴的刻线、标示和网格线进行设置，主要参数如下。</p>
<ul>
<li>axis：可选值为 {'x', 'y', 'both'}，指明要设置哪个坐标轴。</li>
</ul>
<p>其他的参数，都由 kwargs 收集，主要包括以下几个。</p>
<ul>
<li>which：可选值为 {'major', 'minor', 'both'}，默认为 'major'，指定所要设置的刻度是主刻度还是副刻度，亦或两者均有。</li>
<li>direction：可选值为 {'in', 'out', 'inout'}，指定相应坐标轴上的刻线是在轴的外侧、内侧还是内外都有。</li>
<li>length：浮点数，指定表示刻线的线段长度。</li>
<li>width：浮点数，指定表示刻线的线段宽度。</li>
<li>color：Matplotlib 所接受的颜色，指定表示刻线的线段的颜色。</li>
<li>labelsize：浮点数或字符串，比如 'large' 等，设置标示的字号大小。</li>
<li>labelcolor：Matplotlib 所接受的颜色，设置标示文字的颜色。</li>
<li>colors：将刻线和标示颜色设置为同一个值。</li>
</ul>
<p>除了以上几个参数之外，还有别的，还是建议读者经常使用 ax1.tick_params? 查看帮助文档。</p>
<p>阅读完毕上述几个参数的含义，再回头看语句 ⑤，对照图中蓝色的 y 轴，就不难理解了。同样，语句 ⑦ 是设置图中的红色 y 轴，所用参数也在上述参数含义解释范畴。</p>
<p>为了绘制图中红色的 y 轴，也就是将另外一个坐标系可以视为一个新的图层，叠加到原来坐标系之上，就必须使用语句 ⑥。</p>
<p>ax2 = ax1.twinx() 中的函数 twinx 的命名应该来自于单词“twins”（双胞胎），可以比较通俗的理解为：以 ax1 坐标系的 x 轴为基准创建一个双胞胎的坐标系对象 ax2，显然这两个坐标系对象公用 x 轴。那么，y 轴就是相对而立了。</p>
<p>在语句 ⑥ 之后的，就是在 ax2 坐标系对象中的各种操作了。</p>
<p>于是乎，最终得到了上图所示的结果。</p>
<p>对于上面的坐标轴，还可以更精细化设置。</p>
<pre><code class="python language-python">import sys
import numpy as np
from matplotlib.ticker import AutoMinorLocator
x = np.linspace(0, 10, 50)
y1 = np.exp(x)
y2 = np.sin(x)

fig, ax1 = plt.subplots()
ax1.plot(x, y1, "b")
ax1.set_xlabel('x axis')
ax1.set_xlim(0, 10)
ax1.set_xticks(range(11))
ax1.set_ylabel("exp", color='blue')
ax1.set_ylim(0, 3000)    # ⑧
ax1.set_yticks(range(0, 3001, 600))    # ⑨
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))    # ⑩
ax1.tick_params(axis='y', which='major', colors='blue', direction='in')

ax2 = ax1.twinx()
ax2.plot(x, y2, color="red")
ax2.set_ylabel("sin", color="red")
ax2.tick_params(axis='y', colors='red', direction='inout')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d1bf73e0-3356-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>将上述图像和代码跟前面的对比，发现蓝色的纵轴有了变化，主要是以下几个语句：</p>
<ul>
<li>语句 ⑧ 设置了纵轴显示的数值范围；</li>
<li>语句 ⑨ 设置了主刻度的标示所显示的数值；</li>
<li>语句 ⑩ 中的 set_minor_locator，顾名思义，是用来设置副刻度的刻线的，并且以 AutoMinorLocator(5) 规定了主刻线之间的副刻线的段数。</li>
</ul>
<p>最终得到了更精细化的纵轴。</p>
<p>坐标轴的设置还有其他很多内容，在掌握了上述基本方法之后，当项目实践中遇到了新问题，可以遵循本课的方法解决。</p>
<h3 id="">总结</h3>
<p>本课内容属于可视化的基础，在学习过程中，请务必确立如下观念：</p>
<ul>
<li>坐标系是对象，其他都是属性</li>
<li>记不住方法、属性，不用担心，勤搜索，特别是要阅读帮助文档</li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>