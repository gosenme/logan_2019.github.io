---
title: 精通 Spring Boot 42 讲-42
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>最后两课的内容是实践，结合前面课程的技术来做一个简单的用户管理系统，该系统包括以下功能：管理员注册、注册验证、管理员登录、管理员退出、添加用户、修改用户、删除用户、浏览用户信息等功能。</p>
<p>技术选型，使用 MongoDB 存储系统数据、使用 Filter 检查用户的登录状态、使用 Redis 管理用户 Session、数据缓存、使用 Spring Boot Mail 验证用户注册邮箱，使用 Hibernate-validator 做参数校验，使用 BootStrap 前端框架、Thymeleaf 模板，并且使用 Thymeleaf 进行页面布局。</p>
<h3 id="">功能设计</h3>
<p>首先看一下用户管理系统的业务流程图：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/usermind.png" alt="" />  </p>
<ul>
<li>访问首页，需判断用户是否登录</li>
<li>用户登录时判断是否注册，提示用户去注册</li>
<li>注册成功后，发送验证邮件</li>
<li>用户登录邮箱，点击链接验证邮箱</li>
<li>用户登录成功后，进入用户管理页面</li>
<li>用户管理页面可以对用户进行浏览，增、删、改、查等操作</li>
<li>用户可以单击“退出”按钮进行退出操作</li>
<li>每次的请求都会验证用户是否登录，如果 session 失效或者未登录会自动跳转到登录页面</li>
</ul>
<p>从以上的内容可以看出用户管理系统的主要功能，如果在日常的工作中接到这样的一个需求，会怎么设计或者开发呢？</p>
<p>本节课程的开发步骤是：</p>
<ul>
<li>开发数据库层的增、删、改功能</li>
<li>开发 Web 层代码，输出增、删、改、查的请求接口</li>
<li>页面布局、进行数据展示层的代码开发</li>
<li>结合上面前 3 步操作完成用户增、删、改、查功能</li>
<li>开发用户注册、登录、退出功能</li>
<li>注册成功发送验证邮件、单击邮件链接验证修改用户状态</li>
<li>进行 Session 管理，使用 Redis 管理用户的 Session 信息</li>
<li>添加自定义 Filter 对用户的请求进行验证</li>
<li>添加缓存、综合调试</li>
</ul>
<h3 id="-1">前期准备</h3>
<p>我们使用 MongoDB 做为数据库，需要有 MongoDB 数据库环境；使用了 Redis 管理 Session，需要有 Redis 环境；用户注册之后会发送邮件验证，需要准备邮件账户。</p>
<p><strong>添加相关依赖</strong></p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;nz.net.ultraq.thymeleaf&lt;/groupId&gt;
    &lt;artifactId&gt;thymeleaf-layout-dialect&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-data-mongodb&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-data-redis&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.apache.commons&lt;/groupId&gt;
    &lt;artifactId&gt;commons-pool2&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-cache&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-mail&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>从以上配置可以看出，我们使用 spring-boot-starter-web 组件处理 Web 层业务，使用 spring-boot-starter-thymeleaf 组件作为前端页面模板引擎，使用 spring-boot-starter-data-mongodb 组件操作 MongoDB 数据库，使用 spring-session-data-redis 组件和 Redis 交互，使用 spring-boot-starter-mail 组建处理邮件相关内容！</p>
