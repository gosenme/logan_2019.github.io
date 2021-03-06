---
title: Python 快速入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">数据库支持</h3>
<blockquote>
  <p>在大多数应用场景中，数据持久化都是重要的需求。一般地，数据持久化可以采用文件，数据库系统，以及一些混合类型。</p>
  <p>使用简单的文本文件就可以实现数据的读写，辅助完成很多功能。但是，在一些场景下，我们需要更强大的特性，比如，同时采用多个字段或属性进行复杂的搜索，显然，使用文本文件难以实现，数据库倒是一个不错的选择。</p>
</blockquote>
<p>Python 标准数据库接口为 Python DB-API，Python DB-API 为开发人员提供了数据库应用标准接口，可以支持大部分数据库，包括 MySQL、PostgreSQL、Microsoft SQL Server、Oracle、Sybase 等。详细信息可查阅<a href="https://wiki.python.org/moin/DatabaseInterfaces">官网说明</a>。</p>
<p>操作不同的数据库需要下载不同的 DB API 模块，例如访问 Oracle 数据库和 MySQL 数据库，需要下载 Oracle 和 MySQL 数据库模块。DB-API 是一个规范，它定义一个系列必须的对象和数据库存取方式，以便为各种各样的底层数据库系统和数据库接口程序提供一致的访问接口。</p>
<p>Python DB-API 为大多数数据库实现了接口，使用它连接各种数据库后，就可以使用相同的方式操作各种数据库。</p>
<h4 id="pythonmysql">Python 操作 MySQL</h4>
<p>虽然不同数据库差异显著，但使用 Python DB-API 操作各种数据库的方式大体一致，可以归纳为四个步骤：</p>
<ol>
<li>导入模块；</li>
<li>与数据库建立连接；</li>
<li>执行数据库操作；</li>
<li>关闭数据库连接。</li>
</ol>
<p>接下来以关系型数据库 MySQL 为例介绍 Python 操作数据库的一般方式。</p>
<p><strong>1. 搭建数据库系统。</strong></p>
<p>既然要操作数据库，就必须要有现成的数据库系统作为服务端，因此，需安装 MySQL，启动服务（非本文重点，不做展开）。</p>
<p><strong>2. 安装与 MySQL 对应的 Python 模块。</strong></p>
<p>本节以 mysql-connector-python 为例（附：<a href="https://pypi.org/project/mysql-connector-python">下载地址</a>）下载解压到自定义路径下，通过命令行进入包路径，执行安装命令：<code>sudo python setup.py install</code> （Linux或Mac），或 <code>Python setup.py install</code>（Windows）。</p>
<p><strong>3. 导入模块并创建连接。</strong></p>
<p>请参考下面代码：</p>
<pre><code>import mysql.connector

#数据库配置，据实填写
db_config={'host':'127.0.0.1',
        'user':'root',
        'password':'123**456',
        'port':3306,
        'database':'test',
        'charset':'utf8'
        }
try:
   #connect方法加载config的配置进行数据库的连接，完成后用一个变量进行接收
    cnn=mysql.connector.connect(**db_config)
except mysql.connector.Error as e:
    print('operation failed！',str(e))
else:
    print("operation succeeded!")
</code></pre>
<p><strong>4. 执行数据库操作。</strong></p>
<p>代码如下：</p>
<pre><code>#创建表的sql语句
sql_create_table='CREATE TABLE`student`\
(`id`int(10)NOT NULL AUTO_INCREMENT,\
`name`varchar(10) DEFAULT NULL,\
`age`int(3) DEFAULT NULL,\
PRIMARY KEY(`id`))\
ENGINE=MyISAM DEFAULT CHARSET = utf8'

#buffered=True会把结果集保存到本地并一次性返回，这样可以提高性能
cursor = cnn.cursor(buffered = True)
#执行sql语句，创建表
try:
    cursor.execute(sql_create_table)
except mysql.connector.Error as err:
    print('operation failed！',str(err))

