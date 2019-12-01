---
title: Electron 开发入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>如果应用程序需要操作外部文件，通常会使用文件打开对话框选择这个文件，然后交由程序做进一步处理，文件打开对话框会返回一个或多个选择的文件路径。不过更友好的方式是将文件拖动到程序的窗口或某一个区域上，然后同样会返回一个或多个文件给应用程序，这种行为称为拖拽操作。</p>
<p>本节将会通过两个案例介绍如何实现 Electron 应用的拖拽操作。</p>
<h3 id="141">14.1 拖拽操作：拖放并显示图像</h3>
<p>本节将通过一个简单的案例演示如何实现图像文件的拖放操作，本例的主要功能是将一个图像文件拖拽的程序的某个区域，然后在窗口上按等比例显示图像。</p>
<p>下面先看一下本例的效果，首先运行程序，然后找到一个图像文件，将其拖动到窗口上的红色背景区域，如下图所示。</p>
<p><img src="https://images.gitbook.cn/ea31b6e0-85cc-11e9-aa4b-b9572b5412a0"  width = "60%" /></p>
<p>当拖动的图像处在红色背景区域上方时松手，就会在红色区域下方按等比例显示拖动的图像，如下图所示。</p>
<p><img src="https://images.gitbook.cn/f29e6440-85cc-11e9-992c-6988ddf654f9"  width = "40%" /></p>
<p>Electron 应用拖拽操作本子上是利用了 HTML 的拖拽 API，然后再调用 Electron API 和 Node.js API 再做进一步处理。</p>
<p>拖拽操作要实现下面 2 个核心功能：</p>
<ul>
<li>窗口的某一个区域接收拖进来的文件；</li>
<li>接收文件后，需要将文件的路径返回给应用程序，这一点与打开文件对话框的操作类似。</li>
</ul>
<p>下面看一下本例的主页面的代码。</p>
<p>在 index.html 文件中。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;拖放和显示图像&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;!--  红色背景区域，用于接收拖拽的图像文件 --&gt;
&lt;div id="panel"  style="background: red;width: 50px;height: 50px;"
&gt;&lt;/div&gt;
&lt;p/&gt;
&lt;label&gt;请将图像文件拖动到这个红色区域&lt;/label&gt;
&lt;p/&gt;
&lt;!--  用于显示图像文件 --&gt;
&lt;img id="image"  style="width: auto;height: auto; max-width: 300px;max-height: 300px"/&gt;
&lt;script type="text/javascript"&gt;
    const panel = document.getElementById('panel')
    //  必须设置 ondragover 事件，而且要返回 false，这样才会交由我们自己的代码处理，否则系统会自己处理放下事件（ondrop），也就是说不会再触发 ondrop 事件
    panel.ondragover = () =&gt; {
        return false;
    }
   //  放下事件
    panel.ondrop = (e) =&gt; {
        e.preventDefault()
       //  循环扫描所有拖过来的文件
        for (let f of e.dataTransfer.files) {
            alert(f.path)
            image.src = f.path;
            //  只取第一个文件，然后退出 for 循环
            break;
        }
        return false;
    }

