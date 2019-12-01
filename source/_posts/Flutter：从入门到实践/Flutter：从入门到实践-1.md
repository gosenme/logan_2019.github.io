---
title: Flutter：从入门到实践-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>移动开发的前方突破口在哪里？</p>
<p>小团队如何面向未来做技术选型？</p>
<p>想要独立开发一个产品，能不能做到省心省力？</p>
<p>我用两个关键词来回答这些问题：跨平台、Flutter。</p>
<h3 id="">背景</h3>
<p>最近，Flutter 在前端和移动开发圈里引起了不小的热度，阮一峰老师也专门发表了一篇博文。</p>
<p><img src="https://images.gitbook.cn/Fl3DRcI1N9HQJrN6XNfHt3pkmDoq" alt="ruanyf的博文" /></p>
<p>因为，谷歌官方正式宣布 Flutter 全面支持多平台，包括移动平台 Android/iOS、Web( 新发布 )、桌面 PC 平台（内测中）、嵌入式平台（内测中）。</p>
<p>Flutter 具有高扩展性和高性能。可以预见，这门颠覆性编程技术将成为未来主流。一套代码逻辑规范实现全平台开发！不过 Flutter 起步于移动端、目前重心也在移动平台，其他平台 Google Flutter 团队正在逐步拓展完善。所以学习 Flutter 我们也先从移动端的开发学起。</p>
<h4 id="-1">跨平台是趋势</h4>
<p>现在技术更新非常快，可能几年内就会有一个新的技术出现。移动端、前端、后端开发领域的边界逐渐模糊，要求一个开发者掌掌握多端开发的场景也越来越多，所以跨平台开发技术层出不穷。</p>
<p>为什么会这样呢？我们可以来分析一下。</p>
<p><strong>首先，节约成本的优先选择（用人单位的需求）。</strong></p>
<p>互联网行业捡钱的时代已经过去了，现在的公司纷纷选择精简人员配置，尤其对于规模不大的公司来说，开发一个产品要投放各平台，至少需要一个 Web 端开发，一个 Android 开发，一个 iOS 开发，人力成本相当高。因此，在跨平台实现效果与原生开发效果的差别愈发缩小的时候，很多公司更倾向于采用跨平台开发。</p>
<p>反之，对于开发者个人，去提前了解甚至掌握基本的跨平台开发技术，不但能补足自己的技术栈，还能在趋势早期创造明显的就业优势。</p>
<p><strong>其次，设备的发展造成了需求（使用者的需求）。</strong></p>
<p>我们都有体会，以前计算机语言和技术出现和迭代的频率并没有这么高。我认为，其中一个重要因素是硬件设备的制造门槛越来越低，计算机运算速度越来越快。</p>
<p>现在，计算机运算速度提高到了恐怖的程度，它缩小甚至抹平了很多技术的差距，导致不同技术呈现效果几乎相同。设备形态也五花八门多种多样，人们使用着不同尺寸和特点的设备，自然希望自己惯用的某一款产品，在这些设备上都能流畅地打开和使用。难道每增加一个新设备，就要配备一个专门的开发工程师吗？</p>
<p><strong>还有，技术的发展提供了可能性（开发者的需求）。</strong></p>
<p>原有的技术为了迎合使用者的需求，正在不断地更新迭代，与此同时，大量新的技术和语言也在孕育和产生。它们的目标都是更便捷、更高效的开发。</p>
<p>面对产品提出的各种需求，为了提高开发效率，开发者们是倾向于使用包容性强、适配性好的语言和技术。</p>
<p>整个分析下来，可以看到，跨平台正是大势所趋。</p>
<p>而 Flutter 的出现让跨平台移动端的接近原生的高性能体验成为可能，并不断在扩展 Web 端、PC 端等平台。</p>
<h4 id="flutter">Flutter 是趋势</h4>
<blockquote>
  <p><em>Flutter: a Portable UI Framework for Mobile, Web, Embedded, and Desktop.</em></p>
  <p>（Flutter，一个支持手机、网页、可嵌入设备、和桌面的可移植 UI 框架。）</p>
