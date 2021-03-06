---
title: 案例上手 Python 数据可视化-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本课开始，依次介绍常用的一些统计图表，以下引用来自<a href="https://zh.wikipedia.org/zh-sg/%E7%B5%B1%E8%A8%88%E5%9C%96%E8%A1%A8">维基百科中的“统计图表”词条</a>部分内容。</p>
<blockquote>
  <p>图表（Chart），或又称为统计图表，代表了一张图像化的数据，并经常以所用的图像命名，例如圆饼图，是主要使用圆形符号，长条图或直方图，则主要使用长方形符号。折线图，意味着使用线条符号。</p>
  <p>常见的图表包括：直方图（Histogram）、长条图（Bar Chart）、饼图（Pie Chart）、折线图（Line Chart）等。 </p>
</blockquote>
<h3 id="151">1.5.1 柱形图</h3>
<p>柱形图，还称为长条图、条图、条状图、棒形圖、柱状图，长条图，英文中可以使用“bar graph”或者“bar chart”。</p>
<p>柱形图基本样式如下图所示，它是一种以柱子高度为变量的统计图表。在柱形图中可以直观地观察到某些变量之间的相对大小关系。通常，柱形图适用于较小的数据集，如果数据集的维度太多，会造成“柱子”太密集，失去了可视化的效果。</p>
<pre><code class="python language-python">%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

