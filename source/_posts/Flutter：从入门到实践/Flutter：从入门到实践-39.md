---
title: Flutter：从入门到实践-39
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面我们已经学习了很多基础知识，这节课我们继续进行一个扩展实践。我们不应该仅仅局限于常规应用的开发，也应该扩展到其他一些方面的领域，如音视频播放、Android TV 开发等。那么这节课的内容就是做一个简易的音视频播放器，实现音视频的播放功能。通过这个实例我们可以复习巩固我们之前学过的知识，也算是一个总结与检验。本课练习篇主要是将通过一些官方插件库和第三方插件库等来完成一个简易的音视频播放器，一起来实践吧。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 音视频播放器简介</li>
  <li>Flutter 视频播放器的实现</li>
  <li>Flutter 音频播放器的实现</li>
  </ul>
</blockquote>
<h3 id="flutter">Flutter 音视频播放器简介</h3>
<p>音视频部分其实也不是很难，对于原生 Android 平台，Google 有 ExoPlayer，支持常见的很多种视频格式和协议，性能、功能和稳定性也非常的好。其他平台也都有各自的播放器 API。Flutter 本身目前的  API 并不支持音视频播放处理，毕竟无法达到原生播放器的体验和效果。所以官方的插件库也都是分别调用和封装原生播放器进行的 API 交互处理，本质都是使用的原生播放器进行播放处理。</p>
<p>今天我们的视频播放器将要使用的就是官方的 video_player 插件库：</p>
<p><a href="https://pub.dev/packages/video_player">https://pub.dev/packages/video_player</a></p>
<p>官方例子效果图：</p>
<p><img src="https://images.gitbook.cn/01988880-baa3-11e9-8bd3-43e1fddff917" alt="官方例子效果图" /></p>
<p>音频播放器部分我们使用第三方插件库 AudioPlayers ：</p>
<p><a href="https://pub.dev/packages/audioplayers">https://pub.dev/packages/audioplayers</a></p>
<p>这个插件库也是调用的原生播放，只不过封装了一层 API。我们也可以自己写插件，基于原生的一些播放器 API 进行封装。这里暂时以这个音频插件库为例进行讲解。
这个 audioplayers 插件也是原生分别对应：</p>
<ul>
<li>Android 平台：MediaPlayer；</li>
<li>iOS 平台：AVAudioPlayer</li>
</ul>
<h3 id="flutter-1">Flutter 视频播放器的实现</h3>
<p>接下来我们看下 Flutter 视频播放器的一个调用使用。视频播放器将要使用的就是官方的 video_player 插件库：</p>
<p><a href="https://pub.dev/packages/video_player">https://pub.dev/packages/video_player</a></p>
<p><strong>本质就是分别对应调用的就是：</strong></p>
<ul>
<li>Android 平台：ExoPlayer</li>
<li>iOS 平台：AVPlayer</li>
</ul>
<p>做过 Android 或 iOS 原生开发的应该对这两个播放器库都非常的熟悉。 ExoPlayer 是 Google 官方推出的一个播放器库，非常的强大。AVPlayer 是 iOS 平台的原生播放器库。</p>
<p>那么 video_player 插件库就是基于这两个原生播放器进行插件封装 API。</p>
<p><strong>支持的格式：</strong></p>
<p>所支持的视频格式和协议也就是 ExoPlayer 和 AVPlayer 所对应支持的格式。</p>
<p>视频播放器所支持的视频播放地址流主要由三大部分组成：
1、视频/音频流协议（如：http，https，rtsp，rtmp，hls）
2、视频/音频编码格式（如：h264，h265，aac，pcm，mp3，wma）
3、视频/音频封装格式（如：.mp4，.mp3，.flv，.ts，.m3u8）</p>
<p>具体 Android 平台的 ExoPlayer 支持的格式，大家可以看官方文档：</p>
<p><a href="https://exoplayer.dev/supported-formats.html">https://exoplayer.dev/supported-formats.html</a></p>
<p>这里不再列举，大部分的都是支持的。还可以通过 FFmpeg extension 这个 ExoPlayer 的官方扩展库，来扩展更多音视频编解码功能。</p>
<p>苹果 iOS 平台的 AVPlayer 支持的格式、协议也非常的丰富，大家自行网络查询了解。</p>
<p>其实 ExoPlayer 和 AVPlayer 也可以作为音频播放器，这都是没问题的。也就是 video_player 也可以兼容作为音频播放器。</p>
<p>我们先看下视频播放器的效果图：</p>
<p><img src="https://images.gitbook.cn/2b060080-baa3-11e9-8bd3-43e1fddff917" alt="视频播放器的效果图" /></p>
<p><img src="https://images.gitbook.cn/3b7a30d0-baa3-11e9-8bd3-43e1fddff917" alt="视频播放器的效果图" /></p>
<p><img src="https://images.gitbook.cn/4a9d5010-baa3-11e9-8bd3-43e1fddff917" alt="视频播放器的效果图" /></p>
<p><strong>视频播放器实现了：全屏半屏切换，控制操作栏的显示与隐藏，播放和暂停，进度时时显示，播放时长和总时长的格式化显示，手势操作的一部分等功能。</strong></p>
<p>接下来我们就进行编写 Flutter 的视频播放器。</p>
<p>引入 video_player 插件库：</p>
<pre><code class="dart language-dart">dependencies:
  video_player: ^0.10.1+6
