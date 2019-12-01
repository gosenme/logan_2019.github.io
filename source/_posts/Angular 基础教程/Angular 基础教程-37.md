---
title: Angular 基础教程-37
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Angular 的依赖注入机制很强大，这一节我们玩儿三种最典型的场景：</p>
<ul>
<li>全局单例模式的 Service</li>
<li>多实例模式的 Service</li>
<li>异步模块上的 Service</li>
</ul>
<h3 id="">全局单例模式</h3>
<p>我们有一个 UserListComponent，它会利用 UserListService 来加载数据，写法如下。</p>
<p>在 UserListComponent 的构造函数里声明 UserListService：</p>
<p><img src="https://images.gitbook.cn/94de49c0-d260-11e9-84ba-0bd4ba7d7fb3"></p>
<p>编写 UserListService 的具体实现：</p>
<p><img src="https://images.gitbook.cn/9bd239d0-d260-11e9-b943-9d5bb2abdc80"></p>
<p>在根模块 AppModule 的 providers 里面配置 UserListService：</p>
<p><img src="https://images.gitbook.cn/a454e030-d260-11e9-bcae-b7c2737c8da6"></p>
<p>运行起来的效果是这样的：</p>
<p><img src="https://images.gitbook.cn/ab05acc0-d260-11e9-84ba-0bd4ba7d7fb3"></p>
<p>再看一下以上代码，你没有直接 new UserListService 对不对？很明显，Angular 在运行时自动帮你创建了 Service 的实例。</p>
<p>OK，看起来不错，但是如何证明这个 Service 是全局单例呢？</p>
<p>我们在界面上再放一个 UserListComponent 的实例，然后把 UserListService 的 id 打印出来看是否相同，就像这样：</p>
<p><img src="https://images.gitbook.cn/b5fbc420-d260-11e9-84ba-0bd4ba7d7fb3"></p>
<p>运行起来的效果是这样的：</p>
<p><img src="https://images.gitbook.cn/bd823030-d260-11e9-b943-9d5bb2abdc80"></p>
<p>可以看到，在两个 UserListComponent 实例中，使用的都是同一个 UserListService 实例。</p>
<p>这种全局单例模式很有用，你可以利用它来实现整个 App 范围内的数据共享。</p>
<p><strong>注意：在同步 NgModule 里面配置的 provider 在整个 App 范围内都是可见的，也就是说，即使你在某个子模块里面配置的 provider，它们依然是全局可见的，可以被注射到任意类里面。</strong></p>
<h3 id="-1">多实例模式</h3>
<p>有人会说，如果我想创建多个 UserListService 实例，怎么办？</p>
<p>我们把 UserListComponent 改成这样：</p>
<p><img src="https://images.gitbook.cn/cfba57a0-d260-11e9-b943-9d5bb2abdc80"></p>
<p>然后在界面上放两个实例：</p>
<p><img src="https://images.gitbook.cn/d69ae6c0-d260-11e9-bcae-b7c2737c8da6"></p>
<p>运行起来的效果是这样的：</p>
<p><img src="https://images.gitbook.cn/de0b0bb0-d260-11e9-b943-9d5bb2abdc80"></p>
<p>可以看到，如果把 UserListService 配置在 UserListComponent 内部的 providers 中，就不再是单例模式了，每个 UserListComponent 都拥有自己独立的 UserListService 实例。</p>
<p>组件内部的 provider 生命周期与组件自身保持一致，当组件被销毁的时候，它内部的 provider 也会被销毁掉。</p>
<h3 id="-2">异步模块上的注射器</h3>
<p>以上都是同步模块，对于懒加载进来的异步模块，注射器是一种什么样的结构呢？</p>
<p>我们来做一个复杂一点的例子，默认展示首页：</p>
<p><img src="https://images.gitbook.cn/ee57dde0-d260-11e9-bcae-b7c2737c8da6"></p>
<p>点击“用户列表”之后导航到 http://localhost:4200/userlist 展示用户列表：</p>
<p><img src="https://images.gitbook.cn/f5144330-d260-11e9-8d0f-6b56ebcd1907"></p>
<p>“用户列表”是一个异步模块，从 Chrome 的网络面板上可以看到这个模块是点击之后才加载进来的：</p>
<p><img src="https://images.gitbook.cn/fcafe4f0-d260-11e9-bcae-b7c2737c8da6"></p>
<p>用 Augury 展示 UserListService 实例的依赖关系：</p>
<p><img src="https://images.gitbook.cn/03b4c4f0-d261-11e9-b943-9d5bb2abdc80"></p>
<p><strong>注意：异步模块里面配置的 providers 只对本模块中的成员可见。如果你在其它模块里面引用异步模块里面配置的 provider，会产生异常。这里的本质原因是，Angular 会给异步加载的模块创建独立的注射器树。</strong></p>
<p>你可以自己尝试修改以上例子继续测试。</p>
<h3 id="-3">小结</h3>
<p>来总结一下这个注入机制，它的运行规则是这样的：</p>
<ul>
<li>如果组件内部配置了 providers，优先使用组件上的配置来创建注入对象。</li>
<li>否则向父层组件继续查找，父组件上找不到继续向所属的模块查找。</li>
<li>一直到查询到根模块 AppModule 里面的 providers 配置。</li>
<li>如果没有找到指定的服务，抛异常。</li>
<li>同步模块里面配置的 providers 是全局可见的，即使是很深的子模块里面配置的 providers，依然是全局可见的。</li>
<li><strong>异步模块里面配置的 providers 只对本模块中的成员可见。这里的本质是，Angular 会给异步加载的模块创建独立的注射器树。</strong></li>
<li>组件里面配置的 providers 对组件自身和所有子层组件可见。</li>
<li>注射器的生命周期与组件自身保持一致，当组件被销毁的时候，对应的注射器实例也会被销毁。</li>
</ul>
<p>简而言之，Angular 的 Injector Tree 机制与 JavaScript 的原型查找类似。对于日常的开发来说，知道这些已经足够，可以覆盖 90% 以上的业务场景了。</p>
<p>但是，既然这是一个针对 DI 的专题，我们当然要玩儿一些复杂的花样，请继续下一个小节。</p>
<h3 id="-4">参考资源</h3>
<ul>
<li>本节实例代码在这里：<a href="https://gitee.com/learn-angular-series/learn-dependency-injection">https://gitee.com/learn-angular-series/learn-dependency-injection</a>，两个例子分别在 singleton 分支和 async-module 分支上。</li>
<li><a href="http://es6.ruanyifeng.com/#docs/decorator">http://es6.ruanyifeng.com/#docs/decorator</a></li>
<li><a href="https://www.typescriptlang.org/docs/handbook/decorators.html">https://www.typescriptlang.org/docs/handbook/decorators.html</a></li>
</ul></div></article>