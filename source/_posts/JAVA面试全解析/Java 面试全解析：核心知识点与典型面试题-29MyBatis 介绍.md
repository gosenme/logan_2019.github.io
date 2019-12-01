---
title: Java 面试全解析：核心知识点与典型面试题-29
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="mybatis">MyBatis 介绍</h3>
<p>MyBatis 是一款优秀的 ORM（Object Relational Mapping，对象关系映射）框架，它可以通过对象和数据库之间的映射，将程序中的对象自动存储到数据库中。它是 Apache 提供的一个开源项目，之前的名字叫做 iBatis，2010 年迁移到了 Google Code，并且将名字改为我们现在所熟知的 MyBatis，又于 2013 年 11 月迁移到了 Github。</p>
<p>MyBatis 提供了普通 SQL 查询、事务、存储过程等功能，它的优缺点如下。</p>
<p><strong>优点</strong>：</p>
<ul>
<li>相比于 JDBC 需要编写的代码更少</li>
<li>使用灵活，支持动态 SQL</li>
<li>提供映射标签，支持对象与数据库的字段关系映射</li>
</ul>
<p><strong>缺点</strong>：</p>
<ul>
<li>SQL 语句依赖于数据库，数据库移植性差</li>
<li>SQL 语句编写工作量大，尤其在表、字段比较多的情况下</li>
</ul>
<p>总体来说，MyBatis 是一个非常优秀和灵活的数据持久化框架，适用于需求多变的互联网项目，也是当前主流的 ORM 框架。</p>
<h4 id="mybatis-1">MyBatis 重要组件</h4>
<p>MyBatis 中的重要组件如下：</p>
<ul>
<li>Mapper 配置：用于组织具体的查询业务和映射数据库的字段关系，可以使用 XML 格式或 Java 注解格式来实现；</li>
<li>Mapper 接口：数据操作接口也就是通常说的 DAO 接口，要和 Mapper 配置文件中的方法一一对应；</li>
<li>Executor：MyBatis 中所有的 Mapper 语句的执行都是通过 Executor 执行的；</li>
<li>SqlSession：类似于 JDBC 中的 Connection，可以用 SqlSession 实例来直接执行被映射的 SQL 语句；</li>
<li>SqlSessionFactory：SqlSessionFactory 是创建 SqlSession 的工厂，可以通过 SqlSession openSession() 方法创建 SqlSession 对象。</li>
</ul>
<h4 id="mybatis-2">MyBatis 执行流程</h4>
<p>MyBatis 完整执行流程如下图所示：</p>
<p><img src="https://images.gitbook.cn/4070e4c0-da75-11e9-b7a4-5f21fd84c626" alt="1" /></p>
<p>MyBatis 执行流程说明：</p>
<ol>
<li>首先加载 Mapper 配置的 SQL 映射文件，或者是注解的相关 SQL 内容。</li>
<li>创建会话工厂，MyBatis 通过读取配置文件的信息来构造出会话工厂（SqlSessionFactory）。</li>
<li>创建会话，根据会话工厂，MyBatis 就可以通过它来创建会话对象（SqlSession），会话对象是一个接口，该接口中包含了对数据库操作的增、删、改、查方法。</li>
<li>创建执行器，因为会话对象本身不能直接操作数据库，所以它使用了一个叫做数据库执行器（Executor）的接口来帮它执行操作。</li>
<li>封装 SQL 对象，在这一步，执行器将待处理的 SQL 信息封装到一个对象中（MappedStatement），该对象包括 SQL 语句、输入参数映射信息（Java 简单类型、HashMap 或 POJO）和输出结果映射信息（Java 简单类型、HashMap 或 POJO）。</li>
<li>操作数据库，拥有了执行器和 SQL 信息封装对象就使用它们访问数据库了，最后再返回操作结果，结束流程。</li>
</ol>
<h3 id="mybatisxml">MyBatis XML 版</h3>
<p>MyBatis 使用分为两个版本：XML 版和 Java 注解版。接下来我们使用 Spring Boot 结合 MyBatis 的 XML 版，来实现对数据库的基本操作，步骤如下。</p>
<h4 id="1">1）创建数据表</h4>
<pre><code class="sql language-sql">drop table if exists `t_user`;
create table `t_user` (
  `id` bigint(20) not null auto_increment comment '主键id',
  `username` varchar(32) default null comment '用户名',
  `password` varchar(32) default null comment '密码',
  `nick_name` varchar(32) default null,
  primary key (`id`)
) engine=innodb auto_increment=1 default charset=utf8;
</code></pre>
<h4 id="2">2）添加依赖</h4>
<p>在项目添加对 MyBatis 和 MySQL 支持的依赖包，在 pom.xml 文件中添加如下代码：</p>
<pre><code class="xml language-xml">&lt;!-- https://mvnrepository.com/artifact/org.mybatis.spring.boot/mybatis-spring-boot-starter --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
    &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
    &lt;version&gt;2.1.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;mysql&lt;/groupId&gt;
    &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
    &lt;version&gt;8.0.16&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>mybatis-spring-boot-starter 是 MyBatis 官方帮助我们快速集成 Spring Boot 提供的一个组件包，mybatis-spring-boot-starter 2.1.0 对应 MyBatis 的版本是 3.5.2。</p>
