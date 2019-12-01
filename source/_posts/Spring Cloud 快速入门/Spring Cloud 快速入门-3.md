---
title: Spring Cloud 快速入门-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>上一篇带领大家初步了解了如何使用 Spring Boot 搭建框架，通过 Spring Boot 和传统的 SpringMVC 架构的对比，我们清晰地发现 Spring Boot 的好处，它使我们的代码更加简单，结构更加清晰。</p>
<p>从这一篇开始，我将带领大家更加深入的认识 Spring Boot，将 Spring Boot 涉及到东西进行拆解，从而了解 Spring Boot 的方方面面。学完本文后，读者可以基于 Spring Boot 搭建更加复杂的系统框架。</p>
<p>我们知道，Spring Boot 是一个大容器，它将很多第三方框架都进行了集成，我们在实际项目中用到哪个模块，再引入哪个模块。比如我们项目中的持久化框架用 MyBatis，则在 pom.xml 添加如下依赖：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;1.1.1&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;5.1.40&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre>
<h3 id="yamlproperties">yaml/properties 文件</h3>
<p>我们知道整个 Spring Boot 项目只有一个配置文件，那就是 application.yml，Spring Boot 在启动时，就会从 application.yml 中读取配置信息，并加载到内存中。上一篇我们只是粗略的列举了几个配置项，其实 Spring Boot 的配置项是很多的，本文我们将学习在实际项目中常用的配置项（注：为了方便说明，配置项均以 properties 文件的格式写出，后续的实际配置都会写成 yaml 格式）。</p>
<table>
<thead>
<tr>
<th>配置项</th>
<th>说明</th>
<th>举例</th>
</tr>
</thead>
<tbody>
<tr>
<td>server.port</td>
<td>应用程序启动端口</td>
<td>server.port=8080，定义应用程序启动端口为 8080</td>
</tr>
<tr>
<td>server.servlet.context-path</td>
<td>应用程序上下文</td>
<td>server.servlet.context-path=/api，则访问地址为：http://ip:port/api</td>
</tr>
<tr>
<td>spring.servlet.multipart.maxFileSize</td>
<td>最大文件上传大小，-1为不限制</td>
<td>spring.servlet.multipart.maxFileSize=-1</td>
</tr>
<tr>
<td>spring.jpa.database</td>
<td>数据库类型</td>
<td>spring.jpa.database=MYSQL，指定数据库为mysql</td>
</tr>
<tr>
<td>spring.jpa.properties.hibernate.dialect</td>
<td>hql方言</td>
<td>spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL5Dialect</td>
</tr>
<tr>
<td>spring.datasource.url</td>
<td>数据库连接字符串</td>
<td>spring.datasource.url=jdbc:mysql://localhost:3306/database?useUnicode=true&amp;characterEncoding=UTF-8&amp;useSSL=true</td>
</tr>
<tr>
<td>spring.datasource.username</td>
<td>数据库用户名</td>
<td>spring.datasource.username=root</td>
</tr>
<tr>
<td>spring.datasource.password</td>
<td>数据库密码</td>
<td>spring.datasource.password=root</td>
</tr>
<tr>
<td>spring.datasource.driverClassName</td>
<td>数据库驱动</td>
<td>spring.datasource.driverClassName=com.mysql.jdbc.Driver</td>
</tr>
<tr>
<td>spring.jpa.showSql</td>
<td>控制台是否打印 SQL 语句</td>
<td>spring.jpa.showSql=true</td>
</tr>
</tbody>
</table>
<p>下面是我参与的某个项目的 application.yml 配置文件内容：</p>
<pre><code class="yaml language-yaml">server:
  port: 8080
  servlet:
    context-path: /api
  tomcat:
    basedir: /data/tmp
    max-threads: 1000
    min-spare-threads: 50
  connection-timeout: 5000
spring:
  profiles:
    active: dev
  servlet:
    multipart:
      maxFileSize: -1
  datasource:
    url: jdbc:mysql://localhost:3306/database?useUnicode=true&amp;characterEncoding=UTF-8&amp;useSSL=true
    username: root
    password: root
    driverClassName: com.mysql.jdbc.Driver
  jpa:
    database: MYSQL
    showSql: true
    hibernate:
      namingStrategy: org.hibernate.cfg.ImprovedNamingStrategy
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL5Dialect
mybatis:
  configuration:
     #配置项：开启下划线到驼峰的自动转换. 作用：将数据库字段根据驼峰规则自动注入到对象属性
     map-underscore-to-camel-case: true