</code></pre>
<p>使用的地方进行导包：</p>
<pre><code class="dart language-dart">import 'package:video_player/video_player.dart';
</code></pre>
<p>整个视频的播放通过 VideoPlayerController 进行控制，所以我们需要先实例化 VideoPlayerController，它支持三种方式载入视频：</p>
<p><img src="https://images.gitbook.cn/5737a190-baa3-11e9-8bd3-43e1fddff917" alt="VideoPlayer" /></p>
<p>支持本地文件、资源文件、网络视频流的播放。</p>
<p>整个的播放的开始、监听、暂停、停止等等操作都是通过 VideoPlayerController 来控制。</p>
<p>视频的渲染组件是 VideoPlayer。</p>
<p>先大概看下 VideoPlayer 的几个主要的方法：</p>
<pre><code class="dart language-dart">//监听视频状态
_controller.addListener((){);
//缓冲初始化
_controller.initialize();
//是否循环播放
_controller.setLooping(true);
//设置视频音量（0-1）
_controller.setVolume(1);
//播放视频
_controller.play();
//暂停播放
_controller.pause();
//移除监听
_controller.removeListener(listener);
//销毁播放器
_controller.dispose();
//指定播放位置
_controller.seekTo(Duration moment)
</code></pre>
<p>接下来看下具体实现：</p>
<pre><code class="dart language-dart">//播放页很简单，就是调用了播放器的我们自己封装的Widget

import 'package:flutter/material.dart';
import 'package:flutter_video_audio/widgets/video_widget.dart';

class VideoPage extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return VideoPageState();
  }
}

class VideoPageState extends State&lt;VideoPage&gt; with WidgetsBindingObserver {

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      //调用了播放器的我们自己封装的Widget:VideoWidget
      body: VideoWidget(),
    );
  }

  @override
  void dispose() {
    super.dispose();
    WidgetsBinding.instance.removeObserver(this);
  }
}
</code></pre>
<p>接下来具体看下 VideoWidget 的封装内容：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_video_audio/utils/utils.dart';
import 'package:video_player/video_player.dart';

class VideoWidget extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return VideoWidgetState();
  }
}

class VideoWidgetState extends State&lt;VideoWidget&gt; {
  //播放器核心控制器
  VideoPlayerController _controller;
  //记录当前播放位置
  int position = 0;
  //记录播放器高度，用来设置是否全屏
  double height = 0;
  //用来标记设置是否全屏
  bool fullScreen = false;
  //用来标记是否隐藏标题栏
  bool hideAppBar = false;
  //用来标记是否隐藏控制栏和顶部的信息栏
  bool hideControllBar = false;
  //缓冲中提示语
  String tips = '缓冲中...';
  //播放或者暂停的图标切换
  IconData _icons = Icons.pause_circle_outline;
  //拖动手势操作位移记录
  double dy = 0;

