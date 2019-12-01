---
title: Flutter：从入门到实践-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将继续讲解 Flutter 的常用组件中的列表滚动组件。</p>
<p>在实际开发中，会经常涉及到列表滚动。在 Flutter 中可以滚动的组件容器有很多，如 ScrollView、ListView、GridView、CustomScrollView 等等。那么这节课就带领大家对 Flutter 的常用组件中的列表滚动组件进行详细分析讲解，并结合案例进行详细的用法讲解。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>CustomScrollView Widget 用法详解</li>
  <li>ListView Widget 用法详解</li>
  <li>GridView Widget 用法详解</li>
  <li>ScrollView 相关知识点讲解</li>
  <li>ExpansionPanel Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="customscrollviewwidget">CustomScrollView Widget 用法详解</h3>
<p>CustomScrollView 是一个可以自己通过 Flutter 里的 sliver 来组装滚动 Widget 的一个控件，里面可以放置任何我们需要滚动的 Widget，也是相对来说最常使用的一个滚动组件。</p>
<p>我们看下 CustomScrollView 的继承关系：</p>
<p>CustomScrollView -&gt; ScrollView -&gt; StatelessWidget</p>
<p>CustomScrollView 是一个无状态组件，继承自 ScrollView，也扩展了 ScrollView 的功能。</p>
<p>CustomScrollView 最大的特点就是内部的组装的滚动组件都是 Sliver 特性的，也就是必须是 Sliver 可滚动块的 Widget 才可以，如：CustomScrollView 内部可以放置 SliverList、SliverFixedExtentList、SliverGrid、SliverPadding、SliverAppBar、SliverToBoxAdapter 等组件。</p>
<p>CustomScrollView 非常强大，如我们可以把 ListView 和 GridView 组装在一起，也可以拼装其他的 Sliver Widget，实现更复杂的效果。</p>
<p>我们看下 CustomScrollView 的构造方法：</p>
<pre><code class="dart language-dart">const CustomScrollView({
    Key key,
    // 滚动方向
    Axis scrollDirection = Axis.vertical,
    // 是否反向显示
    bool reverse = false,
    // 滚动控制对象
    ScrollController controller,
    // 是否是与父级关联的主滚动视图
    bool primary,
    // 滚动视图应如何响应用户输入
    ScrollPhysics physics,
    // 是否根据正在查看的内容确定滚动视图的范围
    bool shrinkWrap = false,
    Key center,
    double anchor = 0.0,
    // 缓存区域
    double cacheExtent,
    // 内部sliver组件
    this.slivers = const &lt;Widget&gt;[],
    int semanticChildCount,
    DragStartBehavior dragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>来看下 CustomScrollView 效果图：</p>
<p><img src="https://images.gitbook.cn/FtYwLZLKn1WuXnP_dblzB3CgImQg" alt="CustomScrollViewr" /></p>
<p>接下来我们通过一个实例来看下如何使用 CustomScrollView。</p>
<p>这段代码就是实现上面的效果的：</p>
<pre><code class="dart language-dart">@override
  Widget build(BuildContext context) {
    return Material(
      child: CustomScrollView(
        // slivers里面放置sliver滚动块组件
        slivers: &lt;Widget&gt;[
          // 放置一个顶部的标题栏
          SliverAppBar(
            // 是否固定在顶部
            pinned: true,
            // 展开高度
            expandedHeight: 250.0,
            // 可展开区域，通常是一个FlexibleSpaceBar
            flexibleSpace: FlexibleSpaceBar(
              title: const Text('CustomScrollView'),
              background: Image.asset("assets/image_appbar.jpg",fit: BoxFit.cover,),
            ),
          ),
          // 放置一个SliverGrid Widget
          SliverGrid(
            // 设置Grid属性：
            // SliverGridDelegateWithMaxCrossAxisExtent：
            // 按照设置最大扩展宽度计算item个数
            // SliverGridDelegateWithFixedCrossAxisCount:
            // 可以固定设置每行item个数
            gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
              // item最大宽度
              maxCrossAxisExtent: 200.0,
              // 主轴item间隔
              mainAxisSpacing: 10.0,
              // 交叉轴item间隔
              crossAxisSpacing: 10.0,
              // item宽高比
              childAspectRatio: 4.0,
            ),
            // 设置item的布局及属性
            // SliverChildListDelegate：适用于有固定数量的item的List
            // SliverChildBuilderDelegate:适用于不固定数量的item的List
            delegate: SliverChildBuilderDelegate(
              (BuildContext context, int index) {
                return Container(
                  alignment: Alignment.center,
                  color: Colors.teal[100 * (index % 9)],
                  child: Text('grid item $index'),
                );
              },
              // 20个item数量
              childCount: 20,
            ),
          ),
          // 指定item高度的List
          SliverFixedExtentList(
            // item固定高度
            itemExtent: 50.0,
            // 设置item布局和属性
            delegate: SliverChildBuilderDelegate(
              (BuildContext context, int index) {
                return Container(
                  alignment: Alignment.center,
                  color: Colors.lightBlue[100 * (index % 9)],
                  child: Text('list item $index'),
                );
              },
              childCount: 20,
            ),
          ),
        ],
      ),
    );
  }
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FkYP0rU-NmYNSqDRj_GduoiNVXSL" alt="CustomScrollView" /></p>
<p>接下来再给一个稍微复杂点的实例：</p>
<pre><code class="dart language-dart">ScrollController _scrollController =
    ScrollController(initialScrollOffset: 5, keepScrollOffset: true);

Widget customScrollview1() {
  _scrollController.addListener(() {
    ///滚动监听
  });
  return CustomScrollView(
    shrinkWrap: false,
    primary: false,
    // 回弹效果
    physics: BouncingScrollPhysics(),
    scrollDirection: Axis.vertical,
    controller: _scrollController,
    slivers: &lt;Widget&gt;[
      ///SliverGrid用法
      SliverGrid(
        delegate: SliverChildBuilderDelegate(
          (BuildContext context, int index) {
            return Container(
              alignment: Alignment.center,
              color: Colors.teal[100 * (index % 9)],
              child: Text(
                'grid item $index',
                style: TextStyle(fontSize: 12, decoration: TextDecoration.none),
              ),
            );
          },
          childCount: 20,
        ),

        ///设置Grid属性：
        ///SliverGridDelegateWithMaxCrossAxisExtent：
        ///按照设置最大扩展宽度计算item个数
        ///SliverGridDelegateWithFixedCrossAxisCount:
        ///可以固定设置每行item个数
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 5,
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,

          ///item高度缩放比例，默认为1；小于1表示放大，大于1表示缩小
          childAspectRatio: 1,
        ),
        //  SliverGridDelegateWithMaxCrossAxisExtent(
        //   ///item最大宽度
        //   maxCrossAxisExtent: 400.0,
        //   mainAxisSpacing: 10.0,
        //   crossAxisSpacing: 10.0,
        //   childAspectRatio: 4.0,
        // ),
      ),

      ///SliverChildListDelegate：适用于有固定数量的item的List
      ///SliverChildBuilderDelegate:适用于不固定数量的item的List

      SliverList(
        delegate: SliverChildBuilderDelegate((BuildContext context, int index) {
          return Container(
            alignment: Alignment.center,
            color: Colors.lightBlue[100 * (index % 9)],
            child: Text(
              'SliverList item $index',
              style: TextStyle(fontSize: 12, decoration: TextDecoration.none),
            ),
          );
        }, childCount: 20),
      ),
      // 可以伸缩滚动的头部
      SliverPersistentHeader(
        delegate: _SliverAppBarDelegate(
          minHeight: 60.0,
          maxHeight: 180.0,
          child: Container(
            color: Colors.pink,
            child: Image.asset("assets/image_appbar.jpg",fit: BoxFit.cover,),
          ),
        ),
      ),

      ///指定item高度的List
      SliverFixedExtentList(
        ///item固定高度
        itemExtent: 50,
        delegate: SliverChildBuilderDelegate(
          (BuildContext context, int index) {
            return Container(
              alignment: Alignment.center,
              color: Colors.lightBlue[100 * (index % 9)],
              child: Text(
                'list item $index',
                style: TextStyle(fontSize: 12, decoration: TextDecoration.none),
              ),
            );
          },
          childCount: 20,
        ),
      ),
      SliverList(
        delegate: SliverChildListDelegate(&lt;Widget&gt;[
          Text(
            "SliverList SliverChildListDelegate",
            style: TextStyle(fontSize: 12, decoration: TextDecoration.none),
          ),
          Image.asset("assets/flutter-mark-square-64.png"),
        ]),
      ),
      // SliverPadding周围可以设置内边距
      SliverPadding(
        padding: const EdgeInsets.all(10.0),
        sliver: SliverList(
          delegate: SliverChildListDelegate(&lt;Widget&gt;[
            Text(
              "SliverPadding SliverChildListDelegate",
              style: TextStyle(fontSize: 12, decoration: TextDecoration.none),
            ),
            Image.asset("assets/flutter-mark-square-64.png"),
          ]),
        ),
      ),
      // SliverToBoxAdapter内部可以放置任意Widget
      SliverToBoxAdapter(
        child: Text(
          "SliverToBoxAdapter",
          style: TextStyle(fontSize: 16, decoration: TextDecoration.none),
        ),
      ),
    ],
  );
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FqT9n2lx6w3kdsEWkbjpLai583f2" alt="CustomScrollView" /></p>
<h3 id="listviewwidget">ListView Widget 用法详解</h3>
<p>接下来我们看下 ListView 组件用法，很简单，ListView 主要实现线性列表布局，可以横向或者纵向。先看下ListView 的继承关系：</p>
<p>ListView -&gt; BoxScrollView -&gt; ScrollView</p>
<p>ListView 也是继承自 ScrollView 组件，扩展了 ScrollView 的特点。</p>
<p>看下 ListView 的构造方法：</p>
<pre><code class="dart language-dart">ListView({
    Key key,
    // 滚动排列方向
    Axis scrollDirection = Axis.vertical,
    bool reverse = false,
    ScrollController controller,
    bool primary,
    // 物理滑动响应动画
    ScrollPhysics physics,
    // 是否根据子widget的总高度/长度来设置ListView的长度，默认值为false
    bool shrinkWrap = false,
    EdgeInsetsGeometry padding,
    // item固定高度
    this.itemExtent,
    // 是否将item包裹在AutomaticKeepAlive widget中
    bool addAutomaticKeepAlives = true,
    // 是否将item包裹在RepaintBoundary中
    bool addRepaintBoundaries = true,
    bool addSemanticIndexes = true,
    double cacheExtent,
    // 子item元素
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
    int semanticChildCount,
    DragStartBehavior dragStartBehavior = DragStartBehavior.down,
  })
</code></pre>
<p>接下来通过一个实例来看下 ListView 的用法：</p>
<pre><code class="dart language-dart">//ListView最简单的用法
ListView(
  shrinkWrap: true,
  padding: const EdgeInsets.all(20.0),
  children: &lt;Widget&gt;[
    const Text('I\'m dedicating every day to you'),
    const Text('Domestic life was never quite my style'),
    const Text('When you smile, you knock me out, I fall apart'),
    const Text('And I thought I was so smart'),
  ],
),

// 稍复杂用法
// 定义一个List
List&lt;String&gt; items = &lt;String&gt;[
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'O',
];

// 定义个枚举来设置item显示几行及类型
enum _MaterialListType {
  oneLine,

  oneLineWithAvatar,

  twoLine,

  threeLine,
}

class ListViewSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return ListViewSamplesState();
  }
}

