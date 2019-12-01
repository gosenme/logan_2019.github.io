---
title: 案例上手 Spring 全家桶-45
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们学习了如何使用 Spring Boot 整合 Redis，在实际开发中 Redis 有一个非常重要的应用就是使用它来完成 Session 共享。Session 是由 Servlet 创建并管理的，将数据保存在服务端内存中，所谓的 Session 共享并不是单体应用的范畴，如果需要实现负载均衡，为项目搭建服务端集群，那么此时就需要考虑 Session 共享的问题了，为什么呢？</p>
<p>因为在集群项目架构中，同一个客户端的不同请求有可能被分配到不同的服务终端，如下图所示。</p>
<p><img src="https://images.gitbook.cn/073afb70-c75e-11e9-9ae4-c3d609c8bfbd" width = "70%" /></p>
<p>不同服务终端的 Session 数据必须要同步，如何来解决这一问题呢？不用担心，Spring Boot 为我们提供了自动化 Session 共享解决方案，使用起来非常简单，Spring Boot 就是通过整合 Redis 来完成这一功能的，原理很简单，将各个服务终端的 Session 取出来放到一个共享服务器上，统一管理，如下图所示。</p>
<p><img src="https://images.gitbook.cn/15782780-c75e-11e9-a81a-91f9bfe6443e" alt="WX20190617-141753@2x" /></p>
<p>当请求被分配给任意一个服务终端时，操作的 Session 是从 Session Server 中读取到的，操作完成之后再存放到 Session Server 中，这样就实现了所有服务终端共享 Session 数据的功能。</p>
<p>了解完原来，接下来我们来动手实现 Session 共享。</p>
<p>1. 创建 Maven 工程，pom.xml 中添加相关依赖，spring-session-data-redis 为实现 Session 数据共享的依赖。</p>
<pre><code class="xml language-xml">&lt;parent&gt;
  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
  &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
  &lt;version&gt;2.1.0.RELEASE&lt;/version&gt;
&lt;/parent&gt;

&lt;dependencies&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-data-redis&lt;/artifactId&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.session&lt;/groupId&gt;
    &lt;artifactId&gt;spring-session-data-redis&lt;/artifactId&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 创建 SessionHandler，提供两个业务方法，set 用来向 Session 中存数据，get 从 Session 中读数据。</p>
<pre><code class="java language-java">package com.southwind.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpSession;

@RestController
public class SessionHandler {

    @Value("${server.port}")
    private String port;

    @PostMapping("/set/{name}")
    public String set(@PathVariable("name") String name, HttpSession session){
        session.setAttribute("name",this.port+"："+name);
        return (String)session.getAttribute("name");
    }

    @GetMapping("/get")
    public String get(HttpSession session){
        return (String)session.getAttribute("name");
    }
}
</code></pre>
<p>3. 创建配置文件 application.yml，添加 Redis 基本连接信息。</p>
<pre><code class="yaml language-yaml">spring:
  redis:
    database: 0
    host: localhost
    port: 6379
server:
  port: 8080
</code></pre>
<p>4. 创建启动类 Application。</p>
<pre><code class="java language-java">@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>5. 启动 Redis 服务。</p>
<p><img src="https://images.gitbook.cn/4a8d7ab0-c75e-11e9-a81a-91f9bfe6443e" alt="WX20190610-165751@2x" /></p>
<p>6. 启动 Application，打开 Postman 工具测试 8080 端口服务，调用 set 方法向 Session 中存入当前服务的端口信息。</p>
<p><img src="https://images.gitbook.cn/6cb4c3f0-c75e-11e9-a5ba-f1eeeb548c06" width = "60%" /></p>
<p>7. 修改 application.yml，将 8080 改为 8181。</p>
<pre><code class="yaml language-yaml">spring:
  redis:
    database: 0
    host: localhost
    port: 6379
server:
  port: 8181
</code></pre>
<p>8. 创建一个新的启动类 Application2。</p>
<pre><code class="java language-java">@SpringBootApplication
public class Application2 {
    public static void main(String[] args) {
        SpringApplication.run(Application2.class,args);
    }
}
</code></pre>
<p>9. 启动 Application2，打开 Postman 工具测试 8181 端口服务，调用 get 方法获取 Session 中的信息。</p>
<p><img src="https://images.gitbook.cn/8f0d7d70-c75e-11e9-9ae4-c3d609c8bfbd" width = "65%" /></p>
<p>可以看到返回的内容与 8080 服务一致，证明 8181 服务取出的信息就是上一次 8080 服务存入的数据，8080 服务和 8181 服务实现了 Session 数据共享。</p>
<p>接下来我们演示结合 Nginx 负载均衡来实现 Session 数据共享的案例。</p>
<p>10. 首先通过 Nginx 实现两个服务终端的负载均衡，修改 nginx.conf，添加 8080 服务和 8181 服务。</p>
<pre><code class="shell language-shell">worker_processes  1;   #工作进程的个数，一般与计算机的cpu核数一致

events {
    worker_connections  1024;   #单个进程最大连接数（最大连接数 = 连接数 * 进程数）
}


http {
    include       mime.types;   #文件扩展名与文件类型映射表
    default_type  application/octet-stream;   #默认文件类型

    sendfile        on;   #开启高效文件传输模式，普通应用设为 on，如果用来进行下载等应用磁盘 IO 重负载应用，可设置为 off。

    keepalive_timeout  65;   #长连接超时时间，单位是秒

    gzip  on;   #启用 Gizp 压缩

    #Tomcat 集群
    upstream  myapp {   #Tomcat 集群名称 
        server    localhost:8080;   #tomcat1 配置
        server    localhost:8181;   #tomcat2 配置
    }   

    #Nginx 的配置
    server {
        listen       9090;   #监听端口，默认 80
        server_name  localhost;   #当前 Nginx 域名

        location / {
            proxy_pass http://myapp;
            proxy_redirect default;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
</code></pre>
<p>核心配置</p>
<p><img src="https://images.gitbook.cn/b7f74680-c75e-11e9-a5ba-f1eeeb548c06" width = "65%" /></p>
<p>启动 Nginx，访问 9090 端口服务，此时 9090 是在交替访问 8080 服务和 8181 服务，无论是哪个服务，可以看到输出的信息还是 8080：zhangsan，即 8080 服务和 8181 服务在实现负载均衡的情况下，依然 Session 数据共享。</p>
<p><img src="https://images.gitbook.cn/c3744120-c75e-11e9-99c1-c37abd23c4b1" width = "70%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解 Spring Boot 结合 Redis 实现 Session 共享的具体操作，在集群项目架构中，不同服务终端的 Session 数据要实现同步，这是必须解决的问题，Spring Boot 为我们提供了自动化 Session 共享解决方案，结合 Redis 来实现，使用起来非常简单。</p>
<p><a href="https://github.com/southwind9801/gcspringbootsession.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p></div></article>