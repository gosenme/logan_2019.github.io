---
title: 案例上手 Spring 全家桶-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上一讲介绍了 EL 表达式的使用，可以简化 JSP 页面的代码开发，但实际上 EL 表达式也有自己的缺陷，只能做展示，不能编写动态功能，比如集合的遍历，为了解决这一问题，JSP 提供了 JSTL 组件供开发者使用，因此通常情况下 JSP 页面的开发为 EL + JSTL，这一讲我们就来详细学习 JSTL 的使用。</p>
<h3 id="jstl">什么是 JSTL</h3>
<p>JSP Standard Tag Library，简称 JSTL，JSP 标准标签库，提供了一系列的标签供开发者在 JSP 页面中使用，编写各种动态功能。</p>
<h3 id="jstl-1">常用 JSTL 标签库</h3>
<p>JSTL 提供了很多标签，以库为单位进行分类，实际开发中最常用的标签库有 3 种。</p>
<ul>
<li>核心标签库</li>
<li>格式化标签库</li>
<li>函数标签库</li>
</ul>
<h3 id="jstl-2">如何使用 JSTL</h3>
<p>（1）pom.xml 添加 JSTL 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;jstl&lt;/groupId&gt;
    &lt;artifactId&gt;jstl&lt;/artifactId&gt;
    &lt;version&gt;1.2&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>（2）JSP 页面导入 JSTL 标签库，prefix 设置前缀，相当于别名，在 JSP 页面中可以直接通过别名使用标签，uri 设置对应的标签库。</p>
<pre><code class="jsp language-jsp">&lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;
</code></pre>
<p>（3）使用标签完成功能。</p>
<h3 id="-1">核心标签库</h3>
<p>引入核心标签库。</p>
<pre><code class="jsp language-jsp">&lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;
</code></pre>
<p>set：向域对象中添加一个数据。</p>
<p>var 为变量名，value 为变量值，scope 为保存的域对象，默认为 pageContext。</p>
<pre><code class="jsp language-jsp">&lt;c:set var="message" value="张三" scope="request"/&gt;
${requestScope.message }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/cb1925c0-9ad3-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>修改对象的属性值。</p>
<p>property 为属性名，value 为属性值，target 为对象名，注意这里需要使用 EL 表达式。</p>
<pre><code class="jsp language-jsp">&lt;%
    Reader reader = new Reader();
    request.setAttribute("reader", reader);
 %&gt;
 &lt;c:set value="张三" property="name" target="${reader}"&gt;&lt;/c:set&gt;
 &lt;c:set value="1" property="id" target="${reader}"&gt;&lt;/c:set&gt;
 ${reader }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/d9aada70-9ad3-11e8-a178-519d5b470954" width = "50%" /></p>
<p>out：输出域对象中的数据。</p>
<p>value 为变量名，default 的作用是若变量不存在，则输出 default 的值。</p>
<pre><code class="jsp language-jsp">&lt;c:set var="message" value="张三" scope="request"/&gt;
&lt;c:out value="${message }" default="未定义"&gt;&lt;/c:out&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/e60563d0-9ad3-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<pre><code class="jsp language-jsp">&lt;c:out value="${message }" default="未定义"&gt;&lt;/c:out&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/f3e04ba0-9ad3-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>remove：删除域对象中的数据。</p>
<p>var 为要删除的变量名。</p>
<pre><code class="jsp language-jsp">&lt;c:set var="info" value="Java"&gt;&lt;/c:set&gt;
&lt;c:remove var="info"/&gt;
&lt;c:out value="${info }" default="未定义"/&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/07da6e60-9ad4-11e8-831e-0180aea56660" width = "50%" /></p>
<p>catch：捕获异常。</p>
<p>若 JSP 的 Java 脚本抛出异常，会直接将异常信息打印到浏览器。</p>
<pre><code class="jsp language-jsp">&lt;%
   int num = 10/0;
%&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/1d8611b0-9ad4-11e8-a178-519d5b470954" width = "80%" /></p>
<p>使用 catch 可以将异常信息保存到域对象中。</p>
<pre><code class="jsp language-jsp">&lt;c:catch var="error"&gt;
&lt;%
    int num = 10/0;
%&gt;
&lt;/c:catch&gt;
&lt;c:out value="${error }"&gt;&lt;/c:out&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/30052d30-9ad4-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<p>if ：流程控制。</p>
<p>test 为判断条件，如果条件成立，会输出标签内部的内容，否则不输出。</p>
<pre><code class="jsp language-jsp">&lt;c:set value="1" var="num1"&gt;&lt;/c:set&gt;
&lt;c:set value="2" var="num2"&gt;&lt;/c:set&gt;
&lt;c:if test="${num1&gt;num2}"&gt;${num1 } &gt; ${num2 }&lt;/c:if&gt;
&lt;c:if test="${num1&lt;num2}"&gt;${num1 } &lt; ${num2 }&lt;/c:if&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/46d0e680-9ad4-11e8-831e-0180aea56660" width = "50%" /></p>
<p>choose：流程控制。</p>
<p>相当于 if-else 的用法，when 相当于 if，otherwise 相当于 else。</p>
<pre><code class="jsp language-jsp">&lt;c:set value="1" var="num1"&gt;&lt;/c:set&gt;
&lt;c:set value="2" var="num2"&gt;&lt;/c:set&gt;
&lt;c:choose&gt;
     &lt;c:when test="${num1&gt;num2}"&gt;${num1 }&lt;/c:when&gt;
     &lt;c:otherwise&gt;${num2 } &lt;/c:otherwise&gt;   
