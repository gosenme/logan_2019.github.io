---
title: Flutter：从入门到实践-40
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>之前一直在讲 Flutter 在移动端的应用尝试，今天这节内容，我们将拓展到 TV 应用的开发上来。</p>
<p>我们知道目前的智能电视和机顶盒都是基于 Android 系统的，所以一般的 TV 应用开发都是采用 Android 原生进行开发，Google 对 Android TV 的开发也进行了一些规范和库的制定。当然也有的是采用的 B/S 架构进行设计的。这里我们将尝试 Flutter 开发 TV 应用。</p>
<p>这里说明一下，选择 Flutter 开发 TV 应用这个项目既是为了我们实践的练习，也是为了知识的拓展。最终这个应用写出来了，效果也还可以，体验流畅，自动适配，不过开发成本还是挺高的，按键监听、焦点处理和焦点框处理比较麻烦，由于 Google 官方并没有推出 Flutter TV 应用的 SDK，所以建议大家在正经的开发业务中暂时不要用 Flutter 编写 TV 应用，而是建议使用原生 leanback 等库进行开发或者 B/S 结构开发。</p>
<p>接下来，就分享下其中的技术点。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter TV 应用开发主要难点</li>
  <li>Flutter TV 应用开发按键监听</li>
  <li>Flutter TV 应用开发焦点处理</li>
  <li>Flutter TV 应用开发焦点框效果处理</li>
  </ul>
</blockquote>
<p>在进行讲解前，我们先看下 Flutter TV 开发实现的效果图：</p>
<p><img src="https://images.gitbook.cn/10f44150-bd7f-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<p><img src="https://images.gitbook.cn/9079dd80-bd80-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<p><img src="https://images.gitbook.cn/b424e090-bd80-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<h3 id="fluttertv">Flutter TV 应用开发主要难点</h3>
<p>由于 Google Flutter 官方并没有推出 TV 版 Flutter SDK，所以用 Flutter尝试编写 TV 应用，主要难点是焦点框和焦点移动、焦点顺序的处理，其他的和手机应用差别不大。</p>
<p>按键监听、焦点框和焦点处理比较麻烦，所以 Flutter 的 TV 应用开发还不成熟，体验还不错，很流畅，开发成本比较高。所以这里我们只是作为研究拓展，实际开发还是要选择原生的 TV 支持库进行开发，如官方的 Leanback，或者采用 B/S 架构进行开发 TV 应用。</p>
<p>原生 Android 的控件就默认有焦点的处理属性，直接配置使用即可。还支持指定下一个焦点的 id。</p>
<pre><code class="java language-java">//焦点处理
android:focusable="true"
//触摸模式下是否可以点击，可选可不选
android:focusableInTouchMode="true"
</code></pre>
<p>Flutter开发TV应用就要自己处理按键监听、焦点和焦点框、焦点移动顺序了，比较的麻烦，处理好了这几个问题，开发起来也就没太大难度了。</p>
<p><strong>不过最新版的 Flutter 多了一个 DefaultFocusTraversal 这个类，我们可以进行指定方向自动移动焦点了，相对简单了一些。</strong></p>
<h3 id="fluttertv-1">Flutter TV 应用开发按键监听</h3>
<p>Flutter Widget 能够监听到我们的遥控器或者手机端的按键事件，前提是这个 Widget 已经获取了焦点。获取焦点后面会讲到，这里暂时不提了。而按键监听需要使用 RawKeyboardListener 这个 Widget，构造方法如下：</p>
<pre><code class="dart language-dart">const RawKeyboardListener({
    Key key,
    @required this.focusNode,//焦点结点
    @required this.onKey,//按键接收处理事件
    @required this.child,//接收焦点的子控件
  })
</code></pre>
<p>很简单给个例子：</p>
<pre><code class="dart language-dart">FocusNode focusNode0 = FocusNode();

... ...

