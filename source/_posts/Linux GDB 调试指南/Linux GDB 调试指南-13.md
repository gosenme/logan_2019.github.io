---
title: Linux GDB 调试指南-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用 GDB 单步调试时，代码每执行一行才显示下一行，很多用惯了图形界面 IDE 调试的读者可能会觉得非常不方便，而 GDB TUI 可能看起来不错，但是存在经常花屏的问题，也让很多读者不胜其烦。那 Linux 下有没有既能在调试时动态显示当前调试处的文件代码，又能不花屏的工具呢？有的，这就是 CGDB。</p>
<p>CGDB 本质上是对 GDB 做了一层“包裹”，所有在 GDB 中可以使用的命令，在 CGDB 中也可以使用。</p>
<h3 id="cgdb">CGDB 的安装</h3>
<p>CGDB 的官网<a href="http://cgdb.github.io/">请点击这里查看</a>，执行以下命令将 CGDB 压缩包下载到本地：</p>
<pre><code>wget https://cgdb.me/files/cgdb-0.7.0.tar.gz
</code></pre>
<p>然后执行以下步骤解压、编译、安装：</p>
<pre><code>tar xvfz cgdb-0.7.0.tar.gz
cd cgdb-0.7.0
./configure 
make
make install
</code></pre>
<p>CGDB 在编译过程中会依赖一些第三方库，如果这些库系统上不存在就会报错，安装一下就可以了。常见的错误及解决方案如下（这里以 CentOS 系统为例，使用的是 yum 安装方式，其他 Linux 版本都有对应的安装软件命令，请自行查找）。</p>
<p>（1）出现错误：</p>
<pre><code>configure: error: CGDB requires curses.h or ncurses/curses.h to build.
</code></pre>
<p>解决方案：</p>
<pre><code>yum install ncurses-devel
</code></pre>
<p>（2）出现错误：</p>
<pre><code>configure: error: Please install makeinfo before installing
</code></pre>
<p>解决方案：</p>
<pre><code>yum install install texinfo
</code></pre>
<p>（3）出现错误：</p>
<pre><code>configure: error: Please install help2man
</code></pre>
<p>解决方案：</p>
<pre><code>yum install help2man
</code></pre>
<p>（4）出现错误：</p>
<pre><code>configure: error: CGDB requires GNU readline 5.1 or greater to link.
If you used --with-readline instead of using the system readline library,
make sure to set the correct readline library on the linker search path
via LD_LIBRARY_PATH or some other facility.
</code></pre>
<p>解决方案：</p>
<pre><code>yum install readline-devel
</code></pre>
<p>（5）出现错误：</p>
<pre><code>configure: error: Please install flex before installing
</code></pre>
<p>解决方案：</p>
<pre><code>yum install flex
</code></pre>
<h3 id="cgdb-1">CGDB 的使用</h3>
<p>安装成功以后，就可以使用 CGDB 了，在命令行输入 cgdb 命令启动 CGDB ，启动后界面如下：</p>
<p><img src="https://images.gitbook.cn/7f8a9ec0-f1f6-11e8-b37f-7bcfd20d5d3a"  width = "70%" /></p>
<p>界面分为上下两部分：上部为代码窗口，显示调试过程中的代码；下部就是 GDB 原来的命令窗口。默认窗口焦点在下部的命令窗口，如果想将焦点切换到上部的代码窗口，按键盘上的 Esc 键，之后再次按字母 i 键将使焦点回到命令窗口。</p>
<blockquote>
  <p>注意：这个“焦点窗口”的概念很重要，它决定着你当前可以操作的是上部代码窗口还是命令窗口（ 和GDB TUI 一样）。</p>
</blockquote>
<p>我们用 Redis 自带的客户端程序 redis-cli 为例，输入以下命令启动调试：</p>
<pre><code>cgdb redis-cli
</code></pre>
<p>启动后的界面如下：</p>
<p><img src="https://images.gitbook.cn/9bfbcf20-f1f6-11e8-9fa2-2b61cbf641db"  width = "70%" /></p>
<p>然后加两个断点，如下图所示：</p>
<p><img src="https://images.gitbook.cn/b9032500-f1f6-11e8-b2e9-350578bd3de4"  width = "70%" /></p>
<p>如上图所示，我们在程序的 main ( 上图中第 2824 行 ）和第 2832 行分别加了一个断点，添加断点以后，代码窗口的行号将会以红色显示，另外有一个绿色箭头指向当前执行的行（ 这里由于在 main 函数上加了个断点，绿色箭头指向第一个断点位置 ）。单步调试并步入第 2827 行的 sdsnew() 函数调用中，可以看到代码视图中相应的代码也发生了变化，并且绿色箭头始终指向当前执行的行数：</p>
<p><img src="https://images.gitbook.cn/cb32e800-f1f6-11e8-b2e9-350578bd3de4"  width = "70%" /></p>
<p>更多 CGDB 的用法可以查阅官网，也可以参考 CGDB 中文手册，<a href="https://github.com/leeyiw/cgdb-manual-in-chinese/blob/master/SUMMARY.md">点击这里可查看详情</a>。</p>
<h3 id="cgdb-2">CGDB 的不足之处</h3>
<p>CGDB 虽然已经比原始的 GDB 和 GDB TUI 模式在代码显示方面改进了许多，但实际使用时，CGDB 中调用 GDB 的 print 命令无法显示字符串类型中的中文字符，要么显示乱码，要么不显示，会给程序调试带来很大的困扰，这点需要注意。</p>
<p>总的来说，CGDB 仍然能满足我们大多数场景下的调试，瑕不掩瑜， CGDB 在 Linux 系统中调试程序还是比 GDB 方便很多。</p>
<h3 id="">答疑与交流</h3>
<p>如果你在学习过程中有任何问题和想法，欢迎加入本课程的读者交流群，我会抽出时间回复。请加助手伽利略的微信号 GitChatty6（见下图微信二维码），注明 <strong>Linux GDB</strong>，谢谢，到时会拉你入群。</p>
<p><img src="https://images.gitbook.cn/FmCFWs9SvHlH97TzbNXMCR4Z2mp0"  width = "30%" /></p></div></article>