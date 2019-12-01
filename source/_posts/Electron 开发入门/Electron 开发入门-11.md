---
title: Electron 开发入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>现在我们介绍如何为桌面应用创建应用菜单，还会介绍在 Mac OS X 和 Windows 下菜单的不同之处；然后会介绍上下文菜单，它会在用户单击应用内的某个元素时，给用户提供一些选项，例如，在文档的某个位置插入新的文本。</p>
<p>Electron 桌面应用支持三种菜单：应用菜单、上下文菜单及托盘菜单。</p>
<p>我们先来看应用菜单，应用菜单一般在窗口的上面，标准栏的下面，不过在 Mac OS X 系统中会有所不同。</p>
<p>创建应用菜单需要些技巧，你必须要考虑操作系统。</p>
<p>目前主流的操作系统主要有 Windows、Mac OS X 和 Linux，对于应用菜单来说，Windows 和 Linux 很多时候是一致的，每个窗口都在应用内有自己的应用菜单。但 Mac OS X 是个另类，只有 1 个应用菜单供所有的窗口使用，这个应用菜单在操作系统的菜单栏中，与窗口是分离的。在 Electron 中，只提供了一套 API 来处理 3 个操作系统的菜单，因此我们在使用这些 API 时应考虑操作系统的差异性。</p>
<p>在 Electron 中，可以使用模板，也可以使用菜单对象来创建应用菜单，本节会使用模板创建 Mac OS X 和Windows 下的应用菜单。</p>
<p>应用菜单模板就是一个对象数组，每一个数据元素就是一个菜单项，可以通过数组中的对象设置这个菜单项的菜单文本及其他的属性，如菜单的子菜单。</p>
<p>下面就是一个典型的菜单模板的例子。</p>
<pre><code>   const template = [{
        label: '文件',   //设置菜单项文本
        submenu: [    //设置子菜单
            {
                label: '关于',
                role: 'about',       // 设置菜单角色（关于），只针对 Mac  OS X 系统
                click: ()=&gt;{     //设置单击菜单项的动作（弹出一个新的模态窗口）
                    var aboutWin = new BrowserWindow({width:300,height:200,parent:win,modal: true});
                    aboutWin.loadFile('https://geekori.com');}
            },
            {
                type: 'separator'       //设置菜单的类型是分隔栏
            },
            {
                label: '关闭',
                accelerator: 'Command+Q',      //设置菜单的热键
                click: ()=&gt;{win.close()}
            }
        ]
    },
        {
            label: '编辑',
            submenu: [
                {
                    label: '复制',
                    click: ()=&gt;{win.webContents.insertText('复制')}

                },
                {
                    label: '剪切',
                    click: ()=&gt;{win.webContents.insertText('剪切')}

                },
                {
                    type: 'separator'
                },
                {
                    label: '查找',
                    accelerator: 'Command+F',
                    click: ()=&gt;{win.webContents.insertText('查找')}
                },
                {
                    label: '替换',
                    accelerator: 'Command+R',
                    click: ()=&gt;{win.webContents.insertText('替换')}
                }
            ]
        }
    ];
</code></pre>
<p>在上面的菜单模板中添加了 2 个应用菜单：一个是文件菜单，另外一个是编辑菜单，在这个菜单模板中，设置了菜单的多个属性，其中包括菜单的文本（label）、菜单的角色（role）、菜单的动作（click）、菜单的类型（type）、菜单的热键（accelerator）。</p>
<p>创建应用菜单需要 Menu 类，因此现在来编写使用菜单模板的代码。</p>
<pre><code>const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const Menu  = electron.Menu;

