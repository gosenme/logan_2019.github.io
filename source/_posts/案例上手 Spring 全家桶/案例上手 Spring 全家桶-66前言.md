---
title: 案例上手 Spring 全家桶-66
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本节课我们来实现服务提供者 orde，order 为系统提供订单相关服务，包括添加订单、查询订单、删除订单、处理订单，具体实现如下所示。</p>
<p>1. 在父工程下创建一个 Module，命名为 order，pom.xml 添加相关依赖，order 需要访问数据库，所以集成 MyBatis 相关依赖，配置文件从 Git 仓库拉取，添加配置中心 Spring Cloud Config 相关依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
        &lt;!-- eurekaclient --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
            &lt;version&gt;2.0.0.RELEASE&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- MyBatis --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;1.3.0&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- MySQL 驱动 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;8.0.11&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;!-- 配置中心 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
            &lt;artifactId&gt;spring-cloud-starter-config&lt;/artifactId&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
</code></pre>
<p>2. 在 resources 目录下创建 bootstrap.yml，在该文件中配置拉取 Git 仓库相关配置文件的信息。</p>
<pre><code class="yaml language-yaml">spring:
  cloud:
    config:
      name: order #对应的配置文件名称
      label: master #Git 仓库分支名
      discovery:
        enabled: true
        serviceId: configserver #连接的配置中心名称
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>3. 在 java 目录下创建启动类 OrderApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class OrderApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class,args);
    }
}
</code></pre>
<p>4. 接下来为服务提供者 order 集成 MyBatis 环境，首先在 Git 仓库配置文件 order.yml 中添加相关信息。</p>
<pre><code class="yaml language-yaml">server:
  port: 8040