</code></pre>
<p>以上列举了常用的配置项，所有配置项信息都可以在<a href="https://docs.spring.io/spring-boot/docs/2.0.1.RELEASE/reference/htmlsingle/">官网</a>中找到，本课程就不一一列举了。</p>
<h3 id="">多环境配置</h3>
<p>在一个企业级系统中，我们可能会遇到这样一个问题：开发时使用开发环境，测试时使用测试环境，上线时使用生产环境。每个环境的配置都可能不一样，比如开发环境的数据库是本地地址，而测试环境的数据库是测试地址。那我们在打包的时候如何生成不同环境的包呢？</p>
<p>这里的解决方案有很多：</p>
<ol>
<li>每次编译之前手动把所有配置信息修改成当前运行的环境信息。这种方式导致每次都需要修改，相当麻烦，也容易出错。</li>
<li>利用 Maven，在 pom.xml 里配置多个环境，每次编译之前将 settings.xml 里面修改成当前要编译的环境 ID。这种方式会事先设置好所有环境，缺点就是每次也需要手动指定环境，如果环境指定错误，发布时是不知道的。</li>
<li>第三种方案就是本文重点介绍的，也是作者强烈推荐的方式。</li>
</ol>
<p>首先，创建 application.yml 文件，在里面添加如下内容：</p>
<pre><code class="yaml language-yaml">spring:
  profiles:
    active: dev
</code></pre>
<p>含义是指定当前项目的默认环境为 dev，即项目启动时如果不指定任何环境，Spring Boot 会自动从 dev 环境文件中读取配置信息。我们可以将不同环境都共同的配置信息写到这个文件中。</p>
<p>然后创建多环境配置文件，文件名的格式为：application-{profile}.yml，其中，{profile} 替换为环境名字，如 application-dev.yml，我们可以在其中添加当前环境的配置信息，如添加数据源：</p>
<pre><code class="yaml language-yaml">spring:
  datasource:
    url: jdbc:mysql://localhost:3306/database?useUnicode=true&amp;characterEncoding=UTF-8&amp;useSSL=true
    username: root
    password: root
    driverClassName: com.mysql.jdbc.Driver
</code></pre>
<p>这样，我们就实现了多环境的配置，每次编译打包我们无需修改任何东西，编译为 jar 文件后，运行命令：</p>
<pre><code class="shell language-shell">java -jar api.jar --spring.profiles.active=dev
</code></pre>
<p>其中 <code>--spring.profiles.active</code> 就是我们要指定的环境。</p>
<h3 id="-1">常用注解</h3>
<p>我们知道，Spring Boot 主要采用注解的方式，在《第01课：Spring Boot 入门》一节的入门实例中，我们也用到了一些注解。</p>
<p>本文，我将详细介绍在实际项目中常用的注解。</p>
<h4 id="springbootapplication"><code>@SpringBootApplication</code></h4>
<p>我们可以注意到 Spring Boot 支持 main 方法启动，在我们需要启动的主类中加入此注解，告诉 Spring Boot，这个类是程序的入口。如：</p>
<pre><code class="java language-java">@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
</code></pre>
<p>如果不加这个注解，程序是无法启动的。</p>
<p>我们查看下 SpringBootApplication 的源码，源码如下：</p>
<pre><code class="java language-java">@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
        @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
        @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {

    /**
     * Exclude specific auto-configuration classes such that they will never be applied.
     * @return the classes to exclude
     */
    @AliasFor(annotation = EnableAutoConfiguration.class, attribute = "exclude")
    Class&lt;?&gt;[] exclude() default {};

    /**
     * Exclude specific auto-configuration class names such that they will never be
     * applied.
     * @return the class names to exclude
     * @since 1.3.0
     */
    @AliasFor(annotation = EnableAutoConfiguration.class, attribute = "excludeName")
    String[] excludeName() default {};

    /**
     * Base packages to scan for annotated components. Use {@link #scanBasePackageClasses}
     * for a type-safe alternative to String-based package names.
     * @return base packages to scan
     * @since 1.3.0
     */
    @AliasFor(annotation = ComponentScan.class, attribute = "basePackages")
    String[] scanBasePackages() default {};

    /**
     * Type-safe alternative to {@link #scanBasePackages} for specifying the packages to
     * scan for annotated components. The package of each class specified will be scanned.
     * &lt;p&gt;
     * Consider creating a special no-op marker class or interface in each package that
     * serves no purpose other than being referenced by this attribute.
     * @return base packages to scan
     * @since 1.3.0
     */
    @AliasFor(annotation = ComponentScan.class, attribute = "basePackageClasses")
    Class&lt;?&gt;[] scanBasePackageClasses() default {};

}
</code></pre>
<p>在这个注解类上有 3 个注解，如下：</p>
<pre><code>@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
        @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
        @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