position = ['apple', 'facebook', 'google', 'huawei', 'alibaba']
data = [56, 65, 98, 73, 86]
plt.bar(x=position, height=data)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/8c672790-341c-11e9-8f64-a912b70d64e7" alt="enter image description here" /></p>
<p>绘制柱形图所使用的函数为 plt.bar，其完整形式如下：</p>
<pre><code class="python language-python">plt.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)
</code></pre>
<p>下面对若干常用参数进行解释：</p>
<ul>
<li>x，坐标系的横坐标</li>
<li>height，柱子的高度</li>
<li>width，柱子的宽度</li>
<li>bottom，柱子底部与 x 轴之间的距离</li>
<li>align，可选值为 'center' 或 'edge'，设置 x 轴横坐标的主刻线与柱子的中央对齐，还是与边缘对齐</li>
<li>color，柱子的颜色</li>
<li>edgecolor，柱子边缘的颜色</li>
<li>linewidth，柱子边线的宽度，如果为 0，则没有边线</li>
<li>tick_label，横坐标刻线的标示，如果不设置，则默认为数字</li>
</ul>
<p>再使用 plt.bar 制图，加深对某些参数的理解，特别注意观察参数的值和输出结果，并与上面的输出结果对比。</p>
<pre><code class="python language-python">plt.bar(x=position, height=data, width=0.4, bottom=[10,7,0,5,3], color='red', linewidth=5)
plt.grid(True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/a89a6490-341c-11e9-b4e3-a94c6cd09ca9" width = "80%" /></p>
<p>除了使用 plt.bar 之外，前面曾经提过，在 pandas 的 DataFrame 对象下，有专门绘图的方法，柱形图就可以这样来实现。</p>
<pre><code class="python language-python">df = pd.DataFrame({"position":position, 'data':data})
df.plot.bar(x='position', y='data')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5c900be0-3421-11e9-8f64-a912b70d64e7" alt="enter image description here" /></p>
<p>上述柱形图比较的是单个变量（维度、特征）之间的大小关系，在此基础上，还可以用一种称为“堆积柱形图”的方式，展示每个变量（维度、特征）内部的各元素比例。</p>
<p>下面看一个示例，是对近年全国暑期票房收入的统计（仅统计历年 8 月份），借此理解“堆积柱形图”的绘制和应用。</p>
<p>首先本例所用数据来自 Tushare，如果读者愿意使用第三方模块获得数据，请安装：pip3 install Tushare，然后按照如下演示得到数据。但是，这个模块的官方在读者阅读的时候或许已经修改了读取数据的政策，若用下面的方式没有得到数据，请到<a href="http://tushare.org/">官方网站</a>查阅最新政策。另外，为了方便学习，我把以下示例用到的数据整理到了<a href="https://github.com/qiwsir/DataSet/tree/master/boxoffice">数据仓库</a>，可以将此数据下载到本地，然后用<code>pd.read_csv</code>函数加载。</p>
<pre><code class="python language-python">import tushare as ts
box_office = pd.DataFrame()
for y in range(2010, 2019):    # 2010年(含)至2018年(含)
    ym = str(y) + '-8'
    df = ts.month_boxoffice(ym)
    box_office[ym] = df['boxoffice']
box_office

# output
    2010-8  2011-8  2012-8  2013-8  2014-8  2015-8  2016-8  2017-8  2018-8
0    26918   39162   27993   63665   39313   73427   98811   424006  132009
1    17760   30890   23051   29567   36338   54977   58144   53419   122078
2    8816    22919   15020   29460   28981   48912   38770   49087   102581
3    8125    17219   14636   17121   20807   20948   38675   34147   68285
4    5157    6243    13518   16468   18746   19542   34589   29012   55460
5    5133    5326    8895    14473   18714   18083   26931   23652   32013
6    3980    3594    7037    11416   16926   17220   16663   16825   23011
7    2655    3410    6868    7542    9770    14643   15334   15806   19543
8    2581    3301    4159    6286    9729    14458   14736   12588   17830
9    2233    1954    3471    5440    9464    9977    8376    11341   15238
10    8245    13137   17216   24674   53426   69576   54576   66712   93990
</code></pre>
<p>然后计算每年的票房总收入。</p>
<pre><code class="python language-python">box_office = box_office.astype(np.int)    # 将数据类型转化为整数型
total = box_office.sum()
total

# output
2010-8     91603
2011-8    147155
2012-8    141864
2013-8    226112
2014-8    262214
2015-8    361763
2016-8    405605
2017-8    736595
2018-8    682038
dtype: int64
</code></pre>
<p>接下来才是激动人心的时刻，先贴出代码和结果，再慢慢品味。</p>
<pre><code class="python language-python">import matplotlib.ticker as ticker

first = box_office.iloc[0].astype(np.int)    # 历年票房第一
after_first = total - first    # 其他影片票房收入

date_index = pd.to_datetime(total.index)
fig, ax = plt.subplots()
ax.grid(color='gray')

ax.bar(range(1, 10), after_first.values, label='others')    # ①
ax.bar(range(1, 10), first.values, bottom=after_first.values, label='first')    # ②

ax.set_xticks(range(0, 10))   # ③
ax.xaxis.set_major_formatter(ticker.IndexFormatter([0]+date_index.year.tolist()))    # ④

plt.legend(loc=0)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/a25511c0-3421-11e9-a53d-f367a5a2493f" width = "85%" /></p>
<p>先观察输出结果的图示，从中都可以读出什么信息？</p>
<ul>
<li>基本上票房收入在一直增加，2017 年 8 月份是历年 8 月份的最高峰，2018 年则略有下降。</li>
<li>再看每年票房收入第一的影片在当年总收入中所占比重，显然 2017 年的是凸点，这年影片票房收入的头部效应非常显著，而其他影片的票房收入相比上一年并没有太多增加。</li>
</ul>
<p>2017 年票房第一的就是那部高扬民族主义大旗的动作片《战狼2》，据娱乐新闻报道后来也得补税。</p>
<p>看电影的时候热血沸腾，但研究科学问题，还是要静下心来。“科学技术是第一生产力”，再鼓舞士气的电影，也不如扎扎实实的生产力发展。因此，建议读者，还是要认真研究程序中的每个语句，这才是真正民族崛起的保证。</p>
<p>① 和 ② 两个语句，是在坐标系中绘制柱形图，它们的差别在于 ① 中没有设置 bottom 参数，② 中有 bottom = after_first.values，从而实现票房收入第一的和当年其他影片收入成为“堆积柱”，两者的总高度是该年的总票房收入。</p>
<blockquote>
  <p>注意，语句 ③ 和 ④ 是用来设置横坐标的主刻线以及相应的标示，特别是在 ④ 中，使用了 matplotlib.ticker 中的 IndexFormatter 类得到标示对象。</p>
</blockquote>
<p>堆积柱形图可以看做是柱形图的拓展，此外，还有被称为“簇状柱形图”的拓展，即将若干个柱形图作为一簇，在每一簇中，柱子和柱子之间的距离小于簇与簇之间的距离，通常将簇内各柱子之间距离设置为 0。</p>
<pre><code class="python language-python">position = np.arange(1, 6)
a = np.random.random(5)
b = np.random.random(5)

total_width = 0.8    
n = 2
width = total_width / n
position = position - (total_width - width) / n    # ⑤

plt.bar(position, a, width=width, label='a', color='b')    # ⑥
plt.bar(position + width, b, width=width, label='b', color='r')    # ⑦

plt.legend(loc=0)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/bcc34630-3421-11e9-a53d-f367a5a2493f" width = "80%" /></p>
<p>语句 ⑤ 计算除了每簇的中央位置，这个很重要，请揣摩一下它的数学表达式含义。</p>
<p>语句 ⑥ 和 ⑦ 分别绘制每簇中的两个柱子，因为每簇中柱子之间的距离是 0，所以在 ⑦ 中用 position + width 表示第二根柱子的中央线位置。</p>
<p>对于绘制“簇状柱形图”，如果直接使用 DataFrame 对象的方法，可以更简单。例如：</p>
<pre><code class="python language-python">speed = [0.1, 17.5, 40, 48, 52, 69, 88]
lifespan = [2, 8, 70, 1.5, 25, 12, 28]
index = ['snail', 'pig', 'elephant', 'rabbit', 'giraffe', 'coyote', 'horse']
df = pd.DataFrame({'speed': speed,'lifespan': lifespan}, index=index)
ax = df.plot.bar(rot=0)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d48b87f0-3421-11e9-985c-09aa3159296f" width = "80%" /></p>
<p>从实现结果的代码行数来看，通过这种方法非常简单了。在 df.plot.bar 方法中，可以通过增加参数 subplots=True，将上述图像分开。</p>
<pre><code class="python language-python">axes = df.plot.bar(rot=0, subplots=True)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/39fa7b00-3422-11e9-a53d-f367a5a2493f" alt="enter image description here" /></p>
<p>除了以上的几种柱形图之外，其实还可以把柱形图绘制的更多样化，比如下面的“正负柱形图”：</p>
<pre><code class="python language-python">n = 12
X = np.arange(n)
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

for x, y in zip(X, Y1):
    plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

plt.ylim(-1.25, +1.25)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/472f6960-3423-11e9-985c-09aa3159296f" alt="enter image description here" /></p>
<p>但是，要提醒注意了，虽然可以通过各种技术把统计图绘制的很漂亮，但这不是目的。统计图的目标是要让统计数据以适合的方式，即以通俗易懂的方式可视化地展现出来，追求绚丽，不是数据可视化的终极目标。</p>
<p>如果把柱形图转 90°，那张图可以称之为“条形图”。</p>
<h3 id="152">1.5.2 条形图</h3>
<p>把条形图称为柱形图，也无妨。但是依据习惯，竖直的圆柱体为“柱”，水平放置的则用“条”描述。</p>
<p>既然条形图和柱形图没有什么本质区别，那么绘图的方法也就类似了。</p>
<pre><code class="python language-python">position = np.arange(1, 6)
a = np.random.random(5)
plt.barh(position, a)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/58fb3a70-3423-11e9-b4e3-a94c6cd09ca9" width = "80%" /></p>
<p>对于条形图，有一个特例，名之曰“正负条形图”，其实现方法如下：</p>
<pre><code class="python language-python">import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

position = np.arange(1, 6)
a = np.random.random(5)
b = np.random.random(5)

plt.barh(position, a, color='g', label='a')
plt.barh(position, -b, color='r', label='b')

plt.legend(loc=0)

ax = plt.gca()  
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0)) 
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/b9df0010-3423-11e9-985c-09aa3159296f" alt="enter image description here" /></p>
<p>其实，这种正负条形图，与前面的“正负柱形图”其实画法是一样的，只不过这里移动了纵坐标轴罢了，这也是前面曾经介绍过的。因此，此处不对上述代码进行解释，但建议读者对每一行代码进行注释，才能温故知新。</p>
<h3 id="153">1.5.3 三维坐标系中的柱形图</h3>
<p>坐标系，除了由 x、y 轴组成的二维坐标系之外，还有由 x、y、z 三个坐标轴组成的三维坐标系。那么，如何绘制三维坐标系？在这种坐标系中怎么绘制柱形图？</p>
<pre><code class="python language-python">from mpl_toolkits.mplot3d import Axes3D    # 这个引入是必须的，之后才能正确执行⑧

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')    # ⑧
for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    xs = np.arange(20)
    ys = np.random.rand(20)
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/c84bc7a0-3423-11e9-a53d-f367a5a2493f" alt="enter image description here" /></p>
<p>⑧ 是创建三维坐标系的关键，通过参数 projection='3d'，说明在 fig 对象中创建的坐标系是三维坐标系。是否还记得上一课中的极坐标系？也是设置参数 projection 值而实现的。</p>
<p>后续代码，读者利用已学过知识和 Python 语言的知识，理解它们并无困难，因此，建议读者对它们进行注释，阐明其作用——已经有几次建议读者自行对代码进行注释了，这是学习编程的一个好方法，美其名曰“阅读代码”。</p>
<p>通过前述内容的学习，已经对柱形图和条形图的绘制方法有了基本认识。下面就通过一个示例，来检验所学情况。</p>
<h3 id="154">1.5.4 应用举例</h3>
<p>从<a href="https://github.com/qiwsir/DataSet/tree/master/school/school.csv">数据集</a>中读取数据，建议将此仓库克隆到本地使用。</p>
<pre><code class="python language-python">df = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/school/school.csv")
df.sample(5)
</code></pre>
<p>输出结果：</p>
<table>
<thead>
<tr>
<th></th>
<th>School</th>
<th>Women</th>
<th>Men</th>
<th>Gap</th>
</tr>
</thead>
<tbody>
<tr>
<td>3</td>
<td>U.Penn</td>
<td>92</td>
<td>141</td>
<td>49</td>
</tr>
<tr>
<td>18</td>
<td>Emory</td>
<td>68</td>
<td>82</td>
<td>14</td>
</tr>
<tr>
<td>2</td>
<td>Harvard</td>
<td>112</td>
<td>165</td>
<td>53</td>
</tr>
<tr>
<td>6</td>
<td>Georgetown</td>
<td>94</td>
<td>131</td>
<td>37</td>
</tr>
<tr>
<td>16</td>
<td>Brown</td>
<td>72</td>
<td>92</td>
<td>20</td>
</tr>
</tbody>
</table>
<p>用随机抽样方法 sample 查看这个数据集的基本结构，它是 DataFrame 类型的数据，于是就可以直接使用 DataFrame 对象的绘图方法。</p>
<pre><code class="python language-python">df.plot.bar(rot=0)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/d86be480-3423-11e9-985c-09aa3159296f" alt="enter image description here" /></p>
<p>虽然这样做就很简单地得到了柱形图，但是，这张图并不友好。</p>
<pre><code class="python language-python">from matplotlib.ticker import StrMethodFormatter

