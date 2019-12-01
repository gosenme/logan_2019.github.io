---
title: Angular 基础教程-58
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我们可以通过标签的方式使用组件，也可以通过代码的方式来动态创建组件。动态创建组件的过程是通过 ViewContainerRef 和 ComponentFactoryResolver 这两个工具类来配合完成的。</p>
<p>我们可以定义一个这样的模板：</p>
<pre>
&lt;div #dyncomp&gt;&lt;/div&gt;
</pre>
<p>在组件定义里面需要首先 import 需要用到的工具类：</p>
<pre>
import { Component, OnInit,ViewChild,ViewContainerRef,ComponentFactoryResolver, ComponentRef } from '@angular/core';
</pre>
<p>组件内部这样写：</p>
<pre><code>//这里引用模板里面定义的 dyncomp 容器标签
@ViewChild("dyncomp",{read:ViewContainerRef})
dyncomp:ViewContainerRef;

comp1:ComponentRef&lt;Child11Component&gt;;
comp2:ComponentRef&lt;Child11Component&gt;;

constructor(private resolver:ComponentFactoryResolver) {
}
</code></pre>
<p>然后就可以在 ngAfterContentInit 这个钩子里面用代码来动态创建组件了：</p>
<pre>
ngAfterContentInit(){
    const childComp=this.resolver.resolveComponentFactory(Child11Component);
    this.comp1=this.dyncomp.createComponent(childComp); 
}
</pre>
<p>对于创建出来的 comp1 这个组件，可以通过代码直接访问它的 public 型属性，也可以通过代码来 subscribe（订阅）comp 1 上面发出来的事件，就像这样：</p>
<pre>
this.comp1.instance.title="父层设置的新标题";
this.comp1.instance.btnClick.subscribe((param)=>{
    console.log("--->"+param);
});
</pre>
<p>对于用代码动态创建出来的组件，我们可以通过调用 destory() 方法来手动销毁：</p>
<pre>
public destoryChild():void{
    this.comp1.destroy();
    this.comp2.destroy();
}
</pre>
<p><a href="https://gitee.com/learn-angular-series/learn-component">完整实例代码请单击这里</a>，代码在 dynamic-component 这个分支上面。</p>
<p>代码运行起来的效果如下：</p>
<p><img src="https://images.gitbook.cn/aeebebf0-e400-11e8-bfed-8d6b896efba7"  width = "70%" /></p>
<p><strong>注意：用代码动态创建组件这种方式在一般的业务开发里面不常用，而且可能存在一些隐藏的坑，如果你一定要用，请小心避雷。</strong></p></div></article>