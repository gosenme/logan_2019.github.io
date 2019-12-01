---
title: Angular 基础教程-33
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><blockquote>
  <p>这部分内容有深度，如果你暂时不想了解这么多，可以先跳过去，有需要的时候再来看。</p>
</blockquote>
<h3 id="reactiveprogramming">Reactive Programming——反应式编程</h3>
<p><img width="65%" src="https://images.gitbook.cn/33cae4b0-cce6-11e9-beb5-a53251e30de8"></p>
<p>从本质上来说，计算机编程语言分成两大种大的范式：命令式和声明式。</p>
<ul>
<li>典型的命令式编程语言有：C、C++、Java 等。</li>
<li>典型的声明式编程语言有：SQL、XML、HTML、SVG 等。</li>
</ul>
<p>为了帮助你更好地理解这两种编程范式的不同点，我用自己的语言来解释一下。比如 SQL 是一种典型的声明式语言，你会写出这样的语句：</p>
<pre><code>select u.* from user u where u.age &gt; 15;
</code></pre>
<p>但是，数据库在底层是如何解释并执行这条语句，是由数据库自己决定的，不需要程序员来控制，程序员只是在“描述”自己想要什么，而并不需要告诉计算机具体怎么做。</p>
<p>命令式编程语言刚好相反，程序员必须想好需要什么结果，同时需要提供完整的执行过程。</p>
<p>Reactive Programming 属于声明式编程语言的一种，有很多中文资料把它翻译成“响应式编程”，我认为这不够准确，而且容易和UI设计领域的“响应式编程”发生混淆，翻译成“反应式编程”更加贴切，请参考题图。</p>
<h3 id="">发展历程</h3>
<p><img width="100%" src="https://images.gitbook.cn/539a0d20-cce6-11e9-beb5-a53251e30de8"></p>
<p>Reactive Programming 在 1970 年代就开始发展了，后来微软在 .NET 上面做了第一个实现，后面 2013 年的时候有了 Java 版的实现，然后才有了 ReactiveX 宣言。</p>
<p>目前有 18 种语言实现了 ReactiveX，而 RxJS 是其中的 JS 版本。所以，你可以看到，ReactiveX 本身是和语言无关的，你可以把它看成一种编程思想、一种协议、一种规范。</p>
<h3 id="-1">典型的业务场景</h3>
<p>有人会说，OK，我懂了，这是一种编程思想，但是我为什么要用它呢？它能带来什么好处呢？</p>
<p>我举几个典型的业务场景帮助你理解。</p>
<ul>
<li>场景一：事件流与“防抖动”</li>
</ul>
<p><img width="70%" src="https://images.gitbook.cn/808d2970-cce6-11e9-8d89-4fa271cb1633"></p>
<p><img width="70%" src="https://images.gitbook.cn/8847c4e0-cce6-11e9-beb5-a53251e30de8"></p>
<p>用户连续不断地敲击键盘，如果用户每次按下一个键就发起一个网络请求进行查询，很明显就会产生大量无效的查询。那么，如何才能在用户真正输入完成之后再发起查询请求呢？这个场景用 RxJS 实现起来就非常简单。</p>
<ul>
<li>场景二：数据流</li>
</ul>
<p><img width="100%" src="https://images.gitbook.cn/abae6bf0-cce6-11e9-9a11-bbb3551196dc"></p>
<p>我有 3 个 Ajax 请求，业务需要 3 个请求全部都成功之后才能继续后面的业务操作。这个场景可以用 Promise 来实现，也可以用 RxJS 来实现。</p>
<ul>
<li>场景三：数据与 UI 的同步</li>
</ul>
<p><img width="100%" src="https://images.gitbook.cn/c3b76030-cce6-11e9-beb5-a53251e30de8"></p>
<ul>
<li>场景四：Android 中 UI 线程与其它线程的同步问题</li>
</ul>
<p><img width="70%" src="https://images.gitbook.cn/d0b83bb0-cce6-11e9-beb5-a53251e30de8"></p>
<p>对于以上 4 种典型的业务场景，如果完全靠程序员从零自己实现，会非常繁琐，而用 ReactiveX 的思路来做就会非常简单。</p>
<h3 id="reactivexoperator">ReactiveX 中的难点：Operator（操作符）</h3>
<p>ReactiveX 所描述的设计思想是非常清晰的，理解起来也不困难。</p>
<p>但是，在工程实践中，有很多人在抱怨 ReactiveX 过于繁琐，这里面最大的一个难点就是所谓的“操作符”（Operator）的用法。</p>
<p>ReactiveX 官方移动定义了 70 个 Operator，分成 11 个大类（各种语言实现 Operator 的数量不一样）：</p>
<p><img width="30%" src="https://images.gitbook.cn/16024530-cce7-11e9-9a11-bbb3551196dc"></p>
<h3 id="rxjs">RxJS</h3>
<p>RxJS 是 ReactiveX 的 JavaScript 版实现，它本身是独立的，只是 Angular 选用了它来构建自己的内核。</p>
<p>RxJS 一共实现了 105 个 Operator，分成 10 个大类，完整的分类和列表参见这里：</p>
<blockquote>
  <p><a href="https://rxjs.dev/guide/operators">https://rxjs.dev/guide/operators</a></p>
