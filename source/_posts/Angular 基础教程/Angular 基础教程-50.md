---
title: Angular 基础教程-50
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>有的读者可能会问：Angular 相关的文章到处都有，我为什么要来学习这门课？</p>
<p>这是一个非常好的问题，说明读者对阅读内容有质量要求。</p>
<p>如果是我，我也会有这样的疑惑。</p>
<p>整体上说，这门课的内容有以下特色。</p>
<p>最近 5 年我一直在“玩”前端方面的东西，比如 jQuery、SVG、Ext JS、Adobe Flex、Angular；尤其在 2016 年，这一整年的时间我代表 Angular 项目组在中国进行技术推广。因此，我会<strong>按照初学者一般的学习过程</strong>，用我自己的语言<strong>一步一步进行讲解</strong>。</p>
<p>在这 5 年里，我在超过 50 家企业、开源组织、大学里面进行了大量演讲，在网络上发布了大量的视频和文章。在到处奔波的过程中，认识了很多人，有经验丰富的后端开发者、也有新入行的初学者，他们跟我说过很多自己的困惑，我会把<strong>常见的一些疑问融入在内容里面</strong>。</p>
<p>我也会<strong>扫平日常开发中常见的坑</strong>，这些坑大部分都是开发者们反馈给我的，或者是到我这里吐槽过的。举几个典型的例子：</p>
<ul>
<li>很多开发者到我这里来抱怨说，在 Windows 平台上安装 @angular/cli 会报很多 error，那是因为 @angular/cli 在 Windows 平台上面依赖 Python 和 Visual Studio 环境，而很多开发者的机器上并没有安装这些东西。为什么要依赖这些环境？因为某些 npm 包需要在你本地进行源码编译。</li>
<li>node-sass 模块被墙的问题，强烈推荐使用 cnpm 进行安装（<a href="http://npm.taobao.org/">点击这里跳转到安装地址</a>），可以非常有效地避免撞墙。</li>
<li>一些开发者来抱怨说 @angular/cli 在打包的时候加上 <strong>--prod</strong> 参数会报错，无法编译。这是一个很常见的问题，因为 @angular/cli 最新的版本经常会有 bug，只要在项目的 package.json 里面降低一个小版本号就 OK 了。另外，加 <strong>--prod</strong> 参数之后，编译器会进行更加严格的检查，如果存在无用的组件或者配置错误，则编译过不去。</li>
<li>@angular/cli 默认生成的 karma.conf.js 配置文件里面采用了一个有 bug 的 HTML 报告生成器，导致 ng test 运行报错，我们需要把这个 reporter 改成 mocha（摩卡），具体的配置和实例请参考“第10课：自动化测试”中的讲解。</li>
<li>还有的开发者说，本地开发的时候运行得很好，上线之后所有请求 404。这也是一个常见的坑，因为你需要给 Web 容器配置一下处理 HTTP 请求的规则，把前端路由扔回去交给 Angular 处理，<a href="https://github.com/angular-ui/ui-router/wiki/Frequently-Asked-Questions">可点击这里查看具体的情况</a>。</li>
</ul>
<p>诸如此类的坑还有不少，我都是一个一个踩过来的。当然，我相信读者也能踩过来，但是从节约时间的角度来看，跟着我的思路走一遍岂不是更快？</p>
<p>这门课全部聚焦在使用层面上，<strong>覆盖日常开发中使用频率最高的特性</strong>，除非迫不得已，尽量不扯原理。长期以来，我发现有很多读者的学习方式存在误区，比如，有一些人上来就去研究“变更检测”的原理，还有 RxJS 的原理，这种方式除了打击你自己的自信心之外得不到任何好处。因为你迟早会发现，在计算机领域，任何东西研究到最底层都和“算法”、“数据结构”、“设计模式”有关。</p>
<p>据我所知，很多读者平时并没有去研究这些内容的基础知识，因此，我推荐采用<strong>更加务实一点的方案</strong>，首先学会如何使用，等用熟练了，有时间、有闲情的时候再去研究那些底层的原理。设计发动机很难，但是学会开车并不难，对吧？所以我写这门课的目标很简单，就是带你学会开车，而不是教你设计发动机。</p>
<p>这门课非常看重“<strong>概念模型</strong>”（Mental Model）的构建。我发现，很多开发者已经做过非常多的项目了，但是当你跟他聊的时候，很快就会发现他并没有掌握这门框架的精髓。打几个比方：</p>
<ul>
<li>当有人提到 Spring 的时候，你的大脑里面第一个想到的一定是 DI、IoC、AOP 等这些核心概念；</li>
<li>当有人提到 Hibernate、MyBatis、JPA 的时候，你的大脑里面立即会浮现出 ORM 等概念；</li>
<li>当有人提到 React 的时候，你想到的应该是 VDOM、JSX；</li>
<li>当有人提到 jQuery 的时候，你首先想到的应该是 $，对吧？</li>
</ul>
<p>因此，可以看到，任何一个成功的框架都有自己独创的“概念模型”，或者叫“核心价值”也可以，这是框架本身存在的价值，这些核心概念是掌握这个框架应该紧扣的主线，而不是上来就陷入到茫茫的技术细节里面去。</p>
<p>课程里面涉及到的<strong>例子总数量大约有 300 个</strong>，有少量例子来自官方文档（大约 5 个），其他的例子都是我自己一点一点手动敲出来的。我把这些例子分成了 <strong>10 个开源项目</strong>，它们互相独立，方便读者进行参考和练习。这些教学用的开源项目本身是免费的，已放在了本课的末尾。</p>
<h3 id="angular">Angular 的概念模型</h3>
<p>既然如此，问题就来了，新版本的 Angular 的核心概念是什么呢？</p>
<p>非常简单，一切都是围绕着“组件”（Component）的概念展开的。</p>
<p><img src="https://images.gitbook.cn/86a9de10-e25f-11e8-aea1-e3c6bbbc3251"  width = "35%" /> </p>
<ul>
<li>Component（组件）是整个框架的核心，也是终极目标。“组件化”的意义有 2 个：一是分治，因为有了组件之后，我们可以把各种逻辑封装在组件内部，避免混在一起；二是复用，封装成组件之后不仅可以在项目内部复用，而且还可以沉淀下来跨项目复用。</li>
<li>NgModule（模块）是组织业务代码的利器，按照自己的业务场景，把组件、服务、路由打包到模块里面，形成一个个的积木块，然后再用这些积木块来搭建出高楼大厦。</li>
<li>Router（路由）的角色也非常重要，它有 3 个重要的作用：一是封装浏览器的 History 操作；二是负责异步模块的加载；三是管理组件的生命周期。</li>
</ul>
<p>因此，在这门课程里面，Component、NgModule、Router 加起来会占据绝大部分的篇幅，而一些琐碎的小特性会被忽略掉。我相信，读者只要紧扣“组件化”这个主线，就能站在一个很高的角度去统摄全局，从而掌握到这个框架的精髓。</p>
<h3 id="">适合阅读的人群</h3>
<p>本课程内容适合以下人群阅读：</p>
<ul>
<li>Angular 新版本的初学者</li>
<li>有 AngularJS 经验的开发者</li>
<li>希望了解 Angular 新版本核心特性的开发者</li>
<li>Java 和 .NET 开发者，会发现 Angular 里面的很多概念和做法非常适合已经掌握了那些概念模型的开发者，学起来会非常快</li>
</ul>
<p><strong>特别注意：这门课程不是前端入门读物，读者至少需要会一门编程语言，无论前端还是后端都可以，如果你曾经使用过一门前端框架，那就更好了。</strong></p>
<h3 id="-1">集中回答一些常见的问题</h3>
<h4 id="-2">浏览器兼容性</h4>
<p>关于 Angular 的浏览器兼容性，请看下图：</p>
<p><img src="https://images.gitbook.cn/af32e980-e25f-11e8-aea1-e3c6bbbc3251" alt="enter image description here" /></p>
<p>有一些国内的开发者会来争论兼容 IE 8 的问题，请看下面的两个事实。</p>
<ul>
<li>第一个事实：截至 2018 年 10 月底，Chrome 的全球市场份额已经接近 60.6%，Safari 占 14.85%，Firefox 占 5.01%，加起来已经占到 80.46%，真的没有那么多人用 IE 了。</li>
</ul>
<p><img src="https://images.gitbook.cn/bf60e910-e25f-11e8-aea1-e3c6bbbc3251" alt="enter image description here" /></p>
<p><a href="http://gs.statcounter.com/browser-market-share">点击这里查看数据来源</a>。</p>
<ul>
<li>第二个事实：天猫已经于 2016 年 4 月宣布放弃支持 IE 6、7、8 了。而根据百度流量研究院的统计，IE 8 目前的整体市场份额已经下降到了 9.31%。</li>
</ul>
<p><img src="https://images.gitbook.cn/cd5cc660-e25f-11e8-aea1-e3c6bbbc3251" alt="enter image description here" /></p>
<p><a href="http://tongji.baidu.com/data/browser">点击这里查看数据来源</a>。</p>
<p>读者完全可以用上面的两点事实去说服客户，不值得为了这么少的市场份额付出那么多的研发和维护成本。</p>
<h4 id="-3">命名约定</h4>
<p>老版本使用 AngularJS 指代，所有新版本都叫做 Angular。原因很好理解，因为老版本是用 JS 开发的，所以带一个 JS 后缀，而新版本是基于 TypeScript 开发的，带 JS 后缀不合适。</p>
<h4 id="typescript">关于 TypeScript</h4>
<p>这门课程不会单独讲 TypeScript，正如我一直强调的：TypeScript 不难，JavaScript 才难。你跟着我的思路，<strong>TypeScript 绝对不会成为你学习 Angular 的障碍</strong>。相反，一旦你写代码熟练了之后，TypeScript 可以非常有效地提升编码效率和程序可读性。</p>
<h4 id="angular-1">关于 Angular 的版本</h4>
<p>官方的版本发布计划是：</p>
<ul>
<li>每 6 个月发布一个主版本（第一位版本号，主版本）</li>
<li>每个主版本发布 1 ~ 3 个小版本（第二位版本号，Feature 版本号）</li>
<li>每周发布一个补丁版本（第三位版本号，Hotfix 版本号）</li>
</ul>
<p>根据官方的解释，Angular 2.0 之后会保证向下兼容，只有在升级主版本的时候才会做一些 breaking change。因此，这门课程不再强调版本号，涉及到的所有实例代码都已经升级到了当前最新的 7.x 版本（2018-11）。</p>
<p>本课程划分 3 大部分，共计 48 篇（含导读）。</p>
<ul>
<li>第一部分（第 01 课 ~ 第 10 课，共 32 篇）的内容将围绕组件、模块、路由三大概念，兼顾服务、RxJS、表单、i18n 等小工具，全面解释了 Angular 的基本用法。</li>
<li>第二部分（第 11 课，共 8 篇）的内容将专门解释依赖注入，这是 Angular 比较有特色的内容，这部分的内容比较有深度，虽然在日常开发中使用不多，但是理解它能够更加深入理解 Angular。</li>
<li>第三部分（第 12 课 ~ 附录 3，共 7 篇）介绍了产品级案例项目 OpenWMS、PWA 案例、一些参考资源以及 3 个新版本特性附录。</li>
</ul>
<p><a href="https://gitee.com/learn-angular-series/">本系列文章对应的所有示例项目列表可点击这里查看</a>。</p>
<p>最后是那一句套话：水平有限，错漏难免，欢迎指正。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmqqsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote></div></article>