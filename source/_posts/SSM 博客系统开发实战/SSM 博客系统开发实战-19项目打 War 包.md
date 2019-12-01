---
title: SSM 博客系统开发实战-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="war">项目打 War 包</h3>
<p>项目打包之前确保你的编码格式都是 UTF-8 的，否则到 Linux 系统中会出现乱码。设置好编码格式后，看下配置文件有没有乱码，如果有乱码，将乱码文字替换成之前的中文。发生乱码的原因是有的配置文件之前采用的是 GBK 编码格式，设置编码格式如下：</p>
<p><img src="https://images.gitbook.cn/5450c2d0-81b6-11e8-a717-a33813ad3d51" alt="enter image description here" /></p>
<p>上次我们打包使用的是 install 命令，这次我们换个打包方式，如图：</p>
<p><img src="https://images.gitbook.cn/c23d8a30-81ca-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/b29de7f0-81ca-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>War 和 war exploded 的区别请参见博客：<a href="https://blog.csdn.net/xlgen157387/article/details/56498938">《Tomcat 部署时 war 和 war exploded 区别以及平时踩得坑》</a></p>
<p>在你的项目路径 <code>dreamland\dreamland-web\target</code> 下找到刚打包好的 <code>dreamland-web.war</code>，复制到桌面重命名为 ROOT.war，待会部署到 Linux 系统。</p>
<h3 id="linux">Linux 系统安装相关服务</h3>
<p>部署项目需要 JDK、Tomcat、MySQL 等环境，所以要先安装相关服务。</p>
<h4 id="">准备</h4>
<p><strong>1.</strong> 安装 CentOS7。</p>
<p>不会安装的同学请参考博文：<a href="https://blog.csdn.net/guo_ridgepole/article/details/78973763">《VMware 安装14.0安装 CentOS7.2》</a>。</p>
<p><strong>2.</strong> 下载安装 Xshell6 和 Xftp6。</p>
<p>为了更方便操作 Linux 系统，我们下载安装 Xshell6 和 Xftp6，具体步骤参考博文：<a href="https://blog.csdn.net/abcwanglinyong/article/details/80483646">Xshell6 下载安装</a>。</p>
<p><strong>3.</strong> 开启虚拟机。</p>
<p>CentOS7 安装好以后，开启虚拟机，输入用户名密码，登陆后输入命令：</p>
<pre><code>ip addr
</code></pre>
<p>查看该虚拟机分配的 IP 地址，如图：</p>
<p><img src="https://images.gitbook.cn/07795c40-8262-11e8-b6c5-95ed8a49f1f8" alt="enter image description here" /></p>
<p>然后打开 Xshell6，新建连接，输入名称和 IP 后点击确定，如图：</p>
<p><img src="https://images.gitbook.cn/943f9180-8262-11e8-9e1d-f13ca808ab04" alt="enter image description here" /></p>
<p>然后点击 dreamland，输入用户名和密码即可连接此虚拟机，如图：</p>
<p><img src="https://images.gitbook.cn/9a2238a0-8262-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p><strong>4.</strong> 首先我们在 <code>/home</code> 目录下创建 softs 目录，将相关安装包都放在该目录下：</p>
<pre><code>cd /home/
mkdir softs
</code></pre>
<p><strong>5.</strong> 点击 xftp 图标，打开文件传输窗口，找到我们要使用的安装包，通过鼠标右键 -&gt; 传输，将安装包上传到我们刚刚创建的 softs 目录下，如图：</p>
<p><img src="https://images.gitbook.cn/4d7b63c0-8265-11e8-878d-d106b6fbe32a" alt="enter image description here" /></p>
<p>相关安装包我会放到百度网盘中。</p>
<h4 id="jdk">JDK 安装及环境变量配置</h4>
<p>进入 softs 目录查看：</p>
<pre><code>cd /home/softs/ 
ll
</code></pre>
<p><img src="https://images.gitbook.cn/f4d8fc20-826c-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>然后使用 <code>tar -zxvf 压缩包名</code> 解压命令解压 JDK 安装包。</p>
<pre><code>tar -zxvf jdk-8u77-linux-x64.tar.gz 
</code></pre>
<p>解压完成以后，配置环境变量，编辑 profile 文件：</p>
<pre><code>vi /etc/profile
</code></pre>
<p>在 profile 文件最后，点击键盘 i 可编辑内容，在文末加入以下内容：</p>
<pre><code>export JAVA_HOME=/home/softs/jdk1.8.0_77  #你的jdk安装路径
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
    export PATH=$PATH:$JAVA_HOME/bin
