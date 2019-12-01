---
title: Angular 基础教程-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="nodejs">Node.js</h3>
<p>2009 年，Node.js 发布了第一个版本，标志着前端开发正式告别了刀耕火种的原始状态，开始进入工业化时代。</p>
<p>在 Node.js 出现之前，前端开发领域有很多事情我们是做不到的，比如：</p>
<ul>
<li>JS 代码的合并、压缩、混淆</li>
<li>CSS 预处理</li>
<li>前端自动化测试</li>
</ul>
<p>而这一切在 Node.js 出现之后都得到了很好的解决。</p>
<ul>
<li>对 JS 代码的预处理经历了 Grunt、Gulp 的短暂辉煌之后，终于在 Webpack 这里形成了事实标准的局面。</li>
<li>CSS 的预处理也从 LESS 发展到了 SASS 等。</li>
<li>自动化测试一直是前端开发中的一个巨大痛点，由于前端在运行时严重依赖浏览器环境，导致我们一直无法像测试后端代码那样可以去编写测试用例。在有了 Node.js 之后，我们终于有了 Karma + Jasmine 这样的单元测试组合，也有了基于 WebDriverJS 这样的可以和浏览器进行通讯的集成测试神器。</li>
</ul>
<p>就前端开发目前整体的状态来说，无论你使用什么框架，Node.js、Webpack、SASS、Karma + Jasmine、WebDriverJS 这个组合是无论如何绕不过去的。如果你用过其他前端框架的话，就知道手动配置这些东西有多痛苦了，那一坨配置文件没有半天功夫是搞不定的。</p>
<h3 id="angularcli">@angular/cli</h3>
<p><img src="https://images.gitbook.cn/4b1f3900-e3c5-11e8-a1c4-731a3e37324c"  width = "70%" /></p>
<p>在开发 Angular 应用的时候，当然也离不开大量基于 Node.js 的工具，我们需要 TypeScript compiler、Webpack、Karma、Jasmine、Protracter 等模块。</p>
<p>有相关经验的开发者都知道，自己从头开始去搭建一套基于 webpack 的开发环境是一件非常麻烦的事情。很多初学者在搭建环境这一步上面消耗了过多的精力，导致学习热情受到了沉重的打击。</p>
<p>当团队规模比较大的时候，在每个人的机器上配置环境需要消耗大量的时间。有一些团队为了避开这个坑，利用 Docker 来做开发环境的同步和版本升级，看起来也是一个非常不错的方案。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd002">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<p>Angular 项目组从一开始就注意到了这个问题，因此有了 @angular/cli 这个神器，它的底层基于 webpack，集成了以上提到的所有 Node.js 组件。你只要装好 @angular/cli 就够了，而不需要自己从头一步一步安装那些 Node.js 插件。</p>
<p>当然，在安装 @angular/cli 之前需要先把 Node.js 安装好，<a href="https://nodejs.org/">请到官方网站下载安装包</a> ，安装过程和普通软件没有区别。装好 Node.js 之后就可以安装 @angular/cli 了，由于 npm 会自动访问海外的服务器，因而强烈推荐使用 cnpm 进行安装：</p>
<pre><code>npm i -g cnpm --registry=https://registry.npm.taobao.org