ax = df.plot(kind='barh', x='School', figsize=(8, 10), zorder=2, width=0.85)    # ⑨

#隐藏坐标轴
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 设置刻度
ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

# 绘制垂直横轴的虚线
vals = ax.get_xticks()    # ⑩
for tick in vals:
    ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='grey', zorder=1)

ax.set_xlabel("毕业生年平均薪酬", labelpad=20, weight='bold', size=12)
ax.set_ylabel("毕业学校", labelpad=20, weight='bold', size=12)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/e7b3c9d0-3423-11e9-8f64-a912b70d64e7" alt="enter image description here" /></p>
<p>经过优化之后，图示结果的可读性提高了很多。</p>
<p>有几个重点语句，有必要说明。</p>
<p>⑨ 语句是新出现的，以往使用的是 df.plot.bar 或者 df.plot.barh 绘制柱形图或条形图，但这里使用了 df.plot，同时需要在参数中必须要有 kind='barh'，才能绘制条形图，如果是 kind='bar'，绘制的就是柱形图了。参数中的 x='School'，是指定每簇条的值，即数据集中的特征 School 下的值。</p>
<p>⑩ 语句的目的是得到当前横坐标刻度对象，从而在下面的循环语句中，可以得到每个刻度对象，然后依据刻度绘制垂直于 x 轴的虚线——ax.axvline 方法的作用就在于此。</p>
<p>示例中的其他语句都应该不陌生了，因此仍旧建议逐行进行注释，以理解其含义。</p>
<h3 id="">总结</h3>
<p>本课主要练习如何绘制柱形图和条形图，基本方法：</p>
<ul>
<li>柱形图，plt.bar，或者 df.plot.bar、df.plot(kind='bar')</li>
<li>条形图，plt.barh，或者 df.plot.barh、df.plot(kind='barh')</li>
</ul>
<p>此外，为了绘制的图像更美观，或者可读性更强，还会根据具体情况对坐标轴、刻度等进行设置。</p>
<h3 id="-1">答疑与交流</h3>
<p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加编辑小姐姐微信：「GitChatty6」，回复关键字「288」给编辑小姐姐获取入群资格。</p></div></article>