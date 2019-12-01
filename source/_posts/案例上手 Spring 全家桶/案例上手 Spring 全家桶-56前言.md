---
title: 案例上手 Spring 全家桶-56
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们学习了使用 Ribbon + RestTemplate 实现服务调用的负载均衡，在实际开发中，还有另外一种更加便捷的方式来实现同样的功能，这就是 Feign，本节课中我们就来学习使用 Feign 实现服务消费的负载均衡。</p>
<h3 id="feign">什么是 Feign</h3>
<p>与 Ribbon 一样，Feign 也是由 Netflix 提供的，Feign 是一个提供模版的声明式 Web Service 客户端， 使用 Feign 可以简化 Web Service 客户端的编写，开发者可以通过简单的接口和注解来调用 HTTP API，使得开发更加快捷、方便。Spring Cloud 也提供了 Feign 的集成组件：Spring Cloud Feign，它整合了 Ribbon 和 Hystrix，具有可插拔、基于注解、负载均衡、服务熔断等一系列便捷功能。</p>
<p>在 Spring Cloud 中使用 Feign 非常简单，我们说过 Feign 是一个声明式的 Web Service 客户端，所以只需要创建一个接口，同时在接口上添加相关注解即可完成服务提供方的接口绑定，相比较于 Ribbon + RestTemplate 的方式，Feign 大大简化了代码的开发，Feign 支持多种注解，包括 Feign 注解、JAX-RS 注解、Spring MVC 注解等。Spring Cloud 对 Feign 进行了优化，整合了 Ribbon 和 Eureka，从而让 Feign 的使用更加方便。</p>
<blockquote>
  <p><a href="http://cloud.spring.io/spring-cloud-static/Finchley.RELEASE/single/spring-cloud.html#_spring_cloud_openfeign">官网地址请单击这里查看</a></p>
