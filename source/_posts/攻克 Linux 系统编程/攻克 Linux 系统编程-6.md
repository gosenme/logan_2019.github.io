---
title: 攻克 Linux 系统编程-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>目前，多线程模型非常常见，从终端应用到大型服务器程序都会大量使用。在本文中，我们就来<strong>深入探究下 Linux 线程的内部细节</strong>，让读者对线程的把控更加胸有成竹，得心应手，主要包括以下几方面内容：</p>
<ul>
<li>线程的内存布局</li>
<li>线程的实现方案</li>
<li>内核中的用户线程与进程</li>
<li>线程的同步</li>
<li>线程的连接和分离</li>
<li>线程的取消</li>
<li>线程特有数据</li>
</ul>
<h3 id="51">5.1 线程的内存布局</h3>
<p>一个进程可以包含多个线程。多个线程可以并发执行，从而提高系统整体吞吐量，提供更好用户体验。<strong>一个进程中的多个线程共享大多数的进程数据</strong>，包括代码段、初始化数据段、未初始化数据段、堆内存段及动态链接内存段等。比较规整的多线程程序的内存布局如下图所示（实际上，线程栈的位置遵循共享库加载、映射共享内存和线程创建的排列顺序，有时可能会有所变化）：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/a3281330-14a6-11e9-8606-ef049b6ac94d" width="500px" />
</div>
<p>每个线程的代码<strong>均放置在 ELF 文件的 .text 段中</strong>，会在进程启动时加载到可执行内存段内。当进程在运行中动态创建线程时，每个线程特有的数据只是自己的栈，其他数据与所在进程的其他线程共享。因此，相对进程，<strong>线程有以下几点优势</strong>。</p>
<ul>
<li>线程的创建更加快速。相比 fork() 一个子进程，线程创建不需要复制内存页表和文件描述符表等多种进程属性。有数据显示，创建线程比进程要快至少 10 倍。</li>
<li>线程之间的数据共享更加方便。因为它们都在同一进程的虚拟地址空间之内，所有数据相互之间都是可见的，只要处理地足够仔细，甚至可以互相共享各自线程栈内的数据。</li>
<li>同一进程内的线程之间，上下文切换开销更小，因为它们之间有很多相同的内核信息。</li>
</ul>
<p>但也正因如此，<strong>线程相比进程有以下劣势</strong>。</p>
<ul>
<li>鲁棒性稍差。一个线程的异常行为（如空指针访问）会连累进程内的所有线程。</li>
<li>所有线程共享一块堆空间。64 位应用的进程虚拟空间可以达到
128T，所以可以不理会这个限制；但是对 32 位应用，总的用户空间虚拟内存总量只有 3GB，所以这个缺点表现得尤为明显。</li>
</ul>
<h3 id="52">5.2 线程的实现方案</h3>
<p>理论上，<strong>线程的实现模型有以下三种</strong>。</p>
<ul>
<li>多对一模型：线程创建、调度和同步均在进程的用户空间内实现，内核只能看到单一进程。该模型的优点在于线程操作的速度非常快，因为无需切换到内核态。缺点则是一个进程中的多个线程无法被分配到多个 CPU 上并发执行。</li>
<li>一对一模型：每个线程都是一个内核资源调度实体，由内核进行 CPU 的分配和调度，线程同步操作也通过内核中的系统调用实现。该模型能够实现同一进程内的多个线程并行执行，同时因为要切换到内核态，调度和同步操作的开销要大一些。</li>
<li>多对多模型：结合了以上两种模型的优点，每个进程可以拥有多个内核资源调度实体，每个内核调度实体又可以关联多个用户空间线程，通过合理规划用户线程和内核线程，应用可以获得最佳性能。但该模型最大的缺点是实现过于复杂，用户空间和内核空间都需要相应的线程库实现。</li>
</ul>
<p>在 Linux 中，<strong>目前主流的线程实现方案是 NPTL（Native POSIX Thread Library）</strong>，使用的是一对一模型，最早在 Linux 2.6 内核内获得完整支持。</p>
<p>在历史上，最初的 Linux 线程实现称为 LinuxThreads，选择的也是一对一模型，但该实现受限于当时内核的一些功能特性，有诸多与 POSIX 线程标准相违背的地方，这也是 NPTL 后来努力改进的方向。</p>
<p>在 NPTL 设计早期，也曾经考虑过采用多对多模型，但由于对内核的修改范围过大而被否决。此外，由 IBM 提议的 NGPT（Next Generation POSIX Threads）也是采用多对多模型，性能明显优于 LinuxThreads，曾被认为非常有可能成为 LinuxThreads 的继任者。</p>
<p>但是后来，NPTL 的开发者调整了设计方法，仍然<strong>采用一对一模型</strong>，再配合对内核做一些修改，<strong>能实现优于 NGPT 的性能</strong>。所以，NPTL 发布之后，NGPT 的开发也宣布停止。</p>
<p>NPTL 实现不是一个完全独立的内核特性，为了实现高效的线程支持，Linux 内核的其他相关部分也<strong>做了大量修改和优化，包括但不限于以下几个方面</strong>：</p>
<ul>
<li>改进了线程组的实现；</li>
<li>引入 Futex，将其作为一种通用的同步机制；</li>
<li>增加了对线程本地存储的系统调用的支持；</li>
<li>重写了内核调度程序，以实现更有效的调度，以及支持更多的线程；</li>
<li>扩展了系统调用 clone()。</li>
</ul>
<h3 id="53">5.3 内核中的用户线程与进程</h3>
<p>在目前的 Linux 内核实现中，用户线程和进程对应着同样的内核数据结构。实际上，对内核而言，进程和线程的<strong>区别仅仅是一些属性（如虚拟内存、打开的文件、信号处理函数、进程 ID 等）的共享程度不同而已</strong>，在资源分配和调度上，它们并没有本质区别。</p>
<p>clone() 是创建线程的底层系统调用，同时也为进程创建提供底层支持。其函数原型为：</p>
<pre><code>int clone(int (*func)(void *), void * child_stack, int flags, void * func_args, ...)
</code></pre>
<p>其中，参数 flags 可以指定进程复制时与父进程共享的资源。在线程创建函数中，传递的 flags 如下所示：</p>
<pre><code>CLONE_VM | CLONE_FILES | CLONE_FS | CLONE_SIGHAND | CLONE_THREAD | CLONE_SETTLS | CLONE_PARENT_SETTID | CLONE_CHILD_CLEARTID | CLONE_SYSVSEM
</code></pre>
<p>也就是说，新建的实体与父进程共享同一份虚拟内存页、同一个打开的文件描述符表、文件系统信息、信号处理函数表等，且新创建的实体会被放在创建者的线程组内（CLONE_THREAD）。相比之下，用 fork() 创建进程时的 <strong>flags 值仅包含 SIGCHILD</strong>。这也是<strong>线程和进程的本质区别</strong>。</p>
<h3 id="54">5.4 线程的同步</h3>
<p>相比多进程模型，多线程模型<strong>最大的优势在于数据共享非常方便</strong>，同一进程内的多个线程可以使用相同的地址值访问同一块内存数据。但是，当多个线程对同一块内存数据执行“读−处理−更新”操作时，会由于线程的交叉执行而造成数据的错误。</p>
<p>例如以下代码段，当 thread_func() 同时在多个线程中执行时，更新到 glob_value 中的值就会互相干扰，产生错误结果。</p>
<pre><code>#define LOOP_COUNT   1000000
int glob_value = 0;

