---
title: SSM 搭建精美实用的管理系统-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="21">2.1 简介</h3>
<p>本来不打算单独用一个篇幅来介绍基础环境的搭建，但考虑到课程的受众比较广，如果因为环境问题导致某些朋友无法继续后面的课程就真的很遗憾了。</p>
<p>本文会详细的介绍 JDK 8 的安装、IDEA 2018 的安装使用、Maven 的安装和配置、MySQL 8 的安装和使用。如果已经准备好了这些基础环境，可以选择性地略过这一节。</p>
<p>考虑到 Windows 系统更为普及，本文将介绍 Windows 系统之上的环境搭建，Linux 系统上的基础环境搭建将在后续课程中介绍。</p>
<p>工欲善其事必先利其器，接下来跟随十三的讲解来安装和配置实战所需的环境和工具吧！</p>
<h3 id="22jdk8">2.2 JDK 8 安装配置</h3>
<p>根据系统选择需要下载的安装包，这里选择的是 Windows 64 位下 JDK 8 ，如果已经安装了可以跳过。</p>
<h4 id="1">1. 下载安装包</h4>
<p>首先访问 JDK 8 下载页面，链接如下：</p>
<blockquote>
  <p><a href="http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html">JDK 8 下载链接</a></p>
</blockquote>
<p>选择对应的版本，然后下载，下载前需点击 “ Accept License Agreement ” ，不然无法点击下载，过程如下图：</p>
<p><img src="https://images.gitbook.cn/6ee11ca0-89b6-11e8-85bf-17b3ec552090" alt="jdk8-download" /></p>
<h4 id="2">2. 安装</h4>
<p>下载完成后，点击安装包进行安装。需要注意的是，此步骤中 JDK 的安装路径，可以选择默认路径，也可以更改安装路径，比如十三就是更改安装路径到 F:\Java\jdk1.8.0_171 。此外，安装过程中将公共 JRE 取消安装，因为 JDK 中已经包含 JRE 了，过程如下图：</p>
<p><img src="https://images.gitbook.cn/ad5ac3a0-89b6-11e8-9da7-1fbf87a99cae" alt="jdk8-install" /></p>
<p>安装成功！</p>
<h4 id="3">3. 配置环境变量</h4>
<p>右键 “我的电脑” ，依次进入 “属性” -&gt; “高级系统设置” -&gt; “环境变量”，点击新建按钮，首先添加 JAVA<em>HOME 变量，变量值为安装步骤中选择的安装路径 F:\Java\jdk1.8.0</em>171 ，过程如下图：</p>
<p><img src="https://images.gitbook.cn/ea319010-89b6-11e8-9da7-1fbf87a99cae" alt="jdk8-env" /></p>
<p>之后编辑 PATH 变量，在变量的末尾添加 ：
<code>;%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;</code></p>
<p><img src="https://images.gitbook.cn/7be985e0-8a3d-11e8-a3f8-ff18634ae51e" alt="jdk8-path" /></p>
<p>最后增加 CLASS<em>PATH 变量，同添加 JAVA</em>HOME 变量的过程一样，点击新建按钮，输入变量名，并输入变量值 ：
<code>.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\tools.jar</code></p>
<p>环境变量设置完成。</p>
<h4 id="4">4. 检查</h4>
<p>打开命令提示符，输入 java -version ，输出版本号正确即可，十三安装的版本是 1.8.0<em>171 ，命令行输出版本号也是  1.8.0</em>171 ，配置成功，过程如下图：</p>
<p><img src="https://images.gitbook.cn/6a21ade0-89b8-11e8-b84d-8905759e9115" alt="jdk8-valid" /></p>
<p>大功告成！</p>
<h3 id="23idea2018">2.3 IDEA 2018 的安装使用</h3>
<blockquote>
  <p>IDEA 全称 IntelliJ IDEA，是用于 Java 语言开发的集成环境（也可用于其他语言），IntelliJ 在业界被公认为最好的 Java 开发工具之一，尤其在智能代码助手、代码自动提示、重构、J2EE 支持、Ant 、JUnit 、CVS 整合、代码审查、 创新的 GUI 设计等方面的功能可以说是超常的。</p>
