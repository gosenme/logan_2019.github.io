---
title: 重学 Go 语言：基础篇-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">变量是什么?</h3>
<p>抛开云山雾罩的官腔，变量的本质是什么？</p>
<ul>
<li>一块或多块用于存储可变数据的内存。</li>
<li>确切的类型决定了内存长度和数据存储格式。</li>
<li>用于引用该内存的符号名。</li>
</ul>
<blockquote>
  <p>通过 unsafe 包提供的指针运算，可以将多个变量指向同一块内存，比如整数可以当做字节序列读出来，但这并不能改变原变量的类型。</p>
</blockquote>
<p>变量本身的确是一个相对来说比较抽象的概念，变量首先要引用一块内存，需要存储数据并且可修改数据，那这块内存需要可读可写。</p>
<p>可能不是一块内存而是多块内存，例如基本类型整数是一块内存，引用类型切片哈希可能是多块内存构成的。</p>
<p>内存地址可能不是固定的，例如切片的底层数组、哈希表在扩容的时候可能都会重新分配内存。</p>
<p>C 语言、Go 语言某一块内存可能是固定的，但是 Python 语言一个变量涉及到很多东西，名字是独立的字符串对象。目标对象、名字空间共同构成一个变量。</p>
<p>所以一块或多块用于存储可变数据的内存。</p>
<p>第二变量必须有确切的类型，Go 和 Python 是强类型语言，C 是弱类型的语言。所谓强类型的语言不能把一个变量隐式地转化另外一种类型来使用。C 语言是弱类型可以把整数当成浮点型来使用。</p>
<p>通过类型决定需要多长的内存，例如 64 位整数是 8 字节 32 位整数是 4 字节。同时涉及到大小端的问题，例如字节怎么排列的。类型决定了内存长度和数据存储格式，很显然整数和其他类型存储肯定是不一样的。</p>
<p>因为变量的内存是运行期的，我们写代码的时候不知道，所以必须有个符号名字来指代这块内存而不是指代这块内存地址。x = 1 指“x 指代这块内存”，不是说“x 等于它的地址”，地址是地址，内存是内存。当然对于编译器来说，它把 x 解析成一个地址，我们写代码的时候实际上是指代这块内存，代码中内存和指针是完全不同的概念。注意 x = 1 或者 &amp;x 是 x 的指针的两种不同说法。</p>
<p>很显然严格来说变量是由几个东西共同组成的一个概念，在这基础之上的抽象。直接说变量是内存的抽象是有点打官腔的说法，我们未必按照官方的说法去定义变量。</p>
<h3 id="-1">变量定义</h3>
<p>变量的定义和声明是有区别的，定义和声明不是一个概念。</p>
<ul>
<li>定义变量，将为期分配内存。</li>
<li>声明则是告知编译器（或链接器）有这样一个符号（类型）。</li>
</ul>
<p>变量的定义需要明确分配内存，也就是同一个变量只能定义一次，不可能同一个变量分配两次内存。运行期修改是另外一回事，但定义不能指定两块内存。</p>
<p>定义 x = 1 是明确为 x 这个变量分配内存。</p>
<p>声明在 Go 语言里面很少见，C 语言有大量声明。C 语言有个前置的规则，编译是按单个文件来处理，所以我们把声明放在头文件里，假如引用变量 x 在另外一个文件里不知道 x 是什么类型长度，所以必须在函数调用之前这个符号出现过，引用变量也需要出现过。有一种特定的语法 <code>extern int x</code> 表示声明一个变量 x 类型是 int，编译器知道引用的 x 是什么。现代编程语言都会把所有的文件利用词法分析一遍后再编译，所以对于声明很少见。</p>
<p>声明只是告诉编译器或者链接器，“在某个地方有这样一个符号，链接的时候把它指向那个目标地址”的意思，变量或者函数只能定义一次但是可以声明多次。函数其实也是一个变量有内存地址，只不过函数地址在 txt 段里，而且是只读的而已。</p>
<p>所以声明和定义一定要严格区分清楚。这就相当于你出生只有一次，但是亲戚说有个侄子外甥相当于声明，声明可以很多次只是间接指向你不是别名。因为编译或者链接的时候实际上指向你并不是别名，这会涉及到一个问题，编程语言是否允许多个变量同时指向同一个东西。</p>
<p>因为即使是指针它里面存的数据也是复制过的，两个指针虽然指向同一个内存，但是这两个指针里面的数据是不一样的，数据内容可能是相等的，但是和这两个指针没有关系，不能说这两个指针是另外一个变量的别名。但是 Python 语言可以，因为 Python 的名字和目标对象是分开的，它用关联机制来处理。</p>
<h3 id="-2">变量定义语法</h3>
<pre><code class="go language-go">var x int
var s = "abc"
var a, b = 1, 2.0
</code></pre>
<ul>
<li>自动初始化为零值（zero value）</li>
<li>可根据初始化值推断类型</li>
<li>可一次定义多个不同类型的变量</li>
<li>无法定义只读变量（readonly、const）</li>
</ul>
<p>Go 语言变量定义涉及到几个方面。变量的定义方式通常有两种，第一种称之为全局变量，第二种称之为局部变量。全局变量和局部变量定义的时候可以用 var 这种方式。</p>
<p>编译器根据初始化值就可以推断类型，这是一种语法糖，其实在早期必须严格定义类型。通过初始化值来推断默认类型，1 的默认类型是 int，2.0 的默认类型是 float，但是不能推断是 float32 还是 float64。</p>
<p><code>var a, b = 1, 2.0</code> 可以同时提供初始化值定义多个变量，同时允许 a 和 b 是不同类型。</p>
<p>Go 语言不能定义只读变量，只读变量就是只允许初始化修改，后面不允许修改。有些时候我们需要只读变量，官方标准库设计是通过暴露一个全局错误来表达错误结果。用变量定义很多错误，判断错误是否等于通过判断是不是同一个变量，而不是通过错误类型来判断。</p>
<p>但是变量是可以修改的，值会发生变化的，最好的方式是错误变量定义为只读的。作为一个语言既然这样使用，必须要有非常严谨的规则不应该有漏洞，但这种设计明显是个漏洞。判断是不是同一个变量来确定错误，如果这个变量修改呢，这明显是语言设计上的不严谨。</p>
<p>我们可以用分组的方式写法：</p>
<pre><code class="go language-go">var (
    x int
    s = "abc"
    a, b = 1, 200
)
</code></pre>
<p>分组方式只是一种语法糖，定义局部变量同样也可以这样写，主要看开发团队的编码规范和约定。</p>
<h3 id="-3">初始化规则</h3>
<p>初始化实际上有两种方式，第一种方式是显式初始化，比如 <code>var x int = 100</code>，第二种方式由编译器来保证内存是被初始化过的，比如 <code>var y int</code>，编译器实际是插入相关的数值来保证初始化。</p>
<p>自动初始化为零值。初始化零值就是定义变量没有指定初始化值实际上默认初始化零值。我们给这个变量分配内存，它指向的内存是重新分配的，可能是以前有别的函数用过的，那么指向的内存可能有垃圾数据，或者指向的物理内存是垃圾数据。</p>
<p>很多语言必须把变量初始化明确地进行表达，否则不允许使用会提示出错，相当于 Go 语言帮你默认初始化为零。但是不是所有语言都会这么做，尤其是系统语言，初始化和不初始化是非常严肃的事。零值就是内存中的数据全部变成零，我们知道内存里面的数据都是字节数字。零值对于不同类型表达的结果是不一样的，数字可能解释为零，字符串可能解释为空字符串。</p>
<p>全局初始化和局部变量初始化规则是不一样的。</p>
<p>我们首先搞明白全局变量在哪，一个编译好的可执行文件分为多个段，其中有两个段 .data、.bss。.bss 是没有初始化值，.data 里有显式的值。显式的值需要存储到 .data 中的，如果没有显式的值是在 .bss 里面。这些值最终是被映射到虚拟地址空间里面。换句话说，.data 中 0x10，0 映射到虚拟空间里，最终覆盖到物理内存中去。因为程序会把整个段加载到物理内存中，所以确保全局变量是被初始化过的。</p>
<p>这地方有两个规则，.data 中的值已经被存储到可执行文件里面，.bss 全局变量，载入器要确保所有的值是二进制零值，所以说全局变量的初始化是由载入器来保障的。</p>
<p>局部变量谁来保证，我们看下简单的规则。</p>
<pre><code class="go language-go">var x int = 0x100