</blockquote>
<p>请不用担忧，这里面很多 Operator 在日常业务开发里面永远都不会用到。所以你不需要一次性全部掌握，刚开始的时候只要能熟练使用其中的 15 个就可以了。</p>
<p>创建型：</p>
<ul>
<li>ajax</li>
<li>empty</li>
<li>from</li>
<li>of</li>
<li>range</li>
</ul>
<p>join 创建型：</p>
<ul>
<li>concat</li>
<li>merge</li>
<li>zip</li>
</ul>
<p>变换型：</p>
<ul>
<li>map</li>
<li>scan</li>
</ul>
<p>过滤型：</p>
<ul>
<li>filter</li>
<li>first</li>
<li>last</li>
<li>throttle</li>
</ul>
<p>异常处理型：</p>
<ul>
<li>catchError</li>
</ul>
<p>对于其他 Operator，你可以在用到的时候再查文档，也可以通过类比的方式进行理解和记忆。比如：对于数学运算类的 Operator，当你看到有 max 的时候，就能想到一定有 min。这是非常自然的事情，并不需要额外的努力。</p>
<p>在官方的文档中 <a href="https://rxjs.dev/guide/operators">https://rxjs.dev/guide/operators</a>，为每一个 Operator 都提供了实例代码，总共有一千多个例子，你可以对照这些例子进行理解。在例子页面上，还提供了弹珠图。我看到有一些初学者还不会看弹珠图，附一张中文版的弹珠图说明如下：</p>
<p><img width="100%" src="https://images.gitbook.cn/769be270-cce7-11e9-9f23-07a3e2a236db"></p>
<p><strong>弹珠图是从上向下看的：上方的时间线是输入，中间的方框是 Operator，下方的时间线是输出。由于输入输出都是 Observable，所以可以无限链式调用。</strong></p>
<p>比如下面这张弹珠图：</p>
<p><img width="80%" src="https://images.gitbook.cn/82c040a0-cce7-11e9-8d89-4fa271cb1633"></p>
<p>输入是上方的两条时间线，中间的 merge 是 Operator，下方的时间线是输出，所以 merge 操作的效果就是把两条时间线上的值“合并”成了下方的一条时间线。</p>
<h3 id="-2">参考资料</h3>
<ul>
<li><a href="https://en.wikipedia.org/wiki/">https://en.wikipedia.org/wiki/Declarative_programming</a></li>
<li>ReactiveX 宣言：<a href="http://reactivex.io/">http://reactivex.io/</a></li>
<li>RxJS：<a href="https://github.com/ReactiveX/rxjs">https://github.com/ReactiveX/rxjs</a></li>
<li>RxJava：<a href="https://github.com/ReactiveX/RxJava">https://github.com/ReactiveX/RxJava</a></li>
</ul></div></article>