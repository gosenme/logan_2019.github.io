---
title: 案例上手 Spring 全家桶-54
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在分布式项目架构中，我们会将服务进行拆分，不同的微服务负责各自的业务功能，实现软件架构层面的解耦合。但是如果拆分之后的微服务数量太多，是不利于系统开发的，因为每个服务都有不同的网络地址，客户端多次请求不同的微服务需要调用不同的 URL，如果同时去维护多个不同的 URL 无疑会增加开发的成本。</p>
<p>如下图所示，一个外卖订餐系统，需要调用多个微服务接口才能完成一次订餐的业务流程，如果能有一种解决方案可以统一管理不同的微服务 URL，肯定会增强系统的维护性，提高开发效率。</p>
<p><img src="https://images.gitbook.cn/4f766590-d240-11e9-84ba-0bd4ba7d7fb3" alt="1" /></p>
<p>这个解决方案就是 API 网关，API 网关可以对所有的 API 请求进行管理维护，相当于为系统开放出一个统一的接口，所有的外部请求只需要访问这个统一入口即可，系统内部再通过 API 网关去映射不同的微服务。对于开发者而言就不需要关注具体的微服务 URL 了，直接访问 API 网关接口即可，API 网关的结构如下图所示。</p>
<p><img src="https://images.gitbook.cn/7be66f30-d240-11e9-bcae-b7c2737c8da6" alt="2" /></p>
<p>如此一来我们就解决了上述问题，开发变得更加简单方便。本课程里我们使用 Zuul 来实现微服务网关，Spring Cloud 集成了 Zuul。</p>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/36c40000-d242-11e9-b943-9d5bb2abdc80" alt="3" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/3cb43bb0-d242-11e9-84ba-0bd4ba7d7fb3" alt="4" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/47533260-d242-11e9-b943-9d5bb2abdc80" alt="5" /></p>
<p>4. 在 pom.xml 中添加 Zuul 和 Eureka Client 依赖，Zuul 也作为一个 Eureka Client 在注册中心完成注册。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-zuul&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加网关相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8030
spring:
  application:
    name: gateway
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
zuul:
  routes:
    provider: /p/**
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 gateway 服务端口。</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
<li>zuul.routes.*：自定义微服务的访问路径，如 zuul.routes.provider：/p/**，provider 微服务就会被映射到 gateway 的 /p/** 路径。</li>
</ul>
<p>6. 在 java 路径下创建启动类 GateWayApplication。</p>
<pre><code class="java language-java">@EnableZuulProxy
@EnableAutoConfiguration
public class GateWayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GateWayApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@EnableZuulProxy 包含 @EnableZuulServer 的功能，而且还加入了 @EnableCircuitBreaker 和 @EnableDiscoveryClient。</li>
<li>@EnableAutoConfiguration 可以帮助 Spring Boot 应用将所有符合条件的 @Configuration 配置都加载到当前 Spring Boot 创建并使用的 IoC 容器。</li>
</ul>
<p>7. 依次启动注册中心、服务提供者 provider，运行 GateWayApplication，启动成功控制台输出如下信息。</p>
<p><img src="https://images.gitbook.cn/7a468ff0-d242-11e9-8d0f-6b56ebcd1907" alt="6" /></p>
<p>8. 打开浏览器，访问 http://localhost:8761，看到如下界面。</p>
<p><img src="https://images.gitbook.cn/83b12550-d242-11e9-bcae-b7c2737c8da6" alt="7" /></p>
<p>9. 可以看到服务提供者 provider 和网关 gateway 已经在 Eureka Server 完成注册，接下来就可以通过 http://localhost:8030/p/student/findAll 访问 provider 提供的相关服务了，通过 Postman 工具测试如下图所示。</p>
<p><img src="https://images.gitbook.cn/8dbae0e0-d242-11e9-bcae-b7c2737c8da6" alt="8" /></p>
<p>10. 同时 Zuul 自带了负载均衡功能，现在对服务提供者 provider 的代码进行修改，如下所示。</p>
<pre><code class="java language-java">@RequestMapping("/student")
@RestController
public class StudentHandler {

    @Value("${server.port}")
    private String port;

    @GetMapping("/index")
    public String index(){
        return "当前端口："+this.port;
    }
}
</code></pre>
<p>11. 提供了一个返回当前服务端口的方法，现在依次重启注册中心和服务提供者 provider，然后修改 provider 的端口为 8011，创建一个新的 provider 启动类并启动，最后重新启动 gateway，访问 http://localhost:8761，可看到如下界面。</p>
<p><img src="https://images.gitbook.cn/9ac53240-d242-11e9-84ba-0bd4ba7d7fb3" alt="9" /></p>
<p>12. 当前注册中心有两个 provider 服务，通过 Postman 工具测试如下图所示，端口为 8010 和 8011 的微服务交替被访问。</p>
<p><img src="https://images.gitbook.cn/a4eb0150-d242-11e9-8d0f-6b56ebcd1907" alt="10" /></p>
<p><img src="https://images.gitbook.cn/ac24acf0-d242-11e9-8d0f-6b56ebcd1907" alt="11" /></p>
<p>13、现在通过 gateway 来访问，如下图所示。</p>
<p><img src="https://images.gitbook.cn/b411ca10-d242-11e9-84ba-0bd4ba7d7fb3" alt="12" /></p>
<p><img src="https://images.gitbook.cn/c25510a0-d242-11e9-8d0f-6b56ebcd1907" alt="13" /></p>
<p>访问两次 http://localhost:8030/p/student/index，分别请求了端口为 8010 和 8011 的 provider 微服务，实现了负载均衡。</p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了使用 Zuul 组件实现服务网关的具体操作，Zuul 需要结合 Eureka Client 在注册中心完成注册，Zuul 是一个在云平台上提供动态路由，监控，弹性，安全等边缘服务的框架，相当于客户端和 Netflix 流应用 Web 网站后端所有请求的中间层，可以简化代码的开发。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>