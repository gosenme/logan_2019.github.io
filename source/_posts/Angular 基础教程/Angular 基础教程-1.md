---
title: Angular 基础教程-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>有的读者可能会问：Angular 的文章到处有，网上一大堆，我为什么要来学习这个系列内容？</p>
<p>这是一个非常好的问题，说明你对阅读内容有质量要求。</p>
<p>如果是我，我也会有这样的疑惑。</p>
<p>整体上说，这个系列的内容有以下特色。</p>
<p>我会<strong>按照初学者一般的学习过程</strong>，用我自己的语言<strong>一步一步进行讲解</strong>。最近的 5 年我一直在“玩”前端方面的东西，从 jQuery、SVG、ExtJS、Adobe Flex、Angular，这样一路“玩”过来的；尤其是 2016 年，这一整年的时间我代表 Angular 项目组在中国进行技术推广。</p>
<p>在这 5 年里，我在超过 50 家企业、开源组织、大学里面进行了大量演讲，在网络上发布了大量的视频和文章。在到处流串的过程中，认识了很多人，有经验丰富的后端开发者、也有新入行的初学者，他们跟我讲过很多自己的困惑。因此，这个系列文章里面的内容我至少反复讲过 20 遍以上，我会把常见的一些疑问融入在内容里面。</p>
<p>我会<strong>扫平日常开发中常见的坑</strong>，这些坑大部分都是开发者们反馈给我的，或者是到我这里吐槽过的。举几个典型的例子：</p>
<ul>
<li>很多开发者到我这里来抱怨说，在 Windows 平台上安装 @angular/cli 会报很多 error，那是因为 @angular/cli 在 Windows 平台上面依赖 Python 和 Visual Studio 环境，而很多开发者的机器上并没有安装这些东西。为什么要依赖这些环境？因为某些 npm 包需要在你本地进行源码编译。</li>
<li>node-sass 模块被墙的问题，强烈推荐<a href="http://npm.taobao.org/">使用 cnpm 进行安装</a>，可以非常有效地避免撞墙。</li>
<li>一些开发者来抱怨说 @angular/cli 在打包的时候加上 <strong>--prod</strong> 参数会报错，无法编译。这是一个很常见的问题，因为 @angular/cli 最新的版本经常会有 bug，只要在项目的 package.json 里面降低一个小版本号就 OK 了。另外，加 <strong>--prod</strong> 参数之后，编译器会进行更加严格的检查，如果存在无用的组件或者配置错误，编译过不去。</li>
<li>@angular/cli 默认生成的 karma.conf.js 配置文件里面采用了一个有 bug 的 html 报告生成器，导致 ng test 运行报错，我们需要把这个 reporter 改成 mocha（摩卡），具体的配置和实例请参考“前端自动化测试”中的讲解。</li>
<li>有一些朋友说，本地开发的时候运行得很好，上线之后所有请求 404。这也是一个常见的坑，因为你需要给 Web 容器配置一下处理 HTTP 请求的规则，把前端路由扔回去交给 Angular 处理，<a href="https://github.com/angular-ui/ui-router/wiki/Frequently-Asked-Questions">请参考这里</a>。</li>
</ul>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<p>诸如此类的坑还有不少，我都是一个一个踩过来的。当然，我相信你自己也能踩过来，但是从节约时间的角度看，还是跟着我的思路走一遍更快不是吗？</p>
<blockquote>
  <p><strong>需要特别说明的是：有一些坑是 NodeJS 或者某些模块导致的，还有一些是因为被墙，并不全是 Angular 的锅。</strong></p>
