---
title: 精通 Spring Boot 42 讲-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>页面布局就是对前端的页面进行划分区域，每个区域有不同的职责，布局是为了更好地重复利用前端代码，避免大量重复性的劳动。在现有的前端系统中，页面布局成了前端开发最重要的工作之一，Thymeleaf 在设计之初对页面布局就有考虑，通过 Thymeleaf 的相关语法可以很容易地实现对前端页面布局。</p>
<h3 id="">快速入手</h3>
<p><strong>Spring Boot 2.0 将布局单独提取了出来，需要单独引入依赖：thymeleaf-layout-dialect。</strong></p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;nz.net.ultraq.thymeleaf&lt;/groupId&gt;
    &lt;artifactId&gt;thymeleaf-layout-dialect&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>首先定义一个代码片段 copyright.html，放到 layout 目录下：</p>
<pre><code class="html language-html">&lt;footer th:fragment="copyright"&gt; 
&amp;copy; 2018
&lt;/footer&gt;
</code></pre>
<p>th:fragment 定义一个代码片段，创建 index.html 在页面任何地方引入：</p>
<pre><code class="html language-html">&lt;body&gt;
    &lt;div th:insert="layout/copyright :: copyright"&gt;&lt;/div&gt;
    &lt;div th:replace="layout/copyright :: copyright"&gt;&lt;/div&gt;
&lt;/body&gt;
</code></pre>
<blockquote>
  <p>th:insert 和 th:replace 区别，insert 只是加载，replace 是替换。</p>
</blockquote>
<p><strong>Thymeleaf 3.0 推荐使用 th:insert 替换 2.0 的 th:replace。</strong></p>
<p>layout 是文件夹地址，fileName 是文件名，语法这样写 layout/fileName:htmlhead，其中，htmlhead 是指定义的代码片段，如 th:fragment="htmlhead"。</p>
<p>创建一个 indexController，指向 index.html：</p>
<pre><code class="java language-java">@RequestMapping("/index")
public String index() {
    return "index";
}
</code></pre>
<p>在浏览器中输入网址，http://localhost:8080/index，可以看到以下信息：</p>
<pre><code>© 2018
© 2018
</code></pre>
<p>可以看到两条版权信息，说明两种方式都可以引入版权页面信息，这就是 Thymeleaf 最简单的页面布局了。</p>
<blockquote>
  <p>Thymeleaf 的这种特性，可以让我们在开发过程中避免写很多重复的代码，如果页面有共同的头部、尾部或者其他地方均可采用这种技术。</p>
</blockquote>
<h3 id="-1">片段表达式</h3>
<p>Thymeleaf 3.0 引入了一种新型的表达式，作为一般 Thymeleaf 标准的语法表达式之一，它就是：<strong>片段表达式</strong>。</p>
<p>它使用类似 ~{commons::footer} 的语法，作用在 th:insert 和 th:replace 的内部。使用片段表达式支持引入片段的同时传参来构造目标页面，大大提高了代码复用的灵活度。接下来使用一个案例来介绍片段表达式的使用。</p>
<p>创建一个 base.html 基础页面，作为后续其他页面引入的模板。</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head th:fragment="common_header(title,links)"&gt;
    &lt;title th:replace="${title}"&gt;comm title&lt;/title&gt;

    &lt;link rel="stylesheet" type="text/css" media="all" th:href="@{/css/myapp.css}"&gt;
    &lt;link rel="shortcut icon" th:href="@{/images/favicon.ico}"&gt;
    &lt;script type="text/javascript" th:src="@{/js/myapp.js}"&gt;&lt;/script&gt;

    &lt;th:block th:replace="${links}" /&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>使用 th:fragment 创建了一段代码片段，命名为 common_header 并且支持传入两个参数 title 和 links，并且指明了在页面中使用的位置：</p>
<ul>
<li><code>&lt;title th:replace="${title}"&gt;comm title&lt;/title&gt;</code> 在此位置插入传入的 title；</li>
<li><code>&lt;th:block th:replace="${links}" /&gt;</code> 在此位置插入传入的 link，th:block 作为页面的自定义使用不会展示到页面中。</li>
</ul>
<p>接下来创建一个 fragment.html 页面，来使用上面创建的 common_header 代码片段。</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head th:replace="base :: common_header(~{::title},~{::link})"&gt;
    &lt;title&gt;Fragment - Page&lt;/title&gt;
    &lt;link rel="stylesheet" th:href="@{/css/bootstrap.min.css}"&gt;
    &lt;link rel="stylesheet" th:href="@{/cs/fragment.css}"&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 fragment.html 的页面中使用 th:replace 引入了 <code>common_header</code> 代码片段，并且在页面中添加了 title 和 link 作为参数传递到 <code>common_header</code> 页面中。</p>
