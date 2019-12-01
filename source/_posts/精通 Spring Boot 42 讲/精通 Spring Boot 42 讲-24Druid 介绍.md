---
title: 精通 Spring Boot 42 讲-24
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="druid">Druid 介绍</h3>
<p>Druid 是阿里巴巴开源平台上的一个项目，整个项目由数据库连接池、插件框架和 SQL 解析器组成，该项目主要是为了扩展 JDBC 的一些限制，可以让程序员实现一些特殊的需求，比如向密钥服务请求凭证、统计 SQL 信息、SQL 性能收集、SQL 注入检查、SQL 翻译等，程序员可以通过定制来实现自己需要的功能。</p>
<p>Druid 首先是一个数据库连接池，但它不仅仅是一个数据库连接池，还包含了一个 ProxyDriver，一系列内置的 JDBC 组件库，一个 SQL Parser。在 Java 的世界中 Druid 是监控做的最好的数据库连接池，在功能、性能、扩展性方面，也有不错的表现。</p>
<p><strong>Druid 可以做什么</strong></p>
<ul>
<li>替换其他 Java 连接池，Druid 提供了一个高效、功能强大、可扩展性好的数据库连接池。</li>
<li>可以监控数据库访问性能，Druid 内置提供了一个功能强大的 StatFilter 插件，能够详细统计 SQL 的执行性能，这对于线上分析数据库访问性能有很大帮助。</li>
<li>数据库密码加密。直接把数据库密码写在配置文件中，这是不好的行为，容易导致安全问题，DruidDruiver 和 DruidDataSource 都支持 PasswordCallback。</li>
<li>SQL 执行日志，Druid 提供了不同的 LogFilter，能够支持 Common-Logging、Log4j 和 JdkLog，可以按需要选择相应的 LogFilter，监控应用的数据库访问情况。</li>
<li>扩展 JDBC，如果你要对 JDBC 层有编程的需求，可以通过 Druid 提供的 Filter 机制，很方便编写 JDBC 层的扩展插件。</li>
</ul>
<p><strong>Spring Boot 集成 Druid</strong></p>
<p>非常令人高兴的是，阿里为 Druid 也提供了 Spring Boot Starter 的支持。官网这样解释：Druid Spring Boot Starter 用于帮助你在 Spring Boot 项目中轻松集成 Druid 数据库连接池和监控。</p>
<p>Druid Spring Boot Starter 主要做了哪些事情呢？其实这个组件包很简单，主要提供了很多自动化的配置，按照 Spring Boot 的理念对很多内容进行了预配置，让我们在使用的时候更加的简单和方便。</p>
<h3 id="mybatisdruid">MyBatis 中使用 Druid 作为连接池</h3>
<p>在前面课程中的 spring-boot-mybatis-annotation 上去集成。</p>
<p><strong>引入依赖包</strong></p>
<pre><code class="xml language-xml">&lt;dependency&gt;
   &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
   &lt;artifactId&gt;druid-spring-boot-starter&lt;/artifactId&gt;
   &lt;version&gt;1.1.10&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<ul>
<li>druid-spring-boot-starter 的最新版本为 1.1.10，会自动依赖 Druid 相关包。</li>
</ul>
<p><strong>application 配置</strong></p>
<p>Druid Spring Boot Starter 配置属性的名称完全遵照 Druid，可以通过 Spring Boot 配置文件来配置 Druid 数据库连接池和监控，如果没有配置则使用默认值。</p>
<pre><code class="properties language-properties"># 实体类包路径
mybatis.type-aliases-package=com.neo.model

spring.datasource.type: com.alibaba.druid.pool.DruidDataSource
spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# 初始化大小、最小、最大连接数
spring.datasource.druid.initial-size=3
spring.datasource.druid.min-idle=3
spring.datasource.druid.max-active=10

# 配置获取连接等待超时的时间
spring.datasource.druid.max-wait=60000

# 监控后台账号和密码
spring.datasource.druid.stat-view-servlet.login-username=admin
spring.datasource.druid.stat-view-servlet.login-password=admin

