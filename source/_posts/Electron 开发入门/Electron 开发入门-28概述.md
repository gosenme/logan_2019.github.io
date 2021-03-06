---
title: Electron 开发入门-28
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">概述</h3>
<p>本课主要讲解如何用 C++ 开发 Node.js 和 Electron 本地模块，其中涉及到 3 种技术：Node.js、Electron 和 C++ 语言。Electron 是基于 Node.js 的，允许用 Web 技术（HTML5、JavaScript 和 CSS3）开发桌面应用，也就是说，Node.js 将 JavaScript 从前端转移到了后端，而 Electron 又让 JavaScript 从后端以另一个角度转回的前端（也就是桌面应用）。尽管 Electron 是基于 Node.js 的，但由于与 Node.js 使用了不同的 V8 引擎，因而为 Node.js 开发的本地模块并不能直接用于 Electron，需要重新在 Electron 环境进行编译才可以。</p>
<h3 id="nodejs">Node.js 的模块机制</h3>
<p>在讲解如何用 C++ 开发 Node.js 本地模块之前，应该先了解一下 Node.js 中的模块机制，这样更有助于掌握开发 Node.js 本地模块。</p>
<h4 id="commonjs">CommonJS 的模块规范</h4>
<p>我们知道 Node. js 的根基就是 JavaScript 或者说是 ECMAScript，而 JavaScript 自身是不带模块机制的，因此 CommonJS 规范应运而生。</p>
<p>那么 CommonJS 是如何完成模块的引用和暴露模块成员的呢？</p>
<ul>
<li>引用模块：require</li>
</ul>
<p>require 是一个函数，该函数有一个参数代表模块标识，它的返回值就是其所引用的外部模块所暴露的 API。</p>
<p>讲得直白一点，就是能通过代码 const value = require("workman") 的形式引入 workman 这个模块并将返回值赋给 value，根据 workman 模块导出的成员不同，value 可能是一个函数、对象或一个类。</p>
<ul>
<li>导出模块中的成员：exports</li>
</ul>
<p>exports 对象里面挂载的内容会被暴露到模块外部，也就是说，exports 对象是模块与外界交互的唯一桥梁。</p>
<p>下面给出一个基于 CommonJS 规范的模块和使用模块导出 API 的案例。</p>
<p>calc.js：</p>
<pre><code>//导出函数
exports.add = function(a,b) {
    return a + b;
}

function sub(a,b) {
    return a - b;
}
exports.sub = sub;

class Calc {
    mul(a,b) {
        return a * b;
    }
}
//导出类
exports.Calc = Calc;

//导出对象
exports.calc = new Calc();

//导出变量
exports.value = "hello world";
</code></pre>
<p>TestCalc.js：</p>
<pre><code>var add = require('./calc.js').add;
var {sub,Calc,calc,value} = require('./calc.js')
console.log(add(20,30))
console.log(sub(20,30))
c = new Calc();
console.log(c.mul(12,43))
console.log(calc.mul(20,30))
console.log(value)
</code></pre>
<h3 id="module">module 对象</h3>
<p>一个名为 module 的对象，里面包含了这个模块的一些自带属性，如一个只读的 id 属性。实际上在  Node. js 中，module 对象里面还有一个 exports 对象，其初始指针指向与上面说的 exports 相同，而且模块真正暴露出去的是 module 中的 exports，也就是说，如果我直接替换了 module.exports 对象（module.exports = {}}，那么导出的就是被替换的对象，而不是上面说的 exports了。</p>
<p>那么使用 exports 和使用 module.exports 有什么区别呢？区别就是使用 exports，无法替换 exports，只能往这个对象中添加属性，而使用 module.exports 可以替换 exports 对象。</p>
<p>例如，exports = {} 是不会替换 exports 的，必须使用 module.exports = {}。</p>
<p>下面是一个关于 module 对象的案例。</p>
<p>module.js：</p>
<pre><code>module.exports.add = function(a,b) {
    return a + b;
}

function sub(a,b) {
    return a - b;
}
module.exports.sub = sub;

class Calc {
    mul(a,b) {
        return a * b;
    }
}

module.exports.Calc = Calc;

exports.calc = new Calc();
exports.value = "hello world";

//id 属性
console.log(module)

