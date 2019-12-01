---
title: 案例上手 Spring 全家桶-44
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们介绍了安装启动 Redis 的具体操作，这节课我们来学习如何用 Spring Boot 集成 Redis。</p>
<p>实际上 Spring Boot 是通过整合 Spring Data Redis 来实现对 Redis 的管理的，就像我们在前面的课程中通过 Spring Data JPA 完成 Spring Boot 与 MySQL 数据库的整合，所以我们要搞清楚一个概念，并不是 Spring Boot 来直接操作数据库的，Spring Boot 只是提供了一系列开箱即用的模块，开发者可以通过 Spring Boot 快速将需要的模块整合到项目中，所以真正管理数据库的是 Spring Data JPA 或者 Spring Data Redis。</p>
<p>1. 创建 Maven 工程，pom.xml 中添加相关依赖，spring-boot-starter-data-redis 为 Spring Boot 整合 Spring Data Redis 的依赖，Spring Boot 2.x 默认使用 Lettuce 客户端来操作 Redis，所以我们还需要引入 commons-pool2 使得 Lettuce 可以创建 Redis 数据连接池。</p>
<pre><code class="xml language-xml">&lt;parent&gt;
  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
  &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
  &lt;version&gt;2.1.5.RELEASE&lt;/version&gt;
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
    &lt;groupId&gt;org.apache.commons&lt;/groupId&gt;
    &lt;artifactId&gt;commons-pool2&lt;/artifactId&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
    &lt;artifactId&gt;lombok&lt;/artifactId&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 创建实体类 Student。</p>
<pre><code class="java language-java">@Data
@AllArgsConstructor
public class Student implements Serializable {
    private Long id;
    private String name;
    private Double score;
    private Date birthday;
}
</code></pre>
<p>注意实体类必须实现序列化接口，否则在存储数据时会抛出如下异常。</p>
<p><img src="https://images.gitbook.cn/b57c4d10-c7ae-11e9-9db6-1dc435f9b961" alt="WX20190617-093025@2x" /></p>
<p>3. 创建 StudentHandler。</p>
<pre><code class="java language-java">@RestController
public class StudentHandler {

    @Autowired
    private RedisTemplate redisTemplate;

    @PostMapping("/set")
    public void set(@RequestBody Student student){
        redisTemplate.opsForValue().set("stu",student);
    }

    @GetMapping("/get/{key}")
    public Student get(@PathVariable("key") String key){
        Student student = (Student) redisTemplate.opsForValue().get(key);
        return student;
    }

    @DeleteMapping("/delete/{key}")
    public boolean delete(@PathVariable("key") String key){
        redisTemplate.delete(key);
        return redisTemplate.hasKey(key);
    }

}
</code></pre>
<p>4. 创建配置文件 application.yml。</p>
<pre><code class="yaml language-yaml">spring:
  redis:
    database: 0
    host: localhost
    port: 6379
