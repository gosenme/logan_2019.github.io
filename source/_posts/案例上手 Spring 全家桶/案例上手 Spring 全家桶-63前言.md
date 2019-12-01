---
title: 案例上手 Spring 全家桶-63
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们搭建了 Spring Cloud 实战项目的基本环境，本节课我们来实现注册中心和配置中心。</p>
<h3 id="-1">注册中心</h3>
<p>注册中心是管理调度微服务的核心组件，每个服务提供者或者服务消费者在启动时，会将自己的信息存储在注册中心，服务消费者可以从注册中心查询服务提供者的网络信息，并通过此信息来调用服务提供者的接口。微服务实例与注册中心通过心跳机制完成交互，如果注册中心长时间无法连接某个微服务实例，就会自动销毁该微服务，当某个微服务的网络信息发生变化时，会重新注册。所有的微服务（无论是服务提供者还是服务消费者，包括配置中心）都需要在注册中心进行注册，才能实现调用。</p>
<h3 id="-2">代码实现</h3>
<p>1. 在父工程下创建 Module。</p>
<p><img src="https://images.gitbook.cn/af33cdf0-dd54-11e9-9cc8-a572519b0723" alt="1" /></p>
<p><img src="https://images.gitbook.cn/b68b88e0-dd54-11e9-aaec-b5744b419935" alt="2" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/a0327210-dd55-11e9-9cc8-a572519b0723" alt="3" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/a6839270-dd55-11e9-8134-9900814ad853" alt="4" /></p>
<p>4. 在 pom.xml 中引入 Eureka Server 相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-server&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 目录下创建配置文件 application.yml，添加 Eureka Server 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
    service-url:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>6. 在 java 目录下创建启动类 RegistryCenterApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableEurekaServer
public class RegistryCenterApplication {
    public static void main(String[] args) {
        SpringApplication.run(RegistryCenterApplication.class,args);
    }
}
</code></pre>
<h3 id="-3">配置中心</h3>
<p>配置中心可以对所有微服务的配置文件进行统一管理，便于部署和维护，接下来我们为系统创建配置中心 Config Server，将所有微服务的配置文件统一通过 Git 仓库进行管理。</p>
<p>1. 在父工程下创建一个 Module，命名为 configserver，pom.xml 添加 Spring Cloud Config 相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-config-server&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 在 resources 目录下创建配置文件 application.yml，添加 Config Server 相关配置。</p>
<pre><code class="yaml language-yaml">server:
  port: 8888
spring:
  application:
    name: configserver
  cloud:
    bus:
      trace:
        enable: true
    config:
      server:
        git:
          uri: https://github.com/southwind9801/orderingsystem.git #Git 仓库地址
          searchPaths: config #仓库路径
          username: root #Git 仓库用户名
          password: root #Git 仓库密码
      label: master #仓库的分支
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>3. 在 java 目录下创建配置中心的启动类 ConfigServerApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class,args);
    }
}
</code></pre>
<h3 id="-4">创建数据库</h3>
<p>数据库共 5 张表，分别是：</p>
<ul>
<li>t_admin：保存管理员数据</li>
<li>t_menu：保存菜品数据</li>
<li>t_order：保存订单数据</li>
<li>t_type：保存菜品分类数据</li>
<li>t_user：保存用户数据</li>
</ul>
<p>SQL 脚本如下：</p>
<pre><code class="sql language-sql">DROP TABLE IF EXISTS `t_admin`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(11) DEFAULT NULL,
  `password` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `t_menu`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `flavor` varchar(11) DEFAULT NULL,
  `tid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tid` (`tid`),
  CONSTRAINT `t_menu_ibfk_1` FOREIGN KEY (`tid`) REFERENCES `t_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `t_order`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `mid` int(11) DEFAULT NULL,
  `aid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  KEY `mid` (`mid`),
  KEY `aid` (`aid`),
  CONSTRAINT `t_order_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `t_user` (`id`),
  CONSTRAINT `t_order_ibfk_2` FOREIGN KEY (`mid`) REFERENCES `t_menu` (`id`),
  CONSTRAINT `t_order_ibfk_3` FOREIGN KEY (`aid`) REFERENCES `t_admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `t_type`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `t_user`;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(11) DEFAULT NULL,
  `password` varchar(11) DEFAULT NULL,
  `nickname` varchar(11) DEFAULT NULL,
  `gender` varchar(2) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `registerdate` date DEFAULT NULL,
  `address` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
</code></pre>
<h3 id="-5">总结</h3>
<p>本节课我们讲解了实战项目注册中心和配置中心的搭建，同时完成了数据表的创建和数据导入。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>