---
title: 案例上手 Spring 全家桶-59
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在学习远程配置中心之前，我们先来学习如何安装 RabbitMQ，因为远程配置中心的动态更新需要结合 RabbitMQ 来使用。</p>
<h3 id="rabbitmq">什么是 RabbitMQ</h3>
<p>RabbitMQ 是消息队列中间件，它适用于分布式系统，功能是完成消息的存储转发，RabbitMQ 底层是用 Erlang 语言来实现的。消息队列（Message Queue ）为不同的 Application 之间完成通信提供了可能，需要传输的消息通过队列来交互，发消息是向队列中写入数据，获取消息是从队列中读取数据。RabbitMQ 是目前主流的中间件产品，适用于多个行业，具有高可用、易于扩展、安全可靠等优点。</p>
<h3 id="macrabbitmqhomebrew">Mac 下安装 RabbitMQ：安装 Homebrew</h3>
<h4 id="homebrewhomebrew">Homebrew 简介（摘自 Homebrew 官网）</h4>
<blockquote>
  <p>Homebrew 是一个包管理器，用于安装 Apple 没有预装但是你需要的工具。</p>
</blockquote>
<p>Homebrew 会将软件包安装到独立目录 /usr/local/Cellar，并将其文件软链接至 /usr/local。</p>
<p>Homebrew 不会将文件安装到它本身目录之外，所以你可将 Homebrew 安装到任意位置。</p>
<h4 id="homebrew">安装 Homebrew</h4>
<p>打开终端，执行如下命令即可，官网提供的安装包已经包含了 Erlang，所以无需单独安装 Erlang。</p>
<pre><code class="shell language-shell">/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
</code></pre>
<p>在终端执行 brew 命令，如果安装成功，会返回如下信息。</p>
<p><img src="https://images.gitbook.cn/882a7f60-d79b-11e9-8797-4924c0d7c082" width = "70%" /></p>
<h4 id="homebrew-1">卸载 Homebrew</h4>
<p>打开终端，执行如下命令即可。</p>
<pre><code class="shell language-shell">/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
</code></pre>
<h3 id="homebrewrabbitmq">通过 Homebrew 来安装 RabbitMQ</h3>
<p>打开终端，执行如下命令即可。</p>
<pre><code class="shell language-shell">//更新 brew 资源
brew update
//执行安装
brew install rabbitmq
</code></pre>
<p>安装过程如下图所示。</p>
<p><img src="https://images.gitbook.cn/10fcbe20-d79c-11e9-8797-4924c0d7c082" width = "75%" /></p>
<p>看到如下信息则表示 RabbitMQ 已安装成功。</p>
<p><img src="https://images.gitbook.cn/17a6fb00-d79c-11e9-a536-c512dee3d564" width = "75%" /></p>
<p>安装完成之后，需要配置环境变量，在终端执行 <code>vim .bash_profile</code>，将下面两行配置添加到 .bash_profile 中，注意 RABBIT_HOME 替换成你自己的安装路径和版本，我安装的版本是 3.7.10。</p>
<pre><code>export RABBIT_HOME=/usr/local/Cellar/rabbitmq/3.7.10
export PATH=$PATH:$RABBIT_HOME/sbin
</code></pre>
<p>编辑完成之后输入 <code>:wq</code> 保存退出，并执行如下命令使环境变量生效。</p>
<pre><code>source ~/.bash_profile
</code></pre>
<p>环境变量配置完成之后就可以启动 RabbitMQ 了，执行如下命令。</p>
<pre><code>//进入安装路径下的 sbin 目录
cd /usr/local/Cellar/rabbitmq/3.7.10/sbin
//启动服务
sudo rabbitmq-server
</code></pre>
<p>输入 Mac 系统密码，如下图所示。</p>
<p><img src="https://images.gitbook.cn/270c0540-d79c-11e9-a536-c512dee3d564" width = "70%" /></p>
<p>RabbitMQ 启动成功会看到如下所示信息。</p>
<p><img src="https://images.gitbook.cn/2d05b6d0-d79c-11e9-8797-4924c0d7c082" width = "70%" /></p>
<p>打开浏览器在地址栏输入 http://localhost:15672/，进入登录页面。</p>
<p><img src="https://images.gitbook.cn/36a1e380-d79c-11e9-ad2d-e1c058c00235" alt="5" /></p>
<p>输入用户名密码，均为 guest，即可进入主页面。</p>
<p><img src="https://images.gitbook.cn/3d11af70-d79c-11e9-ad2d-e1c058c00235" alt="6" /></p>
<p>Mac 下 RabbitMQ 安装成功。</p>
<p>在终端输入 control+c 即可关闭 RabbitMQ，如下图所示。</p>
<p><img src="https://images.gitbook.cn/4379da40-d79c-11e9-a536-c512dee3d564" width = "70%" /></p>
<h3 id="windowsrabbitmq">Windows 下安装 RabbitMQ</h3>
<p>1. 安装 Erlang，RabbitMQ 服务端代码是用 Erlang 编写的，所以安装 RabbitMQ 必须先安装 Erlang。</p>
<p><a href="http://www.erlang.org/downloads">进入官网</a>，下载 exe 安装包，双击运行完成安装。</p>
<p>2. 配置环境变量，与 Java 环境配置方式一致。</p>
<p>高级系统设置 → 环境变量 → 新建系统环境变量，变量名 ERLANG_HOME，变量值为 Erlang 的安装路径 D:\Program Files\erl9.2，注意这里替换成你自己的安装路径。</p>
<p>将 <code>;%ERLANG_HOME%\bin</code> 加入到 path 中。</p>
<p>3. 安装 RabbitMQ</p>
<p><a href="http://www.rabbitmq.com/install-windows.html">进入官网</a>，下载 exe 安装包，双击运行完成安装。</p>
<p>配置环境变量，与 Java 环境配置方式一致，高级系统设置 → 环境变量 → 新建系统环境变量，变量名 RABBITMQ_SERVER，变量值为 RabbitMQ 的安装路径 D:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.10，注意这里替换成你自己的安装路径。</p>
<p>将 <code>;%RABBITMQ_SERVER%\sbin</code> 加入到 path 中。</p>
<p>安装完成后，打开计算机服务列表，可以看到 RabbitMQ 的服务，如下图所示。</p>
<p><img src="https://images.gitbook.cn/a84ab890-d79c-11e9-ad2d-e1c058c00235" width = "75%" /></p>
<p>4. 安装 RabbitMQ 管理插件</p>
<p>进入安装路径下的 sbin 目录，如下所示。</p>
<pre><code>cd D:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.10\sbin&gt;
</code></pre>
<p>执行如下命令，安装管理插件。</p>
<pre><code>rabbitmq-plugins enable rabbitmq_management
</code></pre>
<p>打开浏览器在地址栏输入 http://localhost:15672/，进入登录页面。</p>
<p><img src="https://images.gitbook.cn/b4c6fac0-d79c-11e9-8797-4924c0d7c082" alt="5" /></p>
<p>输入用户名密码，均为 guest，即可进入主页面。</p>
<p><img src="https://images.gitbook.cn/bb6e9f90-d79c-11e9-8fae-816b29059b0c" alt="6" /></p>
<p>Windows 下 RabbitMQ 安装成功。</p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了在 Mac 以及 Windows 环境下安装 RabbitMQ 的具体步骤，RabbitMQ 在分布式系统中使用较为广泛，通过它完成消息的存储转发，为不同的 Application 之间完成通信提供了可能。</p></div></article>