<p><strong>配置信息</strong></p>
<p>数据库、Thymeleaf、Session 失效时间配置：</p>
<pre><code class="properties language-properties"># mongodb 配置
spring.data.mongodb.uri=mongodb://localhost:27017/manage
# 测试环境取消 thymeleaf 缓存
spring.thymeleaf.cache=false
spring.session.store-type=redis
# 设置 session 失效时间
spring.session.timeout=3600
</code></pre>
<p>Redis 配置：</p>
<pre><code class="properties language-properties"># Redis 服务器地址
spring.redis.host=192.168.0.xx
# Redis 服务器连接端口
spring.redis.port=6379
# Redis 服务器连接密码（默认为空）
spring.redis.password=
# 连接池最大连接数（使用负值表示没有限制） 默认 8
spring.redis.lettuce.pool.max-active=8
# 连接池最大阻塞等待时间（使用负值表示没有限制） 默认 -1
spring.redis.lettuce.pool.max-wait=-1
# 连接池中的最大空闲连接 默认 8
spring.redis.lettuce.pool.max-idle=8
# 连接池中的最小空闲连接 默认 0
spring.redis.lettuce.pool.min-idle=0
# 连接超时时间（毫秒）
spring.redis.timeout=0
</code></pre>
<p>邮件配置：</p>
<pre><code class="properties language-properties">spring.mail.host=smtp.126.com
spring.mail.username=youremail@126.com
spring.mail.password=yourpass
spring.mail.default-encoding=UTF-8
</code></pre>
<h3 id="-2">开发数据库层代码</h3>
<pre><code class="java language-java">public interface UserRepository  extends MongoRepository&lt;User, String&gt; {
    Page&lt;User&gt; findAll(Pageable pageable);
    Optional&lt;User&gt; findById(String id);
    User findByUserNameOrEmail(String userName, String email);
    User findByUserName(String userName);
    User findByEmail(String email);
    void deleteById(String id);
}
</code></pre>
<p>根据前期 MongoDB 的课程我们知道，集成 MongoRepository 会自动实现很多内置的数据库操作方法。</p>
<h3 id="web">Web 层用户管理</h3>
<p>Param 设计，在项目中创建了 param 包用来存放所有请求过程中的参数处理，如登录、注册、用户等，根据不容的请求来设计不同的请求对象。</p>
<p><strong>分页展示用户列表信息</strong></p>
<pre><code class="java language-java">@RequestMapping("/list")
public String list(Model model,@RequestParam(value = "page", defaultValue = "0") Integer page,
                   @RequestParam(value = "size", defaultValue = "6") Integer size) {
    Sort sort = new Sort(Sort.Direction.DESC, "id");
    Pageable pageable = PageRequest.of(page, size, sort);
    Page&lt;User&gt; users=userRepository.findAll(pageable);
    model.addAttribute("users", users);
    logger.info("user list "+ users.getContent());
    return "user/list";
}
</code></pre>
<p><strong>添加用户</strong></p>
<pre><code class="java language-java">public String add(@Valid UserParam userParam,BindingResult result, ModelMap model) {
    String errorMsg="";
    if(result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg=errorMsg + error.getCode() + "-" + error.getDefaultMessage() +";";
        }
        model.addAttribute("errorMsg",errorMsg);
        return "user/userAdd";
    }
    User u= userRepository.findByUserNameOrEmail(userParam.getUserName(),userParam.getEmail());
    if(u!=null){
        model.addAttribute("errorMsg","用户已存在!");
        return "user/userAdd";
    }
    User user=new User();
    BeanUtils.copyProperties(userParam,user);
    user.setRegTime(new Date());
    user.setUserType("user");
    userRepository.save(user);
    return "redirect:/list";
}
</code></pre>
<p>首先验证参数是否正确，再次查询此用户名或者邮箱是否已经添加过，校验无误后将用户信息保存到数据库中，页面跳转到用户列表页。</p>
<p><strong>修改用户</strong></p>
<pre><code class="java language-java">public String edit(@Valid UserParam userParam, BindingResult result,ModelMap model) {
    String errorMsg="";
    if(result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg=errorMsg + error.getCode() + "-" + error.getDefaultMessage() +";";
        }
        model.addAttribute("errorMsg",errorMsg);
        model.addAttribute("user", userParam);
        return "user/userEdit";
    }

    User user=userRepository.findById(userParam.getId()).get();
    BeanUtils.copyProperties(userParam,user);
    user.setRegTime(new Date());
    userRepository.save(user);
    return "redirect:/list";
}
</code></pre>
<p>和添加用户的业务逻辑大体相同，最主要的是需要首先查询此用户信息，再根据前端内容进行修改。</p>
<p><strong>删除用户</strong></p>
<pre><code class="java language-java">public String delete(String id) {
    userRepository.deleteById(id);
    return "redirect:/list";
}
</code></pre>
<p>删除用户比较简单，直接调用 Repository.delete() 方法即可。</p>
<h3 id="-3">前端页面</h3>
<h4 id="-4">用户列表</h4>
<pre><code class="html language-html">&lt;h1&gt;用户列表&lt;/h1&gt;
&lt;br/&gt;&lt;br/&gt;
&lt;div class="with:80%"&gt;
    &lt;table class="table table-hover"&gt;
        &lt;thead&gt;
        &lt;tr&gt;
            &lt;th&gt;User Name&lt;/th&gt;
            &lt;th&gt;Email&lt;/th&gt;
            &lt;th&gt;User Type&lt;/th&gt;
            &lt;th&gt;Age&lt;/th&gt;
            &lt;th&gt;Reg Time&lt;/th&gt;
            &lt;th&gt;Edit&lt;/th&gt;
            &lt;th&gt;Delete&lt;/th&gt;
        &lt;/tr&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
        &lt;tr  th:each="user : ${users}"&gt;
            &lt;td th:text="${user.userName}"&gt;neo&lt;/td&gt;
            &lt;td th:text="${user.email}"&gt;neo@126.com&lt;/td&gt;
            &lt;td th:text="${user.userType}"&gt;User&lt;/td&gt;
            &lt;td th:text="${user.age}"&gt;6&lt;/td&gt;
            &lt;td th:text="${#dates.format(user.regTime, 'yyyy-MM-dd HH:mm:ss')}"&gt;&lt;/td&gt;
            &lt;td&gt;&lt;a th:href="@{/toEdit(id=${user.id})}"  th:if="${user.userType !='manage'}" &gt;edit&lt;/a&gt;&lt;/td&gt;
            &lt;td&gt;&lt;a th:href="@{/delete(id=${user.id})}"  onclick="return confirm('确认是否删除此用户？')"  th:if="${user.userType !='manage'}" &gt;delete&lt;/a&gt;&lt;/td&gt;
        &lt;/tr&gt;
        &lt;/tbody&gt;
    &lt;/table&gt;
    &lt;div th:include="page :: pager" th:remove="tag"&gt;&lt;/div&gt;