# 配置 StatFilter
spring.datasource.druid.filter.stat.log-slow-sql=true
spring.datasource.druid.filter.stat.slow-sql-millis=2000
</code></pre>
<p>在以前项目的基础上，增加了对 Druid 连接池的配置，以及 SQL 监控的配置，druid-spring-boot-starter 默认情况下开启 StatFilter 的监控功能。Druid Spring Boot Starter 不限于对以上配置属性提供支持，DruidDataSource 内提供 setter 方法的可配置属性都将被支持。</p>
<p>更多配置内容请参考 <a href="https://github.com/alibaba/druid/tree/master/druid-spring-boot-starter">druid-spring-boot-starter</a>。</p>
<p>配置完成后，直接启动项目访问地址：http://localhost:8080/druid，就会出现 Druid 监控后台的登录页面，输入账户和密码后，就会进入首页。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/druid01.png" alt="" /> </p>
<p>首页会展示项目使用的 JDK 版本、数据库驱动、JVM 相关统计信息。根据上面的菜单可以看出 Druid 的功能非常强大，支持数据源、SQL 监控、SQL 防火墙、URI 监控等很多功能。</p>
<p>我们这里重点介绍一下 SQL 监控，具体的展示信息如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2017/chat/druid02.png" alt="" /> </p>
<p>这里的 SQL 监控会将项目中具体执行的 SQL 打印出来，展示此 SQL 执行了多少次、每次返回多少数据、执行的时间分布是什么。这些功能非常的实用，方便我们在实际生产中查找出慢 SQL，最后对 SQL 进行调优。</p>
<p>从这个例子可发现，使用 Spring Boot 集成 Druid 非常的简单，只需要添加依赖，简单配置就可以。</p>
<h3 id="mybatisdruid-1">MyBatis + Druid 多数据源</h3>
<p>接下来为大家介绍 MyBatis 多数据源中是如何使用 Druid 数据库连接池的。</p>
<h4 id="">配置文件</h4>
<p>首先我们需要配置两个不同的数据源：</p>
<pre><code class="properties language-properties">spring.datasource.druid.one.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.druid.one.url = jdbc:mysql://localhost:3306/test1?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.druid.one.username = root
spring.datasource.druid.one.password = root

spring.datasource.druid.two.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.druid.two.url = jdbc:mysql://localhost:3306/test2?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.druid.two.username = root
spring.datasource.druid.two.password = root
</code></pre>
<p>第一个数据源以 spring.datasource.druid.one.* 为前缀连接数据库 test1，第二个数据源以 spring.datasource.druid.two.* 为前缀连接数据库 test2。</p>
<p><strong>强烈注意：Spring Boot 2.X 版本不再支持配置继承，多数据源的话每个数据源的所有配置都需要单独配置，否则配置不会生效。</strong></p>
<pre><code class="properties language-properties">#  StatViewServlet 配置
spring.datasource.druid.stat-view-servlet.login-username=admin
spring.datasource.druid.stat-view-servlet.login-password=admin

# 配置 StatFilter
spring.datasource.druid.filter.stat.log-slow-sql=true
spring.datasource.druid.filter.stat.slow-sql-millis=2000

# Druid 数据源 1 配置
spring.datasource.druid.one.initial-size=3
spring.datasource.druid.one.min-idle=3
spring.datasource.druid.one.max-active=10
spring.datasource.druid.one.max-wait=60000

