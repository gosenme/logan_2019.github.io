---
title: Flutter：从入门到实践-35
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Dart 除了可以使用 Flutter 进行移动应用开发外，还可以进行 Web 开发，Dart 主要是替换了 JavaScript，用 Dart 来做 JavaScript 这部分工作，也可以说 Dart 替代了 JavaScript 和 JQuery 框架。我们用 Dart 来写 Web 后，编译器会自动将 Dart 文件编译为 JavaScript 文件进行运行，只不过我们写的语法规范是 Dart 语法。Dart 文件转 JavaScript 文件可以使用 dart2js 来转换。接下来，我们就开始 Dart Web 开发的准备工作吧。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Dart Web 开发环境配置</li>
  <li>Dart Web 开发工具安装</li>
  <li>Dart Web 开发的两种创建 Web 项目的方式</li>
  <li>运行 Dart Web 项目</li>
  </ul>
</blockquote>
<hr />
<h3 id="">开发环境的搭建</h3>
<p>Dart Web 官方配置英文文档地址：
<a href="https://webdev.dartlang.org/guides/get-started">https://webdev.dartlang.org/guides/get-started</a></p>
<p>我们也可以使用 DartPad 体验和运行 Dart 程序：
<a href="https://dartpad.dartlang.org/">https://dartpad.dartlang.org/</a></p>
<p><img src="https://images.gitbook.cn/aee768d0-ae87-11e9-8433-cbc6088d6c11" alt="DartPad界面" /></p>
<h3 id="1dartsdk">1. 下载 Dart SDK</h3>
<p>本文是在 Windows 环境下进行安装配置的。</p>
<p>Windows 下需要先安装 Chocolatey：
<a href="https://chocolatey.org/">https://chocolatey.org/</a></p>
<p>使用 CMD 命令安装：</p>
<pre><code class="java language-java">@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" &amp;&amp; SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
</code></pre>
<p>新建一个 chocolatey.bat 文件，将上面的这段命令复制进去保存。双击运行这个 bat 文件就会自动执行安装 chocolatey 包管理器操作了。</p>
<p>安装好之后，Windows 命令窗口执行如下命令：</p>
<pre><code class="java language-java">C:\&gt; choco install dart-sdk
</code></pre>
<p><img src="https://images.gitbook.cn/dd527f20-ae87-11e9-8433-cbc6088d6c11" alt="Dart-SDK安装" /></p>
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
<p>当然除了用命令安装 Dart SDK 外，我们也可以安装 Windows 版本安装包文件，下载地址：
<a href="http://www.gekorm.com/dart-windows/">http://www.gekorm.com/dart-windows/</a></p>
<p><img src="https://images.gitbook.cn/f67e6f90-ae87-11e9-8433-cbc6088d6c11" alt="Dart Web SDK安装包" /></p>
<p>在 Dart Web SDK 里包含以下工具：</p>
<p><img src="https://images.gitbook.cn/03e8e250-ae88-11e9-8433-cbc6088d6c11" alt="Dart Web SDK里包含的工具" /></p>
<p>其实主要的命令工具就是 webdev，用来构建和部署 Dart Web 程序。dart2js，将 dart 文件转为 js 文件的编译工具。dartdevc，一个模块化的 dart 转 js 文件的编译工具。</p>
<p><img src="https://images.gitbook.cn/322dabf0-ae88-11e9-8433-cbc6088d6c11" alt="Dart Web SDK里包含的工具" /></p>
<p>Chocolatey 执行命令安装完 dart-sdk 后，将 Dart SDK 的 bin 目录加入环境变量：</p>
<p><img src="https://images.gitbook.cn/448912d0-ae88-11e9-8433-cbc6088d6c11" alt="配置Dart环境变量" /></p>
<p>测试我们的 Dart SDK 环境变量是否配置好，输入如下命令：</p>
<pre><code class="java language-java">dart --version
</code></pre>
<p>如能够正确输出版本号，则 dart 环境变量配置成功。</p>
<p><img src="https://images.gitbook.cn/54712fc0-ae88-11e9-8433-cbc6088d6c11" alt="测试Dart环境变量是否配置成功" /></p>
<h3 id="2">2. 下载开发工具</h3>
<p>开发工具官方推荐是 WebStorm，当然也可以使用 Visual Studio Code，也可以使用命令工具创建、运行项目。如果想支持命令行运行项目，这样快速方便些。可以安装 webdev 和 stagehand（这里需要安装执行下面这两个命令）：</p>
<pre><code class="java language-java">&gt; pub global activate webdev
&gt; pub global activate stagehand
</code></pre>
<p>安装命令窗口：</p>
<p><img src="https://images.gitbook.cn/7a65fbc0-ae88-11e9-8433-cbc6088d6c11" alt="安装webdev和stagehand" /></p>
<p>注意：如果你想运行使用 Dart2 以下的版本，WebStorm 版本至少要 2018.1.3 及以上。当然，现在基本都用 Dart2 及新版本开发了。</p>
<p>接下来下载安装 WebStorm。</p>
<p>WebStorm 官方下载地址：
<a href="https://www.jetbrains.com/webstorm/">https://www.jetbrains.com/webstorm/</a></p>
<p><img src="https://images.gitbook.cn/b9763d70-ae88-11e9-8433-cbc6088d6c11" alt="WebStorm安装界面" /></p>
<h3 id="3dartweb">3. 创建 Dart Web 项目</h3>
<p>使用命令行创建。</p>
<pre><code class="java language-java">&gt; mkdir quickstart
&gt; cd quickstart
&gt; stagehand web-simple
&gt; pub get
</code></pre>
<p>使用 WebStorm 创建。</p>
<p>新建项目：</p>
<p><img src="https://images.gitbook.cn/f07649a0-ae88-11e9-8433-cbc6088d6c11" alt="WebStorm新建项目" /></p>
<p>选择 Dart 项目，点击 CREATE：</p>
<p><img src="https://images.gitbook.cn/026c10e0-ae89-11e9-8433-cbc6088d6c11" alt="WebStorm新建项目" /></p>
<p>项目结构目录如下图：</p>
<p><img src="https://images.gitbook.cn/0e1831d0-ae89-11e9-8433-cbc6088d6c11" alt="项目结构目录" /></p>
<p>运行项目：</p>
<p><img src="https://images.gitbook.cn/198e2790-ae89-11e9-8433-cbc6088d6c11" alt="运行项目" /></p>
<p>运行后，可以看到控制台显示的日志，如果看到类似的Dart Server启动成功就可以访问我们的页面了：</p>
<p><img src="https://images.gitbook.cn/FlLIp2JCtHb7_QAiePSpY_eW_kL8" alt="运行项目" /></p>
<p>页面效果截图：</p>
<p><img src="https://images.gitbook.cn/250b9760-ae89-11e9-8433-cbc6088d6c11" alt="运行效果" /></p>
<p>可以看出，这里我们的 dart 文件就是充当操作 HTML 的 Dom 树的功能，也就是替代了 JS 的原始用法，不过最终运行时也是将 dart 文件编译为 js 文件运行，只不过 dart 语法比 JS 的使用更加方便与强大。</p>
<pre><code class="dart language-dart">import 'dart:html';

