---
title: 重学 Go 语言：基础篇-42
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="05newmake">05 用new或make创建引用类型的差别</h3>
<p>在不同语言里，对分配内存不同做法，Go语言分为两种方式，一种是new，一种是make，这两种方式有很大的差别，我们new一个类型，比如<code>new(int)</code>的时候怎么分配内存呢，它计算出类型的长度，int是8bit，然后在堆上或者也可能在栈上分配空间然后返回这个指针，不管是什么类型都是一样的。</p>
<p>new一个数组<code>new([8]byte)</code>计算类型的长度8bit，分配8字节内存空间，指针返回；</p>
<p>new一个切片<code>new([]byte)</code>计算类型长度(ptr(8bit)+len(8bit)+cap(8bit))，三个字段组成的24字节内存空间，指针返回。</p>
<p>new并不会把复合结构完整的去创建，它只计算出当前这个类型究竟需要占用多大的内存空间。很显然用new创建切片，这个切片本身是没有办法工作的，其中指针ptr没有指向任何底层的数组，因为切片是用来管理数组的，如果被管理的对象不存在的话，那这个管理对象本身没有任何意义。</p>
<p>Go语言对于一些复合结构使用了一个语法糖，表面上看上去make函数，但实际上这个make函数是一个语法糖结构，当我们去<code>make([]byte,0,8)</code>时候，首先会创建切片本身头对象(ptr,len,cap)，然后创建底层数组，数组容量是8个，然后把指针指向开始位置，len设为0，cap设为8。很显然make操作就包含了几个步骤：</p>
<ul>
<li>第一步创建切片本身</li>
<li>第二步分配底层数组</li>
<li>第三步初始化切片属性</li>
</ul>
<p>整个make操作是由这三部分组成的，它会翻译成标准的<code>makeslice</code>函数。</p>
<p><img src="images/array_makeslice.png" alt="" /></p>
<p>为什么说Go语言用make创建引用类型比较坑爹，因为把它称之为引用类型仅仅是由于有一个指针，引用其他的数据结构，这样的结构称之为引用类型。就是当前类型内部有一个指针引用另外一个数据结构，和C#、Java的引用类型很大的差别。</p>
<h3 id="05">05 切片传递</h3>
<pre><code class="go language-go">//go:noinline
//go:nosplit
func test(x []int) {
    fmt.Println(x)
}
func main() {
    a := [...]int{0x11, 0x22, 0x33, 0x44}
    b := a[:]
    test(b)
}
</code></pre>
<pre><code>$ go build -gcflags "-m -S" 2&gt;a.txt
</code></pre>
<blockquote>
  <p>切片可能导致堆内存分配。</p>
