---
title: Flutter：从入门到实践-27
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>国际化就是让我们的应用支持多种语言，例如运行在国内的使用中文简体、在港澳台的使用繁体字、美国的使用英文、日本的用户显示的是日文等等类似场景，也可以把国际化称为本地化处理。Flutter 本身的 API 是支持国际化处理的，当然也可以用官方提供的插件库来实现。</p>
<p>那么这节课我们将介绍 Flutter 中应用国际化处理的基本使用详解，并配合一些案例。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>实现应用国际化</li>
  <li>使用插件库实现应用国际化</li>
  </ul>
</blockquote>
<h3 id="">实现应用国际化</h3>
<p>如果我们的应用想提供多种语言模式，那么就需要进行国际化处理，Flutter 本身是支持国际化处理的。</p>
<p>在 Flutter 中使用国际化一般要配合 MaterialApp 或 WidgetsApp 的国际化属性localizationsDelegates 和 supportedLocales。并且在 pubspec.yaml 配置 flutter_localizations 的一个单独包。截至 2017 年 10 月，该软件包支持 15 种语言（来源于官方）。</p>
<p>接下来我们看下 Flutter 实现国际化的步骤。</p>
<p>首先需要配置 pubspec.yaml：</p>
<pre><code class="dart language-dart">dependencies:
  flutter:
    sdk: flutter
  // 添加国际化包
  flutter_localizations:
    sdk: flutter
</code></pre>
<p>接下来在使用的页面导入包：</p>
<pre><code class="dart language-dart">import 'package:flutter_localizations/flutter_localizations.dart';
</code></pre>
<p>使用 MaterialApp 或 WidgetsApp 的属性来配置：</p>
<pre><code class="dart language-dart">class LocalizationsSamplesState extends State&lt;LocalizationsSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        // 这里要自己实现一个Localizations.delegate
      ],
      supportedLocales: [
        const Locale('en', 'US'), // English
        const Locale('zh', 'CN'), // Chinese
        // ... 其他语言支持
      ],
      home: getBody(),
    );
  }
...
}
</code></pre>
<p>supportedLocales 里定义的是语种，Locale 来定义语言语种，参数包括语言和国家两个标志。</p>
<p>接下来我们需要自己实现一个 GlobalMaterialLocalizations，本地化需要 Localizations 和Delegate 两个类才可以，我们先实现 Localizations：</p>
<pre><code class="dart language-dart">import 'package:flutter/widgets.dart';

class PageLocalizations {
  final Locale locale;
  PageLocalizations(this.locale);

  static Map&lt;String, Map&lt;String, String&gt;&gt; _localizedValues = {
    'en': {
      'task title': 'Flutter Demo',
      'titlebar title': 'Flutter Demo Home Page',
      'click tip': 'You have pushed the button this many times:',
      'inc': 'Increment'
    },
    'zh': {
      'task title': 'Flutter 示例',
      'titlebar title': 'Flutter 示例主页面',
      'click tip': '你一共点击了这么多次按钮：',
      'inc': '增加'
    }
  };

  get taskTitle {
    return _localizedValues[locale.languageCode]['task title'];
  }

  get titleBarTitle {
    return _localizedValues[locale.languageCode]['titlebar title'];
  }

  get clickTop {
    return _localizedValues[locale.languageCode]['click tip'];
  }

  get inc {
    return _localizedValues[locale.languageCode]['inc'];
  }

  static PageLocalizations of(BuildContext context) {
    return Localizations.of(context, PageLocalizations);
  }
}
</code></pre>
<p>接下来实现 Delegate：</p>
<pre><code class="dart language-dart">import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_samples/samples/pageLocalizations.dart';

class GlobalPagesLocalizations
    extends LocalizationsDelegate&lt;PageLocalizations&gt; {
  const GlobalPagesLocalizations();

  // 是否支持某个语言
  @override
  bool isSupported(Locale locale) {
    return ['en', 'zh'].contains(locale.languageCode);
  }

    // 加载对应的语言资源，自动调用
  @override
  Future&lt;PageLocalizations&gt; load(Locale locale) {
    return new SynchronousFuture&lt;PageLocalizations&gt;(
        new PageLocalizations(locale));
  }

  // 重新加载
  @override
  bool shouldReload(LocalizationsDelegate&lt;PageLocalizations&gt; old) {
    return false;
  }

  static GlobalPagesLocalizations delegate = const GlobalPagesLocalizations();
}
</code></pre>
<p>最后调用使用即可：</p>
<pre><code class="dart language-dart">class LocalizationsSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return LocalizationsSamplesState();
  }
}