class ListViewSamplesState extends State&lt;ListViewSamples&gt; {
  List widgets = [];

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ListView'),
      ),
      body: listView4(),
    );
  }

  ///最简单的ListView
  Widget listView1() {
    return ListView(
      children: &lt;Widget&gt;[
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
        Text(
          'data',
          style: TextStyle(fontSize: 30),
        ),
      ],
    );
  }

  ///动态封装ListView，使用ListTile作为item
  Widget listView2() {
    // listTiles为item布局集合
    Iterable&lt;Widget&gt; listTiles = items.map&lt;Widget&gt;((String string) {
      return getItem(string);
    });
    ListTile.divideTiles(context: context, tiles: listTiles);
    return ListView(
      children: listTiles.toList(),
    );
  }

  ///使用ListView.builder构造
  Widget listView3() {
    // item widget集合
    return ListView.builder(
      // 设置item数量
      itemCount: items.length,
      itemBuilder: (BuildContext context, int position) {
        return getItem(items.elementAt(position));
      },
    );
  }

  ///ListView.custom构建ListView
  Widget listView4() {
    ///SliverChildListDelegate：适用于有固定数量的item的List
    ///SliverChildBuilderDelegate:适用于不固定数量的item的List
    return ListView.custom(
      // 设置item构建属性
      childrenDelegate:
          SliverChildBuilderDelegate((BuildContext context, int index) {
        // 返回item布局
        return ListTile(
          isThreeLine: true,
          dense: true,
          leading: ExcludeSemantics(
              child: CircleAvatar(child: Text(items.elementAt(index)))),
          title: Text('This item represents .'),
          subtitle: Text("$index"),
          trailing: Icon(Icons.info, color: Theme.of(context).disabledColor),
        );
      }, childCount: 13),
    );
  }

  ///ListView.separated构建ListView
  Widget listView5() {
    // 有分隔线
    return ListView.separated(
      // item数量
      itemCount: items.length,
      // 分隔线属性设置
      separatorBuilder: (BuildContext context, int index) {
        return Container(height: 1, color: Colors.pink);
      },
      // 构建item布局
      itemBuilder: (BuildContext context, int index) {
        return ListTile(
          isThreeLine: true,
          dense: true,
          leading: ExcludeSemantics(
              child: CircleAvatar(child: Text(items.elementAt(index)))),
          title: Text('This item represents .'),
          subtitle: Text(items.elementAt(index)),
          trailing: Icon(Icons.info, color: Theme.of(context).disabledColor),
        );
      },
    );
  }

  // 用来获取item布局的方法
  Widget getItem(String item) {
    // if (i.isOdd) {
    //   return Divider();
    // }
    return GestureDetector(
      child: Padding(
        padding: EdgeInsets.all(10.0),
        child: ListTile(
            dense: true,
            title: Text('Two-line ' + item),
            trailing: Radio&lt;_MaterialListType&gt;(
              value: _MaterialListType.twoLine,
              groupValue: _MaterialListType.twoLine,
              onChanged: changeItemType,
            )),
      ),
      onTap: () {
        setState(() {
          // print('row $i');
        });
      },
      onLongPress: () {},
    );
  }

  void changeItemType(_MaterialListType type) {
    print("changeItemType");
  }
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FnEs23fqrE9OhDdfoKeBneXg_CSk" alt="ListView" /></p>
<h3 id="gridviewwidget">GridView Widget 用法详解</h3>
<p>GridView 的用法和 ListView 类似，可以对比着学习，就是实现网格列表的 item 排列效果。先看下 GridView 的继承关系：</p>
<p>GridView -&gt; BoxScrollView -&gt; ScrollView</p>
<p>GridView 也是继承自 ScrollView 组件，扩展了 ScrollView 的特点。</p>
<p>看下 GridView 的构造方法：</p>
<pre><code class="dart language-dart">GridView({
    Key key,
    Axis scrollDirection = Axis.vertical,
    bool reverse = false,
    ScrollController controller,
    bool primary,
    ScrollPhysics physics,
    bool shrinkWrap = false,
    EdgeInsetsGeometry padding,
    // 控制GridView的item如何排列
    @required this.gridDelegate,
    bool addAutomaticKeepAlives = true,
    bool addRepaintBoundaries = true,
    bool addSemanticIndexes = true,
    double cacheExtent,
    // item集合
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
    int semanticChildCount,
  })
