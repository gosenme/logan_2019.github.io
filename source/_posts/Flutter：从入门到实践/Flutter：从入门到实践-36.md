---
title: Flutter：从入门到实践-36
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Flutter 开发工具很多，有很多支持 Flutter 开发的 IDE。比如 Android Studio、Visual Studio Code、InteIIiJ IDEA、Atom、Komodo 等。这里我们介绍一下 Android Studio 下的 Flutter 开发环境的搭建。模拟器的话，这里推荐使用 Android 官方的模拟器，也就是 Android Studio SDK 里带的模拟器，或者使用真机。接下来，我们就开始 Flutter 在 Android Studio 下的开发环境的搭建吧。</p>
<p>注意：本文是在 Windows 环境下安装的开发环境。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter SDK 下载与环境变量配置</li>
  <li>Android Studio 的 Flutter 和 Dart 插件安装与新建 Flutter 项目</li>
  <li>模拟器的新建与运行</li>
  <li>运行 Flutter 项目到模拟器和真机</li>
  <li>Flutter 常用命令</li>
  </ul>
</blockquote>
<hr />
<h3 id="fluttersdk">Flutter SDK 下载与环境变量配置</h3>
<p>Flutter 的 SDK 目前官方推荐的是 1.5.4 版本，我们可以在它的官方下载到最新版本的 SDK：</p>
<p><a href="https://flutter.dev/docs/get-started/install">https://flutter.dev/docs/get-started/install</a></p>
<p><img src="https://images.gitbook.cn/33ddaf70-b376-11e9-a454-0beea65aa468" alt="Flutter SDK下载" /></p>
<p>我们可以在官方看到一些要求。</p>
<p>我们可以直接下载 zip sdk 压缩包，或者通过 Git 进行下载。</p>
<p>Flutter SDK 的官方 GitHub 上主要有 dev、beta 和 stable 三个官方分支使，这里正式开发的话可以下载 stable 稳定版本。用 Git 命令进行下载 stable 分支：</p>
<pre><code class="java language-java">git clone -b stable https://github.com/flutter/flutter.git
</code></pre>
<p>下载完 SDK 后我们可以把它解压放到指定文件夹里，接下来就是配置 SDK 环境变量量，这样我们就可以在需要的目录执行相关命令了。如果在官网更新下载 SDK 慢的话，可以设置国内的镜像代理地址，这样下载会快一些。可以将如下的国内下载镜像地址加入到环境变量中：</p>
<pre><code class="java language-java">变量名：PUB_HOSTED_URL，变量值：https://pub.flutter-io.cn
变量名：FLUTTER_STORAGE_BASE_URL，变量值：https://storage.flutter-io.cn
</code></pre>
<p><img src="https://images.gitbook.cn/0b87c3f0-b360-11e9-a454-0beea65aa468" alt="Flutter国内镜像地址配置" /></p>
<p>Flutter SDK 环境变量，将 Flutter 的 bin 目录加入环境变量即可：</p>
<pre><code class="java language-java">[你的Flutter文件夹路径]\flutter\bin
</code></pre>
<p><img src="https://images.gitbook.cn/1c734720-b360-11e9-a454-0beea65aa468" alt="Flutter SDK配置" /></p>
<p>这样我们的 Flutter SDK 的环境变量就配置完毕了。接下来在命令提示符窗口中输入命令：</p>
<pre><code class="java language-java">flutter doctor
</code></pre>
<p>它可以帮助我们检查 Flutter 环境变量是否设置成功，Android SDK 是否下载以及配置好环境变量等等。如果有相关的错误提示，根据提示进行修复和安装、设置即可。每次运行这个命令，都会帮你检查是否缺失了必要的依赖。通过运行 flutter doctor 命令来验证你是否已经正确地设置了，并且可以自动更新和下载相关的依赖。如果全部配置正确的话，会出现如下类似的检测信息：</p>
<p><img src="https://images.gitbook.cn/46aa50b0-b360-11e9-a454-0beea65aa468" alt="Flutter配置检查" /></p>
<p>主要检测信息为：Flutter、Android toolchain、Connected device。</p>
<h3 id="flutterdartflutter">Flutter 和 Dart 插件安装与新建 Flutter 项目</h3>
<p>接下来我们启动 Android Studio，安装 Flutter 和 Dart 插件。</p>
<p><img src="https://images.gitbook.cn/5d40f040-b360-11e9-a454-0beea65aa468" alt="Android Studio" /></p>
<p>我这里使用的是 Android Studio3.3.1 版本，大家也可以使用 3.4 及以上的新版本，都没有影响。</p>
<p>打开 Android Studio -&gt; File -&gt; Settings -&gt; Plugins 搜索：Flutter、Dart 插件，进行安装。</p>
<p><img src="https://images.gitbook.cn/6fdf2c80-b360-11e9-a454-0beea65aa468" alt="Android Studio Flutter、Dart插件" /></p>
<p>安装好插件后，就可以重启 Android Studio 了，我们的基本环境、工具就搭建好了。接下来我们就可以新建 Flutter 项目了。</p>
<p>点击 File -&gt; New -&gt; New Flutter Project 新建项目：</p>
<p><img src="https://images.gitbook.cn/506c52e0-b376-11e9-a454-0beea65aa468" alt="新建Flutter项目" /></p>
<p>弹出窗口选择：Flutter Application，后面的几种类型我们将会在以后给大家讲解。</p>
<p><img src="https://images.gitbook.cn/aa506aa0-b360-11e9-a454-0beea65aa468" alt="新建Flutter项目" /></p>
<p>点击下一步：</p>
<p><img src="https://images.gitbook.cn/b457dc40-b360-11e9-a454-0beea65aa468" alt="新建Flutter项目" /></p>
<p>点击下一步：</p>
<p><img src="https://images.gitbook.cn/c0f450a0-b360-11e9-a454-0beea65aa468" alt="新建Flutter项目" /></p>
<p>设置好所有信息后，点击 Finish 就完成了 Flutter 项目的创建。</p>
<p>项目结构如下图：</p>
<p><img src="https://images.gitbook.cn/777945a0-b376-11e9-a454-0beea65aa468" alt="Flutter项目结构" /></p>
<h2 id="">模拟器的新建与运行</h2>
<p>接下来我们进行模拟器的新建和运行。</p>
<p><img src="https://images.gitbook.cn/837a1640-b376-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>我这里已经创建好了一个，这里建议使用 Android9.0 及以下版本的模拟器，Android Q 目前还不太稳定。</p>
<p>这里直接点击运行创建好的 Android 模拟器即可。</p>
<p><img src="https://images.gitbook.cn/f028d170-b360-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>我们的 Android 原生模拟器是支持置顶的：</p>
<p><img src="https://images.gitbook.cn/fe848200-b360-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>勾选就可以置顶了。</p>
<h3 id="flutter">运行 Flutter 项目到模拟器和真机</h3>
<p>我们在 Android Studio 的顶部可以看到运行按钮，点击运行按钮便可以运行项目到模拟器上了：</p>
<p><img src="https://images.gitbook.cn/0b694a00-b361-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>运行成功示意图：</p>
<p><img src="https://images.gitbook.cn/16a284e0-b361-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>支持项目的热重载（Hot Reload）和热重启（Hot Restart）：</p>
<p><img src="https://images.gitbook.cn/28460d70-b361-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>闪电图标为热重载，它的右侧的图标为热重启。</p>
<p>顶部工具栏也有热重载按钮和停止按钮：</p>
<p><img src="https://images.gitbook.cn/90ec5130-b376-11e9-a454-0beea65aa468" alt="模拟器新建与运行" /></p>
<p>Android Studio 是使用按钮进行相应操作的，非常的方便。</p>
<h3 id="flutter-1">Flutter 常用命令</h3>
<p>真机设备运行调试和模拟器的过程基本一样，手机和电脑通过 USB 连接，手机开启开发人员选项和 USB 调试，最后运行 flutter run 命令即可。</p>
<p>其他常用的命令如下：</p>
<pre><code class="java language-java">flutter build apk;           //打包Android应用
flutter build apk –release;
flutter install;              //安装应用
flutter build ios;            //打包IOS应用
flutter build ios –release;
flutter clean;               //清理重新编译项目
flutter upgrade;            //升级Flutter SDK和依赖包
flutter channel;            //查看Flutter官方分支列表和当前项目使用的Flutter分支
flutter channel &lt;分支名&gt;;   //切换分支
</code></pre>
<h3 id="-1">总结</h3>
<p>本节课主要是给大家讲解 Flutter SDK 的主要版本区分、环境变量配置、Android Studio 开发工具的使用、模拟器运行、新建和运行项目等。为后面的正式高效学习与开发做好准备。主要注意点如下：</p>
<ul>
<li>大家可以使用稳定版或者开发版 Flutter SDK，推荐使用稳定版。</li>
<li>如果遇到下载 SDK 慢或者无法下载情况，请按照课程内设置国内下载镜像地址。</li>
<li>配置好环境变量后，需要用 flutter doctor 检查一下环境。</li>
<li>尝试新建个项目运行到手机或模拟器上，看配置是否有问题。</li>
<li>尝试使用 Android Studio 创建运行一个 Flutter 项目到模拟器和真机。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>