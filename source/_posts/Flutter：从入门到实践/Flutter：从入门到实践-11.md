---
title: Flutter：从入门到实践-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面讲解了 Flutter 的几个基础组件，这节课将继续讲解 Flutter 的基础组件——AppBar、AlertDialog 和 Icon，这些基础组件都不是很难，但是算是比较常用的，分别对应到界面的就是标题栏、弹窗对话框、图标。那么就开始吧！</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>AppBar Widget 用法详解</li>
  <li>AlertDialog Widget 用法详解</li>
  <li>Icon Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="1appbarwidget">1 AppBar Widget 用法详解</h3>
<p>AppBar 是页面的顶部标题栏，里面可以定制各种按钮、菜单等，一般配合 Scaffold 使用。大致效果如下图：</p>
<p><img src="https://images.gitbook.cn/FtnbmK9GapZz-PnlTZRqeL0o4njL" alt="Appbar" /></p>
<p>这个效果图里显示了基本上 AppBar 的所有用法。AppBar 是一个 StatefulWidget，我们先看下它的构造方法：</p>
<pre><code class="dart language-dart">AppBar({
    Key key,
    // 标题栏最左侧图标，首页一般默认显示logo，其它页面默认显示返回按钮，可以自定义
    this.leading,
    // 是否提供控件占位
    this.automaticallyImplyLeading = true,
    // 标题内容
    this.title,
    // 标题栏上右侧的菜单，可以用IconButton显示，也可以用PopupMenuButton显示为三个点
    this.actions,
    // AppBar下方的控件，高度和AppBar高度一样，通常在SliverAppBar中使用
    this.flexibleSpace,
    // 标题栏下方的空间，一般放TabBar
    this.bottom,
    // 控制标题栏阴影大小
    this.elevation,
    // 标题栏背景色
    this.backgroundColor,
    // 亮度，有白色和黑色两种主题
    this.brightness,
    // AppBar上图标的颜色、透明度、和尺寸信息
    this.iconTheme,
    // AppBar上的文字样式
    this.textTheme,
    // 是否进入到状态栏
    this.primary = true,
    // 标题是否居中
    this.centerTitle,
    // 标题间距，如果希望title占用所有可用空间，请将此值设置为0.0
    this.titleSpacing = NavigationToolbar.kMiddleSpacing,
    // 透明度
    this.toolbarOpacity = 1.0,
    this.bottomOpacity = 1.0,
  })
</code></pre>
<p>我们看一个最简单的用法：</p>
<pre><code class="dart language-dart"> AppBar(
   title: Text('My Fancy Dress'),
   actions: &lt;Widget&gt;[
     IconButton(
       icon: Icon(Icons.playlist_play),
       tooltip: 'Air it',
       onPressed: _airDress,
     ),
     IconButton(
       icon: Icon(Icons.playlist_add),
       tooltip: 'Restitch it',
       onPressed: _restitchDress,
     ),
     IconButton(
       icon: Icon(Icons.playlist_add_check),
       tooltip: 'Repair it',
       onPressed: _repairDress,
     ),
   ],
 )
