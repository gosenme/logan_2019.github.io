---
title: Spring Cloud 快速入门-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过前面章节，我们已经学习了 SpringCloud 的很多组件，每个组件都创建了一个工程，而每个工程都会有一个配置文件，并且有些配置是一样的。例如：在实际项目中，我们创建了用户和订单两个服务，这两个服务是同一个数据库，那么我们在这两个服务的配置文件都会配置相同的数据源，一旦我们的数据库地址发生改变（只是一种情况），用户和订单两个服务的配置文件都需要改，这还是只是两个服务，在一个大型系统（比如淘宝），将会有成千上万个服务，按照这种方式代价无疑是巨大的。</p>
<p>不过无需担心，正所谓上有政策，下有对策，既然有这个问题，就一定会有解决方案，那就是创建一个配置中心，专门用于管理系统的所有配置，也就是我们将所有配置文件放到统一的地方进行管理。</p>
<p>我们知道，SpringCloud 就是为了简化开发而生的，因此 SpringCloud 为我们集成了配置中心——Spring Cloud Config 组件。</p>
<h3 id="springcloudconfig">Spring Cloud Config 简介</h3>
<p>Spring Cloud Config 是一个高可用的分布式配置中心，它支持将配置存放到内存（本地），也支持将其放到 Git 仓库进行统一管理（本课主要探讨和 Git 的融合）。</p>
<h3 id="">创建配置中心</h3>
<p>创建配置中心一般分为以下几个步骤：</p>
<p>1.创建 Git 仓库。</p>
<p>本文为了演示实例，已经创建好了用于存放配置文件的 Git 仓库，<a href="https://github.com/lynnlovemin/SpringCloudLesson.git">点击这里</a>访问。</p>
<p>2.创建配置中心。</p>
<p>在原有工程创建一个 moudle，命名为 config，在 pom.xml 加入配置中心的依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-config-server&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-hystrix&lt;/artifactId&gt;
        &lt;/dependency&gt;
</code></pre>
<p>创建启动类 Application.java：</p>
<pre><code class="java language-java">@SpringCloudApplication
@EnableConfigServer
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<blockquote>
  <p>注意，要加入 @EnableConfigServer 注解，否则配置中心是无法开启的。</p>
</blockquote>
<p>创建 application.yml 并增加如下内容：</p>
<pre><code class="yaml language-yaml">server:
  port: 8888
spring:
  application:
    name: config
  profiles:
    active: dev
  cloud:
    config:
      server:
        git:
          uri: https://github.com/lynnlovemin/SpringCloudLesson.git #配置git仓库地址
          searchPaths: 第09课/config #配置仓库路径
          username: ****** #访问git仓库的用户名
          password: ****** #访问git仓库的用户密码
      label: master #配置仓库的分支
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>首先分别启动注册中心 eurekaserver 和配置中心 config，浏览器访问：http://localhost:8761，我们可以看到如下界面：</p>
<p><img src="http://images.gitbook.cn/ac2908d0-5a3f-11e8-aeed-29e82ca41b83" alt="enter image description here" /></p>
<p>通过上述过程，配置服务中心已经创建完成，启动它并且访问地址：http://localhost:8888/config/dev，即可看到：</p>
<p><img src="http://images.gitbook.cn/0c1818c0-5a41-11e8-bd2b-4381a443b33d" alt="enter image description here" /></p>
<p>3.修改各个服务配置。</p>
<p>我们创建配置中心的目的就是为了方便其他服务进行统一的配置管理，因此，还需要修改各个服务。</p>
<p>以服务提供者 eurekaclient 为例，按照以下步骤进行操作。</p>
<p>在 pom.xml 加入配置中心依赖：</p>
<pre><code class="xml language-xml"> &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
        &lt;/dependency&gt;
</code></pre>
<p>在 resources 下新建 bootstrap.yml 并删除 application.yml（注意：这里不是 application.yml，而是 bootstrap.yml）：</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: eurekaclient
      label: master
      discovery:
        enabled: true
        serviceId: config
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>在配置中心配置的 Git 仓库相应路径下创建配置文件 eurekaclient.yml（本实例为第09课/config）:</p>
<pre><code class="yaml language-yaml">server:
  port: 8763
spring:
  application:
    name: eurekaclient
