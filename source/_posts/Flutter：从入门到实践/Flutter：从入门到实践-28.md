---
title: Flutter：从入门到实践-28
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>主题这个概念可以大家都不陌生，我们在使用移动应用或者网页时候，都有夜间模式主题、护眼模式主题等等。在 Flutter 中主题的作用基本一致，可以设置全局或者局部的主题样式、字体样式，使得应用具有整体的样式风格。那么这节课我们将介绍 Flutter 中的主题内容，并配合一些案例。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>创建全局主题</li>
  <li>局部主题</li>
  <li>扩展或修改全局主题</li>
  </ul>
</blockquote>
<h3 id="">创建全局主题</h3>
<p>Flutter 支持全局设置 Theme 主题，需要配合 MaterialApp 的 theme 属性进行设置。主题在 Flutter 中主要是通过 ThemeData 来实现配置。</p>
<p>我们看一个最简单的用法：</p>
<pre><code class="dart language-dart">///创建全局主题
Widget theme1() {
  return MaterialApp(
    ///ThemeData.dark()
    ///ThemeData.light()
    ///默认有这两种主题
    ///也可以自定义主题，接近50种配置
    theme: ThemeData(
      brightness: Brightness.light,
      primaryColor: Colors.lightBlue[800],
      accentColor: Colors.cyan[600],
      backgroundColor: Colors.white70,
    ),
    home: Scaffold(
      appBar: AppBar(
        title: Text('Theme'),
      ),
      body: Text(
        'data',
        style: TextStyle(fontSize: 18, decoration: TextDecoration.none),
      ),
    ),
  );
}
</code></pre>
<p>ThemeData 提供了 ThemeData.light() 和 ThemeData.dark() 这两种已经配置好的色调主题，可以直接使用。当然，我们也可以自己配置 ThemeData 来实现个性化主题设置。如果 MaterialApp 没有设置主题的话也没关系，Flutter 会提供一个默认主题设置。</p>
<p>我们看下 ThemeData 有哪些属性可以配置：</p>
<pre><code class="dart language-dart">factory ThemeData({
    // 深色调还是浅色调
    Brightness brightness,
    // 主体颜色样本，可用于导航栏、FloatingActionButton的背景色等
    MaterialColor primarySwatch,
    // 主体的背景色，如导航
    Color primaryColor,
    // primaryColor的亮度:深色还是浅色
    Brightness primaryColorBrightness,
    // primaryColor的亮色调版本
    Color primaryColorLight,
    // primaryColor的暗色调版本
    Color primaryColorDark,
    // 前景色（文本、按钮等）
    Color accentColor,
    Brightness accentColorBrightness,
    Color canvasColor,
    // Scaffold的默认背景颜色
    Color scaffoldBackgroundColor,
    // BottomAppBar的默认颜色
    Color bottomAppBarColor,
    Color cardColor,
    // 分割线颜色
    Color dividerColor,
    // 选中高亮的颜色
    Color highlightColor,
    // 按下波纹颜色
    Color splashColor,
    // 定义按下的效果外观
    InteractiveInkFeatureFactory splashFactory,
    // 选中行时的颜色
    Color selectedRowColor,
    // 非活动/未选中时颜色
    Color unselectedWidgetColor,
    // 不可用时颜色
    Color disabledColor,
    // 按钮颜色
    Color buttonColor,
    // 按钮主题
    ButtonThemeData buttonTheme,
    // 有选定行时PaginatedDataTable标题的颜色
    Color secondaryHeaderColor,
    // 文字选中时颜色
    Color textSelectionColor,
    // 指针光标颜色
    Color cursorColor,
    // 用于调整当前文本的哪个部分的句柄颜色
    Color textSelectionHandleColor,
    // 与primaryColor配合作为背景的颜色，如进度条的背景
    Color backgroundColor,
    // 对话框背景色
    Color dialogBackgroundColor,
    // 指示器颜色
    Color indicatorColor,
    // 提示文本的颜色
    Color hintColor,
    // 输入验证错误的颜色
    Color errorColor,
    // 切换活动状态的颜色
    Color toggleableActiveColor,
    // 字体
    String fontFamily,
    // 文本样式主题
    TextTheme textTheme,
    TextTheme primaryTextTheme,
    TextTheme accentTextTheme,
    // 输入框的主题
    InputDecorationTheme inputDecorationTheme,
    // 图标主题
    IconThemeData iconTheme,
    IconThemeData primaryIconTheme,
    IconThemeData accentIconTheme,
    // Slider主题
    SliderThemeData sliderTheme,
    // TabBar主题
    TabBarTheme tabBarTheme,
    // Card主题
    CardTheme cardTheme,
    // Chip主题
    ChipThemeData chipTheme,
    // 目标平台:android,ios,fuchsia
    TargetPlatform platform,
    MaterialTapTargetSize materialTapTargetSize,
    // 页面过渡主题
    PageTransitionsTheme pageTransitionsTheme,
    // AppBar主题
    AppBarTheme appBarTheme,
    // BottomAppBar主题
    BottomAppBarTheme bottomAppBarTheme,
    ColorScheme colorScheme,
    // Dialog主题
    DialogTheme dialogTheme,
    // FloatingActionButton主题
    FloatingActionButtonThemeData floatingActionButtonTheme,
    Typography typography,
    // Cupertino主题
    CupertinoThemeData cupertinoOverrideTheme,
  })
