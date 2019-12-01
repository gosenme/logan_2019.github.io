---
title: Flutter：从入门到实践-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>经过前面几节理论课程对 Flutter 的介绍，相信大家对 Flutter 有基础了解，也希望对 Flutter 的编程和应用开发产生了更加浓厚的兴趣。理论过后，估计大家正期待进入 Flutter 应用的编写实践。那么这节课就带领大家先尝试编写一个 Flutter 应用，感受一下 Flutter 开发的语法特点和运行效率。</p>
<p>Flutter 应用运行起来比 RN 流畅、编译快、热加载快，所以开发和调试的效率非常高。本文将着重给大家讲解下 Flutter 官方默认创建的应用，然后编写一个简单的 Flutter 尝鲜小应用。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>用 Flutter 创建一个默认应用</li>
  <li>Flutter 默认应用的分析讲解</li>
  <li>Flutter 编写一个小 Demo</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 用 Flutter 创建一个默认应用</h3>
<p>本文的开发工具 IDE 用的是 Visual Studio Code，当然也可以使用 Android Studio 进行开发。关于用 Visual Studio Code 创建新的 Flutter 项目前面讲过，这里就不再重复讲解了。</p>
<p>默认新建的 Flutter 项目都是这个简单的实例，运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fn7Rl1mW5lzDZ_LNWnRVDV49knEJ" alt="Flutter 官方实例" /></p>
<p>点击 + 号 FloatingActionButton，中间的 Text Widget 进行累加更新数字统计计数。整体功能还是很简单的，主要涉及内容为控件点击事件、Text Widget 的显示、 setState(() {...}) 更新内容等。</p>
<p>那么接下来通过代码结合注释讲解方式来看下这个官方实例 main.dart 的实现流程：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

//main.dart为应用入口dart类，里面void main()方法为入口函数
// 这里是lambda缩略写法，完整写法为下面这种：
// void main(){
//   return runApp(MyApp());
// }
void main() =&gt; runApp(MyApp());

class MyApp extends StatelessWidget {
  // 这个Widget是应用的根布局，类似于页面容器
  //构建搭建页面
  @override
  Widget build(BuildContext context) {
    //入口页使用MaterialApp这个页面脚手架
    //可以快速构建页面
    //MaterialApp这个脚手架默认自带顶部ToolBar、路由、主题、国际化等等配置
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // 在这里我们可以配置应用全局主题，后面主题课程部分会详细讲解
        //
        // 我们可以通过flutter run命令来运行程序，会看到蓝色状态栏和标题栏
        // 通过 primarySwatch属性来配置状态栏和标题栏颜色
        primarySwatch: Colors.green,
      ),
      // 设置启动页面Widget
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

// 继承StatefulWidget，有状态管理
class MyHomePage extends StatefulWidget {
  // 这个是有参构造方法，用来传值的，这里我们不管
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  //重写创建状态
  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

