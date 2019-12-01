---
title: Flutter：从入门到实践-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将继续讲解 Flutter 的常用组件中的布局使用的组件，本节课主要讲解 Flutter 里的流式布局（或者瀑布）组件的用法。在 Flutter 中主要通过 Flow 和 Wrap 组件来实现流式、瀑布式布局。那么这节课就对流式布局组件进行详细分析，并结合案例进行详细的用法讲解。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flow 布局 Widget 用法详解</li>
  <li>Wrap 布局 Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="flowwidget">Flow 布局 Widget 用法详解</h3>
<p>流式布局可以用在商品标签列表、不规则瀑布流列表、网格布局的使用上。简单地说流式布局就是可以自动换行的布局，如我们一行里的控件放不下了，则自动绘制到下一行。</p>
<p>Flutter 的 Flow 就可以自己自定义规则来控制子布局排列。Flow 继承自MultiChildRenderObjectWidget，Flow 性能比较好，绘制也比较灵活，可以定制布局效果。</p>
<p>Flow 的构造方法如下：</p>
<pre><code class="dart language-dart">Flow({
    Key key,
    // 子布局排列配置规则
    @required this.delegate,
    // 布局子控件
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>Flow 的构造方法很简单，最重要的就是 delegate 这个规则，我们按照需要编写即可。使用的时候，我们需要创建一个 Delegate 继承自 FlowDelegate。</p>
<p>我们接下来看一个完整的例子：</p>
<pre><code class="dart language-dart">class FlowSamplesState extends State&lt;FlowSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Flow Demo'), primary: true),
        body: Flow(
          // 子控件排列绘制规则
          delegate: FlowWidgetDelegate(margin: EdgeInsets.all(10.0)),
          children: &lt;Widget&gt;[
            Container(
              width: 80.0,
              height: 80.0,
              color: Colors.orange,
            ),
            Container(
              width: 160.0,
              height: 80.0,
              color: Colors.teal,
            ),
            Container(
              width: 80.0,
              height: 80.0,
              color: Colors.red,
            ),
            Container(
              width: 80.0,
              height: 80.0,
              color: Colors.yellow,
            ),
            Container(
              width: 80.0,
              height: 80.0,
              color: Colors.brown,
            ),
            Container(
              width: 80.0,
              height: 80.0,
              color: Colors.purple,
            ),
          ],
        ));
  }
}

class FlowWidgetDelegate extends FlowDelegate {
  EdgeInsets margin = EdgeInsets.all(10);
  // 构造方法，传入每个child的间隔
  FlowWidgetDelegate({this.margin});

  // 必须要重写的方法：child的绘制控制代码，可以调整尺寸位置
  @override
  void paintChildren(FlowPaintingContext context) {
    var screenWidth = context.size.width;
    double offsetX = margin.left; //记录横向绘制的x坐标
    double offsetY = margin.top; //记录纵向绘制的y坐标
    // 遍历子控件进行绘制
    for (int i = 0; i &lt; context.childCount; i++) {
      // 如果当前x左边加上子控件宽度小于屏幕宽度则继续绘制,否则换行
      var width = context.getChildSize(i).width + offsetX + margin.right;
      if (width &lt; screenWidth) {
        // 绘制子控件
        context.paintChild(i,
            transform: Matrix4.translationValues(offsetX, offsetY, 0.0));
        offsetX = width + margin.left;
      } else {
        offsetX = margin.left;
        offsetY += context.getChildSize(i).height + margin.top + margin.bottom;
        //绘制子控件
        context.paintChild(i,
            transform: Matrix4.translationValues(offsetX, offsetY, 0.0));
        offsetX += context.getChildSize(i).width + margin.left + margin.right;
      }
    }
  }

  // 必须要重写的方法：是否需要重绘
  @override
  bool shouldRepaint(FlowDelegate oldDelegate) {
    return oldDelegate != this;
  }

  // 可选重写方法：是否需要重新布局
  @override
  bool shouldRelayout(FlowDelegate oldDelegate) {
    return super.shouldRelayout(oldDelegate);
  }

  // 可选重写方法：设置Flow布局的尺寸
  @override
  Size getSize(BoxConstraints constraints) {
    return super.getSize(constraints);
  }

