---
title: 程序员的 MySQL 面试金典-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="mysql">如何用命令行方式连接 MySQL 数据库？</h3>
<p>使用 <code>mysql -u用户名 -p密码;</code> 输入用户名和密码就可以正常进入数据库连接了，实例如下：</p>
<blockquote>
  <p>mysql -uroot -p123456;</p>
</blockquote>
<p>其中，用户名为 root，密码为 123456。</p>
<h3 id="mysqlh127001urootp3307p3307">关于命令 <code>mysql -h 127.0.0.1 -uroot -P 3307 -p3307</code> 以下说法错误的是？</h3>
<p>A.-h 和 -P 可以省略
B.-u 和用户名之间不能有空格
C.-p 和密码之间不能用空格
D.小写 -p 对应的是用户密码，大写 -P 对应的是 MySQL 服务器的端口</p>
<p>答：B
题目解析：-p 和密码之间不能用空格，否则空格会被识别为密码的一部分，提示密码错误。-u 和用户名之间可以有空格。</p>
<h3 id="">如何创建用户？并给用户授权？</h3>
<p>创建用户使用关键字：<code>CREATE USER</code> ，授权使用关键字： <code>GRANT</code> ，具体实现脚本如下：</p>
<pre><code class="sql language-sql">-- 创建用户 laowang
create user 'laowang'@'localhost' identified by '123456';
-- 授权 test 数据库给 laowang
grant all on test.* to 'laowang'@'localhost'
</code></pre>
<h3 id="mysql-1">如何修改 MySQL 密码？</h3>
<p>使用如下命令，修改密码：</p>
<blockquote>
  <p>mysqladmin -u用户名 -p旧密码 password 新密码;</p>
</blockquote>
<p>注意：刚开始 root 没有密码，所以 -p 旧密码一项就可以省略了。</p>
<h3 id="sql">如何使用 SQL 创建数据库，并设置数据库的编码格式？</h3>
<p>创建数据库可使用关键字： <code>CREATE DATABASE</code> ，设置编码格式使用关键字： <code>CHARSET</code> ，具体 SQL 如下：</p>
<pre><code class="sql language-sql">create database learndb default charset utf8 collate utf8_general_ci;
</code></pre>
<h3 id="-1">如何修改数据库、表的编码格式？</h3>
<p>使用 <code>alter</code> 关键字设置库或表的编码格式即可，具体代码如下：</p>
<blockquote>
  <p>mysql&gt; alter database dbname default character set utf8;
  mysql&gt; alter table t default character set utf8;</p>
</blockquote>
<h3 id="sql-1">如何使用 SQL 创建表？</h3>
<p>创建表的 SQL 如下：</p>
<blockquote>
  <p>create table t(
  t<em>id int not null auto</em>increment,
  t<em>name char(50) not null,
t</em>age int null default 18,
  primary key(t_id)
  )engine=innodb;</p>
</blockquote>
<p>其中：</p>
<ul>
<li>auto_increment：表示自增；</li>
<li>primary key：用于指定主键；</li>
<li>engine：用于指定表的引擎。</li>
</ul>
<h3 id="mysql-2">在 MySQL 命令行中如何查看表结构信息？</h3>
<p>使用 <code>desc 表名</code> 查看表结构信息，示例信息如下：</p>
<p><img src="https://images.gitbook.cn/FgMUr0ZJLJ62VlIcXh7e6UxLcLVy" alt="avatar" /></p>
<p>使用 <code>desc person;</code> 查看表 <code>person</code> 的结构信息。</p>
<h3 id="sql-2">如何使用 SQL 查看已知表的建表脚本？</h3>
<p>查看已知表的建表脚本，命令如下：</p>
<blockquote>
  <p>mysql&gt; show create table 表名; </p>
</blockquote>
<p>效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FtOxBQQ6_3R0suC7NwfdyfhUXhjP" alt="avatar" /></p>
<h3 id="sql-3">如何使用 SQL 语句更新表结构？</h3>
<p>更新表结构信息可以使用 alter table 子句，如，为表增加一列的脚本如下：alter</p>
<blockquote>
  <p>alter table t add name char(20)；</p>
</blockquote>
<p>如果要重命名表名，使用如下命令：</p>
<blockquote>
  <p>rename table new_t to t;</p>
</blockquote>
<h3 id="mysql-3">MySQL 有哪些删除方式？有什么区别？</h3>
<p>MySQL 有三种删除方式：
1）删除表数据：</p>
<blockquote>
  <p>delete from t;</p>
</blockquote>
<p>2）删除数据，保留表结构：</p>
<blockquote>
  <p>truncate table t;</p>
</blockquote>
<p>3）删数据和表结构：</p>
<blockquote>
  <p>drop table t;</p>
</blockquote>
<p>它们的区别如下：</p>
<ul>
<li>delete 可以有条件的删除，也可以回滚数据，删除数据时进行两个动作：删除与备份，所以速度很慢；</li>
<li>truncate 删除所有数据，无条件选择删除，不可回滚，保留表结构；</li>
<li>drop：删除数据和表结构 删除速度最快。</li>
</ul>
<h3 id="mysql-4">如何开启和关闭 MySQL 服务？</h3>
<p>使用 <code>systemctl stop mysqld</code> 停止 MySQL 服务，使用 <code>systemctl start mysqld</code> 启动 MySQL 服务。</p>
<h3 id="mysql-5">如何查询当前 MySQL 安装的版本号？</h3>
<p>使用 <code>SELECT VERSION();</code> 可以查询当前连接的 MySQL 的版本号。</p>
<h3 id="-2">如何查看某张表的存储引擎？</h3>
<p>可使用 <code>show table status from db where name='t';</code> 查询数据库 db 中表 t 的所有信息，其中 <code>Engine</code> 列表示表 t 使用的存储引擎，如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fr4KNWuG6HnTqDYsuWDZMtFLlS9s" alt="avatar" /></p>
<h3 id="-3">如何查看当前数据库增删改查的执行次数统计？</h3>
<p>使用以下命令行查看：</p>
<blockquote>
  <p>mysql&gt; show global status where variable<em>name in('com</em>select','com<em>insert','com</em>delete','com<em>update');
