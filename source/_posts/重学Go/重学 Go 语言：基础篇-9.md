---
title: 重学 Go 语言：基础篇-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>所谓引用类型，是指其内部结构，而非分配于托管堆。</p>
<ul>
<li>slice、map、channel</li>
<li>使用 make 或初始化语句创建实例</li>
<li>使用 new 无法有效初始化</li>
</ul>
<p>从实现角度看，除 slice、interface是结构体外，map、channel、function 都是指针。</p>
<p>引用类型对初学者来说很容易造成误解。在 Go 语言里 slice、map、channel 三种类型称之为引用类型，Java 或者 C# 语言明确区分值类型和引用类型，值类型默认情况下在栈上分配，引用类型在堆上分配，垃圾回收器在托管堆上处理。值类型会涉及到装箱和拆箱。</p>
<p>Go 语言的引用类型只是一种行为上的概念，所谓的引用类型更多时候指的是它引用另外一块或者多块内存，用另外一块或者多块内存来存储或者处理一些相关的数据结构，至于这两块内存分配栈上还是堆上是由编译器决定的。任何时候编译器优先在栈上分配，避免对垃圾回收器造成负担。</p>
<p>所以所谓的引用类型，它内部需要引用另外一块内存，引用另外一块内存也就意味着必须有初始化的操作。切片引用另外一块数组，字典引用哈希桶。</p>
<pre><code class="go language-go">m := make(map[string]int)
</code></pre>
<p>使用 make 初始化，从抽象层面上来看 m 是一个字典，从实现角度来看 m 是指针的包装。make 创建了一个复合的数据内存，然后把它的头部信息用指针的方式返回，字典在不同的函数参数传递的时候其实复制的是这个指针。当我们创建字典的时候，它内部有很复杂的数据结构，真正去持有的这个字典其实就是一个指针的包装。</p>
<p>学习新的语言的时候，抽象层面上是一个类型，但是在实现层面上可能就是指针，只有用实现层面角度去观察，很多行为才能解释得通。</p>
<h3 id="">初始化语法</h3>
<p>有个变量 x 是个数组，正常情况下定义没问题，如果换行的话需要加个 <code>,</code>，这属于语言规范的内容。</p>
<pre><code class="go language-go">func main() {
    x := [4]int{1, 2, 3}

    y := [4]int{
        1,
        2,
        3,
    }

    z := [4]int{
        1,
        2,
        3}

    fmt.Println(x, y, z)
}
</code></pre>
<h3 id="make">引用类型初始化语句和 make 的区别</h3>
<pre><code class="go language-go">func main() {
    a := []int{}
    _ = a
}
</code></pre>
<pre><code>TEXT main.main(SB)
 main.go:4 LEAQ 0(SP), AX
 main.go:4 MOVQ AX, 0(SP)
 main.go:4 TESTB AL, 0(AX)
 main.go:4 JMP 0x104df2a
 main.go:4 MOVQ AX, 0x8(SP)
 main.go:4 XORPS X0, X0
 main.go:4 MOVUPS X0, 0x10(SP)
</code></pre>
<pre><code class="go language-go">func main() {
    a := make([]int, 0)
    _ = a
}
</code></pre>
<pre><code>TEXT main.main(SB)
 main.go:4 LEAQ 0(SP), AX
 main.go:4 TESTB AL, 0(AX)
 main.go:4 JMP 0x104df26
 main.go:4 MOVQ AX, 0(SP)
 main.go:4 XORPS X0, X0
 main.go:4 MOVUPS X0, 0x8(SP)
</code></pre>
<p>初始化语句可提供初始元素，make 函数可预分配内存。</p>
<p>对于引用类型来说，一种方式是使用 make 函数创建，另外一种方式是用初始化语句来创建，这两者在底层上没有什么区别。</p>
<p>我们学习语言很多时候都会遇到类似的问题，用不同的方式来创建一个对象。反汇编以后它大体上是差不多的，所以在编译器眼里是一回事。</p>
<p><code>a := []int{}</code> 可以提供初始化值，make 函数没有办法初初始化值的。但是 make 函数允许预分配内存，避免后面扩展。</p>
<h3 id="newmake">内置函数 new 和 make 的区别</h3>
<p>两者不存在功能重叠或替换。</p>
<ul>
<li>new 按类型大小分配零值内存。</li>
<li>make 转换为目标初始化函数（makeslice）。</li>
<li>make 可通过 len/cap 预分配内存。</li>
<li>初始化函数需分配多块内存，设置内部属性。</li>
<li>编译器优先在栈分配内存。</li>
</ul>
<p>new 返回指针，make 返回实例。</p>
<p>对 new 来说，new 只分配一块被初始化为零值的内存，然后返回它的指针。如果是 new 字典，字典是个指针，它只是返回 8 字节内存，new 不初始化数据，那哈希桶的引用、指数的计算、哈希函数的处理等初始化操作根本不处理，这个字典肯定用不了。</p>
<p>new 只负责按照右边的类型来分配一块内存，这块内存有可能在栈上，也有可能在堆上。</p>
<pre><code class="go language-go">func main() {
    p := new(map[string]int)
    _ = p
}
</code></pre>
<p>我们反汇编看一下：</p>
<pre><code class="bash language-bash">$ go build -gcflags "-N -l"
$ go tool objdump -s "main\.main" test
</code></pre>
<p>注意到在栈上分配的内存，它是把 0x8 地址赋值 AX 里，然后从 AX 赋值 SP0，是 8 字节，除此之外什么没做。</p>
<p>make 可以指定长度和容量：</p>
<pre><code class="go language-go">func main() {
    s := make(map[string]int, 100)
    _ = s
}
</code></pre>
<p>我们反汇编看一下：</p>
<pre><code class="bash language-bash">$ go build -gcflags "-N -l"
$ go tool objdump -s "main\.main" test
</code></pre>
<p>我们会注意到 make 翻译成具体的初始化函数。make 除了分配一系列的内存以外，它内部要执行一套很复杂的、跟这个类型有关系的一套逻辑。比如字典计算出哈希桶，哈希函数数组分配多长，是否要提前预分配，分配完处理哈希函数、桶的链接，这一整套初始化过程。</p></div></article>