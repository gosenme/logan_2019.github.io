---
title: Flutter：从入门到实践-37
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Dart 除了可以使用 Flutter 进行移动应用开发、Web 开发外，还可以进行服务器端开发，也就是后端开发。如建立后端服务、编写接口、查询数据库、任务调度等等后端、服务器端的工作它都可以实现。接下来，我们就开始 Dart Server 开发的准备工作吧。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Dart Server 开发环境配置</li>
  <li>Dart Server 开发工具安装</li>
  <li>Dart Server 开发的两种创建 Server 项目的方式</li>
  <li>运行 Dart Server 项目</li>
  </ul>
</blockquote>
<h4 id="1">1 开发环境的搭建</h4>
<p>Dart Server 官方配置英文文档地址：
<a href="https://www.dartlang.org/tutorials/server/get-started">https://www.dartlang.org/tutorials/server/get-started</a></p>
<p>我们也可以使用 DartPad 体验和运行 Dart 程序：
<a href="https://dartpad.dartlang.org/">https://dartpad.dartlang.org/</a></p>
<p><img src="https://images.gitbook.cn/d37681c0-b352-11e9-a454-0beea65aa468" alt="DartPad界面" /></p>
<h4 id="11dartsdk">1.1 下载 Dart SDK</h4>
<p>官方英文文档地址：
<a href="https://www.dartlang.org/tools/sdk#install">https://www.dartlang.org/tools/sdk#install</a></p>
<p>本文是在 Windows 环境下进行安装配置的。</p>
<p>Windows 下需要先安装 Chocolatey：<a href="https://chocolatey.org/">https://chocolatey.org/</a></p>
<p>使用 CMD 命令安装：</p>
<pre><code class="java language-java">@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" &amp;&amp; SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
</code></pre>
<p>新建一个 chocolatey.bat 文件，将上面的这段命令复制进去保存。双击运行这个 bat 文件就会自动执行安装 Chocolatey 包管理器操作了。
安装好之后，Windows 命令窗口执行如下命令进行 dart-sdk 稳定版安装：</p>
<pre><code class="java language-java">C:\&gt; choco install dart-sdk
</code></pre>
<p><img src="https://images.gitbook.cn/38cd3c70-b354-11e9-a454-0beea65aa468" alt="Dart-SDK安装" /></p>
<p>如果想安装 dev 版，输入以下命令：</p>
<pre><code class="java language-java">choco install dart-sdk --pre
</code></pre>
<p>如果想更新 dart-sdk，输入以下命令：</p>
<pre><code class="java language-java">choco upgrade dart-sdk
</code></pre>
<p>Linux 需要执行以下命令：</p>
<pre><code class="java language-java">&gt; sudo apt-get update
&gt; sudo apt-get install apt-transport-https
&gt; sudo sh -c 'curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'
&gt; sudo sh -c 'curl https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list &gt; /etc/apt/sources.list.d/dart_stable.list'
</code></pre>
<pre><code class="java language-java">&gt; sudo apt-get update
&gt; sudo apt-get install dart
</code></pre>
<p>Mac 下需要执行以下命令：</p>
<pre><code class="java language-java"> &gt; brew tap dart-lang/dart
 &gt; brew install dart
