---
title: Electron 开发入门-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="121">12.1 动态创建菜单</h3>
<p>在很多应用场景需要动态添加菜单项，动态添加菜单项的基本原理就是创建若各个 MenuItem 对象，每一个 MenuItem 对象相当于一个菜单项，然后将 MenuItem 对象逐个添加到 Menu 对象中，Menu 对象相当于带子菜单的菜单项。</p>
<p>本节给一个案例，用来完整阐述如何使用 MenuItem 和 Menu 动态创建菜单。这个案例的功能是首先动态创建最初的菜单，然后通过文本输入一个一个添加菜单项。下面先看一下本例主页面的实现。</p>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;动态添加菜单&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;动态添加菜单&lt;/h1&gt;

&lt;button onclick="onClick_AllOriginMenu()"&gt;添加最初的菜单&lt;/button&gt;
&lt;p/&gt;
菜单文本：&lt;input id="menuitem"/&gt;
&lt;p&gt;&lt;input id="radio" name="radio" type="radio"/&gt; 单选&lt;br&gt;&lt;input id="checkbox" name="radio" type="radio"/&gt; 多选&lt;/p&gt;
&lt;p/&gt;
&lt;button onclick="onClick_AddMenuItem()"&gt;动态添加菜单项目&lt;/button&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 index.html 页面中定义了两个按钮，其中单击“添加最初的菜单”按钮会向应用添加最初的应用菜单，然后在 menuitem 文本框中输入菜单文本，以及用下面的 radio 组件决定添加的菜单项是普通的菜单项，还是单选菜单项，或是多选菜单项。</p>
<ul>
<li>event.js</li>
</ul>
<pre><code>const electron = require('electron');
const app = electron.app;
const remote = electron.remote;
const BrowserWindow = remote.BrowserWindow;
const Menu  = remote.Menu;
const MenuItem  = remote.MenuItem;
function saveClick() {
   // 单击“保存”按钮后弹出一个窗口
    var win = new BrowserWindow({width:300,height:200});
    win.loadURL('https://geekori.com');
}
// 
var customMenu = new Menu();
//  添加最初的应用菜单
function onClick_AllOriginMenu() {

    const menu = new Menu();
    var icon = '';
    if (process.platform != 'win32') {
        icon  = '../../../images/open.png';
    } else {
        icon = '../../../images/folder.ico';
    }
   //  创建菜单项对应的 MenuItem 对象
    var menuitemOpen =    new MenuItem({label:'打开',icon:icon})
    var menuitemSave = new MenuItem({label:'保存',click:saveClick})
   // 创建带子菜单的菜单项
    var menuitemFile = new MenuItem({label:'文件',submenu:[menuitemOpen,menuitemSave]});
   // 创建用于定制的菜单项目
    menuitemCustom =  new MenuItem({label:'定制菜单',submenu:customMenu});

    menu.append(menuitemFile);
    menu.append(menuitemCustom);

    Menu.setApplicationMenu(menu);

}
//  动态添加菜单项
function onClick_AddMenuItem() {
    var type = 'normal';
    if(radio.checked)  {
        type = 'radio';      // 设为单选风格的菜单项
    }
    if(checkbox.checked)  {
        type  =  'checkbox';  //  设为多选风格的菜单项
    }
   //  动态添加菜单项
    customMenu.append(new MenuItem({label:menuitem.value,type:type}))
    menuitem.value = '';
    radio.checked = false;
    checkbox.checked=false;
   //  必须更新菜单，修改才能生效
    Menu.setApplicationMenu(Menu.getApplicationMenu());
}
</code></pre>
<p>运行程序，先单击“添加最初的菜单”按钮添加初始应用菜单，然后根据需要动态添加菜单项，效果如下。</p>
<p>Mac OS X 效果如图。</p>
<p><img src="https://images.gitbook.cn/55e2f1b0-85d7-11e9-93d9-974442b5d3f6"  width = "40%" /></p>
<p>Windows 效果如图。</p>
<p><img src="https://images.gitbook.cn/5c59e990-85d7-11e9-bd42-43ed062f8a3c"  width = "35%" /></p>
<p>PS：在 Electron 中对 JavaScript 代码引用 HTML 中的组件的方式进行了扩展。在传统的 Web 应用中，需要使用document.getElementById 方法根据组件的 id 获取组件的 DOM 对象，但在 Electron 中，可以直接使用组件的 id引用组件中的属性和方法，如 menuItem.value。</p>
<h3 id="122">12.2 上下文菜单</h3>
<p>上下文菜单就是鼠标右键单击某个页面组件弹出的一个菜单，因此上下文菜单也称为鼠标右键菜单。创建上下文菜单的方式与创建应用菜单的方式类似，只是不使用 Menu.setApplicationMenu 方法将菜单作为应用菜单显示，而是使用 menu.popup 方法在鼠标单击的位置弹出菜单。下面的代码完整地演示了如何实现上下文菜单。</p>
<ul>
<li>index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;上下文菜单&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body onload="onload()"&gt;
&lt;h1&gt;上下文菜单&lt;/h1&gt;
&lt;div id = "panel" style="background-color: brown; width: 300px;height:200px"&gt;&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 index.html 页面中放置了一个 \<div> 标签，当鼠标右击 \<div> 标签时就会弹出上下文菜单。</p>
<ul>
<li>event.js</li>
</ul>
<pre><code>const electron = require('electron');
const app = electron.app;
const remote = electron.remote;
const BrowserWindow = remote.BrowserWindow;
const Menu  = remote.Menu;
const MenuItem  = remote.MenuItem;
const dialog = remote.dialog;
function  onload() {
    const menu = new Menu();
    var icon = '';
    if (process.platform != 'win32') {
        icon  = '../../../images/open.png';
    } else {
        icon = '../../../images/folder.ico';
    }
    const win = remote.getCurrentWindow();
    //  添加上下文菜单项，单击菜单项，会弹出打开对话框，并将选择的文件路径设置为窗口标题
    var menuitemOpen = new MenuItem({label:'打开',icon:icon,click:()=&gt;{
        var paths =  dialog.showOpenDialog({properties: ['openFile']});
        if(paths  != undefined)
            win.setTitle(paths[0]);
    }});
    var menuitemSave = new MenuItem({label:'保存',click:saveClick})

    var menuitemFile = new MenuItem({label:'文件',submenu:[menuitemOpen,menuitemSave]});

    var menuitemInsertImage =  new MenuItem({label:'插入图像'});
    var menuitemRemoveImage =  new MenuItem({label:'删除图像'});

    menu.append(menuitemFile);
    menu.append(menuitemInsertImage);
    menu.append(menuitemRemoveImage);
   //  添加上下文菜单响应事件，只有单击鼠标右键，才会触发该事件
    panel.addEventListener('contextmenu',function(event) {
        //  阻止事件的默认行为，例如，submit 按钮将不会向 form 提交
       event.preventDefault();
       x = event.x;
       y = event.y;
       //  弹出上下文菜单
       menu.popup({x:x,y:y});
       return false;
    });
}
function saveClick() {
    var win = new BrowserWindow({width:300,height:200});
    win.loadURL('https://geekori.com');
}
</code></pre>
<p>上下文菜单的效果如下图所示。</p>
<p><img src="https://images.gitbook.cn/642993a0-85d7-11e9-a237-dd6feca557a2"  width = "30%" /></p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>