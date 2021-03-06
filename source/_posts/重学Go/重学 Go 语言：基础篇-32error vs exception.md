---
title: 重学 Go 语言：基础篇-32
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="errorvsexception">error vs exception</h3>
<p>在设计层面错误和异常代表了两种概念，实现上没有抽象概念，异常和错误实际上是抽象层面的事情。</p>
<p>假设错误代表了意外，那么异常可以理解一种可控的意外。</p>
<p>从 CPU 什么或者从汇编层面上来说，不存在错误和异常。因为哪怕就是一个浮点计算错误或许被零除 CPU 实际上操作系统对这个事情都是有预案的，它并没有导致计算机崩溃。</p>
<p>那也就是不管 CPU，还是操作系统对这个事都有一个预案，那么我们可不可以认为根本不存在错误和异常，在实现层面上没有这种东西。如果底层没有这种东西的话，那我们实际上就得放弃从底层来研究这些东西。</p>
<p>错误或者异常实际上可以看成第二种控制流。我们正常一个流控制是一条线，因为种种原因会发生另外一种条件。比如需要的文件找不着了、访问非法内存。在这里面隐隐约约会出现第二套控制流，实际上错误或者异常是备用逻辑、冗余方案，它本身也是正常的操作。</p>
<p>操作系统为了保护自己会阻止一些事情违反了它的保护的一些机制，违反约定，对操作系统来说，它会触发它另外一套机制，那显然是一种非常正常的逻辑，无非不受我们控制。</p>
<p>某些的情况下，我们是很难捕获到一些什么系统层面的异常，比如 runtime 层面 OS 层面的一些异常，这种异常最终是被权限级别更高的运行时或者操作系统捕获，同时我们捕获我们需要控制的东西。</p>
<p>所以从这一点上来说，自然语言里的错误并不适合把 error 或者 throw 一一对应。在编程体系里面，error 代表的不是错误而是另外一套逻辑。</p>
<p>我们可以主动地抛出异常改变流程控制，比如抛出异常来表达没有操作权限，通过异常可以跳过普通的函数调用体系实现远程跳转。跳转逻辑是限制在代码层面，异常实际上是在逻辑层面上完成这件事情。</p>
<p>异常在主动引发的情况下，分成不同的类型，不同的层级。我们通过不同的异常或者不同的捕获点类型来引发不同的跳转。异常和错误是代表了设计层面的理念。</p>
<ul>
<li><p>exception 代表可控，引发异常等于沿着调用堆栈做消息广播，然后把消息发给需要接收方，它们之间不存在耦合关系，我们把它当成一种正常的逻辑处理。</p></li>
<li><p>error 代表不可控。不可控仅仅是因为没有权限，比如运行时访问非法内存，它不属于逻辑层面上的东西，可能会引发一些非常危险的行为，应该交给的运行时或者操作系统让程序崩溃。</p></li>
</ul>
<p>当我们连接不了数据库的时候，或者我们监听一个端口被占用的时候，我们更合适的处理方式应该抛出 runtime 层面上的一个异常，明确地表达是不可修复性的，作为一种预警机制通知监控系统。</p>
<h3 id="">延迟调用的用途</h3>
<blockquote>
  <p>作用域、IDisposable</p>
</blockquote>
<p>IDisposable 在很多语言里面都有，一般的做法是使用 using，确保超出作用域的时候执行某一个方法做清理操作，比如 Disposable 方法，像 C# 或者 Java 都有类似这样的东西。确保超出作用域时候做些清理操作。</p>
<p>Go语言也有，但是级别不一样，像 Java 或者C#的using是语句块级别的，Go语言的延迟调用是函数级别的。</p>
<h3 id="deferfinally">defer 与 finally 的对比</h3>
<ul>
<li>defer 擅长分割微小逻辑。</li>
<li>finally “立即”执行，defer 延迟执行。</li>
<li>finally 嵌套可阅读性弱于 defer 语句。</li>
</ul>
<pre><code class="go language-go">    //每个地方可以只关闭一个
    defer f.Close()
    defer db.Close()

    try{

    }finally{
        //内部需要处理异常
        f.Close() //发生异常，直接跳出
        db.Close() //不会执行
    }
