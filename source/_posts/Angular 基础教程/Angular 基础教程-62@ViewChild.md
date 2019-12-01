---
title: Angular 基础教程-62
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="viewchild">@ViewChild</h3>
<p>我们可以利用 @ViewChild 这个装饰器来操控直属的子组件。</p>
<pre>
&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;父组件&lt;/div&gt;
  &lt;div class="panel-body"&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
  &lt;/div&gt;
&lt;/div&gt;
</pre>
<pre><code>import { Component, OnInit, ViewChild, ViewChildren, QueryList } from '@angular/core';

@ViewChild(ChildOneComponent)
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
<h3 id="viewchildren">@ViewChildren</h3>
<pre>
&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;父组件&lt;/div&gt;
  &lt;div class="panel-body"&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
    &lt;child-one&gt;&lt;/child-one&gt;
  &lt;/div&gt;
&lt;/div&gt;
</pre>
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
<p><a href="https://gitee.com/learn-angular-series/learn-component">本课对应的完整实例代码请点击这里下载</a>，代码在 viewchild 这个分支上面。</p></div></article>