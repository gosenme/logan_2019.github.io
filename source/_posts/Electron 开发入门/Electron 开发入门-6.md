---
title: Electron 开发入门-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Electron 中提供了一个 Dialog 对象，通过该对象的若干个方法，可以显示不同类型的对话框，如打开文件对话框、保存文件对话框、信息对话框、错误对话框等。</p>
<p>获取 Dialog 对象的代码如下：</p>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;
</code></pre>
<p>或使用下面的代码：</p>
<pre><code>const {dialog} = require('electron')
</code></pre>
<p>由于本例还需要从 remote 中获取其他对象，因而使用第一种方式获取 Dialog 对象。</p>
<p>本节课将会讲解如何显示打开对话框，以及相关的设置。打开对话框通过 showOpenDialog 方法显示，该方法的原型如下：</p>
<pre><code>dialog.showOpenDialog([browserWindow, ]options[, callback])
</code></pre>
<p>其中 browserWindow 和 callback 都是可选的，browserWindow 参数允许该对话框将自身附加到父窗口，作为父窗口的模态对话框。callback 是回调函数，用于返回打开文件或目录后的返回值（文件或目录的绝对路径），如果步指定 callback 参数，通过 showOpenDialog 方法返回打开的文件或目录的绝对路径。</p>
<p>options 是必选参数，该参数是一个对象，包含了一些用于设置打开对话框的属性，主要属性的功能及含义如下表所示。</p>
<table>
<thead>
<tr>
<th>属性</th>
<th>数据类型</th>
<th>功能</th>
<th>可选 / 必选</th>
</tr>
</thead>
<tbody>
<tr>
<td>title</td>
<td>String</td>
<td>对话框标题</td>
<td>可选</td>
</tr>
<tr>
<td>defaultPath</td>
<td>String</td>
<td>默认路径</td>
<td>可选</td>
</tr>
<tr>
<td>buttonLabel</td>
<td>String</td>
<td>按钮文本，当为空时，使用默认按钮文本</td>
<td>可选</td>
</tr>
<tr>
<td>filters</td>
<td>Array</td>
<td>过滤器，用于过滤指定类型的文件</td>
<td>可选</td>
</tr>
<tr>
<td>properties</td>
<td>Array</td>
<td>包含对话框的功能，如打开文件、打开目录、多选等</td>
<td>必选</td>
</tr>
<tr>
<td>message</td>
<td>String</td>
<td>将标题显示在打开对话框顶端</td>
<td>可选</td>
</tr>
</tbody>
</table>
<p>下面通过一组案例组合上述属性展示一些常用的打开对话框样式，案例中用于演示对话框的代码都在 event.js 文件中。</p>
<p>在 event.js 文件的开始部分有如下两行代码，用于获取 Dialog 对象。</p>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;
</code></pre>
<h3 id="51">5.1 打开文件对话框</h3>
<p>显示打开文件对话框，只需要将 properties 属性值设为 ['openFile'] 即可，代码如下：</p>
<pre><code>function onClick_OpenFile() {
    const label = document.getElementById('label');
    //  显示打开文件对话框，并将选择的文件显示在页面上
    label.innerText= dialog.showOpenDialog({properties: ['openFile']})
}
</code></pre>
<p>Mac OS X 效果如下：</p>
<p><img src="https://images.gitbook.cn/9c818850-85cf-11e9-a761-d99a3ca26fde"  width = "60%" /></p>
<p>Windows 效果如下：</p>
<p><img src="https://images.gitbook.cn/c8982750-85cf-11e9-8fa4-bd9ee63c82ea"  width = "60%" /></p>
<blockquote>
  <p>PS：如果取消选择，则返回 undefined。</p>
