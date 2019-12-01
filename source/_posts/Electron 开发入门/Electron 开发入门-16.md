---
title: Electron 开发入门-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本例利用 webkitGetUserMedia 方法调用本机的摄像头拍照，该方法是基于 Webkit 内核浏览器专用的。下面先看一下效果。</p>
<p><img src="https://images.gitbook.cn/d0b5d1b0-85cc-11e9-8437-31a8d73a8674"  width = "50%" /></p>
<p>点击页面右下角的按钮，会弹出一个保存对话框，可以将摄像头当前的图像保存成一个 png 格式的图像。</p>
<p>下面先看一下本例的实现代码。</p>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;拍照&lt;/title&gt;
    &lt;link href="index.css" rel="stylesheet" /&gt;
    &lt;link rel="stylesheet" href="css/font-awesome.min.css"&gt;
    &lt;script src="event.js"&gt;&lt;/script&gt;
  &lt;/head&gt;
  &lt;body&gt;
          &lt;!--用于实时显示摄像头拍到的影像--&gt;
      &lt;canvas width="800" height="600"&gt;&lt;/canvas&gt;
         &lt;!--真正的播放摄像头排到的影像--&gt;
      &lt;video autoplay&gt;&lt;/video&gt;
          &lt;!-- 保存按钮 --&gt;
      &lt;div id="takePhoto" onclick="takePhoto()"&gt;
      &lt;i class="fa fa-camera" &gt;&lt;/i&gt;
    &lt;/div&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>本例实现的基本原理是通过 <code>&lt;video&gt;</code> 标签播放摄像头拍到的影像，然后将影像的每一帧绘制到 <code>&lt;canvas&gt;</code> 标签上。</p>
<ul>
<li>event.js</li>
</ul>
<pre><code>const electron = require('electron');
const dialog = electron.remote.dialog;
const fs = require('fs');
let photoData;
let video;
//弹出对话框保存图像
function savePhoto (filePath) {
    if (filePath) {
         //向文件写入 base 64 格式的图像数据
        fs.writeFile(filePath, photoData, 'base64', (err) =&gt; {
            if (err) alert(`保存图像有问题: ${err.message}`);
            photoData = null;
        });
    }
}
//用于初始化视频流
function initialize () {
    video = window.document.querySelector('video');
    let errorCallback = (error) =&gt; {
        console.log(`连接视频流错误: ${error.message}`);
    };

    window.navigator.webkitGetUserMedia({video: true}, (localMediaStream) =&gt; {
        video.src = window.URL.createObjectURL(localMediaStream);
    }, errorCallback);
}
//拍照
function takePhoto () {
    let canvas = window.document.querySelector('canvas');
    //将当前的视频图像绘制在 canvas 上 
    canvas.getContext('2d').drawImage(video, 0, 0, 800, 600);
    //获取  base64 格式的图像数据
    photoData = canvas.toDataURL('image/png').replace(/^data:image\/(png|jpg|jpeg);base64,/, '');
    //显示保存对话框保存图像
    dialog.showSaveDialog({
        title: "保存图像",
        defaultPath: 'face.png',
        buttonLabel: '保存'
    }, savePhoto);
}

window.onload = initialize;
</code></pre>
<p>运行程序后，单击右下角的保存按钮，就会弹出如下图所示的保存对话框，单击“保存”按钮可以保存摄像头当前拍下的图像。</p>
<p><img src="https://images.gitbook.cn/d9c6d560-85cc-11e9-b478-4384352c63d9"  width = "60%" /></p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>