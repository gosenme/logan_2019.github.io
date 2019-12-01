---
title: C_C++ 多线程编程精髓-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面章节介绍了多线程编程的一些基础内容，从本讲开始，我将系统地介绍一遍 Windows 和 Linux 操作系统下各种常用的多线程资源同步对象。</p>
<p>在开始介绍 Windows 多线程资源同步之前，我们来介绍两个重要的 Windows API 函数 <strong>WaitForSingleObject</strong> 和 <strong>WaitForMultipleObjects</strong>，Windows 上所有多线程同步对象基本上都是通过这两个函数完成的，前者只能一次操作一个资源同步对象，后者可以同时操作多个资源同步对象。</p>
<h3 id="waitforsingleobjectwaitformultipleobjects">WaitForSingleObject 与 WaitForMultipleObjects 函数</h3>
<p>先来说 <strong>WaitForSingleObject</strong>，这个函数的签名是：</p>
<pre><code class="c++ language-c++">DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);
</code></pre>
<p>这个函数的作用是等待一个内核对象，在 Windows 系统上一个内核对象通常使用其句柄来操作，参数 <strong>hHandle</strong> 即需要等待的内核对象，参数 <strong>dwMilliseconds</strong> 是等待这个内核对象的最大时间，时间单位是毫秒，其类型是 DWORD，这是一个 <strong>unsigned long</strong> 类型。如果我们需要无限等待下去，可以将这个参数值设置为 <strong>INFINITE</strong> 宏。</p>
<p>在 Windows 上可以调用 <strong>WaitForSingleObject</strong> 等待的常见对象如下表所示：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">可以被等待的对象</th>
<th>等待对象成功的含义</th>
<th style="text-align:center;">对象类型</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">线程</td>
<td>等待线程结束</td>
<td style="text-align:center;">HANDLE</td>
</tr>
<tr>
<td style="text-align:center;">Process</td>
<td>等待进程结束</td>
<td style="text-align:center;">HANDLE</td>
</tr>
<tr>
<td style="text-align:center;">Event（事件）</td>
<td>等待 Event 有信号</td>
<td style="text-align:center;">HANDLE</td>
</tr>
<tr>
<td style="text-align:center;">Mutex (互斥体)</td>
<td>等待持有 Mutex 的线程释放该 Mutex，等待成功，拥有该 Mutex</td>
<td style="text-align:center;">HANDLE</td>
</tr>
<tr>
<td style="text-align:center;">Semaphore（信号量）</td>
<td>等待该 Semaphore 对象有信号</td>
<td style="text-align:center;">HANDLE</td>
</tr>
</tbody>
</table>
<p>上面介绍的等待线程对象上文中已经详细介绍过了，这里不再重复了，等待进程退出与等待线程退出类似，也不再赘述。下文中我们将详细介绍 Event、Mutex、Semaphore 这三种类型的资源同步对象，这里我们先接着介绍 <strong>WaitForSingleObject</strong> 函数的用法，该函数的返回值一般有以下类型：</p>
<ul>
<li><strong>WAIT_FAILED</strong>，表示 <strong>WaitForSingleObject</strong> 函数调用失败了，可以通过 <strong>GetLastError()</strong> 函数得到具体的错误码；</li>
<li><strong>WAIT_OBJECT_0</strong>，表示 <strong>WaitForSingleObject</strong> 成功“等待”到设置的对象；</li>
<li><strong>WAIT_TIMEOUT</strong>，等待超时；</li>
<li><strong>WAIT_ABANDONED</strong>，当等待的对象是 Mutex 类型时，如果持有该 Mutex 对象的线程已经结束，但是没有在结束前释放该 Mutex，此时该 Mutex 已经处于废弃状态，其行为是未知的，不建议再使用。</li>
</ul>
<p><strong>WaitForSingleObject</strong> 如其名字一样，只能“等待”单个对象，如果需要同时等待多个对象可以使用 <strong>WaitForMultipleObjects</strong>，除了对象的数量变多了，其用法基本上和 <strong>WaitForSingleObject</strong> 一样。 <strong>WaitForMultipleObjects</strong> 函数签名如下：</p>
<pre><code>DWORD WaitForMultipleObjects(
    DWORD        nCount,
    const HANDLE *lpHandles,
    BOOL         bWaitAll,
    DWORD        dwMilliseconds
);
</code></pre>
<p>参数 <strong>lpHandles</strong> 是需要等待的对象数组指针，参数 <strong>nCount</strong> 指定了该数组的长度，参数 <strong>bWaitAll</strong> 表示是否等待数组 <strong>lpHandles</strong> 所有对象有“信号”，取值为 <strong>TRUE</strong> 时，<strong>WaitForMultipleObjects</strong> 会等待所有对象有信号才会返回，取值为 <strong>FALSE</strong> 时，当其中有一个对象有信号时，立即返回，此时其返回值表示哪个对象有信号。</p>
<p>在参数 <strong>bWaitAll</strong> 设置为 <strong>FALSE</strong> 的情况下， 除了上面介绍的返回值是 <strong>WAIT<em>FAILED</strong> 和 <strong>WAIT</em>TIMEOUT</strong> 以外，返回值还有另外两种情形（分别对应 <strong>WaitForSingleObject</strong> 返回值是 <strong>WAIT_OBJECT_0</strong> 和 <strong>WAIT_ABANDONED</strong> 两种情形）：</p>
<ul>
<li><strong>WAIT_OBJECT_0</strong> to (<strong>WAIT_OBJECT_0</strong> + <em>nCount</em>– 1)，举个例子，假设现在等待三个对象 A1、A2、A3，它们在数组 <strong>lpHandles</strong> 中的下标依次是 0、1、2，某次 <strong>WaitForMultipleObjects</strong> 返回值是 <strong>Wait_OBJECT_0 + 1</strong>，则表示对象 A2 有信号，导致 WaitForMultipleObjects 调用成功返回。</li>
</ul>
<p>伪码如下：</p>
<pre><code>  HANDLE waitHandles[3];
  waitHandles[0] = hA1Handle;
  waitHandles[1] = hA2Handle;
  waitHandles[2] = hA3Handle;

  DWORD dwResult = WaitForMultipleObjects(3, waitHandles, FALSE, 3000);
  switch(dwResult)
  {
      case WAIT_OBJECT_0 + 0:
          //A1 有信号
          break;

      case WAIT_OBJECT_0 + 1:
          //A2 有信号
          break;

      case WAIT_OBJECT_0 + 2:
          //A3 有信号
          break;

      default:
          //出错或超时
          break;
  }