+---------------+-------+
| Variable</em>name | Value |
  +---------------+-------+
  | Com<em>delete    | 0     |
| Com</em>insert    | 1     |
  | Com<em>select    | 40    |
| Com</em>update    | 0     |
  +---------------+-------+</p>
</blockquote>
<h3 id="-4">如何查询线程连接数？</h3>
<p>使用如下命令：</p>
<blockquote>
  <p>mysql&gt; show global status like 'threads_%';</p>
</blockquote>
<p>执行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FiMigudwDmMeocTm_DaHyFkohKtW" alt="avatar" /></p>
<p>其中：</p>
<ul>
<li>Threads_cached：代表当前此时此刻线程缓存中有多少空闲线程；</li>
<li>Threads_connected：代表当前已建立连接的数量，因为一个连接就需要一个线程，所以也可以看成当前被使用的线程数；</li>
<li>Threads_created：代表从最近一次服务启动，已创建线程的数量；</li>
<li>Threads_running：代表当前激活的（非睡眠状态）线程数。</li>
</ul>
<h3 id="mysql-6">如何查看 MySQL 的最大连接数？能不能修改？怎么修改？</h3>
<p>查询 MySQL 最大连接数，使用如下命令：</p>
<blockquote>
  <p>mysql&gt; show variables like 'max_connections%';</p>
</blockquote>
<p>此命令输出的结果如下：</p>
<p><img src="https://images.gitbook.cn/FuGSsXFvu3O5d0CLZ0xD1c9JSbKM" alt="avatar" /></p>
<p>可以修改 MySQL 的最大连接数，可以在 MySQL 的配置文件 my.cnf 里修改最大连接数，通过修改 max<em>connections 的值，然后重启 MySQL 就会生效，如果 my.ini 文件中没有找到 max</em>connections，可自行添加 max_connections 的设置，内容如下：</p>
<blockquote>
  <p>max_connections=200</p>
</blockquote>
<h3 id="char_lengthlength">CHAR_LENGTH 和 LENGTH 有什么区别？</h3>
<p>CHAR<em>LENGTH 是字符数，而 LENGTH 是字节数。它们在不同编码下，值是不相同的，比如对于 UTF-8 编码来说，一个中文字的 LENGTH 为 1，而 CHAR</em>LENGTH 通常等于 3，如下图所示：</p>
<p><img src="https://images.gitbook.cn/FqB41GGLwDVq3BrNvVqgmnW0M6__" alt="avatar" /></p>
<h3 id="unionunionall">UNION 和 UNION ALL 的用途是什么？有什么区别？</h3>
<p>UNION 和 UNION ALL 都是用于合并数据集的，它们的区别如下：</p>
<ul>
<li>去重：UNION 会对结果进行去重，UNION ALL 则不会进行去重操作；</li>
<li>排序：UNION 会对结果根据字段进行排序，而 UNION ALL 则不会进行排序；</li>
<li>性能：UNION ALL 的性能要高于 UNION。</li>
</ul>
<h3 id="wherehaving">以下关于 WHERE 和 HAVING 说法正确的是？</h3>
<p>A.任何情况 WHERE 和 HAVING 都可以相互替代
B.GROUP BY 前后都可以使用 WHERE
C.使用 SELECT X FROM T HAVING Y&gt;20 查询报错
D.使用 SELECT X FROM T WHERE Y&gt;20 查询报错
答：C，HAVING 非报错用法是 <code>SELECT X,Y FROM T HAVING Y&gt;20</code> 。</p>
<h3 id="null">空值和 NULL 的区别是什么？</h3>
<p>空值表示字段的值为空，而 NULL 则表示字段没有值，它们的区别如下：</p>
<ul>
<li>空值不占用空间，NULL 值是未知的占用空间；</li>
<li>空值判断使用 <code>=''</code> 或 <code>&lt;&gt;''</code> 来判断，NULL 值使用 <code>IS NULL</code> 或 <code>IS NOT NULL</code> 来判断；</li>
<li>使用 COUNT 统计某字段时，如果是 NULL 则会忽略不统计，而空值则会算入统计之内。</li>
</ul>
<p>比如，其中字段 <code>name</code> 有两个 <code>NULL</code> 值和一个空值，查询结果如图：</p>
<p><img src="https://images.gitbook.cn/FvWDQnw2Y1nzz56iIlFlgFkk0h3x" alt="avatar" /></p>
<h3 id="mysql-7">MySQL 的常用函数有哪些？</h3>
<ul>
<li>sum(field) – 求某个字段的和值；</li>
<li>count(*) – 查询总条数；</li>
<li>min(field) – 某列中最小的值；</li>
<li>max(field) – 某列中最大的值；</li>
<li>avg(field) – 求平均数；</li>
<li>current_date() – 获取当前日期；</li>
<li>now() – 获取当前日期和时间；</li>
<li>concat(a, b) – 连接两个字符串值以创建单个字符串输出；</li>
<li>datediff(a, b) – 确定两个日期之间的差异，通常用于计算年龄。</li>
</ul></div></article>