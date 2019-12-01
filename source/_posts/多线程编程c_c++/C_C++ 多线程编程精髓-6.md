---
title: C_C++ 多线程编程精髓-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面课程介绍了创建线程，既然线程可以创建，线程也应该可以结束。那如何等待一个线程结束呢？</p>
<p>实际项目开发中，我们常常会有这样一种需求，即一个线程需要等待另外一个线程执行完任务退出后再继续执行。这在 Linux 和 Windows 操作系统中都提供了相应的操作系统 API，我们来分别介绍一下。</p>
<h3 id="linux">Linux 下等待线程结束</h3>
<p>Linux 线程库提供了 <strong>pthread_join</strong> 函数，用来等待某线程的退出并接收它的返回值。这种操作被称为<strong>连接</strong>（joining），<strong>pthread_join</strong> 函数签名如下：</p>
<pre><code>int pthread_join(pthread_t thread, void** retval);
</code></pre>
<ul>
<li>参数 <strong>thread</strong>，需要等待的线程 id。</li>
<li>参数 <strong>retval</strong>，输出参数，用于接收等待退出的线程的退出码（<strong>Exit Code</strong>），线程退出码可以通过调用 <strong>pthread_exit</strong> 退出线程时指定，也可以在线程函数中通过 <strong>return</strong> 语句返回。 </li>
</ul>
<pre><code>#include &lt;pthread.h&gt;

void pthread_exit(void* value_ptr); 
</code></pre>
<p>参数 <strong>value_ptr</strong> 的值可以在 <strong>pthread_join</strong> 中拿到，没有可以设置为 NULL。</p>
<p><strong>pthread_join 函数等待其他线程退出期间会挂起等待的线程</strong>，被挂起的线程不会消耗宝贵任何 CPU 时间片。直到目标线程退出后，等待的线程会被唤醒。</p>
<p>我们通过一个实例来演示一下这个函数的使用方法，实例功能如下：</p>
<p>程序启动时，开启一个工作线程，工作线程将当前系统时间写入文件中后退出，主线程等待工作线程退出后，从文件中读取出时间并显示在屏幕上。代码如下：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;pthread.h&gt;

#define TIME_FILENAME "time.txt"

void fileThreadFunc(void* arg)
{
    time_t now = time(NULL);
    struct tm* t = localtime(&amp;now);
    char timeStr[32] = {0};
    snprintf(timeStr, 32, "%04d/%02d/%02d %02d:%02d:%02d", 
             t-&gt;tm_year+1900,
             t-&gt;tm_mon+1,
             t-&gt;tm_mday,
             t-&gt;tm_hour,
             t-&gt;tm_min,
             t-&gt;tm_sec);
    //文件不存在，则创建；存在，则覆盖
    FILE* fp = fopen(TIME_FILENAME, "w");
    if (fp == NULL)
    {
      printf("Failed to create time.txt.\n");
        return;
    }

    size_t sizeToWrite = strlen(timeStr) + 1;
    size_t ret = fwrite(timeStr, 1, sizeToWrite, fp);
    if (ret != sizeToWrite)
    {
        printf("Write file error.\n");
    }

    fclose(fp);
}

int main()
{
    pthread_t fileThreadID;
    int ret = pthread_create(&amp;fileThreadID, NULL, fileThreadFunc, NULL);
    if (ret != 0)
    {
        printf("Failed to create fileThread.\n");
        return -1;
    }

    int* retval;
    pthread_join(fileThreadID, &amp;retval);

    //使用r选项，要求文件必须存在
    FILE* fp = fopen(TIME_FILENAME, "r");
    if (fp == NULL)
    {
        printf("open file error.\n");
        return -2;
    }

    char buf[32] = {0};
    int sizeRead = fread(buf, 1, 32, fp);
    if (sizeRead == 0)
    {
      printf("read file error.\n");
      return -3;
    }

    printf("Current Time is: %s.\n", buf);

    return 0;
}
</code></pre>
<p>程序执行结果如下：</p>
<pre><code>[root@localhost threadtest]# ./test
Current Time is: 2018/09/24 21:06:01.
</code></pre>
<h3 id="windows">Windows 下等待线程结束</h3>
<p>Windows 下使用 API <strong>WaitForSingleObject</strong> 或 <strong>WaitForMultipleObjects</strong> 函数，前者用于等待一个线程结束，后者可以同时等待多个线程结束。这是两个非常重要的函数，它们的作用不仅可以用于等待线程退出，还可以用于等待其他线程同步对象，本文后面的将详细介绍这两个函数。与 Linux 的 <strong>pthread_join</strong> 函数不同，Windows 的<strong>WaitForSingleObject</strong> 函数提供了可选择等待时间的精细控制。</p>
<p>这里我们仅演示等待线程退出。</p>
<p><strong>WaitForSingleObject</strong> 函数签名如下：</p>
<pre><code>DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);
</code></pre>
<ul>
<li>参数 <strong>hHandle</strong> 是需要等待的对象的句柄，等待线程退出，传入线程句柄。</li>
<li>参数 <strong>dwMilliseconds</strong> 是需要等待的毫秒数，如果使用 <strong>INFINITE</strong> 宏，则表示无限等待下去。</li>
<li><strong>返回值</strong>：该函数的返回值有点复杂，我们后面文章具体介绍。当 <strong>dwMilliseconds</strong> 参数使用 <strong>INFINITE</strong> 值，该函数会挂起当前等待线程，直到等待的线程退出后，等待的线程才会被唤醒，<strong>WaitForSingleObject</strong> 后的程序执行流继续执行。</li>
</ul>
<p>我们将上面的 Linux 示例代码改写成 Windows 版本的：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;Windows.h&gt;

