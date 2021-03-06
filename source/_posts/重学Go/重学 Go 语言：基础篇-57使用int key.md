---
title: 重学 Go 语言：基础篇-57
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="intkey">使用int key</h3>
<p>使用整数key比使用字符串key要快，这个很正常。<code>makemap</code>函数会检查key和value的长度，默认长度是128字节，也就是说小于或者等于128字节它会把数据直接拷贝到字典里面去，如果是整数的话整个key都在字典中，如果字符串只有两个数据结构指针和长度在字典中，指针还指向另外一个数组。很显然读取key的时候分成两步，先在字典里面读取字符串头信息再读取字符串的内容。比起int直接读出来性能肯定有差异的。</p>
<p>所以某些时候不需要用字符串当作key，因为很多数据的key不见得是字符串，比如有一个全局的序号生成器，未必是自增的，但需要保持全局有唯一的id，用id做key，访问效率要高很多。</p>
<pre><code class="go language-go">var (
    intKeys []int
    strKeys []string

    m1 map[int]struct{}
    m2 map[string]struct{}
)

func init() {
    for i := 0; i &lt; 100000; i++ {
        intKeys = append(intKeys, i)
        strKeys = append(strKeys, strconv.Itoa(i))
    }

    m1 = make(map[int]struct{})
    m2 = make(map[string]struct{})
}

func testIntKeys() {
    // 往里面插入数据
    for _, k := range intKeys {
        m1[k] = struct{}{}
    }
    // 读出来
    for k := range m1 {
        _ = m1[k]
    }
}

func testStrKeys() {
    for _, k := range strKeys {
        m2[k] = struct{}{}
    }
    for k := range m2 {
        _ = m2[k]
    }
}

func BenchmarkIntKeys(b *testing.B) {
    for i := 0; i &lt; b.N; i++ {
        testIntKeys()
    }
}

func BenchmarkStrKeys(b *testing.B) {
    for i := 0; i &lt; b.N; i++ {
        testStrKeys()
    }
}
</code></pre>
<pre><code class="bash language-bash">$ go test -v -bench . -benchmem
</code></pre>
<pre><code class="bash language-bash">BenchmarkIntKeys-8           300           5727832 ns/op               0 B/op          0 allocs/op
BenchmarkStrKeys-8           200           8196354 ns/op               0 B/op          0 allocs/op
</code></pre>
<p>很显然，整数要比字符串快很多，关键问题我们需要了解实现的结构才能有针对的选择适合我们的做法。任何时候字典都比我们想象的复杂，当数据量非常大的时候，如果选型选的不好，可能会造成很严重的性能问题。</p>
<h3 id="20">20 嵌入存储可减轻垃圾回收压力</h3>
<pre><code class="go language-go">func main() {
    const N = 128 // 129
    m := make(map[int][N]byte)
    for i := 0; i &lt; 100000; i++ {
        m[i] = [N]byte{}
    }
    for {
        println(len(m))
        runtime.GC()
        time.Sleep(time.Second)
    }
}
</code></pre>
<pre><code>$ 128
gc 6 @0.053s 0%: 0.005+0.15+0.044 ms clock, 0.020+0/0.073/0.12+0.17 ms cpu, 20-&gt;20-&gt;20 MB, 38 MB goal, 4 P (forced)
gc 7 @1.057s 0%: 0.006+0.27+0.060 ms clock, 0.027+0/0.093/0.32+0.24 ms cpu, 20-&gt;20-&gt;20 MB, 40 MB goal, 4 P (forced)
$ 129
gc 6 @2.059s 0%: 0.006+5.7+0.043 ms clock, 0.027+0/0.12/5.8+0.17 ms cpu, 16-&gt;16-&gt;16 MB, 32 MB goal, 4 P (forced)
gc 7 @3.068s 0%: 0.007+7.4+0.046 ms clock, 0.030+0/0.13/7.3+0.18 ms cpu, 16-&gt;16-&gt;16 MB, 32 MB goal, 4 P (forced)
</code></pre>
<blockquote>
  <p>嵌入存储（非指针）可有效减少垃圾回收需要扫描的对象数量。</p>
