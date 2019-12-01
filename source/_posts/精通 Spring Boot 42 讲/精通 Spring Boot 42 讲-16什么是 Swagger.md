---
title: 精通 Spring Boot 42 讲-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="swagger">什么是 Swagger</h3>
<p>Swagger 是一系列 RESTful API 的工具，通过 Swagger 可以获得项目的一种交互式文档，客户端 SDK 的自动生成等功能。</p>
<p>Swagger 的目标是为 REST APIs 定义一个标准的、与语言无关的接口，使人和计算机在看不到源码或者看不到文档或者不能通过网络流量检测的情况下，能发现和理解各种服务的功能。当服务通过 Swagger 定义，消费者就能与远程的服务互动通过少量的实现逻辑。类似于低级编程接口，Swagger 去掉了调用服务时的很多猜测。 </p>
<p>Swagger（丝袜哥）是世界上最流行的 API 表达工具。</p>
<p>Swagger 是一个简单但功能强大的 API 表达工具。它具有地球上最大的 API 工具生态系统，数以千计的开发人员，使用几乎所有的现代编程语言，都在支持和使用 Swagger。使用 Swagger 生成 API，我们可以得到交互式文档，自动生成代码的 SDK 以及 API 的发现特性等。</p>
<p>使用 Spring Boot 集成 Swagger 的理念是，使用注解来标记出需要在 API 文档中展示的信息，Swagger 会根据项目中标记的注解来生成对应的 API 文档。Swagger 被号称世界上最流行的 API 工具，它提供了 API 管理的全套解决方案，API 文档管理需要考虑的因素基本都包含，这里将讲解最常用的定制内容。</p>
<h3 id="">快速上手</h3>
<p>Spring Boot 集成 Swagger 2.X 很简单，需要引入依赖并做基础配置即可，下面我们来感受一下。</p>
<h4 id="-1">添加依赖包</h4>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;io.springfox&lt;/groupId&gt;
    &lt;artifactId&gt;springfox-swagger2&lt;/artifactId&gt;
    &lt;version&gt;2.8.0&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;io.springfox&lt;/groupId&gt;
    &lt;artifactId&gt;springfox-swagger-ui&lt;/artifactId&gt;
    &lt;version&gt;2.8.0&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<h4 id="swaggerconfig">创建 SwaggerConfig 配置类</h4>
