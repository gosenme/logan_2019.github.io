---
title: 重学 Go 语言：基础篇-23
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="c">参数传递 C 参数复制，返回值</h3>
<p>先看下 C 语言代码例子。</p>
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
<p>三个变量：x、y、z。</p>
<h4 id="">编译</h4>
<pre><code class="bash language-bash">$ gcc -g -O0 -o test test.c #编译，去掉优化
</code></pre>
<h4 id="gbd">使用 GBD 调试</h4>
<pre><code class="bash language-bash">$ gdb test
$ b main #符号名上加上断点，main 函数加上断点
$ r #执行，这时在 main 函数上中断了
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
</code></pre>
<p>注意 main 函数不是程序真正的入口，而是用户代码的入口，因为大部分程序在执行 main 函数之前，会有其它初始化的操作。</p>
<pre><code class="bash language-bash">Dump of assembler code for function main:
   0x0000000000400570 &lt;+0&gt;:    push   rbp
   0x0000000000400571 &lt;+1&gt;:    mov    rbp,rsp
   0x0000000000400574 &lt;+4&gt;:    sub    rsp,0x20 #给main函数分配了16进制20字节的栈桢空间。
   0x0000000000400578 &lt;+8&gt;:    mov    DWORD PTR [rbp-0x14],edi
   0x000000000040057b &lt;+11&gt;:    mov    QWORD PTR [rbp-0x20],rsi
=&gt; 0x000000000040057f &lt;+15&gt;:    mov    DWORD PTR [rbp-0xc],0x100
   0x0000000000400586 &lt;+22&gt;:    mov    DWORD PTR [rbp-0x8],0x200
   0x000000000040058d &lt;+29&gt;:    mov    edx,DWORD PTR [rbp-0x8]
   0x0000000000400590 &lt;+32&gt;:    mov    eax,DWORD PTR [rbp-0xc]
   0x0000000000400593 &lt;+35&gt;:    mov    esi,edx
   0x0000000000400595 &lt;+37&gt;:    mov    edi,eax
   0x0000000000400597 &lt;+39&gt;:    call   0x400548 &lt;add&gt;
   0x000000000040059c &lt;+44&gt;:    mov    DWORD PTR [rbp-0x4],eax
   0x000000000040059f &lt;+47&gt;:    mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004005a2 &lt;+50&gt;:    mov    esi,eax
   0x00000000004005a4 &lt;+52&gt;:    mov    edi,0x40064d
   0x00000000004005a9 &lt;+57&gt;:    mov    eax,0x0
   0x00000000004005ae &lt;+62&gt;:    call   0x400400 &lt;printf@plt&gt;
   0x00000000004005b3 &lt;+67&gt;:    mov    eax,0x0
   0x00000000004005b8 &lt;+72&gt;:    leave
   0x00000000004005b9 &lt;+73&gt;:    ret
End of assembler dump.
</code></pre>
<p>我们看到所有的空间都是基于 BP 寄存器的寻址。我们重点分析下 Go 语言的例子。</p>
<h3 id="go">参数传递 Go 参数复制，返回值</h3>
<p>看下 Go 语言代码例子。</p>
<pre><code class="go language-go">func info(x int) {
    log.Printf("info %d\n", x)
}

func add(x, y int) int {
    z := x + y
    info(z)

    return z
}

