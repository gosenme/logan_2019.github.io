---
title: Angular 基础教程-61
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="contentchild">@ContentChild</h3>
<p>我们可以利用 @ContentChild 这个装饰器来操控被投影进来的组件。</p>
<pre>
&lt;child-one&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
&lt;/child-one&gt;
</pre>
<pre><code>import { Component, ContentChild, ContentChildren, ElementRef, OnInit, QueryList } from '@angular/core';

//注解的写法
@ContentChild(ChildTwoComponent)
childTwo:ChildTwoComponent;

//在 ngAfterContentInit 钩子里面访问被投影进来的组件
ngAfterContentInit():void{
    console.log(this.childTwo);
    //这里还可以访问 this.childTwo 的 public 型方法，监听 this.childTwo 所派发出来的事件
}
</code></pre>
<h3 id="contentchildren">@ContentChildren</h3>
<p>从名字可以看出来，@ContentChildren 是一个复数形式。当被投影进来的是一个组件列表的时候，我们可以用 @ContentChildren 来进行操控。</p>
<pre>
&lt;child-one&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
    &lt;child-two&gt;&lt;/child-two&gt;
&lt;/child-one&gt;
</pre>
<pre>
import { Component, ContentChild, ContentChildren, ElementRef, OnInit, QueryList } from '@angular/core';

//这时候不是单个组件，是一个列表 QueryList
@ContentChildren(ChildTwoComponent) 
childrenTwo:QueryList<ChildTwoComponent>;

//遍历列表
ngAfterContentInit():void{
    this.childrenTwo.forEach((item)=>{
        console.log(item);
    });
}
</pre>
<p><a href="https://gitee.com/learn-angular-series/learn-component">本课对应的完整实例代码请点击这里下载</a>，代码在 contentchild 这个分支上面。</p></div></article>