---
title: 案例上手 Spring 全家桶-26
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们学习了 MyBatis 延迟加载，可以有效减少 Java 程序与数据库的交互次数，从而提高程序的运行效率，但是延迟加载的功能并不全面，它只能在做级联查询的时候提高效率，如果现在的需求就是单表查询，那么延迟加载就无法满足需求了。不用担心，MyBatis 同样为我们提供了这种业务场景下的解决方案，即缓存。</p>
<p>使用缓存的作用也是减少 Java 应用程序与数据库的交互次数，从而提升程序的运行效率。比如第一次查询出某个对象之后，MyBatis 会自动将其存入缓存，当下一次查询同一个对象时，就可以直接从缓存中获取，不必再次访问数据库了，如下图所示。</p>
<p><img src="https://images.gitbook.cn/0925eaa0-b68b-11e9-9778-7bbd052235e6" alt="enter image description here" /></p>
<p>MyBatis 有两种缓存：一级缓存和二级缓存。</p>
<p>MyBatis 自带一级缓存，并且是无法关闭的，一直存在，一级缓存的数据存储在 SqlSession 中，即它的作用域是同一个 SqlSession，当使用同一个 SqlSession 对象执行查询的时候，第一次的执行结果会自动存入 SqlSession 缓存，第二次查询时可以直接从缓存中获取。</p>
<p>但是如果是两个 SqlSession 查询两次同样的 SQL，一级缓存不会生效，需要访问两次数据库。</p>
<p>同时需要注意，为了保证数据的一致性，如果 SqlSession 执行了增加、删除，修改操作，MyBatis 会自动清空 SqlSession 缓存中存储的数据。</p>
<p>一级缓存不需要进行任何配置，可以直接使用。</p>
<p>MyBatis 二级缓存是比一级缓存作用域更大的缓存机制，它是 Mapper 级别的，只要是同一个 Mapper，无论使用多少个 SqlSession 来操作，数据都是共享的，多个不同的 SqlSession 可以共用二级缓存。</p>
<p>MyBatis 二级缓存默认是关闭的，需要使用时可以通过配置手动开启。</p>
<p>下面我们通过代码来学习如何使用 MyBatis 缓存。</p>
<p>首先来演示一级缓存，以查询 Classes 对象为例。</p>
<h3 id="-1">一级缓存</h3>
<p>1. Classes 实体类</p>
<pre><code class="java language-java">public class Classes {
    private Long id;
    private String name;
    private List&lt;Student&gt; students;
}
</code></pre>
<p>2. ClassesReposirory 接口</p>
<pre><code class="java language-java">public interface ClassesRepository {
    public Classes findById(Long id);
}
</code></pre>
<p>3. ClassesReposirory.xml</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.ClassesRepository"&gt;

    &lt;select id="findById" parameterType="java.lang.Long" resultType="com.southwind.entity.Classes"&gt;
        select * from classes where id = #{id}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>4. config.xml</p>
<pre><code class="xml language-xml">&lt;configuration&gt;

    &lt;mappers&gt;
        &lt;mapper resource="com/southwind/repository/ClassesReposirory.xml"/&gt;
    &lt;/mappers&gt;

