---
title: Linux GDB 调试指南-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在某些场景下，我们需要根据自己的程序情况，制定一些可以在调试时输出程序特定信息的命令，这在 GDB 中很容易做到，只要在 Linux 当前用户家（home）目录下，如 root 用户是 “<strong>/root</strong>” 目录，非 root 用户则对应 “<strong>/home/ 用户名</strong>”目录。</p>
<p>在上述目录中自定义一个名叫 <strong>.gdbinit</strong> 文件，在 Linux 系统中以点号开头的文件名一般都是隐藏文件，因此 <strong>.gdbinit</strong> 也是一个隐藏文件，可以使用 <strong>ls -a</strong> 命令查看（<strong>a</strong> 的含义是 <strong>all</strong> 的意思，即显示所有文件，当然也就包括显示隐藏文件）；如果不存在，使用 <strong>vim</strong> 或者 <strong>touch</strong> 命令创建一个就可以，然后在这个文件中写上你自定义命令的 shell 脚本即可。</p>
<p>以 Apache Web 服务器的源码为例（<a href="http://httpd.apache.org/">Apache Server 的源码下载地址请点击这里</a>），在源码根目录下有个文件叫 .gdbinit，这个就是 Apache Server 自定义的 GDB 命令：</p>
<pre><code># gdb macros which may be useful for folks using gdb to debug
# apache.  Delete it if it bothers you.

define dump_table
    set $t = (apr_table_entry_t *)((apr_array_header_t *)$arg0)-&gt;elts
    set $n = ((apr_array_header_t *)$arg0)-&gt;nelts
    set $i = 0
    while $i &lt; $n
    if $t[$i].val == (void *)0L
       printf "[%u] '%s'=&gt;NULL\n", $i, $t[$i].key
    else
       printf "[%u] '%s'='%s' [%p]\n", $i, $t[$i].key, $t[$i].val, $t[$i].val
    end
    set $i = $i + 1
    end
end

# 省略部分代码

# Set sane defaults for common signals:
handle SIGPIPE noprint pass nostop
handle SIGUSR1 print pass nostop
</code></pre>
<p>当然在这个文件的最底部，Apache 设置了让 GDB 调试器不要处理 SIGPIPE 和 SIGUSR1 这两个信号，而是将这两个信号直接传递给被调试的程序本身（即 Apache Server）。</p>
<h3 id="">答疑与交流</h3>
<p>如果你在学习过程中有任何问题和想法，欢迎加入本课程的读者交流群，我会抽出时间回复。请加助手伽利略的微信号 GitChatty6（见下图微信二维码），注明 <strong>Linux GDB</strong>，谢谢，到时会拉你入群。</p>
<p><img src="https://images.gitbook.cn/FmCFWs9SvHlH97TzbNXMCR4Z2mp0"  width = "30%" /></p></div></article>