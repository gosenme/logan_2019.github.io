---
title: Electron 开发入门-26
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="251">25.1 项目概述</h3>
<p>本课将结合多种技术实现一款支持以太防网络的 MySQL 数据库管理系统，可以管理本机或远程的 MySQL 数据库。</p>
<p>本系统涉及到的技术（包括两类技术）如下所示。</p>
<p>（1）JavaScript 语言、Web、Node.js、Electron、MySQL</p>
<p>Electron 允许使用 JavaScript、HTML 和 CSS 开发桌面应用的框架，运行依赖于 Node.js，这也是为什么 JavaScript 成为目前唯一真正意义的全栈开发语言的原因。</p>
<p>因为 JavaScript 可以开发移动应用（React Native、以及其他的混合开发框架）、Web（Node.js + Express）、控制台（命令行应用）、Node.js、桌面应用（Electron）、服务端应用（Node.js）、浏览器插件（如 Chrome）、嵌入式（Ruff）、编译器（antlr）等。</p>
<p>（2）区块链和以太坊理论、Web3.js、Solidity 语言（编写智能合约，用于在以太坊网络上保存数据表，以及从以太坊网络上获取数据表）。</p>
<p>通过本系统不仅可以学到如何使用 Web 栈技术开发跨平台桌面应用，还可以学到如何将二维数据表通过智能合约保存到以太坊网络上，以及从以太坊网络读取指定的二维表数据。</p>
<p>下面是本系统的一些截图：</p>
<p><img src="https://images.gitbook.cn/FrUr0o6ssIUpajkFWdofDiEcq4Hx" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/FuYclP8VMRjDedyUarzAhxJ7Ej3W" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/FsYv7B2nt5T7UpDrTXgW2-12kbKI" width = "60%" /></p>
<h3 id="252">25.2 主界面设计</h3>
<p>在开发系统之前，限号安装一些模块</p>
<pre><code>npm install --save dialog
npm install --save ethereumjs-tx
npm install --save mysql
npm install --save web3
npm install --save web3-eth-abi
</code></pre>
<p>首先来设计主页面（index.html）</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Title&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
hello world
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>不要忘了将 package.json 文件中入口设为 main.js。</p>
<p>main.js</p>
<pre><code>const {app, BrowserWindow} = require('electron')
const path = require('path')
const url = require('url')

// 保持一个对于 window 对象的全局引用，如果你不这样做
// 当 JavaScript 对象被垃圾回收，window 会被自动地关闭
let win

function createWindow () {
    // 创建浏览器窗口

    win = new BrowserWindow({width: 1920, height: 1000,icon: './img/ico.ico'})
    // 然后加载应用的 index1.html
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
    }))

    // 打开开发者工具
    // win.webContents.openDevTools()

    global.win=win;
    // 当 window 被关闭，这个事件会被触发
    win.on('closed', function() {
        // 取消引用 window 对象，如果你的应用支持多窗口的话
        // 通常会把多个 window 对象存放在一个数组里面
        // 与此同时，你应该删除相应的元素
        win = null
    })
}

// Electron 会在初始化后并准备
// 创建浏览器窗口时，调用这个函数
// 部分 API 在 ready 事件触发后才能使用
app.on('ready', createWindow)
</code></pre>
<p>用于运行当前应用的脚本文件（run.js）</p>
<pre><code>var exec = require('child_process').exec;
free = exec('electron .');
</code></pre>
<h3 id="253">25.3 为主页面添加工具条按钮</h3>
<p>修改 index.html 页面代码，需要引用 index.css 样式文件。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;MySQL数据库管理&lt;/title&gt;
    &lt;link type="text/css" href="css/index.css" rel="stylesheet"/&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div class="head"&gt;
    &lt;div class="head_item" id="mysql_connection"&gt;
        &lt;div class="head_item_top"&gt;
            &lt;img src="img/link.png" title="链接数据库" class="head_item_img"&gt;
        &lt;/div&gt;
        &lt;div class="head_item_foot"&gt;
            链接
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="head_h_line"&gt;&lt;/div&gt;
    &lt;div class="head_item" id="mysql_search"&gt;
        &lt;div class="head_item_top"&gt;
            &lt;img src="./img/search.png" title="SQL语句"class="head_item_img"&gt;
        &lt;/div&gt;
        &lt;div class="head_item_foot"&gt;
            SQL语句
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="head_item" id="rth_list"&gt;
        &lt;div class="head_item_top"&gt;
            &lt;img src="./img/d4.png" title="查看以太坊数据" class="head_item_img"&gt;
        &lt;/div&gt;
        &lt;div class="head_item_foot"&gt;
            以太坊
        &lt;/div&gt;
    &lt;/div&gt;


&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<h3 id="254tree">25.4 在主页面放置显示数据库的 Tree 组件</h3>
<p>Tree 组件的脚本文件是 jquery.ztree.core.js。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;MySQL数据库管理&lt;/title&gt;

    &lt;link type="text/css" href="css/zTreeStyle.css" rel="stylesheet"/&gt;