class LocalizationsSamplesState extends State&lt;LocalizationsSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalPagesLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('en', 'US'), // English
        const Locale('zh', 'CN'), // Chinese
        // ... 其他语言支持
      ],
      home: WelcomePage(),
    );
  }
}

class WelcomePage extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return WelcomeState();
  }
}

class WelcomeState extends State&lt;WelcomePage&gt; {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Localizations'),
        primary: true,
      ),
      body: Column(
        children: &lt;Widget&gt;[
          // 调用国际化后的属性资源
          Text(PageLocalizations.of(context).taskTitle,)
        ],
      ),
    );
  }
}
</code></pre>
<p>可以看到调用的方式是:PageLocalizations.of(context).taskTitle。</p>
<p>这样，当我们的手机在切换语言环境时，应用便会自动显示当前语言环境下的字符资源，达到国际化目的。</p>
<h3 id="-1">使用插件库实现应用国际化</h3>
<p>接下来我们看下通过插件库来实现的应用国际化的用法，如 intl 和 flutter_i18n 插件。这两个插件库都是 Flutter 官方的，这两个基本原理是一样的，只不过 flutter_i18n 是自动化执行了将 arb文件转为 dart 的等操作。那么这里直接以 flutter_i18n 插件为例给大家讲解通过插件库实现应用国际化。这里需要使用 Android Studio 安装一个 Flutter i18n 插件：</p>
<p><img src="https://images.gitbook.cn/FrQeeIiVk9Y8-Q-4nua5ggS5P5Oq" alt="Flutter i18n插件" /></p>
<p>Flutter i18n 插件可以帮助我们简化手动编写 arb 和生成 dart 这个过程。其原理是通过 arb 文件来自动生成所需要的代码。</p>
<p>插件安装完后悔自动出现一个按钮，按这个按钮就可以自动根据项目根目录的 res 里的 arb 文件来自动在 lib/generated 生成名字叫 i18n.dart 的 dart 文件。</p>
<p><img src="https://images.gitbook.cn/FupO10DbHETlZxZz5svy510bp1Qn" alt="Flutter i18n插件" /></p>
<p><img src="https://images.gitbook.cn/FrXk4VBr6v3S5bwSOzCnsDo1pFZ-" alt="Flutter i18n插件" /></p>
<p>我们可以右键新建新的需要支持的语言 arb 文件。</p>
<p><img src="https://images.gitbook.cn/FmctfoI69LG0fWYE3-CtEg8cPGHT" alt="Flutter i18n插件" /></p>
<p>我们分别看下 strings_en.arb、strings_zh_CN.arb、i18n.dart 文件内容：</p>
<pre><code class="dart language-dart">// i18n.dart文件内容，这个是自动生成

import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

// ignore_for_file: non_constant_identifier_names
// ignore_for_file: camel_case_types
// ignore_for_file: prefer_single_quotes

//This file is automatically generated. DO NOT EDIT, all your changes would be lost.
class S implements WidgetsLocalizations {
  const S();

  static const GeneratedLocalizationsDelegate delegate =
    GeneratedLocalizationsDelegate();

  static S of(BuildContext context) =&gt; Localizations.of&lt;S&gt;(context, S);

  @override
  TextDirection get textDirection =&gt; TextDirection.ltr;

  String get appName =&gt; "App Name";
  String get title =&gt; "My Title";
  String hello(String name) =&gt; "Hello $name";
}

class $zh_HK extends S {
  const $zh_HK();

  @override
  TextDirection get textDirection =&gt; TextDirection.ltr;

  @override
  String get appName =&gt; "應用名";
  @override
  String get title =&gt; "我的標題";
  @override
  String hello(String name) =&gt; "妳好${name}";
}

class $en extends S {
  const $en();
}

class $zh_CN extends S {
  const $zh_CN();

  @override
  TextDirection get textDirection =&gt; TextDirection.ltr;

  @override
  String get appName =&gt; "应用名";
  @override
  String get title =&gt; "我的标题";
  @override
  String hello(String name) =&gt; "你好${name}";
}

class GeneratedLocalizationsDelegate extends LocalizationsDelegate&lt;S&gt; {
  const GeneratedLocalizationsDelegate();

  List&lt;Locale&gt; get supportedLocales {
    return const &lt;Locale&gt;[
      Locale("zh", "HK"),
      Locale("en", ""),
      Locale("zh", "CN"),
    ];
  }

  LocaleListResolutionCallback listResolution({Locale fallback}) {
    return (List&lt;Locale&gt; locales, Iterable&lt;Locale&gt; supported) {
      if (locales == null || locales.isEmpty) {
        return fallback ?? supported.first;
      } else {
        return _resolve(locales.first, fallback, supported);
      }
    };
  }

