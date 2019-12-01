---
title: 案例上手 Spring 全家桶-37
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在前面的课程中我们已经用 Spring Boot 快速构建了一个 Web 应用，可以向客户端返回数据，如果是在非前后端分离的传统 Web 项目中，只返回数据是不够的，同时还需要返回视图信息。接下来我们就来一起学习 Spring Boot 与视图层的整合，主要介绍两种视图层技术：JSP 和 Thymeleaf。</p>
<p>JSP 是传统 Java Web 开发中的技术层组件，Thymeleaf 是当前比较流行的技术，我们首先来学习 Spring Boot 如何整合 JSP。</p>
<p>首先对 JSP 的基本概念做一个解释。JSP 全称是 Java Server Page，即 Java 服务页面，是 Java Web 提供的一种动态网页技术，可以在 HTML 代码中插入 Java 程序。其本质是一个 Servlet，当客户端第一次访问 JSP 资源的时候，JSP 引擎会自动为目标 JSP 生成一个对应的 Servlet 文件，在这个 Servlet 文件中，通过 response 将定义在 JSP 中的 HTML 代码返回给客户端，来看一个实际案例，比如 JSP 代码定义如下。</p>
<pre><code class="jsp language-jsp">&lt;%@ page contentType="text/html;charset=UTF-8" language="java" %&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Hello World&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>JSP 引擎为其生成的 Servlet 代码如下。</p>
<pre><code class="java language-java">response.setContentType("text/html;charset=UTF-8");
out.write("\n");
out.write("\n");
out.write("\n");
out.write("\n");
out.write("&lt;html&gt;\n");
out.write("&lt;head&gt;\n");
out.write("    &lt;title&gt;Title&lt;/title&gt;\n");
out.write("&lt;/head&gt;\n");
out.write("&lt;body&gt;\n");
out.write("         &lt;h1&gt;Hello World&lt;/h1&gt;");
out.write("\n");
out.write("&lt;/body&gt;\n");
out.write("&lt;/html&gt;\n");
</code></pre>
<p>JSP 相当于一个中间层组件，开发者在这个组件中将 Java 代码和 HTML 代码进行整合，由 JSP 引擎将组件转为 Servlet，再把开发者定义在组件中的混合代码翻译成 Servlet 的响应语句，输出给客户端的，这就是 JSP 的底层原理。</p>
<p>虽说只有在第一次访问 JSP 资源的时候才会生成对应的 Servlet，后续访问不再需要重复生成 Servlet，当然如果修改了 JSP 代码，肯定是要更新的。很显然这种方式的效率并不高，因此这也是目前 Java Web 开发逐渐倾向于使用原生的 HTML 作为视图层组件的原因，因为原生 HTML 的效率更高，不需要做中间转换。</p>
<p>了解完 JSP 的底层原理，接下来我们一起学习如何在 Spring Boot 工程中使用 JSP。</p>
<p>1. 创建基于 Mave 的 Web 工程。</p>
<p><img src="https://images.gitbook.cn/3b741510-c02f-11e9-8e2c-3b4fd17ad6da" width = "70%" /></p>
<p>2. 选择 Maven，右侧菜单勾选 Create from archetype，选中 org.apache.maven.archetypes:maven-archetype-webapp，点击 Next。</p>
<p><img src="https://images.gitbook.cn/f9dd4c10-bcab-11e9-ac77-f5b1a77a87b3" width = "75%" /></p>
<p>3. 工程创建完成之后，在 pom.xml 中添加相关依赖，tomcat-embed-jasper 是用来加载 JSP 资源的依赖。</p>
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
    &lt;groupId&gt;org.apache.tomcat.embed&lt;/groupId&gt;
    &lt;artifactId&gt;tomcat-embed-jasper&lt;/artifactId&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>4. 创建 HelloHandler，定义业务方法向客户端返回视图模型数据。</p>
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
<p>5. 在 webapp 路径下创建 JSP 资源 index.jsp，用 EL 表达式取出服务端返回的模型数据，<code>&lt;%@ page isELIgnored="false" %&gt;</code> 指令是设置让 JSP 页面解析 EL 表达式。</p>
<pre><code class="xml language-xml">&lt;%@ page contentType="text/html;charset=UTF-8" language="java" %&gt;
&lt;%@ page isELIgnored="false" %&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    ${name}
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>6. 在 resources 路径下创建配置文件 application.yml。</p>
<pre><code class="yaml language-yaml">server:
  port: 8080                      #端口
  servlet:
    context-path: /               #项目访问路径
    session:
      cookie:                     #cookie 失效时间，单位为秒
        max-age: 100
      timeout: 100                #session 失效时间，单位为秒
  tomcat:
    uri-encoding: UTF-8           #请求编码格式
