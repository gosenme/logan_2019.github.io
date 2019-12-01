---
title: 案例上手 Spring 全家桶-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>数据校验是每个项目中必不可少的模块，Spring MVC 作为一款成熟的框架，也为我们提供了校验组件，有两种方式可供开发者选择：（1）基于 Validator 接口进行校验；（2）使用 Annotaion JSR-303 标准进行校验。</p>
<p>使用 Validator 接口进行数据校验会稍微复杂一些，具体的数据验证规则需要开发者手动进行设置。而使用 Annotaion JSR-303 标准就相对简单很多，开发者不需要编写验证逻辑，直接通过注解的形式就可以给每一条数据添加验证规则，具体操作是直接在实体类的属性上添加对于的校验规则即可，使用起来更加方便。</p>
<p>两种校验方式的具体使用如下所示。</p>
<h3 id="validator">基于 Validator 接口</h3>
<p>我们通过学生登录的场景来学习使用基于 Validator 接口的验证器。</p>
<p>（1）创建实体类 Student</p>
<pre><code class="java language-java">public class Student {
    private String name;
    private String password;
}
</code></pre>
<p>（2）自定义校验器 StudentValidation，实现 Validator 接口，重新接口的抽象方法，加入校验规则</p>
<pre><code class="java language-java">public class StudentValidator implements Validator{

    public boolean supports(Class&lt;?&gt; clazz) {
        // TODO Auto-generated method stub
        return Student.class.equals(clazz);
    }

    public void validate(Object target, Errors errors) {
        // TODO Auto-generated method stub
        ValidationUtils.rejectIfEmpty(errors, "name", null, "姓名不能为空"); 
        ValidationUtils.rejectIfEmpty(errors, "password", null, "密码不能为空");
    }

}
</code></pre>
<p>（3）创建控制器 HelloHandler，在业务方法 login 参数列表中的 @Validated 表示参数 student 是需要校验的对象，@BindingResult 用来存储错误信息，两者缺一不可，而且必须挨着写，不能中间有其他参数。</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/hello")
public class HelloHandler {

    @GetMapping(value = "/login")
    public String login(Model model){
        model.addAttribute(new Student());
        return "login";
    }

    @PostMapping(value="/login")
    public String login(@Validated Student student,BindingResult br) {
        if (br.hasErrors()) {
            return "login";
        }
        return "success";
    }

}
</code></pre>
<p>（4）在 springmvc.xml 中配置 validator</p>
<pre><code class="xml language-xml">&lt;!-- 配置自动扫描 --&gt;
&lt;context:component-scan base-package="com.southwind"&gt;&lt;/context:component-scan&gt;
&lt;!-- 配置视图解析器 --&gt;
&lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
    &lt;!-- 前缀 --&gt;
    &lt;property name="prefix" value="/"&gt;&lt;/property&gt;
    &lt;!-- 后缀 --&gt;
    &lt;property name="suffix" value=".jsp"&gt;&lt;/property&gt;
    &lt;/bean&gt;
&lt;!-- 基于 Validator 的配置 --&gt;
&lt;mvc:annotation-driven validator="studentValidator"/&gt;
&lt;bean id="studentValidator" class="com.southwind.validator.StudentValidator"/&gt;
</code></pre>
<p>（5）login.jsp</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;学生登录&lt;/h1&gt;
&lt;form:form modelAttribute="student" action="login" method="post"&gt;
    学生姓名：&lt;form:input path="name" /&gt;&lt;form:errors path="name"/&gt;&lt;br/&gt;
    学生密码：&lt;form:password path="password" /&gt;&lt;form:errors path="password"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form:form&gt;
</code></pre>
<p>（6）运行，通过地址栏发送 GET 请求访问 login 方法，绑定模型数据，然后页面跳转到 login.jsp，如下所示，不输入用户名密码直接单击提交按钮。</p>
<p><img src="https://images.gitbook.cn/452cc7e0-9ade-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<p>单击提交按钮后，form 表单发送 POST 请求访问 login 方法，完成数据校验，并将校验结果再次返回到 login.jsp，如下图所示。</p>
<p><img src="https://images.gitbook.cn/4d637120-9ade-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="annotaionjsr303">Annotaion JSR-303 标准</h3>
<p>使用 Annotation JSR-303 标准进行验证，需要导入支持这种标准的 jar 包，这里我们使用 Hibernate Validator。</p>
<p>标准详解如下所示：</p>
<p><img src="https://images.gitbook.cn/8abe0c30-9ae1-11e8-831e-0180aea56660" width = "80%" /></p>
<p>接下来通过用户注册的场景来学习使用 JSR-303 标准进行数据校验。</p>
<p>（1）在 pom.xml 中添加 Hibernate Validator 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework&lt;/groupId&gt;
    &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
    &lt;version&gt;5.0.8.RELEASE&lt;/version&gt;
&lt;/dependency&gt;
&lt;!-- JRS-303 --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
    &lt;artifactId&gt;hibernate-validator&lt;/artifactId&gt;
    &lt;version&gt;5.1.3.Final&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;javax.validation&lt;/groupId&gt;
    &lt;artifactId&gt;validation-api&lt;/artifactId&gt;
    &lt;version&gt;1.1.0.Final&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.jboss.logging&lt;/groupId&gt;
    &lt;artifactId&gt;jboss-logging&lt;/artifactId&gt;
    &lt;version&gt;3.1.1.GA&lt;/version&gt;
 &lt;/dependency&gt;
