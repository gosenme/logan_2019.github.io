---
title: 案例上手 Spring 全家桶-38
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们学习了 Spring Boot 整合 JSP 的具体操作，实现了 Spring Boot 与视图层的交互，相比较于 JSP，Thymeleaf 是目前较为流行的视图层技术，Spring Boot 官方也不推荐使用 JSP，而是建议使用 Thymeleaf，这节课我们就一起来学习 Spring Boot 整合 Thymeleaf 的具体实现方式。</p>
<h3 id="thymeleaf">什么是 Thymeleaf</h3>
<p>Thymeleaf 是一个支持原生 HTML 文件的 Java 模版引擎，可以实现前后端分离的交互方式，即视图与业务数据分开响应，它可以直接将服务端返回的数据生成 HTML 格式，同时也可以处理 XML、JavaScript、CSS 等格式。</p>
<p>Thymeleaf 最大的特点是既可以直接在浏览器打开，就像访问静态页面一样看到样式，也可以结合服务端将业务数据填充进去看到动态生成的页面。Spring Boot 对 Thymeleaf 模版做了很好的集成，在 Spring Boot 应用中使用 Thymeleaf 非常方便。</p>
<p>1. 创建 Maven 工程，不需要创建 Web 工程，创建一个最基础的 Maven 工程即可。</p>
<p><img src="https://images.gitbook.cn/d0dd5590-c1d2-11e9-9166-bdb140d6509f" width = "70%" /></p>
<p>2. pom.xml 中添加相关依赖，spring-boot-starter-thymeleaf 为 Spring Boot 整合 Thymeleaf 模版的依赖。</p>
<pre><code class="xml language-xml">&lt;parent&gt;
  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
  &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
  &lt;version&gt;2.1.5.RELEASE&lt;/version&gt;
&lt;/parent&gt;

&lt;dependencies&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>3. 在 resources 路径下创建 application.yml。</p>
<pre><code class="yaml language-yaml">spring:
  thymeleaf:
    prefix: classpath:/templates/     #模版路径
    suffix: .html                     #模版后缀
    servlet:
      content-type: text/html         #设置 Content-type
    encoding: UTF-8                   #编码方式
    mode: HTML5                       #校验 HTML5 格式
    cache: false                      #关闭缓存，在开发过程中可立即看到页面修改结果
</code></pre>
<p>这里的配置和使用 JSP 类似，通过前缀和后缀完成视图解析，同时可以设置 HTML 页面的其他属性、入编码方式等。</p>
<p>4. 创建 Handler 业务方法，向客户端返回视图和业务数据。</p>
<pre><code class="java language-java">@Controller
public class HelloHandler {

    @GetMapping("/index")
    public ModelAndView index(){
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.addObject("name","张三");
        modelAndView.setViewName("index");
        return modelAndView;
    }
}
</code></pre>
<p>5. 在 resources/templates 路径下创建 index.html，代码如下所示。</p>
<pre><code class="html language-html">&lt;body&gt;
    &lt;p th:text="${name}"&gt;Hello World&lt;/p&gt;
