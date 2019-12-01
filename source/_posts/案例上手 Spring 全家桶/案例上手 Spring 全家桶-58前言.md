---
title: 案例上手 Spring 全家桶-58
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在基于微服务的分布式系统中，每个业务模块都可以拆分为一个独立自治的服务，多个请求来协同完成某个需求，在一个具体的业务场景中某个请求可能需要同时调用多个服务来完成，这就存在一个问题，多个微服务所对应的配置项也会非常多，一旦某个微服务进行了修改，则其他服务也需要作出调整，直接在每个微服务中修改对应的配置项是非常麻烦的，改完之后还需要重新部署项目。</p>
<p>微服务是分布式的，但是我们希望可以对所有微服务的配置文件进行集中统一管理，便于部署和维护，Spring Cloud 提供了对应的解决方案，即 Spring Cloud Config，通过服务端可以为多个客户端提供配置服务。</p>
<blockquote>
  <p><a href="https://cloud.spring.io/spring-cloud-static/Finchley.RELEASE/single/spring-cloud.html#_spring_cloud_config">官方文档地址可点击这里查看</a>。</p>
</blockquote>
<p>Spring Cloud Config 可以将配置文件存放在本地，也可以存放在远程 Git 仓库中。拿远程 Git 仓库来说，具体的操作思路是将所有的外部配置文件集中放置在 Git 仓库中，然后创建 Config Server，通过它来管理所有的配置文件，需要更改某个微服务的配置信息时，只需要在本地进行修改，然后推送到远程 Git 仓库即可，所有的微服务实例都可以通过 Config Server 来读取对应的配置信息。</p>
<p>接下来我们就一起来搭建本地 Config Server。</p>
<h3 id="-1">本地文件系统</h3>
<p>我们可以将微服务的相关配置文件存储在本地文件中，然后让微服务来读取本地配置文件，具体操作如下所示。</p>
<p>首先创建本地 Config Server。</p>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/faa36b20-d79a-11e9-a536-c512dee3d564" alt="1" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/00e6a8d0-d79b-11e9-8797-4924c0d7c082" alt="2" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/07e32460-d79b-11e9-ad2d-e1c058c00235" alt="3" /></p>
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
  port: 8762
spring:
  application:
    name: nativeconfigserver
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/shared
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Config Server 服务端口</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称</li>
<li>profiles.active：配置文件获取方式</li>
<li>cloud.config.server.native.search-locations：本地配置文件的存放路径</li>
</ul>
<p>6. 在 resources 路径下新建 shared 文件夹，并在此目录下创建本地配置文件 configclient-dev.yml，定义 port 和 foo 信息。</p>
<pre><code class="yaml language-yaml">server:
  port: 8070
foo: foo version 1
</code></pre>
<p>7. 在 java 路径下创建启动类 NativeConfigServerApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableConfigServer
public class NativeConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(NativeConfigServerApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
<li>@EnableConfigServer：声明配置中心。</li>
</ul>
<p>本地配置中心已经创建完成，接下来创建客户端来读取本地配置中的配置文件。</p>
<p>8. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/a9089c40-d79a-11e9-ad2d-e1c058c00235" alt="1" /></p>
<p>9. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/b31230c0-d79a-11e9-a536-c512dee3d564" alt="5" /></p>
<p>10. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/b93e8b10-d79a-11e9-ad2d-e1c058c00235" alt="6" /></p>
<p>11. 在 pom.xml 中添加 Spring Cloud Config 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>12. 在 resources 路径下创建 bootstrap.yml，配置读取本地配置中心的相关信息。</p>
<pre><code class="yaml language-yaml">spring:
  application:
    name: configclient
  profiles:
    active: dev
  cloud:
    config:
      uri: http://localhost:8762
      fail-fast: true
</code></pre>
<p>属性说明：</p>
<ul>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>profiles.active：配置文件名，这里需要与当前微服务在 Eureka Server 注册的名称结合起来使用，两个值用 <code>-</code> 连接，比如当前微服务的名称是 configclient，profiles.active 的值是 dev，那么就会在本地 Config Server 中查找名为 configclient-dev 的配置文件。</li>
<li>cloud.config.uri：本地 Config Server 的访问路径。</li>
<li>cloud.config.fail-fast：设置客户端优先判断 config server 获取是否正常，并快速响应失败内容。</li>
</ul>
<p>13. 在 java 路径下创建启动类 NativeConfigClientApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
public class NativeConfigClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(NativeConfigClientApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
</ul>
<p>14. 创建 NativeConfigHandler，定义相关业务方法。</p>
<pre><code class="java language-java">@RestController
@RequestMapping("/native")
public class NativeConfigHandler {

    @Value("${server.port}")
    private String port;

    @Value("${foo}")
    private String foo;

    @GetMapping("/index")
    public String index(){
        return this.port+"-"+this.foo;
    }
}
</code></pre>
<p>15. 依次启动 NativeConfigServer、ConfigClient，如下图所示。</p>
<p><img src="https://images.gitbook.cn/7614f090-d79a-11e9-a536-c512dee3d564" alt="7" /></p>
<p><img src="https://images.gitbook.cn/7cb876b0-d79a-11e9-8797-4924c0d7c082" alt="8" /></p>
<p>16. 通过 Postman 工具访问 http://localhost:8070/native/index，如下图所示。</p>
<p><img src="https://images.gitbook.cn/82c53b10-d79a-11e9-8fae-816b29059b0c" alt="9" /></p>
<p>读取本地配置成功。</p>
<h3 id="-2">总结</h3>
<p>本节课我们讲解了使用 Spring Cloud Config 来实现本地配置的具体操作，Spring Cloud Config 包括服务端（Config Server）和客户端（Config Client），提供了分布式系统外部化配置的功能，下节课我们来学习远程配置中心的搭建方式。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p></div></article>