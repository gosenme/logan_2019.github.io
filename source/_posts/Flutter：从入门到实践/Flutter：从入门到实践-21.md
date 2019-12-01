---
title: Flutter：从入门到实践-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>HTTP 网络请求是开发语言里比较常用和重要的功能，主要用于资源访问、接口数据请求和提交、上传下载文件等等操作，HTTP 请求方式主要有：GET、POST、HEAD、PUT、DELETE、TRACE、CONNECT、OPTIONS。本文主要讲 GET 和 POST 这两种常用请求在 Flutter 中的用法，其中对 POST 将进行着重讲解。Flutter 的 HTTP 网络请求的实现主要分为三种：io.dart 里的 HttpClient 实现、Dart 原生 HTTP 请求库实现、第三方库实现，后面将会给大家详细讲解这几种区别和特点及前两种的使用方法。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>简单介绍几种 HTTP 请求方式</li>
  <li>Flutter 三种 HTTP 网络请求实现的区别和特点</li>
  <li>HttpClient 实现 HTTP 网络请求</li>
  <li>Dart 原生 HTTP 请求库实现 HTTP 网络请求</li>
  <li>第三方库的推荐</li>
  </ul>
</blockquote>
<h3 id="1http">1 HTTP 的请求方式简介</h3>
<p>HTTP 网络请求方式就是描述了客户端想对指定的资源或服务器所要执行的操作。开头介绍过，HTTP 网络请求是一门开发语言里比较常用和重要的功能，主要用于资源访问、接口数据请求和提交、上传下载文件等等操作。其中主要的请求方式有：GET、POST、HEAD、PUT、DELETE、TRACE、CONNECT、OPTIONS 这八种。接下来先简单介绍它们的特点和作用。</p>
<p><strong>GET 请求方式</strong></p>
<p>从 GET 这个单词上也可以看出，它主要是执行获取资源操作的，例如通过 URL 从服务器获取返回的资源，其中 GET 可以把请求的一些参数信息拼接在 URL 上，传递给服务器，由服务器端进行参数信息解析，然后返回相应的资源给请求者。注意：GET 请求拼接的 URL 数据大小和长度是有最大限制的，传输的数据量一般限制在 2KB。</p>
<p><strong>POST 请求方式</strong></p>
<p>POST 主要是执行提交信息、传输信息的操作，POST 请求的可以携带很多的数据，而且格式不限。如 JSON、XML、文本等等都支持。并且 POST 传递的一些数据和参数不是直接拼接在 URL 后的，而是放在 HTTP 请求 Body 里，相对 GET 来说比较安全。并且传递的数据大小和格式是无限制的。POST 请求方式是比较重要和常用的一种，POST 请求包含两部分：请求头（header）和请求体（body）。POST 请求常见的请求体（body）有三种传输内容类型 Content-type：application/x-www-form-urlencoded、application/json、multipart/form-data，当然还有其他的几种，不过不常用，常用的就是这三种。</p>
<p><strong>HEAD 请求方式</strong></p>
<p>HEAD 主要是执行给请求的客户端返回头信息，而不返回 Body 主体内容。和 GET 方式类似，只不过 GET 方式有 Body 实体返回，而 HEAD 只返回头信息，无 Body 实体内容返回。主要是用于确认 URL 的有效性、资源更新的日期时间、查看服务器状态等等，对于有这方面需求的请求来说，比较不占用资源。</p>
<p><strong>PUT 请求方式</strong></p>
<p>PUT 主要是执行传输文件操作，类似于 FTP 的文件上传一样，请求里包含文件内容，并将此文件保存到 URI 指定的服务器位置。和 POST 方式的主要区别是：PUT 请求方式如果前后两个请求相同，则后一个请求会把前一个请求覆盖掉，实现了 PUT 方式的修改资源；而 POST 请求方式如果前后两个请求相同，则后一个请求不会把前一个请求覆盖掉，实现了 POST 的增加资源。</p>
<p><strong>DELETE 请求方式</strong></p>
<p>DELETE 主要是执行告诉服务器想要删除的资源，执行删除指定资源操作。</p>
<p><strong>OPTIONS 请求方式</strong></p>
<p>OPTIONS 主要是执行查询针对所要请求的 URI 资源服务器所支持的请求方式，也就是获取这个URI所支持客户端提交给服务器端的请求方式有哪些。</p>
<p><strong>TRACE 请求方式</strong></p>
<p>TRACE 主要是执行追踪传输路径的操作，例如，我们发起了一个 HTTP 请求，在这个过程中这个请求可能会经过很多个路径和过程，TRACE 就是告诉服务器在收到请求后，返回一条响应信息，将它收到的原始 HTTP 请求信息返回给客户端，这样就可以确认在 HTTP 传输过程中请求是否被修改过。</p>
<p><strong>CONNECT 请求方式</strong></p>
<p>CONNECT 主要就是执行连接代理操作，例如“翻墙”。客户端通过 CONNECT 方式与服务器建立通信隧道，进行 TCP 通信。主要通过 SSL 和 TLS 安全传输数据。CONNECT 的作用就是告诉服务器让它代替客户端去请求访问某个资源，然后再将数据返回给客户端，相当于一个媒介中转。</p>
<h3 id="2flutterhttp">2 Flutter HTTP 网络请求实现的区别和特点</h3>
<p>介绍完了 HTTP 几种请求方式，我们看下 Flutter 中的 HTTP 网络请求的实现方式。Flutter 的 HTTP 网络请求的实现主要分为三种：io.dart 里的 HttpClient 实现、Dart 原生 HTTP 请求库实现、第三方库实现。</p>
<p><strong>我们首先看下第一种：io.dart 里的 HttpClient 实现。</strong></p>
<p>io.dart 里的 HttpClient 实现的 HTTP 网络请求主要是实现基本的网络请求，复杂一些的网络请求还无法完成。例如 POST 里的其他几种 Body 请求体传输内容类型部分还无法支持，multipart/form-data 这个类型传输还不支持。所以如果你的一些 HTTP 网络请求可以通过io.dart 里的 HttpClient 实现的话，用这个也可以完成要求。</p>
<p>那么接下来我们就看下 io.dart 里的 HttpClient 实现的 HTTP 网络请求实现步骤。</p>
<pre><code class="dart language-dart">import 'dart:convert';
import 'dart:io';