func main() {
    var y int
    println(y)
}
</code></pre>
<pre><code class="bash language-bash">$ go build
$ go tool objdump -s "main\.main" 01types
TEXT main.main(SB) main.go
  main.go:5  MOVQ FS:0xfffffff8, CX
  main.go:5  CMPQ 0x10(CX), SP
  main.go:5  JBE 0x44c193
  main.go:5  SUBQ $0x10, SP
  main.go:5  MOVQ BP, 0x8(SP)
  main.go:5  LEAQ 0x8(SP), BP
  main.go:7  CALL runtime.printlock(SB)
  main.go:7  MOVQ $0x0, 0(SP)
  main.go:7  CALL runtime.printint(SB)
  main.go:7  CALL runtime.printnl(SB)
  main.go:7  CALL runtime.printunlock(SB)
  main.go:8  MOVQ 0x8(SP), BP
  main.go:8  ADDQ $0x10, SP
  main.go:8  RET
  main.go:5  CALL runtime.morestack_noctxt(SB)
  main.go:5  JMP main.main(SB)
</code></pre>
<p>我们可以看到编译器自动插入了<code>MOVQ $0x0, 0(SP)</code> 指令，所以局部变量编译器确保是被初始化过的。</p>
<p>在 Go 语言里，编译器确保变量是被确保为二进制零值，我们阅读的 0 值和二进制零值是有差别的。因为计算机只识别二进制数据，所以汇编上看到的全是整数，浮点数都是通过整数来模拟。</p>
<p>一个简单的变量究竟是来表达什么，那么它的初始化值是非常重要的，否则在物理内存上它的值就是不确定的。</p>
<p>很多语言有检查规则，使用变量的时候要检查是否被初始化过，如果没有初始化过这个行为是不确定的，使用的时候编译器会给个警告或者错误，因为会产生不确定的逻辑，Go 语言在这一点做得更符合大部分人的预期。我们只要拿到变量肯定是被初始化过的。要么是全局变量在编译之前，代码显式提供初始化值，要么是局部变量编译器通过相关汇编指令确保二进制零初始化。</p></div></article>