---
title: 案例上手 Spring 全家桶-41
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们学习了 Spring Boot 整合 JdbcTemplate 的具体操作，完成了持久层的集成，我说过 JdbcTemplate 相比于 MyBatis 灵活性要差一些，但是其优势在于是 Spring 框架自带组件，所以额外整合，开箱即用非常方便。而 MyBatis 框架并不是 Spring 生态中的模块，是第三方框架，要集成到 Spring 应用中必然需要进行一系列的整合配置。</p>
<p>回顾我们之前的 SSM 整合课程，实际上就是将 MyBatis 和 Spring 进行整合，需要进行大量的配置，spring.xml 代码如下所示。</p>
<pre><code class="xml language-xml">&lt;!-- 配置 C3P0 数据源 --&gt;
&lt;bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource"&gt;
  &lt;property name="user" value="root"&gt;&lt;/property&gt;
  &lt;property name="password" value="root"&gt;&lt;/property&gt;
  &lt;property name="driverClass" value="com.mysql.cj.jdbc.Driver"&gt;&lt;/property&gt;
  &lt;property name="jdbcUrl" value="jdbc:mysql://localhost:3306/easybuy?useUnicode=true&amp;amp;characterEncoding=UTF-8"&gt;&lt;/property&gt;
  &lt;property name="initialPoolSize" value="5"&gt;&lt;/property&gt;
  &lt;property name="maxPoolSize" value="10"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;!-- 配置 MyBatis SqlSessionFactory --&gt;
&lt;bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
  &lt;!-- 数据源 --&gt;
  &lt;property name="dataSource" ref="dataSource"&gt;&lt;/property&gt;
  &lt;!-- 指定 MyBatis Mapper 文件的位置 --&gt;
  &lt;property name="mapperLocations" value="classpath:com/southwind/repository/*.xml"&gt;&lt;/property&gt;
  &lt;!-- 指定 MyBatis 配置文件 --&gt;
  &lt;property name="configLocation" value="classpath:mybatis.xml"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;!-- 扫描 MyBatis Mapper 接口 --&gt;
&lt;bean class="org.mybatis.spring.mapper.MapperScannerConfigurer"&gt;
  &lt;property name="basePackage" value="com.southwind.repository"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager"&gt;
  &lt;property name="dataSource" ref="dataSource"&gt;&lt;/property&gt;
&lt;/bean&gt;
</code></pre>
<p>非常麻烦，但是你不用担心，在 Spring Boot 工程中，开发者无需再去进行手动整合配置，Spring Boot 会自动完成 MyBatis 的集成配置，并且这套自动配置方案是由 MyBatis 提供的，Spring Boot 只需接入即可，省去了 XML 文件中繁琐的配置，开发者只需要在 application 文件中添加个性化配置，就可以实现 MyBatis 的开箱即用，非常方便。</p>
<p>这节课我们就来学习 Spring Boot 整合 MyBatis 的具体实现，首先简单回顾一下 MyBatis 框架。</p>
<p>MyBatis 是一款优秀的 ORM 框架，原名叫 iBatis，包括现在 MyBaits 源码中包的命名还是沿用 ibatis。MyBatis 可以简单理解为对 JDBC 的封装，简化了配置和结果集的解析，开发者只需要调用接口方法即可完成 CRUD 操作，同时 MyBatis 支持定制化动态 SQL，使得代码编写变得更加高效简洁，是当下主流的持久层框架。</p>
<p>了解完 MyBatis 的基本知识，接下来我们动手完成 Spring Boot 和 MyBatis 的整合。</p>
<p>1. 创建 Maven 工程，pom.xml 中添加相关依赖，mybatis-spring-boot-starter 为 Spring Boot 整合 MyBatis 的依赖，通过 groupId——org.mybatis.spring.boot 可以得出结论，整合相关组件是由 MyBatis 官方提供的，而非 Spring。</p>
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
    &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
    &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
    &lt;version&gt;1.3.1&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;mysql&lt;/groupId&gt;
    &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
    &lt;version&gt;8.0.15&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
    &lt;artifactId&gt;lombok&lt;/artifactId&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 创建数据表。</p>
