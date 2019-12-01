---
title: Spring Cloud 快速入门-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>前面我们提到，对外提供接口通过 gateway 服务网关实现。一个大型的系统由多个微服务模块组成，各模块之间不可避免需要进行通信，一般我们可以通过内部接口调用的形式，服务 A 提供一个接口，服务 B 通过 HTTP 请求调用服务 A 的接口，为了简化开发，Spring Cloud 提供了一个基础组件方便不同服务之间的 HTTP 调用，那就是 OpenFeign。</p>
<h3 id="openfeign">什么是 OpenFeign</h3>
<p>OpenFeign 是一个声明式的 HTTP 客户端，它简化了 HTTP 客户端的开发。使用 OpenFeign，只需要创建一个接口并注解，就能很轻松的调用各服务提供的 HTTP 接口。OpenFeign 默认集成了 Ribbon，默认实现了负载均衡。</p>
<h3 id="feign">创建 Feign 服务</h3>
<p>在根项目上创建一个 module，命名为 feign，然后在 pom.xml 添加如下内容：</p>
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
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix&lt;/artifactId&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
</code></pre>
<p>创建 application.yml，内容如下：</p>
<pre><code class="yaml language-yaml">eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
server:
  port: 8081
spring:
  application:
    name: feign
</code></pre>
<p>最后创建一个启动类 Application:</p>
<pre><code class="java language-java">@SpringCloudApplication
@EnableFeignClients
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
</code></pre>
<p>我们可以看到启动类增加了一个新的注解：<code>@EnableFeignClients</code>，如果我们要使用 OpenFeign 声明式 HTTP 客户端，必须要在启动类加入这个注解，以开启 OpenFeign。</p>
<p>这样，我们的 OpenFeign 就已经集成完成了，那么如何通过 OpenFeign 去调用之前我们写的 HTTP 接口呢？请看下面的做法。</p>
<p>首先创建一个接口 ApiService，并且通过注解配置要调用的服务地址：</p>
<pre><code class="java language-java">@FeignClient(value = "eurekaclient")
public interface ApiService {

    @RequestMapping(value = "/index",method = RequestMethod.GET)
    String index();
}
</code></pre>
<p>分别启动注册中心 EurekaServer、服务提供者EurekaClient（这里服务提供者启动两次，端口分别为8762、8763，以观察 OpenFeign 的负载均衡效果）。</p>
<p>然后在 OpenFeign 里面通过单元测试来查看效果。</p>
<p>1.添加单元测试依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-test&lt;/artifactId&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
</code></pre>
<p>2.添加测试代码。</p>
<pre><code class="java language-java">@SpringBootTest(classes = Application.class)
@RunWith(SpringJUnit4ClassRunner.class)
public class TestDB {

    @Autowired
    private ApiService apiService;

    @Test
    public void test(){
        try {
            System.out.println(apiService.index());
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
</code></pre>
<p>最后分别启动两次单元测试类，我们可以发现控制台分别打印如下信息：</p>
<pre><code class="text language-text">Hello World!,端口：8762
</code></pre>
<pre><code class="text language-text">Hello World!,端口：8763
</code></pre>
<p>由此可见，我们成功调用了服务提供者提供的接口，并且循环调用不同的接口，说明它自带了负载均衡效果。</p></div></article>