---
title: Flutter：从入门到实践-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在实际开发中，经常使用到数据交换格式，如：JSON 或 XML。Flutter 里也同样可以处理 JSON 格式的解析、编码操作，我们可以实现将一个 JSON 字符串转为实体类或将一个实体对象转为JSON 格式字符串。本节课主要讲解 Flutter 里的 JSON 编解码的具体用法，并结合案例进行详细的用法讲解。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>JSON 编解码用法详解</li>
  <li>JSON 编解码优化</li>
  <li>JSON 自动序列化解码</li>
  </ul>
</blockquote>
<h3 id="1json">1 JSON 编解码用法详解</h3>
<p>当我们去请求网络数据接口或者缓存某些结构数据时，一般都会用到 JSON 数据交换格式。JSON在移动端、后端、前端中应用都非常广泛。在 Flutter 中 JSON 格式的解析使用 dart:convert 里的函数类进行编解码处理。</p>
<p>我们看一个最简单的编解码使用的例子：</p>
<pre><code class="dart language-dart">// JSON解码
// 定义一个JSON格式字符串
String _jsonString = '{"name": "Flutter Book","author": "Google"}';

// 使用json.decode进行解码
Map&lt;String, dynamic&gt; book = json.decode(_jsonString);

// 解码后调用获取值
Column(
    children: &lt;Widget&gt;[
        Text('Book Name：${book['name']}'),
        Text('Book Author：${book['author']}'),
    ],
));

// 再看下JSON编码
// 使用json.encode将实体对象编码为JSON字符串
String _bookJson = json.encode(book);
</code></pre>
<p>怎么样，用起来是不是很简单，这些只是最简单的例子。实际开发中可能会遇到更加庞大、复杂嵌套的 JSON 结构。</p>
<pre><code class="dart language-dart">// 如果是一个List集合的JSON字符串的话
String _jsonListString =
      '[{"name": "Flutter Book","author": "Google"},{"name": "Dart Book","author": "Google"}]';

// 解码成List
List books = json.decode(_jsonListString);

// 调用取值
print(books[0]["name"]);
</code></pre>
<h3 id="2json">2 JSON 编解码优化</h3>
<p>接下来我们优化一下我们的 JSON 编解码，让我们在使用的时候更加高效和方便。</p>
<p>我们首先定义一个实体类。 </p>
<p>Book：</p>
<pre><code class="dart language-dart">class Book {
  final String name;
  final String author;

  Book(this.name, this.author);

  Book.fromJson(Map&lt;String, dynamic&gt; json)
      : name = json['name'],
        author = json['author'];

  Map&lt;String, dynamic&gt; toJson() =&gt; {
        'name': name,
        'author': author,
      };
}
</code></pre>
<p>可以看到，实体类里新增了两个方法：fromJson 和 toJson。分别用于将 JSON 字符串解码为实体对象和将实体对象转为 JSON 字符串格式。</p>
<p>我们可以这样使用：</p>
<pre><code class="dart language-dart">// 解析JSON字符串
Map&lt;String, dynamic&gt; bookMap = json.decode(_jsonString);

// 调用Book里的fromJson方法转换创建实体Book
var bookBean = Book.fromJson(bookMap);

// 使用
print(bookBean.name);
print(bookBean.author);

// 编码JSON字符串
// 可以直接调用，推荐
String beanString = json.encode(bookBean);

// 或者调用实体类里的toJson方法即可，没必要，麻烦
String beanString = json.encode(bookBean.toJson());
</code></pre>
<p>这种写法扩展性更强、更高效、更安全。</p>
<h3 id="3json">3 JSON 自动序列化解码</h3>
<p>在实际开发中，我们的实体对象可能属性很多，并且内部嵌套对象或 List 集合。那么类似这种更加复杂的对象，如果我们依然这样一个一个写方法、属性赋值、解析的话那将会非常耗费时间。在 Android 平台有 GsonFomat、Gson 这样的工具和库帮我们处理，在 Flutter 平台同样也有，Flutter 官方提供了一个插件库：json_serializable。</p>
<p>json_serializable 可以方便的帮助我们进行 JSON 自动序列化解码处理，免去很多重复的工作，也会避免出错。</p>
<p>插件库官方地址：</p>
<p><a href="https://pub.dev/packages/json_serializable">https://pub.dev/packages/json_serializable</a></p>
<p>接下来我们看下这个插件的简单用法.</p>
<p>首先我们需要在 pubspec.yaml 里添加依赖：</p>
<pre><code class="dart language-dart">dependencies:
  json_serializable: ^2.3.0
</code></pre>
<p>运行 flutter packages get 命令，或者在 Visual Studio 里更改了配置文件保存后就会自动同步相关资源。</p>
<p>这里建议 flutter sdk 使用最新的 1.5 版本（升级命令：flutter upgrade —force）。</p>
<p>之后，在使用的地方导包即可：</p>
<pre><code class="dart language-dart">import 'package:json_serializable/json_serializable.dart';
</code></pre>
<p>接下来我们看下简单的用法：</p>
<pre><code class="dart language-dart">// 我们新建一个实体类
import 'package:json_annotation/json_annotation.dart';

// book.g.dart 这个是配置自动生成的对应类的名字
part 'book.g.dart';

// JSON序列化注解
@JsonSerializable(nullable: false)

class Book{
  Book(this.name, this.author);

  String name;
  String author;

  factory Book.fromJson(Map&lt;String, dynamic&gt; json) =&gt; _$BookFromJson(json);
  Map&lt;String, dynamic&gt; toJson() =&gt; _$BookToJson(this);
}

// 接下来配置自动生成命令
flutter packages pub run build_runner build

// 或者使用下面命令，每次新增修改实体类后都会自动监听生成

flutter packages pub run build_runner watch

// 执行完命令后，就会在同目录文件夹生成对应实体类

// book.g.dart

// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'book.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Book _$BookFromJson(Map&lt;String, dynamic&gt; json) {
  return Book(json['name'] as String, json['author'] as String);
}

Map&lt;String, dynamic&gt; _$BookToJson(Book instance) =&gt;
    &lt;String, dynamic&gt;{'name': instance.name, 'author': instance.author};

// 会自动帮助我们去补充完成属性的映射工作
</code></pre>
<p>那么我们的 Book 这个类实际上就变成了 book.dart 和 book.g.dart 两部分组成的了。如果放在一起是这样的：</p>
<pre><code class="dart language-dart">class Book{
  Book(this.name, this.author);

  String name;
  String author;

  Book _$BookFromJson(Map&lt;String, dynamic&gt; json) {
    return Book(json['name'] as String, json['author'] as String);
  }

  Map&lt;String, dynamic&gt; _$BookToJson(Book instance) =&gt;
      &lt;String, dynamic&gt;{'name': instance.name, 'author': instance.author};
  }
</code></pre>
<p>接下来看下使用，使用方式和前面没有区别：</p>
<pre><code class="dart language-dart">// JSON字符串
String _jsonString = '{"name": "Flutter Book","author": "Google"}';

// 解码成实体类
Map&lt;String, dynamic&gt; bookMap = json.decode(_jsonString);
var bookBean = Book.fromJson(bookMap);

// 调用
print(bookBean.name);
print(bookBean.author);

// 将实体对象编码为JSON字符串
String beanString = json.encode(bookBean);
</code></pre>
<p>本节课实例地址</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_20">flutter_20</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的 JSON 编解码的用法，内容很简单。</p>
<ul>
<li>重点掌握：JSON 自动生成序列化的用法。</li>
<li>理解 json_serializable 为我们所做的工作。</li>
</ul></div></article>