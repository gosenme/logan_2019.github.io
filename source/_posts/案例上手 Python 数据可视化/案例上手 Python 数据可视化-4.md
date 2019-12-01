---
title: 案例上手 Python 数据可视化-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本达人课不是针对零基础的学习者，需要具备以下知识。</p>
<p>（1）Python 基础知识，包括但不限于：</p>
<ul>
<li>掌握 Python 内置的基本对象类型，如数字、字符串、列表、字典、元组等</li>
<li>掌握 Python 的基本语法规则，如引入模块的方法、for 循环语句等</li>
<li>掌握 Python 中函数的编写方法</li>
<li>掌握 Python 中类的基本概念和了解面向对象的思想</li>
</ul>
<blockquote>
  <p>这里推荐《<a href="https://gitbook.cn/m/mazi/comp/column?columnId=5ad56a79af8f2f35290f6535">Python 快速入门</a>》达人课来学习。</p>
</blockquote>
<p>（2）NumPy 和 Pandas 的基本知识，包括但不限于：</p>
<ul>
<li>利用 NumPy 创建数组，以及数组相关的方法（或者 Numpy 的函数）</li>
<li>利用 Pandas 创建 Series 和 DataFrame 对象，以及相应的操作和方法</li>
</ul>
<blockquote>
  <p>以上知识，在拙作《跟老齐学 Python：轻松入门》《跟老齐学 Python：数据分析》图书中均有详细介绍，可供参考。</p>
</blockquote>
<p>有了以上知识作为基础，接下来要做的是安装数据可视化相关的包（模块）。在 Python 中，基本安装方法是使用 pip 安装，但是在数据科学方面，有两个可供使用的环境。</p>
<h4 id="anaconda">Anaconda</h4>
<p>官方网站：<a href="https://www.anaconda.com/">https://www.anaconda.com/</a></p>
<p><img src="https://images.gitbook.cn/874ef6e0-3320-11e9-b3a9-4f8760d3237f" width = "80%" /></p>
<p>上图是官方网站界面的截图，其中只凸显了 Anaconda 的作用，它是一个数据科学的平台，而且宣称是最流行的，此言绝非虚妄。之所以如此受欢迎，就是因为 Anaconda 已经融汇了很多常用的工具，比如前面提到的 Numpy、Pandas 等已经集成在里面了。所以，只需要下载这个网站的 Anaconda，然后安装，通常使用的模块就都包括了——一次安装，终生受用。</p>
<p>流行，就是因为简单。</p>
<p>但是，它也绝非十全十美，或者说世界上就没有十全十美的东西吧。</p>
<p>因为 Anaconda 高度集成化，也会让你失去对模块的控制，比如你有强迫症，非要把程序文件安装到某个指定位置，这就难度大了。</p>
<p>但是，依然推荐。</p>
<h4 id="pip">pip</h4>
<p>这是我喜欢的，所有在本达人课中的安装演示，都是使用 pip。</p>
<p>除了上面两个之外，还可以直接下载源码安装，源码通常会在 github.com 这样的代码托管网站上。</p>
<p>接下来，就要演示安装本达人课所用工具的过程了。</p>
<p><strong>特别声明</strong>：</p>
<ul>
<li>本达人课中的所有操作和程序，是在 MacOS 操作系统中进行的</li>
<li>完全照搬以下安装方法，在你的计算机上不一定成功，届时请多用 Google 找方法</li>
</ul>
<p>安装工具之前，先要了解通常的命令：</p>
<ul>
<li>如果使用 anaconda，安装命令是 conda install modulename</li>
<li>如果使用的 pip，安装命令是 pip install modulename</li>
</ul>
<h3 id="jupyter">Jupyter</h3>
<p>这是一个网页版的编辑器。</p>
<p>在 Python 中，有一个“交互模式”，如下所示：</p>
<pre><code>&gt;&gt;&gt; print("Life is short, you need Python.")
Life is short, you need Python.
</code></pre>
<p>这种模式非常方便，但是，写过的代码难以保存。因此，它不是一个好的“编辑器”（根本就不是编辑器）。</p>
<p>于是乎，IPython 就应运而生了（不用着急安装 IPython，在此处它只是一个过程）。后来，在 IPython 基础上，发展出了一个基于浏览器的 Notebook，用于文本文件编辑，它兼顾了交互模式的优点，那就是即时运行，并且能够如同 IDE 一样，对代码实施保存、传播、再运行等操作。这个编辑器就是这里推荐的 Jupyter。</p>
<p>Jupyter 也是开源免费的。2014年， Fernando Pérez 发明了它，除了支持 Python 之外，它还可以支持 Julia 和 R，并且可以用于编写 Markdown 文件。</p>
<h4 id="">安装</h4>
<pre><code class="bash language-bash">pip3 install jupyter
</code></pre>
<blockquote>
  <p>注意，后面的所有安装，我都使用 pip3，表示安装适用于 Python 3 的版本。</p>
