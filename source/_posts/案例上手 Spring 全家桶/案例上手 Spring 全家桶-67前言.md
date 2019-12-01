---
title: 案例上手 Spring 全家桶-67
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本节课我们来实现服务提供者 user，user 为系统提供用户相关服务，包括添加用户、查询用户、删除用户，具体实现如下所示。</p>
<p>1. 在父工程下创建一个 Module，命名为 user，pom.xml 添加相关依赖，user 需要访问数据库，所以集成 MyBatis 相关依赖，配置文件从 Git 仓库拉取，添加配置中 Spring Cloud Config 相关依赖。</p>
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
      name: user #对应的配置文件名称
      label: master #Git 仓库分支名
      discovery:
        enabled: true
        serviceId: configserver #连接的配置中心名称
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>3. 在 java 目录下创建启动类 UserApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class UserApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserApplication.class,args);
    }
}
</code></pre>
<p>4. 接下来为服务提供者 user 集成 MyBatis 环境，首先在 Git 仓库配置文件 user.yml 中添加相关信息。</p>
<pre><code class="yaml language-yaml">server:
  port: 8050
spring:
  application:
    name: user
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
<p>5. 在 java 目录下创建 entity 文件夹，新建 User 类对应数据表 t_user。</p>
<pre><code class="java language-java">@Data
public class User {
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
<p>6. 新建 UserVO 类为 layui 框架提供封装类。</p>
<pre><code class="java language-java">@Data
public class UserVO {
    private int code;
    private String msg;
    private int count;
    private List&lt;User&gt; data;
}
</code></pre>
<p>7. 在 java 目录下创建 repository 文件夹，新建 UserRepository 接口，定义相关业务方法。</p>
<pre><code class="java language-java">public interface UserRepository {
    public List&lt;User&gt; findAll(int index, int limit);
    public int count();
    public void save(User user);
    public void deleteById(long id);
}
</code></pre>
<p>8. 在 resources 目录下创建 mapping 文件夹，存放 Mapper.xml，新建 UserRepository.xml，编写 UserRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.UserRepository"&gt;
    &lt;select id="findAll" resultType="User"&gt;
        select * from t_user order by id limit #{param1},#{param2}
    &lt;/select&gt;

    &lt;select id="count" resultType="int"&gt;
        select count(*) from t_user;
    &lt;/select&gt;

    &lt;insert id="save" parameterType="User"&gt;
        insert into t_user(username,password,nickname,gender,telephone,registerdate,address) values(#{username},#{password},#{nickname},#{gender},#{telephone},#{registerdate},#{address})
    &lt;/insert&gt;

    &lt;delete id="deleteById" parameterType="long"&gt;
        delete from t_user where id = #{id}
    &lt;/delete&gt;
&lt;/mapper&gt;
</code></pre>
<p>9. 新建 UserHandler，将 UserRepository 通过 @Autowired 注解进行注入，完成相关业务逻辑。</p>
<pre><code class="java language-java">@RestController
@RequestMapping("/user")
public class UserHandler {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/findAll/{page}/{limit}")
    public UserVO findAll(@PathVariable("page") int page, @PathVariable("limit") int limit){
        UserVO userVO = new UserVO();
        userVO.setCode(0);
        userVO.setMsg("");
        userVO.setCount(userRepository.count());
        userVO.setData(userRepository.findAll((page-1)*limit,limit));
        return userVO;
    }

    @PostMapping("/save")
    public void save(@RequestBody User user){
        user.setRegisterdate(new Date());
        userRepository.save(user);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        userRepository.deleteById(id);
    }
}
</code></pre>
<p>10. 依次启动注册中心、configserver、UserApplication，使用 Postman 测试该服务的相关接口，如图所示。</p>
<p><img src="https://images.gitbook.cn/14a6ff60-dd58-11e9-aaec-b5744b419935" alt="1" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了项目实战 user 模块的搭建，作为一个服务提供者，user 为整个系统提供用户服务，包括添加用户、查询用户、删除用户。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请单击这里下载源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>