</blockquote>
<p>这个系列的文章全部聚焦在使用层面的话题，覆盖日常开发中使用频率最高的特性，除非迫不得已，尽量不扯原理。长期以来，我发现有很多朋友的学习方式存在误区，比如，有一些人上来就去研究“变更检测”的原理，还有 RxJS 的原理，这种方式除了打击你自己的自信心之外并不能得到任何好处。因为你迟早会发现，在计算机领域，任何东西研究到最底层都和“算法”、“数据结构”、“设计模式”有关。而就我所知，很多朋友并不具备研究这些内容的基础知识，不过是白白浪费自己的时间而已。</p>
<p>另外，研究原理不得不去阅读各种源代码，但是很少有源代码会提供详细的文档。阅读这样的源代码肯定会迷路，就像这样：</p>
<p><img src="https://images.gitbook.cn/ea16ee40-ac60-11e9-add6-13ebc1d14b27" width = "60%" /></p>
<p>因此，我推荐采用更加务实一点的方案，首先学会如何使用，等用熟了，有时间、有闲情的时候再去研究那些底层的原理。设计发动机很难，但是学会开车并不难，对吧？所以我写这个系列的目标很简单，就是带你学会开车，而不是教你设计发动机。</p>
<p>这个系列的内容非常看重“概念模型”（Mental Model）的构建。我发现，很多开发者已经做过非常多的项目，但是当你跟他聊的时候，你很快就会发现他并没有掌握这门框架的精髓。打几个比方：</p>
<ul>
<li>当有人提到 Spring 的时候，你的大脑里面第一个想到的一定是 DI、IoC、AOP 这些核心概念；</li>
<li>当有人提到 Hibernate、MyBatis、JPA 的时候，你的大脑里面立即会浮现出 ORM 的概念；</li>
<li>当有人提到 React 的时候，你想到的应该是 VDOM、JSX；</li>
<li>当有人提到 jQuery 的时候，你首先想到的应该是 $，对吧？</li>
</ul>
<p>因此，可以看到，任何一个成功的框架都有自己独创的“概念模型”，或者叫“核心价值”也可以，这是框架本身存在的价值，这些核心概念是你掌握这门框架应该紧扣的主线，而不是上来就陷入到茫茫多的技术细节里面去。</p>
<p>文章里面所涉及到例子总数量大约 300 个左右，有少量例子来自官方文档（大约 5 个），其他都是我自己一点一点手动敲出来的。我把这些例子分成了十几个个开源项目，它们互相独立，方便大家进行参考和练习。这些教学用的开源项目本身是免费的，列在这篇文章的尾部。</p>
<h3 id="angular">Angular 的核心概念模型</h3>
<p>既然如此，问题就来了，新版本的 Angular 的核心概念是什么呢？</p>
<p>非常简单，一切都是围绕着“组件”（Component）的概念展开的：</p>
<p><img src="https://images.gitbook.cn/86a9de10-e25f-11e8-aea1-e3c6bbbc3251"  width = "40%" /> </p>
<ul>
<li>Component（组件）是整个框架的核心，也是终极目标。“组件化”的意义有 2 个：第一是分治，因为有了组件之后，我们可以把各种逻辑封装在组件内部，避免混在一起；第二是复用，封装成组件之后不仅可以在项目内部复用，而且可以沉淀下来跨项目复用。</li>
<li>NgModule（模块）是组织业务代码的利器，按照你自己的业务场景，把组件、服务、路由打包到模块里面，形成一个个的积木块，然后再用这些积木块来搭建出高楼大厦。</li>
<li>Router（路由）的角色也非常重要，它有 3 个重要的作用：第一是封装浏览器的 History 操作；第二是负责异步模块的加载；第三是管理组件的生命周期。</li>
</ul>
<p>所以，在这个系列的文章里面，Component、NgModule、Router 加起来会占据绝大部分篇幅，而一些琐碎的小特性会被忽略掉。我相信，你只要紧扣“组件化”这个主线，就能站在一个很高的角度统摄全局，从而掌握到这门框架的精髓。</p>
<h3 id="">适合阅读的人群</h3>
<p>这个系列的文章适合以下人群阅读：</p>
<ul>
<li>Angular 新版本的初学者</li>
<li>有 AngularJS 1.x 经验的开发者</li>
<li>希望了解 Angular 新版本核心特性的开发者</li>
<li>Java 和 .NET 开发者，因为你们会发现 Angular 里面的很多概念和做法非常适合你已经掌握的那些概念模型，你们学起来会非常快</li>
</ul>
<p><strong>特别注意：这个系列的文章不是前端入门读物，你至少需要会一门编程语言，无论前端还是后端都可以，如果你曾经使用过一门前端框架，那就更好了。</strong></p>
<h3 id="-1">集中回答一些常见的问题</h3>
<h4 id="-2">浏览器兼容性</h4>
<p>关于 Angular 的浏览器兼容性，请看下图：</p>
<p><img src="https://images.gitbook.cn/b11ec620-ac61-11e9-b99d-87fbe4d2a696" alt="enter image description here" /></p>
<p>有一些国内的开发者会来争论兼容 IE 的问题，下面展示一些事实：</p>
<ul>
<li>第一个事实是：天猫已经于 2016 年 4 月宣布放弃支持 IE6、7、8。而根据百度流量研究院的统计，截止到 2019 年 5 月，IE8 以下的浏览器在国内也只有 5.69% 的份额了：</li>
</ul>
<p><img src="https://images.gitbook.cn/ed6a4280-ac61-11e9-add6-13ebc1d14b27" alt="enter image description here" /></p>
<p><a href="http://tongji.baidu.com/data/browser">数据来源</a>，不值得为了这么少的市场份额付出那么多的研发和维护成本。</p>
<ul>
<li>第二个事实是：截至 2019 年 5 月底，Chrome 的全球市场份额已经高达 61.06%，加上 Safari 、Firefox 的份额，所有这些能完美支持 Web 标准的浏览器加起来，份额已经远远超过 80%。</li>
</ul>
<p><img src="https://images.gitbook.cn/0df7b1e0-ac62-11e9-9941-c769c68ebd94" alt="enter image description here" /></p>
<p><a href="http://gs.statcounter.com/browser-market-share">数据来源</a>。</p>
<ul>
<li>第三个事实是：微软 2018 年底宣布，后续新的浏览器会采用 Chromium 内核，并且已经与 2019 年初给出了预览版。如果有兴趣，<a href="https://www.microsoftedgeinsider.com/en-us/">可以到微软的官方网站来下载</a>。这就意味着，到 2019 年底的时候，基于 Chrome 内核的浏览器全球市场份额将会达到 85% 左右。因此，请不要再花那么多钱和时间来解决“浏览器兼容性问题”了，后面根本就不存在这个问题！</li>
</ul>
<p><img src="https://images.gitbook.cn/78934280-ac62-11e9-b243-f31642e7dba4" alt="enter image description here" /></p>
<p>你完全可以用以上事实去说服你的客户。</p>
<h4 id="-3">命名约定</h4>
<p>老版本使用 AngularJS 指代，所有新版本都叫做 Angular。原因很好理解，因为老版本是用 JS 开发的，所以带一个 JS 后缀，而新版本是基于 TypeScript 的，带 JS 后缀不合适。</p>
<h4 id="43typescript">4.3 关于 TypeScript</h4>
<p><img src="https://images.gitbook.cn/d4fc0750-ac62-11e9-9941-c769c68ebd94" width = "35%" /></p>
<p>这个系列的文章不会单独讲 TypeScript，正如我一直强调的：TypeScript 不难，JavaScript 才难。你跟着我的思路，TypeScript 绝对不会成为你学习 Angular 的障碍。相反，一旦你写熟练了之后，TypeScript 可以非常有效地提升编码效率和程序可读性。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<h4 id="angular-1">关于 Angular 的版本</h4>
<p>官方的版本发布计划是：</p>
<ul>
<li>每 6 个月发布一个主版本（第一位版本号，主版本）</li>
<li>每个主版本发布 1 到 3 个小版本（第二位版本号，feature 版本号）</li>
<li>每周发布一个补丁版本（第三位版本号，hotfix 版本号）</li>
</ul>
<p>根据官方的解释，Angular 2.0 之后会保证向下兼容，只有升级主版本的时候才会做一些 breaking change。所以这个系列文章里面不再强调版本号，涉及到的所有实例代码都已经升级到了当前最新的 8.0 版本（2019-07）。</p>
<h3 id="-4">内容结构</h3>
<p>本专栏共分 3 大部分，共计 51 篇文章（含附录）：</p>
<ul>
<li>第一部分：从第 1 篇到第 10 篇，围绕组件、模块、路由三大概念，兼顾服务、RxJS、表单、i18n 等小工具，全面解释 Angular 的基本用法。</li>
<li>第二部分：第 11 篇，专门解释依赖注入，这是 Angular 比较有特色的内容，这部分内容比较有深度，虽然在日常开发中使用不多，但是理解它能够更加深入理解 Angular。</li>
<li>第三部分：从第 12 篇到第 16 篇，介绍产品级案例项目 OpenWMS、PWA 案例、一些参考资源以及三个新版本特性附录。</li>
</ul>
<p>本系列文章对应的所有示例项目列表：<a href="https://gitee.com/learn-angular-series/">请点击这里查看</a>。</p>
<p>最后是那一句套话：水平有限，错漏难免，欢迎指正。</p>
<h3 id="changelog">本教程自己的 Changelog</h3>
<p>每次官方升级大版本，本教程和对应的系列开源项目都会跟随修订升级。为了让读者了解每次教程更新修改了哪些内容，所有修订（包括图文和代码）都会记录 changelog。</p>
<h4 id="201710">首次发布 2017-10</h4>
<p>这个专栏第一个版本是 2017 年 10 月发布的，到目前已经快两年的时间。</p>
<h4 id="220181030">第 2 次修订 2018-10-30</h4>
<ul>
<li>所有相关项目的代码都已经升级到了当前最新的 7.0 版本，NiceFish、OpenWMS、learn-* 系列，保证文字内容和实例代码同步。</li>
<li>《Angular 小专题：玩转注射器》里面的内容全部合并过来，作为第 11 篇的内容，之前购买的读者有福了，无需付费，刷新就能看到全部内容。</li>
<li>修改了一些数据和图表，使用当前最新的数据。</li>
<li>修改了一些配图。</li>
<li>增加 3 个附录，解释 5.0、6.0、7.0 更新了哪些内容。</li>
<li>修改之后共有 14 篇（46 个小节）。</li>
</ul>
<h4 id="320190701">第 3 次修订 2019-07-01</h4>
<ul>
<li>实例项目代码全部升级到了 8.0，<a href="https://gitee.com/learn-angular-series/">请点击这里查看</a>。</li>
<li>NiceFish 升级到了 8.0，<a href="https://gitee.com/mumu-osc/NiceFish">请点击这里查看</a>。</li>
<li>实例代码中的路由写法全部升级到了 8.0 最新的写法。</li>
<li>增加了 1.2 Schematics，解释代码生成器的用法。</li>
<li>增加了 8.2 节，升入解析 RxJS。</li>
<li>其他大量的文字和代码细节修改。</li>
<li>修改之后共有 16 篇（51 个小节）。</li>
</ul>
<p><strong>请放心：后面所有的更新和升级都是免费的，不需要你重新购买，因此现在购买的用户非常合算，你一直跟着看就可以了。</strong></p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<h3 id="-5">分享交流</h3>
<p>我们为本专栏付费读者创建了微信交流群，以方便更有针对性地讨论专栏相关问题。入群方式请到第04 篇末尾添加小助手的微信号，并回复关键字。</p>
<p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）<strong>。你的分享不仅帮助他人，更会提升自己。</strong></p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手微信后需要截已购买的图来验证~</p>
</blockquote></div></article>