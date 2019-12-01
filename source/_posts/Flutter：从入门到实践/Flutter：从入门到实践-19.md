---
title: Flutter：从入门到实践-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从这节课开始，我们将开始讲解 Flutter 中一些常用的技术要点。这些技术点在 Flutter 实际开发中将会用到，本节课主要讲解 Flutter 中路由的概念及使用方法。</p>
<p>在 Flutter 中路由负责页面的跳转和数据传递，类似于 Web 中的路由、Android 中的 Intent 页面跳转等。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 路由基础</li>
  <li>Navigator 和 Route 基本用法详解</li>
  <li>页面跳转及传递参数</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 Flutter 路由基础</h3>
<p>在 Flutter 中路由也是主要用来处理页面跳转、页面数据传递等操作。Flutter 的路由主要通过路由（Route）和导航器（Navigator）配合使用。Navigator 主要负责路由页面的堆栈管理和操作，例如添加跳转页面、移除页面等。</p>
<p>在 Flutter 中路由用法主要有两种用法：一种是在 MaterialApp 里的 routes 参数里配置定义好路由列表，也就是提前定义好要跳转的页面和名称。</p>
<pre><code class="dart language-dart">Map&lt;String, WidgetBuilder&gt; routes；
</code></pre>
<p>先定义路由跳转路径：</p>
<pre><code class="dart language-dart">return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: ShowAppPage(),
      // 定义路由表
      routes: &lt;String, WidgetBuilder&gt;{
        '/buttonpage': (BuildContext context) {
          return ButtonSamples();
        },
        '/routepage': (BuildContext context) {
          return RouteSamples();
        },
      },
    );

// 当然，为了简洁，我们可以用lambda简写路由注册
routes: &lt;String, WidgetBuilder&gt;{
        '/buttonpage': (BuildContext context) =&gt; ButtonSamples(),
        '/routepage': (BuildContext context) =&gt; RouteSamples(),
      },
</code></pre>
<p>主要规则就是前面定义一个路由页面名称，后面定义路径。</p>
<p>接下来就是通过这个名称来执行跳转，这里就要用到 Navigator 了。</p>
<pre><code class="dart language-dart">...

body: Center(
          child: FlatButton(
            child: Text("路由跳转"),
            onPressed: () {
              // 通过之前定义的名字来执行跳转
              Navigator.of(context).pushNamed("buttonpage");
            },
          ),
        )
</code></pre>
<p>Navigator 继承自 StatefulWidget，构造如下：</p>
<pre><code class="dart language-dart">const Navigator({
    Key key,
    // 默认路由
    this.initialRoute,
    // 通用路由跳转规则
    @required this.onGenerateRoute,
    // 未知路由
    this.onUnknownRoute,
    // 路由的观察者，监听
    this.observers = const &lt;NavigatorObserver&gt;[]
  })
</code></pre>
<p>Navigator 的主要方法如下。</p>
<ul>
<li>push：可以自定义使用Route子类进行个性化跳转，如MaterialPageRoute，实现页面跳转。</li>
<li>of：实例化Navigator。</li>
<li>pop：从路由堆栈里移除，退出页面。</li>
<li>canPop：判断当前页面能否进行pop操作，并返回bool值。</li>
<li>maybePop：会进行判断能否弹出，如弹出到首页仅剩一个页面，则不进行弹出操作。</li>
<li>popAndPushNamed：指将当前页面pop，然后跳转到指定页面。</li>
<li>popUntil：返回跳转，直到返回到指定页面停止。</li>
<li>pushAndRemoveUntil：移除所有页面，然后跳转到指定页面。</li>
<li>pushNamed：通过命名好的路由进行跳转。</li>
<li>pushNamedAndRemoveUntil：指将指定命名的页面加入到路由中，然后将之前的路径移除直到指定的页面为止。</li>
<li>pushReplacement：指把当前页面在栈中的位置替换成跳转的页面。</li>
<li>pushReplacementNamed：指把当前页面在栈中的位置替换成命名的跳转的页面。</li>
<li>removeRoute：移除路由。</li>
<li>replace：替换路由。</li>
</ul>
<h3 id="2navigatorroute">2 Navigator 和 Route 基本用法详解</h3>
<p>接下来我们来看 Flutter 中 Navigator 和 Route 基本用法。</p>
<p>Navigator 之前介绍了，Route 在 Flutter 中主要有两种实现方法：一个是使用 MaterialPageRoute；另一个是使用 PageRouteBuilder 来构建。</p>
<p>MaterialPageRoute 构造方法：</p>
<pre><code class="dart language-dart">MaterialPageRoute({
    // 构建页面
    @required this.builder,
    // 路由设置
    RouteSettings settings,
    // 是否保存页面状态、内容
    this.maintainState = true,
    bool fullscreenDialog = false,
  })
</code></pre>
<p>PageRouteBuilder 构造方法：</p>
<pre><code class="dart language-dart">PageRouteBuilder({
    // 路由设置
    RouteSettings settings,
    // 目标页面
    @required this.pageBuilder,
    // 跳转过度动画设置
    this.transitionsBuilder = _defaultTransitionsBuilder,
    this.transitionDuration = const Duration(milliseconds: 300),
    this.opaque = true,
    this.barrierDismissible = false,
    this.barrierColor,
    this.barrierLabel,
    this.maintainState = true,
  })
</code></pre>
<p>PageRouteBuilder 构建的路由可以设置跳转动画效果。</p>
<p>我们通过代码实例来看下这两种基本用法：</p>
<pre><code class="dart language-dart">FlatButton(
      child: Text("路由跳转"),
      onPressed: () {
        Navigator.of(context)
            .push(MaterialPageRoute(builder: (BuildContext context) {
          return ButtonSamples();
        }));
      },
    );
