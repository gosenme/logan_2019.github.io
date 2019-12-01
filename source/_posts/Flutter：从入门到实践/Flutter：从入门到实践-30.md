---
title: Flutter：从入门到实践-30
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用 Flutter 开发的过程中，有时候现有的 Widget 不能满足需求，所以需要自定义 Widget，有点像 Android 和 iOS 平台的自定义 View，来实现我们的各种效果。Flutter 也是支持自定义 Widget 组件的，原理和方法类似于其他平台。这节课我们将介绍 Flutter 中自定义 Widget 的几种实现方式并配合例子，同时也会讲解一下 Flutter 方法的封装。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 自定义 Widget 的方式</li>
  <li>Widget 的继承实现自定义</li>
  <li>Widget 的组合实现自定义</li>
  <li>CustomPaint 绘制 Widget</li>
  <li>Flutter 方法的封装</li>
  </ul>
</blockquote>
<h3 id="1flutterwidget">1 Flutter 自定义 Widget 的方式</h3>
<p>当我们在实际开发中，可能 Flutter 的基础 Widget 组件并不能满足我们的需求，这时我们就需要自定义 Widget 来实现我们的需求。</p>
<p>Flutter 有多种实现自定义 Widget 的方式：</p>
<ul>
<li>通过继承 Widget 来修改和扩展它的功能；</li>
<li>通过组合 Widget 来扩展功能；</li>
<li>使用 CustomPaint 绘制自定义 Widget。</li>
</ul>
<p>这几种方式都有各自的优势和特点，相对来说 CustomPaint 绘制实现自定义是这里面比较复杂的一种自定义 Widget 方式。Flutter 中的很多基础 Widget 也是通过继承 Widget 进行扩展形成新的 Widget 或者是自己绘制 Widget。其实在大部分的平台都存在 Canvas 这个对象，它可以实现绘制布局、组件等功能，当然 Flutter 也可以通过 Canvas 来实现 Widget 的绘制。自定义Widget 在开发中也非常常见，例如：我们可以自定义封装实现一个加载中的对话框、实现一个通用的 ToolBar 等等。</p>
<p>那么接下来我们就开始进入 Flutter 自定义 Widget 的学习。</p>
<h3 id="2widget">2 Widget 的继承实现自定义</h3>
<p>首先我们看下通过 Widget 的继承来实现自定义 Widget 组件。这种例子在 Flutter 中不在少数，例如：NetworkImage 和 AssetImage 都是继承 ImageProvider 来实现不同场景功能的、Center 是继承自 Align 来实现的等等。所以我们可以根据具体的使用场景、特点来选择基础 Widget 进行继承，从而实现我们想要的功能。</p>
<p>这里我们实践一下如何通过继承来实现 Widget。首先我们看一个官方的源码案例，Dialog 这个 Widget 是继承自 StatelessWidget 来进行扩展实现的基础 Widget。我们看下里面的大概内容：</p>
<pre><code class="dart language-dart">// 继承自StatelessWidget
class Dialog extends StatelessWidget {
  // 构造方法，设置传参
  const Dialog({
    Key key,
    this.backgroundColor,
    this.elevation,
    this.insetAnimationDuration = const Duration(milliseconds: 100),
    this.insetAnimationCurve = Curves.decelerate,
    this.shape,
    this.child,
  }) : super(key: key);

  // 设置属性
  final Color backgroundColor;

  final double elevation;

  final Duration insetAnimationDuration;

  final Curve insetAnimationCurve;

  final ShapeBorder shape;

  final Widget child;

  static const RoundedRectangleBorder _defaultDialogShape =
    RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(2.0)));
  static const double _defaultElevation = 24.0;
  // 构建布局样式
  @override
  Widget build(BuildContext context) {
    final DialogTheme dialogTheme = DialogTheme.of(context);
    // 具体构建布局样式
    return AnimatedPadding(
      padding: MediaQuery.of(context).viewInsets + const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0),
      duration: insetAnimationDuration,
      curve: insetAnimationCurve,
      child: MediaQuery.removeViewInsets(
        removeLeft: true,
        removeTop: true,
        removeRight: true,
        removeBottom: true,
        context: context,
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(minWidth: 280.0),
            child: Material(
              color: backgroundColor ?? dialogTheme.backgroundColor ?? Theme.of(context).dialogBackgroundColor,
              elevation: elevation ?? dialogTheme.elevation ?? _defaultElevation,
              shape: shape ?? dialogTheme.shape ?? _defaultDialogShape,
              type: MaterialType.card,
              child: child,
            ),
          ),
        ),
      ),
    );
  }
}
</code></pre>
<p>怎么样，是不是很简单？所以我们也可以按照这个模式来进行继承扩展我们的一个简单功能的组件。</p>
<p>这里我们继承 Dialog 来实现一个简单的加载中效果的对话框。</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