<p>在 IndexController 中添加访问入口：</p>
<pre><code class="java language-java">@RequestMapping("/fragment")
public String fragment() {
    return "fragment";
}
</code></pre>
<p>重新启动项目后，在浏览器中输入网址，http://localhost:8080/fragment，右键单击查看源代码，可以看到以下信息：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;title&gt;Fragment - Page&lt;/title&gt;

    &lt;link rel="stylesheet" type="text/css" media="all" href="/css/myapp.css"&gt;
    &lt;link rel="shortcut icon" href="/images/favicon.ico"&gt;
    &lt;script type="text/javascript" src="/js/myapp.js"&gt;&lt;/script&gt;

    &lt;link rel="stylesheet" href="/css/bootstrap.min.css"&gt;&lt;link rel="stylesheet" href="/cs/fragment.css"&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>说明 fragment.html 页面已经引入了 base.html 页面中的代码片段，fragment.html 页面中传入的 title 和 link 已经成功地插入到了 base.html 页面的代码片段中。</p>
<p>这就是片段表达式最常用的使用方式之一，也是版本 3.0 针对页面布局推出的最新语法。因为这一点，许多布局（或页面）技术在 Thymeleaf 3.0 中变得更容易使用。</p>
<h3 id="-2">页面布局</h3>
<p>按照上面这个思路很容易做页面布局，按照常用的框架模式，将页面分为头部、左侧菜单栏、尾部和中间的展示区来做个示例：</p>
<p>在 templates/layout 目录下新建 footer.html、header.html、left.html 页面，内容如下。</p>
<p>footer.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;footer&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;footer th:fragment="footer"&gt;
    &lt;h1&gt;我是 尾部&lt;/h1&gt;
&lt;/footer&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>header.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;header&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;header th:fragment="header"&gt;
    &lt;h1&gt;我是 头部&lt;/h1&gt;
&lt;/header&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>left.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;left&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;left th:fragment="left"&gt;
    &lt;h1&gt;我是 左侧&lt;/h1&gt;
&lt;/left&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>templates 目录下新建 layout.html 页面内容如下：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org" xmlns:layout="http://www.ultraq.net.nz/web/thymeleaf/layout"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Layout&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div &gt;
        &lt;div th:replace="layout/header :: header"&gt;&lt;/div&gt;
        &lt;div th:replace="layout/left :: left"&gt;&lt;/div&gt;
        &lt;div layout:fragment="content" &gt; content&lt;/div&gt;
        &lt;div th:replace="layout/footer :: footer"&gt;&lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>引入布局的语法命名空间：xmlns:layout="http://www.ultraq.net.nz/web/thymeleaf/layout"，使用 th:replace 的语法将网站的头部、尾部、左侧引入到页面中，同时定义了一个代码片段 content，可以作为后期页面正文的替换内容。</p>
<p>后端添加访问入口：</p>
<pre><code class="java language-java">@RequestMapping("/layout")
public String layout() {
    return "layout";
}
</code></pre>
<p>启动后访问地址：http://localhost:8080/layout，可以看到页面展示如下：</p>
<pre><code>我是 头部
我是 左侧
content
我是 尾部
</code></pre>
<p>可以看出 layout.html 页面已经成功地引入了页面的头部、尾部、左侧。接下来以 layout.html 作为一个页面模板，任何页面想使用此布局时，只需要替换中间的 content 模块即可，新建 home.html 来测试：</p>
<pre><code class="html language-html">&lt;html xmlns:th="http://www.thymeleaf.org"  xmlns:layout="http://www.ultraq.net.nz/web/thymeleaf/layout" layout:decorate="layout"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Home&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div layout:fragment="content" &gt;
        &lt;h2&gt;个性化的内容&lt;/h2&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<ul>
<li><code>&lt;html&gt;</code>标签中添加 layout:decorate="layout" 使用 layout.html 页面的布局。</li>
<li><code>&lt;div layout:fragment="content" &gt;</code>替换 layout.html 页面中的 content 代码片段。</li>
<li><strong>layout:decorator 标签在 3.0 过期，推荐使用新的标签 layout:decorate 进行页面布局。</strong></li>
</ul>
<p>Controller 添加访问：</p>
<pre><code class="java language-java">@RequestMapping("/home")
public String home() {
    return "home";
}
</code></pre>
<p>重启后，在浏览器中输入网址 http://localhost:8080/home，发现 home.html 页面已经采用了 layout.html 的页面布局，content 部分的内容被替换为：“个性化的内容”，展示内容如下：</p>
<pre><code>我是 头部
我是 左侧
个性化的内容
我是 尾部
</code></pre>
<p>这样其他页面如果都是类似的结构都可以采用这样的方式来使用。</p>
<p>采用页面模板布局的时候有两个关键设置：</p>
<ul>
<li>在模板页面定义需要替换的部分 layout:fragment="content"；</li>
<li>在需要引入模板的页面头部写 layout:decorate="layout""，再修改 layout:fragment="content" 中的内容。</li>
</ul>
<h3 id="-3">总结</h3>
<p>通过本课的学习发现 Thymeleaf 对代码片段重复利用、页面布局都有很好的支持，Thymeleaf 3.0 引入代码片段语法更加方便布局技术的使用。Thymeleaf 3.0 的页面布局技术，降低了后端开发人员学习页面布局的成本，使用页面布局技术后会高效地复用前端页面，减少了开发量、稳定前端页面结构。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>