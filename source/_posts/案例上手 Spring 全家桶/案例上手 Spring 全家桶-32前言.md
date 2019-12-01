---
title: 案例上手 Spring 全家桶-32
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>前面的课程中我们学习了如何搭建 MongoDB 数据库以及基本操作，实际开发中我们需要结合框架来完成对数据库的访问和管理，所以本节课我们就来学习管理 MongoDB 的企业级框架。</p>
<p>Spring Data MongoDB 是 Spring Framework 家族中的一员，是 Spring Data 专门针对 MongoDB 设计的子模块，使用它可以非常方便的管理 MongoDB，甚至无需开发者手动编写具体的访问命令，Spring Data MongoDB 提供了一套基于 DAO 的接口，开发者直接调用接口即可完成对 MongoDB 的访问。</p>
<p>同时 Spring Data MongoDB 还提供了一个 MongoTemplate 组件，该组件封装了访问 MongoDB 的常用方法，本节课我们就一起来学习 MongoTemplate 的使用。</p>
<p>1. 创建 Maven 工程，pom.xml 添加依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.data&lt;/groupId&gt;
    &lt;artifactId&gt;spring-data-mongodb&lt;/artifactId&gt;
    &lt;version&gt;2.0.8.RELEASE&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>2. 配置 spring.xml。</p>
<pre><code class="xml language-xml">&lt;!-- Spring 连接 MongoDB 客户端配置 --&gt;
&lt;mongo:mongo-client host="127.0.0.1" port="12345" id="mongo"/&gt;

&lt;!-- 配置 MongoDB 目标数据库 --&gt;
&lt;mongo:db-factory dbname="testdb" mongo-ref="mongo" /&gt;

&lt;!-- 配置 MongoTemplate --&gt;
&lt;bean id="mongoTemplate" class="org.springframework.data.mongodb.core.MongoTemplate"&gt;
  &lt;constructor-arg name="mongoDbFactory" ref="mongoDbFactory"/&gt;
&lt;/bean&gt;
</code></pre>
<p>3. 创建实体类，通过注解于 MongoDB 集合进行映射。</p>
<ul>
<li>@Document：设置实体类与 MongoDB 集合的映射，value 指定集合名，可以省略，默认取首字母小写之后的类名作为集合名。</li>
<li>@Id：设置实体类标识符属性与集合主键的映射。</li>
<li>@Field：设置实体类普通属性与集合字段的映射，value 可以指定字段名，可以省略，默认取对应的属性名作为字段名。</li>
</ul>
<pre><code class="java language-java">@Document(collection="student_info")
public class Student {
    @Id
    private String id;
    @Field
    private String name;
    @Field
    private int age;
    @Field(value="a_time")
    private Date addTime;
}
</code></pre>
<p>4. 测试类中调用 MongoTemplate 接口完成业务操作。</p>
<ul>
<li>新增</li>
</ul>
<pre><code class="java language-java">public class StudentTest {
    private static MongoTemplate mongoTemplate;
    static {
        //实例化 mongoTemplate
        mongoTemplate = (MongoTemplate) new ClassPathXmlApplicationContext("classpath:spring.xml").getBean("mongoTemplate");
    }

    public static void main(String[] args) {
        insert();
    }

    public static void insert() {
        List&lt;Student&gt; list = new ArrayList&lt;Student&gt;();
        for (int i = 0; i &lt; 10; i++) {
            Student student = new Student();
            student.setName("张三"+i);
            student.setAge(16+i);
            student.setAddTime(new Date());
            list.add(student);
        }
        mongoTemplate.insert(list, Student.class);
    }
}
</code></pre>
<p>打开终端，命令行查询结果。</p>
<p><img src="https://images.gitbook.cn/730781e0-9ada-11e8-831e-0180aea56660" width = "70%" /></p>
<p>添加成功。</p>
<ul>
<li>删除</li>
</ul>
<p>条件删除：</p>
<pre><code class="java language-java">mongoTemplate.remove(Query.query(
    new Criteria("name").is("张三0")), Student.class);
