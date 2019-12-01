---
title: 精通 Spring Boot 42 讲-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在前面课程中，我们学习了 Spring Boot Web 开发、JPA 数据库操作、Thymeleaf 和页面交互技术，这节课综合这些内容做一个用户管理功能，包括展示用户列表（分页）、添加用户、修改用户和删除用户。有人说程序员的一生都是在增、删、改、查，这句话不一定全对，但也有一定的道理，相比于这句话，我更认同的是这句：程序员的技术学习都是从增、删、改、查开始的。</p>
<p>这节课将介绍如何使用 JPA 和 Thymeleaf 做一个用户管理功能。</p>
<h3 id="">配置信息</h3>
<h4 id="-1">添加依赖</h4>
<p>pom 包里面添加 JPA 和 Thymeleaf 的相关包引用。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-Thymeleaf&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-data-Jpa&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;mysql&lt;/groupId&gt;
    &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<h4 id="-2">配置文件</h4>
<p>在 application.properties 中添加配置：</p>
<pre><code class="properties language-properties">spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

spring.jpa.properties.hibernate.hbm2ddl.auto=create
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect
spring.jpa.show-sql= true

spring.thymeleaf.cache=false
</code></pre>
<p>其中，spring.Thymeleaf.cache=false 是关闭 Thymeleaf 的缓存，不然在开发过程中修改页面不会立刻生效需要重启，生产可配置为 true。</p>
<p>在项目 resources 目录下会有两个文件夹：static 目录用于放置网站的静态内容如 css、js、图片；templates 目录用于放置项目使用的页面模板。</p>
<h4 id="-3">启动类</h4>
<p>启动类需要添加 Servlet 的支持：</p>
<pre><code class="java language-java">@SpringBootApplication
public class JpaThymeleafApplication extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(JpaThymeleafApplication.class);
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(JpaThymeleafApplication.class, args);
    }
}
</code></pre>
<p>添加 SpringBootServletInitializer 是为了支持将项目打包成独立的 war 在 Tomcat 中运行的情况。</p>
<h3 id="-4">数据库层</h3>
<p>实体类映射数据库表：</p>
<pre><code class="java language-java">@Entity
public class User {
    @Id
    @GeneratedValue
    private long id;
    @Column(nullable = false, unique = true)
    private String userName;
    @Column(nullable = false)
    private String passWord;
    @Column(nullable = false)
    private int age;
    @Column(nullable = false)
    private Date regTime;
    //省略getter settet方法
}
</code></pre>
<p>继承 JpaRepository 类会自动实现很多内置的方法，包括增、删、改、查，也可以根据方法名来自动生成相关 SQL。</p>
<pre><code class="java language-java">public interface UserRepository extends JpaRepository&lt;User, Long&gt; {
    @Query("select u from User u")
    Page&lt;User&gt; findList(Pageable pageable);
    User findById(long id);
    User findByUserName(String userName);
    void deleteById(Long id);
}
</code></pre>
<p>Repository 内编写我们需要的 SQL 和分页查询。</p>
<h3 id="-5">实现一个添加功能</h3>
<p>在处理前端业务的时候一般是使用 param 结尾的参数来处理，在项目下新建 param 包，在 param 包下创建 UserParam 类接收添加用户的请求参数。另外，需要对接收的参数做校验，按照前面课程的内容，引入 hibernate-validator 做校验。</p>
<pre><code class="java language-java">public class UserParam {
    private long id;
    @NotEmpty(message="姓名不能为空")
    private String userName;
    @NotEmpty(message="密码不能为空")
    @Length(min=6,message="密码长度不能小于6位")
    private String passWord;
    @Max(value = 100, message = "年龄不能大于100岁")
    @Min(value= 18 ,message= "必须年满18岁！" )
    private int age;
    //省略getter settet方法
}
</code></pre>
<p>Controller 负责接收请求，首先判断参数是否正确，如果有错误直接返回页面，将错误信息展示给用户，再判断用户是否存在，如果用户已经存在同样返回页面给出提示。验证通过后，将 UserParam 属性复制到 User 并添加用户注册时间，最后将用户信息保存到数据库中。</p>
<pre><code class="java language-java">@RequestMapping("/add")
public String add(@Valid UserParam userParam,BindingResult result, Model model) {
    String errorMsg="";
    // 参数校验
    if(result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg=errorMsg + error.getCode() + "-" + error.getDefaultMessage() +";";
        }
        model.addAttribute("errorMsg",errorMsg);
        return "user/userAdd";
    }
    //判断是否重复添加
    User u= userRepository.findByUserName(userParam.getUserName());
    if(u!=null){
        model.addAttribute("errorMsg","用户已存在!");
        return "user/userAdd";
    }
    User user=new User();
    BeanUtils.copyProperties(userParam,user);
    user.setRegTime(new Date());
    //保存
    userRepository.save(user);
    return "redirect:/list";
}
</code></pre>
<ul>
<li>model 对象主要用于传递控制方法处理数据到结果页面；</li>
<li>return "redirect:/list"; 代表添加成功后直接跳转到用户列表页面。</li>
</ul>
<p><strong>添加用户部分页面</strong>（userAdd.html）</p>
<p>前端页面引入了 Bootstrap 前端框架，以下表单按照 Bootstrap 的格式进行设计。</p>
<pre><code class="html language-html">&lt;form class="form-horizontal"   th:action="@{/add}"  method="post"&gt;
    &lt;!-- 表单内容--&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="userName" class="col-sm-2 control-label"&gt;userName&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="text" class="form-control" name="userName"  id="userName" placeholder="userName"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="password" class="col-sm-2 control-label" &gt;passWord&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="password" class="form-control" name="passWord" id="passWord" placeholder="passWord"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    ....
    &lt;!-- 错误信息展示区--&gt;
    &lt;div class="form-group"&gt;
        &lt;label  class="col-sm-2 control-label"&gt;&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;div th:if="${errorMsg != null}"  class="alert alert-danger" role="alert" th:text="${errorMsg}"&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;!-- 按钮区--&gt;
    &lt;div class="form-group"&gt;
        &lt;div class="col-sm-offset-2 col-sm-10"&gt;
            &lt;input type="submit" value="Submit" class="btn btn-info" /&gt;
            &amp;nbsp; &amp;nbsp; &amp;nbsp;
            &lt;input type="reset" value="Reset" class="btn btn-info" /&gt;
            &amp;nbsp; &amp;nbsp; &amp;nbsp;
            &lt;a href="/toAdd" th:href="@{/list}" class="btn btn-info"&gt;Back&lt;/a&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/form&gt;
