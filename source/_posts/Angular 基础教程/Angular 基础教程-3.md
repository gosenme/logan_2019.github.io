---
title: Angular 基础教程-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="angularcliadd">@angular/cli 内置的 add 命令</h3>
<p>6.0 的时候 @angular/cli 新增了一个命令 ng add。</p>
<p>以前，如果我们需要引用一些第三方的 UI 库或者工具库，只能自己手动安装配置，过程中需要修改很多配置文件，非常繁琐，ng add 主要就是用来解决这个问题的。</p>
<p>如果你引用的第三方库支持了 ng add，那么整个过程全部是自动化的，以下这些事情 ng add 都会帮你自动完成：</p>
<ul>
<li>自动修改 package.json</li>
<li>自动使用 npm 安装依赖包</li>
<li>自动修改相关的配置文件，如果有的话</li>
<li>自动修改对应的模块引用文件</li>
<li>自动修改一些 CSS 样式文件</li>
</ul>
<p>接下来我们就来上手试一试 ng add 命令的用法，以官方的例子为基础，在上面做一些改进。</p>
<h4 id="">第一步：创建一个新项目</h4>
<pre><code>ng new learn-ng-add
</code></pre>
<ul>
<li>创建过程中选择需要 router 模块</li>
<li>样式语法选择 SCSS</li>
</ul>
<h4 id="angularmaterial">第二步：自动引入 @angular/material 库</h4>
<p>在项目根目录里面执行：</p>
<pre><code>ng add @angular/material
</code></pre>
<p><img src="https://images.gitbook.cn/031c0040-ad26-11e9-8f3f-792c82c0addc" width = "70%" /></p>
<p>可以看到，ng add 帮我们自动修改了这些文件：</p>
<p><img src="https://images.gitbook.cn/15206d80-ad26-11e9-b1a9-0994986ea855" width = "40%" /></p>
<p><strong>国内的开发者请注意：官方提供的 Material 这个 UI 组件库会自动应用 Google 的一些字体文件，这一点比较讨厌，你需要手动把这些字体文件下载到项目里面，然后引用你自己项目中的路径。</strong></p>
<h4 id="material">第三步：自动创建 Material 风格的导航栏</h4>
<pre><code>ng generate @angular/material:material-nav --name=my-nav
</code></pre>
<p><img src="https://images.gitbook.cn/2c5f8210-ad26-11e9-a760-01c165706a91" width = "45%" /></p>
<h4 id="-1">第四步：使用上面的导航栏</h4>
<p>稍稍修改一些代码，来使用上面自动生成的导航栏。</p>
<p>把 app.component.html 里面的内容清空，然后使用上面新建的导航栏：</p>
<pre><code>&lt;app-my-nav&gt;&lt;/app-my-nav&gt;
</code></pre>
<p>用 ng serve 启动项目，然后你就可以看到 Material 风格的导航条了：</p>
<p><img src="https://images.gitbook.cn/3e5437e0-ad26-11e9-a760-01c165706a91" width = "60%" /></p>
<h4 id="-2">第五步：继续修改，做一个完整的例子出来</h4>
<p>我们在以上内容的基础上继续修改：继续生成两个组件，然后加上异步路由配置，就可以得到了一个典型的项目界面了。</p>
<p><strong>注意：为了使用异步路由，我们这里在官方的例子上面做了一些改进，请参考我下面的步骤。</strong></p>
<pre><code>ng g module myDashboard
ng g @angular/material:material-dashboard --name=my-dashboard
ng g module myTable
ng g @angular/material:material-table --name=my-table
</code></pre>
<p>此时我们的项目代码结构如下：</p>
<p><img src="https://images.gitbook.cn/4d0645d0-ad26-11e9-b015-0198f673a736" width = "40%" /></p>
<p>接下来：</p>
<ul>
<li>请参考 app.routing.module.ts 里面的路由配置，给上面的两个异步模块都加上独立的路由配置。</li>
<li>修改导航条里面的 routerLink，指向对应的路由配置。</li>
</ul>
<p>然后就可以得到两个很漂亮的界面了：</p>
<p><img src="https://images.gitbook.cn/5ca265a0-ad26-11e9-b1a9-0994986ea855" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/69d7bea0-ad26-11e9-8f3f-792c82c0addc" width = "70%" /></p>
<p><strong>从这个例子你可以看到，ng add 和 ng generate 的功能非常强大，日常工作中的那些任务大多数能自动完成，只有很少的部分需要手动修改。</strong></p>
<p><a href="https://gitee.com/learn-angular-series/learn-ng-add">这个例子完整的代码请点击这里查看</a></p>
<h3 id="ngaddschematics">ng add 命令背后的 Schematics 代码生成器</h3>
<p><strong>请注意：初学者可以跳过这一段，这块是比较高级的内容，等你用熟悉了之后再回来研究不迟。单独使用 Schematics 比较麻烦，因为模板本身也是代码，也是需要维护的。另外，Schematics 特性本身还处于“实验”状态，官方提供的文档不全。</strong></p>
<p>@angular/cli 内部用来自动生成代码的工具叫做 Schematics ：</p>
<p><img src="https://images.gitbook.cn/7acabbe0-ad26-11e9-b1a9-0994986ea855" width = "75%" /></p>
<p>能支持的所有 Schematics 如下：</p>
<p><img src="https://images.gitbook.cn/8866ed00-ad26-11e9-b015-0198f673a736" width = "30%" /></p>
<p>如上图，当我们使用 ng g c \<组件名> 的时候，它实际上调用了底层的 Schematics 来生成组件对应的 4 个文件。</p>
<p>Schematics 是框架无关的，它可以脱离 Angular 环境使用，因此你也可以把它单独拿出来，用来自动生成其他框架的代码。为了演示自定义 Schematic 的方法，我已经整合好了 2 个项目，请看运行效果：</p>
<p><img src="https://images.gitbook.cn/95fd78d0-ad26-11e9-a760-01c165706a91" alt="enter image description here" /></p>
<p><strong>请特别注意：由于 @angular/schematics 是 cli 工具的组成部分，它的版本号与 cli 之间有对应关系。因此，如果你不确定对应关系是什么，请不要修改以上两个示例项目中的 package.json，升级必挂。</strong> <a href="https://www.npmjs.com/package/@angular-devkit/schematics">更多文档和模板语法请参考这里</a>。</p>
<p>你可以利用 Schematics 来创建自己的代码生成器，可以参考以下步骤：</p>
<ul>
<li>npm i -g @angular-devkit/schematics-cli</li>
<li>用 schematics 命令创建一个新项目 schematics blank --name=learn-schematics</li>
<li>创建 schema.json 和 schema.ts 接口，修改 collection.json，指向自己创建的 shema.json 配置文件</li>
<li>修改 index.ts ，加一些生成代码的逻辑，可以参考 @angluar/cli 内部的代码</li>
<li>创建 files 目录和模板文件，目录名和文件名本身也可以参数化</li>
<li>构建项目：npm run build</li>
<li>链接到全局，方便本地调试：npm link</li>
<li>准备测试 schema ，用 @angular/cli 创建一个全新的项目 test-learn-schematics 并装好依赖。cd 到新项目 test-learn-schematics，链接 npm link learn-schematics，然后尝试用我们自定义的规则来生成一个组件 ng g my-component My --service --name="damo" --collection learn-schematics --force</li>
</ul>
<h3 id="workspace">Workspace 与多项目支持</h3>
<p>从 6.0 开始，@angular/cli 支持 workspace 特性，之所以能支持 workspace，也是因为背后有 Schematics 这个底层的工具。</p>
<p>有了 workspace 这个机制之后，可以在一个项目里面配置多个子项目，cli 会根据里面的配置进行依赖管理、校验、编译等等操作。</p>
<p><img src="https://images.gitbook.cn/a815e340-ad26-11e9-b015-0198f673a736" width = "60%" /></p>
<p><a href="https://github.com/angular/angular-cli/wiki/angular-workspace">关于 workspace 官方的完整文档在这里</a>。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd003">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<h3 id="-3">参考资源</h3>
<ul>
<li><a href="https://gitee.com/learn-angular-series/learn-ng-add">本节涉及到的实例代码请点击这里查看</a></li>
<li><a href="https://www.npmjs.com/package/@angular-devkit/schematics">Schematics 的用法文档，请点击这里查看</a></li>
<li><a href="https://github.com/angular/angular-cli/wiki">@angular/cli 官方的 wiki 文档，请点击这里查看</a></li>
<li><a href="https://angular.io/guide/workspace-config">workspace 多项目配置，请点击这里查看</a> </li>
<li><a href="https://blog.angular.io/schematics-an-introduction-dc1dfbc2a2b2">Angular 官方 blog 里面关于 Schematics 的解释，请点击这里查看</a></li>
</ul>
<h3 id="-4">分享交流</h3>
<p>我们为本专栏付费读者创建了微信交流群，以方便更有针对性地讨论专栏相关问题。入群方式请到第 04 篇末尾查看。</p>
<p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）<strong>。你的分享不仅帮助他人，更会提升自己。</strong></p></div></article>