module.exports = {add:function(a,b){return a+b}}
</code></pre>
<p>TestModule.js：</p>
<pre><code>var add = require('./module').add;
console.log(add(20,30))
</code></pre>
<h3 id="-1">模块搜索路径</h3>
<p>下面先给出一个模块的例子。</p>
<p>mystring.js：</p>
<pre><code>exports.repeatStr = function(str,n) {
    var result = "";
    for(var i = 0; i &lt; n;i++) {
        result += str;
    }
    return result;
}
</code></pre>
<p>testmystring.js：</p>
<pre><code>//加不加 .js 都可以
var repeatStr = require('mystring.js').repeatStr
console.log(repeatStr("a",20))
</code></pre>
<p>如果不指定路径，Node.js 会按下面的顺序搜索模块。</p>
<ul>
<li>当前目录的 node_modules 中是否有 mystring.js。</li>
<li>搜索当前目录的父目录中 node_modules 目录是否有 mystring.js，若没有，继续向上搜索，直到找到 mystring.js 为止。</li>
</ul>
<p>上面的搜索路径只是表面现象，本质上，Node.js 是根据 module.paths 变量中的路径顺序搜索模块文件。</p>
<p>先显示一下 module.paths 变量的内容，代码如下：</p>
<pre><code>console.log(module.paths)
</code></pre>
<p>在 testmystring.js 的最开始情况 paths 变量，代码如下：</p>
<pre><code>module.paths = []
</code></pre>
<p>现在执行 testmystring.js，会抛出异常。</p>
<p>使用下面的代码添加一个路径，代码会正常运行。</p>
<pre><code>module.paths.push("/MyStudio/resources/nodejs_nativemodule/src/basic/node_modules")
</code></pre>
<p>这就意味着可以将模块文件放到任意目录下。</p>
<p>重新设置一下 paths 变量（将 mystring.js 放在任意目录），然后运行 testmystring.js。</p>
<p>下面用绝对路径演示调用上述模块的方法。</p>
<pre><code>var repeatStr = require('/MyStudio/resources/nodejs_nativemodule/documents/MyString.js').repeatStr
</code></pre>
<h3 id="packagejson">package.json 文件与模块搜索</h3>
<p>很多系统模块和第三方模块都放在一个目录中，而且目录中有很多 .js 文件，这是如何做到的呢？</p>
<p>其实这是 Node.js 搜索模块的另一种更复杂的方式，搜索目录中的 package.json 文件（仍然是按  module.paths 中的搜索路径顺序搜索，直到第一次找到模块为止）。</p>
<p>在 node_modules 中创建一个 mystr 目录，然后在该目录创建一个 package.json 文件，并且将 mystring.js 也复制到 mystr 目录中。</p>
<p>然后编写 testmystr.js 文件：</p>
<pre><code>var repeatStr = require('mystr').repeatStr
console.log(repeatStr("a",20))
</code></pre>
<p>如果在搜索路径（node_modules）同时存在带 package.json 的模块和单个文件形式的模块，以带 package.json 的模块为准。</p>
<p>mystr 目录可以在任何目录中，只需要设置 module.paths 变量，代码如下：</p>
<pre><code>module.paths = ['/MyStudio/resources/nodejs_nativemodule/documents']
</code></pre>
<p>用相对或绝对路径也可以，如 ./mystr、/a/b/c/mystr。</p>
<h3 id="-2">模块缓存</h3>
<p>下面给出一个模块的例子。</p>
<p>mystring.js：</p>
<pre><code>console.log("mystring1")
exports.repeatStr = function(str,n) {
    var result = "";
    for(var i = 0; i &lt; n;i++) {
        result += str;
    }
    return "hahah：" + result;
}
</code></pre>
<p>只要路径指向一个模块，不管路径是相对还是绝对，第一次装载，会将模块放入缓存，以后直接从内存中装载。</p>
<p>testmystring.js：</p>
<pre><code>var repeatStr = require('./mystring.js').repeatStr
//会使用缓存
var repeatStr1 = require('./mystring.js').repeatStr
var repeatStr1 = require('/MyStudio/resources/nodejs_nativemodule/src/basic/cache/mystring.js').repeatStr
require('/MyStudio/resources/nodejs_nativemodule/src/basic/mystring.js')

console.log(repeatStr("a",20))
</code></pre>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p></div></article>