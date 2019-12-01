---
title: Electron 开发入门-24
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>尽管 electron-packager-interactive 可以完成大多数命令行参数的输入，但仍然需要通过命令行操作，也是比较麻烦，尤其是遇到输入路径的情况下，还需要复制粘贴的过程，因此最好的方法是直接利用 Electron 自己来编写一个可视化的打包工具。</p>
<p>使用 Electron 编写可视化打包工具的基本原理就是通过 Node.js 的进程 API 调用 electron-packager 命令，并自动设置相应的命令行参数。本例只设置了 asar、操作系统等命令行参数，读者可以用同样的方式设置其他的命令行参数。下面先看一下效果。</p>
<p>Windows 的效果：</p>
<p><img src="https://images.gitbook.cn/FoBtV1TQrw3qLnde9b6gc2TMt3tg" width = "60%" /></p>
<p>Mac OS X 下的效果：</p>
<p><img src="https://images.gitbook.cn/FjUad9mUcDjRt8Iz0rNVXwtS518d" width = "60%" /></p>
<p>单击“打包”按钮后，如果打包成功，会在“打包”按钮下方显示打包成功的提示信息。</p>
<p>下面是本例的完整实现代码。</p>
<p>index.html（主页面）：</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--指定页面编码格式--&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--指定页头信息--&gt;
  &lt;title&gt;electron-packager API打包&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body onload="onload()"&gt;
    &lt;button onclick="onClick_SelectProject()"&gt;选择Electron工程目录&lt;/button&gt;
    &lt;p/&gt;
    Electron工程目录：&lt;label id="label_source"&gt;&lt;/label&gt;
    &lt;p/&gt;
    &lt;button onclick="onClick_SelectOut()"&gt;选择输出目录&lt;/button&gt;
    &lt;p/&gt;
    输出目录：&lt;label id="label_out"&gt;&lt;/label&gt;
    &lt;p/&gt;
    &lt;label&gt;应用程序名称：&lt;/label&gt;&lt;input id="appName"/&gt;
    &lt;p/&gt;
    &lt;label&gt;asar：&lt;/label&gt;&lt;input type="checkbox" id="asar"/&gt;
    &lt;p/&gt;
    &lt;label&gt;为哪些操作系统打包&lt;/label&gt;
    &lt;p/&gt;
    &lt;label&gt;Mac OS X&lt;/label&gt;：&lt;input type="checkbox" id="mac"/&gt;
    &lt;p/&gt;
    &lt;label&gt;Windows&lt;/label&gt;：&lt;input type="checkbox" id="windows"/&gt;
    &lt;p/&gt;
    &lt;label&gt;Linux&lt;/label&gt;：&lt;input type="checkbox" id="linux"/&gt;
    &lt;p/&gt;
    &lt;button onclick="onClick_Package()"&gt;打包&lt;/button&gt;
     &lt;p/&gt;
    &lt;label id="packager_status" style="color:red"&gt;&lt;/label&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>event.js：</p>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;
var spawn = require('child_process').execFile;

function onload() {
    //如果是 Windows 平台，禁用 mac 选项
    if (process.platform == 'win32') {
        mac.disabled = true;
    }
}
//选择 Electron 工程目录
function onClick_SelectProject() {
    var options = {};
    options.title = '选择Electron工程目录';
    options.properties = ['openDirectory'];
    label_source.innerText= dialog.showOpenDialog(options)
}
//选择输出目录
function onClick_SelectOut() {
    var options = {};
    options.title = '选择输出目录';
    options.properties = ['openDirectory','createDirectory'];
    //  显示打开目录对话框
    label_out.innerText= dialog.showOpenDialog(options)
}
//开始打包
function onClick_Package() {
    //根据用户的选择和输入，生成 electron-packager 的命令行参数
    const args = [];
    //设置打包需要的各种参数
    args.push(label_source.innerText);
    args.push(appName.value);
    args.push('--out=' + label_out.innerText);
    args.push('--electron-version=3.0.2');
    if(asar.checked) {
        args.push('--asar');
    }
    var os = '';
    //检测是否要为苹果生成打包文件
    if(mac.checked) {
        os += 'darwin';
    }
    //检测是否要为 Windows 生成打包文件
    if(windows.checked) {
        if(os !='') {
            os += ',';
        }
        os += 'win32';
    }
    //检测是否要为 Linux 生成打包文件
    if(linux.checked) {
        if(os !='') {
            os += ',';
        }
        os += 'linux';
    }
    //设置操作系统平台
    if(os != '') {
        args.push('--platform=' + os);
    }
    var cmd = 'electron-packager';
    //如果是 Windows，应该执行 electron-packager.cmd
    if(process.platform == 'win32') {
        cmd += '.cmd';
    }
    //开始执行 electron-packager 命令打包 Electron 应用
    const e = spawn(cmd,args,(error, stdout, stderr) =&gt; {
        //打包出错
        if (error) {
            console.error('stderr', stderr);
        } else {  //打包成功
            packager_status.innerText = '打包成功';
        }

    })
    packager_status.innerText = '正在打包，请稍后...';

}
</code></pre>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a>。</p></div></article>