</code></pre>
<p>我们通过一个实例来看下 GridView 用法：</p>
<pre><code class="dart language-dart">//GridView简单的用法
body: GridView.count(
        primary: false,
        padding: const EdgeInsets.all(20.0),
        crossAxisSpacing: 10.0,
        // 每行多少个item
        crossAxisCount: 2,
        children: &lt;Widget&gt;[
          const Text('He\'d have you all unravel at the'),
          const Text('Heed not the rabble'),
          const Text('Sound of screams but the'),
          const Text('Who scream'),
          const Text('Revolution is coming...'),
          const Text('Revolution, they...'),
        ],
      ),

// 稍微复杂点用法
class GridViewSamplesState extends State&lt;GridViewSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('GridView'),
        backgroundColor: Colors.teal,
        primary: true,
      ),
      body: gridView1(),
    );
  }
  // 构造GriView方式1
  Widget gridView1() {
    return GridView(
      ///设置Grid属性：
      ///SliverGridDelegateWithMaxCrossAxisExtent：
      ///按照设置最大扩展宽度计算item个数
      ///SliverGridDelegateWithFixedCrossAxisCount:
      ///可以固定设置每行item个数
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
      children: &lt;Widget&gt;[
        Image.asset(
          'assets/image_appbar.jpg',
          fit: BoxFit.cover,
        ),
        Image.asset(
          'assets/image_appbar.jpg',
          fit: BoxFit.cover,
        ),
        Image.asset(
          'assets/image_appbar.jpg',
          fit: BoxFit.cover,
        ),
        Image.asset(
          'assets/image_appbar.jpg',
          fit: BoxFit.cover,
        ),
        Image.asset(
          'assets/image_appbar.jpg',
          fit: BoxFit.cover,
        ),
      ],
    );
  }
  // 构造GriView方式2
  Widget gridView2() {
    return GridView.builder(
      // item总数
      itemCount: 20,
      // 构建item
      itemBuilder: (BuildContext context, int index) {
        // GridTile可以构造带有头部、底部、中间内容的item
        return GridTile(
          header: GridTileBar(
            title: Text(
              'header',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
            leading: Icon(
              Icons.star,
              color: Colors.white,
            ),
          ),
          child: Image.asset('assets/image_appbar.jpg'),
          footer: GridTileBar(
            title: Text(
              'bottom',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
          ),
        );
      },
      // GridView排列属性设置
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
    );
  }
  // 构造GriView方式3
  Widget gridView3() {
    return GridView.custom(
      // 设置GridView属性
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 2,
      ),
      // 设置item属性
      childrenDelegate:
          SliverChildBuilderDelegate((BuildContext context, int index) {
        return Container(
          child: Text(
            'GridTile',
            style: TextStyle(fontSize: 16),
          ),
        );
      }, childCount: 20),
    );
  }
  // 构造GriView方式4
  Widget gridView4() {
    return GridView.count(
      crossAxisCount: 2,
      mainAxisSpacing: 10,
      crossAxisSpacing: 10,
      childAspectRatio: 1,
      children: &lt;Widget&gt;[
        GridTile(
          child: Image.asset('assets/image_appbar.jpg'),
        ),
        GridTile(
          child: Image.asset('assets/image_appbar.jpg'),
        ),
        GridTile(
          child: Image.asset('assets/image_appbar.jpg'),
        ),
        GridTile(
          child: Image.asset('assets/image_appbar.jpg'),
        ),
        GridTile(
          child: Image.asset('assets/image_appbar.jpg'),
        ),
      ],
    );
  }

  // 构造GriView方式5
  ///GridView.extent构建GridView，根据最大宽度自动计算item数量
  Widget gridView5() {
    return GridView.extent(
      // item最大宽度
      maxCrossAxisExtent: 150,
      crossAxisSpacing: 10,
      mainAxisSpacing: 10,
      childAspectRatio: 1,
      children: &lt;Widget&gt;[
        GridTile(
          header: GridTileBar(
            title: Text(
              'header',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
            leading: Icon(
              Icons.star,
              color: Colors.white,
            ),
          ),
          child: Image.asset('assets/image_appbar.jpg'),
          footer: GridTileBar(
            title: Text(
              'bottom',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
          ),
        ),
        GridTile(
          header: GridTileBar(
            title: Text(
              'header',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
            leading: Icon(
              Icons.star,
              color: Colors.white,
            ),
          ),
          child: Image.asset('assets/image_appbar.jpg'),
          footer: GridTileBar(
            title: Text(
              'bottom',
              style: TextStyle(fontSize: 20),
            ),
            backgroundColor: Colors.black45,
          ),
        ),
      ],
    );
  }
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FoUfAlo_e7imUxwPIOXtGKP7GfA-" alt="GridView" /></p>
<h3 id="scrollview">ScrollView 相关知识点讲解</h3>
<p>ScrollView 这个 Widget 并不直接单独使用，一般是使用它的扩展类，如 CustomScrollView、ListView、GridView 等等。这里将他们相关的通用特性讲一下：</p>
<p>滚动条样式的设置。一般滚动类组件滚动时，我们希望侧边显示一个滚动条，那么我们可以使用 Scrollbar 进行包裹：</p>
<pre><code class="dart language-dart">///Scrollbar
Widget scroll1() {
  return Scrollbar(
    child: ListView.separated(
      itemCount: 20,
      separatorBuilder: (BuildContext context, int index) {
        return Container(height: 1, color: Colors.black87);
      },
      itemBuilder: (BuildContext context, int index) {
        return ListTile(
          isThreeLine: true,
          dense: true,
          leading:
              ExcludeSemantics(child: CircleAvatar(child: Text('leading'))),
          title: Text('This item represents .'),
          subtitle: Text('subtitle'),
          trailing: Icon(Icons.info, color: Theme.of(context).disabledColor),
        );
      },
    ),
  );
}
</code></pre>
<p>单子元素的 ScrollView（SingleChildScrollView），类似于 Android 里的 ScrollView，内部只能包裹一个子控件：</p>
<pre><code class="dart language-dart">///SingleChildScrollView
Widget scroll2() {
  // 只能放置一个元素
  return SingleChildScrollView(
    child: Column(
      children: &lt;Widget&gt;[
        Container(
          // A fixed-height child.
          color: Colors.yellow,
          height: 620.0,
        ),
        Container(
          color: Colors.orange,
          height: 720.0,
        ),
      ],
    ),
  );
}
</code></pre>
<p>有的时候我们需要自定义放置在内部的子元素排列方式，可以使用 CustomMultiChildLayout 或 CustomSingleChildLayout，这两个不常用，大家了解即可：</p>
<pre><code class="dart language-dart">// CustomMultiChildLayout
Widget scroll5() {
  return CustomMultiChildLayout(
    delegate: MultiChildDelegate(),
    children: &lt;Widget&gt;[
      LayoutId(
        id: MultiChildDelegate.title,
        child: Container(
          color: Colors.teal,
          child: Text('data1'),
        ),
      ),
      LayoutId(
        id: MultiChildDelegate.description,
        child: Container(
          color: Colors.amber,
          child: Text('data2'),
        ),
      ),
    ],
  );
}

class MultiChildDelegate extends MultiChildLayoutDelegate {
  static const String title = 'title';
  static const String description = 'description';

  @override
  void performLayout(Size size) {
    ///约束
    BoxConstraints boxConstraints = BoxConstraints(maxWidth: size.width);

    ///绑定约束
    Size titleSize = layoutChild(title, boxConstraints);

    ///位置
    positionChild(title, Offset(0, 0));
    Size descriptionSize = layoutChild(description, boxConstraints);
    double descriptionY = titleSize.height;
    positionChild(description, Offset(10, descriptionY));
  }

  @override
  bool shouldRelayout(MultiChildLayoutDelegate oldDelegate) {
    return oldDelegate == this;
  }
}

// CustomSingleChildLayout
Widget scroll6() {
  return CustomSingleChildLayout(
    delegate: SingleChildDelegate(Size(300, 200)),
    child: Container(
      color: Colors.teal,
      child: Text('data'),
    ),
  );
}

class SingleChildDelegate extends SingleChildLayoutDelegate {
  Size size;
  SingleChildDelegate(this.size);

  @override
  Size getSize(BoxConstraints constraints) {
    // return super.getSize(constraints);
    return size;
  }

  @override
  BoxConstraints getConstraintsForChild(BoxConstraints constraints) {
    // return super.getConstraintsForChild(constraints);
    return BoxConstraints.tight(size);
  }

  @override
  Offset getPositionForChild(Size size, Size childSize) {
    // return super.getPositionForChild(size, childSize);
    return Offset(30, 20);
  }

  @override
  bool shouldRelayout(SingleChildLayoutDelegate oldDelegate) {
    return oldDelegate == this;
  }
}
</code></pre>
<h3 id="expansionpanelwidget">ExpansionPanel Widget 用法详解</h3>
<p>ExpansionPanel 用来实现类似于 QQ 分组的一个组件，一般搭配 ExpansionPanelList 一起使用。</p>
<p>我们先看下大致效果图：</p>
<p><img src="https://images.gitbook.cn/Fj43pB_4ofXDSQytAM9HMfeZYHvd" alt="ExpansionPanelList" /></p>
<p>ExpansionPanelList 继承自 StatefulWidget，是有状态组件。</p>
<p>我们接下来看下 ExpansionPanelList 的构造方法：</p>
<pre><code class="dart language-dart">const ExpansionPanelList({
    Key key,
    // 子元素ExpansionPanel集合
    this.children = const &lt;ExpansionPanel&gt;[],
    // 展开/关闭回调
    this.expansionCallback,
    // 展开动画执行时长
    this.animationDuration = kThemeAnimationDuration,
  })
</code></pre>
<p>然后是 ExpansionPanel 的构造方法：</p>
<pre><code class="dart language-dart">ExpansionPanel({
    // 标题构造器
    @required this.headerBuilder,
    // 内容区域
    @required this.body,
    // 是否展开
    this.isExpanded = false
  }) 
</code></pre>
<p>接下来通过一个实例来看下 ExpansionPanelList 和 ExpansionPanel 的用法:</p>
<pre><code class="dart language-dart">class ExpansionPanelListPageState extends State&lt;ExpansionPanelListPage&gt; {
  List&lt;ExpansionPanelItem&gt; _expansionPanelItems;
  @override
  void initState() {
    super.initState();
    getExpansionPanelList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ExpansionPanelList"),
      ),
      body: Container(
        padding: EdgeInsets.all(10.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: &lt;Widget&gt;[
            // ExpansionPanelList
            ExpansionPanelList(
              // 动态创建ExpansionPanel item布局
              children: _expansionPanelItems.map((ExpansionPanelItem item) {
                return ExpansionPanel(
                  // 头部区域
                  headerBuilder: (BuildContext context, bool isExpanded) {
                    return Container(
                      padding: EdgeInsets.all(10.0),
                      child: Text(
                        item.headerText,
                        style: Theme.of(context).textTheme.title,
                      ),
                    );
                  },
                  // 内容区域
                  body: item.body,
                  // 面板是否展开
                  isExpanded: item.isExpand,
                );
              }).toList(),
              // 面板展开/关闭回调
              expansionCallback: (int panelIndex, bool isExpanded) {
                setState(() {
                  _expansionPanelItems[panelIndex].isExpand = !isExpanded;
                });
              },
            )
          ],
        ),
      ),
    );
  }
  // 创建面板item布局的集合
  List&lt;ExpansionPanelItem&gt; getExpansionPanelList() {
    _expansionPanelItems = new List();
    for (int i = 0; i &lt; 5; i++) {
      _expansionPanelItems.add(ExpansionPanelItem(
        headerText: 'Panel B',
        body: Container(
          padding: EdgeInsets.all(10.0),
          width: double.infinity,
          child: Text('Content for Panel $i \n The Content'),
        ),
        isExpand: false,
      ));
    }
    _expansionPanelItems.length = 5;
    return _expansionPanelItems;
  }
}

// 自定义item
class ExpansionPanelItem {
  final String headerText;
  final Widget body;
  bool isExpand;
  ExpansionPanelItem({
    this.headerText,
    this.body,
    this.isExpand,
  });
}

// 简单用法

class ExpansionPanelPageState extends State&lt;ExpansionPanelPage&gt; {
  // 面板是否展开状态保存
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ExpansionPanelList"),
      ),
      body: Container(
        padding: EdgeInsets.all(10.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: &lt;Widget&gt;[
            // ExpansionPanelList
            ExpansionPanelList(
              children: &lt;ExpansionPanel&gt;[
                // ExpansionPanel
                ExpansionPanel(
                  // 头部
                  headerBuilder: (BuildContext context, bool isExpanded) {
                    return Container(
                      padding: EdgeInsets.all(10.0),
                      child: Text(
                        'Panel A',
                        style: Theme.of(context).textTheme.title,
                      ),
                    );
                  },
                  // 展开的内容区域
                  body: Container(
                    padding: EdgeInsets.all(10.0),
                    width: double.infinity,
                    child: Text('Content for Panel A\n The Content'),
                  ),
                  // 是否展开
                  isExpanded: _isExpanded,
                ),
                ExpansionPanel(
                  headerBuilder: (BuildContext context, bool isExpanded) {
                    return Container(
                      padding: EdgeInsets.all(10.0),
                      child: Text(
                        'Panel B',
                        style: Theme.of(context).textTheme.title,
                      ),
                    );
                  },
                  body: Container(
                    padding: EdgeInsets.all(10.0),
                    width: double.infinity,
                    child: Text('Content for Panel B\n The Content'),
                  ),
                  isExpanded: _isExpanded,
                )
              ],
              // 展开或关闭回调
              expansionCallback: (int panelIndex, bool isExpanded) {
                setState(() {
                  _isExpanded = !isExpanded;
                });
              },
            )
          ],
        ),
      ),
    );
  }
}
</code></pre>
<p><img src="https://images.gitbook.cn/FgcJbWQ0koEwT08LxQNiBqnJl61G" alt="ExpansionPanelList" /></p>
<p>ExpansionPanelList 和 ExpansionPanel 并不属于滚动组件，只不过看起来类似。这里放在一起顺便讲解。</p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_13">flutter_13</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的几个常用的列表、滚动布局组件 Widget 的用法和特点。主要注意点和建议如下：</p>
<ul>
<li>重点掌握 CustomScrollView、ListView 和 GridView 用法。</li>
<li>实践一下这几个 Widget 使用方法，尝试写一个可以滚动的列表页面。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>