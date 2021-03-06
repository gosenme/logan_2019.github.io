---
title: Angular 基础教程-92
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="iosandroid">iOS 和 Android 上的效果</h3>
<p>拿起手机，打开 Safari 浏览器或者 Chrome 浏览器，<a href="https://damoqiongqiu.github.io/NiceFish-ionic/">访问这个网址</a>。</p>
<p>如果不想手动输入这么长的 URL，可以用微信扫描以下二维码：</p>
<p><img src="https://images.gitbook.cn/81393e50-1412-11e9-9eb4-ed144f53659c"  width = "15%" /></p>
<p>然后选择用对应的浏览器打开：</p>
<p><img src="https://images.gitbook.cn/a29d3790-1412-11e9-8c2a-99fa369b9aa3"  width = "30%" /></p>
<p>在 Safari 浏览器中打开之后，点击浏览器底部的菜单，然后选择“添加到主屏幕”，就像这样：</p>
<p><img src="https://images.gitbook.cn/c55d8c80-1412-11e9-9673-d9141386da8e"  width = "25%" /></p>
<p>Chrome 浏览器的操作步骤是：打开折叠菜单 | 选择“更多工具”| 点击“创建快捷方式”。</p>
<p>然后就可以看到应用图标出现在手机的主屏幕上了，就像这样：</p>
<p><img src="https://images.gitbook.cn/f6888620-1412-11e9-9eb4-ed144f53659c"  width = "25%" /></p>
<p>点击打开应用，就会看到这样的界面：</p>
<p><img src="https://images.gitbook.cn/2fb27730-1413-11e9-9673-d9141386da8e"  width = "30%" /></p>
<blockquote>
  <p>注意：iOS 版本需要大于 11.3。</p>
</blockquote>
<h3 id="windows10pwa">Windows 10 内置了对 PWA 的支持</h3>
<p>Windows 10 也已经支持 PWA 应用，当你在 Chrome 的菜单里面选择把这个应用“添加到主屏幕”之后，就可以看到这样的结果：</p>
<p><img src="https://images.gitbook.cn/558a9370-1413-11e9-8c2a-99fa369b9aa3"  width = "40%" /></p>
<blockquote>
  <p>注意：Windows 10 需要升级到最新的更新包。</p>
