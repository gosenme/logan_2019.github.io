---
title: 精通 Spring Boot 42 讲-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">模板引擎</h3>
<p>模板引擎是为了使用户界面与业务数据（内容）分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎就会生成一个标准的 HTML 文档。</p>
<p>模板引擎的实现方式有很多，最简单的是“置换型”模板引擎，这类模板引擎只是将指定模板内容（字符串）中的特定标记（子字符串）替换，便生成了最终需要的业务数据（如网页）。</p>
<p>“置换型”模板引擎实现简单，但其效率低下，无法满足高负载的应用需求（比如有海量访问的网站），因此还出现了“解释型”模板引擎和“编译型”模板引擎等。</p>
<h3 id="thymeleaf">Thymeleaf 介绍</h3>
<p>Thymeleaf 是⾯向 Web 和独⽴环境的现代服务器端 Java 模板引擎，能够处理 HTML、XML、JavaScript、CSS 甚⾄纯⽂本。</p>
<p>Thymeleaf 旨在提供⼀个优雅的、⾼度可维护的创建模板的⽅式。为了实现这⼀⽬标，Thymeleaf 建⽴在⾃然模板的概念上，将其逻辑注⼊到模板⽂件中，不会影响模板设计原型，从而改善了设计的沟通，弥合了设计和开发团队之间的差距。</p>
<p>Thymeleaf 从设计之初就遵循 Web 标准——特别是 HTML 5 标准，如果需要，Thymeleaf 允许创建完全符合 HTML 5 验证标准的模板。</p>
<p>Spring Boot 体系内推荐使用 Thymeleaf 作为前端页面模板，并且 Spring Boot 2.0 中默认使用 Thymeleaf 3.0，性能提升幅度很大。</p>
<h4 id="thymeleaf-1">Thymeleaf 特点</h4>
<p>简单说，Thymeleaf 是一个跟 Velocity、FreeMarker 类似的模板引擎，它可以完全替代 JSP。与其他的模板引擎相比较，它有如下三个极吸引人的特点。</p>
<ul>
<li><p>Thymeleaf 在有网络和无网络的环境下皆可运行，即它可以让美工在浏览器查看页面的静态效果，也可以让程序员在服务器查看带数据的动态页面效果。这是由于它支持 HTML 原型，然后在 HTML 标签里增加额外的属性来达到模板 + 数据的展示方式。浏览器解释 HTML 时会忽略未定义的标签属性，所以 Thymeleaf 的模板可以静态地运行；当有数据返回到页面时，Thymeleaf 标签会动态地替换掉静态内容，使页面动态显示。</p></li>
<li><p>Thymeleaf 开箱即用的特性。它支持标准方言和 Spring 方言，可以直接套用模板实现 JSTL、 OGNL 表达式效果，避免每天套模板、改 JSTL、改标签的困扰。同时开发人员也可以扩展和创建自定义的方言。</p></li>
<li><p>Thymeleaf 提供 Spring 标准方言和一个与 SpringMVC 完美集成的可选模块，可以快速地实现表单绑定、属性编辑器、国际化等功能。</p></li>
</ul>
<p><strong>对比</strong></p>
<p>我们可以对比一下 Thymeleaf 和常用的模板引擎：Velocity、Freemaker，和其他模板一起不同的是，它使用了自然的模板技术。这意味着 Thymeleaf 的模板语法并不会破坏文档的结构，模板依旧是有效的 XML 文档。模板还可以用做工作原型，Thymeleaf 会在运行期替换掉静态值。Velocity 与 FreeMarker 则是连续的文本处理器。</p>
<p>下面的代码示例分别使用 Velocity、FreeMarker 与 Thymeleaf 打印出一条消息：</p>
<pre><code class="xml language-xml">Velocity: &lt;p&gt;$message&lt;/p&gt;
FreeMarker: &lt;p&gt;${message}&lt;/p&gt;
Thymeleaf: &lt;p th:text="${message}"&gt;Hello World!&lt;/p&gt;
</code></pre>
<p>上面我们可以看出来 Thymeleaf 的作用域在 HTML 标签内，类似标签的一个属性来使用，这就是它的特点。</p>
<p><strong>注意，由于 Thymeleaf 使用了 XML DOM 解析器，因此它并不适合于处理大规模的 XML 文件。</strong></p>
<h3 id="-1">快速上手</h3>
<p>来一个 Thymeleaf 的 Hello World 尝尝鲜。</p>
<h4 id="-2">相关配置</h4>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>在 application.properties 中添加配置：</p>
<pre><code class="properties language-properties">spring.thymeleaf.cache=false
</code></pre>
<p>其中，propertiesspring.thymeleaf.cache=false 是关闭 Thymeleaf 的缓存，不然在开发过程中修改页面不会立刻生效需要重启，生产可配置为 true。</p>
<h4 id="-3">一个简单的页面</h4>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Hello&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1  th:text="${message}"&gt;Hello World&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>所有使用 Thymeleaf 的页面必须在 HTML 标签声明 Thymeleaf：</p>
<pre><code class="html language-html">&lt;html xmlns:th="http://www.thymeleaf.org"&gt;
</code></pre>
<p>表明页面使用的是 Thymeleaf 语法。</p>
<h4 id="controller">Controller</h4>
<pre><code class="java language-java">@Controller
public class HelloController {
    @RequestMapping("/")
    public String index(ModelMap map) {
        map.addAttribute("message", "http://www.ityouknow.com");
        return "hello";
    }
}
</code></pre>
<p>这样就完成了，是不是很简单。启动项目后在浏览器中输入网址：http://localhost:8080/，会出现下面的结果：</p>
<pre><code class="html language-html">http://www.ityouknow.com
</code></pre>
<p>说明页面的值，已经成功的被后端传入的内容所替换。</p>
<h3 id="-4">常用语法</h3>
<p>我们新建 ExampleController 来封装不同的方法进行演示。</p>
<h4 id="-5">赋值、字符串拼接</h4>
<p>赋值和拼接：</p>
<pre><code class="html language-html">&lt;p th:text="${userName}"&gt;neo&lt;/p&gt;
&lt;span th:text="'Welcome to our application, ' + ${userName} + '!'"&gt;&lt;/span&gt;
</code></pre>
<p>字符串拼接还有另外一种简洁的写法：</p>
<pre><code class="html language-html">&lt;span th:text="|Welcome to our application, ${userName}!|"&gt;&lt;/span&gt;
</code></pre>
<p>页面 string.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example String &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div &gt;
        &lt;h1&gt;text&lt;/h1&gt;
        &lt;p th:text="${userName}"&gt;neo&lt;/p&gt;
        &lt;span th:text="'Welcome to our application, ' + ${userName} + '!'"&gt;&lt;/span&gt;
        &lt;br/&gt;
        &lt;span th:text="|Welcome to our application, ${userName}!|"&gt;&lt;/span&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>后端传值：</p>