</blockquote>
<p>十三会使用 IDEA 进行所有教程的编码工作，建议大家也使用这款开发工具。不过如果你习惯了 MyEclipse 或者 Eclipse 的话，也没有关系，项目代码是 Java Web 工程，你也可以使用 MyEclipse 或者 Eclipse 进行后续开发，并不会有什么差别。</p>
<h4 id="1-1">1. 下载安装包</h4>
<p>首先到 IDEA 的官方网站，点击 IDEA 进入下载页面，网址如下：</p>
<blockquote>
  <p><a href="https://www.jetbrains.com/idea/">IDEA 下载链接</a></p>
</blockquote>
<p>注意：<strong>请选择 Ultimate 版本下载</strong>，点击 DOWNLOAD 按钮下载即可，如下图：</p>
<p><img src="https://images.gitbook.cn/426ec140-8a33-11e8-974b-497483da0812" alt="idea-download" /></p>
<h4 id="2-1">2. 安装</h4>
<p>下载完成后，点击安装包进行安装，过程比较简单，一直点击 “ next ” 按钮即可，过程如下面图片所示。</p>
<p><strong>点击安装包程序：</strong></p>
<p><img src="https://images.gitbook.cn/5acade90-8a33-11e8-8e15-d7b3f4327e66" alt="idea-install-1" /></p>
<p><strong>安装过程：</strong></p>
<p><img src="https://images.gitbook.cn/69687a20-8a33-11e8-974b-497483da0812" alt="idea-install-2" /></p>
<p><strong>安装成功：</strong></p>
<p><img src="https://images.gitbook.cn/77fc0390-8a33-11e8-974b-497483da0812" alt="idea-install-3" /></p>
<p>由于文件比较大，可能会花一点时间。</p>
<h4 id="3-1">3. 授权</h4>
<p>由于 Ultimate 版本是收费版本，如果没有购买的话是不能使用的，不过网上有朋友提供了注册地址，因此，使用这些注册地址即可。IDEA 安装成功后第一次打开会直接跳转到授权页面，点击 License Server ，填写授权地址即可，地址为： http://123.206.193.241:1017 （如果失效，可以用这个：  http://active.chinapyg.com/ ），如果资金充裕也可以选择自行购买。</p>
<p>过程如下图：</p>
<p><img src="https://images.gitbook.cn/44321f50-8a37-11e8-974b-497483da0812" alt="idea-install-3" /></p>
<p>成功后再次打开 IDEA 就不会再跳到授权页面了。</p>
<h3 id="24maven">2.4 Maven 的安装和配置</h3>
<h4 id="1-2">1. 下载安装包</h4>
<p>首先到 Maven 的官方网站，点击 Maven 压缩包进行下载，链接及过程见下。</p>
<blockquote>
  <p><a href="http://maven.apache.org/download.cgi">Maven 的官方网站</a></p>
</blockquote>
<p><img src="https://images.gitbook.cn/5366cac0-8a37-11e8-8e15-d7b3f4327e66" alt="maven-dowanload" /></p>
<h4 id="2-2">2. 安装</h4>
<p>选择目录进行安装，我选择的是 D:\maven 目录，解压后，Maven 的安装目录为 D:\maven\apache-maven-3.5.4 ，过程如下图：</p>
<p><img src="https://images.gitbook.cn/5fc54bc0-8a37-11e8-974b-497483da0812" alt="maven-dowanload" /></p>
<p>之后则需要配置 Maven 命令的环境变量，同设置 JDK 环境变量过程一样，新增 MAVEN_HOME 变量，变量值为安装目录  D:\maven\apache-maven-3.5.4 ，过程如下：</p>
<p><img src="https://images.gitbook.cn/7500a110-8a37-11e8-8838-3badd92eb83e" alt="maven-path" /> </p>
<p>之后再修改 PATH 环境变量，在末尾增加   ;%MAVEN_HOME%\bin;  即可。</p>
<p><img src="https://images.gitbook.cn/bcfddc50-8a3a-11e8-974b-497483da0812" alt="maven-path" /> </p>
<h4 id="3-2">3. 配置文件</h4>
<p>修改配置文件，文件目录是安装目录下的 conf 目录，找到  settings.xml 文件，修改为如下配置即可：</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd"&gt;

