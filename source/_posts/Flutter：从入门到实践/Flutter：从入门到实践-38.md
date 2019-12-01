---
title: Flutter：从入门到实践-38
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>经过前面三大部分内容知识点的讲解，相信大家对大部分的布局方式、组件的使用、逻辑业务编写都有了一定的了解了。到这里，我们基本上关于 Flutter 的开发课程的内容就说的差不多了。那么接下来我们就用前面学习的一些知识来进行一个完整的实践：实现一个简易日记本应用。通过这个实例我们可以复习巩固我们之前学过的知识，也算是一个总结与检验。本节作为练习篇，主要用到组件、自定义组件、常用布局、插件等知识点来完成一个简易日记本应用，一起来实践吧。</p>
<h3 id="">知识整理</h3>
<p>本篇练习看似简单，但是已经将应用编写的大部分需要用的功能都贯穿起来进行了实践、并提供了比较好的解决方案，将开发中可能会遇到的很多问题和难点进行了一一解决。</p>
<p>在进行综合实践编写前，我们先整理下我们这节课里用到的一些知识点：</p>
<ul>
<li>引导页（PageView）</li>
<li>顶部 ToolBar（AppBar）</li>
<li>列表（CustomScrollView）</li>
<li>日历（三方库：flutter<em>custom</em>calendar）</li>
<li>权重（Flexible、Expanded）</li>
<li>导航组件（CupertinoTabBar）</li>
<li>弹窗（BottomSheet、SnackBar）</li>
<li>输入框（TextField）</li>
<li>通信（EventBut）</li>
<li>路由</li>
<li>下拉刷新（RefreshIndicator）</li>
<li>数据库（官方库：sqflite）</li>
<li>时间格式化</li>
<li>生命周期监听</li>
<li>返回键拦截</li>
<li>List 的操作</li>
<li>复杂布局实现</li>
<li>其他</li>
</ul>
<p>那么我们这节综合实践课，就通过以上我们学过的一些 Widget 和技术进行实现一个完整的日记本应用，过程不复杂，但是可以检验一下我们的开发实战水平。</p>
<h3 id="-1">应用编写目标</h3>
<p>本节课将要实现的日记本应用，效果图和功能展示如下：</p>
<p><strong>完整实践：实现一个简易日记本应用</strong></p>
<p><img src="https://images.gitbook.cn/078e48b0-b9c2-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p>静态效果图：</p>
<p><img src="https://images.gitbook.cn/cd760000-b9c1-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/0b19f590-b9c4-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/e809bdd0-b9c1-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/f28fae40-b9c1-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/07f93f80-b9c2-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/8f5f8040-b9c4-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/24658de0-b9c2-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/2d476b40-b9c2-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p><img src="https://images.gitbook.cn/37785de0-b9c2-11e9-86fb-d93f58d85bd7" alt="实践篇效果图" /></p>
<p>我们先简单介绍下我们要实现的应用的功能：
日记本有引导页，具备列表显示功能、日记的新建、查看阅读、编辑功能，并加入了搜索功能。日记的数据存储的本地手机数据库内，提供3个页面进行切换。</p>
<p>1.首先是引导页：引导页作为应用的一个基本的功能，会为大家实现并提供解决方案。
2.应用页面基本框架：包括一个底部导航栏，带三个页面切换，并在切换时保持页面数据状态。
3.日记的增删改查功能：存储在手机自带数据库中。
4.日记的搜索功能。
5.关于页面。
6.列表时时通知更新功能。
7.复制剪贴板功能等。</p>
<p>由于功能比较完善、比较多，所以这里就挑选比较常见和重要的技术点来进行代码讲解。其他的完整项目可以在 Github 上进行下载编译、查看学习：</p>
<p><a href="https://github.com/jaychou2012/flutter_notes">flutter_notes</a></p>
<p>项目的 dart 代码结构如下：</p>
<p><img src="https://images.gitbook.cn/61943e50-b9c2-11e9-86fb-d93f58d85bd7" alt="dart代码结构" /></p>
<p>使用到的第三方库如下：</p>
<ul>
<li>sqflite：数据库操作</li>
<li>path_provider：目录路径的读取</li>
<li>oktoast：实现 Toast 提示</li>
<li>event_bus：通信</li>
<li><code>flutter_custom_calendar</code>：日历功能</li>
</ul>
<pre><code class="dart language-dart">dependencies:
  flutter:
    sdk: flutter
  sqflite: ^1.1.6+3
  cupertino_icons: ^0.1.2
  path_provider: ^1.1.0
  oktoast: ^2.2.0
  event_bus: ^1.1.0
  flutter_custom_calendar:
    git:
      url: https://github.com/LXD312569496/flutter_custom_calendar.git
