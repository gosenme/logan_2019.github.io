---
title: 案例上手 Spring 全家桶-34
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>这节课我们用本阶段所学知识实现一个权限管理系统，帮助大家掌握所学技术在实际开发中的使用。</p>
<p>需求简介：</p>
<ol>
<li>权限管理：查询、创建、修改、删除</li>
<li>角色管理：查询、创建、修改、删除、添加权限</li>
<li>用户管理：查询、创建、修改、删除、添加角色</li>
<li>用户登录：登录成功根据该用户角色动态生成权限菜单</li>
</ol>
<p>开发环境：</p>
<ul>
<li>JDK 10.0.1</li>
<li>Maven 3.5.3</li>
<li>tomcat 9.0.8</li>
<li>Eclipse Photon</li>
</ul>
<p>技术选型：</p>
<blockquote>
  <p>layui-v2.3.0 + Spring MVC 4.3.1 + Spring Data 1.8.0 + MongoDB 4.0.0</p>
</blockquote>
<p>代码实现：</p>
<p>1. 新建 Maven Project，选择 webapp 项目。</p>
<p><img src="https://images.gitbook.cn/7b248f00-9ae2-11e8-a178-519d5b470954" width = "70%" /></p>
<p>2. pom.xml 添加相关依赖。</p>
<pre><code class="xml language-xml">&lt;!-- JSTL --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;jstl&lt;/groupId&gt;
    &lt;artifactId&gt;jstl&lt;/artifactId&gt;
    &lt;version&gt;1.2&lt;/version&gt;
&lt;/dependency&gt;

&lt;!-- ServletAPI --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
    &lt;artifactId&gt;javax.servlet-api&lt;/artifactId&gt;
    &lt;version&gt;3.0.1&lt;/version&gt;
    &lt;scope&gt;provided&lt;/scope&gt;
&lt;/dependency&gt;

&lt;!-- Spring MVC --&gt;
&lt;dependency&gt;
     &lt;groupId&gt;org.springframework&lt;/groupId&gt;
     &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
     &lt;version&gt;4.3.1.RELEASE&lt;/version&gt;
&lt;/dependency&gt;

&lt;!-- Spring Data MongoDB --&gt;
&lt;dependency&gt;
     &lt;groupId&gt;org.springframework.data&lt;/groupId&gt;
     &lt;artifactId&gt;spring-data-mongodb&lt;/artifactId&gt;
     &lt;version&gt;1.8.0.RELEASE&lt;/version&gt;
&lt;/dependency&gt;

&lt;!-- alifastjson --&gt;
&lt;dependency&gt;
     &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
     &lt;artifactId&gt;fastjson&lt;/artifactId&gt;
     &lt;version&gt;1.2.18&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>3. 创建实体类 Authority，添加注解与 MongoDB 集合进行映射。</p>
<pre><code class="java language-java">@Document
public class Authority {
    @Id
    private String id;
    @Field
    private String name;
    private boolean has;    
}
</code></pre>
<p>4. 创建 AuthorityVO 类，前端使用 layui 框架，数据表格通过异步加载的方式渲染数据，后台需要返回符合 layui 格式的 JSON 数据，官方文档给出的格式如下，所以我们需要创建 AuthorityVO 类，目的是将 Authority 按照 layui 要求的格式进行封装。</p>
<p><img src="https://images.gitbook.cn/9450a680-9ae2-11e8-8cbe-ad3f3badcc18" width = "60%" /></p>
<p>AuthorityVO：</p>
<pre><code class="java language-java">public class AuthorityVO {
    private int code;
    private String mess;
    private long count;
    private List&lt;Authority&gt; data;
}
</code></pre>
<p>同理创建 Role 和 User 的 VO 类。</p>
<p>5. 创建 Reposity 接口，继承 CrudReposity 接口，完成对数据层的访问和操作。</p>
<p>AuthorityReposity：</p>
<pre><code class="java language-java">@Repository
public interface AuthorityRepository extends CrudRepository&lt;Authority, String&gt;{
    public Authority findById(String id);
    public void deleteById(String id);
    //分页查询
    public PageImpl findAll(Pageable pageable);
}
</code></pre>
<p>RoleReposity：</p>
<pre><code class="java language-java">@Repository
public interface RoleRepository extends CrudRepository&lt;Role, String&gt;{
    public Role findById(String id);
    public void deleteById(String id);
    //分页查询
    public PageImpl findAll(Pageable pageable);
}
</code></pre>
<p>UserReposity：</p>
<pre><code class="java language-java">@Repository
public interface UserRepository extends CrudRepository&lt;User, String&gt;{
    public User findById(String id);
    public void deleteById(String id);
    public User findByName(String name);
    //分页查询
    public PageImpl findAll(Pageable pageable);
}
</code></pre>
<p>6. 创建控制层 Handler。</p>
<p>AuthorityHandler：</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/authority")
public class AuthorityHandler {