# Druid 数据源 2 配置
spring.datasource.druid.two.initial-size=6
spring.datasource.druid.two.min-idle=6
spring.datasource.druid.two.max-active=20
spring.datasource.druid.two.max-wait=120000
</code></pre>
<p>filter 和 stat 作为 Druid 的公共信息配置，其他数据源的配置需要各个数据源单独配置。</p>
<h4 id="-1">注入多数据源</h4>
<p>首先为两个数据源创建不同的 Mapper 包路径，将以前的 UserMapper 复制到包 com.neo.mapper.one 和 com.neo.mapper.two 路径下，并且分别重命名为 UserOneMapper、UserTwoMapper。</p>
<p>定义一个 MultiDataSourceConfig 类，对两个不同的数据源进行加载：</p>
<pre><code class="java language-java">@Configuration
public class MultiDataSourceConfig {
    @Primary
    @Bean(name = "oneDataSource")
    @ConfigurationProperties("spring.datasource.druid.one")
    public DataSource dataSourceOne(){
        return DruidDataSourceBuilder.create().build();
    }
    @Bean(name = "twoDataSource")
    @ConfigurationProperties("spring.datasource.druid.two")
    public DataSource dataSourceTwo(){
        return DruidDataSourceBuilder.create().build();
    }
}
</code></pre>
<p>必须指明一个为默认的主数据源，使用注解：@Primary。加载配置两个数据源的 DataSourceConfig 和前面课程中 MyBatis 多数据源使用的配置一致没有变化。</p>
<blockquote>
  <p>注意：在多数据源的情况下，我们不需要再启动类添加 @MapperScan("com.xxx.mapper") 的注解。</p>
</blockquote>
<h4 id="-2">测试使用</h4>
<p>以上所有的配置内容都完成后，启动项目访问这个地址：http://localhost:8080/druid，单击数据源查看数据库连接信息。</p>
<blockquote>
  <p>如果数据源没有信息，先访问地址：http://localhost:8080/getUsers，用来触发数据库连接。在没有 SQL 使用的情况下，页面监控不到数据源的配置信息，SQL 监控页面也监控不到 SQL 的执行。</p>
</blockquote>
<p>显示效果如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/druid02.png" alt="" /> </p>
<p>摘录自数据源1的显示信息</p>
<table>
<thead>
<tr>
<th>Keyword</th>
<th>value</th>
<th>解释</th>
</tr>
</thead>
<tbody>
<tr>
<td>连接地址</td>
<td>jdbc:mysql://localhost:3306/test1?useUnicode=true&amp;characterEncoding=utf-8</td>
<td>JDBC 连接字符串</td>
</tr>
<tr>
<td>初始化连接大小</td>
<td>3</td>
<td>连接池建立时创建的初始化连接数</td>
</tr>
<tr>
<td>最小空闲连接数</td>
<td>3</td>
<td>连接池中最小的活跃连接数</td>
</tr>
<tr>
<td>最大连接数</td>
<td>10</td>
<td>连接池中最大的活跃连接数</td>
</tr>
<tr>
<td>MaxWait</td>
<td>10000</td>
<td>配置获取连接等待超时的时间</td>
</tr>
</tbody>
</table>
<p>摘录自数据源2的显示信息</p>
<table>
<thead>
<tr>
<th>Keyword</th>
<th>value</th>
<th>解释</th>
</tr>
</thead>
<tbody>
<tr>
<td>连接地址</td>
<td>jdbc:mysql://localhost:3306/test2?useUnicode=true&amp;characterEncoding=utf-8</td>
<td>JDBC 连接字符串</td>
</tr>
<tr>
<td>初始化连接大小</td>
<td>6</td>
<td>连接池建立时创建的初始化连接数</td>
</tr>
<tr>
<td>最小空闲连接数</td>
<td>6</td>
<td>连接池中最小的活跃连接数</td>
</tr>
<tr>
<td>最大连接数</td>
<td>20</td>
<td>连接池中最大的活跃连接数</td>
</tr>
<tr>
<td>MaxWait</td>
<td>120000</td>
<td>配置获取连接等待超时的时间</td>
</tr>
</tbody>
</table>
<p>通过这两个数据源的连接信息来看，两个数据源的配置信息已经生效。</p>
<h3 id="springdatajpadruid">Spring Data JPA 中使用 Druid 作为连接池</h3>
<p>Spring Data JPA 集成 Druid 的方式和 MyBatis 大体相同。</p>
<p>引入相关依赖包：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
   &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
   &lt;artifactId&gt;druid-spring-boot-starter&lt;/artifactId&gt;
   &lt;version&gt;1.1.10&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>添加 Web 依赖是因为需要在启动的时候保持容器运行，同时在项目中添加了 Web 访问，内容如下：</p>
