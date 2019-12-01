---
title: C_C++ 多线程编程精髓-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">线程的创建</h3>
<p>在使用线程之前，我们首先要学会如何创建一个新的线程。不管是哪个库还是哪种高级语言（如 Java），线程的创建最终还是调用操作系统的 API 来进行的。我们这里先介绍操作系统的接口，这里分为 Linux 和 Windows 两个常用的操作系统平台来介绍。当然，这里并不是照本宣科地把 Linux man 手册或者 msdn 上的函数签名搬过来，而是只介绍我们实际开发中常用的参数和需要注意的重难点。</p>
<h4 id="linux">Linux 线程创建</h4>
<p>Linux 平台上使用 <strong>pthread_create</strong> 这个 API 来创建线程，其函数签名如下。</p>
<pre><code>int pthread_create(pthread_t *thread, 
                   const pthread_attr_t *attr,
                   void *(*start_routine) (void *), 
                   void *arg);
</code></pre>
<ul>
<li>参数 <strong>thread</strong>，是一个输入参数，如果线程创建成功，则通过这个参数可以得到创建成功的线程 ID（下文会介绍线程 ID 的知识）。</li>
<li>参数 <strong>attr</strong> 指定了该线程的属性，一般设置为 NULL，表示使用默认属性。</li>
<li>参数 <strong>start_routine</strong> 指定了线程函数，这里需要注意的是这个函数的调用方式必须是 <strong>__cedel</strong> 调用，因为在 C/C++ 中定义函数时默认的调用方式使用 <strong>__cedel</strong>，所以一般很少有人意识到这一点。而后面介绍在 Windows 操作系统上使用 <strong>CreateThread</strong> 定义线程函数时必须使用 <strong>__stdcall</strong> 调用方式时，我们就必须显式声明函数的调用方式了。</li>
</ul>
<p>也就是说，如下函数的调用方式是等价的：</p>
<pre><code>//代码片段1： 不显式指定函数调用方式，其调用方式为默认的 __cdecl
void start_routine (void* args)
{
}

//代码片段2： 显式指定函数调用方式为默认的 __cdecl，等价于代码片段1
void __cdecl start_routine (void* args)
{
}
</code></pre>
<ul>
<li>参数 <strong>arg</strong>，通过这一参数可以在创建线程时将某个参数传入线程函数中，由于这是一个 <strong>void</strong>* 类型，可以方便我们最大化地传入任意多的信息给线程函数（下文会介绍一个使用示例）。</li>
<li>返回值：如果成功创建线程，则返回 <strong>0</strong>；如果创建失败，则返回相应的错误码。常见的错误码有 <strong>EAGAIN</strong>、<strong>EINVAL</strong>。<strong>EAGAIN</strong> 表示系统资源不足导致线程无法创建（如达到系统限制的最大线程数目），<strong>EINVAL</strong> 表示传入了无效的参数 <strong>attr</strong>。在实际开发只要我们正确的设置了各个参数，一般不关心该函数的返回值，即一般认为线程可以正确创建出来。</li>
</ul>
<p>下面是一个使用 <strong>pthread_create</strong> 创建线程的简单示例：</p>
<pre><code class="c++ language-c++">#include &lt;pthread.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdio.h&gt;

void* threadfunc(void* arg)
{
  while(1)
  {
    //睡眠1秒
    sleep(1);

    printf("I am New Thread!\n");
  }
}

int main()
{
  pthread_t threadid;
  pthread_create(&amp;threadid, NULL, threadfunc, NULL);

  while (1)
  {
    sleep(1);
    //权宜之计，让主线程不要提前退出
  }

  return 0;
}
</code></pre>
<p>上述代码片段利用 <strong>pthread_create</strong> 函数在主线程创建了一个工作线程，线程函数为 <strong>threadfunc</strong>。</p>
<h4 id="windows">Windows 线程创建</h4>
<p>Windows 上创建线程使用 <strong>CreateThread</strong>，其函数签名如下：</p>
<pre><code>HANDLE CreateThread(
  LPSECURITY_ATTRIBUTES   lpThreadAttributes,
  SIZE_T                  dwStackSize,
  LPTHREAD_START_ROUTINE  lpStartAddress,
  LPVOID                  lpParameter,
  DWORD                   dwCreationFlags,
  LPDWORD                 lpThreadId
);
</code></pre>
<ul>
<li>参数 <strong>lpThreadAttributes</strong>，是线程的安全属性，一般设置为 NULL。</li>
<li>参数 <strong>dwStackSize</strong>，线程的栈空间大小，单位为字节数，一般指定为 0，表示使用默认大小。</li>
<li>参数 <strong>lpStartAddress</strong>，为线程函数，其类型是 <strong>LPTHREAD_START_ROUTINE</strong>，这是一个函数指针类型，其定义如下：</li>
</ul>
<pre><code>typedef DWORD ( __stdcall *LPTHREAD_START_ROUTINE )(LPVOID lpThreadParameter);
</code></pre>
<blockquote>
  <p>需要注意的是，Windows 上创建的线程的线程函数其调用方式必须是<strong>__stdcall</strong>，如果将如下函数设置成线程函数是不行的：</p>
