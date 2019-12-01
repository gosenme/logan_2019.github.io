---
title: 透视前端工程化-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="1webpack">1 Webpack 的特点</h3>
<p><img src="https://images.gitbook.cn/Fj8gLfdJUoiwprQUT6GVLFSqlhZq" alt="avatar" /></p>
<p>图片来源于网络</p>
<p>Webpack 是一款强大的打包工具。在 Webpack 中一切皆模块。Webpack 官网的 banner 图完美地诠释了这一理念。Webpack 从一个入口文件开始递归地分析模块的依赖关系，根据依赖关系将这些模块打包成一个或多个文件。</p>
<p>目前几乎所有的前端构建和开发都是采用 Webpack 。因为 Webpack 有强大的社区生态，每月 Webpack 的下载量超过百万。通过 loader、plugin 支持 Webpack 与主流的前端框架和语言进行集成，比如 Vue、React、TypeScript。</p>
<ul>
<li><strong>支持所有的模块化</strong> 可以对 ES6 模块、commonjs 模块、AMD 模块等所有标准的模块进行打包。</li>
<li><strong>code splitting</strong> 可以将代码打成多个 chunk，按需加载，意味着我们的站点无需等待整个 js 资源下载完成之后才能交互，可以大大提升速度。</li>
<li><strong>强大灵活的插件系统</strong> Webpack 提供了很多内置的插件，包括其自身也是架构在插件系统上可以满足所有的打包需求。</li>
<li><strong>loader</strong> 借助 loader 预处理非 js 资源，Webpack 可以打包所有的静态资源。</li>
</ul>
<h3 id="2webpack">2 Webpack 构建流程</h3>
<p>Webpack 的构建流程是一种事件流机制。整个构建流程可以看成是一个流水线，每个环节负责单一的任务，处理完将进入下一个环节。Webpack 会在每个环节上发布事件，供内置的和自定义的插件有机会干预 Webpack 的构建过程，控制 Webpack 的构建结果。Webpack 的基本的构建流程图如下：</p>
<p><img src="https://images.gitbook.cn/Fiv2S00oV0nN3zdiVLgClRcX0DJm" alt="webpack 构建流程图" /></p>
<ul>
<li><strong>初始化</strong> 读取 Webpack 配置文件和 shell 脚本中的参数，将参数合并后初始化 Webpack ，生成 <code>Compiler</code>  对象。</li>
<li><strong>开始编译</strong> 执行 <code>Compiler</code> 的 run 方法开始执行编译。</li>
<li><strong>编译完成</strong> 从入口文件开始，调用配置中的 loader 对模块进行编译，并梳理出模块间的依赖关系，直至所有的模块编译完成。</li>
<li><strong>资源输出</strong> 根据入口与模块间的依赖关系，将上一步编译完成的内容组装成一个个的 <code>chunk</code> （代码块），然后把 <code>chunk</code> 加入到等待输出的资源列表中。</li>
<li><strong>完成</strong> 确定好输出资源后，根据指定的输出路径和文件名配置，将资源写入到磁盘的文件系统中，完成整个构建过程。</li>
</ul>
<h3 id="3">3 核心概念</h3>
<h5 id=""><strong>入口</strong></h5>
<p>入口是 Webpack 进行构建的起点，Webpack 在构建过程中从入口文件开始，递归地编译模块，并分析模块间的依赖关系，最终得出依赖图。Webpack 依据该依赖图对模块进行组装，输出到最终的 bundle 文件中。</p>
<p>我们可以在 Webpack 的配置文件中配置 entry 属性，来指定入口文件，入口文件可以是一个也可以指定多个。</p>
<p>我们来看一个例子：</p>
<pre><code>// webpack.config.js
module.exports = {
  entry: './src/app.js'
};
</code></pre>
<p>配置多个入口的场景常见于多页应用中。如果配置多个入口可以这样：</p>
<pre><code>// webpack.config.js
module.exports = {
  entry: {
    pageOne: './src/pageOne/app.js',
    pageTwo: './src/pageTwo/app.js'
  }
};
</code></pre>
<h5 id="-1"><strong>输出</strong></h5>
<p>配置 output 选项可以指示 Webpack 如何去输出、在哪里输出我们的静态资源文件。 </p>
<p>我们通过一个例子来看一下 output 如何使用：</p>
<pre><code>// webpack.config.js
module.exports = {
  output: {
    filename: 'bundle.js',
    path: './dist'
  }
};
</code></pre>
<p>上例中，我们指示 Webpack 最终的输出文件名为 <code>bundle.js</code> ，输出的目录为 <code>./dist</code>。</p>
<h5 id="loader"><strong>loader</strong></h5>
<p><strong>loader 的使用</strong></p>
<p>Webpack 本身是不能处理非 JS 资源的，但我们却可以在 Webpack 中引入 css、图片、字体等非 js 文件。例如:</p>
<pre><code>// app.js
import Styles from './styles.css';
</code></pre>
<p>那么 Webpack 是如何实现的呢？</p>
<p>Webpack 中使用 loader 对非 js 文件进行转换。loader 可以在我们 <code>import</code> 或者加载模块时，对文件进行预处理，将非 js 的文件内容，最终转换成 js 代码。</p>
<p>loader 有三种使用方式：</p>
<ul>
<li><strong>配置</strong> 在 webpack.config.js 文件中指定</li>
<li><strong>内联</strong> 在每个 <code>import</code> 语句中线上指定</li>
<li><strong>CLI</strong> 在 shell 命令中指定。</li>
</ul>
<p>在实际的应用中，绝大数都是采用配置的方式来使用，一方面在配置文件中，可以非常直观地看到某种类型的文件使用了什么 loader，另一方面，在项目复杂的情况下，便于进行维护。</p>
<p>我们通过一个简单的例子来看一下 loader 的使用：</p>
<pre><code>// webpack.config.js
module.exports = {
 module: {
    rules: [
      { test: /\.css$/, use: 'css-loader' }
    ]
  }
};
</code></pre>
<p>我们需要告诉 Webpack 当遇到 css 文件的时候，使用 <code>css-loader</code> 进行预处理。这里由于 css-loader 是单独的 npm 模块，使用前我们需要先进行安装：</p>
<pre><code>npm install --save-dev css-loader
</code></pre>
<p><strong>常用的 loader</strong></p>
<p>Webpack 可以处理任何非 JS 语言，得益于社区提供的丰富的 loader，日常开发中所使用到的 loader，都可以在社区找到。这里对一些常用的 loader 进行简要的说明。</p>
<ul>
<li><strong>babel-loader</strong> 将 ES2015+ 代码转译为 ES5。</li>
<li><strong>ts-loader</strong> 将 TypeScript 代码转译为 ES5。</li>
<li><strong>css-loader</strong>  解析 <code>@import</code> 和 <code>url()</code>，并对引用的依赖进行解析。</li>
<li><strong>style-loader</strong> 在 HTML 中注入 <code>&lt;style&gt;</code> 标签将 css 添加到 DOM 中。通常与 <code>css-loader</code> 结合使用。</li>
<li><strong>sass-loader</strong> 加载 sass/scss 文件并编译成 css。</li>
<li><strong>postcss-loader</strong> 使用 PostCSS 加载和转译 css 文件。</li>
<li><strong>html-loader</strong> 将 HTML 导出为字符串。</li>
<li><strong>vue-loader</strong> 加载和转译 Vue 组件。</li>
<li><strong>url-loader</strong> 和 <code>file-loader</code> 一样，但如果文件小于配置的限制值，可以返回 <code>data URL</code>。</li>
<li><strong>file-loader</strong> 将文件提取到输出目录，并返回相对路径。</li>
</ul>
<h5 id="plugin"><strong>plugin</strong></h5>
<p><strong>插件的使用</strong></p>
<p>插件是 Webpack 的非常重要的功能，Webpack 本身也是建立在插件系统之上的。插件机制极大增强了 Webpack 的功能，为 Webpack 增加了足够的灵活性。通过插件，我们可以在 Webpack 的构建过程中，引入自己的操作，干预构建结果。</p>
<p>我们通过一个示例来看一下插件的使用：</p>
<pre><code>// webpack.config.js
const HtmlWebpackPlugin = require('html-webpack -plugin'); 
const webpack = require('webpack'); 

