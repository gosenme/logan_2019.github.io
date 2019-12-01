---
title: Angular 基础教程-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="viewchild">@ViewChild</h3>
<p>我们可以利用 @ViewChild 这个装饰器来操控直属的子组件。</p>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;父组件&lt;/div&gt;
  &lt;div class="panel-body"&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<pre><code>import { Component, OnInit, ViewChild, ViewChildren, QueryList } from '@angular/core';

@ViewChild(ChildOneComponent,{static:false})
childOne:ChildOneComponent;

//在 ngAfterViewInit 这个钩子里面可以直接访问子组件
ngAfterViewInit():void{
    console.log(this.childOne);
    //用代码的方式订阅子组件上的事件
    this.childOne.helloEvent.subscribe((param)=&gt;{
        console.log(this.childOne.title);
    });
}
</code></pre>
<p><strong>注意：8.0 这里有一个 breaking change，@ViewChild 这里提供了第二个参数，增强了一些功能。这里有详细的描述：<a href="https://angular.io/api/core/ViewChild">https://angular.io/api/core/ViewChild</a>。</strong></p>
<h3 id="viewchildren">@ViewChildren</h3>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;父组件&lt;/div&gt;
  &lt;div class="panel-body"&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<pre><code>import { Component, OnInit, ViewChild, ViewChildren, QueryList } from '@angular/core';

@ViewChildren(ChildOneComponent)
children:QueryList&lt;ChildOneComponent&gt;;

ngAfterViewInit():void{
    this.children.forEach((item)=&gt;{
        // console.log(item);
        //动态监听子组件的事件
        item.helloEvent.subscribe((data)=&gt;{
        console.log(data);
        });
    });
}
</code></pre>
<h3 id="">小结</h3>
<p>本节对应的完整实例代码请参见这里：<a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，代码在 viewchild 这个分支上面。</p>
<h3 id="-1">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>