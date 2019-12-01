---
title: Angular 基础教程-59
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>根据 Angular 官方的说法，Angular 组件的设计灵感来源于 Web Component，在 Web Component 里面，ShadowDOM 是重要的组成部分。在底层，Angular 渲染组件的方式有以下三种。</p>
<ul>
<li>Native：采用 ShadowDOM 的模式来进行渲染。</li>
<li>Emulated：模拟模式。对于不能支持 ShadowDOM 模式的浏览器，Angular 在底层会采用模拟的方式来渲染组件，<strong>这是 Angular 默认的渲染模式</strong>。</li>
<li>None：不采用任何渲染模式。直接把组件的 HTML 结构和 CSS 样式插入到 DOM 流里面，这种方式很容易导致组件互相之间出现 CSS 命名污染的问题。</li>
</ul>
<p>在定义组件的时候，可以通过 encapsulation 配置项手动指定组件的渲染模式，关键代码如下：</p>
<pre><code>@Component({
  selector: 'emulate-mode',
  encapsulation:ViewEncapsulation.Emulated,//默认模式
  templateUrl: './emulate-mode.component.html',
  styleUrls: ['./emulate-mode.component.scss']
})
</code></pre>
<p>请自己尝试修改 encapsulation 这个配置项来测试不同的效果。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-component">完整实例代码请单击这里下载</a>，代码在 shadowdom 这个分支上面。</p>
<p>案例运行后的效果如下：</p>
<p><img src="https://images.gitbook.cn/665e3e40-e402-11e8-a1c4-731a3e37324c"  width = "60%" /></p>
<p>有以下几个注意点。</p>
<ul>
<li>ShadowDOM 模式的封装性更好，运行效率也更高。</li>
<li>ShadowDOM 在 W3C 的状态是 Working Draft（2017-09-22），如果想深入研究请参考<a href="https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM">链接 1</a>、<a href="https://www.w3.org/TR/shadow-dom/">链接 2</a>。</li>
<li>ShadowDOM 目前只有 Chrome 和 Opera 支持得非常好，其他浏览器都非常糟糕：</li>
</ul>
<p><img src="https://images.gitbook.cn/769c9180-e402-11e8-8e04-b95633cc2286" alt="enter image description here" /></p>
<ul>
<li>一般来说，不需要自己手动指定组件的渲染模式，除非你自己知道在做什么。</li>
</ul></div></article>