---
title: Flutter：从入门到实践-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面已经讲解了大量的 Flutter 相关基础知识，从这节课开始，我们将进行 Flutter 的系列 Widget、布局的学习。那么这节课就带领大家对 Flutter 的基础 Widget 中的几个典型，结合案例来讲解用法。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Text Widget 用法详解</li>
  <li>Image Widget 用法详解</li>
  <li>Button Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="1textwidget">1 Text Widget 用法详解</h3>
<p>首先我们看 Text Widget 的作用：</p>
<p>Text Widget，从名字也可以看出，在 Flutter 里是用来负责显示文本信息的一个组件，功能类似于 Android 的TextView、HTML 的一些文本标签等等，属于基础组件。</p>
<p>那么知道了它的作用后，我们再看下 Text 这个组件的继承关系：</p>
<p><strong>Text -> StatelessWidget -> Widget -> DiagnosticableTree -> Diagnosticable -> Object</strong></p>
<p>可以看出 Text 是个 StatelessWidget，也就是无状态组件。</p>
<p>接下来看下 Text Widget 的类结构：</p>
<p><img src="https://images.gitbook.cn/FuOFqwhyd9HKU_kUAtWoyrEzJwdS" alt="Text Widget类结构" /></p>
<p>可以看出有 2 个构造方法，拥有多个属性参数（f 标志的为属性参数）。</p>
<p>那么我们就重点看下 Text 组件的两个比较重要的构造方法的作用和属性的含义和作用：</p>
<pre><code class="dart language-dart">const Text(
    //要显示的文字内容
    this.data, 
   {
    //key类似于id
    Key key,
    //文字显示样式和属性
    this.style,
    this.strutStyle,
    //文字对齐方式
    this.textAlign,
    //文字显示方向
    this.textDirection,
    //设置语言环境
    this.locale,
    //是否自动换行
    this.softWrap,
    //文字溢出后处理方式
    this.overflow,
    //字体缩放
    this.textScaleFactor,
    //最大显示行数
    this.maxLines,
    //图像的语义描述，用于向Andoid上的TalkBack和iOS上的VoiceOver提供图像描述
    this.semanticsLabel,
  })
</code></pre>
<p>其中 data 属性是非空的，必须有的参数，传入要显示的 String 类型的字符串。</p>
<p>这里的 style 属性比较常用，传入的是 TextStyle 对象，我们先细看下它可以配置哪些属性样式：</p>
<pre><code class="dart language-dart">const TextStyle({
    //是否继承父类组件属性
    this.inherit = true,
    //字体颜色
    this.color,
    //文字大小，默认14px
    this.fontSize,
    //字体粗细
    this.fontWeight,
    //字体样式,normal或italic
    this.fontStyle,
    //字母间距，默认为0，负数间距缩小，正数间距增大
    this.letterSpacing,
    //单词间距，默认为0，负数间距缩小，正数间距增大
    this.wordSpacing,
    //字体基线
    this.textBaseline,
    //行高
    this.height,
    //设置区域
    this.locale,
    //前景色
    this.foreground,
    //背景色
    this.background,
    //阴影
    this.shadows,
    //文字划线，下换线等等装饰
    this.decoration,
    //划线颜色
    this.decorationColor,
    //划线样式，虚线、实线等样式
    this.decorationStyle,
    //描述信息
    this.debugLabel,
    //字体
    String fontFamily,
    List&lt;String&gt; fontFamilyFallback,
    String package,
  })
</code></pre>
<p>接下来再看另一个构造方法 Text.rich(...) 。</p>
<p>这个的作用就是可以在 Text 里加入一些 Span 标签，对某部分文字进行个性化改变样式，如加入 @ 符号，加入超链接、变色、加表情等等。Text.rich(…) 等价于 RichText(...)，用哪个都可以。</p>
<pre><code class="dart language-dart">// 里面的属性前面都介绍过，这里就不重复介绍了
const Text.rich(
    // 样式片段标签TextSpan
    this.textSpan,
  {
    Key key,
    this.style,
    this.strutStyle,
    this.textAlign,
    this.textDirection,
    this.locale,
    this.softWrap,
    this.overflow,
    this.textScaleFactor,
    this.maxLines,
    this.semanticsLabel,
  })


const RichText({
    Key key,
    // 样式片段标签TextSpan
    @required this.text,
    this.textAlign = TextAlign.start,
    this.textDirection,
    this.softWrap = true,
    this.overflow = TextOverflow.clip,
    this.textScaleFactor = 1.0,
    this.maxLines,
    this.locale,
    this.strutStyle,
  })
