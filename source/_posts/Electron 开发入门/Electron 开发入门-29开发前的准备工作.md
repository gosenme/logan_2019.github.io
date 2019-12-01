---
title: Electron 开发入门-29
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">开发前的准备工作</h3>
<p>在开发本地模块之前，需要先安装必要的软件，如编译器、各种工具等。</p>
<p>编译器</p>
<ul>
<li>Windows：Visual Studio 2017</li>
<li>Mac OS X：Clang，安装 XCode 就可以</li>
</ul>
<p>node-gyp 是 Node.js 下的 C++ 扩展构建工具，用 Python 编写（必须是 Python 2.7，建议安装 anaconda 环境），是基于 GYP 来进行工作的（Generate Your Projects），Google 出品的一套构建工具，通过一个 *.gyp 文件生成不同系统所需要的项目文件，（如 Makefile、Visual Studio 项目文件等）以供构建和编译。</p>
<p>需要创建一个 binding.gyp 文件，并进行配置。</p>
<p>使用 node-gyp 的条件：</p>
<ul>
<li>Python 2.7</li>
<li>GCC（tdm-gcc-5.1.0-3）</li>
</ul>
<p>使用 Anaconda 切换到 Python 2.7 后的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/FnyAdyCnYappYJiKRKq8KdISr9VI" width = "75%" /></p>
<p>安装 nody-gyp：</p>
<pre><code>npm install -g node-gyp
</code></pre>
<p>查看 node-gyp 命令：</p>
<pre><code>node-gyp -h
</code></pre>
<h3 id="c">用 C++ 开发第一个本地模块</h3>
<p>这一部分会使用 C++ 语言一步一步地编写我们的第一个本地模块，本节的内容需要 C++ 的基础知识。</p>
<p>首先创建一个 first.cc 文件，用于编写本地模块代码。</p>
<pre><code>#include &lt;node.h&gt;
namespace demo {
//下面的代码用于声明本地模块必要的资源，如类型
using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;dddd
using v8::Object;
using v8::String;
using v8::Value;
//这个函数是要暴露给 Node.js 的，该函数没有参数，只有返回值
//任何一个需要导出的函数都必须有一个 args 参数
void getValue(const FunctionCallbackInfo&lt;Value&gt;&amp; args) {
  Isolate* isolate = args.GetIsolate();
 //返回一个字符串  args.GetReturnValue().Set(String::NewFromUtf8(isolate, "这是我的第一个Node.js扩展"));
}
//用于初始化，加载本地模块时调用
void init(Local&lt;Object&gt; exports) {
  NODE_SET_METHOD(exports, "getValue", getValue);
}
//调用 init 函数
NODE_MODULE(addon, init)
}
</code></pre>
<p>接下来编写本地模块配置文件（binding.gyp），该文件指定了本地模块名称以及需要编译从 C++ 源代码文件名（first.cc）。</p>
<pre><code>{
  "targets": [
    {
      "target_name": "first",
      "sources": [ "first.cc" ]
    }
  ]
}
</code></pre>
<p>编写 package.json 文件，用于指定本地模块的位置。</p>
<p>package.json：</p>
<pre><code>{
  "name": "first",
  "version": "1.0.0",
  "description": "This is my first addon",
  "main": "build/Release/first.node",

  "author": "lining",
  "license": "GPL-3.0",

  "homepage": "geekori.com"
}
</code></pre>
<p>最后编写测试代码调用本地模块。</p>
<p>test.js：</p>
<pre><code>var getValue = require('./').getValue;
console.log(getValue())
</code></pre>
<p>运行 test.js 脚本文件，就可以输出 getValue() 函数的返回值。</p>
<h3 id="nodejselectron">让 Node.js 本地模块在 Electron 中使用</h3>
<p>下图是本地模块文件（first.node）的位置。</p>
<p><img src="https://images.gitbook.cn/89944810-85d7-11e9-869c-43732e86c35f" width = "40%" /></p>
<p>如果要让 Node.js 本地模块在 Electron 中使用，需要重新编译，因为 Node.js 和 Electron 使用了不同版本的 V8 引擎。</p>
<p>重新编译本地模块有下面两种方法：</p>
<p>（1）在 first.cc 所在的目录执行下面的命令</p>
<pre><code>node-gyp rebuild --target=3.0.2 --arch=x64 --dist-url=https://atom.io/download/electron
</code></pre>
<p>（2）在 first.cc 所在的目录执行下面的命令</p>
<pre><code>./node_modules/.bin/electron-rebuild -v 3.0.2
</code></pre>
<p>现在可以在 Electron 中引用 first 模块了，不过要注意，这时在 Node.js 中就无法引用这个本地模块了，因为它们不兼容。</p>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p></div></article>