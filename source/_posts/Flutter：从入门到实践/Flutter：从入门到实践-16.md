---
title: Flutter：从入门到实践-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将继续讲解 Flutter 的常用组件，前面已经给大家介绍了 Flutter 系列 Widget，今天讲解导航相关的组件。在 Android 的 Material Design 中，一般是底部使用 TabBar 实现底部导航或者顶部使用 TabBar、TabLayout 结合 ViewPager 来实现导航，那么在 Flutter 里我们如何实现这种效果呢？这节课我们就给大家分析相关组件，并结合案例进行用法讲解。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>TabBar 和 TabBarView Widget 用法详解</li>
  <li>BottomNavigationBar Widget 用法详解</li>
  <li>CupertinoTabBar 和 PageView Widget 用法详解</li>
  <li>BottomAppBar Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="tabbartabbarviewwidget">TabBar 和 TabBarView Widget 用法详解</h3>
<p>TabBar 和 TabBarView 一般是搭配使用，TabBar 用来实现 Tab 导航部分，TabBarView 用来实现 body 内容区域部分。TabBar 继承自 StatefulWidget，是一个有状态组件。TabBarView 同样也是继承自 StatefulWidget。</p>
<p>我们看下 TabBar 实现的效果：</p>
<p><img src="https://images.gitbook.cn/FqZuWgndVBAS3x0bJYh5Py_w0l0r" alt="avatar" /></p>
<p>来看下 TabBar 的构造方法：</p>
<pre><code class="dart language-dart">const TabBar({
    Key key,
    // tab页Widget集合，可以使用Tab组件或者其他组件
    @required this.tabs,
    // TabController对象，控制tab页
    this.controller,
    // 是否可滚动
    this.isScrollable = false,
    // 指示器颜色
    this.indicatorColor,
    // 指示器高度
    this.indicatorWeight = 2.0,
    // 底部指示器的Padding
    this.indicatorPadding = EdgeInsets.zero,
    // 指示器装饰器decoration，例如加边框
    this.indicator,
    // 指示器大小计算方式，TabBarIndicatorSize.label跟文字等宽，TabBarIndicatorSize.tab跟每个tab等宽
    this.indicatorSize,
    // 选中Tab文字颜色
    this.labelColor,
    // 选中Tab文字Style
    this.labelStyle,
    // 每个label的padding值
    this.labelPadding,
    // 未选中label颜色
    this.unselectedLabelColor,
    // 未选中label的Style
    this.unselectedLabelStyle,
    this.dragStartBehavior = DragStartBehavior.down,
    // 点击事件
    this.onTap,
  })
