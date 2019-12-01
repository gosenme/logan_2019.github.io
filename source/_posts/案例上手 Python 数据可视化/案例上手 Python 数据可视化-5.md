---
title: 案例上手 Python 数据可视化-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本课开始，将逐一介绍实现数据可视化的有关工具，第一个要学习的是 Matplotlib。</p>
<p>初次看到这个名字，是不是会想到另外一个著名的数学工具：Matlab（没想到也不要紧，毕竟 Matlab 是一个在数学及相关领域使用的专门工具）。之所以要提及 Matlab，是因为它在与数学有关的应用方面颇有些神通，历史也很悠久。但是，随着应用的要求越来越多，这个有点“古老”的工具，显得力不从心了，于是乎在数据分析、机器学习领域 Python 就异军突起。随着 Python 的广泛应用，还要有很多的工具分别实现不同的应用。那么，在数据可视化层面，最早出现的就是 Matplotlib，因此，标题称其为“开山鼻祖”，丝毫不为过。</p>
<p>Matplotlib 的发明者是 John D. Hunter（一定要向大神献上敬意、崇拜和感谢）。</p>
<p>2003 年发布了 Matplotlib 的 0.1 版，一路发展而来，版本不断更迭、功能不断丰富。截止到写这段内容为止，官方网站（<a href="http://matplotlib.org/">http://matplotlib.org/</a>）上发布的最新版本是 3.02。</p>
<p>Matplotlib 的使用方法有点类似于 Matlab。同时，它提供了“面向对象的 API”，让经过严格程序开发训练的人用起来也相当顺手。并且，它继承了 Python 的优良传统和一贯作风，即免费、开源和跨平台。</p>
<p>随着技术的进步和时代的变迁，现在能够实现数据可视化的工具越来越多，它们都意欲向 Matplotlib 发起挑战。尽管如此，Matplotlib 的江湖地位依然稳固，并且有很多新生代工具也是依靠它而建立的，比如 Seaborn。因此，学习 Matplotlib，合算且有必要，更何况，Matplotlib 也在与时俱进。</p>
<h3 id="11">1.1 按部就班初体验</h3>
<p>好东西，就要有好体验。</p>
<p>先执行 Jupyter，新建一个页面，然后输入如下代码块：</p>
<pre><code class="python language-python">%matplotlib inline
</code></pre>
<p>页面中的效果如下图：</p>
<p><img src="https://images.gitbook.cn/88136310-3346-11e9-b59c-dfe60266e7ff" alt="enter image description here" /></p>
<blockquote>
  <p>注意，在输入这一行的时候，“%”与后面的“matplotlib”之间不要有空格。</p>
</blockquote>
<p>完成这一行输入之后，通过组合键 Shift + Return（Shift + Enter）执行此代码块——以后提到执行代码或程序，都是如此操作。</p>
<p>执行之后，若没有什么反应，这说明完全正确了。这行代码的作用是告诉 Jupyter，如果生成了图像，就嵌入到当前浏览器页面中；如果不写 inline，会在另外一个新的窗口显示所绘制的图像。</p>
<p>在 Matplotlib 中，真正用来绘图的，是其中一个名字为 pyplot 的子模块，它是一个类似 Matlab 的接口。因此，要用下面的方式引入。注意，引入这个模块之后，为了方便，通常重名为 plt。</p>
<pre><code class="python language-python">import matplotlib.pyplot as plt
</code></pre>
<p>上述代码完成之后，不要执行，而是直接按下回车键，即可在当前代码输入框中继续向下输入。</p>
<p>还要引入在数据科学中常用的 NumPy。</p>
<pre><code>import numpy as np
</code></pre>
<p>依然不执行代码块，接下来就要写一段程序，演示如何绘制一个函数的曲线。继续输入：</p>
<pre><code>a = np.linspace(0, 10, 100)
b = np.exp(-a)
plt.plot(a,  b)
</code></pre>
<p>这部分代码输入完毕，然后执行。如果一切顺利，会得到如下图一样的结果；如果报错，首先检查拼写问题哦。</p>
<p><img src="https://images.gitbook.cn/f44c01e0-3346-11e9-b3a9-4f8760d3237f" width = "70%" /></p>
<p>以上代码，是在 Jupyter 中绘图的方式。如果不在这个环境中，而是想把代码写成一个可执行的 Python 文件，还需要增加一点东西。</p>
<pre><code class="python language-python">#coding: utf-8
'''
filename: ./chapter111.py
'''

