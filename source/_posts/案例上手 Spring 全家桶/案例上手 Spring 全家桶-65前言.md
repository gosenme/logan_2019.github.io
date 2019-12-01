---
title: 案例上手 Spring 全家桶-65
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本节课我们来实现服务提供者 menu，menu 为系统提供菜品相关服务，包括添加菜品、查询菜品、修改菜品、删除菜品，具体实现如下所示。</p>
<p>1. 在父工程下创建一个 Module，命名为 menu，pom.xml 添加相关依赖，menu 需要访问数据库，因此集成 MyBatis 相关依赖，配置文件从 Git 仓库拉取，添加配置中心 Spring Cloud Config 相关依赖。</p>
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
      name: menu #对应的配置文件名称
      label: master #Git 仓库分支名
      discovery:
        enabled: true
        serviceId: configserver #连接的配置中心名称
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
</code></pre>
<p>3. 在 java 目录下创建启动类 MenuApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
@MapperScan("com.southwind.repository")
public class MenuApplication {
    public static void main(String[] args) {
        SpringApplication.run(MenuApplication.class,args);
    }
}
</code></pre>
<p>4. 接下来为服务提供者 menu 集成 MyBatis 环境，首先在 Git 仓库配置文件 menu.yml 中添加相关信息。</p>
<pre><code class="yaml language-yaml">server:
  port: 8020
spring:
  application:
    name: menu
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
<p>5. 在 java 目录下创建 entity 文件夹，新建 Menu 类对应数据表 t_menu。</p>
<pre><code class="java language-java">@Data
public class Menu {
    private long id;
    private String name;
    private double price;
    private String flavor;
    private Type type;
}
</code></pre>
<p>6. 新建 MenuVO 类为 layui 框架提供封装类。</p>
<pre><code class="java language-java">@Data
public class MenuVO {
    private int code;
    private String msg;
    private int count;
    private List&lt;Menu&gt; data;
}
</code></pre>
<p>7. 新建 Type 类对应数据表 t_type。</p>
<pre><code class="java language-java">@Data
public class Type {
    private long id;
    private String name;
}
</code></pre>
<p>8. 在 java 目录下创建 repository 文件夹，新建 MenuRepository 接口，定义相关业务方法。</p>
<pre><code class="java language-java">public interface MenuRepository {
    public List&lt;Menu&gt; findAll(int index,int limit);
    public int count();
    public void save(Menu menu);
    public Menu findById(long id);
    public void update(Menu menu);
    public void deleteById(long id);
}
</code></pre>
<p>9. 新建 TypeRepository 接口，定义相关业务方法。</p>
<pre><code class="java language-java">public interface TypeRepository {
    public List&lt;Type&gt; findAll();
}
</code></pre>
<p>10. 在 resources 目录下创建 mapping 文件夹，存放 Mapper.xml，新建 MenuRepository.xml，编写 MenuRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.MenuRepository"&gt;
    &lt;resultMap id="menuMap" type="Menu"&gt;
        &lt;id property="id" column="mid"/&gt;
        &lt;result property="name" column="mname"/&gt;
        &lt;result property="author" column="author"/&gt;
        &lt;result property="price" column="price"/&gt;
        &lt;result property="flavor" column="flavor"/&gt;
        &lt;!-- 映射 type --&gt;
        &lt;association property="type" javaType="Type"&gt;
            &lt;id property="id" column="tid"/&gt;
            &lt;result property="name" column="tname"/&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt;

    &lt;select id="findAll" resultMap="menuMap"&gt;
        select m.id mid,m.name mname,m.price,m.flavor,t.id tid,t.name tname from t_menu m,t_type t where m.tid = t.id order by mid limit #{param1},#{param2}
    &lt;/select&gt;

    &lt;select id="count" resultType="int"&gt;
        select count(*) from t_menu;
    &lt;/select&gt;

    &lt;insert id="save" parameterType="Menu"&gt;
        insert into t_menu(name,price,flavor,tid) values(#{name},#{price},#{flavor},#{type.id})
    &lt;/insert&gt;

    &lt;select id="findById" resultMap="menuMap"&gt;
        select id mid,name mname,price,flavor,tid from t_menu where id = #{id}
    &lt;/select&gt;

    &lt;update id="update" parameterType="Menu"&gt;
        update t_menu set name = #{name},price = #{price},flavor = #{flavor},tid = #{type.id} where id = #{id}
    &lt;/update&gt;

    &lt;delete id="deleteById" parameterType="long"&gt;
        delete from t_menu where id = #{id}
    &lt;/delete&gt;
&lt;/mapper&gt;
</code></pre>
<p>11. 新建 TypeRepository.xml，编写 TypeRepository 接口方法对应的 SQL。</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.TypeRepository"&gt;
    &lt;select id="findAll" resultType="Type"&gt;
        select * from t_type
    &lt;/select&gt;
&lt;/mapper&gt;
</code></pre>
<p>12. 新建 MenuHandler，将 MenuRepository 通过 @Autowired 注解进行注入，完成相关业务逻辑。</p>
<pre><code class="java language-java">@RestController
@RequestMapping("/menu")
public class MenuHandler {

    @Autowired
    private MenuRepository menuRepository;
    @Autowired
    private TypeRepository typeRepository;

    @GetMapping("/findAll/{page}/{limit}")
    public MenuVO findAll(@PathVariable("page") int page, @PathVariable("limit") int limit){
        MenuVO menuVO = new MenuVO();
        menuVO.setCode(0);
        menuVO.setMsg("");
        menuVO.setCount(menuRepository.count());
        menuVO.setData(menuRepository.findAll((page-1)*limit,limit));
        return menuVO;
    }

    @GetMapping("/findAll")
    public List&lt;Type&gt; findAll(){
        return typeRepository.findAll();
    }

    @PostMapping("/save")
    public void save(@RequestBody Menu menu){
        menuRepository.save(menu);
    }

    @GetMapping("/findById/{id}")
    public Menu findById(@PathVariable("id") long id){
        return menuRepository.findById(id);
    }

    @PutMapping("/update")
    public void update(@RequestBody Menu menu){
        menuRepository.update(menu);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        menuRepository.deleteById(id);
    }
}
</code></pre>
<p>13. 依次启动注册中心、configserver、MenuApplication，使用 Postman 测试该服务的相关接口，如图所示。</p>
<p><img src="https://images.gitbook.cn/f89a9630-dd55-11e9-9cc8-a572519b0723" alt="1" /></p>
<p><img src="https://images.gitbook.cn/feb53d40-dd55-11e9-8134-9900814ad853" alt="2" /></p>
<p><img src="https://images.gitbook.cn/04d38dd0-dd56-11e9-8134-9900814ad853" alt="3" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了项目实战 menu 模块的搭建，作为一个服务提供者，menu 为整个系统提供菜品服务，包括添加菜品、查询菜品、修改菜品、删除菜品。</p>
<p><a href="https://github.com/southwind9801/orderingsystem.git">请单击这里下载源码</a></p>
<p><a href="https://pan.baidu.com/s/1eheDU4XoN3BKuzocyIe0oA">微服务项目实战视频链接请点击这里获取</a>，提取码：bfps</p></div></article>