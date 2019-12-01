---
title: Angular 基础教程-74
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>如果没有表单，我们将没有途径收集用户输入，因此，表单是前端开发里面的重头戏，在日常开发中，处理表单将会占据大块的编码时间。</p>
<p>我们先来做一个最简单的用户注册界面：</p>
<p><img width="40%" src="https://images.gitbook.cn/7b7c7cf0-f31c-11e8-aa2b-0173053b4499"></p>
<p>HTML 模版里面的核心代码：</p>
<pre>
&lt;input type="email" class="form-control" placeholder="Email" (keyup)="userNameChange($event)"&gt;

&lt;input #pwd type="password" class="form-control" placeholder="Password" (keyup)="0"&gt;
</pre>
<p>组件核心代码：</p>
<pre><code>export class FormQuickStartComponent implements OnInit {
  public userName:string;

  public userNameChange(event):void{
    this.userName=event.target.value;
  }
}
</code></pre>
<p>这个例子非常简单，里面有两个 input，分别演示两种传递参数的方式。</p>
<ul>
<li>第一个 input：用事件绑定的方式，把 input 的值传递给组件内部定义的 userName 属性，然后页面上再用 {{userName}} 获取数据。</li>
<li>第二个 input：我们定义了一个模板局部变量 #pwd，然后底部直接用这个名字来获取 input 的值 {{pwd.value}}。这里有一个小小的注意点，标签里面必须写 (keyup)="0"，要不然 Angular 不会启动变更检测机制，{{pwd.value}} 取不到值。</li>
</ul>
<p><a href="https://gitee.com/learn-angular-series/learn-form">这个例子完整可运行的代码请单击这里下载</a>，在 quick-start 分支上。</p></div></article>