</code></pre>
<p>运行效果：</p>
<p><img src="https://images.gitbook.cn/FlUq0atfICpG6Z8NF7MNVvgIMWXR" alt="Appbar" /></p>
<p>使用起来很简单，很方便。接下来看一个比较复杂的实例：</p>
<pre><code class="dart language-dart">class AppbarSamplesState extends State&lt;AppbarSamples&gt;
    with SingleTickerProviderStateMixin {
  TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(initialIndex: 0, length: 5, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('AppBar Widget'),
        primary: true,
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () {
            Scaffold.of(context).openDrawer();
          },
        ),
        actions: &lt;Widget&gt;[
          IconButton(icon: Icon(Icons.share), onPressed: () {}),
          IconButton(icon: Icon(Icons.add), onPressed: () {}),
          PopupMenuButton(
            itemBuilder: (BuildContext context) =&gt; &lt;PopupMenuItem&lt;String&gt;&gt;[
                  PopupMenuItem&lt;String&gt;(
                    child: Text("热度"),
                    value: "hot",
                  ),
                  PopupMenuItem&lt;String&gt;(
                    child: Text("最新"),
                    value: "new",
                  ),
                ],
            onSelected: (String action) {
              switch (action) {
                case "hot":
                  print("hot");
                  break;
                case "new":
                  print("new");
                  break;
              }
            },
            onCanceled: () {
              print("onCanceled");
            },
          )
        ],
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: &lt;Widget&gt;[
            Tab(
              text: "Tab1",
              icon: Icon(Icons.battery_full),
            ),
            Tab(
              text: "Tab2",
              icon: Icon(Icons.add),
            ),
            Tab(
              text: "Tab3",
              icon: Icon(Icons.card_giftcard),
            ),
            Tab(
              text: "Tab4",
              icon: Icon(Icons.shop),
            ),
            Tab(
              text: "Tab5",
              icon: Icon(Icons.directions_bike),
            ),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: &lt;Widget&gt;[
          Center(
            child: Text("data1"),
          ),
          Center(
            child: Text("data2"),
          ),
          Center(
            child: Text("data3"),
          ),
          Center(
            child: Text("data4"),
          ),
          Center(
            child: Text("data5"),
          ),
        ],
      ),
    );
  }
}
</code></pre>
<p>这段实例就是前面的图片的效果，运行效果：</p>
<p><img src="https://images.gitbook.cn/FtnbmK9GapZz-PnlTZRqeL0o4njL" alt="Appbar" /></p>
<h3 id="2alertdialogwidget">2 AlertDialog Widget 用法详解</h3>
<p>AlertDialog Widget 也是一个比较常用的组件，主要是实现对话框效果。Flutter 中 dialog 一般分为：AlertDialog（用于警告提示对话框）、SimpleDialog（有列表选项的对话框）、CupertinoAlertDialog（iOS 风格的 alert dialog）、CupertinoDialog（iOS 风格的对话框）。</p>
<p>我们看下这几种效果图。</p>
<p>AlertDialog：</p>
<p><img src="https://images.gitbook.cn/FnRnzoNF18v_b6FIIyBUhxjayxjF" alt="AlertDialog" /></p>
<p>SimpleDialog：</p>
<p><img src="https://images.gitbook.cn/FubpTXKDWjzzMfPaGEtE-QKOm23Y" alt="SimpleDialog" /></p>
<p>CupertinoDialog：</p>
<p><img src="https://images.gitbook.cn/Fsbhm9LvKlk5PQmCBOB4alCHfa_O" alt="CupertinoDialog" /></p>
<p>再看下弹出对话框的方法，Flutter 自带这几个弹出对话框方法。</p>
<ul>
<li>showDialog：弹出 Material 风格对话框</li>
<li>showCupertinoDialog：弹出 iOS 样式对话框</li>
<li>showGeneralDialog：弹出自定义的对话框，默认状态下弹出的窗口点击空白处不消失</li>
<li>showAboutDialog：弹出关于页面适用的对话框</li>
</ul>
<p>接下来直接给实例看下使用方法。</p>
<pre><code class="dart language-dart">enum Option { A, B, C }
enum Location { Barbados, Bahamas, Bermuda }

// AlertDialog
  Future&lt;void&gt; dialog1(BuildContext context) async {
    return showDialog&lt;void&gt;(
        context: context,
        // 点击周围空白区域对话框是否消失
        barrierDismissible: false,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text("提示"),
            content: new Text("是否退出"),
            actions: &lt;Widget&gt;[
              new FlatButton(
                  onPressed: () =&gt; Navigator.of(context).pop(false),
                  child: new Text("取消")),
              new FlatButton(
                  onPressed: () {
                    Navigator.of(context).pop(true);
                  },
                  child: new Text("确定"))
            ],
          );
        });
  }

// AlertDialog
  Future&lt;void&gt; officialDialog2(BuildContext context) async {
    return showDialog&lt;void&gt;(
      context: context,
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Rewind and remember'),
          content: SingleChildScrollView(
            child: ListBody(
              children: &lt;Widget&gt;[
                Text('You will never be satisfied.'),
                Text('You\’re like me. I’m never satisfied.'),
              ],
            ),
          ),
          actions: &lt;Widget&gt;[
            FlatButton(
              child: Text('Regret'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

// SimpleDialog
  Future&lt;void&gt; dialog3(BuildContext context) async {
    return showDialog&lt;void&gt;(
        context: context,
        barrierDismissible: false,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: Text("提示"),
          );
        });
  }

// SimpleDialog
  Future&lt;void&gt; dialog4(BuildContext context) async {
    switch (await showDialog&lt;Option&gt;(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: const Text('Select Answer'),
            children: &lt;Widget&gt;[
              SimpleDialogOption(
                onPressed: () {
                  Navigator.pop(context, Option.A);
                },
                child: const Text('A'),
              ),
              SimpleDialogOption(
                onPressed: () {
                  Navigator.pop(context, Option.B);
                },
                child: const Text('B'),
              ),
              SimpleDialogOption(
                onPressed: () {
                  Navigator.pop(context, Option.C);
                },
                child: const Text('C'),
              ),
            ],
          );
        })) {
      case Option.A:
        // Let's go.
        // ...
        print('A');
        break;
      case Option.B:
        // ...
        print('B');
        break;
      case Option.C:
        // ...
        print('C');
        break;
    }
  }

// 自定义Dialog
  Future&lt;void&gt; dialog5(BuildContext context) async {
    return showDialog&lt;void&gt;(
        context: context,
        builder: (BuildContext context) {
          return LoadingDialog(text: '正在加载...');
        });
  }

// AboutDialog
  Future&lt;void&gt; dialog6(BuildContext context) async {
    return showAboutDialog(
        context: context,
        applicationName: "应用名称",
        applicationVersion: "1.0.0",
        applicationIcon: Icon(Icons.apps),
        applicationLegalese: "内容");
  }
}
</code></pre>
<p>运行效果图：</p>
<p><img src="https://images.gitbook.cn/FisLKb11YRv2ykIOVX_eJ0U2FpN6" alt="Dialog" /></p>
<p><img src="https://images.gitbook.cn/FmYQ3TrLk5vOBtnBoYsJuL-jZF3P" alt="Dialog" /></p>
<h3 id="3iconwidget">3 Icon Widget 用法详解</h3>
<p>Icon Widget 主要是用来显示图标相关的操作，很常用，也很简单。Flutter Icon 也可以使用 unicode、矢量图标、iconfont 里的图标、Flutter 自带的 Material 图标（需要在 pubspec.yaml 中配置开启）。</p>
<pre><code class="dart language-dart">// 配置这句就可以使用Material风格内置的Icons了
flutter:

  uses-material-design: true
