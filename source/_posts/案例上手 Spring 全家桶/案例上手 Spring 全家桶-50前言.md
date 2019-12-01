---
title: 案例上手 Spring 全家桶-50
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们描述了微服务的理论知识，本节课进入 Spring Cloud 的学习阶段，首先我们来学习服务治理。</p>
<p>服务治理的核心组成有三部分：服务提供者、服务消费者、注册中心。</p>
<p>在分布式系统架构中，每个微服务（服务提供者、服务消费者）在启动时，将自己的信息存储在注册中心，我们把这个过程称之为服务注册。服务消费者要调用服务提供者的接口，就得找到服务提供者，从注册中心查询服务提供者的网络信息，并通过此信息来调用服务提供者的接口，这个过程就是服务发现。</p>
<p>既然叫服务治理就不仅仅是服务注册与服务发现，同时还包括了服务的管理，即注册中心需要对记录在案的微服务进行统一管理，如何来具体实现管理呢？各个微服务与注册中心通过心跳机制完成通信，每间隔一定时间微服务就会向注册中心汇报一次，如果注册中心长时间无法与某个微服务通信，就会自动销毁该微服务。当某个微服务的网络信息发生变化时，会重新注册。同时，微服务可以通过客户端缓存将需要调用的服务地址保存起来，并通过定时任务更新的方式来保证服务的时效性，这样可以降低注册中心的压力，如果注册中心出现问题，也不会影响微服务之间的调用。</p>
<p>服务提供者、服务消费者、注册中心的关联：</p>
<ul>
<li>首先启动注册中心；</li>
<li>服务提供者启动时，在注册中心注册可以提供的服务；</li>
<li>服务消费者启动时，在注册中心订阅需要调用的服务；</li>
<li>注册中心将服务提供者的信息推送给服务调用者；</li>
<li>服务调用者通过相关信息（IP、端口等）调用服务提供者的服务。</li>
</ul>
<p>注册中心核心模块：</p>
<ul>
<li>服务注册表：用来存储各个微服务的信息，注册中心提供 API 来查询和管理各个微服务。</li>
<li>服务注册：微服务在启动时，将自己的信息在保存在注册中心。</li>
<li>服务发现：查询需要调用的微服务的网络信息，如 IP 地址、端口。</li>
<li>服务检查：通过心跳机制与完成注册的各个微服务完成通信，如果发现某个微服务长时间无法访问，则销毁该服务。</li>
</ul>
<p>Spring Cloud 的服务治理可以使用 Consul 和 Eureka 组件，这里我们选择 Eureka。</p>
<h3 id="eureka">什么是 Eureka</h3>
<p>Eureka 是 Netflix 开源的基于 REST 的服务治理解决方案，Spring Cloud 集成了 Eureka，即 Spring Cloud Eureka，提供服务注册和服务发现功能，可以和基于 Spring Boot 搭建的微服务应用轻松完成整合，开箱即用，实现 Spring Cloud 的服务治理功能。Spring Cloud 对 Netflix 开源组件进行了二次封装，也就是 Spring Cloud Netflix，Spring Cloud Eureka 是 Spring Cloud Netflix 微服务套件中的一部分，基于 Netflix Eureka 实现了二次封装，实际开发中，我们就使用 Spring Cloud Eureka 来完成服务治理。</p>
<h3 id="springcloudeureka">Spring Cloud Eureka 的组成</h3>
<p>Spring Cloud Eureka 主要包含了服务端和客户端组件：Eureka Server 服务端、Eureka Client 客户端。</p>
<p>Eureka Server，是提供服务注册与发现功能的服务端，也称作服务注册中心，Eureka 支持高可用的配置。</p>
<p>Eureka Client 是客户端组件，它的功能是将微服务在 Eureka Server 完成注册和后期维护功能，包括续租、注销等。需要注册的微服务就是通过 Eureka Client 连接到  Eureka Server 完成注册的，通过心跳机制实现注册中心与微服务的通信，完成对各个服务的状态监控。</p>
<p>简单理解注册中心（Eureka Server）就相当于一个电商平台，服务提供者（Eureka Client）相当于卖家在平台上注册了一个店铺，提供出售商品的服务，服务消费者（另一个 Eureka Client）相当于用户在平台上注册账号，然后就可以在平台的各个店铺中购买商品了，同时平台（Eureka Server）还提供管理买家与卖家信息的功能，比如卖家是否在线、可以提供哪些具体服务等。</p>
<p><img src="https://images.gitbook.cn/ca104260-ccde-11e9-8d89-4fa271cb1633" width = "70%" /></p>
<p>接下来我们就一起实现一个注册中心。</p>
<h3 id="-1">代码实现</h3>
<p>1. 首先创建一个 Maven 父工程。</p>
<p><img src="https://images.gitbook.cn/f1bf6890-ccde-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/f9d28440-ccde-11e9-beb5-a53251e30de8" width = "70%" /></p>
<p>2. 输入 GroupId、ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/0795ec70-ccdf-11e9-9a11-bbb3551196dc" width = "70%" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/0edba600-ccdf-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p>4. 在 pom.xml 中添加相关依赖，Spring Cloud Finchley 使用的是 Spring Boot 2.0.x，不能使用 Spring Boot 1.5.x。</p>
<pre><code class="xml language-xml">&lt;!-- 引入 Spring Boot 的依赖 --&gt;
&lt;parent&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
    &lt;version&gt;2.0.7.RELEASE&lt;/version&gt;