&lt;script src="./javascript/jquery.ztree.core.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;div class="body"&gt;
   &lt;!--  这里显示树控件的内容 --&gt;
    &lt;div class="body_left" id="body_left"&gt;
        &lt;div id="tree" class="ztree"&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="body_right"&gt;

    &lt;/div&gt;
&lt;/div&gt;
&lt;div class="footer"&gt;
    &lt;div class="cmd"&gt;
        &lt;textarea class="cmd-text" cols="30" rows="10"&gt;&lt;/textarea&gt;
    &lt;/div&gt;
可以复制
    &lt;div id="dbBigImg" style="position: fixed;right:20px;bottom:100px;display: none"&gt;&lt;img src="https://geekori.com/images/ewm_dy.jpg" alt="" height="200px" width="200px"  id=""&gt;&lt;/div&gt;

    &lt;img src="https://geekori.com/images/ewm_dy.jpg" alt="" style="width: 80px;height: 80px;margin-right:100px;float:right;margin-left: 50px;margin-top: 10px" id="dbImg"&gt;
    &lt;div style="width:300px;margin-left: 50px;height:70px;float:right;margin-top: 10px"&gt;
        关注订阅号（极客起源），每天分享精彩技术文章:&lt;br&gt;
    &lt;/div&gt;
    &lt;div style="margin-left: 50px;height:70px;float:right;margin-top: 10px"&gt;
        技术交流QQ群:&lt;br&gt;
        1群 : 264268059（已满）,2群 : 140310203&lt;br&gt;

    &lt;/div&gt;

&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<h3 id="255">25.5 响应“连接”按钮单击事件</h3>
<p>相应“连接”按钮单击事件代码在 index.js 脚本文件中，通过 jQuery 指定单击事件，代码如下。</p>
<p>index.js</p>
<pre><code>if(global.rootPath == undefined) {
        global.rootPath = __dirname;
}
window.$ = jQuery = require(global.rootPath + "/javascript/jquery-3.2.1.min.js");
$(function(){
    $('#mysql_connection').click(function(){
        alert('连接数据库')
    })
});
</code></pre>
<p>在 index.html 文件中需要引用 index.js 和 jquery-3.2.1.min.js，代码如下：</p>
<pre><code>&lt;script src="./javascript/index.js"&gt;&lt;/script&gt;
&lt;script src="./javascript/jquery-3.2.1.min.js"&gt;&lt;/script&gt;
</code></pre>
<h3 id="256sql">25.6 执行 SQL 语句</h3>
<p>其他与 UI 相关功能的实现方式差不多，读者可以参考本例提供的源代码，下面看一下本例的一个比较重要的功能：执行 SQL 语句。因为可以将执行结果上传到以太坊永久保存。</p>
<pre><code>$('#mysql_search').click(function(){//SQL 语句按钮
    $('#saveResult').hide();//隐藏保存以太坊按钮
   //  判断数据库是否成功连接
    if(!global.linkOpen){
        alert('mySql未连接...');
        return;
    }
    //  读取菜单页面
    var sqlMenuStr=fs.readFileSync("./otherHtml/sqlMenu.html","utf-8");
    //  显示右键菜单
    $('.body_right').html(sqlMenuStr);
    $('.body_right_sql').focus();
    //  为运行按钮指定单击事件
    $('#runSqlBtn').click(function(){//运行按钮点击
        var sql=$('.body_right_sql').val();
        //运行sql
        db.sql(sql,function(err,result){
            if(err){
                $('.body_right_bottom').html(err);
            }else{
                var keyWord=sql.split(' ')[0];//判断是哪种类型的 sql switch 里还可以定义更多
                switch(keyWord){
                    case 'select': case 'show':
                    //有查询结果是显示保存
                    $('#saveResult').show().click(function(){
                        $('.Rth_name').show();//输入名称的组件
                        $('#rth-submit').click(function(){//提交
                            var rthName=$('#rth-input').val();
                            var rthClass={};
                            rthClass.rthName=rthName;
                            var jsonArr=[];
                            var colNum=0;
                            for(var i in result[0]){
                                jsonArr.push(i);
                                colNum++;
                            }
                            for(var j in result){
                                for(var k in result[j]){
                                    jsonArr.push(result[j][k]);
                                }
                            }

                            rthClass.rthJson=JSON.stringify(jsonArr);
                            rthClass.colNum=colNum;//字段数 global.dataStorage.saveData 倒数第二个参数
                            rthClass.rowNum=result.length;//结果个数 global.dataStorage.saveData 最后一个参数
                            global.EthereumUploadArr.push(rthClass);//存入队列
                            $('.Rth_name').hide();
                        })
                        $('#rth-cancel').click(function(){//取消
                            $('#rth-input').val('');
                            $('.Rth_name').hide();
                        })
                    })

                    var resultHtml=getTable(result);
                    $('.body_right_bottom').html(resultHtml);
                    break;
                    default:
                        var resultHtml='Run Sql : &lt;br&gt;'+ sql+'&lt;br&gt;Is Ok !';
                        $('.body_right_bottom').html(resultHtml);
                }
                // $('.body_right_bottom').html(result.toString())
            }
        })
    })

})
</code></pre>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p></div></article>