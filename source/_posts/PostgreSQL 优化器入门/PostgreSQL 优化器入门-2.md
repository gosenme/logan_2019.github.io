---
title: PostgreSQL 优化器入门-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这部分课程致力于让读者达到对数据库优化器理解的第二个层次：<strong>详细了解</strong>。</p>
<p>愿上层楼骋远目，勿在浮沙筑高台，在开始学习第二个层次的内容之前，让我们先来复习一下第一个层次的内容。为了使对优化器分析的过程更为形象生动，接下来我们跟着小明、大明和牛二哥一起来探讨一下 PostgreSQL 查询优化器的一些基础知识。对这块内容已经了如指掌的朋友可以跳过导读，直接开始后面内容的学习。</p>
<h3 id="">查询优化器的基本原理</h3>
<h4 id="-1">小明与大明</h4>
<p>小明考上了北清大学的计算机研究生，今年学校开了数据库原理课。小明对查询优化的内容不是很理解，虽然已经使出了洪荒之力，仍觉得部分原理有些晦涩难懂，于是打算问一下自己的哥哥大明。</p>
<p>大明是一位资深的数据库内核开发老码农，对 Greenplum/HAWQ 数据库有多年的内核开发经验，眼镜片上的圈圈像年轮一样见证着大明十多年的从业经历。知道小明要来问问题，大明有点紧张，虽然自己做数据库内核好多年了，但是对优化器研究不甚深入，如果被小明这样的小菜鸟问倒就尴尬了。于是大明只好临时抱佛脚，拿出了好多年不看的《数据库系统实现》啃了起来。</p>
<h4 id="-2">小明的问题</h4>
<p>小明的第一个问题：<strong>“为什么数据库要进行查询优化？”</strong></p>
<blockquote>
  <p>大明推了推鼻梁上的眼镜，慢条斯理地说：“不止是数据库要进行优化，基本上所有的编程语言在编译的时候都要优化。比如，你在编译 C 语言的时候，可以通过编译选项 -o 来指定进行哪个级别的优化，只是查询数据库的查询优化和 C 语言的优化还有些区别。”</p>
  <p><strong>“有哪些区别呢？”</strong> 大明停顿了一下，凝视着小明，仿佛期望小明能给出答案，或是给小明腾挪出足够思考的空间。三、五秒之后，大明自答道：“C 语言是过程化语言，已经指定好了需要执行的每一个步骤；但 SQL 是描述性语言，只指定了 WHAT，而没有指定 HOW。这样它的优化空间就大了，你说是不是？”</p>
  <p>小明点了点头说：“对，也就是说条条大路通罗马，它比过程语言的选择更多，是不是这样？” 大明笑道：“孺子可教也。<strong>虽然我们知道它的优化空间大，但具体如何优化呢</strong>？”</p>
  <p>说着大明将身子向沙发一靠，翘上二郎腿继续说：“通常来说分成两个层面，一个是基于规则的优化，另一个是基于代价的优化。基于规则的优化也可以叫逻辑优化（或者规则优化），基于代价的优化也可以叫物理优化（或者代价优化）。”</p>
</blockquote>
<p>小明的第二个问题：<strong>“为什么要进行这样的区分呢？优化就优化嘛，何必还分什么规则和代价呢？”</strong></p>
<blockquote>
  <p>“分层不分层不是重点，有些优化器层次分得清楚些，有些优化器层次分得就不那么清楚，都只是优化手段而已。”大明感到有点心虚，再这么问下去恐怕要被问住，于是试图引开话题：“我们继续说说 SQL 语言吧，我们说它是一种介于关系演算和关系代数之间的语言，关系演算和关系代数你看过吧？”</p>
  <p>小明想了想，好像上课时老师说过关系代数，但没有说关系演算，于是说：“接触过一点，但不是特别明白。”大明得意地说：“关系演算是纯描述性的语言，而关系代数呢，则包含了一些基本的关系操作，SQL 主要借鉴的是关系演算，也包含了关系代数的一部分特点。”</p>
  <p>大明看小明有点懵，顿了一下继续说道：<strong>“上课的时候老师有没有说过关系代数的基本操作？”</strong>小明想了一下说：“好像说了，有投影、选择、连接、并集、差集这几个。”大明点点头说：“对，还有一个叫重命名的，一共 6 个基本操作。另外，结合实际应用在这些基本操作之上又扩展出了外连接、半连接、聚集操作、分组操作等。”</p>
  <p>大明继续说道：“SQL 语句虽然是描述性的，但是我们可以把它转化成一个关系代数表达式。而关系代数中呢，又有一些等价的规则，这样我们就能结合这些等价规则对关系代数表达式进行等价的转换。”</p>