</code></pre>
<p>5. 创建启动类 Application。</p>
<pre><code class="java language-java">package com.southwind;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
</code></pre>
<p>6. 启动 Application，使用 Postman 工具来测试相关接口。</p>
<ul>
<li>set</li>
</ul>
<p><img src="https://images.gitbook.cn/29605ad0-c75c-11e9-99c1-c37abd23c4b1" width = "75%" /></p>
<ul>
<li>get</li>
</ul>
<p><img src="https://images.gitbook.cn/3de8b3d0-c75c-11e9-a5ba-f1eeeb548c06" width = "75%" /></p>
<p>已经成功将 Student 存入 Redis 数据库，但是如果在 Redis 客户端通过命令来查询，发现结果为空。</p>
<p><img src="https://images.gitbook.cn/4b2a8ff0-c75c-11e9-9ae4-c3d609c8bfbd" width = "60%" /></p>
<p>这就出现问题了，直接用命令行 stu 查不到数据，但是使用 RedisTemplate 却可以查到，原因是使用  RedisTemplate 在存数据的时候，key 没做序列化，所以实际存入 Redis 的 key 值并不是 stu，客户端当然是查不到数据的，那 Redis 的 key 值是什么呢？如果 RedisTemplate 没做 key 的序列化处理，实际存入 Redis 的 key 前面会多几个字符，可以通过命令查看真实 key 值。</p>
<p><img src="https://images.gitbook.cn/d325af50-c7ae-11e9-9db6-1dc435f9b961" width = "60%" /></p>
<p>可以看到 "\xac\xed\x00\x05t\x00\x03stu" 才是 Redis 中存入的 key 值，在 stu 前面添加了几个字符串，通过真实 key 值是可以查到数据的，如下所示。</p>
<p><img src="https://images.gitbook.cn/5f7850f0-c75c-11e9-9ae4-c3d609c8bfbd" width = "60%" /></p>
<p>直接使用 RedisTemplate 查询的时候，会自动将 stu 转为 "\xac\xed\x00\x05t\x00\x03stu"，所以是可以直接查到数据的。</p>
<ul>
<li>delete</li>
</ul>
<p><img src="https://images.gitbook.cn/701c91f0-c75c-11e9-a81a-91f9bfe6443e" width = "65%" /></p>
<p>删除成功之后，再次查询，可以看到数据已经删除成功，如下所示。</p>
<p><img src="https://images.gitbook.cn/7b64e800-c75c-11e9-a81a-91f9bfe6443e" width = "65%" /></p>
<p>Redis 支持的数据类型有 5 种，分别是字符串、列表、集合、有序集合、哈希，接下来分别演示 RedisTemplate 对这 5 种类型的支持。</p>
<ul>
<li>字符串</li>
</ul>
<pre><code class="java language-java">@GetMapping("/string")
public void stringTest(){
  redisTemplate.opsForValue().set("str","Hello World");
  System.out.println(redisTemplate.opsForValue().get("str"));
}
</code></pre>
<p>存入 key 为 "str"，value 为 "Hello World" 的数据，再通过 key 取出数据，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/e622ad60-c7ae-11e9-99b2-43dda19383ed" width = "60%" /></p>
<p>同时在 Redis 客户端查询当前所有的 key 值，结果如下所示，数据已经成功存入 Redis。</p>
<p><img src="https://images.gitbook.cn/96ab5400-c75c-11e9-99c1-c37abd23c4b1" width = "50%" /></p>
<ul>
<li>列表</li>
</ul>
<p>这里说的列表就是 List。</p>
<pre><code class="java language-java">@GetMapping("/list")
public void listTest(){
  ListOperations&lt;String,String&gt; list = redisTemplate.opsForList();
  list.leftPush("list","Hello");
  list.leftPush("list","World");
  list.leftPush("list","Java");
  List&lt;String&gt; getList = list.range("list",0,2);
  for (String val:getList){
    System.out.println(val);
  }
}
</code></pre>
<p>获取 ListOperations 对象，存入三个 key 为 "list"，值分别为 "Hello"、"World"、"Java" 的数据，再遍历取出，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/ab12de90-c75c-11e9-a81a-91f9bfe6443e" width = "70%" /></p>
<p>同时在 Redis 客户端查询当前所有的 key 值，结果如下所示，数据已经成功存入 Redis。</p>
<p><img src="https://images.gitbook.cn/b7df1580-c75c-11e9-a5ba-f1eeeb548c06" width = "50%" /></p>
<ul>
<li>集合</li>
</ul>
<pre><code class="java language-java">@GetMapping("/set")
public void setTest(){
  SetOperations&lt;String,String&gt; set = redisTemplate.opsForSet();
  set.add("set","Hello");
  set.add("set","Hello");
  set.add("set","World");
  set.add("set","World");
  set.add("set","Java");
  set.add("set","Java");
  Set&lt;String&gt; getSet = set.members("set");
  for (String val:getSet){
    System.out.println(val);
  }
}
</code></pre>
<p>获取 SetOperations 对象，存入两次 "Hello"、"World"、"Java"，且 key 值都为 "set"，我们知道 Set 值是唯一的，所以重复数据只保存一次，遍历取出，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/f4d5ccc0-c7ae-11e9-a81a-91f9bfe6443e" width = "70%" /></p>
<p>同时在 Redis 客户端查询当前所有的 key 值，结果如下所示，数据已经成功存入 Redis。</p>
<p><img src="https://images.gitbook.cn/cbbadad0-c75c-11e9-a5ba-f1eeeb548c06" width = "70%" /></p>
<ul>
<li>有序集合 </li>
</ul>
<pre><code class="java language-java">@GetMapping("/zset")
public void zsetTest(){
    ZSetOperations&lt;String,String&gt; zset = redisTemplate.opsForZSet();
    zset.add("zset","Hello",1);
    zset.add("zset","World",2);
    zset.add("zset","Java",3);
    Set&lt;String&gt; set = zset.range("zset",0,2);
    for(String val:set){
        System.out.println(val);
    }
}
</code></pre>
<p>ZSetOperations 的用法与 SetOperations 类似，区别在于 ZSetOperations 是有序的，在存入数据时，除了 key 和 value 还需额外传入一个 double 的参数 var3 来为数据排序，存储完成之后再遍历取出，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/93019070-c75d-11e9-a5ba-f1eeeb548c06" width = "70%" /></p>
<p>通过结果可以看到数据是按照 var3 的值递增排序的，同时在 Redis 客户端查询当前所有的 key 值，结果如下所示，数据已经成功存入 Redis。</p>
<p><img src="https://images.gitbook.cn/9fe6a690-c75d-11e9-a5ba-f1eeeb548c06" width = "70%" /></p>
<ul>
<li>哈希</li>
</ul>
<p>我们在使用 HashMap 存储数据的时候只需要传入 key 和 value 两个参数，但是 HashOperations 存入数据缺需要三个参数 key、hashkey、value，value 是具体的数据，那么 key 和 hashkey 是什么关系呢？</p>
<p>key 可以理解为每组数据的 ID，hashkey 和 value 是一组完整的数据，通过 key 来区分不同的 HashMap，比如有下列代码。</p>
<pre><code class="java language-java">HashMap hashMap1 = new HashMap();
hashMap1.put(key1,value1);
HashMap hashMap2 = new HashMap();
hashMap2.put(key2,value2);
HashOperations&lt;String,String,String&gt; hash = redisTemplate.opsForHash();
hash.put(hashMap1,key1,value1);
hash.put(hashMap2,key2,value2);
</code></pre>
<p>hashMap1 和 hashMap2 就是 key，key1 和 key2 就是 hashkey，value1 和 value2 就是 value。</p>
<p>理解了 HashOperations 的使用，具体代码如下。</p>
<pre><code class="java language-java">@GetMapping("/hash")
public void hashTest(){
  HashOperations&lt;String,String,String&gt; hash = redisTemplate.opsForHash();
  hash.put("key","hashkey","Hello");
  System.out.println(hash.get("key","hashkey"));
}
</code></pre>
<p>存入 "key"、"hashkey"、"Hello" 之后再取出数据，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/c5c24540-c75d-11e9-9ae4-c3d609c8bfbd" width = "70%" /></p>
<p>同时在 Redis 客户端查询当前所有的 key 值，结果如下所示，数据已经成功存入 Redis。</p>
<p><img src="https://images.gitbook.cn/cfc08f20-c75d-11e9-a81a-91f9bfe6443e" width = "60%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring Boot 与 Redis 的集成，具体是通过整合 Spring Data Redis 来完成对 Redis 的管理，Spring Data Redis 为开发者提供 RedisTemplate 组件，通过调用 RedisTemplate 的相关方法，可以分别完成对字符串、列表、集合、有序集合、哈希类型数据的管理。</p>
<p><a href="https://github.com/southwind9801/gcspringbootredis.git">请点击这里查看源码</a></p>
<p><a href="https://pan.baidu.com/s/1K2cNTk6JmZa50RYSKwvwGA">点击这里获取 Spring Boot 视频专题</a>，提取码：e4wc</p></div></article>