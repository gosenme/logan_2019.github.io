---
title: Angular 基础教程-49
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><ul>
<li>Ivy：很可惜，社区期盼已久的 Ivy 在 8.0 里面还是“实验”状态，官方不建议在产品里面使用，预计会在下一个大版本释放出来。Ivy 是底层渲染引擎，官方宣称它能“极大地”缩小打包体积，并且能“大幅度”提升渲染性能。如果真的如此的话，那么这将是一个核弹级的升级。官方承诺，升级到 Ivy 之后，业务代码不需要修改，因为它只是底层的渲染引擎，外部接口不会变动。</li>
<li>Bazel：这是 Google 内部的一款构建工具，目前已经开源。Angular 8.0 还不能完整支持 Bazel。引入 Bazel 的主要目的是为了解决当前 Node 构建速度太慢的问题，实际上这不是 Angular 的锅，主要是 Node.js 本身的性能瓶颈导致的。</li>
<li>Differential Loading：差异化加载。名词看起来高大上，实际上思路很简单，我用自己的语言给你描述一下你就懂了。目前市面上主流的浏览器都已经能完整支持 ES6 标准，Chrome/Firefox/Safari 都 OK，但是还有一些老的浏览器不能支持。所以从 Angular 8.0 开始，编译器会生成两种版本的打包文件，一种用来支持标准浏览器，一种用来支持老浏览器。Angular 在运行时自己会进行判断，如果发现你的浏览器比较新，会自动加载 ES6 版本的包，否则就自动加载老版本的包。这样做的好处是，对于新浏览器来说，打包出来的文件体积非常小。请不用担心，这些操作都是编译器自动完成的，你唯一需要修改的地方就是 tsconfig.json 文件，把编译目标改成 ES2015 即可，就像这样：</li>
</ul>
<p><img src="https://images.gitbook.cn/c0251950-dd5b-11e9-aaec-b5744b419935"></p>
<ul>
<li>路由与动态 import：这里主要是为了采纳最新的动态引入标准 import()，有了这个 import 函数之后，后面可以实现很多非常猥琐的功能了。改起来也很简单，就像这样：</li>
</ul>
<p><img src="https://images.gitbook.cn/cfe5ff30-dd5b-11e9-a584-59c5758c1abc"></p>
<ul>
<li>在 CLI 里面内置了对 Service Worker 的支持。</li>
<li>Breaking change：@ViewChild 装饰器多了第二个参数。</li>
<li>其它小特性的修改，参见官方的 changelog，链接在下面。</li>
</ul>
<p><strong>特别注意：某些第三方的组件和库可能还没有升级到 8.0，如果你的项目已经很大，不要盯版本盯太紧，没有必要。从我自己的实际升级体验看，整个升级过程非常平滑，基本没有恶心的地方。</strong></p>
<p>参考：</p>
<ul>
<li><a href="https://update.angular.io/">升级指南</a></li>
<li><a href="https://github.com/angular/angular/releases">官方 Repo</a></li>
<li><a href="https://blog.angular.io/version-8-of-angular-smaller-bundles-cli-apis-and-alignment-with-the-ecosystem-af0261112a27">官方 Blog</a></li>
</ul></div></article>