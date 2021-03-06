---
title: Electron 开发入门-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="61">6.1 保存对话框</h3>
<p>使用 showSaveDialog 方法可以显示保存对话框，保存对话框与打开对话框类似，需要自己输入要保存的用户名，当然，也可以选择已经存储的文件名，不过这样一来就会覆盖这个文件。</p>
<p>这里要强调一点，保存对话框只是提供了要保存的文件名，至于是否保存文件、以何种文件格式保存，保存对话框并不负责，需要另外编写代码解决。showSaveDialog 方法与 showOpenDialog 方法的参数类似，下面的代码演示了如何用 showOpenDialog 方法来显示保存对话框返回的文件名。</p>
<pre><code>function onClick_Save() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '保存文件';
    options.buttonLabel = '保存';
    options.defaultPath = '.';
    //Only Mac OS X，输入文件名文本框左侧的标签文本
    options.nameFieldLabel = '请输入要保存的文件名';
    //是否显示标记文本框，默认值为True
    //options.showsTagField = false;
    //设置要过滤的图像类型  
    options.filters = [
        {name: '图像文件', extensions: ['jpg', 'png', 'gif']},
        {name: '视频文件', extensions: ['mkv', 'avi', 'mp4']},
        {name: '音频文件', extensions: ['mp3','wav']},
        {name: '所有文件', extensions: ['*']}
    ]
    //显示保存文件对话框，并将返回的文件名显示页面上
    label.innerText= dialog.showSaveDialog(options)
}
</code></pre>
<p>运行上面的代码会显示如下图所示保存文件对话框。</p>
<p><img src="https://images.gitbook.cn/0f6d5a20-85cf-11e9-bad9-554e49b75597"  width = "60%" /></p>
<p>如果将标记文本框隐藏会呈现如下图所示的效果。</p>
<p><img src="https://images.gitbook.cn/17342a90-85cf-11e9-8b5e-19343160f289"  width = "60%" /></p>
<p>点击输入文件名文本框右侧向下箭头按钮，会显示如下图所示的对话框。</p>
<p><img src="https://images.gitbook.cn/1dfff930-85cf-11e9-9f5d-ff9d5a0e3ccf"  width = "60%" /></p>
<p>当选择一个已经存在的文件会弹出确认是否覆盖的对话框，如下图所示。</p>
<p><img src="https://images.gitbook.cn/289022d0-85cf-11e9-86c3-219dbd82e842"  width = "60%" /></p>
<p>单击替换按钮，保存文件对话框会关闭，通过 showSaveDialog 方法返回选择的文件名。</p>
<p>下图是 Windows 版本的保存对话框。</p>
<p><img src="https://images.gitbook.cn/30dd6150-85cf-11e9-a046-4d4b556c47f1"  width = "60%" /></p>
<p>showSaveDialog 方法同样也可以指定回调函数，下面的代码通过回调函数得到保存对话框返回的文件名。</p>
<pre><code>function onClick_SaveCallback() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '保存文件';
    options.buttonLabel = '保存';
    options.defaultPath = '.';
    //  Only Mac OS X
    options.nameFieldLabel = '请输入要保存的文件名';
    // 
    options.showsTagField = false;
    options.filters = [
        {name: '图像文件', extensions: ['jpg', 'png', 'gif']},
        {name: '视频文件', extensions: ['mkv', 'avi', 'mp4']},
        {name: '音频文件', extensions: ['mp3','wav']},
        {name: '所有文件', extensions: ['*']}
    ]
    dialog.showSaveDialog(options,(filename) =&gt; {
        label.innerText = filename;
    })
}
</code></pre>
<p>下面先看一下 index.html 文件的代码。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;保存对话框&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;button onclick="onClick_Save()"&gt;保存文件对话框&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;
&lt;button onclick="onClick_SaveCallback()"&gt;保存文件对话框（回调函数）&lt;/button&gt;
&lt;br&gt;
&lt;br&gt;

