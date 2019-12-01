---
title: Electron 开发入门-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在 Electron 中还存在一种创建窗口的方式，就是使用 HTML 5 的 API 创建窗口。在 HTML 5 中提供了 window.open 方法用于打开一个子窗口，该方法返回一个 BrowserWindowProxy 对象，并且打开了一个功能受限的窗口。</p>
<p>window.open 方法的原型如下。</p>
<pre><code>window.open(url[, title] [,attributes)
</code></pre>
<p>参数的说明如下。</p>
<p>（1）url：要打开页面的链接（包括本地页面路径和 Web 链接）。</p>
<p>（2）title：设置要打开页面的标题，如果在要打开页面中已经设置了标题，那么这个参数将被忽略。</p>
<p>（3）attributes：可以设置与窗口相关的一些属性，如窗口的宽度和高度，其中第 1 个参数是必选的，第 2 个和第 3 个参数是可选的。</p>
<h3 id="71open">7.1 用 open 方法创建一个功能受限的子窗口</h3>
<p>使用该方法打开一个本地页面的代码如下。</p>
<pre><code>function onClick_OpenWindow() {
    //  打开本地页面child.html
    win = window.open('./child.html')
}
</code></pre>
<p>运行上面的代码，会看到如下图的效果。</p>
<p><img src="https://images.gitbook.cn/fef188b0-85ce-11e9-8d74-7b09dcbb3496"  width = "50%" /></p>
<p>使用该方法打开一个 Web 页面的代码如下。</p>
<pre><code>function onClick_OpenWindow() {
    //  打开 Web 页面
    win = window.open('https://geekori.com')
}
</code></pre>
<p>通过 open 方法的第 2 个参数可以设置子窗口的标题，通过第 3 个参数可以设置窗口的属性，如宽度和高度。下面的代码为子窗口指定了标题，并重新设置了窗口的宽度和高度。</p>
<pre><code>function onClick_OpenWindow1() {
 // 通过 open 方法指定窗口的标题时，子窗口不能设置 &lt;title&gt; 标签
 win = window.open('./child.html','新的窗口','width=300,height=200')
}
</code></pre>
<p>运行上面的代码，会看到如下图的效果。</p>
<p><img src="https://images.gitbook.cn/ee237890-85ce-11e9-8e05-812dab4fea01"  width = "70%" /></p>
<h3 id="72">7.2 控制子窗口的焦点及关闭子窗口</h3>
<p>BrowserWindowProxy 对象提供了多个方法可以对子窗口进行控制，例如，让子窗口获得焦点和失去焦点、关闭子窗口。</p>
<pre><code>//获得焦点
function onClick_Focus() {
    if(win != undefined) {
       win.focus();
    }
}
//失去焦点
function onClick_Blur() {
    if(win != undefined) {
        win.blur();
    }
}

//关闭子窗口
function onClick_Close() {
    if (win != undefined) {
        //  closed 属性用于判断窗口是否已关闭
        if(win.closed)
        {
            alert('子窗口已经关闭，不需要再关闭');
            return;
        }
        win.close();
    }

}
</code></pre>
<h3 id="73">7.3 显示子窗口的打印对话框</h3>
<p>通过 print 方法可以显示子窗口的对话框，也就是打印对话框中的内容，代码如下。</p>
<pre><code>//  调用子窗口中的打印对话框
function onClick_PrintDialog() {
    if (win != undefined) {
        win.print();
    }
}
</code></pre>
<p>运行上面的代码，会看到如下图所示的打印对话框，通过该打印对话框，可以将当前页面的内容打印出来，或生成 PDF 等格式的文档。</p>
<p><img src="https://images.gitbook.cn/f66126b0-85ce-11e9-94a6-d3ddb4812dc0"  width = "50%" /></p>
<h3 id="74">7.4 完整代码</h3>
<p>本节完整的实现代码如下。</p>
<ul>
<li>index.html（主窗口页面）</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;BrowserWindowProxy与open方法&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;button onclick="onClick_OpenWindow()"&gt;打开子窗口&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_OpenWindow1()"&gt;打开子窗口（设置窗口标题和窗口属性）&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_Focus()"&gt;获得焦点&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_Blur()"&gt;失去焦点&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_Close()"&gt;关闭子窗口&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_PrintDialog()"&gt;打印对话框&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>child.html（子窗口页面）</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
&lt;/head&gt;

&lt;body&gt;
    &lt;h1&gt;子窗口&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>event.js（包含页面的事件代码）</li>
</ul>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;
const ipcMain = remote.ipcMain;
const {ipcRenderer} = require('electron')
ipcMain.on('close', (event, str) =&gt; {
    alert(str);
});
var win;
//  创建并显示一个主窗口
function onClick_OpenWindow() {
    win = window.open('https://geekori.com')
}
//  创建并显示一个主窗口（标题，属性）
function onClick_OpenWindow1() {
    win = window.open('./child.html','新的窗口','width=300,height=200')
}
//  获得焦点
function onClick_Focus() {
    if(win != undefined) {
       win.focus();
    }
}
//  失去焦点
function onClick_Blur() {
    if(win != undefined) {
        win.blur();
    }
}
//  调用子窗口中的打印对话框
function onClick_PrintDialog() {
    if (win != undefined) {
        win.print();
    }
}
//  关闭子窗口
function onClick_Close() {
    if (win != undefined) {
        if(win.closed)
        {
            alert('子窗口已经关闭，不需要再关闭');
            return;
        }
        win.close();
    }
}
</code></pre>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>购买课程后，可扫描以下二维码进群：</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>