&lt;/parent&gt;

&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;!-- 解决 JDK9 以上版本没有 JAXB API jar 的问题，JDK9 以下版本不需要配置 --&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;javax.xml.bind&lt;/groupId&gt;
        &lt;artifactId&gt;jaxb-api&lt;/artifactId&gt;
        &lt;version&gt;2.3.0&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
        &lt;artifactId&gt;jaxb-impl&lt;/artifactId&gt;
        &lt;version&gt;2.3.0&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
        &lt;artifactId&gt;jaxb-core&lt;/artifactId&gt;
        &lt;version&gt;2.3.0&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;javax.activation&lt;/groupId&gt;
        &lt;artifactId&gt;activation&lt;/artifactId&gt;
        &lt;version&gt;1.1.1&lt;/version&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;

&lt;!-- 引入 Spring Cloud 的依赖，管理 Spring Cloud 各组件 --&gt;
&lt;dependencyManagement&gt;
    &lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-dependencies&lt;/artifactId&gt;
            &lt;version&gt;Finchley.SR2&lt;/version&gt;
            &lt;type&gt;pom&lt;/type&gt;
            &lt;scope&gt;import&lt;/scope&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
&lt;/dependencyManagement&gt;
</code></pre>
<p>5. 在父工程下创建一个 Module，实现 Eureka Server。</p>
<p><img src="https://images.gitbook.cn/22002940-ccdf-11e9-9a11-bbb3551196dc" width = "70%" /></p>
<p>6. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/2c17a070-ccdf-11e9-8d89-4fa271cb1633" width = "70%" /></p>
<p>7. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/36b6e540-ccdf-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p>8. 在 pom.xml 中添加 Eureka Server 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-server&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>9. 在 resources 路径下创建配置文件 application.yml，添加 Eureka Server 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
    service-url:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Eureka Server 服务端口。</li>
<li>eureka.client.register-with-eureka：是否将当前 Eureka Server 服务作为客户端进行注册。</li>
<li>eureka.client.fetch-registry：是否获取其他 Eureka Server 服务的数据。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
</ul>
<p>10. 在 Java 路径下创建启动类 RegistryCenter。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableEurekaServer
public class RegistryCenterApplication {
    public static void main(String[] args) {
        SpringApplication.run(RegistryCenterApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
<li>@EnableEurekaServer：声明该类是一个 Eureka Server 微服务，提供发现服务的功能，即注册中心。</li>
</ul>
<p>11. 运行 RegistryCenter，启动成功控制台输出如下信息。</p>
<p><img src="https://images.gitbook.cn/8e3804c0-ccdf-11e9-8d89-4fa271cb1633" alt="9" /></p>
<p>12. 打开浏览器，访问 http://localhost:8761，可看到如下界面，注册中心启动成功。</p>
<p><img src="https://images.gitbook.cn/a26608c0-ccdf-11e9-beb5-a53251e30de8" alt="10" /></p>
<p>13. No instances avaliable 表示当前没有发现微服务实例，即没有微服务完成注册，如果我们将 application.yml 中的 register-with-eureka 属性值改为 true，如下所示，则表示 Eureka Server 将自己作为客户端进行注册。</p>
<pre><code class="yaml language-yaml">server:
  port: 8761
eureka:
  client:
    register-with-eureka: true
    fetch-registry: false
    service-url:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>14. 重启 RegistryCenter，打开浏览器访问 http://localhost:8761，可看到如下界面，当前注册中心有一个客户端服务注册在案，即 Eureka Server 自己。</p>
<p><img src="https://images.gitbook.cn/c95a4360-ccdf-11e9-8d89-4fa271cb1633" alt="11" /></p>
<h3 id="-2">总结</h3>
<p>本节课我们讲解了微服务架构中注册中心的搭建，这里我们使用的组件是 Spring Cloud Eureka，为方便读者阅读及下载源码，本课程的 Spring Cloud 相关代码统一放置在一个父工程下，每节课的内容对应一个 Module。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>