void main() {
  querySelector('#output').text = 'Your Dart app is running.';
}
</code></pre>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;

&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="utf-8"&gt;
    &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;meta name="scaffolded-by" content="https://github.com/google/stagehand"&gt;
    &lt;title&gt;untitled&lt;/title&gt;
    &lt;link rel="stylesheet" href="styles.css"&gt;
    &lt;link rel="icon" href="favicon.ico"&gt;
    &lt;script defer src="main.dart.js"&gt;&lt;/script&gt;
&lt;/head&gt;

&lt;body&gt;

  &lt;div id="output"&gt;&lt;/div&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>再重复下，我们可以用 Visual Studio Code 进行开发，也可以使用命令创建和运行项目。</p>
<p>使用命令行创建：</p>
<pre><code class="java language-java">&gt; mkdir quickstart
&gt; cd quickstart
&gt; stagehand web-simple
&gt; pub get
</code></pre>
<p>命令行运行项目：</p>
<pre><code class="java language-java">webdev serve
</code></pre>
<p>如果想将 dart 文件编译转为 js 文件，使用 Dart SDK 自带的 dart2js 这个工具。
基本用法：</p>
<pre><code class="java language-java">dart2js -O2 -o test.js test.dart
</code></pre>
<p>test.js 为输出的 js 文件的路径+文件名；test.dart 为输入的要转换的 dart 文件的路径+文件名。</p>
<p>更多参数和复杂用法命令，请看官方：
<a href="https://webdev.dartlang.org/tools/dart2js">https://webdev.dartlang.org/tools/dart2js</a></p>
<p>关于 Dart Web 开发环境搭建及新建运行项目就讲解这么多。</p>
<h3 id="-1">总结</h3>
<p>本节课主要是给大家延伸讲解了用 Dart2 开发 Web 项目的基本用法。
希望大家掌握 Dart2 的 API 调用方式和使用步骤，尝试用 Dart2 来编写一个简单的 Web 登录页面。</p></div></article>