---
title: Angular 基础教程-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我们可以通过标签的方式使用组件，也可以通过代码的方式来动态创建组件。动态创建组件的过程是通过 ViewContainerRef 和 ComponentFactoryResolver 这两个工具类来配合完成的。</p>
<p>我们可以定义一个这样的模板：</p>
<pre><code>&lt;div #dyncomp&gt;&lt;/div&gt;
</code></pre>
<p>在组件定义里面需要首先 import 需要用到的工具类：</p>
<pre><code>import { Component, OnInit,ViewChild,ViewContainerRef,ComponentFactoryResolver, ComponentRef } from '@angular/core';
</code></pre>
<p>组件内部这样写：</p>
<pre><code>//这里引用模板里面定义的 dyncomp 容器标签
@ViewChild("dyncomp",{read:ViewContainerRef})
dyncomp:ViewContainerRef;

comp1:ComponentRef&lt;Child11Component&gt;;
comp2:ComponentRef&lt;Child11Component&gt;;

constructor(private resolver:ComponentFactoryResolver) {
}
</code></pre>
<p>然后我们就可以在 ngAfterContentInit 这个钩子里面用代码来动态创建组件了：</p>
<pre><code>ngAfterContentInit(){
    const childComp=this.resolver.resolveComponentFactory(Child11Component);
    this.comp1=this.dyncomp.createComponent(childComp); 
}
</code></pre>
<p>对于创建出来的 comp1 这个组件，可以通过代码直接访问它的 public 型属性，也可以通过代码来 subscribe（订阅）comp1 上面发出来的事件，就像这样：</p>
<pre><code>this.comp1.instance.title="父层设置的新标题";
this.comp1.instance.btnClick.subscribe((param)=&gt;{
    console.log("---&gt;"+param);
});
</code></pre>
<p>对于用代码动态创建出来的组件，我们可以通过调用 destory() 方法来手动销毁：</p>
<pre><code>public destoryChild():void{
    this.comp1.destroy();
    this.comp2.destroy();
}
</code></pre>
<p>本节对应的完整实例代码请参见这里：<a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，代码在 dynamic-component 这个分支上面。</p>
<p>代码运行起来的效果如下：</p>
<p><img width="70%" src="https://images.gitbook.cn/fb944800-b8d3-11e9-a88b-c93a5ea3d618"></p>
<p><strong>注意：用代码动态创建组件这种方式在一般的业务开发里面不常用，而且可能存在一些隐藏的坑，如果你一定要用，请小心避雷。</strong></p>
<h3 id="">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>