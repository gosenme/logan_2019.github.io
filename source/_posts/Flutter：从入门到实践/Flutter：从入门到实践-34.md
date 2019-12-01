---
title: Flutter：从入门到实践-34
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用不同的开发语言进行开发时，一般都会用到调试、断点调试功能。例如 Web、Android 等等都是支持调试和断点调试的，Flutter 也不例外，支持调试和单元测试功能，还有性能、布局分析器等等。那么这节课就给大家讲解下 Flutter 的调试和测试等功能的使用，配合一些实例进行讲解。同时也会为大家讲解下 Flutter 开发后的最后一个部分：应用的打包（Android 和 iOS 打包）。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 的调试</li>
  <li>Flutter 的单元测试</li>
  <li>Flutter 辅助工具的使用</li>
  <li>Flutter Android 应用打包发布</li>
  <li>Flutter iOS 应用打包发布</li>
  </ul>
</blockquote>
<h3 id="flutter">Flutter 的调试</h3>
<p>在开发中经常会用到调试功能，来验证某些输入输出数据、查找分析问题等等。Flutter 也是支持调试功能的，而且也非常的强大。我们先从最简单的说起。</p>
<p>我们可以通过控制台输出 Log 日志来查看调试程序：</p>
<pre><code class="dart language-dart">print(object)
// 例如
int a = 6;
double b = 3.18;
print('$a ,$b');
// print取值通过$符号来取值
// debugPrint参数只能是String
debugPrint(String);
</code></pre>
<p>这种调试方式也成为日志调试。</p>
<p>debugPrint 用于当我们一次输出太多日志时，那么 Android 有时会丢弃一些日志行。为了避免这种情况，我们可以使用 Flutter 的 foundation 库中的 debugPrint()。 这是一个封装 print，可以避免被 Android 内核丢弃某些日志行。</p>
<p>我们可以在窗口通过 <code>flutter logs</code> 来过滤查看输出入日志。</p>
<p>接下来看下断点调试，这个也是比较重要和常用的调试手段。</p>
<p>我们先以 <strong>Android Studio</strong> 为例。</p>
<p>我们只需要在要添加断点的地方左侧点击一下就添加了一个红色的断点按钮。</p>
<p><img src="https://images.gitbook.cn/f7980710-adf1-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>接下来以 Debug 模式运行应用程序即可：</p>
<p><img src="https://images.gitbook.cn/09038fb0-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>我们以官方默认的例子为例，我们在点击 + 号按钮的地方设置了 2 个断点。当我们点击加号时会自动执行到断点地方暂停：</p>
<p><img src="https://images.gitbook.cn/16072a50-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>我们可以在线面的调试控制台里看到断点地方的各个信息和属性值，包括 _counter。</p>
<p>当前断点所在行地方会高亮，我们可以点击调试窗口的 Run to Cusor(Alt+F9) 跳到下一个断点。</p>
<p>怎么样，是不是很简单，和其他平台的断点调试很像。</p>
<p><strong>VS Code 的断点调试同理。</strong></p>
<p>点击要断点调试的所在行的左侧边栏，这时就会添加一个红色的断点按钮。</p>
<p><img src="https://images.gitbook.cn/7ff69c70-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>接着以 Debug 模式运行应用：</p>
<p><img src="https://images.gitbook.cn/8b5dec30-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>编辑器页面顶部会悬浮调试操作栏：</p>
<p><img src="https://images.gitbook.cn/96631ec0-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>左侧的 Debug 窗口可以查看相关属性值：</p>
<p><img src="https://images.gitbook.cn/a082fa60-adf2-11e9-8433-cbc6088d6c11" alt="断点调试" /></p>
<p>除了这几种调试外，还有一些命令的调试的支持。</p>
<p>如：Dart 分析器，用来检查分析代码并帮助发现代码中的一些问题和优化。我们在项目所在根目录输入命令行：<code>flutter analyze</code> 即可运行分析检测。</p>
<p><img src="https://images.gitbook.cn/0611aa70-adf3-11e9-8433-cbc6088d6c11" alt="Dart分析器" /></p>
<p>我们还可以在代码里植入一些调试专用 API 语句来实现调试功能：</p>
<p><strong>debugger()</strong></p>
<p>构造方法如下：</p>
<pre><code class="dart language-dart">external bool debugger({bool when: true, String message});
</code></pre>
<p>使用示例：</p>
<pre><code class="dart language-dart">import 'dart:developer';
... ...
  void _incrementCounter() {
    setState(() {
      _counter++;
    });
    print(_counter);
    // 满足某个条件时执行进入调试
    debugger(when: _counter &gt; 5.0);
  }