&lt;/configuration&gt;
</code></pre>
<p>5. Test 测试类</p>
<pre><code class="java language-java">public class Test {
    public static void main(String[] args) {
        InputStream inputStream = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
        SqlSession sqlSession = sqlSessionFactory.openSession();
        ClassesRepository classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes = classesRepository.findById(2L);
        System.out.println(classes);
        Classes classes2 = classesRepository.findById(2L);
        System.out.println(classes2);
    }
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/8ed4f300-b13e-11e9-8d9f-5d806c870c68" alt="WX20190617-170626@2x" /></p>
<p>可以看到结果，执行了一次 SQL 语句，查询出两个对象，第一个对象是通过 SQL 查询的，并保存到缓存中，第二个对象是直接从缓存中获取的。</p>
<p>我们说过一级缓存是 SqlSession 级别的，所以 SqlSession 一旦关闭，缓存也就不复存在了，修改代码，再次测试。</p>
<pre><code class="java language-java">public class Test {
    public static void main(String[] args) {
        InputStream inputStream = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
        SqlSession sqlSession = sqlSessionFactory.openSession();
        ClassesRepository classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes = classesRepository.findById(2L);
        System.out.println(classes);
        sqlSession.close();
        sqlSession = sqlSessionFactory.openSession();
        classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes2 = classesRepository.findById(2L);
        System.out.println(classes2);
        sqlSession.close();
    }
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/a093cbc0-b13e-11e9-9446-7bea49a7ddfe" alt="WX20190617-170226@2x" /></p>
<p>可以看到，执行了两次 SQL，在关闭 SqlSession、一级缓存失效的情况下，可以启用二级缓存，实现提升效率的需求。</p>
<h3 id="-2">二级缓存</h3>
<p>MyBatis 可以使用自带的二级缓存，也可以使用第三方的 ehcache 二级缓存。</p>
<p>先来使用 MyBatis 自带的二级缓存，具体步骤如下所示。</p>
<p>1. config.xml 中配置开启二级缓存</p>
<pre><code class="xml language-xml">&lt;configuration&gt;

    &lt;!-- 设置 settings --&gt;
    &lt;settings&gt;
        &lt;!-- 打印 SQL --&gt;
        &lt;setting name="logImpl" value="STDOUT_LOGGING"/&gt;
        &lt;!-- 开启二级缓存 --&gt;
        &lt;setting name="cacheEnabled" value="true"/&gt;
    &lt;/settings&gt;

&lt;/configuration&gt;
</code></pre>
<p>2. ClassesReposirory.xml 中配置二级缓存</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.ClassesRepository"&gt;

    &lt;cache&gt;&lt;/cache&gt;

    &lt;select id="findById" parameterType="java.lang.Long" resultType="com.southwind.entity.Classes"&gt;
        select * from classes where id = #{id}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>3. Classes 实体类实现 Serializable 接口</p>
<pre><code class="java language-java">public class Classes implements Serializable {
    private long id;
    private String name;
    private List&lt;Student&gt; students;
}
</code></pre>
<p>4. 测试</p>
<pre><code class="java language-java">public class Test {
    public static void main(String[] args) {
        InputStream inputStream = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
        SqlSession sqlSession = sqlSessionFactory.openSession();
        ClassesRepository classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes = classesRepository.findById(2L);
        System.out.println(classes);
        sqlSession.close();
        sqlSession = sqlSessionFactory.openSession();
        classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes2 = classesRepository.findById(2L);
        System.out.println(classes2);
        sqlSession.close();
    }
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/d8f033a0-b13e-11e9-83fd-07d7da80e621" alt="WX20190617-170516@2x" /></p>
<p>可以看到，执行了一次 SQL，查询出两个对象，二级缓存生效，接下来我们学习如何使用 ehcache 二级缓存，具体步骤如下所示。</p>
<p>1. pom.xml 添加 ehcache 相关依赖</p>
<pre><code class="xml language-xml">&lt;dependencies&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
    &lt;artifactId&gt;mybatis-ehcache&lt;/artifactId&gt;
    &lt;version&gt;1.0.0&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;dependency&gt;
    &lt;groupId&gt;net.sf.ehcache&lt;/groupId&gt;
    &lt;artifactId&gt;ehcache-core&lt;/artifactId&gt;
    &lt;version&gt;2.4.3&lt;/version&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>2. 在 resources 路径下创建 ehcache.xml</p>
<pre><code class="xml language-xml">&lt;ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="../config/ehcache.xsd"&gt;
&lt;diskStore/&gt;
    &lt;defaultCache
        maxElementsInMemory="1000"
        maxElementsOnDisk="10000000"
        eternal="false"
        overflowToDisk="false"
        timeToIdleSeconds="120"
        timeToLiveSeconds="120"
        diskExpiryThreadIntervalSeconds="120"
        memoryStoreEvictionPolicy="LRU"&gt;
    &lt;/defaultCache&gt;
&lt;/ehcache&gt;
</code></pre>
<p>3. config.xml 中配置开启二级缓存</p>
<pre><code class="xml language-xml">&lt;configuration&gt;

    &lt;!-- 设置settings --&gt;
    &lt;settings&gt;
        &lt;!-- 打印SQL --&gt;
        &lt;setting name="logImpl" value="STDOUT_LOGGING"/&gt;
        &lt;!-- 开启二级缓存 --&gt;
        &lt;setting name="cacheEnabled" value="true"/&gt;
    &lt;/settings&gt;

&lt;/configuration&gt;
</code></pre>
<p>4. ClassesReposirory.xml 中配置二级缓存</p>
<pre><code class="xml language-xml">&lt;mapper namespace="com.southwind.repository.ClassesReposirory"&gt; 
    &lt;!-- 开启二级缓存 --&gt;
    &lt;cache type="org.mybatis.caches.ehcache.EhcacheCache" &gt;
        &lt;!-- 缓存创建以后，最后一次访问缓存的时间至失效的时间间隔 --&gt;
        &lt;property name="timeToIdleSeconds" value="3600"/&gt;
        &lt;!-- 缓存自创建时间起至失效的时间间隔--&gt;
        &lt;property name="timeToLiveSeconds" value="3600"/&gt;
        &lt;!-- 缓存回收策略，LRU 移除近期最少使用的对象 --&gt;
        &lt;property name="memoryStoreEvictionPolicy" value="LRU"/&gt;
    &lt;/cache&gt;

    &lt;select id="findById" parameterType="java.lang.Long" resultType="com.southwind.entity.Classes"&gt;
        select * from classes where id = #{id}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>5. Classes 实体类不需要实现 Serializable 接口</p>
<pre><code class="java language-java">public class Classes {
    private long id;
    private String name;
    private List&lt;Student&gt; students;
}
</code></pre>
<p>6. 测试</p>
<pre><code class="java language-java">public class Test {
    public static void main(String[] args) {
        InputStream inputStream = Test.class.getClassLoader().getResourceAsStream("config.xml");
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
        SqlSession sqlSession = sqlSessionFactory.openSession();
        ClassesRepository classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes = classesRepository.findById(2L);
        System.out.println(classes);
        sqlSession.close();
        sqlSession = sqlSessionFactory.openSession();
        classesRepository = sqlSession.getMapper(ClassesRepository.class);
        Classes classes2 = classesRepository.findById(2L);
        System.out.println(classes2);
        sqlSession.close();
    }
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/05d1b930-b13e-11e9-8d9f-5d806c870c68" alt="WX20190617-171012@2x" /></p>
<p>同样执行一次 SQL，查询出两个对象，ehcache 二级缓存生效。</p>
<h3 id="-3">总结</h3>
<p>本节课我们讲解了 MyBatis 框架的缓存机制，MyBatis 的缓存分两种：一级缓存和二级缓存，一级缓存是 SqlSession 级别的，二级缓存是 Mapper 级别的，使用时我们需要注意这两种缓存的区别。缓存机制跟延迟加载功能类型，都是通过减少 Java Application 与数据库的交互频次，从而提高系统的运行效率。</p>
<p><a href="https://github.com/southwind9801/gcmybatis.git">请点击这里查看源码</a></p></div></article>