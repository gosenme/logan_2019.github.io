---
title: SSM 搭建精美实用的管理系统-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="61">6.1 简介</h3>
<p>在前文论述中，十三对后台管理系统作了简单的介绍和总结，希望朋友们对后台管理系统有一个更加清晰的认识，但千万不要觉得后台系统在整个项目中是一个可有可无甚至无关痛痒的角色。如果你依然觉得后台管理系统不需要考虑这么多，那么十三先来带大家看一组某商城后台管理系统的设计稿，请点击访问下面链接，从中你将领悟到更多。</p>
<p>某商城后台管理系统的完整详细的设计稿：<a href="https://www.zcool.com.cn/work/ZMjYzODAxMzY=.html">WeApp Design</a></p>
<p>其中的设计规范基本涵盖了后台管理系统所有的元素，前文中提到的后台系统相关元素都在此设计规范中有提到，如下面这些：</p>
<ul>
<li>布局风格；</li>
<li>字体规范；</li>
<li>配色规范；</li>
<li>菜单栏设计；</li>
<li>按钮设计；</li>
<li>输入框规范；</li>
<li>弹出框；</li>
<li>提示框。</li>
</ul>
<p>甚至交互规范，都清楚地标示在文档中，从中可以看出原来我们并不特别重视的后台管理系统竟然有如此多的门道在里面，在设计和实现的时候竟有如此多需要认真考虑的知识点和规范。</p>
<p>当然，本课程的重点并不在此，因此朋友们也无需担心，我们并不需要完全按照这份规范从头开发，毕竟有很多优秀的前端 HTML/CSS 框架可以直接用到实际项目开发中，而且基本都涵盖了以上规范中的元素和具体实现，比如现在四个比较流行的 HTML/CSS 框架：</p>
<ul>
<li>Bootstrap ；</li>
<li>EasyUI ；</li>
<li>Layui ；</li>
<li>Semantic UI 。</li>
</ul>
<p>这些 HTML/CSS 框架将常见的 CSS 布局组件和 JavaScript 插件进行了整合并进行完善的封装，不仅仅是布局规范而且整合了各种插件，也实现了十三在前文中列举的大部分系统元素，如弹框、按钮、表格、导航栏等等，即使是没有太多前端经验的开发工程师都可以迅速掌握和使用，极大地提升了开发效率。</p>
<h3 id="62bootstrap">6.2 BootStrap</h3>
<p>本次实战所选用的是 BootStrap 4，接下来，十三将对其进行简单的介绍。</p>
<ul>
<li><p><a href="http://www.bootcss.com/">BootStrap中文网</a></p></li>
<li><p><a href="https://github.com/twbs/bootstrap">BootStrap In GitHub</a></p></li>
</ul>
<blockquote>
  <p>Bootstrap 是美国 Twitter 公司的设计师 Mark Otto 和 Jacob Thornton 合作基于 HTML 、CSS 、JavaScript 开发的简洁、直观、强悍的前端开发框架，使得 Web 开发更加快捷。</p>
  <p>Bootstrap 提供了优雅的 HTML 和 CSS 规范，由动态 CSS 语言 Less 编写写成。Bootstrap 一经推出后颇受欢迎，一直是 GitHub 上的热门开源项目（截止十三整理这篇文章，Star 数目为125763），包括 NASA 旗下的 MSNBC Breaking News 都使用了该项目。是国内一些移动开发者较为熟悉的框架，如 WeX5 等前端开源框架，也是基于 Bootstrap 源码进行性能优化升级而来。</p>
</blockquote>
<p>BootStrap的目录结构如下：</p>
<pre><code>bootstrap/
└── dist/
    ├── css/
    │   ├── bootstrap-grid.css
    │   ├── bootstrap-grid.css.map
    │   ├── bootstrap-grid.min.css
    │   ├── bootstrap-grid.min.css.map
    │   ├── bootstrap-reboot.css
    │   ├── bootstrap-reboot.css.map
    │   ├── bootstrap-reboot.min.css
    │   ├── bootstrap-reboot.min.css.map
    │   ├── bootstrap.css
    │   ├── bootstrap.css.map
    │   ├── bootstrap.min.css
    │   └── bootstrap.min.css.map
    └── js/
        ├── bootstrap.bundle.js
        ├── bootstrap.bundle.js.map
        ├── bootstrap.bundle.min.js
        ├── bootstrap.bundle.min.js.map
        ├── bootstrap.js
        ├── bootstrap.js.map
        ├── bootstrap.min.js
        └── bootstrap.min.js.map
