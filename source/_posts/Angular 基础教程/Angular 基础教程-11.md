---
title: Angular 基础教程-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>根据 Angular 官方的说法，Angular 组件的设计灵感来源于 Web Component，在 Web Component 里面，ShadowDOM 是重要的组成部分。在底层，Angular 渲染组件的方式有 3 种：</p>
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
<p><strong>注意：Angular 官方在 2018 年的 NGConnet 大会上表示，在将来的某个版本中，会在内核里面把 ShadowDOM 设置为默认模式。因为这一变更会在内核层面进行，所以业务开发者不用改代码。</strong></p>
<p>本节对应的完整实例代码请参见这里：<a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，代码在 shadowdom 这个分支上面。</p>
<p>本节案例运行起来的效果如下：</p>
<p><img width="80%" src="https://images.gitbook.cn/af07c3d0-b8d4-11e9-a88b-c93a5ea3d618"></p>
<p>注意点：</p>
<ul>
<li>ShadowDOM 模式的封装性更好，运行效率也更高。</li>
<li>ShadowDOM 在 W3C 的状态是 Working Draft（2017-09-22），如果你想深入研究参考以下链接：<a href="https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM">https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM</a>、<a href="https://www.w3.org/TR/shadow-dom/">https://www.w3.org/TR/shadow-dom/</a>。</li>
<li>ShadowDOM 目前只有 Chrome 和 Opera 支持得非常好，其它浏览器都非常糟糕：<img width="80%" src="https://images.gitbook.cn/e8043c40-b8d4-11e9-ba33-51636d56aead"></li>
<li>一般来说，你不需要自己手动指定组件的渲染模式，除非你自己知道在做什么。</li>
</ul>
<h3 id="">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>