spring:
  mvc:
    view:
      prefix: /                   #视图资源所在路径
      suffix: .jsp                #视图资源的后缀
</code></pre>
<p>webapp 是 Web 资源的根目录，因为当前的 index.jsp 放置在 webapp 路径下，所以 prefix 的值为 /，如果我们把 JSP 资源放置在 webapp/jsp 路径下，那么 prefix 的值就应该设置为 /jsp/。</p>
<p>7. 创建启动类 Application。</p>
<pre><code class="java language-java">@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>整个工程结构如下图所示。</p>
<p><img src="https://images.gitbook.cn/28c97940-bcac-11e9-8296-ad04873de5ea" width = "50%" /></p>
<p>8. 启动 Application，打开浏览器访问 http://localhost:8080/index，即可看到如下页面。</p>
<p><img src="https://images.gitbook.cn/30d14a50-bcac-11e9-a349-65f0a13339ef" width = "50%" /></p>
<h3 id="-1">实际应用</h3>
<p>上面我们只是实现了最基本的 Spring Boot 整合 JSP，实际开发中我们往往需要结合业务需求进行功能更为丰富的操作，这里我们结合 JSTL（JavaServer Pages Standard Tag Library，JSP 标准标签库）来完成一个数据展示功能。</p>
<p>1. pom.xml 中添加相关依赖，这里我们引入 JSTL 和 Lombok 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
  &lt;groupId&gt;jstl&lt;/groupId&gt;
  &lt;artifactId&gt;jstl&lt;/artifactId&gt;
  &lt;version&gt;1.2&lt;/version&gt;
&lt;/dependency&gt;

&lt;dependency&gt;
  &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
  &lt;artifactId&gt;lombok&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>使用 Lombok 可以简化实体类代码的编写工作，常用方法诸如 getter、setter、toString 等都可以由 Lombok 自动生成，开发者不需要自己手动编写，但是使用 Lombok 需要首先在 IDEA 中安装插件，具体安装步骤如下所示。</p>
<p><img src="https://images.gitbook.cn/73ca37e0-bcac-11e9-b095-45b8601f64cd" alt="WX20190604-142856@2x" /></p>
<p>2. 创建实体类 User。</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private Integer gender;
}
</code></pre>
<p>3. 在 HelloHandler 中创建业务方法，返回一个 User 对象集合给客户端。</p>
<pre><code class="java language-java">@GetMapping("/findAll")
public ModelAndView findAll(){
  ModelAndView modelAndView = new ModelAndView();
  List&lt;User&gt; list = new ArrayList&lt;&gt;();
  list.add(new User(1L,"张三",1));
  list.add(new User(2L,"李四",0));
  list.add(new User(3L,"王五",1));
  modelAndView.addObject("list",list);
  modelAndView.setViewName("show");
  return modelAndView;
}
</code></pre>
<p>4. 创建 show.jsp，使用 JSTL+EL 表达式取出模型数据。</p>
<pre><code class="jsp language-jsp">&lt;body&gt;
    &lt;h1&gt;用户信息&lt;/h1&gt;
    &lt;table&gt;
        &lt;tr&gt;
            &lt;th&gt;编号&lt;/th&gt;
            &lt;th&gt;姓名&lt;/th&gt;
            &lt;th&gt;性别&lt;/th&gt;
        &lt;/tr&gt;
        &lt;c:forEach items="${requestScope.list}" var="user"&gt;
            &lt;tr&gt;
                &lt;td&gt;${user.id}&lt;/td&gt;
                &lt;td&gt;${user.name}&lt;/td&gt;
                &lt;td&gt;
                    &lt;c:if test="${user.gender == 1}"&gt;男&lt;/c:if&gt;
                    &lt;c:if test="${user.gender == 0}"&gt;女&lt;/c:if&gt;
                &lt;/td&gt;
            &lt;/tr&gt;
        &lt;/c:forEach&gt;
    &lt;/table&gt;
&lt;/body&gt;
</code></pre>
<p>5. 启动 Application，访问 http://localhost:8080/findAll，结果如下所示。</p>
<p><img src="https://images.gitbook.cn/81abd670-bcac-11e9-b095-45b8601f64cd" width = "60%" /></p>
<h3 id="-2">总结</h3>
<p>本节课我们讲解了 Spring Boot 整合视图层技术 JSP 的具体操作，在 Java Web 开发中，视图层技术必不可少，当前 Spring Boot 支持的主流视图层解决方案为 JSP 和 Thymeleaf，一个是用传统的 JSP 组件进行开发，另外一个是用原生 HTML 进行开发，下节课我们将对 Spring Boot 整合 Thymeleaf 进行详细讲解。</p>
<h3 id="-3">源码</h3>
<p><a href="https://github.com/southwind9801/gcspringbootjsp.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p></div></article>