void * thread_func(void * args)
{
    int counter = 0;
    while(counter++ &lt; LOOP_COUNT)
    {
        int local = glob_value;
        local++;
        glob_value = local;
    }
}
</code></pre>
<p><font color="#F39800">解决这类问题的关键在于，当一个线程正在执行“读−处理−更新”操作时，保证其他线程不会中途闯入与其交叉执行。</font>不可被打断的执行序列称为临界区，保证多个线程不会交叉执行同一临界区的技术称为线程同步。</p>
<h4 id="541">5.4.1 互斥锁的使用</h4>
<p><strong>最常用的线程同步技术是互斥锁</strong>，Linux 线程库中的相关函数有：</p>
<pre><code>int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
</code></pre>
<ul>
<li>pthread_mutex_lock() 负责在进入临界区之前对临界区加锁；</li>
<li>pthread_mutex_unlock() 负责在执行完临界区处理时给临界区解锁。</li>
</ul>
<p>当某个线程试图给一个已经处在加锁状态的临界区再次加锁时，该线程就会被临时挂起，一直等到该临界区被解锁后，才会被唤醒并继续执行。如果同时有多个线程等待某个临界区解锁，那下次被唤醒的进程取决于内核的调度策略，并没有固定的顺序。</p>
<p>静态分配的 mutex 变量在使用之前应该被初始化为 PTHREAD_MUTEX_INITIALIZER，而动态分配的 mutex 需要调用 pthread_mutex_init() 进行初始化，且只被某个线程初始化一次，可以利用 pthread_once() 函数方便完成。</p>
<pre><code>int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
int pthread_once(pthread_once_t *once_control, void (*init_routine)(void));
</code></pre>
<p><font color="#F39800">多个线程在临界区上的执行是串行的，开发者应该尽量减少程序在临界区内的停留时间，以提高程序的并行性。</font>因此，临界区不应该包含任何非必须的逻辑，以及任何可能带来高延迟的 IO 等操作。</p>
<h4 id="542">5.4.2  互斥锁的保护范围和使用顺序</h4>
<p>对互斥锁加锁的不恰当使用会造成线程的死锁，比如<strong>下面这两种情况</strong>。</p>
<ul>
<li><p>典型的情况是，两个线程执行时都需要锁定互斥锁 A 和 B，在一个线程中，锁定顺序是先锁定 A，后锁定 B，而另一个线程的锁定顺序是先锁定 B，再锁定 A。这种情况下，当一个线程已经锁定了 A 而另一个线程恰好锁定了 B 时，双方因互相争用对方已锁定的互斥锁，谁也不让步，而陷入死锁状态。</p></li>
<li><p>另一种情况是，一个线程已经锁定了互斥锁 A，但在其后的处理逻辑中试图再次锁定 A，这时该线程会让自己陷入睡眠状态，再也等不到被唤醒的时候。</p></li>
</ul>
<p>为了避免出现死锁问题，<strong>开发者需要仔细规划互斥锁保护范围和使用顺序</strong>，或者使用另外两种变体的锁定函数，如下所示：</p>
<pre><code>int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_timedlock(pthread_mutex_t *restrict mutex, const struct timespec *restrict abs_timeout);
</code></pre>
<p>它们可以在锁定失败后立即返回，或在一段超时时间后返回，应用可以处理这种错误情况，而避免陷入无限的死锁中。</p>
<p>在 Linux 中，<strong>实现互斥锁采用的是 Futex（Fast Userspace Mutex）方案</strong>。在该实现中，只有发生了锁的争用才需要陷入到内核空间中处理，否则所有的操作都可以在用户空间内快速完成。在大多数情况下，互斥锁本身的效率很高，其平均开销大约相当于几十次内存读写和算数运算所花费的时间。</p>
<h3 id="55">5.5 线程的连接和分离</h3>
<p>新创建的线程和进程一样，也需要被连接以监听其退出状态，否则也会变成僵尸线程。背后原因与进程一样，其退出之后，内核会为它保留退出状态数据，直到有人取走为止。连接线程的库函数如下所示：</p>
<pre><code>int pthread_join(pthread_t thread, void **retval);
</code></pre>
<p>进程连接与线程连接<strong>在以下几个方面存在一些区别</strong>：</p>
<ul>
<li>任何线程都可以监听一个指定线程的退出，而不需要是创建该线程的线程；</li>
<li>线程连接函数只能连接一个指定 ID 的线程，而不能像进程一样监听任意线程的退出；</li>
<li>线程创建之后可以使用分离函数设置其不需要等待被连接，这种情况下，线程结束之后会被自动清理。</li>
</ul>
<p>设置线程分离的函数为：</p>
<pre><code>int pthread_detach(pthread_t thread);
</code></pre>
<p>处于分离状态的线程，无法被任何线程执行连接获取其状态，也无法再返回到可连接状态。</p>
<h3 id="56">5.6 线程的取消</h3>
<p><font color="#F39800">运行中的线程可以被其他线程主动取消，这个特性在很多场景中非常有用。</font></p>
<p>比如，很多带 GUI 的应用都会对长时间运行的后台任务<strong>设置一个取消按钮</strong>，还有一些服务器进程可能会<strong>动态调整运行中的工作线程数量</strong>。这些都<strong>可以用线程取消函数来实现</strong>：</p>
<pre><code>int pthread_cancel(pthread_t thread);
</code></pre>
<p>同时，对退出线程状态和类型的掌控，可以进一步控制它们响应取消请求的处理过程。这两个标志可以通过下面两个函数来设置：</p>
<pre><code>int pthread_setcancelstate(int state, int *oldstate);
int pthread_setcanceltype(int type, int *oldtype);
</code></pre>
<p>状态类型分为启用、关闭两种。关闭状态下的线程不可被取消，开启状态下的线程可进一步设置取消类型，在任一点取消，以及在预定的取消点取消。取消点是内核在一些函数实现中埋下的点，这些函数都是有可能造成进程阻塞或触发 IO 行为的函数，如 sleep()、wait()、fsync() 等。</p>
<p><strong>合理控制线程的取消行为，是保证数据一致性、逻辑完整性不被破坏的必要手段</strong>。更多细节可查看系统帮助手册了解。</p>
<h3 id="57">5.7 线程特有数据</h3>
<p>线程概念出现之前，程序中的变量按照有效性范围可分为全局变量、静态变量和局部变量。全局和静态变量在一个程序内的多个函数间共享，而局部变量只在某个函数内有效。</p>
<p>当线程概念引入之后，对变量有效范围的需求又增加了一层，就是在某个线程内的全局和静态变量。开发者希望一些变量可以<strong>在某个线程内的多个函数间共享</strong>，同时又不希望多个线程之间互相影响。这就是<strong>线程特有数据要解决的问题</strong>。正如本课程前面提到的，系统调用中常用的全局 errno 就是线程特有数据的典型应用。</p>
<p>实现线程特有数据还有另外一个原因。线程引入之前，很多库函数的设计都未考虑线程安全性。这些库函数如果均通过实现全新接口提供线程安全版本，所有使用这些库的应用都需修改用到的函数以支持多线程特性。而<strong>有了线程特有数据的支持</strong>，这些库就可以保持对外接口的同时，在内部实现多线程数据安全特性。虽然函数运行效率可能稍低一些，但可为大量应用<strong>省去不少修改源程序的工作量</strong>。</p>
<p>创建线程特有数据 API 的函数为：</p>
<pre><code>int pthread_key_create(pthread_key_t *key, void (*destructor)(void *));
</code></pre>
<p>该函数只在主线程或某个线程中执行一次，可以放在 pthread_once() 函数中执行。destructor 是一个析构函数，用来创建标识某个线程本地存储的 key。key 所对应的内存空间，需在每个线程中具体分享。这里的析构函数注册完成后就是用来在每个线程退出时释放各自内存空间的。</p>
<p>在线程中设置和获取 key 所对应内存空间的函数如下所示：</p>
<pre><code>int pthread_setspecific(pthread_key_t key, const void *value);
void * pthread_getspecific(pthread_key_t key);
</code></pre>
<p>参数 value 可以是一个指向内存区域的指针，也可以是一个标量值，具体选用哪个由线程自己决定。在 Linux 中，最多可定义 1024 个线程特有数据的 key 值。如果考虑程序的可移植性，所定义的 key 数量不应超过 128 个。当确实需要更多线程特有数据时，可将多个值放置在一个结构中，从而减少 key 的数量。</p>
<h3 id="58">5.8 总结</h3>
<p>在本文中，我们深入探讨了 Linux 线程的诸多内部细节，包括在<strong>用户空间的内存排布、Linux 线程的实现方式，互斥锁实现临界区保护的原理</strong>等。另外，还讨论了 <strong>POSIX 线程提供的一些基础功能、线程连接和分离、线程取消、使用线程特有数据</strong>等。希望通过本文的学习，读者可以更好地理解线程，从而更加自如地控制线程。</p>
<h3 id="59">5.9 答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
  <p><strong>参考资料</strong></p>
  <p>GitHub 源代码网址：</p>
  <p><a href="https://github.com/boswelyu/GitChatLesson-LinuxDevInDepth/tree/master/Lesson5">https://github.com/boswelyu/GitChatLesson-LinuxDevInDepth/tree/master/Lesson5</a></p>
</blockquote></div></article>