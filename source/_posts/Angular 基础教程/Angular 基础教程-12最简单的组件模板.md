---
title: Angular 基础教程-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">最简单的组件模板</h3>
<p>你编写了一个这样的面板组件：</p>
<p><img width="50%" src="https://images.gitbook.cn/0e2a0350-b8d5-11e9-ba33-51636d56aead"></p>
<p>组件对应的模板代码是这样的：</p>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;标题&lt;/div&gt;
  &lt;div class="panel-body"&gt;
      内容
  &lt;/div&gt;
  &lt;div class="panel-footer"&gt;
      底部
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<h3 id="-1">投影一块内容</h3>
<p>但是，你希望把面板里面的标题设计成可变的，让调用者能把这个标题传进来，而不是直接写死。这时候“内容投影”机制就可以派上用场了，我们可以这样来编写组件的模板：</p>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;
    &lt;ng-content&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
  &lt;div class="panel-body"&gt;
      内容
  &lt;/div&gt;
  &lt;div class="panel-footer"&gt;
      底部
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>请注意以上模板里面的 <code>&lt;ng-content&gt;&lt;/ng-content&gt;</code>，你看可以把它想象成一个占位符，我们用它来先占住一块空间，等使用方把参数传递进来之后，再用真实的内容来替换它。使用方可以这样来传递参数：</p>
<pre><code>&lt;test-child-two&gt;
    &lt;h3&gt;这是父层投影进来的内容&lt;/h3&gt;
&lt;/test-child-two&gt;
</code></pre>
<p>运行起来的效果是这样的：</p>
<p><img width="45%" src="https://images.gitbook.cn/57848c00-b8d5-11e9-a88b-c93a5ea3d618"></p>
<p>可以看到，标题的部分是由使用方从外部传递进来的。</p>
<h3 id="-2">投影多块内容</h3>
<p>接着，问题又来了，你不仅希望面板的标题部分是动态的，你还希望面板的主体区域和底部区域全部都是动态的，应该怎么实现呢？</p>
<p>你可以这样编写组件的模板：</p>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;
      &lt;ng-content select="h3"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
  &lt;div class="panel-body"&gt;
      &lt;ng-content select=".my-class"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
  &lt;div class="panel-footer"&gt;
      &lt;ng-content select="p"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>然后使用方可以这样来使用你所编写的组件：</p>
<pre><code>&lt;test-child-two&gt;
    &lt;h3&gt;这是父层投影进来的内容&lt;/h3&gt;
    &lt;p class="my-class"&gt;利用CSS选择器&lt;/p&gt;
    &lt;p&gt;这是底部内容&lt;/p&gt;
&lt;/test-child-two&gt;
</code></pre>
<p>运行起来的效果是这样的：</p>
<p><img width="45%" src="https://images.gitbook.cn/7fd1c6f0-b8d5-11e9-ba33-51636d56aead"></p>
<p>你可能已经猜出来了，<code>&lt;ng-content&gt;&lt;/ng-content&gt;</code> 里面的那个 select 参数，其作用和 CSS 选择器非常类似。</p>
<p>这种投影多块内容的方式叫“多插槽模式”（multi-slot），你可以把 <code>&lt;ng-content&gt;&lt;/ng-content&gt;</code> 想形成一个一个的插槽，内容会被插入到这些插槽里面。</p>
<h3 id="-3">投影一个复杂的组件</h3>
<p>到这里还没完，你不仅仅想投影简单的 HTML 标签到子层组件里面，你还希望把自己编写的一个组件投影进去，那又应该怎么办呢？</p>
<p>请看：</p>
<pre><code>&lt;div class="panel panel-primary"&gt;
  &lt;div class="panel-heading"&gt;
      &lt;ng-content select="h3"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
  &lt;div class="panel-body"&gt;
      &lt;ng-content select="test-child-three"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
  &lt;div class="panel-footer"&gt;
      &lt;ng-content select="p"&gt;&lt;/ng-content&gt;
  &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>使用方可以这样来使用这个组件：</p>
<pre><code>&lt;test-child-two&gt;
    &lt;h3&gt;这是父层投影进来的内容&lt;/h3&gt;
    &lt;test-child-three (sayhello)="doSomething()"&gt;&lt;/test-child-three&gt;
    &lt;p&gt;这是底部内容&lt;/p&gt;