  LocaleResolutionCallback resolution({Locale fallback}) {
    return (Locale locale, Iterable&lt;Locale&gt; supported) {
      return _resolve(locale, fallback, supported);
    };
  }

  Locale _resolve(Locale locale, Locale fallback, Iterable&lt;Locale&gt; supported) {
    if (locale == null || !isSupported(locale)) {
      return fallback ?? supported.first;
    }

    final Locale languageLocale = Locale(locale.languageCode, "");
    if (supported.contains(locale)) {
      return locale;
    } else if (supported.contains(languageLocale)) {
      return languageLocale;
    } else {
      final Locale fallbackLocale = fallback ?? supported.first;
      return fallbackLocale;
    }
  }

  @override
  Future&lt;S&gt; load(Locale locale) {
    final String lang = getLang(locale);
    if (lang != null) {
      switch (lang) {
        case "zh_HK":
          return SynchronousFuture&lt;S&gt;(const $zh_HK());
        case "en":
          return SynchronousFuture&lt;S&gt;(const $en());
        case "zh_CN":
          return SynchronousFuture&lt;S&gt;(const $zh_CN());
        default:
          // NO-OP.
      }
    }
    return SynchronousFuture&lt;S&gt;(const S());
  }

  @override
  bool isSupported(Locale locale) =&gt;
    locale != null &amp;&amp; supportedLocales.contains(locale);

  @override
  bool shouldReload(GeneratedLocalizationsDelegate old) =&gt; false;
}

String getLang(Locale l) =&gt; l == null
  ? null
  : l.countryCode != null &amp;&amp; l.countryCode.isEmpty
    ? l.languageCode
    : l.toString();
</code></pre>
<p>再看下 strings_en.arb、strings_zh_CN.arb 文件内容：</p>
<pre><code class="dart language-dart">// strings_en.arb
{
  "appName": "App Name",
  "hello": "Hello $name",
  "title": "My Title"
}
// strings_zn_CN.arb
{
  "appName": "应用名",
  "hello": "你好${name}",
  "title": "我的标题"
}
</code></pre>
<p>可以看到我们也可以通过 $ 符号来进行传递动态值。</p>
<p>flutter_i18n 插件库地址：<a href="https://pub.dev/packages/flutter_i18n">https://pub.dev/packages/flutter_i18n</a>。</p>
<p>首先我们需要引用这个库：</p>
<pre><code class="dart language-dart">dependencies:
  flutter_i18n: ^0.6.3
</code></pre>
<p>在使用的地方导入库：</p>
<pre><code class="dart language-dart">import 'package:flutter_i18n/flutter_i18n.dart';
</code></pre>
<p>然后我们看下使用的方式：</p>
<pre><code class="dart language-dart">import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_app/generated/i18n.dart';
import 'package:flutter_i18n/flutter_i18n.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class LocalizationsSamples extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return LocalizationsSamplesState();
  }
}

class LocalizationsSamplesState extends State&lt;LocalizationsSamples&gt; {
      Locale _locale = const Locale('zh', 'CN');

  @override
  void initState() {
    super.initState();
    localeChange = (locale) {
      setState(() {
        _locale = locale;
      });
    };
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        // 配置delegate
        S.delegate,
      ],
      supportedLocales: [
        // 支持的语言
        const Locale('en', ''), // English
        const Locale('zh', 'CN'), // Chinese
        const Locale("zh", "HK"),
        // ... 其他语言支持
      ],
      // 我们也可以指定一种默认语言
      localeResolutionCallback:
          S.delegate.resolution(fallback: const Locale('en', '')),
      home: WelcomePage(),
    );
  }
}

class WelcomePage extends StatefulWidget {
  @override
  State&lt;StatefulWidget&gt; createState() {
    return WelcomeState();
  }
}

class WelcomeState extends State&lt;WelcomePage&gt; {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Localizations'),
        primary: true,
      ),
      body: Column(
        children: &lt;Widget&gt;[
          // 调用国际化后的属性资源
          Text(
            S.of(context).title,
          )
        ],
      ),
    );
  }
}
</code></pre>
<p>主动切换语言：</p>
<pre><code class="dart language-dart">FlutterI18n.refresh(context, Locale('en', ''));
</code></pre>
<p>当然还有其他方法：</p>
<pre><code class="dart language-dart">FlutterI18n.translate(buildContext, "your.key")

FlutterI18n.plural(buildContext, "select", 0)
</code></pre>
<p>通过插件库实现国际化就大概这么多，大家可以自己实践下。</p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_25">flutter_25</a></p>
<h3 id="-2">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的实现国际化的几种用法。注意掌握原生 API 实现国际化的用法，并尝试实现一个具有语言手动切换功能的小应用。</p>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>