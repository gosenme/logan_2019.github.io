---
title: Linux GDB 调试指南-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课的核心内容：</p>
<ul>
<li>disassemble 命令</li>
<li>set args 和 show args 命令</li>
<li>tbreak 命令</li>
<li>watch 命令</li>
<li>display 命令</li>
</ul>
<h3 id="disassemble">disassemble 命令</h3>
<p>当进行一些高级调试时，我们可能需要查看某段代码的汇编指令去排查问题，或者是在调试一些没有调试信息的发布版程序时，也只能通过反汇编代码去定位问题，那么 <strong>disassemble</strong> 命令就派上用场了。</p>
<pre><code>initServer () at server.c:1839
1839        createSharedObjects();
(gdb) disassemble
Dump of assembler code for function initServer:
   0x000000000042f450 &lt;+0&gt;:     push   %r12
   0x000000000042f452 &lt;+2&gt;:     mov    $0x1,%esi
   0x000000000042f457 &lt;+7&gt;:     mov    $0x1,%edi
   0x000000000042f45c &lt;+12&gt;:    push   %rbp
   0x000000000042f45d &lt;+13&gt;:    push   %rbx
   0x000000000042f45e &lt;+14&gt;:    callq  0x421eb0 &lt;signal@plt&gt;
   0x000000000042f463 &lt;+19&gt;:    mov    $0x1,%esi
   0x000000000042f468 &lt;+24&gt;:    mov    $0xd,%edi
   0x000000000042f46d &lt;+29&gt;:    callq  0x421eb0 &lt;signal@plt&gt;
   0x000000000042f472 &lt;+34&gt;:    callq  0x42f3a0 &lt;setupSignalHandlers&gt;
   0x000000000042f477 &lt;+39&gt;:    mov    0x316d52(%rip),%r8d        # 0x7461d0 &lt;server+2128&gt;
   0x000000000042f47e &lt;+46&gt;:    test   %r8d,%r8d
   0x000000000042f481 &lt;+49&gt;:    jne    0x42f928 &lt;initServer+1240&gt;
   0x000000000042f487 &lt;+55&gt;:    callq  0x421a50 &lt;getpid@plt&gt;
   0x000000000042f48c &lt;+60&gt;:    movq   $0x0,0x316701(%rip)        # 0x745b98 &lt;server+536&gt;
   0x000000000042f497 &lt;+71&gt;:    mov    %eax,0x3164e3(%rip)        # 0x745980 &lt;server&gt;
   0x000000000042f49d &lt;+77&gt;:    callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4a2 &lt;+82&gt;:    mov    %rax,0x3166c7(%rip)        # 0x745b70 &lt;server+496&gt;
   0x000000000042f4a9 &lt;+89&gt;:    callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4ae &lt;+94&gt;:    mov    %rax,0x3166c3(%rip)        # 0x745b78 &lt;server+504&gt;
   0x000000000042f4b5 &lt;+101&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4ba &lt;+106&gt;:   mov    %rax,0x3166c7(%rip)        # 0x745b88 &lt;server+520&gt;
   0x000000000042f4c1 &lt;+113&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4c6 &lt;+118&gt;:   mov    %rax,0x3166c3(%rip)        # 0x745b90 &lt;server+528&gt;
   0x000000000042f4cd &lt;+125&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4d2 &lt;+130&gt;:   movl   $0xffffffff,0x316d6c(%rip)        # 0x746248 &lt;server+2248&gt;
   0x000000000042f4dc &lt;+140&gt;:   mov    %rax,0x31669d(%rip)        # 0x745b80 &lt;server+512&gt;
   0x000000000042f4e3 &lt;+147&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4e8 &lt;+152&gt;:   mov    %rax,0x316ec9(%rip)        # 0x7463b8 &lt;server+2616&gt;
   0x000000000042f4ef &lt;+159&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f4f4 &lt;+164&gt;:   mov    %rax,0x316ec5(%rip)        # 0x7463c0 &lt;server+2624&gt;
   0x000000000042f4fb &lt;+171&gt;:   callq  0x423cb0 &lt;listCreate&gt;
   0x000000000042f500 &lt;+176&gt;:   movl   $0x0,0x316e7e(%rip)        # 0x746388 &lt;server+2568&gt;
   0x000000000042f50a &lt;+186&gt;:   mov    %rax,0x316e6f(%rip)        # 0x746380 &lt;server+2560&gt;
   0x000000000042f511 &lt;+193&gt;:   movl   $0x0,0x316685(%rip)        # 0x745ba0 &lt;server+544&gt;
   0x000000000042f51b &lt;+203&gt;:   callq  0x432e90 &lt;zmalloc_get_memory_size&gt;
   0x000000000042f520 &lt;+208&gt;:   mov    %rax,0x316fd9(%rip)        # 0x746500 &lt;server+2944&gt;
