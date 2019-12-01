---
title: 深度学习 PyTorch 极简入门-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本文将为大家介绍深度学习实战非常重要的两个工具：Anaconda 和 Jupyter Notebook。</p>
<h3 id="31anaconda">3.1 Anaconda</h3>
<h4 id="1anaconda">1. 为什么选择 Anaconda</h4>
<p>我们知道 Python 是人工智能的首选语言。为了更好、更方便地使用 Python 来编写深度学习相关程序，可以使用集成开发环境或集成管理系统，最流行的比如 PyCharm 和 Anaconda。本文我推荐使用 Anaconda。</p>
<p>之所以选择 Anaconda，是因为 Anaconda 作为 Python 的一个集成管理工具，它把 Python 做相关数据计算与分析所需要的包都集成在了一起，我们只需要安装 Anaconda 就行了。Anaconda 是一个打包的集合，里面包含了 120 多个数据科学相关的开源包，在数据可视化、机器学习、深度学习等多方面都有涉及。不仅可以做数据分析，甚至可以用在大数据和人工智能领域。另外，安装它后就默认安装了 Python、IPython、Jupyter Notebook 和集成开发环境 Spyder 等等。总之一句话，安装 Anaconda 让我们省去了大量下载模块包的时间，更加方便。</p>
<h4 id="2anaconda">2. 如何安装 Anaconda</h4>
<p>Anaconda 完全支持 Windows、macOS、Linux 三种平台，版本基于 Python 3.6 或者 Python 2.7，推荐下载 3.6 版本。这里给出 Anaconda 的下载地址：</p>
<blockquote>
  <p><a href="https://www.anaconda.com/download/">https://www.anaconda.com/download/</a></p>