const config = {
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new HtmlWebpackPlugin({template: './src/index.html'})
  ]
};

module.exports = config;
</code></pre>
<p>示例中，我们用到了两个插件，一个是内置的 <code>UglifyJsPlugin</code> 插件，该插件对 js 进行压缩，减小文件的体积。一个是外部插件 <code>HtmlWebpackPlugin</code>，用来自动生成入口文件，并将最新的资源注入到 HTML 中。</p>
<p><strong>常用的插件</strong></p>
<ul>
<li><strong>HtmlWebpackPlugin</strong> 自动生成入口文件，并将最新的资源注入到 HTML 中。</li>
<li><strong>CommonsChunkPlugin</strong> 用以创建独立文件，常用来提取多个模块中的公共模块。</li>
<li><strong>DefinePlugin</strong> 用以定义在编译时使用的全局常量。</li>
<li><strong>DllPlugin</strong> 拆分 bundle 减少不必要的构建。</li>
<li><strong>ExtractTextWebpackPlugin</strong> 将文本从 bundle 中提取到单独的文件中。常见的场景是从 bundle 中将 CSS 提取到独立的 css 文件中。</li>
<li><strong>HotModuleReplacementPlugin</strong> 在运行过程中替换、添加或删除模块，而无需重新加载整个页面。</li>
<li><strong>UglifyjsWebpackPlugin</strong> 对 js 进行压缩，减小文件的体积。</li>
<li><strong>CopyWebpackPlugin</strong> 将单个文件或整个目录复制到构建目录。一个常用的场景是将项目中的静态图片不经构建直接复制到构建后的目录。</li>
</ul>
<h3 id="4webpack">4 如何使用 Webpack</h3>
<p>下面我们通过一个简单的例子来看一下 Webpack 的使用。这里假定你已经安装了最新版本的 Node.js 和 npm，因为使用旧版本可能会遇到各种问题。</p>
<h4 id="41">4.1 安装</h4>
<p>创建 webpack-demo 目录，初始化 npm，并且在 webpack-demo 目录中安装 Webpack 和 webpack-cli：</p>
<pre><code>mkdir webpack-demo &amp;&amp; cd webpack-demo
npm init -y
npm install webpack  webpack-cli --save-dev
</code></pre>
<p>webpack-cli 用来在命令行中运行 Webpack 。这里建议本地安装 Webpack 和 webpack-cli，因为全局安装的话，Webpack 的升级会影响到所有的项目。</p>
<p>接下来我们先在项目中新增一些目录和文件：</p>
<pre><code>webpack-demo
├── package.json
├── dist
├── index.html
└── src
    └── index.js
