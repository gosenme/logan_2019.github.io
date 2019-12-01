---
title: Angular 基础教程-51
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>主要内容：</p>
<ul>
<li>Node.js</li>
<li>Angular CLI</li>
<li>创建第一个项目</li>
<li>一些常见的坑</li>
<li>VS Code</li>
<li>webpack-bundle-analyzer</li>
</ul>
<h3 id="nodejs">Node.js</h3>
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
<li>CSS 的预处理也从 Less 发展到了 Sass 等。</li>
<li>自动化测试一直是前端开发中的一个巨大痛点，由于前端在运行时严重依赖浏览器环境，导致我们一直无法像测试后端代码那样可以去编写测试用例。Node.js 出现之后，终于有了像 Karma + Jasmine 这样的单元测试组合，也有了基于 WebDriverJS 这样的可以和浏览器进行通讯的集成测试神器。</li>
</ul>
<p>就前端开发目前整体的状态来说，无论使用什么框架，Node.js、Webpack、Sass、Karma + Jasmine、WebDriverJS 这个组合是无论如何绕不过去的。</p>
<h3 id="angularcli">Angular CLI</h3>
<p><img src="https://images.gitbook.cn/4b1f3900-e3c5-11e8-a1c4-731a3e37324c"  width = "70%" /></p>
<p>在开发 Angular 应用的时候，当然也离不开大量基于 Node.js 的工具，我们需要 TypeScript Compiler、Webpack、Karma、Jasmine、Protracter 等模块。</p>
<p>有相关经验的开发者都知道，自己从头开始去搭建一套基于 Webpack 的开发环境是一件非常麻烦的事情，很多初学者在搭建环境这一步就消耗了过多的精力，导致学习热情受到了沉重的打击。</p>
<p>当团队规模比较大的时候，在每个人的机器上配置环境需要消耗大量的时间。有一些团队为了避开这个坑，利用 Docker 来做开发环境的同步和版本升级，看起来也是一个非常不错的方案。</p>
<p>Angular 项目组从一开始就注意到了这个问题，所以有了 Angular CLI 这个神器，它的底层基于 Webpack，集成了以上提到的所有 Node.js 组件，你只要安装好 Angular CLI 就够了，不需要自己从头一步一步安装那些 Node.js 插件。</p>
<p>当然，在安装 Angular CLI 之前需要先把 Node.js 安装好，请到官方网站<a href="https://nodejs.org/">（点击这里跳转到官方网站）</a> 下载安装包，安装过程和普通软件没有区别。安装好 Node.js 之后就可以安装 Angular CLI 了，由于 npm 会自动访问海外的服务器，因而强烈推荐使用 cnpm 进行安装：</p>
<pre><code>npm i -g cnpm --registry=https://registry.npm.taobao.org

