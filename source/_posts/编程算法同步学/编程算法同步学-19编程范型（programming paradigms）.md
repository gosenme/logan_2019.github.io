---
title: 编程算法同步学-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="programmingparadigms">编程范型（programming paradigms）</h3>
<p>我们来学习一个新概念：编程范型。</p>
<h4 id="">定义和分类</h4>
<p>范型（Paradigm）这个词来源于希腊语 “paradeigma”，有“模式，例子，样例”的意思。</p>
<p>听着有点悬。其实，编程范型就是<strong>程序组织和实现计算的模式</strong>，也可以简单理解成一种<strong>编程的风格</strong>。</p>
<p>编程范型可以大致分为两大类：</p>
<p><img src="https://images.gitbook.cn/5ae08000-8b69-11e9-abd4-3359f30b3591" alt="enter image description here" /></p>
<ul>
<li><p><strong>命令式（imperative）</strong>：程序一句句地告诉机器该去干什么。</p>
<p>这类范型包括：</p>
<ul>
<li><strong>过程式（procedural）</strong>：把一组组指令封装成过程，程序的组织形式是：算法过程 + 数据结构。</li>
<li><strong>面向对象（object-oriented）</strong>：把数据和针对数据的操作封装成对象，程序是互相通信的对象的集合。</li></ul></li>
<li><p><strong>宣言式（declarative）</strong>：程序告诉计算机它想要什么样的结果，而不是告知获得结果的过程。</p>
<p>这类范型包括：</p>
<ul>
<li><strong>函数式(functional)</strong>：把运算过程封装成函数，程序是各种函数的组合。</li>
<li><strong>逻辑式(logic)</strong>：通过设置答案须匹配的规则来解决问题，程序是规则的组合。</li></ul></li>
</ul>
<p>以上是简要的介绍。</p>
<p><img src="https://images.gitbook.cn/6a61ebe0-8b69-11e9-b38f-03c8201e19f7" alt="enter image description here" /></p>
<h4 id="-1">范型的演进与重合</h4>
<p>范型当然不止上述这几种，不过这几种最常见。</p>
<p>范型本身也是在演进的，新语言的出现可能会带来新的范型，比如随着机器学习的兴起，近几年又出现了一种<strong>概率式(probabilistic)</strong>编程的新范型。</p>
<p>而且，编程语言和范型并非一定是一对一的关系，也可以一对多——一种编程语言可以是<strong>单范型</strong>的，也可以是<strong>多范型</strong>的。</p>
<p>比如我们可爱的Python，就同时支持：</p>
<p><img src="https://images.gitbook.cn/2556f1c0-8b6a-11e9-abd4-3359f30b3591" alt="enter image description here" /></p>
<ul>
<li>过程式</li>
<li>函数式</li>
<li>面向对象</li>
</ul>
<p>三种范型编程，是多范型的典范。</p>
<p>不过，范型虽多，最常用的还是过程式编程。过程式编程不仅使用率高，而且历史悠久，被绝大多数语言支持，理解起来也最为容易。</p>
<blockquote>
  <p><strong>小贴士</strong>：在本课中，我们所有的示例代码都<strong>仅采用过程式编程范型</strong>。</p>
