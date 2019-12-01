---
title: Angular 基础教程-52
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>几乎所有前端框架都在玩“组件化”，而且最近都不约而同地选择了“标签化”这种思路，Angular 也不例外。</p>
<p>对于新版本的 Angular 来说，一切都是围绕着“组件化”来展开的，组件是 Angular 的核心概念模型。</p>
<p>以下是一个最简单的 Angular 组件定义。</p>
<p><img src="https://images.gitbook.cn/09c6de40-e3d4-11e8-a397-15a3bf78ee55"  width = "60%" /></p>
<ul>
<li>@Component：这是一个 Decorator（装饰器），其作用类似于 Java 里面的 Annotation（注解）。Decorator 这个特性目前处于 Stage 2（草稿）状态，还不是 ECMA 的正式规范，<a href="https://tc39.github.io/proposal-decorators/#decorator-semantics">请点击这里查看具体详情</a>。</li>
<li>selector：组件的标签名，外部使用者可以这样来使用以上组件，&lt;app-root&gt;。默认情况下，ng 命令生成出来的组件都会带上一个 app 前缀，如果你不喜欢，可以在 angular-cli.json 里面修改 prefix 配置项，设置为空字符串将会不带任何前缀。</li>
<li>templateUrl：引用外部 HTML 模板。如果你想直接编写内联模板，可以使用 template，支持 ES 6 引入的“模板字符串”写法，<a href="http://es6.ruanyifeng.com/#docs/string">请点击这里查看具体详情</a>。</li>
<li>styleUrls：引用外部 CSS 样式文件，这是一个数组，也就意味着可以引用多份 CSS 文件。</li>
<li>export class AppComponent：这是 ES 6 里面引入的模块和 class 定义方式。</li>
</ul>
<blockquote>
  <p><a href="https://gitee.com/learn-angular-series/learn-component">完整的实例代码请点击这里下载</a>。</p>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmqqsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote></div></article>