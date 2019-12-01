---
title: Flutter：从入门到实践-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将继续讲解 Flutter 的常用基础布局组件，前面已经给大家介绍了几种常用的布局 Widget 及其特点与用法。这节课要讲解的布局 Widget 看起来很多，不过其中几个都具有相似的特点，用法类似。如 Row 和 Column 用于线性布局（横向或者纵向排列子元素）；Flex 和 Expanded 用于弹性布局（按照比例分配子元素所占大小空间）；Stack 和 IndexedStack 用于层叠布局（也可以叫帧布局，也就是布局里的元素有前后层级堆叠在一起的）。那么这节课就带领大家对 Flutter 的基础布局中的这几个 Widget 进行详细分析讲解，并结合案例进行详细的用法讲解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Row 布局 Widget 用法详解</li>
  <li>Column 布局 Widget 用法详解</li>
  <li>Flex 布局 Widget 用法详解</li>
  <li>Expanded 布局 Widget 用法详解</li>
  <li>Stack 布局 Widget 用法详解</li>
  <li>IndexedStack 布局 Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="1rowwidget">1 Row 布局 Widget 用法详解</h3>
<p>Row 布局组件类似于 Android 中的 LinearLayout 线性布局，它用来做水平横向布局使用，里面的 children 子元素按照水平方向进行排列。</p>
<p>Row 的继承关系如下：</p>
<p>Row -&gt; Flex -&gt; MultiChildRenderObjectWidget -&gt; RenderObjectWidget ...</p>
<p>可以看出 Row 是 Flex 的拓展子类，也是多子元素的一个组件之一（内部可以包含多个子元素）。</p>
<p>我们看下 Row 布局组件的大致效果图：</p>
<p><img src="https://images.gitbook.cn/Fu0cqduIm2f8vEmPth7KWhyUx5TR" alt="Row" /></p>
<p>所有元素水平排成一行。</p>
<p>那么接下来我们看下 Row 的构造方法：</p>
<pre><code class="dart language-dart">Row({
    Key key,
    // 主轴方向上的对齐方式（Row的主轴是横向轴）
    MainAxisAlignment mainAxisAlignment = MainAxisAlignment.start,
    // 在主轴方向（Row的主轴是横向轴）占有空间的值，默认是max
    MainAxisSize mainAxisSize = MainAxisSize.max,
    // 在交叉轴方向(Row是纵向轴)的对齐方式，Row的高度等于子元素中最高的子元素高度
    CrossAxisAlignment crossAxisAlignment = CrossAxisAlignment.center,
    // 水平方向子元素的排列方向：从左到右排列还是反向
    TextDirection textDirection,
    // 表示纵轴（垂直）的对齐排列方向，默认是VerticalDirection.down，表示从上到下。这个参数一般用于Column组件里
    VerticalDirection verticalDirection = VerticalDirection.down,
    // 字符对齐基线方式
    TextBaseline textBaseline,
    // 子元素集合
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>接下来详细看下 Row 的主轴和交叉轴属性。</p>
<p><strong>MainAxisAlignment（主轴属性：主轴方向上的对齐方式，Row 是横向轴为主轴）</strong></p>
<pre><code class="dart language-dart">enum MainAxisAlignment {
  // 按照主轴起点对齐，例如：按照靠近最左侧子元素对齐
  start,

  // 将子元素放置在主轴的末尾，按照末尾对齐
  end,

  // 子元素放置在主轴中心对齐
  center,

  // 将主轴方向上的空白区域均分，使得子元素之间的空白区域相等，首尾子元素都靠近首尾，没有间隙。有点类似于两端对齐
  spaceBetween,

  // 将主轴方向上的空白区域均分，使得子元素之间的空白区域相等，但是首尾子元素的空白区域为1/2
  spaceAround,

  // 将主轴方向上的空白区域均分，使得子元素之间的空白区域相等，包括首尾子元素
  spaceEvenly,
}
</code></pre>
<p>再看下 Row 的交叉属性。</p>
<p><strong>CrossAxisAlignment（交叉属性：在交叉轴方向的对齐方式，Row 是纵向轴。Row 的高度等于子元素中最高的子元素高度）</strong></p>
<pre><code class="dart language-dart">enum CrossAxisAlignment {
  // 子元素在交叉轴上起点处展示
  start,

  // 子元素在交叉轴上末尾处展示
  end,

  // 子元素在交叉轴上居中展示
  center,

  // 让子元素填满交叉轴方向
  stretch,

  // 在交叉轴方向，使得子元素按照baseline对齐
  baseline,
}
</code></pre>
<p>再看下 MainAxisSize 属性。</p>
<p><strong>MainAxisSize（在主轴方向子元素占有空间的方式，Row 的主轴是横向轴。默认是 max）</strong></p>
<pre><code class="dart language-dart">enum MainAxisSize {
  // 根据传入的布局约束条件，最大化主轴方向占用可用空间，也就是尽可能充满可用宽度
  max,

  // 与max相反，是最小化占用主轴方向的可用空间
  min,
}
</code></pre>
<p>接下来我们通过一个实例来学习下 Row 的布局特点。</p>
<pre><code class="dart language-dart">Column(
        children: &lt;Widget&gt;[
          // 默认横向排列元素
          Row(
            verticalDirection: VerticalDirection.up,
            textBaseline: TextBaseline.ideographic,
            children: &lt;Widget&gt;[
              RaisedButton(
                color: Colors.blue,
                child: Text(
                  '我是按钮一\n 按钮',
                  style: TextStyle(color: Colors.white),
                ),
                onPressed: () {},
              ),
              RaisedButton(
                color: Colors.grey,
                child: Text(
                  '   我是按钮二  ',
                  style: TextStyle(color: Colors.black),
                ),
                onPressed: () {},
              ),
              RaisedButton(
                color: Colors.orange,
                child: Text(
                  '      我是按钮三    ',
                  style: TextStyle(color: Colors.white),
                ),
                onPressed: () {},
              ),
            ],
          ),
          SizedBox(
            height: 10,
          ),
          // 默认横向排列元素
          Row(
            children: &lt;Widget&gt;[
              const FlutterLogo(),
              const Expanded(
                child: Text(
                    'Flutter\'s hot reload helps you quickly and easily experiment, build UIs, add features, and fix bug faster. Experience sub-second reload times, without losing state, on emulators, simulators, and hardware for iOS and Android.'),
              ),
              const Icon(Icons.sentiment_very_satisfied),
            ],
          ),
          SizedBox(
            height: 10,
          ),
          // 居中排列元素
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: &lt;Widget&gt;[
              Text(
                " 我们居中显示 |",
                style: TextStyle(color: Colors.teal),
              ),
              Text(" Flutter的Row布局组件 "),
            ],
          ),
        ],
    ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FmYu6WTQYf4fS5y5QoTW9W4srY_G" alt="Row" /></p>
<h3 id="2columnwidget">2 Column 布局 Widget 用法详解</h3>
<p>在学习完了 Row 布局组件后，再学习 Column 很容易，Row 是横向排列元素，Column 是纵向排列子元素，可以对比着学习。</p>
<p>Column 的继承关系如下：</p>
<p>Column -&gt; Flex -&gt; MultiChildRenderObjectWidget -&gt; RenderObjectWidget ...</p>
<p>Column 也是 Flex 的拓展子类，也是多子元素的一个组件之一（内部可以包含多个子元素）。</p>
<p>我们看下 Column 布局组件的大致效果图：</p>
<p><img src="https://images.gitbook.cn/Ft-91NfPMd-qC6MScGCRkwHzNIMG" alt="Column" /></p>
<p>所有元素纵向排成一列。</p>
<p><strong>构造方法是一致的，只不过主轴和交叉轴和 Row 是相反的。这里就不再重复讲解了。</strong></p>
<p>接下来看一个实例：</p>
<pre><code class="dart language-dart">Column(
        // 纵向排列子元素
        children: &lt;Widget&gt;[
          RaisedButton(
            color: Colors.blue,
            child: Text(
              '我是按钮一',
              style: TextStyle(color: Colors.white),
            ),
            onPressed: () {},
          ),
          RaisedButton(
            color: Colors.grey,
            child: Text(
              '   我是按钮二  ',
              style: TextStyle(color: Colors.black),
            ),
            onPressed: () {},
          ),
          RaisedButton(
            color: Colors.orange,
            child: Text(
              '      我是按钮三    ',
              style: TextStyle(color: Colors.white),
            ),
            onPressed: () {},
          ),
          SizedBox(
            height: 10,
          ),
          const FlutterLogo(),
          Text(
              'Flutter\'s hot reload helps you quickly and easily experiment, build UIs, add features, and fix bug faster. Experience sub-second reload times, without losing state, on emulators, simulators, and hardware for iOS and Android.'),
          const Icon(Icons.sentiment_very_satisfied),
        ],
      ),
</code></pre>
<p>运行效果如下图所示：</p>
<p><img src="https://images.gitbook.cn/FkSigqSvf9qli3ZKAiricpArPSje" alt="Column" /></p>
<h3 id="3flexexpandedwidget">3 Flex 和 Expanded 布局 Widget 用法详解</h3>
<p>Flex 组件是 Row 和 Column 的父类，主要用于弹性布局，类似于HTML 中的 Flex 弹性盒子布局，可以按照一定比例进行分类布局空间。</p>
<p>Flex 继承自 MultiChildRenderObjectWidget，Flex 也是多子元素的一个组件之一（内部可以包含多个子元素）。</p>
<p>Flex 一般和 Expanded 搭配使用，Expanded 组件从名字就可以看出它的特点，就是让子元素扩展占用 Flex 的剩余空间。</p>
<p>我们看下 Flex 布局组件的大致效果图：</p>
<p><img src="https://images.gitbook.cn/Fjk8ya62I9o_o4MCazy0epxRWYYj" alt="Flex" /></p>
<p>按钮一占用 2/3 的横向空间，按钮二占用剩余 1/3 空间。</p>
<p>我们看下 Flex 构造方法：</p>
<pre><code class="dart language-dart">Flex({
    Key key,
    // 子元素排列方向：横向还是纵向
    @required this.direction,
    this.mainAxisAlignment = MainAxisAlignment.start,
    this.mainAxisSize = MainAxisSize.max,
    this.crossAxisAlignment = CrossAxisAlignment.center,
    this.textDirection,
    this.verticalDirection = VerticalDirection.down,
    this.textBaseline,
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>单独看 Flex 组件没有意义，因为一般直接用它的子类 Row 和 Column 来使用。而 Flex 主要是和 Expanded 搭配使用。我们再看下 Expanded 组件构造方法：</p>
<pre><code class="dart language-dart">const Expanded({
    Key key,
    // 占用空间比重、权重
    int flex = 1,
    // 子元素
    @required Widget child,
  }) 
</code></pre>
<p>我们通过一个实例看下 Flex 和 Expanded 搭配用法：</p>
<pre><code class="dart language-dart">body: Row(
          children: &lt;Widget&gt;[
            Expanded(
              // flex设置权重，这里是占2/5空间
              flex: 2,
              child: RaisedButton(
                color: Colors.blue,
                child: Text(
                  '我是按钮一',
                  style: TextStyle(color: Colors.white),
                ),
                onPressed: () {},
              ),
            ),
            // flex设置权重，这里是占1/5空间
            Expanded(
              flex: 1,
              child: Column(
                children: &lt;Widget&gt;[
                  Expanded(
                    flex: 2,
                    child: RaisedButton(
                      color: Colors.grey,
                      child: Text(
                        '   我是按钮一  ',
                        style: TextStyle(color: Colors.black),
                      ),
                      onPressed: () {},
                    ),
                  ),
                  Expanded(
                    flex: 1,
                    child: RaisedButton(
                      color: Colors.teal,
                      child: Text(
                        '   我是按钮二  ',
                        style: TextStyle(color: Colors.white),
                      ),
                      onPressed: () {},
                    ),
                  )
                ],
              ),
            ),
            // flex设置权重，这里是占2/5空间
            Expanded(
              flex: 2,
              child: RaisedButton(
                color: Colors.grey,
                child: Text(
                  '   我是按钮二  ',
                  style: TextStyle(color: Colors.black),
                ),
                onPressed: () {},
              ),
            )
          ],
        )
</code></pre>
<p>运行效果图如下：</p>
<p><img src="https://images.gitbook.cn/FrgY6BkS2pX2kEO5P4zyiNmmclDq" alt="Flex" /></p>
<h3 id="4stackindexedstackwidget">4 Stack 和 IndexedStack 布局 Widget 用法详解</h3>
<p>Stack 和 IndexStack 都是层叠布局方式，类似于 Android 里的 FrameLayout 帧布局，内部子元素是有层级堆起来的。</p>
<p>Stack 继承自 MultiChildRenderObjectWidget，Stack 也是多子元素的一个组件之一（内部可以包含多个子元素）。</p>
<p>而 IndexedStack 继承自 Stack，扩展了 Stack的一些特性。它的作用是显示第 index 个子元素，其他子元素都是不可见的。所以 IndexedStack 的尺寸永远是跟最大的子元素尺寸一致。</p>
<p>Stack 的布局行为，是根据子元素是 positioned 还是 non-positioned 来区分的：</p>
<ul>
<li>对于 positioned 的子元素，它们的位置会根据所设置的 top、bottom、right 或 left 属性来确定，这几个值都是相对于 Stack 的左上角；</li>
<li>对于 non-positioned 的子元素，它们会根据 Stack 的 aligment 来设置位置。</li>
</ul>
<p>Stack 布局的子元素层级堆叠顺序：最先布局绘制的子元素在最底层，越后绘制的越在顶层。类似于 Web 中的 z-index。</p>
<p>看下 Stack 布局组件的效果图：</p>
<p><img src="https://images.gitbook.cn/FuuwckH_qkMAJ0bBZqQOlYeDsOqB" alt="Stack" /></p>
<p>默认按照左上角，有层级的绘制排列。</p>
<p>看下 Stack 的构造方法：</p>
<pre><code class="dart language-dart">Stack({
    Key key,
    // 对齐方式，默认是左上角（topStart）
    this.alignment = AlignmentDirectional.topStart,
    // 对齐方向
    this.textDirection,
    // 定义如何设置无定位子元素尺寸，默认为loose
    this.fit = StackFit.loose,
    // 超过的部分子元素处理方式
    this.overflow = Overflow.clip,
    // 子元素
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>我们看下 alignment：</p>
<pre><code class="dart language-dart">  // 左上角
  static const Alignment topLeft = Alignment(-1.0, -1.0);

  // 主轴顶部对齐，交叉轴居中
  static const Alignment topCenter = Alignment(0.0, -1.0);

  // 主轴顶部对齐，交叉轴偏右
  static const Alignment topRight = Alignment(1.0, -1.0);

  // 主轴居中，交叉轴偏左
  static const Alignment centerLeft = Alignment(-1.0, 0.0);

  // 居中
  static const Alignment center = Alignment(0.0, 0.0);

  // 主轴居中，交叉轴偏右
  static const Alignment centerRight = Alignment(1.0, 0.0);

  // 主轴底部对齐，交叉轴偏左
  static const Alignment bottomLeft = Alignment(-1.0, 1.0);

  // 主轴底部对齐，交叉轴居中
  static const Alignment bottomCenter = Alignment(0.0, 1.0);

  // 主轴底部对齐，交叉轴偏右
  static const Alignment bottomRight = Alignment(1.0, 1.0);
</code></pre>
<p>看下 fit 属性：</p>
<pre><code class="dart language-dart">enum StackFit {
  // 子元素宽松的取值，可以从min到max的尺寸
  loose,

  // 子元素尽可能的占用剩余空间，取max尺寸
  expand,

  // 不改变子元素的约束条件
  passthrough,
}
</code></pre>
<p>最后看下 overflow 属性：</p>
<pre><code class="dart language-dart">enum Overflow {
  // 超出部分不会被裁剪，正常显示
  visible,

  // 超出部分会被裁剪
  clip,
}
</code></pre>
<p>我们看下 IndexedStack 构造方法：</p>
<pre><code class="dart language-dart">IndexedStack({
    Key key,
    AlignmentGeometry alignment = AlignmentDirectional.topStart,
    TextDirection textDirection,
    StackFit sizing = StackFit.loose,
    // 多了一个索引，索引的这个元素显示，其他元素隐藏
    this.index = 0,
    // 子元素
    List&lt;Widget&gt; children = const &lt;Widget&gt;[],
  })
</code></pre>
<p>接下来通过一个实例来演示下 Stack 和 IndexedStack 的用法：</p>
<pre><code class="dart language-dart">body: Column(
          children: &lt;Widget&gt;[
            // Stack层叠布局
            Stack(
              children: &lt;Widget&gt;[
                Container(
                  width: 300,
                  height: 300,
                  color: Colors.grey,
                ),
                Container(
                  width: 200,
                  height: 200,
                  color: Colors.teal,
                ),
                Container(
                  width: 100,
                  height: 100,
                  color: Colors.blue,
                ),
                Text(
                  "Stack",
                  style: TextStyle(color: Colors.white),
                ),
              ],
            ),
            SizedBox(
              height: 10,
            ),
            // IndexedStack层叠布局
            IndexedStack(
              // 指定显示的子元素序号，其余子元素隐藏
              index: 2,
              children: &lt;Widget&gt;[
                Container(
                  width: 300,
                  height: 300,
                  color: Colors.grey,
                ),
                Container(
                  width: 200,
                  height: 200,
                  color: Colors.teal,
                ),
                Container(
                  width: 100,
                  height: 100,
                  color: Colors.blue,
                ),
                Text(
                  "Stack",
                  style: TextStyle(color: Colors.white),
                ),
              ],
            )
          ],
        )
</code></pre>
<p>运行效果图如下：</p>
<p><img src="https://images.gitbook.cn/FrMj9BZNRgPgY-O_D2d3rblfuIGb" alt="Stack和IndexedStack" /></p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_12">flutter_12</a></p>
<h3 id="">总结</h3>
<p>本节课讲解了 Flutter 的几个常用布局 Widget 的用法和特点，主要分为线性布局组件、弹性布局组件、层叠布局组件。建议如下：</p>
<ul>
<li>尝试写一个各种布局方式组合的实例页面，复习巩固。</li>
</ul></div></article>