<pre><code class="java language-java">@RestController
public class UserController {
    @Autowired
    private UserRepository userRepository;
    @RequestMapping("/getUsers")
    public List&lt;User&gt; getUsers() {
        List&lt;User&gt; users=userRepository.findAll();
        return users;
    }
}
</code></pre>
<p>内容比较简单获取所有的用户信息并展示出来。</p>
<p>Application 中添加以下信息：</p>
<pre><code class="properties language-properties"># 初始化大小、最小、最大链接数
spring.datasource.druid.initial-size=3
spring.datasource.druid.min-idle=3
spring.datasource.druid.max-active=10

# 配置获取连接等待超时的时间
spring.datasource.druid.max-wait=60000

#  StatViewServlet 配置
spring.datasource.druid.stat-view-servlet.login-username=admin
spring.datasource.druid.stat-view-servlet.login-password=admin

# 配置 StatFilter
spring.datasource.druid.filter.stat.log-slow-sql=true
spring.datasource.druid.filter.stat.slow-sql-millis=2000
</code></pre>
<p>好了，这样就成功的在 JPA 项目中配置好了 Druid 的使用。启动项目先访问地址：http://localhost:8080/getUsers，再访问 http://localhost:8080/druid，查看 SQL 执行记录，如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/druid03.png" alt="" /> </p>
<p>会发现有 create table addres... 和  drop table if exist... 这样的 SQL 语句，这是因为我们将 JPA 的策略设置为 create，spring.jpa.properties.hibernate.hbm2ddl.auto=create，意味着每次重启的时候对会重新创建表，方便我们在测试的时候使用。</p>
<h3 id="jpadruid">JPA + Druid + 多数据源</h3>
<p>因为 Druid 官方还没有针对 Spring Boot 2.0 进行优化，在某些场景下使用就会出现问题，比如在 JPA 多数据源的情况下直接使用 Druid 提供的 druid-spring-boot-starter 就会报错，既然 druid-spring-boot-starter 不支持，那么我们就使用 Druid 的原生包进行封装。</p>
<p>在前面示例项目 spring-boot-multi-Jpa 的基础上进行改造。</p>
<h4 id="-3">添加依赖</h4>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
    &lt;artifactId&gt;druid&lt;/artifactId&gt;
    &lt;version&gt;1.1.10&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;log4j&lt;/groupId&gt;
    &lt;artifactId&gt;log4j&lt;/artifactId&gt;
    &lt;version&gt;1.2.17&lt;/version&gt;
&lt;/dependency&gt;
&lt;!--&lt;dependency&gt;
    &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
    &lt;artifactId&gt;druid-spring-boot-starter&lt;/artifactId&gt;
    &lt;version&gt;1.1.10&lt;/version&gt;
