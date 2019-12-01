---
title: Flutter：从入门到实践-31
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用 Flutter 开发的过程中，可能有各种各样的 UI、需求、技术方案，有些无法通过现有的 Flutter Widget 来实现，那么这个时候我们就需要写插件（实际上就是调用原生的 API），想实现与原生的 API 交互、跳转、混合编写，就涉及到了 Flutter 与原生的交互。Flutter 是支持和原生 API 进行交互的，这节课我们将介绍 Flutter 中实现与原生交互的方法，</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 与原生交互简介</li>
  <li>Flutter 中调用原生 API</li>
  <li>原生调用 Flutter 中的 API</li>
  <li>Flutter 原生控件混合使用</li>
  <li>Flutter 跳转到原生页面</li>
  <li>原生页面跳转到 Flutter 页面</li>
  </ul>
</blockquote>
<h3 id="1flutter">1 Flutter 与原生交互简介</h3>
<p>当我们在开发过程中，遇到某些功能无法通过 Flutter 进行实现时，这时我们可以选择使用第三方插件，如果第三方插件没有，那么我们就需要自己进行编写与原生交互的逻辑，通过 Flutter 进行与原生 API 进行交互。当然 Flutter 也可以进行混合开发，就是原生 APP 里加入 Flutter 页面或 Flutter 应用页面里加入原生的页面。</p>
<p>Flutter 与原生交互最核心的就是通过 MethodChannel 方式进行交互、传值、调用。</p>
<p>我们看下官方的原理图：</p>
<p><img src="https://images.gitbook.cn/FjIFqUOdVD1gpCaJFwJDHmuqu_Ed" alt="Flutter与原生" /></p>
<p>所以 Android 和 iOS 都是通过 MethodChannel 方式进行交互、传值、调用。其他平台原理一样，Flutter 的插件库其实就是 Flutter 与原生的交互实现的。</p>
<p>我们可以把 Flutter 看成是客户端，对应的 Android 和 iOS 平台看成是服务器端。双方是通过消息发送来交互通信的，Android 和 iOS 通过 MethodChannel 发送消息给 Flutter 客户端；Flutter 通过 MethodChannel 发送数据、消息给 Android 平台，通过 FlutterMethodChannel 发送数据、消息给 iOS 平台。这样就达到了双向交互通信。</p>
<p>那么这节课我们就以 Android 平台为例，给大家讲解 Flutter 与原生交互的几种实现方法。</p>
<h3 id="2flutterapi">2 Flutter 中调用原生 API</h3>
<p>我们来看下 Flutter 中调用原生 API 和原生 API 调用 Flutter 中 API 的实现。</p>
<p>Flutter 与原生的调用编写建议大家使用 Android Studio 或者 IntelliJ Idea，不建议使用 VSCode。</p>
<p>Flutter 中调用原生 API，并传递参数，然后从原生返回值。</p>
<p>我们先看一个 Flutter 官方给的简单的例子，就是调用原生 API 获取电池电量信息，并返回电量信息。</p>
<p>我们使用 Android Studio 创建项目或打开项目，编写逻辑。结构如下：</p>
<p><img src="https://images.gitbook.cn/Fo_D1JJHRBnIGKZ5KWpUQSJBsTj_" alt="Flutter项目结构" /></p>
<p>我们的主要逻辑都是写在 MainActivity 里：</p>
<pre><code class="dart language-dart">// 编写Android端逻辑
package com.flutter.flutter_app;

import android.content.ContextWrapper;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.BatteryManager;
import android.os.Build;
import android.os.Bundle;

import io.flutter.app.FlutterActivity;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;
import io.flutter.plugins.GeneratedPluginRegistrant;