</code></pre>
<p>index.html 内容如下：</p>
<pre><code>&lt;!doctype html&gt;
&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;webpack-demo&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;script src="./src/index.js"&gt;&lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>src/index.js 内容如下:</p>
<pre><code>function createEl() {
  var element = document.createElement('div')
  element.innerHTML = 'hello world'

  return element;
}

document.body.appendChild(createEl());
</code></pre>
<h4 id="42">4.2 第一次构建</h4>
<p>在命令行运行：</p>
<pre><code>./node_modules/.bin/webpack 

Hash: 2353b0d3d427eaa8a18a
Version: webpack  4.29.6
Time: 175ms
Built at: 2019-04-03 22:08:36
  Asset   Size  Chunks             Chunk Names
main.js  1 KiB       0  [emitted]  main
Entrypoint main = main.js
[0] ./src/index.js 175 bytes {0} [built]
</code></pre>
<p>大家可以发现，我们并没有在配置文件中指定打包的入口和输出的出口，也没有在命令行中指定配置参数，但可以看到在 ./dist 目录下新增了一个 main.js。这是因为 Webpack 配置中 entry 的默认值为 ./src，出口的默认目录是 ./dist。</p>
<pre><code>webpack-demo
├── package.json
├── dist
|    └── main.js
├── index.html
└── src
     └── index.js