</blockquote>
<p>Flutter 是 Google 力推的跨平台框架，将是未来的 Google Fuchsia OS 下开发应用的主要技术框架。</p>
<p>谷歌对 Flutter 的投入非常大，SDK 的更新频率也很高。2019 年 5 月 8 号，谷歌刚刚发布了 Flutter 1.5 稳定版。</p>
<p><strong>Flutter 的开发将不仅仅局限于移动跨平台，目前已经支持 Web 开发、后端开发、PC 桌面应用开发（内测中）、嵌入式开发（内测中）。</strong> </p>
<p>Google 的消息推出后，阮一峰老师也第一时间表达了他对 Flutter 的看好：</p>
<blockquote>
  <p>"我的看法是，如果现在学习跨平台应用开发，第一个要看的不是 React Native，而是 Flutter。"</p>
</blockquote>
<p>其实，撇开个人开发者，许多大公司早就率先尝试了 Flutter。国内的阿里巴巴、腾讯、爱奇艺等大公司已经把 Flutter 应用在实际开发中，例如闲鱼团队已经把 Flutter 技术应用在闲鱼应用上。</p>
<p>那 Flutter 开发体验如何？</p>
<ul>
<li>Flutter 入门容易</li>
</ul>
<p>Flutter 基于 Dart 语言编写，有 React 语言风格，又结合 JavaScript、Java 优点，有面向对象开发语言基础的同学，很容易就上手了。</p>
<ul>
<li>Flutter 真正跨平台</li>
</ul>
<p>除了原生外，目前跨平台技术一般是混合开发，如采用 H5、React Native、Weex、小程序等技术。不过这些或多或少都能感觉到卡顿和体验不流畅，并且开发和学习成本非常高，而且都有各自的局限性。</p>
<p>Flutter 既能用原生代码直接调用的方式来加速图形渲染和 UI 绘制，又能同时运行在两大主流移动操作系统上。看下几种方案的对比情况：</p>
<table>
<thead>
<tr>
<th>技术</th>
<th style="text-align:right;">性能</th>
<th style="text-align:center;">开发效率</th>
<th style="text-align:center;">渲染方式</th>
<th style="text-align:center;">学习成本</th>
<th style="text-align:center;">可扩展性</th>
</tr>
</thead>
<tbody>
<tr>
<td>Flutter</td>
<td style="text-align:right;">高，接近原生体验</td>
<td style="text-align:center;">高</td>
<td style="text-align:center;">Skia 高性能自绘引擎</td>
<td style="text-align:center;">低，Widget 组件化</td>
<td style="text-align:center;">高，采用插件化的库进行扩展</td>
</tr>
<tr>
<td>RN/Weex/小程序</td>
<td style="text-align:right;">有延迟，一般</td>
<td style="text-align:center;">一般，复杂、效率低</td>
<td style="text-align:center;">Js驱动原生渲染</td>
<td style="text-align:center;">高，复杂</td>
<td style="text-align:center;">一般</td>
</tr>
<tr>
<td>原生应用</td>
<td style="text-align:right;">高</td>
<td style="text-align:center;">一般</td>
<td style="text-align:center;">原生渲染</td>
<td style="text-align:center;">高，需要学习 Android 和 iOS 原生 API</td>
<td style="text-align:center;">高</td>
</tr>
</tbody>
</table>
<p>从上面的对比可以看出，<strong>Flutter 的优势明显：高体验度、高开发效率、低学习成本、高可扩展性，未来 Google Flutter 团队还将使 Flutter 支持 PC 和 Web 的跨平台开发，真正全平台。</strong></p>
<ul>
<li>Flutter 用户体验媲美原生</li>
</ul>
<p>可以说 Flutter 是一个革命性、创新性的技术框架，它实现了一套语言实现 Android 和 iOS 终端平台的高效开发，并且非 Web 跨平台模式，而是采用全新渲染引擎 Skia。它实现的应用体验和原生基本一致，流畅度远远高于目前的小程序、React 等技术方案，官方公布可以达到 60 FPS，甚至要高于原生的流畅度体验。</p>
<ul>
<li>Flutter 开发过程轻松</li>
</ul>
<p>太多开发者的切身实践证明，Flutter 的开发体验也相当不错！</p>
<blockquote>
  <p><em>I wrote nicer, more maintainable code that runs on both iOS and Android. It also took considerably less time and fewer lines of code to do so.</em></p>
  <p>（我编写了更漂亮、更易于维护的代码，可以同时运行在 iOS 和 Android 上。 它只花费了我相当少的时间和比原生开发更少的代码行。）</p>
  <p><em>——Why Flutter Will Change Mobile Development for the Best</em></p>
