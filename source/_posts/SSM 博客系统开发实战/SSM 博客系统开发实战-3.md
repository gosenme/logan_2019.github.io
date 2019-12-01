---
title: SSM 博客系统开发实战-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇通过 Maven 已将项目骨架搭好，本文主要向骨架中添充内容，也就是完成配置文件的配置。</p>
<p>我们首先看下 SSM 框架搭建核心步骤：</p>
<ol>
<li>在 pom.xml 中添加 Maven 依赖，主要目的是将项目中所需要用到的 jar 包引入到项目，通过 Maven 进行管理。</li>
<li>配置文件的配置，主要是 web.xml 的配置，数据库连接池的配置，日志文件的配置，SpringMVC 的配置，MyBatis 的配置等，具体配置内容下面会做详细说明。</li>
<li>添加 Web 服务器 Tomcat，因为项目启动需要载体。</li>
<li>启动 Tomcat 服务，访问 127.0.0.1:8080 或者 localhost:8080，页面成功访问，即表示 SSM 框架搭建完成。</li>
</ol>
<h3 id="maven">查看 Maven 的本地仓库</h3>
<p>在配置之前，我们需先了解下 Maven 仓库。</p>
<p>Maven 仓库是 Maven 管理 jar 包的地方，有本地仓库，远程仓库和中央仓库之分。本地仓库即存在于本机。远程仓库，可通过配置 settings.xml 获取，比如阿里云的远程仓库。中央仓库为 Maven 的仓库，不配置远程仓库，默认从中央仓库下载 jar 依赖，然而中央仓库在国外，下载起来速度会很慢，所以我们多会选择配置阿里云远程仓库。</p>
<p>如何查看 Maven 本地仓库的位置，具体步骤如下。</p>
<p>首先，打开 CMD 命令窗口，输入如下 Maven 命令，即可查看 Maven 本地仓库的位置。</p>
<pre><code>mvn help:effective-settings
</code></pre>
<p>如果没有配置 Maven 本地仓库的位置，默认位置在 <code>C:\Users\你的主机名\.m2\repository</code> 下，如图：</p>
<p><img src="http://images.gitbook.cn/562c1630-5e4e-11e8-a59f-c7ac04233ce1" alt="" /></p>
<p>如果你有自己的 Maven 仓库，可在 Maven 的解压目录 <code>apache-maven-3.3.9\conf</code> 下的 settings.xml 中配置。</p>
<pre><code>&lt;localRepository&gt;你的仓库路径&lt;/localRepository&gt;    
</code></pre>
<p>我的 Maven 仓库路径为 <code>D：/repository</code>，配置如下图所示：</p>
<p><img src="http://images.gitbook.cn/686723d0-5e4e-11e8-b864-0bd1f4b74dfb" alt="" /></p>
<p>上面提到，我们多会使用阿里云远程仓库，接下来我们看看它的配置过程。</p>
<p>首先，配置阿里云镜像。这时我们可在 settings.xml 中找到 mirrors 标签，在 mirrors 标签内配置如下内容：</p>
<pre><code>     &lt;mirror&gt;
      &lt;id&gt;alimaven&lt;/id&gt;
      &lt;name&gt;aliyun maven&lt;/name&gt;
      &lt;url&gt;http://maven.aliyun.com/nexus/content/groups/public/&lt;/url&gt;
      &lt;mirrorOf&gt;central&lt;/mirrorOf&gt;        
    &lt;/mirror&gt;
