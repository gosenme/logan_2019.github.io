---
title: Spring Cloud 快速入门-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>接着上一篇，我们继续来搭建基础框架，本文我们将搭建客户端基础模块，集成熔断器，集成持久层框架 MyBatis。</p>
<p>在上一篇我们已经构建好了配置中心，因此，此后搭建的所有工程都是将配置文件放到 Git 上（点击<a href="https://github.com/springcloudlynn/springcloudinactivity">这里</a>获取本课程配置文件的 Git 仓库地址），通过配置中心将配置文件从 Git 仓库上拉取下来。</p>
<h3 id="">客户端基础模块</h3>
<p>为了便于应用的可读性，我们在顶级工程下，先创建一个 packaging 为 pom 的工程，命名为 client，然后在 client 下创建我们的客户端模块，如图所示：</p>
<p><img src="http://images.gitbook.cn/453d6330-754e-11e8-a3f9-f1e4d8a7adbe" alt="enter image description here" /></p>
<p>client 的 pom 内容如下：</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"&gt;
    &lt;parent&gt;
        &lt;artifactId&gt;news&lt;/artifactId&gt;
        &lt;groupId&gt;com.lynn&lt;/groupId&gt;
        &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
    &lt;/parent&gt;
    &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;

    &lt;artifactId&gt;client&lt;/artifactId&gt;
    &lt;description&gt;客户端&lt;/description&gt;
    &lt;modules&gt;
        &lt;module&gt;index&lt;/module&gt;
        &lt;module&gt;article&lt;/module&gt;
        &lt;module&gt;comment&lt;/module&gt;
        &lt;module&gt;user&lt;/module&gt;
    &lt;/modules&gt;
    &lt;packaging&gt;pom&lt;/packaging&gt;
    &lt;properties&gt;
        &lt;mybatis.version&gt;1.1.1&lt;/mybatis.version&gt;
        &lt;mysql.version&gt;5.1.40&lt;/mysql.version&gt;
        &lt;druid.version&gt;1.1.10&lt;/druid.version&gt;
    &lt;/properties&gt;
    &lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-openfeign&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-hystrix-dashboard&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-actuator&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;${mybatis.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;${mysql.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
            &lt;artifactId&gt;druid-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;${druid.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.lynn&lt;/groupId&gt;
            &lt;artifactId&gt;common&lt;/artifactId&gt;
            &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix-dashboard&lt;/artifactId&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
&lt;/project&gt;
</code></pre>
<p>接着继续创建客户端工程：index（首页）、article（文章）、comment（评论）、user（用户）。</p>
<p>在每个客户端模块创建启动类，添加以下内容：</p>
<pre><code class="java language-java">@SpringCloudApplication
@ComponentScan(basePackages = "com.lynn")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>最后在每个客户端工程下创建 bootstrap.yml 配置文件，在 Git 仓库创建每个客户端模块自己的配置项，并添加相应的内容。接下来，我们具体看下每个客户端下需要添加的代码内容。</p>
<ul>
<li>首页</li>
</ul>
<p>首页客户端下 bootstrap.yml 配置文件的代码如下：</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: index
      label: master
      discovery:
        enabled: true
        serviceId: config
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
</code></pre>
<p>首页配置项 index.yml 中添加如下代码：</p>
<pre><code class="yaml language-yaml">server:
  port: 8081
spring:
  application:
    name: index
  profiles:
    active: dev
</code></pre>
<ul>
<li>文章</li>
</ul>
<p>文章客户端下 bootstrap.yml 配置文件的代码如下：</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: article
      label: master
      discovery:
        enabled: true
        serviceId: config
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
</code></pre>
<p>文章配置项 article.yml 中添加如下代码：</p>
<pre><code class="yaml language-yaml">server:
  port: 8082
spring:
  application:
    name: article
  profiles:
    active: dev
</code></pre>
<ul>
<li>评论</li>
</ul>
<p>评论客户端下 bootstrap.yml 配置文件的代码如下：</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: comment
      label: master
      discovery:
        enabled: true
        serviceId: config
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
</code></pre>
<p>评论配置项 comment.yml 中添加如下代码：</p>
<pre><code class="yaml language-yaml">server:
  port: 8083
spring:
  application:
    name: comment
  profiles:
    active: dev
</code></pre>
<ul>
<li>用户</li>
</ul>
<p>用户客户端下 bootstrap.yml 配置文件的代码如下：</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: user
      label: master
      discovery:
        enabled: true
        serviceId: config
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
</code></pre>
<p>用户配置项 user.yml 中添加如下代码：</p>
<pre><code class="yaml language-yaml">server:
  port: 8084
spring:
  application:
    name: user
  profiles:
    active: dev
</code></pre>
<h3 id="-1">熔断器</h3>
<p>熔断机制可以有效提升应用的健壮性，通过 Hystrix Dashboard 也可以监控 Feign 调用，便于我们随时观察服务的稳定性，因此集成熔断器是很有必要的，本实例将集成 Feign 和 Hystrix 框架。</p>
<p>首先，在 client 的 pom 中加入依赖（因为所有客户端都需要依赖它，所以在 client 中依赖即可），代码如下：</p>
<pre><code class="xml language-xml"> &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-openfeign&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-hystrix-dashboard&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-actuator&lt;/artifactId&gt;
        &lt;/dependency&gt;
</code></pre>
<p>在每个 client 的 Application 都加入一下注解：</p>
<pre><code>@EnableHystrixDashboard
@EnableFeignClients
</code></pre>
<p>并加入一下代码：</p>
<pre><code>@Bean
    public ServletRegistrationBean getServlet(){
        HystrixMetricsStreamServlet streamServlet = new HystrixMetricsStreamServlet();
        ServletRegistrationBean registrationBean = new ServletRegistrationBean(streamServlet );
        registrationBean.setLoadOnStartup(1);
        registrationBean.addUrlMappings("/hystrix.stream");
        registrationBean.setName("HystrixMetricsStreamServlet");
        return registrationBean;
    }
</code></pre>
<p>我们随便启动一个客户端来看看效果。</p>
<p>依次启动 register、config 和 index，访问地址：http://localhost:8081/hystrix，即可看到如下图所示界面：</p>
<p><img src="http://images.gitbook.cn/8adc3c10-7551-11e8-a3f9-f1e4d8a7adbe" alt="enter image description here" /></p>
<p>说明我们成功集成了 Hystrix Dashboard。</p>
<h3 id="mybatis">持久层框架 MyBatis</h3>
<p>一个 Web 应用免不了数据库的操作，因此我们继续来集成数据库框架，本应用采取 MyBatis 框架，连接池使用阿里巴巴的 Druid 框架。</p>
<p>首先在 client 下加入依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;1.1.1&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;5.1.40&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
            &lt;artifactId&gt;druid-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;1.1.10&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre>
<p>然后在 Git 仓库创建配置文件 database.yml：</p>
<pre><code class="yaml language-yaml">spring:
  datasource:
    druid:
      url: jdbc:mysql://localhost:3306/blog_db?useUnicode=true&amp;characterEncoding=UTF-8&amp;useSSL=false
      username: root
      password: 1qaz2wsx
      stat-view-servlet:
        login-username: admin
        login-password: admin
</code></pre>
<p>依次启动 register、config 和 index，然后访问：http://localhost:8081/druid，输入配置文件设置的用户名和密码，即可进入如下界面：</p>
<p><img src="http://images.gitbook.cn/b54a8570-7555-11e8-9016-addc5ac06bc8" alt="enter image description here" /></p></div></article>