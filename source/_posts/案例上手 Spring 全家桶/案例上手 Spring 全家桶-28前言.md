---
title: 案例上手 Spring 全家桶-28
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在前面的课程中，我们已经分别学习了 Spring、Spring MVC、MyBatis 框架的使用，在实际开发中我们通常会将这 3 个框架整合起来使用，就是所谓的 SSM 框架，是目前企业中比较常用的一种开发方式，首先来回顾一下这 3 个框架的基本概念。</p>
<p><strong>Spring</strong></p>
<p>Spring 是 2003 年兴起的一个轻量级的企业级开发框架，可以替代传统 Java 应用的 EJB 开发方式，解决企业应用开发的复杂性问题。经过十几年的发展，现在的 Spring 已经不仅仅是一个替代 EJB 的框架了，Spring Framework 已经发展成为一套完整的生态，为现代软件开发的各个方面提供解决方案，是目前 Java 开发的行业标准。</p>
<p><strong>Spring MVC</strong></p>
<p>Spring MVC 全称为 Spring Web MVC，是 Spring 家族的一员，基于 Spring 实现 MVC 设计模式的框架，Spring MVC 使得服务端开发变得更加简单方便。</p>
<p><strong>MyBatis</strong></p>
<p>MyBatis 是当前主流的 ORM 框架，完成对 JDBC 的封装，使得开发者可以更加方便地进行持久层代码开发，它的特点是简单易上手，更加灵活。</p>
<p>在 SSM 框架整合架构中，Spring、Spring MVC、MyBatis 分别负责不同的业务模块，共同完成企业级项目的开发需求。具体来讲，Spring MVC 负责 MVC 设计模式的实现，MyBatis 提供了数据持久层解决方案，Spring 来管理 Spring MVC 和 MyBatis，IoC 容器负责 Spring MVC 和 MyBatis 相关对象的创建和依赖注入，AOP 负责事务管理，SSM 整体结构如下图所示。</p>
<p><img src="https://images.gitbook.cn/e5844800-b7eb-11e9-acbd-8feb0c5ec6b6" width = "75%" /></p>
<p>了解完 SSM 框架整合的基本理解，接下来我们就来动手实现一个 SSM 框架的整合。</p>
<p>1. 创建 Maven Web 工程，pom.xml 添加相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
  &lt;!-- SpringMVC --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework&lt;/groupId&gt;
    &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
    &lt;version&gt;5.0.11.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- Spring JDBC --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework&lt;/groupId&gt;
    &lt;artifactId&gt;spring-jdbc&lt;/artifactId&gt;
    &lt;version&gt;5.0.11.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- Spring AOP --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework&lt;/groupId&gt;
    &lt;artifactId&gt;spring-aop&lt;/artifactId&gt;
    &lt;version&gt;5.0.11.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework&lt;/groupId&gt;
    &lt;artifactId&gt;spring-aspects&lt;/artifactId&gt;
    &lt;version&gt;5.0.11.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- MyBatis --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
    &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
    &lt;version&gt;3.4.5&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- MyBatis 整合 Spring --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
    &lt;artifactId&gt;mybatis-spring&lt;/artifactId&gt;
    &lt;version&gt;1.3.1&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- MySQL 驱动 --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;mysql&lt;/groupId&gt;
    &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
    &lt;version&gt;8.0.11&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- C3P0 --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;c3p0&lt;/groupId&gt;
    &lt;artifactId&gt;c3p0&lt;/artifactId&gt;
    &lt;version&gt;0.9.1.2&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- JSTL --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;jstl&lt;/groupId&gt;
    &lt;artifactId&gt;jstl&lt;/artifactId&gt;
    &lt;version&gt;1.2&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- ServletAPI --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
    &lt;artifactId&gt;javax.servlet-api&lt;/artifactId&gt;
    &lt;version&gt;3.1.0&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
    &lt;artifactId&gt;lombok&lt;/artifactId&gt;
    &lt;version&gt;1.18.6&lt;/version&gt;
    &lt;scope&gt;provided&lt;/scope&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. web.xml 配置开启 Spring、Spring MVC，同时设置字符编码过滤器，加载静态资源（因为 Spring MVC 会拦截所有请求，导致 JSP 页面中对 JS 和 CSS 的引用也被拦截，配置后可以把对静态资源（JS、CSS、图片等）的请求交给项目的默认拦截器而不是 Spring MVC）。</p>
