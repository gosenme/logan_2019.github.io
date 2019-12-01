---
title: 精通 Spring Boot 42 讲-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一课我们介绍了 Thymeleaf 最常用的使用语法，这一课我们继续学习 Thymeleaf 高阶的使用方式，并对这些使用方式进行总结分类。其实上一课的内容，基本可以满足 Thymeleaf 80% 的使用场景，高阶用法会在某些场景下提供更高效、便捷的使用方式。</p>
<h3 id="">内联 [ [ ] ]</h3>
<p>如果不想通过 th 标签而是简单地访问 model 对象数据，或是想在 javascript 代码块里访问 model 中的数据，则要使用内联的方法。</p>
<p>内联文本：[ [...] ] 内联文本的表示方式，使用时，必须先用在 th:inline="text/javascript/none" 激活，th:inline 可以在父级标签内使用，甚至可以作为 body 的标签。内联文本比 th:text 的代码少，不利于原型显示。</p>
<p>页面 inline.html（文本内联）：</p>
<pre><code class="html language-html">&lt;div&gt;
    &lt;h1&gt;内联&lt;/h1&gt;
    &lt;div th:inline="text" &gt;
        &lt;p&gt;Hello, [[${userName}]] !&lt;/p&gt;
        &lt;br/&gt;
    &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>以上代码等价于：</p>
<pre><code class="html language-html">&lt;div&gt;
    &lt;h1&gt;不使用内联&lt;/h1&gt;
    &lt;p th:text="'Hello, ' + ${userName} + ' !'"&gt;&lt;/p&gt;
    &lt;br/&gt;
&lt;/div&gt;
</code></pre>
<p>通过以上代码可以看出使用内联语法会更简洁一些。</p>
<p>如果想在脚本中使用后端传递的值，则必须使用脚本内联，脚本内联可以在 js 中取到后台传过来的参数：</p>
<pre><code>&lt;script th:inline="javascript"&gt;
    var name = [[${userName}]] + ', Sebastian';
    alert(name);
&lt;/script&gt;
</code></pre>
<p>这段脚本的含义是在访问页面的时候，根据后端传值拼接 name 值，并以 alert 的方式弹框展示。</p>
<p>后端传值：</p>
<pre><code class="java language-java">@RequestMapping("/inline")
public String inline(ModelMap map) {
    map.addAttribute("userName", "neo");
    return "inline";
}
</code></pre>
<p>启动项目后在浏览器中输入该网址：http://localhost:8080/inline，则会出现下面的结果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/inline.png" alt="" /></p>
<p>页面会先跳出一个 alert 提示框，然后再展示使用内联和不使用内联的页面内容。</p>
<h3 id="-1">基本对象</h3>
<p>Thymeleaf 包含了一些基本对象，可以用于我们的视图中，这些基本对象使用 # 开头。</p>
<ul>
<li><code>#ctx</code>：上下文对象</li>
<li><code>#vars</code>：上下文变量</li>
<li><code>#locale</code>：区域对象</li>
<li><code>#request</code>：（仅 Web 环境可用）HttpServletRequest 对象</li>
<li><code>#response</code>：（仅 Web 环境可用）HttpServletResponse 对象</li>
<li><code>#session</code>：（仅 Web 环境可用）HttpSession 对象</li>
<li><code>#servletContext</code>：（仅 Web 环境可用）ServletContext 对象</li>
</ul>
<p>Thymeleaf 在 Web 环境中，有一系列的快捷方式用于访问请求参数、会话属性等应用属性，以其中几个常用的对象作为示例来演示。</p>
<ul>
<li><code>#request</code>：直接访问与当前请求关联的 javax.servlet.http.HttpServletRequest 对象；</li>
<li><code>#session</code>：直接访问与当前请求关联的 javax.servlet.http.HttpSession 对象。</li>
</ul>
<p>后台添加方法传值：</p>
<pre><code class="java language-java">@RequestMapping("/object")
public String object(HttpServletRequest request) {
    request.setAttribute("request","i am request");
    request.getSession().setAttribute("session","i am session");
    return "object";
}
</code></pre>
<p>使用 request 和 session 分别传递了一个值，再来查看页面 object.html。</p>
<pre><code class="html language-html">&lt;body&gt;
    &lt;div &gt;
        &lt;h1&gt;基本对象&lt;/h1&gt;
        &lt;p th:text="${#request.getAttribute('request')}"&gt;
        &lt;br/&gt;
        &lt;p th:text="${session.session}"&gt;&lt;/p&gt;
         Established locale country: &lt;span th:text="${#locale.country}"&gt;CN&lt;/span&gt;.
    &lt;/div&gt;