<pre><code class="sql language-sql">create table student(
  id int primary key auto_increment,
  name varchar(11),
  score double,
  birthday date
);
</code></pre>
<p>预先向数据库添加 3 条记录，如下所示。</p>
<p><img src="https://images.gitbook.cn/4ed78f70-c1d7-11e9-9969-976e2ac29eb2" width = "60%" /></p>
<p>3. 创建数据表对应的实体类。</p>
<pre><code class="java language-java">@Data
public class Student {
    private Long id;
    private String name;
    private Double score;
    private Date birthday;
}
</code></pre>
<p>4. 创建 StudentRepository，定义基本的 CRUD 接口。</p>
<pre><code class="java language-java">public interface StudentRepository {
    public List&lt;Student&gt; findAll();
    public Student findById(Long id);
    public int save(Student student);
    public int update(Student student);
    public int deleteById(Long id);
}
</code></pre>
<p>5. 在 /resources/mapping 路径下创建 StudentRepository.xml，作为 StudentRepository 的配套 Mapper 文件，定义每个接口方法对应的 SQL 语句以及结果集解析策略。</p>
<p><img src="https://images.gitbook.cn/5dc064d0-c1d7-11e9-8621-c1fbe3716b21" width = "50%" /></p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.StudentRepository"&gt;
    &lt;select id="findAll" resultType="Student"&gt;
        select * from student
    &lt;/select&gt;

    &lt;select id="findById" parameterType="java.lang.Long" resultType="Student"&gt;
        select * from student where id = #{id}
    &lt;/select&gt;

    &lt;insert id="save" parameterType="Student"&gt;
        insert into student(name,score,birthday) values(#{name},#{score},#{birthday})
    &lt;/insert&gt;

    &lt;update id="update" parameterType="Student"&gt;
        update student set name = #{name},score = #{score},birthday = #{birthday} where id = #{id}
    &lt;/update&gt;

    &lt;delete id="deleteById" parameterType="java.lang.Long"&gt;
        delete from student where id = #{id}
    &lt;/delete&gt;
&lt;/mapper&gt;
</code></pre>
<p>6. 创建 StudentHandler，注入 StudentRepository。</p>
<pre><code class="java language-java">@RestController
public class StudentHandler {
    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("/findAll")
    public List&lt;Student&gt; findAll(){
        return studentRepository.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student get(@PathVariable("id") Long id){
        return studentRepository.findById(id);
    }

    @PostMapping("/save")
    public int save(@RequestBody Student student){
        return studentRepository.save(student);
    }

    @PutMapping("/update")
    public int update(@RequestBody Student student){
        return studentRepository.update(student);
    }

    @DeleteMapping("/deleteById/{id}")
    public int deleteById(@PathVariable("id") Long id){
        return studentRepository.deleteById(id);
    }

}
</code></pre>
<p>7. 创建配置文件 application.yml，添加 MySQL 数据源信息以及 MyBatis 的相关配置。</p>
<pre><code class="yaml language-yaml">spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&amp;characterEncoding=UTF-8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
mybatis:
  mapper-locations: classpath:/mapping/*.xml
  type-aliases-package: com.southwind.entity
</code></pre>
<p>8. 创建启动类 Application，需要注意，这里多了一个类注解 @MapperScan("com.southwind.repository")，这个注解用来干什么？我们知道 MyBatis 并非 Spring 生态下的模块，Spring 并不会自动管理 MyBatis 相关对象的生命周期，因此我们需要手动配置，将 MyBatis 相关对象交给 Spring 容器来管理，这里是通过扫包的方式，@MapperScan 注解的作用就是将目标包下的类全部扫描到 Spring 容器中，所以这里需要指定 MyBatis Mapper 接口所在的包 com.southwind.repository。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>9. 启动 Application，使用 Postman 工具来测试相关接口，结果如下所示。</p>
<ul>
<li>findAll</li>
</ul>
<p><img src="https://images.gitbook.cn/72d4d130-c1d7-11e9-9166-bdb140d6509f" width = "70%" /></p>
<ul>
<li>findById</li>
</ul>
<p><img src="https://images.gitbook.cn/7a677240-c1d7-11e9-97a8-35dcf136a505" width = "70%" /></p>
<ul>
<li>save</li>
</ul>
<p><img src="https://images.gitbook.cn/852e6350-c1d7-11e9-97a8-35dcf136a505" width = "60%" /></p>
<p>添加完成，测试 findAll，可以看到新数据已经添加成功。</p>
<p><img src="https://images.gitbook.cn/91727e80-c1d7-11e9-8621-c1fbe3716b21" width = "60%" /></p>
<ul>
<li>update</li>
</ul>
<p><img src="https://images.gitbook.cn/9965b620-c1d7-11e9-9969-976e2ac29eb2" width = "60%" /></p>
<p>修改完成，测试 findAll，可以看到数据已经修改成功。</p>
<p><img src="https://images.gitbook.cn/a3851c90-c1d7-11e9-8621-c1fbe3716b21" width = "60%" /></p>
<ul>
<li>deleteById</li>
</ul>
<p><img src="https://images.gitbook.cn/ae76c720-c1d7-11e9-97a8-35dcf136a505" width = "65%" /></p>
<p>删除完成，测试 findAll，可以看到数据已经删除成功。</p>
<p><img src="https://images.gitbook.cn/b94d4890-c1d7-11e9-8621-c1fbe3716b21" width = "65%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们学习了 Spring Boot 整合 MyBatis 的具体操作，MyBatis 作为当前主流的 ORM 框架，是很多 Java 开发者的首选，所以如何在基于 Sprint Boot 搭建的 Spring 应用中集成 MyBatis 就是我们必须掌握的技能，Spring Boot 很好地集成了 MyBatis，开发者无需额外进行配置，开箱即用。</p>
<p><a href="https://github.com/southwind9801/gcspringbootmybatis.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>