</blockquote>
<p>切片本身是一个很简单的结构体，那么传递切片的时候，Go语言是值传递，即拷贝三个字段，底层数组和切片不是一个整体。这就是切片传递的时候代价很小。</p>
<p>底层数组如果非常大的情况下，复制切片复制三个字段就可以了。反汇编看到内存逃逸，通过newobject分配内存，<code>statictmp_0</code>是把字面量统一打包到rodata起个名字，把字面量复制进去，接下来把三个参数入栈调用test。</p>
<h3 id="05-1">05 如何比较两个切片内容相等？</h3>
<p>切片操作不支持负索引，不支持倒序，不支持步进。它就是非常简单的半开区间。</p>
<p>切片不支持比较。</p>
<p>比较意义</p>
<pre><code class="go language-go">func main() {
    a := [...]byte{1, 2, 3}
    //b := a //b必然是复制了一份a
    b := [...]byte{1, 2, 3}

    fmt.Println(a == b)
}
</code></pre>
<p>这个意思不是说判断a和b指向同一个对象，因为它不是判断指针，我们想判断它们的内容是否相同。<code>{1, 2, 3}</code>是有存储顺序的，它每个元素长度是固定的，所以按照这东西比较，当其中任何一个不符的话它就会返回一个假值。</p>
<p>我想判断两个切片内容相等怎么办？转换为[]byte，然后bytes.Equal</p>
<pre><code class="go language-go">func main() {
    a := []int{1, 2, 3}
    b := []int{1, 2, 3}

    //fmt.Println(a == b)

    //错误方法
    xa := *(*[]byte)(unsafe.Pointer(&amp;a))
    xb := *(*[]byte)(unsafe.Pointer(&amp;b))
    fmt.Println(bytes.Equal(xa, xb))

    type header struct {
        ptr *int //可以持有这个指针，也可以不持有
        len int
        cap int
    }

    ah := header{&amp;a[0], len(a) * 8, len(a) * 8}
    bh := header{&amp;b[0], len(b) * 8, len(b) * 8}

    ax := *(*[]byte)(unsafe.Pointer(&amp;ah))
    bx := *(*[]byte)(unsafe.Pointer(&amp;bh))

    fmt.Println(bytes.Equal(ax, bx))
}
</code></pre>
<p><code>invalid operation: a == b (slice can only be compared to nil)</code>错误提示slice只能比较是否为nil，也就只能说是否初始化过，但是我们不能用来比较两个切片内容是否相同。</p>
<p>标准库<code>bytes.Equal</code>提供了按照字节来比较两个字节切片内容是否相同，但是如果不是字节怎么办。这种场景很多，有时候我们拿到两份数据，我们想判断这两份数据是否相同。一种情况它们指向相同地址相同长度的内存，如果它们不在同一块内存怎么办？既然标准库提供了<code>bytes.Equal</code>，我们无非把它们转换为字节切片<code>[]byte</code>就好了。</p>
<p>当你手上持有指针的时候，可以转换任何内存结构。</p>
<p><code>*(*[]byte)(unsafe.Pointer(&amp;a))</code>转换出来的到底是头部还是指向的底层数组？我们的目标实际上是比较底层的数据是否相同。</p>
<p>切片的结构体{指针、长度、容量}是一块内存，指针指向的底层数组是一块内存，很显然<code>&amp;a</code>取出来的是结构体的内存地址，<code>*(*[]byte)(unsafe.Pointer(&amp;a))</code>转换完依然是{指针、长度、容量}，是比较第一个整数的三字节，后面相等不相等理论都一样。</p>
<p>切片的结构体{指针Ptr、长度3、容量3}，指针指向的底层数组<code>[...]int{1, 2, 3}</code>，底层数组小端布局实际上是<code>[...]byte{10000000, 01000000, 11000000}</code>。如果把切片头部从<code>[]int</code>转换为<code>[]byte</code>的时候，新的切片结构体是{指针Ptr、长度3、容量3}，实际上是比较3个字节，后面根本不比较。</p>
<p>所以当你转换的时候你有没有考虑过不同单位可能会存在长度不一致的问题，int类型的长度和byte类型的长度在内存中是不一样的。所以需要明白这种转换到底是合法的还是不合法的。那么转换完我们需要长度调整，接下来需要修改<code>[]byte</code>里面的数据。那么原来的信息可能被我们改掉，因为<code>[]int</code>和<code>[]byte</code>内存是同一块内存，只是转换一个指针类型。</p>
<p>最简单的做法我们抛弃对方的切片结构，取出来第一个元素的地址，重新去构建新的头，不直接使用原来的头部信息。</p>
<p>虽然我们了解header结构，但是内存转换的时候一定需要搞清楚内存布局是什么样的，当我们把<code>[]int</code>转换为<code>[]byte</code>的时候，其实用同样的一块内存，只是换种方式来访问，因为数据类型不同，导致访问的内存单位发生变化，原来访问3个整数，现在变成访问3个字节，因为len和cap还是3，你没有修改这个数字。所以转换为<code>[]byte</code>的时候，你需要把len和cap相应的长度转换为新的步进长度。同时需要注意，你不应该修改原来的值。</p>
<p>当你做一些东西的时候一定需要搞清楚内存布局是什么样的这样才能保证你所有的操作是安全的。当你拿到指针的时候你意味着很危险的，因为指针可以越界，而且不同类型的指针访问路径是不一样的。</p></div></article>