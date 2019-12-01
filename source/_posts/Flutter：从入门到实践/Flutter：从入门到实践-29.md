---
title: Flutter：从入门到实践-29
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>经过前面两大部分的详细讲解，相信大家对大部分的布局方式、组件的使用、逻辑业务编写都有了很深入的了解，那么接下来我们就用前面学习的一些知识来进行一个实践：实现一个淘宝风格的商品展示列表，通过这个实例我们可以复习巩固我们之前学过的知识，也算是一个总结与检验。本课练习篇主要是将通过一些组件、自定义组件、常用布局等知识点来完成一个淘宝风格的商品展示列表，一起来学习吧，很简单！</p>
<h3 id="">知识整理</h3>
<p>在进行案例编写前，我们先整理下我们前面学习过的 Flutter 相关 Widget：</p>
<ul>
<li>基础组件（Text、Image、Button）</li>
<li>基础组件（AppBar、AlertDialog、Icon）</li>
<li>基础组件（TextField、Form表单）</li>
<li>基础布局（Scaffold、Container、Center）</li>
<li>基础布局（Row、Column、Flex、Expanded、Stack、IndexedStack）</li>
<li>列表滚动组件（CustomScrollView、ListView、ScrollView、ExpansionPanel）</li>
<li>导航组件（TabBar、NavigationBar、PageView）</li>
<li>流式布局组件（Flow、Wrap）</li>
<li>表格组件（Table、Data Tables）</li>
<li>自定义组件</li>
</ul>
<p>那么我们这节实践课，就通过以上我们学过的一些 Widget 和技术来布局一个淘宝商品列表的应用页面，练练手，也对之前的知识加深一下印象。</p>
<h3 id="-1">应用编写目标</h3>
<p>本节课将用前面所学的一些布局 Widget 和组件 Widget 来编写一个淘宝商品列表的应用页面。效果图和功能展示如下：</p>
<h4 id="-2"><strong>实现一个淘宝风格的商品展示列表</strong></h4>
<p><img src="https://images.gitbook.cn/FvQnU3tM_B16HNy150IfTGeUF6Gk" alt="练习篇效果图" /></p>
<p><strong>里面涉及到：
Scaffold、Container、Row、Column、TextField、AppBar、Text、Image、FloatingActionButton、Icon、ClipRRect、CustomScrollView、SliverPersistentHeader、TabBar、TabBarView 等。</strong></p>
<p>首先分析下这个页面，我们主要是进行 Item 页面的绘制和顶部 Tab 页的效果绘制。我们这里可以使用 Scaffold 构建页面布局框架，然后使用 TabBar 实现顶部的 Tab 页效果。TabBar 的切换页面的 body 显示部分，使用TabBarView 实现。</p>
<p>Item 的布局结构部分，我们通过效果图可以看出，外层可以使用 Column 纵向线性布局 Widget，图片圆角部分处理美化，使用 ClipRRect 和 BoxDecoration 进行圆角处理。</p>
<p><img src="https://images.gitbook.cn/FsrPrP3cnB-yGb8yY55pHUbz-gls" alt="分析" /></p>
<p>具体实现代码如下：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

/// 实现一个淘宝风格的商品展示列表

class PracticeTwoSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return PracticeTwoSamplesState();
  }
}