&lt;label id="label" style="font-size: large"&gt;&lt;/label&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在该文件中放置了两个按钮，一个按钮用于显示保存文件对话框，另外一个按钮用于显示通过回调函数获取文件名的保存文件对话框。</p>
<p>运行程序会看到如下的界面。当在文件保存对话框中输入或选择一个文件后，会返回这个文件的绝对路径，并将这个绝对路径显示在当前页面中。</p>
<p><img src="https://images.gitbook.cn/3967a8d0-85cf-11e9-a867-434383eaaf26"  width = "60%" /></p>
<h3 id="62">6.2 显示对话框消息</h3>
<p>通过 showMessageBox 方法，可以显示各种类型的对话框。该方法的参数与前面介绍的方法类似。</p>
<h4 id="">最简单的消息对话框</h4>
<p>最简单的消息对话框，需要设置对话框标题和显示的消息。标题使用 title 属性设置，消息使用 message 属性设置，实现代码如下。</p>
<pre><code>function onClick_MessageBox() {
    const label = document.getElementById('label');
    var options = {};
    options.title = '信息';
    options.message = '这是一个信息提示框';
    label.innerText= dialog.showMessageBox(options)
}
</code></pre>
<p>运行这个程序会显示如下图的对话框。</p>
<p><img src="https://images.gitbook.cn/4114afb0-85cf-11e9-a5aa-39b56a9a9a17"  width = "50%" /></p>
<h4 id="-1">设置对话框的默认图标</h4>
<p>对话框默认显示 Electron 的图标，但可以通过 icon 属性设置图标，代码如下。</p>
<pre><code>function onClick_MessageBox() {

    var options = {};
    options.title = '信息';
    options.message = '这是一个信息提示框';
    //  设置对话框的图标
    options.icon = '../../../images//note.png';   
    dialog.showMessageBox(options)
}
</code></pre>
<p>运行上面的代码会看到如下图所示的对话框，不管图像的尺寸有多大，总会在对话框左侧显示合适大小的图标。</p>
<p><img src="https://images.gitbook.cn/4895eba0-85cf-11e9-bc89-7d149aab7a8f"  width = "50%" /></p>
<h4 id="-2">设置对话框的类型</h4>
<p>对话框有多种类型，如信息对话框、错误对话框、询问对话框和警告对话框，这些对话框的类型通过 type 属性设置，其值如下。</p>
<ul>
<li>默认对话框：none</li>
<li>信息对话框：info</li>
<li>错误对话框：error</li>
<li>询问对话框：question</li>
<li>警告对话框：warning</li>
</ul>
<p>设置对话框类型的代码如下。</p>
<pre><code>function onClick_MessageBox() {
    var options = {};
    options.title = '警告';
    options.message = '这是一个警告提示框';
   // 设置对话框类型
    options.type = 'warning';
    dialog.showMessageBox(options)
}
</code></pre>
<p>运行上面的代码会看到如下图所示对话框。</p>
<p><img src="https://images.gitbook.cn/5026b7f0-85cf-11e9-a0e1-795743d83c11"  width = "50%" /></p>
<p>在 Mac OS X 系统下的警告对话框会将系统默认的图标覆盖在警告图标上面。而在 Windows 下只显示警告图标，如下图所示。</p>
<p><img src="https://images.gitbook.cn/589bf0d0-85cf-11e9-92c2-4f3fed672673"  width = "50%" /></p>
<p>如果在 Mac OS X 下为对话框设置了新的图标，新的图标仍然会覆盖在警告图标的上面，如下图。</p>
<p><img src="https://images.gitbook.cn/5f786140-85cf-11e9-b515-1fe34e4250c2"  width = "50%" /></p>
<p>在 Windows 下为对话框设置了新的图标，新图标会替换警告图标。</p>
<h4 id="-3">设置对话框的按钮</h4>
<p>通过 buttons 属性可以设置对话框的按钮，默认只显示一个按钮，buttons 属性是字符串数组类型，每一个数组元素代表一个按钮的文本，下面的代码为信息框添加 5 个按钮。</p>
<pre><code>function onClick_MessageBox() {
    var options = {};
    options.title = '警告';
    options.message = '这是一个警告提示框';
    options.icon = '../../../images//note.png';
    options.type = 'warning';
    options.buttons = ['按钮1','按钮2','按钮3','按钮4','按钮5']
    dialog.showMessageBox(options)
}
</code></pre>
<p>运行上面的代码，会显示如下图所示的对话框。在 Mac OS X 下，添加的按钮从右向左显示。</p>
<p><img src="https://images.gitbook.cn/69b14320-85cf-11e9-a3ac-bfcb79173f5d"  width = "60%" /></p>
<p>在 Windows 下，从上到下显示，如下图所示。</p>
<p><img src="https://images.gitbook.cn/71dbb760-85cf-11e9-b086-0fc6bf6aa63b"  width = "50%" /></p>
<h4 id="-4">获取单击按钮的索引</h4>
<p>如果在对话框上有多个按钮，就需要获取单击的是哪一个按钮，这是通过按钮的索引来判断的，因此从 0 开始。通过回调函数可以获取单击按钮的索引，回调函数的第一个参数会返回单击按钮的索引。</p>
<pre><code>function onClick_MessageBox() {
    var options = {};
    options.title = '警告';
    options.message = '这是一个警告提示框';
    options.icon = '../../../images//note.png';
    options.type = 'warning';
    options.buttons = ['按钮1','按钮2','按钮3','按钮4','按钮5']
    //  获取单击按钮的索引，并将索引输出到控制台
    dialog.showMessageBox(options,(response) =&gt; {
        console.log('当前被单击的按钮索引是' + response);
    })
}
</code></pre>
<p>运行上面的代码会看到如下图所示的效果。</p>
<p><img src="https://images.gitbook.cn/7a1f58f0-85cf-11e9-b8cd-114d038769b6"  width = "60%" /></p>
<h4 id="-5">显示错误对话框</h4>
<p>通过 showErrorBox 方法可以非常容易地显示错误对话框，该方法只有两个参数，第一个参数表示标题，第二个参数表示内容，下面的代码显示了错误对话框。</p>
<pre><code>function onClick_ErrorBox() {
    var options = {};
    options.title = '错误';
    options.content = '这是一个错误'
    dialog.showErrorBox('错误', '这是一个错误');
}
</code></pre>
<p>在 Mac OS X 下，错误对话框显示的是警告图标，如下图所示。</p>
<p><img src="https://images.gitbook.cn/821d6600-85cf-11e9-8faa-07e9850dbcac"  width = "60%" /></p>
<p>在 Windows 下显示的是错误图标，如下图所示。</p>
<p><img src="https://images.gitbook.cn/8952f2f0-85cf-11e9-ad76-416f0508b8b7"  width = "50%" /></p>
<h3 id="-6">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>购买课程后，可扫描以下二维码进群：</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>