cnpm i -g @angular/cli
</code></pre>
<p>cnpm 是淘宝发布的一款工具，会自动把 npm 上面的所有包定时同步到国内的服务器上来，cnpm 本身也是一款 Node.js 模块。</p>
<p>Angular CLI 安装成功之后终端里面将会多出一个名叫 ng 的命令，敲下 ng，将会显示完整的帮助文档：</p>
<p><img src="https://images.gitbook.cn/94ab0ae0-e3c5-11e8-a397-15a3bf78ee55" alt="enter image description here" /></p>
<h3 id="">创建第一个项目</h3>
<p>我们来创建第一个入门项目 HelloAngular，请在终端里面运行如下命令：</p>
<pre><code>ng new HelloAngular
</code></pre>
<p>@angular/cli 将会自动帮你把目录结构创建好，并且会自动生成一些模板化的文件，就像这样：</p>
<p><img src="https://images.gitbook.cn/a23847e0-e3c5-11e8-a1c4-731a3e37324c"  width = "50%" /></p>
<p><strong>请特别注意</strong>：@angular/cli 在自动生成好项目骨架之后，会立即自动使用 npm 来安装所依赖的 Node 模块，因此这里我们要用组合键 Ctrl + C 终止掉它，然后自己进入项目的根目录，使用 cnpm 命令来进行安装。</p>
<p><img src="https://images.gitbook.cn/b0b2f220-e3c5-11e8-bfed-8d6b896efba7" alt="enter image description here" /></p>
<p>安装完成之后，使用 ng serve 命令启动项目：</p>
<p><img src="https://images.gitbook.cn/bd719480-e3c5-11e8-a1c4-731a3e37324c" alt="enter image description here" /></p>
<p>打开浏览器，访问默认的 4200 端口，若看到以下界面就说明环境 OK 了：</p>
<p><img src="https://images.gitbook.cn/cb88e910-e3c5-11e8-bfed-8d6b896efba7"  width = "50%" /></p>
<p>请注意以下几点：</p>
<ul>
<li><strong>这里是 serve，不是 server</strong>，我看到一些初学者经常坑在这个地方。</li>
<li>如果需要修改端口号，可以用 ng serve --port **** 命令来进行指定。</li>
<li>ng serve --open 可以自动打开默认的浏览器。</li>
<li>如果想让编译的包更小一些，可以使用 ng serve --prod，@angular/cli 会启用 TreeShaking 特性，加了参数之后编译的过程也会慢很多。因此，在正常的开发过程里面请不要加 --prod 参数。</li>
<li>ng serve 是在内存里面生成项目，如果你想看到项目编译之后的产物，请运行 ng build。构建最终产品版本可以加参数，ng build --prod。</li>
</ul>
<p>ng 提供了很多非常好用的工具，除了可以利用 ng new 命令来自动创建项目骨架之外，它还可以帮助我们创建 Angular 里面所涉及到的很多模块，最常用的有以下几个。</p>
<ul>
<li>自动创建组件（<strong>ng generate component MyComponent</strong>，<strong>ng g c MyComponent</strong>），创建组件的时候也可以带路径，如 <strong>ng generate component mydir / MyComponent</strong>。</li>
<li>自动创建指令：ng g d MyDirective。</li>
<li>自动创建服务：ng g s MyService。</li>
<li>构建项目：ng build，如果想构建最终的产品版本，可以用 ng build --prod 命令。</li>
</ul>
<p>更多的命令和参数请在终端里面输入 ng 命令仔细查看，尽快熟悉这些工具可以非常显著地提升编码效率。</p>
<h3 id="-1">一些常见的坑</h3>
<p>@angular/cli 这种“全家桶”式的设计带来了很大的方便，同时也有一些读者不太喜欢，因为很多底层的东西被屏蔽掉了，开发者不能天马行空的自由发挥。比如，@angular/cli 把底层 Webpack 的配置文件屏蔽掉了，很多喜欢自己手动配 Webpack 的开发者就会感到很不爽。</p>
<p>对于国内的开发者来说，上面这些其实不是最重要的，国内开发者碰到的坑主要是由以下两点问题引起的：</p>
<ul>
<li>网络问题，比如 node-sass 这个模块很有可能就装不上，原因你懂的；</li>
<li>开发环境导致的问题，国内使用 Windows 平台的开发者比例依然巨大，而 @angular/cli 在 Windows 平台上有一些非常恶心的依赖，比如它需要依赖 Python 环境、Visual Studio 环境。</li>
</ul>
<p>因此，如果你的开发平台是 Windows，请特别注意以下几点。</p>
<ul>
<li>如果你知道如何给 npm 配置代理，也知道如何翻墙，请首选 npm 来安装 Angular CLI。否则，请使用 cnpm 来安装 Angular CLI，原因有三：<ul>
<li>cnpm 的缓存服务器在国内，装东西的速度会快很多；</li>
<li>用 cnpm 可以帮你避开某些模块装不上的问题，因为它在服务器上面做了缓存；</li>
<li>cnpm 还把一些包都预编译好了缓存在服务端，比如 node-sass，使用 cnpm 不需要在本地进行源码编译，因此你的机器上可以没有那一大堆麻烦的环境。</li></ul></li>
<li>如果安装失败，请手动把 node_modules 目录删掉重试一遍，全局的 @angular/cli 也需要删掉重装，cnpm uninstall -g @angular/cli。</li>
<li>如果 node_modules 删不掉，报出路径过长等之类的错误，请尝试用一些文件粉碎机之类的工具强行删除，这是 npm 的锅，与 Angular 无关。</li>
<li>最新版本的 Angular CLI 经常会有 bug，尤其是在 Windows 平台上面，请不要追新版本太紧，如果发现了莫名其妙的问题，请尝试降低一个主版本试试。这一点非常重要，很多初学者会非常困惑，代码什么都没改，就升级了一下环境，然后会有各种编译报错。如果你愿意，去官方 <a href="https://github.com/angular/angular-cli/issues">（点击这里跳转到官网）</a> 提 issue 是个很不错的办法。</li>
<li>对于 MAC 用户或者 *nix 用户，请特别注意权限问题，命令前面最好加上 sudo，保证有 root 权限。</li>
<li>无论你用什么开发环境，安装的过程中请仔细看 log，很多读者没有看 log 的习惯，报错的时候直接懵掉，根本不知道发生了什么。</li>
</ul>
<h3 id="vscode">VS Code</h3>
<p><img src="https://images.gitbook.cn/053306a0-e3c6-11e8-8e04-b95633cc2286"  width = "80%" /></p>
<p>如你所知，一直以来，前端开发领域并没有一款特别好用的开发和调试工具。</p>
<ul>
<li>WebStorm 很强大，但是吃资源很严重。</li>
<li>Sublime Text 插件很多，可惜要收费，而国内的企业还没有养成花钱购买开发工具的习惯。</li>
<li>Chrome 的开发者工具很好用，但是要直接调试 TypeScript 很麻烦。</li>
</ul>
<p>因此，<a href="https://github.com/Microsoft/vscode">Visual Studio Code（VS Code）才会呈现出爆炸性增长的趋势</a>，它是微软开发的一款前端编辑器，完全开源免费。VS Code 底层是 Electron，界面本身是用 TypeScript 开发的。对于 Angular 开发者来说，当然要强烈推荐 VS Code。最值得一提的是，从 1.14 开始，可以直接在 VS Code 里面调试 TypeScript 代码。</p>
<h4 id="-2">环境配置</h4>
<ul>
<li>确保 Chrome 安装在默认位置</li>
<li>确保 VS Code 里面安装了 Debugger for Chrome 这个插件</li>
<li>把 Angular CLI 安装到全局空间 npm install -g @angular/cli，国内用户请使用 cnpm 进行安装。注意，最好升级到最新版本的 Angular CLI，避免版本兼容问题。</li>
<li>用 @angular/cli 创建新项目 ng new my-app ，本来就已经用 @angular/cli 创建的项目请忽略这一步，继续往下走，因为只要是 CLI 创建的项目，后面的步骤都是有效的。</li>
<li>用 VS Code 打开项目，进入项目根目录。</li>
</ul>
<h4 id="launchjson">配置 launch.json</h4>
<p><img src="https://images.gitbook.cn/17a9e4c0-e3c6-11e8-a1c4-731a3e37324c"  width = "80%" /></p>
<p>请参照以上步骤打开 launch.json 配置文件。</p>
<p><img src="https://images.gitbook.cn/241955b0-e3c6-11e8-a1c4-731a3e37324c" alt="enter image description here" /></p>
<p>请把本地 launch.json 文件里面的内容改成这样：</p>
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
<h4 id="debug">开始 Debug</h4>
<p>在 app.component.ts 的构造函数里面打个断点，我本地是这样打断点的：</p>
<p><img src="https://images.gitbook.cn/3268aa30-e3c6-11e8-8e04-b95633cc2286" alt="enter image description here" /></p>
<p>打开终端，进入项目根目录，运行 ng serve 启动项目，<strong>然后从 VS Code 的 debug 界面启动 Chrome</strong>：</p>
<p><img src="https://images.gitbook.cn/3fe915f0-e3c6-11e8-a397-15a3bf78ee55"  width = "50%" /></p>
<p><strong>注意，可能需要 F5 刷新一下 Chrome 才能进入断点！</strong></p>
<p><img src="https://images.gitbook.cn/4ba5b1a0-e3c6-11e8-8e04-b95633cc2286" alt="enter image description here" /></p>
<p>市场上有大量的 VSCode 插件可供选择，比如彩虹缩进、智能提示、自动补齐标签之类的功能，将会大幅度提升开发效率，这里列出了 10 款我自己日常使用的插件供你参考，<a href="http://www.ngfans.net/topic/195/post">点击这里查看详情</a>。</p>
<h3 id="webpackbundleanalyzer">webpack-bundle-analyzer</h3>
<p>在真实的业务项目中，我们会用到大量的第三方开源组件，如图形库 ECharts、组件库 PrimeNG 等。</p>
<p>有很多开发者在引入这些组件库之后，没有注意到体积问题，导致最终编译出来的包体积过大，比如我自己的 OpenWMS 项目，以下是 build 出来的体积：</p>
<p><img src="https://images.gitbook.cn/62ea1d60-e3c6-11e8-a397-15a3bf78ee55" alt="enter image description here" /></p>
<p>用 webpack-bundle-analyzer 分析之后可以看到各个模块在编译之后所占的体积：</p>
<p><img src="https://images.gitbook.cn/7416c840-e3c6-11e8-bfed-8d6b896efba7" alt="enter image description here" /></p>
<p>可以看到，主要是因为 ECharts 和 PrimeNG 占的体积比较大，建议在使用的时候做一下异步，用不到的组件不要一股脑全部导入进来。</p>
<p>webpack-bundle-analyzer 的用法和详细文档 <a href="https://github.com/webpack-contrib/webpack-bundle-analyzer">请点击这里查看</a>。</p>
<h3 id="-3">小结</h3>
<p>目前，无论使用什么前端框架，都必然要使用到各种 Node.js 工具，Angular 也不例外。</p>
<p>与其他框架不同，Angular 从一开始走的就是“全家桶”式的设计思路，Angular CLI 这款工具里面集成了日常开发需要使用的所有 Node 模块，使用 @angular/cli 可以大幅度降低搭建开发环境的难度。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5bebdaf22c33167c317cc285&utm_source=dmqqsd001">点击了解更多《Angular 基础教程》</a></p>
</blockquote></div></article>