</blockquote>
<h4 id="-1">运行</h4>
<p>打开终端，到某一个工作目录，执行以下命令：</p>
<pre><code class="bash language-bash">$ jupyter notebook
</code></pre>
<p>通常，会自动打开默认浏览器，并呈现下图所示的界面。</p>
<p><img src="https://images.gitbook.cn/d3387260-3321-11e9-b59c-dfe60266e7ff" alt="enter image description here" /></p>
<p>在图示中可以看到一些扩展名为 ipynb 的文件，这些都是已经创建的 Jupyter 文件，里面都是一些相关代码，如果点击某个文件，就可以在当前环境中打开。</p>
<p>再观察上图的右上角，有“新建”下拉菜单，通过它，可以创建一个全新的编辑界面。</p>
<p>Jupyter 与通常的 GUI 软件差不多，用鼠标点来点去就可以了。当然，它有一些快捷键，如果想了解，可以在网上搜一下。</p>
<h3 id="matplotlib">Matplotlib</h3>
<p>Matplotlib 是基于 NumPy 的、Python 语言环境中的绘图工具包。它可以用于绘制类似 GUI 软件的图像，并且这些绘图工具的 API 都是基于“面向对象”思想开发的，与 Python 语言的开发思想一致（这也是现代编程语言都秉承的思想）。</p>
<p>Matplotlib 的发明者 John D. Hunter，继承了 Python 一贯的开源思想。目前 Matplotlib 已经由一个委员会来负责，发明者 John Hunter 于 2012 年 8 月被上帝接走了。</p>
<p>必须向这位伟大的发明者致以崇高的敬意。</p>
<p>自从 Matplotlib 1.2 之后，就开始支持 Python 3 了。因此，现在所安装的 Matplotlib 如果没有特别的版本指定，默认都是适合于 Python 3 的了。</p>
<p>Matplotlib 有一个重要的子模块，也是我们制图经常用的，名为：pyplot，它是一个类似于 Matlab 的接口（如果学习过 Matplab，就可以直接把其中的用法搬过来了）。其实，Matplotlib 也是参考了 Matlab 中的绘图功能而设计的专门用于 Python 中的绘图工具。</p>
<p>Matplotlib 的官方网站：<a href="https://matplotlib.org/">https://matplotlib.org/</a></p>
<h4 id="-2">安装</h4>
<p>标准方法：pip install matplotlib</p>
<p>理论上讲，如果本地缺少某些依赖程序，执行上面的命令后，会自动地将依赖的程序安装上。</p>
<p>在实际中，总会遇到意想不到的，因此，如果遇到安装不成功的事情，也不要气馁，慢慢找办法，一定能成功的。</p>
<p>最基本的条件，计算机要联网，并且网络情况别太差了。</p>
<h4 id="-3">检测是否安装成功</h4>
<p>安装之后，用下面的方式测试是否安装好。</p>
<p>在工作目录中运行 Jupyter，新建一个页面，并且命名为“chapter0-3”。</p>
<p>然后按照下图的方式输入代码：</p>
<p><img src="https://images.gitbook.cn/b34c56a0-3322-11e9-ae61-ab46ecd2ee1c" alt="enter image description here" /></p>
<p>为了方便，后面演示的时候，就把每个代码块写成如下的形式，上图中显示的是一个代码块。书写的这个代码块的方法就是：每写完一行，回车，然后写下一行。请不要复制代码，而是要自己一个一个字母地敲。</p>
<pre><code class="python language-python">%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 100, 1000)
y = np.sin(x)
plt.plot(x, y)
</code></pre>
<p>写完这个代码块之后，按组合键“Shift + Enter”，即执行这个代码块中的程序。执行结果如下图所示：</p>
<p><img src="https://images.gitbook.cn/d8590c90-3322-11e9-bff5-05638cbe7e78" width = "80%" /></p>
<p>从图中可以看到，在前述代码块的下面显示了执行结果。得到的函数曲线图，也呈现在了当前的页面中，这是因为代码块中的第一行的设置。如果没有 inline，只写 %matplotlib，你会在另外一个窗口看到画出来的图。</p>
<p>上述代码的其他部分，先不用理解，后面会详细介绍。</p>
<p>执行上述代码，如果能够得到跟图中显示一样的，就说明 Matplotlib 安装无误。如果出现错误，请特别认真阅读报错信息，然后根据报错信息到网上搜索有关解决方案。比如常见的一种错误是说缺少 backend，这是因为本地计算机没有安装 GUI 的支持框架（推荐阅读：<a href="https://matplotlib.org/tutorials/introductory/usage.html#what-is-a-backend">What is a backend?</a>，可以根据<a href="https://matplotlib.org/users/installing.html#dependencies">官方文档</a>中的说明，安装一个 backend，比如安装 <a href="https://matplotlib.org/glossary/index.html#term-tk">tk</a>）。</p>
<h3 id="seaborn">Seaborn</h3>
<p>Seaborn 是基于 Matplotlib 的一个可视化工具，它提供了一些更高级的接口，让绘图过程更简洁。</p>
<p>官方网站：<a href="https://matplotlib.org/glossary/index.html#term-tk">https://matplotlib.org/glossary/index.html#term-tk</a></p>
<p>有了前面的基础，安装 seaborn 就比较简单了：</p>
<pre><code class="python language-python">pip3 install seaborn
</code></pre>
<p>安装完毕，如果要检验是否安装成功，直接使用 import seaborn 命令，不报错，说明就没问题了。</p>
<h3 id="plotnine">Plotnine</h3>
<p>Plotnie 是在 ggplot2 的基础上发展而来的，这个模块的绘图思想和前面两个有所不同，不过这些现在不需要掌握，只需要安装它就可以了。</p>
<p>官方网站<a href="https://plotnine.readthedocs.io/en/latest/index.html">详见这里</a>。</p>
<p>官方网站给的安装方法是：pip3 install plotnine</p>
<blockquote>
  <p>如果安装过程没有那么顺利，可以参考我的经历，因为我按照这个官方网站的方法操作也没有成功。</p>
