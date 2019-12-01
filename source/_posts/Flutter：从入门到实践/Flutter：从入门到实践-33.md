---
title: Flutter：从入门到实践-33
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在使用 Flutter 开发时，可能某些功能的实现比较麻烦或者无法实现，这时我们首先应该想到的就是要搜索 Dart Pub：<a href="https://pub.dev/flutter">https://pub.dev/flutter</a>。</p>
<p>这是 Flutter 官方的一个针对 Flutter、Web、Dart 的插件库开源仓库，里面有很多官方和其他开发者开源的插件库。那么这节课我们将介绍 Flutter 中 Dart Pub 的使用，以及我们自己实现开发一款 Flutter 插件库的方法</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Dart Pub 使用</li>
  <li>Flutter 插件库 Flutter Package 的开发</li>
  <li>Flutter 插件库 Flutter Plugin 的开发</li>
  </ul>
</blockquote>
<h3 id="1dartpub">1 Dart Pub 使用</h3>
<p><img src="https://images.gitbook.cn/FvQ8nJBGs-j49ygYiZcBLE7EoorI" alt="Dart Pub" /></p>
<p>Dart Pub 里的 Flutter 插件库都是兼容 Android 和 iOS 的，当然 Dart Pub 里的插件库还有很多是 Web 相关的插件，我们只需要搜索 Flutter 的插件库使用即可。</p>
<p>我们看下 Flutter 相关的使用频率比较高的插件库：</p>
<p>我们这里以 path_provider 这个插件库为例，点击 path_provider 这个链接进入插件库详情描述页。path_provider 是用于为 Flutter 提供访问 Android 和 iOS 的文件系统目录的功能的一个插件库。</p>
<p>点击进入的页面如下：</p>
<p><img src="https://images.gitbook.cn/FhngGx9IVAagrMFfdKnojAprTHjx" alt="Dart Pub" /></p>
<p>有说明文档、更新日志、例子、安装步骤、版本列表、关于页面、插件官方首页、Github 地址、相关问题页面、API 文档等等信息。</p>
<p>我们需要点击 Installing，复制安装依赖库的信息到 pubspec.yaml：</p>
<pre><code class="dart language-dart">dependencies:
  path_provider: ^1.1.2
</code></pre>
<p>接下来我们可以在 Readme 或者 Example 里看到使用的方法和说明，如果没有的话，可以点击进入官方的 Github 进行下载和查看使用的实例。</p>
<h3 id="2flutterflutterpackage">2 Flutter 插件库 Flutter Package 的开发</h3>
<p>我们除了可以使用 Dart Pub 上提供的插件库以外，如果遇到 Dart Pub 上的插件库也没有办法实现我们想要的功能的时候，我们可以自己编写插件库，需要兼容 Android 和 iOS 平台，也就是要分别写 Android 和 iOS 原生代码，并提供给 Flutter 进行调用。当然，我们也可以将我们的插件库提交到 Dart Pub 上供其他人使用。</p>
<p>那么接下来我们就来看看如何编写 Flutter 插件库，并提交到 Dart Pub 上。</p>
<p>Flutter 的 Dart Pub 上的插件库主要分为两种：<strong>一种是包（Flutter Package）：纯 Dart 编写的 API 插件库；另一种就是插件（Flutter Plugin）：编写 Android、iOS 的原生代码，然后通过 Flutter 的 MethodChannel 来调用封装好的对应平台的原生代码来实现的插件库。</strong></p>
<p>这两种插件库各有各的特点和功能，我们的 Android Studio 在创建项目时，也提供了插件库创建的两种方式：</p>
<p><img src="https://images.gitbook.cn/FmDtMLh3_OU_S90Ys9lrS1O4YyoW" alt="Flutter创建插件库" /></p>
<p>我们可以看到有 Flutter Plugin 和 Flutter Package 两种方式来创建插件库。相应地，如果我们的插件库通过纯 Dart 就可以实现这个插件功能的话，就选择 Flutter Package 方式创建插件库；如果我们的插件库必须借助 Android、iOS 平台的原生代码才可以实现插件功能的话，那么就选择 Flutter Plugin 方式创建我们的插件库。</p>
<p>我们先看下 Flutter Package 这种方式创建插件库。</p>
<p>除了可以用 Android Studio 进行界面操作创建外，我们还可以通过命令行方式创建：</p>
<pre><code class="dart language-dart">$ flutter create --template=package hello
</code></pre>
<p>这里的 <code>hello</code> 为插件 Package 名称，英文名称。</p>
<p>我们看下创建后的项目结构：</p>
<p><img src="https://images.gitbook.cn/FhXxeVW5HSBHd1thbXKImYvjK3_I" alt="Flutter创建插件库" /></p>
<p>插件的逻辑写在 lib 目录下，纯 Dart 实现的功能逻辑。</p>
<p>test 目录下面是单元测试文件。</p>
<p>CHANGELOG.md 这个文件是用于描述插件更新的日志的。提交到 Dart Pub 上就是 CHANGELOG 这里显示的内容。</p>
<p>LICENSE 是添加我们的开源插件库所遵循的开源协议是哪些，及其描述。</p>
<p>pubspec.yaml 这里面是我们插件库的描述信息，如插件库名称信息、作者信息、版本信息等其他信息。</p>
<p>我们大致看下 pubspec.yaml 的内容：</p>
<pre><code class="dart language-dart">// 插件库名称
name: flutter_package
// 插件库描述
description: A new Flutter package.
// 插件库版本
version: 0.0.1
// 作者信息，名字 &lt;邮箱&gt;形式
author: Tan Dong &lt;tandongjay@qq.com&gt;
// 插件库的主页
homepage: https://github.con/tandong/flutter_package
// 插件库运行的sdk版本环境
environment:
  sdk: "&gt;=2.1.0 &lt;3.0.0"