<pre><code class="java language-java">@Configuration
@EnableSwagger2
public class SwaggerConfig {
}
</code></pre>
<p>在 SwaggerConfig 的类上添加两个注解：</p>
<ul>
<li>@Configuration，启动时加载此类</li>
<li>@EnableSwagger2，表示此项目启用 Swagger API 文档</li>
</ul>
<p>在 SwaggerConfig 中添加两个方法：</p>
<pre><code class="java language-java">@Bean
public Docket api() {
    return new Docket(DocumentationType.SWAGGER_2)
            .apiInfo(apiInfo())
            .select()
            // 自行修改为自己的包路径
            .apis(RequestHandlerSelectors.basePackage("com.neo.xxx"))
            .paths(PathSelectors.any())
            .build();
}
</code></pre>
<p>此方法使用 @Bean，在启动时初始化，返回实例 Docket（Swagger API 摘要），这里需要注意的是 .apis(RequestHandlerSelectors.basePackage("com.neo.xxx")) 指定需要扫描的包路径，只有此路径下的 Controller 类才会自动生成 Swagger API 文档。</p>
<pre><code class="java language-java">private ApiInfo apiInfo() {
    return new ApiInfoBuilder()
            .title("客户管理")
            .description("客户管理中心 API 1.0 操作文档")
            //服务条款网址
            .termsOfServiceUrl("http://www.ityouknow.com/")
            .version("1.0")
            .contact(new Contact("纯洁的微笑", "http://www.ityouknow.com/", "ityouknow@126.com"))
            .build();
}
</code></pre>
<p>这块配置相对重要一些，主要配置页面展示的基本信息包括，标题、描述、版本、服务条款、联系方式等，查看 ApiInfo 类的源码还会发现支持 license 配置等。</p>
<pre><code class="java language-java">public class ApiInfo {
    public static final Contact DEFAULT_CONTACT = new Contact("", "", "");
    public static final ApiInfo DEFAULT;
    private final String version;
    private final String title;
    private final String description;
    private final String termsOfServiceUrl;
    private final String license;
    private final String licenseUrl;
    private final Contact contact;
    private final List&lt;VendorExtension&gt; vendorExtensions;
    //...

}
</code></pre>
<p>以上信息皆可在此方法进行配置，也可以使用默认值。配置完成之后启动项目，在浏览器中输入网址 http://localhost:8080/swagger-ui.html，即可看到上面的配置信息，效果如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger1.png" alt="" /></p>
<p>访问地址后，发现页面存在这样一句话：No operations defined in spec!，意思是没有找到相关的 API 内容，这是因为还没有添加对应的 Controller 信息，接下来结合代码一一介绍各个注解的使用。</p>
<h3 id="swagger-1">Swagger 常用注解</h3>
<p>Swagger 通过注解表明该接口会生成文档，包括接口名、请求方法、参数、返回信息等，常用注解内容如下：</p>
<table>
<thead>
<tr>
<th>作用范围</th>
<th>API</th>
<th>使用位置</th>
</tr>
</thead>
<tbody>
<tr>
<td>协议集描述</td>
<td>@Api</td>
<td>用于 Controller 类上</td>
</tr>
<tr>
<td>协议描述</td>
<td>@ApiOperation</td>
<td>用在 Controller 的方法上</td>
</tr>
<tr>
<td>非对象参数集</td>
<td>@ApiImplicitParams</td>
<td>用在 Controller 的方法上</td>
</tr>
<tr>
<td>非对象参数描述</td>
<td>@ApiImplicitParam</td>
<td>用在 @ApiImplicitParams 的方法里边</td>
</tr>
<tr>
<td>响应集</td>
<td>@ApiResponses</td>
<td>用在 Controller 的方法上</td>
</tr>
<tr>
<td>响应信息参数</td>
<td>@ApiResponse</td>
<td>用在 @ApiResponses 里边</td>
</tr>
<tr>
<td>描述返回对象的意义</td>
<td>@ApiModel</td>
<td>用在返回对象类上</td>
</tr>
<tr>
<td>对象属性</td>
<td>@ApiModelProperty</td>
<td>用在出入参数对象的字段上</td>
</tr>
</tbody>
</table>
<p>在第 2-8 课讲解的示例项目基础上，添加 RESTful API 文档示例。</p>
<h4 id="api">@Api 的使用</h4>
<p>Api 作用在 Controller 类上，做为 Swagger 文档资源，该注解将一个 Controller（Class）标注为一个 Swagger 资源（API）。在默认情况下，Swagger-Core 只会扫描解析具有 @Api 注解的类，而会自动忽略其他类别资源（JAX-RS endpoints、Servlets 等）的注解。</p>
<p>使用示例：</p>
<pre><code class="java language-java">@Api(value = "消息", description = "消息操作 API", position = 100, protocols = "http")
@RestController
@RequestMapping("/")
public class MessageController {
}
</code></pre>
<p>与 Controller 注解并列使用，属性配置如表所示：</p>
<table>
<thead>
<tr>
<th>属性名称</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>value</td>
<td>url 的路径值</td>
</tr>
<tr>
<td>tags</td>
<td>如果设置这个值，value 的值会被覆盖</td>
</tr>
<tr>
<td>description</td>
<td>对 API 资源的描述</td>
</tr>
<tr>
<td>produces</td>
<td>For example, "application/json, application/xml"</td>
</tr>
<tr>
<td>consumes</td>
<td>For example, "application/json, application/xml"</td>
</tr>
<tr>
<td>protocols</td>
<td>Possible values: http, https, ws, wss</td>
</tr>
<tr>
<td>authorizations</td>
<td>高级特性认证时配置</td>
</tr>
<tr>
<td>hidden</td>
<td>配置为 true 将在文档中隐藏</td>
</tr>
</tbody>
</table>
<p>重启项目之后，在浏览器中输入网址 http://localhost:8080/swagger-ui.html#/message-controller，可以看到如下效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger2.png" alt="" /></p>
<p>自动将 MessageController 内的方法都添加了映射，并标明了每种方法的请求方式。</p>
<h4 id="apioperation">@ApiOperation 的使用</h4>
<p>ApiOperation 定义在方法上，描述方法名、方法解释、返回信息、标记等信息。</p>
<p>使用示例：</p>
<pre><code class="java language-java">@ApiOperation(
            value = "消息列表",
            notes = "完整的消息内容列表",
            produces="application/json, application/xml",
            consumes="application/json, application/xml",
            response = List.class)
