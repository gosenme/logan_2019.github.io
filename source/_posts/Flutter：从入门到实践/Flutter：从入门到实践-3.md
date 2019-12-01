---
title: Flutter：从入门到实践-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>学习一门编程语言，首页要了解它的历史和特点。Dart 是 Google 公司推出的编程语言，于 2011 年就已经亮相了。Dart 也是一门面向对象的语言，语法和 Java、C、JavaScript 很像。所以会 Java 语言，学习 Dart 一般会快一些。</p>
<p>Dart 里所有的类都可以看成是对象，是单继承，动态类语言。可以进行多平台开发，我们的主角 Flutter 就是基于 Dart 语言编写的。本节课程里，我们就开始进行 Dart 语言的基础语法学习。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Dart 的特点及简单介绍</li>
  <li>Dart 的数据类型、操作符、变量常量</li>
  <li>Dart 的运算符、流程控制语句</li>
  <li>Dart 的函数（方法）、类</li>
  <li>Dart 的泛型、接口等</li>
  </ul>
</blockquote>
<h3 id="1dart">1 Dart 简单介绍</h3>
<h4 id="11dart">1.1 为什么要介绍 Dart？</h4>
<p>Google 计划未来的 Flutter 将会是移动应用、Web 应用、PC 应用等平台的跨平台高性能框架，也是未来的 Fuchsia 操作系统的主要框架，而 Flutter 是基于 Dart 编程语言编写的一个跨平台框架，所以一些语法是基于 Dart 语法来使用的，学习 Flutter 就要先了解 Dart。</p>
<h4 id="12dart">1.2 什么是 Dart？</h4>
<p>简单介绍下 Dart 语言。</p>
<p>Dart 是 Google 公司推出的编程语言，属于应用层编程语言，于 2011 年就已经亮相了。Dart 也是一门面向对象的语言，语法和 Java、C、JavaScript 很像。Dart 里所有的类都可以看成是对象，是单继承，动态类语言。Dart 可以进行移动应用、Web应用、服务器应用、PC 应用、物联网应用的开发等等，还在不断拓展开发平台，所以可以说 Dart 在各个平台领域“无所不能”。我们的主角 Flutter 就是基于 Dart 语言编写的。</p>
<p><img src="https://images.gitbook.cn/FngxpTQmf0I29XxlkilaNieZlGrn" alt="Dart的应用" /></p>
<h4 id="13dart">1.3 Dart 的特性</h4>
<p>接下来看下 Dart 的特性。</p>
<ul>
<li>语法简单明了，开发速度快、效率高，学习成本低。</li>
<li>简单但是功能强大，可以开发 Web、移动端、PC、服务器端、物联网等平台应用。</li>
<li>编译执行速度快，拥有自己的 Dart VM，在移动端和 Web 上拥有高性能。</li>
<li>全平台语言，可移植。Dart 类似于中间件语言，可以编译成不同平台的原生代码，可以很方便地扩展成跨平台应用语言，如 Android 和 iOS 平台。</li>
<li>语言的结构融合了 Java、C、JavaScrpit 的特点，并结合 React 响应式编程的思维规范进行构建的一个现代化编程语言。</li>
</ul>
<h4 id="14dart">1.4 Dart 的语法特点</h4>
<ul>
<li>面向对象的语言，一切数据类型、API 都是对象，都继承自 Object 类；</li>
<li>强类型语言，同时也是动态类型语言。对不确定类型的可以定义成一个动态类型；</li>
<li>Dart 没有设置定义访问域的关键字，如果某个变量或者方法、类的名称以"_"开头，说明这个变量或者方法、类是私有的，外部不可以调用使用；</li>
<li>Dart 有入口函数：main(){...}；类似于Java的public void main(String[] args){...};</li>
<li>Dart 吸收了很多现代编程语言的特点，加入了很多便捷的语法支持，可以明显缩减代码量和提高可读性；</li>
<li>拥有 Future 和 Streams 使用方式，可以进行类似 RxJava 式的使用。</li>
</ul>
<h3 id="2dart">2 Dart 的关键字</h3>
<p>好了，说了这么多，接下来该进入正题，我们来学习一些具体知识。
首先看下 Dart 的关键字（33 个保留字，17 个内置标志符）。</p>
<p>33 个 Dart 保留字：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">关键字</th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">assert</td>
<td style="text-align:center;">break</td>
<td style="text-align:center;">const</td>
<td style="text-align:center;">continue</td>
<td style="text-align:center;">case</td>
<td style="text-align:center;">catch</td>
<td style="text-align:center;">class</td>
</tr>
<tr>
<td style="text-align:center;">default</td>
<td style="text-align:center;">else</td>
<td style="text-align:center;">enum</td>
<td style="text-align:center;">extends</td>
<td style="text-align:center;">final</td>
<td style="text-align:center;">finally</td>
<td style="text-align:center;">false</td>
</tr>
<tr>
<td style="text-align:center;">for</td>
<td style="text-align:center;">if</td>
<td style="text-align:center;">in</td>
<td style="text-align:center;">is</td>
<td style="text-align:center;">new</td>
<td style="text-align:center;">null</td>
<td style="text-align:center;">rethrow</td>
</tr>
<tr>
<td style="text-align:center;">return</td>
<td style="text-align:center;">superdo</td>
<td style="text-align:center;">switch</td>
<td style="text-align:center;">throw</td>
<td style="text-align:center;">try</td>
<td style="text-align:center;">typedef</td>
<td style="text-align:center;">this</td>
</tr>
<tr>
<td style="text-align:center;">true</td>
<td style="text-align:center;">var</td>
<td style="text-align:center;">void</td>
<td style="text-align:center;">while</td>
<td style="text-align:center;">with</td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
</tr>
</tbody>
</table>
<p>17 个 Dart 内置标志符：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">关键字</th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">abstract</td>
<td style="text-align:center;">as</td>
<td style="text-align:center;">covariant</td>
<td style="text-align:center;">deferred</td>
<td style="text-align:center;">dynamic</td>
<td style="text-align:center;">export</td>
<td style="text-align:center;">external</td>
</tr>
<tr>
<td style="text-align:center;">factory</td>
<td style="text-align:center;">get</td>
<td style="text-align:center;">implements</td>
<td style="text-align:center;">import</td>
<td style="text-align:center;">library</td>
<td style="text-align:center;">operator</td>
<td style="text-align:center;">part</td>
</tr>
<tr>
<td style="text-align:center;">set</td>
<td style="text-align:center;">static</td>
<td style="text-align:center;">typedef</td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
</tr>
</tbody>
</table>
<p>6 个 Dart2 新增异步功能关键字：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">关键字</th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">async</td>
<td style="text-align:center;">async*</td>
<td style="text-align:center;">await</td>
<td style="text-align:center;">sync*</td>
<td style="text-align:center;">yield</td>
<td style="text-align:center;">yield*</td>
</tr>
</tbody>
</table>
<p>25 个 Dart 特有关键字（和 Java 语言相比）：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">关键字</th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
<th style="text-align:center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">as</td>
<td style="text-align:center;">assert</td>
<td style="text-align:center;">async</td>
<td style="text-align:center;">async*</td>
<td style="text-align:center;">await</td>
<td style="text-align:center;">const</td>
<td style="text-align:center;">covariant</td>
</tr>
<tr>
<td style="text-align:center;">deferred</td>
<td style="text-align:center;">dynamic</td>
<td style="text-align:center;">export</td>
<td style="text-align:center;">external</td>
<td style="text-align:center;">factory</td>
<td style="text-align:center;">get</td>
<td style="text-align:center;">in</td>
</tr>
<tr>
<td style="text-align:center;">is</td>
<td style="text-align:center;">library</td>
<td style="text-align:center;">operator</td>
<td style="text-align:center;">part</td>
<td style="text-align:center;">rethrow</td>
<td style="text-align:center;">set</td>
<td style="text-align:center;">sync*</td>
</tr>
<tr>
<td style="text-align:center;">typedef</td>
<td style="text-align:center;">var</td>
<td style="text-align:center;">yield</td>
<td style="text-align:center;">yield*</td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
<td style="text-align:center;"></td>
</tr>
</tbody>
</table>
<h3 id="3dart">3 Dart 的数据类型</h3>
<p>我们先看一个官方给的最基础的 Dart 例子，例如我们新建一个 demo.dart 类：</p>
<pre><code class="dart language-dart">// 这是程序执行的入口
main() {
  var number = 30; // 定义变量number并进行赋值初始化
  printNumber(number); // 调用方法
}

