---
title: PostgreSQL 优化器入门-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>大家好，我是张树杰，是一名数据库内核开发者。我在 2018 年 6 月出版了《PostgreSQL 技术内幕：查询优化深度探索》一书，这本书对 PostgreSQL 优化器的源代码进行了详尽的分析，但也有一些朋友向我抱怨：“你只顾自己源码分析得 High，考虑过我们的感受吗？”是的，除了 PostgreSQL 的内核开发者，广阔天地间还有更多 PostgreSQL 的使用者以及其他数据库使用者。如果我们切换一个角度，从使用者的角度出发，是否能够把 PostgreSQL 的优化器解释清楚呢？于是我写了这个专栏，相信跟随这个专栏，大家可以翻过数据库优化器这座山峰。</p>
<h3 id="">专栏背景</h3>
<p>PostgreSQL 号称世界上最先进的开源关系数据库，它的优化器虽然比不上商业数据库的优化器那样复杂，但对于大部分用户来说，已经比较晦涩难懂。如果搞一个投票来评选数据库中最难以理解的模块，那么非优化器莫属。在使用 PostgreSQL 数据库的过程中，你可能会遇到下面这些问题：</p>
<ul>
<li>在你遇到一个比较糟糕的执行计划时，你是否有能力对其进行改造？</li>
<li>当你遭遇一个莫名的慢查询时，你是否能够通过优化实现方法提升性能？</li>
<li>当你创建的索引不为优化器所用时，你是否清楚地知道优化器的选择习性？</li>
<li>你是否想通过等价改写一个 SQL 语句来改变执行计划，那等价改写 SQL 语句是否隐藏着某些规则？</li>
</ul>
<p>优化器是数据库的大脑。作为数据库的从业者，你是否想知道数据库的大脑在思考些什么？反之，如果对优化器不够了解，便如同猛虎没有了利爪、苍鹰没有了翅膀，在使用数据库的过程中往往心有余而力不足。因此今天我们明知山有虎，偏向虎山行，拿出愚公移山的精神，把优化器的知识消化掉。</p>
<p>针对数据库从业人员的不同，我想对优化器的理解大致可以分成以下 3 个层次。</p>
<ul>
<li><strong>层次一：粗浅了解</strong>，比如知道优化器分为逻辑优化和物理优化，了解一些逻辑优化的方法，知道执行计划的来源，能看懂优化器产生的执行计划。</li>
<li><strong>层次二：详细了解</strong>，在粗浅了解的基础上，能够根据自己对优化器的了解，调整出优化器“喜爱”的 SQL 语句，并且对于产生的执行计划的优劣一目了然，知其然更知其所以然。</li>
<li><strong>层次三：深度了解</strong>，需要对优化器的每个细节有清楚的认知，在我们写出一个 SQL 语句之后，可以庖丁解牛式地在脑海中浮现出语句在优化器中的优化过程，清楚地知道每个细节的实现过程。</li>
</ul>
<p>要想达到第一个层次只需要阅读一些基础理论即可，这种了解对于实际应用的意义不大；而要想达到第三个层次则需要细致地解读 PostgreSQL 优化器的源代码，这个过程又过于“艰辛”。因此，本专栏的目标是使大家达到第二个层次：<strong>不分析数据库内核的源代码，从数据库使用者的角度出发，结合外在的系统表信息、参数信息、执行计划信息反向把 PostgreSQL 查询优化器的原理讲清楚。</strong></p>
<h3 id="-1">专栏框架</h3>
<p>本专栏内容划分为 5 大部分，共计 25 篇，覆盖了 PostgreSQL 优化器的所有重要知识点。我们通过介绍各种系统表信息、参数信息、执行计划信息，从而引出这些信息背后的优化器理论。</p>
<h4 id="-2">导读部分</h4>
<p>万丈高楼平地起，这部分内容主要介绍了查询优化的一些基本概念。通过小明、大明和牛二哥对话的方式，将查询优化器的基础理论、基本流程、优化规则融入其中。对优化器不甚了解的同学能够快速进入第一个层次，从而为后面的学习打好基础。</p>
<h4 id="0103">第一部分（第 01 ~ 03 篇）：准备工作</h4>
<p>工欲善其事、必先利其器。要想知道优化器怎么优化，就需要知道在优化之前，我们给优化器提供了什么。于是，第 01 篇通过一个 SQL 示例来分析这个 SQL 语句的执行流程，从而能让读者清楚地知道 SQL 语句的执行过程。另外，查看 SQL 语句的执行计划是数据库从业人员必备的技能之一，我们不但对执行计划的查看进行了说明，还对执行计划背后隐藏的理论进行了说明。这些在第 02 篇和第 03 篇进行了说明，有了这些知识，就可以很方便地对优化器进行解读了。</p>
<h4 id="0411">第二部分（第 04 ~ 11 篇）：逻辑优化部分</h4>
<p>逻辑优化也叫基于规则的优化，它主要优化的方式是检查查询树。如果查询树满足既定的优化规则，那么就按照规则对查询树进行改造。PostgreSQL 的优化规则虽然比较多，但是比较重要的有以下规则：子查询提升、表达式预处理、外连接消除、谓词下推、连接顺序交换和等价类推理等。我们在这一部分对这些规则进行了统一的说明。</p>
<h4 id="1218">第三部分（第 12 ~ 18 篇）：物理优化部分</h4>
<p>物理优化中最重要的就是代价计算的部分。为了更好地加深理解代价，我们先是解读了统计信息的内容，根据统计信息可以计算查询数据的选择率，而统计信息和选择率是代价计算的基石。有了这些信息之后，我们尝试对扫描路径、连接路径、Non-SPJ 路径进行代价计算，这样就能让读者了解代价计算的具体过程了。在代价计算之后，我们对路径的搜索算法——动态规划方法和遗传算法进行了说明。</p>
<h4 id="1922">第四部分（第 19 ~ 22 篇）：查询执行的部分</h4>
<p>执行计划在生成之后到底是如何执行的？这部分我们列举了一部分执行算子的执行过程中的关键点，这些关键点或者是优化措施，或者是实现的细节。理解这些执行算子的执行过程，有助于去理解执行算子的代价计算的流程。对于 Greenplum 数据库中的分布式执行计划，我们也尝试作出了说明。</p>
<h3 id="-3">专栏特色</h3>
<p>优化器是数据库从业人员必须熟练掌握的内容，而目前单独针对优化器的专栏少之又少。在通常情况下，它可能在一本书中只能占到一个很小的章节，这些只能让读者对优化器有一个粗浅的了解。另外，如《PostgreSQL 技术内幕：查询优化深度探索》这样专业剖析 PostgreSQL 优化器源代码的书，对于数据库的“使用者”而言又过于繁琐了。因此本专栏致力于不分析 PostgreSQL 的源代码，从一个 SQL 语句的执行开始，逐步分析优化器中涉及的各种优化原则。从参数、系统表、执行计划开始说明，逐步由表及里、由外及内，把 PostgreSQL 优化器背后隐藏的优化思想一一列举出来，最终做到深入浅出解读 PostgreSQL 优化器。</p>
<h3 id="-4">专栏寄语</h3>
<p>本专栏的写作目的是让数据库从业人员对数据库的优化器有一个比较详尽的了解。我希望大家在学习的过程中不但能掌握优化器中的各种优化规则，更能举一反三，在工作中，结合自己学到的优化器知识轻松应对各种优化问题。最后祝大家学习愉快，轻松翻过优化器这座山峰！</p></div></article>