</code></pre>
<p>我们看下样式标签 TextSpan 的构造方法：</p>
<pre><code class="dart language-dart">const TextSpan({
    //样式片段
    this.style,
    //要显示的文字
    this.text,
    //样式片段TextSpan数组，可以包含多个TextSpan
    this.children,
    //用于手势进行识别处理,如点击跳转
    this.recognizer,
  })
</code></pre>
<p>那么关于 Text 的大部分功能和属性都讲到了，接下来通过一个实例来演示下用法：</p>
<pre><code class="dart language-dart">// 给出部分核心代码
body: Container(
      child: Column(
        children: &lt;Widget&gt;[
          Text('Text最简单用法'),
          Text('Text Widget',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 18,
                decoration: TextDecoration.none,
              )),
          Text('放大加粗文字',
              textDirection: TextDirection.rtl,
              textScaleFactor: 1.2,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
                color: Colors.black,
                decoration: TextDecoration.none,
              )),
          Text(
              '可以缩放自动换行的文字，可以缩放自动换行的文字，可以缩放自动换行的文字，可以缩放自动换行的文字，可以缩放自动换行的文字，可以缩放自动换行的文字',
              textScaleFactor: 1.0,
              textAlign: TextAlign.center,
              softWrap: true,
              //渐隐、省略号、裁剪
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
                color: Colors.black,
                decoration: TextDecoration.none,
              )),
          Text.rich(TextSpan(
            text: 'TextSpan',
            style: TextStyle(
              color: Colors.orange,
              fontSize: 30.0,
              decoration: TextDecoration.none,
            ),
            children: &lt;TextSpan&gt;[
              new TextSpan(
                text: '拼接1',
                style: new TextStyle(
                  color: Colors.teal,
                ),
              ),
              new TextSpan(
                text: '拼接2',
                style: new TextStyle(
                  color: Colors.teal,
                ),
              ),
              new TextSpan(
                text: '拼接3有点击事件',
                style: new TextStyle(
                  color: Colors.yellow,
                ),
                recognizer: new TapGestureRecognizer()
                  ..onTap = () {
                    //增加一个点击事件
                    print(
                        '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@');
                  },
              ),
            ],
          )),
          RichText(
            text: TextSpan(
              text: 'Hello ',
              style: DefaultTextStyle.of(context).style,
              children: &lt;TextSpan&gt;[
                TextSpan(
                    text: 'bold',
                    style: TextStyle(
                        fontWeight: FontWeight.bold,
                        decoration: TextDecoration.none)),
                TextSpan(
                    text: ' world!',
                    style: TextStyle(
                        fontWeight: FontWeight.bold,
                        decoration: TextDecoration.none)),
              ],
            ),
          ),
        ],
      ),
    ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FjneBo8yBCK7RGxffecjcwOZfyKb" alt="Text Widget效果" /></p>
<h3 id="2imagewidget">2 Image Widget 用法详解</h3>
<p>首先说一下 Image Widget 的作用：</p>
<p>Image Widget 在 Flutter 里是用来负责显示图片的一个组件，功能类似于 Android的ImageView、Html 的一些image 标签等等，属于基础组件。</p>
<p>Image 这个组件的继承关系：</p>
<p><strong>Image -> StatefulWidget -> Widget -> DiagnosticableTree -> Diagnosticable -> Object</strong>
可以看出 Image 是个 StatefulWidget，也就是有状态组件。</p>
<p>Image Widget 的类结构：</p>
<p><img src="https://images.gitbook.cn/FiGnqtTHNEL0kVarl_X4377KH9U_" alt="Image Widget的类结构" /></p>
<p>可以看出有 5 个构造方法，拥有多个属性参数（f标志的为属性参数）。</p>
<p>整理下，Image 支持 5 种方式加载图片。</p>
<ul>
<li>Image：通过 ImageProvider 来加载图片</li>
<li>Image.network：用来加载网络图片</li>
<li>Image.file：用来加载本地 File 文件图片</li>
<li>Image.asset：用来加载项目内资源图片</li>
<li>Image.memory：用来加载 Uint8List 资源图片/内存图片</li>
</ul>
<p>其中这几种其实都是通过 ImageProvider 来从不同源加载图片的，封装类有：NetworkImage、FileImage、AssetImage、ExactAssetImage、MemoryImage。我们既可以用这几个构造方法加载图片，也可以使用这几个封装类来加载。</p>
<p>我们重点来看 Image 组件的 5 个比较重要的构造方法的作用和属性的含义和作用：</p>
<pre><code class="dart language-dart">//通过ImageProvider来加载图片
const Image({
    Key key,
    // ImageProvider，图像显示源
    @required this.image,
    this.semanticLabel,
    this.excludeFromSemantics = false,
    //显示宽度
    this.width,
    //显示高度
    this.height,
    //图片的混合色值
    this.color,
    //混合模式
    this.colorBlendMode,
    //缩放显示模式
    this.fit,
    //对齐方式
    this.alignment = Alignment.center,
    //重复方式
    this.repeat = ImageRepeat.noRepeat,
    //当图片需要被拉伸显示的时候，centerSlice定义的矩形区域会被拉伸，类似.9图片
    this.centerSlice,
    //类似于文字的显示方向
    this.matchTextDirection = false,
    //图片发生变化后，加载过程中原图片保留还是留白
    this.gaplessPlayback = false,
    //图片显示质量
    this.filterQuality = FilterQuality.low,
  })

