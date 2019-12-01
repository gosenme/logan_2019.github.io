---
title: Angular 基础教程-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>到目前为止，在我们所有例子里面，界面结构都是这样的：</p>
<p><img width="60%" src="https://images.gitbook.cn/376e15d0-b8df-11e9-8b62-c350e3466c22"></p>
<p>但是，有时候我们在同一个界面上需要同时出现两块或者多块动态的内容。比如，你想让左侧的导航栏和右侧的主体区域全部变成动态的，就像这样：</p>
<p><img width="60%" src="https://images.gitbook.cn/3e101550-b8df-11e9-a88b-c93a5ea3d618"></p>
<p>核心代码如下：</p>
<p>app.component.html 里面的内容：</p>
<pre><code>&lt;a [routerLink]="['home', {outlets: {'left-nav': ['leftNav'], 'main-area': ['none']}}]"&gt;主页&lt;/a&gt;
</code></pre>
<p>home.component.html 里面的内容：</p>
<pre><code>&lt;div class="row"&gt;
  &lt;div class="col-xs-3"&gt;
    &lt;router-outlet name="left-nav"&gt;&lt;/router-outlet&gt;
  &lt;/div&gt;
  &lt;div class="col-xs-9"&gt;
    &lt;router-outlet name="main-area"&gt;&lt;/router-outlet&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>left-nav.component.html 里面的核心代码：</p>
<pre><code>&lt;a class="list-group-item" (click)="toogle(1)"&gt;只看图片&lt;/a&gt;
&lt;a class="list-group-item" (click)="toogle(2)"&gt;只看文字&lt;/a&gt;
</code></pre>
<p>left-nav.component.ts 里面的核心代码：</p>
<pre><code>toogle(id) {
    this.router.navigate(['/home', {outlets: {'main-area': [id]}}]);
}
</code></pre>
<p>运行效果：</p>
<p><img width="60%" src="https://images.gitbook.cn/92c51c80-b8df-11e9-ba33-51636d56aead"></p>
<p>请注意看浏览器地址栏里面的内容，形式比较复杂，而且代码写起来也比较繁琐，所以，请尽量避开这种用法。</p>
<p>完整可运行的例子在这里：<a href="https://gitee.com/learn-angular-series/learn-router">https://gitee.com/learn-angular-series/learn-router</a>，代码在 multi-outlet 分支上。</p></div></article>