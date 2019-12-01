---
title: 图解敏捷教练和 ScrumMaster-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p><img src="http://images.gitbook.cn/00e1d160-cab5-11e7-9016-9914a694cb6e" alt="enter image description here" /></p>
<p>新来的敏捷教练小 C 的第一次会议是回顾会议。</p>
<p><img src="http://images.gitbook.cn/5935f850-cab5-11e7-9016-9914a694cb6e" alt="enter image description here" /></p>
<p>上图中相互指责的话语相信很多小伙伴都感同身受。当团队讨论气氛恶化的时候，让大家把目标关注到解决问题上。要想解决问题，应该从提出正确的问题，寻找根本原因开始，过程中要注意避免快速说出解决方案。</p>
<blockquote>
  <p>“Members often begin solving problems by suggesting solutions before agreeing on the problem or its causes.” 
                 –Roger Schwarz, The SkilledFacilitator (1994)</p>
</blockquote>
<p>Team 针对问题进行了细细的讨论之后，决定从共享信息开始。
制定的 Action 如下：</p>
<ol>
<li>尝试结对编程，同时也进行结对测试。</li>
<li>针对每个 Pull Request，都需要有团队其他成员进行 Code Review 之后，才能够合并代码。</li>
<li>每张 User Story 在开始做的时候，召集团队成员进行 Kickoff，列出这张卡的范围和超出范围的内容，讨论 AC。</li>
</ol>
<h3 id="">知识共享</h3>
<p>就锤子自己经历过的团队都有各种各样隐性知识，深深的扎根在不同人的脑海中，每次发生问题需要处理的时候，总有神秘的脚本或者人物横空出世。知识共享不但可以把隐性知识转变成显性知识，还能让团队对信息的理解一致，并利于知识的传承。</p>
<p><img src="http://images.gitbook.cn/f95ecb40-cab5-11e7-9016-9914a694cb6e" alt="enter image description here" /></p>
<h4 id="wiki">团队 Wiki</h4>
<p>提到知识共享，锤子第一个想到的是建立团队的 Wiki，Wiki 特别适合分享项目中的业务知识，流程或者各种坑。</p>
<p>Wiki 的好处多多：</p>
<ul>
<li>集中管理知识。</li>
<li>通过在 Wiki 中整理知识，把隐性知识显性化，可以知识体系化、规范化，而且可以信息缺口。</li>
<li>实现文件协同，降低沟通成本。</li>
<li>还可以提高技术人员的沟通能力（要把事情写清楚并不容易）。</li>
</ul>
<p>用好 Wiki 的关键在于<strong>习惯化，及时更新信息</strong>。
Wiki 并不算技术层面的，下面就来点技术层面——编程方面的共享。先从 Team 制定的 Action 开始。</p>
<h4 id="pairprogramming">Pair Programming</h4>
<p>结对编程（Pair programming）源于极限编程（XP），是指两个程序员在一个电脑上共同工作。见的方式有一个人写（Driver），一个人看（Navigator）；或者一个人测试代码，一个人去实现。两个程序员经常互换角色。在结对编程中，Navigator 考虑工作的战略性方向，提出改进的意见，或将来可能出现的问题以便处理。这样使得 Driver 可以集中精力完成当前任务的“战术”方面。结对编程对开发程序而言，不但利于知识在团队内的分享，也可以增加纪律性，写出更好的代码。</p>
<p>推荐阅读： <a href="http://gitbook.cn/books/58f02c5d23bb8c646f93c406/index.html">如何爱上结对编程</a></p>
<h4 id="codereview">Code Review 代码审查</h4>
<p>尽管结对编程已经起到一定程序代码审查的目的，但是并不能完全替代代码审查，而且有些时候，尤其是开发人员独立开发时，代码审查仍然是必需的。Code Review 可以分成正式和非正式的。正式的 Code Review 需要定好参会人员，选好要 review 的代码，大家一起进行 review。非正式类似 git 上的 Pull request 方式，让没有参与开发这部分代码的开发人员进行 review。</p>
<p>推荐阅读： <a href="http://36kr.com/p/5051144.html">什么才是 Code Review 的正确姿势？</a></p>
<h4 id="mobprogramming">Mob Programming</h4>
<p>（mob 有乌合之众的意思，想想一堆人围观或者抢一个东西的场景，嗯，锤子想到了女生打篮球。）</p>
<p>比结对编程和代码审查更恐怖又有趣的是 Mob programming，也就是一个整个团队都在同一个地点、在同一时间使用同一台电脑进行工作的开发方式。</p>
<p><em>Mob Programming : A Whole Team Approach</em> 的作者 Woody Zuill 解释了 Mob 编程的好处：</p>
<blockquote>
  <p>一个团队在开发软件时所面对的最主要的问题在 Mob 编程中全部消失了。例如：</p>
  <p>（1）再没有交流的问题；整个团队都在那里，随时保持与大家接触。</p>
  <p>（2）为了得到问题（的答案）的等待时间：问题不在于产量，而是获得解答。在这个环境下，再积压中引入新的库存就是浪费了。整天一起工作就消除了这个问题。</p>
  <p>（3）技术负债。这也许是软件开发最无形的方面：在 IT 中，当一个队伍在产品中引入了垃圾，它会留下来。Mob 编程则使持续的高质量成为可能。</p>
