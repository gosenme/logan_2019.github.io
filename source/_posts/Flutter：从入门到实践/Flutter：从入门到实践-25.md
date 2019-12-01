---
title: Flutter：从入门到实践-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在移动应用开发中，经常会使用到手势操作，这也是移动平台应用独有的一个功能特性。我们可以使用手势进行密码设置、通过手势操作进行定义一系列有含义的操作等等。Flutter 也支持手势操作的使用。</p>
<p>这节课除了手势功能的用法外还会给大家讲解下 Flutter 中本地数据库的操作用法， Android 平台本地数据库一般是使用 SQLite，Flutter 通过插件的方式提供了本地数据库的相关操作方法。本节课结合案例，讲解 Flutter 里的手势和数据库缓存的具体用法：</p>
<blockquote>
  <ul>
  <li>手势的用法详解</li>
  <li>数据库的用法详解</li>
  </ul>
</blockquote>
<h3 id="1">1 手势的用法详解</h3>
<p>Flutter 的手势控制包括：长按、点击、双击、拖拽、移动、缩放等等操作。这些手势操作都是通过 GestureDetector 来实现的。</p>
<p>我们看下 GestureDetector。GestureDetector 继承自 StatelessWidget，无状态组件。构造方法如下：</p>
<pre><code class="dart language-dart">GestureDetector({
    Key key,
    // 子控件
    this.child,
    // 点击按下
    this.onTapDown,
    // 点击抬起
    this.onTapUp,
    // 点击
    this.onTap,
    // 触摸屏幕了，但是点击取消
    this.onTapCancel,
    // 双击
    this.onDoubleTap,
    // 长按
    this.onLongPress,
    // 长按开始
    this.onLongPressStart,
    this.onLongPressMoveUpdate,
    this.onLongPressUp,
    this.onLongPressEnd,
    // 垂直滑动拖拽按下
    this.onVerticalDragDown,
    // 垂直滑动拖拽开始
    this.onVerticalDragStart,
    this.onVerticalDragUpdate,
    // 垂直滑动拖拽结束
    this.onVerticalDragEnd,
    // 垂直滑动拖拽取消
    this.onVerticalDragCancel,
    // 水平滑动拖拽按下
    this.onHorizontalDragDown,
    this.onHorizontalDragStart,
    this.onHorizontalDragUpdate,
    this.onHorizontalDragEnd,
    this.onHorizontalDragCancel,
    this.onForcePressStart,
    this.onForcePressPeak,
    this.onForcePressUpdate,
    this.onForcePressEnd,
    // 手指按下
    this.onPanDown,
    // 按下移动开始
    this.onPanStart,
    // 手指按下开始滑动
    this.onPanUpdate,
    // 手指抬起
    this.onPanEnd,
    // 滑动取消
    this.onPanCancel,
    // 缩放开始
    this.onScaleStart,
    // 缩放滑动中
    this.onScaleUpdate,
    // 缩放结束
    this.onScaleEnd,
    this.behavior,
    this.excludeFromSemantics = false,
    this.dragStartBehavior = DragStartBehavior.start,
  })
</code></pre>
<p>接下来我们看下 GestureDetector 中几个常用的、重要的方法的用法：</p>
<pre><code class="dart language-dart">// 首先看下最常用的点击、双击、长按事件
var gestureStatus = 'Gesture';
...
Center(
      child: GestureDetector(
        child: RaisedButton(
          child: Text(gestureStatus),
        ),
        // 点击
        onTap: () {
          setState(() {
            gestureStatus = 'onTap';
          });
        },
        // 双击
        onDoubleTap: () {
          setState(() {
            gestureStatus = 'onDoubleTap';
          });
        },
        // 长按
        onLongPress: () {
          setState(() {
            gestureStatus = 'onLongPress';
          });
        },
      ),
    )
</code></pre>
<p>我们只需要在要添加手势控制的 Widget 的外面包装一个 GestureDetector 即可，是不是很简单？</p>
<p>接下来再看一下 GestureDetector 实现横向或者纵向滑动的手势监听：</p>
<pre><code class="dart language-dart">// 类似于我们使用纵向滚动条时，向下滑动查看内容的操作手势
// Flutter支持沿某一个方向的监听控制,我们先看下垂直方向监听

