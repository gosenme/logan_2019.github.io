---
title: Electron 开发入门-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这里的托盘是指操作系统的一个功能区，在这个功能区中有一些图标，每一个图标代表一个应用程序。通常在图标上单击鼠标的左键或右键，会弹出一个菜单或窗口来完成特定的功能。</p>
<p>Windows、Mac OS X 和 Linux 的托盘效果有一些差异。</p>
<p>Windows 的托盘在任务栏的右侧（屏幕的右下角），如下图所示。</p>
<p><img src="https://images.gitbook.cn/151af970-85cd-11e9-ab9a-9920e00ff74f"  width = "40%" /></p>
<p>Mac OS X 的托盘在菜单栏的右侧（屏幕的右上角），如下图所示。</p>
<p><img src="https://images.gitbook.cn/1cb69b30-85cd-11e9-81a6-9daf6c4211c3" alt="image.png" /></p>
<p>Electron 提供了一些 API，用于在托盘上为应用程序添加图标、弹出菜单以及相应各种动作。</p>
<h3 id="131">13.1 将应用程序放到托盘上</h3>
<p>本节会在托盘上放置一个图标，单击鼠标左键（Mac OS X）或单击鼠标右键（Windows）会弹出上下文菜单，单击菜单项会完成某些动作。</p>
<p>一个托盘图标由一个 Tray 对象表示，因此为应用程序添加托盘图标，首先要先创建一个 Tray 对象。注意，Tray 对象不需要像菜单一样通过特定的方法添加到托盘上，只要创建一个 Tray 对象就会自动将图标放到托盘上，如果在一个应用程序中创建多个 Tray 对象，那么就会在托盘中添加多个图标。</p>
<p>下面是完整的实现代码。</p>
<p>在 index.js 中。</p>
<pre><code>const {app, Menu, Tray,BrowserWindow} = require('electron')
let tray;
let contextMenu
function createWindow () {
    win = new BrowserWindow({file: 'index.html'});
    win.loadFile('./index.html');
    //  创建 Tray 对象，并指定托盘图标
    tray = new Tray('../../../../images/open.png');
    //  创建用于托盘图标的上下文菜单
    contextMenu = Menu.buildFromTemplate([
        {label: '复制', role:'copy'},
        {label: '粘贴', role:'paste'},
        {label: '剪切', role:'cut'}

    ])
    //  设置托盘图标的提示文本
    tray.setToolTip('这是第一个托盘应用')
    //  将托盘图标与上下文菜单关联
    tray.setContextMenu(contextMenu)
    win.on('closed', () =&gt; {
        win = null;
    })

}
app.on('ready', createWindow)
app.on('activate', () =&gt; {

    if (win === null) {
        createWindow();
    }
})
</code></pre>
<p>运行程序，就会在操作系统的托盘上看到图标了。</p>
<p>将鼠标放到托盘图标上，就会显示提示文本。</p>
<p>Mac OS X 的效果如下。</p>
<p><img src="https://images.gitbook.cn/26690f00-85cd-11e9-a5e6-a91b238af86c" alt="image.png" /></p>
<p>Windows 的效果如下。</p>
<p><img src="https://images.gitbook.cn/2dd870a0-85cd-11e9-843e-877d6cbaa416"  width = "30%" /></p>
<p>在应用程序的主窗口上有一个文本输入框，读者可以在文本输入框中输入一些文本，然后测试“复制”、“粘贴”等功能。</p>
<p>在 index.html 中。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;简单的托盘&lt;/title&gt;

&lt;/head&gt;

&lt;body&gt;
&lt;textarea style="width:300px;height:200px"&gt;&lt;/textarea&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>运行程序，在 Mac OS X 下用鼠标左键单击托盘图标，会显示如下图的菜单。</p>
<p><img src="https://images.gitbook.cn/368bc3f0-85cd-11e9-9135-e1ca2ddb14b3"  width = "40%" /></p>
<p>不过在 Windows 下，使用 role 设置菜单项的预定功能不起作用（作为应用菜单可以），因此如果将上下文菜单作为托盘图标的菜单，应该尽量使用 click 属性设置单击事件函数，下面的代码为上下文菜单的“关闭”菜单项设置了单击事件函数，并在函数中调用 win.close 函数关闭了当前应用程序。</p>
<pre><code>    contextMenu = Menu.buildFromTemplate([
        {label: '复制', role:'copy'},
        {label: '粘贴', role:'paste'},
        {label: '剪切', role:'cut'},
        {label: '关闭', role:'close',click:()=&gt;{win.close()}}
    ])
</code></pre>
<blockquote>
  <p>注意：系统并不会压缩托盘图标的尺寸，因此在设置托盘图标时，应该选择适当尺寸的图像文件，通常是16 × 16 大小。</p>