func main() {
    x, y := 0x100, 0x200
    z := add(x, y)

    println(z)
}
</code></pre>
<p>编译：</p>
<pre><code class="bash language-bash">$ go build -gcflags "-N -l" -o test test.go
</code></pre>
<p>GBD 调试：</p>
<pre><code class="bash language-bash">$ gdb test
$ b main.main #打断点
$ r #运行
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
</code></pre>
<pre><code class="bash language-bash">=&gt; 0x0000000000401140 &lt;+0&gt;:    mov    rcx,QWORD PTR fs:0xfffffffffffffff8
   0x0000000000401149 &lt;+9&gt;:    cmp    rsp,QWORD PTR [rcx+0x10]
   0x000000000040114d &lt;+13&gt;:    jbe    0x4011a9 &lt;main.main+105&gt;
   0x000000000040114f &lt;+15&gt;:    sub    rsp,0x30 #首先为这个空间分配了 48 字节栈桢空间
   0x0000000000401153 &lt;+19&gt;:    mov    QWORD PTR [rsp+0x28],0x100 #sp+28 位置存储局部变量 x
   0x000000000040115c &lt;+28&gt;:    mov    QWORD PTR [rsp+0x20],0x200 #sp+20 位置存储局部变量 y
   0x0000000000401165 &lt;+37&gt;:    mov    rax,QWORD PTR [rsp+0x28]
   0x000000000040116a &lt;+42&gt;:    mov    QWORD PTR [rsp],rax #x 参数复制到 rsp+0 位置
   0x000000000040116e &lt;+46&gt;:    mov    rax,QWORD PTR [rsp+0x20]
   0x0000000000401173 &lt;+51&gt;:    mov    QWORD PTR [rsp+0x8],rax #y 参数复制到 rsp+8 位置
   0x0000000000401178 &lt;+56&gt;:    call   0x4010f0 &lt;main.add&gt;
   0x000000000040117d &lt;+61&gt;:    mov    rax,QWORD PTR [rsp+0x10]
   0x0000000000401182 &lt;+66&gt;:    mov    QWORD PTR [rsp+0x18],rax
   0x0000000000401187 &lt;+71&gt;:    call   0x425380 &lt;runtime.printlock&gt;
   0x000000000040118c &lt;+76&gt;:    mov    rax,QWORD PTR [rsp+0x18]
   0x0000000000401191 &lt;+81&gt;:    mov    QWORD PTR [rsp],rax
   0x0000000000401195 &lt;+85&gt;:    call   0x425a10 &lt;runtime.printint&gt;
   0x000000000040119a &lt;+90&gt;:    call   0x4255b0 &lt;runtime.printnl&gt;
   0x000000000040119f &lt;+95&gt;:    call   0x425400 &lt;runtime.printunlock&gt;
   0x00000000004011a4 &lt;+100&gt;:    add    rsp,0x30
   0x00000000004011a8 &lt;+104&gt;:    ret
   0x00000000004011a9 &lt;+105&gt;:    call   0x44b160 &lt;runtime.morestack_noctxt&gt;
   0x00000000004011ae &lt;+110&gt;:    jmp    0x401140 &lt;main.main&gt;
</code></pre>
<p>参考汇编代码画出内存示意图如下：</p>
<pre><code>|---------+---sp
| x100    |
|---------|---+8
| y200    |
|---------|--+10
|         |
|---------|--+18
|         |
|---------|--+20
| y=200   |
|---------|--+28
| x=100   |
|---------|--+30
</code></pre>
<p>Go 语言基于 SP 做加法，因为在 Go 语言里不使用 BP 寄存器，它把 BP 寄存器当作普通寄存器来用，不用 BP 寄存器来维持一个栈桢，只用 SP 指向栈顶就可以了，这跟它的内存管理策略有关系。</p>
<p>在 add 函数执行之前，首先做了参数复制，就是说<strong>函数调用时候参数是被复制的</strong>。理论上所有参数都是复制的，传指针复制的是指针而不是指针指向的目标，指针本身是被复制的，通过这个代码我们就看到复制过程。</p>
<p>接下来调用 add 方法。</p>
<pre><code class="bash language-bash">$ b main.add #打断点
$ c #运行
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
</code></pre>
<pre><code class="bash language-bash">=&gt; 0x00000000004010f0 &lt;+0&gt;:    mov    rcx,QWORD PTR fs:0xfffffffffffffff8
   0x00000000004010f9 &lt;+9&gt;:    cmp    rsp,QWORD PTR [rcx+0x10]
   0x00000000004010fd &lt;+13&gt;:    jbe    0x401136 &lt;main.add+70&gt;
   0x00000000004010ff &lt;+15&gt;:    sub    rsp,0x10 #分配 10 这样的空间
   0x0000000000401103 &lt;+19&gt;:    mov    QWORD PTR [rsp+0x28],0x0 #初始化操作，
   # Go 语言有这样的规则它会把所有的变量初始化为二进制 0
   0x000000000040110c &lt;+28&gt;:    mov    rax,QWORD PTR [rsp+0x18]
   0x0000000000401111 &lt;+33&gt;:    mov    rcx,QWORD PTR [rsp+0x20]
   0x0000000000401116 &lt;+38&gt;:    add    rax,rcx
   0x0000000000401119 &lt;+41&gt;:    mov    QWORD PTR [rsp+0x8],rax
   0x000000000040111e &lt;+46&gt;:    mov    QWORD PTR [rsp],rax
   0x0000000000401122 &lt;+50&gt;:    call   0x401000 &lt;main.info&gt;
   0x0000000000401127 &lt;+55&gt;:    mov    rax,QWORD PTR [rsp+0x8]
   0x000000000040112c &lt;+60&gt;:    mov    QWORD PTR [rsp+0x28],rax
   0x0000000000401131 &lt;+65&gt;:    add    rsp,0x10 #把 add 函数所需要的栈桢空间释放掉
   0x0000000000401135 &lt;+69&gt;:    ret    #把 ip pop 出来
   0x0000000000401136 &lt;+70&gt;:    call   0x44b160 &lt;runtime.morestack_noctxt&gt;
   0x000000000040113b &lt;+75&gt;:    jmp    0x4010f0 &lt;main.add&gt;