</blockquote>
<p><img src="http://images.gitbook.cn/6c9c5270-7f52-11e8-a167-a3b450d69a42" alt="enter image description here" /></p>
<p>以 Windows 为例，根据你电脑是 32 位还是 64 位，选择 Python 3.6，下载相应的 Anaconda。下载完成之后，直接运行 exe 文件，即可完成安装，整个过程非常简单。Anaconda 安装成功之后，包含以下基本模块：</p>
<p><img src="http://images.gitbook.cn/495fd330-7f53-11e8-8f4f-398ed9d7e1c5" alt="enter image description here" /></p>
<h4 id="3python">3. 如何管理 Python 科学包</h4>
<p>Anaconda 的方便之处就在于它管理包非常方便。打开 Anaconda 的 Anaconda Prompt 模块，使用 conda 包管理器命令即可轻松实现对 Python 科学包的管理。下面介绍几个 conda 的基本命令。</p>
<p><img src="http://images.gitbook.cn/9dd77480-7f59-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<ul>
<li>显示已安装的科学包。</li>
</ul>
<p>在 Anaconda Prompt 中输入：</p>
<pre><code>conda list
</code></pre>
<ul>
<li>安装某科学包。</li>
</ul>
<p>在 Anaconda Prompt 中输入：</p>
<pre><code>conda install package_name
</code></pre>
<p>例如，要安装 pandas，则输入以下命令：</p>
<pre><code>conda install pandas
</code></pre>
<ul>
<li>更新某科学包。</li>
</ul>
<p>在 Anaconda Prompt 中输入：</p>
<pre><code>conda update package_name
</code></pre>
<ul>
<li>卸载某科学包。</li>
</ul>
<p>在 Anaconda Prompt 中输入：</p>
<pre><code>conda uninstall package_name
</code></pre>
<h3 id="32jupyternotebook">3.2  Jupyter Notebook</h3>
<p>Jupyter Notebook 是一个交互式笔记本，支持运行 40 多种编程语言。其本质是一个 Web 应用程序，便于创建和共享文学化程序文档，支持实时代码、数学方程、可视化和 Markdown。用途包括数据清理和转换，数值模拟，统计建模，机器学习等等。</p>
<p><img src="http://images.gitbook.cn/63c574c0-7f56-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>在没有 Jupyter Notebook 之前，我们只能在普通的 Python shell 或者在 IDE（集成开发环境）如 Spyder 中编写代码，然后在 Word 中写文档来说明你的项目。这个分立的过程很繁琐，通常是写完代码，再写文档的时候还要从头回敲一遍代码。但是 Jupyter Notebook 可以直接在代码块之间写出叙述性文档包括 LaTex 公式（Markdown 语法），而不需要另外编写单独的文档。也就是说它可以将代码、文档等集中到一处，增加可读性。如今，Jupyter Notebook 已迅速成为数据分析、机器学习的必备工具。因为它可以让数据分析师集中精力向用户解释整个分析过程。</p>
<p>可喜的是， Anaconda 自带了 Jupyter Notebook，不需要我们额外安装，这也是我们选择使用 Anaconda 的重要原因之一。接下来，我们将简单介绍一些 Jupyter Notebook 的基本使用方法。</p>
<h4 id="1jupyternotebook">1. 打开 Jupyter Notebook</h4>
<p>Windows 下直接在 Anaconda 的工具包中就可以直接打开 Jupyter Notebook。如果是 Linux 的话，终端输入 jupyter notebook 即可。</p>
<p><img src="http://images.gitbook.cn/a8bc9bf0-7f59-11e8-8f4f-398ed9d7e1c5" alt="enter image description here" /></p>
<p>Jupyter Notebook 的主窗口显示的路径一般是 Jupyter Notebook 所处的路径下（通常在你的用户目录下）。主界面如下所示：</p>
<p><img src="http://images.gitbook.cn/7a959e10-7f5a-11e8-a167-a3b450d69a42" alt="enter image description here" /></p>
<p>若要创建一个新的 Notebook，只需鼠标左击 New，在下拉选项中选择一个你想启动的 Notebook 类型即可，例如 Python 3。</p>
<p><img src="http://images.gitbook.cn/e87dc1a0-7f5a-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>新建之后，打开新的标签，得到了一个空的 Notebook 界面。</p>
<p><img src="http://images.gitbook.cn/48491260-7f5b-11e8-9678-111d3c638e95" alt="enter image description here" /></p>
<p>Notebook 界面由以下几个部分组成：</p>
<ul>
<li>notebook 名字；</li>
<li>主工具栏，包括保存、导出、重载、重启内核等；</li>
<li>快捷键；</li>
<li>Notebook 主要部分，Notebook 编辑区。</li>
</ul>
<p>你可以将新建的 Notebook 重命名，点击 File -&gt; Rename，然后输入新的名称即可。</p>
<h4 id="2notebook">2. Notebook 编辑区</h4>
<p>Notebook 编辑区由一个个单元（Cell）组成，每个 Cell 可以实现不同的功能。例如，第一个 Cell 如下图所示，以 In[ ] 开头表示这是一个代码单元。在代码单元里，你可以输入任何代码并执行。例如，键盘输入 1+1，然后按 “Shift+Enter”，代码将被运行，并显示结果，由 out[] 为标志。同时，切换到下一个的 Cell 中。</p>
<p><img src="http://images.gitbook.cn/82f20ce0-7f5c-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>如果代码没有返回值，例如 print 函数打印，则没有 out[] 输出。</p>
<p><img src="http://images.gitbook.cn/1afb19f0-7f5d-11e8-8f4f-398ed9d7e1c5" alt="enter image description here" /></p>
<p>Notebook 一个非常重要的特性是可以返回之前的 Cell，修改并重新运行，以此来更新整个文档。例如，现在我们回到第一个 Cell 中，将输入 1+1 改成 1+2，重新按 “Shift+Enter” 运行该单元，结果被立即更新成 3。当你想使用不同参数调试方程又不想运行整个脚本的时候，这条特性非常有用。然而，你也可以通过菜单栏 Cell -&gt; Run all 来重新运行整个 Notebook。</p>
<p>Cell 一般默认为代码单元，如果我们想新建一个 Markdown 单元，可以选择 Code -&gt; Markdown 进行切换，或直接使用快捷键 M，切换为 Markdown 单元。</p>
<p><img src="http://images.gitbook.cn/f1a8ae90-7f5d-11e8-9678-111d3c638e95" alt="enter image description here" /></p>
<p>Markdown 单元完全遵循 Markdown 语法，我们可以建立标题或者代码文档说明，这样就能让解释文本丰富起来了。</p>
<p><img src="http://images.gitbook.cn/c3f64470-7f5e-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>让我们再深入地探讨下 Markdown 单元类型，它同时也支持 HTML 代码。你可以在你的 Cell 中创建更高级的样式，比如添加图片等等。举个例子来说，如果你想在 Notebook 中添加 Jupyter 的图标，尺寸为 100x100，并且放置在 Cell 左侧，可以这样编写：</p>
<pre><code>&lt;img src="http://jupyter.org/assets/main-logo.svg"
style="width:100px;height:100px;float:left"&gt;
</code></pre>
<p>运行该单元，效果如下：</p>
<p><img src="http://images.gitbook.cn/4567dcb0-7f61-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>你还可以直接调用本地图片，须保证图片所在路径的准确性。例如：</p>
<pre><code>![](img/../14.png)
</code></pre>
<p>运行该单元，同样得到 Jupyter 的图标：</p>
<p><img src="http://images.gitbook.cn/d01b13a0-7f65-11e8-9678-111d3c638e95" alt="enter image description here" /></p>
<p>除此之外，Notebook 的 Markdown 还支持 LaTex 语法。你可以在 Markdown 单元中按照 LaTex 语法规则写方程式，然后直接运行，就可以看到结果。例如运行下面方程式：</p>
<pre><code>$$\frac{\partial J}{\partial w}=1$$
</code></pre>
<p>运行结果如下：</p>
<p><img src="http://images.gitbook.cn/f241c0a0-7f65-11e8-8f4f-398ed9d7e1c5" alt="enter image description here" /></p>
<h4 id="3">3. 导出功能</h4>
<p>Notebook 另一个强大的功能就是导出功能，如以下多种形式：</p>
<ul>
<li>HTML</li>
<li>Markdown</li>
<li>ReST</li>
<li>PDF ( Through LaTex )</li>
<li>Raw Python</li>
</ul>
<p>如果导出成 PDF 格式，你甚至可以不使用 LaTex 就创建了一个漂亮的文档。或者，你可以将你的 Notebook 保存为 HTML 格式，发布到个人网站上。你还可以导出成 ReST 格式，作为软件库的文档。</p>
<p>导出方式很简单，选择 File -&gt; Download as -&gt; …… 即可，如下所示：</p>
<p><img src="http://images.gitbook.cn/fcdb43a0-7f66-11e8-9678-111d3c638e95" alt="enter image description here" /></p>
<p>值得一提的是，直接转换为 PDF 格式经常会出现下列错误：</p>
<p><img src="http://images.gitbook.cn/4b270e90-7f67-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>该错误提示没有安装 xelatex。所以，我们需要提前安装 xelatex，方法是安装 TexLive 套装。</p>
<p>Windows 下，从官网下载安装程序：install-tl-windows.exe，直接选择 full 方式安装。如果机器上已经安装了 MiKTex，则先卸载，否则 TexLive 安装后功能不可用。</p>
<blockquote>
  <p>官网下载 install-tl-windows.exe：</p>
  <p><a href="http://www.ctex.org/TeXLive">http://www.ctex.org/TeXLive</a></p>