</blockquote>
<p>如果完全没有用过，不妨在 Team 里尝试一下，记得准备好吃的喝的。</p>
<h4 id="kickoff">Kickoff 卡片</h4>
<p>除了写代码时候的共享，在做 Spint 计划会议的过程中，大家讨论 User Story 的过程也是共享的一部分。但是计划和真正开始实施某张卡片之间还是有一定时间差，这里就有个小技巧来弥补这个时间差可能带来的改动，就是 kickoff 卡片，同时也可以把技术实现的细节推迟到此时讨论，能够有效提高 Sprint 计划会议的效率。</p>
<p>Kickoff 卡片是指团队成员想要开始做一张新的任务卡片时，跟 PO 和其他团队成员一起进行 kickoff。Kickoff 卡片的时候要完成：</p>
<ol>
<li>in：哪些工作在这个卡片的范围之内。</li>
<li>out：哪些工作是范围之外不用考虑的。 </li>
<li>AC（Acceptance Criteria）：讨论已有的 AC 大家是不是都已经了解，同时也进行修正。</li>
</ol>
<p>通过 Kickoff 卡片的过程让团队每个人都可以及时更新信息，不仅在编码阶段，在代码审查和测试阶段也能保证高质量的实施。</p>
<h3 id="-1">个人修炼</h3>
<p>经过知识共享，当大家对业务的了解逐步深入，针对最近频频出现的引入新 bug 的问题，团队在又一次的 retro
 中经过讨论，决定是时候加强团队的个人能力了。</p>
<p><img src="http://images.gitbook.cn/b5c8e4f0-cab6-11e7-ac4a-47599145e13b" alt="enter image description here" /></p>
<p>首先单元测试就提上了议程。</p>
<h4 id="unittest">Unit Test 单元测试</h4>
<p>按照下图的测试金字塔，开发人员进行单元测试的性价比实际上是最高的。</p>
<p><img src="http://images.gitbook.cn/dd8a81b0-cab6-11e7-9016-9914a694cb6e" alt="enter image description here" /></p>
<p>大家对单元测试的重要性有了共识还不够，到底怎么样才能写出真正好的单元测试呢？</p>
<p>下面就介绍一下 Sandy Matz 在 <Practical Object-Oriented Design in Ruby> 提出的正确书写单元测试的方法。</p>
<p>下面的图展示了一个普通的类。公开接口定义一些其他的类可以调用的方法，称之为“入口消息”（incoming message）； 对其他类的接口调用，称之为“发出消息”（outgoing message）。单元测试只需要测试入口消息以及发出消息，而不必去测试内部实现。</p>
<p><img src="http://images.gitbook.cn/525aa1e0-cacc-11e7-9c4f-35f9ba09ec95" alt="enter image description here" /></p>
<p>遵守以下的规则，就可以写出有效且不重复的测试。在帮助小伙伴写出高质量代码的同时也能最大限度的减小对测试的维护。</p>
<h5 id="-2"><strong>入口消息的测试</strong></h5>
<p>入口消息是类定义的对外消息，入口消息必须测试。</p>
<p>入口消息的测试原则是模拟所有的调用场景，然后测试入口消息的返回值，或者对象状态的改变。</p>
<p>入口消息难以测试的一个普遍原因是消息实现中对于其他类的依赖；而构造那个被依赖的对象又十分困难。这个时候就要考虑依赖倒置原则，将这个被依赖的类的接口注入到测试类，然后通过一个实现该接口的伪类（fake class）来完成测试。</p>
<h5 id="-3"><strong>发出消息的测试</strong></h5>
<p>发出消息分成两种，一直是查询型消息，一种是命令型消息。</p>
<ul>
<li>查询型消息调用一个其他类的方法，该方法只提供返回值，但是不改变类的状态。由于我们已经测试了类的公用接口，所以不需要重新验证查询方法会返回什么样的结果。也就是说，查询型消息不需要测试。</li>
<li>命令型消息会改变一个类的状态。它一般是一个工作流的一部分。必须测试这个通知事实上发生了（但不要去测试这个通知发生所引起的状态改变）。在测试命令型发出消息时，一个常用的技术是 mock object。可以在 mock object 上设置期待，然后调用要测试的方法，再验证该期待是否被满足。</li>
</ul>
<h4 id="testdrivendevelopmenttdd">Test Driven Development（TDD）</h4>
<p>《测试驱动开发的艺术》的第一部分《TDD 入门》阐明了 TDD 的真谛：</p>
<blockquote>
  <p>“在 TDD 周期中的第一步中，我们会写测试，实际上这并不只是写测试而已，而是在做设计。我们是在设计 API，即用来访问新功能的接口。编码之前写测试，我们会自然地考虑新代码的调用方式。……测试先行的编码方式会促使我们站在代码用户（开发人员）的角度考虑，设计出更易用的
  API。”</p>