&lt;/body&gt;
</code></pre>
<p>我们之前说过，Thymeleaf 既可以直接在浏览器打开访问，也可以通过服务端进行数据填充之后再返回给客户端，如果此时直接访问 index.html，可以看到如下结果。</p>
<p><img src="https://images.gitbook.cn/ee1a1350-c1d2-11e9-97a8-35dcf136a505" width = "75%" /></p>
<p>可以看到，浏览器直接加载 h1 标签中的 Hello World，如果希望服务将服务端的业务数据填充到 h1 标签中，则需要结合 Thymeleaf 模版标签来完成，首先通过 <code>&lt;html xmlns:th="http://www.thymeleaf.org"&gt;</code> 导入 Thymeleaf 命名空间，接下来再需要填充数据的 HTML 原生标签中使用 <code>th:text</code> 完成数据填充，语法与 EL 表达式一致，通过 <code>${业务数据 key 值}</code> 即可完成。</p>
<p>6. 创建启动类 Application：</p>
<pre><code class="java language-java">@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>7. 启动 Application，访问 http://localhost:8080/index，即可看到如下结果。</p>
<p><img src="https://images.gitbook.cn/12cc2620-c1d3-11e9-8621-c1fbe3716b21" width = "50%" /></p>
<p>此时返回的是经过服务端完成数据填充之后的 index.html，数据为“张三”，index.html 源代码如下所示。</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Title&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;p&gt;张三&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>而如果不通过服务端，直接访问静态资源 index.html，对应的源代码如下所示。</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html xmlns:th="http://www.thymeleaf.org"&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Title&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;p th:text="${name}"&gt;Hello World&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>通过以上对比，我们可以得出结论，Spring Boot 服务端会根据业务方法来动态生成嵌入了业务数据的视图层资源，并响应给客户端，借助的就是 Thymeleaf 模版。</p>
<h3 id="thymeleaf-1">Thymeleaf 常用标签</h3>
<ul>
<li>th:text</li>
</ul>
<p>th:text 用于文本显示，将业务数据的值填充到 HTML 标签中，具体使用如上面案例所示。</p>
<ul>
<li>th:if</li>
</ul>
<p>th:if 用于条件判断，对业务数据的值进行判断，如果条件成立则显示内容，否则不显示，具体使用如下所示。</p>
<p>Handler</p>
<pre><code class="java language-java">@GetMapping("/if")
public ModelAndView ifTest(){
  ModelAndView modelAndView = new ModelAndView();
  modelAndView.setViewName("test");
  modelAndView.addObject("score",90);
  return modelAndView;
}
</code></pre>
<p>HTML</p>
<pre><code class="html language-html">&lt;p th:if="${score&gt;=90}"&gt;优秀&lt;/p&gt;
&lt;p th:if="${score&lt;90 &amp;&amp; score&gt;=80}"&gt;良好&lt;/p&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/4d40bfa0-c1d3-11e9-9969-976e2ac29eb2" width = "50%" /></p>
<ul>
<li>th:unless</li>
</ul>
<p>th:unless 也用作条件判断，逻辑与 th:if 恰好相反，如果条件不成立则显示内容，否则不显示，具体使用如下所示。</p>
<p>Handler</p>
<pre><code class="java language-java">@GetMapping("/unless")
public ModelAndView unlessTest(){
  ModelAndView modelAndView = new ModelAndView();
  modelAndView.setViewName("test");
  modelAndView.addObject("score",90);
  return modelAndView;
}
</code></pre>
<p>HTML</p>
<pre><code class="html language-html">&lt;p th:unless="${score&gt;=90}"&gt;优秀&lt;/p&gt;
&lt;p th:unless="${score&lt;90 &amp;&amp; score&gt;=80}"&gt;良好&lt;/p&gt;
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/684abee0-c1d3-11e9-9969-976e2ac29eb2" width = "50%" /></p>
<p>可以看到，在数据一致的情况下，th:unless 和 th:if 的运行结果完全相反。</p>
<ul>
<li>th:switch th:case</li>
</ul>
<p>th:switch th:case 两个结合起来使用，用作多条件等值判断，逻辑与 Java 中的 switcht-case 一致，当 switch 中的业务数据值等于某个 case 值时，就显示这个 case 对应的内容，具体使用如下所示。</p>
<p>Handler</p>
<pre><code class="java language-java">@GetMapping("/switchcase")
public ModelAndView switchcase(){
  ModelAndView modelAndView = new ModelAndView();
  modelAndView.setViewName("test");
  modelAndView.addObject("studentId",1);
  return modelAndView;
}
</code></pre>
<p>HTML</p>
<pre><code class="html language-html">&lt;div th:switch="${studentId}"&gt;
  &lt;p th:case="1"&gt;张三&lt;/p&gt;
  &lt;p th:case="2"&gt;李四&lt;/p&gt;
  &lt;p th:case="3"&gt;王五&lt;/p&gt;