</code></pre>
<p>然后ESC，输入</p>
<pre><code>:wq!
</code></pre>
<p>保存退出（取消保存是 <code>:q!</code>），如图：</p>
<p><img src="https://images.gitbook.cn/77b03450-826e-11e8-9e1d-f13ca808ab04" alt="enter image description here" /></p>
<p>输入以下命令使配置的环境变量立即生效：</p>
<pre><code>source /etc/profile 
</code></pre>
<p>查看 Java 版本：</p>
<pre><code>java-version
</code></pre>
<p>如果出现 Java 版本信息就表示配置环境变量成功，如图：</p>
<p><img src="https://images.gitbook.cn/dd805a30-826e-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<h3 id="tomcat">Tomcat 安装及开机自启动配置</h3>
<p>进入 softs 目录，使用同样方法解压 Tomcat 安装包：</p>
<pre><code>tar -zxvf apache-tomcat-8.0.47.tar.gz 
</code></pre>
<p>编辑 rc.local 文件，配置 JDK 路径和开机启动设置：</p>
<pre><code>vi /etc/rc.d/rc.local 
</code></pre>
<p>在 rc.local 文件最后加上下面两行脚本，保存后退出：</p>
<pre><code>export JAVA_HOME=/home/softs/jdk1.8.0_77  # jdk的安装路径
/home/softs/apache-tomcat-8.0.47/bin/startup.sh start #tomcat安装目录的启动文件
</code></pre>
<p>修改 rc.local 文件为可执行:</p>
<pre><code>cd /etc/rc.d
chmod +x rc.local
</code></pre>
<p>通过下面命令可查看防火墙状态：</p>
<pre><code>firewall-cmd  --state
</code></pre>
<p>显示 running，说明防火墙默认是打开的。</p>
<p>查看防火墙开放的端口：</p>
<pre><code>firewall-cmd --list-ports
</code></pre>
<p>发现现在还没有开放端口，所以即使启动了 Tomcat 也访问不了。</p>
<h4 id="-1">防火墙设置</h4>
<p>这里根据需要设置防火墙，即开放我们需要的端口，你也可以直接关闭防火墙。</p>
<p>开放端口命令如下：</p>
<pre><code>firewall-cmd --zone=public --add-port=3306/tcp --permanent
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=61616/tcp --permanent
firewall-cmd --zone=public --add-port=8161/tcp --permanent
</code></pre>
<p>然后重启防火墙：</p>
<pre><code>firewall-cmd --reload 
</code></pre>
<p>再次查看已开放端口：</p>
<pre><code>firewall-cmd --list-ports
</code></pre>
<p>发现我们需要的端口已经开放，结果如下：</p>
<pre><code>8161/tcp 3306/tcp 61616/tcp 80/tcp 8080/tcp
</code></pre>
<p>开启、关闭防火墙命令，永久性生效，重启后不会复原。</p>
<blockquote>
  <p>开启： chkconfig iptables on</p>
  <p>关闭： chkconfig iptables off</p>
</blockquote>
<p>开启、关闭防火墙命令即时生效，重启后复原：</p>
<blockquote>
  <p>开启： service iptables start</p>
  <p>关闭： service iptables stop</p>
