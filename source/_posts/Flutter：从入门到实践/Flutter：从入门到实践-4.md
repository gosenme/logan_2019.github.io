---
title: Flutter：从入门到实践-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Flutter 开发工具很多，有很多支持 Flutter 开发的 IDE，比如 Android Studio、Visual Studio Code、InteIIiJ IDEA、Atom、Komodo 等。本课将使用 Visual Studio Code 作为主要开发工具，因为 Visual Studio Code 占用内存和 CPU 比较低，非常流畅，体验也比较好。模拟器的话，这里推荐使用 Android 官方的模拟器，也就是 Android Studio SDK 里带的模拟器。不过，这里的模拟器我们可以单独启动，无需从 Android Studio 启动，当然也可以用真机运行调试。</p>
<p>接下来，我们就开始 Flutter 开发环境的搭建吧。</p>
<p>注意：本文是在 Windows 环境下安装的开发环境。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 下载与环境变量配置</li>
  <li>Visual Studio Code 插件安装与新建 Flutter 项目</li>
  <li>模拟器的安装</li>
  <li>运行 Flutter 项目到模拟器和真机</li>
  <li>Flutter 常用命令</li>
  </ul>
</blockquote>
<h3 id="1fluttersdk">1 下载 Flutter SDK</h3>
<p>Flutter SDK 由两部分构成，一个是 Dart SDK，另一个就是 Flutter SDK，因为 Flutter 是基于 Dart 的。可以通过两种方式下载：一种是 Git 下载；另一种是直接下载 SDK 压缩包。</p>
<p>Git 方式我们可以通过拉取官方 Github 上的 flutter 分支来下载。分支分类如下图：</p>
<p><img src="https://images.gitbook.cn/FieTyQvEAedAb4aAYW0e1U5CaZHI" alt="avatar" /></p>
<p>可以看到主要有 dev、beta 和 stable 三个官方分支，这里正式开发的话可以下载 stable 稳定版本。用 Git 命令进行下载 stable 分支：</p>
<pre><code class="java language-java">git clone -b stable https://github.com/flutter/flutter.git
</code></pre>
<p>另一种是直接官网下载 SDK 压缩包，官方下载地址为：</p>
<pre><code class="java language-java">https://storage.googleapis.com/flutter_infra/releases/stable/windows/flutter_windows_v1.0.0-stable.zip
</code></pre>
<h3 id="2">2 配置环境变量</h3>
<p>下载完 SDK 后我们可以把它解压放到指定文件夹里，接下来就是配置 SDK 环境变量，这样我们就可以在需要的目录执行相关命令了。如果在官网更新下载 SDK 慢的话，可以设置国内的镜像代理地址，这样下载会快一些。可以将如下的国内下载镜像地址加入到环境变量中：</p>
<pre><code class="java language-java">变量名：PUB_HOSTED_URL，变量值：https://pub.flutter-io.cn
变量名：FLUTTER_STORAGE_BASE_URL，变量值：https://storage.flutter-io.cn
</code></pre>
<p><img src="https://images.gitbook.cn/FolXxAP6YPmKgMdDhB_XUJgSoWCz" alt="avatar" /></p>
<p>Flutter SDK 环境变量，将 Flutter 的 bin 目录加入环境变量即可：</p>
<pre><code class="java language-java">[你的Flutter文件夹路径]\flutter\bin
</code></pre>
<p><img src="https://images.gitbook.cn/FhpzeQ548HlEkN6EYE5sLKbVYZ5h" alt="avatar" /></p>
<p>这样我们的 Flutter SDK 的环境变量就配置完毕了。</p>
<p>接下来在命令提示符窗口中输入命令：</p>
<pre><code class="java language-java">flutter doctor
</code></pre>
<p>它可以帮助我们检查 Flutter 环境变量是否设置成功、Android SDK 是否下载以及是否配置好环境变量等等。如果有相关的错误提示，根据提示进行修复和安装、设置即可。每次运行这个命令，都会帮你检查是否缺失了必要的依赖。通过运行 flutter doctor 命令来验证你是否已经正确地设置了，并且可以自动更新和下载相关的依赖。如果全部配置正确的话，会出现如下类似的检测信息：</p>
<p><img src="https://images.gitbook.cn/FoklAH4JlI-9qSN6hJRjrE_TzKwU" alt="avatar" /></p>
<p>主要检测信息为：Flutter、Android toolchain、Connected device。 </p>
<h3 id="3visualstudiocode">3 安装 Visual Studio Code 所需插件</h3>
<p>在 Visual Studio Code 的 Extensions 里搜索安装 Dart 和 Flutter 扩展插件：</p>
<p><img src="https://images.gitbook.cn/FiP_R4Xm9AnhMFXVsfBuSDVh3I2O" alt="avatar" /></p>
<p>安装完成插件后，重启 Visual Studio Code 编辑器即可。</p>
<h3 id="4flutter">4 创建 Flutter 项目</h3>
<p>接下来进行 Flutter 项目的新建。</p>
<p>我们可以通过命令面板或者快捷键 Ctrl+Shif+P 打开命令面板，找到 Flutter：New Project。</p>
<p><img src="https://images.gitbook.cn/FrnjfJ8jWlaVG7ZC7s0OMdSeZP7l" alt="avatar" /></p>
<p>点击 New Project，接下来输入项目名称：</p>
<p><img src="https://images.gitbook.cn/FoBsQyDuFIUuuzVjNjIm9WLWuT7b" alt="avatar" /></p>
<p>回车，然后选择好项目的存储位置即可。这样就完成了 Flutter 项目的新建。</p>
<p>整个的创建流程日志如下：</p>
<pre><code class="java language-java">[undefined] flutter create .
Waiting for another flutter command to release the startup lock...
Creating project ....
  .gitignore (created)
  .idea\libraries\Dart_SDK.xml (created)
  .idea\libraries\Flutter_for_Android.xml (created)
  .idea\libraries\KotlinJavaRuntime.xml (created)
  .idea\modules.xml (created)
  .idea\runConfigurations\main_dart.xml (created)
  .idea\workspace.xml (created)
  .metadata (created)
  android\app\build.gradle (created)
  android\app\src\main\java\com\example\fluttersamples\MainActivity.java (created)
  android\build.gradle (created)
  android\flutter_samples_android.iml (created)
  android\app\src\main\AndroidManifest.xml (created)
  android\app\src\main\res\drawable\launch_background.xml (created)
  android\app\src\main\res\mipmap-hdpi\ic_launcher.png (created)
  android\app\src\main\res\mipmap-mdpi\ic_launcher.png (created)
  android\app\src\main\res\mipmap-xhdpi\ic_launcher.png (created)
  android\app\src\main\res\mipmap-xxhdpi\ic_launcher.png (created)
  android\app\src\main\res\mipmap-xxxhdpi\ic_launcher.png (created)
  android\app\src\main\res\values\styles.xml (created)
  android\gradle\wrapper\gradle-wrapper.properties (created)
  android\gradle.properties (created)
  android\settings.gradle (created)
  ios\Runner\AppDelegate.h (created)
  ios\Runner\AppDelegate.m (created)
  ios\Runner\main.m (created)
  ios\Runner.xcodeproj\project.pbxproj (created)
  ios\Runner.xcodeproj\xcshareddata\xcschemes\Runner.xcscheme (created)
  ios\Flutter\AppFrameworkInfo.plist (created)
  ios\Flutter\Debug.xcconfig (created)
  ios\Flutter\Release.xcconfig (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Contents.json (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-1024x1024@1x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-20x20@1x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-20x20@2x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-20x20@3x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-29x29@1x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-29x29@2x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-29x29@3x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-40x40@1x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-40x40@2x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-40x40@3x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-60x60@2x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-60x60@3x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-76x76@1x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-76x76@2x.png (created)
  ios\Runner\Assets.xcassets\AppIcon.appiconset\Icon-App-83.5x83.5@2x.png (created)
  ios\Runner\Assets.xcassets\LaunchImage.imageset\Contents.json (created)
  ios\Runner\Assets.xcassets\LaunchImage.imageset\LaunchImage.png (created)
  ios\Runner\Assets.xcassets\LaunchImage.imageset\LaunchImage@2x.png (created)
  ios\Runner\Assets.xcassets\LaunchImage.imageset\LaunchImage@3x.png (created)
  ios\Runner\Assets.xcassets\LaunchImage.imageset\README.md (created)
  ios\Runner\Base.lproj\LaunchScreen.storyboard (created)
  ios\Runner\Base.lproj\Main.storyboard (created)
  ios\Runner\Info.plist (created)
  ios\Runner.xcodeproj\project.xcworkspace\contents.xcworkspacedata (created)
  ios\Runner.xcworkspace\contents.xcworkspacedata (created)
  lib\main.dart (created)
  flutter_samples.iml (created)
  pubspec.yaml (created)
  README.md (created)
  test\widget_test.dart (created)
Running "flutter packages get" in flutter_samples...            11.8s
Wrote 64 files.

All done!
[√] Flutter is fully installed. (Channel stable, v1.0.0, on Microsoft Windows [Version 10.0.17134.590], locale zh-CN)
[√] Android toolchain - develop for Android devices is fully installed. (Android SDK 28.0.3)
[√] Android Studio is fully installed. (version 3.3)
[√] IntelliJ IDEA Community Edition is fully installed. (version 2018.3)
[!] Connected device is not available.

Run "flutter doctor" for information about installing additional components.

In order to run your application, type:

  $ cd .
  $ flutter run

Your application code is in .\lib\main.dart.

exit code 0
</code></pre>
<p>Flutter 项目结构如下：</p>
<p><img src="https://images.gitbook.cn/FgyN1LDqJNmW3gJVJPef43BQ_oCW" alt="avatar" /></p>
<p>其中，Android 相关的修改和配置在 android 目录下，结构和 Android 应用项目结构一样；iOS 相关修改和配置在 ios 目录下，结构和 iOS 应用项目结构一样。最重要的 flutter 代码文件是在 lib 目录下，类文件以 .dart 结尾，语法结构为 Dart 语法结构。大致如下：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

void main() =&gt; runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

class _MyHomePageState extends State&lt;MyHomePage&gt; {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: &lt;Widget&gt;[
            Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.display1,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ),
    );
  }
}
</code></pre>
<h3 id="5">5 模拟器的安装与调试</h3>
<p>项目新建完毕了，接下来就是编译运行 Flutter 项目到真机或者模拟器了。先说模拟器，模拟器在我们下载的 Android SDK 的目录里，可以通过两种方法创建模拟器。推荐在 Android Studio 里新建一个模拟器，点击进入 AVD Manager。如果没有模拟器的话，就创建一个即可，可以选择最新的 SDK：</p>
<p><img src="https://images.gitbook.cn/FoE2B8pKzv7LawiWwpWUhIQqj-Te" alt="avatar" /></p>
<p>创建完毕后，我们就可以在电脑的模拟器目录看到我们创建的模拟器：</p>
<p><img src="https://images.gitbook.cn/FolTrOa8C8krRZs2OwneIN8tm0kL" alt="avatar" /></p>
<p>对应的模拟器 AVD Manager 相关也在 Android SDK 目录下：</p>
<p><img src="https://images.gitbook.cn/FhTBkPI2FiLBL18v2GUsk2ZwxJK-" alt="avatar" /></p>
<p>接下来我们就可以关闭相关窗口了，建立一个 bat 文件，写入启动模拟器的命令，这样每次启动模拟器直接运行这个 bat 文件即可：</p>
<pre><code class="java language-java">D:\Sdk\emulator\emulator.exe -avd Pixel_XL_API_28
</code></pre>
<p>模拟器所在的 SDK 目录根据你的实际情况位置修改即可。</p>
<p><img src="https://images.gitbook.cn/FvU09wJFTlpO3xNQn2sc9Yq2xVT4" alt="avatar" /></p>
<p>接下来，双击这个 bat 文件运行模拟器：</p>
<p><img src="https://images.gitbook.cn/Fl5aBUEHmI92ENafsWi8f5SE2G1H" alt="avatar" /></p>
<p>接着在项目所在目录运行 flutter run 命令即可编译运行 flutter 项目到模拟器上：</p>
<p><img src="https://images.gitbook.cn/FvtiHK9HVojNOuCJubiCs6YWZ4zc" alt="avatar" /></p>
<p>运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/Fn7Rl1mW5lzDZ_LNWnRVDV49knEJ" alt="avatar" /></p>
<p>运行成功后，后续运行调试只要不退出应用界面，就可以进行热重载，输入 r 进行热重载当前页面，输入 R 进行整个应用的热重启，输入 h 弹出帮助信息，输入 d 解除关联，输入 q 退出应用调试。如果遇到有多个模拟器或者模拟器和真机同时存在的话，可以通过 -d 参数加设备 ID 指定要运行的设备，例如：</p>
<pre><code class="java language-java">flutter run -d emulator-5556
</code></pre>
<p>可以通过 flutter devices 或 adb devices 命令查看目前已连接的设备信息。</p>
<p>还有一种命令方式创建模拟器，输入如下命令可以查看当前可用的模拟器：</p>
<pre><code class="java language-java">flutter emulator
</code></pre>
<p>输入以下命令可以创建指定名称的模拟器，默认创建的模拟器 Android 版本号为已安装的最新的 SDK 版本号：</p>
<pre><code class="java language-java">flutter emulators --create --name xyz
</code></pre>
<p>运行以下命令可以启动模拟器：</p>
<pre><code class="java language-java">flutter emulators --launch &lt;emulator id&gt;
</code></pre>
<p><emulator id> 替换为你的模拟器 ID 名称即可。</p>
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
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解 Flutter SDK 的主要版本区分、环境变量配置、开发工具的使用、模拟器运行、新建和运行项目等，为后面的正式高效学习与开发做好准备。主要建议如下：</p>
<ul>
<li>大家可以使用稳定版或者开发版 Flutter SDK，推荐使用稳定版。</li>
<li>如果遇到下载 SDK 慢或者无法下载情况，请按照课程内设置国内下载镜像地址。</li>
<li>配置好环境变量后，需要用 flutter doctor 检查一下环境。</li>
<li>尝试新建个项目运行到手机或模拟器上，看配置是否有问题。</li>
<li>开发工具可以使用 Visual Studio Code 或 Android Studio 等。</li>
</ul>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Flutter：从入门到实践》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「110」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>