RawKeyboardListener(
      focusNode: focusNode0,
      child: Container(
        decoration: getCircleDecoration(color0),
        child: Padding(
          child: Card(
            elevation: 5,
            shape: CircleBorder(),
            child: CircleAvatar(
              child: Text(''),
              backgroundImage: AssetImage("assets/icon_tv.png"),
              radius: radius,
            ),
          ),
          padding: EdgeInsets.all(padding),
        ),
      ),
      onKey: (RawKeyEvent event) {
        if (event is RawKeyDownEvent &amp;&amp; event.data is RawKeyEventDataAndroid) {
          RawKeyDownEvent rawKeyDownEvent = event;
          RawKeyEventDataAndroid rawKeyEventDataAndroid = rawKeyDownEvent.data;
          print("keyCode: ${rawKeyEventDataAndroid.keyCode}");
          switch (rawKeyEventDataAndroid.keyCode) {
            case 19: //KEY_UP
              FocusScope.of(context).requestFocus(_focusNode);
              break;
            case 20: //KEY_DOWN
              break;
            case 21: //KEY_LEFT
              FocusScope.of(context).requestFocus(focusNode4);
              break;
            case 22: //KEY_RIGHT
              FocusScope.of(context).requestFocus(focusNode1);
              break;
            case 23: //KEY_CENTER
              break;
            case 66: //KEY_ENTER
            break;
            default:
              break;
          }
        }
      },
    )
</code></pre>
<p>这样就实现了 Card Widget 监听我们的按键事件，遥控器、手机的按键都能监听到。</p>
<h3 id="fluttertv-2">Flutter TV 应用开发焦点处理</h3>
<p>Flutter TV 的 Widget 获取焦点的处理通过 FocusScope 这个 Widget 处理。</p>
<p>主动获取焦点代码如下：</p>
<pre><code class="dart language-dart">FocusNode focusNode0 = FocusNode();
... ...
//主动获取焦点
FocusScope.of(context).requestFocus(focusNode0);
//自动获取焦点
FocusScope.of(context).autofocus(focusNode0);
</code></pre>
<p>这样就可以进行焦点获取处理了。FocusNode 这个类也很重要，负责监听焦点的工作。</p>
<p>焦点的移动我们用最新的 <code>DefaultFocusTraversal</code> 进行自动指定方向，搜索下一个焦点：</p>
<pre><code class="dart language-dart">FocusScope.of(context)
                    .focusInDirection(TraversalDirection.up);
// 或者像下面这样使用
DefaultFocusTraversal.of(context).inDirection(
                    FocusScope.of(context).focusedChild, TraversalDirection.up);

DefaultFocusTraversal.of(context)
                    .inDirection(_focusNode, TraversalDirection.right);
</code></pre>
<p>支持上下左右四个方向。
如果想手动指定下一个焦点是哪个的话，可以像下面这样用：</p>
<pre><code class="dart language-dart">FocusScope.of(context).requestFocus(focusNode);
</code></pre>
<h3 id="fluttertv-3">Flutter TV 应用开发焦点框效果处理</h3>
<p>有了焦点、按键事件监听，剩下的就是选中的焦点框效果的实现了，主要原理这里使用的是用边框，然后动态设置边框颜色或者边框宽度、边框装饰就实现了焦点框选中显示和隐藏的效果。例如选中后焦点框颜色设置为黄色、未选中时就设置为透明色，通过 setState({...}) 进行刷新页面。</p>
<p>例如我们可以在最外层的 Container 里设置 BoxDecoration 进行边框效果的设置实现。</p>
<pre><code class="dart language-dart">var default_decoration = BoxDecoration(
    border: Border.all(width: 3, color: Colors.deepOrange),
    borderRadius: BorderRadius.all(
      Radius.circular(5),
    ));

... ...

child: Container(
          margin: EdgeInsets.all(8),
          decoration: default_decoration,
          child: widget.child,
        ));
</code></pre>
<p>最后给大家一个完整的最新的技术方案的例子代码。</p>
<p>先绘制欢迎页，效果图如下：</p>
<p><img src="https://images.gitbook.cn/5fa5a480-bd82-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<p>代码如下：</p>
<pre><code class="dart language-dart">// 启动欢迎页

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'ui/tv_page.dart';

