---
title: 攻克 Linux 系统编程-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>时钟对计算机系统来说非常重要，在硬件层面，时钟信号是推动 CPU 运转的动力源；在软件层面，很多非常重要的系统功能都依赖于对时间的度量和处理。</p>
<p>本节课，我们就来<strong>深入了解一下计算机系统的定时硬件</strong>，学习 Linux 中的<strong>操作系统定时器的系统调用的使用方法</strong>，并讨论一下<strong>应用层定时器的实现思路</strong>，主要包括以下几方面内容：</p>
<ul>
<li>时钟与定时器概述</li>
<li>Linux 传统间隔定时器</li>
<li>Linux POSIX 定时器</li>
<li>应用层定时器</li>
</ul>
<h3 id="101">10.1 时钟与定时器概述</h3>
<h4 id="1011">10.1.1 计算机系统中的时钟</h4>
<p><strong>时钟信号对计算机系统非常重要</strong>，CPU 中上亿个元器件都需要在时钟信号的统一节拍下协调动作才能完成需要的计算功能。</p>
<p>现实中能形象地类比 CPU 时钟的例子应该是龙舟上的鼓手，所有队员都根据鼓手打出的节拍以相同的节奏划船，才能让整条船快速行进。同时，鼓手也需要根据所有队员的体力状况打出合适的节拍，如果节拍打得太快，有队员拼劲全力也赶不上的话，整条船的行进节奏就会被打乱；如果节奏太慢，就不能充分发挥出大家的体力，达不到最快的速度。CPU 的时钟频率，就对应于龙舟鼓手打拍子的节奏，只是<strong>对一个特定的 CPU 来说，节奏是固定的</strong>。</p>
<h4 id="1012">10.1.2 计算机系统中的定时器</h4>
<p>现代的大多数定时设备，都是通过对一个具有稳定频率的信号源产生的信号的计数来实现对时间的计量，<strong>信号源的频率越稳定，计时就越精确；信号的频率越高，对时间的分辨率就越高</strong>。比如挂钟是对具有稳定摆动周期的单摆的计数，石英钟通过对神奇的石英晶体固定频率的谐振信号的计数来计时。</p>
<p>计算机系统中的时钟脉冲信号源，是用石英晶振配合不同的分频或倍频电路组成的固定频率的晶振模块，随着石英晶体加工技术和半导体制作工艺的提高，目前已经可以制作出振动基频在 GHZ 量级的晶振模块，这也成为在电子设备上进行精确的高精度计时的技术基础。</p>
<p>计算机系统中的定时器，其实就是对固定频率的时钟脉冲的计数器。</p>
<h4 id="1013linux">10.1.3 Linux 使用的时钟与定时硬件</h4>
<p>一个计算机系统中会存在多种频率的时钟信号源，对不同时钟源的多种计数方式就组成了不同功能的定时硬件。<strong>x86 系统中常见的定时器有以下几种</strong>。</p>
<ul>
<li><p><strong>计时时钟</strong>。通俗地说，就是个电子表，带在电脑主板上。主板上装的纽扣电池，就是给它供电的，以保证系统断电后系统设置的时间和日期还是正确的。这个时钟源的频率一般不会很高，通常是几 HZ 到几千 HZ 不等。这个时钟源也只会被系统用来记录和显示适合人类理解的日期和时间。</p></li>
<li><p><strong>时间戳计数器</strong>。这个计数器的时钟源是 CPU 的外部振荡信号，CPU 的内部会有一个 64 位的计数器，每收到一个时钟脉冲，这个计数器的值就会加 1。在 x86 的 CPU 上，使用 RDTSC 汇编指令就可以读到这个计数器的值。这个计数器的时间分辨率非常高，以目前的 3.2 GHZ 的 i5 桌面处理器为例，这个计数器每大约 0.3 纳秒就会加 1。在“遥远”的单核时代，这个指令曾经被用来测量程序的运行性能，但是在目前的多核时代，这种方式已经不再适用。</p></li>
<li><p><strong>CPU 本地定时器</strong>。这种定时器负责为某个特定的 CPU 产生一次性或周期性的中断信号，它也是通过对总线时钟信号的计数来实现的，在每个 CPU 核心的内部都会有一个 I/O 高级可编程中断控制器（APIC），通过控制这个控制器上计数器的累计值大小，就可以控制在该 CPU 上产生周期中断信号的间隔。</p></li>
<li><p><strong>高精度时间定时器（HPET）</strong>。这是一种由 Intel 和微软联合开发的定时芯片，它包含自己的振荡时钟源，而不再使用总线时钟信号。它能同时提供多个高时间分辨率的定时时钟，而且在硬件层面就支持产生周期性中断。一个高精度定时器芯片内至少会有 8 个频率至少为 10M HZ 的振荡时钟源，每个时钟源会驱动一个计数器，然后每个计数器又可以连接 32 组比较器和匹配寄存器，从而构成 32 个定时器，通过对比较器和匹配寄存器的编程，可以控制这些定时器的定时时间或周期。</p></li>
<li><p><strong>ACPI 电源管理定时器</strong>。这是集成在大多数计算机系统主板上的一种时钟设备，它也是一种简单的计数器，时钟源的频率大约在 3.58 MHZ 左右。它的频率是固定的，在一些通过动态调整 CPU 工作频率达到节能目的的平台上，这种定时器会充当一个固定频率的时钟源。这种时钟源通常会为系统产生非屏蔽中断（NMI）信号，可用于对 CPU 假死状态的检测。</p></li>
</ul>
<h4 id="1014">10.1.4 不同定时硬件的优先级</h4>
<p>有这么多种类型的定时硬件，Linux 系统<strong>根据每种的硬件特性和能力为它们设定了优先级</strong>，并从系统当前可用的定时硬件中选择出能力最好的作为主要的时钟源。在现代的计算机系统中，因为总线时钟的信号频率最高，并且设置成本最低，所以会把 TSC 的优先级设置为最高，其次是高分辨率定时硬件，最后是电源管理定时器。</p>
<p>在 <em>Understanding the Linux Kernel</em>（中文版《深入理解 LINUX 内核》）一书中，提到“如果系统中存在 HPET 设备，那么比起其他电路而言它总是成为首选，因为它更为复杂的结构使得功能更强”，这应该是比较古老的 Linux 内核的行为标准，在当前硬件水平上运行的 Linux 总是会<strong>使用 TSC 作为 首选时钟源</strong>。读者可以在自己的系统上用如下的方法确定系统当前的首选时钟源：</p>
<pre><code>cat /sys/devices/system/clocksource/clocksource0/current_clocksource
</code></pre>
<p>了解了时钟硬件，下面来看看在软件层面可以执行的定时操作。</p>
<h3 id="102linux">10.2 Linux 传统间隔定时器</h3>
<h4 id="1021setitimer">10.2.1 设置间隔定时器 setitimer()</h4>
<p>Linux 的传统间隔定时器设置接口是 setitimer，它可以设定在未来某个时间点到期，同时可以可选地设置之后每隔一段时间到期一次。其函数原型为：</p>
<pre><code>int setitimer(int which, const struct itimerval *new_value, struct itimerval *old_value);
</code></pre>
<p>其中 which 可以指定以下三种值。</p>
<ul>
<li>ITIMER_REAL：以真实时间进行度量，超时后会给创建进程发送 SIGALARM 信号。</li>
<li>ITIMER_VIRTUAL：以进程在用户模式下的 CPU 时间为度量，超时后给创建进程发送 SIGVTALRM 信号。</li>
<li>ITIMER_PROF：以进程在用户模式和内核模式的 CPU 总时间为度量，超时后给创建进程发送 SIGPROF 信号。</li>
</ul>
<p>itimerval 结构中包含定时器的间隔时间和开始间隔时间。</p>
<pre><code>struc itimerval {
    struct timeval it_interval;        //定时器固定间隔时间
    struct timeval it_value;           //定时器开始时间
}