&lt;/body&gt;
</code></pre>
<p>启动项目后在浏览器中输入该网址：http://localhost:8080/object，则会出现下面的结果：</p>
<pre><code class="html language-html">基本对象

i am request

i am session

Established locale country: CN.
</code></pre>
<p>第一个展示了 request 如何使用参数，第二行展示了 session 的使用，session 直接使用 <code>.</code> 即可获取到 session 中的值，最后展示了 locale 的用法。</p>
<h3 id="-2">内嵌变量</h3>
<p>为了模板更加易用，Thymeleaf 还提供了一系列 Utility 对象（内置于 Context 中），可以通过 # 直接访问。</p>
<ul>
<li>dates：java.util.Date 的功能方法类</li>
<li>calendars：类似 #dates，面向 java.util.Calendar</li>
<li>numbers：格式化数字的功能方法类</li>
<li>strings：字符串对象的功能类，contains、startWiths、prepending/appending 等</li>
<li>objects：对 objects 的功能类操作</li>
<li>bools：对布尔值求值的功能方法</li>
<li>arrays：对数组的功能类方法</li>
<li>lists：对 lists 的功能类方法</li>
<li>sets：set 的实用方法</li>
<li>maps：map 的实用方法</li>
<li>…</li>
</ul>
<p>下面用一段代码来举例说明一些常用的方法，页面是 utility.html。</p>
<p><strong>1. dates</strong></p>
<p>可以使用 dates 对日期格式化，创建当前时间等操作。</p>
<pre><code class="html language-html">&lt;!--格式化时间--&gt;
&lt;p th:text="${#dates.format(date, 'yyyy-MM-dd HH:mm:ss')}"&gt;neo&lt;/p&gt;
&lt;!--创建当前时间 精确到天--&gt;
&lt;p th:text="${#dates.createToday()}"&gt;neo&lt;/p&gt;
&lt;!--创建当前时间 精确到秒--&gt;
&lt;p th:text="${#dates.createNow()}"&gt;neo&lt;/p&gt;
</code></pre>
<p><strong>2. strings</strong></p>
<p>strings 内置了一些对字符串经常使用的函数。</p>
<pre><code class="html language-html">&lt;!--判断是否为空--&gt;
&lt;p th:text="${#strings.isEmpty(userName)}"&gt;userName&lt;/p&gt;
&lt;!--判断 list 是否为空--&gt;
&lt;p th:text="${#strings.listIsEmpty(users)}"&gt;userName&lt;/p&gt;
&lt;!--输出字符串长度--&gt;
&lt;p th:text="${#strings.length(userName)}"&gt;userName&lt;/p&gt;
&lt;!--拼接字符串--&gt;
&lt;p th:text="${#strings.concat(userName,userName,userName)}"&gt;&lt;/p&gt;
&lt;!--创建自定长度的字符串--&gt;
&lt;p th:text="${#strings.randomAlphanumeric(count)}"&gt;userName&lt;/p&gt;
</code></pre>
<p>后端传值：</p>
<pre><code class="java language-java">@RequestMapping("/utility")
public String utility(ModelMap map) {
    map.addAttribute("userName", "neo");
    map.addAttribute("users", getUserList());
    map.addAttribute("count", 12);
    map.addAttribute("date", new Date());
    return "utility";
}
</code></pre>
<p>启动项目后在浏览器中输入该网址：http://localhost:8080/utility，则会出现下面的结果：</p>
<pre><code>内嵌变量

