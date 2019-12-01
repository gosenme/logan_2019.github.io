---
title: 案例上手 Spring 全家桶-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>本节课我们来学习 Spring MVC 提供的国际化功能，所谓国际化就是指同一个应用程序在不同语言设置的浏览器中，自动显示不同的语言，比如在中文环境下，页面所有的文本全部以中文的形式展示，在英文语言环境下，同样的文字内容全部转换为英文，Spring MVC 框架对国际化操作做了很好的集成，只需简单配置即可完成国际化。</p>
<p>具体步骤如下所示：</p>
<p>（1）搭建 Spring MVC 环境。</p>
<p>（2）配置 springmvc.xml。</p>
<pre><code class="xml language-xml">&lt;!--自动扫描包中的 Controlller --&gt;
&lt;context:component-scan base-package="com.southwind.controller"/&gt;

&lt;!-- 视图解析器 --&gt;
&lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
    &lt;!-- 前缀 --&gt;
    &lt;property name="prefix" value="/"/&gt;
    &lt;!-- 后缀，自动拼接 --&gt;
    &lt;property name="suffix" value=".jsp"/&gt;
&lt;/bean&gt;

&lt;!-- 国际化资源文件 --&gt;
&lt;bean id="messageSource" class="org.springframework.context.support.ReloadableResourceBundleMessageSource"&gt;
    &lt;!-- 表示多语言配置文件在根路径下，以 language 开头的文件--&gt;
    &lt;property name="basename" value="classpath:language"/&gt;
    &lt;property name="useCodeAsDefaultMessage" value="true"/&gt;
&lt;/bean&gt;

&lt;!-- 拦截器 --&gt;
&lt;mvc:interceptors&gt;
    &lt;bean id="localeChangeInterceptor" class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor"&gt;
        &lt;property name="paramName" value="lang"/&gt;
    &lt;/bean&gt;
&lt;/mvc:interceptors&gt;

&lt;!-- 配置 SessionLocaleResolver，动态的获取 Locale 对象存入 Session --&gt;
&lt;bean id="localeResolver" class="org.springframework.web.servlet.i18n.SessionLocaleResolver"&gt;&lt;/bean&gt;
</code></pre>
<p>（3）创建国际化资源文件 language_en_US.properties 和 language_zh_CN.properties，分别存储英文和中文资源。</p>
<p>language_en_US.properties</p>
<pre><code class="properties language-properties">language.cn = \u4E2D\u6587
language.en = English
info = login
username = username
password = password
repassword = repassword
tel = tel
email = email
submit = submit
reset = reset
</code></pre>
<p>language_zh_CN.properties</p>
<pre><code class="properties language-properties">language.cn = \u4E2D\u6587
language.en = English
info = \u6CE8\u518C
username = \u7528\u6237\u540D
password = \u5BC6\u7801
repassword = \u786E\u8BA4\u5BC6\u7801
tel = \u8054\u7CFB\u7535\u8BDD
email = \u7535\u5B50\u90AE\u7BB1
submit = \u63D0\u4EA4
reset = \u91CD\u7F6E
</code></pre>
<p>（4）创建 Handler。</p>
<pre><code class="java language-java">@Controller
public class TestController {
    @RequestMapping("/test")
    public String index() {
        return "index";
    }
}
</code></pre>
<p>（5）创建 JSP，导入 Spring MVC 标签库，用 spring:message 标签绑定不同的语言信息。</p>
<pre><code class="jsp language-jsp">&lt;form action="" method="post"&gt;
    &lt;spring:message code="username"/&gt;：
    &lt;input type="text"/&gt;
    &lt;spring:message code="password"/&gt;：
    &lt;input type="password"/&gt;
    &lt;spring:message code="repassword"/&gt;：
    &lt;input type="password"/&gt;
    &lt;spring:message code="tel"/&gt;：
    &lt;input type="text"/&gt;
    &lt;spring:message code="email"/&gt;：
    &lt;input type="text"/&gt;
    &lt;input type="submit" value="&lt;spring:message code="submit"/&gt;"/&gt;
    &lt;input type="reset" value="&lt;spring:message code="reset"/&gt;"/&gt;
&lt;/form&gt;
</code></pre>
<p>（6）启动 Tomcat，输入 http://localhost:8080/springmvc-inter/test?lang=zh_CN，运行结果如下图。</p>
<p><img src="https://images.gitbook.cn/83974a20-9ad2-11e8-b37c-dd4feba3837e" width = "50%" /></p>
<p>（7）输入 http://localhost:8080/springmvc-inter/test?lang=en_US，运行结果如下图。</p>
<p><img src="https://images.gitbook.cn/8c2cb530-9ad2-11e8-a178-519d5b470954" width = "50%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring MVC 的国际化操作，同样的一个软件系统在不同的国家需要用不同的语言展示给用户，国际化就是用来完成这项工作，通过配置文件的方式可以快速便捷地完成不同语言的切换。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc_international.git">请单击这里下载源码</a></p></div></article>