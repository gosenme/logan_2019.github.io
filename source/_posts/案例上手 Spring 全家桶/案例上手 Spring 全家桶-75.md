---
title: 案例上手 Spring 全家桶-75
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>第七部分（第 7-1 ~ 7-7 课）有了前面的 Spring Cloud 基础，这部分内容将为大家详细讲解 Spring Cloud 的实战操作，包括 Spring Cloud 的高可用、集群、负载均衡，以及使用 layui + Spring Cloud + MyBatis + MySQL 的技术选型来完成本套课程的最终项目实战。</p>
<p>（1）谈谈你对微服务的理解。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>简单来说，微服务就是将一个单体应用拆分成若干个小型的服务，协同完成系统功能的一种架构模式，在系统架构层面进行解耦合，将一个复杂问题拆分成若干个简单问题。这样的好处是对于每一个简单问题，开发、维护、部署的难度就降低了很多，可以实现自治，可自主选择最合适的技术框架，提高了项目开发的灵活性。</li>
<li>微服务架构不仅是单纯的拆分，拆分之后的各个微服务之间还要进行通信，否则就无法协同完成需求，也就失去了拆分的意义。不同的微服务之间可以通过某种协议进行通信，相互调用、协同完成功能，并且各服务之间只需要制定统一的协议即可，至于每个微服务是用什么技术框架来实现的，统统不需要关心。这种松耦合的方式使得开发、部署都变得更加灵活，同时系统更容易扩展，降低了开发、运维的难度。</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul>
<p>（2）微服务分别有哪些优点、哪些缺点？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>微服务的优点：</p>
<ul>
<li>各个服务之间实现了松耦合，彼此之间不需要关注对方是用什么语言，什么技术开发的，只需要保证自己的接口可以正常访问，通过标准协议可以访问其他微服务的接口即可。</li>
<li>各个微服务之间是独立自治的，只需要专注于做好自己的业务，开发和维护不会影响到其他的微服务，这和单体架构中“牵一发而动全身”相比是有很大优势的。</li>
<li>微服务是一个去中心化的架构方式，相当于用零件去拼接一台机器，如果某个零件出现问题，可以随时进行替换从而保证机器的正常运转，微服务就相当于零件，整个项目就相当于零件组成的机器。</li>
</ul>
<p>微服务的不足：</p>
<ul>
<li>各个服务之间是通过远程调用的方式来完成协作任务的，如果因为某些原因导致远程调用出现问题，导致微服务不可用，就有可能产生级联反应，造成整个系统崩溃。</li>
<li>如果某个需求需要调用多个微服务，如何来保证数据的一致性是一个比较大的问题，这就给给分布式事务处理带来了挑战。</li>
<li>相比较于单体应用开发，微服务的学习难度会增加，对于加入团队的新员工来讲，如何快速掌握上手微服务架构，是他需要面对的问题。</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul>
<p>（3）谈谈微服务之间是如何实现通信的。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>远程过程调用（Remote Procedure Invocation）也就是我们常说的服务的注册与发现，直接通过远程过程调用来访问别的 service。</p>
<ul>
<li>优点：简单，因为没有中间件代理，系统更简单。</li>
<li>缺点：只支持请求/响应的模式，不支持其他类型，比如通知、请求/异步响应、发布/订阅、发布/异步响应降低了可用性，因为客户端和服务端在请求过程中必须都是可用的。</li>
</ul>
<p>使用异步消息来做服务间通信，服务间通过消息管道来交换消息，从而通信。</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（4）Spring Boot 如何集成 MyBatis？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>添加 MyBatis 的 starter maven 依赖</li>
</ul>
<pre><code class="xml language-xml">&lt;dependency&gt;
   &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
   &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<ul>
<li>在 application.yml 配置数据源信息</li>
</ul>
<pre><code class="yaml language-yaml">spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&amp;characterEncoding=UTF-8
    username: root
    password: 19900310
    driver-class-name: com.mysql.cj.jdbc.Driver