@GetMapping(value = "messages")
public List&lt;Message&gt; list() {
}
</code></pre>
<table>
<thead>
<tr>
<th>属性名称</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>value</td>
<td>url 的路径值</td>
</tr>
<tr>
<td>tags</td>
<td>如果设置这个值、value的 值会被覆盖</td>
</tr>
<tr>
<td>produces</td>
<td>For example, "application/json, application/xml"</td>
</tr>
<tr>
<td>consumes</td>
<td>For example, "application/json, application/xml"</td>
</tr>
<tr>
<td>protocols</td>
<td>Possible values: http, https, ws, wss</td>
</tr>
<tr>
<td>authorizations</td>
<td>高级特性认证时配置</td>
</tr>
<tr>
<td>hidden</td>
<td>配置为 true 将在文档中隐藏</td>
</tr>
<tr>
<td>response</td>
<td>返回的对象</td>
</tr>
<tr>
<td>responseContainer</td>
<td>这些对象是有效的 "List", "Set" or "Map"，其他无效</td>
</tr>
<tr>
<td>httpMethod</td>
<td>"GET"、"HEAD"、"POST"、"PUT"、"DELETE"、"OPTIONS" and "PATCH"</td>
</tr>
<tr>
<td>code</td>
<td>http 的状态码 默认 200</td>
</tr>
<tr>
<td>extensions</td>
<td>扩展属性</td>
</tr>
</tbody>
</table>
<p>重启项目之后，在浏览器中输入网址 http://localhost:8080/swagger-ui.html#/message-controller/listUsingGET，可以看到如下效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger3.png" alt="" /></p>
<h4 id="apiimplicitparamsapiimplicitparam">@ApiImplicitParams 和 @ApiImplicitParam 的使用</h4>
<p>@ApiImplicitParams 用于描述方法的返回信息，和 @ApiImplicitParam 注解配合使用；@ApiImplicitParam 用来描述具体某一个参数的信息，包括参数的名称、类型、限制等信息。</p>
<p>使用示例：</p>
<pre><code class="java language-java">@ApiOperation(value = "添加消息", notes = "根据参数创建消息")
    @ApiImplicitParams({
            @ApiImplicitParam(name = "id", value = "消息 ID", required = true, dataType = "Long", paramType = "query"),
            @ApiImplicitParam(name = "text", value = "正文", required = true, dataType = "String", paramType = "query"),
            @ApiImplicitParam(name = "summary", value = "摘要", required = false, dataType = "String", paramType = "query"),
})
@PostMapping(value = "message")
public Message create(Message message) {
}
</code></pre>
<table>
<thead>
<tr>
<th>属性名称</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>name</td>
<td>接收参数名</td>
</tr>
<tr>
<td>value</td>
<td>接收参数的意义描述</td>
</tr>
<tr>
<td>required</td>
<td>参数是否必填值为 true 或者 false</td>
</tr>
<tr>
<td>dataType</td>
<td>参数的数据类型只作为标志说明，并没有实际验证</td>
</tr>
<tr>
<td>paramType</td>
<td>查询参数类型，其值：<Br/>path 以地址的形式提交数据<Br/>query 直接跟参数完成自动映射赋<Br/>body 以流的形式提交，仅支持 POST<Br/>header 参数在 request headers 里边提交<Br/>form 以 form 表单的形式提交 仅支持 POST</td>
</tr>
<tr>
<td>defaultValue</td>
<td>默认值</td>
</tr>
</tbody>
</table>
<p>重启项目之后，在浏览器中输入网址 http://localhost:8080/swagger-ui.html#/message-controller/createUsingPOST，可以看到如下效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger4.png" alt="" /></p>
<h4 id="apiresponsesapiresponse">@ApiResponses 和 @ApiResponse 的使用</h4>
<p>@ApiResponses 主要封装方法的返回信息和 @ApiResponse 配置起来使用，@ApiResponse 定义返回的具体信息包括返回码、返回信息等。</p>
<p>使用示例：</p>
<pre><code class="java language-java">@ApiOperation(value = "修改消息", notes = "根据参数修改消息")
@PutMapping(value = "message")
@ApiResponses({
        @ApiResponse(code = 100, message = "请求参数有误"),
        @ApiResponse(code = 101, message = "未授权"),
        @ApiResponse(code = 103, message = "禁止访问"),
        @ApiResponse(code = 104, message = "请求路径不存在"),
        @ApiResponse(code = 200, message = "服务器内部错误")
})
public Message modify(Message message) {
}
</code></pre>
<table>
<thead>
<tr>
<th>属性名称</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>code</td>
<td>http 的状态码</td>
</tr>
<tr>
<td>message</td>
<td>描述</td>
</tr>
<tr>
<td>response</td>
<td>默认响应类 Void</td>
</tr>
<tr>
<td>reference</td>
<td>参考</td>
</tr>
<tr>
<td>responseHeaders</td>
<td>封装返回信息</td>
</tr>
<tr>
<td>responseContainer</td>
<td>字符串</td>
</tr>
</tbody>
</table>
<p>重启项目之后，在浏览器中输入网址 http://localhost:8080/swagger-ui.html#/message-controller/modifyUsingPUT，可以看到如下效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger5.png" alt="" /></p>
<h4 id="apimodelapimodelproperty">@ApiModel 和 @ApiModelProperty 的使用</h4>
<p>在实际的项目中我们常常会封装一个对象作为返回值，@ApiModel 就是负责描述对象的信息，@ApiModelProperty 负责描述对象中属性的相关内容。</p>
<p>使用示例：</p>
<pre><code class="java language-java">@ApiModel(description = "响应对象")
public class BaseResult&lt;T&gt; {
    private static final int SUCCESS_CODE = 0;
    private static final String SUCCESS_MESSAGE = "成功";