</code></pre>
<p>我们还可以设置 assert 断言来判断是否等于某个值。</p>
<p>使用示例：</p>
<pre><code class="dart language-dart">assert(_counter==2);
</code></pre>
<p><strong>debugDumpApp()</strong></p>
<p>我们还可以通过 debugDumpApp() 来获取整个页面的 Widget 树状结构层级图：</p>
<p><img src="https://images.gitbook.cn/133b43a0-adf3-11e9-8433-cbc6088d6c11" alt="debugDumpApp" /></p>
<p>我们可以详细的看到整个页面的Widget的内容。</p>
<p>debugDumpApp要在调用 <code>runApp()</code> 之后。</p>
<p><strong>debugDumpRenderTree()</strong></p>
<p>如果觉得 debugDumpApp() 输入的 Widget 层还不够详细，比较乱的话，也提供了 <code>debugDumpRenderTree()</code> 的使用。</p>
<p>使用 <code>debugDumpRenderTree()</code> 需要导入包：</p>
<pre><code class="dart language-dart">import'package:flutter/rendering.dart';
</code></pre>
<p><img src="https://images.gitbook.cn/561d4dd0-adf3-11e9-8433-cbc6088d6c11" alt="debugDumpRenderTree" /></p>
<p><strong>debugDumpLayerTree()</strong></p>
<p>层级调试信息：</p>
<p><img src="https://images.gitbook.cn/63783030-adf3-11e9-8433-cbc6088d6c11" alt="debugDumpRenderTree" /></p>
<p><strong>debugDumpSemanticsTree()</strong></p>
<p>我们还可以调用 debugDumpSemanticsTree() 获取语义树。</p>
<p>使用示例：</p>
<pre><code class="dart language-dart">debugDumpSemanticsTree(DebugSemanticsDumpOrder.traversalOrder);
</code></pre>
<p>需要开启：</p>
<pre><code class="dart language-dart">class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // 开启showSemanticsDebugger
      showSemanticsDebugger: true,
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
</code></pre>
<p><img src="https://images.gitbook.cn/702c7250-adf3-11e9-8433-cbc6088d6c11" alt="debugDumpSemanticsTree" /></p>
<p><img src="https://images.gitbook.cn/a80c3020-adf3-11e9-8433-cbc6088d6c11" alt="debugDumpSemanticsTree" /></p>
<p><strong>可视化调试</strong></p>
<p>我们可以通过设置 debugPaintSizeEnabled 为 true 以可视化方式调试布局问题。</p>
<pre><code class="dart language-dart">... ...
 @override
  Widget build(BuildContext context) {
    debugPaintSizeEnabled = true;
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
... ...
</code></pre>
<p><img src="https://images.gitbook.cn/60084f10-adf9-11e9-8433-cbc6088d6c11" alt="可视化调试" /></p>
<p>会绘制一些基线、辅助线、箭头、颜色等信息帮助我们分析和绘制布局。</p>
<p>类似这样的配置命令有：
debugPaintBaselinesEnabled、debugPaintPointersEnabled、debugPaintLayerBordersEnabled、debugRepaintRainbowEnabled 等。这些都只能在 debug 模式下使用和看到。</p>
<p>大家可以分别尝试下，看下它们的特点和不同点。</p>
<p>其他命令：debugPrintBeginFrameBanner、debugPrintEndFrameBanner、debugPrintScheduleFrameStacks。用法类似 debugPaintSizeEnabled。</p>
<pre><code class="dart language-dart">... ...
 @override
  Widget build(BuildContext context) {
    debugPrintBeginFrameBanner = true;
    debugPrintEndFrameBanner = true;
    debugPrintScheduleFrameStacks = true;
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
... ...
</code></pre>
<p><strong>动画的调试</strong></p>
<p>当我们制作了一个动画，由于动画运行太快，我们无法观察动画的细节，调试动画最简单的方法是减慢它们的速度。所以 Flutter 也提供了动画调试功能：可以将 timeDilation 变量（在 scheduler 库中）设置为大于 1.0 的数字，例如 60.0。我们只需在应用程序启动时设置赋值一次即可。</p>
<pre><code class="dart language-dart">class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    timeDilation = 60.0;
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      showSemanticsDebugger: false,
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
</code></pre>
<p><strong>性能的调试</strong></p>
<p>要了解我们的应用程序导致重新布局或重新绘制的原因，我们可以分别设置 <code>debugPrintMarkNeedsLayoutStacks</code> 和 <code>debugPrintMarkNeedsPaintStacks</code> 标志。每当渲染盒被要求重新布局和重新绘制时，这些都会将堆栈跟踪记录到控制台。可以使用 <code>services</code> 库中的 <code>debugPrintStack()</code> 方法按需打印堆栈痕迹。</p>
<pre><code class="dart language-dart">class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {

    debugPrintMarkNeedsLayoutStacks = true;
    debugPrintMarkNeedsPaintStacks = true;
    debugPrintStack();

    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      showSemanticsDebugger: false,
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
</code></pre>
<p><strong>应用启动时间的查看</strong></p>
<p>如果我们想查看应用启动时间相关信息，可以通过这种命令方式运行 Flutter 程序：</p>
<pre><code class="dart language-dart">$ flutter run --trace-startup --profile
</code></pre>
<p>在 Flutter 的项目根目录的 build 目录下的 <code>start_up_info.json</code> 文件里。</p>
<p>各个关键阶段的启动时间信息都可以看到：</p>
<pre><code class="json language-json">{ // 进入Flutter引擎
  "engineEnterTimestampMicros": 96025565262,
  // 展示应用第一帧
  "timeToFirstFrameMicros": 2171978,
  // 初始化Flutter框架
  "timeToFrameworkInitMicros": 514585,
  // 完成Flutter框架初始化
  "timeAfterFrameworkInitMicros": 1657393
}
</code></pre>
<p><strong>代码、方法执行时间查看</strong></p>
<p>如果想跟踪代码的性能、执行时间的话，可以使用 <code>dart:developer</code> 的 <code>Timeline</code> API来测试我们的的代码块：</p>
<pre><code class="dart language-dart">Timeline.startSync('interesting function');

// 方法

Timeline.finishSync();
</code></pre>
<p><strong>应用程序性能图</strong></p>
<p>如果想直观的查看应用程序时时性能图，可以开启 <code>showPerformanceOverlay</code>：</p>
<pre><code class="dart language-dart">class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      showPerformanceOverlay: true,
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
</code></pre>
<p>会显示两个图表。第一个是 GPU 线程花费的时间，第二个是 CPU 线程花费的时间。</p>
<p>图中的白线以 16ms 增量沿纵轴显示;如果图中超过这三条线，那么我们的应用运行频率低于 60Hz，横轴代表帧。该图仅在应用程序绘制时更新，因此如果它处于空闲状态，该图将停止移动。</p>
<p><img src="https://images.gitbook.cn/d2e1c3a0-adf3-11e9-8433-cbc6088d6c11" alt="应用程序性能图" /></p>
<p><strong>网格线</strong></p>
<p>Material grid 网格线功能可以辅助我们进行对其验证。用法很简单，开启 <code>debugShowMaterialGrid</code>。</p>
<pre><code class="dart language-dart">class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowMaterialGrid: true,
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}
</code></pre>
<p>效果如下图：</p>
<p><img src="https://images.gitbook.cn/e9094db0-adf3-11e9-8433-cbc6088d6c11" alt="网格线" /></p>
<p>关于调试还有异常捕获、日志收集等，后续会给大家讲解。</p>
<h3 id="flutter-1">Flutter 的单元测试</h3>
<p>接下来我们看下 Flutter 的单元测试。
单元测试在项目根目录的 test 目录下，默认有一个 widget_test.dart 示例文件。</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_app/main.dart';

// main方法为入口函数
void main() {

  // 单元测试的一个用例的方法名
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // 运行应用
    await tester.pumpWidget(MyApp());

    // 验证我们的界面widget显示的是0，而不是1
    // 期望找到一个含有0这个字符的Widget
    expect(find.text('0'), findsOneWidget);
    // 期望没有含有1这个字符的Widget
    expect(find.text('1'), findsNothing);

    // 模拟触发点击+号图标
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // 验证我们的字符已经增加改变了
    // 期望找到0个含有0这个字符的Widget
    expect(find.text('0'), findsNothing);
    // 期望找到一个含有1这个字符的Widget
    expect(find.text('1'), findsOneWidget);
  });
}
</code></pre>
<p>怎么样是不是很简单。</p>
<p>如果我们用的是 VS 
 Code 的话，会看到 <code>Run|Debug</code> 这个点击按钮开始运行单元测试。</p>