&lt;/div&gt;
</code></pre>
<p>运行结果如下所示。</p>
<p><img src="https://images.gitbook.cn/88d288f0-c1d3-11e9-97a8-35dcf136a505" width = "50%" /></p>
<ul>
<li>th:action</li>
</ul>
<p>th:action 用来指定请求的 URL，相当于 form 表单中的 action 属性，具体使用如下所示。</p>
<p>首先我们要创建一个 login.html。</p>
<pre><code class="html language-html">&lt;body&gt;
    &lt;form th:action="@{/login}" method="post"&gt;
        用户名:&lt;input type="text" name="userName"/&gt;&lt;br/&gt;
        密码:&lt;input type="password" name="password"/&gt;&lt;br/&gt;
        &lt;input type="submit" value="登录"/&gt;
    &lt;/form&gt;
&lt;/body&gt;
</code></pre>
<p>输入用户名和密码之后提交表单至 /login，这里需要注意的是我们不能直接访问 login.html，因为这里需要通过 Thymeleaf 模版动态为 form 表单的 action 属性赋值，所以必须通过 Handler 来映射到 HTML，否则无法完成动态赋值，在 Handelr 中添加如下方法。</p>
<pre><code class="java language-java">@GetMapping("/login")
public String login(){
  return "login";
}
</code></pre>
<p>当服务端接收到一个 GET 请求 login 时，映射到 login.html 并响应给客户端，这样 <code>th:action="@{/login}"</code> 才能生效，同时再添加一个处理 login 的业务方法，如下所示。</p>
<pre><code class="java language-java">@PostMapping("/login")
public String login(@RequestParam("userName") String userName,@RequestParam("password") String password){
  System.out.println(userName);
  System.out.println(password);
  return "login";
}
</code></pre>
<p>接收到客户端传来的参数并打印输出，两个 login 方法分别用 @GetMapping("/login") 和 @PostMapping("/login") 进行区分，即如果是 GET 请求则响应动态 HTML 页面，如果是 POST 请求则进行业务逻辑处理。</p>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/ee51f6c0-c1d3-11e9-8621-c1fbe3716b21" width = "55%" /></p>
<p><img src="https://images.gitbook.cn/f86a3140-c1d3-11e9-9166-bdb140d6509f" width = "55%" /></p>
<ul>
<li>th:each</li>
</ul>
<p>th:each 用来遍历集合，具体使用如下所示。</p>
<p>结合 Lombok 创建 User 实体类，首先在 pom.xml 中添加 Lombok 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
  &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
  &lt;artifactId&gt;lombok&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>User</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private Integer gender;
}
</code></pre>
<p>Handler</p>
<pre><code class="java language-java">@GetMapping("/each")
public ModelAndView each(){
  List&lt;User&gt; list = new ArrayList&lt;&gt;();
  list.add(new User(1L,"张三",1));
  list.add(new User(2L,"李四",0));
  list.add(new User(3L,"王五",1));
  ModelAndView modelAndView = new ModelAndView();
  modelAndView.setViewName("test");
  modelAndView.addObject("list",list);
  return modelAndView;
}
</code></pre>
<p>HTML</p>
<pre><code class="html language-html">&lt;h1&gt;用户信息&lt;/h1&gt;
&lt;table&gt;
    &lt;tr&gt;
        &lt;th&gt;编号&lt;/th&gt;
        &lt;th&gt;姓名&lt;/th&gt;
        &lt;th&gt;性别&lt;/th&gt;
    &lt;/tr&gt;
    &lt;tr th:each="user:${list}"&gt;
        &lt;td th:text="${user.id}"&gt;&lt;/td&gt;
        &lt;td th:text="${user.name}"&gt;&lt;/td&gt;
        &lt;td th:if="${user.gender == 1}"&gt;男&lt;/td&gt;
        &lt;td th:if="${user.gender == 0}"&gt;女&lt;/td&gt;
    &lt;/tr&gt;
&lt;/table&gt;
</code></pre>
<p>运行结果如下所示。</p>
<p><img src="https://images.gitbook.cn/298a7c80-c1d4-11e9-8621-c1fbe3716b21" width = "50%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring Boot 整合 Thymeleaf 的具体操作，Thymeleaf 是一个支持原生 HTML 文件的 Java 模版引擎，既能以静态页面的方式直接运行，也可以结合后端代码动态生成，大大简化了前后端开发人员的工作对接，同时我们详细讲解了 Thymeleaf 常用标签的使用。</p>
<p><a href="https://github.com/southwind9801/gcspringbootthymeleaf.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>