</code></pre>
<p>接下来我们针对一些主要的功能进行代码演示讲解。</p>
<p>具体实现代码如下：</p>
<pre><code class="dart language-dart">// 首先我们看下引导页的实现
// 引导页我们主要使用PageView来实现

import 'package:flutter/material.dart';
import 'package:oktoast/oktoast.dart';
import 'ui/Home.dart';

void main() {
  runApp(MyApp());
  // 透明状态栏
//  if (Platform.isAndroid) {
//    SystemUiOverlayStyle systemUiOverlayStyle =
//        SystemUiOverlayStyle(statusBarColor: Colors.transparent);
//    SystemChrome.setSystemUIOverlayStyle(systemUiOverlayStyle);
//  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
      // Toast三方库包裹最外层
    return OKToast(
        child:
        MaterialApp(
          title: '日记本',
          theme: ThemeData(
            primarySwatch: Colors.grey,
          ),
          home: MyHomePage(),
        ),
        backgroundColor: Colors.black54,
        textPadding:
            const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10.0),
        radius: 20.0,
        position: ToastPosition.bottom);
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

class _MyHomePageState extends State&lt;MyHomePage&gt; {
  // 默认选中第一项
  int _selectedIndex = 0;
  var _pageController = new PageController(initialPage: 0);

  @override
  void initState() {
    super.initState();
    _pageController.addListener(() {
      print(_pageController.position);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _buildBody(),
    );
  }
  // 构建页面主体
  _buildBody() {
    //SafeArea包裹，保证不会在刘海屏等屏幕下出现裁剪、适配
    return SafeArea(
        child: Stack(
      children: &lt;Widget&gt;[
          // PageView实现引导页页面切换
        PageView(
          // 监听控制类
          controller: _pageController,
          onPageChanged: _onSelectChanged,
          children: &lt;Widget&gt;[
              // 引导页第一个页面
            Container(
              color: Color.fromRGBO(232, 229, 222, 1),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: &lt;Widget&gt;[
                  Text(
                    '每一天都是电影',
                    style: TextStyle(
                        color: Color.fromRGBO(132, 112, 101, 1), fontSize: 22),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  Text(
                    '记录精彩的生活，让每一天都有所回忆',
                    style: TextStyle(
                        color: Color.fromRGBO(66, 84, 94, 1), fontSize: 20),
                  )
                ],
              ),
            ),
            // 引导页第二个页面
            Container(
              color: Color.fromRGBO(232, 229, 222, 1),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: &lt;Widget&gt;[
                  Text(
                    '简约至尚',
                    style: TextStyle(
                        color: Color.fromRGBO(72, 186, 249, 1), fontSize: 22),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  Text(
                    '从内到外力求简约、精美、个性......',
                    style: TextStyle(
                        color: Color.fromRGBO(66, 84, 94, 1), fontSize: 20),
                  )
                ],
              ),
            ),
            // 引导页第三个页面
            Container(
              color: Color.fromRGBO(232, 229, 222, 1),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: &lt;Widget&gt;[
                  Text(
                    '此刻，回忆独一无二',
                    style: TextStyle(
                        color: Color.fromRGBO(98, 95, 78, 1), fontSize: 22),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  InkWell(
                    onTap: () {
                      toPage();
                    },
                    child: Text(
                      '开始体验之旅&gt;&gt;',
                      style: TextStyle(
                          color: Color.fromRGBO(66, 84, 94, 1), fontSize: 20),
                    ),
                  )
                ],
              ),
            ),
          ],
        ),
        // 绘制引导页的三个圆点指示器
        Align(
          alignment: FractionalOffset.bottomCenter,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: &lt;Widget&gt;[
              Container(
                  width: 10,
                  height: 10,
                  margin: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: (_selectedIndex == 0)
                          ? Colors.white70
                          : Colors.black12)),
              Container(
                  width: 10,
                  height: 10,
                  margin: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: (_selectedIndex == 1)
                          ? Colors.white70
                          : Colors.black12)),
              Container(
                  width: 10,
                  height: 10,
                  margin: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: (_selectedIndex == 2)
                          ? Colors.white70
                          : Colors.black12))
            ],
          ),
        )
      ],
    ));
  }

  void _onSelectChanged(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  // 切换
  void setPageViewItemSelect(int indexSelect) {
    _pageController.animateToPage(indexSelect,
        duration: const Duration(milliseconds: 300), curve: Curves.ease);
  }

  toPage() {
    //跳转并关闭当前页面
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) {
        return HomePage();
      }),
      (route) =&gt; route == null,
    );
  }
}
</code></pre>
<p>接下来看下应用首页的基本框架和结构：</p>
<pre><code class="dart language-dart">import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_note/ui/search.dart';
import 'package:flutter_note/utils/note_db_helper.dart';
import 'package:flutter_note/utils/tost_utils.dart';
import 'package:sqflite/sqflite.dart';