</code></pre>
<p>因此，我们可以用这三个注解代替 SpringBootApplication，如：</p>
<pre><code class="java language-java">@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
</code></pre>
<p>其中，SpringBootConfiguration 表示 Spring Boot 的配置注解，EnableAutoConfiguration 表示自动配置，ComponentScan 表示 Spring Boot 扫描 Bean 的规则，比如扫描哪些包。</p>
<h4 id="configuration"><code>@Configuration</code></h4>
<p>加入了这个注解的类被认为是 Spring Boot 的配置类，我们知道可以在 application.yml 设置一些配置，也可以通过代码设置配置。</p>
<p>如果我们要通过代码设置配置，就必须在这个类上标注 Configuration 注解。如下代码：</p>
<pre><code class="java language-java">@Configuration
public class WebConfig extends WebMvcConfigurationSupport{

    @Override
    protected void addInterceptors(InterceptorRegistry registry) {
        super.addInterceptors(registry);
        registry.addInterceptor(new ApiInterceptor());
    }
}
</code></pre>
<p>不过 Spring Boot 官方推荐 Spring Boot 项目用 SpringBootConfiguration 来代替 Configuration。</p>
<h4 id="bean"><code>@Bean</code></h4>
<p>这个注解是方法级别上的注解，主要添加在 <code>@Configuration</code> 或 <code>@SpringBootConfiguration</code> 注解的类，有时也可以添加在 <code>@Component</code> 注解的类。它的作用是定义一个Bean。</p>
<p>请看下面代码：</p>
<pre><code class="java language-java">    @Bean
    public ApiInterceptor interceptor(){
        return new ApiInterceptor();
    }
</code></pre>
<p>那么，我们可以在 ApiInterceptor 里面注入其他 Bean，也可以在其他 Bean 注入这个类。</p>
<h4 id="value"><code>@Value</code></h4>
<p>通常情况下，我们需要定义一些全局变量，都会想到的方法是定义一个 public static 变量，在需要时调用，是否有其他更好的方案呢？答案是肯定的。下面请看代码：</p>
<pre><code class="java language-java">    @Value("${server.port}")
    String port;
    @RequestMapping("/hello")
    public String home(String name) {
        return "hi "+name+",i am from port:" +port;
    }
</code></pre>
<p>其中，server.port 就是我们在 application.yml 里面定义的属性，我们可以自定义任意属性名，通过 <code>@Value</code> 注解就可以将其取出来。</p>
<p>它的好处不言而喻：</p>
<ol>
<li>定义在配置文件里，变量发生变化，无需修改代码。</li>
<li>变量交给Spring来管理，性能更好。</li>
</ol>
<blockquote>
  <p><strong>注：</strong> 本课程默认针对于对 SpringMVC 有所了解的读者，Spring Boot 本身基于 Spring 开发的，因此，本文不再讲解其他 Spring 的注解。</p>
