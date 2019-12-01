---
title: Flutter：从入门到实践-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面讲解了 Flutter 的几个基础组件，这节课将讲解跟布局相关的 Widget。</p>
<p>每个平台的应用都有其自己的布局方式，例如 Android 有线性布局、相对布局、绝对布局、帧布局、表格布局等等，HTML 前端也有自己的布局方式。Flutter 当然也不例外。那么这节课就带领大家对 Flutter 的基础布局 Widget 中的几个典型的布局Widget进行详细分析，并结合案例进行详细的用法讲解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Scaffold 布局 Widget 用法详解</li>
  <li>Container 布局 Widget 用法详解</li>
  <li>Center 布局 Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="1scaffoldwidget">1. Scaffold 布局 Widget 用法详解</h3>
<p>Flutter 布局系列的 Widget 一般分为两种，一种是只有单个子元素的布局 Widget，也就是SingleChildRenderObjectWidget；另一个种是具有多个子元素的布局 Widget，一般都有 children 参数，继承自MultiChildRenderObjectWidget。非布局系列 Widget 也有无子元素的 Widget，如 Text、Image 组件，这些无子元素的 Widget 属于 LeafRenderObjectWidget。Flutter 中不同的布局 Widget 对子 Widget 的排列渲染方式不同。接下来我们看下其中比较常用的一个布局 Widget——Scaffold。</p>
<p>Scaffold 是一个页面布局脚手架，实现了基本的 Material 布局，继承自 StatefulWidget，是有状态组件。我们知道大部分的应用页面都是含有标题栏，主体内容，底部导航菜单或者侧滑抽屉菜单等等构成，那么每次都重复写这些内容会大大降低开发效率，所以 Flutter 提供了 Material 风格的 Scaffold 页面布局脚手架，可以很快地搭建出这些元素部分：</p>
<p><img src="https://images.gitbook.cn/FndD6HcO6lfKTvscjv5RvE5YEP02" alt="Scaffold" /></p>
<p>Scaffold 有下面几个主要属性。</p>
<ul>
<li>appBar：显示在界面上的一个标题栏 AppBar。</li>
<li>body： 当前页面的主体内容 Widget。</li>
<li>floatingActionButton：页面的主要功能按钮，不配置就不会显示。</li>
<li>persistentFooterButtons：固定显示在下方的按钮，比如对话框下方的确定、取消按钮。</li>
<li>drawer：侧滑抽屉菜单控件。</li>
<li>backgroundColor：body 内容的背景颜色。</li>
<li>bottomNavigationBar：显示在页面底部的导航栏。</li>
<li>resizeToAvoidBottomPadding：类似于 Android 中的 android:windowSoftInputMode='adjustResize'，避免类似弹出键盘这种操作遮挡布局使用的。</li>
<li>bottomSheet：底部拉出菜单。</li>
</ul>
<p>具体可配置的属性参数，我们看下看下 Scaffold 构造方法：</p>
<pre><code class="dart language-dart">const Scaffold({
    Key key,
    // 标题栏
    this.appBar,
    // 中间主体内容部分
    this.body,
    // 悬浮按钮
    this.floatingActionButton,
    // 悬浮按钮位置
    this.floatingActionButtonLocation,
    // 悬浮按钮动画
    this.floatingActionButtonAnimator,
    // 固定在下方显示的按钮
    this.persistentFooterButtons,
    // 侧滑抽屉菜单
    this.drawer,
    this.endDrawer,
    // 底部菜单
    this.bottomNavigationBar,
    // 底部拉出菜单
    this.bottomSheet,
    // 背景色
    this.backgroundColor,
    this.resizeToAvoidBottomPadding,
    // 重新计算body布局空间大小，避免被遮挡
    this.resizeToAvoidBottomInset,
    // 是否显示到底部，默认为true将显示到顶部状态栏
    this.primary = true,
    this.drawerDragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>如果想显示 Snackbar 或 bottomSheet，可以这样调用：</p>
<pre><code class="dart language-dart">Scaffold.of(context).showSnackBar(new SnackBar(
      content: Text('Hello!'),
    ));

Scaffold.of(context).showBottomSheet...
</code></pre>
<p>接下来看个实例的代码：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

class ScaffoldSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return ScaffoldSamplesState();
  }
}