<p><img src="https://images.gitbook.cn/0617a870-adf4-11e9-8433-cbc6088d6c11" alt="单元测试" /></p>
<h3 id="flutter-2">Flutter 辅助工具的使用</h3>
<p>接下来我们看下 Android Studio 下的一些 Flutter 辅助工具：</p>
<p><img src="https://images.gitbook.cn/2d9dc2d0-adf4-11e9-8433-cbc6088d6c11" alt="Flutter 辅助工具" /></p>
<p>我们可以在 View-&gt;Tool Windows 下查看到一些辅助工具，如：Dart Analysis（代码分析审查）、Flutter Inspector（用于可视化和浏览 Flutter Widget 树）、Flutter Outline（代码层级结构查看）、Flutter Performance（性能分析的）。</p>
<p><strong>Dart Analysis</strong> 用于代码的检查和优化分析，如代码中无效的常量、变量声明等等。</p>
<p><strong>Flutter Inspector</strong> 用于可视化和浏览当前页面布局的 Flutter Widget 树。</p>
<p><img src="https://images.gitbook.cn/421cf410-adf4-11e9-8433-cbc6088d6c11" alt="Flutter Inspector" /></p>
<p><img src="https://images.gitbook.cn/b56b14b0-adf4-11e9-8433-cbc6088d6c11" alt="Flutter Inspector" /></p>
<p>点击 Flutter Inspector 工具栏上的 Select widget，然后点击设备选择一个 widget。所选 Widget将在设备和 Widget 树结构中高亮显示。</p>
<p><img src="https://images.gitbook.cn/77802a10-adfd-11e9-8433-cbc6088d6c11" alt="Flutter Inspector" /></p>
<p>点击真机某个 Widget 或点击 Flutter Inspector 某个 Widget，都会在设备上和 Flutter Inspector 上有相应显示。</p>
<p><img src="https://images.gitbook.cn/1016c030-adf5-11e9-8433-cbc6088d6c11" alt="Flutter Inspector" /></p>
<p><strong>Flutter Outline</strong> 可以查看代码的结构层级。</p>
<p><img src="https://images.gitbook.cn/3370e420-adf5-11e9-8433-cbc6088d6c11" alt="Flutter Outline" /></p>
<p><strong>Flutter Performance</strong> 用作时时性能分析和显示的。</p>
<p>如帧率、内存使用等统计显示。</p>
<p><img src="https://images.gitbook.cn/48a9a160-adf5-11e9-8433-cbc6088d6c11" alt="Flutter Performance" /></p>
<p><img src="https://images.gitbook.cn/5201e740-adf5-11e9-8433-cbc6088d6c11" alt="Flutter Performance" /></p>
<p>当然，除了以上这些，还有下图这几个强大的工具：</p>
<p><img src="https://images.gitbook.cn/5c9a2730-adf5-11e9-8433-cbc6088d6c11" alt="Flutter 辅助工具" /></p>
<p><strong>Dart DevTools</strong>
我们可以在 Web 浏览器上打开。功能比较强大，集合了很多工具功能。</p>
<p><img src="https://images.gitbook.cn/7c273d90-adf5-11e9-8433-cbc6088d6c11" alt="Dart DevTools" /></p>
<p>集合了：Flutter Inspector、Timeline、Memory、Performance、Debugger、Logging 功能，这些数据显示变成了在 Web 端显示和操作。大家可以详细体验下，前面都大致给大家说了下这些功能，这里就详细说了。</p>
<p>例如我们可以在这里打断点、查看日志等等：</p>
<p><img src="https://images.gitbook.cn/88f5e580-adf5-11e9-8433-cbc6088d6c11" alt="Dart DevTools" /></p>
<p><img src="https://images.gitbook.cn/ae68d750-adf5-11e9-8433-cbc6088d6c11" alt="Dart DevTools" /></p>
<p><strong>Timeline</strong></p>
<p>访问地址类似于这种格式：
http://127.0.0.1:57553/cAHbB_v162I=/#/timeline
我们可以看到一些方法、程序、页面的执行时间信息：</p>
<p><img src="https://images.gitbook.cn/cc566e80-adf5-11e9-8433-cbc6088d6c11" alt="Timeline" /></p>
<p><strong>Dart VM Observatory</strong></p>
<p>访问地址类似于这种格式：http://127.0.0.1:57553/cAHbB_v162I=/#/vm</p>
<p>这个通过 <code>flutter run</code> 命令启动后，会在控制台自动输出这个访问地址。</p>
<p>我们在这里同样可以看到很多不同功能的工具集合：</p>
<p><img src="https://images.gitbook.cn/e88b3220-adf5-11e9-8433-cbc6088d6c11" alt="Dart VM Observatory" /></p>
<p>大家可以一一详细体验使用下，这里就不再重复详细讲解了。</p>
<h3 id="flutterandroid">Flutter Android 应用打包发布</h3>
<p>终于到了应用打包发布的时候了。我们先看下 Android 的应用打包发布，非常的简单。</p>
<p>主要关注点如下。</p>
<p><strong>应用包名</strong> </p>
<p>应用包名也是应用的唯一标识，格式类似于 com.google.googlemap 这种形式。类似域名倒着写+产品英文名。</p>
<p>包名的配置和修改在 android 项目 app 目录下的 build.gradle 里，它位于项目目录 /android/app/下：</p>
<pre><code class="dart language-dart">applicationId "com.flutter.flutter_app"
</code></pre>
<p>applicationId 便是包名配置项。</p>
<p>versionCode 和 versionName 指定应用程序版本号和版本号字符串。</p>
<p>minSdkVersion 和 targetSdkVersion 指定最低的 API 级别以及应用程序设计运行的 API 级别。</p>
<p>AndroidManifest.xml 主要看是否缺少某些权限。如：</p>
<pre><code class="dart language-dart">&lt;uses-permission android:name="android.permission.INTERNET"/&gt;
&lt;uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/&gt;
&lt;uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/&gt;
</code></pre>
<p><strong>应用图标的替换</strong> </p>
<p>在项目目录 /android/app/src/main/res/ 目录中，将图标文件放入 mipmap-xxx 文件夹下。</p>
<p><img src="https://images.gitbook.cn/f5ca7630-adf5-11e9-8433-cbc6088d6c11" alt="应用图标的替换" /></p>
<p>具体的尺寸按照不同的目录下的 ic_launcher.png 这个默认图标进行设计替换即可。</p>
<p><strong>应用签名</strong> </p>
<p>应用必须要签名后才可以进行发布和使用。</p>
<p>我们接下来看下如何制作 Android 的应用签名文件：</p>
<p>我们先用 Android Studio 单独打开 Android 项目 Module：</p>
<p><img src="https://images.gitbook.cn/2321f9a0-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>我们需要使用 Android Studio 制作签名文件，<code>Build-&gt; Generate Signed Bundle/APK</code>：</p>
<p><img src="https://images.gitbook.cn/46753fc0-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>选择 APK：</p>
<p><img src="https://images.gitbook.cn/632cc7f0-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>接下来就开始制作签名 keystore了：</p>
<p>点击 “Create new…“：</p>
<p>在 Key store path 里选择 keystore 签名文件存储的位置，然后输入签名密钥的密码。Alias 为这个签名文件的别名，也可以理解为备注。</p>
<p><img src="https://images.gitbook.cn/8062cef0-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>输入相关的签名文件信息，前几项不说了，后面的是 Validity——有效年限；First and Last Name——名字；Organizational Unit——单位名称；Organization——组织；City or Locality——城市；State or Province——省份；Country Code——国家代码。</p>
<p>创建好后，回到这个界面。</p>
<p><img src="https://images.gitbook.cn/93b6edb0-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>选择一个打包模式就可以打包了：</p>
<p><img src="https://images.gitbook.cn/af89e240-adf6-11e9-8433-cbc6088d6c11" alt="应用签名" /></p>
<p>当然，我们不这样打包 Flutter 的 APK，这一步只是为了创建我们的签名 keystore。</p>
<p>我们在 Android 项目的 app 目录下的 build.gradle 里配置签名信息：</p>
<pre><code class="java language-java">signingConfigs {
        release {
            keyAlias 'flutterNote'
            keyPassword 'key123'
            storeFile file('D:/flutterapp/flutter.jks')
            storePassword 'key123'
            v1SigningEnabled true
            v2SigningEnabled true
        }
    }

    buildTypes {
        debug {
            buildConfigField "boolean", "LOG_DEBUG", "true"
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.debug
        }
        release {
            //关闭日志输出
            buildConfigField "boolean", "LOG_DEBUG", "false"
            //关闭混淆
            minifyEnabled false
            //Zipalign优化：4字节对齐，减少运行内存消耗　
            zipAlignEnabled true
            //混淆规则文件
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            //签名文件
            signingConfig signingConfigs.release
        }
    }