// 所需要的依赖
dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter

# For information on the generic Dart part of this file, see the
# following page: https://dart.dev/tools/pub/pubspec
</code></pre>
<p>README.md 是插件库的说明文档，包含插件库的功能描述、特点、用法示例等等说明描述性的信息。</p>
<p>当我们的项目具备这些文件和目录结构后，并且在 lib 目录下编写完 dart 功能代码后，我们就可以自己使用了，如果想共享给其他人，就可以发布到 Dart Pub 上。</p>
<p>fluro 这个插件库就是一个 Flutter Package 实现的插件库：<a href="https://pub.dev/packages/fluro">https://pub.dev/packages/fluro</a> ，大家可以参考学习下它的结构。</p>
<p>例如，假如我们的插件库名叫做：flutter_package，那么我们默认就会在 lib 目录下新建一个 flutter_package.dart 文件，建议 lib 根目录的文件名为插件库英文名字命名。</p>
<p>入口文件示例：</p>
<pre><code class="dart language-dart">library flutter_package;

/// A Calculator.
class Calculator {
  /// Returns [value] plus 1.
  int addOne(int value) =&gt; value + 1;
}
</code></pre>
<p>顶部：library + 插件库名字声明。</p>
<p>下面就可以编写相关的 class 和方法类逻辑了。</p>
<p><strong>发布到 Dart Pub</strong></p>
<p>如果我们的项目结构都完整，包含了 lib、pubspec.yaml、README.md 以及 CHANGELOG.md 等文件，我们就可以发布到 Dart Pub 了。</p>
<p>运行如下命令，检查是否一切就绪并且正确：</p>
<pre><code class="dart language-dart">$ flutter packages pub publish --dry-run
</code></pre>
<p>如果检查通过的话，输入如下命令即可发布：</p>
<pre><code class="dart language-dart">$ flutter packages pub publish
</code></pre>
<p><img src="https://images.gitbook.cn/FulCLp9K7HOiifg2QAZsMh1VJcgc" alt="Flutter检查插件库" /></p>
<p>这样就完成了我们 Flutter Package 的发布。</p>
<p><strong>依赖冲突的解决</strong></p>
<p>如果遇到插件库的依赖库引用冲突，如版本不一致，插件库使用了一个版本的依赖库、项目中又引入了另一个版本的插件库，这时可能会产生冲突。</p>
<p>Flutter 官方建议我们的插件库所用的依赖库版本声明中，要声明使用范围，而不是指定某个固定版本号。</p>
<p>例如我们的 flutter_package 插件库的 pubspec.yaml 中声明了依赖：</p>
<pre><code class="dart language-dart">dependencies:
  url_launcher: ^0.4.2
</code></pre>
<p>这样使用范围的声明是推荐的，而不是指定固定一个版本的 url_launcher。</p>
<p>还有一种方式解决冲突：</p>
<pre><code class="dart language-dart">dependencies:
  some_package:
  other_package:
dependency_overrides:
  url_launcher: '0.4.3'
