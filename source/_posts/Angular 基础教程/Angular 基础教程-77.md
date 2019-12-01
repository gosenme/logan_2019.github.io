---
title: Angular 基础教程-77
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面几个内容里面的例子都是“模板驱动型表单”，我们把表单相关的逻辑，包括校验逻辑全部写在模板里面，组件内部几乎没写什么代码。</p>
<p>表单的另一种写法是“模型驱动型表单”，又叫做“响应式表单”。特点是：把表单的创建、校验等逻辑全部用代码写到组件里面，让 HTML 模板变得很简单。</p>
<p><strong>特别注意：如果想使用响应式表单，必须在你的 @NgModule 定义里面 import ReactiveFormsModule。</strong></p>
<p>这里我们来一个复杂一些的表单，运行起来的效果如下：</p>
<p><img width="70%" src="https://images.gitbook.cn/f290d970-f381-11e8-aeb7-01d6aed3aa05"></p>
<p>这个例子代码量比较大，这里不贴代码，<a href="https://gitee.com/mumu-osc/NiceFish">完整可运行的例子请参见这里</a>，代码在 user-register.component.ts 里面。</p>
<p>如果你想查阅“响应式表单”的详细文档，<a href="https://angular.io/guide/reactive-forms">请参考这里</a>。</p></div></article>