import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(0, 10, 100)
b = np.exp(-a)
plt.plot(a,  b)

plt.show()
</code></pre>
<p>上面的代码不是写到当前的 Jupyter 中，而是打开一个 IDE，然后把它写入其中，并保存为某名称的文件，比如这里将其命名为 chapter111.py。而后用如下命令执行：</p>
<pre><code class="bash language-bash">$ python3 chapter111.py
</code></pre>
<p>执行此程序文件之后，注意观察，会出现一个新窗口，如下图所示。</p>
<p><img src="https://images.gitbook.cn/34938b10-3347-11e9-b3a9-4f8760d3237f" width = "60%" /></p>
<p>这个图提供的功能也不少，可以试一试图示中下面一排功能按钮，体会它们的作用。</p>
<p>以上体验了两种开发环境中制图的方式，特别提醒的是，在 IDE 中写制图程序的时候，需要增加 plt.show()，告诉程序把最终的图示展现出来。通常一个程序就一条这个语句，不论在这个程序中有多少个图。</p>
<p>根据数据科学工作者的习惯，我们还是使用 Jupyter，下文都如此。</p>
<p>在上面的代码中，核心就是 plt.plot 函数，可以通过下面的方式查看这个函数的完整内容。</p>
<p>在 Jupyter 中输入：</p>
<pre><code>plt.plot?
</code></pre>
<p>执行之后，可以看到关于此函数的完整内容。下面是摘录的一部分：</p>
<blockquote>
  <p>Signature: plt.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
  Docstring:
  Plot y versus x as lines and/or markers.</p>
  <p>Call signatures::</p>
