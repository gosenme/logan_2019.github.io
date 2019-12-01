---
title: Angular 基础教程-87
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="optional">@Optional 基本用法</h3>
<p>我们在 ChildComponent 的构造函数里面加上 @Optional 装饰器进行装饰：</p>
<p><img src="http://images.gitbook.cn/bf936510-1dee-11e8-88a7-2d09138d19c0"  width = "60%" /></p>
<p>然后父组件 UserListComponent 里面清空，啥也没有：</p>
<p><img src="http://images.gitbook.cn/c5150070-1dee-11e8-a839-ebbde16a4ab7"  width = "60%" /></p>
<p>当然，NgModule 里面也不声明 UserListService。</p>
<p>注射器看到 @Optional 装饰器之后就知道这个服务是可选的，处理逻辑如下：</p>
<ul>
<li>沿着 Injector Tree 向上找一遍，如果找到了需要注入的类型，就创建实例；</li>
<li>如果啥都没找到，直接赋值为 null，<strong>不抛异常</strong>。</li>
</ul>
<h3 id="selfoptional">@Self 与 @Optional 组合使用</h3>
<p><strong>注意：组合使用的方式在官方文档里面没有详细说明，请对照例子仔细理解一下。</strong></p>
<p>装饰器是可以组合使用的，因此 ChildComponent 的构造函数里面可以写成这样：</p>
<pre><code>constructor(
    @Self() @Optional() public userListService:UserListService
) { }
</code></pre>
<p>这种用法的含义是：</p>
<ul>
<li>因为 @Self 装饰器限定了查找范围，所以只在 ChildComponent 自身内部进行查找，父层组件有没有定义对应的服务，不会产生任何影响；</li>
<li>因为有 @Optional 装饰器，所以如果 ChildComponent 自身内部提供了对应的服务，就创建实例，否则就直接赋值为 null，不抛异常。</li>
</ul>
<p>怎么样，挺清晰的对吧？</p>
<p>读者还可以自己测试一下更复杂的玩法，组合使用 3 个以上的装饰器看看。</p>
<h3 id="">参考资源</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-dependency-injection">本节课的实例代码请单击这里下载</a>，在 optional-decorator 分支上。</p></div></article>