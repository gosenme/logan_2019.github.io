---
title: Angular 基础教程-31
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在组件的构造函数里面声明，Angular 会在运行时自动把 Service 实例创建出来并注射给组件：</p>
<p><img width="60%" src="https://images.gitbook.cn/873cebf0-cce3-11e9-8d89-4fa271cb1633"></p>
<h3 id="">单例模式</h3>
<p>如果你希望 Service 是全局单例的，需要把它定义到根模块里面。</p>
<p><img width="70%" src="https://images.gitbook.cn/991910b0-cce3-11e9-9a11-bbb3551196dc"></p>
<h3 id="-1">多实例模式</h3>
<p>下面这个例子用来测试 UserListService 是否是单例，第一个组件会向 UserListService 里面塞数据，第二个组件会尝试去读取数据：</p>
<p><img width="70%" src="https://images.gitbook.cn/bf4196e0-cce3-11e9-8d89-4fa271cb1633"></p>
<p>核心代码如下：</p>
<pre><code>&lt;pre&gt;
@Component({
  selector: 'order-list',
  templateUrl: './order-list.component.html',
  styleUrls: ['./order-list.component.scss'],
  providers: [UserListService] //如果你在这里提供了 providers 配置，UserListService 就不是全局单例了
})
&lt;/pre&gt;
</code></pre>
<p>从运行结果可以看出来，因为我们在组件内部的 providers 里面也配置了一个 UserListService，很明显就不是同一个实例了。</p>
<h3 id="-2">简单解释一下原理</h3>
<p>在新版本的 Angular 里面，每个组件上都有自己的注射器（Injector）实例，所以很明显，注射器也构成了一个树形的结构。</p>
<p><img width="50%" src="https://images.gitbook.cn/e4e49960-cce3-11e9-8d89-4fa271cb1633"></p>
<p>我们的 UserListService 是通过依赖注入机制注射给组件的，DI 机制会根据以下顺序查找服务实例：</p>
<ul>
<li>如果组件内部的 providers 上面配置了服务，优先使用组件上的配置。</li>
<li>否则继续向父层组件继续查找。</li>
<li>直到查询到模块里面的 providers 配置。</li>
<li>如果没有找到指定的服务，抛异常。</li>
</ul>
<p>所以请特别注意：</p>
<ul>
<li>在 Component 里面直接引入 Service，就不是单例了，而是会为每个组件实例都创建一个单独的 Service 单例。</li>
<li>如果你在多个模块（@NgModule）里面同时定义 providers，那也不是单例。</li>
<li>如果你在异步加载的模块里面定义 Service，那也不是全局单例的，因为 Angular 会为异步模块创建独立的 Injector 空间。</li>
</ul>
<h3 id="service">关于 Service 的基本注意点</h3>
<p>有很多朋友说：OK，我会写 Service 了，也知道怎么玩注入了，但还有一个最基本的问题没有解决，那就是应该把什么样的东西做成服务？</p>
<p>整体上说，Angular 里面的 Service 与后端框架里面的 Service 设计思想是一致的：</p>
<ul>
<li>Service 应该是无状态的。</li>
<li>Service 应该可以被很多组件复用，不应该和任何组件紧密相关。</li>
<li>多个 Service 可以组合起来，实现更复杂的服务。</li>
</ul>
<p>在 Angular 核心包里面，最典型的一个服务就是 Htpp 服务。</p>
<blockquote>
  <p><a href="https://en.wikipedia.org/wiki/Service-oriented_architecture">https://en.wikipedia.org/wiki/Service-oriented_architecture</a></p>
</blockquote></div></article>