</code></pre>
<p>当然除了用命令安装 Dart SDK 外，我们也可以安装 Windows 版本安装包文件，下载地址：</p>
<p><a href="http://www.gekorm.com/dart-windows/">http://www.gekorm.com/dart-windows/</a></p>
<p><img src="https://images.gitbook.cn/50ce8f90-b354-11e9-a454-0beea65aa468" alt="Dart Web SDK安装包" /></p>
<p>在 Dart Web SDK 里包含以下工具：</p>
<p><img src="https://images.gitbook.cn/5e065990-b354-11e9-a454-0beea65aa468" alt="Dart Web SDK里包含的工具" /></p>
<p>其实主要的命令工具就是：WebDev，用来构建和部署 Dart Web 程序；dart2js，将 dart 文件转为 js 文件的编译工具；dartdevc，一个模块化的 dart 转 js 文件的编译工具。</p>
<p><img src="https://images.gitbook.cn/6ae75100-b354-11e9-a454-0beea65aa468" alt="Dart Web SDK里包含的工具" /></p>
<p>Chocolatey 执行命令安装完 dart-sdk 后，将 Dart SDK 的 bin 目录加入环境变量：</p>
<p><img src="https://images.gitbook.cn/779c2f60-b354-11e9-a454-0beea65aa468" alt="配置Dart环境变量" /></p>
<p>测试我们的 Dart SDK 环境变量是否配置好，输入如下命令：</p>
<pre><code class="java language-java">dart --version
</code></pre>
<p>如能够正确输出版本号，则 Dart 环境变量配置成功。</p>
<p><img src="https://images.gitbook.cn/836dd9b0-b354-11e9-a454-0beea65aa468" alt="测试Dart环境变量是否配置成功" /></p>
<h4 id="12">1.2 下载开发工具</h4>
<p>官方英文使用文档地址：
<a href="https://webdev.dartlang.org/tools/webstorm">https://webdev.dartlang.org/tools/webstorm</a></p>
<p>开发工具官方推荐是 WebStorm，当然也可以使用 Visual Studio Code，也可以使用命令工具创建、运行项目。如果想支持命令行运行项目，这样快速方便些。可以安装 WebDev 和 stagehand（这里需要安装执行下面这两个命令）：</p>
<pre><code class="java language-java">&gt; pub global activate webdev
&gt; pub global activate stagehand
</code></pre>
<p>安装命令窗口：</p>
<p><img src="https://images.gitbook.cn/a2acf720-b354-11e9-a454-0beea65aa468" alt="安装webdev和stagehand" /></p>
<p>注意：如果你想运行使用 Dart2 以下的版本，WebStorm 版本至少要 2018.1.3 及以上。当然，现在基本都用 Dart2 及新版本开发了。</p>
<p>接下来下载安装 WebStorm。</p>
<p>WebStorm 官方下载地址：
<a href="https://www.jetbrains.com/webstorm/">https://www.jetbrains.com/webstorm/</a></p>
<p><img src="https://images.gitbook.cn/ac377090-b354-11e9-a454-0beea65aa468" alt="WebStorm安装界面" /></p>
<h3 id="2dartserver">2 创建 Dart Server 项目</h3>
<p>最简单的 Dart 应用程序包括如下部分：</p>
<p>一个以 .dart 后缀结尾的 dart 源文件；
一个最顶层的 main() 方法入口函数。</p>
<p>运行这个 dart 文件，我们可以使用命令：</p>
<pre><code class="java language-java">dart main.dart
</code></pre>
<p>Dart 官方 Server 项目结构图如下图：</p>
<p><img src="https://images.gitbook.cn/f31f2480-b354-11e9-a454-0beea65aa468" alt="Server项目结构图" /></p>
<p>bin 目录：主要放置命令行式应用的dart文件，其中的一个dart文件必须有 main() 入口函数。</p>
<p>lib 目录：应用额外使用的代码或者库文件。</p>
<p>pubspec.yaml：应用的配置和描述信息文件，和 Flutter 的 pubspec.yaml 功能一致。</p>
<p>命令行应用程序（Command-line apps）：</p>
<p>Dart 命令行应用程序从命令行独立运行。 命令行应用程序通常用于为Web 应用程序提供服务器端支持，但它们也可以是脚本。</p>
<p>Dart VM 直接运行 Dart 代码而无需中间编译。</p>
<p><img src="https://images.gitbook.cn/fe3d5d50-b354-11e9-a454-0beea65aa468" alt="命令行应用程序" /></p>
<p>使用 WebStorm 创建命令行应用程序：</p>
<p><img src="https://images.gitbook.cn/06fb5f00-b355-11e9-a454-0beea65aa468" alt="WebStorm新建命令行项目" /></p>
<p>项目结构目录如下图：</p>
<p><img src="https://images.gitbook.cn/0f70e600-b355-11e9-a454-0beea65aa468" alt="项目结构目录" /></p>
<p>.dart_tool 目录：主要是 pub 使用的相关支持文件、Dart 工具相关，我们可以不管它。</p>
<p>bin 目录：应用程序入口，一般叫 main.dart 文件，里面有 main() 入口函数。</p>
<p>pubspec.lock：生成的文件，指定应用程序所依赖的软件包的版本号。</p>
<p>lib 目录：存放命令行程序的其他类、源文件，具体业务逻辑dart文件写在这里。</p>
<p>.packages 文件：告诉 Dart 工具在哪里获取应用程序使用的包。该文件由 pub get 命令创建。你可以忽略这一点。</p>
<p>运行命令行应用程序：</p>
<p><img src="https://images.gitbook.cn/1b8f9ee0-b355-11e9-a454-0beea65aa468" alt="运行项目" /></p>
<p>当然我们也可以使用命令运行：</p>
<pre><code class="java language-java">pub run bin/main.dart
</code></pre>
<p>运行效果图片：</p>
<p><img src="https://images.gitbook.cn/27db3420-b355-11e9-a454-0beea65aa468" alt="运行项目" /></p>
<p>关于 main() 入口函数和其他顶层入口函数：
Dart 允许您定义顶级函数，即未封装在类或对象中的函数。 所有应用程序至少有一个顶级函数，即 main() 函数。</p>
<p>函数声明包含两部分：签名和正文（a signature and a body）。</p>
<p><img src="https://images.gitbook.cn/5315f210-b355-11e9-a454-0beea65aa468" alt="函数组成" /></p>
<p>签名设置函数名称，返回值的数据类型以及输入参数的数量和类型。</p>
<p><img src="https://images.gitbook.cn/321eeb70-b355-11e9-a454-0beea65aa468" alt="函数组成" /></p>
<p>方法逻辑代码写在花括号 <code>{...}</code> 之间。如果正文是单个表达式，那么可以跳过大括号并使用 <code>=&gt;</code> 简写：</p>
<pre><code class="dart language-dart">double milesToKM(double miles) =&gt; miles / 0.62;
</code></pre>
<p>关于文件命名：一般都是小写，单词间用下划线 <code>_</code> 分隔。</p>
<p>以上是简单的命令行应用程序（Command-line apps）创建过程。</p>
<p>官方详细的命令行应用程序（Command-line apps）编写英文文档地址：</p>
<p><a href="https://www.dartlang.org/tutorials/server/cmdline">https://www.dartlang.org/tutorials/server/cmdline</a> </p>
<p>后续将给大家详细讲解。</p>
<p>示例代码：</p>
<p>main.dart</p>
<pre><code class="dart language-dart">import 'package:untitled2/untitled2.dart' as untitled2;

