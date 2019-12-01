---
title: Angular 基础教程-75
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Angular 是第一个把“双向数据绑定”机制引入到前端开发领域来的框架，这也是当年AngularJS最受开发者欢迎的特性。</p>
<p>我们接着上一个例子继续改，先看运行效果：</p>
<p><img width="50%" src="https://images.gitbook.cn/a78a9b00-f31d-11e8-afda-792d363f612b"></p>
<p>HTML 模版里面的核心代码：</p>
<pre>
&lt;input type="email" class="form-control" placeholder="Email" [(ngModel)]="regModel.userName" name="userName"&gt;

&lt;input type="password" class="form-control" placeholder="Password" [(ngModel)]="regModel.password" name="password"&gt;

&lt;input type="checkbox" name="rememberMe" [(ngModel)]="regModel.rememberMe"&gt;记住我
</pre>
<p>数据模型和组件核心代码：</p>
<pre><code>export class RegisterModel {
    userName: string;
    password: string;
    rememberMe:boolean=false;
}
</code></pre>
<p>组件里面的核心代码：</p>
<pre><code>import { RegisterModel } from './model/register-model';

export class FormQuickStartComponent implements OnInit {
  public regModel:RegisterModel=new RegisterModel();
}
</code></pre>
<p>一些常见的坑：</p>
<ul>
<li>要想使用 [(ngModel)] 进行双向绑定，必须在你的 @NgModule 定义里面 import FormsModule 模块；</li>
<li>用双向绑定的时候，必须给 &lt;input&gt; 标签设置 name 或者 id，否则会报错（这个行为挺奇怪的，吐槽一下）。</li>
<li>表单上面展现的字段和你处理业务用的数据模型不一定完全一致，推荐设计两个 Model，一个用来给表单进行绑定操作，一个用来处理你的业务。</li>
</ul>
<p><a href="https://gitee.com/learn-angular-series/learn-form">这个例子完整可运行的代码请单击这里下载</a>，在 two-way-data-binding 分支上。</p></div></article>