2018-09-26 20:49:07

Wed Sep 26 00:00:00 CST 2018

Wed Sep 26 20:49:07 CST 2018

false

[false, false, false]

3

neoneoneo

QKERBVPRHFS9
</code></pre>
<p>接下来总结一下 Thymeleaf 表达式。</p>
<h3 id="-3">表达式</h3>
<p>表达式共分为以下五类。</p>
<ul>
<li>变量表达式：${...}</li>
<li>选择或星号表达式：*{...}</li>
<li>文字国际化表达式：#{...}</li>
<li>URL 表达式：@{...}</li>
<li>片段表达式：~{...}</li>
</ul>
<h4 id="-4">变量表达式</h4>
<p>变量表达式即 OGNL 表达式或 Spring EL 表达式（在 Spring 术语中也叫 model attributes），类似 <code>${session.user.name}</code>。</p>
<p>它们将以 HTML 标签的一个属性来表示：  </p>
<pre><code class="html language-html">&lt;span th:text="${book.author.name}"&gt;  
&lt;li th:each="book : ${books}"&gt;  
</code></pre>
<h4 id="-5">选择（星号）表达式</h4>
<p>选择表达式很像变量表达式，不过它们用一个预先选择的对象来代替上下文变量容器（map）来执行，类似：<code>*{customer.name}</code>。</p>
<p>被指定的 object 由 th:object 属性定义：</p>
<pre><code class="html language-html">&lt;div th:object="${book}"&gt;  
  ...  
  &lt;span th:text="*{title}"&gt;...&lt;/span&gt;  
  ...  
&lt;/div&gt;  
</code></pre>
<p>title 即为 book 的属性。</p>
<h4 id="-6">文字国际化表达式</h4>
<p>文字国际化表达式允许我们从一个外部文件获取区域文字信息（.properties），用 Key 索引 Value，还可以提供一组参数（可选）。</p>
<pre><code class="html language-html">#{main.title}  
#{message.entrycreated(${entryId})}  
</code></pre>
<p>可以在模板文件中找到这样的表达式代码：</p>
<pre><code class="html language-html">&lt;table&gt;  
  ...  
  &lt;th th:text="#{header.address.city}"&gt;...&lt;/th&gt;  
  &lt;th th:text="#{header.address.country}"&gt;...&lt;/th&gt;  
  ...  
&lt;/table&gt;  
</code></pre>
<h4 id="url">URL 表达式</h4>
<p>URL 表达式指的是把一个有用的上下文或回话信息添加到 URL，这个过程经常被叫做 URL 重写，比如<code>@{/order/list}</code>。</p>
<ul>
<li>URL 还可以设置参数：<code>@{/order/details(id=${orderId})}</code></li>
<li>相对路径：<code>@{../documents/report}</code></li>
</ul>
<p>让我们看这些表达式：</p>
<pre><code class="html language-html">&lt;form th:action="@{/createOrder}"&gt;  
&lt;a href="main.html" th:href="@{/main}"&gt;
</code></pre>
<h4 id="-7">片段表达式</h4>
<p>片段表达式是 3.x 版本新增的内容。片段表达式是一种标记的片段，并将其移动到模板中的方法。片段表达式的优势是，片段可以被复制或者作为参数传递给其他模板等。</p>
<p>最常见的用法是使用 th:insert 或 th:replace: 插入片段：</p>
<pre><code class="html language-html">&lt;div th:insert="~{commons :: main}"&gt;...&lt;/div&gt;
</code></pre>
<p>也可以在页面的其他位置去使用：</p>
<pre><code class="html language-html">&lt;div th:with="frag=~{footer :: #main/text()}"&gt;
  &lt;p th:insert="${frag}"&gt;