</code></pre>
<p>参考汇编代码画出内存示意图如下：</p>
<pre><code>|---------+---sp
| 300     |
|---------+---+8
| 300     |
|---------|---+10
| ip      |
|---------+---+18
| 100     |
|---------|---+20
| 200     |
|---------|--—+28
| 0       |
|---------|
</code></pre>
<p>很显然，Go 语言调用一个方法的时候，首先在栈顶的位置按顺序准备好参数同时给返回值存储空间，100 和 200 是参数，300 是返回值的空间。所以 Go 语言调用函数的时候，是由调用方来准备参数和返回值的空间。</p>
<pre><code>|---------+---sp
| 100     |
|---------|---+8
| 200     |
|---------|--+10
| 300     |
|---------|--+18
|         |
|---------|--+20
| y=200   |
|---------|--+28
| x=100   |
|---------|--+30
</code></pre>
<pre><code class="bash language-bash">$ b 20 #打断点
$ c #运行
$ set disassembly-flavor intel #设置 intel 样式
$ disass #反汇编
</code></pre>
<pre><code class="bash language-bash">   0x0000000000401140 &lt;+0&gt;:    mov    rcx,QWORD PTR fs:0xfffffffffffffff8
   0x0000000000401149 &lt;+9&gt;:    cmp    rsp,QWORD PTR [rcx+0x10]
   0x000000000040114d &lt;+13&gt;:    jbe    0x4011a9 &lt;main.main+105&gt;
   0x000000000040114f &lt;+15&gt;:    sub    rsp,0x30
   0x0000000000401153 &lt;+19&gt;:    mov    QWORD PTR [rsp+0x28],0x100
   0x000000000040115c &lt;+28&gt;:    mov    QWORD PTR [rsp+0x20],0x200
   0x0000000000401165 &lt;+37&gt;:    mov    rax,QWORD PTR [rsp+0x28]
   0x000000000040116a &lt;+42&gt;:    mov    QWORD PTR [rsp],rax
   0x000000000040116e &lt;+46&gt;:    mov    rax,QWORD PTR [rsp+0x20]
   0x0000000000401173 &lt;+51&gt;:    mov    QWORD PTR [rsp+0x8],rax
   0x0000000000401178 &lt;+56&gt;:    call   0x4010f0 &lt;main.add&gt;
   0x000000000040117d &lt;+61&gt;:    mov    rax,QWORD PTR [rsp+0x10] #返回值
   0x0000000000401182 &lt;+66&gt;:    mov    QWORD PTR [rsp+0x18],rax #返回值 z