</code></pre>
<ul>
<li><strong>WAIT_ABANDONED_0</strong> to (<strong>WAIT_ABANDONED_0</strong> + <em>nCount</em>– 1)，这种情形与上面的使用方法相同，通过 nCount - 1 可以知道是等待对象数组中哪个对象始终没有被其他线程释放使用权。</li>
</ul>
<blockquote>
  <p>这里说了这么多理论知识，读者将在下文介绍的 Windows 常用的资源同步对象章节中看到具体的示例代码。</p>
</blockquote>
<h3 id="windows">Windows 的临界区对象</h3>
<p>在所有的 Windows 资源同步对象中，CriticalSection （临界区对象，有些书上翻译成“关键段”）是最简单易用的，从程序的术语来说，它防止多线程同时执行其保护的那段代码（<strong>临界区代码</strong>），即临界区代码某一时刻只允许一个线程去执行，示意图如下：</p>
<p><img src="https://images.gitbook.cn/ff474c00-cf1b-11e9-af41-f5624add887e" width = "70%" /></p>
<p>Windows 没有公开 CriticalSection 数据结构的定义，我们一般使用如下五个 API 函数操作临界区对象：</p>
<pre><code>void InitializeCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
void DeleteCriticalSection(LPCRITICAL_SECTION lpCriticalSection);

