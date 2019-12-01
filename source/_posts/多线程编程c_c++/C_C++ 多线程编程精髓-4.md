---
title: C_C++ 多线程编程精髓-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在实际开发中，有时候由于我们的程序逻辑不当问题，会导致某个线程<strong>空转</strong>（如无限空循环），进而引起该进程占用 CPU 使用率过高。这不仅会造成我们的系统卡顿，也是对 CPU 资源的一种浪费。那如何定位和排查引起 CPU 使用率过高的线程呢？</p>
<p>在 Linux 下我们可以综合使用 pstack 和 top 命令来排查此类问题。我们先来介绍一下 <strong>pstack</strong> 命令的使用方法。</p>
<h3 id="pstack">pstack 命令</h3>
<p>Linux 系统中可以通过 <strong>pstack</strong> 来命令查看一个进程的线程数量和每个线程的调用堆栈情况。</p>
<pre><code>pstack pid
</code></pre>
<p><strong>pid</strong> 设置为要查看的进程的 id 即可。</p>
<blockquote>
  <p>pstack 命令是 gdb 调试器提供的，如果读者在实际使用时提示找到该命令，可以安装一下 gdb 即可。</p>
</blockquote>
<p>以我机器上 nginx 的 worker 进程为例，首先使用 <strong>ps</strong> 命令查看下 nginx 进程 id，然后使用 <strong>pstack</strong> 命令即可查看该进程每个线程的调用堆栈（我这里演示的 nginx 只有一个线程，如果有多个线程，会显示每个线程的调用堆栈）：</p>
<pre><code>[root@iZ238vnojlyZ ~]# ps -ef | grep nginx
root      2150     1  0 May22 ?        00:00:00 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
nginx     2151  2150  0 May22 ?        00:00:07 nginx: worker process
root     16621 16541  0 18:53 pts/0    00:00:00 grep --color=auto nginx
[root@iZ238vnojlyZ ~]# pstack 2151
#0  0x00007f70a61ca2a3 in __epoll_wait_nocancel () from /lib64/libc.so.6
#1  0x0000000000437313 in ngx_epoll_process_events ()
#2  0x000000000042efc3 in ngx_process_events_and_timers ()
#3  0x0000000000435681 in ngx_worker_process_cycle ()
#4  0x0000000000434104 in ngx_spawn_process ()
#5  0x0000000000435854 in ngx_start_worker_processes ()
#6  0x000000000043631b in ngx_master_process_cycle ()
#7  0x0000000000412229 in main ()
</code></pre>
<p>上述输出即使用 pstack 命令查看进程 2151 的各个线程调用堆栈。</p>
<blockquote>
  <p>注意：<strong>pstack</strong> 命令查看的程序必须携带调试符号，且你所使用的用户必须具有相应的查看权限。</p>
</blockquote>
<h3 id="linuxcpu">如何排查 Linux 进程 CPU 使用率过高问题</h3>
<p>在了解了 pstack 命令的用法之后，我们来看一个具体的例子。</p>
<p>使用 top 命令发现机器上有一个叫 qmarket 的进程 CPU 使用率非常高，如下图所示：</p>
<p><img src="https://images.gitbook.cn/ed523b60-ce47-11e9-bb7f-bd5875ea71a6" alt="enter image description here" /></p>
<p>上图中进程 ID 为 <strong>4427</strong> 的 qmarket 进程占用 CPU 使用率达到 <strong>22.8%</strong>。我们使用 <strong>top -H</strong> 命令再次输出下系统的“进程”列表。</p>
<blockquote>
  <p>top 命令的 -H 选项的作用是显示每个一个进程的各个线程运行状态（线程模式）。</p>