import 'calendar.dart';
import 'center.dart';
import 'list.dart';
import 'write.dart';
import 'package:path/path.dart';

class HomePage extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return HomePageState();
  }
}

class HomePageState extends State&lt;HomePage&gt; {
  // 默认选中第一项
  int _selectedIndex = 0;
  var _pageController = new PageController(initialPage: 0);
  int last = 0;
  int index = 0;

  NoteDbHelper noteDbHelpter;

  @override
  void initState() {
    super.initState();
    noteDbHelpter = NoteDbHelper();
    getDatabasesPath().then((string) {
      String path = join(string, 'notesDb.db');
      noteDbHelpter.open(path);
    });
    _pageController.addListener(() {});
  }

  // 返回键拦截执行方法
  Future&lt;bool&gt; _onWillPop() {
    int now = DateTime.now().millisecondsSinceEpoch;
    print(now - last);
    if (now - last &gt; 1000) {
      last = now;
      Toast.show("再按一次返回键退出");
      return Future.value(false); //不退出
    } else {
      return Future.value(true); //退出
    }
  }

  @override
  Widget build(BuildContext context) {
    // 要用WillPopScope包裹
    return WillPopScope(
        // 编写onWillPop逻辑
        onWillPop: _onWillPop,
        child: Material(
          child: SafeArea(
              child: Scaffold(
            appBar: PreferredSize(
                // Offstage来控制AppBar的显示与隐藏
                child: Offstage(
                  offstage: _selectedIndex == 2 ? true : false,
                  child: AppBar(
                    backgroundColor: Color.fromRGBO(244, 244, 244, 1),
                    title: Text('备忘录'),
                    primary: true,
                    automaticallyImplyLeading: false,
                    actions: &lt;Widget&gt;[
                      IconButton(
                        icon: Icon(Icons.search),
                        tooltip: '搜索',
                        onPressed: () {
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) {
                            return SearchPage(
                              noteDbHelpter: noteDbHelpter,
                            );
                          }));
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.add),
                        tooltip: '写日记',
                        onPressed: () {
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) {
                            return WritePage(
                              noteDbHelpter: noteDbHelpter,
                              id: -1,
                            );
                          }));
                        },
                      ),
                    ],
                  ),
                ),
                preferredSize:
                    Size.fromHeight(MediaQuery.of(context).size.height * 0.07)),
            // 绑定数据
            body: SafeArea(
                child: PageView(
              // 监听控制类
              controller: _pageController,
              onPageChanged: _onItemTapped,
              physics: NeverScrollableScrollPhysics(),
              children: &lt;Widget&gt;[
                // 三个页面已经进行了封装
                ListPage(
                  noteDbHelpter: noteDbHelpter,
                ),
                CalendarPage(noteDbHelpter: noteDbHelpter),
                CenterPage(noteDbHelpter: noteDbHelpter),
              ],
            )),
            // 底部导航栏用CupertinoTabBar
            bottomNavigationBar: CupertinoTabBar(
              // 导航集合
              items: &lt;BottomNavigationBarItem&gt;[
                BottomNavigationBarItem(
                    activeIcon: Icon(
                      Icons.event_note,
                      color: Colors.blue[300],
                    ),
                    icon: Icon(Icons.event_note),
                    title: Text('主页')),
                BottomNavigationBarItem(
                    activeIcon: Icon(
                      Icons.calendar_today,
                      color: Colors.blue[300],
                    ),
                    icon: Icon(Icons.calendar_today),
                    title: Text('日历')),
                BottomNavigationBarItem(
                    activeIcon: Icon(
                      Icons.person,
                      color: Colors.blue[300],
                    ),
                    icon: Icon(Icons.person),
                    title: Text('个人中心')),
              ],
              currentIndex: _selectedIndex,
              onTap: setPageViewItemSelect,
            ),
          )),
        ));
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  // 底部点击切换
  void setPageViewItemSelect(int indexSelect) {
    _pageController.animateToPage(indexSelect,
        duration: const Duration(milliseconds: 300), curve: Curves.ease);
  }
}
</code></pre>
<p>我们这里就看下第一个页面的代码逻辑 ListPage：</p>
<pre><code class="dart language-dart">import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_note/entity/note.dart';
import 'package:flutter_note/ui/read.dart';
import 'package:flutter_note/utils/event_bus.dart';
import 'package:flutter_note/utils/note_db_helper.dart';
import 'package:flutter_note/utils/time_utils.dart';