</code></pre>
<p>这样我们在打包 Android Flutter 项目的 APK 时便会自动根据 debug 版本或 release 版本自动进行签名了。</p>
<p>接下来我们在控制台窗口运行打包命令：</p>
<pre><code class="dart language-dart">$ flutter build apk
// 或
$ flutter build apk --release
</code></pre>
<p>打包好的发布 APK 位于 项目目录 /build/app/outputs/apk/app-release.apk</p>
<p>打包好的 APK 我们也可以对它进行加固处理，可以使用 360 加固保或腾讯乐固进行加固处理。</p>
<p>这个 APK 我们便可以发布到各个应用商店。</p>
<h3 id="flutterios">Flutter iOS 应用打包发布</h3>
<p>接下来我们看下 Flutter iOS 应用的打包发布步骤。</p>
<p>我们需要在 Mac 下安装好 Android Studio 和 Xcode。</p>
<p>Android Studio 可以在官方下载 Mac 版本：
<a href="https://developer.android.google.cn/studio">https://developer.android.google.cn/studio</a></p>
<p>Xcode 在 AppStore 下载即可。</p>
<p>Android Studio 里安装好 Flutter 和 Dart 插件。接着下载 Flutter SDK，配置好 Mac 下环境变量。</p>
<p>给大家讲解下 Mac 下配置 Flutter 环境变量：</p>
<pre><code class="dart language-dart">//在终端进入用户目录，一般打开终端默认就是
cd ~           

