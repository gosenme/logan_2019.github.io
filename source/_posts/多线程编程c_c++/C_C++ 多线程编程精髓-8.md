---
title: C_C++ 多线程编程精髓-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本讲开始，我们讨论的主题为线程之间的同步技术。所谓线程同步技术，指的是多个线程同时操作某个资源（从程序的术语来说，这里的资源可能是一个简单的整型变量，也可能是一个复杂的 C++ 对象）。多线程同时操作资源指的是多线程同时对资源的读和写，我们需要采取一些特殊的措施去保护这些资源，以免引起一些资源访问冲突（如死锁）或者得到意料外的结果。</p>
<p>当然，最简单的资源类型应该就是整形变量了。这里给大家说个小故事：在我刚开始参加工作的那年，公司安排我开发一款即时通讯软件（IM，类似于 QQ 聊天软件），在这之前我心里也知道如果多线程操作一个整型值是要加锁的，但是当时为了图代码简便，而且在实际调试的时候，没有加锁的代码也从来没出过问题。于是我就心存侥幸了，觉得对整型值加锁真是多此一举。</p>
<p>我们的软件有类似于 QQ 这种单人聊天功能，每个用户都有一个整型的 userid，问题就出在这里。当时公司的老板和他媳妇儿也使用这款软件，问题来了：有一天早上老板在这个软件上给他媳妇发了一段亲密的话，问题是，由于多线程操作他媳妇儿的 userid 没加锁，最终变成了另外一个人的 userid，而这个 userid 恰好是我的账户。于是老板发给他媳妇儿的聊天内容就被发给我了。我当时看到聊天内容很奇怪，还回复了他一句，并且还带上了我自己的姓名……事情的结果，可想而知了，老板非常尴尬也非常生气……从那以后，老板看我的眼神都是怪怪的。我自知理亏，再也不侥幸了，凡是多线程读写整型变量都养成加锁的好习惯。</p>
<h3 id="">为什么整型变量赋值操作不是原子的</h3>
<p>那么为什么整型变量的操作不是原子性的呢？常见的整型变量操作有如下几种情况：</p>
<ul>
<li>给整型变量赋值一个确定的值，如：</li>
</ul>
<pre><code>int a = 1;
</code></pre>
<p>这条指令操作一般是原子的，因为对应着一条计算机指令，CPU 将立即数 1 搬运到变量 <strong>a</strong> 的内存地址中即可，汇编指令如下：</p>
<pre><code>mov dword ptr [a], 2
</code></pre>
<p>然后这确是最不常见的情形，由于现代编译器一般存在优化策略，如果变量 <strong>a</strong> 的值在编译期间就可以计算出来（例如这里的例子中 <strong>a</strong> 的值就是<strong>1</strong>），那么 <strong>a</strong> 这个变量本身在正式版本的软件中（release 版）就很有可能被编译器优化掉，凡是使用 <strong>a</strong> 的地方，直接使用常量 <strong>1</strong> 来代替。因此实际的执行指令中，这样的指令存在的可能性比较低。</p>
<ul>
<li>变量自身增加或者减去一个值，如：</li>
</ul>
<pre><code>a ++;
</code></pre>
<p>从 C/C++ 语法的级别来看，这是一条语句，是原子的；但是从实际执行的二进制指令来看，也不是原子的，其一般对应三条指令，首先将变量 <strong>a</strong> 对应的内存值搬运到某个寄存器（如 <strong>eax</strong> ）中，然后将该寄存器中的值自增 <strong>1</strong>，再将该寄存器中的值搬运回 <strong>a</strong> 代表的内存中：</p>
<pre><code>mov eax, dword ptr [a]
inc eax
mov dword ptr [a], eax
</code></pre>
<p>现在假设 <strong>a</strong> 的值是 0，有两个线程，每个线程对变量 <strong>a</strong> 的值递增 <strong>1</strong>，我们预想的结果应该是 <strong>2</strong>，可实际运行的结果可能是 <strong>1</strong>！是不是很奇怪？分析如下：</p>
<pre><code>int a = 0;

//线程1
void thread_func1()
{
    a ++;
}

