---
title: Flutter：从入门到实践-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面已经讲解了一些常用的布局方式、常用 Widget 组件以及 Dart 语法。那么这节课我们就来一个小总结，通过一个实例小页面来复习巩固我们之前学过的知识，理论结合实践。本课练习篇主要是完成一个完整的页面的编写，将会涉及到前面学习过的布局 Widget 和组件 Widget ，一起来学习吧，很简单！</p>
<h3 id="">知识整理</h3>
<p>在进行案例编写前，我们先整理下我们前几节学习的 Flutter 相关 Widget：</p>
<ul>
<li>基础组件（Text、Image、Button）</li>
<li>基础组件（AppBar、AlertDialog、Icon）</li>
<li>基础组件（TextField、Form 表单）</li>
<li>基础布局（Scaffold、Container、Center）</li>
<li>基础布局（Row、Column、Flex、Expanded、Stack、IndexedStack）</li>
</ul>
<p>那么我们这节实践课，就通过以上我们学过的一些 Widget 进行绘制简单的应用页面，也可以加深一下印象。</p>
<h3 id="-1">应用编写目标</h3>
<p>本节课将用前面所学的一些布局 Widget 和组件 Widget 来编写一些简单的应用页面，来巩固练习下。效果图和功能展示如下：</p>
<p><strong>仿写 Instagram 列表页</strong></p>
<p><img src="https://images.gitbook.cn/Fo_1CoXn8eiPkBhXwoLDTPqEjlAW" alt="练习篇效果图1" /></p>
<p><strong>仿写登录页</strong></p>
<p><img src="https://images.gitbook.cn/Fg61Cvcjri6XXOdiYnTecW_qDx-T" alt="练习篇效果图2" /></p>
<p><strong>里面涉及到：
Scaffold、Container、Expand、Column、Row、AppBar、Text、Image、AlertDialog、Icon、RaisedButton、Form、TextFormField 等 Widget。</strong></p>
<p>首先看下第一个例子页面，仿写一个 Instagram 列表页，我们主要是进行 Item 页面的绘制和顶部 Tab 页的效果绘制。我们这里可以使用 Scaffold 构建页面布局框架，然后使用 TabBar 实现顶部的 Tab 页效果。TabBar 的切换页面的 body 显示部分，使用 TabBarView 实现。</p>
<p>Item 的布局结构部分，我们通过效果图可以看出，外层可以使用Column纵向线性布局 Widget，图片圆角部分处理美化，使用 ClipRRect 和 BoxDecoration 进行圆角处理。</p>
<p>具体实现代码如下：</p>
<pre><code class="dart language-dart">// 仿照Instagram列表页
import 'package:flutter/material.dart';
import 'package:flutter_samples/samples/practice_one_login.dart';

class PracticeOneSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return PracticeOneSamplesState();
  }
}