class IOHTTPUtils {
  //创建HttpClient
  HttpClient _HttpClient = HttpClient();

  //要用async关键字异步请求
  getHttpClient() async {
    _HttpClient
        .get('HTTPs://abc.com', 8090, '/path1')
        .then((HttpClientRequest request) {
      //在这里可以对request请求添加headers操作，写入请求对象数据等等
      //调用close()方法
      return request.close();
    }).then((HttpClientResponse response) {
      // 处理response响应
      if (response.statusCode == 200) {
        response.transform(utf8.decoder).join().then((String string) {
          print(string);
        });
      } else {
        print("error");
      }
    });
  }

  getUrlHttpClient() async {
    var url = "HTTPs://abc.com:8090/path1";
    _HttpClient.getUrl(Uri.parse(url)).then((HttpClientRequest request) {
      // 在这里可以对request请求添加headers操作，写入请求对象数据等等
      // 调用close()方法
      return request.close();
    }).then((HttpClientResponse response) {
      // 处理响应数据
      if (response.statusCode == 200) {
        response.transform(utf8.decoder).join().then((String string) {
          print(string);
        });
      } else {
        print("error");
      }
    });
  }

  //进行POST请求
  postHttpClient() async {
    _HttpClient
        .post('HTTPs://abc.com', 8090, '/path2')
        .then((HttpClientRequest request) {
      //这里添加POST请求Body的ContentType和内容
      //这个是application/json数据类型的传输方式
      request.headers.contentType = ContentType("application", "json");
      request.write("{\"name\":\"value1\",\"pwd\":\"value2\"}");
      return request.close();
    }).then((HttpClientResponse response) {
      // 处理响应数据
      if (response.statusCode == 200) {
        response.transform(utf8.decoder).join().then((String string) {
          print(string);
        });
      } else {
        print("error");
      }
    });
  }

  postUrlHttpClient() async {
    var url = "HTTPs://abc.com:8090/path2";
    _HttpClient.postUrl(Uri.parse(url)).then((HttpClientRequest request) {
      //这里添加POST请求Body的ContentType和内容
      //这个是application/x-www-form-urlencoded数据类型的传输方式
      request.headers.contentType =
          ContentType("application", "x-www-form-urlencoded");
      request.write("name='value1'&amp;pwd='value2'");
      return request.close();
    }).then((HttpClientResponse response) {
      // 处理响应数据
      if (response.statusCode == 200) {
        response.transform(utf8.decoder).join().then((String string) {
          print(string);
        });
      } else {
        print("error");
      }
    });
  }

