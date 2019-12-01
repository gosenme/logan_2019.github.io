---
title: Flutter：从入门到实践-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Flutter 的面向对象的编程方式，吸取了 React 的编程组件化思维。Flutter 的所有类都可以看做是 Widget，大部分的类都是继承自 Widget 类。所有学习和了解 Flutter 有哪些 Widget、怎么分类的，对我们后续快速学习非常有用，也可以对 Flutter 的结构层级有一个大致的了解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 的整体结构层级</li>
  <li>Flutter 的 Widget 分类</li>
  <li>Flutter Widget 其他知识点</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 Flutter 的整体结构层级</h3>
<p>之前的章节介绍过 Flutter 的 Framework 的结构层级，再来回顾下这张图：</p>
<p><img src="https://images.gitbook.cn/Fmz1bR818jSQ9ep9vHWv6C9wU-6p" alt="Flutter Framework 1" /></p>
<p><img src="https://images.gitbook.cn/FtHYK0I09XlDiJ9OwmZ2eZzzcQXy" alt="Flutter Framework 2" /></p>
<p>第一张是最新的详细结构图，第二张是比较早的更粗放的 Flutter Framework 结构图。</p>
<p>从第二张图可以看出，Flutter 主要整体分为两层，一个是 Engine 底层，另一个就是 Framework 层。当然我们最常接触和调用 API 的层级当然就是 Framework 层级了，所以对 Engine 层我们先大体了解下就可以了，本课程主要学习和分析的就是 Framework 层。了解和学习 Flutter SDK 的整体结构层级和 Widget 分类及作用，对我们学习 Flutter 开发，以及后续深入的学习研究帮助非常大，所以建议大家对本章节认真学习，巩固一下基础。</p>
<p>我们来看 Flutter Framework 层级。</p>
<p>这里先给大家看下 Flutter SDK 源码里的结构层级：</p>
<p><img src="https://images.gitbook.cn/FgFYpcINlEUnq20uAXiW7ai6phfQ" alt="Flutter Framework 3" /></p>
<p><img src="https://images.gitbook.cn/Fkd-YWJfyfAFczhCbOoeZ1KbYt-8" alt="Flutter Framework 4" /></p>
<p>从之前的官方结构图中大致可以看到，Framework 层中最底层是 Foundation 模块。我们看下 Flutter SDK 源码里 Foundation 模块里都有哪些类：</p>
<p><img src="https://images.gitbook.cn/Fq6XmO8t7XBe20Cw-_3-gvZTuBn7" alt="Flutter Framework" /></p>
<p>从 Foundation 模块里这些类可以看出 Foundation 模块部分主要是负责 Flutter 基础部分，如：注解、断言、基础类型父类、集合、绑定、更新通知、key、编码等等基础部分。关于基础部分，我们在开发中可能涉及到的机会不是太多，所以我们先对其有一个大致概念，不会太详细分析这部分。</p>
<p>再来看 Foundation 的上一层级部分：Animation、Painting、Gestures。</p>
<p>我们看下 Animation 里面都有哪些 Widget：</p>
<p><img src="https://images.gitbook.cn/FqdpPMgGyPTRh2kWiqjHgNP_p5xf" alt="Flutter Framework" /></p>
<p>Animation 里主要是放置一些 Flutter 动画相关的 API Widget，我们使用的动画相关 Widget 类都在这里，如animation.dart、animation_controller.dart（动画控制类）、curves.dart、tween.dart。后续章节的动画学习将会引入这些类的使用，大家可以先大概了解下即可。</p>
<p>接下来是 Painting 模块下都有哪些 Widget：</p>
<p><img src="https://images.gitbook.cn/Fh6EByD1vG3k_IpcNPLtjar6-6mW" alt="Flutter Framework" /></p>
<p>可以从图中看到，Painting 里主要是一些边框绘制、颜色、裁剪图像处理、画笔、插值器等跟绘制、图像、装饰相关的类。里面的如：alignment.dart、box_decoration.dart、colors.dart、decoration.dart、edge_insets.dart、image_provider.dart、text_style.dart、text_painter.dart 后面都会使用到。</p>
<p>最后说到 Gestures 模块，顾名思义里面应该是跟手势处理相关的 Widget 类，先看下结构图片：</p>
<p><img src="https://images.gitbook.cn/FkxeYsNevwB8XFx4PlfrYttDQdk9" alt="Flutter Framework" /></p>
<p>这里面基本上涵盖拖拽操作 Widget、事件类、长按、触摸、放大等等。里面的如：drag.dart、events.dart、long_press.dart、multidrag.dart、multitap.dart、tag.dart、scale.dart 后面也会或多或少接触到。</p>
<p>了解完这一层之后，我们再往 Framework 的上一层看，Rendering 模块层。</p>
<p>首先是 SDK 里的内容：</p>
<p><img src="https://images.gitbook.cn/Fg8f_uUlkWkf8LqCNK3XmNaerEZb" alt="Flutter Framework" /></p>
<p>Rendering 可以看做是渲染库，是 Widget 的父类基础。里面涵盖一些渲染树，如：flex.dart、flow.dart、image.dart、sliver.dart、stack.dart、table.dart、view.dart 等等，是很多渲染 Widget 的基础库。</p>
<p>再往上看，Rendering 的上一层是 Widget 层，Widget 层是依赖 Rendering 层进行构建的，SDK 结构如下：</p>
<p><img src="https://images.gitbook.cn/FlBq6uake3CTI-7sf2qhtPioO0aN" alt="Flutter Framework" /></p>
<p>可以看到这里面的相关 Widget 类非常多，因为 Flutter 里所有的类都可以看做 Widget，而 Widget 也是 Flutter 的核心，所以我们需要掌握的大部分都是 Widget 的用法和构建。这里面的很多都是常用 Widget，我们后面也会详细学习讲解，也有一些是最上层模块的基础类，这里常用的如：app.dart、container.dart、bottom_navigation_bar_item.dart、editable_text.dart、form.dart、gesture_detector.dart、icon.dart、image.dart、navigator.dart、page_view.dart、routes.dart、scroll_view.dart、sliver.dart、spacer.dart、text.dart等等。</p>
<p>来到 Flutter Framework 的最顶层模块，Material 和 Cupertino。</p>
<p>这两个模块分别对应 Android 平台的风格的 Material Widget 和 iOS 平台风格的扁平化 Widget。这样我们就可以很直接方便地使用这两套风格的 Widget 去分别构建符合 Android 和 iOS 风格的应用了。</p>
<p>我们看 Material 源码结构：</p>
<p><img src="https://images.gitbook.cn/Fmoi88HjakJBCWaDupdQ86yHZB72" alt="Flutter Framework" /></p>
<p>可以看到，Material 模块里关于 Material 的风格的 Widget 也非常多，大部分都是我们常用的，后续我们也会详细学习。常用的如：app_bar.dart、button.dart、bottom_app_bart.dart、bottom_navigation_bar.dart、card.dart、colors.dart、data_table.dart、dialog.dart、icons.dart、snack_bar.dart、scaffold.dart、text_field.dart、theme.dart 等等。</p>
<p>接下来 Cupertino 模块里的 Widget：</p>
<p><img src="https://images.gitbook.cn/FvmBRr3rut89O5VpeBDYkTaAHxOh" alt="Flutter Framework" /></p>
<p>可以看到里面的 Cupertino 风格的 Widget 目前并不多，但是 Google 官方 Flutter 团队还在扩充完善。常用的如：action_sheet.dart、bottom_tab_bar.dart、button.dart、colors.dart、dialog.dart、icons.dart、nav_bar.dart、page_scaffold.dart、tab_scaffold.dart、tab_view.dart、text_field.dart、theme.dart 等等。这里就先不详细讲解了，只大概了解目录结构即可。</p>
<h3 id="2flutterwidget">2 Flutter 的 Widget 分类</h3>
<p>介绍了 Flutter 的整体 SDK 结构后，我们着重说说 Flutter 的核心——Widget 的分类。</p>
<p>先看一张官方图：</p>
<p><img src="https://images.gitbook.cn/Ft06Pki12EkIUT-IrLZeUXPKeUZt" alt="Flutter Widget" /></p>
<p>可以看出 Widget 主要分为 StatelessWidget 和 StatefulWidget。分别是无状态 Widget 和有状态 Widget。无状态 Widget 主要是那些无需更新页面显示状态的、无可变状态维护功能的 Widget，如 Text、Icon 等 Widget，只负责显示。而有状态 Widget 主要是组件可以自己维护状态、更新渲染内容，如 Image、Form、TextField 等等。</p>
<p>说了这么多，上一张大致的 Widget 目录分类吧：</p>
<p><a href="https://flutter.dev/docs/development/ui/widgets">Flutter widgets</a></p>
<p><img src="https://images.gitbook.cn/Fl3hAgE-ivb9Fmpy2q7Kzo5hsXXx" alt="Flutter Widget" /></p>
<p>主要将 Widget 分为以下这些类。</p>
<ul>
<li><p>基础组件 Widget（Basics）：</p>
<p>Container、Row、Column、Image、Text、Icon、RaisedButton、Scaffold、Appbar、FlutterLogo、Placeholder</p></li>
<li><p>Material Components：</p></li>
<li><p>App 结构和导航类</p>
<p>Scaffold、Appbar、BottomNavigationBar、TabBar、TabBarView、MaterialApp、WidgetsApp、Drawer、SliverAppBar</p></li>
<li><p>按钮类</p>
<p>RaisedButton、FloatingActionButton、FlatButton、IconButton、DropdownButton、PopupMenuButton、ButtonBar</p></li>
<li><p>输入和选择类</p>
<p>TextField、Checkbox、Raido、Switch、Slider、Date&amp;Time Pickers</p></li>
<li><p>对话框和控制面板类</p>
<p>SimpleDialog、AlertDialog、BottomSheet、ExpansionPanel、SnackBar）；信息显示类（Image、Icon、Chip、Tooltip、DataTable、Card、LinearProgressIndicator、CircularProgressIndicator、GridView</p></li>
<li><p>布局类</p>
<p>ListTile、Stepper、Divider</p></li>
<li><p>Cupertino （iOS-style widgets）：</p>
<p>CupertinoActionSheet、CupertinoActivityIndicator、CupertinoAlertDialog、CupertinoButton、CupertinoDatePicker、CupertinoDialog、CupertinoDialogAction、CupertinoFullscreenDialogTransition、CupertinoPageScaffold、CupertinoPageTransition、CupertinoPicker、CupertinoPopupSurface、CupertinoSegmentedControl、CupertinoSlider、CupertinoSwitch、CupertinoNavigationBar、CupertinoTabBar、CupertinoTabScaffold、CupertinoTabView、CupertinoTextField、CupertinoTimerPicker</p></li>
<li><p>Layout：</p></li>
<li><p>单个子元素的布局 Widget</p>
<p>Container、Padding、Center、Align、FittedBox、AspectRatio、ConstrainedBox、Baseline、FractionallySizedBox、IntrinsicHeight、IntrinsicWidth、LimitedBox、Offstage、OverflowBox、SizedBox、SizedOverflowBox、Transform、CustomSingleChildLayout</p></li>
<li><p>多个子元素的布局 Widget</p>
<p>Row、Column、Stack、IndexedStack、GridView、Flow、Table、Wrap、ListBody、CustomMultiChildLayout、LayoutBuilder、ListView、Expanded</p></li>
<li><p>Text 文本显示类：</p>
<p>Text、RichText、DefaultTextStyle</p></li>
<li><p>Assets、图片、Icons 类：</p>
<p>Image、Icon、RawImage、AssetBundle</p></li>
<li><p>Input 输入类：</p>
<p>Form、FormField、RawKeyboardListener</p></li>
<li><p>动画和 Motion 类：</p>
<p>AnimatedContainer、AnimatedCrossFade、Hero、AnimatedBuilder、DecoratedBoxTransition、FadeTransition、PositionedTransition、RotationTransition、ScaleTransition、SizeTransition、SlideTransition、AnimatedDefaultTextStyle、AnimatedListState、AnimatedModalBarrier、AnimatedOpacity、AnimatedPhysicalModel、AnimatedPositioned、AnimatedSize、AnimatedWidget、AnimatedWidgetBaseState</p></li>
<li><p>交互模型类：</p></li>
<li><p>触摸交互</p>
<p>Draggable、LongPressDraggable、GestureDetector、DragTarget、Dismissible、IgnorePointer、AbsorbPointer、Scrollable</p></li>
<li><p>路由导航</p>
<p>Hero、Navigator</p></li>
<li><p>样式类：</p>
<p>Padding、Theme、MediaQuery</p></li>
<li><p>绘制和效果类：</p>
<p>Transform、Opacity、DecoratedBox、FractionalTranslation、RotatedBox、ClipOval、ClipPath、ClipRect、CustomPaint、BackdropFilter</p></li>
<li><p>Async 异步模型类：</p>
<p>FutureBuilder、StreamBuilder</p></li>
<li><p>滚动类：</p>
<p>GridView、ListView、NestedScrollView、SingleChildScrollView、Scrollable、Scrollbar、CustomScrollView、NotificationListener、ScrollConfiguration、RefreshIndicator、PageView</p></li>
<li><p>辅助功能类：</p>
<p>Semantics、MergeSemantics、ExcludeSemantics</p></li>
</ul>
<p>内容比较多，官方分类主要是这些，希望大家可以认真学习，这对学习 Widget 非常有用。</p>
<p>看了官方的分类后，我这里也给大家整理了一些分类结构图：</p>
<p><img src="https://images.gitbook.cn/FlOkMR8qN2K07EG0J69eMEw-IroG" alt="Flutter Widget" /></p>
<p>这张图有点大，所以我分部分展示：</p>
<p><img src="https://images.gitbook.cn/FiMKcESyJCJ03m4moGaWX50pvg4-" alt="Flutter Widget 1" /></p>
<p><img src="https://images.gitbook.cn/Fq-s9F-8LEhSOK6E4VkOPUa7zeqw" alt="Flutter Widget 2" /></p>
<p><img src="https://images.gitbook.cn/Fldl6LCx18hQxxHXnGH1d0WIuL2N" alt="Flutter Widget 3" /></p>
<p><img src="https://images.gitbook.cn/Fhv4Zy-IsEyf9a0-6tMQ7D5myYH9" alt="Flutter Widget 4" /></p>
<p>那么关于 Flutter 的 Widget 的结构和分类上都给大家提到了，后续的学习将会挑重点的 Widget 进行讲解。</p>
<p>本节课相关图片存放地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_06">flutter_06</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解 Flutter 的 Widget 结构概览和分类，为后续的 Flutter 的开发学习奠定基础，熟悉 Widget 的分类可以更加有利于我们掌握 Widget 的特点和用法用途。本节课主要注意点和建议如下：</p>
<ul>
<li>建议仔细阅读和理解这些分类内容和核心 Widget，大致了解它们的用途。</li>
<li>结构图已经保存在本课程 GitHub 上，大家可以保存一下这些图片，用于随时查看阅读。</li>
</ul></div></article>