</blockquote>
<h3 id="linux">Linux 上的效果</h3>
<p>在 Linux 上的操作步骤是一样的：打开 Chrome 浏览器 | 在菜单中选择“更多工具”|“创建快捷方式”。</p>
<p>得到的效果是这样的：</p>
<p><img src="https://images.gitbook.cn/7ead94f0-1413-11e9-8c2a-99fa369b9aa3"  width = "50%" /></p>
<h3 id="">小结</h3>
<p>可以看到，PWA 是一个极其强大的东西，真正的一套代码搞定多个平台，使用 Web 技术开发，无需打包，也无需发布。</p>
<p><a href="https://github.com/damoqiongqiu/NiceFish-ionic">此项目对应的代码开源可点击这里查看</a>。</p>
<p>下面介绍介绍关于 PWA 的发展过程还有技术细节。</p>
<h3 id="pwa">PWA 是什么</h3>
<p>PWA 是 Google 在 2015 年提出的一种全新的 Web 应用开发规范。</p>
<p>PWA（Progressive Web Apps，渐进式 Web 应用）这个缩写是由 Google Chrome 团队的 Alex Russell 提出来的。</p>
<p>PWA 不针对特定的语言，也不针对特定的框架，它本身只是一种规范，只要你的应用能满足 PWA 提出的规范，那么它就是一款 PWA 应用。</p>
<p>PWA 需要具备的关键特性有：</p>
<ul>
<li>应用无需安装，无需发布到应用市场</li>
<li>可以在主屏幕上创建图标</li>
<li>可以离线运行，利用后台线程与服务端通讯（由 ServiceWorker 特性来支持）</li>
<li>对搜索引擎友好</li>
<li>支持消息推送</li>
<li>支持响应式设计，支持各种类型的终端和屏幕</li>
<li>方便分享，用户可以方便地把应用内部的 URL 地址分享出去</li>
</ul>
<p>如果你想知道自己的应用是否是 PWA，<a href="https://developers.google.com/web/progressive-web-apps/checklist">官方提供了一份清单可供核对，具体可详见这里</a>。</p>
<p>Google 官方对 PWA 的描述是这样的：</p>
<p>Progressive Web Apps are just great web sites that can behave like native apps—or, perhaps, Progressive Web Apps are just great apps, powered by Web technologies and delivered with Web infrastructure.</p>
<h3 id="pwa-1">三大厂商已经全部支持 PWA</h3>
<p>目前，Apple、Microsoft、Google 已经全部支持 PWA 技术。</p>
<p>Google 的 Android 平台、Chrome 平台、Chrome Book 平台已经能全部支持 PWA：</p>
<p><img src="https://images.gitbook.cn/fa198a30-1414-11e9-bcbf-c7935765cfd0"  width = "50%" /></p>
<p><img src="https://images.gitbook.cn/11f0c010-1415-11e9-8c2a-99fa369b9aa3"  width = "50%" /></p>
<p>iOS 11.3 开始内置支持 PWA：</p>
<p><img src="https://images.gitbook.cn/26faf340-1415-11e9-8c2a-99fa369b9aa3"  width = "50%" /></p>
<p>Windows 10 已经全面支持 PWA，目前 Windows 10 的应用商店里面已经有非常多的 PWA 应用了：</p>
<p><img src="https://images.gitbook.cn/3ea74890-1415-11e9-8c2a-99fa369b9aa3"  width = "50%" /></p>
<p><img src="https://images.gitbook.cn/52540ea0-1415-11e9-8c2a-99fa369b9aa3"  width = "60%" /></p>
<p>三大厂商齐心合力支持同一种技术规范是非常罕见的现象，从目前的情况看，PWA 将会成为一个比较大的热点。</p>
<p>注意：国内外的互联网生态完全不同，国内移动互联网基本上被微信、今日头条所把持，目前微信小程序的影响力比 PWA 更大，微信小程序的数量已经超过 100万 个。另外，很多消息推送服务在国内用不了。</p>
<h3 id="pwa-2">中国厂商的“快应用”与 PWA 的区别</h3>
<p><img src="https://images.gitbook.cn/72a25220-1415-11e9-9673-d9141386da8e"  width = "50%" /></p>
<p>2018 年 3 月 20 日，国内 10 大手机厂商共同参会，支持“快应用”标准，这些厂商包括：华为、中兴、小米、Oppo、Vivo、魅族、联想等。</p>
<p>从技术层面看，“快应用”与 React Native 类似，它和 PWA 完全不同。PWA 是完全的 Web 技术，借助于浏览器渲染，是“页面”；而“快应用”是类似于 RN 的“原生渲染”模式，JS 相关的代码运行在 JSCore 里面，然后通过 Bridge 驱动原生代码渲染 UI 界面，整体思路如下图：</p>
<p><img src="https://images.gitbook.cn/9eac46f0-1415-11e9-9673-d9141386da8e"  width = "50%" /></p>
<p>从目前的发展情况来看，小米 8 已经对“快应用”做了很好的支持。</p>
<h3 id="-1">参考资源</h3>
<ul>
<li>2015 年 11 月，Alex Russell 关于 PWA 的原始文章，<a href="https://medium.com/@slightlylate/progressive-apps-escaping-tabs-without-losing-our-soul-3b93a8561955">详见这里</a></li>
<li><a href="https://developers.google.com/web/progressive-web-apps/">Google 官方提供的文档</a></li>
<li><a href="https://www.quickapp.cn/">快应用官方网站</a></li>
</ul></div></article>