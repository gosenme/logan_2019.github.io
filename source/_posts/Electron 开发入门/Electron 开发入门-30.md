---
title: Electron 开发入门-30
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在 2019 年 1 月 5 日，Electron 最新的 4.0.1 版发布了，尽管在写作本系列课程内容时，Electron 4.0 稳定版还没有发布，不过经过测试，本课程中的例子在 Electron 4.0 中仍然可以正常使用。Electron 4.0 及以上版本只是修正了一些 bug，同时还加了一些功能（主要增加了事件、一些方法），大的功能并没有增加什么。</p>
<p><img src="https://images.gitbook.cn/FhcdSyh54S_XjHCzpfpj-V_P41CJ" alt="avatar" /></p>
<p>如果希望升级到 Electron 4.0 或更高版本，可以按下面的方式去做。</p>
<p>如果机器上已经安装了 Electron 3.x 或更低版本，不要直接使用下面的代码升级。</p>
<pre><code>npm update electron -g
</code></pre>
<p>例如，机器上安装了 Electron 3.0.1，使用上面的命令只能升级到 Electron 3.1.0，跨大版本的升级，如从 2 升级到 3，或从 3 升级到 4，需要先使用下面的命令卸载 Electron。</p>
<pre><code>npm uninstall electron -g
</code></pre>
<p>然后使用下面的命令重新安装 Electron。</p>
<pre><code>npm install electron -g
</code></pre>
<p>安装完后，输入 electron --version 命令，如果输出 v4.0.1，说明已经安装成功，Good Luck。</p></div></article>