</blockquote>
<h3 id="-2">注入任何类</h3>
<p>本节通过一个实际的例子来讲解如何注入一个普通类，并且说明这样做的好处。</p>
<p>假设一个需求是这样的：项目要求使用阿里云的 OSS 进行文件上传。</p>
<p>我们知道，一个项目一般会分为开发环境、测试环境和生产环境。OSS 文件上传一般有如下几个参数：appKey、appSecret、bucket、endpoint 等。不同环境的参数都可能不一样，这样便于区分。按照传统的做法，我们在代码里设置这些参数，这样做的话，每次发布不同的环境包都需要手动修改代码。</p>
<p>这个时候，我们就可以考虑将这些参数定义到配置文件里面，通过前面提到的 <code>@Value</code> 注解取出来，再通过 <code>@Bean</code> 将其定义为一个 Bean，这时我们只需要在需要使用的地方注入该 Bean 即可。</p>
<p>首先在 application.yml 加入如下内容：</p>
<pre><code class="yaml language-yaml">oss:
  appKey: 1
  appSecret: 1
  bucket: lynn
  endPoint: https://www.aliyun.com
</code></pre>
<p>其次创建一个普通类：</p>
<pre><code class="java language-java">public class Aliyun {

    private String appKey;

    private String appSecret;

    private String bucket;

    private String endPoint;

    public static class Builder{

        private String appKey;

        private String appSecret;

        private String bucket;

        private String endPoint;

        public Builder setAppKey(String appKey){
            this.appKey = appKey;
            return this;
        }

        public Builder setAppSecret(String appSecret){
            this.appSecret = appSecret;
            return this;
        }

        public Builder setBucket(String bucket){
            this.bucket = bucket;
            return this;
        }

        public Builder setEndPoint(String endPoint){
            this.endPoint = endPoint;
            return this;
        }

        public Aliyun build(){
            return new Aliyun(this);
        }
    }

    public static Builder options(){
        return new Aliyun.Builder();
    }

    private Aliyun(Builder builder){
        this.appKey = builder.appKey;
        this.appSecret = builder.appSecret;
        this.bucket = builder.bucket;
        this.endPoint = builder.endPoint;
    }

    public String getAppKey() {
        return appKey;
    }

    public String getAppSecret() {
        return appSecret;
    }

    public String getBucket() {
        return bucket;
    }

    public String getEndPoint() {
        return endPoint;
    }
}
</code></pre>
<p>然后在 <code>@SpringBootConfiguration</code> 注解的类添加如下代码：</p>
<pre><code class="java language-java">    @Value("${oss.appKey}")
    private String appKey;
    @Value("${oss.appSecret}")
    private String appSecret;
    @Value("${oss.bucket}")
    private String bucket;
    @Value("${oss.endPoint}")
    private String endPoint;

    @Bean
    public Aliyun aliyun(){
        return Aliyun.options()
                .setAppKey(appKey)
                .setAppSecret(appSecret)
                .setBucket(bucket)
                .setEndPoint(endPoint)
                .build();
    }
</code></pre>
<p>最后在需要的地方注入这个 Bean 即可：</p>
<pre><code class="java language-java">    @Autowired
    private Aliyun aliyun;
</code></pre>
<p>以上代码其实并不完美，如果增加一个属性，就需要在 Aliyun 类新增一个字段，还需要在 Configuration 类里注入它，扩展性不好，那么我们有没有更好的方式呢？</p>
<p>答案是肯定的，我们可以利用 ConfigurationProperties 注解更轻松地将配置信息注入到实体中。</p>
<p>1.创建实体类 AliyunAuto，并编写以下代码：</p>
<pre><code>import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "oss")
public class AliyunAuto {

    private String appKey;

    private String appSecret;

    private String bucket;

    private String endPoint;

    public String getAppKey() {
        return appKey;
    }

    public void setAppKey(String appKey) {
        this.appKey = appKey;
    }

    public String getAppSecret() {
        return appSecret;
    }

    public void setAppSecret(String appSecret) {
        this.appSecret = appSecret;
    }

    public String getBucket() {
        return bucket;
    }

    public void setBucket(String bucket) {
        this.bucket = bucket;
    }

    public String getEndPoint() {
        return endPoint;
    }

    public void setEndPoint(String endPoint) {
        this.endPoint = endPoint;
    }

