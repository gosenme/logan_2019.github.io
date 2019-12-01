---
title: 案例上手 Spring 全家桶-21
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>从本节课开始，我们进入 MyBatis 框架的学习阶段。</p>
<h3 id="mybatis">什么是 MyBatis</h3>
<p>MyBatis 是当前主流的 ORM 框架，是由 Apache 提供的一个开源项目，之前的名字叫做 iBatis，2010 年迁移到了 Google Code，并且将名字改为我们现在所熟知的 MyBatis，又于 2013 年 11 月迁移到了 Github。MyBatis 是一个帮助开发者实现数据持久化工作的框架，它同时支持 Java、.NET、Ruby 三种语言的实现，当然我们这里讲的是在 Java Application 中的使用，初学者可以将 MyBatis 简单理解为一个对 JDBC 进行封装的框架。</p>
<p>说到 ORM 框架就不得不提 Hibernate，Hibernate 是实现了 JPA 规范的 ORM 框架，使用非常广泛，Spring Data JPA 底层就是采用 Hibernate 技术支持。同为 ORM 框架，MyBatis 与 Hibernate 的区别是什么呢？</p>
<p>Hibernate 是一个“全自动化”的 ORM 框架，而 MyBatis 则是一个“半自动化”的 ORM 框架。</p>
<p>什么是“全自动化”？意为开发者只需要调用相关接口就可以完成操作，整个流程框架都已经封装好了，开发者无需关注。具体来讲 Hibernate 实现了 POJO 和数据库表之间的映射，同时可以自动生成 SQL 语句并完成执行。</p>
<p>“半自动化”指的是框架只提供了一部分功能，剩下的工作仍需要开发者手动完成，MyBatis 框架没有实现 POJO 与数据库表的映射，它只实现了 POJO 与 SQL 之间的映射关系，同时需要开发者手动定义 SQL 语句，以及数据与 POJO 的装配关系。</p>
<p>虽然功能上没有 Hibernate 更加方便，但是这种“半自动化”的方式提高了框架的灵活性，MyBatis 对所有的 JDBC 代码实现了封装，包括参数设置、SQL 执行、结果集解析等，通过 XML 配置的方式完成 POJO 与数据的映射。</p>
<h3 id="mybatis-1">MyBatis 的优点</h3>
<ul>
<li>极大地简化了 JDBC 代码的开发</li>
<li>简单好用、容易上手，具有更好的灵活性</li>
<li>通过将 SQL 定义在 XML 文件中的方式降低呈现的耦合度</li>
<li>支持动态 SQL，可根据具体业务灵活实现需求</li>
</ul>
<h3 id="mybatis-2">MyBatis 的缺点</h3>
<ul>
<li>相比于 Hibernate，开发者需要完成更多工作，如定义 SQL、设置 POJO 与数据的映射关系等</li>
<li>要求开发人员具备一定的 SQL 编写能力，在一些特定场景下工作量较大</li>
<li>数据库移植性较差，因为 SQL 依赖于底层数据库，如果要进行数据库迁移，部分 SQL 需要重新编写</li>
</ul>
<p>整体来说，MyBatis 是一个非常不错的持久层解决方案，它专注于 SQL 本身，非常灵活，适用于需求变化较多的互联网项目，也是当前主流的 ORM 框架。</p>
<h3 id="mybatis-3">MyBatis 快速入门</h3>
<p>（1）创建 Maven 工程，pom.xml 添加相关依赖，我们使用 MySQL 数据库，因此需要额外引入 MySQL 驱动依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
  &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
  &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
  &lt;version&gt;3.4.5&lt;/version&gt;
&lt;/dependency&gt;

&lt;dependency&gt;
  &lt;groupId&gt;mysql&lt;/groupId&gt;
  &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
  &lt;version&gt;8.0.11&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>（2）新建数据表。</p>