&lt;/div&gt;
</code></pre>
<p>片段表达式可以有参数。</p>
<h4 id="-8">变量表达式和星号表达有什么区别</h4>
<p>如果不考虑上下文的情况下，两者没有区别；星号语法是在选定对象上表达，而不是整个上下文。什么是选定对象？就是父标签的值，如下：</p>
<pre><code class="html language-html">&lt;div th:object="${session.user}"&gt;
&lt;p&gt;Name: &lt;span th:text="*{firstName}"&gt;Sebastian&lt;/span&gt;.&lt;/p&gt;
&lt;p&gt;Surname: &lt;span th:text="*{lastName}"&gt;Pepper&lt;/span&gt;.&lt;/p&gt;
&lt;p&gt;Nationality: &lt;span th:text="*{nationality}"&gt;Saturn&lt;/span&gt;.&lt;/p&gt;
&lt;/div&gt;
</code></pre>
<p>这是完全等价于：</p>
<pre><code class="html language-html">&lt;div th:object="${session.user}"&gt;
  &lt;p&gt;Name: &lt;span th:text="${session.user.firstName}"&gt;Sebastian&lt;/span&gt;.&lt;/p&gt;
  &lt;p&gt;Surname: &lt;span th:text="${session.user.lastName}"&gt;Pepper&lt;/span&gt;.&lt;/p&gt;
  &lt;p&gt;Nationality: &lt;span th:text="${session.user.nationality}"&gt;Saturn&lt;/span&gt;.&lt;/p&gt;
&lt;/div&gt;
</code></pre>
<p>当然，两种语法可以混合使用：</p>
<pre><code class="html language-html">&lt;div th:object="${session.user}"&gt;
  &lt;p&gt;Name: &lt;span th:text="*{firstName}"&gt;Sebastian&lt;/span&gt;.&lt;/p&gt;
      &lt;p&gt;Surname: &lt;span th:text="${session.user.lastName}"&gt;Pepper&lt;/span&gt;.&lt;/p&gt;
  &lt;p&gt;Nationality: &lt;span th:text="*{nationality}"&gt;Saturn&lt;/span&gt;.&lt;/p&gt;