// 继承我们的Dialog组件，这样它就具有Dialog的一些特性和方法属性
class LoadingDialog extends Dialog {
  String text;

  // 建立构造方法，传递参数
  LoadingDialog({Key key, @required this.text}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // 具体构建逻辑
    return Material(
      type: MaterialType.transparency,
      child: Center(
        child: SizedBox(
          width: 120.0,
          height: 120.0,
          child: Container(
            decoration: ShapeDecoration(
              color: Color(0xffffffff),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.all(
                  Radius.circular(8.0),
                ),
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: &lt;Widget&gt;[
                CircularProgressIndicator(),
                Padding(
                  padding: const EdgeInsets.only(
                    top: 20.0,
                  ),
                  child: Text(
                    text,
                    style: TextStyle(fontSize: 12.0),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// 调用使用的地方
class CustomWidgetSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return CustomWidgetSamplesState();
  }
}

class CustomWidgetSamplesState extends State&lt;CustomWidgetSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('CustomWidget'), primary: true),
        body: Container(
          child: Align(
            alignment: Alignment.center,
            // 构造并传递参数
            child: LoadingDialog(text: '加载中...'),
          ),
        ));
  }
}

// 我们只需传递我们的text参数即可
LoadingDialog(text: '加载中...'),
</code></pre>
<p>运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/Ftgg3ozvno7Y74uhRJbls3JxZ4mF" alt="自定义Dialog效果图" /></p>
<p>当然，我们也可以继承 StatefulWidget 或 StatelessWidget 进行自定义 Widget。</p>
<h3 id="3widget">3 Widget 的组合实现自定义</h3>
<p>接下来我们看下通过 Widget 组合来实现自定义组件。</p>
<p>Widget 组合，顾名思义，就是将各种 Flutter 的基础 Widget，进行不同的选择、组合拼装，来实现一个可以满足我们需求的、新的 Widget。Flutter 的基础 Widget 中，也有很多是通过组合来实现的。</p>
<p>我们看一个实例，实现一个自定义的 ToolBar：</p>
<pre><code class="dart language-dart">// 自定义一个ToolBar
import 'package:flutter/material.dart';

class ToolBar extends StatefulWidget implements PreferredSizeWidget {
  // 构造方法，设置传递参数
  ToolBar({@required this.onTap}) : assert(onTap != null);
  // 属性参数，点击回调
  final GestureTapCallback onTap;

  @override
  State createState() {
    return ToolBarState();
  }
  // AppBar需要实现PreferredSizeWidget
  @override
  Size get preferredSize {
    return Size.fromHeight(56.0);
  }
}

class ToolBarState extends State&lt;ToolBar&gt; {
  @override
  Widget build(BuildContext context) {
    // 设置布局
    return SafeArea(
      top: true,
      child: Container(
        color: Colors.blue,
        child: Row(
          children: &lt;Widget&gt;[
            Icon(
              Icons.menu,
              color: Colors.white,
              size: 39,
            ),
            Expanded(
              child: Container(
                color: Colors.white,
                padding: EdgeInsets.all(5),
                margin: EdgeInsets.all(5),
                child: Text(
                  '搜索...',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
            GestureDetector(
              onTap: this.widget.onTap,
              child: Icon(
                Icons.photo_camera,
                color: Colors.white,
                size: 39,
              ),
            )
          ],
        ),
      ),
    );
  }
}

// 调用自定义ToolBar
class CustomWidgetSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return CustomWidgetSamplesState();
  }
}

class CustomWidgetSamplesState extends State&lt;CustomWidgetSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // 设置自定义ToolBar
        appBar:ToolBar(
          onTap: () {
            print('click');
          },
        ),
        primary: true,
        body: Column(
          children: &lt;Widget&gt;[
            Container(
              child: Align(
                alignment: Alignment.center,
                child: LoadingDialog(text: '加载中...'),
              ),
            )
          ],
        ));
  }
}
</code></pre>
<p>运行效果图如下：</p>
<p><img src="https://images.gitbook.cn/Fgs9Kd87j3-vvHhga_EiTsSkGP8x" alt="自定义ToolBar效果图" /></p>
<h3 id="4custompaintwidget">4 CustomPaint 绘制 Widget</h3>
<p>最后，我们看下如何通过 CustomPaint 来实现一个自定义 Widget。CustomPaint 是通过绘制来实现的，比较复杂，也因此可以实现很多复杂的效果，例如：绘制一些不规则的图形、组件、布局、图表等等。</p>
<p>Flutter 中通过 CustomPaint 来实现绘制，而其他平台一般会通过 Canvas 或 Paint 来实现。</p>
<p>CustomPaint 继承自 SingleChildRenderObjectWidget，我们先看下 CustomPainter 的构造方法：</p>
<pre><code class="dart language-dart">const CustomPaint({
    Key key,
    // CustomPainter背景
    this.painter,
    // CustomPainter前景画笔
    this.foregroundPainter,
    // 画布尺寸，
    this.size = Size.zero,
    // 是否是复杂的绘制，Flutter会设置一些缓存优化策略
    this.isComplex = false,
    // 下一帧是否会改变
    this.willChange = false,
    // 子元素，可以为空
    Widget child,
  })
</code></pre>
<p>绘制的核心就是自定义 CustomPainter，我们简单看下 CustomPainter 里面的方法结构：</p>
<pre><code class="dart language-dart">class Sky extends CustomPainter {
  // 绘制方法
  @override
  void paint(Canvas canvas, Size size) {
    // canvas为画布
    // size为画布大小
  }

  // 刷新布局时是否重绘，可以根据实际情况进行返回值
  @override
  bool shouldRepaint(Sky oldDelegate) =&gt; false;

}

 // Canvas和其他平台的Canvas功能和作用基本一样，包含很多绘制方法

  void save() native 'Canvas_save';

  void saveLayer(Rect bounds, Paint paint);

  void _saveLayerWithoutBounds(List&lt;dynamic&gt; paintObjects, ByteData paintData)
      native 'Canvas_saveLayerWithoutBounds';

  void restore() native 'Canvas_restore';

  int getSaveCount() native 'Canvas_getSaveCount';

  void translate(double dx, double dy) native 'Canvas_translate';

  void scale(double sx, [double sy]) =&gt; _scale(sx, sy ?? sx);

  void rotate(double radians) native 'Canvas_rotate';

  void skew(double sx, double sy) native 'Canvas_skew';

  void transform(Float64List matrix4);

  void clipRect(Rect rect, { ClipOp clipOp: ClipOp.intersect, bool doAntiAlias = true });

  void clipRRect(RRect rrect, {bool doAntiAlias = true});

  void clipPath(Path path, {bool doAntiAlias = true});

  void drawColor(Color color, BlendMode blendMode);

  void drawLine(Offset p1, Offset p2, Paint paint);

  void drawPaint(Paint paint);

  void drawRect(Rect rect, Paint paint);

  void drawRRect(RRect rrect, Paint paint);

  void drawDRRect(RRect outer, RRect inner, Paint paint);

  void drawOval(Rect rect, Paint paint);

  void drawCircle(Offset c, double radius, Paint paint);

  void drawArc(Rect rect, double startAngle, double sweepAngle, bool useCenter, Paint paint);

  void drawPath(Path path, Paint paint);

  void drawImage(Image image, Offset p, Paint paint);

  void drawImageRect(Image image, Rect src, Rect dst, Paint paint);

  void drawImageNine(Image image, Rect center, Rect dst, Paint paint);

  void drawPicture(Picture picture);

  void drawParagraph(Paragraph paragraph, Offset offset);

  void drawPoints(PointMode pointMode, List&lt;Offset&gt; points, Paint paint);

  void drawRawPoints(PointMode pointMode, Float32List points, Paint paint);

  void drawVertices(Vertices vertices, BlendMode blendMode, Paint paint);

  void drawAtlas(Image atlas,
                 List&lt;RSTransform&gt; transforms,
                 List&lt;Rect&gt; rects,
                 List&lt;Color&gt; colors,
                 BlendMode blendMode,
                 Rect cullRect,
                 Paint paint);

  void drawRawAtlas(Image atlas,
                    Float32List rstTransforms,
                    Float32List rects,
                    Int32List colors,
                    BlendMode blendMode,
                    Rect cullRect,
                    Paint paint);

  void drawShadow(Path path, Color color, double elevation, bool transparentOccluder);
</code></pre>
<p>在进行 Canvas 画布绘制时，我们就需要画笔 Paint，我们需要创建相应的画笔来绘制到 Canvas 上。Paint 画笔也有很多可以设置的属性，常用的有：</p>
<pre><code class="dart language-dart">color：画笔颜色
style：绘制模式，画线 or 充满
maskFilter：绘制完成，还没有被混合到布局上时，添加的遮罩效果，比如blur效果
strokeWidth：线条宽度
strokeCap：线条结束时的绘制样式
shader：着色器，一般用来绘制渐变效果或ImageShader
... ...

// 可以这样使用
Paint myPaint = Paint()
    ..color = Colors.blueAccent // 画笔颜色
    ..strokeCap = StrokeCap.round // 画笔笔触类型
    ..isAntiAlias = true // 是否启动抗锯齿
    ..blendMode = BlendMode.exclusion // 颜色混合模式
    ..style = PaintingStyle.fill // 绘画风格，默认为填充
    ..colorFilter = ColorFilter.mode(Colors.blueAccent,
        BlendMode.exclusion) // 颜色渲染混合模式
    ..maskFilter = MaskFilter.blur(BlurStyle.inner, 2.0) // 模糊遮罩效果
    ..filterQuality = FilterQuality.high // 颜色渲染模式的质量
    ..strokeWidth = 10.0; // 画笔的宽度
</code></pre>
<p>在了解了这些后，我们来实现一个通过 CustomPaint 自定义的 Widget 就比较容易了：</p>
<pre><code class="dart language-dart">class CustomWidgetSamplesState extends State&lt;CustomWidgetSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('CustomWidget'),
        ),
        body: Column(
          children: &lt;Widget&gt;[
            CustomPaint(
              painter: Sky(),
              child: Center(
                child: Text(
                  '文字',
                ),
              ),
            )
          ],
        ));
  }
}

