---
title: Angular 基础教程-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>几乎所有前端框架都在玩“组件化”，而且最近都不约而同地选择了“标签化”这种思路，Angular 也不例外。</p>
<p>对新版本的 Angular 来说，一切都是围绕着“组件化”展开的，组件是 Angular 的核心概念模型。</p>
<p>以下是一个最简单的 Angular 组件定义：</p>
<p><img src="https://images.gitbook.cn/131ef0d0-ad29-11e9-a760-01c165706a91" width = "60%" /></p>
<ul>
<li>@Component：这是一个 Decorator（装饰器），其作用类似于 Java 里面的 Annotation（注解）。Decorator 这个特性目前处于 Stage 2（草稿）状态，还不是 ECMA 的正式规范，<a href="https://tc39.github.io/proposal-decorators/#decorator-semantics">具体可参考这里</a>。</li>
<li>selector：组件的标签名，外部使用者可以这样来使用以上组件：&lt;app-root&gt;。默认情况下，ng 命令生成出来的组件都会带上一个 app 前缀，如果你不喜欢，可以在 angular-cli.json 里面修改 prefix 配置项，设置为空字符串将会不带任何前缀。</li>
<li>templateUrl：引用外部 HTML 模板。如果你想直接编写内联模板，可以使用 template，支持 ES6 引入的“模板字符串”写法，<a href="http://es6.ruanyifeng.com/#docs/string">具体可参考这里</a>。</li>
<li>styleUrls：引用外部 CSS 样式文件，这是一个数组，也就意味着可以引用多份 CSS 文件。</li>
<li>export class AppComponent：这是 ES6 里面引入的模块和 class 定义方式。</li>
</ul>
<p><a href="https://gitee.com/learn-angular-series/learn-component">本节完整的实例代码请参见这里</a>。</p>
<h3 id="">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>