public class MainActivity extends FlutterActivity {
    // 定义CHANNEL名称，要和Flutter中定义的一致才可以匹配
    private static final String CHANNEL = "samples.flutter.io/battery";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Flutter插件注册
        GeneratedPluginRegistrant.registerWith(this);
        // 使用MethodChannel进行通信
        new MethodChannel(getFlutterView(), CHANNEL).setMethodCallHandler(
                new MethodChannel.MethodCallHandler() {
                    @Override
                    public void onMethodCall(MethodCall call, MethodChannel.Result result) {
                        // 使用MethodCall进行方法名匹配
                        if (call.method.equals("getBatteryLevel")) {
                            // 获取电池电量信息
                            int batteryLevel = getBatteryLevel();
                            if (batteryLevel != -1) {
                                // 通过MethodChannel.Result返回结果给Flutter客户端
                                result.success(batteryLevel);
                            } else {
                                result.error("UNAVAILABLE", "Battery level not available.", null);
                            }
                        } else {
                            result.notImplemented();
                        }
                    }
                });
    }
    // 编写原生API得获取电池电量信息的方法
    private int getBatteryLevel() {
        int batteryLevel = -1;
        if (Build.VERSION.SDK_INT &gt;= Build.VERSION_CODES.LOLLIPOP) {
            BatteryManager batteryManager = (BatteryManager) getSystemService(BATTERY_SERVICE);
            batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
        } else {
            Intent intent = new ContextWrapper(getApplicationContext()).
                    registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
            batteryLevel = (intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) * 100) /
                    intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
        }
        return batteryLevel;
    }
}
</code></pre>
<p>我们来看下其中几个参数：</p>
<pre><code class="dart language-dart">public final class MethodCall {
    public final String method;
    public final Object arguments;
    ... ...
}
</code></pre>
<p>MethodCall 有两个属性：一个 method，用于获取调用的方法名；另一个是 arguments，用于 Flutter 传递参数给原生端。</p>
<pre><code class="dart language-dart">public interface Result {
    void success(@Nullable Object var1);

    void error(String var1, @Nullable String var2, @Nullable Object var3);

    void notImplemented();
}
</code></pre>
<p>MethodChannel.Result 有三个回调方法：success，成功回调；error，错误回调；notImplemented，未实现的方法。</p>
<p>我们再看下 Flutter 端的编写逻辑：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

class NativeSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return NativeSamplesState();
  }
}

class NativeSamplesState extends State&lt;NativeSamples&gt; {
  // 创建MethodChannel
  static const platform = const MethodChannel('samples.flutter.io/battery');
  // 定义电量信息变量
  String _batteryLevel = 'Unknown battery level.';

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter with Native'),
        primary: true,
      ),
      body: Column(
        children: &lt;Widget&gt;[
            // 点击获取电量信息
          RaisedButton(
            child: Text('Get Battery Level'),
            onPressed: _getBatteryLevel,
          ),
          // 显示电量信息
          Text(_batteryLevel),
        ],
      ),
    );
  }
  // 调用原生获取电量信息的方法
  Future&lt;Null&gt; _getBatteryLevel() async {
    String batteryLevel;
    try {
      // 通过invokeMethod进行反射调用获取电量的原生中定义的方法名，获取返回值 
      final int result = await platform.invokeMethod('getBatteryLevel');
      batteryLevel = 'Battery level at $result % .';
    } on PlatformException catch (e) {
      batteryLevel = "Failed to get battery level: '${e.message}'.";
    }
    // 更新返回结果值
    setState(() {
      _batteryLevel = batteryLevel;
    });
  }
}
</code></pre>
<p>我们再实现一个稍微复杂点的权限申请的例子，Flutter 中点击按钮，传递参数实现调用原生的权限申请，并返回状态。</p>
<pre><code class="dart language-dart">// 前面的步骤相同，就不重复，直接写Flutter逻辑
  // 判断是否有权限，无权限就主动申请权限
  Future&lt;Null&gt; _requestPermission() async {
    bool hasPermission;
    try {
      // 传递参数，key-value形式
      hasPermission =
          await platform.invokeMethod('requestPermission', &lt;String, dynamic&gt;{
        'permissionName': 'WRITE_EXTERNAL_STORAGE',
        'permissionId': 0,
      });
    } on PlatformException catch (e) {
      hasPermission = false;
    }

    setState(() {
      _hasPermission = hasPermission;
    });
  }
</code></pre>
<p>这里可以看到传递参数可以传递多个参数，invokeMethod 的构造方法如下：</p>
<pre><code class="dart language-dart">Future&lt;T&gt; invokeMethod&lt;T&gt;(String method, [ dynamic arguments ]) async{
  ... ...
}

