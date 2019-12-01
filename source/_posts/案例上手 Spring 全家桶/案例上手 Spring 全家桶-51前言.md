---
title: 案例上手 Spring 全家桶-51
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课说到 Eureka Server 是注册中心，分布式系统架构中的所有微服务都需要在注册中心完成注册才能被发现进而使用，我们所说的服务提供者和服务消费者是从业务角度来划分的，实际上服务提供者和服务消费者都是通过 Eureka Client 连接到 Eureka Server 完成注册，本节课我们就来一起实现一个服务提供者，并且在 Eureka Server 完成注册，大致思路是先通过 Spring Boot 搭建一个微服务应用，再通过 Eureka Client 将其注册到 Eureka Server，创建 Eureka Client 的过程与创建 Eureka Server 十分相似，如下所示。</p>
<p>1. 在父工程下创建 Module，实现 Eureka Client。</p>
<p><img src="https://images.gitbook.cn/6fa73340-cce0-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p>2. 输入 ArtifactId，点击 Next。</p>
<p><img src="https://images.gitbook.cn/77d1f5a0-cce0-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p>3. 设置工程名和工程存放路径，点击 Finish。</p>
<p><img src="https://images.gitbook.cn/7f2b8550-cce0-11e9-9f23-07a3e2a236db" width = "70%" /></p>
<p>4. 在 pom.xml 中添加 Eureka Client 依赖。</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;
        &lt;artifactId&gt;spring-cloud-starter-netflix-eureka-client&lt;/artifactId&gt;
    &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>5. 在 resources 路径下创建配置文件 application.yml，添加 Eureka Client 相关配置，此时的 Eureka Client 是服务提供者 provider。</p>
<pre><code class="yaml language-yaml">server:
  port: 8010
spring:
  application:
    name: provider
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
<p>6. 在 Java 路径下创建启动类 ProviderApplication。</p>
<pre><code class="java language-java">@SpringBootApplication
public class ProviderApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProviderApplication.class,args);
    }
}
</code></pre>
<p>注解说明：</p>
<ul>
<li>@SpringBootApplication：声明该类是 Spring Boot 服务的入口。</li>
</ul>
<p>7. 依次启动注册中心，ProviderApplication，启动成功控制台输出如下信息。</p>
<p><img src="https://images.gitbook.cn/a1433e30-cce0-11e9-beb5-a53251e30de8" alt="4" /></p>
<p>8. 打开浏览器，访问 http://localhost:8761，看到如下界面。</p>
<p><img src="https://images.gitbook.cn/a886add0-cce0-11e9-9a11-bbb3551196dc" alt="5" /></p>
<p>可以看到服务提供者 provider 已经在 Eureka Server 完成注册，接下来就可以访问 provider 提供的相关服务了，我们在 provider 服务中提供对 Student 的 CRUD 操作。</p>
<p>9. 在 Java 路径下创建实体类 Student，使用 Lombok 来简化实体类代码的编写。</p>
<p>首先在 pom.xml 中引入 Lombok 相关依赖，在当前 Module 或父工程的 pom.xml 中添加均可，建议添加到父工程中，因为其他服务也会用到 Lombok，避免重复添加。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
    &lt;artifactId&gt;lombok&lt;/artifactId&gt;
    &lt;optional&gt;true&lt;/optional&gt;
&lt;/dependency&gt;
</code></pre>
<p>10. 使用 Lombok 需要预先在 IDE 中安装 Lombok 插件，我们以 IDEA 为例，安装步骤如下图所示。</p>
<p><img src="https://images.gitbook.cn/ed4e19d0-cce0-11e9-beb5-a53251e30de8" width = "70%" /></p>
<p>11. 安装完毕，创建 Student 类。</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
@NoArgsConstructor
public class Student {
    private long id;
    private String name;
    private char gender;
}
</code></pre>
<p>12. 创建管理 Student 对象的接口 StudentRepositoy 及其实现类 StudentRepositoryImpl。</p>
<p>StudentRepositoy</p>
<pre><code class="java language-java">public interface StudentRepository {
    public Collection&lt;Student&gt; findAll();
    public Student findById(long id);
    public void saveOrUpdate(Student student);
    public void deleteById(long id);
}
</code></pre>
<p>StudentRepositoryImpl</p>
<pre><code class="java language-java">@Repository
public class StudentRepositoryImpl implements StudentRepository {