// 定义方法printNumber
printNumber(num aNumber) {
  print('The number is $aNumber.'); // 在控制台打印输出内容
}
</code></pre>
<p>这个例子涵盖了 Dart 的一个基础的语法结构，有入口、有变量声明、赋值、定义方法、调用方法、传递参数、数据类型、变量引用等等。</p>
<p>那么接下来我们看下 Dart 支持的几种基本数据类型：numbers(num)、String、bool、List 集合、Map 集合、runes（用于在字符串中表示 Unicode 字符）、symbol。</p>
<p>numbers（num）类型是表示数值型的数据类型，包括 int 和 double 类型两种。num 是 int 和 double 类型的父类。其中 int 整数值一般范围在 -2^53 和 2^53 之间；double 是 64 位双精度浮点型数据类型。举个例子：</p>
<pre><code class="dart language-dart">void main() {
  //定义int和double类型
  int a = 6;
  double b = 3.18;
  print('$a ,$b');

  // String转int
  int twoInt = int.parse('2');
  // String转double
  var twoDouble = double.parse('2.2');
  print('$twoInt ,$twoDouble');

  // int转String
  String intToString = 2.toString();
  // double转String，后面需加入保留小数点位数
  String doubleToString = 3.23456.toStringAsFixed(2);
  print('$intToString,$doubleToString');

  //自动四舍五入
  String fiveString = 2.12832.toStringAsFixed(2);
  print(fiveString);
}
</code></pre>
<p>输出结果为：</p>
<pre><code class="dart language-dart">6 ,3.18
2 ,2.2
2,3.23
2.13
</code></pre>
<p>大家可以在 DartPad 上进行操作：<a href="https://dartpad.dartlang.org">https://dartpad.dartlang.org</a></p>
<p><strong>String 类型</strong></p>
<p>大家应该都很熟悉，字符串类型。</p>
<ul>
<li>Dart 字符串是 UTF-16 编码的字符序列，可以使用单引号或者双引号来创建字符串。</li>
<li>可以在字符串中使用表达式，用法是这样的： ${expression}。</li>
<li>可以使用 + 操作符来把多个字符串链接为一个，当然也可以不用加号，多个带引号的字符串挨着写就可以了。</li>
<li>使用三个单引号或者双引号也可以创建多行字符串。</li>
<li>使用 r 前缀可以创建一个原始字符串。</li>
</ul>
<p>再来看一个例子：</p>
<pre><code class="dart language-dart">void main() {
  //单引号和双引号定义
  String singleString = 'A singleString';
  String doubleString = "A doubleString";
  print('$singleString ,$doubleString');

//使用$字符引用变量，使用{}引入表达式
  String userS = 'It\'s $singleString';
  String userExpression = 'It\'s expression,${singleString.toUpperCase()}';
  print('$userS');
  print('$userExpression');

//使用引号字符串邻接来拼接或者使用+号连接字符串
  String stringLines =
      'String ' 'concatenation' " works even over line breaks.";
  String addString = 'A and ' + 'B';
  print('$stringLines');
  print('$addString');

//使用三个引号（单引号或双引号）来创建多行字符串
  String s3 = '''
You can create
multi-line strings like this one.
''';
  String s33 = """This is also a
multi-line string.""";
  print('$s3');
  print('$s33');

//使用r为开头，显示定义一个原始字符串
  String s = r"It is a \n raw string.";
  print('$s');
}
</code></pre>
<p>输出结果为：</p>
<pre><code class="dart language-dart">A singleString ,A doubleString
It's A singleString
It's expression,A SINGLESTRING
String concatenation works even over line breaks.
A and B
You can create
multi-line strings like this one.

