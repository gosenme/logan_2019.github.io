---
title: 案例上手 Spring 全家桶-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>前面的课程我们介绍过，使用 Spring MVC 框架进行 Web 开发时，前端页面传输的数据会自动封装到业务方法的参数中，这项工作是由 HandlerAdapter 组件完成的。</p>
<p>我们知道 HTTP 表单中的所有请求参数都是 String 类型的，如果业务方法的参数是 String 或者 int 类型，HandlerAdapter 可以自动完成数据转换，但如果参数是其他数据类型，比如 Date 类型，HandlerAdapter 是无法将 String 类型自动转为 Date 类型的，此时需要实现 Converter 接口来辅助 Spring MVC 完成数据类型的转换。</p>
<p>这就是我们本讲的内容，Spring MVC 自定义数据类型转换器的使用，具体操作如下所示。</p>
<p>（1）创建 DateConverter 类，并实现实现 org.springframework.core.convert.converter.Converter 接口，这样它就成为了一个自定义数据类型转换器，同时其泛型为 <code>&lt;String,Date&gt;</code>，表示的意思是将 String 类型的数值转换为 Date 类型，如下所示。</p>
<pre><code class="java language-java">public class DateConverter implements Converter&lt;String,Date&gt;{

    private String pattern;

    public DateConverter(String pattern){
        this.pattern = pattern;
    }

    public Date convert(String source) {
        // TODO Auto-generated method stub
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
        try {
            return simpleDateFormat.parse(source);
        } catch (ParseException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }

}
</code></pre>
<p>（2）在 springmvc.xml 中配置 conversionService bean，这个 bean 是org.springframework.context.support.ConversionServiceFactoryBean 的实例化对象，同时 bean 中必须包含一个 converters 属性，它将列出应用程序中用到的所有自定义 Converter。将我们自定义的 DateConverter 添加到 converters 中，通过有参构造函数创建 DateConverter 实例。</p>
<p>再添加一个 annotation-driven 标签，将 conversion-service 属性值设置为 bean 的名称，即 conversionService，如下所示。</p>
<pre><code class="xml language-xml">&lt;bean id="conversionService" class="org.springframework.context.support.ConversionServiceFactoryBean"&gt;
  &lt;property name="converters"&gt;
    &lt;list&gt;
      &lt;bean class="com.southwind.utils.DateConverter"&gt;
        &lt;!-- 调用有参构造函数创建 bean --&gt;
        &lt;constructor-arg type="java.lang.String" value="yyyy-MM-dd"/&gt;
      &lt;/bean&gt;
    &lt;/list&gt;
  &lt;/property&gt;
&lt;/bean&gt;

&lt;mvc:annotation-driven conversion-service="conversionService"/&gt;
</code></pre>
<p>（3）创建 addDate.jsp，通过 form 表单提交数据到后台。</p>
<pre><code class="jsp language-jsp">&lt;form action="dateConverterTest" method="post"&gt;
    请输入日期：&lt;input type="text" name="date"/&gt;&lt;font style="font-size:13px"&gt;(yyyy-MM-dd)&lt;/font&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>（4）创建 Controller 业务方法。</p>
<pre><code class="java language-java">@RequestMapping(value="/dateConverterTest")
@ResponseBody
public String dateConverterTest(Date date){
    return date.toString();
}
</code></pre>
<p>（5）运行代码，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/e9700820-99f9-11e8-aea0-0b6079bd9920" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/f01a1df0-99f9-11e8-8d5e-1dce8d3a2c27" width = "60%" /></p>
<p>String 转 Date 的自定义数据类型转换器运行成功。</p>
<p>除了 Date 类型的转换，我们还可以自定义数据格式，比如注册一个 Student，前端页面按照 "id-name-age" 的形式输入 String 类型的数据，通过自定义 Convertor，可以将该 String 类型的数据直接转换为 Student 对象，具体操作如下所示。</p>
<p>（1）创建 Student 实体类。</p>
<pre><code class="java language-java">public class Student {
    private int id;
    private String name;
    private int age;
}
</code></pre>
<p>（2）创建 addStudent.jsp，通过 form 表单提交数据到后台。</p>
<pre><code class="jsp language-jsp">&lt;form action="studentConverterTest" method="post"&gt;
    学生信息：&lt;input type="text" name="student"/&gt;&lt;font style="font-size:13px"&gt;(id-name-age)&lt;/font&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>（3）创建 Controller 业务方法。</p>
<pre><code class="java language-java">@RequestMapping(value="/studentConverterTest")
@ResponseBody
public String studentConverterTest(Student student){
    return student.toString();
}
</code></pre>
<p>（4）创建 StudentConverter 转换器。</p>
<pre><code class="java language-java">public class StudentConverter implements Converter&lt;String,Student&gt;{

    public Student convert(String source) {
        // TODO Auto-generated method stub
        String[] args = source.split("-");
        Student student = new Student();
        student.setId(Integer.parseInt(args[0]));
        student.setName(args[1]);
        student.setAge(Integer.parseInt(args[2]));
        return student;
    }

}
</code></pre>
<p>（5）在 springmvc.xml 中配置 StudentConverter 转换器。</p>
<pre><code class="xml language-xml">&lt;bean id="conversionService" class="org.springframework.context.support.ConversionServiceFactoryBean"&gt;
    &lt;property name="converters"&gt;
        &lt;list&gt;
            &lt;!-- 日期转换器 --&gt;
            &lt;bean class="com.southwind.utils.DateConverter"&gt;
                &lt;constructor-arg type="java.lang.String" value="yyyy-MM-dd"/&gt;
            &lt;/bean&gt;
            &lt;!-- Student 转换器 --&gt;
            &lt;bean class="com.southwind.utils.StudentConverter"&gt;&lt;/bean&gt;
        &lt;/list&gt;
    &lt;/property&gt;
&lt;/bean&gt;
</code></pre>
<p>（6）运行程序，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/7b71edc0-9a08-11e8-9724-fb3ff7de9e38" width = "65%" /></p>
<p><img src="https://images.gitbook.cn/81042af0-9a08-11e8-992f-9dfb28d2b53f" width = "65%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring MVC 一个非常实用的功能：自定义数据类型转换器，开发者可以根据特定的需求来定制自己的数据类型转换器，并且我们不需要关心具体的实现逻辑，只需要告诉 Spring MVC 转换逻辑即可，这样就可以很方便地将前端传来的参数转为特定的数据类型，使用起来非常简单。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc-dataconverter.git">请单击这里下载源码</a></p></div></article>