=&gt; 0x000000000042f527 &lt;+215&gt;:   callq  0x42a7b0 &lt;createSharedObjects&gt;
</code></pre>
<p>GDB 默认反汇编为 AT&amp;T 格式的指令，可以通过 show disassembly-flavor 查看，如果习惯 intel 汇编格式可以用命令 set disassembly-flavor intel 来设置。</p>
<pre><code>(gdb) set disassembly-flavor intel
(gdb) disassemble
Dump of assembler code for function initServer:
   0x000000000042f450 &lt;+0&gt;:     push   r12
   0x000000000042f452 &lt;+2&gt;:     mov    esi,0x1
   0x000000000042f457 &lt;+7&gt;:     mov    edi,0x1
   0x000000000042f45c &lt;+12&gt;:    push   rbp
   0x000000000042f45d &lt;+13&gt;:    push   rbx
   0x000000000042f45e &lt;+14&gt;:    call   0x421eb0 &lt;signal@plt&gt;
   0x000000000042f463 &lt;+19&gt;:    mov    esi,0x1
   0x000000000042f468 &lt;+24&gt;:    mov    edi,0xd
   0x000000000042f46d &lt;+29&gt;:    call   0x421eb0 &lt;signal@plt&gt;
   0x000000000042f472 &lt;+34&gt;:    call   0x42f3a0 &lt;setupSignalHandlers&gt;
   0x000000000042f477 &lt;+39&gt;:    mov    r8d,DWORD PTR [rip+0x316d52]        # 0x7461d0 &lt;server+2128&gt;
   0x000000000042f47e &lt;+46&gt;:    test   r8d,r8d
   0x000000000042f481 &lt;+49&gt;:    jne    0x42f928 &lt;initServer+1240&gt;
   0x000000000042f487 &lt;+55&gt;:    call   0x421a50 &lt;getpid@plt&gt;
   0x000000000042f48c &lt;+60&gt;:    mov    QWORD PTR [rip+0x316701],0x0        # 0x745b98 &lt;server+536&gt;
   0x000000000042f497 &lt;+71&gt;:    mov    DWORD PTR [rip+0x3164e3],eax        # 0x745980 &lt;server&gt;
   0x000000000042f49d &lt;+77&gt;:    call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4a2 &lt;+82&gt;:    mov    QWORD PTR [rip+0x3166c7],rax        # 0x745b70 &lt;server+496&gt;
   0x000000000042f4a9 &lt;+89&gt;:    call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4ae &lt;+94&gt;:    mov    QWORD PTR [rip+0x3166c3],rax        # 0x745b78 &lt;server+504&gt;
   0x000000000042f4b5 &lt;+101&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4ba &lt;+106&gt;:   mov    QWORD PTR [rip+0x3166c7],rax        # 0x745b88 &lt;server+520&gt;
   0x000000000042f4c1 &lt;+113&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4c6 &lt;+118&gt;:   mov    QWORD PTR [rip+0x3166c3],rax        # 0x745b90 &lt;server+528&gt;
   0x000000000042f4cd &lt;+125&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4d2 &lt;+130&gt;:   mov    DWORD PTR [rip+0x316d6c],0xffffffff        # 0x746248 &lt;server+2248&gt;
   0x000000000042f4dc &lt;+140&gt;:   mov    QWORD PTR [rip+0x31669d],rax        # 0x745b80 &lt;server+512&gt;
   0x000000000042f4e3 &lt;+147&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4e8 &lt;+152&gt;:   mov    QWORD PTR [rip+0x316ec9],rax        # 0x7463b8 &lt;server+2616&gt;
   0x000000000042f4ef &lt;+159&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f4f4 &lt;+164&gt;:   mov    QWORD PTR [rip+0x316ec5],rax        # 0x7463c0 &lt;server+2624&gt;
   0x000000000042f4fb &lt;+171&gt;:   call   0x423cb0 &lt;listCreate&gt;
   0x000000000042f500 &lt;+176&gt;:   mov    DWORD PTR [rip+0x316e7e],0x0        # 0x746388 &lt;server+2568&gt;
   0x000000000042f50a &lt;+186&gt;:   mov    QWORD PTR [rip+0x316e6f],rax        # 0x746380 &lt;server+2560&gt;
   0x000000000042f511 &lt;+193&gt;:   mov    DWORD PTR [rip+0x316685],0x0        # 0x745ba0 &lt;server+544&gt;
   0x000000000042f51b &lt;+203&gt;:   call   0x432e90 &lt;zmalloc_get_memory_size&gt;
   0x000000000042f520 &lt;+208&gt;:   mov    QWORD PTR [rip+0x316fd9],rax        # 0x746500 &lt;server+2944&gt;