</code></pre>
<p>Query.query(new Criteria("name").is("张三0")) 指定删除条件。</p>
<p>执行完成，再次查询，“张三0”成功删除。</p>
<p><img src="https://images.gitbook.cn/f38926c0-9ada-11e8-a178-519d5b470954" width = "60%" /></p>
<p>删除并返回：</p>
<pre><code class="java language-java">Student student =  mongoTemplate.findAndRemove(
        Query.query(new Criteria("name").is("张三2")), 
        Student.class);
System.out.println(student);
</code></pre>
<p><img src="https://images.gitbook.cn/c3af6540-9ada-11e8-831e-0180aea56660" width = "70%" /></p>
<p>删除多条并返回集合：</p>
<pre><code class="java language-java">List&lt;Student&gt; students =  mongoTemplate.findAllAndRemove(
            Query.query(new Criteria("age").is(19)), 
            Student.class);
System.out.println(students);
</code></pre>
<p><img src="https://images.gitbook.cn/98b6e070-9ada-11e8-831e-0180aea56660" width = "80%" /></p>
<p>删除集合：</p>
<pre><code class="java language-java">mongoTemplate.dropCollection(Student.class);
</code></pre>
<p><img src="https://images.gitbook.cn/18720100-9adb-11e8-b37c-dd4feba3837e" width = "70%" /></p>
<p>删库：</p>
<pre><code class="java language-java">mongoTemplate.getDb().drop();
</code></pre>
<p><img src="https://images.gitbook.cn/237cd8e0-9adb-11e8-831e-0180aea56660" width = "70%" /></p>
<p>删除之后查询，testdb 库已经不存在。</p>
<ul>
<li>修改</li>
</ul>
<p>调用 updateFirst 完成，updateFirst 提供了两个方法重载，分别将实体类的运行时类和集合名作为参数传入。</p>
<p>实体类运行时类名：</p>
<p>update 方法的参数与实体类属性名对应。</p>
<pre><code class="java language-java">mongoTemplate.updateFirst(Query.query(
    new Criteria("name").is("张三5")), 
    Update.update("addTime", new Date()).update("age", 33), Student.class);
</code></pre>
<p><img src="https://images.gitbook.cn/3928a340-9adb-11e8-a178-519d5b470954" width = "70%" /></p>
<p>集合名：</p>
<p>update 方法的参数与集合字段名对应。</p>
<pre><code class="java language-java">mongoTemplate.updateFirst(Query.query(
    new Criteria("name").is("张三6")),
    Update.update("a_time", new Date()).update("age", 36), "student_info");
</code></pre>
<p><img src="https://images.gitbook.cn/484029c0-9adb-11e8-a178-519d5b470954" width = "70%" /></p>
<p>若被修改的对象不存在，可以使用 upsert 接口，先添加对象，再进行修改。</p>
<pre><code class="java language-java">mongoTemplate.upsert(Query.query(
    new Criteria("name").is("张三11")), 
    Update.update("age", 11), Student.class);
</code></pre>
<p><img src="https://images.gitbook.cn/5ea950b0-9adb-11e8-831e-0180aea56660" width = "70%" /></p>
<ul>
<li>查询</li>
</ul>
<p>查询所有记录：</p>
<pre><code class="java language-java">List&lt;Student&gt; list = mongoTemplate.findAll(Student.class);
for (Student stu : list) {
    System.out.println(stu);
}
</code></pre>
<p><img src="https://images.gitbook.cn/73b4bc60-9adb-11e8-831e-0180aea56660" width = "70%" /></p>
<p>查询满足条件的记录数：</p>
<pre><code class="java language-java">long count = mongoTemplate.count(Query.query(
     new Criteria("age").is(18)), Student.class);