&lt;!-- 本地仓库的路径 十三设置的是D盘maven/repo目录下 (自行配置一个文件夹即可，默认是~/.m2/repository) --&gt;
&lt;localRepository&gt;D:\maven\repo&lt;/localRepository&gt;  

 &lt;!-- 配置阿里云镜像服务器 国内镜像速度会快一些 --&gt;
 &lt;mirror&gt;    
    &lt;id&gt;alimaven&lt;/id&gt;    
    &lt;name&gt;aliyun maven&lt;/name&gt;    
    &lt;url&gt;http://maven.aliyun.com/nexus/content/groups/public/&lt;/url&gt;    
    &lt;mirrorOf&gt;central&lt;/mirrorOf&gt;            
&lt;/mirror&gt;

&lt;/settings&gt;
</code></pre>
<h4 id="4-1">4. 验证</h4>
<p>安装配置成功后，需要验证 Maven 命令是否可以在本机正常使用，验证方法同 JDK 验证相同，打开 Windows 的命令提示符，输入以下命令：</p>
<pre><code>mvn -v
</code></pre>
<p>能够正常显示 Maven 安装信息即可：</p>
<p><img src="https://images.gitbook.cn/cf4aeb50-8a3a-11e8-974b-497483da0812" alt="maven-path" /></p>
<h4 id="5ideamaven">5. IDEA 配置 Maven</h4>
<p>IDEA 默认安装了 Maven 环境，想要我们自己安装的 Maven 可以在 IDEA 中正常使用，则需要进行以下配置：</p>
<blockquote>
  <p>File -&gt; Settings -&gt; Maven</p>
</blockquote>
<p><img src="https://images.gitbook.cn/dd172d20-8a3a-11e8-974b-497483da0812" alt="maven-idea" /></p>
<p>至此，关于 Maven 的相关安装和配置已经完成。</p>
<h3 id="25mysql8">2.5 MySQL 8 的安装和使用</h3>
<p>2018 年，MySQL 8.0 正式版 8.0.11 已发布，官方表示 MySQL 8 要比 MySQL 5.7 快两倍，还带来了大量的改进和更快的性能。</p>
<p><img src="https://images.gitbook.cn/ed808800-8a3a-11e8-a075-e124f05aa6d6" alt="mysql8" /></p>
<p>本教程使用的 MySQL 数据库版本是8.0.11，如果你已经安装了其他版本的 MySQL 则可以忽略这一节，如果你想掌握 MySQL 8 的安装使用则可以跟着十三的教程体验一把。</p>
<h4 id="1-3">1. 下载安装包</h4>
<p>首先到 MySQL 8 Installer 的下载页面，链接如下：</p>
<blockquote>
  <p><a href="https://dev.mysql.com/downloads/mysql/8.0.html"> MySQL 8 Installer 下载地址</a></p>
