---
title: Linux GDB 调试指南-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课将介绍 Redis 项目在 Linux 系统中使用 gdb 去调试，这里的调试环境是 CentOS 7.0，但是通常情况下对于 C/C++ 项目我一般习惯使用 <strong>Visual Studio</strong> 去做项目管理，Visual Studio 提供了强大的 C/C++ 项目开发和管理能力。这里介绍一下如何将这种开源项目整体添加到 Visual Studio 的解决方案中去。</p>
<p>（1）启动 Visual Studio 新建一个空的 Win32 控制台程序（工程建好后，关闭该工程防止接下来的步骤中文件占用导致的无法移动）。</p>
<p><img src="https://images.gitbook.cn/e7440e00-1809-11e9-9353-979032778e1a" width = "75%" /></p>
<p>（2）这样会在 redis 源码目录下会根据设置的名称生成一个文件夹（这里是 redis-4.0.1），将该文件夹中所有文件复制到 redis 源码根目录，然后删掉生成的这个文件夹。</p>
<p><img src="https://images.gitbook.cn/85a7ff70-180a-11e9-9a16-dfdfa8850682" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/d3e376b0-180a-11e9-9353-979032778e1a" width = "65%" /></p>
<p>（3）再次用 Visual Studio 打开 redis-4.0.1.sln 文件，然后在<strong>解决方案资源管理器</strong>视图中点击<strong>显示所有文件</strong>按钮并保持该按钮选中（如果找不到<strong>解决方案资源管理器</strong>视图，可以在<strong>“视图”</strong>菜单中打开，快捷键为 Ctrl + Alt + L）。</p>
<p><img src="https://images.gitbook.cn/0712f2e0-180b-11e9-9a16-dfdfa8850682" width = "45%" /></p>
<p>（4）然后选中所有需要添加到解决方案中的文件，右键选择菜单<strong>“包括在项目中”</strong>即可，如果文件比较多，Visual Studio 可能需要一会儿才能完成，为了减少等待时间，读者也可以一批一批的添加。</p>
<p><img src="https://images.gitbook.cn/e372cfd0-180b-11e9-8302-0d1daa9ceb5b" width = "40%" /></p>
<p>（5）接着选择<strong>“文件”</strong>菜单<strong>“全部保存”</strong>菜单项保存即可（快捷键 <strong>Ctrl + Shift + S</strong> ）。</p>
<p>最终效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/2a9a24d0-180c-11e9-9353-979032778e1a" width = "40%" /></p>
<p>这样我们就能利用 Visual Studio 强大的功能管理和阅读源码了。</p>
<blockquote>
  <p>这里要提醒一下读者：<strong>C/C++ 开源项目中一般会使用各种宏去条件编译一些代码，实际生成的二进制文件中不一定包含这些代码，因此在 Visual Studio 中看到某段代码的行号与实际在 gdb 中调试的代码行号不一定相同，在给某一行代码设置断点时请以 gdb 中 list 命令看到的代码行号为准</strong>。</p>
</blockquote></div></article>