</code></pre>
<p>就是强制使用 <code>dependency_overrides</code> 来指定统一 url_launcher 依赖库的版本。</p>
<h3 id="3flutterflutterplugin">3 Flutter 插件库 Flutter Plugin 的开发</h3>
<p>接下来我们看下有了原生代码逻辑的 Flutter Plugin 的插件库的开发。若我们的插件库使用纯Dart 无法实现的话，那么就要通过编写各个平台的原生代码来实现交互调用了。这种方式就是 Flutter Plugin 方式的实现。</p>
<p>这次创建插件库项目我们选择 Flutter Plugin 来创建：</p>
<p><img src="https://images.gitbook.cn/Fl4f2_hXeXsfuGzoOntzwSU_2VSk" alt="Flutter创建插件库" /></p>
<p>也可以使用命令创建：</p>
<pre><code class="dart language-dart">$ flutter create --org com.example --template=plugin hello
</code></pre>
<p>这里建议使用 Android Studio 进行创建。</p>
<p><img src="https://images.gitbook.cn/FnaO35DPXAM5tRZO4xwe1IjXDaQx" alt="Flutter创建插件库" /></p>
<p>语言这里我们可以选择使用 Kotin 或者 Swift。默认是 Java 和 Object-C。</p>
<p>当然我们也可以在命令行中指定开发语言：</p>
<pre><code class="dart language-dart">$ flutter create --template=plugin -i swift -a kotlin hello
</code></pre>
<p>创建后的 Flutter Plugin 项目结构如下：</p>
<p><img src="https://images.gitbook.cn/FmD9Q4ADfIPbcApFlb6JL6YO30aG" alt="Flutter Plugin结构" /></p>
<p>可以看到：</p>
<ul>
<li>android 目录用于编写 Android 插件功能原生代码；</li>
<li>ios 目录用于编写 iOS 插件功能原生代码；</li>
<li>example 里是相关使用插件的例子；</li>
<li>lib 目录用于编写插件的 flutter 部分，用于调用原生封装好的方法；</li>
<li>test 是单元测试目录；</li>
<li>CHANGELOG.md 是插件库更新日志的描述文件；</li>
<li>LICENSE 是插件库所遵循的开源协议和说明；</li>
<li>pubspec.yaml 是插件库的一些配置描述信息，包括名称、描述、作者、主页、版本、运行环境等信息；</li>
<li>README.md 是插件库说明文档。</li>
</ul>
<p>主要的结构和文件就是这些，和 Flutter Package 大同小异。</p>
<p>具体的 Flutter 调用原生的代码逻辑和 Android 及 iOS 平台的代码编写逻辑，请看 <a href="https://gitbook.cn/m/mazi/columns/5cc01cc115a1a10d8cec9e86/topics/5cd571d4e30c87051ad414bb">第 3-2 课：Flutter 和原生的交互</a>  这一课时，其实就是通过 MethodChannel 方式进行交互、传值、调用。</p>
<p><img src="https://images.gitbook.cn/Flc55TCXv6ch8fu_snq1u3dmQV7K" alt="Flutter Plugin" /></p>
<p>Flutter 与原生交互：</p>
<p><img src="https://images.gitbook.cn/FjIFqUOdVD1gpCaJFwJDHmuqu_Ed" alt="Flutter Plugin" /></p>
<p>例如，Flutter 官方的例子实现获取手机电量信息的。其实就是编写了 Android 的方法、iOS 的方法，然后 Flutter 端编写 dart 代码来反射调用对应平台的获取电池电量的方法。</p>
<p>一个典型的 Flutter Plugin 插件例子就是 path_provider 这个官方插件库：</p>
<p><a href="https://pub.dev/packages/path_provider">https://pub.dev/packages/path_provider </a></p>
<p>它分别编写了 Android 和 iOS 的平台代码来获取文件路径，然后 Flutter 端调用封装好的方法。大家可以参考这个来学习：</p>
<p><a href="https://github.com/flutter/plugins/tree/master/packages/path_provider">https://github.com/flutter/plugins/tree/master/packages/path_provider </a>。</p>
<p>插件库的发布同上面的 Flutter Package 步骤一致。</p>
<p>关于 API documentation，即 API 文档，在发布软件包时，API 文档会自动生成并发布到 dartdocs.org。</p>
<p>文档的生成就是根据我们项目代码中的相关注释来生成的，所以我们只需要在每个类、方法、属性、块等地方按照 Dart 说明注释的规则来编写注释即可。</p>
<p>关于 Flutter 未上传发布的库的引入依赖，我们简单讲解下。</p>
<p>本地插件库引入形式：</p>
<pre><code class="dart language-dart">dependencies:
  plugin1:
    path: ../plugin1/
</code></pre>
<p>Github 上托管的插件库引入形式：</p>
<pre><code class="dart language-dart">dependencies:
  package1:
    git:
      url: git://github.com/flutter/packages.git
      path: packages/package2
</code></pre>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 插件库的实现的几种用法。建议大家去尝试编写 2 个插件库发布到 Dart Pub 上。</p></div></article>