#define TIME_FILENAME "time.txt"

DWORD WINAPI FileThreadFunc(LPVOID lpParameters)
{
    time_t now = time(NULL);
    struct tm* t = localtime(&amp;now);
    char timeStr[32] = { 0 };
    sprintf_s(timeStr, 32, "%04d/%02d/%02d %02d:%02d:%02d",
              t-&gt;tm_year + 1900,
              t-&gt;tm_mon + 1,
              t-&gt;tm_mday,
              t-&gt;tm_hour,
              t-&gt;tm_min,
              t-&gt;tm_sec);
    //文件不存在，则创建；存在，则覆盖
    FILE* fp = fopen(TIME_FILENAME, "w");
    if (fp == NULL)
    {
        printf("Failed to create time.txt.\n");
        return 1;
    }

    size_t sizeToWrite = strlen(timeStr) + 1;
    size_t ret = fwrite(timeStr, 1, sizeToWrite, fp);
    if (ret != sizeToWrite)
    {
        printf("Write file error.\n");
    }

    fclose(fp);

    return 2;
}


int main()
{
    DWORD dwFileThreadID;
    HANDLE hFileThread = CreateThread(NULL, 0, FileThreadFunc, NULL, 0, 
                                      &amp;dwFileThreadID);
    if (hFileThread == NULL)
    {
        printf("Failed to create fileThread.\n");
        return -1;
    }

    //无限等待，直到文件线程退出，否则程序将一直挂起
    WaitForSingleObject(hFileThread, INFINITE);

    //使用r选项，要求文件必须存在
    FILE* fp = fopen(TIME_FILENAME, "r");
    if (fp == NULL)
    {
        printf("open file error.\n");
        return -2;
    }

    char buf[32] = { 0 };
    int sizeRead = fread(buf, 1, 32, fp);
    if (sizeRead == 0)
    {
        printf("read file error.\n");
        return -3;
    }

    printf("Current Time is: %s.\n", buf);

    return 0;
}
</code></pre>
<p>与 Linux 版本一样，我们得到类似的程序执行结果：</p>
<p><img src="https://images.gitbook.cn/2ad72550-ce4c-11e9-9f77-155b7642027f" alt="enter image description here" /></p>
<h3 id="c11">C++ 11 提供的等待线程结果函数</h3>
<p>可以想到，C++ 11 的 <strong>std::thread</strong> 既然统一了 Linux 和 Windows 的线程创建函数，那么它应该也提供等待线程退出的接口，确实如此，<strong>std::thread</strong> 的 <strong>join</strong> 方法就是用来等待线程退出的函数。当然使用这个函数时，必须保证该线程还处于运行中状态，也就是说等待的线程必须是可以 “<strong>join</strong>”的，如果需要等待的线程已经退出，此时调用<strong>join</strong> 方法，程序会产生崩溃。因此，C++ 11 的线程库同时提供了一个 <strong>joinable</strong> 方法来判断某个线程是否可以 join，如果不确定线程是否可以“join”，可以先调用 <strong>joinable</strong> 函数判断一下是否需要等待。</p>
<p>还是以上面的例子为例，改写成 C++11 的代码：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;thread&gt;

#define TIME_FILENAME "time.txt"

void FileThreadFunc()
{
    time_t now = time(NULL);
    struct tm* t = localtime(&amp;now);
    char timeStr[32] = { 0 };
    sprintf_s(timeStr, 32, "%04d/%02d/%02d %02d:%02d:%02d",
              t-&gt;tm_year + 1900,
              t-&gt;tm_mon + 1,
              t-&gt;tm_mday,
              t-&gt;tm_hour,
              t-&gt;tm_min,
              t-&gt;tm_sec);
    //文件不存在，则创建；存在，则覆盖
    FILE* fp = fopen(TIME_FILENAME, "w");
    if (fp == NULL)
    {
        printf("Failed to create time.txt.\n");
        return;
    }

    size_t sizeToWrite = strlen(timeStr) + 1;
    size_t ret = fwrite(timeStr, 1, sizeToWrite, fp);
    if (ret != sizeToWrite)
    {
        printf("Write file error.\n");
    }

    fclose(fp);
}

int main()
{
    std::thread t(FileThreadFunc);
    if (t.joinable())
        t.join();

    //使用 r 选项，要求文件必须存在
    FILE* fp = fopen(TIME_FILENAME, "r");
    if (fp == NULL)
    {
        printf("open file error.\n");
        return -2;
    }

    char buf[32] = { 0 };
    int sizeRead = fread(buf, 1, 32, fp);
    if (sizeRead == 0)
    {
        printf("read file error.\n");
        return -3;
    }

    printf("Current Time is: %s.\n", buf);

    return 0;
}
</code></pre>
<h3 id="">总结</h3>
<p>在 A 线程等待 B 线程结束，相当于 A 线程和 B 线程在该点汇集（或连接），这就是 <strong>join</strong> 函数的语义来源，因此很多其他编程语言也使用 join 一词表示等待线程结束。</p>
<p><strong>思考题</strong></p>
<p>C++ 11 的 std::thread 类提供了一个 join() 方法，如果某个线程已经结束，调用其 join() 方法会怎样呢？有没有办法判断一个线程已经结束？ 答案可以在对应的课程微信群中获得。</p>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a>。</p></div></article>