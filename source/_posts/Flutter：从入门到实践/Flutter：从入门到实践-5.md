---
title: Flutter：从入门到实践-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>对于一门新语言或新技术的学习来说，在新建了项目之后，了解其项目结构及含义、配置文件的编写，这些对后续的开发和深入学习起到很重要的作用。俗话说磨刀不误砍柴工，Flutter 的学习也同理，我们在新建了 Flutter 项目后，需要进一步了解和学习 Flutter 的项目结构、文件的配置。而 Flutter 由于是跨平台应用，所以一般都会包括 Android 和 iOS 两个项目的目录以及 Flutter 框架相关的 dart 类源码等。</p>
<p>Flutter 的项目开发比较简单，项目结构也不算太复杂，所以大家应该有信心去掌握和学习 Flutter 相关知识。接下来，就开始我们认识 Flutter 项目结构及配置文件的学习之旅吧。</p>
<p>本节将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 的项目结构</li>
  <li>Flutter 配置文件讲解</li>
  <li>Flutter 代码结构</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 Flutter 的项目结构</h3>
<p>Flutter 包括 Android 和 iOS 两个项目的目录以及相关的 dart 类源码。</p>
<p>前面讲到过 Flutter 的新建项目，这里就不再赘述了。我们新建项目后，会看到如下图所示的 Flutter 默认项目结构：</p>
<p><img src="https://images.gitbook.cn/Fvvpu9rL7kgHKo-BM-v_Xjpg84FP" alt="avatar" /></p>
<p><img src="https://images.gitbook.cn/FkaHVvS2zGeqyf-vjaktAGv_M8RS" alt="avatar" /></p>
<p>我们可以看到主要包含了：android、ios、lib、test 几个目录以及 pubspec.yaml 配置文件等。接下来我们先看这几个目录的作用。</p>
<h4 id="11andorid">1.1 andorid 目录</h4>
<p>android 目录主要是存放一个完整的 Android 项目的目录。编译后，我们的 Flutter 代码会加入整合到这个 Android 项目中，形成一个 Flutter Android 应用。所以 android 目录存放的 Android 项目结构都是完整的，可以通过 Android Studio 打开进行编译、运行、开发、调试等等操作。这里把 android 目录的项目用 Android Studio 打开进行一下预览：</p>
<p><img src="https://images.gitbook.cn/FsaJVqCMgxs6G7d1bGi6sWs_qca3" alt="avatar" /></p>
<p>可以看到它就是一个完整的 Android 项目，代码最终编译为对应的 Android 平台的应用。这里的启动 Activity 就是 MainActivity，看下里面的内容：</p>
<pre><code class="dart language-dart">package com.example.flutter_samples;

import android.os.Bundle;
import io.flutter.app.FlutterActivity;
import io.flutter.plugins.GeneratedPluginRegistrant;

public class MainActivity extends FlutterActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    GeneratedPluginRegistrant.registerWith(this);
  }
}
</code></pre>
<p>可以看到，里面几乎没有什么代码逻辑，只是继承了 FlutterActivity，然后将 Flutter 相关插件注册进来。当然后续如果我们需要编写插件、编写原生交互的时候（一般不用这种，除非一定要写代码逻辑的时候，否则就脱离了 Flutter 插件化跨平台的特性），需要在这里写一些回调插件逻辑。不过这种情况一般是：Flutter 插件库里没有可以实现你的复杂功能的插件库，Flutter SDK 里无法实现你要的功能，这种情况就可能要与原生交互了。推荐是编写插件库形式进行与原生交互，更加规范和方便，也有利于后续组件化维护与共享。</p>
<p>如果需要更改 Android 应用包名、版本号、签名文件，修改方式和修改 Android 项目一样的，都是在 app 目录下的 build.gradle 里进行修改：</p>
<pre><code class="dart language-dart">android {
    compileSdkVersion 28
    ...
    defaultConfig {
        //应用包名
        applicationId "com.example.flutter_samples"
        minSdkVersion 16
        targetSdkVersion 28
        //版本号
        versionCode 1
        //版本名称
        versionName "1.0"
        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
    }
    ...
</code></pre>
<h4 id="12ios">1.2 ios 目录</h4>
<p>ios 目录和 android 目录一样，存放的是 iOS 项目文件，里面的 iOS 项目结构就是一个完整的 iOS 目录结构。可以使用 XCode 打开进行编译、修改、开发、调试等等操作。例如 iOS 平台的图标的修改、版本号的修改等等操作都是在这里，就不再重复说明。</p>
<h4 id="13lib">1.3 lib 目录</h4>
<p>lib 目录就是我们存放核心的 Flutter 代码逻辑的地方了，里面放置了 dart 语言的类源码文件（例如 main.dart）。我们的项目核心逻辑源码文件都是放在这里的，lib 下的源码最终会编译到 Android 和 iOS 平台进行渲染。</p>
<blockquote>
  <p>默认有一个 main.dart 类，这个 main.dart 类名字不可以修改,必须放置在 lib 根目录，它是我们项目的入口文件，入口类。</p>
</blockquote>
<p>test 目录里主要用于编写我们的测试用例，如测试 Widget UI、数据等等。默认里面有一个 widget_test.dart 文件。我们看下它的内容：</p>
<pre><code class="dart language-dart">//这个一个测试用例的小例子
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_samples/main.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // 编译APP
    await tester.pumpWidget(MyApp());

    // 验证初始状态下ui是否有显示为0的Widget和1的Widget
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // 点击"+"号图标，触发事件
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    //验证点击后是否实现加一功能，寻找ui上是否有显示为0的Widget和1的Widget
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });

  // test(description, body);
}
</code></pre>
<p>如果在 Visual Studio Code 里看这段，默认是有 Run 和 Debug 按钮的，我们可以点击 Run 进行运行测试用例：</p>
<p><img src="https://images.gitbook.cn/Fl4vR1xh3dSdoD1tlROh4D9IYiZJ" alt="avatar" /></p>
<h3 id="2flutter">2 Flutter 配置文件讲解</h3>
<h4 id="21pubspecyaml">2.1 pubspec.yaml</h4>
<p>这个是我们的 Flutter 项目的配置文件，也比较重要，我们在这里可以配置引用第三方插件库、添加 assets 图片资源、font 字体资源、音视频资源路径等等。整个文件是参照 YAML（YAML Ain't a Markup Language）语法规范进行定义的格式，其实就是通过缩进来形成结构目录，非常简单，因此就不过多描述语法了。我们看下 pubspec.yaml 配置文件的内容和结构：</p>
<pre><code class="dart language-dart">//项目名称：要用英文，类似于Android中的包名，如果它修改了整个项目的引入的路径都要修改
//所以一般确定了就不要修改
name: flutter_samples
//项目描述
description: A new Flutter project.