</code></pre>
<p>再看下 TabBarVeiw 构造方法：</p>
<pre><code class="dart language-dart">const TabBarView({
    Key key,
    // tab内容页列表,和TabBar的tab数量一样
    @required this.children,
    // TabController对象，控制tab页
    this.controller,
    this.physics,
    this.dragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>我们看一个 TabBar 和 TabBarView 结合的实例：</p>
<pre><code class="dart language-dart">// TabBar和TabBarView最简单的用法

class TabBarSamplesState extends State&lt;TabBarSamples&gt;
    with SingleTickerProviderStateMixin {
  TabController _tabController;

  @override
  void initState() {
    super.initState();
    //initialIndex为初始选中第几个，length为数量
    _tabController = TabController(initialIndex: 0, length: 5, vsync: this);
    // 监听
    _tabController.addListener(() {
      switch (_tabController.index) {
        case 0:

          break;
        case 1:

          break;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('TabBar Demo'),
        primary: true,
        // 设置TabBar
        bottom: TabBar(
          controller: _tabController,
          tabs: &lt;Widget&gt;[
            Tab(
              text: "Tab1",
            ),
            Tab(
              text: "Tab2",
            ),
            Tab(
              text: "Tab3",
            ),
            Tab(
              text: "Tab4",
            ),
            Tab(
              text: "Tab5",
            ),
          ],
        ),
      ),
      // body用TabBarView
      body: TabBarView(
        controller: _tabController,
        children: &lt;Widget&gt;[
          Center(
            child: Text("TabBarView data1"),
          ),
          Center(
            child: Text("TabBarView data2"),
          ),
          Center(
            child: Text("TabBarView data3"),
          ),
          Center(
            child: Text("TabBarView data4"),
          ),
          Center(
            child: Text("TabBarView data5"),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
    _tabController.dispose();
  }
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FlyPW9Hj1CSjZIqXlDoOr5xs7esg" alt="TabBar和TabBarView" /></p>
<p>当然把 TabBar 放在底部也可以，不过一般放在顶部，放在底部的导航效果用另外一种组件，我们接下来将会学到。</p>
<p>如果想放在底部可以这样设置：</p>
<pre><code class="dart language-dart">// 最外层是Scaffold布局
bottomNavigationBar: Material(
        color: Colors.blue,
        child: TabBar(
          controller: _controller,
          tabs: &lt;Tab&gt;[
            Tab(text: "Home", icon: Icon(Icons.home)),
            Tab(text: "Apps", icon: Icon(Icons.list)),
            Tab(text: "Center", icon: Icon(Icons.message)),
          ],
          indicatorWeight: 0.1,
        ),
      ),
</code></pre>
<h3 id="bottomnavigationbarwidget">BottomNavigationBar Widget 用法详解</h3>
<p>BottomNavigationBar 一般用来实现底部导航效果，和 Android 原生效果基本一样。</p>
<p>BottomNavigationBar 继承自 StatefulWidget，一般搭配 BottomNavigationBarItem 进行使用。</p>
<p>我们看下 BottomNavigationBar 实现的效果:</p>
<p><img src="https://images.gitbook.cn/FpfEZCOdJKWEnr5JNM-WS0Cu-MQX" alt="BottomNavigationBar和BottomNavigationBarItem" /></p>
<p>BottomNavigationBar 实现的导航有一个特点就是选中项会稍微有一个放大的动画，这是和其他组件实现的导航效果的一个小差别。</p>
<p>BottomNavigationBar 的构造方法：</p>
<pre><code class="dart language-dart">BottomNavigationBar({
    Key key,
    // BottomNavigationBarItem集合
    @required this.items,
    this.onTap,
    // 当前选中位置
    this.currentIndex = 0,
    // 设置显示的模式
    BottomNavigationBarType type,
    // 主题色
    this.fixedColor,
    // 图标尺寸
    this.iconSize = 24.0,
  })
</code></pre>
<p>BottomNavigationBarItem 的构造方法：</p>
<pre><code class="dart language-dart">const BottomNavigationBarItem({
    // 图标
    @required this.icon,
    // 文字
    this.title,
    // 选中图标
    Widget activeIcon,
    // 背景色
    this.backgroundColor,
  })
</code></pre>
<p>接下来我们通过代码来实现上面的 BottomNavigationBar 的效果：</p>
<pre><code class="dart language-dart">... ...
class NavigationBarState extends State&lt;NavigationBarSamples&gt; {
  // 默认选中第一项
  int _selectedIndex = 0;

  final _widgetOptions = [
    Text('Index 0: Home'),
    Text('Index 1: Business'),
    Text('Index 2: School'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('BottomNavigationBar Demo'),
      ),
      // 主体内容
      body: Center(
        child: _widgetOptions.elementAt(_selectedIndex),
      ),
      // 底部BottomNavigationBar
      bottomNavigationBar: BottomNavigationBar(
        items: &lt;BottomNavigationBarItem&gt;[
          // 单个BottomNavigationBarItem
          BottomNavigationBarItem(icon: Icon(Icons.home), title: Text('Home')),
          BottomNavigationBarItem(
              icon: Icon(Icons.business), title: Text('Business')),
          BottomNavigationBarItem(
              icon: Icon(Icons.school), title: Text('School')),
        ],
        // 选中位置
        currentIndex: _selectedIndex,
        // 主题色
        fixedColor: Colors.deepPurple,
        // 点击
        onTap: _onItemTapped,
      ),
    );
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }
}
</code></pre>
<p>可以得到上面效果图所示的运行效果。</p>
<h3 id="cupertinotabbarpageviewwidget">CupertinoTabBar 和 PageView Widget 用法详解</h3>
<p>想实现 Android 上类似于 ViewPager 和 TabBar 的导航效果的，也可以使用 CupertinoTabBar 配合PageView 进行实现。这也是一种实现底部导航切换页面的一种方式。</p>
<p>我们看下 CupertinoTabBar 实现的效果：</p>
<p><img src="https://images.gitbook.cn/FqoXdnW20y9FSoyNUUzgTqxhgSGe" alt="CupertinoTabBar和PageView" /></p>
<p>CupertinoTabBar 继承自 StatelessWidget，PageView 继承自 StatefulWidget。</p>
<p>我们先看下 CupertinoTabBar 的构造方法：</p>
<pre><code class="dart language-dart">CupertinoTabBar({
    Key key,
    // 导航项
    @required this.items,
    this.onTap,
    this.currentIndex = 0,
    this.backgroundColor,
    // 选中色
    this.activeColor,
    // 未选中色
    this.inactiveColor = CupertinoColors.inactiveGray,
    this.iconSize = 30.0,
    // 边框
    this.border = const Border(
      top: BorderSide(
        color: _kDefaultTabBarBorderColor,
        width: 0.0, // One physical pixel.
        style: BorderStyle.solid,
      ),
    ),
  })
</code></pre>
<p>再看下 PageView 的构造方法：</p>
<pre><code class="dart language-dart">PageView({
    Key key,
    // 滚动方向
    this.scrollDirection = Axis.horizontal,
    this.reverse = false,
    // PageController页面控制
    PageController controller,
    // 滚动的动画效果
    this.physics,
    this.pageSnapping = true,
    // 页面改变监听
    this.onPageChanged,
    // 子元素
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
    this.dragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>接下来我们通过代码来实现上面的 CupertinoTabBar 的效果：</p>
<pre><code class="dart language-dart">class CupertinoTabBarState extends State&lt;CupertinoTabBarSamples&gt; {
  // 默认选中第一项
  int _selectedIndex = 0;
  var _pageController = new PageController(initialPage: 0);

  @override
  void initState() {
    super.initState();
    _pageController.addListener(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('CupertinoTabBar Demo'),
      ),
      // body主体内容用PageView
      body: PageView(
        // 监听控制类
        controller: _pageController,
        onPageChanged: _onItemTapped,
        children: &lt;Widget&gt;[
          Text('Index 0: Home'),
          Text('Index 1: Business'),
          Text('Index 2: School'),
        ],
      ),
      // 底部导航栏用CupertinoTabBar
      bottomNavigationBar: CupertinoTabBar(
        // 导航集合
        items: &lt;BottomNavigationBarItem&gt;[
          BottomNavigationBarItem(icon: Icon(Icons.home), title: Text('Home')),
          BottomNavigationBarItem(
              icon: Icon(Icons.business), title: Text('Business')),
          BottomNavigationBarItem(
              icon: Icon(Icons.school), title: Text('School')),
        ],
        currentIndex: _selectedIndex,
        onTap: setPageViewItemSelect,
      ),
    );
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
<h3 id="bottomappbarwidget">BottomAppBar Widget 用法详解</h3>
<p>实现底部的导航效果，除了上面讲到的这些组件外，还可以用 BottomAppBar 来实现，这个组件自定义功能更加强大一些，也可以实现比较复杂的自定义效果。一般搭配 FloatingActionButton 自定义使用。</p>
<p>BottomAppBar 继承自 StatefulWidget。</p>
<p>我们看下 BottoAppBar 自定义实现的效果图：</p>
<p><img src="https://images.gitbook.cn/Fth6e0kKow3AW2FUpMMHqXjXSqnM" alt="BottoAppBar" /></p>
<p>我们看下 BottomAppBar 的构造方法：</p>
<pre><code class="dart language-dart">const BottomAppBar({
    Key key,
    // 颜色
    this.color,
    this.elevation,
    // 设置底栏的形状
    this.shape,
    this.clipBehavior = Clip.none,
    this.notchMargin = 4.0,
    // 可以放置各种类型的Widget，自定义性更强
    this.child,
  })
</code></pre>
<p>接下来我们通过代码来实现上面的 BottomAppBar 的效果：</p>
<pre><code class="dart language-dart">class BottomAppBarState extends State&lt;BottomAppBarSamples&gt; {

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('BottomAppBar Demo'),
      ),
      // body主体内容
      body: Text("Index 0：Home"),
      // 底部导航栏用BottomAppBar
      bottomNavigationBar: BottomAppBar(
        // 切口的距离
        notchMargin: 6,
        // 底部留出空缺
        shape: CircularNotchedRectangle(),
        child: Row(
          children: &lt;Widget&gt;[
            IconButton(
              icon: Icon(Icons.home),
              onPressed: null,
            ),
            IconButton(
              icon: Icon(Icons.business),
              onPressed: null,
            ),
            IconButton(
              icon: Icon(Icons.school),
              onPressed: null,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
          child: Icon(
            Icons.add,
            color: Colors.white,
          ),
          onPressed: null),
      floatingActionButtonLocation: FloatingActionButtonLocation.endDocked,
    );
  }
}
</code></pre>
<p>运行效果如上面的效果图所示。</p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_14">flutter_14</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的几种实现导航页效果的组件，我们可以根据实际情况需要选择合适的组件进行实现导航页效果，也要知道它们的用法和特点。主要注意点和建议如下：</p>
<ul>
<li>掌握这几种导航页实现的方法、组件特点。</li>
<li>熟练掌握它们的用法，实践一下这几个 Widget 使用方法，尝试写一个可以有顶部和底部导航栏的页面。</li>
</ul></div></article>