spring:
  application:
    name: order
  datasource:
    name: orderingsystem
    url: jdbc:mysql://localhost:3306/orderingsystem?useUnicode=true&amp;characterEncoding=UTF-8
    username: root
    password: root
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
mybatis:
  mapper-locations: classpath:mapping/*.xml
  type-aliases-package: com.southwind.entity
</code></pre>
<p>5. 在 java 目录下创建 entity 文件夹，新建 Order 类对应数据表 t_order。</p>
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
<p>6. 新建 OrderVO 类为 layui 框架提供封装类。</p>
<pre><code class="java language-java">@Data
public class OrderVO {
    private int code;
    private String msg;
    private int count;
    private List&lt;Order&gt; data;
}
</code></pre>
<p>7. 在 java 目录下创建 repository 文件夹，新建 OrderRepository 接口，定义相关业务方法。</p>
<pre><code class="java language-java">public interface OrderRepository {
    public void save(Order order);
    public List&lt;Order&gt; findAllByUid(long uid,int index,int limit);
    public int countByUid(long uid);
    public void deleteByMid(long mid);
    public void deleteByUid(long uid);
    public List&lt;Order&gt; findAllByState(int state,int index,int limit);
    public int countByState(int state);
    public void updateState(long id,long aid,int state);
}
</code></pre>
<p>8. 在 resources 目录下创建 mapping 文件夹，存放 Mapper.xml，新建 OrderRepository.xml，编写 OrderRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.OrderRepository"&gt;
    &lt;resultMap id="orderMap" type="Order"&gt;
        &lt;id property="id" column="oid"/&gt;
        &lt;result property="date" column="date"/&gt;
        &lt;result property="state" column="state"/&gt;
        &lt;!-- 映射 menu --&gt;
        &lt;association property="menu" javaType="Menu"&gt;
            &lt;id property="id" column="mid"/&gt;
            &lt;result property="name" column="name"/&gt;
            &lt;result property="price" column="price"/&gt;
            &lt;result property="flavor" column="flavor"/&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt;

    &lt;resultMap id="orderMap2" type="Order"&gt;
        &lt;id property="id" column="oid"/&gt;
        &lt;result property="date" column="date"/&gt;
        &lt;!-- 映射 menu --&gt;
        &lt;association property="menu" javaType="Menu"&gt;
            &lt;id property="id" column="mid"/&gt;
            &lt;result property="name" column="name"/&gt;
            &lt;result property="price" column="price"/&gt;
            &lt;result property="flavor" column="flavor"/&gt;
        &lt;/association&gt;
        &lt;!-- 映射 user --&gt;
        &lt;association property="user" javaType="User"&gt;
            &lt;id property="id" column="uid"/&gt;
            &lt;result property="nickname" column="nickname"/&gt;
            &lt;result property="telephone" column="telephone"/&gt;
            &lt;result property="address" column="address"/&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt;
    &lt;insert id="save" parameterType="Order"&gt;
        insert into t_order(uid,mid,aid,date,state) values(#{user.id},#{menu.id},#{admin.id},#{date},0)
    &lt;/insert&gt;

    &lt;select id="findAllByUid" resultMap="orderMap"&gt;
        select m.id mid,m.name,m.price,m.flavor,o.id oid,o.date,o.state from t_order o,t_menu m where o.mid = m.id and o.uid = #{param1} order by oid limit #{param2},#{param3}
    &lt;/select&gt;

    &lt;select id="countByUid" parameterType="long" resultType="int"&gt;
        select count(*) from t_order where uid = #{uid}
    &lt;/select&gt;

    &lt;delete id="deleteByMid" parameterType="long"&gt;
        delete from t_order where mid = #{mid}
    &lt;/delete&gt;

    &lt;delete id="deleteByUid" parameterType="long"&gt;
        delete from t_order where uid = #{uid}
    &lt;/delete&gt;

    &lt;select id="findAllByState" resultMap="orderMap2"&gt;
        select m.id mid,m.name,m.price,m.flavor,o.id oid,o.date,u.id uid,u.nickname,u.telephone,u.address from t_order o,t_menu m,t_user u where o.mid = m.id and o.uid = u.id and o.state = #{param1} order by oid limit #{param2},#{param3}
    &lt;/select&gt;

    &lt;select id="countByState" parameterType="int" resultType="int"&gt;
        select count(*) from t_order where state = #{state}
    &lt;/select&gt;

    &lt;update id="updateState"&gt;
        update t_order set aid = #{param2},state = #{param3} where id = #{param1}
    &lt;/update&gt;
&lt;/mapper&gt;
</code></pre>
<p>9. 新建 OrderHandler，将 OrderRepository 通过 @Autowired 注解进行注入，完成相关业务逻辑。</p>
<pre><code class="java language-java">@RestController
@RequestMapping("/order")
public class OrderHandler {

    @Autowired
    private OrderRepository orderRepository;

    @PostMapping("/save")
    public void save(@RequestBody Order order){
        orderRepository.save(order);
    }

    @GetMapping("/findAllByUid/{uid}/{page}/{limit}")
    public OrderVO findAllByUid(@PathVariable("uid") long uid, @PathVariable("page") int page, @PathVariable("limit") int limit){
        OrderVO orderVO = new OrderVO();
        orderVO.setCode(0);
        orderVO.setMsg("");
        orderVO.setCount(orderRepository.countByUid(uid));
        orderVO.setData(orderRepository.findAllByUid(uid,(page-1)*limit,limit));
        return orderVO;
    }

    @DeleteMapping("/deleteByMid/{mid}")
    public void deleteByMid(@PathVariable("mid") long mid){
        orderRepository.deleteByMid(mid);
    }

    @DeleteMapping("/deleteByUid/{uid}")
    public void deleteByUid(@PathVariable("uid") long uid){
        orderRepository.deleteByUid(uid);
    }

    @GetMapping("/findAllByState/{state}/{page}/{limit}")
    public OrderVO findAllByState(@PathVariable("state") int state, @PathVariable("page") int page, @PathVariable("limit") int limit){
        OrderVO orderVO = new OrderVO();
        orderVO.setCode(0);
        orderVO.setMsg("");
        orderVO.setCount(orderRepository.countByState(0));
        orderVO.setData(orderRepository.findAllByState(0,(page-1)*limit,limit));
        return orderVO;
    }

    @PutMapping("/updateState/{id}/{state}/{aid}")
    public void updateState(@PathVariable("id") long id, @PathVariable("state") int state, @PathVariable("aid") long aid){
        orderRepository.updateState(id,aid,state);
    }

}
</code></pre>
<p>10. 依次启动注册中心、configserver、OrderApplication，使用 Postman 测试该服务的相关接口，如图所示。</p>
<p><img src="https://images.gitbook.cn/67419cf0-dd56-11e9-a584-59c5758c1abc" alt="1" /></p>
<p><img src="https://images.gitbook.cn/764dffe0-dd56-11e9-9cc8-a572519b0723" alt="2" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了项目实战 order 模块的搭建，作为一个服务提供者，order 为整个系统提供订单服务，包括添加订单、查询订单、删除订单、处理订单。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请单击这里下载源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>