void main() =&gt; runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SystemChrome.setEnabledSystemUIOverlays([]);
    // 强制横屏
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight
    ]);
    return MaterialApp(
      title: 'Flutter TV',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

class _MyHomePageState extends State&lt;MyHomePage&gt; {
  Timer timer;

  @override
  void initState() {
    startTimeout();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      primary: true,
      backgroundColor: Colors.black54,
      body: Center(
        child: Text(
          '芒果TV',
          style: TextStyle(
              fontSize: 50,
              color: Colors.deepOrange,
              fontWeight: FontWeight.normal),
        ),
      ),
    );
  }

  _toPage() {
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) =&gt; TVPage()),
      (route) =&gt; route == null,
    );
  }

  //倒计时处理
  static const timeout = const Duration(seconds: 3);

  startTimeout() {
    timer = Timer(timeout, handleTimeout);
    return timer;
  }

  void handleTimeout() {
    _toPage();
  }

  @override
  void dispose() {
    if (timer != null) {
      timer.cancel();
      timer = null;
    }
    super.dispose();
  }
}
</code></pre>
<p>应用首页，效果图如下：</p>
<p><img src="https://images.gitbook.cn/71473140-bd82-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<p>代码如下：</p>
<pre><code class="dart language-dart">// 应用首页
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tv/utils/time_utils.dart';
import 'package:flutter_tv/widgets/tv_widget.dart';

import 'home_page.dart';
import 'list_page.dart';

class TVPage extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    SystemChrome.setEnabledSystemUIOverlays([]);
    // 强制横屏
    SystemChrome.setPreferredOrientations(
        [DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight]);
    return TVPageState();
  }
}

class TVPageState extends State&lt;TVPage&gt; with SingleTickerProviderStateMixin {
  TabController _tabController;
  Timer timer;
  var timeString = TimeUtils.getTime();

  bool init = false;
  FocusNode focusNodeB0 = FocusNode();
  FocusNode focusNodeB1 = FocusNode();