</code></pre>
<p>构建后的项目目录中新增了 main.js。</p>
<pre><code>&lt;!doctype html&gt;
&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;webpack-demo&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;script src="./dist/main.js"&gt;&lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>我们现在将 index.html 中的脚本引用修改为构建后的文件 ./dist/main.js，在浏览器预览，如果一切正常应该可以看到页面上会输出文本 <code>hello world</code>。</p>
<h4 id="43">4.3 使用配置文件</h4>
<p>对于简单的构建，Webpack 基本可以做到零配置。但对于复杂的单页应用而言，则需要使用 Webpack 的配置文件来提供个性化的功能。</p>
<p>首先我们在项目根目录下新增 <code>webpack.config.js</code> 文件:</p>
<pre><code>// webpack.config.js
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  }
};
</code></pre>
<p>在配置文件中，通过 <code>entry</code> 指定了入口文件为 <code>./src/index.js</code>，通过 output 指定了输出的目录为 <code>./dist</code>，输出的文件名为 <code>bundle.js</code>。目录结构更新如下：</p>
<pre><code>webpack-demo
├── package.json
├── Webpack .config.js
├── index.html
├── dist
|    └── bundle.js
└── src
     └── index.js
</code></pre>
<p>同时为了调用简单，我们在 package.json 文件中设置快捷命令来调用 <code>./node_modules/.bin/Webpack</code>。</p>
<pre><code>// package.json
{
  "scripts": {
    "build": "webpack"
  }
}
</code></pre>
<p>再次执行构建命令：</p>
<pre><code>npm run build
&gt; Webpack-demo@1.0.0 build C:\work\tech\webpack-demo
&gt; webpack 

Hash: d0fa6b1e011af414e622
Version: webpack  4.29.6
Time: 157ms
Built at: 2019-04-03 22:42:50
 Asset   Size  Chunks             Chunk Names
bundle.js  1 KiB       0  [emitted]  main
Entrypoint main = bundle.js
[0] ./src/index.js 175 bytes {0} [built]
</code></pre>
<p>将  <code>index.html</code>  中的 script 引用链接修改为 <code>./dist/bundle.js</code>，在浏览器中预览页面，不出意外的话会输出文本 <code>hello world</code>。</p>
<h4 id="44">4.4 使用插件</h4>
<p>我们发现在构建的过程中，如果构建后的资源名称发生了变化，index.html 中对资源的引用会被动地跟着修改，非常不方便，我们引入 HtmlWebpackPlugin 来帮助我们自动生成入口文件，自动将生成的资源文件注入 index.html 中。</p>
<p>安装：</p>
<pre><code>npm install --save-dev html-webpack-plugin
</code></pre>
<p>配置：</p>
<pre><code>const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist")
  },
  plugins: [new HtmlWebpackPlugin()]
};
</code></pre>
<p>在配置文件中，我们引入插件，并在 plugins 选项中，将插件实例化后添加到数组中。该插件会自动生成 index.html，因此原目录中的 index.html 文件可以删除。</p>
<pre><code>webpack-demo
├── package.json
├── webpack.config.js
├── dist
|    └── bundle.js
└── src
     └── index.js
</code></pre>
<p>再次执行构建命令：</p>
<pre><code>$ npm run build

&gt; webpack-demo@1.0.0 build C:\work\tech\webpack-demo
&gt; webpack 

Hash: 39dc7567ef99a69140e7
Version: webpack  4.29.6
Time: 1241ms
Built at: 2019-04-03 22:53:44
     Asset       Size  Chunks             Chunk Names
 bundle.js      1 KiB       0  [emitted]  main
