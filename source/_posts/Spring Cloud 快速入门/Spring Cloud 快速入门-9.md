---
title: Spring Cloud 快速入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇，我们讲了服务之间的相互通信，利用 OpenFeign 的声明式 HTTP 客户端，通过注解的形式很容易做到不同服务之间的相互调用。</p>
<p>我们的服务最终是部署在服务器上，因为各种原因，服务难免会发生故障，那么其他服务去调用这个服务就会调不到，甚至会一直卡在那里，导致用户体验不好。针对这个问题，我们就需要对服务接口做错误处理，一旦发现无法访问服务，则立即返回并报错，我们捕捉到这个异常就可以以可读化的字符串返回到前端。</p>
<p>为了解决这个问题，业界提出了熔断器模型。</p>
<h3 id="hystrix">Hystrix 组件</h3>
<p>SpringCloud 集成了 Netflix 开源的 Hystrix 组件，该组件实现了熔断器模型，它使得我们很方便地实现熔断器。</p>
<p>在实际项目中，一个请求调用多个服务是比较常见的，如果较底层的服务发生故障将会发生连锁反应。这对于一个大型项目是灾难性的。因此，我们需要利用 Hystrix 组件，当特定的服务不可用达到一个阈值（Hystrix 默认 5 秒 20 次），将打开熔断器，即可避免发生连锁反应。</p>
<h3 id="">代码实现</h3>
<p>紧接上一篇的代码，OpenFeign 是默认自带熔断器的，但是默认关闭的，我们可以在 application.yml 中开启它：</p>
<pre><code class="yaml language-yaml">eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
server:
  port: 8081
spring:
  application:
    name: feign
#开启熔断器
feign:
  hystrix:
    enabled: true
</code></pre>
<p>新建一个类 ApiServiceError.java 并实现 ApiService：</p>
<pre><code class="java language-java">@Component
public class ApiServiceError implements ApiService {

    @Override
    public String index() {
        return "服务发生故障！";
    }
}
</code></pre>
<p>然后在 ApiService 的注解中指定 fallback：</p>
<pre><code class="java language-java">@FeignClient(value = "eurekaclient",fallback = ApiServiceError.class)
public interface ApiService {

    @RequestMapping(value = "/index",method = RequestMethod.GET)
    String index();
}
</code></pre>
<p>在 pom.xml 中添加 web 依赖：</p>
<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>再创建 Controller 类：ApiController，加入如下代码：</p>
<pre><code class="java language-java">@RestController
public class ApiController {

    @Autowired
    private ApiService apiService;

    @RequestMapping("index")
    public String index(){
        return apiService.index();
    }
}
</code></pre>
<h3 id="-1">测试熔断器</h3>
<p>分别启动注册中心 EurekaServer、服务提供者 EurekaClient 和服务消费者 Feign，然后访问：<a href="http://localhost:8081/index">http://localhost:8081/index</a>，可以看到顺利请求到接口：</p>
<p><img src="http://images.gitbook.cn/e38b2d90-584f-11e8-af46-6927e96ff1fc" alt="enter image description here" /></p>
<p>然后停止 EurekaClient，再次请求，可以看到熔断器生效了：</p>
<p><img src="http://images.gitbook.cn/03b59560-5850-11e8-af46-6927e96ff1fc" alt="enter image description here" /></p>
<h3 id="-2">熔断器监控</h3>
<p>Hystrix 给我们提供了一个强大的功能，那就是 Dashboard。Dashboard 是一个 Web 界面，它可以让我们监控 Hystrix Command 的响应时间、请求成功率等数据。</p>
<p>下面我们开始改造 feign 工程，在 feign 工程的 pom.xml 下加入依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
    &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix-dashboard&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>然后在启动类 Application.java 中加入 <code>@EnableHystrixDashboard</code>，并增加一个 Bean 方法：</p>
<pre><code class="java language-java">@SpringCloudApplication
@EnableFeignClients
@EnableHystrixDashboard
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Bean
    public ServletRegistrationBean getServlet(){
        HystrixMetricsStreamServlet streamServlet = new HystrixMetricsStreamServlet();
        ServletRegistrationBean registrationBean = new ServletRegistrationBean(streamServlet );
        registrationBean.setLoadOnStartup(1);
        registrationBean.addUrlMappings("/hystrix.stream");
     registrationBean.setName("HystrixMetricsStreamServlet");
        return registrationBean;
    }
}
</code></pre>
<p>然后分别启动 EurekaServer、EurekaClient 和 Feign 并访问：<a href="http://localhost:8081/hystrix">http://localhost:8081/hystrix</a>，可以看到如下画面：</p>
<p><img src="http://images.gitbook.cn/0830b5e0-5853-11e8-a6ee-37cda6a3c12b" alt="enter image description here" /></p>
<p>按照上图箭头所示，输入相关信息后，单击 Monitor Stream 按钮进入下一界面，打开新窗口访问：<a href="http://localhost:8081/index">http://localhost:8081/index</a>，在 Dashboard 界面即可看到 Hystrix 监控界面：</p>
<p><img src="http://images.gitbook.cn/452b8510-5853-11e8-af46-6927e96ff1fc" alt="enter image description here" /></p>
<p>Hystrix 熔断器的基本用法就介绍到这里。前面我们创建了注册中心、服务提供者、服务消费者、服务网关和熔断器，每个工程都有配置文件，而且有些配置是想通的，按照这个方式进行应用程序的配置，维护性较差，扩展性也较差，比如很多个服务都会配置数据源，而数据源只有一个，那么如果我们的数据源地址发生变化，所有地方都需要改，如何改进这个问题呢？下一课所讲解的配置中心就是为解决这个问题而生的，敬请期待。</p></div></article>