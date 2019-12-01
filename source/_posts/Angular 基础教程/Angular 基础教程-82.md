---
title: Angular 基础教程-82
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>自动化测试一直是前端开发中的一个巨大痛点，由于前端在运行时严重依赖浏览器环境，导致我们一直没法像测试后端代码那样可以自动跑用例。</p>
<p>在有了 NodeJS 之后，我们终于有了 Karma + Jasmine 这样的单元测试组合，也有了基于 WebDriverJS 这样的可以和浏览器进行通讯的集成测试神器。</p>
<p>目前，无论使用什么样的前端框架，做单元测试一定会用到 Karma + Jasmine，这个组合已经成为了事实标准。Karma 是一个运行时平台，Jasmine 是用来编写测试用例的一种语法。</p>
<p>集成测试（场景测试）稍微复杂一些，但是一般都会用 WebDriverJS 来实现，它也是事实标准。对于 Angular 来说，集成测试所用的工具叫做 Protractor（量角器），底层也是 WebDriverJS。</p>
<p>如果使用 @angular/cli 作为开发环境，在前端自动化测试方面会非常简单，因为它已经在内部集成了这些工具。</p>
<p>但是有一件事非常遗憾，在 @angular/cli 目前发布的所有版本里面，默认生成的项目和配置文件都无法直接运行单元测试，因为 @angular/cli 默认引用的一些 NodeJS 模块在 Windows 平台上面有 bug。</p>
<p>因此，这节课不会列举 Jasmine 和 Protractor 的那些语法特性，而是填平这些小坑，让你能把这个机制跑起来。至于 Jasmine 和 Protractor 详细 API 调用方式，需要你自己去研究并熟悉，请参见以下链接：</p>
<ul>
<li><a href="https://jasmine.github.io/">https://jasmine.github.io/</a></li>
<li><a href="http://www.protractortest.org">http://www.protractortest.org</a></li>
</ul>
<p>注意，Karma、Jasmine、WebDriverJS 是通用技术，与具体的框架无关；Protractor 是专门针对 Angular 设计的，不能用在其他框架里面。</p>
<h3 id="">单元测试</h3>
<p>在 @angular/cli 自动生成的项目结构里面，karma.conf.js 里面有这样一些配置项：</p>
<p><img width="55%" src="https://images.gitbook.cn/2ff1cf50-f444-11e8-a018-a3bc43149496"></p>
<p>很可惜，这里引用的 karma-jasmine-html-reporter 这个 Node 模块在 Windows 下面有 bug。</p>
<p>因此需要进行一些修改，把报告生成器改成 karma-htmlfile-reporter 和 karma-mocha-reporter。</p>
<p>需要修改两份配置文件：package.json 和 karma.conf.js。</p>
<p>第一步，把 package.json 里面的 "karma-jasmine-html-reporter" 这一行删掉，换成以下内容：</p>
<pre><code>"karma-mocha-reporter":"^2.2.3",
"karma-htmlfile-reporter": "~0.3",
</code></pre>
<p>第二步，把 karma.conf.js 里面的 require('karma-jasmine-html-reporter') 这一行配置换成以下内容：</p>
<pre><code>require('karma-htmlfile-reporter'),
require('karma-mocha-reporter'),
</code></pre>
<p>同时把原来 reporters: ['progress', 'kjhtml'] 这一行替换成下面的一段内容：</p>
<pre><code>reporters: ['progress','mocha','html'],
htmlReporter: {
    outputFile: 'unit-test-report/report.html',

    // Optional 
    pageTitle: '单元测试结果',
    subPageTitle: 'learn-test',
    groupSuites: true,
    useCompactStyle: true,
    useLegacyStyle: true
},
</code></pre>
<p>如果直接复制 karma.conf.js 完整的内容，<a href="https://gitee.com/learn-angular-series/learn-test">请参考这个空壳示例项目</a>。</p>
<p>改完这些配置之后，使用 cnpm install 重新安装一下所依赖的 Node 模块，然后在终端里面执行：</p>
<pre><code>ng test
</code></pre>
<p>Karma 将会自动把本地的 Chrome 浏览器拉起来，并且自动运行所有测试用例。</p>
<p><img width="60%" src="https://images.gitbook.cn/1fae6110-f446-11e8-b435-7f45fd734750"></p>
<p><img width="40%" src="https://images.gitbook.cn/2f4095d0-f446-11e8-9460-178de39eb82c"></p>
<p>同时，在 unit-test-report 这个目录里面会生成一个 report.html，我本地跑完之后生成的内容如下：</p>
<p><img width="70%" src="https://images.gitbook.cn/748c4d00-f446-11e8-9460-178de39eb82c"></p>
<p>接下来就看你自己的了，需要去 Jasmine 的主页上面熟悉一下基本语法，然后编写更多的单元测试用例。</p>
<h3 id="-1">集成测试</h3>
<p>在 @angular/cli 自动生成的项目结构里面，有一个 e2e 目录，里面有 3 个文件：</p>
<p><img width="30%" src="https://images.gitbook.cn/a999d800-f446-11e8-9460-178de39eb82c"></p>
<p>打开 app.po.ts，可以看到下面的内容：</p>
<pre><code>import { browser, by, element } from 'protractor';

