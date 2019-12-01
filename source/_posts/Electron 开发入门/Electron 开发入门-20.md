---
title: Electron 开发入门-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>虽然 sql.js 在操作 SQLite 数据库方面没什么问题，但由于 sql.js 是基于 JavaScript 的，因而效率较低，而且操作都是在内存中完成的，如果要保存修改，需要将整个数据库写到文件中，比较费事，而且写数据的效率不高，因此在遇到大量数据的情况下，建议使用 Node.js 中的 sqlite 3 模块操作 SQLite 数据库。</p>
<h3 id="191sqlite3">19.1 安装 sqlite 3 模块</h3>
<p>sqlite 3 并不是 Node.js 的标准模块，因此在使用之前需要在当前工程目录下执行下面的命令进行安装。</p>
<pre><code>npm install --save sqlite3
</code></pre>
<p>执行完上面的命令后，会发现当前工程的 node_modules 目录中出现了一个 sqlite 3 目录，还出现了很多其他的目录，这些目录都是 sqlite 3 依赖的 Node.js 模块。</p>
<p>安装完 sqlite 3 模块后，可以创建一个 test.js 文件然后输入下面的代码测试 sqlite 3 模块是否安装成功。</p>
<pre><code>const sqlite3 = require('sqlite3').verbose();
//创建内存数据库
let db = new sqlite3.Database(':memory:', (err) =&gt; {
    if (err) {
        return console.error(err.message);
    }
    console.log('已经成功连接SQLite数据库');
});
</code></pre>
<p>使用下面的命令执行 test.js 脚本文件，如果执行成功，说明 sqlite 3 模块已经安装成功。</p>
<pre><code>node test.js
</code></pre>
<p>接下来读者可以将上面的代码放到 Electron 应用中运行。不过非常遗憾，会出现下面的错误（Mac OS X 和 Windows 的错误类似，都说的一个意思）。</p>
<p>Mac OS X 的错误页面。</p>
<p><img src="https://images.gitbook.cn/05bfa8a0-85cc-11e9-9e92-5daefb6c9aad"  width = "50%" /></p>
<p>Windows 的错误页面。</p>
<p><img src="https://images.gitbook.cn/10a8a0a0-85cc-11e9-9f60-9b179c220cb8"  width = "50%" /></p>
<p>其实这个错误的意思就是说没有找到相应的模块。但明明在 Node.js 中已经好使了，为什么在基于 Node.js 的 Electron 中会不好使呢？其实这个问题出在 Electron 和 sqlite 3 模块上。</p>
<p>Node.js 和 Electron 使用的都是 Google 的 V8 JavaScript 引擎，但却不是同一个版本，此外 sqlite 3 模块虽然接口是 JavaScript 的，但内核其实是使用 C 实现的，而且编译生成了 Node.js 的本地模块，也就是前面错误中的 node_sqlite3.node 文件。这是一个二进制文件，对 V8 引擎版本敏感。由于 sqlite 3 模块在发布时使用的是 Node.js 中的 V8 引擎，因而放在 Electron 中自然就不好使，要想在 Electron 中使用 sqlite 3 模块，就必须利用 Electron V8 引擎重新编译 sqlite 3 模块。</p>
<h3 id="192sqlite3">19.2 编译 sqlite 3 模块</h3>
<p>由于 sqlite 3 模块底层是使用 C 语言编写的，因而编译 sqlite 3 模块需要 C/C++ 编译器。在 Mac OS X 下，需要安装 XCode，Linux 可以使用 GCC，Windows 下可以选择 Visual Studio。</p>
<p>这里重点说一下 Windows 的配置，因为 Mac OS X 和 Linux 下的 C/C++ 环境比较简单，也没有兼容性问题。</p>
<p>在 Windows 下 C/C++ 开发环境通常使用 Visual Studio，目前最新的是 Visual Studio 2017，读者可以安装免费的 Visual Studio 2017 社区版，不过社区版安装程序的尺寸很大，安装比较费事，可以单独安装 Windows 的建立工具，<a href="https://github.com/felixrieseberg/windows-build-tools">下载地址详见这里</a>。</p>
<p>在编译的过程中，需要使用 node-gyp 工具，来为 Node.js 编译本地模块，不过这个工具是用 Python 写的，而且是 Python 2.7，在安装 node-gyp 之前，需要确认一下。如果读者使用的是 Mac OS X 和大多数 Linux 发行版，默认带 Python 2.7，如果读者使用的 Windows，就需要安装 Python 2.7；如果读者的机器上已经安装了多个 Python 版本，建议安装 Anaconda 环境，可以很容易在 Python 2.7 和 Python 3.x 之间切换。</p>
<p>安装完 Python 2.7 后，使用下面的命令安装 node-gyp。</p>
<pre><code>npm install -g node-gyp
</code></pre>
<p><a href="https://github.com/nodejs/node-gyp">node-gyp 的官方地址详见这里</a>。</p>
<p>一切就绪后，就可以开始编译 sqlite 3 模块了。</p>
<p>现在进入 Electron 工程根目录，使用下面的 3 个命令从零开始安装和编译 sqlite 3 模块。</p>
<pre><code>npm install --save sqlite3
npm install --save electron-rebuild
./node_modules/.bin/electron-rebuild -v 3.0.2
</code></pre>
<p>其中 3.0.2 是依赖的 Electron 版本，一般与当前使用的 Electron 版本相同。执行上面的命令后，如果成功编译，再执行前面的创建内存数据库的内容就会和在 Node.js 中执行的效果相同；如果在 Windows 下编译 sqlite 3 模块，需要将 electron-rebuild 换成 electron-rebuild.cmd，完整的命令如下。</p>
<pre><code>npm install --save sqlite3
npm install --save electron-rebuild
.\node_modules\.bin\electron-rebuild.cmd -v 3.0.2
</code></pre>
<p>如果前面的操作一切顺利，现在可以在 Electron 中使用 sqlite 3 模块操作 SQLite 数据库了，由于 sqlite 3 模块底层使用的是 C 语言，因而运行效率相当高。</p>
<blockquote>
  <p>注意：如果编译成功，可以直接将 node_modules 目录中的 sqlite 3 子目录备份，以后换到新机器上，直接将 sqlite 3 目录作为 node_modules 目录的子目录即可，这样就不需要再编译 sqlite 3 模块了。</p>