</blockquote>
<p>防火墙设置好以后，我们重启 Linux 系统（或者使用 reboot 重启）：</p>
<pre><code>shutdown -r now
</code></pre>
<p>重启完成后，重新连接，然后输入以下命令可查看 Tomcat 服务是否开机启动：</p>
<pre><code>ps -ef | grep tomcat
</code></pre>
<p>如果出现下图所示，说明 Tomcat 开机启动成功：</p>
<p><img src="https://images.gitbook.cn/5d22f010-8277-11e8-9d71-995acabbbf78" alt="enter image description here" /></p>
<p>然后可以通过：http://192.168.241.129:8080/，访问 Tomcat 页面，如图：</p>
<p><img src="https://images.gitbook.cn/c876fb40-8277-11e8-878d-d106b6fbe32a" alt="enter image description here" /></p>
<h4 id="activemq">ActiveMQ 安装及开机自启动配置</h4>
<p>进入 softs 目录，同样方法解压 ActiveMQ 压缩包：</p>
<pre><code>    tar -zxvf apache-activemq-5.15.2-bin.tar.gz
</code></pre>
<p>将 ActiveMQ 文件拷贝到 <code>/etc/init.d</code> 目录下：</p>
<pre><code>cp /home/softs/apache-activemq-5.15.2/bin/activemq /etc/init.d/
</code></pre>
<p>编辑 <code>/etc/init.d</code> 目录下的 ActiveMQ 文件：</p>
<pre><code>vi /etc/init.d/activemq
</code></pre>
<p>将 BEGIN INIT INFO 和 END INIT INFO 之间的内容修改如下：</p>
<pre><code>### BEGIN INIT INFO
# chkconfig: 345 63 37
# description: Auto start ActiveMQ
# Provides:          activemq
# Required-Start:    $remote_fs $network $syslog
# Required-Stop:     $remote_fs $network $syslog
# Default-Start:     3 5
# Default-Stop:      0 1 6
# Short-Description: Starts ActiveMQ
# Description:       Starts ActiveMQ Message Broker Server
### END INIT INFO
</code></pre>
<p>在 <code>EXEC_OPTION=""</code> 下添加以下内容：</p>
<pre><code>export JAVA_HOME=/home/softs/jdk1.8.0_77 #jdk路径
ACTIVEMQ_HOME=/home/softs/apache-activemq-5.15.2 #activemq路径
</code></pre>
<p>如图：</p>
<p><img src="https://images.gitbook.cn/bb36bae0-8279-11e8-878d-d106b6fbe32a" alt="enter image description here" /></p>
<p>ESC 保存后退出：</p>
<pre><code>:wq!
</code></pre>
<p>然后进入 <code>/etc/init.d/</code> 目录下：</p>
<pre><code>cd /etc/init.d/
</code></pre>
<p>修改 ActiveMQ 权限：</p>
<pre><code>chmod +x activemq
</code></pre>
<p>然后将 ActiveMQ 添加到系统服务：</p>
<pre><code>chkconfig --add activemq
</code></pre>
<p>使用以下命令可查看系统服务列表：</p>
<pre><code>chkconfig --list 
</code></pre>
<p>如果出现 ActiveMQ 服务，说明添加系统服务成功。</p>
<p>然后重启 Linux 系统：</p>
<pre><code>shutdown -r now
</code></pre>
<p>重启完成后，重新连接，然后输入以下命令可查看 ActiveMQ 服务是否开机启动:</p>
<pre><code>ps -ef | grep activemq
</code></pre>
<p>如果出现下图所示，说明 ActiveMQ 开机启动成功：</p>
<p><img src="https://images.gitbook.cn/3fd2fba0-827b-11e8-884a-35c5e2ab8361" alt="enter image description here" /></p>
<p>可通过：http://192.168.241.129:8161/，访问 ActiveMQ 的 Web 管理页面，如图：</p>
<p><img src="https://images.gitbook.cn/8ab0f000-827b-11e8-a717-a33813ad3d51" alt="enter image description here" /></p>
<h4 id="redis">Redis 安装及开机自启动配置</h4>
<p>进入 softs 目录下，解压 Redis 压缩包：</p>
<pre><code>tar -zxvf redis-3.2.5.tar.gz
</code></pre>
<p>编写开机自启动脚本：</p>
<pre><code>vi /etc/init.d/redis
</code></pre>
<p>输入以下脚本内容，注意将 EXEC、<code>REDIS_CLI</code> 和 CONF 的值改为自己的路径（最好是通过文件传输将 Redis 文件上传，因为复制的内容语法格式可能会发生错误。Redis文件已放入百度网盘，记得修改相关参数）：</p>
<pre><code># chkconfig: 2345 10 90  
# description: Start and Stop redis   

