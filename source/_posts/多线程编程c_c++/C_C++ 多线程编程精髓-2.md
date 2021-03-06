---
title: C_C++ 多线程编程精髓-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>多年以前，技术面试的时候面试官经常会问“<strong>程序什么时候需要开启新的线程</strong>”这样的问题，当时多核 CPU 才刚开始普及，很多人也是才开始逐渐接触多线程技术。而如今多核 CPU 和多线程编程技术已经是下里巴人的技术了，因此本专栏内容不会花大气力再去回答“<strong>程序什么时候需要开启新的线程</strong>”这一类问题，简单地解释一下，就是为了提高解决问题的效率，毕竟大多数情况下，多个 CPU 并行做一件事总比单个 CPU 做要快很多吧（根本原因其实是：现在的面试官也很少再问“<strong>程序什么时候需要开启新的线程</strong>”这样的问题了，哈哈 ^_^）。</p>
<p>然而，多线程程序虽然强大，但也让原来的程序执行流程变得复杂和具有一定的不确定性，比如带来资源的竞态问题，初学者或不能意识到带来的后果，或不能够很好地处理这个问题。不过不用担心，这是本专栏要介绍的重点内容之一。</p>
<p>多线程编程在现代软件开发中是如此的重要，以至于熟练使用多线程编程是一名合格的后台开发人员的<strong>基本功</strong>，注意，我这里用的是<strong>基本功</strong>一词。它是如此的重要，因此更应该掌握它。本专栏将结合操作系统原理介绍多线程的方方面面，同时涉及到 Windows 和 Linux 两个平台的线程技术，从基础的知识到高级进阶，让我们开始吧。</p>
<h3 id="">线程的基本概念</h3>
<p>线程的英文单词是 <strong>thread</strong>，翻译成对应的中文有“分支”、“枝干”的意思，当然这里翻译成“线程”属于意译了。提高线程就不得不提与线程相关联的另外一个概念“<strong>进程</strong>”，一个“<strong>进程</strong>”代表计算机中实际跑起来的一个程序，在现代操作系统的保护模式下，每个进程拥有自己独立的进程地址空间和上下文堆栈。但是就一个程序本身执行的操作来说，进程其实什么也不做（不执行任何进程代码），它只是提供一个大环境容器，在进程中实际的执行体是“<strong>线程</strong>”。</p>
<p><strong>wiki</strong> 百科上给线程的定义是：</p>
<blockquote>
  <p>In computer science, a thread of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system.</p>
  <p>计算机科学中，线程是操作系统管理的、可以执行编制好的最小单位的指令序列的调度器。</p>
</blockquote>
<p>翻译的有点拗口，通俗地来说，线程是进程中实际执行代码的最小单元，它由操作系统安排调度（何时启动、何时运行和暂停以及何时消亡）。</p>
<h3 id="-1">关于线程的常见问题</h3>
<p>进程与线程的区别及关系这里就不再多说了，任何一本关于操作系统的书籍都会有详细地介绍。这里需要重点强调的是如下几个问题，这也是我们在实际开发中使用多线程需要搞明白的问题。</p>
<h4 id="-2">一个进程至少有一个线程</h4>
<p>上面也提到了，线程是进程中实际干活的单位，因此一个进程至少得有一个线程，我们把这个线程称之为“<strong>主线程</strong>”，也就是说，<strong>一个进程至少要有一个主线程</strong>。</p>
<h4 id="-3">主线程退出，支线程也将退出吗？</h4>
<p>在 <strong>Windows</strong> 系统中，当一个进程存在多个线程时，如果主线程执行结束了，那么这个时候即使支线程（也可以叫<strong>工作线程</strong>）还没完成相关的代码执行，支线程也会退出，也就是说，主线程一旦退出整个进程也就结束了。之所以强调这一点是，很多多线程编程的初学者经常犯在工作线程写了很多逻辑代码，但是没有注意到主线程已经提前退出，导致这些工作线程的代码来不及执行。解决这一问题的方案很多，核心就是让主线程不要退出，或者至少在工作线程完成工作之前主线程不要退出。常见的解决方案有主线程启动一个循环或者主线程等待工作线程退出后再退出（下文将会详细介绍）。</p>
<p>在 <strong>Linux</strong> 系统中，如果主线程退出，工作线程一般不会受到影响，还会继续运行下去，但是此时这个进程就会变成所谓的<strong>僵尸进程</strong>，这是一种不好的做法，实际开发中应该避免产生僵尸进程。</p>
<pre><code>### ps -ef 命令查看系统进程列表时，带有&lt;defunct&gt;字样的进程即僵尸进程
[root@localhost ~]# ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         2     0  0 Jan18 ?        00:00:01 [kthreadd]
root         3     2  0 Jan18 ?        00:00:25 [ksoftirqd/0]
root         5     2  0 Jan18 ?        00:00:00 [kworker/0:0H]
root     60928     1  0 14:48 pts/1    00:00:00 [linuxtid] &lt;defunct&gt;
</code></pre>
<blockquote>
  <p>Linux 版本众多，在某些 Linux 版本实现中，主线程退出也会导致支线程退出，这个行为就和 Windows 上一样了。读者在实际开发时应该以自己的机器测试结果为准。</p>
</blockquote>
<h4 id="-4">某个线程崩溃，会导致进程退出吗？</h4>
<p>这是一个常见的面试题，还有一种问法是：<strong>进程中某个线程崩溃，是否会对其他线程造成影响？</strong></p>
<p>一般来说，每个线程都是独立执行的单位，每个线程都有自己的上下文堆栈，一个线程的的崩溃不会对其他线程造成影响。但是通常情况下，一个线程崩溃会产生一个进程内的错误，例如，在 Linux 操作系统中，可能会产生一个 <strong>Segment Fault</strong> 错误，这个错误会产生一个信号，操作系统默认对这个信号的处理就是结束进程，整个进程都被销毁了，这样的话这个进程中存在的其他线程自然也就不存在了。</p>
<h3 id="-5">总结</h3>
<p>本讲我们介绍了线程的基本概念以及和线程相关一些常见问题，它是多线程编程入门级的概念，希望读者可以掌握它们。</p>
<h3 id="-6">分享交流</h3>
<p>我们为本专栏<strong>付费读者</strong>创建了微信交流群，以方便更有针对性地讨论专栏相关的问题（入群方式请到第 03 篇末尾查看，谢谢）。</p></div></article>