<pre><code class="xml language-xml">&lt;web-app&gt;
  &lt;display-name&gt;Archetype Created Web Application&lt;/display-name&gt;
  &lt;!-- 启动 Spring --&gt;
  &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;classpath:applicationContext.xml&lt;/param-value&gt;
  &lt;/context-param&gt;
  &lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.context.ContextLoaderListener&lt;/listener-class&gt;
  &lt;/listener&gt;

  &lt;!-- Spring MVC 的前端控制器，拦截所有请求 --&gt;
  &lt;servlet&gt;
    &lt;servlet-name&gt;mvc-dispatcher&lt;/servlet-name&gt;
    &lt;servlet-class&gt;org.springframework.web.servlet.DispatcherServlet&lt;/servlet-class&gt;
    &lt;init-param&gt;
      &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
      &lt;param-value&gt;classpath:springmvc.xml&lt;/param-value&gt;
    &lt;/init-param&gt;
  &lt;/servlet&gt;

  &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;mvc-dispatcher&lt;/servlet-name&gt;
    &lt;url-pattern&gt;/&lt;/url-pattern&gt;
  &lt;/servlet-mapping&gt;

  &lt;!-- 字符编码过滤器，一定要放在所有过滤器之前 --&gt;
  &lt;filter&gt;
      &lt;filter-name&gt;CharacterEncodingFilter&lt;/filter-name&gt;
      &lt;filter-class&gt;org.springframework.web.filter.CharacterEncodingFilter&lt;/filter-class&gt;
      &lt;init-param&gt;
          &lt;param-name&gt;encoding&lt;/param-name&gt;
          &lt;param-value&gt;utf-8&lt;/param-value&gt;
      &lt;/init-param&gt;
      &lt;init-param&gt;
          &lt;param-name&gt;forceRequestEncoding&lt;/param-name&gt;
          &lt;param-value&gt;true&lt;/param-value&gt;
      &lt;/init-param&gt;
      &lt;init-param&gt;
          &lt;param-name&gt;forceResponseEncoding&lt;/param-name&gt;
          &lt;param-value&gt;true&lt;/param-value&gt;
      &lt;/init-param&gt;
  &lt;/filter&gt;
  &lt;filter-mapping&gt;
      &lt;filter-name&gt;CharacterEncodingFilter&lt;/filter-name&gt;
      &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
  &lt;/filter-mapping&gt;

  &lt;!-- 加载静态资源 --&gt;
  &lt;servlet-mapping&gt;
      &lt;servlet-name&gt;default&lt;/servlet-name&gt;
      &lt;url-pattern&gt;*.js&lt;/url-pattern&gt;
  &lt;/servlet-mapping&gt;

  &lt;servlet-mapping&gt;
      &lt;servlet-name&gt;default&lt;/servlet-name&gt;
      &lt;url-pattern&gt;*.css&lt;/url-pattern&gt;
  &lt;/servlet-mapping&gt;
&lt;/web-app&gt;
</code></pre>
<p>3. 在 resources 路径下创建各个框架的配置文件。</p>
<p><img src="https://images.gitbook.cn/57c0e100-b6cd-11e9-96e0-d90b4d8f55a3" width = "60%" /></p>
<ul>
<li>applicationContext.xml：Spring 的配置文件</li>
<li>dbconfig.properties：数据库配置文件</li>
<li>mybatis-config.xml：MyBatis 的配置文件</li>
<li>springmvc.xml：Spring MVC 的配置文件</li>
</ul>
<p>我们知道 Spring MVC 本就是 Spring 框架的一个后续产品，所以 Spring MVC 和 Spring 不存在整合，所谓的 SSM 整合实际上是将 MyBatis 和 Spring 进行整合，换句话说，让 Spring 来管理 MyBatis。</p>
<p>4. applicationContext.xml 中配置 MyBatis 相关信息，以及事务管理。</p>
<pre><code class="xml language-xml">&lt;!-- 加载外部文件 --&gt;
&lt;context:property-placeholder location="classpath:dbconfig.properties"/&gt;

&lt;!-- 配置 C3P0 数据源 --&gt;
&lt;bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource"&gt;
  &lt;property name="user" value="${jdbc.user}"&gt;&lt;/property&gt;
  &lt;property name="password" value="${jdbc.password}"&gt;&lt;/property&gt;
  &lt;property name="driverClass" value="${jdbc.driverClass}"&gt;&lt;/property&gt;
  &lt;property name="jdbcUrl" value="${jdbc.jdbcUrl}"&gt;&lt;/property&gt;
  &lt;property name="initialPoolSize" value="5"&gt;&lt;/property&gt;
  &lt;property name="maxPoolSize" value="10"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;!-- 配置 MyBatis SqlSessionFactory --&gt;
