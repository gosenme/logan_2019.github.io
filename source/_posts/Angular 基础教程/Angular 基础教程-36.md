---
title: Angular 基础教程-36
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>为了能更方便地理解后面的内容，你需要预先理解以下两个概念：</p>
<ul>
<li>组件树</li>
<li>注射器树</li>
</ul>
<p>同时还要介绍一个调试神器 Augury，注意，这货读 ['ɔ:ɡjuri]，是“占卜”、“预言”的意思，不是 angry，不是愤怒！</p>
<h3 id="">组件树</h3>
<p>目前，几乎所有前端框架都在玩“组件化”，而且最近都不约而同地选择了“标签化”这种思路，Angular 也不例外。“标签化”会导致一个很自然的结果，组件之间会形成树形结构。例如，对于下面这样一个界面：</p>
<p><img src="https://images.gitbook.cn/d818c9a0-d25f-11e9-84ba-0bd4ba7d7fb3"></p>
<p>用 Angular 实现出来的组件树结构是这样的：</p>
<p><img src="https://images.gitbook.cn/e8783970-d25f-11e9-8d0f-6b56ebcd1907"></p>
<p>在线查看运行效果：</p>
<blockquote>
  <p>http://47.104.13.149:4200/</p>
</blockquote>
<p>repo 地址：</p>
<blockquote>
  <p>http://git.oschina.net/mumu-osc/NiceFish</p>
</blockquote>
<h3 id="injectortree">Injector Tree</h3>
<p>如你所知，AngularJS 是第一个把“依赖注入”（Dependency Injection）思想带到前端开发领域的框架。</p>
<p>在《Angular 初学者快速上手教程》里面，关于“注射器树”这事儿我们没说太细，这里要说得更精确一点：<strong>如果一个 DOM 元素上面被创建了 Component 或者 Directive，Angular 就会创建一个对应的注射器实例。</strong></p>
<p>对于上面的组件结构，形成的注射器结构是这样的：</p>
<p><img src="https://images.gitbook.cn/0292cfa0-d260-11e9-bcae-b7c2737c8da6"></p>
<p>很明显，这些 Injector 实例也构成了树形结构：</p>
<p><img src="https://images.gitbook.cn/092ae410-d260-11e9-8d0f-6b56ebcd1907"></p>
<p><strong>请记住这个树形结构，后续的所有内容都是以此为基础展开的。</strong></p>
<h3 id="augury">利用 Augury 可视化查看注射器树</h3>
<p>Augury 是一款 Chrome 插件，它是调试 Angular 应用的利器，利用它可以可视化展示组件树、路由树，以及服务依赖关系。</p>
<p>比如，对于 NiceFish 首页：</p>
<p><img src="https://images.gitbook.cn/3280b560-d260-11e9-b943-9d5bb2abdc80"></p>
<p>它的服务依赖关系是这样的：</p>
<p><img src="https://images.gitbook.cn/386c0f10-d260-11e9-84ba-0bd4ba7d7fb3"></p>
<p>组件依赖关系是这样的：</p>
<p><img src="https://images.gitbook.cn/3e258350-d260-11e9-b943-9d5bb2abdc80"></p>
<p>整体路由树是这样的：</p>
<p><img src="https://images.gitbook.cn/44e2fa10-d260-11e9-b943-9d5bb2abdc80"></p>
<h3 id="-1">小结</h3>
<p>到这里为止，你知道了：<strong>在 Angular 应用运行时，组件之间会构成树形结构，Injector（注射器）的实例也会构成树形结构。</strong></p>
<p>接下来，我们从易到难，把注射器玩儿出花来。</p>
<h3 id="-2">参考资源</h3>
<ul>
<li><a href="https://angular.io/guide/dependency-injection">https://angular.io/guide/dependency-injection</a></li>
<li><a href="http://git.oschina.net/mumu-osc/NiceFish">http://git.oschina.net/mumu-osc/NiceFish</a></li>
</ul></div></article>