</blockquote>
<h3 id="193sqlite3sqlite">19.3 使用 sqlite 3 模块操作 SQLite 数据库</h3>
<p>下面利用 sqlite 3 模块实现一个对 SQLite 数据库增、删、改、查的例子。</p>
<ul>
<li>主页面 index.html</li>
</ul>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--指定页面编码格式--&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--指定页头信息--&gt;
  &lt;title&gt;SQLite数据库&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;

&lt;/head&gt;
&lt;body&gt;
    &lt;button id="button_create" onclick="onClick_CreateDatabase()"&gt;创建SQLite数据库&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_insert" onclick="onClick_Insert()" disabled&gt;插入记录&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_query" onclick="onClick_Query()" disabled&gt;查询记录&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_update" onclick="onClick_Update()" disabled&gt;更新记录&lt;/button&gt;
    &lt;p/&gt;
    &lt;button id="button_delete" onclick="onClick_Delete()" disabled&gt;删除记录&lt;/button&gt;
    &lt;p/&gt;
    &lt;label id="label_rows"&gt;&lt;/label&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li>event.js 脚本文件</li>
</ul>
<pre><code>const sqlite3 = require('sqlite3').verbose();

let db;
var fs = require('fs');
//创建数据库
function onClick_CreateDatabase() {
    fs.exists('test.db',function(exists){
        if(exists) {
            fs.unlinkSync('test.db');
        }
        db = new sqlite3.Database('test.db', sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) =&gt; {
            if (err) {
                alert(err.message);
            } else {
                alert('成功连接test.db数据库!');

                let createTableSQL = `create table if not exists t_products(
                          id integer primary key autoincrement,
                          product_name varchar(100) not null,
                          price float not null
                      )`;
                db.run(createTableSQL, function(err) {
                    if (err) {
                        alert(err.message);
                    } else {

                        button_create.disabled = true;
                        button_insert.disabled = false;

                    }
                });

            }
        });
    })
}
//插入记录
function onClick_Insert() {
    if(db == undefined) return;
    let insertSQL = 'insert into t_products(product_name,price) select "iPhone10",10000 union all select "Android手机",8888 union all select "特斯拉",888888;'
    db.run(insertSQL, function(err) {
        if (err) {
            alert(err.message);
        } else {
            alert('成功插入记录');
            button_insert.disabled = true;
            button_query.disabled = false;
            button_update.disabled = false;
            button_delete.disabled = false;
        }
    });
}
//查询记录
function onClick_Query() {
    if(db == undefined) return;
    let selectSQL = 'select * from t_products';
    db.all(selectSQL, [],function(err,rows) {
        if (err) {
            alert(err.message);
        } else {
            label_rows.innerText = '';
            for(var i = 0; i &lt; rows.length;i++) {
                label_rows.innerText += '\r\n产品ID:' + rows[i].id +
                                        '\r\n产品名称:' + rows[i].product_name +
                                        '\r\n产品价格:' + rows[i].price + '\r\n';

            }
        }
    });
}
//更新记录
function onClick_Update() {
    if(db == undefined) return;
    let updateSQL = 'update t_products set price = 999999 where id = 3';
    db.run(updateSQL, function(err) {
        if (err) {
            alert(err.message);
        } else {
            alert('成功更新记录');

        }
    });
}
//删除记录
function onClick_Delete() {
    if(db == undefined) return;
    let deleteSQL = 'delete from t_products where id = 2';
    db.run(deleteSQL, function(err) {
        if (err) {
            alert(err.message);
        } else {
            alert('成功删除记录');

        }
    });
}
</code></pre>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>