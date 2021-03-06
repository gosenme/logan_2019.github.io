---
title: Angular 基础教程-78
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>有这样一种业务场景：表单里面的输入项不是固定的，需要根据服务端返回的数据动态进行创建。</p>
<p>这时候我们压根没法把表单的 HTML 模板写死，需要根据配置项用代码动态构建表单，而这些配置项甚至可能是在服务端动态生成的。</p>
<p>在 NiceFish 里面有一个实际的例子，运行效果如下：</p>
<p><img width="70%" src="https://images.gitbook.cn/73243190-f382-11e8-aeb7-01d6aed3aa05"></p>
<p>我们把创建表单相关的逻辑全部移到了组件里面：</p>
<p><img width="35%" src="https://images.gitbook.cn/85fcdec0-f382-11e8-8426-b15c0859cf17"></p>
<p>HTML 模板变得非常简单：</p>
<p><img width="60%" src="https://images.gitbook.cn/9baa08b0-f382-11e8-8426-b15c0859cf17"></p>
<p>这个例子代码量比较大，这里不贴代码，<a href="https://gitee.com/mumu-osc/NiceFish">完整可运行的例子请参见这里</a>，代码在 user-profile.component.ts 里面。</p></div></article>