</blockquote>
<p>基于原生开发的 SDK，能轻松写出同时运行在 Android/iOS 的代码。</p>
<p>Flutter 成为未来主流跨平台开发框架技术已经势在必行，它开发高效、性能优秀、更新频率快、插件三方库支持多、Google 团队的技术支持给力、一套代码多终端运行，这些都非常的吸引人。</p>
<p>最后总结下，Flutter 全面网罗 Web、Android、iOS、Windows、linux、桌面、浏览器甚至物联网设备，未来趋势是属于 Flutter 的！</p>
<p><img src="https://images.gitbook.cn/FoVU16X-6CH0tBun7yQwUsbV46od" alt="谷歌官方图" /></p>
<h3 id="-2">课程大纲</h3>
<p>本课程主要面向有开发经验 1 年及以上的开发者，或者想转入学习 Flutter Dart 的开发者，不限语言。</p>
<p>课程内容注重基础入门，在学习的深度和广度上都有很好的权衡，帮助大家高效学习 Flutter 编程。
课程按照编程思维规划学习路径，可以让我们的学习事半功倍，少走弯路。
每一章节内容都按照 Google 官方源码和文档编写实例，既保留官方的原汁原味，又加入相关辅助学习的案例与注释，可以边学习边实践。</p>
<p>本课程大纲分为四大部分，共计 39 篇，分阶段讲解 Flutter 框架。</p>
<h4 id="flutterdart">第一部分：Flutter 和 Dart 初探</h4>
<p>主要是 Flutter 和 Dart 介绍、最高效的开发工具和环境的搭建、模拟器安装和调试、编译和打包应用、项目结构介绍、配置文件详解、开发规范、基础组件讲解、基础布局讲解等等。</p>
<p>让你快速地进入一个崭新的技术和语言的学习中，了解它的基础中的重点核心部分。</p>
<h4 id="flutterwidget">第二部分：Flutter 核心 Widget 应用</h4>
<p>主要讲解 Flutter 的核心常用 Widget、路由、HTTP 网络请求详解（3 种 POST 和 1 种 GET）、WebSocket、JSON 编解码、文件和图片读写操作详解、手势和数据库缓存详解、动画、应用国际化等。</p>
<p>每一部分都是实例讲解学习，都是精心设计案例。并且实例里面涵盖了官方的大部分 API 的用法，还扩展了其他常用的 API，让你学习到官方文档上没有详细讲解到的 API 用法。</p>
<h4 id="flutter-1">第三部分：Flutter 开发深入</h4>
<p>第三部分主要讲解了自定义 Widget、原生和 Flutter 交互、编写 Flutter Plugin 框架、Flutter 调试、Android 和 iOS 的打包、Dart2 的 Web 开发、Dart Pub 仓库的使用和提交等。最后有一个完整的小应用的实践，综合了整个知识点。</p>
<h4 id="flutter-2">第四部分：Flutter 扩展实践</h4>
<p>第四部分是应用实践的扩展，包括类似音视频播放、权限处理、状态管理如何实践，使学习者的实践技能更加丰富。</p>
<h3 id="-3">寄语</h3>
<p>介绍了这么多，相信未来几年大家可以在热门编程语言/跨平台框架排行榜的前几名上看到 Dart 和 Flutter。本套 Flutter 开发系列课程，可以让你学习 Flutter 事半功倍，更加高效、更加快速地认识和学习这门新技术、新语言、新语法！</p>
<p>希望每一位学习本课程的学习者，能够在技术上有所收获，在心态上更加自信。学习 Flutter，迎合未来主流趋势，赢得新技术主动权！</p>
<p>如果大家有什么更好的建议或者疑问，都可以沟通和交流，一起学习一起进步，加油！</p>
<blockquote>
  <p><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5cc01cc115a1a10d8cec9e86&utm_source=Raysd001">点击了解更多《Flutter：从入门到实践》</a></p>
</blockquote></div></article>