class ScaffoldSamplesState extends State&lt;ScaffoldSamples&gt; {
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return scaffoldWidget(context);
  }

  Widget scaffoldWidget(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("标题栏"),
        actions: &lt;Widget&gt;[
          //导航栏右侧菜单
          IconButton(icon: Icon(Icons.share), onPressed: () {}),
        ],
      ),
      body: Text("Body内容部分"),
      //抽屉
      drawer: Drawer(
        child: DrawerHeader(
          child: Text("DrawerHeader"),
        ),
      ),
      // 底部导航
      bottomNavigationBar: BottomNavigationBar(
        items: &lt;BottomNavigationBarItem&gt;[
          BottomNavigationBarItem(icon: Icon(Icons.home), title: Text('Home')),
          BottomNavigationBarItem(
              icon: Icon(Icons.category), title: Text('Cagergory')),
          BottomNavigationBarItem(
              icon: Icon(Icons.person), title: Text('Persion')),
        ],
        currentIndex: _selectedIndex,
        fixedColor: Colors.blue,
        onTap: _onItemTap,
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () {
          _onAdd();
        },
      ),
    );
  }

  void _onItemTap(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _onAdd() {}
}
</code></pre>
<p>这个实例实现效果如前面两张图片所示效果。</p>
<h3 id="2containerwidget">2 Container 布局 Widget 用法详解</h3>
<p>Container 是一个容器类布局 Widget，Container 可以说是多个小组件的一个组合容器，如可以设置 padding、margin、Align、Decoration、Matrix4 等等，可以说用起来很方便，很高效。</p>
<p>我们看下 Container 构造方法相关属性和作用：</p>
<pre><code class="dart language-dart">Container({
    Key key,
    // 容器子Widget对齐方式
    this.alignment,
    // 容器内部padding
    this.padding,
    // 背景色
    Color color,
    // 背景装饰
    Decoration decoration,
    // 前景装饰
    this.foregroundDecoration,
    // 容器的宽度
    double width,
    // 容器的高度
    double height,
    // 容器大小的限制条件
    BoxConstraints constraints,
    // 容器外部margin
    this.margin,
    // 变换，如旋转
    this.transform,
    // 容器内子Widget
    this.child,
  })
</code></pre>
<p>接下来看个实例的代码：</p>
<pre><code class="dart language-dart">body: Container(
        constraints: BoxConstraints.expand(
          height: Theme.of(context).textTheme.display1.fontSize * 1.1 + 200.0,
        ),
        padding: const EdgeInsets.all(8.0),
        // 背景色
        color: Colors.teal.shade700,
        // 子Widget居中
        alignment: Alignment.center,
        // 子Widget元素
        child: Text('Hello World',
            style: Theme.of(context)
                .textTheme
                .display1
                .copyWith(color: Colors.white)),
        // 前景装饰
        foregroundDecoration: BoxDecoration(
          image: DecorationImage(
            image: NetworkImage('https://www.example.com/images/frame.png'),
            centerSlice: Rect.fromLTRB(270.0, 180.0, 1360.0, 730.0),
          ),
        ),
        // Container旋转
        transform: Matrix4.rotationZ(0.1),
      ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fk7d1HN2dL5LTRkbILmXl5NrisGq" alt="Container" /></p>
<h3 id="3centerwidget">3 Center 布局 Widget 用法详解</h3>
<p>Center 主要用于对齐，将内部子 Widget 与自身进行居中对齐，并根据子 Widget 的大小自动调整自身大小。</p>
<p>Center Widget 是继承自 Align，Align 继承自 SingleChildRenderObjectWidget，也是单子元素 Widget。</p>
<p>看下 Center 的构造方法：</p>
<pre><code class="dart language-dart"> Center({
    Key key,
    // 宽度因子
    double widthFactor, 
    // 高度因子
    double heightFactor, 
    // 子元素
    Widget child
   })
</code></pre>
<p>大家可能对这个宽度和高度因子的作用不太明白，其实就是设置 Center 的宽度和高度是子元素宽度和高度的倍数的，widthFactor 和 heightFactor 可以不设置，默认 Center 容器宽度横向充满，高度包裹子元素。如将widthFactor 和 heightFactor 设置为 2.0 的话，则 Center 容器的占用宽度和高度是子元素宽度和高度的 2 倍，但是最大不超过屏幕的宽高。</p>
<p>接下来看个实例演示用法：</p>
<pre><code class="dart language-dart">body: Column(
        children: &lt;Widget&gt;[
          Container(
            color: Colors.blueGrey,
            child: Center(
              widthFactor: 2,
              heightFactor: 2,
              child: Container(
                width: 60,
                height: 30,
                color: Colors.red,
              ),
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Center(
            child: Container(
              width: 60,
              height: 30,
              color: Colors.teal,
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Center(
            child: Container(
              height: 100.0,
              width: 100.0,
              color: Colors.yellow,
              child: Align(
                // 设置对齐位置约束
                alignment: FractionalOffset(0.2, 0.6),
                child: Container(
                  height: 40.0,
                  width: 40.0,
                  color: Colors.red,
                ),
              ),
            ),
          ),
        ],
      ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fi2mgPLPwdMZKhs71me_983b3WP9" alt="Center" /></p>
<p>本节课代码实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_09">flutter_09</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的几个基础布局 Widget——Scaffold、Container、Center 的用法和特点。布局在 Flutter 中很重要，所以希望大家掌握这几个布局 Widget 的特点、使用场景。建议如下：</p>
<ul>
<li>将本节课内容动手敲一遍，看是否遇到了什么问题，然后尝试去解决。</li>
<li>Scaffold 和 Container 非常常用，Center 相对来说和前两者比频率不是很大，可以着重看前两个布局 Widget。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>