    @Autowired
    private AuthorityRepository authorityRepository;

}
</code></pre>
<p>RoleHandler：</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/role")
public class RoleHandler {

    @Autowired
    private RoleRepository roleRepository;
    @Autowired
    private AuthorityRepository authorityRepository;

}
</code></pre>
<p>UserHandler：</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/user")
public class UserHandler {

    @Autowired
    private RoleRepository roleRepository;
    @Autowired
    private UserRepository userRepository;

}
</code></pre>
<p>LoginHandler：</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/login")
public class LoginHandler {

    @Autowired
    private UserRepository userRepository;
    @Autowired
    private RoleRepository roleRepository;
    @Autowired
    private AuthorityRepository authorityRepository;

}
</code></pre>
<p>7. 配置文件。</p>
<p>spring.xml：</p>
<pre><code class="xml language-xml">&lt;!-- Spring 连接 MongoDB 客户端配置 --&gt;
&lt;mongo:mongo-client host="127.0.0.1" port="12345" id="mongo"/&gt;

&lt;!-- 配置 MongoDB 目标数据库 --&gt;
&lt;mongo:db-factory dbname="testdb" mongo-ref="mongo" /&gt;

&lt;!-- 配置 MongoTemplate --&gt;
&lt;bean id="mongoTemplate" class="org.springframework.data.mongodb.core.MongoTemplate"&gt;
  &lt;constructor-arg name="mongoDbFactory" ref="mongoDbFactory"/&gt;
 &lt;/bean&gt;

&lt;!-- 扫描 Reposity 接口 --&gt;
&lt;mongo:repositories base-package="com.southwind.repository"&gt;&lt;/mongo:repositories&gt;
</code></pre>
<p>springmvc.xml：</p>
<pre><code class="xml language-xml">&lt;!-- 配置自动扫描 --&gt;
&lt;context:component-scan base-package="com.southwind"&gt;&lt;/context:component-scan&gt;

&lt;!-- 配置视图解析器 --&gt;
&lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
    &lt;!-- 前缀 --&gt;
    &lt;property name="prefix" value="/"&gt;&lt;/property&gt;
    &lt;!-- 后缀 --&gt;
    &lt;property name="suffix" value=".jsp"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;mvc:annotation-driven &gt;
    &lt;!-- 消息转换器 --&gt;
    &lt;mvc:message-converters register-defaults="true"&gt;
       &lt;!-- 阿里 fastjson --&gt;
       &lt;bean class="com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter4"/&gt;
    &lt;/mvc:message-converters&gt;
&lt;/mvc:annotation-driven&gt;
</code></pre>
<p>8. JSP 页面使用 layui 框架完成布局和渲染。</p>
<p>程序截图：</p>
<p><img src="https://images.gitbook.cn/90632330-9ae3-11e8-b37c-dd4feba3837e" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/9811d7c0-9ae3-11e8-8cbe-ad3f3badcc18" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/b1672cb0-9ae4-11e8-8cbe-ad3f3badcc18" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/b5a5e7d0-9ae4-11e8-b37c-dd4feba3837e" width = "70%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们用 Spring MVC + LayUI + Spring Data + MongoDB 的技术选型实现了一个项目整合案例，第一个目的是带领大家对本阶段学习的重点知识点进行系统性梳理，另外一个目的是给大家提供一个新的技术选型，包括前、后端分离的一些简单应用，相信这套技术选型对大家会有一定的帮助。</p>
<h3 id="-2">源码</h3>
<p><a href="https://github.com/southwind9801/AuthorityManagement.git">请点击这里查看源码</a></p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
  <p>温馨提示：需购买才可入群哦，加小助手微信后需要截已购买的图来验证~</p>
</blockquote></div></article>