PATH=/usr/local/bin:/sbin:/usr/bin:/bin
REDISPORT=6379
EXEC=/home/softs/redis-3.2.5/src/redis-server    #改为你的server路径
#EXEC=/usr/local/bin/redis-server
REDIS_CLI=/home/softs/redis-3.2.5/src/redis-cli   #改为你的client路径

PIDFILE=/var/run/redis.pid   
CONF="/home/softs/redis-3.2.5/redis.conf"       #改为你的redis.conf路径
AUTH="1234"  


case "$1" in   
    start)   
            if [ -f $PIDFILE ]   
            then   
                    echo "$PIDFILE exists, process is already running or crashed."  
               else  
                       echo "Starting Redis server..."  
                       $EXEC $CONF   
               fi   
               if [ "$?"="0" ]   
               then   
                       echo "Redis is running..."  
               fi   
               ;;   
       stop)   
               if [ ! -f $PIDFILE ]   
               then   
                       echo "$PIDFILE exists, process is not running."  
               else  
                       PID=$(cat $PIDFILE)   
                       echo "Stopping..."  
                      $REDIS_CLI -p $REDISPORT  SHUTDOWN    
                       sleep 2  
                      while [ -x $PIDFILE ]   
                      do  
                               echo "Waiting for Redis to shutdown..."  
                              sleep 1  
                       done   
                       echo "Redis stopped"  
               fi   
               ;;   
       restart|force-reload)   
               ${0} stop   
               ${0} start   
               ;;   
       *)   
              echo "Usage: /etc/init.d/redis {start|stop|restart|force-reload}" &gt;&amp;2  
               exit 1  