</blockquote>
<h3 id="132">13.2 托盘事件</h3>
<p>我们会发现，在 Mac OS X 的托盘图标是单击鼠标左键弹出上下文菜单，而有一些托盘图标是单击右键弹出上下文菜单，这是怎么回事呢？</p>
<p>其实用 Electron 添加的托盘图标在 Mac OS X 默认是单击鼠标左键弹出上下文菜单，在 Windows 是单击鼠标右键弹出上下文菜单，不过这个默认行为可以通过托盘事件修改。Tray 有一个 right-click 事件，该事件在鼠标右键单击托盘图标时触发，可以在该事件中调用 popUpContextMenu 方法弹出上下文菜单，代码如下。</p>
<pre><code>    tray.on('right-click', (event) =&gt;{
       tray.popUpContextMenu(contextMenu);
    });
</code></pre>
<p>下面的代码演示了 Tray 中主要事件的使用方法。</p>
<ul>
<li>event.js</li>
</ul>
<pre><code>const remote= require('electron').remote;
const Menu =  remote.Menu;
const Tray = remote.Tray;
let tray;
let contextMenu
//  添加托盘图标
function onClick_AddTray()  {
    if(tray != undefined) {
        return
    }
    tray = new Tray('../../../../images/open.png');
    var win = remote.getCurrentWindow();
    contextMenu = Menu.buildFromTemplate([
        {label: '复制', role:'copy'},
        {label: '粘贴', role:'paste'},
        {label: '剪切', role:'cut'},
        {label: '关闭', role:'close',click:()=&gt;{win.close()}}

    ])
   /*
         为托盘图标添加鼠标右键单击事件，在该事件中，如果按住 shift 键，再单击鼠标右键，会弹出一个窗口，否则会弹出上下文菜单。

         如果为托盘图标绑定了上下文菜单，在 Windows 下不会响应该事件，这是因为 Windows 下是单击鼠标右键显示上下文菜单的，正好和这个 right-click 事件冲突。

event 参数包括下面的属性，表明当前是否按了对应的键。
1. altKey：Alt 键
2. shiftKey：Shift 键
3. ctrlKey：Ctrl 键
4. metaKey：Meta 键，在 Mac OS X 下是 Command 键，在 Windows 下是窗口键（开始菜单键）
   */
    tray.on('right-click', (event) =&gt;{
        textarea.value += '\r\n' + 'right-click';
        if(event.shiftKey) {
            window.open('https://geekori.com','right-click','width=300,height=200')
        } else  {
            //  单击鼠标右键弹出上下文菜单
            tray.popUpContextMenu(contextMenu);
        }
    });
   /*
           为托盘图标添加鼠标单击事件，在该事件中，如果按住 shift 键，再单击鼠标左键或右键，会弹出一个窗口，否则会弹出上下文菜单。
           如果将上下文菜单与托盘图标绑定，在 Mac OS X 下，单击鼠标左键不会触发该事件，这是由于 Mac OS X 下是单击鼠标左键弹出上下文菜单，与这个事件冲突
   */
    tray.on('click', (event) =&gt;{
        textarea.value += '\r\n' + 'click';
        if(event.shiftKey) {
            window.open('https://geekori.com','click','width=300,height=200')
        } else  {
            //  单击鼠标右键弹出上下文菜单
            tray.popUpContextMenu(contextMenu);
        }
    });
   /*
     当任何东西拖动到托盘图标上时触发，读者可以从 word 中拖动文本到托盘图标上观察效果

Only Mac OS X
  */
    tray.on('drop',()=&gt;{
        textarea.value += '\r\n' + 'drop';

    });
   /*
     当文件拖动到托盘图标上时会触发，files 参数是 String 类型数组，表示拖动到托盘图标上的文件名列表

Only Mac OS X
  */
    tray.on('drop-files',(event,files)=&gt;{
        textarea.value += '\r\n' + 'drop-files';
        //  输出所有拖动到托盘图标上的文件路径
        for(var i = 0; i &lt; files.length;i++) {
            textarea.value += files[i] + '\r\n';
        }
    });
   /*
     当文本拖动到托盘图标上时会触发，text 参数是 String 类型，表示拖动到托盘图标上的文本

Only Mac OS X
  */
    tray.on('drop-files',(event,files)=&gt;{
        textarea.value += '\r\n' + 'drop-files';
        for(var i = 0; i &lt; files.length;i++) {
            textarea.value += files[i] + '\r\n';
        }
    });    
    tray.setToolTip('托盘事件')
    tray.setContextMenu(contextMenu)


}
</code></pre>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;托盘事件&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;

&lt;body&gt;
&lt;textarea id="textarea" style="width:600px;height:200px"&gt;&lt;/textarea&gt;
&lt;p/&gt;
&lt;button onclick="onClick_AddTray()"&gt;添加托盘图标&lt;/button&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>读者可以加多个文件和文本一起拖动到托盘图标上，拖动的过程如下图所示。</p>
<p><img src="https://images.gitbook.cn/440c56c0-85cd-11e9-aed1-97e9ec2b2d71"  width = "50%" /></p>
<p>拖动后，在程序的文本输入框中会显示如下图的文本和文件名。</p>
<p><img src="https://images.gitbook.cn/4bcd5ad0-85cd-11e9-bfb1-c79235441455"  width = "60%" /></p>
<h3 id="133">13.3 托盘方法</h3>
<p>Tray 类提供了多个方法用来控制托盘图标，如设置托盘图标、设置托盘文本、移除托盘图标等。本节将会介绍与托盘相关的一些方法。</p>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;托盘方法&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;