    @Override
    public String toString() {
        return "AliyunAuto{" +
                "appKey='" + appKey + '\'' +
                ", appSecret='" + appSecret + '\'' +
                ", bucket='" + bucket + '\'' +
                ", endPoint='" + endPoint + '\'' +
                '}';
    }
}
</code></pre>
<p>其中，ConfigurationProperties 指定配置文件的前缀属性，实体具体字段和配置文件字段名一致，如在上述代码中，字段为 appKey，则自动获取 oss.appKey 的值，将其映射到 appKey 字段中，这样就完成了自动的注入。如果我们增加一个属性，则只需要修改 Bean 和配置文件即可，不用显示注入。</p>
<h3 id="-3">拦截器</h3>
<p>我们在提供 API 的时候，经常需要对 API 进行统一的拦截，比如进行接口的安全性校验。</p>
<p>本节，我会讲解 Spring Boot 是如何进行拦截器设置的，请看接下来的代码。</p>
<p>创建一个拦截器类：ApiInterceptor，并实现 HandlerInterceptor 接口：</p>
<pre><code class="java language-java">public class ApiInterceptor implements HandlerInterceptor {
    //请求之前
    @Override
    public boolean preHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o) throws Exception {
        System.out.println("进入拦截器");
        return true;
    }
    //请求时
    @Override
    public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {

    }
    //请求完成
    @Override
    public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {

    }
}
</code></pre>
<p><code>@SpringBootConfiguration</code> 注解的类继承 WebMvcConfigurationSupport 类，并重写 addInterceptors 方法，将 ApiInterceptor 拦截器类添加进去，代码如下：</p>
<pre><code class="java language-java">@SpringBootConfiguration
public class WebConfig extends WebMvcConfigurationSupport{

    @Override
    protected void addInterceptors(InterceptorRegistry registry) {
        super.addInterceptors(registry);
        registry.addInterceptor(new ApiInterceptor());
    }
}
</code></pre>
<h3 id="-4">异常处理</h3>
<p>我们在 Controller 里提供接口，通常需要捕捉异常，并进行友好提示，否则一旦出错，界面上就会显示报错信息，给用户一种不好的体验。最简单的做法就是每个方法都使用 try catch 进行捕捉，报错后，则在 catch 里面设置友好的报错提示。如果方法很多，每个都需要 try catch，代码会显得臃肿，写起来也比较麻烦。</p>
<p>我们可不可以提供一个公共的入口进行统一的异常处理呢？当然可以。方法很多，这里我们通过 Spring 的 AOP 特性就可以很方便的实现异常的统一处理。实现方法很简单，只需要在 Controller 类添加以下代码即可。</p>
<pre><code class="java language-java">    @ExceptionHandler
    public String doError(Exception ex) throws Exception{
        ex.printStackTrace();
        return ex.getMessage();
    }
</code></pre>
<p>其中，在 doError 方法上加入 @ExceptionHandler 注解即可，这样，接口发生异常会自动调用该方法。</p>
<p>这样，我们无需每个方法都添加 try catch，一旦报错，则会执行 handleThrowing 方法。</p>
<h3 id="-5">优雅的输入合法性校验</h3>
<p>为了接口的健壮性，我们通常除了客户端进行输入合法性校验外，在 Controller 的方法里，我们也需要对参数进行合法性校验，传统的做法是每个方法的参数都做一遍判断，这种方式和上一节讲的异常处理一个道理，不太优雅，也不易维护。</p>
<p>其实，SpringMVC 提供了验证接口，下面请看代码：</p>
<pre><code class="java language-java">@GetMapping("authorize")
public void authorize(@Valid AuthorizeIn authorize, BindingResult ret){
    if(result.hasFieldErrors()){
            List&lt;FieldError&gt; errorList = result.getFieldErrors();
            //通过断言抛出参数不合法的异常
            errorList.stream().forEach(item -&gt; Assert.isTrue(false,item.getDefaultMessage()));
        }
}
public class AuthorizeIn extends BaseModel{

    @NotBlank(message = "缺少response_type参数")
    private String responseType;
    @NotBlank(message = "缺少client_id参数")
    private String ClientId;

    private String state;

    @NotBlank(message = "缺少redirect_uri参数")
    private String redirectUri;

    public String getResponseType() {
        return responseType;
    }

    public void setResponseType(String responseType) {
        this.responseType = responseType;
    }

    public String getClientId() {
        return ClientId;
    }

