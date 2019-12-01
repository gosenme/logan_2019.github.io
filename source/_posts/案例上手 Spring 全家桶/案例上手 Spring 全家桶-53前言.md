---
title: 案例上手 Spring 全家桶-53
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在前面的课程中，我们通过 Eureka Client 组件创建了一个服务提供者 provider，并且在注册中心完成注册，接下来其他微服务就可以访问 provider 相关服务了。</p>
<p>本节课我们就来实现一个服务消费者 consumer，调用 provider 相关接口，实现思路是先通过 Spring Boot 搭建一个微服务应用，再通过 Eureka Client 将其注册到 Eureka Server。此时的 provider 和 consumer 从代码的角度看并没有区别，都是 Eureka 客户端，我们人为地从业务角度对它们进行区分，provider 提供服务，consumer 调用服务，具体的实现需要结合 RestTemplate 来完成，即在服务消费者 consumer 中通过 RestTemplate 来调用服务提供者 provider 的相关接口。</p>
<p><img src="https://images.gitbook.cn/23f40cc0-d23f-11e9-b943-9d5bb2abdc80" alt="13" /></p>
<p>1. 在父工程下创建 Module，实现 Eureka Client。</p>
<p><img src="https://images.gitbook.cn/4d8ed650-d23f-11e9-84ba-0bd4ba7d7fb3" alt="1" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/575b3ac0-d23f-11e9-bcae-b7c2737c8da6" alt="2" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/61ecc3f0-d23f-11e9-84ba-0bd4ba7d7fb3" alt="3" /></p>
<p>4. 在 pom.xml 中添加 Eureka Client 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加 Eureka Client 相关配置，此时的 Eureka Client 为服务消费者 consumer。</p>
<pre><code class="yaml language-yaml">server:
  port: 8020
spring:
  application:
    name: consumer
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
</code></pre>
<p>属性说明：</p>
<ul>
<li>server.port：当前 Eureka Client 服务端口。</li>
<li>spring.application.name：当前服务注册在 Eureka Server 上的名称。</li>
<li>eureka.client.service-url.defaultZone：注册中心的访问地址。</li>
<li>eureka.instance.prefer-ip-address：是否将当前服务的 IP 注册到 Eureka Server。</li>
</ul>
<p>6. 在 java 路径下创建启动类 ConsumerApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
public class ConsumerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
</ul>
<p>7. 现在让 consumer 调用 provider 提供的服务，首先创建实体类 Student。</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
@NoArgsConstructor
public class Student {
    private long id;
    private String name;
    private char gender;
}
</code></pre>
<p>8. 修改 ConsumerApplication 代码，创建 RestTemplate 实例并通过 @Bean 注解注入到 IoC 容器中，添加代码如下所示。</p>
<pre><code class="java language-java">@SpringBootApplication
public class ConsumerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConsumerApplication.class,args);
    }

    @Bean
    public RestTemplate restTemplate(){
        return new RestTemplate();
    }
}
</code></pre>
<p>9. 创建 StudentHandler，注入 RestTemplate 实例，业务方法中通过 RestTemplate 来调用 provider 的相关服务。</p>
<pre><code class="java language-java">@RequestMapping("/consumer")
@RestController
public class StudentHandler {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/findAll")
    public Collection&lt;Student&gt; findAll(){
        return restTemplate.getForObject("http://localhost:8010/student/findAll",Collection.class);
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id") long id){
        return restTemplate.getForObject("http://localhost:8010/student/findById/{id}",Student.class,id);
    }

    @PostMapping("/save")
    public void save(@RequestBody Student student){
        restTemplate.postForObject("http://localhost:8010/student/save",student,Student.class);
    }

    @PutMapping("/update")
    public void update(@RequestBody Student student){
        restTemplate.put("http://localhost:8010/student/update",student);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        restTemplate.delete("http://localhost:8010/student/deleteById/{id}",id);
    }
}
</code></pre>
<p>10. 依次启动注册中心、服务提供者 provider，并运行 ConsumerApplication，启动成功控制台输出如下信息。</p>
<p><img src="https://images.gitbook.cn/94545c40-d23f-11e9-bcae-b7c2737c8da6" alt="4" /></p>
<p>11. 打开浏览器，访问 http://localhost:8761，看到如下界面。</p>
<p><img src="https://images.gitbook.cn/9e9ef160-d23f-11e9-84ba-0bd4ba7d7fb3" alt="5" /></p>
<p>12. 可以看到服务提供者 provider 和服务消费者 consumer 已经在 Eureka Server 完成注册，接下来就可以访问 consumer 的相关服务了，通过 Postman 工具测试 consumer 接口。</p>
<ul>
<li>findAll 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/aac5c090-d23f-11e9-8d0f-6b56ebcd1907" alt="6" /></p>
<ul>
<li>findById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/b4556a20-d23f-11e9-84ba-0bd4ba7d7fb3" alt="7" /></p>
<ul>
<li>save 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/bc142440-d23f-11e9-bcae-b7c2737c8da6" alt="8" /></p>
<p>添加完成之后再来查询，调用 findAll 接口，可以看到新数据已经添加成功。</p>
<p><img src="https://images.gitbook.cn/c5418990-d23f-11e9-8d0f-6b56ebcd1907" alt="9" /></p>
<ul>
<li>update 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/ccfaec80-d23f-11e9-84ba-0bd4ba7d7fb3" alt="10" /></p>
<p>修改完成之后再来查询，调用 findAll 接口，可以看到修改之后的数据。</p>
<p><img src="https://images.gitbook.cn/d596e740-d23f-11e9-8d0f-6b56ebcd1907" alt="11" /></p>
<ul>
<li>deleteById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/16d02370-d240-11e9-84ba-0bd4ba7d7fb3" alt="12" /></p>
<p>删除完成之后再来查询，调用 findAll 接口，可以看到数据已经被删除。</p>
<p><img src="https://images.gitbook.cn/1d7b98d0-d240-11e9-8d0f-6b56ebcd1907" alt="6" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了使用 Eureka Client 组件在 Eureka Server 注册一个服务消费者 consumer 的具体实现，无论是服务消费者还是服务提供者，都通过 Eureka Client 组件来实现注册，实现服务消费者 consumer 之后，通过 RestTemplate 完成对服务提供者 provider 相关服务的调用。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>