</code></pre>
<p>我们依次启动注册中心、配置中心和服务提供者 eurekaclient，可以看到 eurekaclient 的监听端口为 8763，然后修改 eurekaclient.yml 的 server.port 为8764，重新启动 eurekaclient，可以看到其监听端口为 8764，说明 eurekaclient 成功从 Git 上拉取了配置。</p>
<h3 id="-1">配置自动刷新</h3>
<p>我们注意到，每次修改配置都需要重新启动服务，配置才会生效，这种做法也比较麻烦，因此我们需要一个机制，每次修改了配置文件，各个服务配置自动生效，Spring Cloud 给我们提供了解决方案。</p>
<h4 id="-2">手动刷新配置</h4>
<p>我们先来看看如何通过手动方式刷新配置。</p>
<p>1.在 eurekaclient 工程的 pom.xml 添加依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-actuator&lt;/artifactId&gt;
        &lt;/dependency&gt;
</code></pre>
<p>2.修改远程 Git 仓库的配置文件 eurekaclient.yml，增加以下内容：</p>
<pre><code class="yaml language-yaml">management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info
</code></pre>
<p>Spring Boot 2.0 以后，actuator 默认只开启 health 和 info 端点，要使用 refresh 端点需要通过 management 指定。</p>
<p>3.在 HelloController 类加入 <code>@RefeshScope</code> 依赖：</p>
<pre><code class="java language-java">@RestController
@RefreshScope
public class HelloController {

    @Value("${server.port}")
    private int port;

    @RequestMapping("index")
    public String index(){
        return "Hello World!,端口："+port;
    }
}
</code></pre>
<p>以上步骤就集成了手动刷新配置。下面开始进行测试。</p>
<ol>
<li>依次启动注册中心，配置中心，客户端；</li>
<li>访问地址：http://localhost:8763/index，即可看到：
<img src="http://images.gitbook.cn/2d7602e0-5ef4-11e8-95e8-074055ff8c6f" alt="enter image description here" /></li>
<li>修改 Git 仓库远程配置文件 eurekaclient.yml 的端口为8764；</li>
<li>重新访问2的地址，我们发现端口未发生改变；</li>
<li>POST 方式请求地址：http://localhost:8763/actuator/refresh，如：<code>curl -X POST http://localhost:8763/refresh</code>，或在postman上请求，可以在客户端控制台看到如下日志信息：
<img src="http://images.gitbook.cn/bba42c90-5ef4-11e8-b82b-ffbb9d1e8856" alt="enter image description here" />
说明 refresh 端点已请求配置中心刷新配置。
6.再次访问2的地址，可以看到：
<img src="http://images.gitbook.cn/86750fd0-5ef4-11e8-b82c-e1d608026a45" alt="enter image description here" />
我们发现端口已发生改变，说明刷新成功！</li>
</ol>
<h4 id="-3">自动刷新配置</h4>
<p>前面我们讲了通过 <code>/refresh</code> 端点手动刷新配置，如果每个微服务的配置都需要我们手动刷新，代价无疑是巨大的。不仅如此，随着系统的不断扩张，维护也越来越麻烦。因此，我们有必要实现自动刷新配置。</p>
<h5 id="-4"><strong>自动刷新配置原理</strong></h5>
<ol>
<li>利用 Git 仓库的 WebHook，可以设置当有内容 Push 上去后，则通过 HTTP 的 POST 远程请求指定地址。</li>
<li>利用消息队列如 RabbitMQ、Kafka 等自动通知到每个微服务（本文以 RabbitMQ 为例讲解）。</li>
</ol>
<h5 id="-5"><strong>实现步骤</strong></h5>
<p>下面我们就来实现自动刷新配置。</p>
<p>1.安装 RabbitMQ（安装步骤省略，请自行百度）。</p>
<p>2.在 eurekaclient 加入如下依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-bus-amqp&lt;/artifactId&gt;
        &lt;/dependency&gt;
</code></pre>
<p>3.在 config的application.yml 添加以下内容：</p>
<pre><code class="yaml language-yaml">management:
    endpoints:
        web:
            exposure:
                include: refresh,health,info,bus-refresh
spring:
    rabbitmq:
        host: 127.0.0.1
        port: 5672
        username: guest
        password: guest
        virtualHost: /
        publisherConfirms: true
</code></pre>
<p>4.启动注册中心、配置中心和客户端；</p>
<p>5.POST 方式请求：http://localhost:8763/actuator/bus-refresh，可以看到配置已被刷新。</p>
<p>6.利用 Git 的 WebHook，实现自动刷新，如图：</p>
<p><img src="http://images.gitbook.cn/5c494220-5efa-11e8-b82c-e1d608026a45" alt="enter image description here" /></p>
<p>设置好刷新 URL 后，点击提交。以后每次有新的内容被提交后，会自动请求该 URL 实现配置的自动刷新。</p></div></article>