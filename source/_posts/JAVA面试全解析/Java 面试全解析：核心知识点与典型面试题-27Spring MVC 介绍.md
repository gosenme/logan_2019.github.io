---
title: Java 面试全解析：核心知识点与典型面试题-27
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="springmvc">Spring MVC 介绍</h3>
<p>Spring MVC（Spring Web MVC）是 Spring Framework 提供的 Web 组件，它的实现基于 MVC 的设计模式：Controller（控制层）、Model（模型层）、View（视图层），提供了前端路由映射、视图解析等功能，让 Java Web 开发变得更加简单，也属于 Java 开发中必须要掌握的热门框架。</p>
<h3 id="">执行流程</h3>
<p>Spring MVC 的执行流程如下：</p>
<ol>
<li>客户端发送请求至前端控制器（DispatcherServlet）</li>
<li>前端控制器根据请求路径，进入对应的处理器</li>
<li>处理器调用相应的业务方法</li>
<li>处理器获取到相应的业务数据</li>
<li>处理器把组装好的数据交还给前端控制器</li>
<li>前端控制器将获取的 ModelAndView 对象传给视图解析器（ViewResolver）</li>
<li>前端控制器获取到解析好的页面数据</li>
<li>前端控制器将解析好的页面返回给客户端</li>
</ol>
<p>流程如下图所示：</p>
<p><img src="https://images.gitbook.cn/b12460c0-d9da-11e9-970d-b51140896651" alt="1" /></p>
<h3 id="-1">核心组件</h3>
<p>Spring MVC 的核心组件如下列表所示：</p>
<ol>
<li><strong>DispatcherServlet</strong>：核心处理器（也叫前端控制器），负责调度其他组件的执行，可降低不同组件之间的耦合性，是整个 Spring MVC 的核心模块。</li>
<li><strong>Handler</strong>：处理器，完成具体业务逻辑，相当于 Servlet 或 Action。</li>
<li><strong>HandlerMapping</strong>：DispatcherServlet 是通过 HandlerMapping 将请求映射到不同的 Handler。</li>
<li><strong>HandlerInterceptor</strong>：处理器拦截器，是一个接口，如果我们需要做一些拦截处理，可以来实现这个接口。</li>
<li><strong>HandlerExecutionChain</strong>：处理器执行链，包括两部分内容，即 Handler 和 HandlerInterceptor（系统会有一个默认的 HandlerInterceptor，如果需要额外拦截处理，可以添加拦截器设置）。</li>
<li><strong>HandlerAdapter</strong>：处理器适配器，Handler 执行业务方法之前，需要进行一系列的操作包括表单数据的验证、数据类型的转换、将表单数据封装到 POJO 等，这一系列的操作，都是由 HandlerAdapter 来完成，DispatcherServlet 通过 HandlerAdapter 执行不同的 Handler。</li>
<li><strong>ModelAndView</strong>：装载了模型数据和视图信息，作为 Handler 的处理结果，返回给 DispatcherServlet。</li>
<li><strong>ViewResolver</strong>：视图解析器，DispatcherServlet 通过它将逻辑视图解析成物理视图，最终将渲染结果响应给客户端。</li>
</ol>
<h3 id="-2">自动类型转换</h3>
<p>自动类型转换指的是，Spring MVC 可以将表单中的字段，自动映射到实体类的对应属性上，请参考以下示例。</p>
<h4 id="1jsp">1. JSP 页面代码</h4>
<pre><code class="html language-html">&lt;%@ page contentType="text/html;charset=UTF-8" language="java" %&gt;
&lt;html&gt;
&lt;body&gt;
&lt;form action="add"&gt;
    名称：&lt;input type="input" name="name"&gt;&lt;br&gt;
    年龄：&lt;input type="input" name="age"&gt;&lt;br&gt;
    &lt;input type="submit" value=" 提交 "&gt;
&lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<h4 id="2">2. 编写实体类</h4>
<pre><code class="java language-java">public class PersonDTO {
    private String name;
    private int age;

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}
</code></pre>
<h4 id="3">3. 编写控制器</h4>
<pre><code class="java language-java">import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
public class PersonController {
    @RequestMapping(value = "/add", produces = "text/plain;charset=utf-8")
    public String add(PersonVO person) {
        return person.getName() + ":" + person.getAge();
    }
}
</code></pre>
<h4 id="4">4. 执行结果</h4>
<p>执行结果如下图所示：</p>
<p><img src="https://images.gitbook.cn/dd1a0a40-d9da-11e9-970d-b51140896651" alt="2" /></p>
<h4 id="-3">中文乱码处理</h4>
<p>业务的操作过程中可能会出现中文乱码的情况，以下是处理中文乱码的解决方案。<br />第一步，在 web.xml 添加编码过滤器，配置如下：</p>
<pre><code class="xml language-xml">&lt;filter&gt;
    &lt;filter-name&gt;encodingFilter&lt;/filter-name&gt;
    &lt;filter-class&gt;org.springframework.web.filter.CharacterEncodingFilter&lt;/filter-class&gt;
    &lt;init-param&gt;
        &lt;param-name&gt;encoding&lt;/param-name&gt;
        &lt;param-value&gt;UTF-8&lt;/param-value&gt;
    &lt;/init-param&gt;
&lt;/filter&gt;
&lt;filter-mapping&gt;
    &lt;filter-name&gt;encodingFilter&lt;/filter-name&gt;
    &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
&lt;/filter-mapping&gt;
</code></pre>
<p>第二步，设置 RequestMapping 的 produces 属性，指定返回值类型和编码，如下所示：</p>
<pre><code class="java language-java">@RequestMapping(value  = "/add", produces = "text/plain;charset=utf-8")
</code></pre>
<h3 id="-4">拦截器</h3>
<p>在 Spring MVC 中可以通过配置和实现 HandlerInterceptor 接口，来实现自己的拦截器。</p>
<h4 id="1">1. 配置全局拦截器</h4>
<p>在 Spring MVC 的配置文件中，添加如下配置：</p>
<pre><code class="xml language-xml">&lt;mvc:interceptors&gt;
  &lt;bean class="com.learning.core.MyInteceptor"&gt;&lt;/bean&gt;
&lt;/mvc:interceptors&gt;
</code></pre>
<h4 id="2-1">2. 添加拦截器实现代码</h4>
<p>拦截器的实现代码如下：</p>
<pre><code class="java language-java">import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
/**
 * 拦截器
 **/
public class MyInteceptor implements HandlerInterceptor {
    // 在业务处理器处理请求之前被调用
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
                             Object handler) throws Exception {
        System.out.println("preHandle");
        return true;
    }
    // 在业务处理器处理请求完成之后，生成视图之前执行
    public void postHandle(HttpServletRequest request, HttpServletResponse response,
                           Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("postHandle");
    }
    // 在 DispatcherServlet 完全处理完请求之后被调用
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) throws Exception {
        System.out.println("afterCompletion");
    }
}
</code></pre>
<h3 id="-5">参数验证</h3>
<h4 id="1pomxml">1. pom.xml 添加验证依赖包</h4>
<p>配置如下：</p>
<pre><code class="xml language-xml">&lt;!-- Hibernate 参数验证包 --&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.hibernate.validator&lt;/groupId&gt;
    &lt;artifactId&gt;hibernate-validator&lt;/artifactId&gt;
    &lt;version&gt;6.0.17.Final&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<h4 id="2-2">2.  开启注解验证</h4>
