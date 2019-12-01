---
title: Angular 基础教程-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我看到了一些观点，一些开发者认为 Angular 的组件设计不如 Polymer 那种直接继承原生 HTMLElement 的方式优雅。</p>
<p>以下是 Polymer 组件的定义方式：</p>
<p><img width="70%" src="https://images.gitbook.cn/3e6533d0-b8d7-11e9-a88b-c93a5ea3d618"></p>
<p>以下是 Polymer 的根类 Polymer.Element 的源代码：</p>
<p><img width="60%" src="https://images.gitbook.cn/4d5de7b0-b8d7-11e9-a194-19c3d4002b01"></p>
<p>可以看到，在 Polymer 中，开发者自定义标签的地位与浏览器原生标签完全是平等的，属性、事件、行为，都是平等的，Polymer 组件的渲染由浏览器内核直接完成。</p>
<p>Polymer 的这种封装方式和目前市面上的大部分前端框架都不一样，Polymer 直接继承原生 HTML 元素，而其它大部分框架都只是在“包装”、“装饰”原生 HTML 元素，这是两种完全不同的设计哲学。</p>
<blockquote>
  <p><a href="https://www.polymer-project.org/">https://www.polymer-project.org/</a></p>
</blockquote>
<p>目前，使用 Polymer 最著名的网站是 Google 自家的 YouTube：</p>
<p><img width="75%" src="https://images.gitbook.cn/d088b390-b8d7-11e9-a88b-c93a5ea3d618"></p>
<h3 id="">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>