</blockquote>
<h4 id="-2">直观感受不同的编程语言</h4>
<p>2019年GitChat出了一本年历，每星期一页，每页都用一种不同的编程语言写了一个相同功能的程序。</p>
<p>一年可是有52周哦，所以想想看看，光是这一本日历用到的了52种编程语言。这么多编程语言，写出来到底有什么不同呢？我们就挑几个典型的例子来看看——</p>
<p>注意，下面每个程序样例中程序所用的语言虽然不同，<strong>功能完全一样</strong>：<strong><em>从计算机系统中获取当时的日期，并打印出来。</em></strong></p>
<p><img src="https://images.gitbook.cn/c5243c30-8b33-11e9-b38f-03c8201e19f7" alt="enter image description here" /></p>
<p><strong>汇编语言</strong>：低级语言，直接书写操作码和地址码。</p>
<hr />
<p><img src="https://images.gitbook.cn/da53aaa0-8b33-11e9-abd4-3359f30b3591" alt="enter image description here" /></p>
<p><strong>Fortran语言</strong>： 1953年IBM的工程师约翰·巴科斯（J. Backus）提出，应该研发一种新的、区别于汇编的程序设计语言。</p>
<p>这一提议被计算机体系结构之父冯诺伊曼反对，理由是：没必要。但得到了时任IBM董事长斯伯特·赫德（Cuthbert Hurd）的批准。</p>
<p>Fortran于1957年诞生在IBM，成了世界上第一款被正式采用的高级语言。</p>
<p>由于被发明出来的目的是为了满足数值计算的需求，Fortran的语法形式接近数学公式的自然描述，在计算机里具有很高的执行效率；很多专用的大型数值运算计算机针对Fortran做了优化。</p>
<p>这些特性使得Fortran至今仍然广泛地应用于并行计算和高性能计算领域。</p>
<hr />
<p><img src="https://images.gitbook.cn/e953b180-8b33-11e9-b5ce-69c389c366b3" alt="enter image description here" /></p>
<p><strong>Lisp语言</strong>：诞生于1958（仅比Fortran年轻），由MIT的约翰·麦卡锡（John McCarthy）发明。</p>
<p>约翰·麦卡锡1956年在达特茅斯会议上提出了“人工智能”这个概念，并于1971年因在人工智能领域的贡献而获得图灵奖。</p>
<p>发明者的学术背景使得Lisp出现后很快成为人工智能研究中最受欢迎的编程语。Lisp早期被作为“人工智能语言”。</p>
<p>Lisp开创了很多先驱性的概念，包括：树结构、自动存储器管理、动态类型、条件表达式、递归等等，这些概念为后来许许多多的编程语言所采用。</p>
<p>在创建之初，Lisp就将lambda演算用于程序的数学表达，这一点则是后来所谓“函数式编程”的主要特征。如此一来，Lisp后来则常被作为“函数式语言”提起。</p>
<hr />
<p><img src="https://images.gitbook.cn/0216c370-8b33-11e9-b38f-03c8201e19f7" alt="enter image description here" /></p>
<p><strong>PASCAL语言</strong>：诞生于1970年，由瑞士计算机科学家维尔特（Wirth）设计，为纪念法国数学家和哲学家布莱兹·帕斯卡而命名。</p>
<p>PASACAL语言设计初衷在于推广结构化编程和数据结构的使用。虽然在软件开发的实践中并不出彩，但因为其结构的清晰和严谨，因此作为“教学语言”著称于世。</p>
<p>很多代学生——比如作者——都使用PASCAL作为本科计算机课程的入门语言。许多信息奥林比克竞赛训练也是从PASCAL入手的。</p>
<hr />
<p><img src="https://images.gitbook.cn/193dedc0-8b34-11e9-b5ce-69c389c366b3" alt="enter image description here" /></p>
<p><strong>C语言</strong>：诞生于1970年代初，由美国计算机科学家丹尼斯·里奇（Dennis M. Ritchie，简称dmr）设计，由他和B语言的发明者肯·汤普逊（Ken Thompson，简称ken）共同实现。</p>
<p>C是一款高效、灵活、功能丰富、表达力强的开发语言，广泛应用于软件开发工作中。至今仍然是世界上最重要的几种编程语言之一。</p>
<hr />
<p><img src="https://images.gitbook.cn/2439d180-8b34-11e9-abd4-3359f30b3591" alt="enter image description here" /></p>
<p><strong>Erlang语言</strong>：诞生于1980年代，由瑞典爱立信公司的乔·阿姆斯特朗（Joe Armstrong）发明。</p>
<p>Erlang得名的解释有两种：1. 爱立信语言（Ericsson Language）；2. 为了纪念丹麦数学家及统计学家Agner Krarup Erlang。</p>
<p>Erlang支持函数式编程，以及并发和分布式程序设计机制，还提供了脚本运行的方式。总体上，Erlang被认为是一种典型的函数式编程语言，主要应用在通讯领域。</p>
<p>Erlang其自身的语言特点可以用四个字概括：极其别扭。但也许就是这种别扭，使得它成为某些Geek炫技的选择，如果你认识一位不是写通讯软件的Erlang使用者，TA是Geek/Nerd的可能性会很高。</p>
<hr />
<p><img src="https://images.gitbook.cn/341bfb00-8b34-11e9-b5ce-69c389c366b3" alt="enter image description here" /></p>
<p><strong>Java语言</strong>：诞生于1990年代初的Sun Microsystems公司，由詹姆斯·高斯林（James Gosling）等人设计实现。</p>
<p>Java语言对于面向对象范型的强支持，垃圾自动回收机制的易用性，以及通过虚拟机运行的跨平台特征，使得它在互联网时代大放异彩，逐渐成为几乎是最重要的网络编程语言。</p>
<p>目前大部分的Web服务和应用后端，都是用Java开发的。</p>
<hr />
<p><img src="https://images.gitbook.cn/3c93a4e0-8b34-11e9-abd4-3359f30b3591" alt="enter image description here" /></p>
<p><strong>Python语言</strong>：诞生于1991年（很年轻啊），由荷兰程序员吉多·范罗苏姆（Guido van Rossum）创造。</p>
<p>Python最初被认为是一种改良的Lisp，又具备了一些其它语言的有点，例如动态类型和垃圾回收机制等。</p>
<p>它支持多种（几乎所有））编程范型，还拥有一个巨大的支持库。目前被大量应用于Web开发，数据处理和人工智能领域。</p>
<hr />
<p><img src="https://images.gitbook.cn/488affa0-8b34-11e9-b38f-03c8201e19f7" alt="enter image description here" /></p>
<p><strong>Scratch</strong>： Scratch其实并不是一种语言，而是一个编程平台，发布于2006年，旨在让小白用户不需学习编程语言语法就能编写程序。</p>
<p>它最大的特点就是：不用“写代码”（敲字符），而是通过拖拽不同的“积木块”来拼搭程序控制流程，同时提供了填写式的变量定义和大量内置图形元素。</p>
<p>这些特征使得它自诞生起便成了“少儿编程”的第一选择。</p>
<p>原因很简单，小朋友（特别是8、9岁以下的）基本上还不认识字，更不会打字，让他们在键盘上找个abcd都得找半天，要写一串代码出来不得痛苦死？直接搭积木就轻松多了。</p>
<p>而且内置的各种图形UI元素结合相对简单的逻辑流程就可以编写“小游戏”。使用者很容易获得成就感，继而引起兴趣。</p></div></article>