<pre><code>plot([x], y, [fmt], data=None, **kwargs)
plot([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)
</code></pre>
  <p>The coordinates of the points or line nodes are given by <em>x</em>, <em>y</em>.</p>
</blockquote>
<p>plt.plot 主要用于绘制曲线和点，需要提供 x 和 y 两个坐标轴的参数。至于这个函数的详细应用，后面会讲述。在这里，请掌握一种<strong>重要的学习方法：查看帮助文档</strong>。操作方式就如同上面所示。</p>
<p>以上绘图过程，其基本思路是承接了 Matlab 的思想，不是在现代编程语言中所倡导的“面向对象”的思想——但并不意味着这种方式不能使用。</p>
<p>那么，如果依据“面向对象”的思想，怎么使用 Matplotlib 作图呢？</p>
<p>先看来自 Matplotlib 官网上的一张图，这张图的内涵相当丰富。</p>
<p><img src="https://images.gitbook.cn/6e9a6ea0-3347-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>这张图，可以看做是一张 Matplotlib 的藏宝图，在以后的课程中，我们会对其中的各对象逐一剖析，内化为自己的知识。</p>
<p>如果将这张图或绘制这张图的过程看作对象，那么图中各元素就是“属性”，其呈现的结果就是“属性的值”，而制作某个元素就是用对象的“方法”实现了。</p>
<p>比如把图中的坐标系看做一个对象，那么在这个坐标系中绘制一条曲线（例如上图中蓝色的那条曲线），就是执行这个坐标系的一种绘图方法。而所绘制的图线的颜色，则是此曲线的属性（属性值是“蓝色”）。</p>
<p>下面就依照“面向对象”的过程，绘制图像。</p>
<p>（1）创建 Figure 对象，它类似于一张画布，可以在这张画布上绘制其他对象。</p>
<pre><code class="python language-python">fig = plt.figure()
</code></pre>
<p>首先创建一个 Figure 对象，它就相当于一张画布。</p>
<p>创建 Figure 实例对象的方法还可以是：plt.Figure()。</p>
<p>（2）创建坐标系</p>
<p>如果要绘制某种曲线，坐标系是不可或缺的。依据面向对象的思想，所创建的 fig 实例对象，应该具有一种创建坐标系的方法。</p>
<p>这个推论完全正确。</p>
<p>继续在上面的代码块中写如下语句：</p>
<pre><code class="python language-python">ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
</code></pre>
<p>add_axes 就是 fig 实例对象中用来创建坐标系的方法，即由此创建了一个 axes 对象，用变量 ax 引用。</p>
<p>如果想知道 fig 实例对象中都有哪些方法？可以如此操作。</p>
<p>在一个代码块中先输入 fig.（注意那个英文句点），然后按下键盘上的 TAB 键，就会看到下图的效果，这里面的都是 fig 实例的属相和方法。因此，不用有意识地去记忆，使用这种方式查找方法和属性名称。</p>
<p><img src="https://images.gitbook.cn/f0394350-3347-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>再解释一下上面那一行代码。参数 [0.1, 0.1, 0.8, 0.8] 确定了这个坐标系的位置，其含义为 [left, bottom, width, height]，左右尺寸都是相对于画布（即 fig 对象）的百分比。例如，第一个 0.1，表示坐标系的左侧相对画布左侧距离为画布宽度的 10%；第四个 0.8，表示坐标系的高度为画布高度的 80%。</p>
<p>目前，代码块中有了上述两行代码了，执行后，就可以看到一张已经有坐标系的图了。</p>
<p><img src="https://images.gitbook.cn/51048270-3349-11e9-ae61-ab46ecd2ee1c" width = "80%" /></p>
<p>（3）在坐标系内画曲线</p>
<p>利用 fig.add_axes() 创建了一个 Axes 对象，它跟 Figure 对象类似，都是“容器”，即 Axes 对象可以包含其他东西。</p>
<p>还是按照“面向对象”的思路，调用变量 ax 所引用的 axes 对象的方法（切换到 Jupyter）。</p>
<p>在前面的代码块里面，接着写入下面的语句：</p>
<pre><code class="python language-python">a = np.linspace(0, 10, 100)
b = np.exp(-a)
ax.plot(a, b)
</code></pre>
<p>写好这段代码，就可以立刻执行了，看下效果，如下图所示。</p>
<p><img src="https://images.gitbook.cn/87f5e8a0-3349-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>如此，就完成了制图，得到了函数曲线。</p>
<p>以上两个作图过程，可以理解为两种风格：</p>
<ul>
<li>第一种是继承了 Matlab 的做法，称为“Matlab 风格”，主要是通过 plt 操作各种绘图相关的函数；</li>
<li>第二种以“面向对象”的编程思想为基础，通过对象的方法和属性完成作图。</li>
</ul>
<p>两者所使用的方法和属性也都是相同的或类似的，下表分别列出了常用的几项。</p>
<table>
<thead>
<tr>
<th>plt 函数</th>
<th>ax 对象方法</th>
</tr>
</thead>
<tbody>
<tr>
<td>plt.plot</td>
<td>ax.plot</td>
</tr>
<tr>
<td>plt.legend</td>
<td>ax.legend</td>
</tr>
<tr>
<td>plt.xlabel</td>
<td>ax.set_xlabel</td>
</tr>
<tr>
<td>plt.ylabel</td>
<td>ax.set_ylabel</td>
</tr>
<tr>
<td>plt.xlim</td>
<td>ax.set_xlim</td>
</tr>
<tr>
<td>plt.ylim</td>
<td>ax.set_ylim</td>
</tr>
<tr>
<td>plt.title</td>
<td>ax.set_title</td>
</tr>
</tbody>
</table>
<p>“面向对象”和“Matlab 风格”没有优劣之分，因此，后面会交叉使用，请不必厚此薄彼。</p>
<p>用 Matplotlib 除了能完成函数曲线图之外，还能做常规的统计图，比如直方图，它是统计学中常用的一种图形。</p>
<p>在新的代码块中输入如下代码：</p>
<pre><code class="python language-python">from numpy.random import normal,rand
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
x = normal(size=200)
ax.hist(x, bins=30)
</code></pre>
<p>然后执行，会看到下图效果：</p>
<p><img src="https://images.gitbook.cn/d0d6fb90-3349-11e9-ae61-ab46ecd2ee1c" width = "65%" /></p>
<p>因为所用的是随机数，所以，看到的直方图可能互不相同。</p>
<p>ax.hist 就是坐标系对象绘制直方图的方法。</p>
<p>当然，可以绘制的图还有很多种，后面我们会逐渐接触到。</p>
<h3 id="">总结</h3>
<p>本课是对 Matplot 的初步体验，特别介绍了两种制图方式。在初步接触中，几个函数（方法），并且重点强调要阅读帮助文档，这是一种重要学习方法。</p>
<hr />
<p>此外，还有如下学习资源，供选择使用：</p>
<ul>
<li><a href="https://github.com/qiwsir/data_visualization">本课程的代码仓库</a></li>
<li><a href="https://github.com/qiwsir/DataSet">本课程所需的数据集</a></li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>