&lt;bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
  &lt;!-- 指定 MyBatis 数据源 --&gt;
  &lt;property name="dataSource" ref="dataSource"/&gt;
  &lt;!-- 指定 MyBatis mapper 文件的位置 --&gt;
  &lt;property name="mapperLocations" value="classpath:com/southwind/repository/*.xml"/&gt;
  &lt;!-- 指定 MyBatis 全局配置文件的位置 --&gt;
  &lt;property name="configLocation" value="classpath:mybatis-config.xml"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;!-- 扫描 MyBatis 的 mapper 接口 --&gt;
&lt;bean class="org.mybatis.spring.mapper.MapperScannerConfigurer"&gt;
  &lt;!--扫描所有 Repository 接口的实现，加入到 IoC 容器中 --&gt;
  &lt;property name="basePackage" value="com.southwind.repository"/&gt;
&lt;/bean&gt;

&lt;!-- 配置事务管理器 --&gt;
&lt;bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager"&gt;
  &lt;!-- 配置数据源 --&gt;
  &lt;property name="dataSource" ref="dataSource"&gt;&lt;/property&gt;
&lt;/bean&gt;

&lt;!-- 配置事务增强，事务如何切入  --&gt;
&lt;tx:advice id="txAdvice" transaction-manager="transactionManager"&gt;
  &lt;tx:attributes&gt;
    &lt;!-- 所有方法都是事务方法 --&gt;
    &lt;tx:method name="*"/&gt;
    &lt;!-- 以get开始的所有方法  --&gt;
    &lt;tx:method name="get*" read-only="true"/&gt;
  &lt;/tx:attributes&gt;
&lt;/tx:advice&gt;

&lt;!-- 开启基于注解的事务  --&gt;
&lt;aop:config&gt;
  &lt;!-- 切入点表达式 --&gt;
  &lt;aop:pointcut expression="execution(* com.southwind.service.impl.*.*(..))" id="txPoint"/&gt;
  &lt;!-- 配置事务增强 --&gt;
  &lt;aop:advisor advice-ref="txAdvice" pointcut-ref="txPoint"/&gt;
&lt;/aop:config&gt;
</code></pre>
<p>5. dbconfig.properties 配置数据库连接信息。</p>
<pre><code class="properties language-properties">jdbc.jdbcUrl=jdbc:mysql://localhost:3306/ssm?useUnicode=true&amp;characterEncoding=UTF-8
jdbc.driverClass=com.mysql.jdbc.Driver
jdbc.user=root
jdbc.password=root
</code></pre>
<p>6. mybatis-config.xml 配置 MyBatis 的相关设置，因为 MyBatis 的大部分配置交给 Spring 来管理了，即在applicationContext.xml 中进行了配置，所以 mybatis-config.xml 只是配置一些辅助性设置，可以省略。</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd"&gt;
&lt;configuration&gt;
    &lt;settings&gt;
        &lt;!-- 打印 SQL--&gt;
        &lt;setting name="logImpl" value="STDOUT_LOGGING" /&gt;
    &lt;/settings&gt;

    &lt;typeAliases&gt;
        &lt;!-- 指定一个包名，MyBatis 会在包名下搜索需要的JavaBean--&gt;
        &lt;package name="com.southwind.entity"/&gt;
    &lt;/typeAliases&gt;

&lt;/configuration&gt;
</code></pre>
<p>7. 配置 springmvc.xml。</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-3.2.xsd"&gt;

    &lt;!-- 告知 Spring，启用 Spring MVC 的注解驱动 --&gt;
    &lt;mvc:annotation-driven /&gt;

    &lt;!-- 扫描业务代码 --&gt;
    &lt;context:component-scan base-package="com.southwind"&gt;&lt;/context:component-scan&gt;

    &lt;!-- 配置视图解析器 --&gt;
    &lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
        &lt;property name="prefix" value="/"&gt;&lt;/property&gt;
        &lt;property name="suffix" value=".jsp"&gt;&lt;/property&gt;
    &lt;/bean&gt;

