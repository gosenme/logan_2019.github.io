---
title: Electron 开发入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="111role">11.1 菜单项的角色（role）</h3>
<h4 id="">常用的菜单项角色</h4>
<p>菜单项的角色就是菜单的预定义动作，通过菜单对象的 role 属性设置，通用的角色如下：</p>
<ul>
<li>undo</li>
<li>redo</li>
<li>cut</li>
<li>copy</li>
<li>paste</li>
<li>pasteAndMatchStyle</li>
<li>selectAll</li>
<li>delete</li>
<li>minimize，最小化当前窗口</li>
<li>close，关闭当前窗</li>
<li>quit，退出应用程序</li>
<li>reload，重新装载当前窗口</li>
<li>forceReload，重新装载当前窗口（不考虑缓存）</li>
<li>toggleDevTools，在当前窗口显示开发者工具</li>
<li>toggleFullScreen，全屏显示当前窗口</li>
<li>resetZoom，重新设置当前页面的尺寸为最初的尺寸</li>
<li>zoomIn，将当前页面放大 10%</li>
<li>zoomOut，将当前页面缩小 10%</li>
<li>editMenu，整个“Edit”菜单，包括 Undo、Copy 等</li>
<li>windowMenu，整个“Window”菜单，包括 Minimize、Close 等</li>
</ul>
<p>下面的角色仅用于 Mac OS X 系统。</p>
<ul>
<li>about：显示“关于”对话框</li>
<li>hide：隐藏</li>
<li>hideOthers：隐藏其他应用程序</li>
<li>unhide：取消隐藏其他应用程序</li>
<li>startSpeaking：开始说话</li>
<li>stopSpeaking ：停止说话</li>
<li>front：映射 arrangeInFront 动作</li>
<li>zoom：映射 performZoom 动作</li>
<li>toggleTabBar：显示 TabBar</li>
<li>selectNextTab：选择下一个 Tab</li>
<li>selectPreviousTab：选择前一个 Tab</li>
<li>mergeAllWindows：合并所有的窗口</li>
<li>moveTabToNewWindow：移动 Tab 到新的窗口</li>
<li>window：Window 的子菜单</li>
<li>help：Help 的子菜单</li>
<li>services：Services 的子菜单</li>
<li>recentDocuments：Open Recent 菜单的子菜单</li>
<li>clearRecentDocuments：清除最近打开的文档</li>
</ul>
<h4 id="-1">实现代码</h4>
<p>下面完整地演示如何使用菜单项角色。</p>
<p>在 index.js 文件中：</p>
<pre><code>const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const Menu  = electron.Menu;

