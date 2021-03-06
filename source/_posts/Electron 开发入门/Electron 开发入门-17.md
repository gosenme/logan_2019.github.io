---
title: Electron 开发入门-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>尽管 Electron 可以开发跨平台桌面应用，但仍然需要考虑不同平台的差异，例如，Mac OS  X 的菜单和 Windows、Linux 的菜单有一定的差异，因此需要单独处理 Mac OS  X 下的菜单，或者在不同操作系统平台下使用不同的样式文件进行布局或设置 UI 风格，在这些情况下，就需要知道当前运行的操作系统类型。</p>
<p>Node.js 本身提供了 os 模块可以用来获取当前操作系统的类型，本例会根据不同的操作系统使用不同的样式文件，并在页面上显示不同的文本。</p>
<p>Mac OS X 下运行的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/b629b500-85cc-11e9-9391-d11d0e880e26"  width = "40%" /></p>
<p>Windows 下运行的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/bf338cc0-85cc-11e9-8880-e5aede292a2f"  width = "50%" /></p>
<p>例子实现步骤如下。</p>
<p>（1）实现主页面（index.html）</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;检测当前操作系统&lt;/title&gt;
&lt;link rel="stylesheet" href="index.css"&gt;
&lt;script src="event.js"&gt;
&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;p&gt;您当前运行的操作系统是 &lt;span id="os-label"&gt;&lt;/span&gt;&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 index.html 页面中放置了一个 <code>&lt;span&gt;</code> 标签，在检测完操作系统类型后，会通过 JavaScript 将相应的信息显示在 <code>&lt;span&gt;</code> 标签中。</p>
<p>（2）实现主页面样式（index.css）</p>
<pre><code>body {
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial','Helvetica','sans serif';
  text-align: center;
}
</code></pre>
<p>（3）实现 Mac OS X 系统下的样式（mac.css）</p>
<p>该样式以不同样式显示文本，Windows 和 Linux 下的样式类似。</p>
<pre><code>body {
  background: #fff;
  color: #3DABEB;
}
</code></pre>
<p>（4）实现 Windows 系统下的样式（windows.css）</p>
<pre><code>body {
  background: #f1f1f1;
  color: #555;
}
</code></pre>
<p>（5）实现 Linux 系统下的样式（linux.css）</p>
<pre><code>body {
  background: #fff;
  color: #729C4A;
}
</code></pre>
<p>（6）编写 event.js 脚本文件</p>
<p>event.js 文件中的代码用于 index.html 页面，在该文件中主要设置了 window 对象的 onload 事件方法，在初始化页面的过程中获取当前操作系统的类型，并根据操作系统类型在页面上显示相应的信息。</p>
<pre><code>'use strict';
//动态创建 link 标签，并指定样式文件
function addStylesheet (stylesheet) {
  var head = document.getElementsByTagName('head')[0];
   //创建 link 标签
  var link = document.createElement('link');
  link.setAttribute('rel','stylesheet');
  //设置 link 标签的 href 属性值
  link.setAttribute('href',stylesheet+'.css');
  //将 link 标签添加到 head 标签中
  head.appendChild(link);
}
//设置 span 标签，让该标签显示相应操作系统的名字
function labelOS (osName) {
  document.getElementById('os-label').innerText = osName;
}
//页面初始化时使用
function initialize () {
  //导入 os 模块
  var os         = require('os');
  //获取平台信息
  var platform     = os.platform();
  //判断操作系统类型
  switch (platform) {
      case 'darwin':    //Mac OS X 系统
        addStylesheet('mac');
          labelOS('macOS');   
        break;
      case 'linux':      //Linux 系统
        addStylesheet('linux');
          labelOS('Linux');
        break;
      case 'win32':     //Windows 系统
        addStylesheet('windows');
          labelOS('Microsoft Windows');
        break;
      default:
        console.log('无法检测您当前的操作系统平台',platform);
  }
}
window.onload = initialize;   //设置 onload 事件方法
</code></pre>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>