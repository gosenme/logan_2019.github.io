---
title: Angular 基础教程-55
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课的主要内容：</p>
<ul>
<li>直接调用</li>
<li>@Input 和 @Output</li>
<li>利用 Service 单例进行通讯</li>
<li>利用 cookie 或者 localstorage 进行通讯</li>
<li>利用 Session 进行通讯</li>
</ul>
<p>组件就像零散的积木，我们需要把这些积木按照一定的规则拼装起来，而且要让它们之间能相互进行通讯，这样才能构成一个有机的完整系统。</p>
<p>在真实的应用中，组件最终会构成树形结构，就像人类社会中的家族树一样：</p>
<p><img src="https://images.gitbook.cn/03749550-e3e8-11e8-a1c4-731a3e37324c"  width = "50%" /></p>
<p>在树形结构里面，组件之间有几种典型的关系：父子关系、兄弟关系、没有直接关系。</p>
<p>相应地，组件之间也有以下几种典型的通讯方案：</p>
<ul>
<li>直接的父子关系，父组件直接访问子组件的 public 属性和方法</li>
<li>直接的父子关系，借助于 @Input 和 @Output 进行通讯</li>
<li>没有直接关系，借助于 Service 单例进行通讯</li>
<li>利用 cookie 和 localstorage 进行通讯</li>
<li>利用 Session 进行通讯</li>
</ul>
<p>无论使用什么前端框架，组件之间的通讯都离开不以上几种方案，这些方案与具体框架无关。</p>
<h3 id="">直接调用</h3>
<p>对于有直接父子关系的组件，父组件可以直接访问子组件里面 public 型的属性和方法，示例代码片段如下：</p>
<pre>
&lt;child #child&gt;&lt;/child&gt;
&lt;button (click)="child.childFn()" class="btn btn-success"&gt;调用子组件方法&lt;/button&gt;
</pre>
<p>显然，子组件里面必须暴露一个 public 型的 childFn 方法，就像这样：</p>
<pre>
public childFn():void{
    console.log("子组件的名字是>"+this.panelTitle);
}
</pre>
<p>以上是通过在模板里面定义局部变量的方式来直接调用子组件里面的 public 型方法。在父组件的内部也可以访问到子组件的实例，需要利用到 @ViewChild 装饰器，示例如下：</p>
<pre>
@ViewChild(ChildComponent)
private childComponent: ChildComponent;
</pre>
<p>关于 @ViewChild 在后面的内容里面将会有更加详细的解释。</p>
<p>很明显，如果父组件直接访问子组件，那么两个组件之间的关系就会被固定死了。父子两个组件紧密依赖，谁也离不开谁，也就说都不能单独的使用。因此，除非你知道自己在做什么，最好不要在父组件里面直接访问子组件上的属性和方法，以免未来一改一大片的 bug。</p>
<h3 id="inputoutput">@Input 和 @Output</h3>
<p>我们可以利用 @Input 装饰器，让父组件直接给子组件传递参数，子组件上这样写：</p>
<pre>
@Input()
public panelTitle:string;
</pre>
<p>父组件上可以这样设置 panelTitle 这个参数：</p>
<pre>
&lt;child panelTitle="一个新的标题"&gt;&lt;/child&gt;
</pre>
<p>@Output 的本质是事件机制，我们可以利用它来监听子组件上派发的事件，子组件上这样写：</p>
<pre>
@Output()
public follow=new EventEmitter<string>();
</pre>
<p>触发 follow 事件的方式如下：</p>
<pre>
this.follow.emit("follow");
</pre>
<p>父组件上可以这样监听 follow 事件：</p>
<pre>
&lt;child (follow)="doSomething()"&gt;&lt;/child&gt;
</pre>
<p>我们可以利用 @Output 来自定义事件，监听自定义事件的方式也是通过小圆括号，与监听 HTML 原生事件的方式一模一样。</p>
<h3 id="service">利用 Service 单例进行通讯</h3>
<p><img src="https://images.gitbook.cn/25d0d140-e3e8-11e8-8e04-b95633cc2286"  width = "70%" /></p>
<p>如果你在根模块（一般是 app.module.ts）的 providers 里面注册一个 Service，那么这个 Service 就是全局单例的，这样一来我们就可以利用这个单例的 Service 在不同的组件之间进行通讯了。</p>
<ul>
<li>比较粗暴的方式：我们可以在 Service 里面定义 public 型的共享变量，然后让不同的组件都来访问这块变量，从而达到共享数据的目的。</li>
<li>优雅一点的方式：利用 RxJS，在 Service 里面定义一个 public 型的 Subject（主题），然后让所有组件都来 Subscribe（订阅）这个主题，类似于一种“事件总线”的效果。</li>
</ul>
<p>实例代码片段如下：</p>
<pre>
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

/**
 * 用来充当事件总线的 Service
 */
@Injectable()
export class EventBusService {
  public eventBus:Subject<string> = new Subject<string>();

  constructor() { }

}
</pre>
<pre>
import { Component, OnInit } from '@angular/core';
import { EventBusService } from '../service/event-bus.service';

@Component({
  selector: 'child-1',
  templateUrl: './child-1.component.html',
  styleUrls: ['./child-1.component.css']
})
export class Child1Component implements OnInit {

  constructor(public eventBusService:EventBusService) { }

  ngOnInit() {
  }

  public triggerEventBus():void{
    this.eventBusService.eventBus.next("第一个组件触发的事件");
  }
}
</pre>
<pre>
import { Component, OnInit } from '@angular/core';
import { EventBusService } from '../service/event-bus.service';

@Component({
  selector: 'child-2',
  templateUrl: './child-2.component.html',
  styleUrls: ['./child-2.component.css']
})
export class Child2Component implements OnInit {
  public events:Array<any>=[];

  constructor(public eventBusService:EventBusService) {

  }

  ngOnInit() {
    this.eventBusService.eventBus.subscribe((value)=>{
      this.events.push(value+"-"+new Date());
    });
  }
}
</pre>
<h3 id="cookielocalstorage">利用 cookie 或者 localstorage 进行通讯</h3>
<p><img src="https://images.gitbook.cn/3a8fcaa0-e3e8-11e8-bfed-8d6b896efba7"  width = "70%" /></p>
<p>示例代码片段如下：</p>
<pre>
public writeData():void{
    window.localStorage.setItem("json",JSON.stringify({name:'大漠穷秋',age:18}));
}
</pre>
<pre>
var json=window.localStorage.getItem("json");
// window.localStorage.removeItem("json");
var obj=JSON.parse(json);
console.log(obj.name);
console.log(obj.age);
</pre>
<p><strong>很多朋友写 Angular 代码的时候出现了思维定势，总感觉 Angular 会封装所有东西，实际上并非如此，比如 cookie、localstorage 这些东西都可以直接用原生的 API 进行操作。千万别忘记原生的那些 API 啊，都能用的！</strong></p>
<h3 id="session">利用 Session 进行通讯</h3>
<p><img src="https://images.gitbook.cn/4b816850-e3e8-11e8-a1c4-731a3e37324c"  width = "70%" /></p>
<h3 id="-1">小结</h3>
<p>组件间的通讯方案是通用的，无论使用什么样的前端框架，都会面临这个问题，而解决的方案无外乎本课所列出的这几种。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-component">完整可运行的实例请点击这里下载</a>，请检出 communication 分支。</p></div></article>