System.out.println(count);
</code></pre>
<p><img src="https://images.gitbook.cn/7e7a9c00-9adb-11e8-831e-0180aea56660" width = "70%" /></p>
<p><img src="https://images.gitbook.cn/88bea170-9adb-11e8-831e-0180aea56660" width = "60%" /></p>
<p>查询所有满足条件的记录：</p>
<pre><code class="java language-java">List&lt;Student&gt; list2 = mongoTemplate.find(Query.query(
            new Criteria("age").is(18)), Student.class);
for (Student stu : list2) {
    System.out.println(stu);
}
</code></pre>
<p><img src="https://images.gitbook.cn/959d00d0-9adb-11e8-831e-0180aea56660" width = "65%" /></p>
<p>查询满足条件的第一条记录：</p>
<pre><code class="java language-java">Student student = mongoTemplate.findOne(Query.query(
        new Criteria("age").is(18)), Student.class);
System.out.println(student);
</code></pre>
<p><img src="https://images.gitbook.cn/a60aef90-9adb-11e8-8cbe-ad3f3badcc18" width = "75%" /></p>
<p>分页查询，去掉第 1 条，取 2 条：</p>
<pre><code class="java language-java">List&lt;Student&gt; list3 = mongoTemplate.find(Query.query(
            new Criteria("age").is(18)).skip(1).limit(2), 
            Student.class);
for (Student stu : list3) {
    System.out.println(stu);
}
</code></pre>
<p><img src="https://images.gitbook.cn/b40c7230-9adb-11e8-a178-519d5b470954" width = "70%" /></p>
<p>根据 ID 查询：</p>
<pre><code class="java language-java">Student student2 = mongoTemplate.findById(
        new ObjectId("5b62c6f55a41f60d93ffe6c2"), 
        Student.class);
System.out.println(student2);
</code></pre>
<p><img src="https://images.gitbook.cn/c18e6490-9adb-11e8-8cbe-ad3f3badcc18" width = "70%" /></p>
<p>in 查询：</p>
<pre><code class="java language-java">List&lt;Student&gt; list4 = mongoTemplate.find(Query.query(
            new Criteria("age").in(18,19)), Student.class);
for (Student stu : list4) {
    System.out.println(stu);
}
</code></pre>
<p><img src="https://images.gitbook.cn/d697d470-9adb-11e8-b37c-dd4feba3837e" width = "70%" /></p>
<p>or 查询：</p>
<pre><code class="java language-java">List&lt;Student&gt; list5 = mongoTemplate.find(Query.query(new Criteria().orOperator(
                    new Criteria("age").is(18),
                    new Criteria("age").is(19)
                )),
                Student.class);
for (Student stu : list5) {
    System.out.println(stu);
}
</code></pre>
<p><img src="https://images.gitbook.cn/ed0e1ac0-9adb-11e8-a178-519d5b470954" width = "70%" /></p>
<p>and 查询：</p>
<pre><code class="java language-java">Student student3 = mongoTemplate.findOne(Query.query(new Criteria().andOperator(
                 new Criteria("age").is(18),
                 new Criteria("name").is("张三1")
             )), Student.class);
System.out.println(student3);
</code></pre>
<p><img src="https://images.gitbook.cn/f8972350-9adb-11e8-8cbe-ad3f3badcc18" width = "75%" /></p>
<p>CRUD 基本操作全部完成。</p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了如何使用 Spring Data 框架对 MongoDB 数据库进行管理，Spring Data 是 Spring 框架体系中的另外一款产品，与 Spring MVC 师出同门，因此可以做到很好的整合开发，同时还讲解了如何使用 Spring Data 的 MongoTemplate 组件完成开发。</p>
<h3 id="-2">源码</h3>
<p><a href="https://github.com/southwind9801/springdata_mongotemplate.git">请点击这里查看源码</a></p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc-dataconverter.git">请单击这里下载源码</a></p></div></article>