<p>在 Spring MVC 的配置文件中，添加如下配置信息：</p>
<pre><code class="xml language-xml">&lt;mvc:annotation-driven /&gt;
</code></pre>
<h4 id="3-1">3. 编写控制器</h4>
<p>代码如下：</p>
<pre><code class="java language-java">import com.google.gson.JsonObject;
import com.learning.pojo.PersonDTO;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
public class PersonController {
    @RequestMapping(value = "/check", produces = "text/plain;charset=utf-8")
    public String check(@Validated PersonDTO person, BindingResult bindResult) {
        // 需要 import com.google.gson.Gson
        JsonObject result = new JsonObject();
        StringBuilder errmsg = new StringBuilder();
        if (bindResult.hasErrors()) {
            List&lt;ObjectError&gt; errors = bindResult.getAllErrors();
            for (ObjectError error : errors) {
                errmsg.append(error.getDefaultMessage());
            }
            result.addProperty("status", -1);
        } else {
            result.addProperty("status", 1);
        }
        result.addProperty("errmsg", errmsg.toString());
        return result.toString();
    }

}
</code></pre>
<h4 id="4-1">4. 编写实体类</h4>
<p>代码如下：</p>
<pre><code class="java language-java">import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
public class PersonDTO {
    @NotNull(message = "姓名不能为空")
    private String name;
    @Min(value = 18,message = "年龄不能低于18岁")
    private int age;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}