</blockquote>
<p>Ubuntu 下，直接输入以下命令：</p>
<pre><code>sudo apt-get install texlive-full
</code></pre>
<h4 id="4matplotlib">4. Matplotlib 集成</h4>
<p>Matplotlib 是用来画图的 Python 库，与 Jupyter Notebook 结合使用时效果更好。为了在 Jupyter notebook 中使用 Matplotlib，你需要告诉 Jupyter 获取所有 Matplotlib 生成的图形，并把它们全部嵌入到 Notebook 中。为此，只需输入以下命令：</p>
<pre><code>%matplotlib inline
</code></pre>
<p>这条语句执行可能耗费几秒钟，但是只需要你打开 Notebook 时执行一次就好。让我们作个图，看看是怎么集成的：</p>
<pre><code>import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(10, 0.1)
y = x**2

plt.plot(x, y)
plt.show()
</code></pre>
<p>这段简单代码将绘出 y=x^2y=x2 对应的二次曲线。运行这个 Cell，结果如下所示：</p>
<p><img src="http://images.gitbook.cn/94f46b60-7f69-11e8-a88c-dd6ae79624fa" alt="enter image description here" /></p>
<p>很明显，图直接嵌入到 Notebook 中，位于代码下面。修改代码，重新运行，图形将自动同步更新。这是一个很好的特性，这样可以清楚知道每段代码究竟干了什么。</p>
<h3 id="33">3.3 总结</h3>
<p>本文主要介绍了 Anaconda 和 Jupyter Notebook。Anaconda 作为 Python 的一个集成管理工具，它把 Python 相关数据计算与分析科学包都集成在了一起，省去了各个安装的麻烦，非常方便。而且，Anaconda 自带了 Jupyter Notebook，Jupyter Notebook 是一个非常强大的工具，允许使用者为数据分析、教育、文件等任何你可以想到的内容创建漂亮的交互式文档，已迅速成为数据分析、机器学习、深度学习的必备工具。本达人课的实战代码都将在 Jupyter Notebook 上实现。</p></div></article>