---
title: Angular 基础教程-57
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本课的主要内容：</p>
<ul>
<li>非常重要的说明</li>
<li>用法示范</li>
</ul>
<h3 id="">非常重要的说明</h3>
<p>Angular 默认的动画模块使用的是 Web Animations 规范，这个规范目前处于 Editor’s Draft 状态（2017-09-22），<a href="https://w3c.github.io/web-animations/">具体详情请点击这里查看</a>。</p>
<p>目前，各大浏览器厂商对 Web Animations 规范的支持并不好，请看下图：</p>
<p><img src="https://images.gitbook.cn/30e4c450-e3fd-11e8-bfed-8d6b896efba7" alt="enter image description here" /></p>
<p><a href="http://caniuse.com/#feat=web-animation">具体详情请点击这里查看</a>。</p>
<p>Web Animations 这套新的规范在 FireFox、Chrome、Opera 里面得到了完整的支持，而其他所有浏览器内核几乎都完全不支持，所以请慎重选择。我的建议是，请优先使用 CSS 3 规范里面的 anmimation 方案，<a href="https://www.w3schools.com/css/css3_animations.asp">具体详情请点击这里查看</a>。</p>
<h3 id="-1">用法示范</h3>
<p>第一步：导入动画模块。</p>
<p><img src="https://images.gitbook.cn/43e062d0-e3fd-11e8-8e04-b95633cc2286"  width = "80%" /></p>
<p>第二步：编写动效。</p>
<p><img src="https://images.gitbook.cn/7876c200-e3fd-11e8-a1c4-731a3e37324c"  width = "80%" /></p>
<p>flyIn 是这个动效的名称，后面就可以在组件里面引用 flynIn 这个名字了。</p>
<p>动效整体上是由“状态”和“转场”两个部分构成。</p>
<ul>
<li>以上代码里面的星号（*）表示“不可见状态”，void 表示任意状态，这是两种内置的状态，（*=&gt;void）表示进场动画，而（void=&gt;*）表示离场动画。当然也可以定义自己的状态名称，注意不要和内置的状态名称发生冲突。</li>
<li>keyframes 里面的内容是关键帧的定义，语法和 CSS 3 里面定义动画的方式非常类似。</li>
</ul>
<p>第三步：在组件里面使用 flyIn 这个动效。</p>
<p><img src="https://images.gitbook.cn/8da32330-e3fd-11e8-bfed-8d6b896efba7"  width = "60%" /></p>
<p><img src="https://images.gitbook.cn/9bd0e5f0-e3fd-11e8-8e04-b95633cc2286"  width = "60%" /></p>
<p><a href="https://gitee.com/learn-angular-series/learn-component">例子的完整代码请点击这里下载</a>，代码在  animation 分支上面，运行后可以看到这个效果界面：</p>
<p><img src="https://images.gitbook.cn/a8087e00-e3fd-11e8-a1c4-731a3e37324c"  width = "80%" /></p>
<p>Angular 官方的动效文档<a href="https://angular.io/guide/animations">请点击这里查看</a>。</p>
<p>如果不愿意自己编写动效，推荐这个开源项目，它和 Angular 之间结合得比较紧，<a href="https://github.com/jiayihu/ng-animate">具体详情请点击这里查看</a>。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-component">完整的示例代码请点击这里下载</a>，请检出 animation 分支。</p></div></article>