&lt;!-- 解决 JDK9 以上版本没有 JAXB API jar 的问题，JDK9 以下版本不需要配置 --&gt;
&lt;dependency&gt;
   &lt;groupId&gt;javax.xml.bind&lt;/groupId&gt;
   &lt;artifactId&gt;jaxb-api&lt;/artifactId&gt;
   &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
   &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
   &lt;artifactId&gt;jaxb-impl&lt;/artifactId&gt;
   &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
    &lt;artifactId&gt;jaxb-core&lt;/artifactId&gt;
    &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;javax.activation&lt;/groupId&gt;
    &lt;artifactId&gt;activation&lt;/artifactId&gt;
    &lt;version&gt;1.1.1&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>这里我们需要注意，如果环境是 JDK9 以下的，可以不用添加以下四个依赖；如果环境是 JDK9 以上版本，必须添加这四个依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;javax.xml.bind&lt;/groupId&gt;
    &lt;artifactId&gt;jaxb-api&lt;/artifactId&gt;
    &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
    &lt;artifactId&gt;jaxb-impl&lt;/artifactId&gt;
    &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
    &lt;artifactId&gt;jaxb-core&lt;/artifactId&gt;
    &lt;version&gt;2.3.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;javax.activation&lt;/groupId&gt;
    &lt;artifactId&gt;activation&lt;/artifactId&gt;
    &lt;version&gt;1.1.1&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>（2）创建实体类 User，通过注解的方式给属性指定校验规则。</p>
<p>校验规则详解如下所示：</p>
<p><img src="https://images.gitbook.cn/dcda6720-9ae1-11e8-8cbe-ad3f3badcc18" width = "80%" /></p>
<p>创建 User 实体类，并通过注解给每个属性添加校验规则：</p>
<pre><code class="java language-java">public class User {
    @NotEmpty(message = "用户名不能为空")
    private String username;
    @Size(min = 6,max = 20,message = "密码长度为6-12位")
    private String password;
    @Email(regexp = "^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*\\.[a-zA-Z0-9]{2,6}$", message = "请输入正确的邮箱格式")
    private String email;
    @Pattern(regexp = "^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\\\d{8}$",message="请输入正确的电话格式")
    private String phone;
}
</code></pre>
<p>（3）创建控制器 HelloHandler，在业务方法 register 使用 @Valid 来绑定校验对象，@BindingResult 来保存错误信息。</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/hello")
public class HelloHandler {

    @GetMapping(value="/register")
    public String register(Model model){
        model.addAttribute(new User());
        return "register";
    }

    @PostMapping(value="/register")
    public String register2(@Valid User user,BindingResult br) {
        if (br.hasErrors()){
            return "register";
        }
        return "success";
    }

}
</code></pre>
<p>（4）在 springmvc.xml 中添加配置</p>
<pre><code class="xml language-xml">&lt;!-- 配置自动扫描 --&gt;
&lt;context:component-scan base-package="com.southwind"&gt;&lt;/context:component-scan&gt;
&lt;!-- 配置视图解析器 --&gt;
&lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
    &lt;!-- 前缀 --&gt;
    &lt;property name="prefix" value="/"&gt;&lt;/property&gt;
    &lt;!-- 后缀 --&gt;
    &lt;property name="suffix" value=".jsp"&gt;&lt;/property&gt;
&lt;/bean&gt;
&lt;!-- JSR-303配置 --&gt;
&lt;mvc:annotation-driven /&gt;
</code></pre>
<p>（5）register.jsp</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;用户注册&lt;/h1&gt;
&lt;form:form modelAttribute="user" action="register" method="post"&gt;
     用户名：&lt;form:input path="username" /&gt;&lt;form:errors path="username" /&gt;&lt;br/&gt;
     密码：&lt;form:password path="password" /&gt;&lt;form:errors path="password" /&gt;&lt;br/&gt;
     邮箱：&lt;form:input path="email" /&gt;&lt;form:errors path="email" /&gt;&lt;br/&gt;
     电话：&lt;form:input path="phone" /&gt;&lt;form:errors path="phone" /&gt;&lt;br/&gt;
     &lt;input type="submit" value="提交"/&gt;
&lt;/form:form&gt;
</code></pre>
<p>（6）运行，通过地址栏发送 GET 请求访问 register 方法，绑定模型数据，然后页面跳转到 register.jsp，如下所示，不输入用户名、密码、邮箱、电话信息，直接单击提交按钮。</p>
<p><img src="https://images.gitbook.cn/09dcc5b0-9ae2-11e8-8cbe-ad3f3badcc18" width = "50%" /></p>
<p>单击提交按钮后，form 表单发送 POST 请求访问 register 方法，完成数据校验，并将校验结果再次返回到 register.jsp，如下所示。</p>
<p><img src="https://images.gitbook.cn/14853240-9ae2-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring MVC 对于数据校验的支持，Spring MVC 提供了两种数据校验的方式，基于 Validator 接口的校验、使用 Annotaion JSR-303 标准进行校验。Annotaion JSR-303 标准可以结合注解来完成校验工作，实际开发中推荐使用。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc_datavalidator.git">请单击这里下载源码</a></p></div></article>