    public void setClientId(String clientId) {
        ClientId = clientId;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getRedirectUri() {
        return redirectUri;
    }

    public void setRedirectUri(String redirectUri) {
        this.redirectUri = redirectUri;
    }
}
</code></pre>
<p>我们再把验证的代码单独封装成方法：</p>
<pre><code class="java language-java">protected void validate(BindingResult result){
        if(result.hasFieldErrors()){
            List&lt;FieldError&gt; errorList = result.getFieldErrors();
            errorList.stream().forEach(item -&gt; Assert.isTrue(false,item.getDefaultMessage()));
        }
    }
</code></pre>
<p>这样每次参数校验只需要调用 validate 方法就行了，我们可以看到代码的可读性也大大提高了。</p>
<h3 id="-6">接口版本控制</h3>
<p>一个系统上线后会不断迭代更新，需求也会不断变化，有可能接口的参数也会发生变化，如果在原有的参数上直接修改，可能会影响线上系统的正常运行，这时我们就需要设置不同的版本，这样即使参数发生变化，由于老版本没有变化，因此不会影响上线系统的运行。</p>
<p>一般我们可以在地址上带上版本号，也可以在参数上带上版本号，还可以再 header 里带上版本号，这里我们在地址上带上版本号，大致的地址如：http://api.example.com/v1/test，其中，v1 即代表的是版本号。具体做法请看代码：</p>
<pre><code class="java language-java">@Target({ElementType.METHOD,ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Mapping
public @interface ApiVersion {

    /**
     * 标识版本号
     * @return
     */
    int value();
}
public class ApiVersionCondition implements RequestCondition&lt;ApiVersionCondition&gt; {

    // 路径中版本的前缀， 这里用 /v[1-9]/的形式
    private final static Pattern VERSION_PREFIX_PATTERN = Pattern.compile("v(\\d+)/");

    private int apiVersion;

    public ApiVersionCondition(int apiVersion){
        this.apiVersion = apiVersion;
    }

    @Override
    public ApiVersionCondition combine(ApiVersionCondition other) {
        // 采用最后定义优先原则，则方法上的定义覆盖类上面的定义
        return new ApiVersionCondition(other.getApiVersion());
    }

    @Override
    public ApiVersionCondition getMatchingCondition(HttpServletRequest request) {
        Matcher m = VERSION_PREFIX_PATTERN.matcher(request.getRequestURI());
        if(m.find()){
            Integer version = Integer.valueOf(m.group(1));
            if(version &gt;= this.apiVersion)
            {
                return this;
            }
        }
        return null;
    }

    @Override
    public int compareTo(ApiVersionCondition other, HttpServletRequest request) {
        // 优先匹配最新的版本号
        return other.getApiVersion() - this.apiVersion;
    }

    public int getApiVersion() {
        return apiVersion;
    }
}
public class CustomRequestMappingHandlerMapping extends
        RequestMappingHandlerMapping {

    @Override
    protected RequestCondition&lt;ApiVersionCondition&gt; getCustomTypeCondition(Class&lt;?&gt; handlerType) {
        ApiVersion apiVersion = AnnotationUtils.findAnnotation(handlerType, ApiVersion.class);
        return createCondition(apiVersion);
    }

    @Override
    protected RequestCondition&lt;ApiVersionCondition&gt; getCustomMethodCondition(Method method) {
        ApiVersion apiVersion = AnnotationUtils.findAnnotation(method, ApiVersion.class);
        return createCondition(apiVersion);
    }

    private RequestCondition&lt;ApiVersionCondition&gt; createCondition(ApiVersion apiVersion) {
        return apiVersion == null ? null : new ApiVersionCondition(apiVersion.value());
    }
}
@SpringBootConfiguration
public class WebConfig extends WebMvcConfigurationSupport {

    @Bean
    public AuthInterceptor interceptor(){
        return new AuthInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor());
    }

    @Override
    @Bean
    public RequestMappingHandlerMapping requestMappingHandlerMapping() {
        RequestMappingHandlerMapping handlerMapping = new CustomRequestMappingHandlerMapping();
        handlerMapping.setOrder(0);
        handlerMapping.setInterceptors(getInterceptors());
        return handlerMapping;
    }
}
</code></pre>
<p>Controller 类的接口定义如下：</p>
<pre><code class="java language-java">@ApiVersion(1)
@RequestMapping("{version}/dd")
public class HelloController{}
</code></pre>
<p>这样我们就实现了版本控制，如果增加了一个版本，则创建一个新的 Controller，方法名一致，ApiVersion 设置为2，则地址中 v1 会找到 ApiVersion 为1的方法，v2 会找到 ApiVersion 为2的方法。</p>
<h3 id="json">自定义 JSON 解析</h3>
<p>Spring Boot 中 RestController 返回的字符串默认使用 Jackson 引擎，它也提供了工厂类，我们可以自定义 JSON 引擎，本节实例我们将 JSON 引擎替换为 fastJSON，首先需要引入 fastJSON：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
            &lt;artifactId&gt;fastjson&lt;/artifactId&gt;
            &lt;version&gt;${fastjson.version}&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre>
<p>其次，在 WebConfig 类重写 configureMessageConverters 方法：</p>
<pre><code class="java language-java">@Override
    public void configureMessageConverters(List&lt;HttpMessageConverter&lt;?&gt;&gt; converters) {
        super.configureMessageConverters(converters);
        /*
        1.需要先定义一个 convert 转换消息的对象；
        2.添加 fastjson 的配置信息，比如是否要格式化返回的 JSON 数据
        3.在 convert 中添加配置信息
        4.将 convert 添加到 converters 中
         */
        //1.定义一个 convert 转换消息对象
        FastJsonHttpMessageConverter fastConverter=new FastJsonHttpMessageConverter();
        //2.添加 fastjson 的配置信息，比如是否要格式化返回 JSON 数据
        FastJsonConfig fastJsonConfig=new FastJsonConfig();
        fastJsonConfig.setSerializerFeatures(
                SerializerFeature.PrettyFormat
        );
        fastConverter.setFastJsonConfig(fastJsonConfig);
        converters.add(fastConverter);
    }
</code></pre>
<h3 id="-7">单元测试</h3>
<p>Spring Boot 的单元测试很简单，直接看代码：</p>
<pre><code class="java language-java">@SpringBootTest(classes = DemoApplication.class)
@RunWith(SpringJUnit4ClassRunner.class)
public class TestDB {

    @Test
    public void test(){
    }
}
</code></pre>
<h3 id="-8">模板引擎</h3>
<p>在传统的 SpringMVC 架构中，我们一般将 JSP、HTML 页面放到 webapps 目录下面，但是 Spring Boot 没有 webapps，更没有 web.xml，如果我们要写界面的话，该如何做呢？</p>
<p>Spring Boot 官方提供了几种模板引擎：FreeMarker、Velocity、Thymeleaf、Groovy、mustache、JSP。</p>
<p>这里以 FreeMarker 为例讲解 Spring Boot 的使用。</p>
<p>首先引入 FreeMarker 依赖：</p>
<pre><code class="xml language-xml">    &lt;dependency&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-freemarker&lt;/artifactId&gt;
    &lt;/dependency&gt;
</code></pre>
<p>在 resources 下面建立两个目录：static 和 templates，如图所示：</p>
<p><img src="http://images.gitbook.cn/74c66370-535e-11e8-ab64-81de3901ec9a" alt="这里写图片描述" /></p>
<p>其中 static 目录用于存放静态资源，譬如 CSS、JS、HTML 等，templates 目录存放模板引擎文件，我们可以在 templates 下面创建一个文件：index.ftl（freemarker 默认后缀为 <code>.ftl</code>），并添加内容：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html&gt;
    &lt;head&gt;

    &lt;/head&gt;
    &lt;body&gt;
        &lt;h1&gt;Hello World!&lt;/h1&gt;
    &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>然后创建 PageController 并添加内容：</p>
<pre><code class="java language-java">@Controller
public class PageController {

    @RequestMapping("index.html")
    public String index(){
        return "index";
    }
}
</code></pre>
<p>启动 Application.java，访问：http://localhost:8081/api/index.html，就可以看到如图所示：</p>
<p><img src="https://images.gitbook.cn/23c18b90-3e85-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<blockquote>
  <p><a href="https://gitbook.cn/gitchat/column/5af108d20a989b69c385f47a?utm_source=lysd001">点击了解《Spring Cloud 快速入门》，解决更多实际问题</a>。</p>
</blockquote></div></article>