</code></pre>
<p>效果图：</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/add.png"  width = "60%" /></p>
<h3 id="-6">用户列表</h3>
<p>参考前面课程，JPA 依赖 Pageable 为用户列表页做分页，默认每页展示 6 个用户，并且按照用户注册的倒序来排列，具体信息如下：</p>
<pre><code class="java language-java">@RequestMapping("/list")
public String list(Model model,@RequestParam(value = "page", defaultValue = "0") Integer page,
                   @RequestParam(value = "size", defaultValue = "6") Integer size) {
    Sort sort = new Sort(Sort.Direction.DESC, "id");
    Pageable pageable = PageRequest.of(page, size, sort);
    Page&lt;User&gt; users=userRepository.findList(pageable);
    model.addAttribute("users", users);
    return "user/list";
}
</code></pre>
<ul>
<li>@RequestParam 常用来处理简单类型的绑定，注解有三个属性：value、required 和 defaultValue；value 用来指定要传入值的 ID 名称，required 用来指示参数是否必须绑定，defaultValue 可以设置参数的默认值。</li>
</ul>
<p>前端页抽取一个公共的分页信息——page.html，页面部分信息如下：</p>
<pre><code class="html language-html">&lt;div th:if="${(users.totalPages le 10) and (users.totalPages gt 0)}" th:remove="tag"&gt;
    &lt;div th:each="pg : ${#numbers.sequence(0, users.totalPages - 1)}" th:remove="tag"&gt;
            &lt;span th:if="${pg eq users.getNumber()}" th:remove="tag"&gt;
                &lt;li class="active"&gt;&lt;span class="current_page line_height" th:text="${pg+1}"&gt;${pageNumber}&lt;/span&gt;&lt;/li&gt;
            &lt;/span&gt;
        &lt;span th:unless="${pg eq users.getNumber()}" th:remove="tag"&gt;
                &lt;li&gt;&lt;a href="#" th:href="@{${pageUrl}(page=${pg})}" th:text="${pg+1}"&gt;&lt;/a&gt;&lt;/li&gt;
            &lt;/span&gt;
    &lt;/div&gt;