class PracticeTwoSamplesState extends State&lt;PracticeTwoSamples&gt;
    with SingleTickerProviderStateMixin {
  // 页面切换TabController
  TabController _tabController;
  @override
  void initState() {
    super.initState();
    _tabController = TabController(initialIndex: 0, length: 4, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 定义顶部标题栏
      appBar: AppBar(
        primary: true,
        elevation: 0,
        automaticallyImplyLeading: true,
        title: Container(
          padding: EdgeInsets.only(left: 0, right: 0, top: 10, bottom: 10),
          child: TextField(
            maxLines: 1,
            autofocus: false,
            // TextFiled装饰
            decoration: InputDecoration(
                filled: true,
                contentPadding: EdgeInsets.all(10),
                fillColor: Colors.white,
                border: OutlineInputBorder(
                    borderSide: BorderSide.none,
                    gapPadding: 0,
                    borderRadius: BorderRadius.all(Radius.circular(20))),
                hintText: '衬衫男',
                suffixIcon: Icon(Icons.photo_camera)),
          ),
        ),
        centerTitle: true,
        // 右侧收起的更多按钮菜单
        actions: &lt;Widget&gt;[
          PopupMenuButton(
            itemBuilder: (BuildContext context) =&gt; &lt;PopupMenuItem&lt;String&gt;&gt;[
                  PopupMenuItem&lt;String&gt;(
                    child: Text("消息"),
                    value: "message",
                  ),
                  PopupMenuItem&lt;String&gt;(
                    child: Text("分享"),
                    value: "share",
                  ),
                ],
            onSelected: (String action) {
              switch (action) {
                case "message":
                  print("message");
                  break;
                case "share":
                  print("share");
                  break;
              }
            },
            onCanceled: () {
              print("onCanceled");
            },
          )
        ],
        // 紧挨着标题栏AppBar的TabBar
        bottom: TabBar(
          controller: _tabController,
          isScrollable: false,
          // 标签选中颜色
          labelColor: Color.fromRGBO(247, 70, 0, 1),
          unselectedLabelColor: Colors.black,
          indicatorColor: Color.fromRGBO(247, 70, 0, 1),
          indicatorSize: TabBarIndicatorSize.label,
          // 几个Tab按钮
          tabs: &lt;Widget&gt;[
            Tab(
              text: "全部",
            ),
            Tab(
              text: "天猫",
            ),
            Tab(
              text: "店铺",
            ),
            Tab(
              text: "淘宝经验",
            ),
          ],
        ),
      ),
      // 右下角悬浮的按钮Button
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.white,
        onPressed: () {},
        mini: true,
        elevation: 1,
        highlightElevation: 2,
        child: Icon(
          Icons.vertical_align_top,
        ),
      ),
      // 主体部分布局内容，使用了TabBarView
      body: TabBarView(
        controller: _tabController,
        // 内部切换页布局内容
        children: &lt;Widget&gt;[
          getPage1(),
          getPage1(),
          Center(
            child: Text("data3"),
          ),
          Center(
            child: Text("data4"),
          ),
        ],
      ),
    );
  }

  // 将页面布局单独提取出来写，方便
  Widget getPage1() {
    // 建议最外层使用Container包裹一层
    return Container(
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.only(
              topLeft: Radius.circular(30), topRight: Radius.circular(30))),
      // 内部页面使用CustomScrollView来实现滚动效果
      child: CustomScrollView(slivers: &lt;Widget&gt;[
        // 放置一个可推上去的顶部的标题栏
        SliverPersistentHeader(
          floating: true,
          delegate: _SliverAppBarDelegate(
              maxHeight: 30,
              minHeight: 30,
              child: Container(
                height: 30,
                color: Colors.white,
                alignment: Alignment.center,
                child: Text('淘宝购物悬浮Header'),
              )),
        ),
        // 放置一个固定的顶部的标题栏
        SliverPersistentHeader(
          pinned: true,
          delegate: _SliverAppBarDelegate(
              maxHeight: 30,
              minHeight: 30,
              child: Container(
                color: Colors.white,
                padding: EdgeInsets.all(5),
                height: 30,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: &lt;Widget&gt;[
                    Row(
                      children: &lt;Widget&gt;[
                        Text(
                          '综合',
                          style: TextStyle(color: Colors.orange),
                        ),
                        Icon(
                          Icons.arrow_drop_down,
                          color: Colors.orange,
                        ),
                      ],
                    ),
                    Text(
                      '销量',
                      style: TextStyle(color: Colors.black),
                    ),
                    Row(
                      children: &lt;Widget&gt;[
                        Text(
                          '筛选 ',
                          style: TextStyle(color: Colors.black),
                        ),
                        Icon(
                          Icons.filter_vintage,
                          color: Colors.black,
                          size: 16,
                        ),
                      ],
                    ),
                  ],
                ),
              )),
        ),
        // 列表内容，使用SliverList实现
        SliverList(
          delegate:
              SliverChildBuilderDelegate((BuildContext context, int index) {
            return Container(
              alignment: Alignment.center,
              // 每条内容的布局Item
              child: getItem(),
            );
          },
                  // 定义了60条Item数据
                  childCount: 60),
        )
      ]),
    );
  }

  // 每条内容的布局Item
  Widget getItem() {
    return Container(
        padding: EdgeInsets.all(5),
        child: Row(children: &lt;Widget&gt;[
          // 圆角图片
          ClipRRect(
            borderRadius: BorderRadius.circular(10.0),
            child: Image.network(
              'https://g-search2.alicdn.com/img/bao/uploaded/i4/i4/778081993/O1CN01R7Ytfe1QapseIzl8o_!!778081993.jpg_250x250.jpg_.webp',
              height: 108,
            ),
          ),
          // 用SizedBox增加间距
          SizedBox(
            width: 10,
          ),
          // 右侧的商品描述信息
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: &lt;Widget&gt;[
              SizedBox(
                height: 6,
              ),
              Row(
                children: &lt;Widget&gt;[
                  // 天猫的标签实现
                  Container(
                    padding:
                        EdgeInsets.only(left: 1, right: 1, top: 0, bottom: 0),
                    decoration: BoxDecoration(
                        color: Colors.red,
                        border:
                            Border.all(color: Color(0xFFFF0000), width: 0.5),
                        borderRadius: BorderRadius.all(Radius.circular(5))),
                    child: Text(
                      '天猫',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                      ),
                    ),
                  ),
                  // 商品标题
                  Text(
                    ' 夏季格子男士韩版修身薄款休闲棉衬衣 ',
                    style: TextStyle(
                      color: Colors.black,
                    ),
                    maxLines: 2,
                    softWrap: true,
                  )
                ],
              ),
              SizedBox(
                height: 3,
              ),
              // 商品特征属性
              Text(
                '格子布面料 | 方领 | 薄面料',
                style: TextStyle(color: Colors.grey, fontSize: 12),
              ),
              SizedBox(
                height: 3,
              ),
              // 两个横向标签
              Row(
                children: &lt;Widget&gt;[
                  Container(
                    padding:
                        EdgeInsets.only(left: 3, right: 3, top: 1, bottom: 1),
                    decoration: BoxDecoration(
                        border:
                            Border.all(color: Color(0xFFFF0000), width: 0.5),
                        borderRadius: BorderRadius.all(Radius.circular(5))),
                    child: Text(
                      '天猫无忧购',
                      style: TextStyle(
                        color: Colors.red,
                        fontSize: 10,
                      ),
                    ),
                  ),
                  SizedBox(
                    width: 10,
                  ),
                  Container(
                    padding:
                        EdgeInsets.only(left: 3, right: 3, top: 1, bottom: 1),
                    decoration: BoxDecoration(
                        border: Border.all(color: Colors.yellow, width: 0.5),
                        borderRadius: BorderRadius.all(Radius.circular(5))),
                    child: Text(
                      '包邮',
                      style: TextStyle(
                        color: Colors.yellow,
                        fontSize: 10,
                      ),
                    ),
                  )
                ],
              ),
              SizedBox(
                height: 3,
              ),
              // 价格信息
              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: &lt;Widget&gt;[
                  Text(
                    '￥',
                    style: TextStyle(color: Colors.orange, fontSize: 12),
                  ),
                  Text(
                    '78',
                    style: TextStyle(color: Colors.orange, fontSize: 20),
                  ),
                  SizedBox(
                    width: 10,
                  ),
                  Text(
                    '530人付款  杭州',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                ],
              ),
              SizedBox(
                height: 2,
              ),
              // Item底部店铺信息
              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: &lt;Widget&gt;[
                  Text(
                    '哥尼诺旗舰店',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                  Text(
                    '  进店 &gt;',
                    style: TextStyle(color: Colors.black, fontSize: 12),
                  ),
                  SizedBox(
                    width: 10,
                  ),
                  Icon(
                    Icons.more_horiz,
                    color: Colors.grey,
                    size: 20,
                  ),
                ],
              )
            ],
          )
        ]));
  }
}

