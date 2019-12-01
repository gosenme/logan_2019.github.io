---
title: Electron 开发入门-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>不管是 localStorage，还是 SQLite，都将数据保存在本地，而且无法多台电脑共享（除非将数据库文件复制到其他的电脑中）。如果想让数据在多台电脑之间共享，而且支持更复杂的操作，如锁定某张表或某条记录、防止脏数据等，可以使用网络关系型数据库，其中 MySQL 是这类数据库的代表，用户基数非常大。本节将会讲解如何直接在 Electron 中连接 MySQL 数据库。</p>
<p>几乎所有的 Web 应用以及桌面管理系统，都是在服务端访问数据库，然后将数据通过 HTTP(S) 返回给客户端，客户端并不直接与数据库交互。但对于某些应用，如 DBMS（数据库管理系统），需要直接与数据库交互，这样就需要在客户端直接与服务端的数据库交互，也称为数据库的直连。</p>
<h3 id="201mysql">20.1 安装 mysql 模块</h3>
<p>在 Node.js 中访问 MySQL 数据库需要使用 mysql 模块，该模块不是 Node.js 的标准模块，因此需要在 Electron 工程根目录执行下面的命令安装。</p>
<pre><code>npm install --save mysql
</code></pre>
<p>mysql 模块是纯的 JavaScript 实现的，不存在兼容性问题，在 Node.js 和 Electron 中都可以使用。而且 mysql 模块操作 MySQL 数据库执行的是网络操作，用任何编程语言实现的效率差不多，并不会因为是用 JavaScript 实现的而降低操作 MySQL 数据库的效率。</p>
<p>首先用下面的代码导入 mysql 模块。</p>
<pre><code>const mysql = require('mysql');
</code></pre>
<p>然后使用下面的代码连接 MySQL 数据库。</p>
<pre><code>conn = mysql.createConnection({
    host: MySQL服务器的IP或域名,
    user: 用户名,
    password: 密码,
    database: 数据库名,
    port: 3306   //MySQL 的默认端口号
});
</code></pre>
<p>接下来可以使用 conn.query 方法执行 SQL 语句。</p>
<h3 id="202mysqlmysql">20.2 使用 mysql 模块操作 MySQL 数据库</h3>
<p>下面给出一个完整的案例，用来演示如何使用 mysql 模块操作 MySQL 数据库。</p>
<p>（1）首先编写主页面（index.html）的代码。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;!--指定页面编码格式--&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;!--指定页头信息--&gt;
  &lt;title&gt;MySQL数据库&lt;/title&gt;
  &lt;script src="event.js"&gt;&lt;/script&gt;

&lt;/head&gt;
&lt;body&gt;
    &lt;button id="button_create" onclick="onClick_OpenDatabase()"&gt;打开MySQL数据库&lt;/button&gt;
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
<p>通常操作 MySQL 数据库时不会用代码创建数据库，而是利用已经创建好的数据库，因此，index.html 页面中只添加了“打开 MySQL 数据库”按钮。</p>
<p>（2）接下来编写 event.js 文件的代码。</p>
<pre><code>const mysql = require('mysql');
let conn;
//打开 MySQL 数据库
function onClick_OpenDatabase() {

    conn = mysql.createConnection({
        host: '127.0.0.1',
        user: "root", //数据库用户名
        password: "12345678", //数据库密码
        database: "cloudnote", //数据库
        port: 3306
    });
    const createTableSQL = `create table if not exists t_products(
                          id integer primary key auto_increment,
                          product_name varchar(100) not null,
                          price float not null  )`;
    //创建 t_products 表
    conn.query(createTableSQL, function (err, result) {
        if (err) console.log(err);
        else {
            const clearSQL = 'delete from t_products';
            conn.query(clearSQL,[],function (err,result) {
                alert('成功打开MySQL数据库');
                button_create.disabled = true;
                button_insert.disabled = false;
            });
        }
    });
}
//插入记录
function onClick_Insert() {
    if(conn == undefined) return;
    let insertSQL = 'insert into t_products(product_name,price) select "iPhone10",10000 union all select "Android手机",8888 union all select "特斯拉",888888;'
    conn.query(insertSQL,function (err, result) {
        if (err) console.log(err);
        else {
            alert('成功向t_products表插入记录');
            button_insert.disabled = true;
            button_query.disabled = false;
            button_update.disabled = false;
            button_delete.disabled = false;
        }
    });
}
//查询记录
function onClick_Query() {
    if(conn == undefined) return;
    let selectSQL = 'select * from t_products';
    conn.query(selectSQL, function (err, result) {
        if (err) console.log(err);
        else {
            label_rows.innerText = '';
            for(var i = 0; i &lt; result.length;i++) {
                label_rows.innerText += '\r\n产品ID:' + result[i].id +
                    '\r\n产品名称:' + result[i].product_name +
                    '\r\n产品价格:' + result[i].price + '\r\n';

            }
        }
    });
}
//更新记录
function onClick_Update() {
    if(conn == undefined) return;
    let updateSQL = 'update t_products set price = 999999 where product_name = "特斯拉"';
    conn.query(updateSQL, function (err, result) {
        if (err) console.log(err);
        else {
            alert('成功更新记录');
        }
    });
}
//删除记录
function onClick_Delete() {
    if(conn == undefined) return;
    let deleteSQL = 'delete from t_products where product_name = "iPhone10"';
    conn.query(deleteSQL, function (err, result) {
        if (err) console.log(err);
        else {
            alert('成功删除记录');
        }
    });

}
</code></pre>
<p>运行程序，并打开数据库，插入记录，然后查询记录，会看到如下图的输出结果。由于本例未删除 t_products 表，因而删除记录再重新插入时，t_products 表的自增字段的值并不会归位（从 1 开始），仍然会在自增字段最大值的基础上加 1，因此第 1 条记录的 id 字段值是 4。</p>
<p><img src="https://images.gitbook.cn/ee6cbdf0-85cb-11e9-8d2b-35887fa4df64"  width = "40%" /></p>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>请添加小助手伽利略微信 GitChatty6，并将支付截图发给她，小助手会拉你进课程学习群。</p></div></article>