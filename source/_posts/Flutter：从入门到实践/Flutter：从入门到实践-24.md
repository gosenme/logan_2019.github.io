---
title: Flutter：从入门到实践-24
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在实际开发中，经常离不开文件和图片的读写操作，例如缓存数据、创建删除文件/文件夹、读取文本/图片/音视频等数据、读取显示图片等等。Flutter 也提供了相关的操作 API。那么这节课我们就开始学习 Flutter 中与文件和图片读写操作相关的内容，并结合案例进行用法讲解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Flutter 文件操作</li>
  <li>Flutter 图片操作</li>
  </ul>
</blockquote>
<h3 id="flutter">Flutter 文件操作</h3>
<p>常见的文件操作有：创建文件/文件夹、删除文件/文件夹、判断文件/文件夹是否存在、列出目录文件列表、文件读取写入、获取文件/文件夹信息等。Flutter 也可以实现这些常用功能，使用的API 主要就是 File 和 Directory。</p>
<p>实现文件操作我们可以通过使用 Flutter 原生 API、Flutter 第三方插件库、自己编写插件库这三种方式来实现。我们这里主要给大家讲解如何通过 Flutter 原生 API 和 Flutter 第三方插件库来实现文件操作。</p>
<p>首先我们看下使用 Flutter 原生 API 实现：</p>
<pre><code class="dart language-dart">// 我们的File和Directory操作都在dart:io包里
import 'dart:io';

/// 创建文件夹
Future directory1() async {
  var directory = Directory("temp1");
  directory.create();
}

/// 递归创建文件夹
void directory2() {
  Directory('dir/subdir').create(recursive: true).then((Directory directory) {
    print(directory.path);
  });
}

///列出目录文件列表
void directory3() {
  var systemTempDir = Directory('sdcard');
  systemTempDir
      .list(recursive: true, followLinks: false)
      .listen((FileSystemEntity entity) {
    print(entity.path);
  });
}

///判断文件夹是否存在
void directory4() {
  var directory = Directory('dir/subdir');
  directory.exists().then((isThere) {
    print(isThere);
  });
}

///文件夹重命名
void directory5() {
  var directory = Directory('dir/subdir');
  directory.rename('dir/subRightDir').then((Directory directory) {});
}

///判断文件是否存在
void file1() {
  var file = File('E:/file.txt');
  file.exists().then((isThere) {
    print(isThere);
  });
}

///创建文件
void file2() {
  var file = File('E:/file2.txt');
  file.create().then((file) {
    print(file);
  });
}

///最强大的读取文件的方式，Stream方式
void file3() {
  var file = File('E:/file.txt');
  Stream&lt;List&lt;int&gt;&gt; inputStream = file.openRead();
  inputStream
      .transform(utf8.decoder)
      .transform(LineSplitter())
      .listen((string) {
    print(string);
  }).onDone(() {
    print('File is now closed.');
  });
}

///文件写入内容
void file4() {
  var file = File('E:/file2.txt');
  file.writeAsString('some content').then((file) {
    print(file);
  });
}

///文件写入内容
void file5() {
  var file = File('E:/file2.txt');
  var sink = file.openWrite();
  sink.write('FILE ACCESSED ${new DateTime.now()}\n');
  sink.close();
}

///获取文件长度等信息
void file6() {
  var file = File('E:/file.txt');
  file.length().then((len) {
    print(len);
  });
}

/// 如果我们需要访问SDCARD目录或内容可以写好路径
/// 不过我们也可以通过第三方插件库来实现
void sdcard() {
  var sdcardDir = Directory('sdcard');
  var sdcardFile=File('sdcard/file.txt');
}
</code></pre>
<p>怎么样，是不是非常简单？跟其他平台的使用方式很像。</p>
<p>接下来我们再看下通过第三方插件库实现文件操作。</p>
<p>Flutter 官方给我们提供了一个文件操作插件库：path_provider。</p>
<p>首先需要在 pubspec.yaml 文件里添加引用：</p>
<pre><code class="dart language-dart">dependencies:
  path_provider: ^1.1.0