BOOL TryEnterCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
void EnterCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
void LeaveCriticalSection(LPCRITICAL_SECTION lpCriticalSection);
</code></pre>
<p><strong>InitializeCriticalSection</strong> 和 <strong>DeleteCriticalSection</strong> 用于初始化和销毁一个 <strong>CRITICAL_SECTION</strong> 对象；位于<strong>EnterCriticalSection</strong> 和 <strong>LeaveCriticalSection</strong> 之间的代码即临界区代码；调用 <strong>EnterCriticalSection</strong> 的线程会尝试“进入“临界区，如果进入不了，则会阻塞调用线程，直到成功进入或者超时；<strong>TryEnterCriticalSection</strong> 会尝试进入临界区，如果可以进入，则函数返回 <strong>TRUE</strong> ，如果无法进入则立即返回不会阻塞调用线程，函数返回 <strong>FALSE</strong>。<strong>LeaveCriticalSection</strong> 函数让调用线程离开临界区，离开临界区以后，临界区的代码允许其他线程调用 <strong>EnterCriticalSection</strong> 进入。</p>
<blockquote>
  <p><strong>EnterCriticalSection</strong>  超时时间很长，可以在注册表 <strong>HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager</strong> 这个位置修改参数 CriticalSectionTimeout 的值调整，当然实际开发中我们从来不会修改这个值，如果你的代码等待时间较长最终超时，请检查你的逻辑设计是否合理。</p>
