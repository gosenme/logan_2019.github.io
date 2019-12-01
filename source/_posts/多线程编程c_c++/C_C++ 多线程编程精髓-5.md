---
title: C_C++ 多线程编程精髓-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面介绍了如何创建一个线程，本讲我们来介绍一下线程 ID 的内容，线程 ID 一般是用于标识一个线程的整形数值。</p>
<h3 id="id">线程 ID</h3>
<p>一个线程创建成功以后，我们可以拿到一个线程 ID。我们可以使用线程 ID 来标识和区分线程，例如在日志文件中，把打印日志的所在的线程 ID 也一起打印出来，我们通过线程 ID 来确定日志内容是不是属于同一个线程上下文。创建线程时，上文也介绍了可以通过 <strong>pthread_create</strong> 函数的第一个参数 <strong>thread</strong> （linux平台）和 <strong>CreateThread</strong> 函数的最后一个参数 <strong>lpThreadId</strong> （Windows平台）得到线程的 ID。大多数时候，我们需要在当前调用线程中获取当前线程的 ID，在 Linux 平台上可以使用 <strong>pthread_self</strong> 函数（还有另外两种方式，下问介绍），在 Windows 平台上可以使用 <strong>GetCurrentThreadID</strong> 函数获取，这两个函数的签名分别如下：</p>
<pre><code>pthread_t pthread_self(void);

DWORD GetCurrentThreadId();
</code></pre>
<p>这两个函数比较简单，这里就不介绍了，无论是 <strong>pthread_t</strong> 还是 <strong>DWORD</strong> 类型，都是一个 32 位无符号整型值。</p>
<p>Windows 操作系统中可以在任务管理器中查看某个进程的线程数量：</p>
<p><img src="https://images.gitbook.cn/07273ce0-ce23-11e9-8bf7-f7666cc59bcf" alt="enter image description here" /></p>
<p>上图中标红的一栏即每个进程的线程数量，例如对于 vmware-tray.exe 进程一共有三个进程。如果读者打开任务管理器没有看到<strong>线程数</strong>这一列，可以点击任务管理器的【<strong>查看</strong>】- 【<strong>选择列</strong>】菜单，在弹出的对话框中勾选<strong>线程数</strong>即可显示出<strong>线程数</strong>这一列。</p>
<h3 id="linuxid">Linux 系统线程 ID 的本质</h3>
<p>Linux 系统中有三种方式可以获取一个线程的 ID。</p>
<p><strong>方法一</strong></p>
<p>调用 <strong>pthread_create</strong> 函数时，第一个参数在函数调用成功后可以得到线程 ID：</p>
<pre><code>#include &lt;pthread.h&gt;

pthread_t tid;
pthread_create(&amp;tid, NULL, thread_proc, NULL);
</code></pre>
<p><strong>pthread_create</strong> 函数我们在前面篇幅中已经介绍过了。</p>
<p><strong>方法二</strong></p>
<p>在需要获取 ID 的线程中调用 <strong>pthread_self()</strong> 函数获取。</p>
<pre><code>#include &lt;pthread.h&gt;

pthread_t tid = pthread_self();
</code></pre>
<p><strong>方法三</strong> </p>
<p>通过系统调用获取线程 ID</p>
<pre><code>#include &lt;sys/syscall.h&gt;
#include &lt;unistd.h&gt;

int tid = syscall(SYS_gettid);
</code></pre>
<p><strong>方法一</strong>和<strong>方法二</strong>获取的线程 ID 结果是一样的，这是一个 <strong>pthread_t</strong>，输出时本质上是一块内存空间地址，示意图如下：</p>
<p><img src="https://images.gitbook.cn/6307bf10-ce48-11e9-bdf7-7924fedc9f4e" alt="enter image description here" /></p>
<p>由于不同的进程可能有同样地址的内存块，因此<strong>方法一</strong>和<strong>方法二</strong>获取的线程 ID 可能不是全系统唯一的，一般是一个很大的数字（内存地址）。而<strong>方法三</strong>获取的线程 ID 是系统范围内全局唯一的，一般是一个不会太大的整数，这个数字也是就是所谓的 LWP （Light Weight Process，轻量级进程，早期的 Linux 系统的线程是通过进程来实现的，这种线程被称为轻量级线程）的 ID。</p>
<p>我们来看一段具体的代码：</p>
<pre><code>#include &lt;sys/syscall.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;
#include &lt;pthread.h&gt;

void* thread_proc(void* arg)
{
    pthread_t* tid1 = (pthread_t*)arg;
    int tid2 = syscall(SYS_gettid);
    pthread_t tid3 = pthread_self();

    while(true)
    {
        printf("tid1: %ld, tid2: %ld, tid3: %ld\n", *tid1, tid2, tid3);
        sleep(1);
    }

}

