---
title: 重学 Go 语言：基础篇-65
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="02receiver">02 隐式实例接收参数receiver</h3>
<p>Go限制是给一个类型定义方法只能在当前包，如果不是在当前包不能为它定义方法。像C#可以给标准库里面的类型增加扩展方法。Go涉及的思想基于的是包是个封闭状态，定义扩展方法实际上是侵入式设计。我们设计时候尽可能希望依赖关系变得很简单，因为多数时候我们并不需要把我们依赖的东西暴露出去。</p>
<p>定义方法两种方式，第一种选择与接口类型相绑定<code>pointer</code>，还有一种选择与值类型相绑定<code>value</code>。这隶属于不同的方法集。</p>
<p>创建一个变量，有两种执行方式，直接用值类型调用接口方法。或者取指针，指针同样会调用任何方法。编译器会帮我们处理类型的转换，这就是很典型的语法糖。换句话说，我们不应该用方法的概念理解它，这种语法糖给我们的困惑在于为什么区分<code>*X</code>和<code>X</code>。是因为如果把方法翻译为函数，不要用方法来理解把它转换为函数来理解，就会知道这两种函数执行方式根本不同。方法和函数的区别在于第一个参数，编译器其实做了很特殊的处理在于把方法用特殊的语法表达出来然后执行时候也用特殊的语法来表达，其实就是编译器上的语法糖。不管是方法还是函数翻译到汇编层面其实就是text段一段代码，方法和函数都要传参数。</p>
<p>不管是用值类型调用还是指针调用，它就是把第一个参数翻译一下。</p>
<pre><code class="go language-go">type X int

func (x *X) pointer() {
    fmt.Printf("p: %p: %v\n", x, *x)
}

func (x X) value() {
    fmt.Printf("v: %p: %v\n", &amp;x, x)
}

func main() {
    var x X = 0x1234
    fmt.Printf("x: %p: %v\n", &amp;x, x)

    //值类型调用方法
    println("---x.call---")

    x.pointer() //用值类型调用指针方法时候，它会自动帮我们取地址，可以看成pointer(&amp;x)，那么输出地址信息和x的地址信息是一样的
    x.value() // 默认情况下x被拷贝的，上面拷贝的是指针，这是拷贝完整对象类型，我们看到它的地址和x是不一样的，被复制过了

    //指针类型调用方法
    println("---p.call----")

    var p *X = &amp;x
    p.pointer() //用指针类型调用指针方法时候
    p.value() //用指针类型调用值方法时候，指针做取值操作，value(*p)，因为接收的第一个参数是值类型，提供的指针先需要把值取出来。
}
</code></pre>
<p>不管用值调用或者指针调用也好，归根结底和调用没有关系，关键是根据操作的类型编译器完成自动转换操作。转换操作是由编译器完成的，其实就是语法糖。</p>
<p>Go没有方法，就是一直特殊函数，方法并不是说编译器编译完了有方法这个东西，它只是很特殊的调用格式。因为不管是方法还是函数，它实际上是一段汇编指令，这个指令存在text段里面，然后有个地址，调用指令的时候必须先提供相应的参数，然后用call指令调用。方法和函数的区别在于第一个参数怎么样处理。函数显式提供，方法通过实例提供。</p>
<h3 id="02tt">02 T或*T类型方法</h3>
<p>这么做很显然让Go整个OO这方面复杂度提升了很多，而且相当的别扭。但是我们把方法还原成函数，所有语法糖全部取消，这样的意图很简单。</p>
<p>传指针就是要修改目标对象、复制成本太高。方法是绑定在特定对象上的行为，方法是OOP很核心的理念，代表当前实例的的行为，修改当前对象状态，输出当前对象状态。属性是很特殊的方法，尽可能不要暴露字段，通过属性和方法暴露。OO的核心理念是封装，封装也就意味着只能通过逻辑交流，逻辑就是一段代码，方法就是做两件事，一是通过接收参数改变自己，二是输出当前内部状态。从这两个理由不可能把当前对象复制两份做别的事情。</p>
<p>传值就是复制当前实例，得到复制品，针对复制品进行操作，这里面的行为和当前实例没有关系，复制操作是调用方法之前完成复制操作。从设计角度来说，当我们把数据用复制的方式传递过去以后它就应该和当前实例脱离关系没有任何关联。更希望把它设计为独立函数，它接收参数操作完整个生命周期就结束了，和当前类型没有任何关系。它和我们操作的对象实例没有耦合关系。</p>
<p>这是基于传统设计模式的想法，这种想法讲究的是不要把于当前实例无关系的功能放进来，只是借鉴约定并没有耦合关系。<code>pointer</code>和当前实例绑定很正常，想尝试修改实例的某个值，或者输出内部很大的数据，符合我们通常设计的OO理念。<code>value</code>应该考虑是否能从当前类型独立出去，因为它不会修改当前类型的任何状态，就相当于x通过消息队列mq传递给<code>value</code>执行，这种架构好处可以把<code>value</code>函数放到其他的类型甚至包里面和当前类型脱离。</p>
<p>方法总是和某个实例相绑定，例如bound－method就是当某个方法与实例相绑定的时候它才能执行。</p>
<p>还有个地方，Go官方文档推荐方法的参数建议用很简短的字母来代替，但是我们在大多数语言通常习惯于this、self特指当前实例。可能因为Go一开始就没有方法这个说法，如果转化为函数的话使用this、self参数名就非常别扭。</p>
<h3 id="02">02 指针不能是临时变量</h3>
<p>当方法不再是方法的时候，是特殊函数的时候，很多事很容易理解。我们为类型提供了两个方法，正常调用都可以。</p>
<p><code>X</code>是类型，在类型实例上调用方法<code>pointer</code>，首先有个对象实例，然后调用方法，实例必须要存在。拥有一个不存在的对象实例可以调用它的方法？</p>
<p><code>pointer</code>方法属于<code>*X</code>类型，<code>p</code>已经有内存空间了，是8byte，都为00000000。就是<code>p</code>对象已经存在，调用<code>p</code>自己的方法没有问题。</p>
<p>用函数的眼光看待方法。<code>X</code>和<code>*X</code>属于不同类型。</p>
<p><code>X{}</code>是创建临时对象，但是没有任何变量引用它。<code>(X{}).pointer()</code>不能取得地址，这地方涉及到传参问题，我们把方法还原成函数<code>value(X)</code>、<code>pointer(*X)</code>，调用<code>value(X{})</code>和<code>pointer(&amp;(X{}))</code>没有问题。为什么用方法方式不行。</p>
<p><code>(X{}).pointer()</code>是语法糖，实际上是创建了一个临时变量<code>X{}</code>，临时变量取地址操作，然后把地址复制，去执行<code>pointer</code>方法。没有语言支持临时变量取地址操作。有左值和右值才会叫变量，<code>X{}</code>必须存个地方然后才能取地址操作。</p>
<pre><code class="go language-go">type X struct{}

func (X) value() {
}

// type *X
func (*X) pointer() {
}

func main() {
    var p *X = nil

    p.pointer() //正常调用
    (*X)(nil).pointer() //等同上面

    p.value()

    (X{}).value() // X{} -&gt; x:copy -&gt; value
    //(X{}).pointer() //不能取得地址 X{} -&gt; &amp;temp -&gt; p:copy -&gt; pointer
}
</code></pre></div></article>