function createWindow () {

    win = new BrowserWindow({file: 'index.html'});

    win.loadFile('./index.html');

    const template = [
        {
            label: '编辑',
            submenu: [
                {
                    label: '撤销',
                    role:'undo'

                },
                {
                    label: '重做',
                    role:'redo'

                },
                {
                    label: '剪切',
                    role:'cut'
                },
                {
                    label: '复制',
                    role:'copy'
                },
                {
                    label: '粘贴',
                    role:'paste'
                }
            ]
        },
        {
            label: '调试',
            submenu: [
                {
                    label: '显示调试工具',
                    role:'toggleDevTools'

                }
            ]
        }
        ,
        {
            label: '窗口',
            submenu: [
                {
                    label: '全屏显示窗口',
                    role:'toggleFullScreen'

                },
                {
                    label: '窗口放大10%',
                    role:'zoomIn'

                },
                ,
                {
                    label: '窗口缩小10%',
                    role:'zoomOut'

                }
            ]
        }
    ];
    if (process.platform == 'darwin') {

        template.unshift({
            label: 'Mac',
            submenu: [
                {
                    label: '关于',
                    role:'about'

                },
                {
                    label: '开始说话',
                    role:'startSpeaking'

                },
                {
                    label: '停止说话',
                    role:'stopSpeaking'

                }
            ]
        })
    }
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
    win.on('closed', () =&gt; {
      console.log('closed');
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
<p>运行上面程序之前，要先在 index.html 中加一个文本输入框，用来演示文本的复制、粘贴、剪切等功能，代码如下。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--  指定页面编码格式  --&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--  指定页头信息 --&gt;
  &lt;title&gt;菜单项角色（role）&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;默认模板&lt;/h1&gt;
&lt;textarea style="width:400px;height:300px"&gt;&lt;/textarea&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在前面的代码中添加菜单时考虑到了操作系统的差异，如果是 Mac OS X，会在开始添加一个 Mac 菜单，并添加Mac OS X 特有的角色作为菜单项。</p>
<p>Mac OS X 的效果如下。</p>
<p><img src="https://images.gitbook.cn/fc70edc0-85cd-11e9-95b6-2577493fda20"  width = "50%" /></p>
<p>在 Mac OS X，在文本输入框输入一些文本，选中这些文本，然后单击“开始说话”菜单项，Mac OS X 就会将这行文本读出来，这是苹果系统内置的功能，Windows 和 Linux 是没这个“待遇”的。</p>
<p>Windows 的效果如下。</p>
<p><img src="https://images.gitbook.cn/05ef3230-85ce-11e9-83b9-6dc2ad7a9ca7"  width = "50%" /></p>
<p>读者可以使用相应的菜单项演示各种角色的功能，如窗口放大 10%，每单击一次，会让当前页面所有的内容放大 10%。</p>
<h3 id="112type">11.2 菜单项的类型（type)</h3>
<p>菜单项的类型通过 type 属性设置，该属性可以设置的值及其含义如下。</p>
<ul>
<li>normal：默认菜单项</li>
<li>separator：菜单项分隔条</li>
<li>submenu：子菜单</li>
<li>checkbox：多选菜单项</li>
<li>radio：单选菜单项</li>
</ul>
<p>其中 normal 是 type 属性的默认值，如果未设置 type 属性，那么菜单项就是普通的菜单项。下面是一个完整的用于演示如何设置菜单项类型的案例。</p>
<p>在 index.js 文件中。</p>
<pre><code>const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const Menu  = electron.Menu;


function createWindow () {

    win = new BrowserWindow({file: 'index.html'});


    win.loadFile('./index.html');

    const template = [
        {
            label: '编辑',
            submenu: [
                {
                    label: '撤销',
                    role:'undo'

                },
                {
                    label: '重做',
                    role:'redo'

                },
                {
                  type:'separator'   // 设置菜单项分隔条
                },
                {
                    label: '剪切',
                    role:'cut'
                },
                {
                    label: '复制',
                    role:'copy'
                },
                {
                    label: '粘贴',
                    role:'paste'
                }
            ]
        }
        ,
        {
            label: '我的菜单',   //  包含单选菜单项、多选菜单项和带子菜单的菜单项
            submenu: [
                {
                    label: '多选1',
                    type:'checkbox'
                },
                {
                    label: '多选2',
                    type:'checkbox'
                }
                ,
                {
                    label: '多选3',
                    type:'checkbox'
                }
                ,
                {
                    label: '单选1',
                    type:'radio'

                }
                ,
                {
                    label: '单选2',
                    type:'radio'

                }
                ,

                {
                    label: '单选3',
                    type:'radio'

                }
                ,

                {
                    label: 'windows',
                    type:'submenu', // 加不加这个，都可以添加子菜单
                    role:'windowMenu'

                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);

    win.on('closed', () =&gt; {
      console.log('closed');

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
<p>运行程序，会看到如下面几个图的菜单效果。</p>
<p>Mac OS X 的菜单效果如下。</p>
<p><img src="https://images.gitbook.cn/0fc819c0-85ce-11e9-98b2-2591a789cca1"  width = "40%" /></p>
<p>Windows 的菜单效果如下。</p>
<p><img src="https://images.gitbook.cn/172b4660-85ce-11e9-a3db-f130074db178"  width = "40%" /></p>
<p>对于多线菜单项类型，Windows 和 Mac OS X 的效果是相同的，但对于单选菜单项的效果，Windows 和 Mac OS X 有明显的差异。</p>
<p>另外，如果设置了 submenu 属性，或 role 的值本身就带有子菜单（如本例的 services），那么即使不设置 type，系统也会认为当前菜单项带有子菜单。</p>
<h3 id="113">11.3 为菜单项添加图标</h3>
<p>通过设置菜单项的 icon 属性，可以为菜单项添加图标（显示在菜单项文字的前方）。在 Windows 中，建议使用 ico 图标文件，在 Mac OS X 和 Linux 下，一般使用 png 图像。菜单项图标的标准尺寸是 16 × 16，图标尺寸太大时，Electron 是不会压缩图像尺寸的，图标都会按原始尺寸显示。</p>
<p>下面的代码演示了如何为菜单项添加图标，其中考虑了操作系统的差异。</p>
<pre><code>const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const Menu  = electron.Menu;
function createWindow () {
    win = new BrowserWindow({file: 'index.html'});
    win.loadFile('./index.html');
    var icon = '';
    //  如果不是 Windows，使用 png 格式的图像
    if (process.platform != 'win32') {
        icon  = '../../../images/open.png';
    } else {  //  如果是 Windows，使用 ico 格式的图像
        icon = '../../../images/folder.ico';
    }
    const template = [
        {
            label: '文件',
            submenu: [
                {
                    label: '打开',
                    icon:icon  //  设置“打开”菜单项的图标
                },
                {
                    label: '重做',
                    role:'redo'

                }
            ]
        }

    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);

    win.on('closed', () =&gt; {
      console.log('closed');

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
<p>运行效果如下。</p>
<p>Mac OS  X 的效果如图。</p>
<p><img src="https://images.gitbook.cn/1f7a0b80-85ce-11e9-97a5-715ee03f6cd9"  width = "20%" /></p>
<p>Windows 的效果如图。</p>
<p><img src="https://images.gitbook.cn/27a12460-85ce-11e9-8187-6d43b0889bae"  width = "50%" /></p>
<p>之所以 Windows 菜单项图标这么大，是因为 ico 文件的尺寸本来很多，所以要想让图标正常显示，应使用尺寸为 16 × 16 的 ico 文件。</p>
<h3 id="-2">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>购买课程后，可扫描以下二维码进群：</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>