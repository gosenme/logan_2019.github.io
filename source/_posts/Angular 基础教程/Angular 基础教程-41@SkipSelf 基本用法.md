---
title: Angular 基础教程-41
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="skipself">@SkipSelf 基本用法</h3>
<p>从名字可以猜出来它的含义：跳过组件自身，然后沿着 Injector Tree 向上查找。</p>
<p>继续在前面的例子上改造 ChildComponent，改成这样：</p>
<p><img src="https://images.gitbook.cn/e60caee0-d7c9-11e9-9143-0bdf45914741"></p>
<p>父组件是这样的：</p>
<p><img src="https://images.gitbook.cn/ec53e430-d7c9-11e9-8797-4924c0d7c082"></p>
<p>可以看到，我们在 ChildComponent 和它的父层组件 UserListComponent 上都配置了 UserListService。但是， ChildComponent 上有 @SkipSelf 装饰器，所以 ChildComponent 上的配置并没有起作用，使用的还是 UserListComponent 上的实例：</p>
<p><img src="https://images.gitbook.cn/f67f3180-d7c9-11e9-8fae-816b29059b0c"></p>
<h3 id="skipselfoptional">@SkipSelf 与 @Optional 组合使用</h3>
<p>同样，我们可以组合使用 @SkipSelf 与 @Optional：</p>
<pre><code>@SkipSelf() @Optional() public userListService: UserListService
</code></pre>
<p>这样写的含义是：</p>
<ul>
<li>因为使用了 @SkipSelf 装饰器，所以直接跳过 ChildComponent 组件自身，从 Injector Tree 的父层节点向上进行查找。也就是说，不管 ChildComponent 组件自己有没有配置 UserListService 都不起作用，因为跳过去了。</li>
<li>因为使用了 @Optional 装饰器，如果在父层上面找到了指定的类型，那就创建实例；否则，直接设置为 null，不抛异常。</li>
</ul>
<h3 id="">参考资源</h3>
<p>本节实例代码都在这里：<a href="https://gitee.com/learn-angular-series/learn-dependency-injection">https://gitee.com/learn-angular-series/learn-dependency-injection</a>，在 skipself-decorator 分支上。</p></div></article>