int main()
{    
    pthread_t tid;
    pthread_create(&amp;tid, NULL, thread_proc, &amp;tid);

    pthread_join(tid, NULL);

    return 0;
}
</code></pre>
<p>上述代码在新开的线程中使用上面介绍的三种方式获取线程 ID，并打印出来，输出结果如下：</p>
<pre><code>tid1: 140185007511296, tid2: 60837, tid3: 140185007511296
</code></pre>
<p><strong>tid2</strong> 即 LWP 的 ID，而 <strong>tid1</strong> 和 <strong>tid3</strong> 是一个内存地址，转换成 16 进制即：</p>
<pre><code>0x7F7F5D935700
</code></pre>
<p>这与我们用 pstack 命令看到的线程 ID 是一样的：</p>
<pre><code>[root@localhost ~]# ps -efL | grep linuxtid
root     60712 60363 60712  0    2 13:25 pts/1    00:00:00 ./linuxtid
root     60712 60363 60713  0    2 13:25 pts/1    00:00:00 ./linuxtid
root     60720 60364 60720  0    1 13:25 pts/3    00:00:00 grep --color=auto linuxtid
[root@localhost ~]# pstack 60712
Thread 2 (Thread 0x7fd897a50700 (LWP 60713)):
#0  0x00007fd897b15e2d in nanosleep () from /lib64/libc.so.6
#1  0x00007fd897b15cc4 in sleep () from /lib64/libc.so.6
#2  0x0000000000400746 in thread_proc (arg=0x7fff390921c8) at linuxtid.cpp:15
#3  0x00007fd898644dd5 in start_thread () from /lib64/libpthread.so.0
#4  0x00007fd897b4eead in clone () from /lib64/libc.so.6
Thread 1 (Thread 0x7fd898a6e740 (LWP 60712)):
#0  0x00007fd898645f47 in pthread_join () from /lib64/libpthread.so.0
#1  0x000000000040077e in main () at linuxtid.cpp:25
[root@localhost ~]# ps -ef | grep linuxtid
root     60838 60363  0 14:27 pts/1    00:00:00 ./linuxtid
root     60846 60364  0 14:28 pts/3    00:00:00 grep --color=auto linuxtid
[root@localhost ~]# pstack 60838
Thread 2 (Thread 0x7f7f5d935700 (LWP 60839)):
#0  0x00007f7f5d9fae2d in nanosleep () from /lib64/libc.so.6
#1  0x00007f7f5d9facc4 in sleep () from /lib64/libc.so.6
#2  0x0000000000400746 in thread_proc (arg=0x7fff0523ae68) at linuxtid.cpp:15
#3  0x00007f7f5e529dd5 in start_thread () from /lib64/libpthread.so.0
#4  0x00007f7f5da33ead in clone () from /lib64/libc.so.6
Thread 1 (Thread 0x7f7f5e953740 (LWP 60838)):
#0  0x00007f7f5e52af47 in pthread_join () from /lib64/libpthread.so.0
#1  0x000000000040077e in main () at linuxtid.cpp:25
</code></pre>
<h3 id="c11id">C++11 的获取当前线程 ID 的方法</h3>
<p>C++11 的线程库可以使用 <strong>std::this_thread</strong> 类的 <strong>get_id</strong> 获取当前线程的 id，这是一个类静态方法。</p>
<p>当然也可以使用 <strong>std::thread</strong> 的 <strong>get_id</strong> 获取指定线程的 ID，这是一个类实例方法。</p>
<p>但是 <strong>get_id</strong> 方法返回的是一个包装类型的 <strong>std::thread::id</strong> 对象，不可以直接强转成整型，也没有提供任何转换成整型的接口。因此，我们一般使用 <strong>std::cout</strong> 这样的输出流来输出，或者先转换为 <strong>std::ostringstream</strong> 对象，再转换成字符串类型，然后把字符串类型转换成我们需要的整型。这一点，个人觉得算是 C++11 线程库获取线程 ID 一个不太方便的地方。</p>
<pre><code>#include &lt;thread&gt;
#include &lt;iostream&gt;
#include &lt;sstream&gt;

void worker_thread_func()
{
    while (true)
    {

    }
}

int main()
{
    std::thread t(worker_thread_func);
    //获取线程t的ID
    std::thread::id worker_thread_id = t.get_id();
    std::cout &lt;&lt; "worker thread id: " &lt;&lt; worker_thread_id &lt;&lt; std::endl;

    //获取主线程的线程 ID
    std::thread::id main_thread_id = std::this_thread::get_id();
    //先将std::thread::id转换成std::ostringstream对象
    std::ostringstream oss;
    oss &lt;&lt; main_thread_id;
    //再将std::ostringstream对象转换成std::string
    std::string str = oss.str();
    //最后将 std::string 转换成整型值
    int threadid = atol(str.c_str());

    std::cout &lt;&lt; "main thread id: " &lt;&lt; threadid &lt;&lt; std::endl;

    while (true)
    {
        //权宜之计，让主线程不要提前退出
    }

    return 0;
}
</code></pre>
<p>上述代码中我们在主线程创建了一个工作线程，然后分别获取工作线程和主线程的线程 ID。</p>
<p>程序运行结果如下：</p>
<p><img src="https://images.gitbook.cn/82979490-ce48-11e9-bdf7-7924fedc9f4e" alt="enter image description here" /></p>
<h3 id="">总结</h3>
<p>线程 ID 在实际编码中是一个很重要的上下文信息，因此熟练地获取某个线程的线程 ID，是多线程编程的基本功之一。</p>
<p>这里给读者留一个小问题：</p>
<blockquote>
  <p>线程 ID 是系统唯一的吗？答案可以在对应的课程微信群中获得。</p>
</blockquote>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a>。</p></div></article>