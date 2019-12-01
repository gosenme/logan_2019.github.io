---
title: 案例上手 Spring 全家桶-60
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>前面的课程我们学习了本地 Config Server 的搭建方式，本节课我们一起学习远程 Config Server 的环境搭建，即将各个微服务的配置文件放置在远程 Git 仓库中，通过 Config Server 进行统一管理，本课程中我们使用基于 Git 的第三方代码托管远程仓库 GitHub 作为远程仓库，实际开发中也可以使用 Gitee、SVN 或者自己搭建的私服作为远程仓库，Config Server 结构如下图所示。</p>
<p><img src="https://images.gitbook.cn/0e7b26e0-d79d-11e9-8797-4924c0d7c082" alt="17" /></p>
<p>接下来我们就来一起搭建远程 Config Server。</p>
<h3 id="github">GitHub 远程配置文件</h3>
<p>首先将配置文件上传到 GitHub 仓库。</p>
<p>1. 在父工程下创建文件夹 config，config 中创建 configclient.yml。</p>
<p><img src="https://images.gitbook.cn/246fd8c0-d7ab-11e9-8797-4924c0d7c082" width = "70%" /></p>
<p>2. configclient.yml 中配置客户端相关信息。</p>
<pre><code class="yaml language-yaml">eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
server:
  port: 8070
spring:
  application:
    name: configclient
management:
  security:
    enabled: false
</code></pre>
<p>3. 将 config 上传至 GitHub，作为远程配置文件。</p>
<p><img src="https://images.gitbook.cn/2d82ff50-d7ab-11e9-a536-c512dee3d564" alt="2" /></p>
<h3 id="configserver">创建 Config Server</h3>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/356a5010-d7ab-11e9-a536-c512dee3d564" width = "70%" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/3e28ee00-d7ab-11e9-ad2d-e1c058c00235" width = "70%" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/4690b960-d7ab-11e9-ad2d-e1c058c00235" width = "70%" /></p>
<p>4. 在 pom.xml 中添加 Spring Cloud Config 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-config-server&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加 Config Server 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8888
spring:
  application:
    name: configserver
  cloud:
    config:
      server:
        git:
          uri: https://github.com/southwind9801/myspringclouddemo.git
          searchPaths: config
          username: root
          password: root
      label: master
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Config Server 服务端口。</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>cloud.config.server.git：Git 仓库配置文件信息。</li>
<li>uri：Git Repository 地址。</li>
<li>searchPaths：配置文件路径。</li>
<li>username：访问 Git Repository 的用户名。</li>
<li>password：访问 Git Repository 的密码。</li>
<li>cloud.config.server：Git Repository 的分支。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
</ul>
<p>6. 在 java 路径下创建启动类 ConfigServerApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
<li>@EnableConfigServer：声明配置中心。</li>
</ul>
<p>远程 Config Server 环境搭建完成，接下来创建 Config Client，读取远程配置中心的配置信息。</p>
<h3 id="configclient">创建 Config Client</h3>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/8059f7b0-d7ab-11e9-8fae-816b29059b0c" width = "65%" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/8db37a80-d7ab-11e9-8fae-816b29059b0c" width = "65%" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/949d0a50-d7ab-11e9-8797-4924c0d7c082" width = "65%" /></p>
<p>4. 在 pom.xml 中添加 Eureka Client、Spring Cloud Config 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;

    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下新建 bootstrap.yml，配置读取远程配置中心的相关信息。</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: configclient
      label: master
      discovery:
        enabled: true
        serviceId: configserver
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>属性说明：</p>
<ul>
<li>spring.cloud.config.name：当前服务注册在 Eureka Server 上的名称，与远程 Git 仓库的配置文件名对应。</li>
<li>spring.cloud.config.label：Git Repository 的分支。</li>
<li>spring.cloud.config.discovery.enabled：是否开启 Config 服务发现支持。</li>
<li>spring.cloud.config.discovery.serviceId：配置中心的名称。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
</ul>
<p>6. 在 java 路径下创建启动类 ConfigClientApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
public class ConfigClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigClientApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
</ul>
<p>7. 创建 HelloHandler，定义相关业务方法。</p>
<pre><code class="java language-java">@RequestMapping("/config")
@RestController
public class HelloHandler {

    @Value("${server.port}")
    private int port;

