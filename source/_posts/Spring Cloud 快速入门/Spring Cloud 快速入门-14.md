---
title: Spring Cloud 快速入门-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>首先我们应知道，事务是为了保证数据的一致性而产生的。那么分布式事务，顾名思义，就是我们要保证分布在不同数据库、不同服务器、不同应用之间的数据一致性。</p>
<h3 id="">为什么需要分布式事务？</h3>
<p>最传统的架构是单一架构，数据是存放在一个数据库上的，采用数据库的事务就能满足我们的要求。随着业务的不断扩张，数据的不断增加，单一数据库已经到达了一个瓶颈，因此我们需要对数据库进行分库分表。为了保证数据的一致性，可能需要不同的数据库之间的数据要么同时成功，要么同时失败，否则可能导致产生一些脏数据，也可能滋生 Bug。</p>
<p>在这种情况下，分布式事务思想应运而生。</p>
<h3 id="-1">应用场景</h3>
<p>分布式事务的应用场景很广，我也无法一一举例，本文列举出比较常见的场景，以便于读者在实际项目中，在用到了一些场景时即可考虑分布式事务。</p>
<h4 id="-2">支付</h4>
<p>最经典的场景就是支付了，一笔支付，是对买家账户进行扣款，同时对卖家账户进行加钱，这些操作必须在一个事务里执行，要么全部成功，要么全部失败。而对于买家账户属于买家中心，对应的是买家数据库，而卖家账户属于卖家中心，对应的是卖家数据库，对不同数据库的操作必然需要引入分布式事务。</p>
<h4 id="-3">在线下单</h4>
<p>买家在电商平台下单，往往会涉及到两个动作，一个是扣库存，第二个是更新订单状态，库存和订单一般属于不同的数据库，需要使用分布式事务保证数据一致性。</p>
<h4 id="-4">银行转账</h4>
<p>账户 A 转账到账户 B，实际操作是账户 A 减去相应金额，账户 B 增加相应金额，在分库分表的前提下，账户 A 和账户 B 可能分别存储在不同的数据库中，这时需要使用分布式事务保证数据库一致性。否则可能导致的后果是 A 扣了钱 B 却没有增加钱，或者 B 增加了钱 A 却没有扣钱。</p>
<h3 id="springbootatomikos">SpringBoot 集成 Atomikos 实现分布式事务</h3>
<h4 id="atomikos">Atomikos 简介</h4>
<p>Atomikos 是一个为 Java 平台提供增值服务的开源类事务管理器。</p>
<p>以下是包括在这个开源版本中的一些功能：</p>
<ul>
<li>全面崩溃 / 重启恢复；</li>
<li>兼容标准的 SUN 公司 JTA API；</li>
<li>嵌套事务；</li>
<li>为 XA 和非 XA 提供内置的 JDBC 适配器。</li>
</ul>
<blockquote>
  <p>注释：XA 协议由 Tuxedo 首先提出的，并交给 X/Open 组织，作为资源管理器（数据库）与事务管理器的接口标准。目前，Oracle、Informix、DB2 和 Sybase 等各大数据库厂家都提供对 XA 的支持。XA 协议采用两阶段提交方式来管理分布式事务。XA 接口提供资源管理器与事务管理器之间进行通信的标准接口。XA 协议包括两套函数，以 <code>xa_</code> 开头的及以 <code>ax_</code> 开头的。</p>
</blockquote>
<h4 id="-5">具体实现</h4>
<p>1.在本地创建两个数据库：test01，test02，并且创建相同的数据库表：</p>
<p><img src="http://images.gitbook.cn/9f49fae0-662c-11e8-8202-7be2e53cf056" alt="enter image description here" /></p>
<p>2.改造上篇的工程，在 pom.xml 增加以下依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-jta-atomikos&lt;/artifactId&gt;
        &lt;/dependency&gt;

        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;1.1.1&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;5.1.40&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre>
<p>3.修改配置文件 application.yml 如下：</p>
<pre><code class="yaml language-yaml">server:
  port: 8080
spring:
  redis:
    host: localhost
    port: 6379
mysql:
  datasource:
    test1:
      url: jdbc:mysql://localhost:3306/test01?useUnicode=true&amp;characterEncoding=utf-8
      username: root
      password: 1qaz2wsx
      minPoolSize: 3
      maxPoolSize: 25
      maxLifetime: 20000
      borrowConnectionTimeout: 30
      loginTimeout: 30
      maintenanceInterval: 60
      maxIdleTime: 60
      testQuery: select 1
    test2:
      url: jdbc:mysql://localhost:3306/test02?useUnicode=true&amp;characterEncoding=utf-8
      username: root
      password: 1qaz2wsx
      minPoolSize: 3
      maxPoolSize: 25
      maxLifetime: 20000
      borrowConnectionTimeout: 30
      loginTimeout: 30
      maintenanceInterval: 60
      maxIdleTime: 60
      testQuery: select 1