class Sky extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    // 绘制圆角矩形
    // 用Rect构建一个边长50,中心点坐标为150,150的矩形
    Rect rectCircle =
        Rect.fromCircle(center: Offset(150.0, 150.0), radius: 60.0);
    // 根据上面的矩形,构建一个圆角矩形
    RRect rrect = RRect.fromRectAndRadius(rectCircle, Radius.circular(30.0));
    canvas.drawRRect(rrect, Paint()..color = Colors.yellow);
  }

  @override
  bool shouldRepaint(Sky oldDelegate) =&gt; false;
  @override
  bool shouldRebuildSemantics(Sky oldDelegate) =&gt; false;
}
</code></pre>
<p>运行效果图如下：</p>
<p><img src="https://images.gitbook.cn/Fv3VIwAnVPZ_BQAHcldm8JQKqu8-" alt="CustomPaint效果图" /></p>
<p>通过 CustomPaint 我们可以实现很多自定义的绘制，可以绘制各种各样复杂的图形、图案等等，大家自己可以尝试下。</p>
<h3 id="5flutter">5 Flutter 方法的封装</h3>
<p>同很多编程语言一样，Flutter 也支持一些工具类、方法的封装，方便我们进行使用，使代码逻辑清晰等。Flutter 的方法封装和 Java 有点像，我们这里直接创建一个工具类来展示：</p>
<pre><code class="dart language-dart">import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