This is also a
multi-line string.
It is a \n raw string.
</code></pre>
<p><strong>bool 类型</strong></p>
<p>用于定义 true 或 false 的数据类型，很简单。需要区别注意的是有些写法在 Dart 里不支持。</p>
<pre><code class="dart language-dart">var name = 'Tom';
if (name) {
  // JavaScript可以这样写，Dart不行
  print('He is Tom!');
}

// JavaScript可以这样写，Dart不行
if (1) {
  print('A line Data.');
} else {
  print('A good Data.');
}
</code></pre>
<p><strong>List 集合</strong></p>
<p>Dart 里使用 List 来表示数据集合结构。</p>
<pre><code class="dart language-dart">void main() {
  //定义初始化一个集合
  var list = [1, 2, 3];
  List listData = [5, 6, 7];
  print(list.length);
  print(list[0]);
  //集合数据赋值
  listData[1] = 8;
  print(listData[1]);
  //如果在集合前加了const关键字，集合数据不可以进行操作
  var constantList = const [1, 2, 3];
  List datas = List();
  datas.add('data1');
  datas.addAll(['data2', 'data3', 'data4', 'data5', 'data6']);
  //输出第一个元素
  print(datas.first);
  // 获取最后一个元素
  print(datas.last);
  // 获取元素的位置
  print(datas.indexOf('data1'));
  // 删除指定位置元素
  print(datas.removeAt(2));
  //删除元素
  datas.remove('data1');
  //删除最后一个元素
  datas.removeLast();
  // 删除指定范围元素，含头不含尾
  datas.removeRange(0, 2);
  //删除指定条件的元素
  datas.removeWhere((item) =&gt; item.length &gt; 3);
  // 删除所有的元素
  datas.clear();
  //其他方法可以自己尝试
}
</code></pre>
<p><strong>Map 集合</strong></p>
<p>Map 集合存储数据特点就是键值对（key-value）形式。key 是唯一的，value 允许重复。看一个实例：</p>
<pre><code class="dart language-dart">void main() {
  //定义一个map并赋值
  var gifts = {
    // Keys      Values
    'first': 'dog',
    'second': 'cat',
    'fifth': 'orange'
  };

  var nobleGases = {
    // Keys  Values
    2: 'a',
    10: 'b',
    18: 'b',
  };
  //定义一个map并赋值
  Map map = Map();
  map['first'] = 'a-value';
  map['second'] = 'b-value';
  map['fifth'] = 'c-value';
  Map nobleGasesMap = Map();
  nobleGasesMap[2] = 'a-value';
  nobleGasesMap[10] = 'b-value';
  nobleGasesMap[18] = 'c-value';
  //指定键值对类型
  var nobleGases = new Map&lt;int, String&gt;();
  //获取某个key的value
  print(map['first']);
  //获取map大小
  print(map.length);
  //定义一个不可变的map
  final constantMap = const {
    2: 'a',
    10: 'b',
    18: 'c',
  };
  //其他API用法和List类似
}
</code></pre>
<p><strong>Runes 类型</strong></p>
<p>表示字符串 Unicode 编码字符（UTF-32 code points）等。</p>
<pre><code class="dart language-dart">void main() {
  //看一个官方例子
  var clapping = '\u{1f44f}';
  print(clapping);
  print(clapping.codeUnits);
  print(clapping.runes.toList());

  Runes input = new Runes(
      '\u2665  \u{1f605}  \u{1f60e}  \u{1f47b}  \u{1f596}  \u{1f44d}');
  print(new String.fromCharCodes(input));
}
</code></pre>
<p><strong>Symbols 类型</strong></p>
<p>使用 Symbol 字面量来获取标识符的 symbol 对象，也就是在标识符前面添加一个 # 符号。</p>
<pre><code class="dart language-dart"> //看一个官方例子
 #radix
 #bar