</code></pre>
<p>如下图所示：</p>
<p><img src="http://images.gitbook.cn/786d7720-5e4e-11e8-b864-0bd1f4b74dfb" alt="" /></p>
<p>配置阿里云镜像的目的是使用阿里云的远程仓库，如果不配置，则默认使用中央仓库，而中央仓库在国外，下载依赖时会很慢。</p>
<p>然后在 file -&gt; settings 中找到 Maven，在下图所示的位置添加 Maven 的路径以及 Maven 配置文件 settings.xml 的路径，仓库的位置（即在 settings.xml 中配置的仓库）将自动显示出来。</p>
<p><img src="http://images.gitbook.cn/8cae3fd0-5e4e-11e8-8a60-1bdde4cc4659" alt="" /></p>
<h3 id="mysql">选用 MySQL 数据库</h3>
<p>MySQL 是一种开放源代码的关系型数据库管理系统（RDBMS），使用最常用的数据库管理语言——结构化查询语言（SQL）进行数据库管理。</p>
<p>因为 MySQL 相比 Oracle 开源、免费，很多企业也在用，所以本课程我们选用 MySQL 数据库作为存储数据库。</p>
<p>如果还没有安装 MySQL 数据的同学请参考这篇博文：<a href="https://blog.csdn.net/Liu68686868/article/details/79518471">《MySQL 安装》</a>。</p>
<h3 id="maven-1">添加 Maven 依赖</h3>
<p>完成了以上的准备工作，接下来，我们就可以正式开始 SSM 的搭建了。首先是添加 Maven 依赖。</p>
<p>Maven 依赖有很多，这里只给出部分依赖，用来正常启动项目。每个依赖都在代码中添加了注释，这里就不赘述了。如果遇到报错，通过 Alt+Enter 组合键进行下载即可。 </p>
<p>在 dreamland-web 子工程的 pom.xml 中添加以下代码：</p>
<pre><code>        &lt;properties&gt;
        &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt;
        &lt;maven.compiler.source&gt;1.7&lt;/maven.compiler.source&gt;
        &lt;maven.compiler.target&gt;1.7&lt;/maven.compiler.target&gt;

        &lt;!-- spring版本号 --&gt;
        &lt;spring.version&gt;4.2.5.RELEASE&lt;/spring.version&gt;

        &lt;!-- mybatis版本号 --&gt;
        &lt;mybatis.version&gt;3.2.8&lt;/mybatis.version&gt;

        &lt;!-- mysql驱动版本号 --&gt;
        &lt;mysql-driver.version&gt;5.1.29&lt;/mysql-driver.version&gt;

        &lt;!-- log4j日志包版本号 --&gt;
        &lt;slf4j.version&gt;1.7.18&lt;/slf4j.version&gt;
        &lt;log4j.version&gt;1.2.17&lt;/log4j.version&gt;

        &lt;!--spring-security版本号--&gt;
        &lt;spring-security.version&gt;4.1.3.RELEASE&lt;/spring-security.version&gt;

        &lt;!--spring-data-redis版本号--&gt;
        &lt;spring.data.redis.version&gt;1.7.1.RELEASE&lt;/spring.data.redis.version&gt;
    &lt;/properties&gt;

    &lt;dependencies&gt;
        &lt;!-- 添加jstl依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;jstl&lt;/groupId&gt;
            &lt;artifactId&gt;jstl&lt;/artifactId&gt;
            &lt;version&gt;1.2&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;dependency&gt;
            &lt;groupId&gt;javax&lt;/groupId&gt;
            &lt;artifactId&gt;javaee-api&lt;/artifactId&gt;
            &lt;version&gt;7.0&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- 添加spring核心依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-core&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-web&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-oxm&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-tx&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-jdbc&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-context&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-context-support&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-aop&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-test&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- 添加mybatis依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
            &lt;version&gt;${mybatis.version}&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- 添加mybatis/spring整合包依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring&lt;/artifactId&gt;
            &lt;version&gt;1.2.2&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- 添加mysql驱动依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;${mysql-driver.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- 添加数据库连接池依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;commons-dbcp&lt;/groupId&gt;
            &lt;artifactId&gt;commons-dbcp&lt;/artifactId&gt;
            &lt;version&gt;1.2.2&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- 添加日志相关jar包 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;log4j&lt;/groupId&gt;
            &lt;artifactId&gt;log4j&lt;/artifactId&gt;
            &lt;version&gt;${log4j.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
            &lt;artifactId&gt;slf4j-api&lt;/artifactId&gt;
            &lt;version&gt;${slf4j.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
            &lt;artifactId&gt;slf4j-log4j12&lt;/artifactId&gt;
            &lt;version&gt;${slf4j.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- log end --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-jms&lt;/artifactId&gt;
            &lt;version&gt;${spring.version}&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- https://mvnrepository.com/artifact/org.apache.xbean/xbean-spring --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.apache.xbean&lt;/groupId&gt;
            &lt;artifactId&gt;xbean-spring&lt;/artifactId&gt;
            &lt;version&gt;4.0&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;!-- https://mvnrepository.com/artifact/commons-beanutils/commons-beanutils --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;commons-beanutils&lt;/groupId&gt;
            &lt;artifactId&gt;commons-beanutils&lt;/artifactId&gt;
            &lt;version&gt;1.9.3&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- 通用mapper --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;tk.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mapper&lt;/artifactId&gt;
            &lt;version&gt;3.1.2&lt;/version&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
</code></pre>
<p>pom.xml 的位置如下图所示：</p>
<p><img src="http://images.gitbook.cn/ab2922e0-5e4e-11e8-b977-f33e31f528f0" alt="" /></p>
<h3 id="">配置文件</h3>
<p>这一小节，我们将完成配置文件的配置。配置文件的加载顺序以及各配置文件有什么作用，我会在最后进行介绍。</p>
<p>各配置文件位置如下图：</p>
<p><img src="http://images.gitbook.cn/ba5765b0-5e4e-11e8-8a60-1bdde4cc4659" alt="" /></p>
<h4 id="jdbcproperties">jdbc.properties文件配置——数据库连接的配置</h4>
<p>这个配置文件主要是 spring-mybatis.xml 引用的主要参数，jdbc.properties 包括 JDBC 加载类、URL、用户名和密码.</p>
<pre><code>jdbcUrl=jdbc:mysql://localhost:3306/dream_db?useUnicode=true&amp;characterEncoding=utf-8&amp;zeroDateTimeBehavior=convertToNull
</code></pre>
<p>上面代码表示使用的是 MySQL 数据库，关于 MySQL 数据库的下载安装，这里不做介绍了，MySQL 数据库的默认端口是3306，端口号后的 <code>dream_db</code> 是你的数据库名称，后面的 <code>useUnicode=true&amp;characterEncoding=utf-8&amp;zeroDateTimeBehavior=convertToNull</code>是指定字符的编码和解码格式。</p>
<p>配置代码如下：</p>
<pre><code>    driverClasss=com.mysql.jdbc.Driver
    jdbcUrl=jdbc:mysql://localhost:3306/dream_db?useUnicode=true&amp;characterEncoding=utf-8&amp;zeroDateTimeBehavior=convertToNull
    username=root
    password=root

    #定义初始连接数
    initialSize=0
    #定义最大连接数
    maxActive=20
    #定义最大空闲
    maxIdle=20
    #定义最小空闲
    minIdle=1
    #定义最长等待时间
    maxWait=60000
</code></pre>
<p>注意 dream_db 是数据库名称，username 和 password 分别是数据库用户名和密码。</p>
<h4 id="log4jpropertieslog">log4j.properties文件配置——log日志的配置</h4>
<p>log4j.properties 为 log4j 日志配置文件，主要将程序中打印的日志信息输出到控制台、保存到目录文件，可以通过配置设置日志文件的输出级别、格式、输出路径等。</p>
<p>配置代码如下：</p>
<pre><code>    log4j.rootLogger=DEBUG,Console,File

    #日志输出到控制台
    og4j.appender.Console=org.apache.log4j.ConsoleAppender
    #指定输出到控制台
    log4j.appender.Console.Target=System.out
    #灵活地指定布局模式
    log4j.appender.Console.layout=org.apache.log4j.PatternLayout
    #日志输出格式设置
    log4j.appender.Console.layout.ConversionPattern=[%p][%t][%d{yyyy-MM-dd HH\:mm\:ss}][%C] - %m%n

    #日志输出到文件
    log4j.appender.File=org.apache.log4j.RollingFileAppender
    #日志存放位置
    log4j.appender.File.File=D/wly/git/dreamland/logs/run.log
    #单个日志文件大小设置
    log4j.appender.File.MaxFileSize=10MB
    #输出日志，如果换成DEBUG表示输出DEBUG以上级别日志
    log4j.appender.File.Threshold=ALL
    log4j.appender.File.layout=org.apache.log4j.PatternLayout
    log4j.appender.File.layout.ConversionPattern=[%p][%t][%d{yyyy-MM-dd HH\:mm\:ss}][%C] - %m%n
</code></pre>
<pre><code>
</code></pre>
<p>下面我们解释下以上代码中需要注意的地方。</p>
<p>（1）日志输出级别分为以下四种，优先级别为：</p>
<blockquote>
  <p>ERROR &gt; WARN &gt; INFO &gt; DEBUG</p>
</blockquote>
<p>输出原则为：程序会打印出高于或等于所设置级别的日志，设置的日志等级越高，打印出来的日志就越少，即：</p>
<blockquote>
  <p>设置级别为 ERROR 只会打印出 ERROR 日志；</p>
  <p>设置级别为 WARN 会打印出 ERROR 和 WRAN 日志；</p>
  <p>设置级别为 INFO 会打印出 ERROR、WARN 和 INFO 日志；</p>
  <p>设置为 DEBUG 会打印出所有日志。</p>
</blockquote>
<p>本案例中 <code>log4j.rootLogger=DEBUG,Console,File</code>表示输出 DEBUG 以上级别日志。</p>
<p>（2）上面代码中出现的 <code>%m</code>、<code>%p</code>、<code>%d</code>、<code>%c</code>、<code>%n</code>……分别代表的含义如下所示：</p>
<pre><code>    %m 输出代码中指定的消息 
    %p 输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL 
    %r 输出自应用启动到输出该log信息耗费的毫秒数 
    %c 输出所属的类目，通常就是所在类的全名 
    %t 输出产生该日志事件的线程名 
    %n 输出一个回车换行符，Windows平台为“rn”，Unix平台为“n” 
    %d 输出日志时间点的日期或时间，默认格式为ISO8601，也可以在其后指定格式，比如：%d{yyyy MMM dd HH:mm:ss,SSS}，输出类似：2002年10月18日 ：10：28，921
    %l 输出日志事件的发生位置，包括类目名、发生的线程，以及在代码中的行数。
    %x Used to output the NDC (nested diagnostic context) associated with the thread that generated the logging event
    %X Used to output the MDC (mapped diagnostic context) associated with the thread that generated the logging event for specified key
</code></pre>
<p>（3）如下代码用来设定当文件到达设定大小时产生一个新的文件。</p>
<pre><code>log4j.appender.File=org.apache.log4j.RollingFileAppender
</code></pre>
<p>将 RollingFileAppender 换成 DailyRollingFileAppender，则表示每天产生一个日志文件。</p>
<p>（4）可以在下面的代码中设置你的日志文件的存放位置。</p>
<pre><code>    log4j.appender.File.File=D/wly/git/dreamland/logs/run.log
</code></pre>
<h4 id="springmvcxml">spring-mvc.xml 的配置</h4>
<p>srping-mvc.xml 为 SpringMVC 核心配置文件，主要包括 Controller 层的包扫描、视图模式配置（跳转路径的前后缀）、文件上传配置、静态资源处理等。</p>
<p>配置代码如下，关键地方均有注释说明：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                        http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
                        http://www.springframework.org/schema/context
                        http://www.springframework.org/schema/context/spring-context-4.0.xsd
                        http://www.springframework.org/schema/mvc
                        http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd"&gt;

    &lt;mvc:default-servlet-handler /&gt;
    &lt;!-- 自动扫描 --&gt;
    &lt;context:component-scan base-package="wang.dreamland.www.controller"/&gt;

    &lt;!--避免IE执行AJAX时，返回JSON出现下载文件 --&gt;
    &lt;bean id="mappingJacksonHttpMessageConverter"
          class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter"&gt;
        &lt;property name="supportedMediaTypes"&gt;
            &lt;list&gt;
                &lt;value&gt;text/html;charset=UTF-8&lt;/value&gt;
            &lt;/list&gt;
        &lt;/property&gt;
    &lt;/bean&gt;

    &lt;!-- 默认的注解映射的支持，自动注册DefaultAnnotationHandlerMapping和AnnotationMethodHandlerAdapter --&gt;
    &lt;mvc:annotation-driven /&gt;

    &lt;!-- 定义跳转的文件的前后缀 ，视图模式配置 --&gt;
    &lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
        &lt;property name="prefix" value="/WEB-INF/" /&gt;
        &lt;property name="suffix" value=".jsp"/&gt;
    &lt;/bean&gt;

    &lt;!-- 文件上传配置 --&gt;
    &lt;bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver"&gt;
        &lt;!-- 默认编码 --&gt;
        &lt;property name="defaultEncoding" value="UTF-8"/&gt;
        &lt;!-- 上传文件大小限制为31M，31*1024*1024 --&gt;
        &lt;property name="maxUploadSize" value="32505856"/&gt;
        &lt;!-- 内存中的最大值 --&gt;
        &lt;property name="maxInMemorySize" value="4096"/&gt;
    &lt;/bean&gt;

    &lt;!-- 对静态资源文件的访问--&gt;
    &lt;mvc:resources mapping="/images/**" location="/images/" cache-period="31556926"/&gt;
    &lt;mvc:resources mapping="/js/**" location="/js/" cache-period="31556926"/&gt;
    &lt;mvc:resources mapping="/css/**" location="/css/" cache-period="31556926"/&gt;

    &lt;/beans&gt;
</code></pre>
<p>配置后会看到有报红，我们创建相对应的包路径和文件夹，注意 css、js、images 在 webapp 路径下。</p>
<p>在 java 目录右键 new -&gt; Package -&gt; wang.dreamland.www.controller。</p>
<p>然后在 webapp 下右键 new -&gt; Directory 分别创建 css、js 和 images 文件夹，如下图：</p>
<p><img src="http://images.gitbook.cn/d436c7a0-5e4e-11e8-a59f-c7ac04233ce1" alt="" /></p>
<h4 id="springmybatisxml">spring-mybatis.xml 配置</h4>
<p>spring-mybatis.xml 为 Spring 和 Mybatis 整合配置文件，主要进行扫描包的配置、数据源的配置、映射文件的配置、事务管理配置等，配置文件中都有注释，这里不再赘述。</p>
<p>配置代码如下：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context" xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                        http://www.springframework.org/schema/beans/spring-beans-3.1.xsd
                        http://www.springframework.org/schema/context
                        http://www.springframework.org/schema/context/spring-context-3.1.xsd
                        http://www.springframework.org/schema/tx
                        http://www.springframework.org/schema/tx/spring-tx.xsd"&gt;

    &lt;!-- 自动扫描 --&gt;
    &lt;context:component-scan base-package="wang.dreamland.www"/&gt;

     &lt;!--第二种方式：加载多个properties文件--&gt;
    &lt;bean id="configProperties" class="org.springframework.beans.factory.config.PropertiesFactoryBean"&gt;
        &lt;property name="locations"&gt;
            &lt;list&gt;
                &lt;value&gt;classpath:jdbc.properties&lt;/value&gt;
            &lt;/list&gt;
        &lt;/property&gt;
        &lt;property name="fileEncoding" value="UTF-8"/&gt;
    &lt;/bean&gt;
    &lt;bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PreferencesPlaceholderConfigurer"&gt;
        &lt;property name="properties" ref="configProperties"/&gt;
    &lt;/bean&gt;

    &lt;!-- 配置数据源 --&gt;
    &lt;bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource"
          destroy-method="close"&gt;
        &lt;property name="driverClassName" value="${driverClasss}"/&gt;
        &lt;property name="url" value="${jdbcUrl}"/&gt;
        &lt;property name="username" value="${username}"/&gt;
        &lt;property name="password" value="${password}"/&gt;
        &lt;!-- 初始化连接大小 --&gt;
        &lt;property name="initialSize" value="${initialSize}"&gt;&lt;/property&gt;
        &lt;!-- 连接池最大数量 --&gt;
        &lt;property name="maxActive" value="${maxActive}"&gt;&lt;/property&gt;
        &lt;!-- 连接池最大空闲 --&gt;
        &lt;property name="maxIdle" value="${maxIdle}"&gt;&lt;/property&gt;
        &lt;!-- 连接池最小空闲 --&gt;
        &lt;property name="minIdle" value="${minIdle}"&gt;&lt;/property&gt;
        &lt;!-- 获取连接最大等待时间 --&gt;
        &lt;property name="maxWait" value="${maxWait}"&gt;&lt;/property&gt;
    &lt;/bean&gt;

    &lt;!-- mybatis和spring完美整合，不需要mybatis的配置映射文件 --&gt;
    &lt;bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
        &lt;!-- 配置Mybati的核心配置文件 --&gt;
        &lt;property name="configLocation" value="classpath:mybatis-config.xml" /&gt;

        &lt;!-- 自动扫描mapping.xml文件 --&gt;
     &lt;!--   &lt;property name="mapperLocations" value="classpath:mapping/*.xml"&gt;&lt;/property&gt;--&gt;
    &lt;/bean&gt;

    &lt;!--  DAO接口所在包名，Spring会自动查找其下的类 --&gt;
    &lt;bean class="org.mybatis.spring.mapper.MapperScannerConfigurer"&gt;
        &lt;property name="basePackage" value="wang.dreamland.www.dao"/&gt;
        &lt;property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"&gt;&lt;/property&gt;
    &lt;/bean&gt;


    &lt;!-- 事务管理--&gt;
    &lt;bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
    &lt;/bean&gt;

    &lt;tx:annotation-driven transaction-manager="transactionManager"/&gt;
    &lt;/beans&gt;
</code></pre>
<p>注意 dao 接口扫描包路径是 wang.dreamland.www.dao，之后配置
 dao 时记得别配错路径了，否则会报错。</p>
<pre><code>     &lt;property name="basePackage" value="wang.dreamland.www.dao"/&gt;
</code></pre>
<h4 id="mybatisconfigxml">mybatis-config.xml 配置</h4>
<p>mybatis-config.xml 是 MyBatis 的核心配置文件，包括驼峰命名、别名、通用 mapper、分页插件配置等。</p>
<p>配置代码如下，关键地方均有注释说明：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
    &lt;!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd"&gt;

    &lt;configuration&gt;
    &lt;!-- 开启驼峰匹配 --&gt;
    &lt;settings&gt;
        &lt;setting name="mapUnderscoreToCamelCase" value="true"/&gt;
    &lt;/settings&gt;
    &lt;!-- 别名 --&gt;
    &lt;typeAliases&gt;
        &lt;!--默认别名为：javabean 的首字母小写的非限定类名来作为它的别名--&gt;
        &lt;package name="wang.dreamland.www.entity" /&gt;
    &lt;/typeAliases&gt;
    &lt;plugins&gt;
        &lt;plugin interceptor="tk.mybatis.mapper.mapperhelper.MapperInterceptor"&gt;
            &lt;!--主键自增回写方法,默认值MYSQL,详细说明请看文档HSQLDB--&gt;
            &lt;property name="IDENTITY" value="MYSQL"/&gt;

            &lt;!--可选参数一共3个，对应0,1,2,分别为SequenceName，ColumnName,PropertyName--&gt;
            &lt;property name="seqFormat" value="{0}.nextval"/&gt;

            &lt;!--通用Mapper接口，多个通用接口用逗号隔开--&gt;
            &lt;property name="mappers" value="tk.mybatis.mapper.common.Mapper"/&gt;
        &lt;/plugin&gt;
            &lt;!-- 自定义分页插件 --&gt;
         &lt;!--   &lt;plugin interceptor="wang.dreamland.www.common.PageHelper"&gt;&lt;/plugin&gt;--&gt;

    &lt;/plugins&gt;
    &lt;/configuration&gt;
</code></pre>
<p>上面代码中，wang.dreamland.www.entity 对应的是实体类包路径，之后新建实体时就放在该路径下：</p>
<pre><code>     &lt;package name="wang.dreamland.www.entity" /&gt;
</code></pre>
<h4 id="webxml">web.xml 配置</h4>
<p>web.xml 为 Web 容器的配置文件，用来初始化配置信息，主要定义了：</p>
<ol>
<li>Web 应用的名字、描述（display-name 和 description 标签）; </li>
<li>应用范围的初始化参数（context-param 标签）；</li>
<li>过滤器配置（filter 标签）；</li>
<li>监听器配置(listener 标签)；</li>
<li>servlet 配置（servlet 标签，如前端控制器和验证码）；</li>
<li>欢迎页面（welcome-file-list 标签，如 index.jsp 页面）；</li>
<li>session失效时间（session-config 标签）；</li>
<li>错误页面配置（error-page 标签，如 404、500错误页面等）。</li>
</ol>
<p>配置代码如下所示：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;web-app xmlns="http://java.sun.com/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
          http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
         version="3.0"&gt;

    &lt;display-name&gt;dreamland-web&lt;/display-name&gt;

    &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;
      classpath*:spring-mybatis.xml
    &lt;/param-value&gt;
    &lt;/context-param&gt;

      &lt;context-param&gt;
    &lt;param-name&gt;log4jConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;classpath:log4j.properties&lt;/param-value&gt;
      &lt;/context-param&gt;

    &lt;!-- 编码过滤器 解决POST乱码问题--&gt;
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

      &lt;!-- spring监听器 --&gt;
      &lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.context.ContextLoaderListener&lt;/listener-class&gt;
      &lt;/listener&gt;

      &lt;!-- 防止spring内存溢出监听器，比如quartz --&gt;
      &lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.util.IntrospectorCleanupListener&lt;/listener-class&gt;
      &lt;/listener&gt;

      &lt;!-- spring mvc servlet--&gt;
      &lt;servlet&gt;
    &lt;servlet-name&gt;SpringMVC&lt;/servlet-name&gt;
    &lt;servlet-class&gt;org.springframework.web.servlet.DispatcherServlet&lt;/servlet-class&gt;
    &lt;init-param&gt;
      &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
      &lt;param-value&gt;classpath:spring-mvc.xml&lt;/param-value&gt;
    &lt;/init-param&gt;
    &lt;load-on-startup&gt;1&lt;/load-on-startup&gt;
    &lt;async-supported&gt;true&lt;/async-supported&gt;
      &lt;/servlet&gt;
      &lt;!-- servlet-mapping --&gt;
      &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;SpringMVC&lt;/servlet-name&gt;
    &lt;!-- 此处也可以配置成 *.do 形式 --&gt;
    &lt;url-pattern&gt;/&lt;/url-pattern&gt;
      &lt;/servlet-mapping&gt;

      &lt;!-- 指明对于如下资源文件不采用spring的过滤器 --&gt;
      &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;default&lt;/servlet-name&gt;
    &lt;url-pattern&gt;*.xml&lt;/url-pattern&gt;
      &lt;/servlet-mapping&gt;
      &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;default&lt;/servlet-name&gt;
    &lt;url-pattern&gt;*.css&lt;/url-pattern&gt;
      &lt;/servlet-mapping&gt;

      &lt;welcome-file-list&gt;
    &lt;welcome-file&gt;index.jsp&lt;/welcome-file&gt;
      &lt;/welcome-file-list&gt;

      &lt;!-- session配置 --&gt;
      &lt;session-config&gt;
    &lt;session-timeout&gt;15&lt;/session-timeout&gt;
      &lt;/session-config&gt;
    &lt;/web-app&gt;
</code></pre>
<p>配置完成后的整体目录结构如下：</p>
<p><img src="http://images.gitbook.cn/eca868c0-5e4e-11e8-b864-0bd1f4b74dfb" alt="" /></p>
<h3 id="tomcat">添加 Tomcat 服务并启动</h3>
<h4 id="tomcatserver">添加 Tomcat Server</h4>
<p>点击右上角的倒三角 -&gt; Edit Configurations，如下图所示：</p>
<p><img src="http://images.gitbook.cn/fb6a5530-5e4e-11e8-b977-f33e31f528f0" alt="" /></p>
<p>接下来的设置请参考下面图示说明：</p>
<p><img src="http://images.gitbook.cn/12053a80-5e4f-11e8-b977-f33e31f528f0" alt="" /></p>
<p><img src="http://images.gitbook.cn/22026610-5e4f-11e8-a59f-c7ac04233ce1" alt="" /></p>
<p><img src="http://images.gitbook.cn/301bb670-5e4f-11e8-b977-f33e31f528f0" alt="" /></p>
<p><img src="http://images.gitbook.cn/3e0480f0-5e4f-11e8-b977-f33e31f528f0" alt="" /></p>
<h4 id="tomcat-1">启动 Tomcat</h4>
<p>启动项目后，访问 127.0.0.1:8080 或者 localhost:8080，可以看到页面上出现了熟悉的 “Hello World!”，表示 SSM 框架搭建完成！</p>
<p><img src="http://images.gitbook.cn/4b3c7200-5e4f-11e8-b977-f33e31f528f0" alt="" /></p>
<h3 id="-1">配置文件加载顺序</h3>
<h4 id="web">Web 容器加载配置文件顺序</h4>
<p>上面，我们把配置文件配置好了，那怎样才能起作用呢？这就需要 Web 容器来加载了。Web 容器加载配置文件的过程如下。</p>
<p>启动 Tomcat 后，Web 容器首先加载 web.xml 文件。</p>
<p>web.xml 文件是创建 Web 项目所需要的配置文件，用来初始化配置信息，主要包含拦截器、过滤器、servlet 等的配置，它的位置在项目 WEB-INF 目录下。</p>
<p>在 web.xml 的 <code>&lt;context-param&gt;</code>中加载其他 XML 和 log4j.properties 文件，代码如下：</p>
<pre><code>     &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;
      classpath*:spring-mybatis.xml,
      classpath*:applicationContext-redis.xml,
      classpath*:applicationContext-activemq.xml,
    &lt;/param-value&gt;
      &lt;/context-param&gt;

     &lt;context-param&gt;
    &lt;param-name&gt;log4jConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;classpath:log4j.properties&lt;/param-value&gt;
      &lt;/context-param&gt;
</code></pre>
<p>其中 param-name 的名称是固定格式，param-value 是要加载的配置文件名，多个用逗号隔开，通过 Ctrl+鼠标左键可定位到相应配置文件。</p>
<p>接着，根据 spring-mybatis.xml 中的 PropertiesFactoryBean 加载多个 properties 文件，代码如下：</p>
<pre><code>       &lt;bean id="configProperties" class="org.springframework.beans.factory.config.PropertiesFactoryBean"&gt;
        &lt;property name="locations"&gt;
            &lt;list&gt;
                &lt;value&gt;classpath:jdbc.properties&lt;/value&gt;
                &lt;value&gt;classpath:redis.properties&lt;/value&gt;              
            &lt;/list&gt;
        &lt;/property&gt;
        &lt;property name="fileEncoding" value="UTF-8"/&gt;
    &lt;/bean&gt;
    &lt;bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PreferencesPlaceholderConfigurer"&gt;
        &lt;property name="properties" ref="configProperties"/&gt;
    &lt;/bean&gt;
</code></pre>
<p>通过 property 标签内的 list 标签可以加载多个 properties 文件，value 标签内就是具体的 properties 文件的路径，通过 Ctrl+鼠标左键可以定位到相应的文件。</p>
<p>根据 spring-mybatis.xml 的 SqlSessionFactoryBean 加载 mybatis 核心配置文件 mybatis-config.xml 以及其他映射文件</p>
<pre><code>    &lt;bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
        &lt;!-- 配置Mybatis的核心配置文件 --&gt;
        &lt;property name="configLocation" value="classpath:mybatis-config.xml" /&gt;
        &lt;!-- 自动扫描mapping.xml文件 --&gt;
        &lt;property name="mapperLocations" value="classpath:mapping/*.xml"&gt;&lt;/property&gt;
    &lt;/bean&gt;
</code></pre>
<p>其中 property 标签的 name 值是固定的，通过该属性加载对应的 value 中的值，value 的值是配置文件的路径，通过 Ctrl+鼠标左键可访问该文件。</p>
<p>然后，加载前端控制器 DispatcherServlet 的配置文件 srping-mvc.xml。</p>
<pre><code>      &lt;!-- spring mvc servlet--&gt;
      &lt;servlet&gt;
    &lt;servlet-name&gt;SpringMVC&lt;/servlet-name&gt;
    &lt;servlet-class&gt;org.springframework.web.servlet.DispatcherServlet&lt;/servlet-class&gt;
    &lt;init-param&gt;
      &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
      &lt;param-value&gt;classpath:spring-mvc.xml&lt;/param-value&gt;
    &lt;/init-param&gt;
    &lt;load-on-startup&gt;1&lt;/load-on-startup&gt;
    &lt;async-supported&gt;true&lt;/async-supported&gt;
      &lt;/servlet&gt;
      &lt;!-- servlet-mapping --&gt;
      &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;SpringMVC&lt;/servlet-name&gt;
    &lt;!-- 此处也可以配置成 *.do 形式 --&gt;
    &lt;url-pattern&gt;/&lt;/url-pattern&gt;
      &lt;/servlet-mapping&gt;
</code></pre>
<p>其中 init-param 标签是前端控制器的初始化参数配置，param-name 参数名为固定值，param-value 参数值为具体的配置文件路径，以此来加载对应的配置文件。</p>
<p><code>&lt;load-on-startup&gt;1&lt;/load-on-startup&gt;</code>的正数值越小，启动该 Servlet 的优先级越高。</p>
<p>这样所有的配置文件就加载完毕了！</p></div></article>