<h4 id="3">3）增加配置文件</h4>
<p>在 application.yml 文件中添加以下内容：</p>
<pre><code class="xml language-xml">spring:
  datasource:
    url: jdbc:mysql://localhost:3306/learndb?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
mybatis:
  config-location: classpath:mybatis/mybatis-config.xml
  mapper-locations: classpath:mybatis/mapper/*.xml
  type-aliases-package: com.interview.mybatislearning.model
</code></pre>
<p>其中：</p>
<ul>
<li>mybatis.config-location：配置  MyBatis 基础属性；</li>
<li>mybatis.mapper-locations：配置 Mapper 对应的 XML 文件路径；</li>
<li>mybatis.type-aliases-package：配置项目中实体类包路径。</li>
</ul>
<p>注：如果配置文件使用的是 application.properties，配置内容是相同的，只是内容格式不同。</p>
<h4 id="4">4）创建实体类</h4>
<pre><code class="java language-java">public class UserEntity implements Serializable {
    private static final long serialVersionUID = -5980266333958177104L;
    private Integer id;
    private String userName;
    private String passWord;
    private String nickName;
    public UserEntity(String userName, String passWord, String nickName) {
        this.userName = userName;
        this.passWord = passWord;
        this.nickName = nickName;
    }
    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public String getUserName() {
        return userName;
    }
    public void setUserName(String userName) {
        this.userName = userName;
    }
    public String getPassWord() {
        return passWord;
    }
    public void setPassWord(String passWord) {
        this.passWord = passWord;
    }
    public String getNickName() {
        return nickName;
    }
    public void setNickName(String nickName) {
        this.nickName = nickName;
    }
}
</code></pre>
<h4 id="5xml">5）创建 XML 文件</h4>
<p><strong>mybatis-config.xml</strong>（基础配置文件）：</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd"&gt;
&lt;configuration&gt;
    &lt;typeAliases&gt;
        &lt;typeAlias alias="Integer" type="java.lang.Integer"/&gt;
        &lt;typeAlias alias="Long" type="java.lang.Long"/&gt;
        &lt;typeAlias alias="HashMap" type="java.util.HashMap"/&gt;
        &lt;typeAlias alias="LinkedHashMap" type="java.util.LinkedHashMap"/&gt;
        &lt;typeAlias alias="ArrayList" type="java.util.ArrayList"/&gt;
        &lt;typeAlias alias="LinkedList" type="java.util.LinkedList"/&gt;
    &lt;/typeAliases&gt;
&lt;/configuration&gt;
</code></pre>
<p>mybatis-config.xml 主要是为常用的数据类型设置别名，用于减少类完全限定名的长度，比如：<code>resultType="Integer"</code> 完整示例代码如下：</p>
<pre><code class="xml language-xml">&lt;select id="getAllCount" resultType="Integer"&gt;
    select
    count(*)
    from t_user
&lt;/select&gt;
</code></pre>
<p><strong>UserMapper.xml</strong>（业务配置文件）：</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" &gt;
&lt;mapper namespace="com.interview.mybatislearning.mapper.UserMapper"&gt;
    &lt;resultMap id="BaseResultMap" type="com.interview.mybatislearning.model.UserEntity" &gt;
        &lt;id column="id" property="id" jdbcType="BIGINT" /&gt;
        &lt;result column="username" property="userName" jdbcType="VARCHAR" /&gt;
        &lt;result column="password" property="passWord" jdbcType="VARCHAR" /&gt;
        &lt;result column="nick_name" property="nickName" jdbcType="VARCHAR" /&gt;
    &lt;/resultMap&gt;
    &lt;sql id="Base_Column_List" &gt;
        id, username, password, nick_name
    &lt;/sql&gt;
    &lt;sql id="Base_Where_List"&gt;
        &lt;if test="userName != null  and userName != ''"&gt;
            and userName = #{userName}
        &lt;/if&gt;
    &lt;/sql&gt;
    &lt;select id="getAll" resultMap="BaseResultMap"  &gt;
        SELECT
        &lt;include refid="Base_Column_List" /&gt;
        FROM t_user
    &lt;/select&gt;
    &lt;select id="getOne" parameterType="Long" resultMap="BaseResultMap" &gt;
        SELECT
        &lt;include refid="Base_Column_List" /&gt;
        FROM t_user
        WHERE id = #{id}
    &lt;/select&gt;
    &lt;insert id="insert" parameterType="com.interview.mybatislearning.model.UserEntity" &gt;
       INSERT INTO
               t_user
               (username,password,nick_name)
           VALUES
               (#{userName}, #{passWord}, #{nickName})
    &lt;/insert&gt;
    &lt;update id="update" parameterType="com.interview.mybatislearning.model.UserEntity" &gt;
        UPDATE
        t_user
        SET
        &lt;if test="userName != null"&gt;username = #{userName},&lt;/if&gt;
        &lt;if test="passWord != null"&gt;password = #{passWord},&lt;/if&gt;
        nick_name = #{nickName}
        WHERE
        id = #{id}
    &lt;/update&gt;
    &lt;delete id="delete" parameterType="Long" &gt;
       DELETE FROM
                t_user
       WHERE
                id =#{id}
    &lt;/delete&gt;
&lt;/mapper&gt;
</code></pre>
<p>以上配置我们增加了增删改查等基础方法。</p>
<h4 id="6mapper">6）增加 Mapper 文件</h4>
<p>此步骤我们需要创建一个与 XML 对应的业务 Mapper 接口，代码如下：</p>
<pre><code class="java language-java">public interface UserMapper {
    List&lt;UserEntity&gt; getAll();
    UserEntity getOne(Long id);
    void insert(UserEntity user);
    void update(UserEntity user);
    void delete(Long id);
}
</code></pre>
<h4 id="7mapper">7）添加 Mapper 包扫描</h4>
<p>在启动类中添加 @MapperScan，设置 Spring Boot 启动的时候会自动加载包路径下的 Mapper。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.interview.mybatislearning.mapper")
public class MyBatisLearningApplication {
   public static void main(String[] args) {
       SpringApplication.run(MyBatisLearningApplication.class, args);
   }
}
</code></pre>
<h4 id="8">8）编写测试代码</h4>
<p>经过以上步骤之后，整个 MyBatis 的集成就算完成了。接下来我们写一个单元测试，验证一下。</p>
<pre><code class="java language-java">@RunWith(SpringRunner.class)
@SpringBootTest
public class MybatislearningApplicationTests {
    @Resource
    private UserMapper userMapper;
    @Test
    public void testInsert() {
        userMapper.insert(new UserEntity("laowang", "123456", "老王"));
        Assert.assertEquals(1, userMapper.getAll().size());
    }
}
</code></pre>
<h3 id="">总结</h3>
<p>通过本文我们知道 MyBatis 是一个优秀和灵活的数据持久化框架，MyBatis 包含 Mapper 配置、Mapper 接口、Executor、SqlSession、SqlSessionFactory 等几个重要的组件，知道了 MyBatis 基本流程：MyBatis 首先加载 Mapper 配置和 SQL 映射文件，通过创建会话工厂得到 SqlSession 对象，再执行 SQL 语句并返回操作信息。我们也使用 XML 的方式，实现了 MyBatis 对数据库的基础操作。</p>
<blockquote>
  <p><a href="https://github.com/vipstone/java-interview/tree/master/mybatislearning-xml">点击此处下载本文源码</a></p>
</blockquote></div></article>