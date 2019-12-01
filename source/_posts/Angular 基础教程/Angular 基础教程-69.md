---
title: Angular 基础教程-69
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我尽量把 Router 叫做“路由”或者“路由机制”，而不叫“路由器”，因为我总感觉“路由器”是一种网络设备，在前端开发领域叫“路由器”怪怪的。</p>
<p><strong>请特别注意：Angular 中的 Router 模块会负责模块的加载、组件的初始化、销毁等操作，它是整个乐队的总指挥。</strong></p>
<h3 id="">前端为什么要路由</h3>
<p>我发现很多开发者代码写得很溜，但是并不理解为什么要 Router 这个机制。</p>
<p>在目前的前端开发领域，无论你使用哪一种框架，“路由”都是一个绕不开的机制。那么，前端为什么一定要路由机制？举两个简单的例子来帮助理解。</p>
<ul>
<li>如果没有 Router，浏览器的前进后退按钮没法用。做过后台管理系统的开发者应该遇到过这种场景，整个系统只有一个 login.jsp 和 index.jsp，用户从 login.jsp 登录完成之后，跳转到 index.jsp 上面，然后浏览器地址栏里面的 URL 就一直停留在 index.jsp 上面，页面内部的所有内容全部通过 Ajax 进行刷新。这种处理方式实际上把浏览器的 URL 机制给废掉了，整个系统只有一个 URL，用户完全无法通过浏览器的前进、后退按钮进行导航。</li>
<li>如果没有 Router，你将无法把 URL 复制并分享给你的朋友。比如，在某段子网站上看到了一个很搞笑的内容，你把 URL 复制下来分享给了你的朋友，如果这个段子网站没有做好路由机制，你的朋友将无法顺利打开这个链接。</li>
</ul>
<p>Router 的本质是记录当前页面的状态，它和当前页面上展示的内容一一对应。</p>
<p>在 Angular 里面，Router 是一个独立的模块，定义在 @angular/router 模块里面，它有以下重要的作用：</p>
<ul>
<li>Router 可以配合 NgModule 进行模块的懒加载、预加载操作；</li>
<li>Router 会管理组件的生命周期，它会负责创建、销毁组件。</li>
</ul>
<h3 id="-1">服务端的配置</h3>
<p>很多开发者会遇到这个问题：代码在开发状态运行得好好的，但是部署到真实的环境上之后所有路由都 404。</p>
<p>这是一个非常典型的问题，你需要配置一下 Server 才能很好地支持前端路由。</p>
<p>你想啊，既然启用了前端路由，也就意味着浏览器地址栏里面的那些 URL 在 Server 端并没有真正的资源和它对应，直接访问过去当然 404 了。</p>
<p>以 Tomcat 为例，需要在 web.xml 里面加一段配置：</p>
<pre>
&lt;error-page&gt;
    &lt;error-code&gt;404&lt;/error-code&gt;
    &lt;location&gt;/&lt;/location&gt;
&lt;/error-page&gt;
</pre>
<p>这意思就是告诉 Tomcat，对于 404 这种事你别管了，直接扔回前端去。由于 Angular 已经在浏览器里面接管了路由机制，因而接下来就由 Angular 来负责了。</p>
<p>如果你正在使用其他的 Web 容器，<a href="https://github.com/angular-ui/ui-router/wiki/Frequently-Asked-Questions">请从这个链接里面查找对应的配置方式</a>，在
How to: Configure your server to work with html5Mode 这个小节里面把常见的 Web 容器的配置方式都列举出来了，包括 IIS、Apache、Nginx、NodeJS、Tomcat 全部都有，过去抄过来就行。</p>
<h3 id="-2">小结</h3>
<p>Angular 新版本的路由机制极其强大，除了能支持无限嵌套之外，还能支持模块懒加载、预加载、权限控制、辅助路由等高级功能，在接下来的几个课里面我们就来写例子一一演示。</p>
<p>Angular Router 模块的作者是 Victor Savkin，<a href="https://vsavkin.com/">他的个人 Blog 请单击这里</a>，他专门编写了一本小薄书来完整描述 Angular 路由模块的设计思路和运行原理，这本书只有 151 页，<a href="https://leanpub.com/router">如果有兴趣请点这里查看</a>。</p></div></article>