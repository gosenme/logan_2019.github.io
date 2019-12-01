---
title: 案例上手 Spring 全家桶-57
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们说到 Feign 提供了容错功能，该功能是结合 Hystrix 实现的，本节课我们就来学习 Hystrix 的相关知识。</p>
<h3 id="-1">什么是微服务容错机制？</h3>
<p>在一个分布式系统中，各个微服务之间相互调用、彼此依赖，实际运行环境中可能会因为各种个样的原因导致某个微服务不可用，则依赖于该服务的其他微服务就会出现响应时间过长或者请求失败的情况，如果这种情况出现的次数较多，从一定程度上就可以能导致整个系统崩溃，如何来解决这一问题呢？</p>
<p>在不改变各个微服务调用关系的前提下，可以针对这些错误情况提前设置处理方案，遇到问题时，整个系统可以自主进行调整，这就是微服务容错机制的原理，发现故障并及时处理。</p>
<h3 id="hystrix">什么是 Hystrix？</h3>
<p>Hystrix 是 Netflix 的一个开源项目，是一个熔断器模型的具体实现，熔断器就类似于电路中的保险丝，某个单元发生故障就通过烧断保险丝的方式来阻止故障蔓延，微服务架构的容错机制也是这个原理。Hystrix 的主要作用是当服务提供者发生故障无法访问时，向服务消费者返回 fallback 降级处理，从而响应时间过长或者直接抛出异常的情况。</p>
<p>Hystrix 设计原则：</p>
<ul>
<li>服务隔离机制，防止某个服务提供者出问题而影响到整个系统的运行。</li>
<li>服务降级机制，服务出现故障时向服务消费者返回 fallback 处理机制。</li>
<li>熔断机制，当服务消费者请求的失败率达到某个特定数值时，会迅速启动熔断机制并进行修复。</li>
<li>提供实时的监控和报警功能，迅速发现服务中存在的故障。</li>
<li>提供实时的配置修改功能，保证故障问题可以及时得到处理和修复。</li>
</ul>
<p>上节课中我们演示了 Hystrix 的熔断机制，本节课重点介绍 Hystrix 的另外一个重要功能——数据监控。</p>
<p>Hystrix 除了可以为服务提供容错机制外，同时还提供了对请求的监控，这个功能需要结合 Spring Boot Actuator 来使用，Actuator 提供了对服务的健康监控、数据统计功能，可以通过 hystrix-stream 节点获取监控到的请求数据，Dashboard 组件则提供了数据的可视化监控功能，接下来我们通过代码来实现 Hystrix 的数据监控。</p>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/e3d840f0-d25e-11e9-84ba-0bd4ba7d7fb3" alt="5" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/ecceb7c0-d25e-11e9-bcae-b7c2737c8da6" alt="2" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/f75878c0-d25e-11e9-b943-9d5bb2abdc80" alt="3" /></p>
<p>4. 在 pom.xml 中添加 Eureka Client、Feign、Hystrix 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-openfeign&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-actuator&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加 Hystrix 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8060
spring:
  application:
    name: hystrix
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
feign:
  hystrix:
    enabled: true