  // 可选重写方法：设置每个child的布局约束条件，会覆盖已有的
  @override
  BoxConstraints getConstraintsForChild(int i, BoxConstraints constraints) {
    return super.getConstraintsForChild(i, constraints);
  }
}
</code></pre>
<p>我们看下 Flow 布局的效果图：</p>
<p><img src="https://images.gitbook.cn/Fq_3ul_VKbwX-fjQ8jI3WWeIYsbw" alt="Flow" /></p>
<p>我们使用 Flow 的重点就是继承重写一个 FlowDelegate，FlowDelegate 里面最重要的方法就是paintChildren 方法，来定制我们的排列绘制子控件规则。</p>
<p>当然我们也可以实现更复杂一点的效果，可以根据自己的需求进行排列子控件，来实现流式布局或瀑布流布局效果。</p>
<h3 id="wrapwidget">Wrap 布局 Widget 用法详解</h3>
<p>Wrap 从字面意思上也很好理解，就是组件的大小是根据自身的实际大小来包裹的。在 Flutter 中Wrap 组件是一个可以使子控件自动换行的布局组件，默认的内部子控件排列方向是水平的。也就是超过指定宽度大小，就自动换到下一行。例如我们平时看到的商品标签页，标签是自动按行排列的。</p>
<p>我们看下 Wrap 布局的效果图（截图来自美团 Android 客户端）：</p>
<p><img src="https://images.gitbook.cn/FnabemEWqVsXMoO0Bs1_Y5QvsftK" alt="Wrap" /></p>
<p>其实 Wrap 可以实现的效果，Flow 也可以实现。我们可以根据方便程度进行合理选择。</p>
<p>Wrap 也是继承自 MultiChildRenderObjectWidget，内部可以放置多个子控件。</p>
<p>我们看下 Wrap 的构造方法：</p>
<pre><code class="dart language-dart">Wrap({
    Key key,
    // 子控件在主轴上的排列方向
    this.direction = Axis.horizontal,
    // 子控件在主轴方向上的对齐方式
    this.alignment = WrapAlignment.start,
    // 主轴方向上子控件的间距
    this.spacing = 0.0,
    // 子控件在纵轴方向上的对齐方式
    this.runAlignment = WrapAlignment.start,
    // 子控件在纵轴方向上的间距
    this.runSpacing = 0.0,
    // 交叉轴上子控件的对齐方式
    this.crossAxisAlignment = WrapCrossAlignment.start,
    // 文本方向
    this.textDirection,
    // direction为Vertical时子控件排序顺序
    this.verticalDirection = VerticalDirection.down,
    // 子控件集合
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>属性虽然多，但是很好理解，因为Wrap 很多属性和 Row、Column、Flex 这些组件的属性有所重复。</p>
<p>接下来通过一个代码实例，来看下 Wrap 的特点和用法：</p>
<pre><code class="dart language-dart">class WrapSamplesState extends State&lt;WrapSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Wrap Demo'), primary: true),
        // Wrap包裹的子控件会自动换行排列
        body: Wrap(
          spacing: 8.0, // 子控件横向间距
          runSpacing: 4.0, // 子控件纵向（每行）的间距
          // 子控件元素集合
          children: &lt;Widget&gt;[
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('A')),
              label: Text('全部'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('B')),
              label: Text('好评 66207'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('C')),
              label: Text('差评 3913'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('D')),
              label: Text('点映1'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('E')),
              label: Text('购票 75985'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('F')),
              label: Text('认证作者 23'),
            ),
            Chip(
              avatar: CircleAvatar(
                  backgroundColor: Colors.blue.shade900, child: Text('G')),
              label: Text('同城 1496'),
            ),
          ],
        ));
  }
}
</code></pre>
<p>我们看下实例中 Wrap 布局实现的效果图：</p>
<p><img src="https://images.gitbook.cn/FmetaN1PTEDMzZM2ARTB6U4xKmE-" alt="avatar" /></p>
<p>怎么样，是不是很简单？当我们流式布局效果不是非常复杂的情况下，Wrap 用起来要简单些，如果Wrap 实现不了，那么就可以用 Flow 来尝试实现流式布局或瀑布式布局的效果。</p>
<p>本节课实例地址：
<a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_15">flutter_15</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的几个常用的流式布局组件 Widget 的用法和特点。Wrap 用法简单些，Flow 用法复杂些，Flow 可以实现更复杂定制化流式或瀑布式布局效果。</p>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>