class Utils {
  BuildContext context;

  // 可以设置构造方法，传递参数，参数传递时有区别，通过key:value形式
  Utils({@required this.context}) : assert(context != null);

  // 首先指定返回类型，然后定义方法名
  ///获取时间戳毫秒数,13位
  int getMilliseconds() {
    return DateTime.now().millisecondsSinceEpoch;
  }
  // 方法名后可以设置传递的参数
  ///复制到剪贴板
  void setClipData(String text) {
    Clipboard.setData(ClipboardData(text: text));
  }

  // 以下划线开始的方法名这个类的外部不可以调用，只能内部进行调用使用
  ///获取屏幕宽度
  double _getScreenWidth(BuildContext context) {
    return MediaQuery.of(context).size.width;
  }

  ///获取屏幕高度
  double getScreenHeight(BuildContext context) {
    return MediaQuery.of(context).size.height;
  }

  ///获取屏幕状态栏高度
  double getStatusBarTop(BuildContext context) {
    return MediaQuery.of(context).padding.top;
  }

  ///获取屏幕方向
  Orientation getScreenOrientation(BuildContext context) {
    return MediaQuery.of(context).orientation;
  }

  Future&lt;String&gt; getBatteryLevel() async {
    var batteryLevel = 'unknown';
    MethodChannel methodChannel = MethodChannel('samples.flutter.io/battery');
    try {
      int result = await methodChannel.invokeMethod('getBatteryLevel');
      batteryLevel = 'Battery level: $result%';
    } on PlatformException {
      batteryLevel = 'Failed to get battery level.';
    }
    return batteryLevel;
  }
}

// 使用时，构造方法传参通过key：value形式传递设置
Utils utils = Utils(context: context);

// 调用方法
utils.getScreenHeight(context);
</code></pre>
<p>好啦，这样就实现了基本的方法封装！</p>
<p>本节课的实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_27">flutter_27</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的自定义 Widget 的三种方式，其中，前两种方式大致相同，大家可以自己练习一下。此外，我们还说了 Flutter 的方法的封装。</p>
<p>今天的课后作业是：尝试使用 CustomPaint 绘制一个复杂的控件。遇到问题欢迎在交流群里提出和讨论。</p>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>