// 使用示例如下
_channel.invokeMethod('play', &lt;String, dynamic&gt;{
        'song': song.id,
        'volume': volume,
}
</code></pre>
<p>我们再看下 Android 端调用代码逻辑:</p>
<pre><code class="dart language-dart">public class MainActivity extends FlutterActivity {
    private static final String CHANNEL = "samples.flutter.io/battery";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Flutter插件注册
        GeneratedPluginRegistrant.registerWith(this);

        new MethodChannel(getFlutterView(), CHANNEL).setMethodCallHandler(
                new MethodChannel.MethodCallHandler() {
                    @Override
                    public void onMethodCall(MethodCall call, MethodChannel.Result result) {
                        switch (call.method) {
                            case "getBatteryLevel":
                                int batteryLevel = getBatteryLevel();
                                if (batteryLevel != -1) {
                                    result.success(batteryLevel);
                                } else {
                                    result.error("UNAVAILABLE", "Battery level not available.", null);
                                }
                                break;
                            case "requestPermission":
                                // 申请权限，获取参数
                                final String permissionName = call.argument("permissionName");
                                final int permissionId = call.argument("permissionId");
                                // 调用申请权限方法
                                boolean hasPermission = requestPermission();
                                System.out.println(permissionName + "   " + permissionId);
                                // 回调返回结果给Flutter
                                result.success(hasPermission);
                                break;
                            default:
                                result.notImplemented();
                        }
                    }
                });
    }

    private int getBatteryLevel() {
        int batteryLevel = -1;
        if (Build.VERSION.SDK_INT &gt;= Build.VERSION_CODES.LOLLIPOP) {
            BatteryManager batteryManager = (BatteryManager) getSystemService(BATTERY_SERVICE);
            batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
        } else {
            Intent intent = new ContextWrapper(getApplicationContext()).
                    registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
            batteryLevel = (intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) * 100) /
                    intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
        }
        return batteryLevel;
    }

    // 请求权限
    private boolean requestPermission() {
        if (Build.VERSION.SDK_INT &gt;= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) {
                requestPermissions(
                        new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        0);
                return false;
            } else {
                return true;
            }
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 0) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "权限已申请", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "权限已拒绝", Toast.LENGTH_SHORT).show();
            }
        }
    }
}
</code></pre>
<p>下面是这两个实例的运行效果图：</p>
<p><img src="https://images.gitbook.cn/FpCZnfco81ksyobqTCaC7MAVKuDS" alt="交错动画效果图" /></p>
<h3 id="3flutterapi">3 原生调用 Flutter 中的 API</h3>
<p>之前讲了 Flutter 可以发送消息给原生端，来实现调用原生方法 API。这里给大家讲解原生发送消息给 Flutter 客户端，实现原生调用 Flutter 的 API。本质还是通过 MethodChannel，不过这里要使用的是封装过的 MethodChannel：EventChannel。</p>
<p>我们看下原生 Android 端的编写逻辑：</p>
<pre><code class="dart language-dart">public class EventChannelActivity extends FlutterActivity {
    // 定义一个Channel名字,Flutter端要和它一致
    public static final String STREAM = "com.flutter.eventchannel/stream";
    @BindView(R.id.toolBar)
    Toolbar toolBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event_channel);
        ButterKnife.bind(this);
        toolBar.setTitle("EventChannel");

        new EventChannel(getFlutterView(), STREAM).setStreamHandler(
                new EventChannel.StreamHandler() {
                    @Override
                    public void onListen(Object args, final EventChannel.EventSink events) {
                        // 这样我们就可以通过监听，随时随地发送消息指令给Flutter客户端了
                        Log.i("info", "adding listener");
                        events.success("从原生发送过来的指令信息");
                    }

                    @Override
                    public void onCancel(Object args) {
                        Log.i("info", "cancelling listener");
                    }
                }
        );
    }
}

// EventSink的三个回调方法
public interface EventSink {
    void success(Object var1);

    void error(String var1, String var2, Object var3);

    void endOfStream();
}
</code></pre>
<p>接下来看下 Flutter 客户端的逻辑：</p>
<pre><code class="dart language-dart">... ...
class _MyHomePageState extends State&lt;MyHomePage&gt; {
  // 定义一个Channel名字,Flutter端要和原生端一致
  static const EventChannel eventChannel =
      EventChannel('com.flutter.eventchannel/stream');
  StreamSubscription _streamSubscription = null;

