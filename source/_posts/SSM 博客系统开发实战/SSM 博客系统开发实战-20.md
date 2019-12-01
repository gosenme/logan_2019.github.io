---
title: SSM 博客系统开发实战-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>到这里所有课程已经讲完了，不知道大家学的怎么样？下面带大家对整个课程做一个总结。</p>
<h3 id="ssm">SSM 框架</h3>
<p>课程开始，在导读文章中为大家详细介绍了 SSM 框架，然后带大家用 SSM 框架搭建了一个 HelloWolrd 项目，这里简单回顾下 SSM 框架。</p>
<blockquote>
  <p>SSM = SpringMVC + Spring + Mybatis</p>
</blockquote>
<h4 id="springmvc">SpringMVC</h4>
<p>关于 SpringMVC 要掌握它的工作流程，面试的时候有可能会问到。</p>
<p>springMVC 工作流程见下说明：</p>
<ol>
<li><p>用户发送请求至前端控制器 DispatcherServlet。</p></li>
<li><p>DispatcherServlet 收到请求后调用 HandlerMapping 处理器映射器。</p></li>
<li><p>HandlerMapping 找到具体的处理器返回给 DispatcherServlet。</p></li>
<li><p>DispatcherServlet 通过 HandlerAdapter 处理器适配器调用具体的 Controller 控制器。</p></li>
<li><p>Controller 控制器将处理结果封装到 ModelAndView 中并返回。</p></li>
<li><p>ModelAndView 经过视图解析器 ViewReslover 解析后返回具体的视图 View。</p></li>
<li><p>DispatcherServlet 将 View 渲染之后响应给用户。</p></li>
</ol>
<h4 id="spring">Spring</h4>
<p>关于 Spring 不得不说它的三个特性：IOC、DI 和 AOP。</p>
<ul>
<li><p>IOC：将对象创建的权利交给 Spring 来管理，由 Spring 框架来完成对象的实例化。</p></li>
<li><p>DI：依赖注入，注入方式包括：构造方法注入、setter 方法注入、接口注入、配置文件注入、注解注入等。</p></li>
<li><p>AOP：面向切面编程，传统的编程方式都是纵向编程，即从上到下依次执行。如果想在代码中间加上日志，只能修改别人的代码，这样就违背了开闭原则。而使用切面编程的方式，可以在不改变原代码的情况下，在某个方法执行前后执行我们想执行的代码，比如添加 log 日志等。</p></li>
</ul>
<p>开闭原则（Open-Closed Principle, OCP），即一个软件实体应当对扩展开放，对修改关闭。即软件实体应尽量在不修改原有代码的情况下进行扩展。</p>
<h4 id="mybatis">Mybatis</h4>
<p>Mybatis 是 ORM（对象关系映射）型持久层框架，用于操作数据库的框架，支持定制化 SQL、存储过程以及高级映射等。</p>
<p>Mapper 和 Mybatis 相结合使得操作数据库更加方便、简单。通用 Mapper 是国内某技术大牛基于 Mybatis 开发的一个插件，封装了大部分常用的增删改查方法。使用方法很简单，只要继承 <code>Mapper&lt;T&gt;</code> 接口即可拥有其所有的通用方法。省去手写 XML 的烦恼，简化开发。但对于比较复杂的查询语句，我们还是要手写 XML 的。在项目中也有体现。</p>
<p>面试官有可能会问 Mybatis 和 Hibernate 的区别？主要从以下三点来回答：</p>
<ol>
<li>难易程度：Mybatis 简单易用，上手快，而 Hibernate 掌握起来难度较大。</li>
<li>对象管理：Hibernate 是完整的对象/关系映射解决方案，它提供了对象状态管理的功能，使开发者不需要关心底层数据库系统的细节。而 Mybatis 在这一块没有文档说明，用户需要自己对对象进行详细的管理。</li>
<li>优势对比：Mybatis 可以进行更为细致的 SQL 优化，可以减少查询字段。Hibernate 数据库移植性很好，Mybatis 的数据库移植性不好，不同的数据库需要写不同的 SQL。</li>
</ol>
<h3 id="maven">Maven 项目管理工具</h3>
<p>Maven 是一个项目管理工具，通过 pom.xml 文件中的配置可以引入相关依赖 Jar 包。通过 Maven 相关命令可进行项目的清理、测试、编译、打包、安装等操作。Maven 常用命令如下：</p>
<pre><code>mvn archetype:generate 创建Maven项目
mvn compile 编译源代码
mvn deploy 发布项目
mvn test-compile 编译测试源代码
mvn test 运行应用程序中的单元测试
mvn site 生成项目相关信息的网站
mvn clean 清除项目目录中的生成结果
mvn package 根据项目生成的 Jar
mvn install 在本地 Repository 中安装 Jar
mvn eclipse:eclipse 生成 Eclipse 项目文件
mvn jetty:run 启动 Jetty 服务
mvn tomcat:run 启动 Tomcat 服务
mvn clean package 
-Dmaven.test.skip=true  清除以前的包后重新打包，跳过测试类
</code></pre>
<h3 id="redis">Redis 非关系型数据库</h3>
<p>Redis 是一种非关系型数据库（NoSQL），以 <code>key-value</code> 的形式存储数据。Redis 目前主要用于缓存数据库，以减轻 MySQL 数据库的访问压力。例如，某大型电商网站，网页加载数据时首先会去 Redis 缓存数据库中查找（不考虑其他缓存技术的情况下）。找到返回，如果未找到则去 MySQL 数据库查询，将查询结果返回并保存
一份到 Redis 数据库中，下次查询的时候直接从 Redis 中获取。提高访问速度，减轻 MySQL 数据库压力。</p>
<p>一般 Redis 数据库存储数据主要有两种：</p>
<ol>
<li>热点数据，就是经常被查询的数据，出现频率高。</li>
<li>查询耗时高的数据，可能某条数据不是经常需要，但是一旦查询就耗时很长，这样会影响系统性能，所以也会放到 Redis 数据库中。</li>
</ol>
<h4 id="redis-1">Redis 优点</h4>
<p>Redis 的优点主要包括以下几点：</p>
<ol>
<li><p>性能极高：Redis 能支持超过 100k+ 每秒的读写频率。</p></li>
<li><p>丰富的数据类型：Redis 支持 String（字符串）、List（列表）、Hash（字典）、Set（集合）和 Sorted Set（有序集合）数据类型操作。</p></li>
<li><p>原子性：Redis 的所有操作都是原子性的。</p></li>
</ol>
<h4 id="redis-2">Redis 缺点</h4>
<p>Redis数据库容量受到物理内存的限制，不能用作海量数据的高性能读写，因此 Redis 适合的场景主要局限在较小数据量的高性能操作和运算上。</p>
<h3 id="ajax">AJAX 请求</h3>
<p>AJAX 请求分同步和异步请求，默认都是异步请求，同步请求需要设置 <code>async:false</code>。</p>
<ul>
<li><p>AJAX 同步请求：浏览器必须等到 AJAX 请求返回后才会向下执行代码。如果一直不返回，此时可能会出现浏览器卡死现象。</p></li>
<li><p>AJAX 异步请求：AJAX 异步请求不会影响浏览器页面的加载以及用户的其他操作。</p></li>
</ul>
<p>大部分情况下都是使用 AJAX 异步请求，只有当下一个步骤的参数需要的是 AJAX 同步请求的结果时才会使用 AJAX 同步请求。</p>
<p>AJAX异步请求格式如下：</p>
<pre><code>    $.ajax({
            type:'post',
            url:'/queryList',
            data: {"id":id,"username":username},
            dataType:'json',
            success:function(data){

            }
        });