&lt;body&gt;

&lt;button onclick="onClick_AddTray()"&gt;添加托盘图标&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_SetImage()"&gt;设置托盘图标&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_SetTitle()"&gt;设置托盘标题&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_SetPressedImage()"&gt;设置托盘按下图标&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_SetTooltip()"&gt;设置托盘提示文本&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_RemoveTray()"&gt;移除托盘图标&lt;/button&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>event.js</li>
</ul>
<pre><code>const remote= require('electron').remote;
const Menu =  remote.Menu;
const Tray = remote.Tray;
var tray;
var contextMenu

function onClick_AddTray()  {
    if(tray != undefined  ) {
        return
    }
    tray = new Tray('../../../../images/open.png');
    var win = remote.getCurrentWindow();
    contextMenu = Menu.buildFromTemplate([
        {label: '复制', role:'copy'},
        {label: '粘贴', role:'paste'},
        {label: '剪切', role:'cut'},
        {label: '关闭', role:'close',click:()=&gt;{win.close()}}

    ])

    tray.setToolTip('托盘事件')
    tray.setContextMenu(contextMenu)
}
//  设置托盘图像
function  onClick_SetImage() {
    if(tray != undefined) {
        tray.setImage('../../../../images/note1.png')
    }
}
//  设置托盘标题（仅适用于Mac OS X）
function onClick_SetTitle() {
    if(tray != undefined) {
        tray.setTitle('hello world')
    }
}
//  设置托盘按下显示的图标（仅适用于Mac OS X）
function onClick_SetPressedImage() {
    if(tray != undefined) {
        tray.setPressedImage('../../../../images/open.png')
    }
}
//  设置托盘提示文本
function onClick_SetTooltip() {
    if(tray != undefined) {
        tray.setToolTip('This is a tray')
    }
}
//  移除托盘
function onClick_RemoveTray()  {
    if(tray != undefined) {
        tray.destroy();
        tray = undefined;   //  应该将tray设为undefined，否则无法再创建托盘对象
    }
}
</code></pre>
<p>其中托盘标题和托盘图标按下图像仅适用于 Mac OS X 系统，托盘标题的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/541ff080-85cd-11e9-8db3-615203e2a7bd" alt="image.png" /></p>
<h3 id="134windows">13.4 显示气泡消息（Windows）</h3>
<p>在 Windows 下，还可以使用 displayBalloon 方法显示托盘气泡消息，效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/7b588720-85cd-11e9-95d3-5917077eb2ce"  width = "50%" /></p>
<p>气泡消息包括标题、内容和图标，完整的实现代码如下。</p>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;显示气泡消息&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;

&lt;body&gt;
&lt;textarea id="log" style="width:300px;height:200px"&gt;&lt;/textarea&gt;
&lt;p/&gt;
&lt;button onclick="onClick_AddTray()"&gt;添加托盘图标&lt;/button&gt;
&lt;p/&gt;
&lt;button onclick="onClick_DisplayBalloon()"&gt;显示气泡消息&lt;/button&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>event.js</li>
</ul>
<pre><code>const remote= require('electron').remote;
const Menu =  remote.Menu;
const Tray = remote.Tray;
var tray;
var contextMenu

function onClick_AddTray()  {
    if(tray != undefined  ) {
        return
    }
    tray = new Tray('../../../../images/open.png');
    var win = remote.getCurrentWindow();
    contextMenu = Menu.buildFromTemplate([
        {label: '复制', role:'copy'},
        {label: '粘贴', role:'paste'},
        {label: '剪切', role:'cut'},
        {label: '关闭', role:'close',click:()=&gt;{win.close()}}

    ])
   //  添加气泡消息显示事件
    tray.on('balloon-show',()=&gt;{
        log.value += 'balloon-show\r\n';
    });
    //  添加气泡消息单击事件
    tray.on('balloon-click',()=&gt;{
        log.value += 'balloon-click\r\n';
    });
    //  添加气泡消息关闭事件
    tray.on('balloon-closed',()=&gt;{
        log.value += 'balloon-closed\r\n';
    });
    tray.setToolTip('托盘事件')
    tray.setContextMenu(contextMenu)

}
function onClick_DisplayBalloon() {
    if(tray != undefined) {
        //  显示气泡消息
        tray.displayBalloon({title:'有消息了',icon:'../../../../images/note.png',content:'软件有更新了，\r\n赶快下载啊'})
    }
}
</code></pre>
<p>气泡消息包含如下 3 个事件：</p>
<ul>
<li>balloon-show，当气泡消息显示时触发；</li>
<li>balloon-click，当单击气泡消息时触发；</li>
<li>balloon-closed，当气泡消息关闭时触发。</li>
</ul>
<p>其中 balloon-click 和 balloon-closed 是互斥的，也就是说，单击气泡消息后，气泡消息会立刻关闭，在这种情况下，并不会触发 balloon-closed 事件。因此 balloon-closed 事件只有当气泡消息自己关闭后才会触发，气泡消息在显示几秒后会自动关闭。</p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>