</blockquote>
<pre><code>DWORD threadfunc(LPVOID lpThreadParameter);
</code></pre>
<p>如上文所说，如果不指定函数的调用方式，使用默认调用方式 <strong>__cdecl</strong>，而这里的线程函数要求是 <strong>__stdcall</strong>，因此必须在函数名前面显式指定函数调用方式为 <strong>__stdcall</strong>。</p>
<pre><code>DWORD __stdcall threadfunc(LPVOID lpThreadParameter);
</code></pre>
<p>Windows 上的宏 <strong>WINAPI</strong> 和 <strong>CALLBACK</strong> 这两个宏的定义都是 <strong>__stdcall</strong>。因为在项目中看到的线程函数的签名大多写成如下两种形式的一种：</p>
<pre><code>//写法1
DWORD WINAPI threadfunc(LPVOID lpThreadParameter);
//写法2
DWORD CALLBACK threadfunc(LPVOID lpThreadParameter);
</code></pre>
<ul>
<li>参数 <strong>lpParameter</strong> 为传给线程函数的参数，和 Linux 下的 <strong>pthread_create</strong> 函数的 <strong>arg</strong> 一样，这实际上也是一个 <strong>void</strong>* 类型（LPVOID 类型是用过 typedef 包装后的 void* 类型）。</li>
</ul>
<pre><code>typedef void* LPVOID;
</code></pre>
<ul>
<li>参数 <strong>dwCreationFlags</strong>，是一个 32 位无符号整型（DWORD），一般设置为 0，表示创建好线程后立即启动线程的运行；有一些特殊的情况，我们不希望创建线程后立即开始执行，可以将这个值设置为 <strong>4</strong>（对应 Windows 定义的宏 <strong>CREATE_SUSPENDED</strong>），后面在需要的时候，再使用 <strong>ResumeThread</strong> 这个 API 让线程运行起来。</li>
<li>参数 <strong>lpThreadId</strong>，为线程创建成功返回的线程 ID，这也是一个 32 位无符号整数（DWORD）的指针（LPDWORD）。</li>
<li>返回值：Windows 上使用句柄（HANDLE 类型）来管理线程对象，句柄本质上是内核句柄表中的索引值。如果成功创建线程，则返回该线程的句柄；如果创建失败，则返回 NULL。</li>
</ul>
<p>下面的代码片段，演示了 Windows 上如何创建一个线程：</p>
<pre><code>#include &lt;Windows.h&gt;
#include &lt;stdio.h&gt;

DWORD WINAPI ThreadProc(LPVOID lpParameters)
{
    while (true)
    {
        //睡眠 1 秒，Windows 上的 Sleep 函数参数事件单位为毫秒
        Sleep(1000);

        printf("I am New Thread!\n");
    }
}

int main()
{
    DWORD dwThreadID;
    HANDLE hThread = CreateThread(NULL, 0, ThreadProc, NULL, 0, &amp;dwThreadID);
    if (hThread == NULL)
    {
        printf("Failed to CreateThread.\n");
    }

    while (true)
    {
        Sleep(1000);
        //权宜之计，让主线程不要提前退出
    }

    return 0;
}
</code></pre>
<p>上述代码片段利用 <strong>CreateThread</strong> 函数在主线程创建了一个工作线程，线程函数为 <strong>ThreadProc</strong>，线程函数名 <strong>ThreadProc</strong> 符合 Windows 程序设计风格。</p>
<h4 id="windowscrt">Windows CRT 提供的线程创建函数</h4>
<p>这里的 CRT，指的是 <strong>C</strong> <strong>R</strong>un<strong>t</strong>ime（C 运行时），通俗地说就是 C 函数库。在 Windows 操作系统上，微软实现的 C 库也提供了一套用于创建线程的函数（当然这个函数底层还是调用相应的操作系统平台的线程创建 API）。<strong>在实际项目开发中推荐使用这个函数来创建线程而不是使用 CreateThread 函数。</strong></p>
<p>Windows C 库创建线程常用的函数是 _beginthreadex，声明位于 process.h 头文件中，其签名如下：</p>
<pre><code>uintptr_t _beginthreadex( 
   void *security,  
   unsigned stack_size,  
   unsigned ( __stdcall *start_address )( void * ),  
   void *arglist,  
   unsigned initflag,  
   unsigned *thrdaddr   
);  
</code></pre>
<p>函数签名基本上和 Windows 上的 <strong>CreateThread</strong> 函数基本一致，这里就不再赘述了。</p>
<p>以下是使用 <strong>_beginthreadex</strong> 创建线程的一个例子：</p>
<pre><code>#include &lt;process.h&gt;
//#include &lt;Windows.h&gt;
#include &lt;stdio.h&gt;

