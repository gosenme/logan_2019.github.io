---
title: Spring Cloud 快速入门-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h1 id="04springcloud">第04课：初识 Spring Cloud</h1>
<hr />
<p>Spring Cloud 基于 Spring Boot，因此在前几篇，我们系统地学习了 Spring Boot 的基础知识，为深入研究 Spring Cloud 打下扎实的基础。</p>
<p>从本章开始，我们将正式进入探索 Spring Cloud 秘密的旅程中。学习完本课程后，读者将从中学习到如何搭建一个完整的分布式架构，从而向架构师方向靠近。</p>
<h3 id="">微服务概述</h3>
<p>根据官网，微服务可以在“自己的程序”中运行，并通过“轻量级设备与 HTTP 型 API 进行沟通”。关键在于该服务可以在自己的程序中运行。通过这一点我们就可以将服务公开与微服务架构（在现有系统中分布一个 API）区分开来。在服务公开中，许多服务都可以被内部独立进程所限制。如果其中任何一个服务需要增加某种功能，那么就必须缩小进程范围。在微服务架构中，只需要在特定的某种服务中增加所需功能，而不影响整体进程。</p>
<p>微服务的核心是 API，在一个大型系统中，我们可以将其拆分为一个个的子模块，每一个模块就可以是一个服务，各服务之间通过 API 进行通信。</p>
<h3 id="springcloud">什么是 Spring Cloud</h3>
<p>Spring Cloud 是微服务架构思想的一个具体实现，它为开发人员提供了快速构建分布式系统中一些常见模式的工具（例如配置管理、服务发、断路器，智能路由、微代理、控制总线等）。</p>
<p>Spring Cloud 基于 Spring Boot 框架，它不重复造轮子，而是将第三方实现的微服务应用的一些模块集成进去。准确的说，Spring Cloud 是一个容器。</p>
<h3 id="springcloud-1">最简单的 Spring Cloud 项目</h3>
<p>学习任何一门语言和框架，从 Hello World 入门是最合适的，Spring Cloud 也不例外，接下来，我们就来实现一个最简单的 Spring Cloud 项目。</p>
<p>最简单的 Spring Cloud 微服务架构包括服务发现和服务提供者（即一个大型系统拆分出来的子模块），最极端的微服务可以做到一个方法就是一个服务，一个方法就是一个项目。在一个系统中，服务怎么拆分，要具体问题具体分析，也取决于系统的并发性、高可用性等因素。</p>
<p>接下来，我们就先创建一个最简单的 Spring Cloud 项目。</p>
<p><strong>1.</strong> 新建一个 Maven 工程，ArtifactId 为 springcloud，GroupId 为 com.lynn，如图：</p>
<p><img src="https://images.gitbook.cn/64b7cca0-494c-11e9-99d4-dfadbb5b8dbf" alt="enter image description here" />
<img src="https://images.gitbook.cn/689e2e90-494c-11e9-9f9a-07ff224f37b2" alt="enter image description here" /></p>
<p>并在 pom.xml 添加依赖：</p>
<pre><code>&lt;packaging&gt;pom&lt;/packaging&gt;

    &lt;parent&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
        &lt;version&gt;2.1.3.RELEASE&lt;/version&gt;
        &lt;relativePath/&gt; &lt;!-- lookup parent from repository --&gt;
    &lt;/parent&gt;
    &lt;dependencyManagement&gt;
        &lt;dependencies&gt;
            &lt;dependency&gt;
                &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
                &lt;artifactId&gt;spring-cloud-dependencies&lt;/artifactId&gt;
                &lt;version&gt;Greenwich.RELEASE&lt;/version&gt;
                &lt;type&gt;pom&lt;/type&gt;
                &lt;scope&gt;import&lt;/scope&gt;
                &lt;exclusions&gt;
                &lt;/exclusions&gt;
            &lt;/dependency&gt;
        &lt;/dependencies&gt;
    &lt;/dependencyManagement&gt;
</code></pre>
<p><strong>2</strong>.创建服务的注册与发现服务端，在 springcloud 工程右键 New-Module，ArtifactId 取名为 eurekaserver，如图：</p>
<p><img src="https://images.gitbook.cn/ddf16e00-494c-11e9-99d4-dfadbb5b8dbf" alt="enter image description here" /></p>
<p>在 eurekaserver 下的 pom.xml 中添加依赖如下：</p>
<pre><code>&lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-server&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
</code></pre>
<p><strong>3.</strong> 在 eurekaserver 新建配置文件 application.yml，并添加以下内容：</p>
<pre><code class="yaml language-yaml">server:
  port: 8761
spring:
  application:
    name: eurekaserver
  profiles:
    active: dev
  cloud:
    inetutils:
      preferred-networks: 127.0.0.1
    client:
      ip-address: 127.0.0.1
eureka:
  server:
    peer-node-read-timeout-ms: 3000
    enable-self-preservation: true
  instance:
    prefer-ip-address: true
    instance-id: ${spring.cloud.client.ip-address}:${server.port}
  client:
    registerWithEureka: true
    fetchRegistry: false
    healthcheck:
      enabled: true
    serviceUrl:
      defaultZone: http://127.0.0.1:8761/eureka/
</code></pre>
<p><strong>4.</strong> 添加一个启动类 Application.java：</p>
<pre><code class="java language-java">@SpringCloudApplication
@EnableEurekaServer
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
</code></pre>
<p>启动 Application 的 main 方法，浏览器输入：http://localhost:8761，可以看到如图所示界面：</p>
<p><img src="https://images.gitbook.cn/b614e450-494e-11e9-9675-055a4c4b91fa" alt="enter image description here" /></p>
<p>以上只是 Spring Cloud 的入门实例，是为了给大家展示什么是 Spring Cloud，本文暂不对上述代码做任何解释，在后面的学习中，将依次介绍Spring Cloud的各个组件，如果要深入研究它，就必须学习本文之后的课程。在后面的课程中，我将各个模块逐步拆解，一个一个给大家详细讲解。</p></div></article>