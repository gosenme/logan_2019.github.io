---
title: Electron 开发入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>用 open 方法打开的子窗口也会面临和其他窗口交互的问题，交互无外乎互相传递数据，并接收其他窗口传递过来的数据。</p>
<h3 id="81">8.1 最简单的传递接收数据</h3>
<p>向 open 方法创建的子窗口传递数据有多种方法，其中之一就是使用 BrowserWindowProxy.postMessage 方法，该方法可以向指定的窗口传递任意类型的数据和来源（origin），如果不知来源，可以使用星号 '*' 代替，关于来源是什么，以及如何使用，在后面的内容会详细介绍。</p>
<p>如果只是想向另外的窗口传递数据，需要使用下面的代码。</p>
<pre><code>function onClick_Message() {
    //向 win 指定的窗口传递数据
    win.postMessage('my data', '*');
}

var win;
//创建并显示一个主窗口
function onClick_OpenWindow() {
    //用 open 方法打开一个子窗口
    win = window.open('./child.html','接收消息','width=300,height=200')
}
</code></pre>
<p>其中 postMessage 方法的第 1 个参数用于指定要传递的数据，第 2 个参数是来源，一个字符串类型的值，如果不知道来源，可以使用 '*'。</p>
<p>下面的代码在 event.js 文件中，onLoad() 函数是 child.html 的 load() 函数，当 child.html 页面装载完会调用 onLoad() 函数，该函数添加了一个 message 事件的 listener，当使用 postMessage 方法传递数据时，接收数据的页面就会触发 message 事件，并通过事件回调函数参数的 data 属性得到传过来的数据。</p>
<pre><code>var label
function onLoad() {
    label = document.getElementById('label');
    window.addEventListener('message', function (e) {
        //e.data 表示传递过来的数据，就是 postMessage 函数的第 1 个参数值
        label.innerText = e.data
    });
}
</code></pre>
<h3 id="82">8.2 子窗口返回数据</h3>
<p>如果想子窗口返回数据，仍然可以使用 ipcRenderer 和 ipcMain，代码如下。</p>
<ul>
<li>子窗口（event.js）</li>
</ul>
<pre><code>function onClick_Close() {
    const win  =  remote.getCurrentWindow();
    //  返回数据，其中 close 是事件名
    ipcRenderer.send('close','窗口已经关闭');
    win.close();
}
</code></pre>
<ul>
<li>主窗口（event.js）</li>
</ul>
<pre><code>//  在主线程中接收 close 事件
ipcMain.on('close', (event, str) =&gt; {
    //  str参数就是字窗口返回的数据 
    alert(str);
});
</code></pre>
<p>运行上面的程序，显示子窗口，然后关闭子窗口，会发现在主窗口显示了一个如下图的对话框，表明子窗口已经成功返回了数据。</p>
<p><img src="https://images.gitbook.cn/c80d68f0-85ce-11e9-af77-b9700dee5b73"  width = "70%" /></p>
<p>前面提到过“来源（origin）”，其实这个来源就是谁使用 URL 打开的新的子窗口，这个“谁”在本例中就是指 index.html 所在的域名（domain），下面来看个例子。</p>
<p>我们可以使用下面的代码获取来源。</p>
<pre><code>    window.addEventListener('message', function (e) {
        //获取来源
        alert(e.origin);
    });
</code></pre>
<p>如果 index.html 在本地，那么来源永远是 “file://”，如下图所示。</p>
<p><img src="https://images.gitbook.cn/cfec7c50-85ce-11e9-8a60-7162c597d604"  width = "50%" /></p>
<p>如果 index.html 页面在服务端，那么来源就是域名，例如，index.html 的 Web 地址是：<a href="https://geekori.com/test/index.html">https://geekori.com/test/index.html</a>。</p>
<p>现在修改 index.js 文件的代码如下。</p>
<pre><code>const {app, BrowserWindow} = require('electron');
function createWindow () {
win = new BrowserWindow({show:false});
// 装载 Web 页面
 win.loadURL('https://geekori.com/test/index.html')
win.on('ready-to-show', () =&gt; {
     win.show()
});
win.on('closed', () =&gt; {
  console.log('closed');
  win = null;
})
}
app.on('ready', createWindow)
</code></pre>
<p>由于 child.html 文件使用的是相对路径，因此使用的是 child.html 在服务端的版本，不过这里使用 child.html 在本地的路径也可以。在上传文件时，为了避免麻烦，建议将当前工程中所有的文件上传到服务端。</p>
<p>现在重新创建子窗口，并传递数据，会发现子窗口的 label 标签显示了传递过来的值。</p>
<p><img src="https://images.gitbook.cn/d846da30-85ce-11e9-8044-59559e84f4fd"  width = "30%" /></p>
<h3 id="83eval">8.3 使用 eval 方法向子窗口传递数据</h3>
<p>除了 postMessage 方法外，还可以用 eval 方法向子窗口传递数据。eval 方法用于执行子窗口中的代码，也就是说，使用 eval 方法执行的 JavaScript 代码的上下文是子窗口的，这就意味着代码中可以访问子窗口中的组件，比如本例创建的 label 组件。</p>
<p>eval 方法的使用非常简单，只需要为 eval 传入要执行的 JavaScript 代码即可，如下面代码所示。</p>
<pre><code>function onClick_Eval() {
    win.eval('label.innerText="hello world"')
}
</code></pre>
<p>这里的 label 是在子窗口中获得的 label 组件的对象。</p>
<h3 id="84">8.4 完整代码</h3>
<p>本节给出案例实现的完整代码，首先是 child.html 页面的代码。</p>
<ul>
<li>child.html</li>
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

&lt;body onload="onLoad()"&gt;
&lt;h1&gt;子窗口&lt;/h1&gt;
&lt;p/&gt;
&lt;button onclick="onClick_Close()"&gt;关闭&lt;/button&gt;
&lt;label id="label"&gt;&lt;/label&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;!--指定页面编码格式 --&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;!--指定页头信息--&gt;
    &lt;title&gt;BrowserWindowProxy与open方法&lt;/title&gt;
    &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;button onclick="onClick_OpenWindow()"&gt;打开子窗口&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_Message()"&gt;向子窗口发送消息&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;

&lt;button onclick="onClick_Eval()"&gt;向子eval方法窗口发送消息&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;label id="label" style="font-size: large"&gt;&lt;/label&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>event.js</li>
</ul>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;
const ipcMain = remote.ipcMain;
const {ipcRenderer} = require('electron')
ipcMain.on('close', (event, str) =&gt; {
    alert(str);
});
var win;
//创建并显示一个主窗口
function onClick_OpenWindow() {
    //win = window.open('https://geekori.com/test/child.html')
    win = window.open('./child.html','接收消息','width=300,height=200')
}

function onClick_Message() {

    win.postMessage('abcd', '*');

}

var label
function onLoad() {
    label = document.getElementById('label');
    window.addEventListener('message', function (e) {
        alert(e.origin);
        label.innerText = e.data
    });
}
function onClick_Close() {
    const win  =  remote.getCurrentWindow();
    ipcRenderer.send('close','窗口已经关闭');
    win.close();
}

function onClick_Eval() {
    //通过 eval 方法设置 child 窗口中的 label 标签
    win.eval('label.innerText="hello world"')
}
</code></pre>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>