mybatis:
  mapper-locations: classpath:/mapping/*.xml
  type-aliases-package: com.southwind.entity
</code></pre>
<ul>
<li>在启动类添加 @MapperScan 注解</li>
</ul>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（5）Spring Boot 和 Spring Cloud 有哪些区别？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>Spring Boot 专注于快速方便地开发单个个体微服务。</li>
<li>Spring Cloud 是关注全局的微服务协调、整理、治理的框架，它将 Spring Boot 开发的单体整合并管理起来。</li>
<li>Spring Boot 可以脱离 Spring Cloud 独立使用开发项目，但是 Spring Cloud 离不开 Spring Boot，属于依赖关系。    </li>
</ul>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（6）使用 layui 的数据表格组件展示业务数据，后台实体类应该如何定义？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<pre><code class="java language-java">@Data
public class Order {
    private long id;
    private User user;
    private Menu menu;
    private Admin admin;
    private Date date;
    private int state;
}
</code></pre>
<pre><code class="java language-java">@Data
public class OrderVO {
    private int code;
    private String msg;
    private int count;
    private List&lt;Order&gt; data;
}
</code></pre>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（7）JPA 和 Spring Data JPA 是一回事吗？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>JPA 和 Spring Data JPA 是完全不同的两个概念，JPA（Java Persistence API）是 Java 持久层规范，定义了一些列 ORM 接口，它本身是不能直接使用的，因为接口需要实现才能使用，Hibernate 框架就是实现 JPA 规范的框架。</li>
<li>Spring Data JPA 是 Spring 框架提供的对 JPA 规范的抽象，通过约定的命名规范完成持久层接口的编写，在不需要实现接口的情况下，就可以实现对数据库的操作。简单理解就是通过 Spring Data JPA，你只需要定义接口而不需要实现，就能完成 CRUD 操作。</li>
<li>Spring Data JPA 本身并不是一个具体实现，它只是一个抽象层，底层还是需要 Hibernate 这样的 JPA 实现来提供支持。</li>
</ul>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（8）如果要给项目添加权限管理系统，一般包含哪些需求？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>权限管理：查询，创建，修改，删除</li>
<li>角色管理：查询，创建，修改，删除，添加权限</li>
<li>用户管理：查询，创建，修改，删除，添加角色</li>
</ul>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（9）微服务架构的拆分都有哪些原则？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li>基于业务逻辑拆分</li>
</ul>
<p>将系统中的业务模块按照职责范围识别出来，每个单独的业务模块拆分为一个独立的服务。</p>
<p>例如，做一个电商系统，可以划分为商品、交易、用户 3 个服务，也可以划分为商品、订单、支付、发货、买家、卖家 6 个服务。</p>
<ul>
<li>基于可扩展拆分</li>
</ul>
<p>将系统中的业务模块按照稳定性排序，将已经成熟和改动不大的服务拆分为稳定服务，将经常变化和迭代的服务拆分为变动服务。稳定服务的粒度可以粗一些，即使逻辑上关联不强的也可以放在一个服务中，例如日志服务、升级服务放在一个子系统中。变动服务的粒度可以细一些，但要注意服务的数量。这种拆分方式是为了提升项目快速迭代的效率，避免变动服务的改动升级影响了成熟的功能。</p>
<ul>
<li>基于可靠性拆分</li>
</ul>
<p>将系统中可靠性要求高的核心服务和可靠性要求低的非核心服务拆分开来，然后重点保证核心服务的高可用。</p>
<ul>
<li>基于性能拆分</li>
</ul>
<p>将性能压力大的模块拆出来，避免影响其他服务，同时对其做性能提升、高可用等优化都更简单高效。例如电商的抢购，排队功能的性能压力很大，就可以将其独立为一个服务。</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（10）Feign 和 Ribbon + RestTemplate 的区别是什么？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>Ribbon + RestTemplate 实现了服务调用的负载均衡，相比较于这种方式，使用 Feign 可以直接通过声明式接口的形式来调用服务，非常方便，比 Ribbon 使用起来要更加简便，只需要创建接口并添加相关注解配置，即可实现服务消费的负载均衡。</p>
<p>Feign 的特点</p>
<ul>
<li>Feign 是一个声明式 Web Service 客户端</li>
<li>支持 Feign 注解、JAX-RS 注解、Spring MVC 注解</li>
<li>Feign 基于 Ribbon 实现，使用起来更加简单</li>
<li>Feign 集成了 Hystrix，具备服务熔断功能</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul></div></article>