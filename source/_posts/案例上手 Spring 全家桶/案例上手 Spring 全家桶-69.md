---
title: 案例上手 Spring 全家桶-69
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>第一部分（第 1-1 ~ 1-6 课）这部分内容讲解了 Spring Framework 的基本概念、组成，以及 IoC 容器的特性和使用，AOP 的使用，通过案例让大家熟练掌握 Spring Framework，为后面的课程打下基础。</p>
<p>（1）IoC 属于哪种设计模式？（单选题）</p>
<p>A. 单例模式</p>
<p>B. 原型模式</p>
<p>C. 工厂模式</p>
<p>D. 适配器模式</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>C</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（2）谈谈你对 Spring IoC 和 DI 的理解，它们有什么区别？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p></p>
<ul>
<li><p>IoC Inverse of Control 反转控制的概念，就是将原本在程序中手动创建 UserService 对象的控制权，交由 Spring 框架管理，简单说就是创建 UserService 对象控制权被反转到了 Spring 框架。</p></li>
<li>DI：Dependency Injection 依赖注入，在 Spring 框架负责创建 Bean 对象时，动态的将依赖对象注入到 Bean 组件。</p>

<dl>
    <dt></dt>
    <dd></dd></dl>

</details></li>
</ul>
<p>（3）简单谈谈 IoC 容器的原理。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>IoC 容器在加载时对 XML 配置文件进行解析，获取所有的 bean 配置，结合 bean 中的信息（实体类，属性），通过反射机制来创建实例化对象并完成成员变量的赋值操作，最后以键值对的形式将创建好的实例化对象存入容器。</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（4）bean 的 scope 有几种类型？请详细列举。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>共有 4 种。</p>
<ul>
<li>singleton：单例，表示通过 Spring 容器获取的该对象是唯一的。</li>
<li>prototype：原型，表示通过 Spring 容器获取的对象都是不同的。</li>
<li>reqeust：请求，表示在一次 HTTP 请求内有效。</li>
<li>session：会话，表示在一个用户会话内有效。</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul>
<p>（5）说说 IoC 中的继承和 Java 继承的区别。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>IoC 中继承是对象层面的，指继承对象可以获取被继承对象的所有成员变量值，并赋给其对应的成员变量。Java 中的继承是类层面的，指子类可以获取父类的非私有成员变量和方法，不需要再次定义。</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（6）IoC 中 car 对象的配置如下，现在要添加 user 对象，并且将 car 注入到 user 中，正确的配置是（）（多选题）</p>
<pre><code>&lt;bean id="car" class="com.southwind.entity.Car"&gt;&lt;/bean&gt;
</code></pre>
<p>A.</p>
<pre><code>&lt;bean id="user" class="com.southwind.entity.User"&gt;

  ​    &lt;property name="car" value="car"&gt;&lt;/property&gt;

  &lt;/bean&gt;
</code></pre>
<p>B.</p>
<pre><code>&lt;bean id="user" class="com.southwind.entity.User"&gt;

  ​    &lt;property name="car" ref="car"&gt;&lt;/property&gt;

  &lt;/bean&gt;
</code></pre>
<p>C.</p>
<pre><code>&lt;bean id="user" class="com.southwind.entity.User" p:car-ref="car"&gt;&lt;/bean&gt;
</code></pre>
<p>D.</p>
<pre><code>&lt;bean id="user" class="com.southwind.entity.User" p:car="car"&gt;&lt;/bean&gt;
</code></pre>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>BC</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（7）请分别写出 IoC 静态工厂方法和实例工厂方法的配置。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p> </p>
<pre><code class="xml language-xml">&lt;!-- 配置静态工厂创建 car 对象 --&gt;
&lt;bean id="car1" class="com.southwind.entity.StaticCarFactory" factory-method="getCar"&gt;
&lt;constructor-arg value="1"&gt;&lt;/constructor-arg&gt;
&lt;/bean&gt;

&lt;!-- 配置实例工厂对象 --&gt;
&lt;bean id="carFactory" class="com.southwind.entity.InstanceCarFactory"&gt;&lt;/bean&gt;

&lt;!-- 通过实例工厂对象创建 car 对象 --&gt;
&lt;bean id="car2" factory-bean="carFactory" factory-method="getCar"&gt;
&lt;constructor-arg value="2"&gt;&lt;/constructor-arg&gt;
&lt;/bean&gt; 
</code></pre>
<p></p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p>
<p>（8）IoC 自动装载有几种方式？</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>有两种。</p>
<ul>
<li>byName：通过属性名自动装载。</li>
<li>byType：通过属性对应的数据类型自动装载。</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul>
<p>（9）介绍一下 Spring 框架中 bean 的生命周期。</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>1）bean 定义：在配置文件里面用 <bean></bean> 来进行定义。</p>
<p>2）bean初始化，有两种方式初始化：</p>
<ul>
<li>在配置文件中通过指定 init-method 属性来完成；</li>
<li>实现 org.springframwork.beans.factory.InitializingBean 接口。</li>
</ul>
<p>3）bean 调用。</p>
<p>4）bean 销毁，销毁有两种方式：</p>
<ul>
<li>使用配置文件指定的 destroy-method 属性</li>
<li>实现 org.springframwork.bean.factory.DisposeableBean 接口</p><dl>
    <dt></dt>
    <dd></dd></dl></details></li>
</ul>
<p>（10）IoC 容器自动完成装载，默认是 ___的方式</p>
<p><details stylecolor=red>
    <summary><b><font color=207f06>点击查看答案</font></b></summary>
    <p>byType</p>
    <dl>
        <dt></dt>
        <dd></dd></dl>
</details></p></div></article>