=&gt; 0x000000000042f527 &lt;+215&gt;:   call   0x42a7b0 &lt;createSharedObjects&gt;
</code></pre>
<h3 id="setargsshowargs">set args 和 show args 命令</h3>
<p>很多程序需要我们传递命令行参数。在 GDB 调试中，很多人会觉得可以使用 <strong>gdb filename args</strong> 这种形式来给 GDB 调试的程序传递命令行参数，这样是不行的。正确的做法是在用 GDB 附加程序后，在使用 <strong>run</strong> 命令之前，使用“<strong>set args 参数内容</strong>”来设置命令行参数。</p>
<p>还是以 redis-server 为例，Redis 启动时可以指定一个命令行参数，它的默认配置文件位于 redis-server 这个文件的上一层目录，因此我们可以在 GDB 中这样传递这个参数：<strong>set args ../redis.conf</strong>（即文件 redis.conf 位于当前程序 redis-server 的上一层目录），可以通过 <strong>show args</strong> 查看命令行参数是否设置成功。</p>
<pre><code>(gdb) set args ../redis.conf
(gdb) show args
Argument list to give program being debugged when it is started is "../redis.conf ".
(gdb)
</code></pre>
<p>如果单个命令行参数之间含有空格，可以使用引号将参数包裹起来。</p>
<pre><code>(gdb) set args "999 xx" "hu jj"
(gdb) show args
Argument list to give program being debugged when it is started is ""999 xx" "hu jj"".
(gdb)
</code></pre>
<p>如果想清除掉已经设置好的命令行参数，使用 <strong>set args</strong> 不加任何参数即可。</p>
<pre><code>(gdb) set args
(gdb) show args
Argument list to give program being debugged when it is started is "".
(gdb)
</code></pre>
<h3 id="tbreak">tbreak 命令</h3>
<p><strong>tbreak</strong> 命令也是添加一个断点，第一个字母“<strong>t</strong>”的意思是 temporarily（临时的），也就是说这个命令加的断点是临时的，所谓临时断点，就是一旦该断点触发一次后就会自动删除。添加断点的方法与上面介绍的 break 命令一模一样，这里不再赘述。</p>
<pre><code>(gdb) tbreak main
Temporary breakpoint 1 at 0x423450: file server.c, line 3704.
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /root/redis-4.0.9/src/redis-server
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".