// 加载网络图片，封装类：NetworkImage
Image.network(
    //路径
    String src, 
   {
    Key key,
    //缩放
    double scale = 1.0,
    this.semanticLabel,
    this.excludeFromSemantics = false,
    this.width,
    this.height,
    this.color,
    this.colorBlendMode,
    this.fit,
    this.alignment = Alignment.center,
    this.repeat = ImageRepeat.noRepeat,
    this.centerSlice,
    this.matchTextDirection = false,
    this.gaplessPlayback = false,
    this.filterQuality = FilterQuality.low,
    Map&lt;String, String&gt; headers,
  })

// 加载本地File文件图片，封装类：FileImage
Image.file(
    //File对象
    File file, 
  {
    Key key,
    double scale = 1.0,
    this.semanticLabel,
    this.excludeFromSemantics = false,
    this.width,
    this.height,
    this.color,
    this.colorBlendMode,
    this.fit,
    this.alignment = Alignment.center,
    this.repeat = ImageRepeat.noRepeat,
    this.centerSlice,
    this.matchTextDirection = false,
    this.gaplessPlayback = false,
    this.filterQuality = FilterQuality.low,
  })

// 加载本地资源图片,例如项目内资源图片
// 需要把图片路径在pubspec.yaml文件中声明一下，如：
// assets:
//      - packages/fancy_backgrounds/backgrounds/background1.png
// 封装类有：AssetImage、ExactAssetImage
Image.asset(
    //文件名称，包含路径
    String name, 
  {
    Key key,
    // 用于访问资源对象
    AssetBundle bundle,
    this.semanticLabel,
    this.excludeFromSemantics = false,
    double scale,
    this.width,
    this.height,
    this.color,
    this.colorBlendMode,
    this.fit,
    this.alignment = Alignment.center,
    this.repeat = ImageRepeat.noRepeat,
    this.centerSlice,
    this.matchTextDirection = false,
    this.gaplessPlayback = false,
    String package,
    this.filterQuality = FilterQuality.low,
  })

// 加载Uint8List资源图片/从内存中获取图片显示
// 封装类：MemoryImage
Image.memory(
    // Uint8List资源图片
    Uint8List bytes,
  {
    Key key,
    double scale = 1.0,
    this.semanticLabel,
    this.excludeFromSemantics = false,
    this.width,
    this.height,
    this.color,
    this.colorBlendMode,
    this.fit,
    this.alignment = Alignment.center,
    this.repeat = ImageRepeat.noRepeat,
    this.centerSlice,
    this.matchTextDirection = false,
    this.gaplessPlayback = false,
    this.filterQuality = FilterQuality.low,
  })
