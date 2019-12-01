---
title: Electron 开发入门-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在 Electron 中通过 clipboard 对象操作剪贴板，目前主要支持如下几种类型的数据：</p>
<ul>
<li>纯文本</li>
<li>HTML 代码</li>
<li>RTF 文档</li>
<li>图像</li>
</ul>
<p>通过 readxxx 和 writexxx 方法，可以分别从剪贴板读取和写入上述 4 个类型的数据，其中 xxx 是 Text、HTML、RTF 和 Image。下面的例子演示了如何在 Electron 应用中操作剪贴板。</p>
<p>（1）首先编写主页面 index.html 的代码。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--指定页面编码格式--&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--指定页头信息--&gt;
  &lt;title&gt;剪贴板演示&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;

&lt;/head&gt;
&lt;body onload="init()"&gt;
    &lt;button id="button_read_text" onclick="onClick_WriteText()"&gt;复制文本&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_write_text" onclick="onClick_ReadText()"&gt;粘贴文本&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_read_html" onclick="onClick_WriteHTML()"&gt;复制HTML&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_write_html" onclick="onClick_ReadHTML()"&gt;粘贴HTML&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_read_rtf" onclick="onClick_WriteRTF()"&gt;复制RTF&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_write_rtf" onclick="onClick_ReadRTF()"&gt;粘贴RTF&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_read_image" onclick="onClick_WriteImage()"&gt;复制图像&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_write_image" onclick="onClick_ReadImage()"&gt;粘贴图像&lt;/button&gt;
    &lt;p/&gt;
  &lt;!--可编辑的 div 标签，用于复制和粘贴文本--&gt;
   &lt;div id="text" contenteditable="true" style="width: 500px;height: 500px; border: 1px solid #ccc; padding: 5px;"&gt;&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在主页面上放置了多个按钮，分别用来读写剪贴板中的上述 4 个类型的数据，最下方是一个可编辑的 <code>&lt;div&gt;</code> 标签，用于显示带格式的文本，剪贴板会从这里复制，并且会将剪贴板中的文本数据显示在这个 <code>&lt;div&gt;</code> 标签中，页面的效果如下图所示。</p>
<p>Mac OS X 的效果。</p>
<p><img src="https://images.gitbook.cn/b06f4bd0-85cb-11e9-80d0-37dc17eff04b"  width = "50%" /></p>
<p>Windows 的效果。</p>
<p><img src="https://images.gitbook.cn/bf148880-85cb-11e9-b2ff-d9800d5ec581"  width = "50%" /></p>
<p>（2）下面编写 event.js 脚本文件，在该文件中包含了所有操作剪贴板的代码。</p>
<pre><code>const {remote} = require('electron')
//在 Renderer 进程中需要使用 remote 获取 nativeImage、Tray 和 clipboard
const nativeImage =  remote.nativeImage;
const Tray = remote.Tray;
const clipboard = remote.clipboard;
function init() {
    //为 div 标签设置初始化的内容
    text.innerHTML = '&lt;h1&gt;hello world&lt;/h1&gt;'
}
//向剪贴板写入文本
function onClick_WriteText() {
    clipboard.writeText(text.innerHTML);
    alert('已经成功将文本复制到剪贴板！')
}
//从剪贴板读取文本
function onClick_ReadText() {
    text.innerHTML = text.readText();
}
//向剪贴板写入 HTML 代码
function onClick_WriteHTML(){
    clipboard.writeHTML(text.innerHTML);
    alert('已经成功将HTML复制到剪贴板！')
}
//从剪贴板读取 HTML 代码
function onClick_ReadHTML(){
    alert(clipboard.readHTML())
    text.innerHTML = clipboard.readHTML();
}
//向剪贴板写入 RTF 代码
function onClick_WriteRTF() {
    clipboard.writeRTF(text.innerHTML);
    alert('已经成功将RTF复制到剪贴板！')
}
//从剪贴板读取 RTF 代码
function onClick_ReadRTF() {
    text.innerText = clipboard.readRTF();
    alert(clipboard.readRTF())
}
//将本地图像文件保存在剪贴板
function onClick_WriteImage() {
    const image = nativeImage.createFromPath('./images/pythonbook.png');
    clipboard.writeImage(image);
    alert('已经成功将Image复制到剪贴板！')
}
//从剪贴板读取图像
function onClick_ReadImage() {
    const image = clipboard.readImage()
    const appIcon = new Tray(image)
    console.log(appIcon)
}
</code></pre>
<p>本例中读写剪贴板中的文本、HTML 和 RTF 格式数据的方式类似，只是在读写图像时需要使用 nativeImage 对象，在从剪贴板读取图像后，创建了一个托盘图标，将该图像显示在托盘上，如下所示。</p>
<p>Mac OS X 的效果。</p>
<p><img src="https://images.gitbook.cn/cd3022d0-85cb-11e9-9ee5-4baa5672fc75"  width = "50%" /></p>
<p>Windows 的效果。</p>
<p><img src="https://images.gitbook.cn/d640ff70-85cb-11e9-8399-8d8154c01333"  width = "40%" /></p>
<p>由于写入剪贴板的图像比较大，在 Mac OS X 托盘上是按全尺寸显示的，因而看起来图像很大，而在 Windows 下不管图像多大，都是按正常尺寸显示的，因此托盘图标看起来是正常的。</p>
<p>另外，在 Renderer 进程中使用剪贴板要使用 remote 对象获取 clipboard 对象以及其他相关对象，否则剪贴板可能会无法正常工作。</p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>购买课程后，可扫描以下二维码进群：</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>