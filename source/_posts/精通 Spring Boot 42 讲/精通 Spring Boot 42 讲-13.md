---
title: 精通 Spring Boot 42 讲-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在互联网行业中上传文件是一个高频的使用场景，常用的案例有上传头像、上传身份证信息等。Spring Boot 利用 MultipartFile 的特性来接收和处理上传的文件，MultipartFile 是 Spring 的一个封装的接口，封装了文件上传的相关操作，利用 MultipartFile 可以方便地接收前端文件，将接收到的文件存储到本机或者其他中间件中。</p>
<p>首先通过一个小的示例来了解 Spring Boot 对上传文件的支持，项目前端页面使用 Thymeleaf 来处理。</p>
<h3 id="">快速上手</h3>
<h4 id="-1">添加依赖包</h4>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
&lt;/dependency&gt;
</code></pre>
<p>引入了 spring-boot-starter-thymeleaf 做页面模板引擎。</p>
<h4 id="-2">配置信息</h4>
<p>常用配置内容，单位支持 MB 或者 KB：</p>
<pre><code>#支持的最大文件
spring.servlet.multipart.max-file-size=100MB
#文件请求最大限制
spring.servlet.multipart.max-request-size=100MB
</code></pre>
<p>以上配置主要是通过设置 MultipartFile 的属性来控制上传限制，MultipartFile 是 Spring 上传文件的封装类，包含了文件的二进制流和文件属性等信息，在配置文件中也可对相关属性进行配置。</p>
<p>除过以上配置，常用的配置信息如下：</p>
<ul>
<li>spring.servlet.multipart.enabled=true，是否支持 multipart 上传文件</li>
<li>spring.servlet.multipart.file-size-threshold=0，支持文件写入磁盘</li>
<li>spring.servlet.multipart.location=，上传文件的临时目录</li>
<li>spring.servlet.multipart.max-file-size=10Mb，最大支持文件大小</li>
<li>spring.servlet.multipart.max-request-sizee=10Mb，最大支持请求大小</li>
<li>spring.servlet.multipart.resolve-lazily=false，是否支持 multipart 上传文件时懒加载</li>
</ul>
<h4 id="-3">启动类</h4>
<pre><code class="java language-java">@SpringBootApplication
public class FileUploadWebApplication {

    public static void main(String[] args) throws Exception {
        SpringApplication.run(FileUploadWebApplication.class, args);
    }

    //Tomcat large file upload connection reset
    @Bean
    public TomcatServletWebServerFactory tomcatEmbedded() {
        TomcatServletWebServerFactory tomcat = new TomcatServletWebServerFactory();
        tomcat.addConnectorCustomizers((TomcatConnectorCustomizer) connector -&gt; {
            if ((connector.getProtocolHandler() instanceof AbstractHttp11Protocol&lt;?&gt;)) {
                //-1 means unlimited
                ((AbstractHttp11Protocol&lt;?&gt;) connector.getProtocolHandler()).setMaxSwallowSize(-1);
            }
        });
        return tomcat;
    }

}
</code></pre>
<p>TomcatServletWebServerFactory() 方法主要是为了解决上传文件大于 10M 出现连接重置的问题，此异常内容 GlobalException 也捕获不到。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/connect_rest.png" alt="" /></p>
<h4 id="-4">编写前端页面</h4>
<p>上传页面：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html xmlns:th="http://www.thymeleaf.org"&gt;
&lt;body&gt;
&lt;h1&gt;Spring Boot file upload example&lt;/h1&gt;
&lt;form method="POST" action="/upload" enctype="multipart/form-data"&gt;
    &lt;input type="file" name="file" /&gt;&lt;br/&gt;&lt;br/&gt;
    &lt;input type="submit" value="Submit" /&gt;
&lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>非常简单的一个 Post 请求，一个选择框选择文件、一个提交按钮，效果如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/upload_submit.png" alt="" /></p>
<p>上传结果展示页面：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;body&gt;
&lt;h1&gt;Spring Boot - Upload Status&lt;/h1&gt;
&lt;div th:if="${message}"&gt;
    &lt;h2 th:text="${message}"/&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>效果图如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/uploadstatus.png" alt="" /></p>
