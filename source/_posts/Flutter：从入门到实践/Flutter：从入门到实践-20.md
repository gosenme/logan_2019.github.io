---
title: Flutter：从入门到实践-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Flutter 中的页面也有生命周期的概念，类似于 Android 中 Activity 的生命周期，不过也有很大的不同。这节课我们将讲解 Flutter 中生命周期及按键监听相关内容。在 Flutter 中生命周期主要体现在State 的回调函数上。那么这节课就带大家学习 Flutter 的生命周期及按键监听，本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 生命周期</li>
  <li>Flutter 按键监听</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 Flutter 生命周期</h3>
<p>我们先了解下生命周期的概念，也就是一个页面对象从创建到销毁的整个状态管理。我们看下 Flutter 的 State 生命周期的示意图：</p>
<p><img src="https://images.gitbook.cn/FkRX-0lvjsLbgEJHHgUfIv6nfykT" alt="生命周期" /></p>
<p>可以看到我们的一个页面在加载创建时需要执行：</p>
<p>构造函数 -&gt; initState -&gt; didChangeDependencies -&gt; build 方法，然后才会渲染为一个页面。</p>
<p>当销毁关闭时：</p>
<p>deactivate -&gt; dispose</p>
<p>内部的前后台页面状态变化主要有：</p>
<pre><code class="dart language-dart">enum AppLifecycleState {
  // 恢复可见
  resumed,
  // 不可见，后台运行，无法处理用户响应
  inactive,
  // 处在并不活动状态，无法处理用户响应。例如来电，画中画，弹框
  paused,
  // 应用被立刻暂停挂起，ios上不会回调这个状态
  suspending,
}
</code></pre>
<p>当页面更新时会执行：</p>
<p>didUpdateWidget -&gt; build</p>
<p>可能会调用多次。</p>
<p>那么接下来通过代码实例来了解 Flutter 的生命周期：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';

class StateSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return StateSamplesState();
  }
}

class StateSamplesState extends State&lt;StateSamples&gt;
    with WidgetsBindingObserver {
  //插入渲染树时调用，只调用一次
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  //构建Widget时调用
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('LifeCycleState'),
      ),
      body: Center(
        child: Column(
          children: &lt;Widget&gt;[],
        ),
      ),
    );
  }

  //state依赖的对象发生变化时调用
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  //组件状态改变时候调用，可能会调用多次
  @override
  void didUpdateWidget(StateSamples oldWidget) {
    super.didUpdateWidget(oldWidget);
  }

  //当移除渲染树的时候调用
  @override
  void deactivate() {
    super.deactivate();
  }

  //组件即将销毁时调用
  @override
  void dispose() {
    super.dispose();
    WidgetsBinding.instance.removeObserver(this);
  }

  //APP生命周期监听
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      //恢复可见
    } else if (state == AppLifecycleState.paused) {
      //处在并不活动状态，无法处理用户响应
      //例如来电，画中画，弹框
    } else if (state == AppLifecycleState.inactive) {
      //不可见，后台运行，无法处理用户响应
    } else if (state == AppLifecycleState.suspending) {
      //应用被立刻暂停挂起，ios上不会回调
    }
    super.didChangeAppLifecycleState(state);
  }

  //其他方法

  //热重载时调用
  @override
  void reassemble() {
    super.reassemble();
  }

  //路由弹出
  @override
  Future&lt;bool&gt; didPopRoute() {
    return super.didPopRoute();
  }

  //新的路由
  @override
  Future&lt;bool&gt; didPushRoute(String route) {
    return super.didPushRoute(route);
  }

  //系统窗口相关改变回调，例如旋转
  @override
  void didChangeMetrics() {
    super.didChangeMetrics();
  }

  //文字缩放大小变化
  @override
  void didChangeTextScaleFactor() {
    super.didChangeTextScaleFactor();
  }

  //本地化语言变化
  @override
  void didChangeLocales(List&lt;Locale&gt; locale) {
    super.didChangeLocales(locale);
  }

  //低内存回调
  @override
  void didHaveMemoryPressure() {
    super.didHaveMemoryPressure();
  }

  //当前系统改变了一些访问性活动的回调
  @override
  void didChangeAccessibilityFeatures() {
    super.didChangeAccessibilityFeatures();
  }

  //平台色调主题变化时
  @override
  void didChangePlatformBrightness() {
    super.didChangePlatformBrightness();
  }
}
</code></pre>
<h3 id="2flutter">2 Flutter 按键监听</h3>
<p>我们知道在 Android 或 iOS 平台上，手机上或遥控器上的一些实体按键是可以被监听到的，可以执行相关操作，当然 Flutter 上也可以进行按键监听。</p>
<p>首先看下返回键的监听，返回键监听拦截在 Flutter 中比较不一样。是单独使用一个组件：WillPopScope。</p>
<p>然后通过一个实例来看下 Flutter 中实现连按两次返回键退出的效果：</p>
<pre><code class="dart language-dart">class KeyListenerState extends State&lt;KeyListenerSamples&gt; {
  int last = 0;
  int index = 0;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // 要用WillPopScope包裹
    return WillPopScope(
      // 编写onWillPop逻辑
      onWillPop: _onWillPop,
      child: Scaffold(
          appBar: AppBar(
            title: Text('KeyListener Demo'),
          ),
          body: Center(
            child: Text("按键监听"),
          )),
    );
  }

  // 返回键拦截执行方法
  Future&lt;bool&gt; _onWillPop() {
    int now = DateTime.now().millisecondsSinceEpoch;
    print(now - last);
    if (now - last &gt; 1000) {
      last = now;
      // showToast("再按一次返回键退出");
      return Future.value(false); //不退出
    } else {
      return Future.value(true); //退出
    }
  }
}
</code></pre>
<p>那么其他按键的监听使用的是 RawKeyboardListener。</p>
<p>RawKeyboardListener 继承自 StatefulWidget。</p>
<pre><code class="dart language-dart">const RawKeyboardListener({
    Key key,
    // 焦点节点
    @required this.focusNode,
    // RawKeyEvent，按键事件
    @required this.onKey,
    // 子控件
    @required this.child,
  })
