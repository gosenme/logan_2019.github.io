---
title: Angular 基础教程-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">非常重要的说明</h3>
<p>Angular 默认的动画模块使用的是 Web Animations 规范，这个规范目前处于 Editor’s Draft 状态（2017-09-22），详情请看这里：</p>
<blockquote>
  <p><a href="https://w3c.github.io/web-animations/">https://w3c.github.io/web-animations/</a></p>
</blockquote>
<p>目前，各大浏览器厂商对 Web Animations 规范的支持并不好，请看下图：</p>
<p><img width="100%" src="https://images.gitbook.cn/de64ed30-b8d2-11e9-ba33-51636d56aead"></p>
<p>（图片来自：http://caniuse.com/#feat=web-animation）</p>
<p>Web Animations 这套新的规范在 FireFox、Chrome、Opera 里面得到了完整的支持，而其它所有浏览器内核几乎都完全不支持，所以请慎重选择。我的建议是，请优先使用 CSS3 规范里面的 anmimation 方案：</p>
<blockquote>
  <p><a href="https://www.w3schools.com/css/css3_animations.asp">https://www.w3schools.com/css/css3_animations.asp</a></p>
</blockquote>
<h3 id="-1">用法示范</h3>
<p>第一步，导入动画模块：</p>
<p><img width="100%" src="https://images.gitbook.cn/192ab3f0-b8d3-11e9-ba33-51636d56aead"></p>
<p>第二步，编写动效：</p>
<p><img width="100%" src="https://images.gitbook.cn/20660d40-b8d3-11e9-a194-19c3d4002b01"></p>
<p>flyIn 是这个动效的名称，后面我面就可以在组件里面引用 flynIn 这个名字了。</p>
<p>动效整体上是由“状态”和“转场”两个部分构成的：</p>
<ul>
<li>以上代码里面的星号（*）表示“不可见状态”，void 表示任意状态。这是两种内置的状态，*=&gt;void 表示是进场动画，而 void=&gt;* 表示离场动画。当然你也可以定义自己的状态名称，注意不要和内置的状态名称发生冲突。</li>
<li>keyframes 里面的内容是关键帧的定义，语法和 CSS3 里面定义动画的方式非常类似。</li>
</ul>
<p>第三步，在组件里面使用 flyIn 这个动效：</p>
<p><img width="100%" src="https://images.gitbook.cn/68b1be00-b8d3-11e9-a194-19c3d4002b01"></p>
<p><img width="100%" src="https://images.gitbook.cn/70e61d50-b8d3-11e9-a194-19c3d4002b01"></p>
<p>这个例子完整的代码在这里：</p>
<blockquote>
  <p><a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a></p>
</blockquote>
<p>代码在 animation 分支上面，运行起来你可以看到这个效果界面：</p>
<p><img width="100%" src="https://images.gitbook.cn/8c2b9ef0-b8d3-11e9-a88b-c93a5ea3d618"></p>
<h3 id="-2">小结</h3>
<p>Angular 官方的动效文档在这里：</p>
<blockquote>
  <p><a href="https://angular.io/guide/animations">https://angular.io/guide/animations</a></p>
</blockquote>
<p>如果你不愿意自己编写动效，推荐这个开源项目，它和 Angular 之间结合得比较紧：</p>
<blockquote>
  <p><a href="https://github.com/jiayihu/ng-animate">https://github.com/jiayihu/ng-animate</a></p>
</blockquote>
<p>本节完整的示例代码在这里：<a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，请检出 animation 分支。</p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>