&lt;/dependency&gt;--&gt;
</code></pre>
<p>删掉对 druid-spring-boot-starter 包的依赖，添加 Druid 的依赖包，添加 log4j 的原因是因为 Druid 依赖于 log4j 打印日志。</p>
<h4 id="-4">多数据源配置</h4>
<p>配置文件我们做这样的设计，将多个数据源相同配置抽取出来共用，每个数据源个性配置信息单独配置。</p>
<p>数据库1的配置，以 spring.datasource.druid.one 开头：</p>
<pre><code class="properties language-properties">spring.datasource.druid.one.url=jdbc:mysql://localhost:3306/test1?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.druid.one.username=root
spring.datasource.druid.one.password=root
spring.datasource.druid.one.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.druid.one.initialSize=3
spring.datasource.druid.one.minIdle=3
spring.datasource.druid.one.maxActive=10
</code></pre>
<p>数据库2的配置，以 spring.datasource.druid.two 开头：</p>
<pre><code class="properties language-properties">spring.datasource.druid.two.url=jdbc:mysql://localhost:3306/test2?serverTimezone=UTC&amp;useUnicode=true&amp;characterEncoding=utf-8&amp;useSSL=true
spring.datasource.druid.two.username=root
spring.datasource.druid.two.password=root
spring.datasource.druid.two.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.druid.two.initialSize=6
spring.datasource.druid.two.minIdle=20
spring.datasource.druid.two.maxActive=30
</code></pre>
<p>多数据源的共同配置，以 spring.datasource.druid 开头，是多个数据源的公共配置项。</p>
<pre><code class="properties language-properties">配置获取连接等待超时的时间
spring.datasource.druid.maxWait=60000
#配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
spring.datasource.druid.timeBetweenEvictionRunsMillis=60000
#配置一个连接在池中最小生存的时间，单位是毫秒
spring.datasource.druid.minEvictableIdleTimeMillis=600000
spring.datasource.druid.maxEvictableIdleTimeMillis=900000
spring.datasource.druid.validationQuery=SELECT 1 FROM DUAL
#y检测连接是否有效
spring.datasource.druid.testWhileIdle=true
#是否在从池中取出连接前进行检验连接池的可用性
spring.datasource.druid.testOnBorrow=false
#是否在归还到池中前进行检验连接池的可用性
spring.datasource.druid.testOnReturn=false
# 是否打开 PSCache，
spring.datasource.druid.poolPreparedStatements=true
#并且指定每个连接上 PSCache 的大小
spring.datasource.druid.maxPoolPreparedStatementPerConnectionSize=20
#配置监控统计拦截的 filters
spring.datasource.druid.filters=stat,wall,log4j
#通过 connectProperties 属性来打开 mergeSQL 功能，慢 SQL 记录
spring.datasource.druid.connectionProperties=druid.stat.mergeSql=true;druid.stat.slowSqlMillis=600
</code></pre>
<p>更多的配置信息请<a href="https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8">参考这里</a>。</p>
<p>我们定义一个 DruidConfig 来加载所有的公共配置项，如下：</p>
<pre><code class="java language-java">@Component
@ConfigurationProperties(prefix="spring.datasource.druid")
public class DruidConfig {
    protected String url;
    protected String username;
    protected String password;
    protected String driverClassName;
    protected int initialSize;
    protected int minIdle;
    protected int maxActive;
    protected int maxWait;
    protected int timeBetweenEvictionRunsMillis;
    protected long minEvictableIdleTimeMillis;
    protected long maxEvictableIdleTimeMillis;
    protected String validationQuery;
    protected boolean testWhileIdle;
    protected boolean testOnBorrow;
    protected boolean testOnReturn;
    protected boolean poolPreparedStatements;
    protected int maxPoolPreparedStatementPerConnectionSize;
    protected String filters;
    protected String connectionProperties;
    // 省略 getter setter
}
</code></pre>
<p>再定义一个 DruidOneConfig 来加载数据源 1 的配置项，并继承 DruidConfig：</p>
<pre><code class="java language-java">@Component
@ConfigurationProperties(prefix="spring.datasource.druid.one")
public class DruidOneConfig  extends  DruidConfig{
    private String url;
    private String username;
    private String password;
    private String driverClassName;
    private int initialSize;
    private int minIdle;
    private int maxActive;
    // 省略 getter setter
}
</code></pre>
<p>再定义一个 DruidTwoConfig 来加载数据源 2 的配置项并继承 DruidConfig，代码和 DruidOneConfig 类基本一致。</p>
<h4 id="-5">启动时加载</h4>
<p>创建类 DruidDBConfig 在启动的时候注入配置的多数据源信息。</p>
<pre><code class="java language-java">@Configuration
public class DruidDBConfig {
    @Autowired
    private DruidConfig druidOneConfig;
    @Autowired
    private DruidConfig druidTwoConfig;
    @Autowired
    private DruidConfig druidConfig;

}
</code></pre>
<p>在类中创建 initDruidDataSource() 方法，初始化 Druid 数据源各属性。各个数据库的个性化配置从 config 对读取，公共配置项从 druidConfig 对象获取。</p>
<pre><code class="java language-java">private DruidDataSource initDruidDataSource(DruidConfig config) {
    DruidDataSource datasource = new DruidDataSource();

    datasource.setUrl(config.getUrl());
    datasource.setUsername(config.getUsername());
    datasource.setPassword(config.getPassword());
    datasource.setDriverClassName(config.getDriverClassName());
    datasource.setInitialSize(config.getInitialSize());
    datasource.setMinIdle(config.getMinIdle());
    datasource.setMaxActive(config.getMaxActive());

    // common config
    datasource.setMaxWait(druidConfig.getMaxWait());
    datasource.setTimeBetweenEvictionRunsMillis(druidConfig.getTimeBetweenEvictionRunsMillis());
    datasource.setMinEvictableIdleTimeMillis(druidConfig.getMinEvictableIdleTimeMillis());
    datasource.setMaxEvictableIdleTimeMillis(druidConfig.getMaxEvictableIdleTimeMillis());
    datasource.setValidationQuery(druidConfig.getValidationQuery());
    datasource.setTestWhileIdle(druidConfig.isTestWhileIdle());
    datasource.setTestOnBorrow(druidConfig.isTestOnBorrow());
    datasource.setTestOnReturn(druidConfig.isTestOnReturn());
    datasource.setPoolPreparedStatements(druidConfig.isPoolPreparedStatements());
    datasource.setMaxPoolPreparedStatementPerConnectionSize(druidConfig.getMaxPoolPreparedStatementPerConnectionSize());
    try {
        datasource.setFilters(druidConfig.getFilters());
    } catch (SQLException e) {
        logger.error("druid configuration initialization filter : {0}", e);
    }
    datasource.setConnectionProperties(druidConfig.getConnectionProperties());

    return datasource;
}
</code></pre>
<p>启动时调用 initDruidDataSource() 方法构建不同的数据源。</p>
<pre><code class="java language-java">@Bean(name = "primaryDataSource")
public DataSource dataSource() {
    return initDruidDataSource(druidOneConfig);
}