//版本号，这个会覆盖对应Android和IOS的应用版本号
//+号前对应Android的versionCode，+号后对应Android的versionName
//+号前对应IOS的CFBundleVersion，+号后对应IOS的CFBundleShortVersionString
version: 1.0.0+1

//表示项目的编译环境要求为dart sdk版本号在2.1.0和3.0.0之间
environment:
  sdk: "&gt;=2.1.0 &lt;3.0.0"


//项目的依赖插件库
//Flutter插件库在这里查找引用：https://pub.dartlang.org/flutter
dependencies:
  flutter:
    sdk: flutter
//我们可以在这里引入插件库
  cupertino_icons: ^0.1.2
  flutter_webview_plugin: ^0.3.1

dev_dependencies:
  flutter_test:
    sdk: flutter

//flutter相关配置
flutter:
//是否使用material图标，建议为true
  uses-material-design: true

  //配置项目文件里的图片路径
  //如果需要使用项目目录内附带的图片、音视频等资源，必须在这里配置定义
  assets:
    - images/a_dot_burr.jpeg
    - images/a_dot_ham.jpeg

  //字体文件资源相关配置
  fonts:
    - family: Schyler
      fonts:
        - asset: fonts/Schyler-Regular.ttf
        - asset: fonts/Schyler-Italic.ttf
          style: italic
    - family: Trajan Pro
      fonts:
        - asset: fonts/TrajanPro.ttf
        - asset: fonts/TrajanPro_Bold.ttf
          weight: 700

//下面这几项一般只有在编写插件库发布到Dart Pub时才写，一般不用写  
//作者
authors:
- Natalie Weizenbaum &lt;nweiz@google.com&gt;
- Bob Nystrom &lt;rnystrom@google.com&gt;
//主页
homepage: https://example-pet-store.com/newtify
//文档地址
documentation: https://example-pet-store.com/newtify/docs
//发布到
publish_to: none
</code></pre>
<p>这里再多说一句，如果我们在配置文件里引入了一个插件库后，比如 shared<em>preferences，我们再用 Android Studio 打开 Android 项目后，可以看到目录的依赖项里增加了 shared</em>preferences：</p>
<p><img src="https://images.gitbook.cn/Fi8If_ZTtmBuGaiLPcyDZ6pec0Ft" alt="avatar" /></p>
<p>然后 Android 项目主工程 GeneratedPluginRegistrant 类里增加了如下内容：</p>
<pre><code class="dart language-dart">package io.flutter.plugins;

import io.flutter.plugin.common.PluginRegistry;
import io.flutter.plugins.sharedpreferences.SharedPreferencesPlugin;

/**
 * 增加了注册shared_preferences插件库方法
 */
public final class GeneratedPluginRegistrant {
  public static void registerWith(PluginRegistry registry) {
    if (alreadyRegisteredWith(registry)) {
      return;
    }
    SharedPreferencesPlugin.registerWith(registry.registrarFor("io.flutter.plugins.sharedpreferences.SharedPreferencesPlugin"));
  }

