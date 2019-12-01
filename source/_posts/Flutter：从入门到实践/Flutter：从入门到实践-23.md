---
title: Flutter：从入门到实践-23
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>WebSocket 在我们平时开发推送、聊天、数据传输时经常使用，无论是 Web 端还是移动端。那么这节课我们将介绍 Flutter 中 WebSocket 的基本使用：连接、发送消息、接收消息、断开连接。Flutter 自身 SDK 带 WebSocket 功能，或者通过第三方插件库也可以实现这些功能，这两种实现方式都非常简单，本节课会给大家讲解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>WebSocket 介绍</li>
  <li>WebSocket 简单用法</li>
  <li>第三方插件库实现 WebSocket</li>
  </ul>
</blockquote>
<h3 id="1websocket">1 WebSocket介绍</h3>
<p>在开始学习之前，先给大家简单介绍下 WebSocket。我们应该对 Socket 和TCP、UDP 协议都有所了解，它们都可以用来做长链接、数据通信。WebSocket 也是基于 TCP 实现的双向全双工通信协议，它可以实现客户端和服务器端数据双向传输交换。只需连接一次，便可以持久化连接通信。</p>
<p>这里我们可以对比 HTTP 来了解 WebSocket 的特性，我们知道 HTTP 是单向的请求/响应式协议，是无连接的协议，客户端发起请求，服务器端对请求做相应处理，这个过程是单向的。如果服务器端有数据或状态变化，无法及时告知客户端，所以很多的推送如果用 HTTP 来实现的话，都是进行轮询，这样不但效率低、容易出错，而且浪费资源，毕竟它是不停的发送 HTTP 请求给服务器端进行轮询。</p>
<p>那么 WebSocket 就解决了这个问题，它可以双向通信，并且是长连接、无需轮询，效率大大提升。</p>
<p>而使用 WebSocket 很简单，一般就如下几个步骤和功能：</p>
<ul>
<li>连接 WebSocket 服务器</li>
<li>发送消息</li>
<li>接收消息</li>
<li>关闭 WebSocket 连接</li>
</ul>
<p>那么接下来我们就学习下 Flutter 中 WebSocket 的基本用法。</p>
<h3 id="2websocket">2 WebSocket 简单用法</h3>
<p>Flutter SDK 中目前已经自带 WebSocket API。基本的使用步骤就是：连接 WebSocket 服务器、发送消息、接收消息、关闭 WebSocket 连接。</p>
<pre><code class="dart language-dart">// 导入websocket的包
import 'dart:io';
...
// 连接WebSocket服务器
Future&lt;WebSocket&gt; webSocketFuture =
        WebSocket.connect('ws://192.168.1.8:8080');

// WebSocket.connect返回的是 Future&lt;WebSocket&gt;对象
static WebSocket _webSocket;

webSocketFuture.then((WebSocket ws) {
      _webSocket = ws;

      void onData(dynamic content) {
        print('收到');
      }
      // 调用add方法发送消息
      _webSocket.add('message');
      // 监听接收消息，调用listen方法
     _webSocket.listen(onData, onDone: () {
        print('onDone');
      }, onError: () {
        print('onError');
      }, cancelOnError: true);

    });

... 

// 发送消息
_webSocket.add('发送消息内容');

...

// 监听接收消息，调用listen方法
void onData(dynamic content) {
        print('收到消息:'+content);
    }

_webSocket.listen(onData, onDone: () {
        print('onDone');
      }, onError: () {
        print('onError');
      }, cancelOnError: true);

...

// 关闭WebSocket连接
_webSocket.close();
</code></pre>
<p>基本用法就这些，怎么样，是不是很简单？</p>
<p>接下来我们看下通过第三方插件库进行 WebSocket 通信的基本用法。</p>
<h3 id="3websocket">3 第三方插件库实现 WebSocket</h3>
<p>第三方插件库我们选择官方的插件库：web<em>socket</em>channel。</p>
<p>基本使用步骤也都是：连接 WebSocket 服务器、发送消息、接收消息、关闭 WebSocket 连接。</p>
<p>插件库地址：<a href="https://pub.dev/packages/web_socket_channel">https://pub.dev/packages/web<em>socket</em>channel</a></p>
<p>首先安装。</p>
<p>在项目的 pubspec.yaml 里加入引用：</p>
<pre><code class="dart language-dart">dependencies:
  web_socket_channel: ^1.0.13
</code></pre>
<p>导入包：</p>
<pre><code class="dart language-dart">import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/status.dart' as status;
</code></pre>
<p>连接 WebSocket 服务器：</p>
<pre><code class="dart language-dart">var channel = IOWebSocketChannel.connect("ws://192.168.1.8:8080");
// 通过IOWebSocketChannel我们便可以进行各种操作
</code></pre>
<p>发送消息：</p>
<pre><code class="dart language-dart">channel.sink.add("connected!");
</code></pre>
<p>监听接收消息：</p>
<pre><code class="dart language-dart">channel.stream.listen((message) {
      print('收到消息:' + message);
    });
</code></pre>
<p>关闭 WebSocket 连接：</p>
<pre><code class="dart language-dart">channel.sink.close();
</code></pre>
<p>以上就是 Flutter 通过第三方插件库实现 WebSocket 通信功能的基本步骤。</p>
<p>当然 Flutter 也支持 Socket 相关 API 操作，大家可以自行学习。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的 WebSocket 的两种不同实现方式的用法，内容很简单。希望大家多多练习。</p>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>