  ///其余的HEAD、PUT、DELETE请求用法类似，大同小异，大家可以自己试一下
  ///在Widget里请求成功数据后，使用setState来更新内容和状态即可
  ///setState(() {
  ///    ...
  ///  });

}
</code></pre>
<p><strong>第二种：Dart 原生 HTTP 请求库实现。</strong></p>
<p>这里推荐这种方式使用，毕竟 Dart 原生的 HTTP 请求库支持的 HTTP 请求比较全面，比较复杂的请求都可以实现，如上传和下载文件等等操作。</p>
<p>Dart 目前官方的仓库里有大量的三方库和官方库，引用也非常的方便，Dart PUB 官方地址为：
<a href="HTTPs://pub.dartlang.org">https://pub.dartlang.org</a>。</p>
<p>打开后如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fn5xGt02ZreNhZfmXT70rL78YWv6" alt="Dart PUB仓库" /></p>
<p>使用 Dart 原生 HTTP 库，我们首先需要在 Dart PUB 或官方 GitHub 里把相关的 HTTP 库引用下来。</p>
<p>在 Dart PUB 里搜索 HTTP，便可以查找到我们的 HTTP 库，根据说明进行引用和使用即可。</p>
<p>HTTP 库官方 GitHub 库地址为：
<a href="HTTPs://github.com/dart-lang/HTTP">https://github.com/dart-lang/HTTP</a>。</p>
<p><img src="https://images.gitbook.cn/FtT0Nzy0g7ibGI6cVZdxsm401o-O" alt="HTTP库" /></p>
<p>点击 Installing，查看引用方法进行引用即可。</p>
<p><img src="https://images.gitbook.cn/FoogjfB71oWtDwi3kDQrEKO1_wo_" alt="引用HTTP库" /></p>
<p>在项目的 pubspec.yaml 配置文件里加入引用：</p>
<p><img src="https://images.gitbook.cn/FruYAp2ERtdR8URRxJzUh-yq24-K" alt="加入引用HTTP库" /></p>
<p>完毕，这样就可以在 dart 文件类里直接 import 使用了。</p>
<p>接下来给一个完整的使用例子：</p>
<pre><code class="dart language-dart">import 'dart:convert';
import 'dart:io';

import 'package:HTTP/HTTP.dart' as HTTP;
import 'package:HTTP_parser/HTTP_parser.dart';

class DartHTTPUtils {
  //创建client实例
  var _client = HTTP.Client();

  //发送GET请求
  getClient() async {
    var url = "HTTPs://abc.com:8090/path1?name=abc&amp;pwd=123";
    _client.get(url).then((HTTP.Response response) {
      //处理响应信息
      if (response.statusCode == 200) {
        print(response.body);
      } else {
        print('error');
      }
    });
  }

//发送POST请求，application/x-www-form-urlencoded
  postUrlencodedClient() async {
    var url = "HTTPs://abc.com:8090/path2";
    //设置header
    Map&lt;String, String&gt; headersMap = new Map();
    headersMap["content-type"] = "application/x-www-form-urlencoded";
    //设置body参数
    Map&lt;String, String&gt; bodyParams = new Map();
    bodyParams["name"] = "value1";
    bodyParams["pwd"] = "value2";
    _client
        .post(url, headers: headersMap, body: bodyParams, encoding: Utf8Codec())
        .then((HTTP.Response response) {
      if (response.statusCode == 200) {
        print(response.body);
      } else {
        print('error');
      }
    }).catchError((error) {
      print('error');
    });
  }

  //发送POST请求，application/json
  postJsonClient() async {
    var url = "HTTPs://abc.com:8090/path3";
    Map&lt;String, String&gt; headersMap = new Map();
    headersMap["content-type"] = ContentType.json.toString();
    Map&lt;String, String&gt; bodyParams = new Map();
    bodyParams["name"] = "value1";
    bodyParams["pwd"] = "value2";
    _client
        .post(url,
            headers: headersMap,
            body: jsonEncode(bodyParams),
            encoding: Utf8Codec())
        .then((HTTP.Response response) {
      if (response.statusCode == 200) {
        print(response.body);
      } else {
        print('error');
      }
    }).catchError((error) {
      print('error');
    });
  }

  // 发送POST请求，multipart/form-data
  postFormDataClient() async {
    var url = "HTTPs://abc.com:8090/path4";
    var client = new HTTP.MultipartRequest("post", Uri.parse(url));
    client.fields["name"] = "value1";
    client.fields["pwd"] = "value2";
    client.send().then((HTTP.StreamedResponse response) {
      if (response.statusCode == 200) {
        response.stream.transform(utf8.decoder).join().then((String string) {
          print(string);
        });
      } else {
        print('error');
      }
    }).catchError((error) {
      print('error');
    });
  }

// 发送POST请求，multipart/form-data，上传文件
  postFileClient() async {
    var url = "HTTPs://abc.com:8090/path5";
    var client = new HTTP.MultipartRequest("post", Uri.parse(url));
    HTTP.MultipartFile.fromPath('file', 'sdcard/img.png',
            filename: 'img.png', contentType: MediaType('image', 'png'))
        .then((HTTP.MultipartFile file) {
      client.files.add(file);
      client.fields["description"] = "descriptiondescription";
      client.send().then((HTTP.StreamedResponse response) {
        if (response.statusCode == 200) {
          response.stream.transform(utf8.decoder).join().then((String string) {
            print(string);
          });
        } else {
          response.stream.transform(utf8.decoder).join().then((String string) {
            print(string);
          });
        }
      }).catchError((error) {
        print(error);
      });
    });
  }

