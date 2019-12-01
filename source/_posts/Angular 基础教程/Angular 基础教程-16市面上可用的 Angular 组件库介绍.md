---
title: Angular 基础教程-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="angular">市面上可用的 Angular 组件库介绍</h3>
<p>开源免费的组件库：</p>
<ul>
<li>PrimeNG：<a href="http://www.primefaces.org/primeng">http://www.primefaces.org/primeng</a>，这款组件库做得比较早，代码质量比较高。Telerik 这家公司专门做各种 UI 组件库，jQuery/Flex/Angular，全部都有。</li>
<li>NG-Zorro：<a href="https://github.com/NG-ZORRO/ng-zorro-antd">https://github.com/NG-ZORRO/ng-zorro-antd</a>，来自阿里云团队，外观是 AntDesign 风格。</li>
<li>Clarity：<a href="https://vmware.github.io/clarity/">https://vmware.github.io/clarity/</a>，来自 Vmware 团队。</li>
<li>Angular-Material：<a href="https://github.com/angular/material2">https://github.com/angular/material2</a>，Angular 官方提供的组件库。</li>
<li>Element-Angular：<a href="https://element-angular.faas.ele.me/guide/install">https://element-angular.faas.ele.me/guide/install</a>，作者来自饿了么团队。</li>
<li>Jigsaw（七巧板）：<a href="https://github.com/rdkmaster/jigsaw">https://github.com/rdkmaster/jigsaw</a>，来自 ZTE 中兴通讯。组件数量比较多，外观不够漂亮。</li>
<li>Ionic：<a href="https://ionic.io/">https://ionic.io/</a>，专门为移动端打造的组件库，自带周边工具，生态很完善。</li>
</ul>
<p>收费版组件库：</p>
<ul>
<li>来自 Telerik 的 KendoUI for Angular：<a href="http://www.telerik.com/kendo-angular-ui/">http://www.telerik.com/kendo-angular-ui/</a>，Telerik 的这套组件库的特色是组件的功能比较强大，尤其是 Grid，做得非常强大。</li>
</ul>
<h3 id="">如何在你的项目里面引入开源组件库</h3>
<p>以 PrimeNG 为例，首先在 package.json 里面定义好依赖：</p>
<p><img width="65%" src="https://images.gitbook.cn/7fbe5ea0-b8d8-11e9-8b62-c350e3466c22"></p>
<p>然后打开终端用 cnpm install 安装 PrimeNG 到你本地，在你自己的业务模块里面 import 需要用到的组件模块就好了：</p>
<p><img width="70%" src="https://images.gitbook.cn/78bba180-b8d8-11e9-8b62-c350e3466c22"></p>
<p>从 Angular 6.0 开始，@angular/cli 增加了一个 <code>ng add</code> 命令，所有支持 Schematics 语法的组件库都可以通过这个命令自动整合，并且在创建你自己组件的时候可以指定需要哪种风格，详细的例子和解释请参考“1-2Schematics 与代码生成器”这一小节。</p>
<h3 id="npm">如何把你的组件库发布到 npm 上去</h3>
<p>有朋友问过一个问题，他觉得 npm 很神奇，比如当我们在终端里面输入以下命令的时候：</p>
<pre><code>npm install -g @angular/cli
</code></pre>
<p>npm 就会自动去找到@angular/cli 并安装，看起来很神奇的样子。</p>
<p>其实，背后的处理过程很简单，npm 官方有一个固定的 registry url，你可以把它的作用想象成一个 App Store，全球所有开发者编写的 node 模块都需要发布上去，然后其他人才能安装使用。</p>
<p>如果你开发了一个很强大的 Angular 组件库，希望发布到 node 上面让其他人也能使用，应该怎么做呢？简略的处理步骤如下：</p>
<ul>
<li>第 1 步：用 npm init 初始化项目（只要你的项目里面按照 npm 的规范编写一份 package.json 文件就可以了，不一定用 npm init 初始化）。</li>
<li>第 2 步：编写你自己的代码。</li>
<li>第 3 步：到 https://www.npmjs.com/ 去注册一个账号。</li>
<li>第 4 步：用 npm publish 把项目 push 上去。</li>
</ul>
<p>publish 之后，全球开发者都可以通过名字查找并安装你这个模块了。</p>
<h3 id="-1">一些小小的经验供你参考</h3>
<p>在我的上一家公司工作期间，我曾经参与、领导过公司两代前端框架的组件库设计和维护，涉及到 jQuery、Flex 等多个技术体系。从 2011 年开始计算，整个维护周期已经有 6 年多。</p>
<p>我自己也从零开始编写过一款页面流程图组件库，整体大约 1.9 万行 AS3 代码，至今仍在公司几十个产品里面运行。</p>
<p>因此，我特别想谈一谈两个常见的误区：</p>
<ul>
<li>第一个误区是：开源组件可以满足你的所有需求。我可以负责任地告诉你，这是不可能的！开源组件库都是通用型的组件，并不会针对任何特定的行业或者领域进行设计。无论选择哪一款开源组件库，组件的外观 CSS 你总要重新写一套的吧？组件里面缺的那些功能你总得自己去写吧？组件里面的那些 Bug 你总得自己去改掉吧？所以，千万不要幻想开源组件能帮你解决所有问题，二次开发是必然的。</li>
<li>第二个误区是：开发组件库很简单，分分钟可以搞定。在 jQuery 时代，有一款功能极其强大树组件叫 <a href="http://www.treejs.cn/v3/main.php#_zTreeInfo">zTree</a>。你能想到的那些功能 zTree 都实现了，而且运行效率特别高。但是你要知道，zTree 的作者已经花了超过 5 年的时间来维护这个组件。维护一个组件尚且如此，何况要长期维护一个庞大的库？所以，做好一个组件库并不像有些人想象的那么轻松，这件事是需要花钱、花时间的。做开源，最让使用者蛋疼的不是功能够不够强大，而是开发者突然弃坑，这也是很多企业宁愿花钱自己开发组件库的原因。所以，如果你只是单兵作战，最好选一款现有的开源库，在此基础上继续开发。强烈建议你只做一个组件，就像 zTree 的作者那样，把一个组件做好、做透，并且长期维护下去。这比搞一个庞大的组件库，每个组件做得都像个玩具，然后突然弃坑要好很多。</li>
</ul>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>