management:
  endpoints:
    web:
      exposure:
        include: 'hystrix.stream'
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Hystrix 服务端口。</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
<li>eureka.instance.prefer-ip-address：是否将当前服务的 IP 注册到 Eureka Server。</li>
<li>feign.hystrix.enabled：是否开启熔断器。</li>
<li>management.endpoints.web.exposure.include：用来暴露 endpoints 的相关信息。</li>
</ul>
<p>6. 在 java 路径下创建启动类 HystrixApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableFeignClients
@EnableCircuitBreaker
public class HystrixApplication {
    public static void main(String[] args) {
        SpringApplication.run(HystrixApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
<li>@EnableFeignClients：声明启用 Feign。</li>
<li>@EnableCircuitBreaker：声明启用数据监控。</li>
<li>@EnableHystrixDashboard：声明启用可视化数据监控。</li>
</ul>
<p>7. 接下来通过接口的方式调用 Provider 服务，首先创建对应的实体类 Student。</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
@NoArgsConstructor
public class Student {
    private long id;
    private String name;
    private char gender;
}
</code></pre>
<p>8. 创建 FeignProviderClient 接口。</p>
<pre><code class="java language-java">@FeignClient(value = "provider")
public interface FeignProviderClient {

    @GetMapping("/student/index")
    public String index();

    @GetMapping("/student/findAll")
    public Collection&lt;Student&gt; findAll();

    @GetMapping("/student/findById/{id}")
    public Student findById(@PathVariable("id") long id);

    @PostMapping("/student/save")
    public void save(@RequestBody Student student);

    @PutMapping("/student/update")
    public void update(@RequestBody Student student);

    @DeleteMapping("/student/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id);
}
</code></pre>
<p>@FeignClient 指定 Feign 要调用的微服务，直接指定服务提供者 Provider 在注册中心的 application name 即可。</p>
<p>9. 创建 HystrixHandler，通过 @Autowired 注入 FeignProviderClient 实例，完成相关业务。</p>
<pre><code class="java language-java">@RequestMapping("/hystrix")
@RestController
public class HystrixHandler {
    @Autowired
    private FeignProviderClient feignProviderClient;

    @GetMapping("/index")
    public String index(){
        return feignProviderClient.index();
    }

    @GetMapping("/findAll")
    public Collection&lt;Student&gt; findAll(){
        return feignProviderClient.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id") long id){
        return feignProviderClient.findById(id);
    }

    @PostMapping("/save")
    public void save(@RequestBody Student student){
        feignProviderClient.save(student);
    }

    @PutMapping("/update")
    public void update(@RequestBody Student student){
        feignProviderClient.update(student);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        feignProviderClient.deleteById(id);
    }
}
</code></pre>
<p>10. 依次启动注册中心、Provider、Hystrix，如下图所示。</p>
<p><img src="https://images.gitbook.cn/3f12e600-d25f-11e9-b943-9d5bb2abdc80" alt="4" /></p>
<p>11. 可以直接访问红框中的 URL 来监控数据，在浏览器地址栏输入 http://localhost:8060/actuator/hystrix.stream，可看到如下界面。</p>
<p><img src="https://images.gitbook.cn/48388320-d25f-11e9-bcae-b7c2737c8da6" alt="5" /></p>
<p>12. 此时没有客户端请求，所以没有数据，访问 http://localhost:8060/hystrix/index，可看到如下界面。</p>
<p><img src="https://images.gitbook.cn/5062f760-d25f-11e9-bcae-b7c2737c8da6" alt="6" /></p>
<p>13. 再次访问 http://localhost:8060/actuator/hystrix.stream，可看到如下界面。</p>
<p><img src="https://images.gitbook.cn/58ae1300-d25f-11e9-84ba-0bd4ba7d7fb3" alt="7" /></p>
<p>14. 显示了监控数据情况，但是这种方式并不直观，通过可视化界面的方式能够更加直观地进行监控数据，添加 Dashboard 即可，pom.xml 添加相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
  &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
  &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix-dashboard&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>15. HystrixApplication 类定义处添加 @EnableHystrixDashboard 注解。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableFeignClients
@EnableCircuitBreaker
@EnableHystrixDashboard
public class HystrixApplication {
    public static void main(String[] args) {
        SpringApplication.run(HystrixApplication.class,args);
    }
}
</code></pre>
<p>访问 http://localhost:8060/hystrix，可看到如下界面。</p>
<p><img src="https://images.gitbook.cn/674f3100-d25f-11e9-b943-9d5bb2abdc80" alt="8" /></p>
<p>16. 在红框处输入 http://localhost:8060/actuator/hystrix.stream 以及 Tiltle，点击 Monitor Stream 按钮，如下图所示。</p>
<p><img src="https://images.gitbook.cn/70ba1480-d25f-11e9-8d0f-6b56ebcd1907" alt="9" /></p>
<p>17. 来了到可视化监控数据界面。</p>
<p><img src="https://images.gitbook.cn/77475380-d25f-11e9-b943-9d5bb2abdc80" alt="10" /></p>
<h3 id="-2">总结</h3>
<p>本节课我们讲解了使用 Hystrix 来实现数据监控的具体操作，Hystrix 是 Netflix 的一个开源项目，可以通过熔断器模型来阻止故障蔓延，从而提升系统的可用性与容错性，同时可以通过 Hystrix 实现数据监控。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>