</code></pre>
<h3 id="4dart">4 Dart的操作符</h3>
<p>看下 Dart 的操作符：</p>
<table>
<thead>
<tr>
<th style="text-align:center;">描述</th>
<th style="text-align:center;">操作符</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;">一元后缀符（unary postfix）</td>
<td style="text-align:center;">expr++  &emsp;   expr--  &emsp;  () &emsp;   []   &emsp; .   &emsp; ?.</td>
</tr>
<tr>
<td style="text-align:center;">一元前缀符（unary postfix）</td>
<td style="text-align:center;">-expr  &emsp;  !expr  &emsp;  ~expr &emsp;   ++expr  &emsp;  --expr</td>
</tr>
<tr>
<td style="text-align:center;">乘法类型（multiplicative）</td>
<td style="text-align:center;">*  &emsp;  /  &emsp;  % &emsp; ~/</td>
</tr>
<tr>
<td style="text-align:center;">加法类型（additive）</td>
<td style="text-align:center;">+  &emsp;  -</td>
</tr>
<tr>
<td style="text-align:center;">位操作符（shift）</td>
<td style="text-align:center;"><<  &emsp;  >&gt;</td>
</tr>
<tr>
<td style="text-align:center;">按位与（bitwise AND）</td>
<td style="text-align:center;">&amp;</td>
</tr>
<tr>
<td style="text-align:center;">按位异或（bitwise XOR）</td>
<td style="text-align:center;">^</td>
</tr>
<tr>
<td style="text-align:center;">按为或（bitwise OR）</td>
<td style="text-align:center;">\</td>
</tr>
<tr>
<td style="text-align:center;">比较和类型测试（relational and type test）</td>
<td style="text-align:center;">&gt;=  &emsp;  &gt; &emsp;   &lt;=  &emsp;  &lt;  &emsp;  as    &emsp; is  &emsp;  is!</td>
</tr>
<tr>
<td style="text-align:center;">等价（equality）</td>
<td style="text-align:center;">==  &emsp;  !=</td>
</tr>
<tr>
<td style="text-align:center;">逻辑与（logical AND）</td>
<td style="text-align:center;">&amp;&amp;</td>
</tr>
<tr>
<td style="text-align:center;">逻辑或（logical OR）</td>
<td style="text-align:center;">\</td>
</tr>
<tr>
<td style="text-align:center;">是否是空（if null）</td>
<td style="text-align:center;">??</td>
</tr>
<tr>
<td style="text-align:center;">条件运算符（conditional）</td>
<td style="text-align:center;">expr1 ? expr2 : expr3</td>
</tr>
<tr>
<td style="text-align:center;">级联运算符（cascade）</td>
<td style="text-align:center;">..</td>
</tr>
<tr>
<td style="text-align:center;">赋值（assignment）</td>
<td style="text-align:center;">=  &emsp;  *=  &emsp;  /=  &emsp;  ~/=  &emsp;  %=  &emsp;  +=   &emsp; -= &emsp;   <<=  &emsp;  >&gt;=  &emsp;  &amp;=   &emsp; ^=  &emsp;</td>
</tr>
</tbody>
</table>
<p>这些操作符用法和其他语言的含义和用法大同小异。</p>
<h3 id="5dart">5 Dart 的流程控制语句</h3>
<p>Dart 流程控制语句也不多，比较简单。主要有：</p>
<ul>
<li>if 和 else</li>
<li>for 循环</li>
<li>while 和 do-while 循环</li>
<li>break 和 continue</li>
<li>switch 和 case</li>
<li>assert 断言（判断是否相等）</li>
</ul>
<p>如果其中涉及到使用 try-catch 和 throw，可能会影响一些流程控制的跳转。</p>
<pre><code class="dart language-dart">void main() {
  //if和else
  if (hasData()) {
    print("hasData");
  } else if (hasString()) {
    print("hasString");
  } else {
    print("noStringData");
  }

  //for循环
  var message = new StringBuffer("Dart is good");
  for (var i = 0; i &lt; 6; i++) {
    message.write(',');
  }

  //while
  while (okString()) {
    print('ok');
  }
//do-while
  do {
    print('okDo');
  } while (!hasData());

  //break和continue
  while (true) {
    if (noData()) {
      break;
    }
    if (hasData()) {
      continue;
    }
    doSomething();
  }

  //switch和case
  var command = 'OPEN';
  switch (command) {
    case 'A':
      executeA();
      break;
    case 'B':
      executeB();
      break;
    case 'C':
      executeC();
      break;
    default:
      executeUnknown();
  }

  //Assert（断言）
  assert(string != null);
  assert(number &lt; 80);
  assert(urlString.startsWith('https'));
}
</code></pre>
<p>Exceptions 异常捕获处理。</p>
<p>使用 throw 抛出异常。</p>
<pre><code class="dart language-dart">throw new FormatException('Expected at least 2 section');
</code></pre>
<p>也可以抛出其他类型对象。</p>
<pre><code class="dart language-dart">throw 'no data!';
</code></pre>
<p>使用 catch 捕获异常。</p>
<pre><code class="dart language-dart">try {
  getData();
} on OutOfLlamasException {
  sendData();
} on Exception catch (e) {
  print('Unknown data Exception: $e');
} catch (e) {
  print('Some Exception really unknown: $e');
}
</code></pre>
<p>使用 rethrow 可以把捕获的异常给重新抛出。</p>
<pre><code class="dart language-dart">//给出一个官方例子
final foo = '';