</blockquote>
<p>我们说过 Feign 是一种比 Ribbon 更加方便好用的 Web 服务客户端，那么二者有什么具体区别呢？Feign 好用在哪里？</p>
<h3 id="ribbonfeign">Ribbon 与 Feign 的区别</h3>
<p>关于 Ribbon 和 Feign 的区别可以简单地理解为 Ribbon 是个通用的 HTTP 客户端工具，而 Feign 则是基于 Ribbon 来实现的，同时它更加灵活，使用起来也更加简单，上节课中我们通过 Ribbon + RestTemplate 实现了服务调用的负载均衡，相比较于这种方式，使用 Feign 可以直接通过声明式接口的形式来调用服务，非常方便，比 Ribbon 使用起来要更加简便，只需要创建接口并添加相关注解配置，即可实现服务消费的负载均衡。</p>
<h3 id="feign-1">Feign 的特点</h3>
<ul>
<li>Feign 是一个声明式 Web Service 客户端。</li>
<li>支持 Feign 注解、JAX-RS 注解、Spring MVC 注解。</li>
<li>Feign 基于 Ribbon 实现，使用起来更加简单。</li>
<li>Feign 集成了 Hystrix，具备服务熔断功能。</li>
</ul>
<p>了解完 Feign 的基本概念，接下来我们一起实现 Feign。</p>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/52852600-d25d-11e9-b943-9d5bb2abdc80" alt="1" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/5cc7cbe0-d25d-11e9-8d0f-6b56ebcd1907" alt="2" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/646fa2a0-d25d-11e9-bcae-b7c2737c8da6" alt="3" /></p>
<p>4. 在 pom.xml 中添加 Eureka Client 和 Feign 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-openfeign&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加 Feign 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8050
spring:
  application:
    name: feign
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Feign 服务端口。</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
<li>eureka.instance.prefer-ip-address：是否将当前服务的 IP 注册到 Eureka Server。</li>
</ul>
<p>6. 在 java 路径下创建启动类 FeignApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableFeignClients
public class FeignApplication {
    public static void main(String[] args) {
        SpringApplication.run(FeignApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
<li>@EnableFeignClients：声明启用 Feign。</li>
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
<p>@FeignClient 指定 Feign 要调用的微服务，直接指定服务提供者在注册中心的 application name 即可。</p>
<p>9. 创建 FeignHandler，通过 @Autowired 注入 FeignProviderClient 实例，完成相关业务。</p>
<pre><code class="java language-java">@RequestMapping("/feign")
@RestController
public class FeignHandler {

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
<p>10. 依次启动注册中心，端口为 8010 的 Provider，端口为 8011 的 Provider、Feign，如下图所示。</p>
<p><img src="https://images.gitbook.cn/c9495a90-d25d-11e9-84ba-0bd4ba7d7fb3" alt="4" /></p>
<p>11. 打开浏览器，访问 http://localhost:8761，看到如下界面。</p>
<p><img src="https://images.gitbook.cn/d0ffb040-d25d-11e9-b943-9d5bb2abdc80" alt="5" /></p>
<p>12. 可以看到两个 Provider 和 Feign 已经在注册中心完成注册，接下来使用 Postman 工具测试 Feign 相关接口，如下图所示。</p>
<ul>
<li>findAll 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/d8229f90-d25d-11e9-bcae-b7c2737c8da6" alt="6" /></p>
<ul>
<li>findById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/de9c0870-d25d-11e9-84ba-0bd4ba7d7fb3" alt="7" /></p>
<ul>
<li>save 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/e5346b00-d25d-11e9-b943-9d5bb2abdc80" alt="8" /></p>
<p>添加完成之后再来查询，调用 findAll 接口，可以看到新数据已经添加成功。</p>
<p><img src="https://images.gitbook.cn/ec206bd0-d25d-11e9-8d0f-6b56ebcd1907" alt="9" /></p>
<ul>
<li>update 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/f307ffd0-d25d-11e9-8d0f-6b56ebcd1907" alt="10" /></p>
<p>修改完成之后再来查询，调用 findAll 接口，可以看到修改之后的数据。</p>
<p><img src="https://images.gitbook.cn/fa2a2bd0-d25d-11e9-84ba-0bd4ba7d7fb3" alt="11" /></p>
<ul>
<li>deleteById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/012dac40-d25e-11e9-b943-9d5bb2abdc80" alt="12" /></p>
<p>删除完成之后再来查询，调用 findAll 接口，可以看到数据已经被删除。</p>
<p><img src="https://images.gitbook.cn/099cf1b0-d25e-11e9-8d0f-6b56ebcd1907" alt="6" /></p>
<p>13. Feign 也提供了负载均衡功能，通过 Postman 访问 http://localhost:8050/feign/index，交替出现下图所示情况，实现了负载均衡。</p>
<p><img src="https://images.gitbook.cn/13e36820-d25e-11e9-bcae-b7c2737c8da6" alt="13" /></p>
<p><img src="https://images.gitbook.cn/1a99da00-d25e-11e9-b943-9d5bb2abdc80" alt="14" /></p>
<p>14. Feign 同时提供了容错功能，如果服务提供者 Provider 出现故障无法访问，直接访问 Feign 会报错，如下图所示。</p>
<p><img src="https://images.gitbook.cn/20dcf0a0-d25e-11e9-bcae-b7c2737c8da6" alt="15" /></p>
<p>15. 很显然这种直接返回错误状态码的交互方式不友好，可以通过容错机制给用户相应的提示信息，而非错误状态码，使得交互方式更加友好，容错机制非常简单，首先在 application.yml 中添加配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8050
spring:
  application:
    name: feign
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
feign:
  hystrix:
    enabled: true
</code></pre>
<p>feign.hystrix.enabled：是否开启熔断器。</p>
<p>16. 创建 FeignProviderClient 接口的实现类 FeignError ，定义容错处理逻辑，通过 @Component 将 FeignError 实例注入 IoC 容器。</p>
<pre><code class="java language-java">@Component
public class FeignError implements FeignProviderClient {
    @Override
    public String index() {
        return "服务器维护中....";
    }

    @Override
    public Collection&lt;Student&gt; findAll() {
        return null;
    }

    @Override
    public Student findById(long id) {
        return null;
    }

    @Override
    public void save(Student student) {

    }

    @Override
    public void update(Student student) {

    }

    @Override
    public void deleteById(long id) {

    }
}
</code></pre>
<p>17. 在 FeignProviderClient 定义处通过 @FeignClient 的 fallback 属性设置映射。</p>
<pre><code class="java language-java">@FeignClient(value = "provider",fallback = FeignError.class)
public interface FeignProviderClient {
}
</code></pre>
<p>18. 启动注册中心和 Feign，此时没有服务提供者 Provider 被注册，直接访问 Feign 接口，如下图所示。</p>
<p><img src="https://images.gitbook.cn/3b0ff0d0-d25e-11e9-84ba-0bd4ba7d7fb3" alt="16" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了使用 Feign 来实现服务消费负载均衡的具体操作，Feign 是一个提供模版的声明式 Web Service 客户端，可以帮助开发者更加方便地调用服务接口，并实现负载均衡，Feign 和 Ribbon + RestTemplate 都可以完成服务消费的负载均衡，实际开发中推荐使用 Feign。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>