&lt;/c:choose&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/5e8cf340-9ad4-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>forEach：迭代集合。</p>
<pre><code class="jsp language-jsp">&lt;%
   Reader reader1 = new Reader();
   reader1.setId(1);
   reader1.setName("张三");
   Reader reader2 = new Reader();
   reader2.setId(2);
   reader2.setName("李四");
   Reader reader3 = new Reader();
   reader3.setId(3);
   reader3.setName("王五");
   List&lt;Reader&gt; list = new ArrayList&lt;Reader&gt;();
   list.add(reader1);
   list.add(reader2);
   list.add(reader3);
   request.setAttribute("list", list);
   Map&lt;Integer,Reader&gt; map = new HashMap&lt;Integer,Reader&gt;();
   map.put(1, reader1);
   map.put(2, reader2);
   map.put(3, reader3);
   request.setAttribute("map", map);
   Set&lt;Reader&gt; set = new HashSet&lt;Reader&gt;();
   set.add(reader1);
   set.add(reader2);
   set.add(reader3);
   request.setAttribute("set", set);
%&gt;
&lt;c:forEach items="${list }" var="reader"&gt;
     ${reader }&lt;br/&gt;
&lt;/c:forEach&gt;
&lt;hr/&gt;
&lt;c:forEach items="${map }" var="reader"&gt;
       ${reader }&lt;br/&gt;
&lt;/c:forEach&gt;
&lt;hr/&gt;
&lt;c:forEach items="${set}" var="reader"&gt;
       ${reader }&lt;br/&gt;
&lt;/c:forEach&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/9530aea0-9ad4-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<h3 id="-2">格式化标签库</h3>
<p>可以将日期和数字按照一定的格式进行格式化输出。</p>
<p>引入格式化标签库：</p>
<pre><code class="jsp language-jsp">&lt;%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %&gt;
</code></pre>
<p>日期格式化：</p>
<pre><code class="jsp language-jsp">&lt;%
   pageContext.setAttribute("date", new Date());
%&gt;
&lt;c:out value="${date }"&gt;&lt;/c:out&gt;&lt;br/&gt;
&lt;fmt:formatDate value="${date }"/&gt;&lt;br/&gt;
&lt;fmt:formatDate value="${date }" pattern="yyyy-MM-dd hh:mm:ss" /&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/b35d98c0-9ad4-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>数字格式化：</p>
<p>value 为数值，maxIntegerDigits 为整数位，maxFractionDigits 为小数位。</p>
<pre><code class="jsp language-jsp">&lt;fmt:formatNumber value="32165.23434" maxIntegerDigits="2" maxFractionDigits="3"&gt;&lt;/fmt:formatNumber&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/be8ee460-9ad4-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<h3 id="-3">函数标签库</h3>
<p>引入函数标签库。</p>
<pre><code class="jsp language-jsp">&lt;%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %&gt;
</code></pre>
<p>函数标签库的使用与其他标签稍有区别，类似与 EL 表达式。</p>
<pre><code class="jsp language-jsp">&lt;%
   pageContext.setAttribute("info", "Java,C");
%&gt;
判断是否包含"Ja"：${fn:contains(info,"Java") }&lt;br/&gt;
判断是否以"Ja"开始：${fn:startsWith(info,"Ja") }&lt;br/&gt;
判断是否以"C"结尾：${fn:endsWith(info,"C") }&lt;br/&gt;
求"va"的下标：${fn:indexOf(info,"va") }&lt;br/&gt;
"Java"替换为"JavaScript"：${fn:replace(info,"Java","JavaScript") }&lt;br/&gt;
截取：${fn:substring(info,2,3) }&lt;br/&gt;
以","分割：${fn:split(info,",")[1] }
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/d6262b10-9ad4-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="-4">总结</h3>
<p>本节课我们讲解了 JSTL（JSP Standard Tag Library，JSP 标准标签库），它和 EL 表达式一样也是作用于视图层的组件，通常情况下两个组件会配合起来使用，JSTL 负责完成模式数据的逻辑处理，如遍历集合、判断等，EL 只负责展示结果，二者相结合的方式可以大大简化 JSP 的代码开发。</p>
<h3 id="-5">分享交流</h3>
<p>我们为本课程付费读者创建了微信交流群，以方便更有针对性地讨论课程相关问题。入群方式请添加小助手的微信号：GitChatty5，并注明「全家桶」。</p>
<p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手微信后需要截已购买的图来验证~</p>
</blockquote></div></article>