---
title: Electron 开发入门-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>使用 <code>&lt;webview&gt;</code> 标签可以在窗口中创造另外一个页面。不像 iframe，webview 在与应用程序不同的进程中运行，它与你的网页没有相同的权限，应用程序和嵌入内容之间的所有交互都将是异步的。 </p>
<h3 id="91webwebview">9.1 在 Web 页面中使用 <code>&lt;webview&gt;</code> 标签</h3>
<p><code>&lt;webview&gt;</code> 标签可以直接嵌入到 Web 页面中，代码如下。</p>
<pre><code> &lt;webview id="geekori" src="https://geekori.com" style="width:400px; height:300px" &gt;&lt;/webview&gt;
</code></pre>
<p>装载包含上面代码的页面，就会在当前窗口中嵌入 <a href="https://geekori.com">https://geekori.com</a> 的页面，如下图所示。</p>
<p><img src="https://images.gitbook.cn/87c96230-85ce-11e9-820a-398659fc7dab"  width = "60%" /></p>
<p>不过在上面的代码中，通过样式限制了 <code>&lt;webview&gt;</code> 标签的尺寸，如果要让 <code>&lt;webview&gt;</code> 标签的尺寸自动调整，需要使用下面的代码。</p>
<pre><code>&lt;webview id="geekori" src="https://geekori.com"  style="height:700px" autosize minwidth="576" minheight="400"&gt;&lt;/webview&gt;
</code></pre>
<p>现在对比一下这两种效果。很明显，设为自动尺寸的 <code>&lt;webview&gt;</code> 标签会随着窗口的变化而改变尺寸。</p>
<p><img src="https://images.gitbook.cn/8f445c90-85ce-11e9-8502-ef0df191d484"  width = "60%" /></p>
<h3 id="92">9.2 相应页面的事件</h3>
<p><code>&lt;webview&gt;</code> 标签支持很多事件，例如，did-start-loading 可以监听页面正在装载事件，did-stop-loading 可以监听页面装载完成事件。<code>&lt;webview&gt;</code> 标签使用事件的代码如下。</p>
<pre><code>&lt;script&gt;
    onload = () =&gt; {
        const webview = document.getElementById('geekori');
        const loadstart = () =&gt; {
             console.log('loadstart');
        }
        const loadstop = () =&gt; {
            console.log('loadstop');
        }
        webview.addEventListener('did-start-loading', loadstart)
        webview.addEventListener('did-stop-loading', loadstop)
    }
&lt;/script&gt;
</code></pre>
<p>在这段代码中，添加了上述两个事件，当页面正在装载时和装载完成后都会在 Console 中输出相应的文本。</p>
<h3 id="93nodejsapi">9.3 在页面中使用 Node.js API</h3>
<p>使用 <code>&lt;webview&gt;</code> 标签装载的页面在默认情况下是不能调用 Node.js API 的，但 <code>&lt;webview&gt;</code> 标签添加 nodeintegration 属性后，页面就可以使用 Node.js API 了，读者可以对比下面两个 <code>&lt;webview&gt;</code> 标签。</p>
<pre><code>&lt;webview id="other" src="./other.html" style="width:400px; height:300px" &gt;&lt;/webview&gt;

&lt;webview id="other" src="./other1.html" style="width:400px; height:300px" nodeintegration&gt;&lt;/webview&gt;
</code></pre>
<p>上面两个标签分别装载了 other.html 和 other1.html，由于后一个 <code>&lt;webview&gt;</code> 标签使用了 nodeintegration 属性，因此可以在 other1.html 中访问 Node.js API。</p>
<h3 id="94webviewapi">9.4 <code>&lt;webview&gt;</code> 标签中的 API</h3>
<p><code>&lt;webview&gt;</code> 标签有很多方法，这里介绍一些常用的方法，代码如下。</p>
<pre><code>webview = document.getElementById('geekori');
//装载新的页面
webview.loadURL('https://www.baidu.com');
//重新装载当前页面
webview.reload();
//获取当前页面的标题
console.log(webview.getTitle());
//获取当前页面对应的 URL
console.log(webview.getURL());
const title = webview.getTitle();
//在装载的页面执行 JavaScript 代码
webview.executeJavaScript('console.log("' + title + '");')
//打开调试工具
webview.openDevTools()
</code></pre>
<p>上面代码中使用 console.log 方法只是在当前窗口的调试工具中输出日志，而不会在 webview.openDevTools 方法打开的调试工具中输出任何日志，除非使用 webview.executeJavaScript 方法在 <code>&lt;webview&gt;</code> 标签打开的页面中执行日志输出代码。</p>
<h3 id="95api">9.5 其他窗口 API</h3>
<h4 id="webframe">渲染当前网页（webFrame）</h4>
<p>通过 webFrame，可以渲染当前网页，如放大和缩小当前页面、在获得焦点的文本框中插入文本等。</p>
<pre><code>//让页面放大或缩小整数倍
//webFrame.setZoomLevel(2)

//让页面按一定级别放大和缩小，默认是 0（原始大小），没增加或减少 1，放大或缩小 20%，最大放大到 300%，最小缩小到原来的 50%
webFrame.setZoomLevel(webFrame.getZoomLevel() + 1)

console.log(webFrame.getZoomFactor())
//在获得焦点的文本框中插入文本
webFrame.insertText("hello world");
</code></pre>
<p>下图是让页面放大，并在文本框中插入文本的效果。</p>
<p><img src="https://images.gitbook.cn/967c0c60-85ce-11e9-b968-9b2f7376aaa4"  width = "50%" /></p>
<h4 id="api">屏幕 API</h4>
<p>通过 screen 对象提供的方法，可以获得与屏幕相关的值，下面的代码演示了 screen 对象中常用的方法。</p>
<pre><code>const electron = require('electron')
const {app, BrowserWindow} = electron
const remote = electron.remote;
function onClick_Test() {
    const win = remote.getCurrentWindow();
    //  获取当前屏幕的宽度和高度（单位：像素）
    const {width, height} = electron.screen.getPrimaryDisplay().workAreaSize
    win.setSize(width,height,true)
    console.log('width:' + width);
    console.log('height:' + height);
   win.setPosition(0,0)
    //  获取鼠标的绝对坐标值
    console.log('x：' + electron.screen.getCursorScreenPoint().x)
    console.log('y：' + electron.screen.getCursorScreenPoint().y)
    console.log('菜单栏高度：' + electron.screen.getMenuBarHeight()) // Mac OS X

}
</code></pre>
<p>执行上面的代码，会在日志窗口输出如下图所示的值。</p>
<p><img src="https://images.gitbook.cn/adfcbdd0-85ce-11e9-91fb-3bd59859bbad"  width = "60%" /></p>
<h4 id="">任务栏的进度条</h4>
<p>通过 BrowserWindow.setProgressBar 方法可以在状态栏的应用程序图标上设置进度条，这个功能仅限于Windows，代码如下。</p>
<pre><code>const remote = require('electron').remote;
function onClick_Test() {
    const win = remote.getCurrentWindow();
    win.setProgressBar(0.5)
}
</code></pre>
<p>执行上面的代码，会看到如下图的进度条效果。</p>
<p><img src="https://images.gitbook.cn/b7e70a80-85ce-11e9-8b73-3d3b89e81c98"  width = "30%" /></p>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p>
<h3 id="-1">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>