&lt;/beans&gt;
</code></pre>
<p>8. SSM 环境搭建完成，在 MySQL 中创建数据表 department、employee。</p>
<pre><code class="sql language-sql">CREATE TABLE `department` (
  `d_id` int(11) NOT NULL AUTO_INCREMENT,
  `d_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

INSERT INTO `department` VALUES ('1', '研发部');
INSERT INTO `department` VALUES ('2', '销售部');
INSERT INTO `department` VALUES ('3', '行政部');
</code></pre>
<pre><code class="sql language-sql">CREATE TABLE `employee` (
  `e_id` int(11) NOT NULL AUTO_INCREMENT,
  `e_name` varchar(255) DEFAULT NULL,
  `e_gender` varchar(255) DEFAULT NULL,
  `e_email` varchar(255) DEFAULT NULL,
  `e_tel` varchar(255) DEFAULT NULL,
  `d_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`e_id`),
  KEY `d_id` (`d_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `department` (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

INSERT INTO `employee` VALUES ('1', '张三', '男', 'zhangsan@163.com', '13567896657', '1');
INSERT INTO `employee` VALUES ('2', '李四', '男', 'lisi@163.com', '16789556789', '1');
INSERT INTO `employee` VALUES ('3', '王五', '男', 'wangwu@163.com', '16678906541', '2');
INSERT INTO `employee` VALUES ('4', '小明', '男', 'xiaoming@163.com', '15678956781', '2');
INSERT INTO `employee` VALUES ('5', '小红', '女', 'xiaohong@163.com', '13345678765', '3');
INSERT INTO `employee` VALUES ('6', '小花', '女', 'xiaohua@163.com', '18367654678', '3');
</code></pre>
<p>9. 创建实体类 Department、Employee。</p>
<pre><code class="java language-java">public class Department {
    private int id;
    private String name;
}
</code></pre>
<pre><code class="java language-java">public class Employee {
    private int id;
    private String name;
    private String gender;
    private String email;
    private String tel;
    private Department department;
}
</code></pre>
<p>10. 数据库测试数据创建完成，接下来开始写业务代码，首先 Handler。</p>
<pre><code class="java language-java">@Controller
public class EmployeeHandler {
    @Autowired
    private EmployeeService employeeService;

    @RequestMapping(value="/queryAll")
    public ModelAndView test(){
        List&lt;Employee&gt; list = employeeService.queryAll();
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("index");
        modelAndView.addObject("list", list);
        return modelAndView;
    }
}
</code></pre>
<p>11. Handler 调用 Service，创建 Service 接口及实现类。</p>
<pre><code class="java language-java">public interface EmployeeService {
    public List&lt;Employee&gt; queryAll();
}
</code></pre>
<pre><code class="java language-java">@Service
public class EmployeeServiceImpl implements EmployeeService{

    @Autowired
    private EmployeeRepository employeeRepository;

    public List&lt;Employee&gt; queryAll() {
        // TODO Auto-generated method stub
        return employeeRepository.queryAll();
    }

}
</code></pre>
<p>12. Service 调用 Repository，创建 Repository 接口，此时没有 Repository 的实现类，使用 MyBatis 框架，在 Repository.xml 中配置实现接口方法需要的 SQL，程序运行时，通过动态代理产生实现接口的代理对象。</p>
<pre><code class="java language-java">public interface EmployeeRepository {
    public List&lt;Employee&gt; queryAll();
}
</code></pre>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.EmployeeRepository"&gt;

    &lt;resultMap type="Employee" id="employeeMap"&gt;
        &lt;id property="id" column="e_id"/&gt;
        &lt;result property="name" column="e_name"/&gt;
        &lt;result property="gender" column="e_gender"/&gt;
        &lt;result property="email" column="e_email"/&gt;
        &lt;result property="tel" column="e_tel"/&gt;
        &lt;association property="department" javaType="Department"&gt;
            &lt;id property="id" column="d_id"/&gt;
            &lt;result property="name" column="d_name"/&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt; 

    &lt;select id="queryAll" resultMap="employeeMap"&gt;
        select * from employee e, department d where e.d_id = d.d_id
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>13. 创建 index.jsp，前端使用 Bootstrap 框架。</p>
<pre><code class="html language-html">&lt;body&gt;
    &lt;div class="container"&gt;
        &lt;!-- 标题 --&gt;
        &lt;div class="row"&gt;
            &lt;div class="col-md-12"&gt;
                &lt;h1&gt;SSM-员工管理&lt;/h1&gt;
            &lt;/div&gt;
        &lt;/div&gt;
        &lt;!-- 显示表格数据 --&gt;
        &lt;div class="row"&gt;
            &lt;div class="col-md-12"&gt;
                &lt;table class="table table-hover" id="emps_table"&gt;
                    &lt;thead&gt;
                        &lt;tr&gt;
                            &lt;th&gt;
                                &lt;input type="checkbox" id="check_all"/&gt;
                            &lt;/th&gt;
                            &lt;th&gt;编号&lt;/th&gt;
                            &lt;th&gt;姓名&lt;/th&gt;
                            &lt;th&gt;性别&lt;/th&gt;
                            &lt;th&gt;电子邮箱&lt;/th&gt;
                            &lt;th&gt;联系电话&lt;/th&gt;
                            &lt;th&gt;部门&lt;/th&gt;
                            &lt;th&gt;操作&lt;/th&gt;
                        &lt;/tr&gt;
                    &lt;/thead&gt;
                    &lt;tbody&gt;
                        &lt;c:forEach items="${list }" var="employee"&gt;
                            &lt;tr&gt;
                                &lt;td&gt;&lt;input type='checkbox' class='check_item'/&gt;&lt;/td&gt;
                                &lt;td&gt;${employee.id }&lt;/td&gt;
                                &lt;td&gt;${employee.name }&lt;/td&gt;
                                &lt;td&gt;${employee.gender }&lt;/td&gt;
                                &lt;td&gt;${employee.email }&lt;/td&gt;
                                &lt;td&gt;${employee.tel }&lt;/td&gt;
                                &lt;td&gt;${employee.department.name }&lt;/td&gt;
                                &lt;td&gt;
                                    &lt;button class="btn btn-primary btn-sm edit_btn"&gt;
                                        &lt;span class="glyphicon glyphicon-pencil"&gt;编辑&lt;/span&gt;
                                    &lt;/button&gt;&amp;nbsp;&amp;nbsp;
                                    &lt;button class="btn btn-danger btn-sm delete_btn"&gt;
                                        &lt;span class="glyphicon glyphicon-trash"&gt;删除&lt;/span&gt;
                                    &lt;/button&gt;
                                &lt;/td&gt;
                            &lt;/tr&gt;
                        &lt;/c:forEach&gt;
                    &lt;/tbody&gt;
                &lt;/table&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
</code></pre>
<p>14. 部署 Tomcat，启动测试，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/d3723920-b6cd-11e9-96e0-d90b4d8f55a3" alt="WX20190618-162938@2x" /></p>
<p>SSM 框架搭建成功。</p>
<p><strong>注意</strong></p>
<p>1. Handler、Service、Repository 交给 IoC 容器管理，一定要结合配置文件的自动扫描和类定义处的注解完成，对象之间的依赖注入通过 @Autowire 来完成。</p>
<pre><code class="xml language-xml">&lt;!-- 扫描业务代码 --&gt;
&lt;context:component-scan base-package="com.southwind"&gt;&lt;/context:component-scan&gt;
</code></pre>
<pre><code class="java language-java">@Controller
public class EmployeeHandler {

    @Autowired
    private EmployeeService employeeService;
</code></pre>
<p>2. Repository.xml 的 namspace 与 Repository 接口一定要对应起来，不能写错。</p>
<pre><code>&lt;mapper namespace="com.southwind.repository.EmployeeRepository"&gt;
</code></pre>
<p>3. Repository.xml 中 的 parameterType 和 resultType，或者 resultMap 所对应的类型要与 mybatis-config.xml 中配置的 typeAliases 结合使用，组成对应实体类的全类名，如果 mybatis-config.xml 中没有配置 typeAliases，则 Repository.xml 中直接写实体类的全类名即可。</p>
<pre><code class="xml language-xml">&lt;resultMap type="Employee" id="employeeMap"&gt;
</code></pre>
<pre><code class="xml language-xml">&lt;typeAliases&gt;
    &lt;!-- 指定一个包名，MyBatis 会在包名下搜索需要的 JavaBean--&gt;
    &lt;package name="com.southwind.entity"/&gt;
&lt;/typeAliases&gt;
</code></pre>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 SSM 框架整合的具体步骤，作为一个阶段的小结，我们将前面学习的 Spring、Spring MVC、MyBatis 框架整合起来完成一个小练习，SSM 框架整合开发是当前比较主流的 Java Web 技术栈，是每一个 Java 开发者都必须掌握的基本技术。</p>
<h3 id="-2">源码</h3>
<p><a href="https://github.com/southwind9801/gcssm.git">请点击这里查看源码</a></p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>