</blockquote>
<p>以下安装步骤是针对 Python 3.7 的环境。</p>
<ul>
<li>Pandas 要先升级，顺便把 Numpy 也升级吧：</li>
</ul>
<pre><code class="bash language-bash">pip3 install --upgrade pandas
pip3 install --upgrade numpy
</code></pre>
<ul>
<li>安装 Cython：</li>
</ul>
<pre><code class="bash language-bash">pip3 install cython
</code></pre>
<ul>
<li>安装最新的 Pyproj。如果这个不安装或者不适用于 Python 3.7，则会报出 gcc 错误：</li>
</ul>
<pre><code class="bash language-bash">pip3 install git+https://github.com/jswhit/pyproj.git#egg=pyproj
</code></pre>
<p>这里是下载源码来安装的，理论上用 pip3 install pyproj 也行，但是因为源程序的服务器在境外，经常性的出现访问超时现象。</p>
<ul>
<li>如果 geppandas 没有安装，也要安装：</li>
</ul>
<pre><code class="bash language-bash">pip3 install geopandas
</code></pre>
<ul>
<li>最后安装 plotnine：</li>
</ul>
<pre><code class="bash language-bash">pip3 install 'plotnine[all]'
</code></pre>
<p>经历以上过程之后，如果还没有安装好，就只能 Google 了。</p>
<p>完成了坑爹的过程之后，plotnine 安装完毕。</p>
<h3 id="plotly">Plotly</h3>
<p>Plotly 是一款能够实现基于网页作图的工具软件，其底层是 plotly.js，基于 D3.js、stack.gl 和 SVG，因此能够实现用 JavaScript 在网页上绘制类似于 Matplotlib 的各种统计图形。</p>
<p>官方网站：<a href="https://plot.ly/">https://plot.ly/</a></p>
<p>Plotly 原本是收费的软件，但自 2016 年 6 月开始，提供免费的社区版。</p>
<p>它能够实现在线发布制图结果，为了实现这个目的，还需要到该网站进行注册。</p>
<p>注册完毕，登录网站，并在界面的右上角用户名的下拉菜单中选择“setting”项目，再从左侧栏选择“API Keys”，设置 Username 和 API KEY，记录下来，以备后用。</p>
<p>安装方法：pip3 install plotly</p>
<h3 id="pyecharts">Pyecharts</h3>
<p>Pyecharts 是国产的可视化工具包。</p>
<p>官方网站：<a href="http://pyecharts.org/">http://pyecharts.org/</a></p>
<blockquote>
  <p>难得有中文文档。</p>
