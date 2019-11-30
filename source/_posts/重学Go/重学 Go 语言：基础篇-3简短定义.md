---
title: 重学 Go 语言：基础篇-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">简短定义</h3>
<pre><code class="go language-go">x := 123
</code></pre>
<ul>
<li>符号不同（:=）</li>
<li>必须显式提供初始化值</li>
<li>不能提供数据类型</li>
<li>只能用于函数内部</li>
</ul>
<p>这种简短定义必须有初始化值，同时不能提供类型，必须通过初始化值进行推导，只能用于函数内部。</p>
<p>在变量定义时候，Go 语言有个很特殊的习惯是在函数内部用简短定义方式，即有初始化值的时候可以省略类型，编译器通过初始化值推断出它的类型，相当于补全类型，因为有类型的变量编译器才知道分配多大空间和存储什么格式，我们管这个叫类型推断。第二必须在函数内部使用，也就是说不能在全局变量中使用。</p>
<p>在函数内部 <code>x := 0x100</code> 定义就相当于 <code>var x int = 0x100</code>。</p>
<h3 id="-1">简短定义的问题</h3>
<pre><code class="go language-go">var x int

func main() {
    x := 100
}
</code></pre>
<ul>
<li>对新手而言，需明确要操作的目标。</li>
<li>通过命名方式改善。</li>
</ul>
<p>在函数内部我们可以使用简短定义，简短定义使用了一个特殊的符号 <code>x := 100</code>，完整的定义是这样 <code>var x = 100</code> 或者 <code>var x int = 100</code>，我们编写代码时需要明确，是修改全局变量还是定义局部变量。如果有相同名称的全局变量，本来想对全局变量修改却不小心定义了新的变量。所以 <code>x := 100</code> 是变量定义而不是变量赋值，定义的话实际上分配了新的内存，修改的话就是赋值。</p>
<p>这种简短定义的问题，一般通过命名的方式来解决。也就是说使用全局变量的时候，不应该使用短名，明确使用全名。</p>
<p>全局变量或者全局常量定义倾向使用多个单词组成的全名，而对于函数内部的局部变量命名倾向于使用短名。因为全局变量可能跨很多函数甚至在不同文件。对应用开发来说，我们通常会把一个函数的控制在有限的规模，短名给我们提供更好的可阅读性。</p>
<p>现在知道了变量是什么，声明和定义有什么不同，另外简短定义可能会带来一些潜在的问题。以后换一个新的语言可以找一个比较熟悉的方式，或者这门语言有几种风格，尝试用一种比较接受的风格去写。</p>
<pre><code class="go language-go">var (
    x int = 0x100
)

func main() {
    println(x) //global var
    x := "abc" //var x string ="abc"
    {
        x := 0x200 //var x int = 0x200
        println(x) // print x int
    }
    println(x) //print var x string
}
</code></pre>
<p>在第一行打印是全局变量，第二行重新定义局部变量，相当于 <code>var x string ="abc"</code>，第七行实际打印 x 字符串，很显然是局部变量。</p>
<p>在同一个函数内部用同一个符号名引用了完全不同的变量，变量名只在当前作用域上有效，超出作用域可能指向外层空间的引用。<code>x := 0x200</code> 虽然看上去少写点代码，但是很容易引起误解。</p>
<h3 id="-2">同名定义的问题</h3>
<pre><code class="go language-go">var x = 100