class PracticeOneSamplesState extends State&lt;PracticeOneSamples&gt;
    with SingleTickerProviderStateMixin {
  TabController _tabController;
  String imageUrl =
      'https://gss0.bdstatic.com/94o3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike272%2C5%2C5%2C272%2C90/sign=eaad8629b0096b63951456026d5aec21/342ac65c103853431b19c6279d13b07ecb8088e6.jpg';
  @override
  void initState() {
    super.initState();
    _tabController = TabController(initialIndex: 0, length: 5, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    // 用Scaffold构建页面布局框架
    return Scaffold(
      // AppBar构建页面标题栏
      appBar: AppBar(
        title: Text('PracticeOne Widget'),
        primary: true,
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () {
            Scaffold.of(context).openDrawer();
          },
        ),
        // 点击跳转页面
        actions: &lt;Widget&gt;[
          IconButton(
              icon: Icon(Icons.add),
              onPressed: () {
                gotoPage();
              }),
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
        // 加入TabBar功能
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: &lt;Widget&gt;[
            Tab(
              text: "最新",
            ),
            Tab(
              text: "关注",
            ),
            Tab(
              text: "搜搜",
            ),
            Tab(
              text: "热门",
            ),
            Tab(
              text: "我的",
            ),
          ],
        ),
      ),
      // 主体内容布局
      body: TabBarView(
        controller: _tabController,
        children: &lt;Widget&gt;[
          Center(
            child: Column(
              children: &lt;Widget&gt;[
                getTabOne(),
                getTabOne(),
              ],
            ),
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

  // 主体内容布局
  Widget getTabOne() {
    return Padding(
      // 四周加入内容页内边距
      padding: EdgeInsets.only(top: 10,left: 10,right: 10,),
      // 使用Column纵向线性布局
      child: Column(
        children: &lt;Widget&gt;[
          // 对图片进行个性化圆角美化处理
          ClipRRect(
            // 使用Stack层叠布局实现右下角红色Tag标签角标
            child: Stack(
              alignment: Alignment.bottomRight,
              children: &lt;Widget&gt;[
                Image.network(
                  imageUrl,
                  fit: BoxFit.fitWidth,
                  width: MediaQuery.of(context).size.width,
                  height: 200,
                ),
                // 右下角红色Tag标签角标
                Container(
                  padding: EdgeInsets.all(5),
                  decoration: BoxDecoration(
                    color: Colors.red,
                    shape: BoxShape.rectangle,
                    borderRadius: BorderRadius.only(
                        topLeft: Radius.circular(10),
                        bottomLeft: Radius.circular(10),
                        bottomRight: Radius.circular(10)),
                  ),
                  margin: EdgeInsets.all(10),
                  child: Text(
                    'best',
                    style: TextStyle(color: Colors.white, fontSize: 10),
                  ),
                )
              ],
            ),
            // 个性化圆角处理
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(20),
              bottomLeft: Radius.circular(20),
              bottomRight: Radius.circular(20),
            ),
          ),
          // 标题设置，居左居中
          Container(
            alignment: Alignment.centerLeft,
            child: Text(
              '2019春天来了~',
              style: TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                  fontSize: 20),
            ),
          ),
          // 用Row横向线性布局来实现数据展示
          Row(
            children: &lt;Widget&gt;[
              Text(
                '2000 浏览 .',
                style: TextStyle(color: Colors.grey, fontSize: 10),
              ),
              Text(
                '126 喜欢 .',
                style: TextStyle(color: Colors.grey, fontSize: 10),
              ),
              Text(
                '132 评论',
                style: TextStyle(color: Colors.grey, fontSize: 10),
              ),
            ],
          ),
          // 设置间隔
          SizedBox(
            height: 5,
          ),
          Row(
            children: &lt;Widget&gt;[
              // 圆形头像
              Container(
                width: 26,
                height: 26,
                child: CircleAvatar(
                  backgroundImage: AssetImage("assets/assets_image.png"),
                  radius: 50.0,
                ),
              ),
              // 昵称
              Text(
                '   哎呦不错 ',
                style: TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                    fontSize: 12),
              ),
              // 认证图标Icon
              Icon(
                Icons.verified_user,
                size: 15,
                color: Colors.teal,
              ),
              // 用Expanded来实现发表时间居右显示，宽度占用横向剩余空间
              Expanded(
                child: Container(
                  alignment: Alignment.centerRight,
                  child: Text(
                    ' 5 分钟前',
                    style: TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                ),
              ),
            ],
          ),
          // 分隔线
          Container(
            margin: EdgeInsets.only(top: 10, bottom: 10),
            width: MediaQuery.of(context).size.width,
            height: 0.2,
            color: Colors.grey,
          )
        ],
      ),
    );
  }
  // 页面跳转，跳转到登录页
  void gotoPage() {
    Navigator.push(context, MaterialPageRoute(builder: (context) {
      return PracticeOneLoginSamples();
    }));
  }
}
</code></pre>
<p><strong>仿写Instagram列表页效果图：</strong></p>
<p><img src="https://images.gitbook.cn/Fo_1CoXn8eiPkBhXwoLDTPqEjlAW" alt="练习篇效果图1" /></p>
<p><strong>接下来再看一个例子：仿写登录页面。</strong></p>
<p>登录页面主要由这几个元素构成：标题栏、用户名输入框、密码输入框、登录按钮等。
依然使用Scaffold来构建页面布局框架，由于是有多个输入框，为了方便这里外层用Form来包裹输入框相关Widget，用户名和密码输入框使用TextFormField Widget。然后设置好输入框相关的属性配置即可，使用RaisedButton来实现登录按钮。当我们点击RaisedButton登录时候，通过Form表单来获取输入的用户名和密码信息进行显示。</p>
<p>很简单，接下来看下登录页例子实例代码：</p>
<pre><code class="dart language-dart">// 仿写登录页面

import 'package:flutter/material.dart';

class PracticeOneLoginSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return PracticeOneLoginSamplesState();
  }
}

class PracticeOneLoginSamplesState extends State&lt;PracticeOneLoginSamples&gt; {
  // 用于Form表单的状态管理控制
  GlobalKey&lt;FormState&gt; _formKey = new GlobalKey&lt;FormState&gt;();
  FormState _formState;
  String _name;
  String _password;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // 使用Scaffold来构建页面布局框架
    return Scaffold(
      // AppBar设置页面标题栏
      appBar: AppBar(
          title: Text('PracticeOne Login Samples'),
          backgroundColor: Colors.teal,
          primary: true),
      // 主体内容，设置了页面内边距，当然后面可以用SafeArea
      body: Padding(
        padding: EdgeInsets.only(left: 20, right: 20, top: 60),
        // 用Form表单来管理组件
        child: Form(
          key: _formKey,
          child: Column(
            children: &lt;Widget&gt;[
              // 用户名输入框相关
              Container(
                // 用户名输入框底部分隔横线
                decoration: BoxDecoration(
                  border: Border(
                      bottom: BorderSide(color: Colors.grey, width: 0.2)),
                ),
                // 用户名输入框
                child: TextFormField(
                  maxLines: 1,
                  keyboardType: TextInputType.emailAddress,
                  style: TextStyle(fontSize: 18),
                  // 光标颜色
                  cursorColor: Colors.grey,
                  // 保存
                  onSaved: (String value) {
                    _name = value;
                  },
                  // 验证
                  validator: (String value) {
                    return value.contains('@') ? null : '要使用邮箱格式';
                  },
                  // 装饰输入框相关属性配置
                  decoration: InputDecoration(
                      hintText: '请输入邮箱帐号...',
                      labelText: '用户名',
                      // 无边框
                      border: InputBorder.none,
                      // 前缀图标
                      prefixIcon: Icon(Icons.person)),
                ),
              ),
              // 设置间隔
              SizedBox(
                height: 20,
              ),
              // 密码输入框相关配置
              Container(
                decoration: BoxDecoration(
                  border: Border(
                      bottom: BorderSide(color: Colors.grey, width: 0.2)),
                ),
                child: TextFormField(
                  obscureText: true,
                  cursorColor: Colors.grey,
                  maxLines: 1,
                  onSaved: (value) {
                    _password = value;
                  },
                  onFieldSubmitted: (value) {},
                  keyboardType: TextInputType.numberWithOptions(),
                  style: TextStyle(fontSize: 18),
                  // 装饰输入框相关属性配置
                  decoration: InputDecoration(
                      hintText: '请输入密码...',
                      labelText: '密码',
                      border: InputBorder.none,
                      // 前缀图标
                      prefixIcon: Icon(Icons.lock)),
                ),
              ),
              // 设置间隔
              SizedBox(
                height: 30,
              ),
              // 登录按钮
              Container(
                width: MediaQuery.of(context).size.width,
                // 使用RaisedButton
                child: RaisedButton(
                  padding: EdgeInsets.all(13),
                  // 圆角配置
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.all(Radius.circular(6))),
                  color: Colors.teal[500],
                  child: Text(
                    "登录",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),
                  // 登录按钮点击事件
                  onPressed: () {
                    showLogin(context);
                  },
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  // 登录按钮点击执行的方法
  Future&lt;void&gt; showLogin(BuildContext context) async {
    final _formState = _formKey.currentState;
    // Form表单验证通过
    if (_formState.validate()) {
      // 调用save方法回调获取输入框内值
      _formState.save();
      // 弹出对话框AlerDialog
      return showDialog&lt;void&gt;(
          context: context,
          // 点击周围空白区域对话框是否消失
          barrierDismissible: false,
          builder: (BuildContext context) {
            // 弹出对话框AlerDialog
            return AlertDialog(
              title: Text("提示"),
              content: new Text("用户名:'$_name' \n 密码：'$_password'"),
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
  }
}
</code></pre>
<p><strong>仿写登录页效果图：</strong></p>
<p><img src="https://images.gitbook.cn/Fg61Cvcjri6XXOdiYnTecW_qDx-T" alt="练习篇效果图2" /></p>
<p>这样就实现了两个简单的页面，涵盖了我们前面所学习的Widget。相信通过这样一个综合小实例，大家可以对Flutter的页面绘制、应用开发有了一个更深入的了解。</p>
<p>也可以在这个Flutter案例网站进行学习和查看：
<a href="https://itsallwidgets.com/">https://itsallwidgets.com/</a></p>
<p>本节课实例地址：
<a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/practice_one">practice_one</a></p>
<h3 id="-2">总结</h3>
<p>本节课主要是给大家总结了前面所学的一些知识，通过案例小练习来巩固和检查之前所学到的这些 Widget 和布局相关。主要注意点和建议如下：</p>
<ul>
<li>熟练掌握 Scaffold 用法，构建页面框架，对一些 Widget 的细节用法一定要学会举一反三和自己扩展学习理解，只有在项目实践中，才会更深入的、更快的巩固知识。</li>
<li>将本节课内容动手敲一遍，看是否遇到了什么问题，然后尝试去解决。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>