  String _eventString = '';

  @override
  void initState() {
    super.initState();
    // 创建EventChannel，并监听数据
    _streamSubscription = eventChannel
        .receiveBroadcastStream()
        .listen(_onEvent, onError: _onError);
  }

  void _onEvent(Object event) {
    print("原生发送过来的：$event.toString()");
    setState(() {
      _eventString = "原生发送过来的：$event";
    });
  }

  void _onError(Object error) {
    setState(() {
      PlatformException exception = error;
      _eventString = exception?.message ?? '错误';
    });
  }
  // 停止监听接收消息
  void _disableEvent() {
    if (_streamSubscription != null) {
      _streamSubscription.cancel();
      _streamSubscription = null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: &lt;Widget&gt;[
            RaisedButton(
              child: Text('接收原生发送的消息$_eventString'),
              onPressed: null,
            ),
          ],
        ),
      ),
    );
  }
}
</code></pre>
<p>这样的通信方式，我们可以应用在例如接收原生的广播、网络状态、时间变化、电池电量等等信息上，或者其他方面。</p>
<h3 id="4flutter">4 Flutter 原生控件混合使用</h3>
<p>Flutter 支持原生控件和 Flutter 控件进行混合使用，不过不推荐这种方式，一个是因为麻烦；另一个就是可能会引起其他问题。所以不是必须要这样实现的情况下，不推荐这种用法。</p>
<p>原理跟 Flutter 和原生交互一样，通过 MethodChannel。</p>
<pre><code class="dart language-dart">// 编写Flutter端方法

// 添加原生布局/控件
Future&lt;Null&gt; _addNativeLayout() async {
  try {
    await platform.invokeMethod('addNativeLayout');
  } on PlatformException catch (e) {}
}

// 编写Android端逻辑
private static final String CHANNEL = "samples.flutter.io/battery";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Flutter插件注册
        GeneratedPluginRegistrant.registerWith(this);

        new MethodChannel(getFlutterView(), CHANNEL).setMethodCallHandler(
                new MethodChannel.MethodCallHandler() {
                    @Override
                    public void onMethodCall(MethodCall call, MethodChannel.Result result) {
                        switch (call.method) {
                            case "addNativeLayout":
                                // 添加布局到现有的Flutter布局中
                                FrameLayout v = (FrameLayout) findViewById(android.R.id.content);
                                View linearLayout = new LinearLayout(MainActivity.this);
                                linearLayout.setBackgroundColor(0xff00BFFF);
                                ViewGroup.MarginLayoutParams marginLayoutParams = new ViewGroup.MarginLayoutParams(600, 600);
                                ((LinearLayout) linearLayout).setGravity(Gravity.CENTER);
                                marginLayoutParams.setMargins(200, 230, 0, 0);
                                linearLayout.setLayoutParams(marginLayoutParams);
                                v.addView(linearLayout);
                                TextView textView = new TextView(MainActivity.this);
                                textView.setText("我是原生布局/控件");
                                textView.setTextColor(Color.parseColor("#FFFFFF"));
                                textView.setGravity(Gravity.CENTER);
                                ((LinearLayout) linearLayout).addView(textView);
                                break;
                            default:
                                result.notImplemented();
                        }
                    }
                });
    }
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FkOIOgwhdq551yHauG0qneTeMGUC" alt="原生控件添加效果图" /></p>
<p>我们通过 <code>findViewById(android.R.id.content)</code> 获取到我们 UI 的最外层父布局FrameLayout，然后向里面 addView。我们的 Flutter 的页面其实就是一个 SurfaceView。</p>
<h3 id="5flutter">5 Flutter 跳转到原生页面</h3>
<p>接下来我们看下如何从 Flutter 页面跳转到原生页面。</p>
<p>跳转原生页面其实也是通过 MethodChannel 定义一个跳转方法即可：</p>
<pre><code class="dart language-dart">// 编写Flutter端方法

// 跳转到原生页面
Future&lt;Null&gt; _toNativeActivity() async {
  try {
    await platform.invokeMethod('toNativeActivity');
  } on PlatformException catch (e) {}
}