//线程2
void thread_func2()
{
    a ++;
}
</code></pre>
<p><img src="https://images.gitbook.cn/122d6e10-cf19-11e9-9620-ed84a236482a" alt="enter image description here" /></p>
<p>我们预想的结果是<strong>线程 1</strong> 和 <strong>线程 2</strong> 的三条指令各自执行，最终 <strong>a</strong> 的值变为 <strong>2</strong>，但是由于操作系统线程调度的不确定性，<strong>线程 1</strong> 执行完指令 ① 和 ② 后，<strong>eax</strong> 寄存器中的值变为 <strong>1</strong>，此时操作系统切换到 <strong>线程2</strong> 执行，执行指令 ③ ④ ⑤，此时 <strong>eax</strong> 的值变为 <strong>1</strong>；接着操作系统切回<strong>线程 1</strong> 继续执行，执行指令 ⑥，得到 <strong>a</strong> 的最终结果 <strong>1</strong>。</p>
<ul>
<li>把一个变量的值赋值给另外一个变量，或者把一个表达式的值赋值给另外一个变量，如</li>
</ul>
<pre><code>int a = b;
</code></pre>
<p>从 C/C++ 语法的级别来看，这也是一条语句，是原子的；但是从实际执行的二进制指令来看，由于现代计算机 CPU 架构体系的限制，数据不可以直接从内存搬运到另外一块内存，必须借助寄存器中断，这条语句一般对应两条计算机指令，即将变量 <strong>b</strong> 的值搬运到某个寄存器（如 <strong>eax</strong>）中，再从该寄存器搬运到变量 <strong>a</strong> 的内存地址：</p>
<pre><code>mov eax, dword ptr [b]
mov dword ptr [a], eax 
</code></pre>
<p>既然是两条指令，那么多个线程在执行这两条指令时，某个线程可能会在第一条指令执行完毕后被剥夺 CPU 时间片，切换到另外一个线程而产生不确定的情况。这和上一种情况类似，就不再详细分析了。</p>
<p>说点题外话，网上很多人强调某些特殊的整型数值类型（如 bool 类型）的操作是原子的，这是由于，某些 CPU 生产商开始有意识地从硬件平台保证这一类操作的原子性，但这并不是每一种类型的 CPU 架构都支持，在这一事实成为标准之前，我们在多线程操作整型时还是老老实实使用下文介绍的原子操作或线程同步技术来对这些数据类型进行保护。</p>
<h3 id="windows">Windows 平台上整型变量的原子操作</h3>
<p>整型变量的原子操作是一些非常常用且实用的操作，因此 Windows 操作系统也提供了 API 级别的支持，使用这些 API 可以直接对整型变量进行原子操作，而不用借助专门的锁对象，在 Windows 平台上，它们是 <strong>Interlocked</strong> 系列函数。这里给出 Interlocked 常用的 API 的一个列表：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">函数名</th>
<th style="text-align:center;">函数说明</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">InterlockedIncrement</td>
<td style="text-align:center;">将 32 位整型变量自增 1</td>
</tr>
<tr>
<td style="text-align:center;">InterlockedDecrement</td>
<td style="text-align:center;">将 32 位整型变量自减 1</td>
</tr>
<tr>
<td style="text-align:center;">InterlockedExchangeAdd</td>
<td style="text-align:center;">将 32 位整型值增加 n （n 可以是负值）</td>
</tr>
<tr>
<td style="text-align:center;">InterlockedXor</td>
<td style="text-align:center;">将 32 位整型值与 n 进行异或操作</td>
</tr>
<tr>
<td style="text-align:center;">InterlockedCompareExchange</td>
<td style="text-align:center;">将 32 位整型值与 n1 进行比较，如果相等，则替换成 n2</td>
</tr>
</tbody>
</table>
<p>上表中仅列出了与 32 位（bit）整型相关的 API 函数，Windows 还提供了对 8 位、16 位以及 64 位的整型变量进行原子操作的 API，读者在实际使用时可以自行参考 MSDN。</p>
<p>我们以上表中 <strong>InterlockedIncrement</strong> 为例来说明这类函数的用法，<strong>InterlockedIncrement</strong>  的函数签名是：</p>
<pre><code>LONG InterlockedIncrement(LONG volatile *Addend);
</code></pre>
<p>这个函数的作用是将变量 <strong>Addend</strong> 自增 1，并返回自增后的值。</p>
<blockquote>
  <p>注意：这里的 LONG 型即 long 型，在 32 位系统中，LONG 占 4个字节。</p>
</blockquote>
<p>我们来写一个例子来验证一下：</p>
<pre><code>#include &lt;Windows.h&gt;