</code></pre>
<p>接下来在使用的地方导入包：</p>
<pre><code class="dart language-dart">import 'package:path_provider/path_provider.dart';
</code></pre>
<p>使用方法：</p>
<pre><code class="dart language-dart">// 相当于Android上的getCacheDir和IOS上的NSCachesDirectory
void getCacheDir() {
  Future&lt;Directory&gt; tempDir = getTemporaryDirectory();
  tempDir.then((Directory directory) {
    print(directory.path);
  });
}

// 相当于Android上的getDataDirectory和IOS上的NSDocumentDirectory
void getAppDocDir() {
  Future&lt;Directory&gt; appDocDir = getApplicationDocumentsDirectory();
  appDocDir.then((Directory directory) {
    print(directory.path);
  });
}

// 相当于Android上的getExternalStorageDirectory
void getAppExternalDir() {
  Future&lt;Directory&gt; appExternalDir = getExternalStorageDirectory();
  appExternalDir.then((Directory directory) {
    print(directory.path);
  });
}}
</code></pre>
<h3 id="flutter-1">Flutter 图片操作</h3>
<p>接下来我们看下 Flutter 的图片相关操作。前面已经给大家讲解过 Flutter 的 Image 组件的基本用法，也涉及了很多图片加载和显示相关的知识点和操作。</p>
<p>Flutter 图片的加载一般主要是 网络加载、本地加载、资源文件里加载 这几种。</p>
<p>加载网络图片：</p>
<pre><code class="dart language-dart">// 返回了一个Image Widget
Image.network(imageUrl)

// 也可以通过NetworkImage来加载，需要Image Widget包裹
// NetworkImage返回的是一个ImageProvider
Image(
  image: NetworkImage(imageUrl),
)

// 也可以在加载网络图片时放置一个加载出来前的占位图
FadeInImage.assetNetwork(
  placeholder: "assets/flutter-mark-square-64.png",
  image: imageUrl,
)
</code></pre>
<p>加载本地图片：</p>
<pre><code class="dart language-dart">// 也就是从硬盘、SDCARD里加载读取的图片

Image.file(
  File('/sdcard/img.png'),
  width: 200,
  height: 80,
)

Image(
  image: FileImage(File('/sdcard/img.png')),
)

// 也可以从内存缓存中读取byte数组图片
Image.memory(bytes)

Image(
  image: MemoryImage(bytes),
)
</code></pre>
<p>加载项目资源文件里图片：</p>
<pre><code class="dart language-dart">// 从项目目录里读取图片，需要在pubspec.yaml注册路径

assets:
    - assets/flutter-mark-square-64.png
...

// assets这个目录是位于项目的根目录
Image.asset("assets/flutter-mark-square-64.png"),

Image(
  image: AssetImage("assets/flutter-mark-square-64.png"),
)
</code></pre>
<p>那么如果我想实现类似 Android 里的图片资源适配加载，按照不同屏幕密度来加载不同大小的图片怎么做？</p>
<p>类似的，我们在资源文件的文件夹命名时加入标识即可：</p>
<p>…/image.png
…/2.0x/image.png
…/3.0x/image.png</p>
<p>默认不带标识的为适配像素比率为 1.0 的设备，2.0x 为适配像素比率接近 2.0 的设备，其他的同理。</p>
<p>如果我们使用了依赖插件库里的图片资源的话，那么一定要加上 packages 包名这个标识才可以找到。例如：</p>
<pre><code class="dart language-dart">AssetImage('icons/logo.png', package: 'lib_icons')
</code></pre>
<p>大家看，Flutter 的图片加载处理也很简单对不对。当然我们也可以通过 Image 组件来对加载的图片做一些个性化设置，如：尺寸大小、填充模式、颜色混合模式、重复规则等等。大家可以自己结合之前的 Image Widget 课程进行巩固复习。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的文件读写操作和图片相关的用法，内容很简单。可以：</p>
<ul>
<li>重点掌握文件读写的用法，包括一些路径、信息的获取；</li>
<li>图片的加载可以结合 Image 组件来进行实践操作一下。</li>
</ul></div></article>