  // 自定义创建状态管理，继承自State&lt;T&gt;
class _MyHomePageState extends State&lt;MyHomePage&gt; {
  //声明变量临时存储次数
  int _counter = 0;
  // 定义方法来累加次数
  void _incrementCounter() {
    setState(() {
      //setState里用于刷新UI和绑定数据
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    // 这个方法每次调用 setState 都会调用
    //
    // Flutter框架已经帮我们优化了这部分，所以当我们需要刷新状态的时候不用担心性能问题
    // 这个用来构建页面具体布局，这里使用了Scaffold脚手架
    // 里面包含了AppBar、body、bottomNavigationBar、floatingActionButton等
    return Scaffold(
      appBar: AppBar(
        // 通过配置AppBar属性来控制显示效果，这里通过title来设置标题内容
        title: Text(widget.title),
      ),
      body: Center(
        // body部分用Center Widget布局来加载Widget布局内容，子控件居中排列
        child: Column(
          // Column是一个纵向列布局，子控件纵向排列
          mainAxisAlignment: MainAxisAlignment.center,
          children: &lt;Widget&gt;[
            //子控件，Text Widget用来显示文字内容
            Text(
              'You have pushed the button this many times:',
            ),
            // 动态绑定数据
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.display1,
            ),
          ],
        ),
      ),
      // 浮动+号按钮
      floatingActionButton: FloatingActionButton(
        // 设置点击事件，执行_incrementCounter方法累加计数
        onPressed: _incrementCounter,
        // 设置长按提示的信息
        tooltip: 'Increment',
        // 设置图标
        child: Icon(Icons.add),
      ),
    );
  }
}
</code></pre>
<p>通过 primarySwatch 属性来配置状态栏和标题栏颜色效果如下图：</p>
<p><img src="https://images.gitbook.cn/FmbQpHtBXDnQ85QoGfIE781i0XrZ" alt="Flutter更改主题色调" /></p>
<p>一般入口文件用 MaterialApp 脚手架构建，其它页面可以不使用。</p>
<p>我们看下 MaterialApp 脚手架构造方法都提供了哪些可配置的属性功能：</p>
<pre><code class="dart language-dart">const MaterialApp({
    Key key,
    this.navigatorKey,
    this.home,
    this.routes = const &lt;String, WidgetBuilder&gt;{},
    this.initialRoute,
    this.onGenerateRoute,
    this.onUnknownRoute,
    this.navigatorObservers = const &lt;NavigatorObserver&gt;[],
    this.builder,
    this.title = '',
    this.onGenerateTitle,
    this.color,
    this.theme,
    this.darkTheme,
    this.locale,
    this.localizationsDelegates,
    this.localeListResolutionCallback,
    this.localeResolutionCallback,
    this.supportedLocales = const &lt;Locale&gt;[Locale('en', 'US')],
    this.debugShowMaterialGrid = false,
    this.showPerformanceOverlay = false,
    this.checkerboardRasterCacheImages = false,
    this.checkerboardOffscreenLayers = false,
    this.showSemanticsDebugger = false,
    this.debugShowCheckedModeBanner = true,
  })
</code></pre>
<p>再看下 Scaffold 脚手架构造方法给我们提供的可配置的属性功能：</p>
<pre><code class="dart language-dart">const Scaffold({
    Key key,
    this.appBar,
    this.body,
    this.floatingActionButton,
    this.floatingActionButtonLocation,
    this.floatingActionButtonAnimator,
    this.persistentFooterButtons,
    this.drawer,
    this.endDrawer,
    this.bottomNavigationBar,
    this.bottomSheet,
    this.backgroundColor,
    this.resizeToAvoidBottomPadding,
    this.resizeToAvoidBottomInset,
    this.primary = true,
    this.drawerDragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>具体这些属性作用，大家可以大致有所了解，这里不再详细解释，后面课程会讲解。</p>
<p>看到这里，你觉得怎么样，Flutter 实现一个页面就是这样简单的。</p>
<h3 id="2flutterdemo">2 用 Flutter 编写一个小 Demo</h3>
<p>接下来我们动手自己写一个简单的页面，实现页面显示一段文字加一张图片，点击按钮切换文字内容的小 Demo：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

void main() {
  return runApp(ShowApp());
}

class ShowApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: ShowAppPage(),
    );
  }
}


class ShowAppPage extends StatefulWidget {

  @override
  _ShowAppPageState createState() {
    return _ShowAppPageState();
  }
}

class _ShowAppPageState extends State&lt;ShowAppPage&gt; {
  String title = '春天的脚步近了，我们应该更加青春有朝气';
  bool change = false;

  void _changeTextContent() {
    setState(() {
      //setState里用于刷新UI和绑定数据
      title = change ? "这个图片很好看，描述了春天的气息" : "春天的脚步近了，我们应该更加青春有朝气";
      change = !change;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('春天的气息'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: &lt;Widget&gt;[
            Padding(
              padding: EdgeInsets.all(10),
              child: Image.network(
                  'https://gss0.bdstatic.com/94o3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike272%2C5%2C5%2C272%2C90/sign=eaad8629b0096b63951456026d5aec21/342ac65c103853431b19c6279d13b07ecb8088e6.jpg'),
            ),
            // 动态绑定数据
            Padding(
              padding: EdgeInsets.all(10),
              child: Text(
                '$title',
                style: Theme.of(context).textTheme.title,
              ),
            ),

            RaisedButton(
              onPressed: _changeTextContent,
              child: Text('点击更换内容'),
            ),
          ],
        ),
      ),
    );
  }
}
</code></pre>
<p>用 flutter run 编译运行到真机或者模拟器上，运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FjG0rQbtAdMGu1uo0xWfK8JEWFQl" alt="Flutter小Demo效果" /></p>
<p>怎么样，效果是不是很好？构建这一个页面，对于其他语言可能要花费比较多的工作量，而 Flutter 构建的非常快，运行体验也很流畅。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家实践用 Flutter 搭建一个小应用 Demo，给大家一个入门的印象。俗话说熟能生巧，我们不但要理解理论知识，也需要动手实践，才能够更好地进行深入的研究和开发。建议如下：</p>
<ul>
<li>将本节课内容动手敲一遍，亲身体验 Flutter 的应用编写和运行的流畅度。</li>
<li>先了解 Flutter 的入口文件和入口函数，以及简单了解 MaterialApp、Scaffold 脚手架的概念。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>