struct timeval {
    time_t tv_sec;             //秒数
    suseconds_t tv_usec;       //微秒数
}
</code></pre>
<p>虽然以上参数的最小时间单位是微秒，但是定时器实际工作时的时间分辨率与当前的系统负载、内核的时钟中断周期等都有关系，通常远远达不到 1 微秒的精度。<strong>常见的 Linux 服务器的最小时间分辨率能达到 500 微秒，这样的精度对大多数的应用来说足够用了</strong>。</p>
<h4 id="1022getitimer">10.2.2 查询定时器状态 getitimer()</h4>
<p>与 setitimer 接口相对应，系统还提供了一个 getitimer 接口来获取指定定时器的当前状态，函数原型为：</p>
<pre><code>int getitimer(int which, struct itimerval * curr_value);
</code></pre>
<p>距离下一次的到期时间会被设置在 curr_value.it_value 中。</p>
<h4 id="1023alarm">10.2.3 更简单的定时接口 alarm()</h4>
<p>如果对定时器的时间精度要求不高，只需要精确到秒就足够，还可以使用另外一个更简单的接口：</p>
<pre><code>unsigned int alarm(unsigned int seconds);
</code></pre>
<p>这个接口只有一个标识到期的秒数的参数，到期时，内核会向进程发送 SIGALARM 信号。需要注意的是，<strong>在底层的实现中，这个接口与 setitimer 会共享相同的实时定时器</strong>，所以，同一个进程用这两个接口设置的定时器会相互覆盖。如果把 alarm 的参数指定为 0，则表示停用当前的 SIGALARM 定时器。</p>
<h4 id="1024">10.2.4 传统定时器的应用</h4>
<ul>
<li>为阻塞操作设置超时</li>
</ul>
<p>系统定时器的通知方式是中断，它可以打断当前阻塞的系统调用，所以，可以<strong>用它给没有提供超时参数的阻塞式系统调用提供超时检查</strong>。只需要在执行阻塞的系统调用之前启动一个定时器，当阻塞操作（比如 read）没能在规定的时间内完成时，就会被 SIGALARM 信号所打断，并返回负值标识操作没有成功完成，进一步通过 errno 确认错误原因是被打断，就可以识别出超时的情况。示例代码如下：</p>
<pre><code>static void sigHandler(int sig)
{
    //什么都不用做
}