// 编写Android端逻辑
public class MainActivity extends FlutterActivity {
    private static final String CHANNEL = "samples.flutter.io/battery";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Flutter插件注册
        GeneratedPluginRegistrant.registerWith(this);

        new MethodChannel(getFlutterView(), CHANNEL).setMethodCallHandler(
                new MethodChannel.MethodCallHandler() {
                    @Override
                    public void onMethodCall(MethodCall call, MethodChannel.Result result) {
                        switch (call.method) {
                            case "toNativeActivity":
                                // 跳转到原生Activity界面
                                Intent intent = new Intent(MainActivity.this, NativeActivity.class);
                                startActivity(intent);
                                break;
                            default:
                                result.notImplemented();
                        }
                    }
                });
    }
}
</code></pre>
<p>我们在 Android 项目里新建一个 Activity，绘制自己的布局和编写原生逻辑。</p>
<p>这里建议新建一个 Android Studio 项目窗口（并且打开 Android 项目这一级别的项目目录，而不是 Flutter 这一级别的），这样就可以用 Android Studio 编写 Android 端逻辑了。</p>
<p>运行效果如下：</p>
<p><img src="https://images.gitbook.cn/FphN308miG4zlzF0czHINIdkoWzE" alt="跳转原生页面效果图" /></p>
<h3 id="6flutter">6 原生页面跳转到 Flutter 页面</h3>
<p>接下来我们看下如何从原生页面跳转到 Flutter 页面，步骤有点不太一样。</p>
<p>我们要使用 Android Studio 新建一个 Flutter Module。</p>
<p><img src="https://images.gitbook.cn/FgphKyXVemcRWzE3aMA57gsPXnpQ" alt="新建Flutter Module" /></p>
<p><img src="https://images.gitbook.cn/FrPhSuow-SHTt8rxFJC_013mzbtR" alt="avatar" /></p>
<p>新建后的结构如下：</p>
<p><img src="https://images.gitbook.cn/FlZ2bMhKffF6r2G8_Nn-yX1pBJhY" alt="新建Flutter Module" /></p>
<p>我们将 Android 项目用新的窗口打开一下，这样方便编写 Android 逻辑：</p>
<p><img src="https://images.gitbook.cn/FqujXBJHBFZHKabwGPh0iHXgBDRK" alt="新建Flutter Module" /></p>
<p>可以看到，我们的 module 为 Flutter，Android 项目目录为 app。</p>
<p>其他的配置工作我们不用关心，Android Studio 已经帮我们配置好了，包括依赖 Flutter 这个 module。</p>
<p>我们不管默认的 MainActivity，新建一个 NativeActivity.class（名字可以随便取），在里面编写原生逻辑：</p>
<pre><code class="dart language-dart">// NativeActivity里我们就新建一个按钮，点击按钮跳转到Flutter页面
 @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.fab:
                Intent intent
                        = new Intent(this, NativeFlutterActivity.class);
                startActivity(intent);
                break;
        }
    }
</code></pre>
<p>这里可以直接跳转到 Flutter 页面，也可以新建一个单独的承载 Flutter 页面的 Activity 来管理，我这里又单独建了一个 NativeFlutterActivity：</p>
<pre><code class="dart language-dart">package com.flutter.flutter_module.host;

import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.FrameLayout;

import io.flutter.facade.Flutter;
import io.flutter.view.FlutterView;

public class NativeFlutterActivity extends AppCompatActivity {
    private FrameLayout fl_container;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_flutter);
        fl_container = findViewById(R.id.fl_container);

        // 第一种方式：Flutter.createView，route1为自定义的路由名称
        FlutterView flutterView = Flutter.createView(
                NativeFlutterActivity.this,
                getLifecycle(),
                "route1"
        );
        fl_container.addView(flutterView);

        // 第二种方式：Flutter.createFragment，route1为自定义的路由名称
        // FragmentTransaction fragmentTransaction = getSupportFragmentManager().beginTransaction();
        // fragmentTransaction.replace(R.id.fl_container, Flutter.createFragment("route1"));
        // fragmentTransaction.commit();

        // 为了避免跳转黑屏以及过渡，默认布局隐藏invisible，可以在第一帧绘制出来后，显示布局
        final FlutterView.FirstFrameListener[] listeners = new FlutterView.FirstFrameListener[1];
        listeners[0] = new FlutterView.FirstFrameListener() {
            @Override
            public void onFirstFrame() {
                fl_container.setVisibility(View.VISIBLE);
            }
        };
        flutterView.addFirstFrameListener(listeners[0]);
    }
}