&lt;/div&gt;
&lt;div class="form-group"&gt;
    &lt;div class="col-sm-2 control-label"&gt;
        &lt;a href="/toAdd" th:href="@{/toAdd}" class="btn btn-info"&gt;添加&lt;/a&gt;
    &lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>效果图如下:</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/user_list.png" alt="" /></p>
<p>可以看出此页面的功能主要使用 Thymeleaf 语法循环遍历展示用户信息，并且给出修改和删除的链接；使用了 th:if 来根据用户的不同状态来选择是否显示编辑和删除链接；页面中有这么一句：<code>&lt;div th:include="page :: pager" th:remove="tag"&gt;&lt;/div&gt;</code>，其实就是引入了封装好的分页信息 page.html，前面课程已经介绍了分页信息这里不再多说。</p>
<h4 id="-5">添加用户</h4>
<pre><code class="html language-html">&lt;form class="form-horizontal"   th:action="@{/add}"  method="post"&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="userName" class="col-sm-2 control-label"&gt;userName&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="text" class="form-control" name="userName"  id="userName" placeholder="userName"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="form-group"&gt;
        &lt;label for="email" class="col-sm-2 control-label" &gt;email&lt;/label&gt;
        &lt;div class="col-sm-10"&gt;
            &lt;input type="text" class="form-control" name="email" id="email" placeholder="email"/&gt;
        &lt;/div&gt;
    &lt;/div&gt;

...

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
<p>主要是输入用户相关信息，并提供提交、重置、返回的功能。</p>
<p>效果图如下:</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/user_add.png"  width = "70%" /></p>
<p>修改页面和添加类似，大家可以参考示例代码。</p>
<h3 id="-6">注册、登录、退出</h3>
<h4 id="-7">注册</h4>
<p>注册的用户类型为 manage，后台添加的用户类型为 user，两者区分开来方便后续管理。</p>
<p>注册页面代码：</p>
<pre><code class="html language-html">&lt;div class="with:60%"&gt;
    &lt;div style="margin: 10px 90px;"&gt;已有账户？直接&lt;a  th:href="@{/toLogin}"&gt;登录&lt;/a&gt;&lt;/div&gt;

    &lt;form class="form-horizontal"   th:action="@{/register}"  method="post" &gt;
        &lt;div class="form-group"&gt;`
            &lt;label for="userName" class="col-sm-2 control-label"&gt;User Name&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;input type="text" class="form-control" name="userName"  id="userName"  placeholder="enter userName"/&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="form-group"&gt;`
            &lt;label for="email" class="col-sm-2 control-label"&gt;email&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;input type="text" class="form-control" name="email"  id="email" placeholder="enter email"/&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="form-group"&gt;
            &lt;label for="password" class="col-sm-2 control-label" &gt;Password&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;input type="password" class="form-control" name="password" id="password" placeholder="enter password"/&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
            &lt;label   class="col-sm-2 control-label"&gt;&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;div th:if="${errorMsg != null}"  class="alert alert-danger" role="alert" th:text="${errorMsg}"&gt;

                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
            &lt;div class="col-sm-offset-2 col-sm-6"&gt;
                &lt;input type="submit" value="Submit" class="btn btn-info" /&gt;
                &amp;nbsp; &amp;nbsp; &amp;nbsp;
                &lt;input type="reset" value="Reset" class="btn btn-info" /&gt;

            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/form&gt;