index.html  182 bytes          [emitted]
Entrypoint main = bundle.js
[0] ./src/index.js 175 bytes {0} [built]
</code></pre>
<p>命令执行后我们发现我们的 ./dist 下多了一个 index.html 文件，并且 index.html 中的资源引用被自动更新为了 <code>&lt;script type="text/javascript" src="bundle.js"&gt;&lt;/script&gt;</code>。</p>
<h4 id="45loadercss">4.5 使用 loader 处理 css 文件</h4>
<p>为了使 Webpack 可以处理 import 进来的 css 文件，我们需要安装并配置 <code>style-loader</code>  和  <code>css-loader</code>。</p>
<pre><code>npm install --save-dev style-loader css-loader
</code></pre>
<p>修改 Webpack 的配置如下：</p>
<pre><code>const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist")
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  plugins: [new HtmlWebpackPlugin()]
};
</code></pre>
<p>如此一来，当 Webpack 匹配到后缀为 .css 的文件都会使用 css-loader 和 style-loader 进行处理。</p>
<p>接下来我们在 ./src 目录下新增一个样式文件 <code>main.css</code>。在样式中，设置文本的字体颜色为红色。</p>
<pre><code>// main.css
div{color: red}
</code></pre>
<p>紧接着我们在 ./src/index.js 中引用 main.css：</p>
<pre><code>import "./main.css";

function createEl() {
  var element = document.createElement("div");
  element.innerHTML = "hello world";

  return element;
}

document.body.appendChild(createEl());
</code></pre>
<p>执行构建命令：</p>
<pre><code>$ npm run build

&gt; webpack-demo@1.0.0 build C:\work\tech\webpack-demo
&gt; webpack 

Hash: f9fcb8cfd689f4b96ce6
Version: Webpack  4.29.6
Time: 2672ms
Built at: 2019-04-03 23:24:40
     Asset       Size  Chunks             Chunk Names
 bundle.js   6.85 KiB       0  [emitted]  main
index.html  182 bytes          [emitted]
Entrypoint main = bundle.js
[0] ./src/index.js 199 bytes {0} [built]
[1] ./src/main.css 1.05 KiB {0} [built]
[2] ./node_modules/css-loader/dist/cjs.js!./src/main.css 170 bytes {0} [built]
    + 3 hidden modules
</code></pre>
<p>在浏览器预览，不出意外字体的颜色已经变成了红色，打开浏览器调试工具，可以看到在 <code>&lt;head&gt;</code> 标签里插入了一个 <code>&lt;style&gt;</code> 标签。</p>
<pre><code>&lt;style type="text/css"&gt;
  div {
    color: red;
  }
&lt;/style&gt;
</code></pre>
<p>通过以上完整的示例，我们演示了 Webpack 的核心的几个配置的使用方式，我们对 Webpack 的使用应该有了一个基本的认识。</p>
<p>Webpack 中还有很多其他有用的配置项，篇幅原因不做详细的介绍。大家可以查阅 <a href="https://www.webpackjs.com/configuration/">官方文档</a> 自行配置和练习。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5cf77250ce53ed3f49faf0e5&utm_source=wcsd001">点击了解《透视前端工程化》</a>。</p>
</blockquote>
<h3 id="-2">总结</h3>
<p>本节我们对 Webpack 进行了总体的介绍。借助 loader、Webpack 可以处理一切资源，JS 的、非 JS 的，都可以。</p>
<p>通过插件，我们可以在 Webpack 的构建过程中的每个事件节点加入自己的行为，来影响 Webpack 的构建。对 Webpack 的使用有了认识后，接下来我们要以之为基础搭建起项目的基本框架。</p>
<blockquote>
  <p>注意！！！
  为了方便学习和技术交流，特意创建了《透视前端工程化》的读者群，入群方式放在<a href="https://gitbook.cn/m/mazi/columns/5cf77250ce53ed3f49faf0e5/topics/5d0c77c3820bf61799b753e1">第 4 篇</a>文末，欢迎已购本课程的同学入群交流。</p>
</blockquote></div></article>