---
title: Linux GDB 调试指南-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>时下的业界，相对于传统的关系型数据库，以 key-value 思想实现的 NoSQL 内存数据库非常流行，而提到内存数据库，很多读者第一反应就是 Redis 。确实，Redis 以其高效的性能和优雅的实现成为众多内存数据库中的翘楚。</p>
<p>前面课程介绍了单个服务器的基本结构，这个课程我们再来一个实战演习，以 Redis 为例来讲解实际项目中的服务器结构是怎样的。当然，本课程介绍的角度与前面课程的思路不一样，前面是先给结论，然后再加以论证，而本课程则是假设预先不清楚 Redis 网络通信层的结构，结合 GDB 调试，以探究的方式逐步搞清楚 Redis 的网络通信模块结构。</p>
<h3 id="redis">Redis 源码下载与编译</h3>
<p>Redis 的最新源码下载地址可以在 <a href="https://redis.io/">Redis 官网</a>获得。我使用的是 CentOS 7.0 系统，使用 wget 命令将 Redis 源码文件下载下来：</p>
<pre><code>[root@localhost gdbtest]# wget http://download.redis.io/releases/redis-4.0.11.tar.gz
--2018-09-08 13:08:41--  http://download.redis.io/releases/redis-4.0.11.tar.gz
Resolving download.redis.io (download.redis.io)... 109.74.203.151
Connecting to download.redis.io (download.redis.io)|109.74.203.151|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1739656 (1.7M) [application/x-gzip]
Saving to: ‘redis-4.0.11.tar.gz’

54% [==================================================================&gt;                                                         ] 940,876     65.6KB/s  eta 9s
</code></pre>
<p>解压：</p>
<pre><code>[root@localhost gdbtest]# tar zxvf redis-4.0.11.tar.gz 
</code></pre>
<p>进入生成的 redis-4.0.11 目录使用 makefile 进行编译：</p>
<pre><code>[root@localhost gdbtest]# cd redis-4.0.11
[root@localhost redis-4.0.11]# make -j 4
</code></pre>
<p>编译成功后，会在 src 目录下生成多个可执行程序，其中 redis-server 和 redis-cli 是我们即将调试的程序。</p>
<p>进入 src 目录，使用 GDB 启动 redis-server 这个程序：</p>
<pre><code>[root@localhost src]# gdb redis-server 
Reading symbols from /root/redis-4.0.9/src/redis-server...done.
(gdb) r
Starting program: /root/redis-4.0.9/src/redis-server 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
31212:C 17 Sep 11:59:50.781 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
31212:C 17 Sep 11:59:50.781 # Redis version=4.0.9, bits=64, commit=00000000, modified=0, pid=31212, just started
31212:C 17 Sep 11:59:50.781 # Warning: no config file specified, using the default config. In order to specify a config file use /root/redis-4.0.9/src/redis-server /path/to/redis.conf
31212:M 17 Sep 11:59:50.781 * Increased maximum number of open files to 10032 (it was originally set to 1024).
[New Thread 0x7ffff07ff700 (LWP 31216)]
[New Thread 0x7fffefffe700 (LWP 31217)]
[New Thread 0x7fffef7fd700 (LWP 31218)]
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 4.0.9 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 31212
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

31212:M 17 Sep 11:59:50.793 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
31212:M 17 Sep 11:59:50.793 # Server initialized
31212:M 17 Sep 11:59:50.793 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
31212:M 17 Sep 11:59:50.794 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never &gt; /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
31212:M 17 Sep 11:59:50.794 * DB loaded from disk: 0.000 seconds
31212:M 17 Sep 11:59:50.794 * Ready to accept connections
</code></pre>
<p>以上是 redis-server 启动成功后的画面。</p>
<p>我们再开一个 session，再次进入 Redis 源码所在的 src 目录，然后使用 GDB 启动 Redis 客户端 redis-cli：</p>
<pre><code>[root@localhost src]# gdb redis-cli
Reading symbols from /root/redis-4.0.9/src/redis-cli...done.
(gdb) r
Starting program: /root/redis-4.0.9/src/redis-cli 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
127.0.0.1:6379&gt; 
</code></pre>
<p>以上是 redis-cli 启动成功后的画面。</p>
<h3 id="">通信示例</h3>
<p>本课程的学习目的是研究 Redis 的网络通信模块，为了说明问题方便，我们使用一个简单的通信实例，即通过 redis-cli 产生一个 key 为“hello”、值为“world”的 key-value 数据，然后得到 redis-server 的响应。</p>
<pre><code>127.0.0.1:6379&gt; set hello world
OK
127.0.0.1:6379&gt; 
</code></pre>
<p>读者需要注意的是，我这里说是一个“简单”的实例，其实并不简单。有两个原因：</p>
<ul>
<li>我们是在 <strong>redis-cli</strong> （Redis 客户端）输入的命令，这个命令经 <strong>redis-cli</strong> 处理后封装成网络通信包，通过客户端的网络通信模块发给 <strong>redis-server</strong>，然后 <strong>redis-server</strong> 网络通信模块收到后解析出命令，执行命令后得到结果再封装成相应的网络数据包，返回给 <strong>redis-cli</strong>。这个过程中涉及到两端的网络通信模块是我们研究和学习的重点。</li>
<li><strong>redis-server</strong> 基本的数据类型都是可以通过类似的命令产生，因此这个例子是一个典型的研究 <strong>redis</strong> 的典范。</li>
</ul>
<h3 id="-1">小结</h3>
<p>这节课介绍了我们利用调试 <strong>Redis</strong> 源码来学习 <strong>GDB</strong> 的一些准备工作和实例代码，有兴趣的读者可以根据本节课中介绍的内容准备一下学习材料，以备后面的进一步学习，从下一课开始我们正式利用 GDB 来调试 <strong>Redis</strong>。</p>
<h3 id="-2">答疑与交流</h3>
<p>如果你在学习过程中有任何问题和想法，欢迎加入本课程的读者交流群，我会抽出时间回复。请加助手伽利略的微信号 GitChatty6（见下图微信二维码），注明 <strong>Linux GDB</strong>，谢谢，到时会拉你入群。</p>
<p><img src="https://images.gitbook.cn/FmCFWs9SvHlH97TzbNXMCR4Z2mp0"  width = "30%" /></p></div></article>