</code></pre>
<p>defer 相当于注册一个延迟调用，延迟调用什么时候执行呢？就是在函数退出时候才执行，using 是超出语句块就执行，这个有差别的。</p>
<p>如果忽略了作用域，defer 有点像 finally，因为结构化异常有这种做法<code>try/except/finally</code>，finally 块代码保证永远被执行，不管异常会不会抛出都会被执行。</p>
<p>defer  与 finally 不太一样的地方在于实现机制不一样，finally 依然是语句块级别的，finally 的作用域是 try 语句块，而 defer 不管在哪里注册的，都需要等函数调用结束的时候去执行，每个函数最后一条汇编指令是 ret，就是在这之前执行。</p>
<p>所以它的作用域比传统的结构化异常要大。</p>
<h3 id="-1">延迟调用</h3>
<pre><code class="go language-go">func main() {
    defer println("exit")
    defer func() {
    }()
}
</code></pre>
<blockquote>
  <p>在宿主函数终止前调用。</p>
</blockquote>
<ul>
<li>以 deferproc 注册延迟调用(立即对参数求值打包)。</li>
<li>在 ret 前，以 deferreturn 调用当前函数所属的全部延迟函数。</li>
<li>如果是 nil func，会引发运行时错误。</li>
<li>多个 defer 以 FILO 顺序执行。</li>
</ul>
<p>在延迟调用出现之前，在不同语言里都会有 atexit。它实际上会注册一个函数，函数在程序退出的时候执行。在很多 OOP 语言里有构造方法和析构方法，析构方法是这个对象死之前要干件事。一些语言有模块级别的初始化函数和模块退出。类似概念其实很多，都代表了一种延迟执行。</p>
<p>最常见的用来清理一些现场，比如说关闭数据连接关闭文件。它相当于给函数注册一个实例，在这个实例退出之前做出功能。</p>
<p>延迟执行的时候，<code>x</code>输出是1。</p>
<pre><code class="go language-go">func main(){
    x := 1
    defer println(x)
    x = 2
}
</code></pre>
<p>当执行<code>println(x)</code>的时候，并不是执行<code>println</code>，实际上把<code>println</code>函数的指针加上X进行打包交给<code>derferproc</code>函数去注册。<code>derfer</code>不是调用<code>println</code>函数是注册一次调用。</p>
<p>调用指的是立即执行，注册指的是把函数名字或者函数指针，函数所需要的参数打包放到某个地方以后去执行。所以<code>derfer</code>代表的不是执行而是注册操作。</p>
<p>既然把函数和参数进行打包，意味着它会把参数立即求值，即执行<code>derfer</code>时候，会立即把<code>x</code>计算出来，因为是值传递就把1传递进来，接下来对<code>x</code>的修改和它无关。如果是指针，实际上把指针打包；如果是函数，会立即打包函数的指针同时把结果立即计算出来，形成一次函数调用。</p>
<p><code>x</code>是一个参数的话会立即求值，因为它不会把 test 作为延迟函数进行打包，因为延迟函数本身只有一个，所有的东西全是它的参数，实际上把函数调用的返回值作为参数打包。</p>
<p>它究竟注册的是什么？第一个是函数，第二个是所有参数，它会立即求值，把参数和函数一起打包放在一个地方，等着后面去执行。因为这样对 X 的修改跟它没关系。</p>
<p><code>derfer</code>语句实际上形成两个函数调用，第一个是<code>derferproc</code>注册，把函数和参数打包放在一个地方不执行，然后在<code>RET</code>之前通过<code>deferreturn</code>函数来调用注册的函数。</p>
<p>每次 defer 语句都会形成一次注册，无论普通函数还是匿名函数。这个函数必须是可以调用的，如果是空函数肯定不行。多个 defer 语句是按照先进先出的顺序执行。</p>
<pre><code class="bash language-bash">$ go tool objdump -s "main\.main" test
TEXT main.main(SB)
 main.go:4 CALL runtime.deferproc(SB)
 main.go:5 CALL runtime.deferproc(SB)
 main.go:5 TESTL AX, AX
 main.go:5 JNE 0x104df8e
 main.go:6 CALL runtime.deferreturn(SB)
 main.go:6 RET
</code></pre></div></article>