  @override
  void initState() {
    super.initState();
    //实例化播放器控制器
    _controller = VideoPlayerController.network(
        'https://media.w3.org/2010/05/sintel/trailer.mp4');

        //添加监听
    _controller.addListener(() {
      if (_controller.value.hasError) {
        print(_controller.value.errorDescription);
        setState(() {
          tips = '播放出错';
        });
      } else if (_controller.value.initialized) {
        setState(() {
          position = _controller.value.position.inSeconds;
          tips = '';
        });
      } else if (_controller.value.isBuffering) {
        setState(() {
          tips = '缓冲中...';
        });
      }
    });
    _controller.initialize().then((_) {
      setState(() {
        _controller.play();
        _controller.setVolume(1);
      });
    });
    _controller.setLooping(true);
    height = 200;
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
        // 编写onWillPop逻辑，拦截返回键
        onWillPop: _onWillPop,
        child: Scaffold(
            appBar: getAppBar(),
            body: Container(
              color: Colors.black,
              height: height,
              child: _controller.value.initialized
                  ? Stack(
                      alignment: Alignment.center,
                      children: &lt;Widget&gt;[
                        AspectRatio(
                          aspectRatio: _controller.value.aspectRatio,
                          child: InkWell(
                            child: Stack(
                              alignment: Alignment.center,
                              children: &lt;Widget&gt;[
                                // 滑动控制音量、亮度、进度等操作
                                GestureDetector(
                                  onVerticalDragStart: (details) {
                                    dy = 0;
                                  },
                                  onVerticalDragUpdate: (details) {
                                    dy += details.delta.dy;
                                    print('${details.delta.dy}  :  $dy');
                                    print(dy /
                                        MediaQuery.of(context).size.height);
                                    _controller.setVolume(1);
                                  },
                                  onVerticalDragEnd: (details) {},
                                  child: VideoPlayer(_controller),
                                ),
                                Text(
                                  tips,
                                  style: TextStyle(
                                      fontSize: 16, color: Colors.white),
                                )
                              ],
                            ),
                            onTap: () {
                              setState(() {
                                hideControllBar = !hideControllBar;
                              });
                            },
                          ),
                        ),
                        // 播放器顶部标题栏
                        Align(
                          alignment: Alignment.topCenter,
                          child: Offstage(
                            offstage: hideControllBar,
                            child: Container(
                              color: Colors.black38,
                              padding: EdgeInsets.all(5),
                              child: Row(
                                children: &lt;Widget&gt;[
                                  InkWell(
                                    onTap: () {
                                      setState(() {
                                        if (fullScreen) {
                                          height = 200;
                                          //控制旋转屏幕
                                          SystemChrome
                                              .setPreferredOrientations([
                                            DeviceOrientation.portraitUp,
                                            DeviceOrientation.portraitUp,
                                          ]);
                                          SystemChrome
                                              .setEnabledSystemUIOverlays([
                                            SystemUiOverlay.top,
                                            SystemUiOverlay.bottom
                                          ]);
                                          hideAppBar = false;
                                        } else {
                                          print('关闭');
                                          Navigator.pop(context);
                                        }
                                      });
                                    },
                                    child: Icon(
                                      Icons.arrow_back_ios,
                                      color: Colors.white,
                                    ),
                                  ),
                                  Text(
                                    '标题',
                                    style: TextStyle(
                                        color: Colors.white, fontSize: 18),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                        // 播放器底部控制栏
                        Align(
                          alignment: Alignment.bottomCenter,
                          child: Offstage(
                            offstage: hideControllBar,
                            child: Container(
                              padding: EdgeInsets.all(5),
                              color: Colors.black54,
                              child: Row(children: &lt;Widget&gt;[
                                //播放或暂停按键
                                InkWell(
                                  onTap: () {
                                    setState(() {
                                      if (_controller.value.isPlaying) {
                                        _controller.pause();
                                        _icons = Icons.play_circle_outline;
                                      } else {
                                        _controller.play();
                                        _icons = Icons.pause_circle_outline;
                                      }
                                    });
                                  },
                                  child: Icon(
                                    _icons,
                                    color: Colors.white,
                                    size: 30,
                                  ),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                //播放进度
                                Text(
                                  TimeUtils.getCurrentPosition(position),
                                  style: TextStyle(color: Colors.white),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                // 进度条
                                Expanded(
                                    child: LinearProgressIndicator(
                                  value: TimeUtils.getProgress(position,
                                      _controller.value.duration.inSeconds),
                                  backgroundColor: Colors.black87,
                                )),
                                SizedBox(
                                  width: 10,
                                ),
                                //总时长
                                Text(
                                  TimeUtils.getCurrentPosition(
                                      _controller.value.duration.inSeconds),
                                  style: TextStyle(color: Colors.white),
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                //全屏按钮
                                InkWell(
                                  child: Icon(
                                    Icons.fullscreen,
                                    color: Colors.white,
                                    size: 30,
                                  ),
                                  onTap: () {
                                    fullOrMin();
                                  },
                                ),
                              ]),
                            ),
                          ),
                        ),
                      ],
                    )
                  : Container(
                      alignment: Alignment.center,
                      //没初始化时的显示的布局内容
                      child: Text(
                        tips,
                        style: TextStyle(fontSize: 16, color: Colors.white),
                      ),
                    ),
            )));
  }

  Widget getAppBar() {
    return PreferredSize(
        // Offstage来控制AppBar的显示与隐藏
        child: Offstage(
          offstage: hideAppBar,
          child: AppBar(
            title: Text('VideoPlayer'),
            primary: true,
          ),
        ),
        preferredSize:
            Size.fromHeight(MediaQuery.of(context).size.height * 0.07));
  }

  // 返回键拦截执行方法
  Future&lt;bool&gt; _onWillPop() {
    if (fullScreen) {
      setState(() {
        height = 200;
        //控制旋转屏幕
        SystemChrome.setPreferredOrientations([
          DeviceOrientation.portraitUp,
          DeviceOrientation.portraitUp,
        ]);
        SystemChrome.setEnabledSystemUIOverlays(
            [SystemUiOverlay.top, SystemUiOverlay.bottom]);
        hideAppBar = false;
        fullScreen = !fullScreen;
      });
      return Future.value(false); //不退出
    } else {
      return Future.value(true); //退出
    }
  }
  //全屏切换逻辑
  void fullOrMin() {
    setState(() {
      if (fullScreen) {
        height = 200;
        SystemChrome.setPreferredOrientations([
          DeviceOrientation.portraitUp,
          DeviceOrientation.portraitUp,
        ]);
        SystemChrome.setEnabledSystemUIOverlays(
            [SystemUiOverlay.top, SystemUiOverlay.bottom]);
        hideAppBar = false;
      } else {
        hideAppBar = true;
        height = MediaQuery.of(context).size.height;
        SystemChrome.setPreferredOrientations([
          DeviceOrientation.landscapeLeft,
          DeviceOrientation.landscapeLeft,
        ]);
        SystemChrome.setEnabledSystemUIOverlays([]);
      }
      fullScreen = !fullScreen;
    });
  }

  @override
  void dispose() {
    super.dispose();
    //退出销毁播放器
    _controller.dispose();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitUp,
    ]);
  }
}
</code></pre>
<p>再看下时间戳的转换处理：</p>
<pre><code class="dart language-dart">class TimeUtils {
  //获取格式化后的播放进度
  static String getCurrentPosition(int seconds) {
    String hours = '00';
    int timeHours = (seconds / (60 * 60)).toInt();
    int timeMinutes = (seconds / 60).toInt() - (timeHours * 60);
    int timeSeconds = seconds - (timeHours * 60 * 60) - (timeMinutes * 60);

    if (timeHours &gt; 9) {
      hours = '$timeHours';
    } else if (timeHours &gt; 0 &amp;&amp; timeHours &lt; 10) {
      hours = '0${timeHours}';
    } else {
      hours = '00';
    }
    String minutes = '00';
    if (timeMinutes &gt; 9) {
      minutes = '${timeMinutes}';
    } else if (timeMinutes &gt; 0 &amp;&amp; timeMinutes &lt; 10) {
      minutes = '0${timeMinutes}';
    } else {
      minutes = '00';
    }
    String second = '00';
    if (timeSeconds &gt; 9) {
      second = '${timeSeconds}';
    } else if (timeSeconds &gt; 0 &amp;&amp; timeSeconds &lt; 10) {
      second = '0${timeSeconds}';
    } else {
      second = '00';
    }
    return '${hours}:${minutes}:${second}';
  }

  //进度条百分比
  static double getProgress(int seconds, int duration) {
    return seconds / duration;
  }
}
</code></pre>
<p>关于进度条拖动快进这块例子里没有给具体实现，默认的 LinearProgressIndicator 不支持拖动，所以我们可以自定义包装一个 LinearProgressIndicator 或者搜索一下插件库里的 seekbar 来实现，很简单，大家可以自行实现。屏幕滑动控制音量、亮度、进度这块也不难，例子里已经大概写了原理和操作，音量这块还要操作手机系统音量才可以，所以需要写一个插件或者 pub.dev 里已有这样的控制手机音量的也可以使用。</p>
<h3 id="flutter-2">Flutter 音频播放器的实现</h3>
<p>音频播放器部分我们使用第三方插件库 AudioPlayers：</p>
<p><a href="https://pub.dev/packages/audioplayers">https://pub.dev/packages/audioplayers</a> </p>
<p>这个插件库也是调用的原生播放，只不过封装了一层 API。我们也可以自己写插件，基于原生的一些播放器 API 进行封装。这里暂时以这个音频插件库为例进行讲解。
这个 audioplayers 插件对应的原生调用分别是：</p>
<ul>
<li>Android 平台：MediaPlayer</li>
<li>iOS 平台：AVAudioPlayer</li>
</ul>
<p>接下来我们看下我们实现的效果图：</p>
<p><img src="https://images.gitbook.cn/7584bde0-baa3-11e9-8bd3-43e1fddff917" alt="音频播放器的效果图" /></p>
<p>静态效果图：</p>
<p><img src="https://images.gitbook.cn/862fdcb0-baa3-11e9-8bd3-43e1fddff917" alt="音频播放器的效果图" /></p>
<p><strong>音频播放器实现了：播放、暂停、停止销毁、进度时时显示、播放时长和总时长的格式化显示，状态监听、支持播放网络音频文件、本地音频文件、资源目录音频文件。</strong></p>
<p>接下来我们就进行编写 Flutter 的音频播放器。</p>
<p>引入 audioplayers 插件库：</p>
<pre><code class="dart language-dart">dependencies:
  audioplayers: ^0.13.1
</code></pre>
<p>使用的地方进行导包：</p>
<pre><code class="dart language-dart">import 'package:audioplayers/audioplayers.dart';
</code></pre>
<p>整个音频的播放通过 AudioPlayer 进行控制，所以我们需要先实例化 AudioPlayer。</p>
<p>支持本地文件、资源文件、网络音频流的播放。</p>
<p>先大概看下 audioplayers 的几个主要的方法：</p>
<pre><code class="dart language-dart">//播放网络音频
 play(String url) async {
    int result = await audioPlayer.play(url);
    if (result == 1) {
      // success
    } else {}
  }
//播放本地音频
  playLocal(String localPath) async {
    int result = await audioPlayer.play(localPath, isLocal: true);
    if (result == 1) {
      // success
    } else {}
  }
//播放assets音频
AudioCache player = AudioCache(fixedPlayer: audioPlayer);
player.play('audios/gbqq.mp3').then((AudioPlayer assetsAudioPlayer) {});
//设置音频音量（0-1）
audioPlayer.setVolume(1);
//播放视频
audioPlayer.resume();
//暂停播放
audioPlayer.pause();
//移除监听
_controller.removeListener(listener);
//销毁播放器
audioPlayer.release();
audioPlayer.dispose();
//指定播放位置
 int result = await audioPlayer.seek(Duration(milliseconds: 1200));
// 停止播放
 int result = await audioPlayer.stop();
</code></pre>
<p>接下来看下具体实现：</p>
<pre><code class="dart language-dart">//播放页很简单，就是调用了播放器的我们自己封装的Widget

import 'package:audioplayers/audio_cache.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter_video_audio/utils/utils.dart';

class AudioWidget extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return AudioWidgetState();
  }
}

class AudioWidgetState extends State&lt;AudioWidget&gt; {
  // 用来播放assets目录的音频文件，拷贝后当成本地文件播放
  static AudioCache player;
  AudioPlayer audioPlayer = AudioPlayer();
  Duration _duration = Duration();
  Duration _currentDuration = Duration();
  IconData _icons = Icons.pause_circle_filled;

  var kUrl1 = 'https://luan.xyz/files/audio/ambient_c_motion.mp3';
  var kUrl2 = 'https://luan.xyz/files/audio/nasa_on_a_mission.mp3';
  var kUrl3 = 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1xtra_mf_p';
  bool playing = false;

  @override
  void initState() {
    super.initState();
    player = AudioCache(fixedPlayer: audioPlayer);
    //是否打印日志
    AudioPlayer.logEnabled = true;
    //设置地址，并不播放，调用player.resume开始播放
//    audioPlayer.setUrl(kUrl1, isLocal: false);

    // 播放本地音频
//    Future&lt;Directory&gt; _externalDocumentsDirectory =
//        getExternalStorageDirectory().then((Directory directory) {
//      print('${directory.path}/gbqq.mp3');
//      playLocal('${directory.path}/gbqq.mp3');
//    });

    // 播放assets目录音频
    player.play('audios/gbqq.mp3').then((AudioPlayer assetsAudioPlayer) {});

    //播放网络音频
//    play(kUrl1);

    //播放状态改变
    audioPlayer.onPlayerStateChanged.listen((AudioPlayerState playerState) {
      if (playerState == AudioPlayerState.COMPLETED) {
      } else if (playerState == AudioPlayerState.PAUSED) {
        setState(() {
          playing = false;
        });
      } else if (playerState == AudioPlayerState.PLAYING) {
        setState(() {
          playing = true;
        });
      } else if (playerState == AudioPlayerState.STOPPED) {}
    });
    //播放音频总时长
    audioPlayer.onDurationChanged.listen((Duration d) {
      print('Max duration: $d');
      setState(() {
        _duration = d;
      });
    });
    //播放进度变化
    audioPlayer.onAudioPositionChanged.listen((Duration d) {
      setState(() {
        _currentDuration = d;
      });
    });
    //播放完成
    audioPlayer.onPlayerCompletion.listen((event) {
      setState(() {});
    });
    // 播放出错
    audioPlayer.onPlayerError.listen((String error) {});
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.bottomCenter,
      child: Column(
        children: &lt;Widget&gt;[
          Row(
            children: &lt;Widget&gt;[
              SizedBox(
                width: 10,
              ),
              Text(
                TimeUtils.getCurrentPosition(_currentDuration.inSeconds),
                style: TextStyle(
                  color: Color.fromRGBO(104, 112, 161, 1),
                ),
              ),
              SizedBox(
                width: 10,
              ),
              // 进度条
              Expanded(
                  child: LinearProgressIndicator(
                value: TimeUtils.getProgress(
                    _currentDuration.inSeconds, _duration.inSeconds),
                valueColor: AlwaysStoppedAnimation&lt;Color&gt;(
                    Color.fromRGBO(115, 137, 186, 1)),
                backgroundColor: Color.fromRGBO(211, 211, 221, 1),
              )),
              SizedBox(
                width: 10,
              ),
              Text(
                TimeUtils.getCurrentPosition(_duration.inSeconds),
                style: TextStyle(
                  color: Color.fromRGBO(104, 112, 161, 1),
                ),
              ),
              SizedBox(
                width: 10,
              ),
            ],
          ),
          SizedBox(
            height: 10,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: &lt;Widget&gt;[
              IconButton(
                iconSize: 40,
                icon: Icon(
                  Icons.skip_previous,
                  color: Color.fromRGBO(111, 135, 199, 1),
                  size: 40,
                ),
                onPressed: () {},
              ),
              IconButton(
                iconSize: 60,
                alignment: Alignment.center,
                icon: Icon(
                  _icons,
                  color: Color.fromRGBO(111, 135, 199, 1),
                  size: 60,
                ),
                onPressed: () {
                  playOrPause();
                },
              ),
              IconButton(
                iconSize: 40,
                icon: Icon(
                  Icons.skip_next,
                  color: Color.fromRGBO(111, 135, 199, 1),
                  size: 40,
                ),
                onPressed: () {},
              ),
            ],
          ),
          SizedBox(
            height: 30,
          ),
        ],
      ),
    );
  }

  play(String url) async {
    int result = await audioPlayer.play(url);
    print('播放状态：$result');
    if (result == 1) {
      // success
    } else {}
  }

  playLocal(String localPath) async {
    int result = await audioPlayer.play(localPath, isLocal: true);
    print('播放状态：$result');
    if (result == 1) {
      // success
    } else {}
  }

  playOrPause() {
    if (audioPlayer.state == AudioPlayerState.PLAYING) {
      setState(() {
        _icons = Icons.play_circle_filled;
        audioPlayer.pause();
      });
    } else {
      setState(() {
        _icons = Icons.pause_circle_filled;
        audioPlayer.resume();
      });
    }
    playing = !playing;
  }

  @override
  void dispose() {
    super.dispose();
    player.clear('audios/gbqq.mp3');
    player.fixedPlayer.stop();
    player.fixedPlayer.release();
    player.fixedPlayer.dispose();
    audioPlayer.stop();
    audioPlayer.release();
    audioPlayer.dispose();
  }
}
</code></pre>
<p>assets目录的音频需要注册：</p>
<pre><code class="dart language-dart">flutter:

  uses-material-design: true

  assets:
    - assets/audios/gbqq.mp3
</code></pre>
<p>本节课的项目完整代码：</p>
<p><a href="https://github.com/jaychou2012/flutter_video_audio">video_audio</a></p>
<h3 id="">总结</h3>
<p>本节课主要是进行了一个实现音视频播放器的扩展实践，通过真实案例来巩固和检查之前所学到的这些内容，这节课内容非常典型，所以大家可以认真学习里面的技术方案。</p></div></article>