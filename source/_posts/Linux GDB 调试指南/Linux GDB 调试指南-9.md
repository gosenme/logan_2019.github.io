---
title: Linux GDB 调试指南-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课的核心内容：</p>
<ul>
<li>将 print 打印结果显示完整</li>
<li>让被 GDB 调试的程序接收信号</li>
<li>函数明明存在，添加断点时却无效</li>
</ul>
<h3 id="print">将 print 打印结果显示完整</h3>
<p>当使用 print 命令打印一个字符串或者字符数组时，如果该字符串太长，print 命令默认显示不全的，我们可以通过在 GDB 中输入 set print element 0 命令设置一下，这样再次使用 print 命令就能完整地显示该变量的所有字符串了。</p>
<pre><code>void ChatSession::OnGetFriendListResponse(const std::shared_ptr&lt;TcpConnection&gt;&amp; conn)
{
    std::string friendlist;
    MakeUpFriendListInfo(friendlist, conn);
    std::ostringstream os;
    os &lt;&lt; "{\"code\": 0, \"msg\": \"ok\", \"userinfo\":" &lt;&lt; friendlist &lt;&lt; "}";
    Send(msg_type_getofriendlist, m_seq, os.str());

    LOG_INFO &lt;&lt; "Response to client: userid=" &lt;&lt; m_userinfo.userid &lt;&lt; ", cmd=msg_type_getofriendlist, data=" &lt;&lt; os.str();    
}
</code></pre>
<p>以上代码中，当第一次打印 friendlist 这个变量值时，只能显示部分字符串。使用 set print element 0 设置以后就能完整地显示出来了。</p>
<pre><code>(gdb) n
563         os &lt;&lt; "{\"code\": 0, \"msg\": \"ok\", \"userinfo\":" &lt;&lt; friendlist &lt;&lt; "}";
(gdb) p friendlist
$1 = "[{\"members\":[{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"\",\"facetype\":2,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"bj_man\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":4,"...
(gdb) set print element 0
(gdb) p friendlist       
$2 = "[{\"members\":[{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"\",\"facetype\":2,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"bj_man\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":4,\"username\":\"13811411052\"},{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"\",\"facetype\":0,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"Half\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":5,\"username\":\"15618326596\"},{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"\",\"facetype\":34,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"云淡风轻\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":7,\"username\":\"china001\"},{\"address\":\"上海市浦东新区南泉路1200号409室\",\"birthday\":20170914,\"clienttype\":0,\"customface\":\"\",\"facetype\":5,\"gender\":0,\"mail\":\"balloonwj@qq.com\",\"markname\":\"\",\"nickname\":\"qqq123\",\"phonenumber\":\"\",\"signature\":\"{“id”：12}\",\"status\":0,\"userid\":10,\"username\":\"qqq\"},{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"be19574dcdd11fb9a96cf00f7e5f0e66\",\"facetype\":0,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"TzdnerC\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":15,\"username\":\"TzdnerC\"},{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0,\"customface\":\"\",\"facetype\":0,\"gender\":0,\"mail\":\"\",\"markname\":\"\",\"nickname\":\"Barry\",\"phonenumber\":\"\",\"signature\":\"\",\"status\":0,\"userid\":16,\"username\":\"17091203068\"},{\"address\":\"\",\"birthday\":19900101,\"clienttype\":0...太长了，这里省略...
</code></pre>
<h3 id="gdb">让被 GDB 调试的程序接收信号</h3>
<p>请看下面的代码：</p>
<pre><code>void prog_exit(int signo)
{
    std::cout &lt;&lt; "program recv signal [" &lt;&lt; signo &lt;&lt; "] to exit." &lt;&lt; std::endl;
}

int main(int argc, char* argv[])
{
    //设置信号处理
    signal(SIGCHLD, SIG_DFL);
    signal(SIGPIPE, SIG_IGN);
    signal(SIGINT, prog_exit);
    signal(SIGTERM, prog_exit);

    int ch;
    bool bdaemon = false;
    while ((ch = getopt(argc, argv, "d")) != -1)
    {
        switch (ch)
        {
        case 'd':
            bdaemon = true;
            break;
        }
    }

    if (bdaemon)
        daemon_run();

    //省略无关代码...
 }
</code></pre>
<p>在这个程序中，我们接收到 Ctrl + C 信号（对应信号 SIGINT）时会简单打印一行信息，而当用 GDB 调试这个程序时，由于 Ctrl + C 默认会被 GDB 接收到（让调试器中断下来），导致无法模拟程序接收这一信号。解决这个问题有两种方式：</p>
<ul>
<li>在 GDB 中使用 signal 函数手动给程序发送信号，这里就是 signal SIGINT；</li>
<li>改变 GDB 信号处理的设置，通过 handle SIGINT nostop print 告诉 GDB 在接收到 SIGINT 时不要停止，并把该信号传递给调试目标程序 。</li>
</ul>
<pre><code>(gdb) handle SIGINT nostop print pass
SIGINT is used by the debugger. 
Are you sure you want to change it? (y or n) y  

Signal Stop Print Pass to program Description  
SIGINT No Yes Yes Interrupt
(gdb)  
</code></pre>
<h3 id="">函数明明存在，添加断点时却无效</h3>
<p>有时候一个函数明明存在，并且我们的程序也存在调试符号，使用 break functionName 添加断点时 GDB 却提示：</p>
<pre><code>Make breakpoint pending on future shared library load? y/n
</code></pre>
<p>即使输入 y 命令，添加的断点可能也不会被正确地触发，此时需要改变添加断点的方式，使用该函数所在的代码文件和行号添加断点就能达到效果。</p>
<h3 id="-1">答疑与交流</h3>
<p>如果你在学习过程中有任何问题和想法，欢迎加入本课程的读者交流群，我会抽出时间回复。请加助手伽利略的微信号 GitChatty6（见下图微信二维码），注明 <strong>Linux GDB</strong>，谢谢，到时会拉你入群。</p>
<p><img src="https://images.gitbook.cn/FmCFWs9SvHlH97TzbNXMCR4Z2mp0"  width = "30%" /></p></div></article>