<pre><code class="java language-java">@RequestMapping("/string")
public String string(ModelMap map) {
    map.addAttribute("userName", "ityouknow");
    return "string";
}
</code></pre>
<p>使用 ModelMap 以 KV 的方式存储传递到页面。</p>
<p>启动项目后在浏览器中输入网址：http://localhost:8080/string，会出现下面的结果：</p>
<pre><code class="html language-html">text

ityouknow

Welcome to our application, ityouknow!
Welcome to our application, ityouknow!
</code></pre>
<h4 id="ifunless">条件判断 If/Unless</h4>
<p>Thymeleaf 中使用 th:if 和 th:unless 属性进行条件判断，在下面的例子中，<code>&lt;a&gt;</code> 标签只有在 th:if 中条件成立时才显示：</p>
<pre><code class="html language-html">&lt;a th:if="${flag == 'yes'}"  th:href="@{http://favorites.ren/}"&gt; home &lt;/a&gt;
&lt;a th:unless="${flag != 'no'}" th:href="@{http://www.ityouknow.com/}" &gt;ityouknow&lt;/a&gt;
</code></pre>
<p>th:unless 与 th:if 恰好相反，只有表达式中的条件不成立，才会显示其内容。</p>
<p>页面 if.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example If/Unless &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div &gt;
    &lt;h1&gt;If/Unless&lt;/h1&gt;
    &lt;a th:if="${flag == 'yes'}"  th:href="@{http://favorites.ren/}"&gt; home &lt;/a&gt;
    &lt;br/&gt;
    &lt;a th:unless="${flag != 'no'}" th:href="@{http://www.ityouknow.com/}" &gt;ityouknow&lt;/a&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>后端传值：</p>