</code></pre>
<p>4.创建以下类：</p>
<pre><code class="java language-java">@ConfigurationProperties(prefix = "mysql.datasource.test1")
@SpringBootConfiguration
public class DBConfig1 {

    private String url;
    private String username;
    private String password;
    private int minPoolSize;
    private int maxPoolSize;
    private int maxLifetime;
    private int borrowConnectionTimeout;
    private int loginTimeout;
    private int maintenanceInterval;
    private int maxIdleTime;
    private String testQuery;
    public String getUrl() {
        return url;
    }
    public void setUrl(String url) {
        this.url = url;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public int getMinPoolSize() {
        return minPoolSize;
    }
    public void setMinPoolSize(int minPoolSize) {
        this.minPoolSize = minPoolSize;
    }
    public int getMaxPoolSize() {
        return maxPoolSize;
    }
    public void setMaxPoolSize(int maxPoolSize) {
        this.maxPoolSize = maxPoolSize;
    }
    public int getMaxLifetime() {
        return maxLifetime;
    }
    public void setMaxLifetime(int maxLifetime) {
        this.maxLifetime = maxLifetime;
    }
    public int getBorrowConnectionTimeout() {
        return borrowConnectionTimeout;
    }
    public void setBorrowConnectionTimeout(int borrowConnectionTimeout) {
        this.borrowConnectionTimeout = borrowConnectionTimeout;
    }
    public int getLoginTimeout() {
        return loginTimeout;
    }
    public void setLoginTimeout(int loginTimeout) {
        this.loginTimeout = loginTimeout;
    }
    public int getMaintenanceInterval() {
        return maintenanceInterval;
    }
    public void setMaintenanceInterval(int maintenanceInterval) {
        this.maintenanceInterval = maintenanceInterval;
    }
    public int getMaxIdleTime() {
        return maxIdleTime;
    }
    public void setMaxIdleTime(int maxIdleTime) {
        this.maxIdleTime = maxIdleTime;
    }
    public String getTestQuery() {
        return testQuery;
    }
    public void setTestQuery(String testQuery) {
        this.testQuery = testQuery;
    }

}
</code></pre>
<pre><code class="java language-java">@ConfigurationProperties(prefix = "mysql.datasource.test2")
@SpringBootConfiguration
public class DBConfig2 {

    private String url;
    private String username;
    private String password;
    private int minPoolSize;
    private int maxPoolSize;
    private int maxLifetime;
    private int borrowConnectionTimeout;
    private int loginTimeout;
    private int maintenanceInterval;
    private int maxIdleTime;
    private String testQuery;
    public String getUrl() {
        return url;
    }
    public void setUrl(String url) {
        this.url = url;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public int getMinPoolSize() {
        return minPoolSize;
    }
    public void setMinPoolSize(int minPoolSize) {
        this.minPoolSize = minPoolSize;
    }
    public int getMaxPoolSize() {
        return maxPoolSize;
    }
    public void setMaxPoolSize(int maxPoolSize) {
        this.maxPoolSize = maxPoolSize;
    }
    public int getMaxLifetime() {
        return maxLifetime;
    }
    public void setMaxLifetime(int maxLifetime) {
        this.maxLifetime = maxLifetime;
    }
    public int getBorrowConnectionTimeout() {
        return borrowConnectionTimeout;
    }
    public void setBorrowConnectionTimeout(int borrowConnectionTimeout) {
        this.borrowConnectionTimeout = borrowConnectionTimeout;
    }
    public int getLoginTimeout() {
        return loginTimeout;
    }
    public void setLoginTimeout(int loginTimeout) {
        this.loginTimeout = loginTimeout;
    }
    public int getMaintenanceInterval() {
        return maintenanceInterval;
    }
    public void setMaintenanceInterval(int maintenanceInterval) {
        this.maintenanceInterval = maintenanceInterval;
    }
    public int getMaxIdleTime() {
        return maxIdleTime;
    }
    public void setMaxIdleTime(int maxIdleTime) {
        this.maxIdleTime = maxIdleTime;
    }
    public String getTestQuery() {
        return testQuery;
    }
    public void setTestQuery(String testQuery) {
        this.testQuery = testQuery;
    }

}
</code></pre>
<pre><code class="java language-java">@SpringBootConfiguration
@MapperScan(basePackages = "com.lynn.demo.test01", sqlSessionTemplateRef = "sqlSessionTemplate")
public class MyBatisConfig1 {