</blockquote>
<h3 id="52">5.2 定制对话框</h3>
<p>通过设置 options 对象中的一些属性，可以设置打开对话框的标题、按钮文本和默认目录，代码如下。</p>
<pre><code>function onClick_CustomOpenFile() {
    const label = document.getElementById('label');
    var options = {};
    //  设置 Windows 版打开对话框的标题
    options.title = '打开文件';
    //  设置 Mac OS X 版本打开对话框的标题
    options.message = '打开我的文件';
    //  设置按钮的文本
    options.buttonLabel = '选择';
    // 设置打开文件对话框的默认路径（当前目录）
    options.defaultPath = '.';
    options.properties = ['openFile'];
    label.innerText= dialog.showOpenDialog(options)
}
</code></pre>
<p>Mac OS X 版的打开文件对话框的标题需要使用 message 属性设置，title 属性只用于设置 Windows 版打开文件对话框的标题。defaultPath 属性设置的是打开文件对话框中用来选中文件后执行打开动作的按钮的文本，Mac OS X 是右下角第 2 个按钮，Windows 是右下角第 1 个按钮。</p>
<p>Mac OS X 效果如下：</p>
<p><img src="https://images.gitbook.cn/d3616250-85cf-11e9-97ff-0f8f0575d166"  width = "60%" /></p>
<p>Windows 效果如下：</p>
<p><img src="https://images.gitbook.cn/daa06520-85cf-11e9-9bcd-97cab7e20a05"  width = "60%" /></p>
<h3 id="53">5.3 选择指定类型的文件</h3>
<p>如果需要打开指定类型的文件，需要设置 filters 属性，例如，下面的代码为打开文件对话框指定了图像文件、视频文件、音频文件等文件类型，文件类型是通过文件扩展名指定的。</p>
<pre><code>function onClick_FileType(){
    const label = document.getElementById('label');
    var options = {};
    options.title = '打开文件';
    options.buttonLabel = '选择';
    options.defaultPath = '.';
    options.properties = ['openFile'];
    //  指定特定的文件类型
    options.filters = [
        {name: '图像文件', extensions: ['jpg', 'png', 'gif']},
        {name: '视频文件', extensions: ['mkv', 'avi', 'mp4']},
        {name: '音频文件', extensions: ['mp3','wav']},
        {name: '所有文件', extensions: ['*']}
    ]
    label.innerText= dialog.showOpenDialog(options)
}
</code></pre>
<p>为打开文件对话框指定文件类型后，在 Mac OS X 版本对话框下部会显示指定的文件类型，如下图所示。</p>
<p><img src="https://images.gitbook.cn/e2848190-85cf-11e9-bc86-1bb1acc67c4c"  width = "60%" /></p>
<p>在 Windows 版本打开文件对话框右下角的列表中会显示指定的文件类型，如下图所示。</p>
<p><img src="https://images.gitbook.cn/e97a9480-85cf-11e9-bac6-b3a9a9571246"  width = "60%" /></p>
<p>在 Mac OS X 下，不管选择哪一个文件类型，当前目录中的文件都会显示，只是文件扩展名不符合当前文件类型的文件无法选择，而在 Windows 下，不符合条件的文件不会显示出来。</p>
<h3 id="54">5.4 打开和创建目录</h3>
<p>如果需要打开目录，而不是文件，properties 属性值需要包含 'openDirectory'。在 Windows 下，鼠标右键单击目录的空白处，就会弹出一个菜单，通过该菜单可以完成很多工作，如在当前目录创建一个子目录。但在 Mac  OS X 下，没有这个弹出菜单，所以需要使用 'createDirectoryr' 属性在对话框左下角添加一个用于创建目录的按钮才能在当前目录中创建子目录，代码如下。</p>
<pre><code>function onClick_OpenAndCreateDirectory() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '打开目录';
    //  createDirectory仅用于Mac OS 系统
    options.properties = ['openDirectory','createDirectory'];
    label.innerText= dialog.showOpenDialog(options)
}
</code></pre>
<p>Mac OS X 效果如下。</p>
<p><img src="https://images.gitbook.cn/f1b95410-85cf-11e9-a710-79bdd5d94ada"  width = "60%" /></p>
<h3 id="55">5.5 选择多个文件和目录</h3>
<p>选择多个文件和目录，需要为 properties 属性指定 'multiSelections' 值，不过 Mac OS X 和 Windows 的表现有些不太一样。如果要想同时选择多个文件和目录，在 Mac OS X 下需要同时为 properties 属性指定 'openFile' 和 'openDirectory'，而在 Windows 下，只需要为 properties 属性指定 'openFile' 即可。如果在 Windows 下指定了 'openDirectory'，不管是否指定 'openFile'，都只能选择目录，而不能显示文件（对话框中根本就不会显示文件），所以如果要让 Mac OS X 和 Windows 都能同时选择文件和目录，需要单独考虑每个操作系统，代码如下：</p>
<pre><code>function onClick_MultiSelection() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '选择多个文件和目录';
    options.message = '选择多个文件和目录';
    //  添加多选属性和打开文件属性
    options.properties = ['openFile','multiSelections'];
    //  如果是Mac OS X，添加打开目录属性
    if (process.platform === 'darwin') {
        options.properties.push('openDirectory');
    }
    label.innerText= dialog.showOpenDialog(options)
}
</code></pre>
<p>Mac OS X 下选择多个文件和目录的效果：</p>
<p><img src="https://images.gitbook.cn/f94a9590-85cf-11e9-8c2b-710c7e079e53"  width = "60%" /></p>
<p>Windows下选择多个文件和目录的效果：</p>
<p><img src="https://images.gitbook.cn/014176b0-85d0-11e9-9916-85895229eaa4"  width = "60%" /></p>
<h3 id="56">5.6 通过回调函数返回选择结果</h3>
<p>showOpenDialog 方法的最后一个参数用于指定一个回调函数，如果指定了回调函数，showOpenDialog 方法就会通过回调函数的第 1 个参数返回选择的文件和目录，该回调函数的第 1 个参数是字符串数组类型的值。</p>
<pre><code>function onClick_Callback() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '选择多个文件和目录';
    options.message = '选择多个文件和目录';

    options.properties = ['openFile','multiSelections'];
    if (process.platform === 'darwin') {
        options.properties.push('openDirectory');
    }
   //  指定回调函数，在回调函数中通过循环获取选择的多个文件和目录
    dialog.showOpenDialog(options,(filePaths) =&gt;{
        for(var i = 0; i &lt; filePaths.length;i++) {
            label.innerText += filePaths[i] + '\r\n';
        }

    });
}
</code></pre>
<h3 id="57">5.7 本例完整的代码</h3>
<p>这一节看一下本例的完整代码，首先是 index.html 页码的代码，该页面用于布局 UI。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;打开对话框&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;