</code></pre>
<h4 id="1">1. 优点</h4>
<p>其火热和广泛流行的原因总结起来如下：</p>
<ul>
<li>BootStrap 提供了一套完整的基础 CSS 插件；</li>
<li>BootStrap 提供了一组基于 jQuery 的 JavaScript 插件集；</li>
<li>Bootstrap 提供了非常丰富的组件与插件，组件包含小图标、按钮组、菜单导航、标签页等等；</li>
<li>Bootstrap 扩展性强，兼容各种脚本插件；</li>
<li>Bootstrap 拥有现成 UI 组件，可以快速搭建网页页面；</li>
<li>Bootstrap 使得响应式网站的实现更加简单；</li>
<li>Bootstrap 框架为用户提供了一套响应式移动设备优先的流式栅格系统，拥有完备的框架结构，整体效果和谐，对谷歌、火狐、IE 等浏览器均可支持，项目开发方便快捷；</li>
<li>Bootstrap 不断适应 Web 技术的发展，其十分成熟，在大量的项目中已得到充分的使用和测试；</li>
<li>十分重要的一点是，Bootstrap 拥有完善的文档，使用起来十分方便。</li>
</ul>
<p>借助 BootStap 提供的插件集、组件集可以很方便地搭建我们想要的网站。</p>
<p>前文中提到的其他三个 HTML/CSS 框架，想要了解和学习的朋友也可以自行去学习体验，这里就不再花费篇幅一一介绍了。</p>
<h4 id="2bootstrap">2. 为什么选择 BootStrap</h4>
<p>主要原因，可以归结为以下几点。</p>
<ul>
<li>符合规范。</li>
</ul>
<p>网站的产品设计中，各个元素和组件都需要涉及到，BootStrap 则提供了从字体到页面布局再到交互体验所有的风格和设计，且提供了多种规范的风格和标准的可替换主题。</p>
<ul>
<li>使用成本低。</li>
</ul>
<p>官方提供了源码和工具包，只需要导入其 JS 文件和 CSS 样式表就可以轻松实现一个 BootStrap 风格的页面，集成的过程十分简单、方便、快捷，使用起来很简单。</p>
<ul>
<li>复用性。</li>
</ul>
<p>复用性是衡量一个工具或者框架优劣的重要指标，代码复用性高可以节省开发者的开发时间且代码不会臃肿复杂，BootStrap 包中包含了大量现成的代码片段可以直接拿来使用，只要找到符合产品的代码段直接使用即可，减少了开发者重复编码的频率，提高了代码的复用性。</p>
<ul>
<li>学习成本低。</li>
</ul>
<p>BootStrap 是 2011 年在 GitHub 上发布的开源产品，至今已有 7 个年头，但是依然更新频繁、不停迭代，由于其众多优异的特性使得其在开源社区十分活跃，且帮助文档十分齐全，国内网站上的相关教程也比较多，因此学习起来很容易。</p>
<ul>
<li>可维护性。</li>
</ul>
<p>开箱即用、上手快使得集成了 BootStrap 的项目维护难度降低，同时 Bootstrap 具有现成的组件、CSS 样式以及可以直接在代码中引用的插件，可以减轻对代码的维护，以便高效地组织代码。</p>
<ul>
<li>减少时间成本。</li>
</ul>
<p>详尽的学习文档使得 BootStrap 学习成本降低，因此花费较少的时间就可以掌握并使用，Bootstrap 提供了非常丰富的组件与插件，可以显著地节省时间和精力，使得项目进展加快，实现快速开发，节省了大量的时间成本。</p>
<ul>
<li>响应式。</li>
</ul>
<p>响应式网站最大的特点就是不管在电脑、平板还是手机上，都会根据屏幕尺寸自动调节大小，图片分辨率等等，已经渐渐成为一股强力的技术趋势，而 Bootstrap 就是响应式框架，Bootstrap 能以超快的速度与效率适应不同平台间的差异。</p>
<h3 id="63adminlte3">6.3 AdminLTE3</h3>
<p>在开篇词中，十三向大家展示了本课所要完成的最终实战 Demo 效果，如下图所示：</p>
<p>登录页：</p>
<p><img src="https://images.gitbook.cn/5dae6670-8e18-11e8-bd0f-f38f8b899327" alt="log-in" /></p>
<p>富文本编辑页：</p>
<p><img src="https://images.gitbook.cn/7fa243a0-8e18-11e8-a3e9-3b5653895392" alt="rich-text-manage" /></p>
<p>可能有朋友会问，我们的实战项目是用 BootStrap 技术实现的网站吗？</p>
<p>十三给你的答案是：可以说是，也可以说不是。说不是的原因是这个项目的 HTML 模板选用的是 AdminLTE3 而不是 BootStrap，说是原因则是因为 AdminLTE3 这个 WebApp 模板同样是基于 BootStrap4 开发而来，接下来十三会简单的介绍一下 AdminLTE3 。</p>
<blockquote>
  <p>AdminLTE3 是一个完全响应式管理并基于 Bootstrap 4 的免费高级管理控制面板主题，目前开源于 GitHub 上，截止十三整理这篇文章时已经有 24K 的 Star 数量，开源社区十分活跃且特别受欢迎，其开源协议是 MIT 许可证，拥有相对宽松的软件授权条款，开源、流行且高度可定制化、易于使用，这只是它众多优点中的凤毛麟角而已。</p>