    // 配置数据源
    @Primary
    @Bean(name = "dataSource")
    public DataSource dataSource(DBConfig1 config) throws SQLException {
        MysqlXADataSource mysqlXaDataSource = new MysqlXADataSource();
        mysqlXaDataSource.setUrl(config.getUrl());
        mysqlXaDataSource.setPinGlobalTxToPhysicalConnection(true);
        mysqlXaDataSource.setPassword(config.getPassword());
        mysqlXaDataSource.setUser(config.getUsername());
        mysqlXaDataSource.setPinGlobalTxToPhysicalConnection(true);

        AtomikosDataSourceBean xaDataSource = new AtomikosDataSourceBean();
        xaDataSource.setXaDataSource(mysqlXaDataSource);
        xaDataSource.setUniqueResourceName("dataSource");

        xaDataSource.setMinPoolSize(config.getMinPoolSize());
        xaDataSource.setMaxPoolSize(config.getMaxPoolSize());
        xaDataSource.setMaxLifetime(config.getMaxLifetime());
        xaDataSource.setBorrowConnectionTimeout(config.getBorrowConnectionTimeout());
        xaDataSource.setLoginTimeout(config.getLoginTimeout());
        xaDataSource.setMaintenanceInterval(config.getMaintenanceInterval());
        xaDataSource.setMaxIdleTime(config.getMaxIdleTime());
        xaDataSource.setTestQuery(config.getTestQuery());
        return xaDataSource;
    }
    @Primary
    @Bean(name = "sqlSessionFactory")
    public SqlSessionFactory sqlSessionFactory(@Qualifier("dataSource") DataSource dataSource)
            throws Exception {
        SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
        bean.setDataSource(dataSource);
        return bean.getObject();
    }

    @Primary
    @Bean(name = "sqlSessionTemplate")
    public SqlSessionTemplate sqlSessionTemplate(
            @Qualifier("sqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
</code></pre>
<pre><code class="java language-java">@SpringBootConfiguration
//basePackages 最好分开配置 如果放在同一个文件夹可能会报错
@MapperScan(basePackages = "com.lynn.demo.test02", sqlSessionTemplateRef = "sqlSessionTemplate2")
public class MyBatisConfig2 {

    // 配置数据源
    @Bean(name = "dataSource2")
    public DataSource dataSource(DBConfig2 config) throws SQLException {
        MysqlXADataSource mysqlXaDataSource = new MysqlXADataSource();
        mysqlXaDataSource.setUrl(config.getUrl());
        mysqlXaDataSource.setPinGlobalTxToPhysicalConnection(true);
        mysqlXaDataSource.setPassword(config.getPassword());
        mysqlXaDataSource.setUser(config.getUsername());
        mysqlXaDataSource.setPinGlobalTxToPhysicalConnection(true);

        AtomikosDataSourceBean xaDataSource = new AtomikosDataSourceBean();
        xaDataSource.setXaDataSource(mysqlXaDataSource);
        xaDataSource.setUniqueResourceName("dataSource2");

        xaDataSource.setMinPoolSize(config.getMinPoolSize());
        xaDataSource.setMaxPoolSize(config.getMaxPoolSize());
        xaDataSource.setMaxLifetime(config.getMaxLifetime());
        xaDataSource.setBorrowConnectionTimeout(config.getBorrowConnectionTimeout());
        xaDataSource.setLoginTimeout(config.getLoginTimeout());
        xaDataSource.setMaintenanceInterval(config.getMaintenanceInterval());
        xaDataSource.setMaxIdleTime(config.getMaxIdleTime());
        xaDataSource.setTestQuery(config.getTestQuery());
        return xaDataSource;
    }

    @Bean(name = "sqlSessionFactory2")
    public SqlSessionFactory sqlSessionFactory(@Qualifier("dataSource2") DataSource dataSource)
            throws Exception {
        SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
        bean.setDataSource(dataSource);
        return bean.getObject();
    }

    @Bean(name = "sqlSessionTemplate2")
    public SqlSessionTemplate sqlSessionTemplate(
            @Qualifier("sqlSessionFactory2") SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
</code></pre>
<p>在 com.lynn.demo.test01 和 com.lynn.demo.test02 中分别创建以下 mapper：</p>
<pre><code class="java language-java">@Mapper
public interface UserMapper1 {

    @Insert("insert into test_user(name,age) values(#{name},#{age})")
    void addUser(@Param("name")String name,@Param("age") int age);
}
</code></pre>
<pre><code class="java language-java">@Mapper
public interface UserMapper2 {

    @Insert("insert into test_user(name,age) values(#{name},#{age})")
    void addUser(@Param("name") String name,@Param("age") int age);
}
</code></pre>
<p>创建 service 类：</p>
<pre><code class="java language-java">@Service
public class UserService {

    @Autowired
    private UserMapper1 userMapper1;
    @Autowired
    private UserMapper2 userMapper2;

    @Transactional
    public void addUser(User user)throws Exception{
        userMapper1.addUser(user.getName(),user.getAge());
        userMapper2.addUser(user.getName(),user.getAge());
    }
}
</code></pre>
<p>5.创建单元测试类进行测试：</p>
<pre><code class="java language-java">@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(classes = Application.class)
public class TestDB {

    @Autowired
    private UserService userService;

    @Test
    public void test(){
        User user = new User();
        user.setName("lynn");
        user.setAge(10);
        try {
            userService.addUser(user);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
</code></pre>
<p>经过测试，如果没有报错，则数据被分别添加到两个数据库表中，如果有报错，则数据不会增加。</p></div></article>