class ListPage extends StatefulWidget {
    // 构造方法传入了全局数据库操作类
  const ListPage({
    Key key,
    @required this.noteDbHelpter,
  }) : super(key: key);

  final NoteDbHelper noteDbHelpter;

  @override
  State&lt;StatefulWidget&gt; createState() {
    return ListPageState();
  }
}

// 继承实现了AutomaticKeepAliveClientMixin用来保证切换页面后数据不会丢失销毁
class ListPageState extends State&lt;ListPage&gt; with AutomaticKeepAliveClientMixin {
  ScrollController _scrollController =
      ScrollController(initialScrollOffset: 5, keepScrollOffset: true);
  // 记录列表的数量
  int _size = 0;
  // 记录列表的数据
  List&lt;Note&gt; _noteList = List();
  // EventBus通信类
  StreamSubscription subscription;

  @override
  void initState() {
    super.initState();
    // 注册和监听t发送来的UserEven类型事件、数据
    subscription = eventBus.on&lt;NoteEvent&gt;().listen((NoteEvent event) {
      _onRefresh();
    });
    _scrollController.addListener(() {
      ///滚动监听
    });
    // 刷新加载数据
    _onRefresh();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: RefreshIndicator(
          child: CustomScrollView(
            shrinkWrap: false,
            primary: false,
            // 回弹效果
            physics: BouncingScrollPhysics(),
            scrollDirection: Axis.vertical,
            controller: _scrollController,
            slivers: &lt;Widget&gt;[
              SliverToBoxAdapter(
                child: SizedBox(
                  height: 10,
                ),
              ),
              SliverList(
                delegate: SliverChildBuilderDelegate(
                    (BuildContext context, int index) {
                    // 列表的Item布局和数据绑定
                  return InkWell(
                    child:
                        index % 2 == 0 ? getItem(index) : getImageItem(index),
                    onTap: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (context) {
                        return ReadPage(
                          id: _noteList.elementAt(index).id,
                          noteDbHelpter: widget.noteDbHelpter,
                        );
                      }));
                    },
                    onLongPress: () {
                      _showBottomSheet(index, context);
                    },
                  );
                }, childCount: _size),
              ),
            ],
          ),
          onRefresh: _onRefresh),
    );
  }
    // 长按列表弹窗
  _showBottomSheet(int index, BuildContext c) {
    showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return new Column(
            mainAxisSize: MainAxisSize.min,
            children: &lt;Widget&gt;[
              ListTile(
                leading: Icon(Icons.content_copy),
                title: Text("复制"),
                onTap: () async {
                  Clipboard.setData(
                      ClipboardData(text: _noteList.elementAt(index).content));
                  Scaffold.of(c).showSnackBar(SnackBar(
                    content: Text("已经复制到剪贴板"),
                    backgroundColor: Colors.black87,
                    duration: Duration(
                      seconds: 2,
                    ),
                  ));
                  Navigator.pop(context);
                },
              ),
              ListTile(
                leading: Icon(Icons.delete_sweep),
                title: Text("删除"),
                onTap: () async {
                  widget.noteDbHelpter
                      .deleteById(_noteList.elementAt(index).id);
                  setState(() {
                    _noteList.removeAt(index);
                    _size = _noteList.length;
                  });
                  Navigator.pop(context);
                },
              ),
            ],
          );
        });
  }

  // 刷新
  Future&lt;Null&gt; _onRefresh() async {
    await Future.delayed(Duration(seconds: 1), () {
      print('refresh');
      widget.noteDbHelpter.getDatabase().then((database) {
        database
            .query('notes', orderBy: 'time DESC')
            .then((List&lt;Map&lt;String, dynamic&gt;&gt; records) {
          _size = records.length;
          _noteList.clear();
          for (int i = 0; i &lt; records.length; i++) {
            _noteList.add(Note.fromMap(records.elementAt(i)));
          }
          setState(() {
            print(_noteList.length);
          });
        });
      });
    });
  }

  Widget getItem(int index) {
    return Container(
      child: Card(
        margin: EdgeInsets.fromLTRB(10, 8, 10, 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: &lt;Widget&gt;[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: &lt;Widget&gt;[
                Container(
                  padding: EdgeInsets.fromLTRB(20, 10, 20, 5),
                  child: Row(
                    children: &lt;Widget&gt;[
                      Text(
                        '${DateTime.fromMillisecondsSinceEpoch(_noteList.elementAt(index).time).day}',
                        style: TextStyle(
                            color: Color.fromRGBO(52, 52, 54, 1),
                            fontSize: 50,
                            fontWeight: FontWeight.normal),
                      ),
                      SizedBox(
                        width: 5,
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: &lt;Widget&gt;[
                          Text(
                            '星期${TimeUtils.getWeekday(DateTime.fromMillisecondsSinceEpoch(_noteList.elementAt(index).time).weekday)}',
                            style: TextStyle(
                                color: Color.fromRGBO(149, 149, 148, 1),
                                fontSize: 18),
                          ),
                          Text(
                            TimeUtils.getDate(
                                DateTime.fromMillisecondsSinceEpoch(
                                    _noteList.elementAt(index).time)),
                            style: TextStyle(
                                color: Color.fromRGBO(149, 149, 148, 1),
                                fontSize: 18),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Container(
                    alignment: Alignment.centerRight,
                    padding: EdgeInsets.fromLTRB(0, 5, 20, 5),
                    child: Icon(
                      Icons.wb_sunny,
                      size: 50,
                      color: Color.fromRGBO(252, 205, 24, 1),
                    ),
                  ),
                ),
              ],
            ),
            Container(
              margin: EdgeInsets.all(10),
              child: Text(
                _noteList.elementAt(index).content,
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  color: Color.fromRGBO(103, 103, 103, 1),
                  fontSize: 18,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget getImageItem(int index) {
    return Container(
      child: Card(
        margin: EdgeInsets.fromLTRB(10, 8, 10, 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: &lt;Widget&gt;[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: &lt;Widget&gt;[
                Container(
                  padding: EdgeInsets.fromLTRB(20, 10, 20, 5),
                  child: Row(
                    children: &lt;Widget&gt;[
                      Text(
                        _noteList.length == 0
                            ? ''
                            : '${DateTime.fromMillisecondsSinceEpoch(_noteList.elementAt(index).time).day}',
                        style: TextStyle(
                            color: Color.fromRGBO(52, 52, 54, 1),
                            fontSize: 50,
                            fontWeight: FontWeight.normal),
                      ),
                      SizedBox(
                        width: 5,
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: &lt;Widget&gt;[
                          Text(
                            _noteList.length == 0
                                ? ''
                                : '星期${TimeUtils.getWeekday(DateTime.fromMillisecondsSinceEpoch(_noteList.elementAt(index).time).weekday)}',
                            style: TextStyle(
                                color: Color.fromRGBO(149, 149, 148, 1),
                                fontSize: 18),
                          ),
                          Text(
                            _noteList.length == 0
                                ? ''
                                : TimeUtils.getDate(
                                    DateTime.fromMillisecondsSinceEpoch(
                                        _noteList.elementAt(index).time)),
                            style: TextStyle(
                                color: Color.fromRGBO(149, 149, 148, 1),
                                fontSize: 18),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Container(
                    alignment: Alignment.centerRight,
                    padding: EdgeInsets.fromLTRB(0, 5, 20, 5),
                    child: Icon(
                      Icons.wb_sunny,
                      size: 50,
                      color: Color.fromRGBO(252, 205, 24, 1),
                    ),
                  ),
                ),
              ],
            ),
            Container(
                margin: EdgeInsets.all(10),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: &lt;Widget&gt;[
                    ClipRRect(
                      borderRadius: BorderRadius.circular(5.0),
                      child: Image.network(
                        'https://timgsa.baidu.com/timg?image&amp;quality=80&amp;size=b9999_10000&amp;sec=1564678338847&amp;di=ab19cbea9b5d88a9969ce0825ac5c84d&amp;imgtype=0&amp;src=http%3A%2F%2Fattachments.gfan.net.cn%2Fforum%2F201501%2F13%2F143316yttiiyiuvufcoyjh.jpg',
                        height: 108,
                        width: 108,
                        fit: BoxFit.cover,
                      ),
                    ),
                    Expanded(
                        child: Container(
                      padding: EdgeInsets.fromLTRB(10, 0, 0, 0),
                      child: Text(
                        _noteList.elementAt(index).content,
                        maxLines: 4,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          color: Color.fromRGBO(103, 103, 103, 1),
                          fontSize: 18,
                        ),
                      ),
                    )),
                  ],
                )),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
    subscription.cancel();
  }
    // 保证数据留存
  @override
  bool get wantKeepAlive =&gt; true;
}
</code></pre>
<p>里面有一个剪贴板复制的操作：</p>
<pre><code class="dart language-dart">Clipboard.setData(
                      ClipboardData(text: _noteList.elementAt(index).content));
</code></pre>
<p>接下来我们看下时间工具类：</p>
<pre><code class="dart language-dart">// 主要就是DateTime的一个操作

class TimeUtils {
  static String getWeekday(int day) {
    switch (day) {
      case 1:
        return "一";
      case 2:
        return "二";
      case 3:
        return "三";
      case 4:
        return "四";
      case 5:
        return "五";
      case 6:
        return "六";
      case 7:
        return "日";
    }
  }

  static String getDateTime(DateTime dateTime) {
    return '${dateTime.year}年${dateTime.month}月${dateTime.day}日 ${dateTime.hour}:${dateTime.minute}:${dateTime.second}';
  }

  static String getDate(DateTime dateTime) {
    return '${dateTime.year}年${dateTime.month}月';
  }
}
</code></pre>
<p>其他的页面内容大同小异，通知刷新页面使用的是 EventBus，之前的课程有讲解用法，这里就不重复讲解了。</p>
<p>数据库 sqflite 之前也有讲过，这里也不重复讲解了。</p>
<p>最后附上一个个人中心的和数据库操作类的代码：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_note/utils/note_db_helper.dart';

import 'about.dart';

class CenterPage extends StatefulWidget {
  const CenterPage({
    Key key,
    @required this.noteDbHelpter,
  }) : super(key: key);

  final NoteDbHelper noteDbHelpter;

  @override
  State&lt;StatefulWidget&gt; createState() {
    return CenterPageState();
  }
}

class CenterPageState extends State&lt;CenterPage&gt;
    with AutomaticKeepAliveClientMixin {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color.fromRGBO(244, 244, 244, 1),
      padding: EdgeInsets.fromLTRB(10, 0, 10, 0),
      child: Column(
        children: &lt;Widget&gt;[
          SizedBox(
            height: 10,
          ),
          Row(
            children: &lt;Widget&gt;[
              SizedBox(
                width: 5,
              ),
              Container(
                decoration:
                    BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                padding: EdgeInsets.all(3),
                child: CircleAvatar(
                  backgroundColor: Colors.white,
                  foregroundColor: Colors.blue,
                  backgroundImage: NetworkImage(
                      "https://timgsa.baidu.com/timg?image&amp;quality=80&amp;size=b9999_10000&amp;sec=1564763468169&amp;di=02627b2a0ff227690f3a89c5214bfd86&amp;imgtype=0&amp;src=h"
                      "ttp%3A%2F%2Fpic49.nipic.com%2Ffile%2F20140922%2F2531170_191654419000_2.jpg"),
                  radius: 30.0,
                ),
              ),
              SizedBox(
                width: 10,
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: &lt;Widget&gt;[
                  Text(
                    "最美的日记",
                    style: TextStyle(color: Colors.black, fontSize: 26),
                  ),
                  Text(
                    "编辑资料",
                    style: TextStyle(
                        color: Color.fromRGBO(162, 162, 162, 1), fontSize: 18),
                  )
                ],
              )
            ],
          ),
          SizedBox(
            height: 20,
          ),
          Expanded(
              child: Container(
            child: Column(
              children: &lt;Widget&gt;[
                Flexible(
                  child: Row(
                    children: &lt;Widget&gt;[
                      _buildItem(0),
                      _buildItem(1),
                    ],
                  ),
                  flex: 1,
                ),
                Flexible(
                  child: Row(
                    children: &lt;Widget&gt;[
                      _buildItem(2),
                      _buildItem(3),
                    ],
                  ),
                  flex: 1,
                ),
                Flexible(
                  child: Row(
                    children: &lt;Widget&gt;[
                      _buildItem(4),
                      _buildItem(5),
                    ],
                  ),
                  flex: 1,
                ),
              ],
            ),
          )),
          SizedBox(
            height: 10,
          ),
        ],
      ),
    );
  }

  _buildItem(int index) {
    return Expanded(
      child: Container(
        padding: EdgeInsets.fromLTRB(5, 5, 5, 5),
        child: GestureDetector(
          child: Card(
            child: Container(
              padding: EdgeInsets.all(26),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: &lt;Widget&gt;[
                  _icons.elementAt(index),
                  Expanded(child: Text("")),
                  _title.elementAt(index),
                  _des.elementAt(index),
                ],
              ),
            ),
          ),
          onTap:(){
            _click(index);
          },
        ),
      ),
      flex: 1,
    );
  }

  void _click(int index) {
    switch (index) {
      case 0:
        break;
      case 4:
        Navigator.push(context, MaterialPageRoute(builder: (context) {
          return AboutPage();
        }));
        break;
    }
  }

  List&lt;Icon&gt; _icons = [
    Icon(
      Icons.favorite,
      size: 38,
      color: Colors.yellow,
    ),
    Icon(
      Icons.lock,
      size: 38,
      color: Colors.blue,
    ),
    Icon(
      Icons.feedback,
      size: 38,
      color: Colors.blueAccent,
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

  List&lt;Text&gt; _title = [
    Text(
      "我的收藏",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
    Text(
      "密码锁",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
    Text(
      "吐槽反馈",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
    Text(
      "分享",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
    Text(
      "关于日记",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
    Text(
      "系统设置",
      style: TextStyle(color: Colors.black, fontSize: 20),
    ),
  ];

  List&lt;Text&gt; _des = [
    Text(
      "收藏的重要日记",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "设置密码锁",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "吐槽反馈你的想法",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "分享应用给他人",
      style: TextStyle(color: Color.fromRGBO(162, 162, 162, 1), fontSize: 16),
    ),
    Text(
      "版本信息",
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
<p>数据库操作类：</p>
<pre><code class="dart language-dart">import 'package:flutter_note/entity/note.dart';
import 'package:sqflite/sqflite.dart';

// 数据库操作工具类
class NoteDbHelper {
  Database db;

  Future open(String path) async {
    // 打开/创建数据库
    db = await openDatabase(path, version: 1,
        onCreate: (Database db, int version) async {
      await db.execute(
          "create table notes (_id INTEGER primary key autoincrement,title TEXT not null,content TEXT not null,star INTEGER not null,time INTEGER not null,weather INTEGER not null)");
      print("Table is created");
    });
  }

  Future&lt;Database&gt; getDatabase() async {
    Database database = await db;
    return database;
  }

  // 增加一条数据
  Future&lt;Note&gt; insert(Note note) async {
    note.id = await db.insert("notes", note.toMap());
    return note;
  }

  // 通过ID查询一条数据
  Future&lt;Note&gt; getNoteById(int id) async {
    List&lt;Map&gt; maps = await db.query('notes',
        columns: [
          columnId,
          columnTitle,
          columnContent,
          columnTime,
          columnStar,
          columnWeather
        ],
        where: '_id = ?',
        whereArgs: [id]);
    if (maps.length &gt; 0) {
      return Note.fromMap(maps.first);
    }
    return null;
  }

  // 通过关键字查询数据
  Future&lt;List&lt;Note&gt;&gt; getNoteByContent(String text) async {
    List&lt;Note&gt; _noteList = List();
    List&lt;Map&gt; maps = await db.query('notes',
        columns: [
          columnId,
          columnTitle,
          columnContent,
          columnTime,
          columnStar,
          columnWeather
        ],
        where: 'content like ? ORDER BY time ASC',
        whereArgs: ["%" + text + "%"]);
    if (maps.length &gt; 0) {
      for (int i = 0; i &lt; maps.length; i++) {
        _noteList.add(Note.fromMap(maps.elementAt(i)));
      }
      return _noteList;
    }
    return null;
  }

  // 通过ID删除一条数据
  Future&lt;int&gt; deleteById(int id) async {
    return await db.delete('notes', where: '_id = ?', whereArgs: [id]);
  }

  // 更新数据
  Future&lt;int&gt; update(Note note) async {
    return await db
        .update('notes', note.toMap(), where: '_id = ?', whereArgs: [note.id]);
  }

  // 关闭数据库
  Future close() async =&gt; db.close();
}
</code></pre>
<p>完整项目可以在 Github 上进行下载编译、查看学习：</p>
<p><a href="https://github.com/jaychou2012/flutter_notes">flutter_notes</a></p>
<p>这个项目也会持续更新，开源。后续更新内容：</p>
<p>登录页、注册页、密码锁的绘制、日历事件的完善、收藏页、主题切换、天气和表情及图片的添加等。</p>
<h3 id="-2">总结</h3>
<p>本节课主要是给大家进行了一个完整的项目实践，通过真实案例来巩固和检查之前所学到的这些内容，所以这节课的内容还是挺重要和典型的，大家可以认真看下里面的技术方案。主要注意点和建议如下：</p>
<ul>
<li>熟练掌握这里面涉及到技术点的解决方案，都是常用的比较重要的。</li>
<li>将本节课内容动手敲一遍，看是否遇到了什么问题，然后尝试去解决，也可以在交流群里讨论。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>