=&gt; 0x0000000000401187 &lt;+71&gt;:    call   0x425380 &lt;runtime.printlock&gt;
   0x000000000040118c &lt;+76&gt;:    mov    rax,QWORD PTR [rsp+0x18]
   0x0000000000401191 &lt;+81&gt;:    mov    QWORD PTR [rsp],rax
   0x0000000000401195 &lt;+85&gt;:    call   0x425a10 &lt;runtime.printint&gt;
   0x000000000040119a &lt;+90&gt;:    call   0x4255b0 &lt;runtime.printnl&gt;
   0x000000000040119f &lt;+95&gt;:    call   0x425400 &lt;runtime.printunlock&gt;
   0x00000000004011a4 &lt;+100&gt;:    add    rsp,0x30
   0x00000000004011a8 &lt;+104&gt;:    ret
   0x00000000004011a9 &lt;+105&gt;:    call   0x44b160 &lt;runtime.morestack_noctxt&gt;
</code></pre>
<pre><code>|---------+---sp
| 100     |
|---------|---+8
| 200     |
|---------|--+10
| 300     |
|---------|--+18
| z=300   |
|---------|--+20
| y=200   |
|---------|--+28
| x=100   |
|---------|--+30
</code></pre>
<p>Go 语言执行一个函数的时候，它的栈桢空间实际上分成两大块，上面 sp 至 sp+18 一整块是用来调用其它函数所需要的空间，因为<strong>Go 语言调用函数的时候得为函数准备参数和返回值的空间</strong>，所以上面一块是为调用其它函数所需要使用的空间。</p>
<p>下面 sp+18 到 sp+30 是当前函数局部变量的空间。注意到下面的区间空间肯定比较固定的，而上面空间的大小和其它函数调用是复用的，所以这个空间的大小是当前函数里面调用所需要空间最多的函数空间，比如调用 add 需要三个，调用 div 需要四个，上面就至少分配四个，否则的话就不够用。那么这样一来，想计算一下一个函数栈桢需要多大空间其实就很简单了，把下面的和上面的相加就知道栈桢到底有多大。</p>
<p>知道了调用函数的时候是怎么样复制参数的，然后怎么样返回值的，同时栈里面参数的顺序是什么样的。另外怎么样通过 IP 寄存器来确定，基于 SP 做偏移量，SP 做加法就知道具体指向哪个地址。</p>
<p>我们看了当调用函数的时候，这些汇编指令都没有复杂的操作，都是很简单的把数据从一个地址搬到另外一个地址，无非中间通过某个寄存器交换一次，它没有很复杂的操作，完全需要我们耐心。</p>
<p>如果第一次看汇编不熟悉，你就像上面一样画出格子，把偏移量记下来，自己画出这个过程看汇编代码就知道究竟干什么。</p>
<p>到目前为止，这些汇编代码除了恢复现场以外，大部分都是做一些简单的数据搬移操作，我们要确定栈桢空间位置，从类似 <code>sub rsp,0x30</code> 的指令来确定。为当前这个栈桢分配多大空间，到 ret 结束，这段中间就是函数执行的那段代码。其他代码并不要做太多的关注。</p>
<p>对象分配到栈上的时候，我们知道它是用什么样的方式来寻址，如果基于 SP 或者 BP 方式寻址，那么这个对象本身肯定是在栈上的。而判断一个地址可以做很简单的加法或者减法，比如说：</p>
<pre><code class="bash language-bash">$ p/x $rsp #开始地址
$ p/x $rsp+0x30 #结束地址
</code></pre>
<p>如果地址不在这中间，那么就不在这个栈桢里。要不然在上一级栈桢里，要不然就在堆上面，而且在堆上面的时候根据不同的语言可能没有办法通过 <code>info proc mappings</code> 来确定，因为 Go 语言并不使用这个 heap，它使用的是自己管理的。</p>
<p>因为不同的语言对这个方式管理不太一样。所以要确定是否在栈上，可以通过 rsp 寄存器减去栈桢空间，你可以知道开始位置和结束位置以此来判断。</p>
<p>就这个例子而言：</p>
<pre><code class="bash language-bash">$ info locals #输出变量
$ p/x &amp;z #z的地址
</code></pre>
<p>很显然，我们通过这样操作来确定是否在一个栈桢内，就可以确定在栈上还是在堆上分配。</p></div></article>