export class AppPage {
  navigateTo() {
    return browser.get('/');
  }

  getParagraphText() {
    return element(by.css('app-root h1')).getText();
  }
}
</code></pre>
<p>我不打算在这节课里面列举 Protractor 的技术特性和 API 列表，借着上面的这段代码，我大概介绍一下 Protractor 的整体设计思路和使用方式。</p>
<p>如前所述，Protractor 的底层是 WebDriverJS，从 WebDriverJS 这个名字你可以猜出来，这是一个 Driver（驱动），它是用来和浏览器进程通讯的。</p>
<p>Protractor 在 WebDriverJS 的基础上封装了一层，暴露出了几个非常核心的接口：</p>
<ul>
<li>browser 对象，可以利用这个对象来操纵浏览器，比如打开和关闭浏览器窗口、让浏览器窗口最大（小）化、控制浏览器导航到某个 URL 路径；</li>
<li>element 和 by 对象，可以利用这两个对象来控制浏览器内部的 HTML 元素，而其基本的语法和 CSS 选择器非常类似，并没有太多的学习成本。</li>
</ul>
<h3 id="-2">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-test">本节课完整可运行的实例代码请参见这里</a>。</p>
<p>推荐阿里发布的前端自动化测试 F2etest 框架，这是我目前看到的<strong>最强大的一款前端自动化框架</strong>，而且是<strong>开源免费</strong>的。F2etest 的底层也是用的 Karma + Jasmine 和 WebDriverJS 这套东西，它在此基础上进行了自己的封装，可以利用多台虚拟机实现浏览器云的效果。<a href="https://github.com/alibaba/f2etest">关于 F2etest 的更多详情请参考这个链接</a>，里面有详细的文档和上手教程。</p>
<p><img width="70%" src="https://images.gitbook.cn/4876ca00-f447-11e8-b435-7f45fd734750"></p>
<p>据我所知，虽然已经有了这么多强大的工具，但是国内大多数企业并没有真正去编写测试用例。因为测试用例本身也是代码，而国内大多数企业都会不停地改需求，这就会导致测试用例的代码也需要不停地改，不写测试用例我们已经 996 了，根本没有任何动力去把工作量增加一倍。</p>
<p>因此，像 TDD 这种东西，还是让它停留在美丽的幻想里面吧。</p>
<p>对于自动化测试这件事，各位量力而行，能做就做一些，实在不想做的话，最起码要知道怎么做。</p>
<p>当然，我也看到有少量的企业自己搭建了完善的持续集成平台，如果有这样的技术基础，自动化测试做起来会轻松很多。</p></div></article>