#define BUFF_SIZE 1024
......

    //设置 SIGALARM 的信号处理函数为 sigHandler，详细代码省略
    alarm(10);         //启动一个 10 秒的定时器
    char buffer[BUFF_SIZE];
    int nread = read(STDIN_FILENO, buffer, BUFF_SIZE - 1);

    if(nread &lt; 0) {
        if(errno == EINTR) {
            //read 操作超时处理
        }else {
            //其他读取失败处理
        }
    }
    else {
        //读取成功处理
    }
</code></pre>
<ul>
<li>性能剖析</li>
</ul>
<p>你可能已经注意到，setitimer 接口的 which 参数有一个取值是 ITIMER_PROF，它会度量进程在用户模式和内核模式下的 CPU 总时间，超时后向创建进程发送 SIGPROF 信号。</p>
<p>之所以叫这个名字，就是因为它<strong>非常适合用来做性能测试</strong>。实际上，Google 开源的一个性能剖析工具 gproftools，它里面的 CPU Profiler 工作的核心就是一个这样的定时器。它会在进程运行的时间内，周期性地向目标进程发送 SIGPROF 信号，在信号处理程序中使用 backtrace 技术采样当前被中断的程序位置，通过统计一段时间内的采样数据，就可以确定程序的性能热点分布。</p>
<p>gperftools 的默认采样频率是 100 HZ，最大可以调整到 1000 HZ，也就是每毫秒采样一次。这种<strong>基于周期性采样统计的性能分析方法的好处是不需要对目标程序做任何修改</strong>，不需要埋点，只需要在编译时链接采样库，并添加合适的启动和结束采样的开关就可以了，而且给目标程序带来的附加负载非常低，甚至可以链接进最终的发布版本里去，因为它不工作的时候不会给目标进程带来任何额外的负载。</p>
<h4 id="1025">10.2.5 传统定时器的局限性</h4>
<p>从传统定时器的接口也可以看出，它的局限性体现在如下几个方面：</p>
<ul>
<li>每个进程最多只能启动三个产生不同信号的定时器，对同一类型的定时器多次调用 setitimer，会发生覆盖；</li>
<li>只能用中断的方式发出通知，而且每种定时器只能产生固定的中断信号；</li>
<li>计时器的时间精度只能精确到毫秒。</li>
</ul>
<h3 id="103posix">10.3 POSIX 定时器</h3>
<p>为了克服传统定时器的局限性，POSIX 标准组织设计了新的计时器接口和规范，使它们能提供更加灵活的计时控制，并且提供了更高的时间精度。常用的接口有：</p>
<pre><code>// 创建间隔定时器
int timer_create(clockid_t clockid, struct sigevent *evp, timer_t * timerid);

// 启动或停止定时器
int timer_settime(timer_t timerid, int flags, const struct itimerspec *value,
    struct itimerspec * old_value);