&lt;/head&gt;

&lt;body&gt;
&lt;button onclick="onClick_OpenFile()"&gt;打开文件对话框&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_CustomOpenFile()"&gt;定制打开对话框&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_FileType()"&gt;指定文件类型&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_OpenAndCreateDirectory()"&gt;打开和创建目录&lt;/button&gt;
&lt;br&gt;
&lt;br&gt; 

&lt;button onclick="onClick_MultiSelection()"&gt;选择多个文件或目录&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_Callback()"&gt;通过回调函数返回选择的文件和目录&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;label id="label" style="font-size: large"&gt;&lt;/label&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 index.html 页面上放置了若干个按钮，单击按钮，执行特定的函数，用于演示打开对话框的各种功能，该页面的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/08888fd0-85d0-11e9-927f-613d88d529f5"  width = "60%" /></p>
<p>这些函数都在 event.js 文件中，该文件的完整代码如下：</p>
<pre><code>const remote = require('electron').remote;
const dialog = remote.dialog;

function onClick_OpenFile() {
    const label = document.getElementById('label');
    label.innerText= dialog.showOpenDialog({properties: ['openFile']})
}

function onClick_CustomOpenFile() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '打开文件';
    options.message = '打开我的文件';
    options.buttonLabel = '选择';
    //  Mac OSX 默认目录是桌面
    options.defaultPath = '.';
    options.properties = ['openFile'];
    label.innerText= dialog.showOpenDialog(options)
}

function onClick_FileType(){
    const label = document.getElementById('label');
    var options = {};
    options.title = '打开文件';
    options.buttonLabel = '选择';
    //  Mac OSX 默认目录是桌面
    options.defaultPath = '.';
    options.properties = ['openFile'];
    options.filters = [
        {name: '图像文件', extensions: ['jpg', 'png', 'gif']},
        {name: '视频文件', extensions: ['mkv', 'avi', 'mp4']},
        {name: '音频文件', extensions: ['mp3','wav']},
        {name: '所有文件', extensions: ['*']}
    ]
    label.innerText= dialog.showOpenDialog(options)
}

function onClick_OpenAndCreateDirectory() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '打开目录';
    //  createDirectory仅用于Mac OS 系统
    options.properties = ['openDirectory','createDirectory'];
    label.innerText= dialog.showOpenDialog(options)
}

function onClick_MultiSelection() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '选择多个文件和目录';
    options.message = '选择多个文件和目录';

    options.properties = ['openFile','multiSelections'];
    if (process.platform === 'darwin') {
        options.properties.push('openDirectory');
    }
    label.innerText= dialog.showOpenDialog(options)
}

function onClick_Callback() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '选择多个文件和目录';
    options.message = '选择多个文件和目录';

    options.properties = ['openFile','multiSelections'];
    if (process.platform === 'darwin') {
        options.properties.push('openDirectory');
    }
    dialog.showOpenDialog(options,(filePaths) =&gt;{
        for(var i = 0; i &lt; filePaths.length;i++) {
            label.innerText += filePaths[i] + '\r\n';
        }

    });
}
</code></pre>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>