&lt;/div&gt;

&lt;li th:if="${users.hasNext()}"&gt;&lt;a href="#" th:href="@{${pageUrl}(page=${users.number+1})}"&gt;下一页&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#" th:href="${users.totalPages le 0 ? pageUrl+'page=0':pageUrl+'&amp;amp;page='+(users.totalPages-1)}"&gt;尾页&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;span th:utext="'共'+${users.totalPages}+'页 / '+${users.totalElements}+' 条'"&gt;&lt;/span&gt;&lt;/li&gt;
</code></pre>
<p>page.html 页面的作用是显示主页的页码，包括首页、末页、第几页，共几页这类信息，需要根据页码的数据进行动态调整。页面中使用了 Thymeleaf 大量语法：th:if 判断、th:each 循环、th:href 链接等，分页信息主要从后端传递的 Page 对象获取。</p>
<p>然后在 list.html 页面中引入 page.html 页面分页信息。</p>
<pre><code class="html language-html">&lt;h1&gt;用户列表&lt;/h1&gt;
&lt;br/&gt;&lt;br/&gt;
&lt;div class="with:80%"&gt;
    &lt;table class="table table-hover"&gt;
        &lt;thead&gt;
         &lt;!-- 表头信息--&gt;
        &lt;tr&gt;
            &lt;th&gt;#&lt;/th&gt;
            &lt;th&gt;User Name&lt;/th&gt;
            &lt;th&gt;Password&lt;/th&gt;
            &lt;th&gt;Age&lt;/th&gt;
            &lt;th&gt;Reg Time&lt;/th&gt;
            &lt;th&gt;Edit&lt;/th&gt;
            &lt;th&gt;Delete&lt;/th&gt;
        &lt;/tr&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
        &lt;!-- 表循环展示用户信息--&gt;
        &lt;tr  th:each="user : ${users}"&gt;
            &lt;th scope="row" th:text="${user.id}"&gt;1&lt;/th&gt;
            &lt;td th:text="${user.userName}"&gt;neo&lt;/td&gt;
            &lt;td th:text="${user.passWord}"&gt;Otto&lt;/td&gt;
            &lt;td th:text="${user.age}"&gt;6&lt;/td&gt;
            &lt;td th:text="${#dates.format(user.regTime, 'yyyy/MMM/dd HH:mm:ss')}"&gt;&lt;/td&gt;
            &lt;td&gt;&lt;a th:href="@{/toEdit(id=${user.id})}"&gt;edit&lt;/a&gt;&lt;/td&gt;
            &lt;td&gt;&lt;a th:href="@{/delete(id=${user.id})}"  onclick="return confirm('确认是否删除此用户？')"  &gt;delete&lt;/a&gt;&lt;/td&gt;
        &lt;/tr&gt;
        &lt;/tbody&gt;
    &lt;/table&gt;
    &lt;!-- 引入分页内容--&gt;
    &lt;div th:include="page :: pager" th:remove="tag"&gt;&lt;/div&gt;
&lt;/div&gt;
&lt;div class="form-group"&gt;
    &lt;div class="col-sm-2 control-label"&gt;
        &lt;a href="/toAdd" th:href="@{/toAdd}" class="btn btn-info"&gt;add&lt;/a&gt;
    &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p><code>&lt;tr  th:each="user : ${users}"&gt;</code> 这里会从 Controler 层 model set 的对象去获取相关的内容，th:each 表示会循环遍历对象内容。</p>
