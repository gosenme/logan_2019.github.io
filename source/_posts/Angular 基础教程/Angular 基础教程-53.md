---
title: Angular 基础教程-53
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Sass 是一款非常好用的 CSS 预编译器，BootStrap 官方从 4.0 开始已经切换到了 Sass。</p>
<p>本课的主要内容：</p>
<ul>
<li>创建项目的时候指定</li>
<li>手动修改</li>
</ul>
<h3 id="">创建项目的时候指定</h3>
<p>Angular CLI 当前（2018 年 10 月 30 日）最新的版本是 7.0.2，可以支持多款 CSS 预编译器，可以在创建项目的过程中指定：</p>
<p><img src="https://images.gitbook.cn/bb604d70-e3d5-11e8-bfed-8d6b896efba7"  width = "70%" /></p>
<h3 id="-1">手动修改</h3>
<blockquote>
  <p>某些老项目可能需要手动修改预编译器的类型，所以我把手动修改的方法也留下来备查。</p>
</blockquote>
<p>目前（2017 年 10 月），@angular/cli 创建项目的时候没有自动使用 Sass 作为预编译器，我们需要自己手动修改一些配置文件，请按照以下步骤依次修改。</p>
<ul>
<li>angular-cli.json 里面的 styles.css 后缀改成 .scss </li>
</ul>
<p><img src="https://images.gitbook.cn/e7dab750-e3d5-11e8-8e04-b95633cc2286"  width = "60%" /></p>
<p>当你后面再使用 ng g c *** 自动创建组件的时候，默认就会生成 .scss 后缀的样式文件了。</p>
<ul>
<li>angular-cli.json 里面的 styleExt 改成 .scss</li>
</ul>
<p><img src="https://images.gitbook.cn/d04126b0-e3d5-11e8-a397-15a3bf78ee55"  width = "50%" /></p>
<ul>
<li>src 下面 style.css 改成 style.scss</li>
</ul>
<p><img src="https://images.gitbook.cn/204b4370-e3d6-11e8-8e04-b95633cc2286"  width = "30%" /></p>
<ul>
<li>app.component.scss</li>
</ul>
<p><img src="https://images.gitbook.cn/2dfc3510-e3d6-11e8-a1c4-731a3e37324c"  width = "30%" /></p>
<ul>
<li>app.component.ts 里面对应修改</li>
</ul>
<p><img src="https://images.gitbook.cn/41f434f0-e3d6-11e8-8e04-b95633cc2286"  width = "70%" /></p>
<p>改完之后，重启 ng serve，打开浏览器查看效果。</p>
<h3 id="-2">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-component">完整的实例代码请点击这里下载</a>。</p>
<p><a href="http://sass-lang.com/">点击这里跳转到 Sass 的 API 官方网站</a>。</p>
<p><strong>Sass 只是一个预编译器，它支持所有 CSS 原生语法。利用 Sass 可以提升 CSS 编码效率、增强 CSS 代码的可维护性，但是千万不要幻想从此就可以不用学习 CSS 基础知识了。</strong></p></div></article>