int main()
{
    LONG nPreValue = 99;
    LONG nPostValue = InterlockedIncrement(&amp;nPreValue);

    printf("nPreValue=%d, nPostValue=%d\n", nPreValue, nPostValue);

    return 0;
}
</code></pre>
<p>程序执行结果：</p>
<p><img src="https://images.gitbook.cn/887b1310-cf19-11e9-9cb8-a1abccba9727" alt="enter image description here" /></p>
<h3 id="c11">C++11 对整型变量原子操作的支持</h3>
<p>在 C++ 98/03 标准中，如果想对整型变量进行原子操作，要么利用操作系统提供的相关原子操作 API，要么利用对应操作系统提供的锁对象来对变量进行保护，无论是哪种方式，编写的代码都无法实现跨平台操作。例如上一小介绍的 <strong>Interlocked</strong> 系列 API 代码仅能运行于 Windows 系统，无法移植到 Linux 系统。C++ 11 新标准发布以后，改变了这种困境，新标准提供了对整型变量原子操作的相关库，即 std::atomic ，这是一个模板类型：</p>
<pre><code>template&lt;class T&gt;
struct atomic;
</code></pre>
<p>你可以传入具体的整型类型（如 bool、char、short、int、uint 等）对模板进行实例化，实际上 stl 库也提供了这些实例化的模板类型：</p>
<p><img src="https://images.gitbook.cn/FnXmmECnZEji5D_mz9OnINWxS6xs" alt="avatar" /></p>
<p>上表中仅列出了 C++ 11 支持的常用的整型原子变量，<a href="https://zh.cppreference.com/w/cpp/atomic/atomic">完整的列表读者可以参考这里</a>。</p>
<p>有了 C++ 语言本身对原子变量的支持以后，我们就可以“愉快地”写出跨平台的代码了，来看一段代码：</p>
<pre><code>#include &lt;atomic&gt;
#include &lt;stdio.h&gt;

int main()
{
    std::atomic&lt;int&gt; value;
    value = 99;
    printf("%d\n", (int)value);

    //自增1，原子操作
    value++;
    printf("%d\n", (int)value);

    return 0;
}
</code></pre>
<p>以上代码可以同时在 Windows 和 Linux 平台上运行，但是有读者可能会根据个人习惯将上述代码写成如下形式：</p>
<pre><code>#include &lt;atomic&gt;
#include &lt;stdio.h&gt;

int main()
{
    std::atomic&lt;int&gt; value = 99;
    printf("%d\n", (int)value);

    //自增1，原子操作
    value++;
    printf("%d\n", (int)value);

    return 0;
}
</code></pre>
<p>代码仅仅做了一点简单的改动，这段代码在 Windows 平台上运行良好，但是在 Linux 平台上会无法编译通过（这里指的是在支持 C++ 11 语法的 G++ 编译中编译），提示错误是：</p>
<pre><code>error: use of deleted function ‘std::atomic&lt;int&gt;::atomic(const std::atomic&lt;int&gt;&amp;)’
</code></pre>
<p>产生这个错误的原因是 “<strong>std::atomic\<int> value = 99;</strong>” 这一行代码调用的是 std::atomic 的拷贝构造函数，对于 int 型，其形式一般如下：</p>
<pre><code>std::atomic&lt;int&gt;::atomic(const std::atomic&lt;int&gt;&amp; rhs);
</code></pre>
<p>而根据 C++ 11 的规范，这个拷贝构造函数是默认使用 <strong>=delete</strong> 语法禁止编译器生成的，g++ 遵循了这个标准，<a href="https://zh.cppreference.com/w/cpp/atomic/atomic/operator%3D">参见这里</a>：</p>
<pre><code>atomic&amp; operator=( const atomic&amp; ) = delete;
</code></pre>
<p>因此 Linux 平台上编译器会提示错误，而 Windows 的 VC++ 编译器没有遵循这个规范。而对于代码：</p>
<pre><code>value = 99;
</code></pre>
<p>g++ 和 VC++ 同时实现规范中的：</p>
<pre><code>T operator=( T desired )
</code></pre>
<blockquote>
  <p>因此，如果读者想利用 C++ 11 提供的 std::atomic 库编写跨平台的代码，在使用 std::atomic 提供的方法时建议参考官方 std::atomic 提供的接口说明来使用，而不是想当然地认为一个方法在此平台上可以运行，在另外一个平台也能有相同的行为，避免出现上面说的这种情形。</p>
</blockquote>
<p>上述代码中之所以可以对 value 进行自增（++）操作是因为 <strong>std::atomic</strong> 类内部重载了 <strong>operator =</strong> 运算符，除此以外， <strong>std::atomic</strong> 还提供了大量有用的方法，这些方法读者一定会觉得似曾相似：</p>
<p><img src="https://images.gitbook.cn/Fipp5M8Dox4HWrwSxeVtjj-qkwGa" alt="avatar" /></p>
<p>上表中各个函数基本上是见名知义，读者不必死记硬背，需要时知道如何查询即可。</p>
<h3 id="-1">总结</h3>
<p>本讲介绍了整型变量的原子操作，以及为何多线程操作一个整型变量是不安全的。整型变量的原子操作是实际开发中非常常用一个技术场景，建议读者熟练掌握。</p>
<p><strong>思考题</strong>：</p>
<p>请读者想一想，整型变量的原子操作函数是如何实现的？答案可以在对应的课程微信群中获得。</p>
<p><a href="https://github.com/balloonwj/gitchat_cppmultithreadprogramming">点击这里下载课程源代码</a>。</p></div></article>