//打开配置文件
open .bash_profile    

//如果 .bash_profile文件不存在需先创建再打开，具体如下：
touch .bash_profile
open .bash_profile

//添加环境变量
export PATH=${PATH}:/Users/xxx/flutter/bin:$PATH
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn

// 执行文件 使命令生效
source .bash_profile      
</code></pre>
<p>假如我的 Flutter SDK 目录在 Users/td 下的 Documents 目录下，那么 PATH 就是：</p>
<pre><code class="dart language-dart">export PATH=${PATH}:/Users/td/Documents/flutter/bin:$PATH
</code></pre>
<p>接下来输入 <code>flutter</code> 查看是否配置成功。</p>
<p>然后输入 <code>flutter doctor</code> 来检查 Flutter 运行环境是否完整：</p>
<p><img src="https://images.gitbook.cn/d1e533d0-adf6-11e9-8433-cbc6088d6c11" alt="检查环境" /></p>
<p>根据提示安装好各种所缺的库、文件即可。</p>
<p>这里讲解下安装 brew。</p>
<p>brew 官方地址：<a href="https://brew.sh/">https://brew.sh/</a></p>
<p>安装命令为：</p>
<pre><code class="dart language-dart">/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
</code></pre>
<p>但是一般安装速度非常慢，我们需要更换源：</p>
<p>首先获取 brew_install 文件。</p>
<pre><code class="dart language-dart">curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install &gt;&gt; brew_install
</code></pre>
<p>接下来找到并编辑 brew_install 文件。</p>
<pre><code class="dart language-dart">#BREW_REPO = "https://github.com/Homebrew/brew".freeze
BREW_REPO = "git://mirrors.ustc.edu.cn/brew.git".freeze
</code></pre>
<p>这样我们就可以用新的源安装 brew。</p>
<pre><code class="dart language-dart">/usr/bin/ruby ./brew_install
</code></pre>
<p>安装好 brew 后如果想下载其他库非常慢的话，可以使用清华镜像：
<a href="https://mirror.tuna.tsinghua.edu.cn/help/homebrew/">https://mirror.tuna.tsinghua.edu.cn/help/homebrew/</a></p>
<p>替换现有上游：</p>
<pre><code class="dart language-dart">git -C "$(brew --repo)" remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