</blockquote>
<p>为了获得更好的效果，先安装如下依赖：</p>
<ul>
<li>安装 Nodejs 环境，<a href="https://nodejs.org/en/download/">请点击这里下载</a></li>
<li>安装 phantomjs</li>
</ul>
<pre><code class="bash language-bash">$ sudo npm install -g phantomjs-prebuilt --upgrade --unsafe-perm
</code></pre>
<p>而后，使用下述方式安装：</p>
<pre><code class="bash language-bash">pip3 install pyecharts
</code></pre>
<p>在后续操作中，还要用到其他的模块，比如主题模块，可以参考官方文档进行安装。因为是中文的，而且文档内容非常详细，相信读者一看便知。</p>
<h3 id="bokeh">Bokeh</h3>
<p>Bokeh 也是当前使用量日益提升的制图工具，它的核心特点在于能够基于服务器发布各种具有强交互性的图示。</p>
<p>官方网站：<a href="https://bokeh.pydata.org/en/latest/">https://bokeh.pydata.org/en/latest/</a></p>
<p>安装方法：</p>
<pre><code class="bash language-bash">pip3 install bokeh
</code></pre>
<p>经过上面的一系列折腾，应该已经把自己的计算机开发环境配置好了。</p>
<p>不过，要说明的是，本达人课所介绍的几种可视化工具，仅仅是我选择的，其实还有很多可视化工具没有纳入到本达人课的范畴。我相信，读者学习这几种各具特色的工具之后，可以非常快速地掌握任何一种新的工具。</p>
<h3 id="-4">总结</h3>
<p>本课主要是为后续的正式学习做好准备，特别是开发环境的配置。在 Python 生态环境中做开发，难免还要安装其他各类包和模块。</p>
<ul>
<li>通常使用 pip 即可，并且会自动安装有关依赖。</li>
<li>如果出现“访问超时”这类问题时，可能是网络不太好，解决方法有两个：一是换一个速度更快的网络环境；二是找个“梯子”（自备，不要询问我哦）或许就解决问题了。</li>
<li>下载相应模块的代码（通常官方网站或者 github.com 上都有）直接安装（比如执行：python3 install setup.py）。</li>
<li>还有一个重要的解决问题途径，就是使用 Google 找一找其他人是怎么解决的，参考一下。</li>
</ul></div></article>