@Bean(name = "secondaryDataSource")
@Primary
public DataSource secondaryDataSource() {
    return initDruidDataSource(druidTwoConfig);
}
</code></pre>
<p>下面通过不同的数据源构建 entityManager，最后注入到 Repository 的逻辑和以前一样，变化的地方只是在数据源构建和开启监控页面。</p>
<h4 id="-6">开启监控页面</h4>
<p>因为我们使用了原生的 Druid 包，因此需要手动开启监控、配置统计相关内容。</p>
<pre><code class="java language-java">@Configuration
public class DruidConfiguration {
    @Bean
    public ServletRegistrationBean&lt;StatViewServlet&gt; druidStatViewServlet() {
        ServletRegistrationBean&lt;StatViewServlet&gt; servletRegistrationBean = new ServletRegistrationBean&lt;&gt;(new StatViewServlet(), "/druid/*");
        servletRegistrationBean.addInitParameter("loginUsername", "admin");
        servletRegistrationBean.addInitParameter("loginPassword", "admin");
        servletRegistrationBean.addInitParameter("resetEnable", "false");
        return servletRegistrationBean;
    }

    @Bean
    public FilterRegistrationBean&lt;WebStatFilter&gt; druidStatFilter() {
        FilterRegistrationBean&lt;WebStatFilter&gt; filterRegistrationBean = new FilterRegistrationBean&lt;&gt;(new WebStatFilter());
        filterRegistrationBean.setName("DruidWebStatFilter");
        filterRegistrationBean.addUrlPatterns("/*");
        filterRegistrationBean.addInitParameter("exclusions", "*.js,*.gif,*.jpg,*.png,*.css,*.ico,/druid/*");
        return filterRegistrationBean;
    }
}
</code></pre>
<p>配置完成后，重启启动项目访问地址 http://localhost:8080/druid/sql.html 就可以看到有两个数据源的 SQL 操作语句，证明多数据源 SQL 监控配置成功。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/druid04.png" alt="" /> </p>
<p>到此 JPA + Druid + 多数据源的集成完成了。</p>
<h3 id="-7">总结</h3>
<p>Druid 是一款非常优秀的数据库连接池开源软件，使用 Druid 提供的 druid-spring-boot-starter 可以非常简单地对 Druid 进行集成。Druid 提供了很多预置的功能，非常方便我们对 SQL 进行监控、分析。Druid 对 Spring Boot 2.0 的支持还不够完善，对于使用 Druid 的特殊场景，可以使用 Druid 原生包自行进行封装。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote>
<p>参考资料：<a href="https://github.com/alibaba/druid/wiki">Druid 官网指南</a></p></div></article>