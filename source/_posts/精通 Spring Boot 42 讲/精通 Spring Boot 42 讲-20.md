---
title: 精通 Spring Boot 42 讲-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>自从 Java 1.5 开始引入了注解，注解便被广泛地应用在了各种开源软件中，使用注解大大地降低了系统中的配置项，让编程变得更为优雅。MyBatis 也顺应潮流基于注解推出了 MyBatis 的注解版本，避免开发过程中频繁切换到 XML 或者 Java 代码中，从而让开发者使用 MyBatis 会有统一的开发体验。</p>
<p>因为最初设计时，MyBatis 是一个 XML 驱动的框架，配置信息是基于 XML 的，而且映射语句也是定义在 XML 中的，而到了 MyBatis 3，就有新选择了。MyBatis 3 构建在全面且强大的基于 Java 语言的配置 API 之上，这个配置 API 是基于 XML 的 MyBatis 配置的基础，也是新的基于注解配置的基础。注解提供了一种简单的方式来实现简单映射语句，而不会引入大量的开销。</p>
<h3 id="">注解版</h3>
<p>注解版的使用方式和 XML 版本相同，只有在构建 SQL 方面有所区别，所以本课重点介绍两者之间的差异部分。</p>
<h4 id="-1">相关配置</h4>
<p>注解版在 application.properties 只需要指明实体类的包路径即可，其他保持不变：</p>
<pre><code class="properties language-properties">mybatis.type-aliases-package=com.neo.model

spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
</code></pre>
<h4 id="-2">传参方式</h4>
<p>先来介绍一下使用注解版的 MyBatis 如何将参数传递到 SQL 中。</p>
<p><strong>直接使用</strong></p>
<pre><code class="java language-java">@Delete("DELETE FROM users WHERE id =#{id}")
void delete(Long id);
</code></pre>
<p>在 SQL 中使用 #{id} 来接收同名参数。</p>
<p><strong>使用 @Param</strong></p>
<p>如果你的映射方法的形参有多个，这个注解使用在映射方法的参数上就能为它们取自定义名字。若不给出自定义名字，多参数则先以 "param" 作前缀，再加上它们的参数位置作为参数别名。例如，#{param1}、#{param2}，这个是默认值。如果注解是 @Param("person")，那么参数就会被命名为 #{person}。</p>
<pre><code class="java language-java">@Select("SELECT * FROM users WHERE user_sex = #{user_sex}")
List&lt;User&gt; getListByUserSex(@Param("user_sex") String userSex);
</code></pre>
<p><strong>使用 Map</strong></p>
<p>需要传送多个参数时，可以考虑使用 Map：</p>
<pre><code class="java language-java">@Select("SELECT * FROM users WHERE username=#{username} AND user_sex = #{user_sex}")
List&lt;User&gt; getListByNameAndSex(Map&lt;String, Object&gt; map);
</code></pre>
<p>使用时将参数依次加入到 Map 中即可：</p>
<pre><code class="java language-java">Map param=  new HashMap();
param.put("username","aa");
param.put("user_sex","MAN");
List&lt;User&gt; users = userMapper.getListByNameAndSex(param);
</code></pre>
<p><strong>使用对象</strong></p>
<p>最常用的使用方式是直接使用对象：</p>
<pre><code class="java language-java">@Insert("INSERT INTO users(userName,passWord,user_sex) VALUES(#{userName}, #{passWord}, #{userSex})")
void insert(User user);
</code></pre>
<p>在执行时，系统会自动读取对象的属性并值赋值到同名的 #{xxx} 中。</p>
<h4 id="-3">注解介绍</h4>
<p><strong>注解版最大的特点是具体的 SQL 文件需要写在 Mapper 类中，取消了 Mapper 的 XML 配置</strong>。</p>
<p>上面介绍参数的时候，已经使用了 @Select、@Delete 等标签，这就是 MyBatis 提供的注解来取代其 XML 文件配置，下面我们一一介绍。</p>
<p><strong>@Select 注解</strong></p>
<p>@Select 主要在查询的时候使用，查询类的注解，所有的查询均使用这个，具体如下：</p>
<pre><code class="java language-java">@Select("SELECT * FROM users WHERE user_sex = #{user_sex}")
List&lt;User&gt; getListByUserSex(@Param("user_sex") String userSex);
</code></pre>
<p><strong>@Insert 注解</strong></p>
<p>@Insert，插入数据库时使用，直接传入实体类会自动解析属性到对应的值，示例如下：</p>
<pre><code class="java language-java">@Insert("INSERT INTO users(userName,passWord,user_sex) VALUES(#{userName}, #{passWord}, #{userSex})")
void insert(User user);
</code></pre>
<p><strong>@Update 注解</strong></p>
<p>@Update，所有的更新操作 SQL 都可以使用 @Update。</p>
<pre><code class="java language-java">@Update("UPDATE users SET userName=#{userName},nick_name=#{nickName} WHERE id =#{id}")
void update(UserEntity user);
</code></pre>
<p><strong>@Delete 注解</strong></p>
<p>@Delete 处理数据删除。</p>
<pre><code class="java language-java">@Delete("DELETE FROM users WHERE id =#{id}")
void delete(Long id);
</code></pre>
<p>以上就是项目中常用的增、删、改、查，但有时候我们有一些特殊的场景需要处理，比如查询的对象返回值属性名和字段名不一致，或者对象的属性中使用了枚举。我们期望查询的返回结果可以将此字段自动转化为对应的类型，MyBatis 提供了另外两个注解来支持：@Results 和 @Result。</p>
<p><strong>@Results 和 @Result 注解</strong></p>
<p>这两个注解配合来使用，主要作用是将数据库中查询到的数值转化为具体的字段，修饰返回的结果集，关联实体类属性和数据库字段一一对应，如果实体类属性和数据库属性名保持一致，就不需要这个属性来修饰。示例如下：</p>
<pre><code class="java language-java">@Select("SELECT * FROM users")
@Results({
    @Result(property = "userSex",  column = "user_sex", javaType = UserSexEnum.class),
    @Result(property = "nickName", column = "nick_name")
})
List&lt;UserEntity&gt; getAll();
</code></pre>
<p>为了更接近实际项目，特地将 user_sex、nick_name 两个属性加了下划线和实体类属性名不一致，另外 user_sex 使用了枚举，使用 @Results 和 @Result 即可解决这样的问题。</p>
<p><a href="http://www.mybatis.org/mybatis-3/zh/java-api.html">了解更多注解使用请点击这里查看</a>。</p>
<p><strong>注意，使用 # 符号和 <code>$</code> 符号的不同：</strong></p>
<pre><code class="java language-java">// This example creates a prepared statement, something like select * from teacher where name = ?;
@Select("Select * from teacher where name = #{name}")
Teacher selectTeachForGivenName(@Param("name") String name);