#执行数据库操作
try: 
    #插入  
    sql_insert1="insert into student(name,age) values ('zhang san',18)"
    cursor.execute(sql_insert1)  
except mysql.connector.Error as err:
    print('operation failed！',str(err))
finally:
    #关闭数据库相关链接
    cursor.close()
    cnn.close()
</code></pre>
<p><strong>5. 补充说明。</strong></p>
<p>数据库的操作非常多，不便展开，本节仅做简要介绍。</p>
<h4 id="pythonredis">Python 操作 Redis</h4>
<p><strong>1. 搭建数据库系统。</strong></p>
<p>首先，既然要操作数据库，前提是必须已经有现成的数据库系统作为服务端，本节以 Redis 为例，那么就需要搭建基于 Redis 的数据库服务端。</p>
<p>如果你还不会使用Redis，请参考我撰写的另一篇文章：<a href="http://gitbook.cn/gitchat/activity/5a9b8abbf055ac6f65966638">《基于 Redis 的分布式缓存实现方案及可靠性加固策略》</a>。</p>
<p><strong>2. 引入与数据库对应的 Python 模块。</strong></p>
<p>本例数据库采用 Redis，那么就需要导入支持 Python 的 Redis 客户端模块，如 redis-py（附：<a href="https://pypi.org/project/redis/#description">官方下载网址</a>），安装十分简单，以 Linux 系统为例（Mac，Windows 类似)。</p>
<ul>
<li>在线安装：</li>
</ul>
<pre><code>    $ sudo pip install redis
</code></pre>
<ul>
<li>离线安装</li>
</ul>
<p>需要下载安装包，解压，进入解压后的包路径，执行下面的安装命令：</p>
<pre><code>$ sudo python setup.py install
</code></pre>
<p><strong>3. 与数据库建立连接（普通）</strong></p>
<p>代码如下：</p>
<pre><code>import redis

#redis连接的配置：服务端的IP、端口及密码
redis_config = {
    "host": "100.120.227.67",
    "port": 6388,
    "password":"123**456"}
#创建redis连接对象
redis_con = redis.Redis(**redis_config)
#增
redis_con.set("name","ping121212121212")
#查
print("result1: %s"%(redis_con.get("name")))
#改
redis_con.set("name","ABJHJHSCJCBNJCBH")
print("result2: %s"%(redis_con.get("name")))
#删
redis_con.delete("name")
print("result3: %s"%(redis_con.get("name")))

执行结果：
result1: b'ping121212121212'
result2: b'ABJHJHSCJCBNJCBH'
result3: None
</code></pre>
<p><strong>4. 连接池。</strong></p>
<p>redis-py 使用 connection pool 来管理对一个 Redis Server 的所有连接，避免每次建立、释放连接的开销。</p>
<pre><code>import redis

#redis连接的配置：服务端的IP、端口及密码
redis_config = {
    "host": "100.120.227.67",
    "port": 6388,
    "password":"123**456"}
#创建与redis-server的连接池
redis_pool = redis.ConnectionPool(**redis_config)
redis_con = redis.Redis(connection_pool=redis_pool)
#增
redis_con.set("name","ping121212121212")
#查
print("result1: %s"%(redis_con.get("name")))
#改
redis_con.set("name","ABJHJHSCJCBNJCBH")
print("result2: %s"%(redis_con.get("name")))
#删
redis_con.delete("name")
print("result3: %s"%(redis_con.get("name")))

执行结果：
result1: b'ping121212121212'
result2: b'ABJHJHSCJCBNJCBH'
result3: None
</code></pre>
<p><strong>5. 补充说明</strong></p>
<p>数据库的操作非常多，不便展开，本节仅介绍几个常用的操作，读者若感兴趣，可以自行深入探索。</p>
<h3 id="-1">网络编程</h3>
<blockquote>
  <p>Python 集成了针对常用网络协议的库，对网络协议的各个层次都进行了抽象封装，如此，开发者可以集中精力处理程序逻辑，而不必关心网络实现的细节。</p>
  <p>Python 提供了丰富的网络工具，接下来，本节将介绍 Python 标准库提供的一个最基础的网络设计模块：Socket，以点带面。在最后两章的抢票软件和爬虫实例中将介绍一些高级的网络编程模块。</p>