</blockquote>
<p>字典使用桶存储键值对，存储是嵌入式的存储。数据小于或等于128字节直接把数据拷贝到它内部，对垃圾回收器的扫描时间小很多，我们来简单测试。对比分别存储长度128的数组和长度129的数组，看垃圾回收器的压力，主要看扫描时间，我们可以注意到扫描所消耗的时间明显大了很多。</p>
<p>如果数据长度在128以内，直接把数据存到数组里面，对垃圾回收器来说，不需要扫描数据项因为字典是一个对象，数据长度超过128的时候，对象必须存在外部，数组里存的是指针，对垃圾回收器来说除了扫描字典以外，外部对象也需要扫描，垃圾回收器的压力会大很多。我们尽可能把KeyValue嵌入存到map里提升性能。如果存指针的话，对象在外部。</p>
<p>其实是runtime对他的优化，默认情况下，如果没有超过128字节，他会把数据直接拷贝到字典里面去，数据拷贝到字典以后有个特点是GC去扫描的时候，只要字典对象活着，里面所有存的数据是不需要扫描的，也就是说哪怕有100w项只需要扫描一次。另外一点是假如存的是一个指针，然后指向另外一个对象，另外的对象也会被GC扫描，就要扫描100w次。</p>
<p>所以有些时候应该考虑把数据直接存在字典内部不需要一个指针再去引用它，当然这里有个限制，大小不能超过128字节，但是很多时候其实够用了，因为key的长度超过128字节情况很小，就像uuid也就64字节就够了，value的结构对于简单的数据结构128字节也够用了。</p>
<p>如果全部存到字典里没有外部引用的话只检查一个字典是不是还活着就可以了。但指针引用堆上对象时候，那堆上所有对象都得被扫描。</p>
<pre><code class="go language-go">func main() {
    // 创建一个数据类型，长度是100字节没有超出限制是保存在字典内部
    type data struct {
        x [100]byte
    }

    // 创建一个字典
    m := make(map[int]data)
    // m := make(map[int]*data) //保存指针

    // 添加数据
    for i := 0; i &lt; 1000000; i++ {
        m[i] = data{}
        // m[i] = new(data) //在堆上分配，然后把指针保存到字典里面去
    }

    for {
        runtime.GC()
        time.Sleep(time.Second)
    }
}
</code></pre>
<pre><code class="bash language-bash">$ GODEBUG=gctrace=1 go run main.go
</code></pre>
<p>我们这时候跟踪垃圾回收占用CPU百分比，就是用于垃圾回收的时间占整个程序运行的百分比。换成指针，我们注意到垃圾回收的占比非常的高，因为扫描对象多。</p>
<p>我们需要测试数据容器到底有什么弊端，优点和缺点是什么？开发东西就知道到底合不合用。如果不合用怎么办。只有了解缺点时候才能避开缺点。</p>
<h3 id="">键值保存</h3>
<p>键值有两种存储方式，第一种所有哈希表上只存指针，那么键值都会保存到堆上去，有多少对键值就会在堆上分配多少对象，这样显然对我们的性能带来很大的影响。</p>
<p>把键值的值直接复制到字典里，用字典来存。这样有助于减少在堆上的对象数量，有助于减少垃圾扫描的时间。</p>
<pre><code class="go language-go">var m = make(map[int]*int)

func pointer() {
    for i := 0; i &lt; 1000000; i++ {
        value := i  // i 变量复用，所以用 value。
        m[i] = &amp;value
    }
}

func main() {
    pointer()

    for i := 0; i &lt; 10; i++ {
        runtime.GC()
        time.Sleep(time.Second)
    }
}
</code></pre>
<p>创建一个字典，value用指针方式来存。</p>
<pre><code class="go language-go">var m = make(map[int]int)

func value() {
    for i := 0; i &lt; 1000000; i++ {
        m[i] = i
    }
}