// 删除定时器    
int timer_delete(timer_t timerid);
</code></pre>
<p>这三个接口的作用是名字自解释的，就不用过多解释了，下面对出现的各个参数做稍微详细的介绍。</p>
<h4 id="1031clockid">10.3.1 clockid</h4>
<p>clockid 的可能取值包括以下几个。</p>
<ul>
<li>CLOCK_REALTIME：系统级实时时钟，用于度量真实时间，当修改系统时间时，该值会跟着发生跳跃性的变化。</li>
<li>CLOCK_MONOTONIC：恒定态时钟，在系统启动后，该类时钟就会记录相对于某一个固定时间点的相对时间，即使系统时间被手工修改，这个值也不会发生跳跃性的变化。</li>
<li>CLOCK_PROCESS_CPUTIME_ID：记录调用进程的用户和系统 CPU 总时间。</li>
<li>CLOCK_THREAD_CPUTIME_ID：记录调用线程的用户和系统 CPU 总时间。</li>
</ul>
<h4 id="1032sigevent">10.3.2 sigevent</h4>
<p>sigevent 是一个复杂的联合结构体，其中可以指定定时器超时的通知方式有如下两种：</p>
<ul>
<li>用指定的信号以中断方式通知</li>
<li>执行指定的线程函数</li>
</ul>
<p>该结构详细的定义在 timer_create() 的帮助手册中有详细的解释，这里就不展开了。</p>
<h4 id="1033timerid">10.3.3 timerid</h4>
<p>timer_create() 如果创建成功，会返回 0 值，同时把创建的定时器的标识符设置在 timerid 指定的存储空间内，timer_settime() 和 timer_delete() 接口使用 timerid 参数来标识要操作的定时器。</p>
<h4 id="1034flags">10.3.4 flags</h4>
<p>timer_settime() 接口的 flags 参数可以有两个不同的取值，0 表示设置在 value 字段中的超时时间是相对调用点的相对值；而如果将 flags 设置为 TIMER_ABSTIME，则表示超时时间是从 0 值开始的绝对时间。在需要频繁处理中断而需要重启未到期的定时器的系统中，使用绝对时间能避免出现定时器的嗜睡现象。</p>
<h4 id="1035valueold_value">10.3.5 value &amp; old_value</h4>
<p>itimerspec 结构类似于之前的 itimerval，不同之处在于最小时间的精度能达到纳秒：</p>
<pre><code>struct itimerspec {
    struct timespec it_interval;   //周期性定时器的重复间隔
    struct timespec it_value;      //首次到期的时间
};

