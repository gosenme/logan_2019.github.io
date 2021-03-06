---
title: Angular 基础教程-43
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p><strong>官方文档特别强调：开发者可以手动操作 Injector 的实例，但是这种情况非常罕见。</strong></p>
<p>所以那部分文档隐藏了一些黑魔法，这里我们自己揭开盖子来玩儿。</p>
<h3 id="injector">注入 Injector 实例</h3>
<p>我们继续在前面的例子上改进，来尝试手动操作 Injector 的实例：</p>
<p><img src="https://images.gitbook.cn/cdc041a0-d7cc-11e9-a536-c512dee3d564"></p>
<p>你可以自己用 Chrome 打开开发者工具看看 Injector 实例上面都有些什么属性：</p>
<p><img src="https://images.gitbook.cn/df6aa800-d7cc-11e9-a536-c512dee3d564"></p>
<p><strong>很明显，Injector 本身也是一个服务。</strong></p>
<h3 id="">手动创建注射器实例</h3>
<p>在上面的例子里面，Injector 实例是 Angular 帮我们自动创建的。如果我们自己创建注射器，可不可以呢？</p>
<p>当然是 OK 的，Angular 内核默认提供了 3 种 Injector 的实现，：</p>
<p><img src="https://images.gitbook.cn/f02704e0-d7cc-11e9-8fae-816b29059b0c"></p>
<ul>
<li>_NullInjector 是内部使用的私有类，外部无法引用。</li>
<li>StaticInjector 可以在外部使用，但是文档里面没有描述。</li>
<li>ReflectiveInjector，反射型注射器。如果你学过 Java 里面的反射机制，从 ReflectiveInjector 这个名字你可以猜测到它内部是怎么运行的。</li>
</ul>
<p>测试 Demo 的核心代码如下：</p>
<pre><code>import { Component, OnInit, Injector, ReflectiveInjector } from '@angular/core';
import { TestService } from './service/test.service';

ngOnInit() {
    //尝试自己手动创建 userListService 实例
    this.userListService=this.injector.get(UserListService);
    console.log(this.userListService);

    this.userListService.getUserList().subscribe((userList:Array&lt;any&gt;)=&gt;{
        this.userList=userList;
    });

    //尝试自己创建注射器，然后利用注射器自己注射 TestService 服务实例
    let myInjector = ReflectiveInjector.resolveAndCreate([
        { provide: "TestService", useClass: TestService }
    ]);

    console.log(myInjector);

    this.testService = myInjector.get("TestService");

    console.log(this.testService);
}
</code></pre>
<p>运行效果如下：</p>
<p><img src="https://images.gitbook.cn/034c9990-d7cd-11e9-8fae-816b29059b0c"></p>
<p>尝试自己创建注射器，然后利用注射器自己创建了 TestService 服务实例。</p>
<p><strong>注意：从 Angular 5.x 开始，ReflectiveInjector 被标记成了过时的，官方建议使用静态方法 Injector.create。</strong></p>
<h3 id="-1">参考资源</h3>
<p>本节实例代码都在这里：<a href="https://gitee.com/learn-angular-series/learn-dependency-injection">https://gitee.com/learn-angular-series/learn-dependency-injection</a>，在 injector-decorator 分支上。</p></div></article>