  private static boolean alreadyRegisteredWith(PluginRegistry registry) {
    final String key = GeneratedPluginRegistrant.class.getCanonicalName();
    if (registry.hasPlugin(key)) {
      return true;
    }
    registry.registrarFor(key);
    return false;
  }
}
</code></pre>
<h4 id="22">2.2 其余几个文件</h4>
<p><strong>pubspec.lock</strong></p>
<p>里面指明了我们的 pubspec.yaml 等依赖包和项目依赖的库的具体版本号，我们可以在这里查看我们项目引用的依赖的具体版本号等信息，如果某个配置文件丢失，可以通过这个文件重新下载和恢复依赖库。为自动生成文件。</p>
<p><strong>.packages</strong></p>
<p>里面放置了项目依赖的库的具体在本机电脑上的绝对路径。为自动生成文件，如果项目出错或者无法找到某个库，可以把这个文件删除，重新自动配置即可。</p>
<p><strong>.metadata</strong></p>
<p>里面记录了我们项目的属性信息，如使用 Flutter SDK 哪个分支开发的，项目属性等，用于切换分支、升级 SDK 使用。自动生成，无需修改删除。</p>
<h3 id="3flutter">3 Flutter 代码结构</h3>
<p>前面介绍了 Flutter 的项目基本结构，我们来着重看下 lib 里的代码结构。</p>
<p>默认 lib 下有一个 main.dart 类，这个 main.dart 类名字不可以修改，必须放置在 lib 根目录，它是我们项目的入口文件，入口类。当然我们在实际开发中，还是根据需要进行源码类的包划分，这里给出一个示例：</p>
<p><img src="https://images.gitbook.cn/Fhxg6-b7M-L6KaYCfDEHQZIMKrww" alt="avatar" /></p>
<p><img src="https://images.gitbook.cn/FkTUU3CSZ5nTUPim_X66S3OxwA4V" alt="avatar" /></p>
<p>我们可以根据实际需要在 lib 里建立相关的文件夹，可以按照项目功能分、类的类型和功能分等等。</p>
<p>我们再看下 main.dart 入口文件内容结构：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

//void main()为入口方法,main.dart文件独有
void main() =&gt; runApp(MyApp());

class MyApp extends StatelessWidget {
  //应用的最顶层入口
  @override
  Widget build(BuildContext context) {
    //这里使用了MaterialApp脚手架，当然也可以使用WidgetApp，建议入口使用MaterialApp。
    //直接定义一个容器布局也可以
    return MaterialApp(
      //标题
      title: 'Flutter Demo',
      theme: ThemeData(
        //可以自定义配置主题色调
        primarySwatch: Colors.blue,
      ),
      //页面
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

//使用StatefulWidget有状态Widget
class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  //创建State状态
  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

class _MyHomePageState extends State&lt;MyHomePage&gt; {
  int _counter = 0;

  void _incrementCounter() {
    //每次执行这个方法_counter加一，然后用setState方法进行UI刷新
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    //Scaffold布局脚手架组件
    return Scaffold(
      //标题栏Widget组件
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
        //定义了一个Button，点击执行_incrementCounter()方法
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ),
    );
  }
}
</code></pre>
<p>这个代码例子是官方默认新建后的内容，运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/Fn7Rl1mW5lzDZ_LNWnRVDV49knEJ" alt="avatar" /></p>
<p>实现的功能就是每点击+号浮动按钮一次，显示 0 的 Widget 组件就加一。</p>
<p>代码整体风格就是 React 组件化响应式风格，类似于 DOM 树结构，通过小的 Widget 来组成一个大的页面。部分代码类似于 Java 的写法，其实还是比较简单。刚开始看的时候可能会觉得有点迷惑，不过不要担心，接触 Widget的学习后，大家就会对 Flutter 的编写风格有更直观的了解。 </p>
<p>再给大家一个简化版的 main.dart：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

//void main()为入口方法,main.dart文件独有
void main() =&gt; runApp(MyMainApp());

class MyMainApp extends StatefulWidget {
  //这里可以简写为：State&lt;StatefulWidget&gt; createState() =&gt; _MyMainPageState();
  @override
  State&lt;StatefulWidget&gt; createState() {
    return _MyMainPageState();
  }
}

class _MyMainPageState extends State&lt;MyMainApp&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      //页面
      home: Scaffold(
        appBar: AppBar(
          title: Text('标题'),
        ),
        body: Center(
          child: Text("我是内容"),
        ),
      ),
    );
  }
}
</code></pre>
<p>这样看着是不是更简单清晰了，效果如下图：</p>
<p><img src="https://images.gitbook.cn/FqZROSFWbn1FnS7keBhCYm9FKA6H" alt="avatar" /></p>
<p>大家可以按照这个效果图倒推看代码逻辑结构。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解 Flutter 项目结构及配置文件相关知识，为后面的 Flutter 学习打下基础。注意点和建议如下：</p>
<ul>
<li>可以尝试新建一个项目，查看和熟悉下项目相关目录文件信息和结构。</li>
<li>在项目配置文件里添加和修改一下配置信息，看看有什么变化。</li>
<li>多试多实践。</li>
</ul>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Flutter：从入门到实践》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「110」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>