struct timespec {
    time_t tv_sec;                //秒数
    long   tv_nsec;               //纳秒数
};
</code></pre>
<h4 id="1036posix">10.3.6 POSIX 定时器的优势</h4>
<p>可以看到，相对于传统定时器，POSIX 定时器在如下几个方面做了增强：</p>
<ul>
<li>一个进程可以支持多个同类定时器；</li>
<li>可以自定义定时器到期时的中断通知信号；</li>
<li>可以支持在定时器到期时执行线程函数，所以超时处理函数不需要遵循信号处理函数的编写标准，因而可以更加灵活；</li>
<li>支持精确到纳秒的时间精度。</li>
</ul>
<h3 id="104">10.4 应用层定时器</h3>
<p>虽然系统级的定时器可以充分利用底层的定时硬件，达到很高的时间精度，但是<strong>对一些需要频繁创建和维护大量定时器的应用来说，直接使用系统定时器并不合适</strong>。比如大型的多人在线游戏服务器，取决于同时在线的玩家人数，可能需要同时维护上万甚至更大量级的定时器，如果完全使用系统定时器，很快就会让系统变得不堪重负。而且，因为系统定时器的到期通知方式是信号或者线程函数，会给超时处理函数的编写带来一些额外的负担。因此，<strong>很多需要大量使用定时器的应用都会自己实现应用层的定时器</strong>。</p>
<p>在应用层高效率地维护大量定时器的核心，在于选择高效的数据结构维护所有的定时器，尽量减少定时器的添加移除以及遍历操作的性能开销。要实现这一点，我们或许可以借鉴一下 Linux 内核对动态定时器的维护方式。</p>
<h4 id="1041linux">10.4.1 Linux 内核维护动态定时器</h4>
<p>在 Linux 内核中，动态定时器的超时检查是在时钟中断处理程序中进行的，内核编译期间就会确定一个时钟中断的频率，大多数服务器的默认设置是 100 Hz，也就是每 10 ms 触发一次时钟中断处理程序，动态定时器的超时检查就是在该中断处理程序中执行的。</p>
<p>为了尽量减少每次中断处理程序中遍历检查的定时器数量，Linux 内核中<strong>采用了精巧的数据结构来组织所有的动态定时器</strong>。</p>
<p>Linux 内核中把不同到期时间的定时器组织在不同的组中，根据到期时间的长短，划分成了五个不同的组，每个组包含若干个 Bucket，每个 Bucket 中保存若干个用链表链接起来的定时器，如下图所示：</p>
<p><img src="https://images.gitbook.cn/a2165730-1ccc-11e9-b5b7-abf0ec0c666a" alt="" /></p>
<p>其中，tv1 指向的组内包含 256 个 Bucket，依次保存到期时间在 0 到 255 个时钟周期之间的所有定时器；tv2 到 tv5 指向的组每个都包含 64 个 Bucket，存放的定时器的到期时间时钟周期数请见如下说明。</p>
<ul>
<li>tv2：256 到 2 的 14 次方 - 1。</li>
<li>tv3：2 的 14 次方 到 2 的 20 次方 - 1。</li>
<li>tv4：2 的 20 次方 到 2 的 26 次方 - 1。</li>
<li>tv5：2 的 26 次方 到 2 的 32 次方 - 1。</li>
</ul>
<p>有了这样的存储结构，内核在每次收到时钟中断信号时，每次检查执行 tv1 组内的一个 Bucket 就可以了，每次信号中断处理都把索引位置加 1，当 tv1 的所有 256 个项都处理完成之后，将第二组中一个 Bucket 中的所有定时器一次补充到 tv1 组内的对应位置，并增加 tv2 的位置索引。</p>
<p>因为 tv2 中每个 Bucket 中的定时器可能有 256 个不同的到期时间，所以第二组内每个项的数据就足以填充整个第一组，后续各组也有同样的规律，tv(n) 组内的每个项都刚好足以填充整个 tv(n-1) 组。</p>
<p><strong>用这样的方式，Linux 内核用非常紧凑的数据结构，实现了高效的定时器管理</strong>。</p>
<h4 id="1042">10.4.2 应用层定时器管理</h4>
<p>受到 Linux 内核中这种设计的启发，应用层可以用类似的策略实现高效的定时器管理，而且，<strong>在应用层可以考虑用更大的内存换取更高的效率</strong>。比如，对上面提到的大型多人在线游戏的服务器来说，定时管理可以采用这样的策略：</p>
<ul>
<li>游戏每帧的时间间隔对应 Linux 内核中的中断周期，把所有定时器以帧间隔为时间单位组织在不同的 Bucket 中，如果服务器按照 60 帧的帧率执行更新逻辑，那每帧的间隔就是 16.6 毫秒；</li>
<li>给 tv1 组分配更大的内存空间，比如，考虑到游戏中用到的定时器大多数都在几秒到几分钟的量级，可以考虑把 tv1 数组扩充到 36000 个 Bucket，也就是超时时间在 10 分钟之内的定时器都可以直接定位到目标 Bucket；</li>
<li>给 tv2 组分配 14400 个 Bucket，每个 Bucket 的时间范围是 10 分钟，所以，tv2 可以包含超时时间在 100 天以内的所有定时器</li>
<li>tv3，tv4，tv5 就都不需要了，超过 100 天时长的定时器都单独链接在一个超长定时器 Bucket 里面就可以了。</li>
</ul>
<p>这样组织定时器之后，每帧的更新逻辑只需要简单地取出 tv1 组内的一个 Bucket 下的定时器，执行并移除它们，然后增加索引位置就可以了。每十分钟才需要检查一次 tv2 数组内的一项，把这里的定时器填充到 tv1 的对应位置。因为绝大多数定时器的超时时间都不超过几分钟，所以处理 tv2 组内一项的开销会非常有限。然后每 100 天检查一次超长定时器 Bucket，把剩余到期时间在 100 天以内的计时器填充到 tv2 或 tv1 中。</p>
<h3 id="105">10.5 总结</h3>
<p>本节课我们详细<strong>讲解了 Linux 系统中的定时器</strong>，介绍了 <strong>Linux 中传统定时器和新的 POSIX 定时器的使用方法</strong>，并<strong>对比了它们各自的优缺点</strong>，然后<strong>探讨了 Linux 内核中对动态定时器的管理策略</strong>，一次启发我们设计了一套高效的应用层定时器管理算法。</p>
<p>希望通过本课的内容，读者可以对系统定时器有更加透彻的理解，能够更加自如地使用定时器。</p>
<h3 id="106">10.6 答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
</blockquote></div></article>