Temporary breakpoint 1, main (argc=1, argv=0x7fffffffe588) at server.c:3704
3704    int main(int argc, char **argv) {
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /root/redis-4.0.9/src/redis-server
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
21652:C 14 Sep 07:05:39.288 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
21652:C 14 Sep 07:05:39.288 # Redis version=4.0.9, bits=64, commit=00000000, modified=0, pid=21652, just started
21652:C 14 Sep 07:05:39.288 # Warning: no config file specified, using the default config. In order to specify a config file use /root/redis-4.0.9/src/redis-server /path/to/redis.conf
21652:M 14 Sep 07:05:39.289 * Increased maximum number of open files to 10032 (it was originally set to 1024).
[New Thread 0x7ffff07ff700 (LWP 21653)]
[New Thread 0x7fffefffe700 (LWP 21654)]
[New Thread 0x7fffef7fd700 (LWP 21655)]
                _._
           _.-``__ ''-._
      _.-``    `.  `_.  ''-._           Redis 4.0.9 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 21652
  `-._    `-._  `-./  _.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           http://redis.io
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |
</code></pre>
<p>上述代码，我们使用 <strong>tbreak</strong> 命令在 main() 函数处添加了一个断点，当断点触发后，再次运行程序不再触发断点，因为这个临时断点已经被删除。</p>
<h3 id="watch">watch 命令</h3>
<p><strong>watch</strong> 命令是一个强大的命令，它可以用来监视一个变量或者一段内存，当这个变量或者该内存处的值发生变化时，GDB 就会中断下来。被监视的某个变量或者某个内存地址会产生一个 watch point（观察点）。</p>
<p>我在数年前去北京中关村软件园应聘一个 C++ 开发的职位，当时一个面试官问了这样一个问题：有一个变量其值被意外地改掉了，通过单步调试或者挨个检查使用该变量的代码工作量会非常大，如何快速地定位到该变量在哪里被修改了？其实，面试官想要的答案是“硬件断点”。具体什么是硬件断点，我将在后面高级调试课程中介绍，而 watch 命令就可以通过添加硬件断点来达到监视数据变化的目的。watch 命令的使用方式是“watch 变量名或内存地址”，一般有以下几种形式：</p>
<ul>
<li>形式一：整型变量</li>
</ul>
<pre><code>int i;
watch i
</code></pre>
<ul>
<li>形式二：指针类型</li>
</ul>
<pre><code>char *p;
watch p 与 watch *p
</code></pre>
<blockquote>
  <p><strong>注意</strong>：watch p 与 watch *p 是有区别的，前者是查看 *(&amp;p)，是 p 变量本身；后者是 p 所指内存的内容。我们需要查看地址，因为目的是要看某内存地址上的数据是怎样变化的。</p>
</blockquote>
<ul>
<li>形式三：watch 一个数组或内存区间</li>
</ul>
<pre><code>char buf[128];
watch buf
</code></pre>
<p>这里是对 buf 的 128 个数据进行了监视，此时不是采用硬件断点，而是用软中断实现的。用软中断方式去检查内存变量是比较耗费 CPU 资源的，精确地指明地址是硬件中断。</p>
<blockquote>
  <p><strong>注意</strong>：当设置的观察点是一个局部变量时，局部变量无效后，观察点也会失效。在观察点失效时 GDB 可能会提示如下信息：</p>
<pre><code>Watchpoint 2 deleted because the program has left the block in which its expression is valid.
</code></pre>
</blockquote>
<h3 id="display">display 命令</h3>
<p><strong>display</strong> 命令监视的变量或者内存地址，每次程序中断下来都会自动输出这些变量或内存的值。例如，假设程序有一些全局变量，每次断点停下来我都希望  GDB 可以自动输出这些变量的最新值，那么使用“<strong>display 变量名</strong>”设置即可。</p>
<pre><code>Program received signal SIGINT, Interrupt.
0x00007ffff71e2483 in epoll_wait () from /lib64/libc.so.6
(gdb) display $ebx
1: $ebx = 7988560
(gdb) display /x $ebx
2: /x $ebx = 0x79e550
(gdb) display $eax
3: $eax = -4
(gdb) b main
Breakpoint 8 at 0x4201f0: file server.c, line 4003.
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /root/redis-5.0.3/src/redis-server
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".

Breakpoint 8, main (argc=1, argv=0x7fffffffe4e8) at server.c:4003
4003    int main(int argc, char **argv) {
3: $eax = 4325872
2: /x $ebx = 0x0
1: $ebx = 0
(gdb)
</code></pre>
<p>上述代码中，我使用 <strong>display</strong> 命令分别添加了寄存器 <strong>ebp</strong> 和寄存器 <strong>eax</strong>，<strong>ebp</strong> 寄存器分别使用十进制和十六进制两种形式输出其值，这样每次程序中断下来都会自动把这些值打印出来，可以使用 <strong>info display</strong> 查看当前已经自动添加了哪些值，使用 <strong>delete display</strong> 清除全部需要自动输出的变量，使用 <strong>delete diaplay 编号</strong> 删除某个自动输出的变量。</p>
<pre><code>(gdb) delete display
Delete all auto-display expressions? (y or n) n
(gdb) delete display 3
(gdb) info display
Auto-display expressions now in effect:
Num Enb Expression
2:   y  $ebp
1:   y  $eax
</code></pre>
<h3 id="">小结</h3>
<p>到目前为止已把 GDB 常用的命令都介绍完了，不知道读者是否能记得每一个命令的用途和用法？只要理解了，记忆它们其实也不难，这些基础命令，希望读者能熟练掌握。</p></div></article>