</code></pre>
<p>Material 风格图标使用通过 Icons. 来调用，如 Icons.add，这样就可以使用加号图标了。Flutter 的 Icon 也封装了ImageIcon、IconButton 来提供使用。</p>
<p>Material Design 所有图标可以在官网查看：https://material.io/tools/icons/</p>
<p><img src="https://images.gitbook.cn/FtVVHHpqNsWOi1pYu213KNH2a97F" alt="Material Design Icon" /></p>
<p>使用 Icon 有以下好处：</p>
<ul>
<li>体积小：可以减小应用安装包体积</li>
<li>矢量：iconfont 和自带的 Material 图标都是矢量图标，即使放大也不会影像图标清晰度</li>
<li>可以动态改变颜色、大小：由于是 PNG 有透明度图标，可以改变图标的颜色、大小、对齐等</li>
<li>可以像表情一样通过 TextSpan 和文本混用展示</li>
</ul>
<p>Icon 是属于 StatelessWidget，我们看下构造方法：</p>
<pre><code class="dart language-dart">const Icon(this.icon, {
    Key key,
    // 图标大小，默认为24px
    this.size,
    // 图标颜色
    this.color,
    this.semanticLabel,
    // 渲染图标的方向，前提需要IconData.matchTextDirection字段设置为true
    this.textDirection,
  })
</code></pre>
<p>接下来我们看一个实例：</p>
<pre><code class="dart language-dart">class IconSamplesState extends State&lt;IconSamples&gt;
    with TickerProviderStateMixin {
  AnimationController _controller;

  @override
  void initState() {
    super.initState();

    ///动画控制类，产生0-1之间小数
    _controller = AnimationController(
        lowerBound: 0,
        upperBound: 1,
        duration: const Duration(seconds: 3),
        vsync: this);
        _controller.forward();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Icon Widget'),
        primary: true,
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () {},
        ),
      ),
      body: Column(
        children: &lt;Widget&gt;[
          IconButton(
            icon: Icon(Icons.directions_bike),
            // 按钮处于按下状态时按钮的主要颜色
            splashColor: Colors.teal,
            // 按钮处于按下状态时按钮的辅助颜色
            highlightColor: Colors.pink,
            // 不可点击时颜色
            disabledColor: Colors.grey,
            // PNG图标主体颜色
            color: Colors.orange,
            onPressed: () {},
          ),
          // 图片PNG格式，有透明度
          ImageIcon(
            AssetImage('assets/check-circle.png'),
            color: Colors.teal,
            size: 30,
          ),
          Icon(
            Icons.card_giftcard,
            size: 26,
          ),
          // 使用unicode
          Text(
            "\uE000",
            style: TextStyle(
                fontFamily: "MaterialIcons",
                fontSize: 24.0,
                color: Colors.green),
          ),
          Icon(IconData(0xe614,
              // 也可以使用自己自定义字体
              fontFamily: "MaterialIcons",
              matchTextDirection: true)),
          AnimatedIcon(
            icon: AnimatedIcons.menu_arrow,
            progress: _controller,
            semanticLabel: 'Show menu',
          )
        ],
      ),
    );
  }
}
</code></pre>
<p>运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/FsXjqogUt9c3XJElnRGo2ysmKgst" alt="Icon" /></p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_10">flutter_10</a></p>
<h3 id="">总结</h3>
<p>本节课讲解的几个基础 Widget：AppBar、AlertDialog、Icon 很常用也很简单。</p>
<p>Icon 非常常用，也非常有意思，可以尝试自己用 Text、TextSpan 显示图标和文字混排的效果。</p></div></article>