    @ApiModelProperty(value = "响应码", name = "code", required = true, example = "" + SUCCESS_CODE)
    private int code;
    @ApiModelProperty(value = "响应消息", name = "msg", required = true, example = SUCCESS_MESSAGE)
    private String msg;
    @ApiModelProperty(value = "响应数据", name = "data")
    private T data;
}
</code></pre>
<p>属性配置如下表所示：</p>
<table>
<thead>
<tr>
<th>属性名称</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td>value</td>
<td>属性描述</td>
</tr>
<tr>
<td>name</td>
<td>如果配置覆盖属性名称</td>
</tr>
<tr>
<td>allowableValues</td>
<td>允许的值</td>
</tr>
<tr>
<td>access</td>
<td>可以不配置</td>
</tr>
<tr>
<td>notes</td>
<td>没有使用</td>
</tr>
<tr>
<td>dataType</td>
<td>数据类型</td>
</tr>
<tr>
<td>required</td>
<td>是否为必传参数</td>
</tr>
<tr>
<td>position</td>
<td>显示的顺序位置</td>
</tr>
<tr>
<td>hidden</td>
<td>是否因此</td>
</tr>
<tr>
<td>example</td>
<td>举例</td>
</tr>
<tr>
<td>readOnly</td>
<td>只读</td>
</tr>
<tr>
<td>reference</td>
<td>引用</td>
</tr>
</tbody>
</table>
<p>这样我们在 Controller 中封装返还信息时就可以这样操作：</p>
<pre><code class="java language-java">@PatchMapping(value="/message/text")
public BaseResult&lt;Message&gt; patch(Message message) {
    Message messageResult=this.messageRepository.updateText(message);
    return BaseResult.successWithData(messageResult);
}
</code></pre>
<p>重启项目之后，在浏览器中输入网址 http://localhost:8080/swagger-ui.html，点解页面 Models 折叠项，可以看到如下效果：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/swagger6.png" alt="" /></p>
<p>以上就是在项目中最常用的一些注解，灵活地利用这些注解就可以自动构建出清晰的 API 文档。</p>
<h3 id="tryitout">Try it out</h3>
<p>使用 Swagger 创建的在线 API 还有一个非常强大的功能，可以在页面直接测试接口的可用性，这样在前端和后端接口调试出现问题时，可以非常方便地利用此功能进行接口验证。在上面参数讲解过程中，我们发现每个接口描述右侧都有一个按钮 try it out，单击 try it out 按钮即可进入表单页面，如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/try.png" alt="" /></p>
<p>在表单页面添加相关字段后，单击“Execute”按钮就会将请求发送到后台，从而进行接口验证，通过按钮下面的命令可以看出，实际上是使用了 curl 命令进行的 post 测试：</p>
<pre><code>curl -X POST "http://localhost:8080/message?id=6&amp;summary=%E8%BF%99%E6%98%AF%E4%B8%80%E4%B8%AA%E6%B6%88%E6%81%AF&amp;text=hello" -H "accept: */*"
</code></pre>
<p>在后端调整 Swagger 方法上对应参数，即可看到 curl 命令参数的变化。</p>
<h3 id="-2">总结</h3>
<p>通过这节课的学习我们掌握了在 Spring Boot 项目中使用 Swagger，利用 Swagger 的相关注解可以容易地构建出丰富的 API 文档。使用 Swagger 之后可以帮助生成标准的 API 说明文档，避免接口交互中的低效沟通问题，Swagger 做为强大的 API 生成框架其实还有更多的功能，大家有机会可以在线下继续学习。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>