git -C "$(brew --repo homebrew/core)" remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

brew update
</code></pre>
<p>接下来进入正题，我们用 Xcode 打开我们通过 Android Studio 或 VS Code 创建的 Flutter 项目的 iOS 项目目录：</p>
<p><img src="https://images.gitbook.cn/ebf6a240-adf6-11e9-8433-cbc6088d6c11" alt="IOS项目" /></p>
<p>打开后可以看到这样的项目信息界面：</p>
<p><img src="https://images.gitbook.cn/fa232c80-adf6-11e9-8433-cbc6088d6c11" alt="IOS项目" /></p>
<p>我们依然只需要像 Android 一样关注几个点即可。</p>
<p><strong>Display Name</strong> 要在主屏幕和其他地方显示的应用程序的名称。</p>
<p><strong>Bundle Identifier</strong> 在 iTunes Connect 上注册的 App ID。（类似于 Android 的应用唯一包名：com.xxx.xxx）</p>
<p><strong>Version</strong> 版本名称，类似于 Android 的 VersionName。</p>
<p><strong>Build</strong> 版本号，类似于 Android 的 VersionCode。</p>
<p><strong>Team</strong> 选择与我们注册的 Apple Developer 帐户关联的团队。如果需要，请选择 Add Account…，然后更新此设置。新版 XCode 要求必须要有 Team 账户。</p>
<p><strong>App Icons and Launch Images</strong> 应用图标设置。当创建新的 Flutter 应用程序时，会创建一个默认的 Flutter 图标占位图标集。在这一步中，我们可以用自己的图标替换这些占位图标。</p>
<p><img src="https://images.gitbook.cn/0a936530-adf7-11e9-8433-cbc6088d6c11" alt="IOS项目" /></p>
<p>有不同尺寸的图标：</p>
<p><img src="https://images.gitbook.cn/240d0070-adf7-11e9-8433-cbc6088d6c11" alt="IOS项目" /></p>
<p>在 Runner 文件夹中选择 Assets.xcassets，里面有相应的图标，替换即可。</p>
<p>替换后，我们可以运行 <code>flutter run</code>，验证应用图标是否已被替换。</p>
<p>这样主要的关注点都已经大致了解了。</p>
<p>但是如果要开发、测试、发布 iOS 应用，还应先在 App Store Connect：<a href="https://appstoreconnect.apple.com/">https://appstoreconnect.apple.com/</a>  上注册相应的开发者账号。</p>
<p>App Store Connect 是我们创建和管理应用程序的地方。我们可以创建应用程序名称和说明，添加屏幕截图，设置价格并管理版本到 App Store 和 TestFlight。</p>
<p>注册创建我们的应用程序涉及两个步骤：注册唯一的 Bundle ID，并在 App Store Connect 上选择运行的设备创建应用程序。</p>
<p><strong>注册 Bundle ID</strong></p>
<p>每个 iOS 应用程序都与一个 Bundle ID 关联，这是一个在 Apple 注册的唯一标识符。操作步骤：</p>
<ol>
<li>打开开发者帐户的 App IDs 页：<a href="https://developer.apple.com/account/ios/identifier/bundle">https://developer.apple.com/account/ios/identifier/bundle</a> ；</li>
<li>点击 + 创建一个 Bundle ID；</li>
<li>输入应用程序名称, 选择 Explicit App ID, 然后输入一个 ID；</li>
<li>选择我们的应用将使用的服务，然后点击 ”Continue”；</li>
<li>在下一页中，确认详细信息，然后点击 Register 注册Bundle ID。</li>
</ol>
<p><strong>在 App Store Connect 上创建应用程序记录</strong></p>
<ol>
<li>在浏览器中打开 App Store Connect：<a href="https://appstoreconnect.apple.com/">https://appstoreconnect.apple.com/</a>；</li>
<li>在 App Store Connect 登陆页上，点击 “My Apps“；</li>
<li>点击 My App 页面左上角的 “+“ ，然后选择 New App；</li>
<li>填写我们的应用详细信息。在 Platforms 部分中，确保已选中 iOS。由于 Flutter 目前不支持 tvOS，请不要选中该复选框。点击 “Create“；</li>
<li>跳转到我们的 APP 的应用程序详细信息页，App Information；</li>
<li>在 General Information 部分, 选择并填写我们在上一步中注册的 Bundle ID。</li>
</ol>
<p>在开发过程中，我们一直在开发、调试、测试 debug 版本。如果想正式发布应用到 App Store 或 TestFlight 上时，需要准备 release 版本:</p>
<p>运行 <code>flutter build ios</code> 来创建 iOS 的 release 版本（flutter build 默认为 --release）。</p>
<p><strong>归档并上传到 App Store Connect</strong></p>
<p>接下来我们如果要上传到 App Store Connect 上需要进行归档：</p>
<ol>
<li>选择 Product &gt; Archive 来归档；</li>
<li>在 Xcode Organizer 窗口的边栏中，选择我们的 iOS 应用程序，然后选择刚刚生成的 build 档案。
点击 “Validate…“ 按钮；</li>
<li>档案已成功验证后，单击 “Upload to App Store…“，您可以在 App Store Connect 的应用详情页的 “Activities” 选项卡中查看构建状态；</li>
</ol>
<p>我们大概在 30 分钟内收到一封电子邮件，通知构建归档已经过验证，并可以在 TestFlight 上发布给测试人员。此时，我们可以选择是否在 TestFlight 上发布，或继续并直接将我们的 release 版发布到 App Store。</p>
<p><strong>在 TestFlight 发布应用到 App Store</strong></p>
<p>TestFlight 允许开发人员将应用程序推送给内部和外部测试人员。在这个可选步骤中，您将在 TestFlight 上发布 build：</p>
<ol>
<li>在 App Store Connect 上跳转到应用程序详细信息页面的 TestFlight 选项卡；</li>
<li>在侧边栏选择 “Internal Testing“；</li>
<li>选择要发布到测试人员的 build，然后单击 “Save“；</li>
<li>加任何内部测试人员的电子邮件地址。我们可以在 App Store Connect 的用户和角色页面添加更多的内部用户，可从页面顶部的下拉菜单中看到。</li>
</ol>
<p><strong>发布到 App Store</strong></p>
<p>最后一个步骤：准备将应用发布到 App Store，我们可以按照以下步骤将应用提交给 App Store 进行审查和发布：</p>
<p>1、从 iTunes 应用程序的应用程序详情页的边栏中选择 “Pricing and Availability“，然后填写所需的信息；
2、从边栏选择状态。如果这是该应用的第一个版本，则其状态将为 <code>1.0 Prepare for Submission</code>，并完成所有必填字段；
3、最后点击 “Submit for Review“。</p>
<p>Apple 会在应用程序审查完成时通知我们。我们的应用将根据我们在 Version Release 部分指定的说明描述进行发布到 App Store。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的几种调试方法以及 Android 和 iOS 应用的打包和发布。主要注意点和建议如下。</p>
<ul>
<li>掌握 Flutter 的几种调试方式，重点是断点调试。</li>
<li>熟练掌握 Android 的签名及打包、iOS 的打包发布流程，可以尝试发布一个小应用到应用市场。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>