// 布局
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/fl_container"
    android:layout_width="match_parent"
    android:background="@color/white"
    android:visibility="invisible"
    android:layout_height="match_parent"
    tools:context=".NativeFlutterActivity"&gt;
&lt;/FrameLayout&gt;

// 避免黑屏，主题设置为透明，背景色改为白色
&lt;style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar"&gt;
    &lt;!-- Customize your theme here. --&gt;
    &lt;item name="android:windowBackground"&gt;@drawable/launch_background&lt;/item&gt;
    &lt;item name="android:windowIsTranslucent"&gt;true&lt;/item&gt;
&lt;/style&gt;

// 项目清单注册设置好主题
&lt;activity
    android:name=".NativeFlutterActivity"
    android:theme="@style/AppTheme" /&gt;
</code></pre>
<p>我们再编写 Flutter 页面逻辑：</p>
<pre><code class="dart language-dart">import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'practice_two_samples.dart';

//void main() =&gt; runApp(MyApp());

void main() =&gt; runApp( _widgetForRoute(window.defaultRouteName));

// 处理路由跳转
Widget _widgetForRoute(String route) {
  switch (route) {
    case 'route1':
      return MyApp();
    case 'route2':
      return MaterialApp(
        title: 'Flutter with Native',
        theme: ThemeData(
          primarySwatch: Colors.teal,
        ),
        home: PracticeTwoSamples(),
      );
    default:
      return Center(
        child: Text('Unknown route: $route', textDirection: TextDirection.ltr),
      );
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter with Native',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: MyHomePage(title: 'Flutter with Native'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() =&gt; _MyHomePageState();
}

class _MyHomePageState extends State&lt;MyHomePage&gt; {
  static const platform = const MethodChannel('samples.flutter.io/battery');

  // Get battery level.
  String _batteryLevel = 'Unknown battery level.';
  bool _hasPermission = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
... ...
</code></pre>
<p>最后来看下运行效果：</p>
<p><img src="https://images.gitbook.cn/Fg6uaF86hKYMQd36lwJb2NaVaQpB" alt="原生跳转到Flutter页面动画效果图" /></p>
<p>如果想处理 Flutter 的返回事件，那么就要重写 Activity 的返回事件：</p>
<pre><code class="java language-java"> @Override
    public void onBackPressed() {
        if (this.flutterView != null) {
            this.flutterView.popRoute();
        } else {
            super.onBackPressed();
        }
    }
</code></pre>
<p>官方介绍的原生混合 Flutter 页面的文档地址：</p>
<p><a href="https://github.com/flutter/flutter/wiki/Add-Flutter-to-existing-apps">https://github.com/flutter/flutter/wiki/Add-Flutter-to-existing-apps</a></p>
<p>最后扩展一下，如果我们想判断某个页面是否是 Flutter 编写的，例如闲鱼的商品详情页就是 Flutter 编写的。那么就在手机的开发者模式中开启：显示布局边界。</p>
<p><img src="https://images.gitbook.cn/FhuLfrZf8xPWwPIPf9ddaddnCbWB" alt="显示布局边界" /></p>
<p><img src="https://images.gitbook.cn/Fjx6KnC6d9A8GFMks3ZfWudtnmZa" alt="闲鱼原生页面" /></p>
<p><img src="https://images.gitbook.cn/Ft1x-qZiovp6vSD3kBbUzGpIWrCy" alt="闲鱼Flutter页面" /></p>
<p>我们可以很明显看到，Flutter 编写的页面整体就一个 FlutterView（SurfaceView）。</p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_28">flutter_28</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 与原生交互的几种用法。需要大家重点掌握 Flutter 调用原生 API、Flutter 跳转到原生及原生跳转到 Flutter 页面的方法，实践后尝试编写混合应用。</p></div></article>