</code></pre>
<p>我们再看下 RawKeyEvent 的构造方法：</p>
<pre><code class="dart language-dart">const RawKeyEvent({
    // RawKeyEventData
    @required this.data,
    this.character,
  })
</code></pre>
<p>监听 Android 平台使用 RawKeyEventDataAndroid，监听 Fuchsia 平台使用RawKeyEventDataFuchsia，iOS 平台暂时还没有发布。</p>
<p>RawKeyboardListener 用法：</p>
<pre><code class="dart language-dart">class KeyListenerState extends State&lt;KeyListenerSamples&gt; {
  FocusNode focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    FocusScope.of(context).requestFocus(focusNode);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('RawKeyboardListener Demo'),
        ),
        // RawKeyboardListener包裹
        body: RawKeyboardListener(
            // 可以监听到的前提是有焦点，我们可以让组件先获取焦点
            focusNode: focusNode,
            onKey: (RawKeyEvent event) {
              // 这里是监听Android平台按键，并且是KeyDown事件
              if (event is RawKeyDownEvent &amp;&amp;
                  event.data is RawKeyEventDataAndroid) {
                RawKeyDownEvent rawKeyDownEvent = event;
                RawKeyEventDataAndroid rawKeyEventDataAndroid =
                    rawKeyDownEvent.data;
                print("keyCode: ${rawKeyEventDataAndroid.keyCode}");
                switch (rawKeyEventDataAndroid.keyCode) {
                  // 这里面的KeyCode值和Android平台的一致
                  case 19: //KEY_UP
                    break;
                  case 20: //KEY_DOWN
                    break;
                  case 21: //KEY_LEFT

                    break;
                  case 22: //KEY_RIGHT

                    break;
                  case 23: //KEY_CENTER
                    break;
                  default:
                    break;
                }
              }
            },
            child: Center(
              child: Text("按键监听"),
            )),
      );
  }
}
</code></pre>
<p>当然我们也可以把 RawKeyboardListener 应用在输入框的焦点获取和监听上。</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_18">本节课实例地址请单击这里查看</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的生命周期和按键监听的用法和特点。主要注意点和建议如下：</p>
<ul>
<li>重点掌握 Flutter 生命周期的几个状态和返回键的拦截处理的用法。</li>
<li>尝试编写监听输入框的按键事件和焦点事件。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>