</blockquote>
<p>选择对应的版本然后点击 Dowanload 按钮，之后会跳转到下载页面，点击页面下方的 No thanks, just start my download. 即可进行下载，过程如下图：</p>
<p><img src="https://images.gitbook.cn/0655a5e0-8a3b-11e8-8e15-d7b3f4327e66" alt="mysql8-installer-download" /></p>
<h4 id="2-3">2. 安装</h4>
<ul>
<li>解压至安装目录。</li>
</ul>
<p>首先是确定 MySQL 8 的安装目录，可以自行决定，我是将其安装在 F:\mysql-8.0.11-winx64 目录下，解压安装包至安装目录下即可。</p>
<p><img src="https://images.gitbook.cn/15a10da0-8a3b-11e8-974b-497483da0812" alt="mysql8-unzip" /></p>
<ul>
<li>配置文件。</li>
</ul>
<p>在安装目录下新建配置文件 my.ini ，配置文件中写入：</p>
<pre><code>[mysqld] 
port=3306 
basedir =F:\mysql-8.0.11-winx64 
datadir =F:\mysqlData\
max_allowed_packet = 20M
</code></pre>
<p>保存即可，其中 datadir 为数据存储目录，十三将其放在了  F:\mysqlData\ 目录下，你可以对应地进行修改。</p>
<ul>
<li>初始化 MySQL 8 。</li>
</ul>
<p>打开命令行，进入 MySQL 的 bin 目录下，之后进行初始化，命令为：</p>
<pre><code>mysqld --initialize --console
</code></pre>
<p>初始化成功后，命令行会打印出 root 用户的初始密码（记得保存，如果没有报错或者忘记的话，删掉初始化的 datadir 目录再次进行初始化即可），过程如下图：</p>
<p><img src="https://images.gitbook.cn/2429e8b0-8a3b-11e8-8e15-d7b3f4327e66" alt="mysql8-initialize" /></p>
<ul>
<li>启动 MySQL 服务。</li>
</ul>
<p>在启动服务前，首先要将 MySQL 8 安装为 Windows 的系统服务，在 MySQL 的 bin 目录执行命令如下：</p>
<pre><code>mysqld --install mysql8
</code></pre>
<p>其中 mysql8 为服务名称，你可以自行修改成想要的名字。</p>
<p>服务注册成功后，就可以启动 MySQL 服务了，执行命令：</p>
<pre><code>net start mysql8
</code></pre>
<ul>
<li>登录 MySQL 。</li>
</ul>
<p><img src="https://images.gitbook.cn/2279dcd0-8a3d-11e8-974b-497483da0812" alt="mysql8-login" /></p>
<p>服务启动成功后，则可以登录 MySQL 服务器了，在 bin 目录下执行 mysql -uroot -p ，输入刚刚保存的密码即可。不过首次登录 MySQL 时需要修改 root 用户密码，不然是无法进行操作的。需要执行的修改 root 用户密码操作，如下：</p>
<pre><code>ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '131313';
FLUSH PRIVILEGES;
</code></pre>
<p><img src="https://images.gitbook.cn/3b10e040-8a3d-11e8-8e15-d7b3f4327e66" alt="mysql8-alter-password" /></p>
<p>十三修改密码为 131313 ，你可以按照你的要求进行设置，之后就可以进行操作了。</p>
<ul>
<li>验证。</li>
</ul>
<p>通过客户端连接 MySQL 8，输入用户名密码无报错即为登录成功，如下图：</p>
<p><img src="https://images.gitbook.cn/46c51780-8a3d-11e8-974b-497483da0812" alt="mysql8-login-by-app" /></p>
<p>安装成功！</p>
<p>还是要再提醒一下各位，如果已经安装了其他版本的 MySQL 也是可以的，后续实战教程对于 MySQL 版本没有特殊要求。</p>
<h3 id="26">2.6 总结</h3>
<p>磨刀不误砍柴工，事先准备好环境才有利于进行后续的操作，不过篇幅有限，本篇文章只介绍了 Windows 系统上的安装配置过程，Linux 系统上基础环境的搭建会在另一篇文章中介绍。</p>
<p>通过以上几个步骤，本次实战教程的基础准备工作就完成了。同时还要提醒各位的是，如果你习惯了其他的代码编辑工具或者已经安装了其他版本的 MySQL 、Maven 、JDK，都没有关系，代码与这些是没有强关联的，因此不用过多地纠结于这个事情，如果看完本教程你没有安装成功，可以另行通过其他详细些的教程进行环境搭建。</p></div></article>