class GestureSamplesState extends State&lt;GestureSamples&gt; {
  var gestureStatus = 'Gesture';
  var _top = 100.0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return getstureVertical(context);
  }

  Widget getstureVertical(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Gesture'),
      ),
      body: Container(
          child: Stack(
        children: &lt;Widget&gt;[
          Positioned(
            top: _top,
            left: 100.0,
            child: GestureDetector(
                child: Icon(Icons.history),
                //垂直方向拖动监听
                onVerticalDragUpdate: (DragUpdateDetails details) {
                  setState(() {
                      // 动态更新垂直坐标
                    _top += details.delta.dy;
                  });
                }),
          )
        ],
      )),
    );
  }

}
</code></pre>
<p>效果图如下：</p>
<p><img src="https://images.gitbook.cn/Fkx3k99HkBGX-noT730m2RGMk25J" alt="纵向滚动监听效果图" /></p>
<p>同理，水平监听滚动也是同样的用法。如果一个组件既有水平拖拽监听又有垂直拖拽监听的话，执行哪个方向的主要取决于你在哪个方向上的位移大。</p>
<p>再看下 Flutter GestureDetector 实现缩放操作：</p>
<pre><code class="dart language-dart">class GestureSamplesState extends State&lt;GestureSamples&gt; {
  var gestureStatus = 'Gesture';

  var _width = 180.0;
  var _scale = 1.0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return getstureScale(context);
  }

  Widget getstureScale(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Gesture'),
      ),
      body: Container(
          child: Stack(
        children: &lt;Widget&gt;[
          Center(
            child: GestureDetector(
              // 动态控制宽度，高度自适应
              child: Image.asset(
                "assets/image_appbar.jpg",
                width: _width,
              ),
              onScaleStart: (ScaleStartDetails details) {
                print('onScaleStart:$details.focalPoint');
              },
              onScaleEnd: (ScaleEndDetails details) {
                print('onScaleEnd:$details.focalPoint');
              },
              onScaleUpdate: (ScaleUpdateDetails details) {
                setState(() {
                  // 除了缩放也可以进行旋转操作
                  // details.rotation.clamp(0, 360);
                  // 缩放倍数在0.5到5倍之间
                  _scale = details.scale.clamp(0.5, 5);
                  _width = 180 * _scale;
                });
              },
            ),
          )
        ],
      )),
    );
  }

}
</code></pre>
<p>效果图如下：</p>
<p><img src="https://images.gitbook.cn/ljp2koSnL89GmaodQVeTnSaJrnmU" alt="缩放监听效果图" /></p>
<p>接下来看下 GestureDetector 实现移动拖拽操作：</p>
<pre><code class="dart language-dart">class GestureSamplesState extends State&lt;GestureSamples&gt; {
  var gestureStatus = 'Gesture';
  var _top = 100.0;
  var _left = 100.0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return getstureMove(context);
  }

  Widget getstureMove(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Gesture'),
      ),
      body: Container(
          child: Stack(
        children: &lt;Widget&gt;[
          Positioned(
            top: _top,
            left: _left,
            child: GestureDetector(
              child: Icon(Icons.home),
              //手指按下时
              onPanDown: (DragDownDetails e) {
                //手指按下的位置
                print("按下位置：${e.globalPosition}");
              },
              //手指滑动时
              onPanUpdate: (DragUpdateDetails e) {
                //手指滑动时，更新偏移，重新构建
                setState(() {
                  _top += e.delta.dy;
                  _left += e.delta.dx;
                });
              },
              // 手指抬起时
              onPanEnd: (DragEndDetails e) {
                //滑动结束时在x轴、y轴上的速度
                print("结束时速度：${e.velocity}");
              },
            ),
          )，
        ],
      )),
    );
  }

}
</code></pre>
<p>效果图如下：</p>
<p><img src="https://images.gitbook.cn/Fn33xbtD15rkF56Ce78AbE5kmYc2" alt="缩放监听效果图" /></p>
<blockquote>
  <p><strong>扩展内容：</strong></p>
  <p><strong>针对手势监听大家也可以自学了解下 Listener 用法、GestureRecognizer 用法、RawGestureDetector 用法。可以对比着进行扩展学习。</strong></p>
</blockquote>
<h3 id="2">2 数据库的用法详解</h3>
<p>Flutter 原生 API 是不支持数据库操作的，目前是以插件库方式进行数据库操作。Flutter 官方提供了一个官方插件库：sqflite，实现了数据库的增删改查操作。</p>
<p>插件库地址：<a href="https://pub.dev/packages/sqflite">https://pub.dev/packages/sqflite</a></p>
<p>首先需要在 pubspec.yaml 里添加依赖：</p>
<pre><code class="dart language-dart">dependencies:
  sqflite: ^1.1.5
</code></pre>
<p>在使用的地方导入：</p>
<pre><code class="dart language-dart">import 'package:sqflite/sqflite.dart';
</code></pre>
<p>接下来看下具体用法，首先我们要建立一个数据库表实体类，这里举例为 Note 类：</p>
<pre><code class="dart language-dart">final String tableName = 'notes';// 表名
final String columnId = '_id';// 属性名
final String columnTitle = 'title';// 属性名
final String columnContent = 'content';// 属性名