</code></pre>
<p>更多验证注解，如下所示：</p>
<table>
<thead>
<tr>
<th style="text-align:left;">注解</th>
<th style="text-align:left;">运行时检查</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left;">@AssertFalse</td>
<td style="text-align:left;">被注解的元素必须为 false</td>
</tr>
<tr>
<td style="text-align:left;">@AssertTrue</td>
<td style="text-align:left;">被注解的元素必须为 true</td>
</tr>
<tr>
<td style="text-align:left;">@DecimalMax(value)</td>
<td style="text-align:left;">被注解的元素必须为一个数字，其值必须小于等于指定的最大值</td>
</tr>
<tr>
<td style="text-align:left;">@DecimalMin(Value)</td>
<td style="text-align:left;">被注解的元素必须为一个数字，其值必须大于等于指定的最小值</td>
</tr>
<tr>
<td style="text-align:left;">@Digits(integer=, fraction=)</td>
<td style="text-align:left;">被注解的元素必须为一个数字，其值必须在可接受的范围内</td>
</tr>
<tr>
<td style="text-align:left;">@Future</td>
<td style="text-align:left;">被注解的元素必须是日期，检查给定的日期是否比现在晚</td>
</tr>
<tr>
<td style="text-align:left;">@Max(value)</td>
<td style="text-align:left;">被注解的元素必须为一个数字，其值必须小于等于指定的最大值</td>
</tr>
<tr>
<td style="text-align:left;">@Min(value)</td>
<td style="text-align:left;">被注解的元素必须为一个数字，其值必须大于等于指定的最小值</td>
</tr>
<tr>
<td style="text-align:left;">@NotNull</td>
<td style="text-align:left;">被注解的元素必须不为 null</td>
</tr>
<tr>
<td style="text-align:left;">@Null</td>
<td style="text-align:left;">被注解的元素必须为 null</td>
</tr>
<tr>
<td style="text-align:left;">@Past(java.util.Date/Calendar)</td>
<td style="text-align:left;">被注解的元素必须过去的日期，检查标注对象中的值表示的日期比当前早</td>
</tr>
<tr>
<td style="text-align:left;">@Pattern(regex=, flag=)</td>
<td style="text-align:left;">被注解的元素必须符合正则表达式，检查该字符串是否能够在 match 指定的情况下被 regex 定义的正则表达式匹配</td>
</tr>
<tr>
<td style="text-align:left;">@Size(min=, max=)</td>
<td style="text-align:left;">被注解的元素必须在制定的范围（数据类型：String、Collection、Map、Array）</td>
</tr>
<tr>
<td style="text-align:left;">@Valid</td>
<td style="text-align:left;">递归的对关联对象进行校验, 如果关联对象是个集合或者数组，那么对其中的元素进行递归校验，如果是一个 map，则对其中的值部分进行校验</td>
</tr>
<tr>
<td style="text-align:left;">@CreditCardNumber</td>
<td style="text-align:left;">对信用卡号进行一个大致的验证</td>
</tr>
<tr>
<td style="text-align:left;">@Email</td>
<td style="text-align:left;">被注释的元素必须是电子邮箱地址</td>
</tr>
<tr>
<td style="text-align:left;">@Length(min=, max=)</td>
<td style="text-align:left;">被注解的对象必须是字符串的大小必须在制定的范围内</td>
</tr>
<tr>
<td style="text-align:left;">@NotBlank</td>
<td style="text-align:left;">被注解的对象必须为字符串，不能为空，检查时会将空格忽略</td>
</tr>
<tr>
<td style="text-align:left;">@NotEmpty</td>
<td style="text-align:left;">被注释的对象必须不为空（数据：String、Collection、Map、Array）</td>
</tr>
<tr>
<td style="text-align:left;">@Range(min=, max=)</td>
<td style="text-align:left;">被注释的元素必须在合适的范围内（数据：BigDecimal、BigInteger、String、byte、short、int、long 和原始类型的包装类）</td>
</tr>
<tr>
<td style="text-align:left;">@URL(protocol=, host=, port=, regexp=, flags=)</td>
<td style="text-align:left;">被注解的对象必须是字符串，检查是否是一个有效的 URL，如果提供了 protocol、host 等，则该 URL 还需满足提供的条件</td>
</tr>
</tbody>
</table>
<h4 id="5">5. 执行结果</h4>
<p>执行结果，如下图所示：</p>
<p><img src="https://images.gitbook.cn/f5b5c8a0-d9da-11e9-970d-b51140896651" alt="3" /></p>
<p>访问 Spring MVC 官方说明文档：<a href="http://1t.click/H7a">http://1t.click/H7a</a></p>
<h3 id="-6">相关面试题</h3>
<h4 id="1springmvc">1. 简述一下 Spring MVC 的执行流程？</h4>
<p>答：前端控制器（DispatcherServlet） 接收请求，通过映射从 IoC 容器中获取对应的 Controller 对象和 Method 方法，在方法中进行业务逻辑处理组装数据，组装完数据把数据发给视图解析器，视图解析器根据数据和页面信息生成最终的页面，然后再返回给客户端。</p>
<h4 id="2pojojavabean">2. POJO 和 JavaBean 有什么区别？</h4>
<p>答：POJO 和 JavaBean 的区别如下：</p>
<ul>
<li>POJO（Plain Ordinary Java Object）普通 Java 类，具有 getter/setter 方法的普通类都就可以称作 POJO，它是 DO/DTO/BO/VO 的统称，禁止命名成 xxxPOJO。</li>
<li>JavaBean 是 Java 语言中的一种可重用组件，JavaBean 的构造函数和行为必须符合特定的约定：这个类必须有一个公共的缺省构造函数；这个类的属性使用 getter/setter 来访问，其他方法遵从标准命名规范；这个类应是可序列化的。</li>
</ul>
<p>简而言之，当一个 POJO 可序列化，有一个无参的构造函数，它就是一个 JavaBean。</p>
<h4 id="3-2">3. 如何实现跨域访问？</h4>
<p>答：常见的跨域的实现方式有两种：使用 JSONP 或者在服务器端设置运行跨域。服务器运行跨域的代码如下：</p>
<pre><code class="java language-java">import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
@Configuration
public class MyConfiguration {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                // 设置允许跨域的请求规则
                registry.addMapping("/api/**");
            }
        };
    }
}
</code></pre>
<h4 id="4-2">4. 以下代码描述正确的是？</h4>
<pre><code class="java language-java">@RequestMapping(value="/list",params={"age=10"}
public String list(){
   // do something
}
</code></pre>
<p>A：age 参数不传递的时候，默认值是 10<br />B：age 参数可以为空<br />C：age 参数不能为空<br />D：以上都不对</p>
<p>答：C<br />题目解析：params={"age=10"} 表示必须包含 age 参数，且值必须等于 10。</p>
<h4 id="5requestmapping">5. @RequestMapping 注解的常用属性有哪些？</h4>
<p>答：@RequestMapping 常用属性如下：</p>
<ul>
<li>value：指定 URL 请求的实际地址，用法：@RequestMapping(value="/index")；</li>
<li>method：指定请求的 method 类型，如 GET/POST/PUT/DELETE 等，用法：@RequestMapping(value="/list",method=RequestMethod.POST)；</li>
<li>params：指定请求参数中必须包含的参数名称，如果不存在该名称，则无法调用此方法，用法：@RequestMapping(value="/list",params={"name","age"})。</li>
</ul>
<h4 id="6">6. 访问以下接口不传递任何参数的情况下，执行的结果是？</h4>
<pre><code class="java language-java">@RequestMapping(value="/list")
@ResponseBody
public String list(int id){
    return "id="+id;
}
</code></pre>
<p>A：id=0<br />B：id=<br />C：页面报错 500<br />D：id=null</p>
<p>答：C<br />题目解析：页面报错会提示：可选的参数“id”不能转为 null，因为基本类型不能赋值 null，所以会报错。</p>
<h4 id="7403">7.访问页面时显示 403 代表的含义是？</h4>
<p>A：服务器繁忙<br />B：找不到该页面<br />C：禁止访问<br />D：服务器跳转中</p>
<p>答：C<br />题目解析：常用 HTTP 状态码及对应的含义：</p>
<ul>
<li>400：错误请求，服务器不理解请求的语法</li>
<li>401：未授权，请求要求身份验证</li>
<li>403：禁止访问，服务器拒绝请求</li>
<li>500：服务器内部错误，服务器遇到错误，无法完成请求</li>
<li>502：错误网关，服务器作为网关或代理，从上游服务器收到无效响应</li>
<li>504：网关超时，服务器作为网关或代理，但是没有及时从上游服务器收到请求</li>
</ul>
<h4 id="8forwardredirect">8.forward 和 redirect 有什么区别？</h4>
<p>答：forward 和 redirect 区别如下：</p>
<ul>
<li>forward 表示请求转发，请求转发是服务器的行为；redirect 表示重定向，重定向是客户端行为；</li>
<li>forward 是服务器请求资源，服务器直接访问把请求的资源转发给浏览器，浏览器根本不知道服务器的内容是从哪来的，因此它的地址栏还是原来的地址；redirect 是服务端发送一个状态码告诉浏览器重新请求新的地址，因此地址栏显示的是新的 URL；</li>
<li>forward 转发页面和转发到的页面可以共享 request 里面的数据；redirect 不能共享数据；</li>
<li>从效率来说，forward 比 redirect 效率更高。</li>
</ul>
<h4 id="9">9. 访问以下接口不传递任何参数的情况下，执行的结果是？</h4>
<pre><code class="java language-java">@RequestMapping(value="/list")
@ResponseBody
public String list(Integer id){
    return "id="+id;
}
</code></pre>
<p>A：id=0<br />B：id=<br />C：页面报错 500<br />D：id=null</p>
<p>答：D<br />题目解析：包装类可以赋值 null，不会报错。</p>
<h4 id="10springmvc">10. Spring MVC 中如何在后端代码中实现页面跳转？</h4>
<p>答：在后端代码中可以使用 forward:/index.jsp 或 redirect:/index.jsp 完成页面跳转，前者 URL 地址不会发生改变，或者 URL 地址会发生改变，完整跳转代码如下：</p>
<pre><code class="java language-java">@RequestMapping("/redirect")
public String redirectTest(){
    return "redirect:/index.jsp";
}
</code></pre>
<h4 id="11springmvc">11. Spring MVC 的常用注解有哪些？</h4>
<p>答：Spring MVC 的常用注解如下：</p>
<ul>
<li>@Controller：用于标记某个类为控制器；</li>
<li>@ResponseBody ：标识返回的数据不是 html 标签的页面，而是某种格式的数据，如 JSON、XML 等；</li>
<li>@RestController：相当于 @Controller 加 @ResponseBody 的组合效果；</li>
<li>@Component：标识为 Spring 的组件；</li>
<li>@Configuration：用于定义配置类；</li>
<li>@RequestMapping：用于映射请求地址的注解；</li>
<li>@Autowired：自动装配对象；</li>
<li>@RequestHeader：可以把 Request 请求的 header 值绑定到方法的参数上。</li>
</ul>
<h4 id="12">12. 拦截器的使用场景有哪些？</h4>
<p>答：拦截器的典型使用场景如下：</p>
<ul>
<li>日志记录：可用于记录请求日志，便于信息监控和信息统计；</li>
<li>权限检查：可用于用户登录状态的检查；</li>
<li>统一安全处理：可用于统一的安全效验或参数的加密 / 解密等。</li>
</ul>
<h4 id="13springmvc">13. Spring MVC 如何排除拦截目录？</h4>
<p>答：在 Spring MVC 的配置文件中，添加 <mvc:exclude-mapping path="/static/**" /> ，用于排除拦截目录，完整配置的示例代码如下：</p>
<pre><code class="xml language-xml">&lt;mvc:interceptors&gt;
    &lt;mvc:interceptor&gt;
        &lt;mvc:mapping path="/**" /&gt;
        &lt;!-- 排除拦截地址 --&gt;
        &lt;mvc:exclude-mapping path="/api/**" /&gt;
        &lt;bean class="com.learning.core.MyInteceptor"&gt;&lt;/bean&gt;
    &lt;/mvc:interceptor&gt;
&lt;/mvc:interceptors&gt;
</code></pre>
<h4 id="14validatedvalid">14.@Validated 和 @Valid 有什么区别 ？</h4>
<p>答：@Validated 和 @Valid 都用于参数的效验，不同的是：</p>
<ul>
<li>@Valid 是 Hibernate 提供的效验机制，Java 的 JSR 303 声明了 @Valid 这个类接口，而 Hibernate-validator 对其进行了实现；@Validated 是 Spring 提供的效验机制，@Validation 是对 @Valid 进行了二次封装，提供了分组功能，可以在参数验证时，根据不同的分组采用不同的验证机制；</li>
<li>@Valid 可用在成员对象的属性字段验证上，而 @Validated 不能用在成员对象的属性字段验证上，也就是说 @Validated 无法提供嵌套验证。</li>
</ul>
<h4 id="15springmvcrequest">15.Spring MVC 有几种获取 request 的方式？</h4>
<p>答：Spring MVC 获取 request 有以下三种方式：</p>
<p>① 从请求参数中获取</p>
<p>示例代码：</p>
<pre><code class="java language-java">@RequestMapping("/index")
@ResponseBody
public void index(HttpServletRequest request){
　　// do something
}
</code></pre>
<p>该方法实现的原理是 Controller 开始处理请求时，Spring 会将 request 对象赋值到方法参数中。</p>
<p>② 通过 RequestContextHolder上下文获取 request 对象</p>
<p>示例代码：</p>
<pre><code class="java language-java">@RequestMapping("/index")
@ResponseBody
public void index(){
    ServletRequestAttributes servletRequestAttributes = (ServletRequestAttributes)RequestContextHolder.getRequestAttributes();
    HttpServletRequest request = servletRequestAttributes.getRequest();
    // do something
}
</code></pre>
<p>③ 通过自动注入的方式</p>
<pre><code class="java language-java">@Controller
public class HomeController{
    @Autowired
    private HttpServletRequest request; // 自动注入 request 对象
    // do something
}
</code></pre>
<h3 id="-7">总结</h3>
<p>本文我们了解了 Spring MVC 运行的 8 个步骤和它的 8 大核心组件，也尝试了 Spring MVC 方面的类型转换，可将表单自动转换为实体对象，也使用 Hibernate 的验证功能优雅地实现了参数的验证，还可以通过配置和实现 HandlerInterceptor 接口来自定义拦截器，相信有了这些知识，可以帮助我们更高效地开发 Web 和接口项目。</p>
<blockquote>
  <p><a href="https://github.com/vipstone/java-interview/tree/master/springlearning">点击此处下载本文源码</a></p>
</blockquote></div></article>