// SliverPersistentHeader的SliverPersistentHeaderDelegate实现
class _SliverAppBarDelegate extends SliverPersistentHeaderDelegate {
  _SliverAppBarDelegate({
    @required this.minHeight,
    @required this.maxHeight,
    @required this.child,
  });

  final double minHeight;
  final double maxHeight;
  final Widget child;

  @override
  double get minExtent =&gt; minHeight;

  @override
  double get maxExtent =&gt; maxHeight;

  @override
  Widget build(
      BuildContext context, double shrinkOffset, bool overlapsContent) {
    return child;
  }

  @override
  bool shouldRebuild(_SliverAppBarDelegate oldDelegate) {
    return maxHeight != oldDelegate.maxHeight ||
        minHeight != oldDelegate.minHeight ||
        child != oldDelegate.child;
  }
}
</code></pre>
<p>运行效果如下：</p>
<p><img src="https://images.gitbook.cn/FuJDhoz9pjmD22m2mgfxeQTwUyo9" alt="练习篇实例图" /></p>
<p>动态效果如下：</p>
<p><img src="https://images.gitbook.cn/gifhome_540x960_20s.gif" alt="练习篇动态效果图" /></p>
<p>这样就实现了一个淘宝风格的商品展示列表，涵盖了我们前面所学习的一些 Widget。相信通过这样一个综合实例，大家可以对 Flutter 的页面绘制、应用开发的学习有一个总结。</p>
<p>也可以在这个 Flutter 案例网站进行学习和查看、仿写：<a href="https://itsallwidgets.com/">https://itsallwidgets.com/</a></p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/practice_two">flutter_practice_two</a></p>
<h2 id="-3">总结</h2>
<p>本节课先给大家总结了前面所学的知识，再通过实践案例来检查和巩固之前学到的这些 Widget 和布局相关内容。主要注意点和建议如下：</p>
<ul>
<li><p>熟练掌握这里面涉及到的 Widget 用法，都是常用的、比较重要的，对其中 Widget 的细节用法一定要学会举一反三和自己扩展学习理解，只有在项目实践中，才会更深入、更快地巩固知识。</p></li>
<li><p>将本节课内容动手敲一遍，看是否遇到了什么问题，然后尝试去解决；也可以在读者交流群中问我。</p></li>
</ul>
<hr />
<p>是的，我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>