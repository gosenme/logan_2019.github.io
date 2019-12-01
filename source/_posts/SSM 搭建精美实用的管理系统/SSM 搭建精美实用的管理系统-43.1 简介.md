---
title: SSM 搭建精美实用的管理系统-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="31">3.1 简介</h3>
<p>基础环境搭建完成后，本文将开始整合 Spring MVC+Spring+Mybatis，整个过程会结合 Maven 工具进行，整个项目是一个普通的 Maven 工程。</p>
<p>如果不想使用 Maven 的话，推荐看一下十三发布在 GitHub 上的项目：<a href="https://github.com/ZHENFENG13/ssm-demo/tree/master/ssm-login">ssm-login</a>，此项目是一个基础的 Java Web 项目，没有使用 Maven，所有 Jar 包也都放到目录中。</p>
<p>不过我还是建议大家使用 Maven 工具进行 Jar 包的管理，非 Maven 的项目作为过渡项目是可以的，不建议一直使用，毕竟后面的实战教程也是 Maven 工程。</p>
<p>本文已将框架整合的过程完整详细列出，篇幅和过程有些长，如果觉得太麻烦，也可以跳过这些步骤，直接下载和使用即可，教程在最后一段。</p>
<h3 id="32maven">3.2 Maven 项目</h3>
<p>在整合之前，我们首先需要生成 Maven 工程骨架。</p>
<h4 id="1">1. 新建</h4>
<p>打开 IDEA 工具，通过 File -&gt; New -&gt; Project，新建项目，或者直接在 IDEA 欢迎页面点击新建项目，过程如下图：</p>
<p><img src="https://images.gitbook.cn/0b922850-8a43-11e8-a3f8-ff18634ae51e" alt="new-project" /></p>
<p>重点讲一下 “ New Project ” 这一页面，首先是左侧的选项栏，在这里需要选择你新建的项目类型，比如咱们需要新建的是 Maven 项目，则选择 “ Maven ” 选项，之后是设置 “ Project SDK ” ，即设置 Java 运行环境，前一篇中已经讲述了 JDK 8 的安装，选择其主目录即可，之后是选择 Maven 项目的模板，需要注意的是 “ Create from archetype ” 需要打上对勾，不然下面的所有模板将无法被选择，最后是选择本次的 Maven 项目模板，请注意是 “ org.apache.maven.archetypes:maven-archetype-webapp ”，之后点击 “ Next ” 进行下一步操作。</p>
<p><img src="https://images.gitbook.cn/1832ed00-8a44-11e8-974b-497483da0812" alt="new-maven-project" /></p>
<p>总结下，主要步骤包括：选择 Maven 项目、设置 JDK 、勾选 “ Create from archetype ” 、选择 “ maven-archetype-webapp ” 模板。</p>
<ul>
<li>名称、版本。</li>
</ul>
<p>点击 “ Next ” 之后则进入工程名称设置界面，如下图：</p>
<p><img src="https://images.gitbook.cn/37c90410-8a44-11e8-974b-497483da0812" alt="project-name" /></p>
<p>“ GroupID ” 是项目组织唯一的标识符，实际对应 Java 的包结构，是 main 目录里 Java 的目录结构，由于这是我们的第一个 SSM 项目，就设置为 com.ssm.demo 。</p>
<p>“ ArtifactID ” 是项目的唯一的标识符，实际对应项目的名称，也就是项目根目录的名称，名为 ssm-demo 。</p>
<p>Version 是项目版本号，IDEA 默认为 1.0-SNAPSHOT 。</p>
<p>温馨提示：以上三个配置项的命名都可以根据个人习惯或者公司要求来做，是一个较为主观的事情。 </p>
<ul>
<li>Maven 目录设置。</li>
</ul>
<p>点击 “ Next ” 之后则进入 Maven 相关设置界面，设置过程如下图：</p>
<p><img src="https://images.gitbook.cn/b530bec0-8a44-11e8-974b-497483da0812" alt="maven-setting" /></p>
<p>首先设置 Maven 工具的主目录及相关信息，前一篇文章中已经提到了 Maven 的安装，选择安装目录即可，下面的 “ Properties ” 即为上一步中设置的参数，这个步骤中有个参数需要注意一下：archetypeCatalog，建议将其设置为 “ internal ” ，点击右上角的加号设置即可。此步骤是为了提升 Maven 项目的生成速度，关于这个参数，有兴趣的朋友可以看一下十三的这篇文章：<a href="https://blog.csdn.net/ZHENFENGSHISAN/article/details/60149987">《解决新建 Maven 项目速度慢的问题》</a>。</p>
<ul>
<li>新建成功。</li>
</ul>
<p>最后就是设置本工程的磁盘路径了，如下图：</p>
<p><img src="https://images.gitbook.cn/2e974710-8a46-11e8-baa3-d3bd3f3e5753" alt="project-location" /></p>
<p>之后点击 “ Finish ” 按钮即可，整个过程就完成了，耐心地等待一会儿就可以看到如下情形：</p>
<p><img src="https://images.gitbook.cn/3dc318e0-8a46-11e8-affa-b587dc6ff574" alt="build-success" /></p>
<p>共耗时 13 秒第一个 Maven 项目构建成功！</p>
<h4 id="2">2. 整合</h4>
<p>接下来我们开始进行三大框架的整合工作。</p>
<ul>
<li>pom.xml 。</li>
</ul>
<p>首先是添加 Maven 依赖，生成的 Maven 工程中有 “ pom.xml ” 文件，POM 是项目对象模型（Project Object Model）的简称，它是 Maven 工程必不可少的文件，使用 XML 表示，该文件用于管理项目的依赖关系、开发者的信息和角色、组织信息、项目授权、项目的基础信息等等。</p>
<p>以下为本工程的 pom.xml 文件：</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"&gt;
    &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;
    &lt;groupId&gt;com.ssm.demo&lt;/groupId&gt;
    &lt;artifactId&gt;ssm-demo&lt;/artifactId&gt;
    &lt;packaging&gt;war&lt;/packaging&gt;
    &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
    &lt;name&gt;ssm-demo&lt;/name&gt;
    &lt;url&gt;http://maven.apache.org&lt;/url&gt;

    &lt;properties&gt;
        &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt;
        &lt;project.reporting.outputEncoding&gt;UTF-8&lt;/project.reporting.outputEncoding&gt;

        &lt;spring.version&gt;4.2.4.RELEASE&lt;/spring.version&gt;
        &lt;java.version&gt;1.8&lt;/java.version&gt;
        &lt;jdbc.driver.version&gt;5.1.38&lt;/jdbc.driver.version&gt;
        &lt;aspectj.version&gt;1.7.4&lt;/aspectj.version&gt;
        &lt;javax.servlet-api.version&gt;3.1.0&lt;/javax.servlet-api.version&gt;
        &lt;jsp-api.version&gt;2.2&lt;/jsp-api.version&gt;
        &lt;jstl.version&gt;1.2&lt;/jstl.version&gt;
        &lt;mybatis.version&gt;3.2.5&lt;/mybatis.version&gt;
        &lt;mybatis-spring.version&gt;1.2.2&lt;/mybatis-spring.version&gt;
        &lt;maven.test.skip&gt;true&lt;/maven.test.skip&gt;
    &lt;/properties&gt;

    &lt;dependencies&gt;
        &lt;!-- Begin: Spring依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-context-support&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-jdbc&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-tx&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- End: Spring依赖 --&gt;

        &lt;!-- Begin: Spring MVC依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- End: Spring MVC依赖 --&gt;

        &lt;!-- Begin: Mybatis依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
            &lt;version&gt;${mybatis.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring&lt;/artifactId&gt;
            &lt;version&gt;${mybatis-spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- End: mybatis依赖 --&gt;

        &lt;!-- Begin: 数据库依赖包 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;${jdbc.driver.version}&lt;/version&gt;
            &lt;scope&gt;runtime&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;!-- End: 数据库依赖包 --&gt;

        &lt;!-- Begin: aspectj相关jar包--&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.aspectj&lt;/groupId&gt;
            &lt;artifactId&gt;aspectjrt&lt;/artifactId&gt;
            &lt;version&gt;${aspectj.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.aspectj&lt;/groupId&gt;
            &lt;artifactId&gt;aspectjweaver&lt;/artifactId&gt;
            &lt;version&gt;${aspectj.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- End: aspectj相关jar包--&gt;

        &lt;!-- Begin: Servlet相关依赖包 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
            &lt;artifactId&gt;javax.servlet-api&lt;/artifactId&gt;
            &lt;version&gt;${javax.servlet-api.version}&lt;/version&gt;
            &lt;scope&gt;provided&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;javax.servlet.jsp&lt;/groupId&gt;
            &lt;artifactId&gt;jsp-api&lt;/artifactId&gt;
            &lt;version&gt;${jsp-api.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
            &lt;artifactId&gt;jstl&lt;/artifactId&gt;
            &lt;version&gt;${jstl.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- End: Servlet相关依赖包 --&gt;
    &lt;/dependencies&gt;

    &lt;build&gt;
        &lt;finalName&gt;ssm-demo&lt;/finalName&gt;
        &lt;plugins&gt;

            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-compiler-plugin&lt;/artifactId&gt;
                &lt;version&gt;3.2&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;source&gt;1.8&lt;/source&gt;
                    &lt;target&gt;1.8&lt;/target&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;

        &lt;/plugins&gt;
    &lt;/build&gt;
&lt;/project&gt;
</code></pre>
<ul>
<li>完善目录结构。</li>
</ul>
<p>通过 Maven 骨架生成的项目结构只有 main 目录及其目录下的  webapp 目录，这两个目录并不完善，缺少了 java 目录和  resource 目录，因此需要在 main 目录新建这两个目录，过程如下：</p>
<p>main -&gt; New -&gt; Directory -&gt; 新建 Java 目录
main -&gt; New -&gt; Directory -&gt; 新建 Resources 目录</p>
<p>之后需要右键选择 “ Mark Directory as ” ，分别将 java  目录和 resource 目录设置为 “ 源码根目录 ” 和 “ 配置文件目录 ” ，过程如下图：</p>
<p><img src="https://images.gitbook.cn/9647c5b0-8a46-11e8-974b-497483da0812" alt="build-success" /></p>
<p>这样 ssm-demo 的基本目录结构就完成了，如下图所示：</p>
<p><img src="https://images.gitbook.cn/93d96d90-8be2-11e8-a9c3-3f94e4ff5662" alt="" /></p>
<p>接下来需要新建代码目录，如下所示：</p>
<pre><code>controller ——控制层目录
dao        ——dao层目录
entity     ——实体层目录
service    ——业务层目录
utiles     ——工具类目录
</code></pre>
<p>之后在 resources 目录下新建 mappers 目录用来存放 MyBatis 的 mapper 文件，整个项目的目录结构就完成了，如下所示：</p>
<pre><code>ssm-demo                                ——项目名称
     ├── src/main/java                  ——Java 源码根目录
            ├── controller              ——控制层目录
            ├── dao                     ——dao层目录
            ├── entity                  ——实体层目录
            ├── service                 ——业务层目录
                └── impl                ——业务实现类目录
            └── utiles                  ——工具类目录
     ├── src/main/resources             ——配置文件根目录
            └── mappers                 ——mapper文件目录
     ├── src/main/webapp                ——网站 Web 资源
     └── pom.xml                        ——pom文件
</code></pre>
<ul>
<li>applicationContext.xml 。</li>
</ul>
<p>Spring 的核心默认配置文件的名字叫做 applicationContext.xml，如有需要也可以自行修改此名称，此文件是用于指导 Spring 工厂进行 Bean 生产、依赖关系注入（装配）及 Bean 实例分发的 “ 图纸 ” ，在常见的 Java Web 开发中，Spring 配置文件通常有一套万能的流程模板，如下所示：</p>
<p>——  注解驱动的依赖性注入，自动扫描；
——  存储数据库信息；
——  加载数据源；
——  装配 sessionFactory；
——  整合 ORM 框架，如 MyBatis；
——  配置事务；
——  配置事务通知属性；
——  配置事务切面；
——  整合 MVC 框架，如 Spring MVC 。</p>
<p>以下为 ssm-demo 的 Spring 配置文件：</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.0.xsd
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd

        http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.0.xsd"&gt;

    &lt;!-- 自动扫描 --&gt;
    &lt;context:component-scan base-package="com.ssm.demo.dao"/&gt;
    &lt;context:component-scan base-package="com.ssm.demo.service"/&gt;

    &lt;!-- 配置数据源 --&gt;
    &lt;bean id="dataSource"
          class="org.springframework.jdbc.datasource.DriverManagerDataSource"&gt;
        &lt;property name="driverClassName" value="com.mysql.jdbc.Driver"/&gt;
        &lt;property name="url"
                  value="jdbc:mysql://localhost:3306/ssm-demo"/&gt;
        &lt;!-- 改为你的地址即可 --&gt;
        &lt;property name="username" value="root"/&gt;
        &lt;property name="password" value="131313"/&gt;
    &lt;/bean&gt;


    &lt;!-- 配置mybatis的sqlSessionFactory --&gt;
    &lt;bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
        &lt;!-- 自动扫描mappers.xml文件 --&gt;
        &lt;!--&lt;property name="mapperLocations" value="classpath:mappers/*.xml"&gt;&lt;/property&gt;--&gt;
        &lt;!-- mybatis配置文件 --&gt;
        &lt;property name="configLocation" value="classpath:mybatis-config.xml"&gt;&lt;/property&gt;
    &lt;/bean&gt;

    &lt;!-- DAO接口所在包名，Spring会自动查找其下的类 --&gt;
    &lt;bean class="org.mybatis.spring.mapper.MapperScannerConfigurer"&gt;
        &lt;property name="basePackage" value="com.ssm.demo.dao"/&gt;
        &lt;property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"&gt;&lt;/property&gt;
    &lt;/bean&gt;

    &lt;!-- (事务管理)transaction manager, use JtaTransactionManager for global tx --&gt;
    &lt;bean id="transactionManager"
          class="org.springframework.jdbc.datasource.DataSourceTransactionManager"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
    &lt;/bean&gt;

    &lt;!-- 配置事务通知属性 --&gt;
    &lt;tx:advice id="txAdvice" transaction-manager="transactionManager"&gt;
        &lt;!-- 定义事务传播属性 --&gt;
        &lt;tx:attributes&gt;
            &lt;tx:method name="insert*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="update*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="upd*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="edit*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="save*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="add*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="new*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="set*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="remove*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="delete*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="del*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="change*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="check*" propagation="REQUIRED"/&gt;
            &lt;tx:method name="get*" propagation="REQUIRED" read-only="true"/&gt;
            &lt;tx:method name="search*" propagation="REQUIRED" read-only="true"/&gt;
            &lt;tx:method name="find*" propagation="REQUIRED" read-only="true"/&gt;
            &lt;tx:method name="load*" propagation="REQUIRED" read-only="true"/&gt;
            &lt;tx:method name="*" propagation="REQUIRED" read-only="true"/&gt;
        &lt;/tx:attributes&gt;
    &lt;/tx:advice&gt;

    &lt;!-- 配置事务切面 --&gt;
    &lt;aop:config&gt;
        &lt;aop:pointcut id="serviceOperation"
                      expression="(execution(* com.ssm.demo.service.*.*(..)))"/&gt;
        &lt;aop:advisor advice-ref="txAdvice" pointcut-ref="serviceOperation"/&gt;
    &lt;/aop:config&gt;

&lt;/beans&gt;
</code></pre>
<ul>
<li>mybatis-config.xml 。</li>
</ul>
<p>mybatis-config.xml 是 MyBatis 的核心配置文件，MyBatis 的相关配置都写在这个文件里，这里只做了简单的别名配置。</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd"&gt;
&lt;configuration&gt;
    &lt;typeAliases&gt;
        &lt;package name="com.ssm.demo.entity"/&gt;
    &lt;/typeAliases&gt;
&lt;/configuration&gt;
</code></pre>
<ul>
<li>spring-mvc.xml 。</li>
</ul>
<p>代码如下:</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd"&gt;

    &lt;!-- 使用注解的包，包括子集 --&gt;
    &lt;context:component-scan base-package="com.ssm.demo.controller"/&gt;

    &lt;!-- 视图解析器 --&gt;
    &lt;bean id="viewResolver"
          class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
        &lt;property name="prefix" value="/"/&gt;
        &lt;property name="suffix" value=".jsp"&gt;&lt;/property&gt;
    &lt;/bean&gt;
&lt;/beans&gt;
</code></pre>
<ul>
<li>web.xml 。</li>
</ul>
<p>关于三大框架的配置文件已创建且配置完成，想使得这些配置生效的话还需要一步操作，就是在 web.xml 中加入框架的设置语句， web.xml 文件是 Java web 项目中的一个配置文件，主要用于配置欢迎页、Filter 、Listener 、Servlet 等，ssm-demo 工程的 web.xml 配置文件如下：</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee"
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
         id="WebApp_ID" version="2.5"&gt;
    &lt;display-name&gt;ssm-demo&lt;/display-name&gt;


    &lt;!--Start 欢迎页--&gt;
    &lt;welcome-file-list&gt;
        &lt;welcome-file&gt;index.jsp&lt;/welcome-file&gt;
    &lt;/welcome-file-list&gt;
    &lt;!--End 欢迎页--&gt;

    &lt;context-param&gt;
        &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
        &lt;param-value&gt;classpath:applicationContext.xml&lt;/param-value&gt;
    &lt;/context-param&gt;

    &lt;!--Start 编码过滤器 解决乱码问题--&gt;
    &lt;filter&gt;
        &lt;filter-name&gt;encodingFilter&lt;/filter-name&gt;
        &lt;filter-class&gt;org.springframework.web.filter.CharacterEncodingFilter&lt;/filter-class&gt;
        &lt;init-param&gt;
            &lt;param-name&gt;encoding&lt;/param-name&gt;
            &lt;param-value&gt;UTF-8&lt;/param-value&gt;
        &lt;/init-param&gt;
    &lt;/filter&gt;
    &lt;filter-mapping&gt;
        &lt;filter-name&gt;encodingFilter&lt;/filter-name&gt;
        &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
    &lt;/filter-mapping&gt;
    &lt;!--End 编码过滤器 解决乱码问题--&gt;

    &lt;!--Start spring监听器 --&gt;
    &lt;listener&gt;
        &lt;listener-class&gt;org.springframework.web.context.ContextLoaderListener&lt;/listener-class&gt;
    &lt;/listener&gt;
    &lt;!--End Start spring监听器 --&gt;

    &lt;!--Start spring mvc servlet--&gt;
    &lt;servlet&gt;
        &lt;servlet-name&gt;springMVC&lt;/servlet-name&gt;
        &lt;servlet-class&gt;org.springframework.web.servlet.DispatcherServlet&lt;/servlet-class&gt;
        &lt;init-param&gt;
            &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
            &lt;param-value&gt;classpath:spring-mvc.xml&lt;/param-value&gt;
        &lt;/init-param&gt;
        &lt;load-on-startup&gt;1&lt;/load-on-startup&gt;
    &lt;/servlet&gt;
    &lt;!--End spring mvc servlet--&gt;

    &lt;!--Start servlet-mapping --&gt;
    &lt;servlet-mapping&gt;
        &lt;servlet-name&gt;springMVC&lt;/servlet-name&gt;
        &lt;url-pattern&gt;*.do&lt;/url-pattern&gt;
    &lt;/servlet-mapping&gt;
    &lt;!--End servlet-mapping --&gt;

&lt;/web-app&gt;
</code></pre>
<p>此配置文件主要定义了：</p>
<p>—— 工程基本信息：名字、描述（ display-name 和 description 标签)；
—— 声明应用范围内的初始化参数（ context-param 标签)；
—— 过滤器配置（ Filter 标签，如编码过滤器）；
—— 监听器配置（ Listener 标签）；
—— servlet配置（ servlet 标签，如 Spring MVC ）；
—— 欢迎页面（ welcome-file-list 标签，index.jsp 页面）。</p>
<p>以上即是一些通用的文件配置，当然还有诸如错误页面配置（ error-page 标签）、安全限制配置（ security-constraint  标签），以后如果用到的话再进行介绍。</p>
<p>到这里，配置已经完成了，目前 ssm-demo 的目录结构如下：</p>
<p><img src="https://images.gitbook.cn/047f07c0-8a54-11e8-974b-497483da0812" alt="ssm-dictionary" /></p>
<ul>
<li>构建。</li>
</ul>
<p>项目骨架生成且配置完成后，则需要进行构建验证了，在 ssm-demo 目录下执行命令行进行项目构建：</p>
<pre><code>mvn clean package
</code></pre>
<p>过程如下：</p>
<p><img src="https://images.gitbook.cn/1f04bbd0-8a54-11e8-974b-497483da0812" alt="mvn-clean-package" /></p>
<p>或者通过 IDEA 右边的 Maven 工具栏来进行构建，双击 “ clean ” 和 “ package ” 按钮即可:</p>
<p><img src="https://images.gitbook.cn/377b6600-8a54-11e8-8b1f-a92aedaeed58" alt="mvn-tool" /></p>
<p>可以看到已经生成的 target 目录已经有 “ ssm-demo.war ” 文件，这个 war 包文件可以直接部署，ssm-demo 作为教程的第一个项目还不是很完善，只有一个 JSP 页面可以看，因为还没有开始编写业务代码。</p>
<p>部署后可以看到如下场景：</p>
<p><img src="https://images.gitbook.cn/054249e0-8bd7-11e8-8998-e3cb09ec2904" alt="hello-ssm" /></p>
<p>证明三大框架基础整合成功！</p>
<h3 id="33">3.3 总结</h3>
<p>整合的过程，十三已详细做了说明，篇幅和过程有些长，如果觉得太麻烦的话也可以跳过这些步骤。文章最后贴出了代码的百度云下载地址，如果想直接使用项目的话也是可以的，下载代码后解压，并使用 IDEA 或者其他工具打开即可，过程如下：</p>
<p><img src="https://images.gitbook.cn/3f5505b0-8a55-11e8-a075-e124f05aa6d6" alt="download-ssm-demo" /></p>
<p>需要注意的是，在 applicationContext.xml 配置文件中已经配置了数据源信息，如果数据库环境没有安装或者数据库信息不匹配的话在部署的时候可能会报错，这里需要注意。</p>
<p>关于部署的相关知识点会在后面课程详细介绍。</p>
<blockquote>
  <p>本篇教程所完成的整合代码也已经上传到百度云，地址和提取密码如下：</p>
  <p>链接：https://pan.baidu.com/s/1cYmu1WLEWdfedbvLK-2MBQ </p>
  <p>密码：lbty</p>
</blockquote></div></article>