</blockquote>
<p>我们来看下执行结果：</p>
<p><img src="https://images.gitbook.cn/3b402ee0-ce48-11e9-bdf7-7924fedc9f4e" alt="enter image description here" /></p>
<p>如上图所示，top 命令第一栏虽然输出还叫 PID，但此时显示的实际是每个线程的线程 ID。可以发现 qmarket 程序的线程号为 <strong>4429</strong>、<strong>4430</strong>、<strong>4431</strong>、<strong>4432</strong>、<strong>4433</strong>、<strong>4434</strong>、<strong>4445</strong> 这几个线程占用 CPU 使用率较高。那么这几个线程到底做了什么导致 CPU 使用率高呢？我们使用 <strong>pstack 4427</strong> 来看一下这几个线程（<strong>4427</strong> 是 qmarket 的进程 ID）。</p>
<pre><code>[root@js-dev2 ~]# pstack 4427
Thread 9 (Thread 0x7f315cb39700 (LWP 4428)):
#0  0x00007f315db3d965 in pthread_cond_wait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0
#1  0x00007f315d8dc82c in std::condition_variable::wait(std::unique_lock&lt;std::mutex&gt;&amp;) () from /lib64/libstdc++.so.6
#2  0x0000000000467a89 in CAsyncLog::WriteThreadProc () at ../../sourcebase/utility/AsyncLog.cpp:300
#3  0x0000000000469a0f in std::_Bind_simple&lt;void (*())()&gt;::_M_invoke&lt;&gt;(std::_Index_tuple&lt;&gt;) (this=0xddeb60) at /usr/include/c++/4.8.2/functional:1732
#4  0x0000000000469969 in std::_Bind_simple&lt;void (*())()&gt;::operator()() (this=0xddeb60) at /usr/include/c++/4.8.2/functional:1720
#5  0x0000000000469902 in std::thread::_Impl&lt;std::_Bind_simple&lt;void (*())()&gt; &gt;::_M_run() (this=0xddeb48) at /usr/include/c++/4.8.2/thread:115
#6  0x00007f315d8e0070 in ?? () from /lib64/libstdc++.so.6
#7  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#8  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 8 (Thread 0x7f3157fff700 (LWP 4429)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7ffc5eed32e0, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7ffc5eed32e0) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7ffc5eed32e0) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 7 (Thread 0x7f31573fd700 (LWP 4430)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3150022390, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3150022390) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3150022390) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 6 (Thread 0x7f3156bfc700 (LWP 4431)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3150047890, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3150047890) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3150047890) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 5 (Thread 0x7f31563fb700 (LWP 4432)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3148041fd8, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3148041fd8) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3148041fd8) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 4 (Thread 0x7f3155bfa700 (LWP 4433)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3148052620, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3148052620) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3148052620) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 3 (Thread 0x7f31553f9700 (LWP 4434)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3148062ee0, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3148062ee0) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3148062ee0) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 2 (Thread 0x7f3154bf8700 (LWP 4445)):
#0  0x00007f315d00ae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f315d03b704 in usleep () from /lib64/libc.so.6
#2  0x000000000043ed67 in CThread::SleepMs (this=0x7f3150001b00, nMilliseconds=1000) at ../../sourcebase/event/Thread.cpp:106
#3  0x0000000000441f82 in CEventDispatcher::Run (this=0x7f3150001b00) at ../../sourcebase/event/EventDispatcher.cpp:63
#4  0x000000000043eb33 in CThread::_ThreadEntry (pParam=0x7f3150001b00) at ../../sourcebase/event/Thread.cpp:26
#5  0x00007f315db39dd5 in start_thread () from /lib64/libpthread.so.0
#6  0x00007f315d043ead in clone () from /lib64/libc.so.6
Thread 1 (Thread 0x7f315f2ca3c0 (LWP 4427)):
#0  0x00007f315db3af47 in pthread_join () from /lib64/libpthread.so.0
#1  0x000000000043edc7 in CThread::Join (this=0x7ffc5eed32e0) at ../../sourcebase/event/Thread.cpp:130
#2  0x000000000040cc61 in main (argc=1, argv=0x7ffc5eed3668) at ../../sourceapp/qmarket/qmarket.cpp:309
</code></pre>
<p>在 pstack 输出的各个线程中，只要逐一对照我们的程序源码来梳理下该线程中是否有大多数时间都处于空转的逻辑，然后修改和优化这些逻辑就可以解决 CPU 使用率过高的问题了，一般情况下，不工作的线程应尽量使用锁对象让其挂起，而不是空转，这样可以提高系统资源利用率。关于线程各种锁对象，下文中将详细介绍。</p>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a>。</p>
<h3 id="">分享交流</h3>
<p>我们为本专栏<strong>付费读者</strong>创建了微信交流群，以方便更有针对性地讨论专栏相关的问题。入群方式请添加 GitChat 小助手泰勒的微信号：GitChatty5（或扫描以下二维码），然后给小助手发「222」消息，即可拉你进群~</p>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" /></p></div></article>