<pre><code class="java language-java">@RequestMapping("/if")
public String ifunless(ModelMap map) {
    map.addAttribute("flag", "yes");
    return "if";
}
</code></pre>
<p>使用 ModelMap 以 KV 的方式存储传递到页面。</p>
<p>启动项目后在浏览器中输入网址：http://localhost:8080/if，会出现下面的结果：</p>
<pre><code class="html language-html">If/Unless

home
</code></pre>
<p>单击 home 链接会跳转到：http://favorites.ren/ 地址。</p>
<h4 id="for">for 循环</h4>
<p>for 循环在我们项目中使用的频率太高了，一般结合前端的表格来使用。</p>
<p>首先在后端定义一个用户列表：</p>
<pre><code class="java language-java">private List&lt;User&gt; getUserList(){
    List&lt;User&gt; list=new ArrayList&lt;User&gt;();
    User user1=new User("大牛",12,"123456");
    User user2=new User("小牛",6,"123563");
    User user3=new User("纯洁的微笑",66,"666666");
    list.add(user1);
    list.add(user2);
    list.add(user3);
    return  list;
}
</code></pre>
<p>按照键 users，传递到前端：</p>
<pre><code class="java language-java">@RequestMapping("/list")
public String list(ModelMap map) {
    map.addAttribute("users", getUserList());
    return "list";
}
</code></pre>
<p>页面 list.html 进行数据展示：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example If/Unless &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div &gt;
    &lt;h1&gt;for 循环&lt;/h1&gt;
    &lt;table&gt;
        &lt;tr  th:each="user,iterStat : ${users}"&gt;
            &lt;td th:text="${user.name}"&gt;neo&lt;/td&gt;
            &lt;td th:text="${user.age}"&gt;6&lt;/td&gt;
            &lt;td th:text="${user.pass}"&gt;213&lt;/td&gt;
            &lt;td th:text="${iterStat.index}"&gt;index&lt;/td&gt;
        &lt;/tr&gt;
    &lt;/table&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>iterStat 称作状态变量，属性有：</p>
<ul>
<li>index，当前迭代对象的 index（从 0 开始计算）；</li>
<li>count，当前迭代对象的 index（从 1 开始计算）；</li>
<li>size，被迭代对象的大小；</li>
<li>current，当前迭代变量；</li>
<li>even/odd，布尔值，当前循环是否是偶数/奇数（从 0 开始计算）；</li>
<li>first，布尔值，当前循环是否是第一个；</li>
<li>last，布尔值，当前循环是否是最后一个。</li>
</ul>
<p>在浏览器中输入网址：http://localhost:8080/list，页面展示效果如下：</p>
<pre><code class="html language-html">for 循环
大牛  12  123456  0
小牛  6   123563  1
纯洁的微笑   66  666666  2
</code></pre>
<h4 id="url">URL</h4>
<p>URL 在 Web 应用模板中占据着十分重要的地位，需要特别注意的是 Thymeleaf 对于 URL 的处理是通过语法<code>@{...}</code>来处理的。如果需要 Thymeleaf 对 URL 进行渲染，那么务必使用 th:href、th:src 等属性，下面是一个例子：</p>
<pre><code class="html language-html">&lt;a th:href="@{http://www.ityouknow.com/{type}(type=${type})}"&gt;link1&lt;/a&gt;
&lt;a th:href="@{http://www.ityouknow.com/{pageId}/can-use-springcloud.html(pageId=${pageId})}"&gt;view&lt;/a&gt;
</code></pre>
<p>也可以使用<code>@{...}</code>设置背景：</p>
<pre><code class="html language-html">&lt;div th:style="'background:url(' + @{${img url}} + ');'"&gt;
</code></pre>
<p>几点说明：</p>
<ul>
<li>上例中 URL 最后的<code>(pageId=${pageId})</code>表示将括号内的内容作为 URL 参数处理，该语法避免使用字符串拼接，大大提高了可读性；</li>
<li><code>@{...}</code>表达式中可以通过<code>{pageId}</code>访问 Context 中的 pageId 变量；</li>
<li><code>@{/order}</code>是 Context 相关的相对路径，在渲染时会自动添加上当前 Web 应用的 Context 名字，假设 context 名字为 app，那么结果应该是 <code>/app/order</code>。</li>
</ul>
<p>完整的页面内容 url.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example If/Unless &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div &gt;
    &lt;h1&gt;URL&lt;/h1&gt;
    &lt;a  th:href="@{http://www.ityouknow.com/{type}(type=${type})}"&gt;link1&lt;/a&gt;
    &lt;br/&gt;
    &lt;a th:href="@{http://www.ityouknow.com/{pageId}/can-use-springcloud.html(pageId=${pageId})}"&gt;view&lt;/a&gt;
    &lt;br/&gt;
    &lt;div th:style="'background:url(' + @{${img}} + ');'"&gt;
        &lt;br/&gt;&lt;br/&gt;&lt;br/&gt;
    &lt;/div&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>后端程序：</p>