</blockquote>
<p>AdminLTE3 基于 Bootstrap，因此前文中提到的 Bootstrap 的优点 AdminLTE 模板也都有，不仅仅如此，AdminLTE 自适应多种屏幕分辨率，兼容 PC 端和手机移动端，且内置了多个模板页面，包括仪表盘、邮箱、日历、锁屏、登录及注册、404 错误、500 错误等页面，拥有多种主题皮肤，支持多种浏览器，插件齐全，AdminLTE 是基于模块化设计，因此很容易在其之上定制和重制及二次开发。</p>
<p>目前市面上比较流行的是 2.x 版本，本教程选用的是 AdminLTE 3 版本，因此就不再对 2.x 版本进行介绍了，有兴趣的朋友可以去其官网查看。</p>
<ul>
<li><a href="https://adminlte.io/">AdminLTE</a></li>
<li><a href="https://github.com/almasaeed2010/AdminLTE">AdminLTE In GitHub</a></li>
</ul>
<p>AdminLTE 3 效果预览：</p>
<p><img src="https://images.gitbook.cn/6f6a3c80-8e19-11e8-bd0f-f38f8b899327" alt="Adminlte3-1" /></p>
<p><img src="https://images.gitbook.cn/813ee730-8e19-11e8-80d1-2d51ff7e1c55" alt="Adminlte3-2" /></p>
<h4 id="1-1">1. 产品对比</h4>
<p>类似 AdminLTE 的基于 BootStrap 的成品后台模板还有：Hui 、Ace Admin 、Metronic 、H+ UI(hplus) 。</p>
<p>—— <strong>Hui</strong></p>
<blockquote>
  <p><a href="http://demo.h-ui.net/H-ui.admin/3.1/index.html">Hui 预览地址</a></p>
</blockquote>
<p>Hui 具有以下特点：</p>
<ul>
<li>采用源生 HTML 语言，完全免费，简单灵活，兼容性好，可以快速搭建中小型网站后台；</li>
<li>作者是国人；</li>
<li>开源免费；</li>
<li>2018 年并没有特别大的版本改动。</li>
</ul>
<p><img src="https://images.gitbook.cn/441aefb0-8e1a-11e8-b093-3f5eaa2cb071" alt="hui" /></p>
<p>—— <strong>Ace Admin</strong> </p>
<blockquote>
  <p><a href="http://ace.jeka.by/">Ace Admin 预览地址</a></p>
</blockquote>
<p>Ace Admin 具有以下特点：</p>
<ul>
<li>流行过一段时间的后台管理系统模板；</li>
<li>开源免费； </li>
<li>很久没更新了。</li>
</ul>
<p><img src="https://images.gitbook.cn/9ffc0df0-8e1a-11e8-a3e9-3b5653895392" alt="ace-admin" /></p>
<p>—— <strong>Metronic</strong> </p>
<blockquote>
  <p><a href="https://www.metronic.com/"> Metronic 预览地址</a></p>
</blockquote>
<p>Metronic 具有以下特点：</p>
<ul>
<li>优秀的后台模板； </li>
<li>收费产品。</li>
</ul>
<p><img src="https://images.gitbook.cn/be321fd0-8e1a-11e8-b093-3f5eaa2cb071" alt="metronic" /></p>
<p>—— <strong>H+ UI（hplus）</strong> </p>
<blockquote>
  <p><a href="http://www.zi-han.net/theme/hplus/">H+ UI（hplus）预览地址</a> </p>