<pre><code class="sql language-sql">CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(11) DEFAULT NULL,
  `password` varchar(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 
</code></pre>
<p>（3）创建对应的实体类 User。</p>
<pre><code class="java language-java">public class User{
    private Integer id;
    private String username;
    private String password;
    private Integer age;
}
</code></pre>
<p>（4）在 resources 路径下创建 MyBatis 配置文件 config.xml（文件名可自定义），配置数据源信息。</p>
<pre><code class="xml language-xml">&lt;configuration&gt;
    &lt;!-- 配置 MyBatis 运行环境 --&gt;
    &lt;environments default="development"&gt;
        &lt;environment id="development"&gt;
            &lt;!-- 配置 JDBC 事务管理 --&gt;
            &lt;transactionManager type="JDBC" /&gt;
            &lt;!-- POOLED 配置 JDBC 数据源连接池 --&gt;
            &lt;dataSource type="POOLED"&gt;
                &lt;property name="driver" value="com.mysql.cj.jdbc.Driver" /&gt;
                &lt;property name="url" value="jdbc:mysql://localhost:3306/mybatis?useUnicode=true&amp;amp;characterEncoding=UTF-8" /&gt;
                &lt;property name="username" value="root" /&gt;
                &lt;property name="password" value="root" /&gt;
            &lt;/dataSource&gt;
        &lt;/environment&gt;
    &lt;/environments&gt;
&lt;/configuration&gt;
</code></pre>
<p>（5）MyBatis 开发有两种方式：</p>
<ul>
<li>使用原生接口</li>
<li>Mapper 代理实现自定义接口</li>
</ul>
<p>先来说第一种使用原生接口的开发方式。</p>
<p>第一步，创建 Mapper 文件 UserMapper.xml。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.mapper.UserMapper"&gt; 

    &lt;select id="get" parameterType="int" resultType="com.southwind.entity.User"&gt;
        select * from user where id=#{id}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>namespace 通常设置为文件所在包名 + 文件名，但不是一定要这样设置，可以自定义，出于代码规范一般设置为包名 + 文件名的形式，parameterType 为参数数据类型，resultType 为返回值数据类型。</p>
<p>第二步，在全局配置文件 config.xml 中注册 UseMapper.xml。</p>
<pre><code class="xml language-xml">&lt;configuration&gt;

    &lt;!-- 注册UserMapper.xml --&gt;
    &lt;mappers&gt;
        &lt;mapper resource="com/southwind/mapper/UserMapper.xml"/&gt;
    &lt;/mappers&gt;

&lt;/configuration&gt;
</code></pre>
<p>第三步，在测试类中调用原生接口执行 SQL 语句获取结果。</p>
<pre><code class="java language-java">public class Test {
      public static void main(String[] args) {
        //加载 MyBatis 配置文件
        InputStream is = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(is);
        //获取 SqlSession
        SqlSession sqlSession = sqlSessionFactory.openSession();
        //调用 MyBatis 原生接口执行 SQL
        //statement 为 UserMapper.xml 的 namespace 值+"."+select 标签的 id 值
        String statement = "com.southwind.mapper.UserMapper.get";
        User user = sqlSession.selectOne(statement , 1);
        System.out.println(user);
      }
}
</code></pre>
<p>运行结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/24390990-ab72-11e9-b076-bda4ece4a323" width = "70%" /></p>
<p>我们在实际开发中，推荐使用第二种方式：自定义接口，但是开发者不需要实现该接口，只需要定义即可，具体的实现工作由 Mapper 代理结合配置文件完成，实现逻辑或者说要执行的 SQL 语句配置在 Mapper.xml 中，这里为了统一，我们换了一个名字 UserRepository.xml，实际和 UserMapper.xml 是一样的。</p>
<p>第一步，自定义接口。</p>
<pre><code class="java language-java">public interface UserRepository {
    public int addUser(User user);
    public int deleteUser(Integer id);
    public int updateUser(User user);
    public User selectUserById(Integer id);
}
</code></pre>
<p>第二步，创建 UserRepository.xml，定义接口方法对应的 SQL 语句。statement 标签根据 SQL 执行的业务可选择 insert、delete、update、select，MyBatis 会根据规则自动创建 UserRepository 接口实现类的代理对象。</p>
<p>规则如下: </p>
<ul>
<li>UserRepository.xml 中 namespace 为接口的全类名</li>
<li>UserRepository.xml 中 statement 的 id 为接口中对应的方法名</li>
<li>UserRepository.xml 中 statement 的 parameterType 和接口中对应方法的参数类型一致</li>
<li>UserRepository.xml 中 statement 的 resultType 和接口中对应方法的返回值类型一致</li>
</ul>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt; 
&lt;mapper namespace="com.southwind.repository.UserRepository"&gt; 

    &lt;insert id="addUser" parameterType="com.southwind.entity.User"&gt;
       insert into t_user (username,password,age) values (#{username},#{password},#{age})
    &lt;/insert&gt;

    &lt;delete id="deleteUser" parameterType="java.lang.Integer"&gt;
       delete from t_user where id=#{id}  
    &lt;/delete&gt; 

    &lt;update id="updateUser" parameterType="com.southwind.entity.User"&gt;
       update t_user set username=#{username},password=#{password},account=#{account} where id=#{id}
    &lt;/update&gt;

    &lt;select id="selectUserById" parameterType="java.lang.Integer" resultType="com.southwind.entity.User"&gt;
       select * from t_user where id=#{id}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>第三步，在 config.xml 中注册 UserRepository.xml。</p>
<pre><code class="xml language-xml">&lt;configuration&gt;

    &lt;!-- 注册 UserRepository.xml --&gt;
    &lt;mappers&gt;
        &lt;mapper resource="com/southwind/repository/UserRepository.xml"/&gt;
    &lt;/mappers&gt;

&lt;/configuration&gt;
</code></pre>
<p>第四步，测试。</p>
<pre><code class="java language-java">public class Test {
    public static void main(String[] args) {
        //加载 MyBatis 配置文件
        InputStream is = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(is);
        //获取 SqlSession
        SqlSession sqlSession = sqlSessionFactory.openSession();
        //获取实现接口的代理对象
        UserRepository userRepository = sqlSession.getMapper(UserRepository.class);

        //新增用户
        User user = new User();
        user.setUsername("张三");
        user.setPassword("123");
        user.setAge(22);
        System.out.println(userRepository.addUser(user));
        sqlSession.commit();

        //删除用户
        System.out.println(userRepository.deleteUser(2));
        sqlSession.commit();

        //查询用户
        User user = userRepository.selectUserById(3);
        System.out.println(user);

        //修改用户
        User user = userRepository.selectUserById(3);
        user.setUsername("李四");
        System.out.println(userRepository.updateUser(user));
        sqlSession.commit();
    }
}
</code></pre>
<h3 id="">总结</h3>
<p>本节课我们讲解了 MyBatis 框架的基本概念和使用，MyBatis 是当下主流的 ORM 框架，以其轻量级、灵活、易扩展的特性而受大广大开发者的青睐，MyBatis 的关注点在于 POJO 与 SQL 之间的映射关系，因此它是一个“半自动化”的 ORM 框架。</p>
<p><a href="https://github.com/southwind9801/gcmybatis.git">请单击这里下载源码</a></p>
<h3 id="-1">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>