    @RequestMapping(value = "/index")
    public String index(){
        return "当前端口："+this.port;
    }
}
</code></pre>
<p>8. 依次启动注册中心、configserver、configclient，如下图所示。</p>
<p><img src="https://images.gitbook.cn/b687e6d0-d7ab-11e9-a536-c512dee3d564" alt="8" /></p>
<p><img src="https://images.gitbook.cn/c0826020-d7ab-11e9-a536-c512dee3d564" alt="9" /></p>
<p>通过控制台输出信息可以看到，configclient 已经读取到了 Git 仓库中的配置信息。</p>
<p>9. 通过 Postman 工具访问 http://localhost:8070/config/index，如下图所示。</p>
<p><img src="https://images.gitbook.cn/c9cf8270-d7ab-11e9-ad2d-e1c058c00235" alt="10" /></p>
<h3 id="-1">动态更新</h3>
<p>如果此时对远程配置中心的配置文件进行修改，微服务需要重启以读取最新的配置信息，实际运行环境中这种频繁重启服务的方式是需要避免的，我们可以通过动态更新的方式，实现在不重启服务的前提下自动更新配置信息的功能。</p>
<p>动态更新的实现需要借助于 Spring Cloud Bus 来完成，Spring Cloud Bus 是一个轻量级的分布式通信组件，它的原理是将各个微服务组件与消息代理进行连接，当配置文件发生改变时，会自动通知相关微服务组件，从而实现动态更新，具体实现如下。</p>
<p>1. 修改 Config Server 的 application.yml，添加 RabbitMQ。</p>
<pre><code class="yaml language-yaml">server:
  port: 8888
spring:
  application:
    name: configserver
  cloud:
    bus:
      trace:
        enable: true
    config:
      server:
        git:
          uri: https://github.com/southwind9801/myspringclouddemo.git
          searchPaths: config
          username: root
          password: root
      label: master
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
management:
  endpoints:
    web:
      exposure:
        include: bus-refresh
</code></pre>
<p>2. 修改 Config Client 的 pom.xml，添加 actuator、bus-amqp 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;

    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
    &lt;/dependency&gt;

    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-actuator&lt;/artifactId&gt;
    &lt;/dependency&gt;

    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-bus-amqp&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>3. 修改 Config Client 的 bootstrap.yml，添加 bus-refresh。</p>
<pre><code class="yaml language-yaml">spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
  cloud:
    config:
      name: configclient
      label: master
      discovery:
        enabled: true
        serviceId: configserver
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
management:
  endpoints:
    web:
      exposure:
        include: bus-refresh
</code></pre>
<p>4. 修改 HelloHandler，添加 @RefreshScope 注解。</p>
<pre><code class="java language-java">@RequestMapping("/config")
@RestController
@RefreshScope
public class HelloHandler {

    @Value("${server.port}")
    private int port;

    @RequestMapping(value = "/index")
    public String index(){
        return "当前端口："+this.port;
    }
}
</code></pre>
<p>5. 修改 config 中的配置文件，将端口改为 8080，并更新到 GitHub。</p>
<p><img src="https://images.gitbook.cn/e1f4d850-d7ab-11e9-ad2d-e1c058c00235" alt="11" /></p>
<p>6. 在不重启服务的前提下，实现配置文件的动态更新，启动 RabbitMQ，成功后如下图所示。</p>
<p><img src="https://images.gitbook.cn/e91b7120-d7ab-11e9-8797-4924c0d7c082" width = "65%" /></p>
<p>7. 发送 POST 请求，访问 http://localhost:8070/actuator/bus-refresh，如下图所示。</p>
<p><img src="https://images.gitbook.cn/f275b2d0-d7ab-11e9-a536-c512dee3d564" alt="13" /></p>
<p>8. 这样就实现动态更新了，再来访问 http://localhost:8070/config/index，如下图所示。</p>
<p><img src="https://images.gitbook.cn/fa817b80-d7ab-11e9-8797-4924c0d7c082" alt="14" /></p>
<p>可以看到端口已经更新为 8080。</p>
<p>9. 设置 GitHub 自动推送更新，添加 Webhooks，如下图所示。</p>
<p><img src="https://images.gitbook.cn/015c8c60-d7ac-11e9-8fae-816b29059b0c" alt="15" /></p>
<p>10. 在 Payload URL 输入你的服务地址，如 http://localhost:8070/actuator/bus-refresh，注意将 localhost 替换成服务器的外网 IP。</p>
<p><img src="https://images.gitbook.cn/1ae0fd10-d7ac-11e9-ad2d-e1c058c00235" alt="16" /></p>
<h3 id="-2">总结</h3>
<p>本节课我们讲解了使用 Spring Clound Config 来实现远程配置中心的具体操作，使用 Git 存储配置信息，每次修改配置信息后都需要重启各种微服务，非常麻烦，Spring Cloud 提供了自动刷新的解决方案，在不重启微服务的情况下，通过 RabbitMQ 来完成配置信息的自动更新。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p></div></article>