void misbehave() {
  try {
    foo = "You can't change a final variable's value.";
  } catch (e) {
    print('misbehave() partially handled ${e.runtimeType}.');
    rethrow; // rethrow重新抛出，允许main()里的函数继续捕获处理异常
  }
}

void main() {
  try {
    misbehave();
  } catch (e) {
    print('main() finished handling ${e.runtimeType}.');
  }
}
</code></pre>
<p>Finally 处理，和 Java 里的类似，不管是否出现异常，最终都要执行的方法写在这里。</p>
<pre><code class="dart language-dart">try {
  getData();
} catch(e) {
  print('Error: $e');
} finally {
  //始终执行
  sendData();
}
</code></pre>
<h3 id="6dart">6 Dart 的类和函数（方法）</h3>
<p>类这个概念是面向对象里的，Dart 也依然保留。我们创建对象需要创建类对象，可以使用 new 关键字，也可以不使用：</p>
<pre><code class="dart language-dart">var map=Map();
var map2=new Map();
</code></pre>
<p>调用类方法：</p>
<pre><code class="dart language-dart">var map=Map();
  map.length;
  //通过 对象.方法 的形式来调用使用方法
</code></pre>
<p>使用 ?. 来替代 . 可以避免当左边对象为 null 时抛出异常：</p>
<pre><code class="dart language-dart">  a?.name = 'Tom';
</code></pre>
<p>关于获取对象的类型，可以使用 Object 的 runtimeType 属性来获取实例的类型。</p>
<p>先看一个实例化对象，并获取和调用属性和方法的例子，和 Java 用法基本一致：</p>
<pre><code class="dart language-dart">class Position {
  num x;
  num y;
  methodPosition(){
      ...
  }
}

