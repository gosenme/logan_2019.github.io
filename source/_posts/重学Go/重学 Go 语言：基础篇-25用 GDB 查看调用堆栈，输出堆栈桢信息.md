---
title: 重学 Go 语言：基础篇-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="gdb">用 GDB 查看调用堆栈，输出堆栈桢信息</h3>
<pre><code class="c language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

__attribute__((noinline)) void info(int x)
{
    printf("info %d\n", x);
}

__attribute__((noinline)) int add(int x, int y)
{
    int z = x + y;
    info(z);

    return z;
}

int main(int argc, char **argv)
{
    int x = 0x100;
    int y = 0x200;
    int z = add(x, y);

    printf("%d\n", z);

    return 0;
}
</code></pre>
<p>上面这段代码分配了两个变量 x 和 y，调用 add 函数，函数内部调用 info 函数用于输出结果。执行下面语句编译。</p>
<pre><code class="bash language-bash">$ gcc -g -O0 -o test test.c #编译，去掉优化
</code></pre>
<h3 id="gdb-1">使用 GDB 调试</h3>
<pre><code class="bash language-bash">$ gdb test
$ b main #符号名上加上断点，main 函数加上断点
$ b add #add 函数加上断点
$ b info #info 函数加上断点
$ info breakpoints #查看断点，一共有三个断点
$ r #执行，这时在 main 函数上中断了
$ bt #查看当前调用堆栈，其中栈帧 #0 只为 main 函数分配了内存，#0 表示自己
$ l main #查看 main 代码 19 行中断内容，意味着 19 行还没有执行
$ c #继续执行,这时在 add 函数上中断
$ bt #查看当前调用堆栈，有两个，下面是 main 函数，上面是 add 函数，#0 表示自己，#1 表示谁调用你的
$ l main #查看 main 代码 21 行栈帧内容
$ l add #查看 add 代码 11 行中断内容，意味着 11 行还没有执行
$ info frame #输出当前栈帧里面相关数据 rip 表示 IP 寄存器中的值
$ info args #输出当前参数
$ info locals #输出当前局部变量
$ frame 1 #查看上一级栈帧数据，切换帧 1
$ info frame #输出当前栈帧里面相关数据，这时显示 main 函数的栈帧内存
$ down 1 #切换栈帧
$ up 1 #向外切换栈帧，谁调用你的
</code></pre>
<h3 id="ip">IP 寄存器的用途</h3>
<p>当执行 <code>callq &lt;add&gt;</code> 指令的时候，IP 寄存器应该保存下一行指令位置，因为这样才能恢复到 main 函数的状态。但是进入 add 函数里面的时候，IP 寄存器其实是指向 add 方法里面的地址，所以为了 add 函数在执行结束时可以恢复到下一行，必须要把 IP 寄存器里面的值保存起来。接下来我们看下怎么样保存 IP 寄存器。</p>
<pre><code class="bash language-bash">$ gdb test
$ b main #符号名上加上断点，main 函数加上断点
$ r #执行，这时在 main 函数上中断了
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
$ p/x $rip #IP 寄存器保存的是下一行指令的位置，使用p/x查看
$ ni #单步执行
$ p/x $rip #再看 IP 寄存器值，和上面不一样了，永远指向下一行指令的地址。
</code></pre>
<p>main 函数准备调用 add 函数的时候，它需要保存哪些值？最简单的方法是把这些值保存到栈上面，首先把 IP 寄存器压到栈上，然后 BP、SP 全部保存起来，保存完了以后把 BP 指向栈顶，执行 add 方法，SP 指向 add 方法的栈顶，这时 BP 就是 add 方法的栈底。</p>
<p>当 add 方法执行完了以后，只需要把栈里的那些值 pop 到指定的寄存器里面去，就可以恢复到 main 函数的状态了。只要 pop 出来，就可以恢复 BP、SP、IP 的值，这样就可以完全地把 main 函数当时执行的状态恢复出来。</p>
<p>所以把这些寄存器保存起来的方式称之为现场保护，pop 出来就叫做现场恢复。</p>
<pre><code class="bash language-bash">$ b *0x0000000000000400597 #下一行 call &lt;add&gt; 函数打断点
$ c #执行
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
$ info registers #记录一些值，rbp=e680，rsp=e660，rip=059c
$ si #进入 add 函数里
$ disass #反汇编
</code></pre>
<h3 id="">相关汇编指令</h3>
<ul>
<li>call(push ip)</li>
<li>leave(mov sp,bp;pop bp)</li>
<li>ret(pop ip)</li>
</ul>
<p>call 指令把 IP 的值先入栈，执行 call 指令的汇编代码如下：</p>
<pre><code class="bash language-bash">push %rbp #把 BP 寄存器入栈保存起来
mov %rsp,%rbp #把 SP 里面的值赋值给 BP，就是 BP 指向 SP
sub $0x20,%rsp #把 SP 减去 20，地址从高往低分配的，就是 SP 指向上面位置，20 的空间就是 add 函数空间
</code></pre>
<p>在调用 add 函数之前做了几件事，第一件事 call 指令除了调用函数之外，首先把 IP 保存起来，然后在函数头部把 BP 保存起来。这与根据不同的函数调用不同的编译器也有关系。</p>
<p>对于 GCC 来说，如果保存这两个足够用就没问题，因为它的编译器会分析需要保存哪些状态，这是编译器来处理的。现在起码知道 IP、BP 是被保护起来的。</p>
<p>接下来执行：</p>
<pre><code class="bash language-bash">$ b *0x0000000000000400550 #下一行 mov %edi,-0x14(%rbp) 打断点
$ c #执行
$ p/x $rip #这时候 IP 是指向 add 函数里面的值，IP 指向 0x400550，因为这时候执行的是 add 函数的逻辑，所以你得告诉 IP 寄存器接下来执行什么。
$ b *0x000000000000040056e #下一行 leaveq 打断点
$ c #执行
</code></pre>
<p>leave 和 ret 指令完成现场恢复，leave 指令其实是一个复合指令。不是所有时候都会使用 leave 有些时候可能直接用 pop 这样的指令，在最后会用相关的指令完成现场恢复。复合指令实际上需要执行几次操作，<code>mov sp,bp</code> 首先它把 SP 指向当前 BP 的位置，就是把 add 函数所需要的内存空间释放掉，<code>pop bp</code> 把 BP pop 出来，因为 BP 是当时保存的，BP 就回到原来的位置，接下来 SP 调整位置。</p>
<p>ret 指令，<code>pop ip</code> 把 IP 寄存器 pop 出来，这样 IP 就指回了原来的位置，SP 继续调整位置指向 main 函数顶部了。所以 BP、SP、IP 都恢复了就完成了现场恢复的过程。</p>
<pre><code class="bash language-bash">$ info registers #查看寄存器值，rbp，rsp，rip
$ info frame #查看当前栈桢
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
$ ni #单步执行下一行 leave
</code></pre>
<p>执行这条指令，刚刚说过恢复 SP、BP 的值，下面看下是否恢复：</p>
<pre><code class="bash language-bash">$ info registers #查看寄存器值，rbp=e680，rsp=e658，rip
$ set disassembly-flavor intel #设置intel样式
$ disass #反汇编
$ info frame #查看当前栈桢
$ p/x $rbp #e680
$ ni #单步执行下一行 ret
$ disass #反汇编 恢复到 main 函数状态
$ info registers #查看寄存器值，rbp=e680，rsp=e660，rip=059c
$ p/x $rip #IP 寄存器 059c
</code></pre>
<p>编译器会自己处理需要哪些数据需要去保护，对于 GCC 来说，在栈上都是基于 BP 寄存器来寻址的，所以关键要保存 BP 和 IP 这两个状态，因为把栈上数据全部去掉以后 SP 自然就恢复了。</p>
<p>Go 语言可能不是基于 BP 来寻址，是基于 SP 来寻址的，它就需要把 SP 保护起来，而 BP 就不管了。不同的编译器不同的做法，因为 GCC 栈上的寻址都是基于 BP 做减法，因为 BP 在下面高位栈底的位置，往上寻址就减去偏移量就可以了，这是 GCC 基于 BP 寄存器做减法。</p>
<p>比如 add 函数空间，BP 在栈底，高位地址。比如在 add 函数上存放 x=100，就得把 BP 减去一个偏移量 0x8，那么 BP-0x8 就是 x 的地址。要么通过 BP 做减法寻址，要么通过 SP 做加法寻址。总归选择一个作为基准。不同的编译器不同的实现方式。</p>
<h3 id="-1">总结</h3>
<p>函数调用的时候，首先函数是被线程执行的，这个线程要执行函数调用必须要内存分配，内存分为两块，一块称为堆，一块称为栈。每个线程都会有自己的栈内存，栈内存是个大整块，调用的时候通过 BP 或者 SP 这两个寄存器来维持当前函数需要操作哪块内存，操作完了以后，直接来调整 BP 或者 SP 寄存器的位置，就可以把调用函数的所分配的栈桢空间释放掉。</p>
<p>栈上的内存释放了以后，那个内存还在，因为整个栈内存是个整体。这就是整个一大块，我们只不过就是调用时候通过两个寄存器，来确定当前操作的时候在这一大块中操作哪一个区域。</p>
<p>栈上内存用 BP 和 SP 来操作一整块内存的一个区域，用完之后把 SP 寄存器指回去，那块空间接下来调用其它函数时候进行复用。整个栈内存是一大块，是一整块，它没有说释放某块内存这样的一个说法。除非就有一种可能，就是把整个栈空间释放掉。</p>
<p>在堆上我们申请了一段内存，不用的时候可以把这块释放掉，因为在一个函数里面可以多次调用堆内存分配，然后可以分块释放。栈上没有内存释放这种说法。所以这就有个好处在栈上只需要调整两个寄存器 BP、SP 的位置，就可以决定这个内存当前是正在用，或者说可以被其它函数调用来覆盖掉。</p>
<p>所以有这样一个说法，<strong>我们尽可能把对象分配到栈上</strong>。因为不需要执行释放操作。现场恢复时候只需要调整寄存器，那块内存就变得可复用状态了。但是在堆上必须要释放，在栈上的效率显然是要高很多。而且栈这种特性就决定了它是有顺序操作的机制，所以它的效率就高很多。在堆上分配时候要么手动释放，要么由垃圾回收器来释放。所以我们在栈上分配的时候：</p>
<ul>
<li>效率比较高；</li>
<li>不会给垃圾回收器带来负担。</li>
</ul>
<p>每个函数调用的时候，都会在栈上用两个寄存器划出一个区域来存储参数、返回值、本地变量类似这样的一些内容，这个区域我们称之为叫栈桢。那么多级调用时候所有的栈桢串在一起，我们称之为调用堆栈。</p>
<p>那么究竟有哪些东西分配在栈上呢？比如说在函数里面 <code>x=10</code> 这种东西默认情况下肯定分配在栈上，<code>*p=malloc()</code> 这个时候这东西在堆上还是在栈上呢？这时候实际上有两块内存，第一 malloc 的确是在堆上分配一个内存空间，这个内存空间分配完了之后得有个指针指向它。</p>
<p>除了堆上的内存块，还有个指针变量，这个指针变量可能是在栈上。指针本身是个标准的变量，它是有内存空间的，因为可以给指针赋值的，能给它赋值肯定是个对象，没有对地址赋值这样一个说法，地址肯定不能赋值的。所以指针和地址不是一回事。指针是一个标准的变量，里面存了地址信息而已。</p>
<p>复合对象是不是分配在堆上？也未必，这得看不同的语言对复合对象怎么定义了。比如说结构体算不算复合对象？数组算不算复合对象？默认情况在栈上分配没有问题，当然里面可以用指针指向堆上其它的地址。当里面有指针指向别的对象的时候，这个指针本身它依然是在栈上的。</p>
<p>比如说有个复合对象结构体，有个 x 和一个指针 p，指针 p 指向堆上一个内存对象，堆上内存对象不属于结构体本身的内容。因为只有这个指针属于这个结构体，至于这个指针指向谁和这个结构体没关系，这结构体本身是完全分配在栈上的。只不过结构体里面有个东西记录了堆上的地址信息而已。</p></div></article>