func main() {
    value()

    for i := 0; i &lt; 10; i++ {
        runtime.GC()
        time.Sleep(time.Second)
    }
}
</code></pre>
<p>我们把Key和Value全部存到字典里面。</p>
<pre><code class="bash language-bash">$ GODEBUG="gctrace=1" go run gc_pointer.go
</code></pre>
<pre><code>gc 1 @0.024s 2%: 0.005+2.4+0.008 ms clock, 0.005+0.46/0.080/0+0.008 ms cpu, 4-&gt;4-&gt;0 MB, 5 MB goal, 1 P
# command-line-arguments
gc 1 @0.000s 28%: 0.002+3.6+0.011 ms clock, 0.002+1.2/0/0+0.011 ms cpu, 4-&gt;5-&gt;5 MB, 5 MB goal, 1 P
gc 2 @0.005s 23%: 0.001+8.9+0.004 ms clock, 0.001+1.2/0.85/0+0.004 ms cpu, 6-&gt;8-&gt;8 MB, 10 MB goal, 1 P
gc 3 @0.014s 21%: 0.001+16+0.006 ms clock, 0.001+0.67/2.7/0+0.006 ms cpu, 10-&gt;12-&gt;11 MB, 16 MB goal, 1 P
gc 4 @0.039s 24%: 0.003+13+0.007 ms clock, 0.003+1.8/4.1/0+0.007 ms cpu, 15-&gt;17-&gt;15 MB, 22 MB goal, 1 P
gc 1 @0.012s 8%: 0.003+15+0.005 ms clock, 0.003+1.4/0.85/0+0.005 ms cpu, 5-&gt;6-&gt;4 MB, 6 MB goal, 1 P
gc 2 @0.029s 13%: 0.002+21+0.004 ms clock, 0.002+0.59/3.7/0+0.004 ms cpu, 9-&gt;9-&gt;8 MB, 10 MB goal, 1 P
gc 3 @0.065s 16%: 0.004+6.8+0.020 ms clock, 0.004+0.34/4.8/0+0.020 ms cpu, 9-&gt;9-&gt;6 MB, 16 MB goal, 1 P
gc 4 @0.074s 21%: 0.002+21+0.004 ms clock, 0.002+0.44/8.3/0+0.004 ms cpu, 16-&gt;16-&gt;16 MB, 17 MB goal, 1 P
gc 5 @0.145s 20%: 0.003+32+0.004 ms clock, 0.003+2.1/14/0+0.004 ms cpu, 38-&gt;38-&gt;33 MB, 39 MB goal, 1 P
gc 6 @0.217s 22%: 0.003+33+0.005 ms clock, 0.003+0.55/17/0+0.005 ms cpu, 34-&gt;35-&gt;24 MB, 66 MB goal, 1 P
gc 7 @0.285s 24%: 0.003+117+0.005 ms clock, 0.003+3.5/38/0+0.005 ms cpu, 66-&gt;66-&gt;66 MB, 67 MB goal, 1 P
gc 8 @0.448s 23%: 0.005+33+0.004 ms clock, 0.005+0/16/16+0.004 ms cpu, 67-&gt;67-&gt;45 MB, 133 MB goal, 1 P (forced)
gc 9 @1.482s 8%: 0.005+73+0.005 ms clock, 0.005+0/14/58+0.005 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 10 @2.557s 5%: 0.008+62+0.004 ms clock, 0.008+0/15/47+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 11 @3.620s 4%: 0.009+69+0.004 ms clock, 0.009+0/15/54+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 12 @4.691s 3%: 0.008+62+0.004 ms clock, 0.008+0/15/47+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 13 @5.754s 3%: 0.009+69+0.004 ms clock, 0.009+0/15/54+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 14 @6.824s 3%: 0.009+79+0.004 ms clock, 0.009+0/19/60+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 15 @7.904s 2%: 0.008+75+0.004 ms clock, 0.008+0/15/59+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 16 @8.980s 2%: 0.008+61+0.004 ms clock, 0.008+0/15/46+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
gc 17 @10.050s 2%: 0.009+66+0.004 ms clock, 0.009+0/15/50+0.004 ms cpu, 45-&gt;45-&gt;45 MB, 91 MB goal, 1 P (forced)
</code></pre>
<pre><code class="bash language-bash">$ GODEBUG="gctrace=1" go run gc_value.go
</code></pre>
<pre><code>gc 1 @0.023s 1%: 0.004+2.0+0.007 ms clock, 0.004+0.40/0/0+0.007 ms cpu, 4-&gt;4-&gt;0 MB, 5 MB goal, 1 P
# command-line-arguments
gc 1 @0.000s 27%: 0.002+3.6+0.005 ms clock, 0.002+1.1/0/0+0.005 ms cpu, 4-&gt;5-&gt;5 MB, 5 MB goal, 1 P
gc 2 @0.005s 23%: 0.001+9.9+0.004 ms clock, 0.001+2.4/0/0+0.004 ms cpu, 6-&gt;9-&gt;8 MB, 10 MB goal, 1 P
gc 3 @0.015s 19%: 0.001+22+0.007 ms clock, 0.001+1.6/2.2/0+0.007 ms cpu, 10-&gt;14-&gt;13 MB, 17 MB goal, 1 P
gc 4 @0.041s 22%: 0.002+18+0.007 ms clock, 0.002+1.7/4.2/0+0.007 ms cpu, 14-&gt;17-&gt;16 MB, 26 MB goal, 1 P
gc 1 @0.013s 0%: 0.002+0.21+0.005 ms clock, 0.002+0.067/0/0+0.005 ms cpu, 5-&gt;5-&gt;3 MB, 6 MB goal, 1 P
gc 2 @0.021s 0%: 0.003+0.32+0.003 ms clock, 0.003+0.10/0/0+0.003 ms cpu, 9-&gt;9-&gt;7 MB, 10 MB goal, 1 P
gc 3 @0.041s 0%: 0.002+0.42+0.004 ms clock, 0.002+0.14/0/0+0.004 ms cpu, 8-&gt;8-&gt;5 MB, 15 MB goal, 1 P
gc 4 @0.042s 1%: 0.001+5.8+0.005 ms clock, 0.001+0.17/0.032/0+0.005 ms cpu, 15-&gt;15-&gt;15 MB, 16 MB goal, 1 P
gc 5 @0.077s 0%: 0.003+6.0+0.010 ms clock, 0.003+0.16/0/0+0.010 ms cpu, 16-&gt;17-&gt;11 MB, 30 MB goal, 1 P
gc 6 @0.083s 1%: 0.001+4.2+0.005 ms clock, 0.001+0.22/0.045/0+0.005 ms cpu, 30-&gt;30-&gt;30 MB, 31 MB goal, 1 P
gc 7 @0.144s 0%: 0.003+4.3+0.004 ms clock, 0.003+0.18/0.014/0+0.004 ms cpu, 31-&gt;31-&gt;20 MB, 60 MB goal, 1 P
gc 8 @0.168s 1%: 0.002+0.83+0.003 ms clock, 0.002+0/0.51/0+0.003 ms cpu, 60-&gt;60-&gt;60 MB, 61 MB goal, 1 P
gc 9 @0.240s 0%: 0.002+0.098+0.003 ms clock, 0.002+0/0.092/0+0.003 ms cpu, 60-&gt;60-&gt;38 MB, 120 MB goal, 1 P (forced)
gc 10 @1.240s 0%: 0.008+0.54+0.035 ms clock, 0.008+0/0.53/0+0.035 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 11 @2.243s 0%: 0.008+0.58+0.010 ms clock, 0.008+0/0.54/0+0.010 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 12 @3.246s 0%: 0.008+0.60+0.013 ms clock, 0.008+0/0.58/0+0.013 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 13 @4.249s 0%: 0.003+0.11+0.002 ms clock, 0.003+0/0.10/0+0.002 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 14 @5.250s 0%: 0.008+0.54+0.031 ms clock, 0.008+0/0.52/0+0.031 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 15 @6.253s 0%: 0.011+0.56+0.010 ms clock, 0.011+0/0.52/0+0.010 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 16 @7.254s 0%: 0.008+0.54+0.010 ms clock, 0.008+0/0.53/0+0.010 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 17 @8.262s 0%: 0.008+0.55+0.032 ms clock, 0.008+0/0.53/0+0.032 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
gc 18 @9.263s 0%: 0.008+0.54+0.009 ms clock, 0.008+0/0.52/0+0.009 ms cpu, 38-&gt;38-&gt;38 MB, 76 MB goal, 1 P (forced)
</code></pre>
<p>这里的<code>2%</code>百分比是垃圾回收占程序运行的百分比，也就是说这个数字越大垃圾回收时间就越多，很明显的对比这两个时间差别非常的大，仅仅是因为扫描的对象数量变少了。</p>
<p>而且很重要的原因是垃圾回收器对内置字典做了一次优化，假如字典里面的KeyValue不是指针的话，意味着不会引用其它对象，只需要扫描字典是不是失效就可以了，如果字典失效，里面所有数据都可以回收，因为它不会引用其它对象只会有字典引用它们，所以说KeyValue不是指针的话根本不需要对它们进行扫描，因为它们不会引用堆上的任何对象，不管里面存储多少KeyValue，GC只需要扫描1个map对象就可以了。如果是指针的话，垃圾回收器得遍历所有的KeyValue对象，然后看引用堆上的对象是不是需要回收。</p></div></article>