</code></pre>
<p>MaterialPageRoute 无须预先配置好路由目标页面和名称，比较的灵活，也可以传递参数。</p>
<pre><code class="dart language-dart"> Navigator.push(context, PageRouteBuilder(
   opaque: false,
   pageBuilder: (BuildContext context, Animation&lt;double&gt; animation,
                Animation&lt;double&gt; secondaryAnimation) {
     return ButtonSamples();
   },
   transitionsBuilder: (BuildContext context, Animation&lt;double&gt; animation, Animation&lt;double&gt; secondaryAnimation, Widget child) {
     return FadeTransition(
       opacity: animation,
       child: RotationTransition(
         turns: Tween&lt;double&gt;(begin: 0.5, end: 1.0).animate(animation),
         child: child,// 这里的child是pageBuilder里返回的目标页面
       ),
     );
   }
 ));
</code></pre>
<p>PageRouteBuilder 可以创建一个更加丰富复杂的页面路由跳转，可以设置跳转动画。</p>
<p>好，最后在看一个复杂一些的情况处理。例如我们有一个首页 Tab 页面，内部有自己的路由跳转，当我们跳转到个人中心时候，需要判断是否登录，没有登录就跳到登录页，登录过就直接显示个人中心信息。这种就是路由里面的内部还有一个自己的路由。这就需要我们用 Navigator 里的 RouteSettings 了，我们看下实现方法：</p>
<pre><code class="dart language-dart"> class MyApp extends StatelessWidget {
   @override
   Widget build(BuildContext context) {
     return MaterialApp(
       initialRoute: '/',
       routes: {
         '/': (BuildContext context) =&gt; HomePage(),
         // 登录页
         '/signup': (BuildContext context) =&gt; SignUpPage(),
       },
     );
   }
 }

 class SignUpPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // SignUpPage有自己的内部路由
    return Navigator(
      // 默认路由页面
      initialRoute: 'signup/personal_info',
      // 内部路由的跳转处理
      onGenerateRoute: (RouteSettings settings) {
        WidgetBuilder builder;
        switch (settings.name) {
          case 'signup/personal_info':
            builder = (BuildContext _) =&gt; CollectPersonalInfoPage();
            break;
          case 'signup/choose_credentials':
            builder = (BuildContext _) =&gt; ChooseCredentialsPage();
            break;
          default:
            throw Exception('Invalid route: ${settings.name}');
        }
        return MaterialPageRoute(builder: builder, settings: settings);
      },
    );
  }
 }
</code></pre>
<h3 id="3">3 页面跳转及传递参数</h3>
<p>接下来我们学习路由页面跳转并且传递参数的实现方法。</p>
<p>页面跳转传递参数，这里建议使用动态路由，而不是使用在 MaterialApp 的 routes 属性里静态定义的这种。</p>
<p>我们先看静态定义的传参用法：</p>
<pre><code class="dart language-dart">// 通过key，value传参
Navigator.pushNamed(
      context,
      '/weather',
      arguments: &lt;String, String&gt;{
        'city': 'Berlin',
        'country': 'Germany',
      },
    );
// 通过Object来传递参数
class WeatherRouteArguments {
  WeatherRouteArguments({this.city, this.country});
  final String city;
  final String country;
}

Navigator.pushNamed(
    context,
    '/weather',
    arguments: WeatherRouteArguments(city: 'Berlin', country: 'Germany'),
  );

// 接收页面通过RouteSettings进行接收参数，比较不灵活和麻烦
MaterialApp(
        onGenerateRoute: (RouteSettings settings){
            ...
            settings.arguments
            ...
},
</code></pre>
<p>通常我们通过动态路由传参方式来实现：</p>
<pre><code class="dart language-dart">Navigator.push(context, new MaterialPageRoute(builder: (BuildContext context){
  return new ButtonSamples(
    title:'标题'，
    name:'名称'
  );
}))

...
// 第二个页面构造方法里接收参数
class ButtonSamples extends StatefulWidget {
  String title;
  String name;
  ButtonSamples({Key key, this.title, this.name}) : super(key: key);

  @override
  State&lt;StatefulWidget&gt; createState() {
    return ButtonSamplesState();
  }
}
</code></pre>
<p>或者，也可以传递一个 Object 对象：</p>
<pre><code class="dart language-dart">class Book{
  String title;
  String name;

  Book({this.title, this.name});
}

Navigator.push(context, new MaterialPageRoute(builder: (BuildContext context){
  return new ButtonSamples(Book
    title:'标题'，
    name:'名称'
  );
}))

// 第二个页面构造方法里接收参数
class ButtonSamples extends StatefulWidget {
  Book book;

  ButtonSamples({Key key, this.book}) : super(key: key);

  @override
  State&lt;StatefulWidget&gt; createState() {
    return ButtonSamplesState();
  }
}
</code></pre>
<p>接下来是关闭页面返回数据和上一个页面接收返回数据的用法：</p>
<pre><code class="dart language-dart">// 关闭页面返回数据
Navigator.pop(context, '返回数据');

// 接收返回数据
Navigator.push&lt;String&gt;(context,
        MaterialPageRoute(builder: (BuildContext context) {
      return ButtonSamples(title: '标题', name: '名称');
    })).then((String result) {
      //处理代码
    });
</code></pre>
<p>路由效果如图：</p>
<p><img src="https://images.gitbook.cn/Fp9ejgG-2EyNoLZCyvSr1lEtToJo" alt="路由跳转" /></p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_17">flutter_17</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的路由基础知识和页面跳转传参用法和特点。</p>
<ul>
<li>重点掌握 MaterialPageRoute 和 Navigator 的用法，做到熟练。</li>
<li>练习一下页面传递参数的用法和接收返回参数的用法。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>