<h4 id="-5">编写上传控制类</h4>
<p>访问 localhost:8080 自动跳转到上传页面：</p>
<pre><code class="java language-java">@GetMapping("/")
public String index() {
    return "upload";
}
</code></pre>
<p>上传业务处理：</p>
<pre><code class="java language-java">@PostMapping("/upload") 
public String singleFileUpload(@RequestParam("file") MultipartFile file,
                               RedirectAttributes redirectAttributes) {
    if (file.isEmpty()) {
        redirectAttributes.addFlashAttribute("message", "Please select a file to upload");
        return "redirect:uploadStatus";
    }
    try {
        // Get the file and save it somewhere
        byte[] bytes = file.getBytes();
        // UPLOADED_FOLDER 文件本地存储地址
        Path path = Paths.get(UPLOADED_FOLDER + file.getOriginalFilename());
        Files.write(path, bytes);

        redirectAttributes.addFlashAttribute("message",
                "You successfully uploaded '" + file.getOriginalFilename() + "'");

    } catch (IOException e) {
        e.printStackTrace();
    }
    return "redirect:/uploadStatus";
}
</code></pre>
<p>上面代码的意思就是，通过 MultipartFile 读取文件信息，如果文件为空跳转到结果页并给出提示；如果不为空读取文件流并写入到指定目录，最后将结果展示到页面。最常用的是最后两个配置内容，限制文件上传大小，上传时超过大小会抛出异常：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/uploadmax.png" alt="" /></p>
<p>当然在真实的项目中我们可以在业务中会首先对文件大小进行判断，再将返回信息展示到页面。</p>
<h4 id="-6">异常处理</h4>
<p>这里演示的是 MultipartException 的异常处理，也可以稍微改造监控整个项目的异常问题。</p>
<pre><code class="java language-java">@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MultipartException.class)
    public String handleError1(MultipartException e, RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("message", e.getCause().getMessage());
        return "redirect:/uploadStatus";
    }
}
</code></pre>
<p>设置一个 @ControllerAdvice 用来监控 Multipart 上传的文件大小是否受限，当出现此异常时在前端页面给出提示。利用 @ControllerAdvice 可以做很多东西，比如全局的统一异常处理等，感兴趣的读者可以抽空了解一下。</p>
<h3 id="-7">上传多个文件</h3>
<p>在项目中经常会有一次性上传多个文件的需求，我们稍作修改即可支持。</p>
<h4 id="-8">前端页面</h4>
<p>首先添加可以支持上传多文件的页面，内容如下：</p>
<pre><code class="html language-html">&lt;!DOCTYPE html&gt;
&lt;html xmlns:th="http://www.thymeleaf.org"&gt;
&lt;body&gt;
&lt;h1&gt;Spring Boot files upload example&lt;/h1&gt;
&lt;form method="POST" action="/uploadMore" enctype="multipart/form-data"&gt;
    文件1： &lt;input type="file" name="file" /&gt;&lt;br/&gt;&lt;br/&gt;
    文件2： &lt;input type="file" name="file" /&gt;&lt;br/&gt;&lt;br/&gt;
    文件3： &lt;input type="file" name="file" /&gt;&lt;br/&gt;&lt;br/&gt;
    &lt;input type="submit" value="Submit" /&gt;
&lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<h4 id="-9">后端处理</h4>
<p>后端添加页面访问入口：</p>
<pre><code class="java language-java">@GetMapping("/more")
public String uploadMore() {
    return "uploadMore";
}
</code></pre>
<p>在浏览器中输入网址，http://localhost:8080/more，就会进入此页面。</p>
<p>MultipartFile 需要修改为按照数组的方式去接收。</p>
<pre><code class="java language-java">@PostMapping("/uploadMore")
public String moreFileUpload(@RequestParam("file") MultipartFile[] files,
                               RedirectAttributes redirectAttributes) {
    if (files.length==0) {
        redirectAttributes.addFlashAttribute("message", "Please select a file to upload");
        return "redirect:uploadStatus";
    }
    for(MultipartFile file:files){
        try {
            byte[] bytes = file.getBytes();
            Path path = Paths.get(UPLOADED_FOLDER + file.getOriginalFilename());
            Files.write(path, bytes);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    redirectAttributes.addFlashAttribute("message", "You successfully uploaded all");
    return "redirect:/uploadStatus";
}
</code></pre>
<p>同样是先判断数组是否为空，在循环遍历数组内容将文件写入到指定目录下。在浏览器中输入网址 http://localhost:8080/more，选择三个文件进行测试，当页面出现以下信息时表示上传成功。</p>
<pre><code>Spring Boot - Upload Status
You successfully uploaded all
</code></pre>
<h3 id="-10">总结</h3>
<p>经过本课的内容发现 Spring Boot 完美支持文件上传，不论是单个文件上传还是多个文件上传都很简单。在上传文件的过程中也可以通过配置文件来选择关闭或者限制上传文件大小，利用 @ControllerAdvice 可以灵活地对异常进行全局处理。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote>
<p>参考资料：<a href="https://www.mkyong.com/spring-boot/spring-boot-file-upload-example/">Spring Boot file upload example</a></p></div></article>