</code></pre>
<p>这里对其中的 colorBlendMode 混合模式和 fit 缩放显示模式进行简单讲解下。</p>
<p>colorBlendMode 混合模式：</p>
<pre><code class="dart language-dart">// Flutter一共29种混合模式
enum BlendMode {
  clear,src,dst,srcOver,dstOver,srcIn,dstIn,srcOut,dstOut,srcATop,dstATop,xor,plus，modulate,screen,overlay,darken,lighten,colorDodge,colorBurn,hardLight,softLight,difference,exclusion,multiply,hue,saturation,color,luminosity,
}
</code></pre>
<p>主要的混合模式效果如下:</p>
<p><img src="https://images.gitbook.cn/FjyX5gudUv69suEug3EFUJ81pbCv" alt="BlendMode主要的混合模式效果" /></p>
<p>fit 缩放显示模式:</p>
<pre><code class="dart language-dart">//主要有7种
enum BoxFit {
  fill,
  contain,
  cover,
  fitWidth,
  fitHeight,
  none,
  scaleDown,
}
</code></pre>
<p>fit 缩放显示模式效果对比图如下。
fill 填充模式，拉伸充满：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fill.png" alt="" /></p>
<p>contain，全图显示，显示原比例，不需充满：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_contain.png" alt="" /></p>
<p>cover，显示可能拉伸，可能裁剪，充满：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_cover.png" alt="" /></p>
<p>fitWidth，显示可能拉伸，可能裁剪，宽度充满：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fitWidth.png" alt="" /></p>
<p>fitHeight，显示可能拉伸，可能裁剪，高度充满：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fitHeight.png" alt="" /></p>
<p>none，对图片不做任何处理显示，高出控件大小就裁剪，否则不处理：</p>
<p><img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_none.png" alt="" /></p>
<p>scaleDown，全图显示，显示原比例，不允许显示超过源图片大小，可小不可大：
  <img src="https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_scaleDown.png" alt="" /></p>