void main() {
  var pos = new Position();
  pos.x = 5;//赋值
  print(pos.x);//取值
  pos.methodPosition();//调用方法
}
</code></pre>
<p>定义同名构造方法：</p>
<pre><code class="dart language-dart">class Position {
  num x;
  num y;

  Position(num x, num y) {
    this.x = x;
    this.y = y;
  }
}
//也可以这样简化定义构造方法
class Point {
  num x;
  num y;

  Point(this.x, this.y);
}
</code></pre>
<blockquote>
  <p>注意：Dart 的构造函数不可以继承，父类的构造函数也不可以继承。</p>
</blockquote>
<p>Dart 也支持抽象函数（抽象类）：</p>
<pre><code class="dart language-dart">abstract class Dog {
  //可以定义变量和抽象方法

  void doSomething(); // 定义抽象方法
}

class GoodDog extends Dog {
  void doSomething() {
    //实现逻辑
  }
}
</code></pre>
<p>Dart 的类可以继承多个类，这个 Dart 的一大特点。Dart 也支持实现多个接口，使用 implements 关键字：</p>
<pre><code class="dart language-dart">class Comparable {
  final _name;

  Comparable(this._name);

  String good1(who) =&gt; 'Hello';
}

class Location {
  Location();

  String good2() =&gt; 'World!';
}

class ImlClass implements Comparable, Location {
  // ...
}
</code></pre>
<p>Dart 通过 extends 来继承拓展类，子类可以重写父类方法，通过 supper 来引用父类方法。</p>
<pre><code class="dart language-dart">class Product {
  void open() {
    //...
  }
   // ...
}

class SmartProduct extends Product {
  void open() {
    super.open();
    //重写加入新的逻辑
  }
  // ...
}
//也可以使用@override注解来表示重写了父类方法 
</code></pre>
<p>还有其他注解，如可以使用 @proxy 注解来避免警告信息。</p>
<p>Dart 也支持枚举类型 enum：</p>
<pre><code class="dart language-dart">enum Color {
  red,
  green,
  blue
}
//使用时候直接调用
Color.blue
</code></pre>
<p>可以使用 with 关键字实现多继承：</p>
<pre><code class="dart language-dart">//看一个官方例子
class Musician extends Performer with Musical {
  // ...
}

class Maestro extends Person
    with Musical, Aggressive, Demented {
  Maestro(String maestroName) {
    name = maestroName;
    canConduct = true;
  }
}
</code></pre>
<p>Dart 支持静态函数使用，使用时候直接类名.函数名即可。</p>
<pre><code class="dart language-dart">class Position {

  static num getLongPosition() {
    return 20;
  }
}