</blockquote>
<p>TDD 的基本思路是通过测试来推动整个开发的进行，但测试驱动开发并不只是单纯的测试工作，而是把需求分析，设计，质量控制量化的过程。TDD 首先考虑使用需求（对象、功能、过程、接口等），主要是编写测试用例框架对功能的过程和接口进行设计，而测试框架可以持续进行验证。</p>
<p>TDD 的反馈循环跟敏捷的理念相当契合，快速反馈，不断改进。</p>
<p><img src="http://images.gitbook.cn/04b913e0-cb80-11e7-8434-c96d2575d6ec" alt="enter image description here" /></p>
<h4 id="behaviordrivendevelopmentbdd">Behavior Driven Development（BDD）</h4>
<p>Dan North 在 <a href="https://dannorth.net/introducing-bdd/">https://dannorth.net/introducing-bdd/</a> 中首次介绍了 BDD 行为驱动开发（Behavior Driven Development）。行为驱动开发鼓励软件项目中的开发者、QA 和非技术人员或商业参与者之间的协作。主要是从用户的需求出发，强调系统行为。</p>
<p>BDD 的描述方式是：</p>
<blockquote>
  <p>Given some initial context (the givens), 
  when an event occurs, 
  then ensure some outcomes.</p>
</blockquote>
<p>现在大多数的测试框架都支持 BDD 方式的测试用例。</p>
<h3 id="-4">团队协作</h3>
<p>随着团队渐入佳境，团队意识到仅仅是个人修炼还不足够，应该通过协作让整个开发部署的过程更加流畅。</p>
<p><img src="http://images.gitbook.cn/67c302f0-cb82-11e7-bd73-a5e299f09609" alt="enter image description here" /></p>
<h4 id="-5">持续交付</h4>
<p>《持续交付——发布可靠软件的系统方法》译者乔梁给出的定义是：</p>
<blockquote>
  <p>持续交付本身是一种能力，什么样的能力？以一种可持续的方式，安全快速的把你的变更，无论是features、配置管理、用户体验，放到你的生产环境上让用户使用。所以说持续交付本身定义的是一种能力，一种软件团队端到端的交付能力。</p>
  <p><img src="http://images.gitbook.cn/5809a4f0-cac3-11e7-ac4a-47599145e13b" alt="enter image description here" /></p>
  <p>持续集成，会逐步打破开发和测试之间的墙。敏捷开发，则引导往上游走了一步，让 PO（在 XP 方法中，叫现场客户）卷入进来，试图消除业务需求与产品研发之间的墙。DevOps，则想要解决的是运维团队和研发团队之间的墙。持续交付则是希望端到端的去解决隔离墙的问题</p>
</blockquote>
<h4 id="-6">微服务架构</h4>
<p>微服务的概念源于2014年3月 Martin Fowler 所写的一篇文章 <a href="http://martinfowler.com/articles/microservices.html">Microservices</a>。</p>
<p>微服务架构的思考是从与整体应用对比而产生的。
 <img src="http://images.gitbook.cn/6eafb860-cac4-11e7-ac4a-47599145e13b" alt="enter image description here" /></p>