    private Map&lt;Long,Student&gt; studentMap;

    public StudentRepositoryImpl(){
        studentMap = new HashMap&lt;&gt;();
        studentMap.put(1L,new Student(1L,"张三",'男'));
        studentMap.put(2L,new Student(2L,"李四",'女'));
        studentMap.put(3L,new Student(3L,"王五",'男'));
    }

    @Override
    public Collection&lt;Student&gt; findAll() {
        return studentMap.values();
    }

    @Override
    public Student findById(long id) {
        return studentMap.get(id);
    }

    @Override
    public void saveOrUpdate(Student student) {
        studentMap.put(student.getId(),student);
    }

    @Override
    public void deleteById(long id) {
        studentMap.remove(id);
    }
}
</code></pre>
<p>13. 创建 StudentHandler，通过 @Autowired 注解将 StudentRepository 的实例注入 StudentHandler。</p>
<pre><code class="java language-java">@RequestMapping("/student")
@RestController
public class StudentHandler {

    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("/findAll")
    public Collection&lt;Student&gt; findAll(){
        return studentRepository.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id") long id){
        return studentRepository.findById(id);
    }

    @PostMapping("/save")
    public void save(@RequestBody Student student){
        studentRepository.saveOrUpdate(student);
    }

    @PutMapping("/update")
    public void update(@RequestBody Student student){
        studentRepository.saveOrUpdate(student);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        studentRepository.deleteById(id);
    }
}
</code></pre>
<p>14. 重启 ProviderApplication，通过 Postman 工具测试该服务的相关接口。</p>
<ul>
<li>findAll 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/fefd1410-cce0-11e9-9f23-07a3e2a236db" alt="7" /></p>
<ul>
<li>findById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/06e4b2f0-cce1-11e9-9a11-bbb3551196dc" alt="8" /></p>
<ul>
<li>save 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/0dbcdda0-cce1-11e9-beb5-a53251e30de8" alt="9" /></p>
<p>添加完成之后再来查询，调用 findAll 接口，可以看到新数据已经添加成功。</p>
<p><img src="https://images.gitbook.cn/19fd9d70-cce1-11e9-9a11-bbb3551196dc" alt="10" /></p>
<ul>
<li>update 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/20b65940-cce1-11e9-9f23-07a3e2a236db" alt="11" /></p>
<p>修改完成之后再来查询，调用 findAll 接口，可以看到修改之后的数据。</p>
<p><img src="https://images.gitbook.cn/292f1490-cce1-11e9-beb5-a53251e30de8" alt="12" /></p>
<ul>
<li>deleteById 接口</li>
</ul>
<p><img src="https://images.gitbook.cn/30a86140-cce1-11e9-8d89-4fa271cb1633" alt="13" /></p>
<p>删除完成之后再来查询，调用 findAll 接口，可以看到数据已经被删除。</p>
<p><img src="https://images.gitbook.cn/397caa10-cce1-11e9-9a11-bbb3551196dc" alt="7" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了使用 Eureka Client 组件来注册一个服务提供者 provider 的具体实现，不同业务需求下的微服务统一使用 Eureka Client 组件进行注册，我们现在已经实现了一个服务提供者，其他微服务就可以调用它的接口来完成相关业务需求了。</p>
<p><a href="https://github.com/southwind9801/myspringclouddemo.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1P_3n6KnPdWBFnlAtEdTm2g">点击这里获取 Spring Cloud 视频专题</a>，提取码：yfq2</p></div></article>