function createWindow () {

    win = new BrowserWindow({file: 'index.html'});

    win.loadFile('./index.html');
    const template = ... //  定义菜单模板
    //  创建菜单对象
    const menu = Menu.buildFromTemplate(template);
    //  安装应用
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
<p>运行上面的程序，会看到如下图的菜单。</p>
<p>Mac OS X 菜单效果如下。</p>
<p><img src="https://images.gitbook.cn/3806d5c0-85ce-11e9-8765-b1828b64ac5a"  width = "30%" /></p>
<p><img src="https://images.gitbook.cn/40681170-85ce-11e9-a093-2bb2886648bf"  width = "30%" /></p>
<p>Windows 菜单效果如下。</p>
<p><img src="https://images.gitbook.cn/47f645b0-85ce-11e9-bd51-bbe10ca22d44"  width = "30%" /></p>
<p><img src="https://images.gitbook.cn/4f54de70-85ce-11e9-83ef-6b35738fc9b5"  width = "30%" /></p>
<p>可以看到，Mac OS X 与 Windows 下的应用菜单有显著的差异，Mac  OS  X 在“编辑”菜单下面又添加了两个系统菜单项。不过一个最大的不同是，第 1 个菜单的文本明明是“文件”，在Windows 中是正常的，在 Mac OS X 中为什么变成了 Electron 呢？</p>
<p>其实这个问题是 Mac OS X 系统本身导致的。在 Mac OS X 系统中，使用 electron 命令运行应用时第一个菜单的文本都是“Electron”，不过在发布后，第 1 个应用菜单的文本就变成了应用名称了。注意，不管是哪种情况，第一个应用菜单的 label 属性是不起作用的。</p>
<p>那么问题来了，如何打包和发布 Electron 应用呢？其实现在有很多第三方的工具可以完成这些工作。由于 Electron 是跨平台的，所以选择打包工具时应尽量选择支持多个操作系统平台的，如 electron-packager，读者可以通过下面的地址访问 electron-packager 的官网。</p>
<p><a href="https://github.com/electron-userland/electron-packager">https://github.com/electron-userland/electron-packager</a></p>
<p>electron-packager 是一个命令行程序，参数比较多，这里只介绍一种比较简单的用法。</p>
<p>首先要使用下面的命令安装 electron-managerr。</p>
<pre><code>npm install electron-packager -g
</code></pre>
<p>如果觉得 npm 命令慢，可以使用 cnpm 命令，不过要先安装 cnpm 命令，安装命令如下。</p>
<pre><code>npm install -g cnpm --registry=https://registry.npm.taobao.org
</code></pre>
<p>假设“firstmenu”是应用程序名称，使用下面的命令会将当前目录中的 electron 工程打包，打包后的应用会将Node.js 等系统一起打包，所以在发布应用时可以只复制打包文件即可（不需要再分发 electron、Node.js 等包）。</p>
<pre><code>electron-packager . firstmenu --electron-version=3.0.0
</code></pre>
<p>在 Mac OS X 下打包后，在当前目录会建立一个名为 firstmenu-darwin-x64 的子目录，进入该子目录，会看到如下图的一些目录和文件。</p>
<p><img src="https://images.gitbook.cn/58b847e0-85ce-11e9-a45b-abad6067eb6d"  width = "30%" /></p>
<p>其中 firstmenu 是一个目录，这个目录是 Mac OS X 特有的，将作为 Mac OS X 的可执行程序来运行。现在升级firstmenu，会运行程序，应用菜单如下图所示。很明显，左上角的 Electron 菜单变成了 firstmenu。</p>
<p><img src="https://images.gitbook.cn/61871270-85ce-11e9-a625-71c8b9bd2801"  width = "30%" /></p>
<p>在 Windows 下打包的命令如下，不过 Windows 下的可执行文件是 exe，所以需要找到 firstmenu.exe 文件，然后执行它。</p>
<p>如果设置了菜单项的角色（role），单击事件将被忽略。不过有些角色只适合特定的操作系统，例如，about 角色只适合 Mac OS X，所以在 Windows 中仍然会响应菜单项的单击事件，本例在 Windows 中的”关于“菜单项弹出了一个模式窗口，如下图所示。</p>
<p><img src="https://images.gitbook.cn/70983050-85ce-11e9-98a7-d9c9689169cd"  width = "40%" /></p>
<p>在 Mac OS X 中会显示 about 角色的对话框，如下图所示。</p>
<p><img src="https://images.gitbook.cn/77be05d0-85ce-11e9-b4b2-553e1b961637"  width = "40%" /></p>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>