</code></pre>
<ul>
<li>type：请求方式（Post）；</li>
<li>url：请求路径；</li>
<li>data：请求携带的 JSON 数据；</li>
<li>dataType：请求返回的数据类型（JSON）；</li>
<li>success：成功回调函数，返回的数据封装在 Data 中。</li>
</ul>
<p>上面是经过简化后的 AJAX 请求，最原始的 AJAX 请求如下：</p>
<pre><code>    //1.获取ajax核心对象
    var XHR = getXHR();
    //2.设置请求方式
    XHR.open("get","${pageContext.request.contextPath}/queryList?username="+username);
    //4.监听服务器返回状态
    XHR.onreadystatechange=function(){
         if (XHR.readyState==4 &amp;&amp; XHR.status==200)
            {
            // 5.获取服务器端响应数据  
            var jsonStr = XHR.responseText;          
         }
    }
    //3.发送请求
    XHR.send();
</code></pre>
<h3 id="activemq">ActiveMQ 消息中间件</h3>
<p>ActiveMQ 具有异步通信、解耦、流量消峰等优点：</p>
<ol>
<li><p>异步通信：生产者将消息创建好以后发送给 ActiveMQ，生产者任务已完成，而不必等待消费者消费以后才能进行其他操作。而消费者只要监听 ActiveMQ 中有没有消息，有就消费消息，没有就什么都不做。</p></li>
<li><p>解耦：不同模块之间，使用 ActiveMQ 消息中间件进行间接通信。降低耦合度，不同模块之间不会相互影响。不会因为一个模块挂掉而导致另一个模块也挂掉。</p></li>
<li><p>流量削锋：特别是在秒杀活动中应用最多，因为秒杀活动在短时间内流量很大，导致流量暴增，如果不采取缓冲策略将会击垮服务。加入 ActiveMQ 消息中间件可以控制活动的人数，缓解短时间内流量过大而压垮服务。</p></li>
</ol>
<p>假如消息队列长度超过最大数量，则直接抛弃用户请求或跳转到错误页面，秒杀业务根据消息队列中的请求信息，再做后续处理。也就是说只让部分用户成功进入秒杀活动，其他用户被拦截了，后续从
进入 ActiveMQ 中的部分用户中抽取幸运用户。</p>
<p>ActiveMQ 有两种模式：</p>
<ol>
<li><p>队列模式：即一对一的模式，一个生产者生产消息，对应一个消费者消费消息。</p></li>
<li><p>订阅模式：即一对多的模式，一个生产者生产消息，所有订阅了此消息的消费者将监听并消费此消息。</p></li>
</ol>
<h3 id="solr">Solr 搜索引擎</h3>
<p>Solr 是基于 Lucene 开发的一款企业级的搜索引擎技术。具有查询速度快，对查询结果高亮显示等优点。</p>
<p>之前课程已经教大家怎么使用 Solr，这里和大家简单说下 Solr 全文检索的实现原理。</p>
<h4 id="">全文检索</h4>
<p>首先举个例子。</p>
<p>比如现在有5个文档，我现在想从5个文档中查找出包含“Solr 工作原理”的文档，此时有两种做法。</p>
<p><strong>1.</strong> 顺序扫描法：对5个文档依次查找，包含目标字段的文档就记录下来，最后查找的结果可能是在2、3文档中，这种查找方式叫做顺序扫描法。</p>
<p>顺序扫描法在文档数量较少的情况下，查找速度还是很快的，但是当文档数量很多时，查找速度就差强人意了。</p>
<p><strong>2.</strong> 全文检索：对文档内容进行分词，对分词后的结果创建索引，然后通过对索引进行搜索的方式叫做全文检索。</p>
<p>全文检索就相当于根据偏旁部首或者拼音去查找字典，在文档很多的情况，这种查找速度肯定比你一个一个文档查找要快。</p>
<h4 id="-1">索引创建和搜索过程</h4>
<p><strong>1.创建索引。</strong></p>
<p>我们举例子。</p>
<p>文档一：Solr 是基于 Lucene 开发的企业级搜索引擎技术。</p>
<p>文档二：Solr 是一个独立的企业级搜索应用服务器，Solr 是一个高性能，基于 Lucene 的全文搜索服务器。</p>
<p>首先两个文档经过分词器分词，Solr 会为分词后的结果（词典）创建索引，然后将索引和文档 ID 列表对应起来，如下图所示：</p>
<p><img src="https://images.gitbook.cn/2901da10-866b-11e8-956e-f528114b28bd" alt="enter image description here" /></p>
<p>比如：Solr 在文档1和文档2中都有出现，所以对应的文档 ID 列表中既包含文档1的 ID 也包含文档2的 ID，文档 ID 列表对应到具体的文档，并体现该词典在该文档中出现的频次，频次越多说明权重越大，权重越大搜索的结果就会排在前面。</p>
<p>Solr 内部会对分词的结果做如下处理：</p>
<ol>
<li><p>去除停词和标点符号，例如英文的 this，that 等，中文的“的”、“一”等没有特殊含义的词。</p></li>
<li><p>会将所有的大写英文字母转换成小写，方便统一创建索引和搜索索引。</p></li>
<li><p>将复数形式转为单数形式，比如 students 转为 student，也是方便统一创建索引和搜索索引。</p></li>
</ol>
<p><strong>2. 索引搜索过程。</strong></p>
<p>知道了创建索引的过程，那么根据索引进行搜索就变得简单了，主要包括以下几步：</p>
<ol>
<li>用户输入搜索条件；</li>
<li>对搜索条件进行分词处理；</li>
<li>根据分词的结果查找索引；</li>
<li>根据索引找到文档 ID 列表；</li>
<li>根据文档 ID 列表找到具体的文档，根据出现的频次等计算权重，最后将文档列表按照权重排序返回。</li>
</ol>
<h3 id="springsecurity">Spring Security 安全框架</h3>
<p>Spring Security 的流程图如下所示：</p>
<p><img src="https://images.gitbook.cn/12685380-869b-11e8-9b0d-95de449dc107" alt="enter image description here" /></p>
<p>过程可拆解为以下8步：</p>
<ol>
<li><p>用户发出登录请求。</p></li>
<li><p>首先经过 SecurityContextPersistenceFilter 过滤器，将 Session 中的认证信息保存到 SecurityContextHodlder 中。</p></li>
<li><p>根据用户名密码还是根据手机号验证，会走不同的认证逻辑过滤器，如果根据用户名密码验证就走 UsernamePasswordAuthenticationFilter，封装令牌 Token，设置请求信息等。</p></li>
<li><p>然后通过 AuthenticationManager 认证管理器，遍历所有的 AuthenticationProvider，找到支持该 Token 的认证提供者即 AbstractUserDetailsAuthenticationProvide。</p></li>
<li><p>AbstractUserDetailsAuthenticationProvider 会调用它的子类 DaoAuthenticationProvider 的 retrieveUser 方法来获取用户信息 UserDetails。</p></li>
<li><p>而 DaoAuthenticationProvider 会调用 UserDetailsService 接口的 loadUserByUsername 方法来获取用户信息 UserDetails，我们只要实现 UserDetailsService 接口，写获取用户信息的逻辑就可以了。</p></li>
<li><p>如果整个过程都没有异常，则认证通过，最终将认证结果 Authentication 保存到 SecurityContext 中，然后将 SecurityContext 保存到 SecurityContextHolder 中。</p></li>
<li><p>再次经过 SecurityContextPersistenceFilter 过滤器时，将 SecurityContextHolder 中的 SecurityContext 保存到 Session 中，清空 SecurityContextHolder 中的内容，这样就记住了当前用户的登录状态。</p></li>
</ol>
<h3 id="-2">问题总结</h3>
<p><strong>1.</strong> Spring Security整合时  如果报“Unable to create a Configuration, because no Bean Validation provider could be found. Add a provider like Hibernate Validator (RI) to your classpath”异常，我们采取的解决方法是：加入 <code>hibernate-validator</code> 依赖：</p>
<pre><code>&lt;dependency&gt;
  &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
  &lt;artifactId&gt;hibernate-validator&lt;/artifactId&gt;
  &lt;version&gt;5.2.4.Final&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p><strong>2.</strong> 如果报“Access is denied (user is anonymous); redirecting to authentication entry point org.springframework.security.access.AccessDeniedException: Access is denied”异常，我们采取的解决办法是：检查不需要拦截的 URL 是否都已配置，比如验证码、CSS、JS、Images 等。</p>