func main() {
    x := x
    if x := 20; x &gt; 10 {
        x := x
        println(x)
    }
    println(x)
}
</code></pre>
<p>不同作用域形成的遮蔽效应。</p>
<p>同名定义的问题属于编码不规范，变量命名作用域按照块进行的。什么叫块？对于函数里面就是左右大括号构成一个块。</p>
<p>上面例子中，在 main 块里面定义的 <code>x := x</code> 右值 x 是全局变量，if 语句有个初始化变量 <code>x := 20</code>，在 if 块里面又定义一个 <code>x := x</code>。当我们打印 x 的时候，实际上会找一个离它最近的变量，如果没有，往外找一直找到全局。</p>
<p>这种命名习惯带来代码看上去非常别扭。会造成变量的遮蔽效应。所谓遮蔽效应就是最近的变量会遮蔽稍微远的变量。往外遮蔽总是访问最近的变量，但是最近的不好说，因为源码和汇编不是一回事。</p>
<p>汇编如何去理解？可能官方的文档里说访问相同作用域的优先。什么叫相同作用域？两个大括号匹配的区域叫做相同作用域，找不着就接着往外找。</p>
<p>那么最好的方式是变量命名有明确的定义，在相同作用域里对一个变量名的复用一定要慎重。代码的可阅读性和可维护性也是非常重要的，不要产生歧义或者误导。</p>
<h3 id="-3">退化赋值</h3>
<pre><code class="go language-go">//go:noinline
func test() (int, int) {
    return 1, 2
}
func main() {
    a, x := test()
    println(&amp;a, &amp;x)
    b, x := test()
    println(&amp;b, &amp;x)
}
</code></pre>
<ul>
<li>简短定义退化为对同一变量的赋值操作</li>
<li>必须有新变量被定义</li>
<li>常用于处理错误返回值（err）</li>
</ul>
<p>Go 语言函数允许返回多个值。test() 函数有两个返回值，<code>a, x := test()</code> 是简短定义写法，它同时定义了 a 和 x 两个变量，a 和 x 用于接收 test() 函数的返回值。<code>b, x := test()</code> 在相同作用域重复定义了 x 变量，但是这样写法是可以编译的。a 和 b 的地址不一样，但 x 地址一样，这就是所谓退化赋值的概念。第一次的时候 a 和 x 都是定义，但是第二次的时候 x 不是定义而是赋值，也就是说它会重复使用上面 x 的内存。</p>
<p>为什么出现退化赋值的概念呢？因为 Go 语言很多函数通过返回一个值和一个错误值来判断函数的结果对不对，我们为每个 err 定义内存是不合理的，最好的方式是复用内存，这样一来就变成所谓退化赋值的概念。</p>
<p>退化赋值有些要求，当进行所谓退化赋值的时候最少必须有一个新的变量未定义。</p>
<p>退化赋值在语法设计上有二义性，同一个符号 <code>:=</code> 在不同的地方有不同的解释。因为退化赋值必须有新的变量出现，所以符号 <code>:=</code> 是针对 b 的，而 x 只是顺便做赋值操作。</p>
<h3 id="-4">反汇编退化赋值</h3>
<pre><code class="bash language-bash">$ go build
$ go tool objdump -s "main\.main" test
TEXT main.main(SB)
 main.go:9 CALL main.test(SB)
 main.go:9 MOVQ 0(SP), AX
 main.go:9 MOVQ 0x8(SP), CX
 main.go:9 MOVQ AX, 0x20(SP) ; a
 main.go:9 MOVQ CX, 0x10(SP) ; x
 main.go:11 CALL main.test(SB)
 main.go:11 MOVQ 0(SP), AX
 main.go:11 MOVQ 0x8(SP), CX
 main.go:11 MOVQ AX, 0x18(SP) ; b
 main.go:11 MOVQ CX, 0x10(SP) ; x
</code></pre>
<p>我们通过输出变量的内存地址知道 x 复用内存空间。内部机制怎么实现呢？我们现在怎么去验证？</p>
<p>反汇编，调用 test 函数返回两个值，返回值应该保存在 0(SP) 和 0x8(SP)。第一次调用 AX 返回 a、a 指向 0x20(SP)，CX 返回 x、x 指向 0x10(SP)。第二次调用的时候，返回值 b 指向新的内存 0x18(SP)，x 依然指向 0x10(SP) 内存地址。很显然不管 print 输出内存地址还是反汇编都明确地知道 x 指向同一块内存。</p>
<p>我们为本专栏<strong>付费读者</strong>创建了微信交流群，以方便更有针对性地讨论专栏相关的问题。入群方式请添加 GitChat 小助手伽利略的微信号：GitChatty6（或扫描以下二维码），然后给小助手发「361」消息，即可拉你进群~</p>
<p><img src="https://images.gitbook.cn/FsONnMw_1O_6pkv-U-ji0U1injRm" width = "40%" /></p></div></article>