</blockquote>
<p>小明的第三个问题：<strong>“进行等价转换的目的是找到性能更好的代数表达式吧？”</strong></p>
<blockquote>
  <p>“对，就是这样。”大明投去赞许的目光。</p>
  <p>“<strong>那么如何确定等价变换之后的表达式就能变得比之前性能更好呢？</strong>或者说为什么要进行这样的等价变换，而不是使用原来的表达式呢？”</p>
  <p>大明愣了一下，仿佛没有想到小明会提出这样的问题，但是基于自己多年的忽悠经验，他定了定神，回答道：“这既有经验的成分，也有量化的考虑。例如，将选择操作下推，就能优先过滤数据，那么表达式的上层计算结点就能降低计算量，因此很容易可以知道是能降低代价的。再例如，我们通常会对相关的子查询进行提升，这是因为如果不提升这种子查询，那么它执行的时候就会产生一个嵌套循环。这种嵌套循环的执行代价是 O(N^2)，这种复杂度已经是最坏的情况了，提升上来至少不会比它差，因此提升上来是有价值的。”大明心里对自己的临危不乱暗暗点了个赞。</p>
  <p>大明看小明没有提问，继续说道：“这些基于关系代数等价规则做等价变换的优化，就是基于规则的优化。当然数据库本身也会结合实际的经验，产生一些优化规则，比如外连接消除，因为外连接优化起来不太方便，如果能把它消除掉，我们就有了更大的优化空间，这些统统都是基于规则的优化。同时这些都是建立在逻辑操作符上的优化，这也是为什么基于规则的优化也叫做逻辑优化。”</p>
</blockquote>
<p>小明想了想，自己好像对逻辑操作符不太理解，连忙问第四个问题：<strong>“逻辑操作符是啥？既然有物理优化，难道还有物理操作符吗？”</strong></p>
<blockquote>
  <p>大明伸了个懒腰继续说：“比如说吧，你在 SQL 语句里写上了两个表要做一个左外连接，那么数据库怎么来做这个左外连接呢？”</p>
  <p>小明一头雾水地摇摇头，向大明投出了期待的眼神。</p>
  <p>大明继续说道：“数据库说‘我也不知道啊，你说的左外连接意思我懂，但我也不知道怎么实现啊？你需要告诉我实现方法啊’。因此优化器还承担了一个任务，就是告诉执行器，怎么来实现一个左外连接。”</p>
  <p>“<strong>数据库有哪些方法来实现一个左外连接呢？</strong>它可以用嵌套循环连接、哈希连接、归并连接等。注意了，重要的事情说三遍，你看内连接、外连接是连接操作，嵌套循环连接、归并连接等也叫连接，但内连接、外连接这些就是逻辑操作符，而嵌套循环连接、归并连接这些就是物理操作符。因此，你说对了，物理优化就是建立在物理操作符上的优化。”</p>
  <p>大明：“从北京去上海，你说你怎么去？”</p>
  <p>小明：“坐高铁啊，又快又方便。”</p>
  <p>大明：“坐高铁先去广州再倒车到上海行不？”</p>
  <p>小明：“有点扎心了，这不是吃饱了撑的吗？”</p>
  <p>大明：“为什么？”</p>
  <p>小明：“很明显，我有直达的高铁，既省时间又省钱，先去广州再倒车？我脑子瓦特了？！”</p>
  <p>大明笑了笑说：“不知不觉之间，你的大脑就建立了一个代价模型，那就是性价比。优化器作为数据库的大脑，也需要建立代价模型，对物理操作符计算代价，然后筛选出最优的物理操作符来。因此，基于代价的优化是建立在物理操作符上的优化，所以也叫物理优化。”</p>
