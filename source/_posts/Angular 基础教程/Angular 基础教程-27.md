---
title: Angular 基础教程-27
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Angular 是第一个把“双向数据绑定”机制引入到前端开发领域来的框架，这也是当年 AngularJS 最受开发者欢迎的特性。</p>
<p>我们接着上一个例子继续改，先看运行效果：</p>
<p><img width="70%" src="https://images.gitbook.cn/0e441a00-b8e0-11e9-8b62-c350e3466c22"></p>
<p>HTML 模版里面的核心代码：</p>
<pre><code>&lt;input type="email" class="form-control" placeholder="Email" [(ngModel)]="regModel.userName" name="userName"&gt;

&lt;input type="password" class="form-control" placeholder="Password" [(ngModel)]="regModel.password" name="password"&gt;

&lt;input type="checkbox" name="rememberMe" [(ngModel)]="regModel.rememberMe"&gt;记住我
</code></pre>
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
<li>要想使用 [(ngModel)] 进行双向绑定，必须在你的 @NgModule 定义里面 import FormsModule 模块。</li>
<li>用双向绑定的时候，必须给 <code>&lt;input&gt;</code> 标签设置 name 或者 id，否则会报错。（这个行为挺奇怪的，吐槽一下！）</li>
<li>表单上面展现的字段和你处理业务用的数据模型不一定完全一致，推荐设计两个 Model，一个用来给表单进行绑定操作，一个用来处理你的业务。</li>
</ul>
<p>这个例子完整可运行的代码参见：<a href="https://gitee.com/learn-angular-series/learn-form">https://gitee.com/learn-angular-series/learn-form</a>，在 two-way-data-binding 分支上。</p></div></article>