unsigned int __stdcall threadfun(void* args)
{
    while (true)
    {        
        //Sleep(1000);

        printf("I am New Thread!\n");
    }
}

int main(int argc, char* argv[])
{
    unsigned int threadid;
    _beginthreadex(0, 0, threadfun, 0, 0, &amp;threadid);

    while (true)
    {
        //Sleep(1000);
        //权宜之计，让主线程不要提前退出
    }

    return 0;
}
</code></pre>
<p>上述代码片段利用 <strong>_beginthreadex</strong> 函数在主线程创建了一个工作线程，线程函数为 <strong>threadfun</strong>。</p>
<h4 id="c11stdthread">C++ 11 提供的 std::thread 类</h4>
<p>无论是 Linux 还是 Windows 上创建线程的 API，都有一个非常不方便的地方，就是线程函数的签名必须是固定的格式（参数个数和类型、返回值类型都有要求）。C++11 新标准引入了一个新的类 <strong>std::thread</strong>（需要包含头文件\<thread\>），使用这个类的可以将任何签名形式的函数作为线程函数。以下代码分别创建两个线程，线程函数签名不一样：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;thread&gt;

void threadproc1()
{
    while (true)
    {
        printf("I am New Thread 1!\n");
    }
}

void threadproc2(int a, int b)
{
    while (true)
    {
        printf("I am New Thread 2!\n");
    }
}

int main()
{
    //创建线程t1
    std::thread t1(threadproc1);
    //创建线程t2
    std::thread t2(threadproc2, 1, 2);

    while (true)
    {
        //Sleep(1000);
        //权宜之计，让主线程不要提前退出
    }

    return 0;
}
</code></pre>
<p>当然， <strong>std::thread</strong> 在使用上容易犯一个错误，即在 <strong>std::thread</strong> 对象在线程函数运行期间必须是有效的。什么意思呢？我们来看一个例子：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;thread&gt;

void threadproc()
{
    while (true)
    {
        printf("I am New Thread!\n");
    }
}

void func()
{
    std::thread t(threadproc);
}

int main()
{
    func();

    while (true)
    {
        //Sleep(1000);
        //权宜之计，让主线程不要提前退出
    }

    return 0;
}
</code></pre>
<p>上述代码在 <strong>func</strong> 中创建了一个线程，然后又在 <strong>main</strong> 函数中调用 <strong>func</strong> 方法，乍一看好像代码没什么问题，但是在实际运行时程序会崩溃。崩溃的原因是，当 <strong>func</strong> 函数调用结束后，<strong>func</strong> 中局部变量 <strong>t</strong> （<strong>线程对象</strong>）被销毁了，而此时<strong>线程函数</strong>仍然在运行。这就是我所说的，使用 <strong>std::thread</strong> 类时，必须保证线程函数运行期间，其线程对象有效。这是一个很容易犯的错误，解决这个问题的方法是，<strong>std::thread</strong> 对象提供了一个 <strong>detach</strong> 方法，这个方法让<strong>线程对象</strong>与<strong>线程函数</strong>脱离关系，这样即使<strong>线程对象</strong>被销毁，仍然不影响<strong>线程函数</strong>的运行。我们只需要在在 <strong>func</strong> 函数中调用 <strong>detach</strong> 方法即可，代码如下：</p>
<pre><code>//其他代码保持不变，这里就不重复贴出来了
void func()
{
    std::thread t(threadproc);
    t.detach();
}
</code></pre>
<p>然而，在实际编码中，这也是一个不推荐的做法，原因是我们需要使用<strong>线程对象</strong>去控制和管理线程的运行和生命周期。所以，我们的代码应该尽量保证<strong>线程对象</strong>在线程运行期间有效，而不是单纯地调用 <strong>detach</strong> 方法使线程对象与线程函数的运行分离。</p>
<h3 id="-1">总结</h3>
<p>本讲介绍了 Linux 和 Windows 平台的线程创建基础 API，同时也介绍了 CRT 和 C++ 11 语言标准提供的创建线程的方法（它们可以方便我们写跨平台代码），但是读者一定要明白 CRT 和 C++ 11 创建线程的函数其实现是在对应的操作系统平台调用我们介绍的线程创建函数。</p>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a></p>
<h3 id="-2">分享交流</h3>
<p>我们为本专栏<strong>付费读者</strong>创建了微信交流群，以方便更有针对性地讨论专栏相关的问题。入群方式请添加 GitChat 小助手泰勒的微信号：GitChatty5（或扫描以下二维码），然后给小助手发「222」消息，即可拉你进群~</p>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" /></p></div></article>