</blockquote>
<p>小明似乎懂了：“公司派我去上海出差就是一个逻辑操作符，它和我们写一个 SQL 语句要求数据库对两个表做左外连接类似；而去上海的实际路径有很多种，这些就像是物理操作符，我们对这些实际的物理路径计算代价之后，就可以选出来最好的路径了。”</p>
<p>大明掏出手机，分别打开了两个不同的地图 App，输入了北京到上海的信息，然后拿给小明看。小明发现两个 App 给出的最优路径是不一样的。小明若有所思地说：<strong>“看来代价模型很重要，代价模型是不是准确决定了最优路径选择得是否准确？”</strong></p>
<p>大明一拍大腿，笑着说：“太对了，所以我作为一个数据库内核的资深开发人员，需要不断地调整优化器的代价模型，以期望获得一个相对稳定的代价模型，不过仍然是任重道远啊。”</p>
<h3 id="-3">关于语法树</h3>
<p>听了大明对查询优化器基本原理的讲解，小明在学校的数据库原理课堂上顺风顺水，每天吃饭睡觉打豆豆，日子过得非常悠哉。不过眼看就到了数据库原理实践课，老师给出的题目是分析一个数据库的某一模块的实现。小明千挑万选，终于选定了要分析 PostgreSQL 数据库的查询优化器的实现，据说 PostgreSQL 数据库的查询优化器层（相）次（当）清（复）晰（杂），具有教科书级的示范作用。</p>
<p>可是当小明下载了 PostgreSQL 数据库的源代码，顿时就懵圈了，虽然平时理论说得天花乱坠，但到了实践的时候却发现，理论和实际对应不上。小明深深陷入代码细节中不可自拔，查阅了好多资料，结果是读破书万卷，下笔如有锤，一点进展都没有。于是小明又想到了与 PostgreSQL 有着不解之缘的大明，想必他一定能站得更高，看得更远，于是小明蹬着自己的宝马向大明驶去。</p>
<p>大明看着大汗淋漓找上门的小明，意味深长地说：“PostgreSQL 的查询优化器功能比较多，恐怕一次说不完，我们分成几次来说清楚吧。”</p>
<p>小明说：“的确是，我在看查询优化器代码的时候觉得无从下手。虽然一些理论学过了，但不知道代码和理论如何对应，而且还有一些优化规则好像我们讲数据库原理的时候没有涉及，毕竟理论和实践之间还是有一些差距。”</p>
<h4 id="postgresql">PostgreSQL 查询执行的基本流程</h4>
<p>大明打开电脑，调出 PostgreSQL 的代码说：“我们先来看一下 PostgreSQL 一个查询执行的基本流程。”然后调出了一张图。</p>
<div style="text-align:center"><img src="https://images.gitbook.cn/7740d080-cdf8-11e8-9819-c5f6b437e972" width="350px" /></div>
<p></br></p>
<p>“这张图是我自己画的，这种图已经成了优化器培训开篇的必备图了，我们有必要借助这张图来看一下 PostgreSQL 源码的大体结构，了解查询优化器所处的位置。”</p>
<p>大明一边指点着电脑屏幕，一边继续说：“我们要执行一条 SQL 语句，首先会进行词法分析，也就是说把 SQL 语句做一个分割，分成很多小段段……”小明连忙说：“我们在学编译原理的时候老师说了，分成的小段段可以是关键字、标识符、常量、运算符和边界符，是不是分词之后就会给这些小段段赋予这些语义？”</p>
<p>“对的！看来你对《编译原理》的第 1 章很熟悉嘛。”大明笑着说。</p>
<p>“当然，我最擅长写 Hello World。”</p>
<p>“好吧，Let’s 继续，PostgreSQL 的分词是在 scan.l 文件中完成的。它可能分得更细致一些，比如常量它就分成了 SCONST、FCONST、ICONST 等，不过基本的原理是一样的。进行分词并且给每个单词以语义之后，就可以去匹配 gram.y 里的语法规则了。gram.y 文件里定义了所有的 SQL 语言的语法规则，我们的查询经过匹配之后，最终形成了一颗语法树。”</p>
<p><strong>“语法树？我还听过什么查询树、计划树，这些树要怎么区分呢？”</strong></p>
<p>“一个查询语句在不同的阶段，生成的树是不同的，这些树的顺序应该是先生成语法树，然后得到查询树，最终得到计划树，计划树就是我们说的执行计划。”</p>
<p><strong>“那为什么要做这些转换呢？”</strong>小明不解地问。</p>
<p>“我们通过词法分析、语法分析获得了语法树，但这时的语法树还和 SQL 语句有很紧密的关系。比如我们在语法树中保存的还是一个表的名字，一个列的名字，但实际上在 PostgreSQL 数据库中，有很多系统表，比如 PG_CLASS 用来将表保存成数据库的内部结构。当我们创建一个表的时候，会在 PG_CLASS、PG_ATTRIBUTE 等系统表里增加新的元数据，我们要用这些元数据的信息取代语法树中表的名字、列的名字等。”</p>
<p>小明想了想，说：“这个取代的过程就是语义分析？这样就把语法树转换成了查询树，而查询树是使用元数据来描述的，所以我们在数据库内核中使用它就更方便了？”</p>
<p>看着小明迷离的眼神，大明继续说：“我们可以把查询树认为是一个关系代数表达式。”</p>
<p>小明定了定神，问道：“关系代数表达式？上次我问你查询优化原理的时候你是不是说<strong>基于规则的优化就是使用关系代数的等价规则对关系代数表达式进行等价的变换</strong>，所以查询优化器的工作就是用这个查询树做等价变换？”</p>
<p>“恭喜你，答对了。”大明暗暗赞许小明的理解能力和记忆力，继续说：“查询树就是查询优化器的输入，经过逻辑优化和物理优化，最终产生一颗最优的计划树，而我们要做的就是看看查询优化器是如何产生这棵最优的计划树的。”</p>
<h3 id="-4">逻辑优化示例</h3>
<p>午饭过后，大明惬意地抽起了中华烟，小明看着他好奇地问：“咱爷爷抽的是在农村种的烟叶，自给自足还省钱，你也干脆回农村种烟叶吧。你这中华烟和农村的自己卷的烟叶，能有什么区别？”</p>
<p>大明看电视剧正看得起劲，心不在焉地说：“自己种的烟叶直接用报纸卷了抽，没有过滤嘴，会吸入有害颗粒物，而且烟叶的味道也不如现在改进的香烟。”说到这里大明好像想到了什么，继续说：“这就像是查询优化器的逻辑优化，查询树输入之后，需要进行持续的改进。无论是自己用报纸卷的烟，还是在超市买的成品烟，都是香烟，但是通过改进之后，香烟的毒害作用更低、香型更丰富了。逻辑优化也是这个道理，通过改进查询树，能够得到一个更‘好’的查询树。”</p>
<p><strong>“那逻辑优化是如何在已有的查询树上增加香型的呢？”</strong></p>
<p>大明继续说：“我总结，PostgreSQL 在逻辑优化阶段有这么几个重要的优化——子查询 &amp; 子连接提升、表达式预处理、外连接消除、谓词下推、连接顺序交换、等价类推理。”大明又抽了一口烟，接着说：“从代码逻辑上来看，我们还可以把子查询 &amp; 子连接提升、表达式预处理、外连接消除叫做逻辑重写优化，因为他们主要是对查询树进行改造。而后面的谓词下推、连接顺序交换、等价类推理则可以称为逻辑分解优化，他们已经把查询树蹂躏得不成样子了，已经到了看香烟不是香烟的地步了。”</p>
<p>“可是我们的数据库原理课上并没有说有逻辑重写优化和逻辑分解优化啊。”</p>
<p>“嗯，是的，这是我根据 PostgreSQL 源代码的特征自己总结的，不过它能比较形象地将现有的逻辑优化区分开来，这样就能更好地对逻辑优化进行提炼、总结、分析。”大明想了一下觉得如果把所有的逻辑优化规则都说完有点多，于是对小明说：“我们就从中挑选一两个详细说明吧，我们就借用关系代数表达式来说一下谓词下推和等价类推理吧。”</p>
<p>小明想了想说：<strong>“选择下推和等价类是逻辑分解优化中的内容了，可是逻辑重写优化里还有子查询提升、表达式预处理、外连接消除这些大块头你还没有给我讲解过呀。”</strong></p>
<p>大明说：“这些先留给你自己去理解，如果理解不了再来找我吧。逻辑优化的规则实际上还是比较多的，但可以逐个击破，也就是他们之间通常而言并没有多大的关联，我们不打算在这上面纠缠太多时间，我相信以你自己的能力把他们搞定是没有问题的。” <em>（注意：课程中会对这些内容做介绍。）</em></p>
<p><strong>“选择下推是为了尽早地过滤数据，这样就能在上层结点降低计算量，是吧？”</strong></p>
<p>“是的。”大明点了点头，“还是通过一个关系代数的示例来说明一下吧，顺便我们把等价类推理也说一说。比如说我们想要获得编号为 5 的老师承担的所有课程名字，我们可以给出它的关系代数表达式。”说着在电脑上敲了一个关系代数表达式：</p>
<pre><code>Πcname,tname (σTEACHER.tno=5∧TEACHER.tno=COURSE.tno (TEACHER×COURSE))
</code></pre>
<p>“小明，你看这个关系代数表达式怎么下推选择操作？”</p>
<p>小明看着关系代数表达式思考了一会，说：“我看这个 TEACHER.tno = 5 比较可疑。你看这个关系代数表达式，先做了 TEACHER×COURSE，也就是先做了卡氏积，我要是把 TEACHER.tno = 5 放到 TEACHER 上先把一些数据过滤掉，岂不是……完美！”说着小明也在电脑上敲出了把 TEACHER.tno = 5 下推之后的关系代数表达式。</p>
<pre><code>Πcname,tname (TEACHER.tno=COURSE.tno (σTEACHER.tno=5(TEACHER)×COURSE))
</code></pre>
<p>大明说：“对，你这样下推下来的确能降低计算量，这应用的是关系代数表达式中的分配率 σF(A × B) == σF1(A) × σF2(B)，那你看看，既然下推这么好，是不是投影也能下推？”小明看了一下，关系代数表达式中值需要对 cname 进行投影，顿时想到了，COURSE 表虽然有很多个列，但是我们只需要使用 cname 就够了嘛，于是小明在电脑上敲了投影下推的关系代数表达式。</p>
<pre><code>Πcname,tname (σTEACHER.tno=COURSE.tno (Πcname(σTEACHER.tno=5(TEACHER))×Πcname(COURSE))
</code></pre>
<p>大明拍了小明的头一下说：“笨蛋，你这样下推投影，TEACHER.tno=COURSE.tno 还有办法做吗？”小明顿时领悟了，如果只在 COURSE 上对 cname 做投影是不行的，上层结点所有的表达式都需要考虑到，于是修改了表达式：</p>
<pre><code>Πcname,tname (σTEACHER.tno=COURSE.tno (Πtname,tno(σTEACHER.tno=5(TEACHER))×Πcname,tno(COURSE)))
</code></pre>
<p>“这还差不多。”大明笑着说：“这是使用的投影的串接率，也是一个非常重要的关系代数等价规则，目前我们对这个表达式的优化主要是使用了选择下推和投影下推，如果用 SQL 语句来表示，就像这样。”大明在电脑的记事本上快速打出了两个 SQL 语句：</p>
<pre><code>SELECT sname FROM TEACHER t, COURSE c WHERE t.tno = 5 AND t.tno = c.tno;

SELECT sname FROM (SELECT * FROM TEACHER WHERE tno = 5) tt, (SELECT cname, tno FROM COURSE) cc WHERE tt.tno = cc.tno;
</code></pre>
<p>“你看这两个语句，就是谓词下推和投影下推前后的对照语句。在做卡氏积之前，先做了过滤，这样笛卡尔积的计算量会变小。”</p>
<p>小明仔细观察代数表达式和这两个 SQL 语句，发现了一个问题，就是关系代数表达式中有 TEACHER.tno = 5 和 TEACHER.tno = COURSE.tno 这样两个约束条件，这是不是意味着 COURSE.tno 也应该等于 5 呢？小明试着在电脑上写了一个 SQL 语句：</p>
<pre><code>SELECT sname FROM (SELECT * FROM TEACHER WHERE tno = 5) tt, (SELECT cname, tno FROM COURSE WHERE tno=5) cc WHERE tt.tno = cc.tno;
</code></pre>
<p>然后小明说：“你看，由于有 TEACHER.tno = 5 和 TEACHER.tno = COURSE.tno 两个约束条件，我们是不是可以推理出一个 COURSE.tno = 5 的新约束条件来呢？这样还可以把这个条件下推到 COURSE 表上，也能降低笛卡尔积的计算量。”</p>
<p>大明说：“是的，这就是等价推理。PostgreSQL 在查询优化的过程中，会将约束条件中等价的部分都记录到等价类中，这样就能根据等价类生成新的约束条件。比如示例的语句中就会产生一个等价类 {TEACHER.tno, COURSE.tno, 5}，这是一个含有常量的等价类，是查询优化器比较喜欢的等价类，这种等价类可以得到列属性和常量组合成的约束条件，通常都是能下推的。”</p>
<p>小明心里很高兴，自己通过仔细观察，得到了等价类的优化，感觉有了学习的动力，心里美滋滋的，然后问大明：“那上面的 SQL 语句还有什么可优化的吗？”</p>
<p>大明观察了一下这个语句说：“我们已经在 TEACHER 表上进行了 TEACHER.tno = 5 的过滤，在 COURSE 表上也做了 COURSE.tno = 5 的过滤，这就说明在做笛卡尔积时，实际上已确定了 TEACHER.tno = COURSE.tno = 5。也就是说 TEACHER.tno = COURSE.tno 这个约束条件已经隐含成立了，也就没什么用了，我们可以把它去掉，最终形成一个这样的 SQL 语句。”大明敲下了最终的语句：</p>
<pre><code>SELECT sname FROM (SELECT * FROM TEACHER WHERE tno = 5) tt, (SELECT cname, tno FROM COURSE WHERE tno=5) cc；
</code></pre>
<p>同时也敲出了这个语句对应的关系代数表达式：</p>
<pre><code>Πcname,tname (Πtname, tno(σTEACHER.tno=5(TEACHER))× Πcname, tno(σCOURSE.tno=5(COURSE)))
</code></pre>
<p>大明说：“经过选择下推、投影下推和等价类推理，我们对这个 SQL 语句或者说关系代数表达式进行了优化，最终降低了计算量。”</p>
<p>小明感觉对谓词下推已经理解了：“看上去也不复杂嘛，我发现了可以下推的选择我就下推，完全没有问题啊。”大明笑着说：“甚矣，我从未见过如此厚颜无耻之人。我们现在看的这个例子，只不过是最简单的一种情况啊，你就这样大言不惭，你的人生字典里还有羞耻二字吗？”</p>
<p>小明愤愤地说：“我的人生没有字典……”</p>
<p>大明问道：“我们这个例子有一个问题，它是内连接，因此我们可以肆意妄为地将选择下推下来，可以没羞没臊地做等价类推理。但如果是外连接，还能这么做吗？”</p>
<p>小明顿时陷入了苦苦的沉思。</p></div></article>