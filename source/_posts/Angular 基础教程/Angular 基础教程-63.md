---
title: Angular 基础教程-63
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我看到了一些观点，一些开发者认为 Angular 的组件设计不如 Polymer 那种直接继承原生 HTMLElement 的方式优雅。</p>
<p>以下是 Polymer 组件的定义方式：</p>
<p><img src="https://images.gitbook.cn/ff20b1f0-eca2-11e8-a56e-b14ca1e28a87"  width = "70%" /></p>
<p>以下是 Polymer 的根类 Polymer.Element 的源代码：</p>
<p><img src="https://images.gitbook.cn/126feeb0-eca3-11e8-a56e-b14ca1e28a87"  width = "60%" /></p>
<p>可以看到，在 Polymer 中，开发者自定义标签的地位与浏览器原生标签完全是平等的，属性、事件、行为，都是平等的，Polymer 组件的渲染由浏览器内核直接完成。</p>
<p>Polymer 的这种封装方式和目前市面上的大部分前端框架都不一样，Polymer 直接继承原生 HTML 元素，而其他大部分框架都只是在“包装”、“装饰”原生 HTML 元素，这是两种完全不同的设计哲学。</p>
<p><a href="https://www.polymer-project.org/">Polymer Project 的网址，点击这里查看</a>。</p></div></article>