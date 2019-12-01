---
title: SSM 博客系统开发实战-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">接口设计</h3>
<p>项目开发一般都是分工协作的，大家要按照一定规则去开发，接口就是一套规则，设计人员定义好所有接口名称，接口参数以及返回值类型等，实现接口的人员负责实现接口的功能，接口一经定义就很难改变，因为牵一发而动全身，所以设计的时候就要考虑周全，尽量把所有可能性都考虑进去。创建接口步骤如下.</p>
<p>首先，新建接口包路径：</p>
<blockquote>
  <p>在 wang.dreamland.www 右键 -&gt; package -&gt; service</p>
</blockquote>
<p>以用户 User 为例：</p>
<blockquote>
  <p>点击 service -&gt; 右键 new -&gt; Java Class</p>
  <p>Name：UserService
  Kind：Interface（选择接口）</p>
</blockquote>
<p>接口一般主要包含增删改查方法。</p>
<p>1.用户注册。</p>
<pre><code>int regist(User user);
</code></pre>
<p>2.用户登录。</p>
<pre><code>User login(String email,String password);
</code></pre>
<p>3.根据用户邮箱查询用户。</p>
<pre><code>User findByEmail(String email);
</code></pre>
<p>4.根据用户手机号查询用户。</p>
<pre><code>User findByEmail(String phone);
</code></pre>
<p>5.根据 id 查询用户。</p>
<pre><code>User findById(Long id);
</code></pre>
<p>6.根据邮箱账号删除用户。</p>
<pre><code>void deleteByEmail(String email);
</code></pre>
<p>7.更新用户信息。</p>
<pre><code>void update(User user);
</code></pre>
<p>其他实体类以此类推创建接口方法，创建完成后如图：</p>
<p><img src="http://images.gitbook.cn/0cdb95e0-67e1-11e8-8d09-2b69210772e4" alt="" /></p>
<p>之后就是实现所有接口的方法了，在创建实现类之前首先引入通用 Mapper。</p>
<h3 id="mapper">通用 Mapper</h3>
<p>通用 Mapper 是基于 MyBatis 的一个插件，它实现了大部分常用的增删改查方法，只要继承它就能拥有所有的通用方法，省去手写 XML 的烦恼。但是对于复杂的查询语句还是需要手写 XML 的。</p>
<p>关于 MyBatis 的配置，之前已经讲解过，这里将配置文件中的部分注释解开。</p>
<p>1.在 spring-mybatis.xm 配置文件中，将自动扫描 mapping.xml 文件下面的注释解开，如下：</p>
<p><img src="http://images.gitbook.cn/5c35c390-67e1-11e8-b87e-87b76270ed83" alt="" /></p>
<p>mapping 文件夹就是我们以后存放手写 XML 的地方。</p>
<p>解开注释后发现报红，主要是缺少路径。点击 main 下的 resources，右键新建文件夹，命名为 mapping，然后新建一个 user.xml 文件即可。</p>
<pre><code class="     language-    ">    &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
    &lt;!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt;
    &lt;mapper namespace="wang.dreamland.www.dao.UserMapper"&gt;

    &lt;/mapper&gt;
</code></pre>
<p>其中 namespace 是名称空间，对应的是该实体类的 mapper 接口或者说 dao 接口，增删改查的 SQL 就写在 mapper 标签之间，我们暂时不写，以后用到了再写。</p>
<p>2.在 mybatis-config.xml 文件中，将自定义分页插件下面的注释解开，如下：</p>
<p><img src="http://images.gitbook.cn/acdc9580-67e1-11e8-b87e-87b76270ed83" alt="" /></p>
<p>然后在 wang.dreamland.www 右键新建包 common，作为通用包，包含常用工具类及分页插件等。然后将分页插件 PageHelper.java 复制到 common 包下。PageHelper.java 文件我会放到百度网盘中（见文末链接），大家直接导入即可，当做工具类使用。</p>
<p>导入 PageHelper.java 以后，打开 UserContentService，在该接口中增加关于分页查询的方法：</p>
<pre><code class="     language-    ">     /**
     * 查询所有Content并分页
     * @param content
     * @param pageNum
     * @param pageSize
     * @return
     */
    Page&lt;UserContent&gt;  findAll(UserContent content, Integer pageNum, Integer pageSize);
    Page&lt;UserContent&gt;  findAll(UserContent content, Comment comment, Integer pageNum, Integer pageSize);
    Page&lt;UserContent&gt;  findAllByUpvote(UserContent content, Integer pageNum, Integer pageSize);
