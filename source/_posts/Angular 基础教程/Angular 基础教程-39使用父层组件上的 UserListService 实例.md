---
title: Angular 基础教程-39
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="userlistservice">使用父层组件上的 UserListService 实例</h3>
<p>第一节里面说到，Injector 会构成树形结构，就像这样：</p>
<p><img src="https://images.gitbook.cn/f6fd3200-d261-11e9-8d0f-6b56ebcd1907"></p>
<p>这就意味着，如果我们在父层组件里面定义了 UserListService，子层组件可以直接使用同一个实例。</p>
<p>我们继续前面的例子进行改造，给 UserListComponent 加一层子组件，组件名字就叫 ChildComponent，运行起来的界面效果是这样的：</p>
<p><img src="https://images.gitbook.cn/031f1f30-d262-11e9-b943-9d5bb2abdc80" width = "60%"></p>
<p>ChildComponent 里面没有配置 providers，代码如下：</p>
<p><img src="https://images.gitbook.cn/09ea0370-d262-11e9-84ba-0bd4ba7d7fb3" width = "70%"></p>
<p>父层的 UserListComponent 配置了 providers，代码如下：</p>
<p><img src="https://images.gitbook.cn/11356250-d262-11e9-84ba-0bd4ba7d7fb3" width = "70%"></p>
<p>Augury 图形化展示出来的依赖关系是这样的：</p>
<p><img src="https://images.gitbook.cn/172290c0-d262-11e9-bcae-b7c2737c8da6" width = "60%"></p>
<p>从运行效果可以看到：由于 ChildComponent 嵌套在 UserListComponent 内部，而且它自己没有配置 providers，所以它共享了父层的 UserListService 实例。</p>
<p>那么问题就来了，如果 ChildComponent 想要自己独立的 UserListService 实例，应该怎么做呢？</p>
<h3 id="self">@Self 装饰器</h3>
<p>我们可以利用 @Self 装饰器来提示注射器，不要向上查找，只在组件自身内部查找依赖。</p>
<p>我们给 ChildComponent 内部的 UserListService 声明加上@Self 装饰器：</p>
<p><img src="https://images.gitbook.cn/22b647b0-d262-11e9-b943-9d5bb2abdc80" width = "60%"></p>
<p>然后当然就报错啦：</p>
<p><img src="https://images.gitbook.cn/28f6ed50-d262-11e9-84ba-0bd4ba7d7fb3"></p>
<p>很好理解对吧，我们用 @Self 装饰器把查找依赖的范围限定在 ChildComponent 组件自身内部，但是 ChildComponent 自己并没有配置 UserListService，当然就找不到了。</p>
<p>所以，我们要在 ChildComponent 组件内部补上 providers 配置项：</p>
<p><img src="https://images.gitbook.cn/32c107d0-d262-11e9-8d0f-6b56ebcd1907" width = "60%"></p>
<p>然后从运行结果可以看到，父层和子层已经是不同的 UserListService 实例了：</p>
<p><img src="https://images.gitbook.cn/391890d0-d262-11e9-bcae-b7c2737c8da6" width = "60%"></p>
<p>Augury 图形化展示出来的依赖关系是这样的：</p>
<p><img src="https://images.gitbook.cn/3ec3fb50-d262-11e9-84ba-0bd4ba7d7fb3" width = "75%"></p>
<p>顺便说一句：很多初学者遇到异常的时候不仔细看堆栈，碰到问题就在群里叫，然后被人鄙视。</p>
<p><strong>像这种“No provider for...”基本上都是因为缺了 providers 配置项导致的，老司机扫一眼就懂，并不需要 Debug，也不需要查文档，知道为什么别人打代码速度辣么快了吧？</strong></p>
<p><img src="https://images.gitbook.cn/584c3c90-d262-11e9-8d0f-6b56ebcd1907" width = "50%"></p>
<h3 id="">参考资源</h3>
<p>本节实例代码都在这里：<a href="https://gitee.com/learn-angular-series/learn-dependency-injection">https://gitee.com/learn-angular-series/learn-dependency-injection</a>，在 self-decorator 分支上。</p></div></article>