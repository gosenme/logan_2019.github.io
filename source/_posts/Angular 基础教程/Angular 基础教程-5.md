---
title: Angular 基础教程-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>SASS 是一款非常好用的 CSS 预编译器，Bootstrap 官方从 4.0 开始已经切换到了 SASS。</p>
<h3 id="">创建项目的时候指定</h3>
<p>@angular/cli 当前（2019-06）最新的版本是 8.0，可以支持多款 CSS 预编译器，你可以在创建项目的过程中指定：</p>
<p><img src="https://images.gitbook.cn/72144200-ad2b-11e9-8f3f-792c82c0addc" width = "70%" /></p>
<h3 id="-1">手动修改</h3>
<p><em>某些老项目可能需要手动修改预编译器的类型，所以我把手动修改的方法也留下来备查。</em></p>
<p>目前（2019-06），@angular/cli 创建项目的时候没有自动使用 SASS 作为预编译器，我们需要自己手动修改一些配置文件，请按照以下步骤依次修改：</p>
<ul>
<li><p>angular-cli.json 里面的 styleExt 改成 scss</p>
<p><img src="https://images.gitbook.cn/8a3949c0-ad2b-11e9-b1a9-0994986ea855" width = "45%" /></p>
<p>当后面再使用 ng g c *** 自动创建组件的时候，默认就会生成 .scss 后缀的样式文件了。</p></li>
<li><p>angular-cli.json 里面的 styles.css 后缀改成 .scss</p></li>
</ul>
<p><img src="https://images.gitbook.cn/9ac3e840-ad2b-11e9-b015-0198f673a736" width = "50%" /></p>
<ul>
<li><p>src 下面 style.css 改成 style.scss</p>
<p><img src="https://images.gitbook.cn/d25ed4e0-ad2b-11e9-a760-01c165706a91" width = "30%" /></p></li>
<li><p>app.component.scss</p>
<p><img src="https://images.gitbook.cn/e6cfae40-ad2b-11e9-8f3f-792c82c0addc" width = "35%" /></p></li>
<li><p>app.component.ts 里面对应修改</p>
<p><img src="https://images.gitbook.cn/fda7c3a0-ad2b-11e9-b015-0198f673a736" width = "60%" /></p></li>
</ul>
<p>改完之后，重新 ng serve，打开浏览器查看效果。</p>
<h3 id="-2">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-component">本节完整的实例代码请参见这里</a>。</p>
<p><a href="http://sass-lang.com/">SASS 的 API 请参考官方网站</a>。</p>
<p><strong>SASS 只是一个预编译器，它支持所有 CSS 原生语法。利用 SASS 可以提升你的 CSS 编码效率，增强 CSS 代码的可维护性，但是千万不要幻想从此就可以不用学习 CSS 基础知识了。</strong></p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>