// This example creates n inlined statement, something like select * from teacher where name = 'someName';
@Select("Select * from teacher where name = '${name}'")
Teacher selectTeachForGivenName(@Param("name") String name);
</code></pre>
<p>同上，上面两个例子可以发现，使用 # 会对 SQL 进行预处理，使用 <code>$</code> 时拼接 SQL，建议使用 #，使用 $ 有 SQL 注入的可能性。</p>
<h3 id="sql">动态 SQL</h3>
<p>MyBatis 最大的特点是可以灵活的支持动态 SQL，在注解版中提供了两种方式来支持，第一种是使用注解来实现，另一种是提供 SQL 类来支持。</p>
<h4 id="-4">使用注解来实现</h4>
<p>用 script 标签包围，然后像 XML 语法一样书写：</p>
<pre><code>@Update("&lt;script&gt;
  update users
    &lt;set&gt;
      &lt;if test="userName != null"&gt;userName=#{userName},&lt;/if&gt;
      &lt;if test="nickName != null"&gt;nick_name=#{nickName},&lt;/if&gt;
    &lt;/set&gt;
  where id=#{id}
&lt;/script&gt;")
void update(User user);
</code></pre>
<p>这种方式就是注解 + XML 的混合使用方式，既有 XML 灵活又有注解的方便，但也有一个缺点需要在 Java 代码中拼接 XML 语法很不方便，因此 MyBatis 又提供了一种更优雅的使用方式来支持动态构建 SQL。</p>
<h4 id="sql-1">使用 SQL 构建类来支持</h4>
<p>以分页为例进行演示，首先定义一个 UserSql 类，提供方法拼接需要执行的 SQL：</p>
<pre><code class="java language-java">public class UserSql {
    public String getList(UserParam userParam) {
        StringBuffer sql = new StringBuffer("select id, userName, passWord, user_sex as userSex, nick_name as nickName");
        sql.append(" from users where 1=1 ");
        if (userParam != null) {
            if (StringUtils.isNotBlank(userParam.getUserName())) {
                sql.append(" and userName = #{userName}");
            }
            if (StringUtils.isNotBlank(userParam.getUserSex())) {
                sql.append(" and user_sex = #{userSex}");
            }
        }
        sql.append(" order by id desc");
        sql.append(" limit " + userParam.getBeginLine() + "," + userParam.getPageSize());
        log.info("getList sql is :" +sql.toString());
        return sql.toString();
    }
}
</code></pre>
<p>可以看出 UserSql 中有一个方法 getList，使用 StringBuffer 对 SQL 进行拼接，通过 if 判断来动态构建 SQL，最后方法返回需要执行的 SQL 语句。</p>
<p>接下来只需要在 Mapper 中引入这个类和方法即可。</p>
<pre><code class="java language-java">@SelectProvider(type = UserSql.class, method = "getList")
List&lt;UserEntity&gt; getList(UserParam userParam);
</code></pre>
<ul>
<li>type：动态生成 SQL 的类 </li>
<li>method：类中具体的方法名 </li>
</ul>
<p>相对于 @SelectProvider 提供查询 SQL 方法导入，还有 @InsertProvider、@UpdateProvider、@DeleteProvider 提供给插入、更新、删除的时候使用。</p>
<h4 id="sql-2">结构化 SQL</h4>
<p>可能你会觉得这样拼接 SQL 很麻烦，SQL 语句太复杂也比较乱，别着急！MyBatis 给我们提供了一种升级的方案：结构化 SQL。</p>
<p>示例如下：</p>
<pre><code class="java language-java">public String getCount(UserParam userParam) {
   String sql= new SQL(){{
        SELECT("count(1)");
        FROM("users");
        if (StringUtils.isNotBlank(userParam.getUserName())) {
            WHERE("userName = #{userName}");
        }
        if (StringUtils.isNotBlank(userParam.getUserSex())) {
            WHERE("user_sex = #{userSex}");
        }
        //从这个 toString 可以看出，其内部使用高效的 StringBuilder 实现 SQL 拼接
    }}.toString();

    log.info("getCount sql is :" +sql);
    return sql;
}
</code></pre>
<ul>
<li>SELECT 表示要查询的字段，可以写多行，多行的 SELECT 会智能地进行合并而不会重复。</li>
<li>FROM 和 WHERE 跟 SELECT 一样，可以写多个参数，也可以在多行重复使用，最终会智能合并而不会报错。这样语句适用于写很长的 SQL，且能够保证 SQL 结构清楚，便于维护、可读性高。</li>
</ul>
<p>更多结构化的 SQL 语法请参考 <a href="http://www.mybatis.org/mybatis-3/zh/statement-builders.html">SQL 语句构建器类</a>。</p>
<blockquote>
  <p>具体使用和 XML 版本一致，直接注入到使用的类中即可。</p>
</blockquote>
<h3 id="-5">多数据源使用</h3>
<p>注解版的多数据源使用和 XML 版本的多数据源基本一致。</p>
<p>首先配置多数据源：</p>
<pre><code>mybatis.type-aliases-package=com.neo.model

spring.datasource.test1.jdbc-url=jdbc:mysql://localhost:3306/test1?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.test1.username=root
spring.datasource.test1.password=root
spring.datasource.test1.driver-class-name=com.mysql.cj.jdbc.Driver

spring.datasource.test2.jdbc-url=jdbc:mysql://localhost:3306/test2?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.test2.username=root
spring.datasource.test2.password=root
spring.datasource.test2.driver-class-name=com.mysql.cj.jdbc.Driver
</code></pre>
<p>分别构建两个不同的数据源。</p>
<p>DataSource1 配置：</p>
<pre><code class="java language-java">@Configuration
@MapperScan(basePackages = "com.neo.mapper.test1", sqlSessionTemplateRef  = "test1SqlSessionTemplate")
public class DataSource1Config {

    @Bean(name = "test1DataSource")
    @ConfigurationProperties(prefix = "spring.datasource.test1")
    @Primary
    public DataSource testDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "test1SqlSessionFactory")
    @Primary
    public SqlSessionFactory testSqlSessionFactory(@Qualifier("test1DataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
        bean.setDataSource(dataSource);
        return bean.getObject();
    }

    @Bean(name = "test1TransactionManager")
    @Primary
    public DataSourceTransactionManager testTransactionManager(@Qualifier("test1DataSource") DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }

    @Bean(name = "test1SqlSessionTemplate")
    @Primary
    public SqlSessionTemplate testSqlSessionTemplate(@Qualifier("test1SqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
</code></pre>
<p>DataSource2 配置和 DataSource1 配置基本相同，只是去掉了 @Primary。</p>
<p>将以前的 Userapper 分别复制到 test1 和 test2 目录下，分别作为两个不同数据源的 Mapper 来使用。</p>
<p><strong>测试</strong></p>
<p>分别注入两个不同的 Mapper，想操作哪个数据源就使用哪个数据源的 Mapper 进行操作处理。</p>
<pre><code class="java language-java">@RunWith(SpringRunner.class)
@SpringBootTest
public class UserMapperTest {
    @Autowired
    private User1Mapper user1Mapper;
    @Autowired
    private User2Mapper user2Mapper;

    @Test
    public void testInsert() throws Exception {
        user1Mapper.insert(new User("aa111", "a123456", UserSexEnum.MAN));
        user1Mapper.insert(new User("bb111", "b123456", UserSexEnum.WOMAN));
        user2Mapper.insert(new User("cc222", "b123456", UserSexEnum.MAN));
    }
}
</code></pre>
<p>执行测试用例完成后，检查 test1 库中的用户表有两条数据，test2 库中的用户表有 1 条数据证明测试成功。</p>
<h3 id="-6">如何选择</h3>
<p>两种模式各有特点，注解版适合简单快速的模式，在微服务架构中，一般微服务都有自己对应的数据库，多表连接查询的需求会大大的降低，会越来越适合注解版。XML 模式比适合大型项目，可以灵活地动态生成 SQL，方便调整 SQL，也有痛痛快快、洋洋洒洒地写 SQL 的感觉。在具体开发过程中，根据公司业务和团队技术基础进行选型即可。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>