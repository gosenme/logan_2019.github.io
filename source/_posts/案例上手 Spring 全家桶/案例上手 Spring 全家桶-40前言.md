---
title: 案例上手 Spring 全家桶-40
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>前面的课程我们已经学会了如何使用 Spring Boot 整合视图层技术，我推荐大家使用 Thymeleaf，因为它是目前的趋势，但是仅有视图层技术是远远不够的，我们知道一个完整的 Web 应用由三大部分组成，分别是客户端、Web 服务、数据库，如下图所示。</p>
<p><img src="https://images.gitbook.cn/8e099be0-c1d5-11e9-8621-c1fbe3716b21" alt="WX20190614-112447@2x" /></p>
<p>Spring Boot + JSP 或者 Spring Boot + Thymeleaf 只是完成了这个架构的前半部分，即客户端和 Web Server 的组合，还有后半部分需要我们去处理，即 Web Server 对数据库的持久化操作，这部分其实更为重要，我们知道一个 Web 应用最有价值的资源不是客户端，也不是 Web 服务，而是数据。</p>
<p>你可以设想一下，电商平台的前端交互或者后端服务都是可以根据需求随时调整重构的，但是如果用户数据丢失，那将是毁灭性打击，所以数据才是一个应用的重中之重，这就是为什么会有删库跑路的段子，你听说过删代码跑路的段子吗？没有吧，所以数据的重要性可见一斑。</p>
<p>从这节课开始我们来学习 Spring Boot 整合持久层的具体操作，我们会讲解五种持久层技术，分别是 JdbcTemplate、MyBatis、Spring Data JPA、Spring Data Redis、Spring Data MongoDB，对应 MySQL、Redis、MongoDB 数据库，干货满满，话不多说，直接开干，首先学习 Spring Boot 整合 JdbcTemplate。</p>
<p>JdbcTemplate 是 Spring 自带的 JDBC 模版组件，底层实现了对 JDBC 的封装，用法与 MyBatis 类似，需要开发者自定义 SQL 语句，JdbcTemplate 帮助我们完成数据库连接，SQL 执行，以及结果集的封装。</p>
<p>但是它的不足之处是灵活性不如 MyBatis，因为 MyBatis 的 SQL 语句都是定义在 XML 文件中的，更有利于维护和扩展，而 JdbcTemplate 是以硬编码的方式将 SQL 直接写在 Java 代码中的，不利于扩展维护。</p>
<p>虽有不足，但整体来讲使用 JdbcTemplate 还是非常方便的，因为是 Spring 自带组件，所以开发者不需要关注它的生命周期，直接从 Spring 容器中获取即可使用，具体操作如下所示。</p>
<p>1. 创建 Maven 工程，pom.xml 中添加相关依赖，spring-boot-starter-jdbc 是 JdbcTemplate 的相关依赖，同时我们这里使用的是 MySQL 数据库，因此还需要添加 MySQL 驱动依赖 mysql-connector-java。</p>
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
    &lt;artifactId&gt;spring-boot-starter-jdbc&lt;/artifactId&gt;
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
<p><img src="https://images.gitbook.cn/27841340-c1d6-11e9-9166-bdb140d6509f" width = "50%" /></p>
<p>3. 创建实体类。</p>
<pre><code class="java language-java">@Data
public class Student {
    private Long id;
    private String name;
    private Double score;
    private Date birthday;
}
</code></pre>
<p>4. 创建 StudentRepository。</p>
<pre><code class="java language-java">public interface StudentRepository {
    public List&lt;Student&gt; findAll();
    public Student findById(Long id);
    public int save(Student student);
    public int update(Student student);
    public int deleteById(Long id);
}
</code></pre>
<p>5. 创建实现类 StudentRepositoryImpl 实现上面定义的 StudentRepository 接口，直接通过 @Autowire 注解将 Spring 创建好的 JdbcTemplate 实例对象注入即可。</p>
<p>JdbcTemplate 对基本的 CRUD 操作提供了良好的支持，通过调用 query 和 update 方法即可完成操作，其中 query 是用来做查询操作的，增加、删除、修改的操作都是通过调用 update 方法来完成。</p>
<h4 id="query">query</h4>
<p>query 相关方法很多，我们这里主要说两个，第一个是 <code>query(String sql, RowMapper&lt;T&gt; rowMapper)</code>，该方法用来查询一组数据，并封装成一个集合对象，具体定义如下所示。</p>
<pre><code class="java language-java">public &lt;T&gt; List&lt;T&gt; query(String sql, RowMapper&lt;T&gt; rowMapper) throws DataAccessException {
  return (List)result(this.query((String)sql, (ResultSetExtractor)(new RowMapperResultSetExtractor(rowMapper))));
}
</code></pre>
<p>两个参数 sql 和 rch，sql 就不必再解释了，重点来说说 RowMapper，它是一个接口，作用是解析结果集，将 JDBC 查询出的 ResultSet 对象转换成对应的 Java 对象，我们在调用方法的时候需要指定目标类的结构，如下所示。</p>
<pre><code class="java language-java">jdbcTemplate.query("select * from student",new BeanPropertyRowMapper&lt;Student&gt;(Student.class));
</code></pre>
<p>这段代码表示将 "select * from student" 的查询结果封装成一个 Student 的实例化对象集合，很显然 BeanPropertyRowMapper 是 RowMapper 接口的一个实现类。</p>
<p>第二个方法是 <code>queryForObject(String sql, @Nullable Object[] args, RowMapper&lt;T&gt; rowMapper)</code>，该方法用来查询一条数据，并封装成一个 Java 对象，方法定义如下所示。</p>
<pre><code class="java language-java">@Nullable
public &lt;T&gt; T queryForObject(String sql, @Nullable Object[] args, RowMapper&lt;T&gt; rowMapper) throws DataAccessException {
  List&lt;T&gt; results = (List)this.query((String)sql, (Object[])args, (ResultSetExtractor)(new RowMapperResultSetExtractor(rowMapper, 1)));
  return DataAccessUtils.nullableSingleResult(results);
}
</code></pre>
<p>相比于 <code>query(String sql, RowMapper&lt;T&gt; rowMapper)</code>，该方法多了一个参数 Object[] args，相信你已经猜到了这个参数的作用，没错，就是用来做条件查询的，因为条件不确定，有可能是一个也可能是多个，所以这里定义为数组，满足了参数的可变性，具体使用如下所示。</p>
<pre><code class="java language-java">jdbcTemplate.queryForObject("select * from student where id = ?",new Object[]{id},new BeanPropertyRowMapper&lt;Student&gt;(Student.class));
</code></pre>
<p>这段代码表示将 "select * from student where id = 1" 的查询结果封装成一个 Student 的实例化对象。</p>
<h4 id="update">update</h4>
<p>说完了 query 方法，接下来我们学习 update，增加、删除、修改的操作都可以调用这个方法，具体定义如下所示。</p>
<pre><code class="java language-java">public int update(String sql, @Nullable Object... args) throws DataAccessException {
  return this.update(sql, this.newArgPreparedStatementSetter(args));
}
</code></pre>
<p>参数列表包括两部分内容，一个是要执行的 SQL 语句，另外一个是可变参数 Object... args，因为 update 方法不用解析结果集，所以这里不需要定义 RowMapper 参数。</p>
<p>可变参数 Object... args 的原理和 queryForObject 方法中的 Object[] args 相同，都是为了满足参数的可变性，update 方法的具体使用如下所示。</p>
<pre><code class="java language-java">jdbcTemplate.update("delete from student where id = ?",id);
</code></pre>
<p>非常简单，删除 student 表中 id = 1 的记录。</p>
<p>StudentRepositoryImpl 完整的 CRUD 代码如下所示。</p>
<pre><code class="java language-java">@Repository
public class StudentRepositoryImpl implements StudentRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List&lt;Student&gt; findAll() {
        return jdbcTemplate.query("select * from student",new BeanPropertyRowMapper&lt;Student&gt;(Student.class));
    }

    @Override
    public Student findById(Long id) {
        return jdbcTemplate.queryForObject("select * from student where id = ?",new Object[]{id},new BeanPropertyRowMapper&lt;Student&gt;(Student.class));
    }

    @Override
    public int save(Student student) {
        return jdbcTemplate.update("insert into student(name,score,birthday) values(?,?,?)", student.getName(), student.getScore(), student.getBirthday());
    }

    @Override
    public int update(Student student) {
        return jdbcTemplate.update("update student set name = ?,score = ?,birthday=? where id = ?", student.getName(), student.getScore(), student.getBirthday(), student.getId());
    }

    @Override
    public int deleteById(Long id) {
        return jdbcTemplate.update("delete from student where id = ?",id);
    }
}
</code></pre>
<p>6. 创建 StudentHandler，并注入 StudentRepository。</p>
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
<p>7. 创建配置文件 application.yml，添加数据源配置。</p>
<pre><code class="yaml language-yaml">spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&amp;characterEncoding=UTF-8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
</code></pre>
<p>8. 创建启动类 Application。</p>
<pre><code class="java language-java">package com.southwind;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
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
<p><img src="https://images.gitbook.cn/39de1a90-c1d6-11e9-9969-976e2ac29eb2" width = "60%" /></p>
<ul>
<li>findById</li>
</ul>
<p><img src="https://images.gitbook.cn/473134c0-c1d6-11e9-9166-bdb140d6509f" width = "60%" /></p>
<ul>
<li>save</li>
</ul>
<p><img src="https://images.gitbook.cn/4ff26ac0-c1d6-11e9-9166-bdb140d6509f" width = "60%" /></p>
<p>添加完成，测试 findAll，可以看到新数据已经添加成功。</p>
<p><img src="https://images.gitbook.cn/59f03f70-c1d6-11e9-9166-bdb140d6509f" width = "60%" /></p>
<ul>
<li>update</li>
</ul>
<p><img src="https://images.gitbook.cn/63910000-c1d6-11e9-97a8-35dcf136a505" width = "65%" /></p>
<p>修改完成，测试 findAll，可以看到数据已经修改成功。</p>
<p><img src="https://images.gitbook.cn/6d8a40d0-c1d6-11e9-9166-bdb140d6509f" width = "50%" /></p>
<ul>
<li>deleteById</li>
</ul>
<p><img src="https://images.gitbook.cn/782e8eb0-c1d6-11e9-97a8-35dcf136a505" width = "60%" /></p>
<p>删除完成，测试 findAll，可以看到数据已经删除成功。</p>
<p><img src="https://images.gitbook.cn/809ce9c0-c1d6-11e9-9969-976e2ac29eb2" width = "75%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们进入 Spring Boot 整合持久层技术的学习，首先讲解了 Spring Boot 整合 JdbcTemplate 的具体实现，JdbcTemplate 底层实现了对 JDBC 的封装，是 Spring 自带的 JDBC 模版组件，所以可以做到开箱即用，具体用法需要开发者自定义 SQL 语句，JdbcTemplate 可以帮助我们完成数据库连接、SQL 执行，以及结果集的封装。</p>
<p><a href="https://github.com/southwind9801/gcspringbootjdbc.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>