</code></pre>
<p>3.根据接口创建实现类：</p>
<blockquote>
  <p>service -&gt; 右键 new -&gt; Package -&gt; impl -&gt; OK</p>
</blockquote>
<p>同样以 User 为例创建 UserServiceImpl，然后实现 UserService 接口并在类上加入 <code>@Service</code> 注解，表示属于 Service 层，Alt+Enter 重写所有方法。</p>
<pre><code>    @Service
    public class UserServiceImpl implements UserService {
        //实现所有方法  具体实现先不写
    }
</code></pre>
<p>4.在 wang.dreamland.www 上右键 -&gt; new -&gt; Package -&gt;dao，依次新建 UserMapper、UserInfoMapper、UserContentMapper、CommentMapper、LoginLogMapper、RoleMapper、UpvoteMapper 等接口。</p>
<p>并依次继承通用 Mapper 接口，一旦继承了 <code>Mapper&lt;T&gt;</code>，继承的 Mapper 就拥有了 <code>Mapper&lt;T&gt;</code> 所有的通用方法。例如 UserMapper：</p>
<pre><code>    public interface UserMapper extends Mapper&lt;User&gt;{

    }
</code></pre>
<p>此时 userMapper 就拥有了通用 Mapper 的所有通用方法。然后回到实现类 UserServiceImpl 中，重写实现方法如下：</p>
<pre><code class="     language-    ">    @Service
    public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;

    public int regist(User user) {
       return userMapper.insert(user);
    }

    public User login(String name, String password) {
        User user = new User();
        user.setEmail( name );
        user.setPassword( password );
        return userMapper.selectOne( user );
        //return userMapper.findUserByNameAndPwd( name,password );
    }

    public User findByEmail(String email) {
        User user = new User();
        user.setEmail( email );
        return userMapper.selectOne( user );
       // return userMapper.findByEmail(email);
    }

    @Override
    public User findByPhone(String phone) {
        User user = new User();
        user.setPhone(phone);
        return userMapper.selectOne(user);
    }

    @Override
    public User findById(Long id) {
        User user = new User();
        user.setId(id);
        return userMapper.selectOne(user);
    }

    public User findByEmailActive(String email) {
        User user = new User();
        user.setEmail( email );
        return userMapper.selectOne( user );
        // return userMapper.findByEmail(email);
    }

    public User findById(String id) {
        User user = new User();
        Long uid = Long.parseLong( id );
        user.setId( uid );
        return userMapper.selectOne( user );
    }

    public User findById(long id) {
        User user = new User();
        user.setId( id );
        return userMapper.selectOne( user );
    }

    public void deleteByEmail(String email) {
        User user = new User();
        user.setEmail( email );
        userMapper.delete( user );
    }

    public void deleteByEmailAndFalse(String email) {
        User user = new User();
        user.setEmail( email );
        userMapper.delete( user );
    }

    public void update(User user) {
        userMapper.updateByPrimaryKeySelective( user );
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入 UserMapper 对象，如果注入的 mapper 有报红，可能是 IDEA 工具的问题，可通过下面方式去除红色错误：</p>
<p><img src="http://images.gitbook.cn/386a71d0-67e2-11e8-9a37-f5d3ad5c8a4a" alt="" /></p>
<p>（2）通过 userMapper 中的通用方法分别实现每个方法。</p>
<h3 id="spring">Spring 事务管理</h3>
<p>事务是指访问并可能更新数据库中各种数据项的一个程序执行单元。事务可以是一条 SQL 语句或者一组 SQL 语句。</p>
<p>事务具有四个基本特性（ACID）：</p>
<ol>
<li><p>原子性（Atomicity）:一个事务是一个不可分割的工作单位，事务中包括的操作要么一起成功，要么一起失败；</p></li>
<li><p>一致性（Consistency）：事务必须使数据库从一个一致性状态变换到另一个一致性状态，也就是说一个事务执行之前和执行之后都必须处于一致性状态；</p></li>
<li><p>隔离性（Isolation）：一个事务的执行不能被其他事务干扰。比如多个用户操作同一张表时，数据库为每一个用户开启的事务，不能被其他事务的操作所干扰，多个并发事务之间要相互隔离；</p></li>
<li><p>持久性（Durability）：持久性是指一个事务一旦被提交了，那么对数据库中的数据的改变就是永久性的，即便是在数据库系统遇到故障的情况下也不会丢失提交事务的操作。</p></li>
</ol>
<p>关于事务的更多详细内容请查看相关文档，这里主要说下使用方法。</p>
<h4 id="-1">使用方法</h4>
<p>1.之前在 spring-mybatis.xml 配置文件中已配置事务管理，如下：</p>
<pre><code>    &lt;!-- 事务管理 --&gt;
    &lt;bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
    &lt;/bean&gt;

    &lt;tx:annotation-driven transaction-manager="transactionManager"/&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）将 DataSourceTransactionManager 交给 Spring 管理，注入数据源 dataSource；</p>
<p>（2）开启事务注解支持。</p>
<p>2.在 service.impl 包下的实现类的增、删、改方法上添加 <code>@Transactional</code> 注解，表示开启事务，注意导入的包是下面这个：</p>
<pre><code>import org.springframework.transaction.annotation.Transactional;
</code></pre>
<p>3.使用的数据库存储引擎要支持事务。</p>
<p>查看当前 MySQL 当前存储引擎，打开 Navicat -&gt; 选择数据库 -&gt; 点击查询 -&gt; 新建查询 -&gt; 输入如下查询语句 -&gt; 运行：</p>
<pre><code>show variables like '%storage_engine%'
</code></pre>
<p>如下图所示：</p>
<p><img src="http://images.gitbook.cn/49360990-67e5-11e8-af77-43c8fbf31a49" alt="" /></p>
<p>如果是 InnoDB 说明是支持事务的。如果不是，需要配置下，在配置文件 my.ini 中的 <code>[mysqld]</code> 下面加上如下配置：</p>
<pre><code>    default-storage-engine=INNODB 
</code></pre>
<p>如果不知道 my.ini 在哪，可以按下 WIN+R 组合键，在运行窗口中输入 services.msc，打开系统服务，找到 MySQL 服务，然后右键属性，可查看 my.ini 的路径，如图：</p>
<p><img src="http://images.gitbook.cn/6fe12d40-67e5-11e8-b87e-87b76270ed83" alt="" /></p>
<p>4.MySQL 事务默认是自动提交的（Autocommit），需要将自动提交关闭。</p>
<p>同样方法输入 SQL 语句后运行，关闭自动提交：</p>
<pre><code>set autocommit=0;  
</code></pre>
<p>查看自动提交是否已经关闭：</p>
<pre><code>select @@autocommit;
</code></pre>
<p>如果查询结果是0，说明自动提交已经关闭</p>
<h4 id="-2">单元测试事务回滚</h4>
<p>1.在 <code>src/test/java</code> 目录下新建 TestTransaction.java 测试类：</p>
<pre><code>    @ContextConfiguration(locations = {"classpath:spring-mybatis.xml","classpath:spring-mvc.xml"})
    public class TestTransaction extends AbstractJUnit4SpringContextTests {
    @Autowired
    private UserService userService;

    @Test
    public void testSave(){
        User user = new User();
        user.setNickName("封剑主-叹希奇");
        user.setEmail("123456@qq.com");
        userService.regist(user);
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）<code>@ContextConfiguration</code> 注解表示加载配置文件，如果有多个配置文件用逗号隔开；</p>
<p>（2）测试类必须要继承 AbstractJUnit4SpringContextTests 测试基类；</p>
<p>（3）通过 <code>@Autowired</code> 注解注入 UserService 对象；</p>
<p>（4）<code>@Test</code> 注解代表这是一个测试方法；</p>
<p>（5）在测试方法 testSave 方法中 new 一个对象 User，设置两个属性，然后调用 userService 的 regist 插入方法；</p>
<p>（6）点击 testSave 右键运行该方法。</p>
<p>此时查看数据库，发现数据库已经成功插入一条数据。然后将这条数据删除，进行事务回滚测试。</p>
<p>2.演示事务回滚。</p>
<p>在 UserServiceImpl 中，将 regist 方法修改如下：</p>
<pre><code>    @Transactional
    public int regist(User user) {
        int i = userMapper.insert(user);
        i = i / 0;
        return i;
    }
</code></pre>
<p>故意将 <code>i / 0</code>，制造 ArithmeticException 异常，我们预期的结果是数据插入不了数据库。</p>
<p>再次执行 testSave 方法，执行之后查看数据库，确实没有数据插入，说明事务回滚成功！</p>
<p>测试完成之后记得把 regist 方法恢复。</p>
<blockquote>
  <p>第04课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1tUb8qiGKZYm3p9fNQjlnfg 
  密码：8bc6</p>
</blockquote></div></article>