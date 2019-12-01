---
title: Angular 基础教程-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">组件与指令之间的关系</h3>
<p><img width="60%" src="https://images.gitbook.cn/03315710-b8d9-11e9-a88b-c93a5ea3d618"></p>
<p>再看一下核心源代码里面的内容：</p>
<p><img width="60%" src="https://images.gitbook.cn/0b879640-b8d9-11e9-a194-19c3d4002b01"></p>
<p>根据 Angular 官方文档的描述，Angular 里面有 3 种类类型的指令：</p>
<ul>
<li>Component 是 Directive 的子接口，是一种特殊的指令，Component 可以带有 HTML 模板，Directive 不能有模板。</li>
<li>属性型指令：用来修改 DOM 元素的外观和行为，但是不会改变 DOM 结构，Angular 内置指令里面典型的属性型指令有 ngClass、ngStyle。如果你打算封装自己的组件库，属性型指令是必备的内容。</li>
<li>结构型指令：可以修改 DOM 结构，内置的常用结构型指令有 *ngFor、*ngIf 和 NgSwitch。由于结构型指令会修改 DOM 结构，所以同一个 HTML 标签上面不能同时使用多个结构型指令，否则大家都来改 DOM 结构，到底听谁的呢？如果要在同一个 HTML 元素上面使用多个结构性指令，可以考虑加一层空的元素来嵌套，比如在外面套一层空的 <code>&lt;ng-container&gt;&lt;/ng-container&gt;</code>，或者套一层空的 <code>&lt;div&gt;</code>。</li>
</ul>
<h3 id="-1">有了组件为什么还要指令？</h3>
<p>请注意：即使你认真、仔细地看完以上内容，你依然会感到非常茫然。因为有一个最根本的问题在所有文档里面都没有给出明确的解释，这个问题也是很多开发者经常来问我的，那就是：<strong>既然有了组件（Component），为什么还要指令（Directive）？</strong></p>
<p>我们知道，在很多的 UI 框架里面，并没有指令的概念，它们的基类都是从 Component 开始的。比如：</p>
<ul>
<li>Swing 里面基类名字就叫 Component，没有指令的概念</li>
<li>ExtJS 里面基类是 Ext.Component，没有指令的概念</li>
<li>Flex 里面基类名字叫 UIComponent，没有指令的概念</li>
<li>React 里面的基类名字叫 React.Component，没有指令的概念</li>
</ul>
<p>以下是 Swing 的类结构图：</p>
<p><img width="70%" src="https://images.gitbook.cn/9c1a8af0-b8d9-11e9-a194-19c3d4002b01"></p>
<p>以下是 ExtJS 3.2 的 UI 组件继承结构图局部，请注意 Ext.Component 类的位置：</p>
<p><img width="80%" src="https://images.gitbook.cn/a953db90-b8d9-11e9-8b62-c350e3466c22"></p>
<p>下面是整体缩略图：</p>
<p><img width="80%" src="https://images.gitbook.cn/b0ecbe30-b8d9-11e9-8b62-c350e3466c22"></p>
<p>以下是Adobe Flex 3的类结构图：</p>
<p><img width="100%" src="https://images.gitbook.cn/b7bb4bf0-b8d9-11e9-a194-19c3d4002b01"></p>
<p>上面这些框架都走的组件化的路子，Swing 和 ExtJS 完全是“代码流”，所有 UI 都通过代码来创建；而 Flex 和 React 是“标签流”，也就通过标签的方式来创建 UI。</p>
<p>但是，所有这些框架都没有“指令”这个概念，为什么 Angular 里面一定要引入“指令”这个概念呢？</p>
<p><strong>根本原因是：我们需要用指令来增强标签的功能，包括 HTML 原生标签和你自己自定义的标签。</strong></p>
<p>举例来说：<code>&lt;div&gt;</code> 是一个常用的原生 HTML 标签，但是请不要小看它，它上面实际上有非常多的属性，这些属性都是 W3C 规范规定好的。</p>
<p><img width="100%" src="https://images.gitbook.cn/f63d5760-b8d9-11e9-ba33-51636d56aead"></p>
<p>还能支持以下事件属性：</p>
<p><img width="100%" src="https://images.gitbook.cn/fffc0030-b8d9-11e9-a194-19c3d4002b01"></p>
<p>完整的列表请查看 W3C 规范：</p>
<blockquote>
  <p><a href="https://www.w3schools.com/tags/ref_standardattributes.asp">https://www.w3schools.com/tags/ref_standardattributes.asp</a></p>
</blockquote>
<p><strong>但是，这些内置属性还不够用，你想给原生的 HTML 标签再扩展一些属性。比方说：你想给 <code>&lt;div&gt;</code> 标签增加一个自定义的属性叫做 my-high-light，当鼠标进入 div 内部时，div 的背景就会高亮显示，可以这样使用 <code>&lt;div my-high-light&gt;</code>。这时候，没有指令机制就无法实现了。</strong></p></div></article>