  ///其余的HEAD、PUT、DELETE请求用法类似，大同小异，大家可以自己试一下
  ///在Widget里请求成功数据后，使用setState来更新内容和状态即可
  ///setState(() {
  ///    ...
  ///  });
}
</code></pre>
<p><strong>第三种：第三方库实现。</strong></p>
<p>Flutter 第三方库有很多可以实现 HTTP 网络请求，例如国内开发者开发的 dio 库，dio 支持多个文件上传、文件下载、并发请求等复杂的操作。在 Dart PUB 上可以搜索 dio。</p>
<p><img src="https://images.gitbook.cn/FuCw7U79AUK30cqtWxZ24tsvLHvT" alt="引用dio库" /></p>
<p>在项目的 pubspec.yaml 配置文件里加入引用：</p>
<pre><code class="dart language-dart">dependencies:
  dio: ^2.0.14
</code></pre>
<p>这样就可以引用 dio 的 API 库来实现 HTTP 网络请求了。</p>
<p>给一个完整的 dio 用法例子：</p>
<pre><code class="dart language-dart">import 'dart:io';

import 'package:dio/dio.dart';

class DartHTTPUtils {
  //配置dio，通过BaseOptions
  Dio _dio = Dio(BaseOptions(
      baseUrl: "HTTPs://abc.com:8090/",
      connectTimeout: 5000,
      receiveTimeout: 5000));

  //dio的GET请求
  getDio() async {
    var url = "/path1?name=abc&amp;pwd=123";
    _dio.get(url).then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    });
  }

  getUriDio() async {
    var url = "/path1?name=abc&amp;pwd=123";
    _dio.getUri(Uri.parse(url)).then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

//dio的GET请求，通过queryParameters配置传递参数
  getParametersDio() async {
    var url = "/path1";
    _dio.get(url, queryParameters: {"name": 'abc', "pwd": 123}).then(
        (Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

//发送POST请求，application/x-www-form-urlencoded
  postUrlencodedDio() async {
    var url = "/path2";
    _dio
        .post(url,
            data: {"name": 'value1', "pwd": 123},
            options: Options(
                contentType:
                    ContentType.parse("application/x-www-form-urlencoded")))
        .then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

  //发送POST请求，application/json
  postJsonDio() async {
    var url = "/path3";
    _dio
        .post(url,
            data: {"name": 'value1', "pwd": 123},
            options: Options(contentType: ContentType.json))
        .then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

  // 发送POST请求，multipart/form-data
  postFormDataDio() async {
    var url = "/path4";
    FormData _formData = FormData.from({
      "name": "value1",
      "pwd": 123,
    });
    _dio.post(url, data: _formData).then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

  // 发送POST请求，multipart/form-data，上传文件
  postFileDio() async {
    var url = "/path5";
    FormData _formData = FormData.from({
      "description": "descriptiondescription",
      "file": UploadFileInfo(File("./example/upload.txt"), "upload.txt")
    });
    _dio.post(url, data: _formData).then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

  //dio下载文件
  downloadFileDio() {
    var urlPath = "HTTPs://abc.com:8090/";
    var savePath = "./abc.html";
    _dio.download(urlPath, savePath).then((Response response) {
      if (response.statusCode == 200) {
        print(response.data.toString());
      }
    }).catchError((error) {
      print(error.toString());
    });
  }

  ///其余的HEAD、PUT、DELETE请求用法类似，大同小异，大家可以自己试一下
  ///在Widget里请求成功数据后，使用setState来更新内容和状态即可
  ///setState(() {
  ///    ...
  ///  });
}
</code></pre>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解 Flutter 进行 HTTP 请求的三种方式及其特点。网络请求是比较重要和常用的功能，全面详细的学习用法后，可以为高效的开发做好准备。注意点和建议如下：</p>
<ul>
<li>建议这三种方式大家都了解，这样可以更全面深入地了解 Flutter 的网络请求使用；</li>
<li>推荐使用第二种和第三种方式，可以满足常用和复杂的场景；</li>
<li>学习完后，可以进行一个实践练习，如用 GitHub 开放的接口进行测试 GET 和 POST 请求。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>