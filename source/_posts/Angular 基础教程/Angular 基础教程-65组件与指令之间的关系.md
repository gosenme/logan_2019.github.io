---
title: Angular 基础教程-65
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">组件与指令之间的关系</h3>
<p><img src="https://images.gitbook.cn/6757f320-ecab-11e8-a56e-b14ca1e28a87"  width = "60%" /></p>
<p>再看一下核心源代码里面的内容：</p>
<p><img src="https://images.gitbook.cn/b59406a0-ecab-11e8-9a75-31990b0290b3"  width = "70%" /></p>
<p>根据 Angular 官方文档的描述，Angular 里面有 3 种类型的指令。</p>
<ul>
<li>Component 是 Directive 的子接口，是一种特殊的指令，Component 可以带有 HTML 模板，Directive 不能有模板。</li>
<li>属性型指令：用来修改 DOM 元素的外观和行为，但是不会改变 DOM 结构，Angular 内置指令里面典型的属性型指令有 ngClass、ngStyle，如果打算封装自己的组件库，属性型指令是必备的内容。</li>
<li>结构型指令：可以修改 DOM 结构，内置的常用结构型指令有 *ngFor、*ngIf 和 NgSwitch。由于结构型指令会修改 DOM 结构，因而同一个 HTML 标签上面不能同时使用多个结构型指令，否则大家都来改 DOM 结构，到底听谁的呢？如果要在同一个 HTML 元素上面使用多个结构性指令，可以考虑加一层空的元素来嵌套，比如在外面套一层空的 &lt;ng-container&gt;&lt;/ng-container&gt;，或者套一层空的 &lt;div&gt;。</li>
</ul>
<h3 id="-1">有了组件为什么还要指令</h3>
<p>请注意：即使你认真、仔细地看完以上内容，依然感到非常茫然。因为有一个最根本的问题在所有文档里面都没有给出明确的解释，这个问题也是很多开发者经常来问我的，那就是：<strong>既然有了组件（Component），为什么还要指令（Directive）？</strong></p>
<p>我们知道，在很多 UI 框架里面，并没有指令的概念，它们的基类都是从 Component 开始的，比如：</p>
<ul>
<li>Swing 里面基类名字就叫 Component，没有指令的概念；</li>
<li>ExtJS 里面基类是 Ext.Component，没有指令的概念；</li>
<li>Flex 里面基类名字叫 UIComponent，没有指令的概念；</li>
<li>React 里面的基类名字叫 React.Component，没有指令的概念。</li>
</ul>
<p>以下是 Swing 的类结构图：</p>
<p><img src="https://images.gitbook.cn/c9cf7820-ecab-11e8-9a75-31990b0290b3"  width = "60%" /></p>
<p>以下是 ExtJS 3.2 的 UI 组件继承结构图局部，请注意 Ext.Component 类的位置：</p>
<p><img src="https://images.gitbook.cn/d9d3cfa0-ecab-11e8-a95e-2d541f7a88eb"  width = "70%" /></p>
<p>下面是整体缩略图：</p>
<p><img src="https://images.gitbook.cn/e75e4d80-ecab-11e8-a95e-2d541f7a88eb"  width = "70%" /></p>
<p>以下是 Adobe Flex 3 的类结构图：</p>
<p><img src="https://images.gitbook.cn/f54e43f0-ecab-11e8-a56e-b14ca1e28a87" alt="enter image description here" /></p>
<p>上面这些框架走的是组件化的路子，Swing 和 ExtJS 完全是“代码流”，所有 UI 都通过代码来创建；而 Flex 和 React 是“标签流”，也就通过标签的方式来创建 UI。</p>
<p>但是，所有这些框架都没有“指令”这个概念，为什么 Angular 里面一定要引入“指令”这个概念呢？</p>
<p><strong>根本原因是：我们需要用指令来增强标签的功能，包括 HTML 原生标签和你自己自定义的标签。</strong></p>
<p>举例来说：&lt;div&gt; 是一个常用的原生 HTML 标签，但是请不要小看它，它上面实际上有非常多的属性，这些属性都是 W3C 规范规定好的：</p>
<p><img src="https://images.gitbook.cn/041a1b70-ecac-11e8-98cb-171ea57578dc" alt="enter image description here" /></p>
<p>还能支持以下事件属性：</p>
<p><img src="https://images.gitbook.cn/526ee710-ecac-11e8-9a75-31990b0290b3" alt="enter image description here" /></p>
<p><a href="https://www.w3schools.com/tags/ref_standardattributes.asp">完整的列表请单击这里查看 W3C 规范</a>。</p>
<p>但是，这些内置属性还不够用，若想给原生的 HTML 标签再扩展一些属性，比方说：你想给 &lt;div&gt; 标签增加一个自定义的属性叫做 my-high-light，当鼠标进入 div 内部时，div 的背景就会高亮显示，可以这样使用 &lt;div my-high-light&gt;。</p>
<p>这时候，没有指令机制就无法实现了。</p></div></article>