<p>那么关于 Image 的大部分功能和属性都讲到了，接下来通过一个实例来演示下用法：</p>
<pre><code class="dart language-dart">body: CustomScrollView(
        slivers: &lt;Widget&gt;[
          SliverPadding(
            padding: const EdgeInsets.all(20.0),
            sliver: SliverList(
              delegate: SliverChildListDelegate(
                &lt;Widget&gt;[
                  //从项目目录里读取图片，需要在pubspec.yaml注册路径
                  Image.asset("assets/assets_image.png"),
                  Text(
                    "项目asset目录里读取",
                    textAlign: TextAlign.center,
                  ),
                  Image(
                    image: AssetImage("assets/assets_image.png"),
                    width: 200,
                    height: 130,
                  ),
                  Text(
                    "AssetImage读取",
                    textAlign: TextAlign.center,
                  ),
                  //从文件读取图片
                  Image.file(
                    File('/sdcard/img.png'),
                    width: 200,
                    height: 80,
                  ),
                  Image(
                    image: FileImage(File('/sdcard/img.png')),
                  ),

                  ///读取加载原始图片
                  // RawImage(
                  //   image: imageInfo?.image,
                  // ),

                  ///内存中读取byte数组图片
                  /// Image.memory(bytes)
                  /// Image(
                  ///   image: MemoryImage(bytes),
                  /// ),

                  // 读取网络图片
                  Image.network(imageUrl),
                  Text(
                    "读取网络图片",
                    textAlign: TextAlign.center,
                  ),
                  Image(
                    image: NetworkImage(imageUrl),
                  ),
                  Text(
                    "用NetworkImage读取网络图片",
                    textAlign: TextAlign.center,
                  ),

                  ///加入占位图的加载图片
                  FadeInImage(
                    placeholder: AssetImage("assets/assets_image.png"),
                    image: FileImage(File('/sdcard/img.png')),
                  ),
                  Text(
                    "加入占位图的加载图片",
                    textAlign: TextAlign.center,
                  ),
                  FadeInImage.assetNetwork(
                    placeholder: "assets/assets_image.png",
                    image: imageUrl,
                  ),

                  /// FadeInImage.memoryNetwork(
                  ///   placeholder: byte,
                  ///   image: imageUrL,
                  /// ),

                  ///加载圆角图片
                  CircleAvatar(
                    backgroundColor: Colors.brown.shade800,
                    child: Text("圆角头像"),
                    backgroundImage: AssetImage("assets/assets_image.png"),
                    radius: 50.0,
                  ),
                  Text(
                    "加载圆角图片",
                    textAlign: TextAlign.center,
                  ),
                  ImageIcon(NetworkImage(imageUrl)),
                  Text(
                    "ImageIcon",
                    textAlign: TextAlign.center,
                  ),
                  ClipRRect(
                    child: Image.network(
                      imageUrl,
                      scale: 8.5,
                      fit: BoxFit.cover,
                    ),
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(20),
                      topRight: Radius.circular(20),
                    ),
                  ),
                  Text(
                    "ClipRRect",
                    textAlign: TextAlign.center,
                  ),
                  Container(
                    width: 120,
                    height: 60,
                    decoration: BoxDecoration(
                      shape: BoxShape.rectangle,
                      borderRadius: BorderRadius.circular(10.0),
                      image: DecorationImage(
                          image: NetworkImage(imageUrl), fit: BoxFit.cover),
                    ),
                  ),
                  Text(
                    "BoxDecoration",
                    textAlign: TextAlign.center,
                  ),
                  ClipOval(
                    child: Image.network(
                      imageUrl,
                      scale: 8.5,
                    ),
                  ),
                  Text(
                    "ClipOval",
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FjZY2Pcn317QQtmAYvJvq3rK2YDe" alt="Image Widget效果" /></p>
<h3 id="3buttonwidget">3 Button Widget 用法详解</h3>
<p>Button Widget 的作用：</p>
<p>Button Widget 在 Flutter 里是用来负责按钮功能的组件，功能类似于 Android 的 Button，HTML 的一些 button 标签等等，属于基础组件。</p>
<p>在 Flutter 中 Button 有很多封装好的 Widget 类：FlatButton（扁平化）、RaisedButton（有按下状态）、OutlineButton（有边框）、MaterialButton（Material风格）、RawMaterialButton（没有应用 style 的 Material 风格按钮）、FloatingActionButton（悬浮按钮）、BackButton（返回按钮）、IconButton（Icon 图标）、CloseButton（关闭按钮）、ButtonBar（可以排列放置按钮元素的）等。</p>
<p>其中大部分的 Button 都是基于 RawMaterialButton 进行的修改定制而成的。</p>
<p>我们看下其中几个的效果。</p>
<ul>
<li>FlatButton</li>
</ul>
<p><img src="https://images.gitbook.cn/FnBFll3bIsHJ2yTjmpdNp7W3TdiV" alt="Image Widget效果" /></p>
<ul>
<li>RaisedButton</li>
</ul>
<p><img src="https://images.gitbook.cn/FotbHGMJnCWE5_GfZC7LBW1PzxD5" alt="Image Widget效果" /></p>
<ul>
<li>OutlineButton</li>
</ul>
<p><img src="https://images.gitbook.cn/Fqgb99eGCg-vwhOlerr8EUDIYP3d" alt="Image Widget效果" /></p>
<ul>
<li>IconButton</li>
</ul>
<p><img src="https://images.gitbook.cn/Fp77sndiz1mU_qgPoH02qogoPxE8" alt="Image Widget效果" /></p>
<p>接下来我们挑一个比较常用的 Button（FlatButton）来分析下它的构造方法的作用和属性的含义：</p>
<pre><code class="dart language-dart">const FlatButton({
    Key key,
    // 点击事件
    @required VoidCallback onPressed,
    // 高亮改变，按下和抬起时都会调用的方法
    ValueChanged&lt;bool&gt; onHighlightChanged,
    // 定义按钮的基色，以及按钮的最小尺寸，内部填充和形状的默认值
    ButtonTextTheme textTheme,
    // 按钮文字的颜色
    Color textColor,
    // 按钮禁用时的文字颜色
    Color disabledTextColor,
    // 按钮背景颜色
    Color color,
    // 按钮禁用时的背景颜色
    Color disabledColor,
    // 按钮按下时的背景颜色
    Color highlightColor,
    // 点击时，水波动画中水波的颜色，不要水波纹效果设置透明颜色即可
    Color splashColor,
    // 按钮主题，默认是浅色主题，分为深色和浅色 
    Brightness colorBrightness,
    // 按钮的填充间距
    EdgeInsetsGeometry padding,
    // 外形
    ShapeBorder shape,
    Clip clipBehavior = Clip.none,
    MaterialTapTargetSize materialTapTargetSize,
    // 按钮的内容，里面可以放子元素
    @required Widget child,
  })
</code></pre>
<p>通过一个实例来演示下它的用法和 Button 效果：</p>
<pre><code class="dart language-dart">body: CustomScrollView(
        slivers: &lt;Widget&gt;[
          SliverList(
            delegate: SliverChildListDelegate(&lt;Widget&gt;[
              Center(
                child: Column(
                  children: &lt;Widget&gt;[
                    //返回按钮
                    BackButton(
                      color: Colors.orange,
                    ),
                    //关闭按钮
                    CloseButton(),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //扁平化按钮
                        FlatButton(
                          child: Text('FLAT BUTTON',
                              semanticsLabel: 'FLAT BUTTON 1'),
                          onPressed: () {
                            // Perform some action
                          },
                        ),
                        //扁平化禁用状态按钮
                        FlatButton(
                          child: Text(
                            'DISABLED',
                            semanticsLabel: 'DISABLED BUTTON 3',
                          ),
                          onPressed: null,
                        ),
                      ],
                    ),
                    //可以使用图标
                    FlatButton.icon(
                      disabledColor: Colors.teal,
                      label:
                          Text('FLAT BUTTON', semanticsLabel: 'FLAT BUTTON 2'),
                      icon: Icon(Icons.add_circle_outline, size: 18.0),
                      onPressed: () {},
                    ),
                    FlatButton.icon(
                      icon: const Icon(Icons.add_circle_outline, size: 18.0),
                      label: const Text('DISABLED',
                          semanticsLabel: 'DISABLED BUTTON 4'),
                      onPressed: null,
                    ),
                    ButtonBar(
                      mainAxisSize: MainAxisSize.max,
                      children: &lt;Widget&gt;[
                        //有边框轮廓按钮
                        OutlineButton(
                          onPressed: () {},
                          child: Text('data'),
                        ),
                        OutlineButton(
                          onPressed: null,
                          child: Text('data'),
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //有图标，有边框轮廓按钮
                        OutlineButton.icon(
                          label: Text('OUTLINE BUTTON',
                              semanticsLabel: 'OUTLINE BUTTON 2'),
                          icon: Icon(Icons.add, size: 18.0),
                          onPressed: () {},
                        ),
                        OutlineButton.icon(
                          disabledTextColor: Colors.orange,
                          icon: const Icon(Icons.add, size: 18.0),
                          label: const Text('DISABLED',
                              semanticsLabel: 'DISABLED BUTTON 6'),
                          onPressed: null,
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //有波纹按下状态的按钮
                        RaisedButton(
                          child: Text('RAISED BUTTON',
                              semanticsLabel: 'RAISED BUTTON 1'),
                          onPressed: () {
                            // Perform some action
                          },
                        ),
                        RaisedButton(
                          child: Text('DISABLED',
                              semanticsLabel: 'DISABLED BUTTON 1'),
                          onPressed: null,
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //有波纹按下状态有图标的按钮
                        RaisedButton.icon(
                          icon: const Icon(Icons.add, size: 18.0),
                          label: const Text('RAISED BUTTON',
                              semanticsLabel: 'RAISED BUTTON 2'),
                          onPressed: () {
                            // Perform some action
                          },
                        ),
                        RaisedButton.icon(
                          icon: const Icon(Icons.add, size: 18.0),
                          label: Text('DISABLED',
                              semanticsLabel: 'DISABLED BUTTON 2'),
                          onPressed: null,
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //Material风格Button
                        MaterialButton(
                          child: Text('MaterialButton1'),
                          onPressed: () {
                            // Perform some action
                          },
                        ),
                        MaterialButton(
                          child: Text('MaterialButton2'),
                          onPressed: null,
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //原始的Button
                        RawMaterialButton(
                          child: Text('RawMaterialButton1'),
                          onPressed: () {
                            // Perform some action
                          },
                        ),
                        RawMaterialButton(
                          child: Text('RawMaterialButton2'),
                          onPressed: null,
                        ),
                      ],
                    ),
                    ButtonBar(
                      children: &lt;Widget&gt;[
                        //悬浮按钮
                        FloatingActionButton(
                          child: const Icon(Icons.add),
                          heroTag: 'FloatingActionButton1',
                          onPressed: () {
                            // Perform some action
                          },
                          tooltip: 'floating action button1',
                        ),
                        FloatingActionButton(
                          child: const Icon(Icons.add),
                          onPressed: null,
                          heroTag: 'FloatingActionButton2',
                          tooltip: 'floating action button2',
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ]),
          ),
        ],
      ),
</code></pre>
<p><img src="https://images.gitbook.cn/Fri28jD0K9mnubR-jpw6R0K1Vr1P" alt="Button Widget效果" /></p>
<p>本节课完整的例子可以在 Github 上查看：<a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_08">flutter_08</a></p>
<h3 id="">总结</h3>
<p>本节课主要讲解了 Flutter 的几个基础组件：Text、Image、Button 的用法和特点，这几个基础组件都很简单，但都很常用。课程里面基本介绍了这几个组件所有的属性和作用，希望大家有所了解和熟悉，不但要看，也要动手实践。亲身体验 Flutter 的几个基础组件的特点和用法和运行的流畅度。</p>
<p>建议将这几个组件组合实践写一个简单的页面出来。</p>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>