  @override
  void initState() {
    super.initState();
    //initialIndex为初始选中第几个，length为数量
    _tabController = TabController(initialIndex: 0, length: 8, vsync: this);
    // 监听
    _tabController.addListener(() {
      switch (_tabController.index) {
        case 0:
          break;
        case 1:
          break;
      }
    });

    focusNodeB0.addListener(() {
      if (focusNodeB0.hasFocus) {
        setState(() {
          _tabController.animateTo(0);
        });
      }
    });
    focusNodeB1.addListener(() {
      if (focusNodeB1.hasFocus) {
        setState(() {
          _tabController.animateTo(1);
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black87,
      padding: EdgeInsets.all(30),
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.black87,
          leading: Icon(
            Icons.live_tv,
            color: Colors.deepOrange,
            size: 50,
          ),
          title: Text(
            '芒果TV',
            style: TextStyle(
                fontSize: 30, color: Colors.white, fontStyle: FontStyle.italic),
          ),
          primary: true,
          actions: &lt;Widget&gt;[
            FlatButton(
              child: Text(
                '$timeString',
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
          // 设置TabBar
          bottom: TabBar(
            controller: _tabController,
            indicatorColor: Colors.deepOrange,
            labelColor: Colors.deepOrange,
            unselectedLabelColor: Colors.white,
            tabs: &lt;Widget&gt;[
              Tab(
                child: TVWidget(
                  hasDecoration: false,
                  focusChange: (hasFocus) {
                    if (hasFocus) {
                      setState(() {
                        _tabController.animateTo(0);
                      });
                    }
                  },
                  child: Text(
                    '首页',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  requestFocus: true,
                ),
              ),
              Tab(
                  child: TVWidget(
                hasDecoration: false,
                focusChange: (hasFocus) {
                  if (hasFocus) {
                    setState(() {
                      _tabController.animateTo(1);
                    });
                  }
                },
                child: Text(
                  '精选',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              )),
              Tab(
                  child: TVWidget(
                hasDecoration: false,
                focusChange: (hasFocus) {
                  if (hasFocus) {
                    setState(() {
                      _tabController.animateTo(2);
                    });
                  }
                },
                onclick: () {
                  print("点击");
                },
                child: Text(
                  '国产',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              )),
              Tab(
                  child: TVWidget(
                hasDecoration: false,
                focusChange: (hasFocus) {
                  if (hasFocus) {
                    setState(() {
                      _tabController.animateTo(3);
                    });
                  }
                },
                child: Text(
                  '欧美',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              )),
              Tab(
                child: TVWidget(
                  hasDecoration: false,
                  focusChange: (hasFocus) {
                    if (hasFocus) {
                      setState(() {
                        _tabController.animateTo(4);
                      });
                    }
                  },
                  child: Text(
                    '日漫',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              Tab(
                child: TVWidget(
                  hasDecoration: false,
                  focusChange: (hasFocus) {
                    if (hasFocus) {
                      setState(() {
                        _tabController.animateTo(5);
                      });
                    }
                  },
                  child: Text(
                    '亲子',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              Tab(
                child: TVWidget(
                  hasDecoration: false,
                  focusChange: (hasFocus) {
                    if (hasFocus) {
                      setState(() {
                        _tabController.animateTo(6);
                      });
                    }
                  },
                  child: Text(
                    '少综',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              Tab(
                child: TVWidget(
                  focusChange: (hasFocus) {
                    if (hasFocus) {
                      setState(() {
                        _tabController.animateTo(7);
                      });
                    }
                  },
                  hasDecoration: false,
                  child: Text(
                    '分类',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
        ),
        body: TabBarView(
          controller: _tabController,
          children: &lt;Widget&gt;[
            HomePage(),
            ListPage(),
            HomePage(),
            ListPage(),
            HomePage(),
            ListPage(),
            HomePage(),
            ListPage(),
          ],
        ),
      ),
    );
  }

  startTimeout() {
    timer = Timer.periodic(Duration(minutes: 1), (t) {
      setState(() {
        timeString = TimeUtils.getTime();
      });
    });
  }

  @override
  void dispose() {
    if (timer != null) {
      timer.cancel();
      timer == null;
    }
    super.dispose();
  }
}


// TAB页面中的其中一个页面，其他类似
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_tv/widgets/tv_widget.dart';

class HomePage extends StatefulWidget {
  const HomePage({
    Key key,
    @required this.index,
  }) : super(key: key);

  final int index;

  @override
  State&lt;StatefulWidget&gt; createState() {
    return HomePageState();
  }
}

class HomePageState extends State&lt;HomePage&gt; with AutomaticKeepAliveClientMixin {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black87,
      child: Row(
        children: &lt;Widget&gt;[
          Flexible(
            child: Column(
              children: &lt;Widget&gt;[
                _buildItem(0),
                _buildItem(1),
                _buildItem(2),
              ],
            ),
            flex: 1,
          ),
          Flexible(
            child: Column(
              children: &lt;Widget&gt;[
                _buildImageItem(3, 2),
                Expanded(
                    flex: 1,
                    child: Row(
                      children: &lt;Widget&gt;[
                        _buildImageItem(4, 1),
                        _buildImageItem(5, 1),
                      ],
                    )),
              ],
            ),
            flex: 4,
          ),
          Flexible(
            child: Column(
              children: &lt;Widget&gt;[
                _buildImageItem(6, 2),
                _buildImageItem(7, 1),
              ],
            ),
            flex: 2,
          ),
          Flexible(
            child: Column(
              children: &lt;Widget&gt;[
                _buildImageItem(8, 2),
                _buildImageItem(9, 1),
              ],
            ),
            flex: 2,
          ),
        ],
      ),
    );
  }

  _buildItem(int index) {
    return Expanded(
      child: TVWidget(
          focusChange: (hasfocus) {},
          child: Container(
            width: MediaQuery.of(context).size.width,
            child: GestureDetector(
              child: Card(
                elevation: 5,
                margin: EdgeInsets.all(0),
                color: _colors.elementAt(index),
                child: Container(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: &lt;Widget&gt;[
                      _icons.elementAt(index),
                      _title.elementAt(index),
                    ],
                  ),
                ),
              ),
              onTap: () {
                _click(index);
              },
            ),
          )),
      flex: 1,
    );
  }

  _buildImageItem(int index, int flex) {
    return Expanded(
      child: TVWidget(
        child: Container(
          width: MediaQuery.of(context).size.width,
          child: GestureDetector(
            child: Card(
              elevation: 5,
              margin: EdgeInsets.all(0),
              color: _colors.elementAt(index),
              child: Container(
                child: Stack(
                  alignment: Alignment.bottomLeft,
                  children: &lt;Widget&gt;[
                    ClipRRect(
                      child: Image.asset(
                        _images.elementAt(index),
                        fit: BoxFit.fill,
                        width: MediaQuery.of(context).size.width,
                        height: MediaQuery.of(context).size.height,
                      ),
                      borderRadius: BorderRadius.all(
                        Radius.circular(5),
                      ),
                    ),
                    Container(
                      width: MediaQuery.of(context).size.width,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: &lt;Widget&gt;[
                          _title.elementAt(index),
                          index == 3
                              ? _des.elementAt(index)
                              : SizedBox(
                                  height: 0,
                                ),
                        ],
                      ),
                      color: _colors.elementAt(index).withAlpha(240),
                      padding: EdgeInsets.all(5),
                    ),
                  ],
                ),
              ),
            ),
            onTap: () {
              _click(index);
            },
          ),
        ),
        focusChange: (hasfocus) {},
      ),
      flex: flex,
    );
  }

  void _click(int index) {
    switch (index) {
      case 0:
        break;
      case 4:
//        Navigator.push(context, MaterialPageRoute(builder: (context) {
//          return AboutPage();
//        }));
        break;
    }
  }

  List&lt;Icon&gt; _icons = [
    Icon(
      Icons.search,
      size: 38,
      color: Colors.white,
    ),
    Icon(
      Icons.history,
      size: 38,
      color: Colors.white,
    ),
    Icon(
      Icons.event,
      size: 38,
      color: Colors.white,
    ),
    Icon(
      Icons.share,
      size: 38,
      color: Colors.deepPurpleAccent,
    ),
    Icon(
      Icons.error_outline,
      size: 38,
      color: Colors.orange,
    ),
    Icon(
      Icons.settings,
      size: 38,
      color: Colors.red,
    )
  ];

  List&lt;String&gt; _images = [
    'assets/htpy.jpg',
    'assets/htpy.jpg',
    'assets/htpy.jpg',
    'assets/htpy.jpg',
    'assets/agzz.jpg',
    'assets/amypj.jpg',
    'assets/hmjz.jpg',
    'assets/dxflqm.jpg',
    'assets/lifeandpi.jpg',
    'assets/nanasqc.jpg',
  ];

  List&lt;Color&gt; _colors = [
    Colors.red,
    Colors.orange,
    Colors.green,
    Colors.red,
    Colors.orange,
    Colors.green,
    Colors.orange,
    Colors.orange,
    Colors.orange,
    Colors.orange,
  ];

  List&lt;Text&gt; _title = [
    Text(
      "搜索",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "历史",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "专题",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "环太平洋",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "阿甘正传",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "傲慢与偏见",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "黑猫警长",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "当幸福来敲门",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "Life Or PI",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
    Text(
      "哪啊哪啊神去村",
      style: TextStyle(color: Colors.white, fontSize: 18),
    ),
  ];

  List&lt;Text&gt; _des = [
    Text(
      "非常好看的电影",
      style: TextStyle(color: Colors.white, fontSize: 12),
    ),
    Text(
      "设置密码锁",
      style: TextStyle(color: Colors.white, fontSize: 12),
    ),
    Text(
      "吐槽反馈你的想法",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "非常好看的电影",
      style: TextStyle(color: Colors.white, fontSize: 12),
    ),
    Text(
      "版本信息",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "系统相关设置",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "系统相关设置",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
  ];

  @override
  // TODO: implement wantKeepAlive
  bool get wantKeepAlive =&gt; true;
}
</code></pre>
<p>封装的核心类：</p>
<pre><code class="dart language-dart">// 封装的核心焦点处理类

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

class TVWidget extends StatefulWidget {
  TVWidget(
      {Key key,
      @required this.child,
      @required this.focusChange,
      @required this.onclick,
      @required this.decoration,
      @required this.hasDecoration = true,
      @required this.requestFocus = false})
      : super(key: key);

  Widget child;
  onFocusChange focusChange;
  onClick onclick;
  bool requestFocus;
  BoxDecoration decoration;
  bool hasDecoration;

  @override
  State&lt;StatefulWidget&gt; createState() {
    return TVWidgetState();
  }
}

typedef void onFocusChange(bool hasFocus);
typedef void onClick();

class TVWidgetState extends State&lt;TVWidget&gt; {
  FocusNode _focusNode;
  bool init = false;
  var default_decoration = BoxDecoration(
      border: Border.all(width: 3, color: Colors.deepOrange),
      borderRadius: BorderRadius.all(
        Radius.circular(5),
      ));
  var decoration = null;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(() {
      if (widget.focusChange != null) {
        widget.focusChange(_focusNode.hasFocus);
      }
      if (_focusNode.hasFocus) {
        setState(() {
          if (widget.hasDecoration) {
            decoration = widget.decoration == null
                ? default_decoration
                : widget.decoration;
          }
        });
      } else {
        setState(() {
          decoration = null;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (widget.requestFocus &amp;&amp; !init) {
      FocusScope.of(context).requestFocus(_focusNode);
      init = true;
    }
    return RawKeyboardListener(
        focusNode: _focusNode,
        onKey: (event) {
          if (event is RawKeyDownEvent &amp;&amp;
              event.data is RawKeyEventDataAndroid) {
            RawKeyDownEvent rawKeyDownEvent = event;
            RawKeyEventDataAndroid rawKeyEventDataAndroid =
                rawKeyDownEvent.data;
            print("keyCode: ${rawKeyEventDataAndroid.keyCode}");
            switch (rawKeyEventDataAndroid.keyCode) {
              case 19: //KEY_UP
//                DefaultFocusTraversal.of(context).inDirection(
//                    FocusScope.of(context).focusedChild, TraversalDirection.up);
                FocusScope.of(context)
                    .focusInDirection(TraversalDirection.up);
                break;
              case 20: //KEY_DOWN
                FocusScope.of(context)
                    .focusInDirection(TraversalDirection.down);
                break;
              case 21: //KEY_LEFT
//                            FocusScope.of(context).requestFocus(focusNodeB0);
                FocusScope.of(context)
                    .focusInDirection(TraversalDirection.left);
                // 手动指定下一个焦点
               // FocusScope.of(context).requestFocus(focusNode);
                break;
              case 22: //KEY_RIGHT
//                            FocusScope.of(context).requestFocus(focusNodeB1);
                FocusScope.of(context)
                    .focusInDirection(TraversalDirection.right);
//                DefaultFocusTraversal.of(context)
//                    .inDirection(_focusNode, TraversalDirection.right);
//                if(_focusNode.nextFocus()){
//                  FocusScope.of(context)
//                      .focusInDirection(TraversalDirection.right);
//                }
                break;
              case 23: //KEY_CENTER
                widget.onclick();
                break;
              case 66: //KEY_ENTER
                widget.onclick();
                break;
              default:
                break;
            }
          }
        },
        child: Container(
          margin: EdgeInsets.all(8),
          decoration: decoration,
          child: widget.child,
        ));
  }
}
</code></pre>
<p><img src="https://images.gitbook.cn/bb19d020-bd82-11e9-bb40-bd92c8f37632" alt="运行效果" /></p>
<p>关于 Flutter TV 开发就讲解这么多。</p>
<p>在前面实现过一个比较旧的版本的 Flutter TV 开发，Github 项目地址：</p>
<p><a href="https://github.com/flutteranddart/flutterTV">flutterTV</a></p>
<p>新版的技术方案的 Flutter TV 的 Github 地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_tv">flutter<em>tv</em>new</a></p>
<p>新版的技术方案里面有些细节约束处理并没有仔细处理，细节大家可以进行自己处理下，后续也会更新完善。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter TV 的应用开发，拓展一下思路和技术方向，通过完整的案例来巩固和检查之前所学到的这些内容，这节课的内容很新颖，所以大家可以学习一下里面的技术方案。主要注意点和建议如下：</p>
<ul>
<li>熟练掌握这里面涉及到技术点的解决方案，例如按键监听、焦点处理。</li>
<li>将本节课内容动手敲一遍，然后对比新的技术方案和旧的版本的技术方案的差别，并整理总结下。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>