&lt;/test-child-two&gt;
</code></pre>
<p>运行起来的效果是这样的：</p>
<p><img width="45%" src="https://images.gitbook.cn/d21bc190-b8d5-11e9-ba33-51636d56aead"></p>
<p>请注意 <code>&lt;ng-content select="test-child-three"&gt;&lt;/ng-content&gt;</code> 里面的内容，你把 select 属性设置成了子组件的名称。</p>
<p>同时，对于被投影的组件 <code>&lt;test-child-three&gt;&lt;/test-child-three&gt;</code> 来说，我们同样可以利用小圆括号的方式来进行事件绑定，就像上面例子里的 <code>(sayhello)="doSomething()"</code> 这样。</p>
<h3 id="-4">内容投影这个特性存在的意义是什么？</h3>
<p>如果没有“内容投影”特性我们也能活得很好，那么它就没有存在的必要了，而事实并非如此，如果没有“内容投影”，有些事情我们就没法做了，典型的有两类：</p>
<ul>
<li>组件标签不能嵌套使用。</li>
<li>不能优雅地包装原生的 HTML 标签。</li>
</ul>
<p>依次解释如下：</p>
<p>比如你自己编写了两个组件 my-comp-1 和 my-comp-2，如果没有内容投影，这两个组件就没办法嵌套使用，比如你想这样用就不行：</p>
<pre><code>&lt;my-comp-1&gt;
    &lt;my-comp-2&gt;&lt;/my-comp-2&gt;
&lt;/my-comp-1&gt;
</code></pre>
<p>因为没有“内容投影”机制，my-comp-1 无法感知到 my-comp-2 的存在，也无法和它进行交互。这明显有违 HTML 设计的初衷，因为 HTML 的本质是一种 XML 格式，标签能嵌套是最基本的特性，原生的 HTML 本身就有很多嵌套的情况：</p>
<pre><code>&lt;ul&gt;
  &lt;li&gt;神族&lt;/li&gt;
  &lt;li&gt;人族&lt;/li&gt;
  &lt;li&gt;虫族&lt;/li&gt;
&lt;/ul&gt;
</code></pre>
<p>在真实的业务开发里面，另一个典型的嵌套组件就是 Tab 页，以下代码是很常见的：</p>
<pre><code>&lt;tab&gt;
    &lt;pane title="第一个标签页"/&gt;
    &lt;pane title="第二个标签页"/&gt;
    &lt;pane title="第三个标签页"/&gt;
&lt;/tab&gt;
</code></pre>
<p>如果没有内容投影机制，想要这样嵌套地使用自定义标签也是不可能的。</p>
<p>内容投影存在的第二个意义与组件的封装有关。</p>
<p>虽然 Angular 提供了 @Component 装饰器让开发者可以自定义标签，但是请不要忘记，自定义标签毕竟与 HTML 原生标签不一样，原生 HTML 标签上面默认带有很多属性、事件，而你自己定义标签是没有的。原生 HTML 标签上面暴露的属性和事件列表请参见 W3C 的规范：</p>
<blockquote>
  <p><a href="https://www.w3schools.com/tags/ref_attributes.asp">https://www.w3schools.com/tags/ref_attributes.asp</a></p>
</blockquote>
<p>从宏观的角度看，所有的自定义标签都只不过是一层“虚拟的壳子”，浏览器并不认识自定义标签，真正渲染出来的还是 div、form、input 之类的原生标签。所以，自定义标签只不过是一层逻辑上的抽象和包装，让人类更容易理解和组织自己的代码而已。</p>
<p>既然如此，自定义标签和HTML原生标签之间的关系是什么呢？本质上说，这是“装饰模式”的一种应用，而内容投影存在的意义就是可以让这个“装饰”的过程做得更加省力、更加优雅一些。</p>
<h3 id="-5">接下来</h3>
<p>本节对应的完整实例代码请参见这里：<a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，代码在 ng-content 这个分支上面。</p>
<p>我们已经学会了内容投影最基本的用法，但是故事并没有结束，接下来的问题又来了：</p>
<ul>
<li>如何访问投影进来的复杂组件？比如：如何访问被监听组件上的 public 属性？如何监听被投影组件上的事件？接下来的小节就来解决这个问题。</li>
<li>如何访问投影进来的 HTML 元素？比如：如何给被投影进来的 HTML 元素添加 CSS 样式？这个话题反而比访问被投影组件要复杂一些，我们在讲指令的那一个小节里面给例子来描述。</li>
</ul>
<h3 id="-6">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>