</blockquote>
<h4 id="socket">Socket</h4>
<p>在网络编程中，最基本的组件就是套接字（Socket），套接字是两个端点的程序之间信息传递的通道。程序通常分布运行在不同的计算机上，通过套接字相互传递信息，在 Python 中，大多数网络编程模块都隐藏了 Socket 模块的基本细节，不直接和套接字交互。</p>
<p>Python 中，我们用 socket() 函数来创建套接字，语法格式如下：</p>
<pre><code>socket.socket([family[, type[, proto]]])
</code></pre>
<p><strong>1. 参数解释：</strong></p>
<ul>
<li>family：地址族。默认为 <code>AF_INET</code>，可以是 <code>AF_UNIX</code>；</li>
<li>type：套接字类型可以根据是面向连接的还是非连接分为流（<code>SOCK_STREAM</code>）或数据报（<code>SOCK_DGRAM</code>）；</li>
<li>protocol: 使用的协议，默认为0，一般使用默认值即可。</li>
</ul>
<p><strong>2. Socket 常用内建函数</strong></p>
<ul>
<li>服务端套接字</li>
</ul>
<table>
<thead>
<tr>
<th>函数名</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td>s.bind()</td>
<td>绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。</td>
</tr>
<tr>
<td>s.listen()</td>
<td>开始 TCP 监听。backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。</td>
</tr>
<tr>
<td>s.accept()</td>
<td>被动接受 TCP 客户端连接，（阻塞式）等待连接的到来。</td>
</tr>
</tbody>
</table>
<ul>
<li>客户端套接字</li>
</ul>
<table>
<thead>
<tr>
<th>函数名</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td>s.connect()</td>
<td>主动初始化 TCP 服务器连接。一般 address 的格式为元组（hostname,port），如果连接出错，返回 socket.error 错误。</td>
</tr>
<tr>
<td>s.connect_ex()</td>
<td>connect() 函数的扩展版本，出错时返回出错码，而不是抛出异常。</td>
</tr>
</tbody>
</table>
<ul>
<li>公共用途套接字函数</li>
</ul>
<table>
<thead>
<tr>
<th>函数名</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td>s.recv()</td>
<td>接收 TCP 数据，数据以字符串形式返回，bufsize 指定要接收的最大数据量。flag 提供有关消息的其他信息，通常可以忽略。</td>
</tr>
<tr>
<td>s.send()</td>
<td>发送 TCP 数据，将 string 中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于 string 的字节大小。</td>
</tr>
<tr>
<td>s.close()</td>
<td>关闭套接字</td>
</tr>
</tbody>
</table>
<h4 id="socket-1">Socket 实例</h4>
<p>基于 Socket 模块搭建一个简单的 server-client 系统，服务端启动后一直监听来自客户端的连接并回应“Hello！”。</p>
<p><strong>1. 服务端代码</strong></p>
<pre><code>import socket

#创建 socket 对象
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host=socket.gethostname() 
port=6666
# 绑定端口号
s.bind((host,port))
# 设置最大连接数，超过后排队
s.listen(5)
while True:
    # 建立客户端连接
    client,addr=s.accept()
    print("Got connection from %s"%str(addr)) 
    #回应客户端信息：hello
    msg="Hello!"  
    client.send(msg.encode('utf-8'))
    client.close()
</code></pre>
<p><strong>2. 客户端代码</strong></p>
<pre><code>import socket

# 创建 socket 对象
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名，设置端口
host=socket.gethostname() 
port=6666
# 连接服务，指定主机和端口
s.connect((host,port))
# 接收小于 1024 字节的数据
msg=s.recv(1024)
print(msg.decode('utf-8'))
s.close()
</code></pre>
<p>先执行服务端代码，再执行客户端代码，执行结果：</p>
<pre><code>服务端：Got connection from xxxxx
客户端：Hello！
</code></pre></div></article>