<p><strong>3.</strong> 如果图片上传时一直处于等待状态，查看 <code>spring-security.xml</code> 中是否进行了下面的配置：</p>
<pre><code>&lt;security:headers&gt;
    &lt;security:frame-options disabled="true"&gt;&lt;/security:frame-options&gt;
&lt;/security:headers&gt;
</code></pre>
<p><strong>4.</strong> 如果遇到数据库插入不了的情况，检查表的字段是否含有非空（not null）的字段（除了主键），如果有，将其修改为 default null，否则此字段没有数据时则插入不了。</p>
<p><strong>5.</strong> 如果使用的是阿里云服务器部署项目，发送邮件的25端口被禁用了，可以申请解封或者使用465端口，还有激活链接之前使用的是 <code>localhost:8080</code> 开头，如果你使用自己的域名的话记得更换。</p>
<h3 id="-3">意见反馈</h3>
<p>希望每个人学完这个课程之后都能有所收获！</p>
<p>如果您对我的课程有什么意见或者建议，希望您发送至我的邮箱：dreamland_wang@163.com，或者直接添加好友（微信：w364107350、QQ：2844860842），加好友时请备注：gitchat。</p>
<p>dreamland 项目 Github 下载地址：</p>
<blockquote>
  <p>https://github.com/wanglinyong/dreamland</p>
</blockquote>
<p>我的 CSDN 博客地址：</p>
<blockquote>
  <p>https://blog.csdn.net/abcwanglinyong</p>
</blockquote>
<p>我的 Hexo 博客地址：</p>
<blockquote>
  <p>https://wanglinyong.github.io</p>
</blockquote></div></article>