</code></pre>
<p>可以看出，Flutter 主题可以全局配置的属性非常全面非常多。</p>
<p>通过 ThemeData 就可以简单配置出一个全局个性化主题：</p>
<pre><code class="dart language-dart">theme: ThemeData(
      brightness: Brightness.light,
      primaryColor: Colors.lightBlue[800],
      accentColor: Colors.cyan[600],
      backgroundColor: Colors.white70,
    ),
</code></pre>
<h3 id="-1">局部主题</h3>
<p>有的时候我们不想使用全局的主题，而是想在某些页面有自己的风格样式，而 Flutter 也支持局部主题的设置。</p>
<p>我们可以通过局部主题去覆盖全局主题，此时我们需要借助 Theme 来实现：</p>
<pre><code class="dart language-dart">// 局部主题覆盖全局主题
Widget theme2() {
  return Theme(
    data: ThemeData(
      primaryColor: Colors.yellow[800],
      accentColor: Colors.yellow[600],
      backgroundColor: Colors.white,
    ),
    child: Scaffold(
      appBar: AppBar(
        title: Text('Theme'),
      ),
      body: Text(
        'data',
        style: TextStyle(fontSize: 18, decoration: TextDecoration.none),
      ),
    ),
  );
}
</code></pre>
<p>我们只需要在最外层包裹一层 Theme 即可，然后 data 属性里重新配置个性化的 ThemeData 即可。child 属性放置原来的布局或者 Widget。</p>
<p>怎么样，是不是很灵活和简单！</p>
<h3 id="-2">扩展或修改全局主题</h3>
<p>有的时候我们不仅仅想使用局部主题，还需要进行修改全局主题或者扩展全局主题。例如手机QQ，支持手动切换全局主题等等。</p>
<p>那么我们就要借助 <code>Theme.of(context).copyWith(…)</code> 这个方法了。我们看下如何使用：</p>
<pre><code class="dart language-dart">// 扩展或修改全局主题
Widget theme3(BuildContext context) {
  return Theme(
    data: Theme.of(context).copyWith(
      // 修改全局主题primaryColor属性
      primaryColor: Colors.white30,
    ),
    child: Scaffold(
      appBar: AppBar(
        title: Text('Theme'),
      ),
      body: Text(
        'data',
        style: TextStyle(
            // 调用使用主题颜色
            color: Theme.of(context).primaryColor,
            fontSize: 18,
            decoration: TextDecoration.none),
      ),
    ),
  );
}
</code></pre>
<p>如果我们想使用主题中的一些属性值或者色调的话，可以通过 <code>Theme.of(context)</code> 来调用：</p>
<pre><code class="dart language-dart"> Container(
  // 调用全局的主题accentColor色调值
  color: Theme.of(context).accentColor,
  child: Text(
    'A Flutter Theme !',
    style: Theme.of(context).textTheme.title,
  ),
);
</code></pre>
<p>当然我们可以根据不同平台使用不同 Theme。</p>
<p>通过 ThemeData 也可以完成换肤功能或者更换主题功能。</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_26">本节课实例地址请单击这里查看</a></p>
<h3 id="-3">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的主题的几种用法。熟练掌握全局和局部的配置方法，尝试实现一个白天模式/夜间模式切换功能的小应用。</p></div></article>