main(List&lt;String&gt; arguments) {
  print('Hello world: ${untitled2.calculate()}!');
}
</code></pre>
<p>untitled2.dart</p>
<pre><code class="dart language-dart">int calculate() {
  return 6 * 7;
}
</code></pre>
<p>接下来看下 Http Server 后端应用（HTTP Clients &amp; Servers）的创建方法。</p>
<p>使用 WebStorm 创建。</p>
<p>新建项目：</p>
<p><img src="https://images.gitbook.cn/6b658c40-b355-11e9-a454-0beea65aa468" alt="WebStorm新建项目" /></p>
<p>选择 Dart 项目，点击 CREATE：</p>
<p><img src="https://images.gitbook.cn/7562ebc0-b355-11e9-a454-0beea65aa468" alt="WebStorm新建项目" /></p>
<p>或者创建 Dart Web 项目，再新建个 bin 目录也可以：</p>
<p><img src="https://images.gitbook.cn/7f2edb00-b355-11e9-a454-0beea65aa468" alt="WebStorm新建项目" /></p>
<p>项目结构目录如下图：</p>
<p><img src="https://images.gitbook.cn/88badb10-b355-11e9-a454-0beea65aa468" alt="项目结构目录" /></p>
<p>运行项目：</p>
<p><img src="https://images.gitbook.cn/92e42c90-b355-11e9-a454-0beea65aa468" alt="运行项目" /></p>
<p>运行后，可以看到控制台显示的日志，如果看到类似的 Dart Server 启动成功就可以访问我们的页面了：</p>
<p><img src="https://images.gitbook.cn/9d8d8380-b355-11e9-a454-0beea65aa468" alt="运行项目" /></p>
<p>页面效果截图：</p>
<p><img src="https://images.gitbook.cn/af821240-b355-11e9-a454-0beea65aa468" alt="运行效果" /></p>
<p>页面信息监控：</p>
<p><a href="http://127.0.0.1:54212/#/vm">http://127.0.0.1:54212/#/vm</a></p>
<p><img src="https://images.gitbook.cn/bbcee000-b355-11e9-a454-0beea65aa468" alt="页面信息监控" /></p>
<p>官方的 Http Server 后端应用（HTTP Clients &amp; Servers）编写英文文档地址：</p>
<p><a href="https://www.dartlang.org/tutorials/server/httpserver">https://www.dartlang.org/tutorials/server/httpserver</a></p>
<p>示例代码：</p>
<pre><code class="dart language-dart">import 'dart:io';

import 'package:args/args.dart';
import 'package:shelf/shelf.dart' as shelf;
import 'package:shelf/shelf_io.dart' as io;

main(List&lt;String&gt; args) async {
  var parser = ArgParser()..addOption('port', abbr: 'p', defaultsTo: '8080');

  var result = parser.parse(args);

  var port = int.tryParse(result['port']);

  if (port == null) {
    stdout.writeln(
        'Could not parse port value "${result['port']}" into a number.');
    // 64: command line usage error
    exitCode = 64;
    return;
  }

  var handler = const shelf.Pipeline()
      .addMiddleware(shelf.logRequests())
      .addHandler(_echoRequest);

  var server = await io.serve(handler, 'localhost', port);
  print('Serving at http://${server.address.host}:${server.port}');
}

shelf.Response _echoRequest(shelf.Request request) =&gt;
    shelf.Response.ok('Request for "${request.url}"');
</code></pre>
<h3 id="">总结</h3>
<p>本节课主要是给大家延伸讲解了用 Dart2 开发后端 Server 项目的基本用法。</p>
<ul>
<li>重点掌握 Dart2 开发运行 Web 服务器后端的整个流程。</li>
<li>与 Java 和其他后端语言，对比进行学习。尝试用 Dart2 写一个接口服务器，分别写一个 GET 和 POST 请求的接口。</li>
</ul></div></article>