</blockquote>
<p>H+ UI（hplus）具有以下特点：</p>
<ul>
<li>国内比较流行的后台管理系统模板； </li>
<li>作者是国人； </li>
<li>收费产品； </li>
<li>2015 年后并没有特别大的版本改动。</li>
</ul>
<p><img src="https://images.gitbook.cn/ef08b7e0-8e1a-11e8-80d1-2d51ff7e1c55" alt="hplus" /></p>
<h4 id="2adminlte3">2. 为什么选择 AdminLTE3</h4>
<p>以上四个后台管理系统模板加上 AdminLTE3 模板都十分优秀，且在大量的项目中充分使用，因此都可以当做后台管理系统的模板页面来进行快速开发，至于为什么选择 AdminLTE3 作为本次教程的模板则有以下原因。</p>
<ul>
<li>基于 BootStrap 。</li>
</ul>
<p>前文中谈到 BootStrap 的优点 AdminLTE 模板也都有，响应式、代码复用性高、上手快……</p>
<ul>
<li>视觉效果。</li>
</ul>
<p>对比了几个系统模板，AdminLTE 应该是最漂亮的，从看到的第一眼就会喜欢上，美观、大气。</p>
<ul>
<li>社区活跃。</li>
</ul>
<p>关注度高、更新迭代快，一直在进步和优化。</p>
<ul>
<li>复用性高。</li>
</ul>
<p>工具齐全且内置了比较完善的后台管理系统所需页面，可以大大减少开发工作量，开箱即用。</p>
<ul>
<li>开源免费。</li>
</ul>
<p>一般这种类似成品的 WebApp 模板都是收费的，而 AdminLTE 是完全免费的，开源在 GitHub 上。</p>
<h3 id="64">6.4 总结</h3>
<p>本文主要介绍了 BootStrap 和 AdminLTE，本次实战教程的前端页面和交互均基于 BootStrap 和 AdminLTE3 。二者虽不相同但是关系十分紧密，AdminLTE 模板基于 BootStrap 同时又做了相应的完善和改造，因此可以当作一个成品模板直接拿来运用到项目开发中。</p>
<p>相较于 AdminLTE 3，BootStrap 并没有组装完成，想要完整的产品还需要自己去实现。BootStrap 更像是一个个的组件，相当于一个个的工具类，同时又是一套优秀的前端规范，不过，没有 BootStrap 就没有 AdminLTE 模板的出现，而 AdminLTE 又将 BootStrap 的闪光点进一步扩大，使人惊叹。</p>
<p>前端工具选型，首先要明确目的，之后根据自己的需求和技术能力进行选择，确定自己需要开发什么样的产品或者说公司更需要哪种技术栈的人才，然后针对性地去学习，这样才会事半功倍。</p>
<p>同后端技术选型类似，复用性和可维护性是十分重要的指标，工具性的产品就是为了减少代码臃肿和提升开发效率，在技术选型中这两个指标一定不能忽略，之后则需要从工具的成熟度、社区活跃度、学习成本来考虑。</p>
<p>如果社区比较活跃且各种文档齐全的话学习起来比较简单，遇到问题也可以很快地得到解答，同时这种活跃的气氛也会反哺这个工具，使得 Bug 修复速度加快、迭代优化更频繁，这才是一种良性循环，总结下来有如下几点需要重点关注：</p>
<ul>
<li>是否符合需要；</li>
<li>能否提升开发效率；</li>
<li>框架的普及程度；</li>
<li>社区活跃度；</li>
<li>学习成本。</li>
</ul>
<p>不仅仅是前端技术选型，工作中使用的一些技术都可以按照以上五个原则进行对比和选择，之后则是学习并运用到实际工作中。</p>
<p>至此，本项目的基本技术选型都已经介绍完毕，后端框架使用 Spring+Spring MVC+MyBatis，前端页面模板则是 AdminLTE3+BootStrap，希望通过本课程的介绍，朋友们对后台管理系统又有了新的认识。</p>
<p>部分文件已上传至百度云，可自行下载查看体验，百度云盘分享地址：</p>
<blockquote>
  <p>链接：https://pan.baidu.com/s/1b5oJjkSp5EuReu6SsI8SuQ </p>
  <p>密码：r3fe</p>
</blockquote></div></article>