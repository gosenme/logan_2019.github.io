---
title: Flutter：从入门到实践-41
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>恭喜大家，终于完成了整个 Flutter 课程的学习！希望大家经过这个课程的学习，可以独立地进行应用开发了。不论是个人开发还是实际的公司项目研发，希望大家后续多多探索，继续加油。</p>
<p>这个课程是我精心规划、很认真编写的课程，课程内容的编写、结构设计、案例的编写都是独立完成的，我付出了很多，当然也收获了很多。我很高兴和大家一起成长和进步，并且对 Flutter 的未来发展充满信心，相信 Web、PC 和嵌入式等平台的 SDK 会很快推出，Flutter 会更加强大和完善。那么最后一节内容我就跟大家聊一下：</p>
<blockquote>
  <ul>
  <li>课程总结与感想</li>
  <li>Flutter 和 Dart 的总结和展望</li>
  <li>经验与建议</li>
  </ul>
</blockquote>
<h3 id="">课程总结与感想</h3>
<p>这门课程我大概写了5个月，每一篇都一个字一个字地去组织和表达，案例也是从 0 编写。虽然有时很辛苦，但是看到了自己的研究和写作成果后，我的内心其实是非常欣慰的。当然，看到其他学习者、开发者在阅读学习这门课程，给我一些很好的反馈的时候，我内心更是充满了欣喜和动力。</p>
<p>我们都知道，Flutter 和 Dart 是 Google Flutter 团队推出的，最近大家都很关注的鸿蒙系统其实也有些类似 Flutter 和 Fuchsia OS。Flutter 是基于 Dart 语言的跨平台框架，未来的 Flutter 将全面跨主流平台：Android、IOS、Windows（研发中）、Mac（研发中）、Linux（研发中）、Fuchsia OS（研发中）、Web（研发中）、物联网系统（研发中）、后端、前端等等。</p>
<p>其中，很多人期待的 Web SDK 很可能会在今年发布一个比较完善的版本。</p>
<p>希望大家能够认真学习 Flutter，对于一门新兴的、有前景的技术，如果你能够成为第一批学习者，那么你可以很快地成为技术引领者，自身的收益也会非常大。</p>
<h3 id="flutterdart">Flutter 和 Dart 的总结和展望</h3>
<p><img src="https://images.gitbook.cn/d76a89d0-bf3b-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>Google 公司于 2018 年 12 月 5 日发布了 Flutter 1.0 正式版，大半年的时间过去了，Flutter 最新版本已经到了 V1.8.4 了，更加完善和稳定。Dart 的最新版本已经到了 v2.5.0。Flutter 和 Dart 的更新频率很快，官方维护的一些插件库和开发者提交的插件库也越来越多，相关的文档、资源也更加丰富，能够看到 Flutter 生态已经逐步完善。</p>
<h5 id="flutter">Flutter 目前发展</h5>
<p>Flutter 从 1.0 正式版发布的大半年的时间里，开发者数量、插件库数量等都在指数级增长，吸引了来自全球各个国家的开发者和科技公司，目前 Flutter 已经成为最热门的开源项目之一了。当然，Flutter 在国内的发展也非常的迅猛。在 StackOverflow 2019 年的全球开发者问卷调查中，Flutter 被选为最受开发者欢迎的框架之一，超过了 TensorFlow 和 Node.js。</p>
<p><img src="https://images.gitbook.cn/3d309d90-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>全球已经有很多大家熟悉的公司采用了 Flutter 进行研发，其中包括一些国内的知名大厂，比如阿里巴巴、腾讯、京东、美团等。</p>
<p><img src="https://images.gitbook.cn/5ceb0580-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>来自丹麦的应用 Reflectly，已经率先使用 Flutter 重写了客户端，一套 Flutter 代码编写了 Android 和 iOS 端的 Reflectly 应用。</p>
<p><img src="https://images.gitbook.cn/8590e7c0-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>在国内，Flutter 的开发者和社区非常活跃，其中最令人激动的就是：在今年 Google I/O 前举办的全球 Flutter Create 大赛中，来自中国广东的胡泽标凭借一个特别精致的罗盘应用摘得了 Flutter Create 全球大奖。</p>
<p><img src="https://images.gitbook.cn/b0183430-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>笔者也获得了一张证书：</p>
<p><img src="https://images.gitbook.cn/f02e4d20-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>更多参赛作品及源码可以在下面地址进行查看和学习：</p>
<p><a href="https://flutter.dev/create">https://flutter.dev/create</a> </p>
<p>前面我们介绍过，Flutter 会支持大部分的主流平台，一套语言、一套逻辑就可以实现跨多平台，如 Android、IOS、Web、PC、Fuchsia OS、物联网等主流平台。</p>
<p><img src="https://images.gitbook.cn/d1bba770-bf3c-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<h5 id="fuchsiaos">Fuchsia OS</h5>
<p>除了 Flutter 外，Google 的 Fuchsia OS 有望成为一个未来的热门操作系统，虽然还没有推出正式版本，但是吸引了一大批开发者和学习爱好者。Flutter 和 Dart 开发的应用是 Fuchsia OS 默认支持的。Fuchsia OS 是一套可运行在手机、平板、PC 等端口的跨平台系统，放弃了 Linux 内核，而是基于 Zircon微核，采用 Flutter 引擎+ Dart 语言编写。预测在 2020~2021 年，Fuchsia OS 正式版将会推出使用，也许有一天会替代 Android 系统。据传，Google 已经聘请了有着十多年 Mac OS 开发经验的资深苹果系统开发工程师 Bill Stevenson 来操盘 Fuchsia，目标是推向成熟市场。华为的很多设备也已经很早就配合 Flutter 和 Fuchsia OS 进行了测试，我们也期待 Fuchsia OS 可以早日推出。</p>
<h5 id="flutterweb">Flutter Web</h5>
<p><img src="https://images.gitbook.cn/1d7f9560-bf45-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>除了 Flutter 移动平台外，最引入瞩目的就是 <a href="https://flutter.dev/web">Flutter Web</a> 的支持了，虽然 Web SDK 正式版还没有发布，不过通过预览测试版，我们就有理由相信 Flutter Web 将会大大简化我们开发 Web 页面的成本，无需编写繁杂的 CSS 和 JS、HTML，一套 Flutter 代码就轻松搞定一个 Web 页面系统。</p>
<p>目前，Flutter for Web 的示例应用在桌面浏览器基本能达到每秒 60 帧的渲染速度。但是在移动浏览器，特别是在低端机型上还有很大的优化空间。</p>
<p>Flutter Web 官方的测试预览例子可以在：<a href="flutter.github.io/samples">flutter.github.io/samples</a> 进行学习和体验，目前通过这几个例子来看，效果非常的不错。</p>
<p><img src="https://images.gitbook.cn/736924f0-bf45-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>Flutter for Web 目前处在技术预览阶段，相信很快会推出正式版本。</p>
<h5 id="flutter-1">Flutter 桌面和嵌入式</h5>
<p>Flutter 也将支持桌面 PC 平台，目前处于研发实验阶段，未来可以用 Flutter 开发 Mac、Windows 和 Linux 、Chrome OS 、Fuchsia OS 上运行的 Flutter 应用。</p>
<p>Flutter 桌面的实验性项目：</p>
<p><a href="https://github.com/google/flutter-desktop-embedding">https://github.com/google/flutter-desktop-embedding</a></p>
<p>Flutter 桌面的早期说明：</p>
<p><a href="https://github.com/flutter/flutter/wiki/Desktop-shells">https://github.com/flutter/flutter/wiki/Desktop-shells</a></p>
<p>Flutter 未来也将支持在嵌入式设备商进行开发和运行，例如在 Raspberry Pi 等小型设备上运行 Flutter 应用。</p>
<p>Flutter嵌入式示例：</p>
<p><a href="https://medium.com/flutter-io/flutter-on-raspberry-pi-mostly-from-scratch-2824c5e7dcb1">https://medium.com/flutter-io/flutter-on-raspberry-pi-mostly-from-scratch-2824c5e7dcb1</a></p>
<p>Flutter 嵌入式 API：</p>
<p><a href="https://github.com/flutter/flutter/wiki/Custom-Flutter-Engine-Embedders">https://github.com/flutter/flutter/wiki/Custom-Flutter-Engine-Embedders</a></p>
<p>目前项目处于实验测试阶段。</p>
<h5 id="flutter-2">Flutter 游戏</h5>
<p>在 Google I/O 19 期间，Flutter 团队和 2Dimensions 联合发布了一款运营 / RPG 游戏: Flutter Developer Quest。除了作为游戏本身在游戏性上毫不缩水外，代码也完全开源。</p>
<p>游戏源代码地址：</p>
<p><a href="https://github.com/2d-inc/developer_quest">https://github.com/2d-inc/developer_quest</a></p>
<p>这是一个新的拓展和尝试，大家可以自行进行游戏源码的阅读和学习。</p>
<h5 id="flutter-3">Flutter 近期展望</h5>
<p>Flutter 的近期动态已经在 FlutterGithub 主页的 Github wiki 上进行了公开。</p>
<p><img src="https://images.gitbook.cn/fe73ee90-bf45-11e9-bb40-bd92c8f37632" alt="Flutter" /></p>
<p>"accepted" 目录中的为工程实施阶段，"working" 目录中的为设计阶段，大家可以持续关注。</p>
<p>地址：</p>
<p><a href="https://github.com/flutter/flutter/wiki/Roadmap">https://github.com/flutter/flutter/wiki/Roadmap</a></p>
<p><a href="https://github.com/dart-lang/language">https://github.com/dart-lang/language</a></p>
<p>当然我们也可以关注「谷歌开发者」这个微信公众账号来获取更多更新的动态消息。</p>
<p>总之，Flutter 和 Dart 都在按照计划研发中，相信不久我们便可以看到一些关于 Flutter 和 Dart 的新的东西。</p>
<h3 id="-1">经验与建议</h3>
<p>我学习和研究 Flutter 这门新技术，当时文档非常少，基本上是看着官方文档、例子进行的学习和研究，设立一个目标进行边开发边学习，渐渐扩展到很多知识点上面，所以这里也建议大家按照自己之前擅长的编程语言对比着进行学习，有目的地进行学习，这样可能会一点一点扩展研究和学习的范围，效率更高。</p>
<p>还有就是借鉴“前人”的经验。我希望大家能通过本课程，可以做到学习和开发上的事半功倍，少走一些弯路。</p>
<p>建议使用自己擅长的 IDE 进行开发，每个 IDE 都有自己的优点和缺点，所以大家可以根据实际情况进行选择。关于使用模拟器还是真机进行开发调试也是一样，都有各自的优缺点，大家可以根据实际情况，根据效率最高的方式进行选择搭配。</p>
<p>最后，感谢大家的认真学习和反馈，也感谢大家的热情，希望后续可以推出更多更好的 Flutter 和 Dart 新拓展的文章分享给大家，我们一起研究、一起学习、一起进步。</p></div></article>