// 实体类
class Note {
  int id;
  String title;
  String content;

  // 将实体对象类转为数据集合
  Map&lt;String, dynamic&gt; toMap() {
    var map = &lt;String, dynamic&gt;{
      columnTitle: title,
      columnContent: content,
    };
    if (id != null) {
      map[columnId] = id;
    }
    return map;
  }

  // 构造方法/实例化方法
  Note();

  // 通过数据集合返回一个实体对象
  Note.fromMap(Map&lt;String, dynamic&gt; map) {
    id = map[columnId];
    title = map[columnTitle];
    content = map[columnContent];
  }
}
</code></pre>
<p>接下来创建数据库表的操作工具类：</p>
<pre><code class="dart language-dart">import 'package:sqflite/sqflite.dart';

import 'Note.dart';

// 数据库操作工具类
class NoteDbHelper {
  Database db;

  Future open(String path) async {
    // 打开/创建数据库
    db = await openDatabase(path, version: 1,
        onCreate: (Database db, int version) async {
      await db.execute('''
create table Notes ( 
  _id integer primary key autoincrement, 
  title text not null,
  content text not null)
''');
    });
  }

  Database getDatabase(){
    return db;
  }

  // 增加一条数据
  Future&lt;Note&gt; insert(Note note) async {
    note.id = await db.insert("notes", note.toMap());
    return note;
  }

  // 通过ID查询一条数据
  Future&lt;Note&gt; getNoteById(int id) async {
    List&lt;Map&gt; maps = await db.query('notes',
        columns: [columnId, columnTitle, columnContent],
        where: '_id = ?',
        whereArgs: [id]);
    if (maps.length &gt; 0) {
      return Note.fromMap(maps.first);
    }
    return null;
  }

  // 通过ID删除一条数据
  Future&lt;int&gt; deleteById(int id) async {
    return await db.delete('notes', where: '_id = ?', whereArgs: [id]);
  }

  // 更新数据
  Future&lt;int&gt; update(Note note) async {
    return await db.update('notes', note.toMap(),
        where: '_id = ?', whereArgs: [note.id]);
  }

  // 关闭数据库
  Future close() async =&gt; db.close();
}
</code></pre>
<p>最后我们看下如何调用使用：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_samples/samples/note_db_helpter.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

import 'Note.dart';

...

class SQLiteSamplesState extends State&lt;SQLiteSamples&gt; {
  NoteDbHelper noteDbHelpter;

  @override
  void initState() {
    super.initState();
    noteDbHelpter = NoteDbHelper();
    String databasesPath = getDatabasesPath().toString();
    String path = join(databasesPath, 'notesDb.db');
    noteDbHelpter.open(path);

    noteDbHelpter.getNoteById(1).then((Note note) {
      print(note.title);
    });

    // 也可以这样使用
    noteDbHelpter
        .getDatabase()
        .query('notes')
        .then((List&lt;Map&lt;String, dynamic&gt;&gt; records) {
      Map&lt;String, dynamic&gt; mapRead = records.first;
      // 读取属性值
      mapRead['title'] = '1';
      // 如果想修改的话
      Map&lt;String, dynamic&gt; map = Map&lt;String, dynamic&gt;.from(mapRead);
      // 更新修改
      map['title'] = '2';
    });

    // 支持原始SQL语句使用
    noteDbHelpter.getDatabase().rawUpdate(
        'UPDATE notes SET title = ?, content = ? WHERE _id = ?',
        ['my title', 'my content', 2]).then((int count) {
      print('updated: $count');
    });
  }

}

....
</code></pre>
<p>sqflite 同样也支持事物操作和批量操作。</p>
<pre><code class="dart language-dart">// 事务操作
await db.transaction((txn) async {
  await txn.execute('CREATE TABLE Test1 (id INTEGER PRIMARY KEY)');
  ...
});

// 批量操作
batch = db.batch();
batch.insert('Test', {'name': 'item'});
batch.update('Test', {'name': 'new_item'}, where: 'name = ?', whereArgs: ['item']);
batch.delete('Test', where: 'name = ?', whereArgs: ['item']);
results = await batch.commit();
</code></pre>
<p>sqflite 支持如下数据类型：INTEGER（对应 int）、REAL（对应 num）、TEXT（对应 String）、BLOB（对应 Uint8List）。</p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_23">flutter_23</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的手势和数据库的用法，数据库的使用我们要重点掌握。主要注意点和建议如下：</p>
<ul>
<li>重点掌握数据库增删改查的用法;</li>
<li>使用 GestureDetector 进行实践操作一下。</li>
</ul></div></article>