cnpm i -g @angular/cli
</code></pre>
<p>cnpm 是淘宝发布的一款工具，会自动把 npm 上面的所有包定时同步到国内的服务器上来（目前大约 10 分钟全量同步一次），cnpm 本身也是一款 Node.js 模块。由于 cnpm 的服务器在国内，因而中文开发者用它装东西比较快。除了定时同步 npm 模块之外，cnpm 还做了一些其他的事情，比如把某些包预先编译好了缓存在服务器上，这样就不用拉源码到你本地进行编译了。有人抱怨使用 cnpm 安装的目录结构和 npm 不同，包括还有其他一些小坑，如果你非常在意这些，可以使用 nrm 来管理多个 registry。nrm 本身也是一个 Node.js 模块，你可以这样安装：</p>
<pre><code>npm i -g nrm
</code></pre>
<p>然后你就可以用 nrm 来随时切换 registry 了，比如：</p>
<pre><code>nrm use cnpm
</code></pre>
<p>这样就不用每次都用 cnpm 进行安装了，直接使用 npm 即可。</p>
<p>@angular/cli 安装成功之后你的终端里面将会多出一个名叫 ng 的命令，敲下 ng，将会显示完整的帮助文档：</p>
<p><img src="https://images.gitbook.cn/3ec779e0-ac67-11e9-add6-13ebc1d14b27" width = "65%" /></p>
<p>官方文档里面列出了所有这些命令的含义和示例，<a href="https://angular.io/cli/">链接在这里</a>。<strong>但是请注意，官方提供的 cli 文档过于简单，有非常多的细节都没有提到，所以你懂的，请跟着我的 demo 走。</strong></p>
<h3 id="">创建第一个项目</h3>
<p>我们来创建第一个入门项目 HelloAngular，请在你的终端里面运行：</p>
<pre><code>ng new HelloAngular
</code></pre>
<p>@angular/cli 将会自动帮你把目录结构创建好，并且会自动生成一些模板化的文件，就像这样：</p>
<p><img src="https://images.gitbook.cn/6bb0ab20-ac67-11e9-add6-13ebc1d14b27" width = "50%" /></p>
<p><strong>请特别注意：</strong> @angular/cli 在自动生成好项目骨架之后，会立即自动使用 npm 来安装所依赖的 Node 模块，因此这里我们要 Ctrl+C 终止掉，然后自己进入项目的根目录，使用 cnpm 来进行安装。</p>
<p><img src="https://images.gitbook.cn/9d8181b0-ac67-11e9-add6-13ebc1d14b27" alt="enter image description here" /></p>
<p>安装完成之后，使用 ng serve 命令启动项目：</p>
<p><img src="https://images.gitbook.cn/ab185ba0-ac67-11e9-b243-f31642e7dba4" alt="enter image description here" /></p>
<p>打开你的浏览器，访问默认的 4200 端口，看到以下界面说明环境 OK 了：</p>
<p><img src="https://images.gitbook.cn/b76836a0-ac67-11e9-b99d-87fbe4d2a696" width = "40%" /></p>
<p>请注意以下几点。</p>
<ul>
<li><strong>这里是 serve，不是 server，serve 是服务，动词；server 是服务器，名词。</strong>，我看到一些初学者经常坑在这个地方。</li>
<li>如果你需要修改端口号，可以用 ng serve --port **** 来进行指定。</li>
<li>ng serve --open 可以自动打开你默认的浏览器。</li>
<li>如果你想让编译的包更小一些，可以使用 ng serve --prod，@angular/cli 会启用 TreeShaking 特性，加了参数之后编译的过程也会慢很多。因此，在正常的开发过程里面请不要加 --prod 参数。</li>
<li>ng serve 是在内存里面生成项目，如果你想看到项目编译之后的产物，请运行 ng build。构建最终产品版本可以加参数，ng build --prod。</li>
</ul>
<p>ng 提供了很多非常好用的工具，除了可以利用 ng new 来自动创建项目骨架之外，它还可以帮助我们创建 Angular 里面所涉及到的很多模块，最常用的几个如下。</p>
<ul>
<li>自动创建组件：<strong>ng generate component MyComponent</strong>，可以简写成<strong>ng g c MyComponent</strong>。创建组件的时候也可以带路径，如 <strong>ng generate component mydir/MyComponent</strong></li>
<li>自动创建指令：ng g d MyDirective</li>
<li>自动创建服务：ng g s MyService</li>
<li>构建项目：ng build，如果你想构建最终的产品版本，可以用 ng build --prod</li>
</ul>
<p>更多的命令和参数请在终端里面敲 ng g --help 仔细查看，尽快熟悉这些工具可以非常显著地提升你的编码效率。</p>
<p><img src="https://images.gitbook.cn/3870ef20-ad13-11e9-8f3f-792c82c0addc" width = "70%" /></p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd002">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<h3 id="-1">一些常见的坑</h3>
<p>@angular/cli 这种“全家桶”式的设计带来了很大的方便，同时也有一些人不太喜欢，因为很多底层的东西被屏蔽掉了，开发者不能天马行空地自由发挥。比如，@angular/cli 把底层 webpack 的配置文件屏蔽掉了，很多喜欢自己手动配 webpack 的开发者就感到很不爽。</p>
<p>对于国内的开发者来说，上面这些其实不是最重要的，国内开发者碰到的坑主要是由两点引起的：</p>
<ul>
<li>第一点是网络问题，比如 node-sass 这个模块你很有可能就安装不上，原因你懂的；</li>
<li>第二点是开发环境导致的问题，国内使用 Windows 平台的开发者比例依然巨大，而 @angular/cli 在 Windows 平台上有一些非常恶心的依赖，比如它需要依赖 Python 环境、Visual Studio 环境，这是因为某些 Node.js 的模块需要下载到你的本地进行源码编译。</li>
</ul>
<p>因此，如果你的开发平台是 Windows，请特别注意：</p>
<ul>
<li>如果你知道如何给 npm 配置代理，也知道如何翻墙，请首选 npm 来安装@angular/cli 。</li>
<li>否则，请使用 cnpm 来安装 @angular/cli，原因有三：（1）cnpm 的缓存服务器在国内，你装东西的速度会快很多；（2）用 cnpm 可以帮你避开某些模块装不上的问题，因为它在服务器上面做了缓存；（3）cnpm 还把一些包都预编译好了缓存在服务端，比如 node-sass。使用 cnpm 不需要在你本地进行源码编译，因此你的机器上可以没有那一大堆麻烦的环境。</li>
<li>推荐装一个 nrm 来自动切换 registry：npm i -g nrm。</li>
<li>如果 cli 安装失败，请手动把 node_modules 目录删掉重试一遍，全局的 @angular/cli 也需要删掉重装，cnpm uninstall -g @angular/cli。</li>
<li>如果 node_modules 删不掉，爆出路径过长之类的错误，请尝试用一些文件粉碎机之类的工具强行删除。这是 npm 的锅，与 Angular 无关。</li>
<li>最新版本的 @angular/cli 经常会有 bug，尤其是在 Windows 平台上面，因此请不要追新版本追太紧。如果你发现了莫名其妙的问题，请尝试降低一个主版本试试。这一点非常重要，很多初学者会非常困惑，代码什么都没改，就升级了一下环境，然后就各种编译报错。如果你愿意，<a href="https://github.com/angular/angular-cli/issues">去官方提 issue 是个很不错的办法</a>。</li>
<li>对于 MAC 用户或者 *nix 用户，请特别注意权限问题，命令前面最好加上 sudo，保证有 root 权限。</li>
<li>无论你用什么开发环境，安装的过程中请仔细看 log。很多朋友没有看 log 的习惯，报错的时候直接懵掉，根本不知道发生了什么。</li>
</ul>
<h3 id="vscode">VS Code</h3>
<p><img src="https://images.gitbook.cn/03569c70-ad1f-11e9-a760-01c165706a91" width = "70%" /></p>
<p>如你所知，一直以来，前端开发领域并没有一款特别好用的开发和调试工具。</p>
<ul>
<li>WebStorm 很强大，但是吃资源很严重。</li>
<li>Sublime Text 插件很多，可惜要收费，而国内的企业还没有养成花钱购买开发工具的习惯。</li>
<li>Chrome 的开发者工具很好用，但是要直接调试 TypeScript 很麻烦。</li>
</ul>
<p>因此，Visual Studio Code（简称 VS Code）才会呈现出爆炸性增长的趋势。它是微软开发的一款<a href="https://github.com/Microsoft/vscode">前端编辑器</a>，完全开源免费。VS Code 底层是 Electron，界面本身是用 TypeScript 开发的。对于 Angular 开发者来说，当然要强烈推荐 VS Code。最值得一提的是，从 1.14 开始，可以直接在 VS Code 里面调试 TypeScript 代码。</p>
<h4 id="-2">第一步：环境配置</h4>
<ul>
<li>确保 Chrome 安装在默认位置。</li>
<li>确保 VS Code 里面安装了 Debugger for Chrome 这个插件。</li>
<li>把 @angular/cli 安装到全局空间 npm install -g @angular/cli，国内用户请使用 cnpm 进行安装。注意，你最好升级到最新版本的 @angular/cli，避免版本兼容问题。</li>
<li>用 @angular/cli 创建新项目 ng new my-app，本来就已经用 @angular/cli 创建的项目请忽略这一步，继续往下走，因为只要是 cli 创建的项目，后面的步骤都是有效的。</li>
<li>用 VS Code 打开项目，进入项目根目录。</li>
</ul>
<h4 id="launchjson">第二步：配置 launch.json</h4>
<p><img src="https://images.gitbook.cn/cf1397f0-ad1f-11e9-b1a9-0994986ea855" alt="enter image description here" />
<img src="" width = "50%" /></p>
<p>请参照以上步骤打开 launch.json 配置文件。</p>
<p><img src="https://images.gitbook.cn/e1549900-ad1f-11e9-b015-0198f673a736" alt="enter image description here" /></p>
<p>请把你本地 launch.json 文件里面的内容改成这样：</p>
<pre>
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome",
            "url": "http://localhost:4200",
            "webRoot": "${workspaceRoot}"
        }
    ]
}
</pre>
<h4 id="debug">第三步：开始 Debug</h4>
<p>在你的 app.component.ts 的构造函数里面打个断点，我本地是这样打断点的：</p>
<p><img src="https://images.gitbook.cn/fa7c91d0-ad1f-11e9-8f3f-792c82c0addc" alt="enter image description here" /></p>
<p>打开终端，进入项目根目录，运行 ng serve 启动项目，<strong>然后从 VS Code 的 debug 界面启动 Chrome</strong>：</p>
<p><img src="https://images.gitbook.cn/0bb4fc80-ad20-11e9-b1a9-0994986ea855" width = "40%" /></p>
<p><strong>注意，你可能需要 F5 刷新一下 Chrome 才能进入断点！</strong></p>
<p><img src="https://images.gitbook.cn/1c6858b0-ad20-11e9-b1a9-0994986ea855" alt="enter image description here" /></p>
<p>VSCode 的插件市场上有大量的插件可供选择，比如彩虹缩进、智能提示、自动补齐标签之类的功能，将会大幅度提升你的开发效率，这里列出了 10 款我自己日常使用的插件供你参考，<a href="http://www.ngfans.net/topic/195/post">详见这里</a>。</p>
<h3 id="webpackbundleanalyzer">webpack-bundle-analyzer</h3>
<p>在真实的业务项目中，我们会用到大量的第三方开源组件，例如图形库 ECharts、组件库 PrimeNG 等。</p>
<p>有很多开发者在引入这些组件库之后，没有注意到体积问题，导致最终编译出来的包体积过大，比如我自己的 OpenWMS 项目，以下是 build 出来的体积：</p>
<p><img src="https://images.gitbook.cn/4924d4a0-ad20-11e9-a760-01c165706a91" width = "65%" /></p>
<p>用 webpack-bundle-analyzer 分析之后可以看到各个模块在编译之后所占的体积：</p>
<p><img src="https://images.gitbook.cn/7312c740-ad20-11e9-a760-01c165706a91" width = "70%" /></p>
<p>可以看到，主要是因为 ECharts 和 PrimeNG 占的体积比较大，建议在使用的时候做一下异步，用不到的组件不要一股脑全部导入进来。</p>
<p><a href="https://github.com/webpack-contrib/webpack-bundle-analyzer">webpack-bundle-analyzer 的用法和详细文档详见这里</a>。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmsd002">点击了解更多《Angular 基础教程》</a></p>
</blockquote>
<h3 id="-3">小结</h3>
<p>目前，无论你使用什么前端框架，都必然要使用到各种 Node.js 工具，Angular 也不例外。</p>
<p>与其他框架不同，Angular 从一开始就走的“全家桶”式的设计思路，因此 @angular/cli 这款工具里面集成了日常开发需要使用的所有 Node 模块，使用 @angular/cli 可以大幅度降低搭建开发环境的难度。</p>
<h3 id="-4">分享交流</h3>
<p>我们为本专栏付费读者创建了微信交流群，以方便更有针对性地讨论专栏相关问题。入群方式请到第 04 篇末尾添加小助手的微信号，并回复关键字。</p>
<p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）<strong>。你的分享不仅帮助他人，更会提升自己。</strong></p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手微信后需要截已购买的图来验证~</p>
</blockquote></div></article>