&lt;/div&gt;
</code></pre>
<p>效果图如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/register.png"  width = "50%" /></p>
<p>后端处理逻辑如下：</p>
<pre><code class="java language-java">@RequestMapping("/register")
public String register(@Valid RegisterParam registerParam, BindingResult result, ModelMap model) {
    logger.info("register param"+ registerParam.toString());
    String errorMsg = "";
    if (result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg = errorMsg + error.getCode() + "-" + error.getDefaultMessage() + ";";
        }
        model.addAttribute("errorMsg", errorMsg);
        return "register";
    }
    UserEntity u = userRepository.findByUserNameOrEmail(registerParam.getUserName(), registerParam.getEmail());
    if (u != null) {
        model.addAttribute("errorMsg", "用户已存在!");
        return "register";
    }
    UserEntity user = new UserEntity();
    BeanUtils.copyProperties(registerParam, user);
    user.setRegTime(new Date());
    user.setUserType("manage");
    user.setState("unverified");
    userRepository.save(user);
    logger.info("register user "+ user.toString());
    return "login";
}
</code></pre>
<p>判断参数输入是否正确，用户是否已经存在，验证完毕后将用户信息存入数据库，并跳转到登录页面。</p>
<h4 id="-8">登录</h4>
<p>登录页面代码：</p>
<pre><code class="html language-html">&lt;div class="with:60%"&gt;
    &lt;div style="margin: 10px 90px;"&gt;没有账户？先去&lt;a  th:href="@{/toRegister}"&gt;注册&lt;/a&gt;&lt;/div&gt;

    &lt;form class="form-horizontal"   th:action="@{/login}"  method="post" &gt;
        &lt;div class="form-group"&gt;`
            &lt;label for="loginName" class="col-sm-2 control-label"&gt;Login Name&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;input type="text" class="form-control" name="loginName"  id="loginName" placeholder="enter userName or email"/&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="form-group"&gt;
            &lt;label for="password" class="col-sm-2 control-label" &gt;Password&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;input type="password" class="form-control" name="password" id="password" placeholder="enter password"/&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
            &lt;label   class="col-sm-2 control-label"&gt;&lt;/label&gt;
            &lt;div class="col-sm-6"&gt;
                &lt;div th:if="${errorMsg != null}"  class="alert alert-danger" role="alert" th:text="${errorMsg}"&gt;

                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
            &lt;div class="col-sm-offset-2 col-sm-6"&gt;
                &lt;input type="submit" value="Submit" class="btn btn-info" /&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/form&gt;
&lt;/div&gt;
</code></pre>
<p>效果图如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/login.png"  width = "60%" /></p>
<p>后端处理逻辑如下：</p>
<pre><code class="java language-java">@RequestMapping("/login")
public String login(@Valid LoginParam loginParam, BindingResult result, ModelMap model, HttpServletRequest request) {
    String errorMsg = "";
    if (result.hasErrors()) {
        List&lt;ObjectError&gt; list = result.getAllErrors();
        for (ObjectError error : list) {
            errorMsg = errorMsg + error.getCode() + "-" + error.getDefaultMessage() + ";";
        }
        model.addAttribute("errorMsg", errorMsg);
        return "login";
    }
    UserEntity user = userRepository.findByUserName(loginParam.getLoginName());
    if (user == null) {
        user = userRepository.findByEmail(loginParam.getLoginName());
    }
    if (user == null) {
        model.addAttribute("errorMsg", "用户名不存在!");
        return "login";
    } else if (!user.getPassword().equals(loginParam.getPassword())) {
        model.addAttribute("errorMsg", "密码错误！");
        return "login";
    }

    request.getSession().setAttribute(WebConfiguration.LOGIN_KEY, user.getId());
    request.getSession().setAttribute(WebConfiguration.LOGIN_USER, user);
    return "redirect:/list";
}
</code></pre>
<p>首先根据用户名或者用户邮件去查找此用户，如果用户不存在返回并给出提示；如果找到用户判断用户密码是否正确，如正确，将用户信息存入 Session 中，并跳转到用户列表页。</p>
<h4 id="-9">退出</h4>
<p>退出比较简单只需要清空 Session 中的用户信息即可：</p>
<pre><code class="java language-java">@RequestMapping("/loginOut")
public String loginOut(HttpServletRequest request) {
    request.getSession().removeAttribute(WebConfiguration.LOGIN_KEY);
    request.getSession().removeAttribute(WebConfiguration.LOGIN_USER);
    return "login";
}
</code></pre>
<blockquote>
  <p>下一课我们继续介绍用户管理系统的设计研发。</p>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>