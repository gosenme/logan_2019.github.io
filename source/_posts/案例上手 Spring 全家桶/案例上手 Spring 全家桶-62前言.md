---
title: 案例上手 Spring 全家桶-62
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>经过前面课程的学习，大家已经对微服务架构的理论有了一定的了解，并且也掌握了 Spring Cloud 相关组件的使用，一切的理论学习都是为了实际应用，通过实践也能更好的去消化理论知识，从本节课开始，我们将一起来搭建一个基于微服务架构的外卖点餐系统实际案例。</p>
<p>本节课首先来搭建 Spring Cloud 实战项目的基础环境。</p>
<h3 id="-1">项目需求</h3>
<p>本项目分为客户端和后台管理系统两个界面，客户端针对普通用户，功能包括用户登录、用户退出、菜品订购、我的订单。</p>
<p>后台管理系统针对管理员，功能包括管理员登录、管理员退出、添加菜品、查询菜品、修改菜品、删除菜品、订单处理、添加用户、查询用户、删除用户。</p>
<p><img src="https://images.gitbook.cn/b065be50-d7ae-11e9-8797-4924c0d7c082" alt="1" /></p>
<p>了解完需求之后，接下来设计系统架构，首先分配出 4 个服务提供者：account、menu、order、user。</p>
<ul>
<li>account 提供账户服务：用户和管理员登录。</li>
<li>menu 提供菜品服务：添加菜品、查询菜品、修改菜品、删除菜品。</li>
<li>order 提供订单服务：添加订单、查询订单、删除订单、处理订单。</li>
<li>user 提供用户服务：添加用户、查询用户、删除用户。</li>
</ul>
<p>接下来分配出 1 个服务消费者，包括客户端的前端页面和后台接口、后台管理系统的前端页面和后台接口，用户/管理员直接访问的资源都保存在服务消费者中，然后服务消费者调用 4 个服务提供者对应的接口完成业务逻辑，并通过 Feign 实现负载均衡。</p>
<p>4 个服务提供者和 1 个服务消费者都需要在注册中心进行注册，同时要注册配置中心，提供远程配置信息读取，服务提供者和服务消费者的配置信息保存在 Git 远程仓库，由配置中心负责拉取。</p>
<p>本系统共由 8 个模块组成，包括注册中心、配置中心、Git 仓库配置信息、服务消费者、4 个服务提供者，关系如下图所示。</p>
<p><img src="https://images.gitbook.cn/d1e61930-d7ae-11e9-a536-c512dee3d564" alt="2" /></p>
<p>系统架构搞清楚之后，接下来开始写代码。</p>
<h3 id="-2">代码实现</h3>
<p>1. 新建 Maven 工程。</p>
<p><img src="https://images.gitbook.cn/1e4bbf00-d7af-11e9-8797-4924c0d7c082" alt="3" /></p>
<p><img src="https://images.gitbook.cn/2b47df90-d7af-11e9-8fae-816b29059b0c" alt="4" /></p>
<p>2. 输入 GroupId、ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/328fbc00-d7af-11e9-a536-c512dee3d564" alt="5" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/39733150-d7af-11e9-8797-4924c0d7c082" alt="6" /></p>
<p>4. 在 pom.xml 中引入 Spring Boot 和 Spring Cloud 相关依赖，其中 JAXB API 的依赖只针对 JDK 9 以上版本，如果你是 JDK 9 以下版本，不需要配置。</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"&gt;
    &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;

    &lt;groupId&gt;com.southwind&lt;/groupId&gt;
    &lt;artifactId&gt;orderingsystem&lt;/artifactId&gt;
    &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;

    &lt;!-- 引入 Spring Boot 的依赖 --&gt;
    &lt;parent&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
        &lt;version&gt;2.0.7.RELEASE&lt;/version&gt;
    &lt;/parent&gt;

    &lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;!-- 解决 JDK 9 以上版本没有 JAXB API 的问题 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;javax.xml.bind&lt;/groupId&gt;
            &lt;artifactId&gt;jaxb-api&lt;/artifactId&gt;
            &lt;version&gt;2.3.0&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
            &lt;artifactId&gt;jaxb-impl&lt;/artifactId&gt;
            &lt;version&gt;2.3.0&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.sun.xml.bind&lt;/groupId&gt;
            &lt;artifactId&gt;jaxb-core&lt;/artifactId&gt;
            &lt;version&gt;2.3.0&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;javax.activation&lt;/groupId&gt;
            &lt;artifactId&gt;activation&lt;/artifactId&gt;
            &lt;version&gt;1.1.1&lt;/version&gt;
        &lt;/dependency&gt;

        &lt;dependency&gt;
            &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
            &lt;artifactId&gt;lombok&lt;/artifactId&gt;
            &lt;optional&gt;true&lt;/optional&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;

    &lt;!-- 引入 Spring Cloud 的依赖，管理 Spring Cloud 生态各个组件 --&gt;
    &lt;dependencyManagement&gt;
        &lt;dependencies&gt;
            &lt;dependency&gt;
                &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
                &lt;artifactId&gt;spring-cloud-dependencies&lt;/artifactId&gt;
                &lt;version&gt;Finchley.SR2&lt;/version&gt;
                &lt;type&gt;pom&lt;/type&gt;
                &lt;scope&gt;import&lt;/scope&gt;
            &lt;/dependency&gt;
        &lt;/dependencies&gt;
    &lt;/dependencyManagement&gt;

&lt;/project&gt;
</code></pre>
<p>系统环境搭建完成，从下节课开始我们来实现各种服务提供者。</p>
<h3 id="-3">总结</h3>
<p>本节课是我们整个 Spring 全家桶课程的最后一个章节，使用 Spring Cloud 实现分布式系统：外卖订餐系统，首先我们讲解了系统的需求，让大家对整个系统有一个直观的认知，然后搭建了 Spring Cloud 的基本环境，后续的课程我们会一步步完善实战项目的开发。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>