&lt;/script&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>本例将所有的 JavaScript 代码都放在了 index.html 页面中，因此不需要引用任何外部的脚本文件，直接运行 run.js 脚本即可，该脚本在每一个例子中都有，可以从 GitHub下载。</p>
<h3 id="142">14.2 拖拽操作：生成图像的多尺寸图标</h3>
<p>本例稍微复杂一些，通过拖拽一个图像文件（不支持拖拽多个图像文件），将该图像文件变成多个尺寸的图标，如16 × 16、32 × 32、64 × 64 等，效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/fbc47690-85cc-11e9-83a9-9979bff7a6e3"  width = "50%" /></p>
<p>首先看一下本例主页面的代码。</p>
<p>在 index.html 文件中。</p>
<pre><code>&lt;html&gt;
    &lt;head&gt;
        &lt;title&gt;Icon&lt;/title&gt;
        &lt;link rel="stylesheet" href="index.css" /&gt;
        &lt;script src="event.js"&gt;&lt;/script&gt;
    &lt;/head&gt;
    &lt;body&gt;
                &lt;!--  需要将图像拖动到这个 div 上  --&gt;
        &lt;div id="load-icon-holder"&gt;
            &lt;h1&gt;将图像文件拖放到此处&lt;/h1&gt;
            &lt;img src="images/drop-here.png" /&gt;
        &lt;/div&gt;
                &lt;!--  下面的多个 img 标签用于显示不同尺寸的图像  --&gt;
        &lt;div id="icons"&gt;
            &lt;div class="icon-holder"&gt;
                &lt;label&gt;16x16&lt;/label&gt;
                &lt;img class="icon sixteen" /&gt;
            &lt;/div&gt;
            &lt;div class="icon-holder"&gt;
                &lt;label&gt;32x32&lt;/label&gt;
                &lt;img class="icon thirtytwo" /&gt;
            &lt;/div&gt;
            &lt;div class="icon-holder"&gt;
                &lt;label&gt;64x64&lt;/label&gt;
                &lt;img class="icon sixtyfour" /&gt;
            &lt;/div&gt;
            &lt;div class="icon-holder"&gt;
                &lt;label&gt;128x128&lt;/label&gt;
                &lt;img class="icon onetwoeight" /&gt;
            &lt;/div&gt;
            &lt;div class="icon-holder"&gt;
                &lt;label&gt;256x256&lt;/label&gt;
                &lt;img class="icon twofivesix" /&gt;
            &lt;/div&gt;

        &lt;/div&gt;
    &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>index.html 页面使用了 index.css 样式文件，代码如下。</p>
<pre><code>body {
    padding: 0px;
    margin: 0px;
    background: #ddd;
    color: #888;
    font-family: 'Helvetica Neue', 'Arial';
}

#load-icon-holder {
    padding-top: 10px;
    text-align: center;
    top: 0px;
    left: 0px;
    bottom: 0px;
    right: 0px;
    width: 100%;
}

#icons {
    display: none;
}

.icon-holder {
    float: left;
    margin: 1em;
    padding: 5px;
    border: solid 1px #bbb;
    border-radius: 3px;
}

.sixteen {
    width: 16px;
    height: 16px;
}

.thirtytwo {
    width: 32px;
    height: 32px;
}

.sixtyfour {
    width: 64px;
    height: 64px;
}

.onetwoeight {
    width: 128px;
    height: 128px;
}

.twofivesix {
    width: 256px;
    height: 256px;
}

#save {
    margin-top: 1em;
    float: left;
}
</code></pre>
<p>运行程序后，默认的页面如下图所示，需要将图像文件拖动到该页面的图像上（指定区域）。</p>
<p><img src="https://images.gitbook.cn/03ca24c0-85cd-11e9-83f6-9d216a081f8e"  width = "40%" /></p>
<p>index.html 页面中引用了 event.js 脚本文件，在该脚本文件中设置好了相应的事件，并完成拖放操作的处理工作。</p>
<p>在 event.js 中。</p>
<pre><code>function stopDefaultEvent (event) {
    event.preventDefault();
    return false;
}
//  必须设置，否则 ondrop 事件不会被触发
window.ondragover = stopDefaultEvent;

//  显示不同尺寸的图像
function displayImageInIconSet (filePath) {
        //  获取 div 下所有的 img 标签 
    var images = window.document.querySelectorAll('#icons img');
        //  在所有的 img 标签中显示同样的图像
    for (var i=0;i &lt; images.length;i++) {
        images[i].src = filePath;
    }
}
//  设置 div 样式
function displayIconsSet () {
    var iconsArea = window.document.querySelector('#icons');
    iconsArea.style.display = 'block';
}

function init () {
    var loadiconholder = window.document.querySelector('#load-icon-holder');
    //  设置 div 的 ondrop 事件
    loadiconholder.ondrop = function (event) {
        event.preventDefault();
        if (event.dataTransfer.files.length !== 1) {
            alert('只能拖动一个图像文件.');
        } else {
            loadiconholder.style.display = 'none';
            displayIconsSet();
            var file = event.dataTransfer.files[0];
                        //  显示不同尺寸的图像 
            displayImageInIconSet(file.path);
        }
        return false;
    };
}

window.onload = function () {
    init();
};
</code></pre>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>