</blockquote>
<p>我们来看一段实例代码：</p>
<pre><code>1  #include &lt;Windows.h&gt;
2  #include &lt;list&gt;
3  #include &lt;iostream&gt;
4  #include &lt;string&gt;
5 
6  CRITICAL_SECTION       g_cs;
7  int                    g_number = 0;
8
9  DWORD __stdcall WorkerThreadProc(LPVOID lpThreadParameter)
10 {
11    DWORD dwThreadID = GetCurrentThreadId();
12    
13    while (true)
14    {
15        EnterCriticalSection(&amp;g_cs);
16          std::cout &lt;&lt; "EnterCriticalSection, ThreadID: " &lt;&lt; dwThreadID &lt;&lt; std::endl;
17        g_number++;
18        SYSTEMTIME st;
19        //获取当前系统时间
20        GetLocalTime(&amp;st);
21        char szMsg[64] = { 0 };
22        sprintf(szMsg, 
23                "[%04d-%02d-%02d %02d:%02d:%02d:%03d]NO.%d, ThreadID: %d.", 
24                st.wYear, st.wMonth, st.wDay, 
25                  st.wHour, st.wMinute, st.wSecond, st.wMilliseconds, 
26                g_number, dwThreadID);
27
28        std::cout &lt;&lt; szMsg &lt;&lt; std::endl;
29        std::cout &lt;&lt; "LeaveCriticalSection, ThreadID: " &lt;&lt; dwThreadID &lt;&lt; std::endl;
30        LeaveCriticalSection(&amp;g_cs);
31
32        //睡眠1秒
33        Sleep(1000);
34    }
35
36    return 0;
37 }
38
39 int main()
40 {
41    InitializeCriticalSection(&amp;g_cs);
42
43    HANDLE hWorkerThread1 = CreateThread(NULL, 0, WorkerThreadProc, NULL, 0, NULL);
44    HANDLE hWorkerThread2 = CreateThread(NULL, 0, WorkerThreadProc, NULL, 0, NULL);
45
46    WaitForSingleObject(hWorkerThread1, INFINITE);
47    WaitForSingleObject(hWorkerThread2, INFINITE);
48
49    //关闭线程句柄
50    CloseHandle(hWorkerThread1);
51    CloseHandle(hWorkerThread2);
52
53    DeleteCriticalSection(&amp;g_cs);
54
55    return 0;
56 }
</code></pre>
<p>上述程序执行输出结果如下：</p>
<pre><code>EnterCriticalSection, ThreadID: 1224
[2019-01-19 22:25:41:031]NO.1, ThreadID: 1224.
LeaveCriticalSection, ThreadID: 1224
EnterCriticalSection, ThreadID: 6588
[2019-01-19 22:25:41:031]NO.2, ThreadID: 6588.
LeaveCriticalSection, ThreadID: 6588
EnterCriticalSection, ThreadID: 6588
[2019-01-19 22:25:42:031]NO.3, ThreadID: 6588.
LeaveCriticalSection, ThreadID: 6588
EnterCriticalSection, ThreadID: 1224
[2019-01-19 22:25:42:031]NO.4, ThreadID: 1224.
LeaveCriticalSection, ThreadID: 1224
EnterCriticalSection, ThreadID: 1224
[2019-01-19 22:25:43:031]NO.5, ThreadID: 1224.
LeaveCriticalSection, ThreadID: 1224
EnterCriticalSection, ThreadID: 6588
[2019-01-19 22:25:43:031]NO.6, ThreadID: 6588.
LeaveCriticalSection, ThreadID: 6588
EnterCriticalSection, ThreadID: 1224
[2019-01-19 22:25:44:031]NO.7, ThreadID: 1224.
LeaveCriticalSection, ThreadID: 1224
EnterCriticalSection, ThreadID: 6588
[2019-01-19 22:25:44:031]NO.8, ThreadID: 6588.
LeaveCriticalSection, ThreadID: 6588
</code></pre>
<p>在上述代码中我们新建两个工作线程，线程函数都是 <strong>WorkerThreadProc</strong>。线程函数在 <strong>15</strong> 行调用 <strong>EnterCriticalSection</strong> 进入临界区，在 <strong>30</strong> 行调用 <strong>LeaveCriticalSection</strong> 离开临界区，<strong>16</strong> ～ <strong>29</strong> 行之间的代码即临界区的代码，这段代码由于受到临界区对象 <strong>g_cs</strong> 的保护，因为每次只允许一个工作线程执行这段代码。虽然临界区代码中有多个输出，但是这些输出一定都是连续的，不会出现交叉输出的结果。</p>
<p>细心的读者会发现上述输出中存在同一个的线程连续两次进入临界区，这是有可能的。也就是说，当其中一个线程离开临界区，即使此时有其他线程在这个临界区外面等待，由于线程调度的不确定性，此时正在等待的线程也不会有先进入临界区的优势，它和刚离开这个临界区的线程再次竞争进入临界区是机会均等的。我们来看一张图：</p>
<p><img src="https://images.gitbook.cn/d100fbc0-cf1b-11e9-af41-f5624add887e" alt="enter image description here" /></p>
<p>上图中我们将线程函数的执行流程绘制成一个流程图，两个线程竞争进入临界区可能存在如下情形，为了表述方便，将线程称为 A、B。</p>
<ul>
<li><strong>情形一</strong>：线程 A 被唤醒获得 CPU 时间片进入临界区，执行流程 ①，然后执行临界区代码输出 → 线程 B 获得 CPU 时间片，执行流程 ②，然后失去 CPU 时间片进入休眠 → 线程 A 执行完临界区代码离开临界区后执行流程 ⑤，然后失去 CPU 时间片进入休眠 → 线程 B 被唤醒获得 CPU 时间片执行流程 ③、①，然后执行临界区代码输出。</li>
</ul>
<p>这种情形下，线程 A 和线程 B 会轮流进入临界区执行代码。</p>
<ul>
<li><strong>情形二</strong>：线程 A 被唤醒获得 CPU 时间片进入临界区，执行流程 ①，然后执行临界区代码输出  →  线程 B 获得 CPU 时间片，执行流程 ③，然后执行流程 ② 在临界区外面失去 CPU 时间片进入休眠 → 线程 A 执行完临界区代码离开临界区后执行流程 ④、① 。</li>
</ul>
<p>这种情形下，会出现某个线程连续两次甚至更多次的进入临界区执行代码。</p>
<p>如果在某个线程在尝试进入临界区时引无法阻塞而进入睡眠状态，当其他线程离开这个临界区后，之前因为这个临界区而阻塞的线程可能会被唤醒进行再次竞争，也可能不被唤醒。但是存在这样一种特例，假设现在存在两个线程 A 和 B，线程 A 离开临界区的线程再也不需要再次进入临界区，那么线程 B 在被唤醒时一定可以进入临界区。线程 B 从睡眠状态被唤醒，这涉及到一次线程的切换，有时候这种开销是不必要的，我们可以让 B 简单地执行一个循环等待一段时间后去进去临界区，而不是先睡眠再唤醒，与后者相比，执行这个循环的消耗更小。这就是所谓的“自旋”，在这种情形下，Windows 提供了另外一个初始化临界区的函数 <strong>InitializeCriticalSectionAndSpinCount</strong>，这个函数比 <strong>InitializeCriticalSection</strong> 多一个自旋的次数：</p>
<pre><code>BOOL InitializeCriticalSectionAndSpinCount(
      LPCRITICAL_SECTION lpCriticalSection,
      DWORD              dwSpinCount
);
</code></pre>
<p>参数 <strong>dwSpinCount</strong> 是自旋的次数，利用自旋来代替让 CPU 进入睡眠和再次被唤醒，消除线程上下文切换带来的消耗，提高效率。当然，在实际开发中这种方式是靠不住的，线程调度是操作系统内核的策略，应用层上的应用不应该假设线程的调度策略是按预想的来执行。但是理解线程与临界区之间的原理有利于编写出更高效的应用来。</p>
<p>需要说明的是，临界区对象通过保护一段代码不被多个线程同时执行，进而来保证多个线程之间读写一个对象是安全的。由于同一时刻只有一个线程可以进入临界区，因此这种对资源的操作是排他的，即对于同一个临界区对象，不会出现多个线程同时操作该资源，哪怕是资源本身可以在同一时刻被多个线程进行操作，如多个线程对资源进行读操作，这就带来了效率问题。</p>
<p>我们一般将进入临界区的线程称为该临界区的拥有者（owner）——临界区持有者。</p>
<p>最后，为了避免死锁，<strong>EnterCriticalSection</strong> 和 <strong>LeaveCriticalSection</strong> 需要成对使用，尤其是在具有多个出口的函数中，记得在每个分支处加上 <strong>LeaveCriticalSection</strong>。伪码如下：</p>
<pre><code>void someFunction()
{
    EnterCriticalSection(&amp;someCriticalSection);
    if (条件A)
    {
        if (条件B)
        {
            LeaveCriticalSection(&amp;someCriticalSection);
            //出口1
            return;
        }

        LeaveCriticalSection(&amp;someCriticalSection);
        //出口2
        return;
    }

    if (条件C)
    {
        LeaveCriticalSection(&amp;someCriticalSection);
        // 出口3
        return;
    }

    if (条件C)
    {
        LeaveCriticalSection(&amp;someCriticalSection);
        // 出口4
        return;
    }
}
</code></pre>
<p>上述代码中，为了能让临界区对象被正常的释放，在函数的每个出口都加上了 <strong>LeaveCriticalSection</strong> 调用，如果函数的出口非常多，这样的代码太难维护了。因此一般建议使用 RAII 技术将临界区 API 封装成对象，该对象在函其作用域内进入临界区，在出了其作用域后自动离开临界区，示例代码如下：</p>
<pre><code>class CCriticalSection
{
public:
    CCriticalSection(CRITICAL_SECTION&amp; cs) : mCS(cs)
    {
        EnterCriticalSection(&amp;mCS);
    }

    ~CCriticalSection()
    {
        LeaveCriticalSection(&amp;mCS);
    }

private:
    CRITICAL_SECTION&amp; mCS;
};
</code></pre>
<p>利用 <strong>CCriticalSection</strong> 类，我们可以对上述伪码进行优化：</p>
<pre><code>void someFunction()
{
    CCriticalSection autoCS(someCriticalSection);
    if (条件A)
    {
        if (条件B)
        { 
            //出口1
            return;
        }

        //出口2
        return;
    }

    if (条件C)
    {      
        // 出口3
        return;
    }

    if (条件C)
    {        
        // 出口4
        return;
    }
}
</code></pre>
<p>上述代码中由于变量 <strong>autoCS</strong> 会在出了函数作用域后调用其析构函数，在析构函数中调用 <strong>LeaveCriticalSection</strong> 自动离开临界区。</p>
<h3 id="">总结</h3>
<p>本讲介绍了 WaitForSingleObject 和 WaitForMultipleObjects 这两个重要的 Windows API 函数，同时介绍了 Windows 上第一个线程同步对象——临界区，为了避免因函数有多个出口造成的编码疏漏，我们介绍了使用 RAII 封装临界区对象的方法。临界区对象是 Windows 系统多线程资源同步最常用的对象之一。</p>
<p><strong>思考题</strong></p>
<blockquote>
  <p>Windows 临界区对象可以跨进程使用吗？答案可以在对应的课程微信群中获得。</p>
</blockquote>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a>。</p></div></article>