&lt;/div&gt;
</code></pre>
<h4 id="-9">表达式支持的语法</h4>
<h5 id="literals"><strong>字面（Literals）</strong></h5>
<ul>
<li>文本文字（Text literals）：<code>'one text', 'Another one!',…</code></li>
<li>数字文本（Number literals）：<code>0, 34, 3.0, 12.3,…</code></li>
<li>布尔文本（Boolean literals）：<code>true, false</code></li>
<li>空（Null literal）：<code>null</code></li>
<li>文字标记（Literal tokens）：<code>one, sometext, main,…</code></li>
</ul>
<h5 id="textoperations"><strong>文本操作（Text operations）</strong></h5>
<ul>
<li>字符串连接（String concatenation）：<code>+</code></li>
<li>文本替换（Literal substitutions）：<code>|The name is ${name}|</code></li>
</ul>
<h5 id="arithmeticoperations"><strong>算术运算（Arithmetic operations）</strong></h5>
<ul>
<li>二元运算符（Binary operators）：<code>+, -, *, /, %</code></li>
<li>减号（单目运算符）Minus sign（unary operator）：<code>-</code></li>
</ul>
<h5 id="booleanoperations"><strong>布尔操作（Boolean operations）</strong></h5>
<ul>
<li>二元运算符（Binary operators）：<code>and, or</code></li>
<li>布尔否定（一元运算符）Boolean negation (unary operator)：<code>!, not</code></li>
</ul>
<h5 id="comparisonsandequality"><strong>比较和等价（Comparisons and equality）</strong></h5>
<ul>
<li>比较（Comparators）：<code>&gt;, &lt;, &gt;=, &lt;= (gt, lt, ge, le)</code></li>
<li>等值运算符（Equality operators）：<code>==, != (eq, ne)</code></li>
</ul>
<h5 id="conditionaloperators"><strong>条件运算符（Conditional operators）</strong></h5>
<ul>
<li>If-then：<code>(if) ? (then)</code></li>
<li>If-then-else：<code>(if) ? (then) : (else)</code></li>
<li>Default: (value) ?：<code>(defaultvalue)</code></li>
</ul>
<p>所有这些特征可以被组合并嵌套：</p>
<pre><code class="html language-html">'User is of type ' + (${user.isAdmin()} ? 'Administrator' : (${user.type} ?: 'Unknown'))
</code></pre>
<h3 id="th">常用 th 标签</h3>
<p>页面常用的 HTML 标签几乎都有 Thymeleaf 对应的 th 标签。</p>
<table>
<thead>
<tr>
<th>关键字</th>
<th>功能介绍</th>
<th>案例</th>
</tr>
</thead>
<tbody>
<tr>
<td>th:id</td>
<td>替换 id</td>
<td><code>&lt;input th:id="'xxx' + ${collect.id}"/&gt;</code></td>
</tr>
<tr>
<td>th:text</td>
<td>文本替换</td>
<td><code>&lt;p  th:text="${collect.description}"&gt;description&lt;/p&gt;</code></td>
</tr>
<tr>
<td>th:utext</td>
<td>支持 html 的文本替换</td>
<td><code>&lt;p  th:utext="${htmlcontent}"&gt;conten&lt;/p&gt;</code></td>
</tr>
<tr>
<td>th:object</td>
<td>替换对象</td>
<td><code>&lt;div th:object="${session.user}"&gt;</code></td>
</tr>
<tr>
<td>th:value</td>
<td>属性赋值</td>
<td><code>&lt;input th:value="${user.name}" /&gt;</code></td>
</tr>
<tr>
<td>th:with</td>
<td>变量赋值运算</td>
<td><code>&lt;div th:with="isEven=${prodStat.count}%2==0"&gt;&lt;/div&gt;</code></td>
</tr>
<tr>
<td>th:style</td>
<td>设置样式</td>
<td><code>th:style="'display:' + @{(${sitrue} ? 'none' : 'inline-block')} + ''"</code></td>
</tr>
<tr>
<td>th:onclick</td>
<td>点击事件</td>
<td><code>th:onclick="'getCollect()'"</code></td>
</tr>
<tr>
<td>th:each</td>
<td>属性赋值</td>
<td><code>tr th:each="user,userStat:${users}"&gt;</code></td>
</tr>
<tr>
<td>th:if</td>
<td>判断条件</td>
<td><code>&lt;a th:if="${userId == collect.userId}" &gt;</code></td>
</tr>
<tr>
<td>th:unless</td>
<td>和 th:if 判断相反</td>
<td><code>&lt;a th:href="@{/login}" th:unless=${session.user != null}&gt;Login&lt;/a&gt;</code></td>
</tr>
<tr>
<td>th:href</td>
<td>链接地址</td>
<td><code>&lt;a th:href="@{/login}" th:unless=${session.user != null}&gt;Login&lt;/a&gt; /&gt;</code></td>
</tr>
<tr>
<td>th:switch</td>
<td>多路选择 配合 th:case 使用</td>
<td><code>&lt;div th:switch="${user.role}"&gt;</code></td>
</tr>
<tr>
<td>th:case</td>
<td>th:switch 的一个分支</td>
<td><code>&lt;p th:case="'admin'"&gt;User is an administrator&lt;/p&gt;</code></td>
</tr>
<tr>
<td>th:fragment</td>
<td>布局标签，定义一个代码片段，方便其他地方引用</td>
<td><code>&lt;div th:fragment="alert"&gt;</code></td>
</tr>
<tr>
<td>th:include</td>
<td>布局标签，替换内容到引入的文件</td>
<td><code>&lt;head th:include="layout :: htmlhead" th:with="title='xx'"&gt;&lt;/head&gt; /&gt;</code></td>
</tr>
<tr>
<td>th:replace</td>
<td>布局标签，替换整个标签到引入的文件</td>
<td><code>&lt;div th:replace="fragments/header :: title"&gt;&lt;/div&gt;</code></td>
</tr>
<tr>
<td>th:selected</td>
<td>selected 选择框 选中</td>
<td><code>th:selected="(${xxx.id} == ${configObj.dd})"</code></td>
</tr>
<tr>
<td>th:src</td>
<td>图片类地址引入</td>
<td><code>&lt;img class="img-responsive" alt="App Logo" th:src="@{/img/logo.png}" /&gt;</code></td>
</tr>
<tr>
<td>th:inline</td>
<td>定义 js 脚本可以使用变量</td>
<td><code>&lt;script type="text/javascript" th:inline="javascript"&gt;</code></td>
</tr>
<tr>
<td>th:action</td>
<td>表单提交的地址</td>
<td><code>&lt;form action="subscribe.html" th:action="@{/subscribe}"&gt;</code></td>
</tr>
<tr>
<td>th:remove</td>
<td>删除某个属性</td>
<td><code>&lt;tr th:remove="all"&gt;</code><br>1.all：删除包含标签和所有的子节点；<br>2.body：不包含标记删除，但删除其所有的子节点；<br>3.tag：包含标记的删除，但不删除它的子节点；<br>4.all-but-first：删除所有包含标签的子节点，除了第一个。<br>5.none：什么也不做。这个值是有用的动态评估</td>
</tr>
<tr>
<td>th:attr</td>
<td>设置标签属性，多个属性可以用逗号分隔</td>
<td>比如 th:attr="src=@{/image/aa.jpg},title=#{logo}"，此标签不太优雅，一般用的比较少</td>
</tr>
</tbody>
</table>
<p>还有非常多的标签，这里只列出最常用的几个，由于一个标签内可以包含多个 th:x 属性，其生效的优先级顺序为：</p>
<pre><code>include,each,if/unless/switch/case,with,attr/attrprepend/attrappend,value/href,src ,etc,text/utext,fragment,remove。
</code></pre>
<h3 id="thymeleaf">Thymeleaf 配置</h3>
<p>我们可以通过 application.properties 文件灵活的配置 Thymeleaf 的各项特性，以下为 Thymeleaf 的配置和默认参数：</p>
<pre><code># THYMELEAF (ThymeleafAutoConfiguration)
#开启模板缓存（默认值：true）
spring.thymeleaf.cache=true 
#检查模板是否存在，然后再呈现
spring.thymeleaf.check-template=true 
#检查模板位置是否正确（默认值:true）
spring.thymeleaf.check-template-location=true
#Content-Type的值（默认值：text/html）
spring.thymeleaf.content-type=text/html
#开启MVC Thymeleaf视图解析（默认值：true）
spring.thymeleaf.enabled=true
#模板编码
spring.thymeleaf.encoding=UTF-8
#要被排除在解析之外的视图名称列表，用逗号分隔
spring.thymeleaf.excluded-view-names=
#要运用于模板之上的模板模式。另见StandardTemplate-ModeHandlers(默认值：HTML5)
spring.thymeleaf.mode=HTML5
#在构建URL时添加到视图名称前的前缀（默认值：classpath:/templates/）
spring.thymeleaf.prefix=classpath:/templates/
#在构建URL时添加到视图名称后的后缀（默认值：.html）
spring.thymeleaf.suffix=.html
#Thymeleaf 模板解析器在解析器链中的顺序，默认情况下，它排第一位，顺序从1开始，只有在定义了额外的 TemplateResolver Bean 时才需要设置这个属性。
spring.thymeleaf.template-resolver-order=
#可解析的视图名称列表，用逗号分隔
spring.thymeleaf.view-names=
</code></pre>
<p>在实际项目中可以根据实际使用情况来修改。</p>
<h3 id="-10">总结</h3>
<p>Thymeleaf 的使用方式非常灵活，可以结合 JS 来获取后端传递的值，Thymeleaf 本身也内嵌了很多对象和函数方便我们在页面来直接调用。Thymeleaf 通过不同的表达式来灵活的控制页面结构和内容，配合着 Spring Boot 的使用，Thymeleaf 可以通过多项参考来控制其特性。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>