<p>整体架构与微服务架构的主要差异体现在对应用组件封装的方式。相关联的业务逻辑和数据作为一个微服务存在，形成独立的边界，为外界提供 APIs，可以在不影响其他微服务的情况下单独更快的交付。</p>
<p>微服务架构的优点：</p>
<ul>
<li>每个微服务相对简单，只关注于一个业务功能。 </li>
<li>微服务之间松耦合的，可以提供更高的灵活性。</li>
<li>每个微服务可以选择合适的工具和开发语言。</li>
<li>每个微服务可由不同团队独立开发和维护。</li>
</ul>
<p>微服务架构的缺点：</p>
<ul>
<li>微服务数量上升会导致其业务复杂的上升。</li>
<li>运维开销及成本增加。</li>
<li>代码重复。</li>
<li>分布式系统的复杂性。</li>
<li>异步机制：微服务往往使用异步编程、消息与并行机制，如果应用存在跨微服务的事务性处理，其实现机制会变得复杂化。</li>
<li>可测性的挑战：在动态环境下服务间的交互会产生非常微妙的行为，难以可视化及全面测试。</li>
</ul>
<p>在合适的项目，合适的团队，采用微服务架构收益会大于成本。但在拥抱微服务之前，也需要认清它所带来的挑战。必须避免为了“微服务”而“微服务”。Martin Fowler 在<a href="https://martinfowler.com/bliki/MicroservicePremium.html">这篇文章</a>做出来比较。</p>
<p><img src="http://images.gitbook.cn/87e3c9b0-cac5-11e7-9016-9914a694cb6e" alt="enter image description here" /></p>
<p>推荐阅读：</p>
<ul>
<li><a href="http://gitbook.cn/books/59870d65d115e231bf3e3f5f/index.html">为什么微服务实施那么难？如何高效推进微服务架构演进？</a></li>
<li><a href="http://gitbook.cn/books/58f9cf76f3b99c3750fe0e5c/index.html">微服务的集成测试，怎么做才高效？</a></li>
</ul>
<h4 id="cloud">云 Cloud</h4>
<p>Cloud 现在已经不是新鲜的概念了，随着越来越多的应用都成为 cloud based application，那么就应该了解一些别人的好的实践，尤其推荐 <a href="https://12factor.net/zh_cn/">云端软件开发的 12 factors</a>。</p>
<p>I. 基准代码：一份基准代码，多份部署</p>
<p>II. 依赖：显式声明依赖关系</p>
<p>III. 配置：在环境中存储配置</p>
<p>IV. 后端服务：把后端服务当作附加资源</p>
<p>V. 构建，发布，运行：严格分离构建和运行</p>
<p>VI. 进程：以一个或多个无状态进程运行应用</p>
<p>VII. 端口绑定：通过端口绑定提供服务</p>
<p>VIII. 并发：通过进程模型进行扩展</p>
<p>IX. 易处理：快速启动和优雅终止可最大化健壮性</p>
<p>X. 开发环境与线上环境等价：尽可能的保持开发，预发布，线上环境相同</p>
<p>XI. 日志：把日志当作事件流</p>
<p>XII. 管理进程：后台管理任务当作一次性进程运行</p>
<p>12 factors 应用的这些原则已经被应用于绝大部分主流软件以及框架中。它为设计一个健壮的，可靠的，可扩展的系统架构奠定了基础。</p>
<h4 id="docker">容器 Docker</h4>
<p>以 Docker 为代表的容器化已经日渐成为创建，发布，运行分布式应用的主流方式，还催生了专门管理容器化应用的各种平台，比如 AWS ECS，Kubernetes（一个开源的，用于管理云平台中多个主机上的容器化的应用，目标是让部署容器化的应用简单并且高效，提供了应用部署，规划，更新，维护的一种机制）。</p>
<p>容器化优点包括：</p>
<ul>
<li>资源独立、隔离， 不同应用或服务以“集装箱”（container）为单</li>
<li>环境的一致性 </li>
<li>轻量化：相比传统的虚拟化技术（VM），Docker Container 的快速创建、启动、销毁相当方便快捷。</li>
<li>Build Once, Run Everywhere.</li>
</ul>
<p>所以还没有开始应用 Docker 的团队，建议不妨一试。</p>
<h3 id="-7">尾声</h3>
<p>故事的结尾，必然是团队从此快乐的工作在敏捷环境中，持续学习和进步，比如现在流行的 GraphQL 的 API 设计，机器学习，AI，区块链技术。。。。</p>
<p>什么？你的团队还没到那个境界？
那么作为敏捷教练，你需要的是继续完成这次达人课的学习 ~~~~ 加油！</p></div></article>