---
title: 案例上手 Spring 全家桶-64
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本节课我们来实现服务提供者 account，account 为系统提供所有的账户相关业务，包括用户和管理员登录、退出，具体实现如下所示。</p>
<p>1. 在父工程下创建建一个 Module，命名为 account，pom.xml 添加相关依赖，account 需要访问数据库，因此要添加 MyBatis 相关依赖，同时配置文件从 Git 仓库拉取，所以还要添加 Spring Cloud Config 相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;!-- eurekaclient --&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
        &lt;version&gt;2.0.0.RELEASE&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!-- MyBatis --&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
        &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
        &lt;version&gt;1.3.0&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!-- MySQL 驱动 --&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;mysql&lt;/groupId&gt;
        &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
        &lt;version&gt;8.0.11&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!-- 配置中心 --&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 在 resources 目录下创建 bootstrap.yml，在该文件中配置拉取 Git 仓库相关配置文件的信息。</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: account #对应的配置文件名称
      label: master #Git 仓库分支名
      discovery:
        enabled: true
        serviceId: configserver #连接的配置中心名称
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>3. 在 java 目录下创建启动类 AccountApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
public class AccountApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountApplication.class,args);
    }
}
</code></pre>
<p>4. 接下来为服务提供者 account 集成 MyBatis 环境，首先在 Git 仓库配置文件 account.yml 中添加相关信息。</p>
<pre><code class="yaml language-yaml">server:
  port: 8010
spring:
  application:
    name: account
  datasource:
    name: orderingsystem
    url: jdbc:mysql://localhost:3306/orderingsystem?useUnicode=true&amp;characterEncoding=UTF-8
    username: root
    password: root
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
mybatis:
  mapper-locations: classpath:mapping/*.xml
  type-aliases-package: com.southwind.entity
</code></pre>
<p>5. 在 java 目录下创建 entity 文件夹，新建 Account 类。</p>
<pre><code class="java language-java">@Data
public class Account {
    private long id;
    private String username;
    private String password;
    private String nickname;
    private String gender;
    private String telephone;
    private Date registerdate;
    private String address;
}
</code></pre>
<p>6. 新建 User 类继承 Account 类，对应数据表 t_user。</p>
<pre><code class="java language-java">@Data
public class User extends Account{

}
</code></pre>
<p>7. 新建 Admin 类继承 Account 类，对应数据表 t_admin。</p>
<pre><code class="java language-java">@Data
public class Admin extends Account{

}
</code></pre>
<p>8. 在 java 目录下创建 repository 文件夹，新建 UserRepository 接口。</p>
<pre><code class="java language-java">public interface UserRepository {
    public User login(String username,String password);
}
</code></pre>
<p>9. 新建 AdminRepository 接口。</p>
<pre><code class="java language-java">public interface AdminRepository {
    public Admin login(String username,String password);
}
</code></pre>
<p>10. 在 resources 目录下创建 mapping 文件夹，存放 Mapper.xml，新建 UserRepository.xml，编写 UserRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.UserRepository"&gt;
    &lt;select id="login" resultType="User"&gt;
        select * from t_user where username = #{param1} and password = #{param2}
    &lt;/select&gt;
&lt;/mapper&gt;
</code></pre>
<p>11. 新建 AdminRepository.xml，编写 AdminRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.AdminRepository"&gt;
    &lt;select id="login" resultType="Admin"&gt;
        select * from t_admin where username = #{param1} and password = #{param2}
    &lt;/select&gt;
&lt;/mapper&gt;
</code></pre>
<p>12. 将 Mapper 注入，在启动类添加注解 @MapperScan("com.southwind.repository")。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class AccountApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountApplication.class,args);
    }
}
</code></pre>
<p>13. 新建 AccountHandler，将 UserRepository 和 AdminRepository 通过 @Autowired 注解进行注入，完成相关业务逻辑。</p>
<pre><code class="java language-java">@RestController
@RequestMapping("/account")
public class AccountHandler {

    @Autowired
    private UserRepository userRepository;
    @Autowired
    private AdminRepository adminRepository;

    @GetMapping("/login/{username}/{password}/{type}")
    public Account login(@PathVariable("username") String username,@PathVariable("password") String password,@PathVariable("type") String type){
        Account account = null;
        switch (type){
            case "user":
                account = userRepository.login(username, password);
                break;
            case "admin":
                account = adminRepository.login(username, password);
                break;
        }
        return account;
    }
}
</code></pre>
<p>14. 依次启动注册中心、configserver、AccountApplication，使用 Postman 测试该服务的相关接口，如图所示。</p>
<p><img src="https://images.gitbook.cn/84676cc0-dd55-11e9-9cc8-a572519b0723" alt="1" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了项目实战 account 模块的搭建，作为一个服务提供者，account 为整个系统提供账户服务，包括用户和管理员登录。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请单击这里下载源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>