<pre><code class="java language-java">@RequestMapping("/url")
public String url(ModelMap map) {
    map.addAttribute("type", "link");
    map.addAttribute("pageId", "springcloud/2017/09/11/");
    map.addAttribute("img", "http://www.ityouknow.com/assets/images/neo.jpg");
    return "url";
}
</code></pre>
<p>在浏览器中输入网址：http://localhost:8080/url，页面展示效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/url.png" alt="" /></p>
<h4 id="-6">三目运算</h4>
<p>三目运算是我们常用的功能之一，普遍应用在各个项目中，下面来做一下演示。</p>
<p>三目运算及表单显示：</p>
<pre><code class="html language-html">&lt;input th:value="${name}"/&gt;
&lt;input th:value="${age gt 30 ? '中年':'年轻'}"/&gt;
</code></pre>
<p>说明：在表单标签中显示内容使用：<code>th:value;${age gt 30 ? '中年':'年轻'}</code>表示如果 age 大于 30 则显示中年，否则显示年轻。</p>
<ul>
<li>gt：great than（大于）</li>
<li>ge：great equal（大于等于）</li>
<li>eq：equal（等于）</li>
<li>lt：less than（小于）</li>
<li>le：less equal（小于等于）</li>
<li>ne：not equal（不等于）</li>
</ul>
<p>结合三目运算也可以将上面的 if else 改成这样：</p>
<pre><code class="html language-html">&lt;a th:if="${flag eq 'yes'}"  th:href="@{http://favorites.ren/}"&gt; favorites &lt;/a&gt;
</code></pre>
<p>完整的页面内容 eq.html：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example If/Unless &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div &gt;
    &lt;h1&gt;EQ&lt;/h1&gt;
    &lt;input th:value="${name}"/&gt;
    &lt;br/&gt;
    &lt;input th:value="${age gt 30 ? '中年':'年轻'}"/&gt;
    &lt;br/&gt;
    &lt;a th:if="${flag eq 'yes'}"  th:href="@{http://favorites.ren/}"&gt; favorites &lt;/a&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>后端程序：</p>
<pre><code class="java language-java">@RequestMapping("/eq")
public String eq(ModelMap map) {
    map.addAttribute("name", "neo");
    map.addAttribute("age", 30);
    map.addAttribute("flag", "yes");
    return "eq";
}
</code></pre>
<p>在浏览器中输入网址：http://localhost:8080/eq，页面展示效果如下：</p>
<pre><code class="html language-html">EQ

neo
年轻

favorites
</code></pre>
<p>单击 favorites 链接会跳转到：http://favorites.ren/ 地址。</p>
<h4 id="switch">switch 选择</h4>
<p>switch\case 多用于多条件判断的场景下，以性别举例：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"  xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;&lt;/meta&gt;
    &lt;title&gt;Example switch &lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div &gt;
    &lt;div th:switch="${sex}"&gt;
        &lt;p th:case="'woman'"&gt;她是一个姑娘...&lt;/p&gt;
        &lt;p th:case="'man'"&gt;这是一个爷们!&lt;/p&gt;
        &lt;!-- *: case的默认的选项 --&gt;
        &lt;p th:case="*"&gt;未知性别的一个家伙。&lt;/p&gt;
    &lt;/div&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>后端程序：</p>
<pre><code class="java language-java">@RequestMapping("/switch")
public String switchcase(ModelMap map) {
    map.addAttribute("sex", "woman");
    return "switch";
}
</code></pre>
<p>在浏览器中输入网址：http://localhost:8080/switch，页面展示效果如下：</p>
<pre><code>她是一个姑娘...
</code></pre>
<p>可以在后台改 sex 的值来查看结果。</p>
<h3 id="-7">总结</h3>
<p>本课介绍了模板引擎、Thymeleaf 的使用特点、应用场景，通过实例演练展示了 Thymeleaf 各种语法特性。通过学习可以了解到，Thymeleaf 是一个非常灵活和优秀的前端页面模板引擎，使用 Thymeleaf 可以非常灵活地展示页面内容。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>