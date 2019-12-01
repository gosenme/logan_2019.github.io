---
title: Angular 基础教程-44
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过前面的小节，我们已经熟悉了 Angular 的方方面面，最后，我们来一个综合的大例子。</p>
<p>OpenWMS 也是一个开源项目，同时提交在 GithuHb 和 Gitee 上：</p>
<ul>
<li><a href="https://github.com/damoqiongqiu/OpenWMS-Frontend">https://github.com/damoqiongqiu/OpenWMS-Frontend</a></li>
<li><a href="https://gitee.com/mumu-osc/OpenWMS-Frontend">https://gitee.com/mumu-osc/OpenWMS-Frontend</a></li>
</ul>
<p>这个项目的技术特性如下：</p>
<ul>
<li>Angular 核心包：7.0.0</li>
<li>组件库：PrimeNG 6.1.5</li>
<li>图表：ngx-echarts</li>
<li>国际化：ngx-translate</li>
<li>字体图标：font-awesome</li>
</ul>
<p>OpenWMS 为你提供了一个可以借鉴的项目模板，把真实业务开发过程中的模块都配置好了。</p>
<h3 id="">模块分析</h3>
<p>以下是项目 build 出来的体积：</p>
<p><img src="https://images.gitbook.cn/449fed70-d7cd-11e9-a536-c512dee3d564"></p>
<p>用 webpack-bundle-analyzer 分析之后可以看到各个模块在编译之后所占的体积：</p>
<p><img src="https://images.gitbook.cn/4bd134a0-d7cd-11e9-8797-4924c0d7c082"></p>
<p>可以看到，主要是因为 ECharts 和 PrimeNG 占的体积比较大，建议您在使用的时候做一下异步，用不到的组件不要一股脑全部导入进来。</p>
<h3 id="-1">效果截图</h3>
<p><img src="https://images.gitbook.cn/54fb8cb0-d7cd-11e9-8797-4924c0d7c082"></p>
<p><img src="https://images.gitbook.cn/5a8f7790-d7cd-11e9-8fae-816b29059b0c"></p>
<p><img src="https://images.gitbook.cn/64978570-d7cd-11e9-a536-c512dee3d564"></p></div></article>