---
title: 案例上手 Spring 全家桶-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本讲我们一起来学习 Expression Language（EL） 表达式的使用，在 Java Web 开发中，如果使用 JSP 作为视图层技术，那么 EL 表达式就是必须要用到的技术，是每一个 Java 开发者都必须掌握的技能。</p>
<h3 id="el">什么是 EL 表达式</h3>
<p>Expression Language，表达式语言。使用 EL 表达式可以替代 JSP 页面中获取业务数据的复杂代码，让开发变得更加简单， JSP 的结构也更加清晰简洁。</p>
<h3 id="el-1">如何使用 EL 表达式</h3>
<p>基本语法：\${expression}，如果不使用 EL 表达式，JSP 页面获取后台传来的数据，需要通过 Java 脚本的方式获取，如下所示。</p>
<pre><code class="jsp language-jsp">&lt;%
    String message = (String)request.getAttribute("message");
%&gt;
&lt;%=message %&gt;
</code></pre>
<p>使用 EL 表达式之后，可大大简化这种繁琐的开发方式，让 JSP 页面更加简洁。</p>
<pre><code class="jsp language-jsp">${message }
</code></pre>
<p>\${message} 中的 message 对应域对象中数据的 key 值，那么问题来了，域对象有 4 种，如果每一个域对象中都存放一个 key=message 的数据，那么 EL 表达式取的是哪个呢？我们通过一段示例代码来寻找答案。</p>
<pre><code class="jsp language-jsp">&lt;%
    pageContext.setAttribute("message", "page");
    request.setAttribute("message", "request");
    session.setAttribute("message", "session");
    application.setAttribute("message", "application");
%&gt;
${message }
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/d9b8b290-9ad2-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>可以看到取的是 pageContext 中的数据，EL 表达式默认取数据的方式是根据 pageContext→request→session→application 的顺序进行，如果在某个域对象中获取了数据，则返回，不再继续查找，如果没有找到，继续来到下一个域对象中查找，直到遍历完 4 个域对象。</p>
<p>我们也可以指定 EL 在某个特定的域对象中查找，只需要在 EL 表达式中添加前缀即可：pageScope、requestScope、sessionScope、applicationScope，分别对于 page 作用域、request 作用域、session 作用域、application作用域。</p>
<p>比如，指定 EL 在 request 中查找。</p>
<pre><code>&lt;%
    pageContext.setAttribute("message", "page");
    request.setAttribute("message", "request");
    session.setAttribute("message", "session");
    application.setAttribute("message", "application");
%&gt;
${requestScope.message }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/f5be4fe0-9ad2-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="el-2">使用 EL 表达式获取对象的属性值</h3>
<p>EL 表达式可以直接通过属性名取出对应的值，底层实际在调用 getter 方法。</p>
<pre><code class="jsp language-jsp">&lt;%
    Reader reader = new Reader();
    reader.setId(1);
    reader.setName("张三");
    request.setAttribute("reader", reader);
%&gt;
${reader.id }--${reader.name }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/0713b870-9ad3-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="el-3">EL 表达式获取集合</h3>
<pre><code>&lt;%
    Reader reader = new Reader();
    reader.setId(1);
    reader.setName("张三");
    Reader reader2 = new Reader();
    reader2.setId(2);
    reader2.setName("李四");
    Reader reader3 = new Reader();
    reader3.setId(3);
    reader3.setName("王五");
    List&lt;Reader&gt; list = new ArrayList&lt;Reader&gt;();
    list.add(reader);
    list.add(reader2);
    list.add(reader3);
    request.setAttribute("list", list);
%&gt;
${list[0].id }--${list[0].name }&lt;br/&gt;
${list[1].id }--${list[1].name }&lt;br/&gt;
${list[2].id }--${list[2].name }&lt;br/&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/18ff4680-9ad3-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<h3 id="el-4">EL 表达式支持关系运算符和逻辑运算符</h3>
<p>运算符可以使用转义字符来表示：</p>
<pre><code>&amp;&amp;：and
||：or
!：not
==：eq
!=：ne
&lt;：lt
&gt;：gt
&lt;=：le
&gt;=：ge
</code></pre>
<pre><code class="jsp language-jsp">&lt;%
    request.setAttribute("num1", 8);
    request.setAttribute("num2", 9);
    request.setAttribute("num3", 9);
%&gt;
${ num1 &lt; num2 }&lt;br/&gt;
${ num1 lt num2 }&lt;br/&gt;
${ num1 &gt; num2 }&lt;br/&gt;
${ num1 gt num2 }&lt;br/&gt;
${ num2 == num3 }&lt;br/&gt;
${ num2 eq num3 }&lt;br/&gt;
${ num1 &lt; num2 &amp;&amp; num1 &gt; num2 }&lt;br/&gt;
${ num1 &lt; num2 and num1 &gt; num2 }&lt;br/&gt;
${ num1 &lt; num2 || num1 &gt; num2 }&lt;br/&gt;
${ num1 &lt; num2 or num1 &gt; num2 }&lt;br/&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/4249cd30-9ad3-11e8-831e-0180aea56660" width = "50%" /></p>
<h3 id="empty">关键字 empty 判断变量是否为空</h3>
<p>null，长度为零的 String，size 为 0 的集合都会认为是空。</p>
<pre><code class="jsp language-jsp">&lt;%
    Integer num = null; 
    String str = "";
    List&lt;String&gt; list = new ArrayList&lt;String&gt;();
    request.setAttribute("num", num);
    request.setAttribute("str", str);
    request.setAttribute("list", list);
%&gt;
${ empty num }&lt;br/&gt;
${ empty str }&lt;br/&gt;
${ empty list }&lt;br/&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/55c6f7c0-9ad3-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<h3 id="elhttp">EL 访问 HTTP 请求参数对象</h3>
<p>添加 param 前缀即可。</p>
<pre><code class="jsp language-jsp">${param.id }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/64de0910-9ad3-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<p>如果是多个参数，通过 paramValues 来获取。</p>
<pre><code class="jsp language-jsp">${paramValues.id[0] }&lt;br/&gt;
${paramValues.id[1] }&lt;br/&gt;
${paramValues.id[2] }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/77d4eca0-9ad3-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<h3 id="elpagecontext">EL 访问 pageContext 对象</h3>
<pre><code class="jsp language-jsp">${pageContext.servletConfig.servletName}&lt;br/&gt;
${pageContext.servletContext.contextPath}&lt;br/&gt;
${pageContext.request}
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/88b1c9d0-9ad3-11e8-b37c-dd4feba3837e" width = "60%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 EL 表达式：Expression Language（表达式语言），它的作用是替代 JSP 页面中数据访问时的复杂编码，简化开发，让 JSP 代码更加简洁，同时语法非常简单，是应用在视图层的组件。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>