void main(){
    //直接调用
    Position.getLongPosition();
}
</code></pre>
<h3 id="7dart">7 Dart 的泛型和限制域</h3>
<p>Java 中泛型使用 T 来表示，Dart 里同样可以使用 T 来表示泛型类型。</p>
<pre><code class="dart language-dart">abstract class Dog&lt;T&gt; {
  T getDogByName(String name);
  setDogByname(String name, T value);
}

//也可以限制泛型继承自什么类等操作
class Foo&lt;T extends SomeBaseClass&gt; {...}

class Extender extends SomeBaseClass {...}

void main() {
  var someBaseClassFoo = new Foo&lt;SomeBaseClass&gt;();
  var extenderFoo = new Foo&lt;Extender&gt;();
  var foo = new Foo();
}
</code></pre>
<p>Dart 的库的引入和使用：Dart 使用 import 关键字来导入库和类。</p>
<pre><code class="dart language-dart">import 'dart:io';
import 'package:mylib/mylib.dart';
import 'package:utils/utils.dart';
//如果两个导入的库里的类有重名的，可以使用as关键字
import 'package:utils2/utils2.dart' as utils2;

//也可以只导入库的一小部分
//只导入foo库
import 'package:lib1/lib1.dart' show foo;

//除了foo，其他的都导入
import 'package:lib2/lib2.dart' hide foo;

//延迟载入库，可以减少APP启动时间，优化性能
import 'package:deferred/hello.dart' deferred as hello;
//延迟后，使用的时候使用loadLibrary（）来调用
//在一个库上可以多次调用loadLibrary() 函数,只执行载入一次
greet() async {
  await hello.loadLibrary();
  hello.printGreeting();
}
</code></pre>
<p>如果我们想自己创建声明一个库想被别人引用时候，可以用 library 声明：</p>
<pre><code class="dart language-dart"> // 声明库，名字为abc
  library abc;
  // 导入需要用到的相关库
  import 'dart:html';
  //编写逻辑
  ...
  //如果需要的话，可以借助part关键字来实现部分需求
</code></pre>
<p>如果你想声明某个变量、常量、方法函数不能被外部调用，只需要在名字前加上 _ 下划线前缀即可。</p>
<h3 id="8dart">8 Dart 的异步处理</h3>
<p>Dart 支持异步编程操作，例如我们的网络请求、耗时操作都可以使用。可以使用 async 和 await 关键字来进行标识异步操作。</p>
<p>Dart 里也有 Future 和 Stream 对象进行异步操作，非常的强大和方便。</p>
<pre><code class="dart language-dart">//例如用await来表示这个方法异步的，需要等待完成后才能继续执行后面的方法
await lookUpVersion()
//要使用 await，其方法必须带有 async 关键字：
checkVersion() async {
  var version = await lookUpVersion();
  if (version == expectedVersion) {
    //执行操作
  } else {
    //执行操作
  }
}
//我们也可以使用Future来修饰包转返回类型，这样我们可以支持数据的后续其他操作
Future&lt;String&gt; lookUpVersion() async =&gt; '1.6.0';
</code></pre>
<p>在 await 表达式中，表达式的返回值通常是一个 Future 类型；如果返回的值不是 Future，则 Dart 会自动把该值放到 Future 中返回。</p>
<p>Dart 的基础语法知识部分就大概这么多，还有很多细节，大家有兴趣可以进行深入研究使用方法。</p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解 Dart 的基础语法部分，为后续 Flutter 的开发学习奠定基础，以期更好地进行深入研究和开发。Dart 的语法比较简单，和 Java 类似，可以对照着理解，全面详细的学习用法后，可以为高效开发做好准备。主要注意点和建议如下：</p>
<ul>
<li>建议将例子进行编写实践下，使用开发工具输出下结果加深理解。</li>
<li>学习完后，可以进行一个实践练习，也为学习下一课时作准备。</li>
</ul>
<blockquote>
  <p><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5cc01cc115a1a10d8cec9e86&utm_source=Raysd001">点击了解更多《Flutter：从入门到实践》</a></p>
</blockquote>
<hr />
<blockquote>
  <p>注意！！！
  为了方便学习和技术交流，特意创建了《Flutter：从入门到实践》的读者群，入群方式放在 <a href="https://gitbook.cn/gitchat/column/5cc01cc115a1a10d8cec9e86/topic/5cc0254915a1a10d8cec9fd3">1-3课</a> 文末，欢迎已购本课程的同学入群交流。</p>
</blockquote></div></article>