<p>效果图如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/list.png"  width = "60%" /></p>
<h3 id="-7">修改功能</h3>
<p>点击修改功能的时候，需要带上用户的 ID 信息：</p>
<pre><code class="html language-html">&lt;td&gt;&lt;a th:href="@{/toEdit(id=${user.id})}"&gt;edit&lt;/a&gt;&lt;/td&gt;
</code></pre>
<p>后端根据用户 ID 获取用户信息，并放入 Model 中。</p>
<pre><code class="java language-java">@RequestMapping("/toEdit")
public String toEdit(Model model,Long id) {
    User user=userRepository.findById(id);
    model.addAttribute("user", user);
    return "user/userEdit";
}
</code></pre>
<p>修改页面展示用户信息，以下为 userEdit.html 页面部分内容：</p>
<pre><code class="html language-html">&lt;form class="form-horizontal"   th:action="@{/edit}" th:object="${user}"  method="post"&gt;
    &lt;!--隐藏用户 ID--&gt;
    &lt;input type="hidden" name="id" th:value="*{id}" /&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="userName" class="col-sm-2 control-label"&gt;userName&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="text" class="form-control" name="userName"  id="userName" th:value="*{userName}" placeholder="userName"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="password" class="col-sm-2 control-label" &gt;passWord&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="password" class="form-control" name="passWord" id="passWord"  th:value="*{passWord}" placeholder="passWord"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;!--错误信息--&gt;
    &lt;div class="form-group"&gt;
        &lt;label  class="col-sm-2 control-label"&gt;&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;div th:if="${errorMsg != null}"  class="alert alert-danger" role="alert" th:text="${errorMsg}"&gt;

            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;!--按钮区--&gt;
    &lt;div class="form-group"&gt;
        &lt;div class="col-sm-offset-2 col-sm-10"&gt;
            &lt;input type="submit" value="Submit" class="btn btn-info" /&gt;
            &amp;nbsp; &amp;nbsp; &amp;nbsp;
            &lt;a  th:href="@{/list}" class="btn btn-info"&gt;Back&lt;/a&gt;
        &lt;/div&gt;

    &lt;/div&gt;
&lt;/form&gt;
</code></pre>
<p>修改完成后提交到后台：</p>
<pre><code class="java language-java">@RequestMapping("/edit")
public String edit(@Valid UserParam userParam, BindingResult result,Model model) {
    String errorMsg="";
    //参数校验
    if(result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg=errorMsg + error.getCode() + "-" + error.getDefaultMessage() +";";
        }
        model.addAttribute("errorMsg",errorMsg);
        model.addAttribute("user", userParam);
        return "user/userEdit";
    }

    //复制属性保持修改后数据
    User user=new User();
    BeanUtils.copyProperties(userParam,user);
    user.setRegTime(new Date());
    userRepository.save(user);
    return "redirect:/list";
}
</code></pre>
<p>后台同样需要进行参数验证，无误后修改对应的用户信息。</p>
<p>效果图：</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/edit.png"  width = "60%" /></p>
<h3 id="-8">删除功能</h3>
<p>单击删除按钮的时候需要用户再次确认，确认后才能删除。</p>
<pre><code class="html language-html">&lt;td&gt;&lt;a th:href="@{/delete(id=${user.id})}"  onclick="return confirm('确认是否删除此用户？')"  &gt;delete&lt;/a&gt;&lt;/td&gt;
</code></pre>
<p>效果如下:</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/delete.png"  width = "60%" /></p>
<p>后端根据用户 ID 进行删除即可。</p>
<pre><code class="java language-java">@RequestMapping("/delete")
public String delete(Long id) {
    userRepository.delete(id);
    return "redirect:/list";
}
</code></pre>
<p>删除完成之后，再跳转到用户列表页。</p>
<h3 id="-9">总结</h3>
<p>用户管理功能包含了用户的增加、修改、删除、展示等功能，也是我们日常开发中最常用的四个功能。在实现用户管理功能的过程中使用了 JPA 的增加、修改、删除、查询、分页查询功能；使用了 Thymeleaf 展示用户信息，在 list 页面引入分页模板，使用了 Thymeleaf 内嵌的 dates 对日期进行了格式化；经过今天的学习较全面演练了前期的学习内容。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>