esac    
</code></pre>
<p>保存后退出：</p>
<pre><code>:wq!
</code></pre>
<p>然后进入 <code>/etc/init.d/</code> 目录下：</p>
<pre><code>cd /etc/init.d/
</code></pre>
<p>设置 Redis 权限为可执行文件：</p>
<pre><code>chmod 755 redis
</code></pre>
<p>设置 Redis 开机自启动：</p>
<pre><code>chkconfig redis on
</code></pre>
<p>然后重启 Linux 系统：</p>
<pre><code>shutdown -r now
</code></pre>
<p>重启完成后，重新连接，然后输入以下命令可查看 Redis 服务是否开机启动：</p>
<pre><code>ps -ef | grep redis
</code></pre>
<p>如果出现下图所示，说明 Redis 开机启动成功：</p>
<p><img src="https://images.gitbook.cn/4fa617b0-8280-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<h4 id="mysql">MySQL 安装及开机自启动设置</h4>
<p>因为我们需要使用 wget 命令下载 MySQL 源码包，所以先下载安装 wget（需联网）：</p>
<pre><code>yum -y install wget
</code></pre>
<p>然后下载 MySQL 源安装包：</p>
<pre><code>wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
</code></pre>
<p>安装 MySQL 源：</p>
<pre><code>yum localinstall mysql57-community-release-el7-8.noarch.rpm
</code></pre>
<p>中间有提示“Is this ok”，输入：y。</p>
<p>检查 MySQL 源是否安装成功：</p>
<pre><code>yum repolist enabled | grep "mysql.*-community.*"
</code></pre>
<p>如果出现下图所示，说明安装成功：</p>
<p><img src="https://images.gitbook.cn/ab3e5b30-8282-11e8-9f90-95294e517933" alt="enter image description here" /></p>
<p>安装 MySQL：</p>
<pre><code>yum install mysql-community-server
</code></pre>
<p>设置 MySQL 开机启动：</p>
<pre><code>systemctl enable mysqld
</code></pre>
<p>重新载入 systemd，扫描新的或有变动的单元：</p>
<pre><code>systemctl daemon-reload
</code></pre>
<p>然后重启 Linux 系统：</p>
<pre><code>shutdown -r now
</code></pre>
<p>重启完成后，重新连接，然后输入以下命令可查看 MySQL 服务是否开机启动：</p>
<pre><code>ps -ef | grep mysql
</code></pre>
<p>如果出现下图所示，说明 MySQL 开机启动成功：</p>
<p><img src="https://images.gitbook.cn/525a6570-8284-11e8-884a-35c5e2ab8361" alt="enter image description here" /></p>
<p>MySQL 安装完成之后，在 <code>/var/log/mysqld.log</code> 文件中给 root 生成了一个默认密码。通过下面的命令找到 root 默认密码：</p>
<pre><code>grep 'temporary password' /var/log/mysqld.log
</code></pre>
<p>如图所示：</p>
<p><img src="https://images.gitbook.cn/d52250d0-8284-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>在修改密码之前，我们先修改下 MySQL 密码检查策略，因为 MySQL 5.7默认安装了密码安全检查插件，默认密码检查策略要求密码必须包含：大小写字母、数字和特殊符号，并且长度不能少于8位。太复杂不方便记忆，你也可以选择不修改。</p>
<p>编辑 <code>/etc/my.cnf</code> 文件：</p>
<pre><code>vi /etc/my.cnf
</code></pre>
<p>在文件最后添加 <code>validate_password = off</code> 禁用密码检查策略。</p>
<p>重新启动 MySQL 服务使配置生效：</p>
<pre><code>systemctl restart mysqld
</code></pre>
<p>修改 MySQL 默认登录密码，首先登录 MySQL，用户名为 root，密码为上面查到的：<code>s/jOu_fdr3,r</code>，输入：</p>
<pre><code>mysql -uroot -p
</code></pre>
<p>然后输入密码后回车，此方式可使密码不可见。</p>
<p>MySQL 登录成功后，设置新密码，我这里就把密码设置为 root （和项目中的数据库密码一致）：</p>
<pre><code>set password for 'root'@'localhost'=password('root'); 
</code></pre>
<p>添加远程登录用户，下面语句表示：允许 wly 用户在任意主机上访问该数据库，访问密码为 <code>root</code>：</p>
<pre><code>GRANT ALL PRIVILEGES ON *.* TO 'wly'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
</code></pre>
<p>此时我就可以通过 Navicat 管理工具访问 MySQL 数据库了，如图：</p>
<p><img src="https://images.gitbook.cn/acf3e120-8287-11e8-9f90-95294e517933" alt="enter image description here" /></p>
<p>退出 MySQL 的命令是：</p>
<pre><code>exit
</code></pre>
<p>退出后，设置 MySQL 默认编码为 UTF-8，修改 <code>/etc/my.cnf</code> 配置文件：</p>
<pre><code>vi /etc/my.cnf
</code></pre>
<p>在 <code>[mysqld]</code> 下添加编码配置，如下所示：</p>
<pre><code>[mysqld]
character_set_server=utf8
init_connect='SET NAMES utf8'
</code></pre>
<p>保存后退出。</p>
<p>重新启动 MySQL 服务：</p>
<pre><code>systemctl restart mysqld
</code></pre>
<p>可用新密码登录 MySQL 并查看数据库默认编码：</p>
<pre><code>show variables like '%character%';
</code></pre>
<p>查询结果如图：</p>
<p><img src="https://images.gitbook.cn/2b92c6d0-8289-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>将本地数据库导出为 <code>dream_db.sql</code>，在 <code>/home</code> 目录下新建 dreamland 目录，通过 xftp 文件上传工具，将 <code>dream_db.sql</code> 文件上传到 <code>/home/dreamland/</code> 目录下。</p>
<p>然后登录 MySQL，创建数据库 <code>dream_db</code> 并设置字符集：</p>
<pre><code>create database dream_db default charset utf8 collate utf8_general_ci;
</code></pre>
<p>使用 <code>show databases;</code> 可查看所有数据库，然后切换数据库：</p>
<pre><code>use dream_db;
</code></pre>
<p>导入 SQL 文件：</p>
<pre><code>source /home/dreamland/dream_db.sql;
</code></pre>
<p>使用 <code>show tables;</code> 可查看所有表。</p>
<p>使用 <code>desc user;</code> 可查看 User 表的表结构。</p>
<h3 id="-2">部署项目</h3>
<p><strong>1.</strong> 将 <code>/home/softs/apache-tomcat-8.0.47/webapps/</code> 目录下的 ROOT 文件夹删除。</p>
<p><strong>2.</strong> 通过 xftp 文件传输工具将之前放在桌面的 ROOT.war 上传到 <code>/home/softs/apache-tomcat-8.0.47/webapps/</code> 目录下。</p>
<p><strong>3.</strong> 重启 Linux 系统，重启完成后访问：http://192.168.241.129:8080/，即可访问我们的项目，如图：</p>
<p><img src="https://images.gitbook.cn/75bfda60-828c-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p><strong>4.</strong> 将 Tomcat 图标换成自己的，之前申请 QQ 互联的时候有上传网站图标。通过 xftp 将 <code>favicon.ico</code> 图标上传到 ROOT 目录下，如图：</p>
<p><img src="https://images.gitbook.cn/d1c5beb0-828c-11e8-884a-35c5e2ab8361" alt="enter image description here" /></p>
<p>重新访问，图标已更换，如图：</p>
<p><img src="https://images.gitbook.cn/5752e490-828d-11e8-884a-35c5e2ab8361" alt="enter image description here" /></p>
<p><strong>5.</strong> 注意修改你的 QQ 回调地址，在 <code>/home/softs/apache-tomcat-8.0.47/webapps/ROOT/WEB-INF/classes/</code> 目录下：</p>
<pre><code>redirect_URI = http://192.168.241.129:8080/qq_login
</code></pre>
<p>同时你的 QQ 互联网站回调域中也要增加此回调地址。</p>
<p><strong>6.</strong> QQ 登录时出现 <code>Table 'dream_db.Open_User' doesn't exist</code>，这是因为 Linux 下 MySQL 表名默认是区分大小写的，编辑 my.cnf 文件：</p>
<pre><code>vi /etc/my.cnf
</code></pre>
<p>在文件最后加上以下内容，表示表名不区分大小写：</p>
<pre><code>lower_case_table_names = 1 
</code></pre>
<p>然后重新启动 MySQL 服务：</p>
<pre><code>systemctl restart mysqld
</code></pre>
<p><strong>注意：</strong> 如果你的 QQ 第三方登录总是报500错误，可能是浏览器缓存的原因。清除浏览器缓存或者更换浏览器访问！</p>
<p><strong>7.</strong> 激活邮件中的激活地址得修改成你的 IP：</p>
<pre><code>message.setContent( "&lt;a href=\"http://192.168.241.129:8080/activecode?email="+email+"&amp;validateCode="+va....
</code></pre>
<p>重新打包后，将 SendEmail.class 文件替换即可。</p>
<p><strong>注意</strong>： 如果你用的是阿里云服务器，因为25端口被封禁，需使用465端口，添加以下代码：</p>
<pre><code>props.put("mail.smtp.auth", "true"); //这样才能通过验证
props.put("mail.smtp.socketFactory.port", "465");// 设置ssl端口
props.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
</code></pre>
<p><strong>8.</strong> Linux 下的 solr 服务。</p>
<p>将之前本地 Tomcat 的 webapps 目录下的 solr 上传到 Linux 系统 Tomcat 的 webapps 目录下，如图：</p>
<p><img src="https://images.gitbook.cn/7ab57050-82b6-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>然后将之前的 <code>solr_home</code>（我放在了 D 盘根目录下）文件夹上传到 <code>/home/dreamland/</code> 目录下，如图：</p>
<p><img src="https://images.gitbook.cn/dc77fd30-82b6-11e8-9f90-95294e517933" alt="enter image description here" /></p>
<p>然后编辑 <code>/home/softs/apache-tomcat-8.0.47/webapps/solr/WEB-INF/</code> 下的 web.xml：</p>
<pre><code>vi /home/softs/apache-tomcat-8.0.47/webapps/solr/WEB-INF/web.xml 
</code></pre>
<p>将 <code>solr_home</code> 的路径修改为 <code>/home/dreamland/solr_home</code>，如图所示：</p>
<p><img src="https://images.gitbook.cn/a850be10-82b7-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>保存后退出。</p>
<p>最后编辑 applicationContext-solr.xml 文件：</p>
<pre><code>vi /home/softs/apache-tomcat-8.0.47/webapps/ROOT/WEB-INF/classes/applicationContext-solr.xml
</code></pre>
<p>将 mycore 的访问路径修改如下：</p>
<pre><code>&lt;constructor-arg name="builder" value="http://192.168.241.129:8080/solr/mycore"/&gt;
</code></pre>
<p>重新启动 Linux 系统。然后在首页测试 solr 搜索功能，如下图所示：</p>
<p><img src="https://images.gitbook.cn/788fc6a0-82b5-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p><strong>9.</strong> 在 <code>/home/dreamland/</code> 目录下新建 logs 目录，我们将日志存放在这里：</p>
<pre><code>cd /home/dreamland/
mkdir logs
</code></pre>
<p>编辑 log4j.properties 文件：</p>
<pre><code>vi /home/softs/apache-tomcat-8.0.47/webapps/ROOT/WEB-INF/classes/log4j.properties 
</code></pre>
<p>将日志存储位置改为 <code>/home/dreamland/logs/</code> 目录下：</p>
<pre><code>log4j.appender.File.File=/home/dreamland/logs/run.log
</code></pre>
<p>重启 Linux 系统。重启完成后，进入 logs 目录下：</p>
<pre><code>cd /home/dreamland/logs/
</code></pre>
<p>使用以下命令可实时查看日志：</p>
<pre><code>tail -f run.log 
</code></pre>
<p>Ctrl+C 退出当前窗口。</p>
<p>如果 Linux 系统下 Tomcat 日志出现中文乱码，可在 <code>/home/softs/apache-tomcat-8.0.47/bin/</code> 目录下的 catalina.sh 文件中加入以下设置解决：</p>
<pre><code>JAVA_OPTS="$JAVA_OPTS -Djavax.servlet.request.encoding=UTF-8 -Dfile.encoding=UTF-8 -Duser.language=zh_CN -Dsun.jnu.encoding=UTF-8"
</code></pre>
<p><strong>温馨提示：</strong> 在 vi 编辑页面使用 <code>:g/指定内容</code>，可查找指定内容，比如查找 <code>JAVA_OPTS</code>：</p>
<pre><code>:g/JAVA_OPTS 
</code></pre>
<p>按 n 查找下一个，Shift+n 查找上一个。</p>
<blockquote>
  <p>第18课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1Wp6PG4vXO0MDzJQ53RKbkA</p>
  <p>密码：if82</p>
</blockquote></div></article>