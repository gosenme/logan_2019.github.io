---
title: 案例上手 Spring 全家桶-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>这一讲来学习 Spring MVC 的数据绑定，什么是数据绑定？在后台业务方法中，直接获取前端 HTTP 请求中的参数。</p>
<p>首先来了解一下底层原理，HTTP 请求传输的参数都是 String 类型，但是 Hanlder 业务方法中的参数都是我们指定的数据类型，如 int、Object 等，因此需要处理参数的类型转换。此项工作不需要我们开发人员去完成，Spring MVC 的 HandlerAdapter 组件会在执行 Handler 业务方法之前，完成参数的绑定。</p>
<p>了解完大致理论，接下来我们就直接上代码，实践出真知。</p>
<h3 id="-1">基本数据类型</h3>
<p>以 int 为例，后台需要 int 类型的参数，直接在业务方法定义处添加 int 类型的形参即可，HTTP 请求参数名必须与形参名一致。</p>
<p>@ResponseBody 注解直接返回字符串到客户端，不需要返回 jsp 页面。</p>
<pre><code class="java language-java">@RequestMapping(value="/baseType")
@ResponseBody
public String baseType(int id){
    return "id:"+id;
}
</code></pre>
<p>测试，HTTP 请求不带参数，直接报 500 错误。</p>
<p><img src="https://images.gitbook.cn/18a831b0-96f5-11e8-a80f-e9b555a946c4" width = "60%" /></p>
<p>错误原因：</p>
<p><img src="https://images.gitbook.cn/221eadf0-96f5-11e8-a80f-e9b555a946c4" width = "75%" /></p>
<p>可选的参数“id”不能转为 null，因为我们都知道，基本数据类型不能赋值 null。</p>
<p>测试：参数类型为字符串。</p>
<p><img src="https://images.gitbook.cn/29e57e60-96f5-11e8-ab3d-7b3c8b8e2dff" width = "60%" /></p>
<p>400 错误，错误原因：</p>
<p><img src="https://images.gitbook.cn/30d8f940-96f5-11e8-a80f-e9b555a946c4" width = "70%" /></p>
<p>String 类型不能转换为 int 类型。</p>
<p>正确使用：</p>
<p><img src="https://images.gitbook.cn/3938d560-96f5-11e8-9e0c-8bfb55c56242" width = "70%" /></p>
<h3 id="-2">包装类</h3>
<pre><code class="java language-java">@RequestMapping(value="/packageType")
@ResponseBody
public String packageType(Integer id){
    return "id:"+id;
}
</code></pre>
<p>测试：不传参数。</p>
<p><img src="https://images.gitbook.cn/415d7d40-96f5-11e8-ab3d-7b3c8b8e2dff" width = "70%" /></p>
<p>没有报错，直接打印 null，因为包装类可以赋值 null。</p>
<p>测试：参数类型为字符串。</p>
<p><img src="https://images.gitbook.cn/48fc7a60-96f5-11e8-9e0c-8bfb55c56242" width = "60%" /></p>
<p>400 错误，错误原因如下：</p>
<p><img src="https://images.gitbook.cn/51463670-96f5-11e8-9f54-b3cc9167c22b" width = "70%" /></p>
<p>String 类型不能转换为 Integer 类型。</p>
<p>正确使用：</p>
<p><img src="https://images.gitbook.cn/5914cf10-96f5-11e8-9f54-b3cc9167c22b" width = "70%" /></p>
<p>参数列表添加 @RequestParam 注解，可以对参数进行相关设置。</p>
<pre><code class="java language-java">@RequestMapping(value="/packageType")
@ResponseBody
public String packageType(@RequestParam(value="id",required=false,defaultValue="1") Integer id){
    return "id:"+id;
}
</code></pre>
<ul>
<li>value="id"：将 HTTP 请求中名为 id 的参数与形参进行映射。</li>
<li>required=false：id 参数非必填，可省略。</li>
<li>defaultValue="1"：若 HTTP 请求中没有 id 参数，默认值为1。</li>
</ul>
<p><img src="https://images.gitbook.cn/6045a110-96f5-11e8-9e0c-8bfb55c56242" width = "60%" /></p>
<p>修改代码：required=true，删除 defaultValue 参数。</p>
<pre><code class="java language-java">@RequestMapping(value="/packageType")
@ResponseBody
public String packageType(@RequestParam(value="id",required=true) Integer id){
    return "id:"+id;
}
</code></pre>
<p>再次运行。</p>
<p><img src="https://images.gitbook.cn/67cfddb0-96f5-11e8-ab3d-7b3c8b8e2dff" width = "60%" /></p>
<p>报错，因为 id 为必填参数，此时客户端没有传 id 参数，同时业务方法中 id 也没有默认值，所以报错。</p>
<p>若客户端传 id 或者 id 有 dafaultValue，程序不会报错。</p>
<h3 id="-3">数组</h3>
<pre><code class="java language-java">@RequestMapping(value="/arrayType")
@ResponseBody
public String arrayType(String[] name){
     StringBuffer sbf = new StringBuffer();
     for(String item:name) {
         sbf.append(item).append(" ");
     }
    return "name:"+sbf.toString();
}
</code></pre>
<p><img src="https://images.gitbook.cn/73894510-96f5-11e8-a80f-e9b555a946c4" width = "75%" /></p>
<h3 id="pojo">POJO</h3>
<p>（1）创建 User 类。</p>
<pre><code class="java language-java">public class User {
    private String name;
    private int age;
}
</code></pre>
<p>（2）JSP 页面 input 标签的 name 值与实体类的属性名对应。</p>
<pre><code class="jsp language-jsp">&lt;form action="pojoType" method="post"&gt;
    姓名：&lt;input type="text" name="name"/&gt;&lt;br/&gt;
    年龄：&lt;input type="text" name="age"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>（3）业务方法。</p>
<pre><code class="java language-java">@RequestMapping(value="/pojoType")
@ResponseBody
public String pojoType(User user){
    return "注册用户信息："+user;
}
</code></pre>
<p>（4）运行。</p>
<p><img src="https://images.gitbook.cn/7c038700-96f5-11e8-a80f-e9b555a946c4" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/825088b0-96f5-11e8-ab3d-7b3c8b8e2dff" width = "60%" /></p>
<p>处理 @ResponseBody 中文乱码：在 springmvc.xml 中配置消息转换器。</p>
<pre><code class="xml language-xml">&lt;mvc:annotation-driven &gt;
    &lt;!-- 消息转换器 --&gt;
    &lt;mvc:message-converters register-defaults="true"&gt;
      &lt;bean class="org.springframework.http.converter.StringHttpMessageConverter"&gt;
        &lt;property name="supportedMediaTypes" value="text/html;charset=UTF-8"/&gt;
      &lt;/bean&gt;
    &lt;/mvc:message-converters&gt;
&lt;/mvc:annotation-driven&gt;
</code></pre>
<h3 id="pojo-1">POJO 级联关系</h3>
<p>（1）创建 Address 类。</p>
<pre><code class="java language-java">public class Address {
    private int id;
    private String name;
}
</code></pre>
<p>（2）修改 User 类，添加 Address 属性。</p>
<pre><code class="java language-java">public class User {
    private String name;
    private int age;
    private Address address;
}
</code></pre>
<p>（3）修改 JSP，添加 address 信息，为 input 标签的 name 设置属性级联，即先关联 User 的 address 属性，再级联 address 的 id 和 name。</p>
<pre><code class="jsp language-jsp">&lt;form action="pojoType" method="post"&gt;
    姓名：&lt;input type="text" name="name"/&gt;&lt;br/&gt;
    年龄：&lt;input type="text" name="age"/&gt;&lt;br/&gt;
    地址编号：&lt;input type="text" name="address.id"/&gt;&lt;br/&gt;
    地址：&lt;input type="text" name="address.name"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>（4）运行</p>
<p><img src="https://images.gitbook.cn/8eb30150-96f5-11e8-9e0c-8bfb55c56242" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/94d4d450-96f5-11e8-ab3d-7b3c8b8e2dff" width = "60%" /></p>
<h3 id="list">List</h3>
<p>Spring MVC 不支持 List 类型的直接转换，需要包装成 Object。</p>
<p>List 的自定义包装类：</p>
<pre><code class="java language-java">public class UserList {
    private List&lt;User&gt; users;
}
</code></pre>
<p>业务方法：</p>
<pre><code class="java language-java">@RequestMapping(value="/listType")
@ResponseBody
public String listType(UserList userList){
    StringBuffer sbf = new StringBuffer();
    for(User user:userList.getUsers()){
        sbf.append(user);
    }
    return "用户："+sbf.toString();
}
</code></pre>
<p>创建 addList.jsp，同时添加三个用户信息，input 的 name 指向自定义包装类 UserList 中的 users 属性，级联到 name 和 age，同时以下标区分集合中不同的对象。</p>
<pre><code class="jsp language-jsp">&lt;form action="listType" method="post"&gt;
    用户1姓名：&lt;input type="text" name="users[0].name"/&gt;&lt;br/&gt;
    用户1年龄：&lt;input type="text" name="users[0].age"/&gt;&lt;br/&gt;
    用户2姓名：&lt;input type="text" name="users[1].name"/&gt;&lt;br/&gt;
    用户2年龄：&lt;input type="text" name="users[1].age"/&gt;&lt;br/&gt;
    用户3姓名：&lt;input type="text" name="users[2].name"/&gt;&lt;br/&gt;
    用户3年龄：&lt;input type="text" name="users[2].age"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>执行代码。</p>
<p><img src="https://images.gitbook.cn/9fa33f70-96f5-11e8-a80f-e9b555a946c4" width = "50%" /></p>
<p><img src="https://images.gitbook.cn/afb3f300-96f5-11e8-9f54-b3cc9167c22b" width = "70%" /></p>
<h3 id="set">Set</h3>
<p>和 List 一样，需要封装自定义包装类，将 Set 集合作为属性。不同的是，使用 Set 集合，需要在包装类构造函数中，为 Set 添加初始化对象。</p>
<pre><code class="java language-java">public class UserSet {
    private Set&lt;User&gt; users = new HashSet&lt;User&gt;();

    public UserSet(){  
        users.add(new User());  
        users.add(new User());  
        users.add(new User());  
    }
}
</code></pre>
<p>业务方法：</p>
<pre><code class="java language-java">@RequestMapping(value="/setType")
@ResponseBody
public String setType(UserSet userSet){
    StringBuffer sbf = new StringBuffer();
    for(User user:userSet.getUsers()){
        sbf.append(user);
    }
    return "用户："+sbf.toString();
}
</code></pre>
<p>JSP 用法与 List 一样，input 标签的 name 指向 Set 内对象的属性值，通过下标区分不同的对象。</p>
<pre><code class="jsp language-jsp">&lt;form action="setType" method="post"&gt;
        用户1姓名：&lt;input type="text" name="users[0].name"/&gt;&lt;br/&gt;
        用户1年龄：&lt;input type="text" name="users[0].age"/&gt;&lt;br/&gt;
        用户2姓名：&lt;input type="text" name="users[1].name"/&gt;&lt;br/&gt;
        用户2年龄：&lt;input type="text" name="users[1].age"/&gt;&lt;br/&gt;
        用户3姓名：&lt;input type="text" name="users[2].name"/&gt;&lt;br/&gt;
        用户3年龄：&lt;input type="text" name="users[2].age"/&gt;&lt;br/&gt;
        &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>执行代码。</p>
<p><img src="https://images.gitbook.cn/b8d08f70-96f5-11e8-9e0c-8bfb55c56242" width = "50%" /></p>
<p><img src="https://images.gitbook.cn/bf4e8c30-96f5-11e8-ab3d-7b3c8b8e2dff" width = "65%" /></p>
<h3 id="map">Map</h3>
<p>自定义包装类：</p>
<pre><code class="java language-java">public class UserMap {
    private Map&lt;String,User&gt; users;
}
</code></pre>
<p>业务方法，遍历 Map 集合的 key 值，通过 key 值获取 value。</p>
<pre><code class="java language-java">@RequestMapping(value="/mapType")
@ResponseBody
public String mapType(UserMap userMap){
    StringBuffer sbf = new StringBuffer();
    for(String key:userMap.getUsers().keySet()){
        User user = userMap.getUsers().get(key);
        sbf.append(user);
    }
    return "用户："+sbf.toString();
}
</code></pre>
<p>JSP 与 List 和 Set 不同的是，不能通过下标区分不同的对象，改为通过 key 值区分。</p>
<pre><code class="jsp language-jsp">&lt;form action="mapType" method="post"&gt;
    用户1姓名：&lt;input type="text" name="users['a'].name"/&gt;&lt;br/&gt;
    用户1年龄：&lt;input type="text" name="users['a'].age"/&gt;&lt;br/&gt;
    用户2姓名：&lt;input type="text" name="users['b'].name"/&gt;&lt;br/&gt;
    用户2年龄：&lt;input type="text" name="users['b'].age"/&gt;&lt;br/&gt;
    用户3姓名：&lt;input type="text" name="users['c'].name"/&gt;&lt;br/&gt;
    用户3年龄：&lt;input type="text" name="users['c'].age"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form&gt;
</code></pre>
<p>执行代码。</p>
<p><img src="https://images.gitbook.cn/cae6d700-96f5-11e8-a80f-e9b555a946c4" width = "50%" /></p>
<p><img src="https://images.gitbook.cn/d24b3c20-96f5-11e8-9e0c-8bfb55c56242" width = "60%" /></p>
<h3 id="json">JSON</h3>
<p>JSP：Ajax 请求后台业务方法，并将 JSON 格式的参数传给后台。</p>
<pre><code class="javascript language-javascript">&lt;script type="text/javascript"&gt;
    var user = {
            "name":"张三",
            "age":22
    };
    $.ajax({
        url:"jsonType",
        data:JSON.stringify(user),
        type:"post",
        contentType: "application/json;charse=UTF-8",
        dataType:"text",
        success:function(data){
            var obj = eval("(" + data + ")");
            alert(obj.name+"---"+obj.age);
        }
    })
&lt;/script&gt;
</code></pre>
<h4 id="-4">注意</h4>
<ul>
<li>JSON 数据必须用 JSON.stringify() 方法转换成字符串</li>
<li>contentType 不能省略</li>
</ul>
<p>业务方法：</p>
<pre><code class="java language-java">@RequestMapping(value="/jsonType")
@ResponseBody
public User jsonType(@RequestBody User user){
    //修改年龄
    user.setAge(user.getAge()+10);
    //返回前端
    return user;
}
</code></pre>
<h4 id="requestbody">@RequestBody 注解</h4>
<p>读取 HTTP 请求参数，通过 Spring MVC 提供的 HttpMessageConverter 接口将读取的参数转为 JSON、XML 格式的数据，绑定到业务方法的形参。</p>
<h4 id="responsebody">@ResponseBody 注解</h4>
<p>将业务方法返回的对象，通过 HttpMessageConverter 接口转为指定格式的数据，JSON、XML等，响应给客户端。</p>
<p>我们使用的是阿里的 FastJson 来取代 Spring 默认的 Jackson 进行数据绑定。FastJson 的优势在于如果属性为空就不会将其转化为 JSON，数据会简洁很多。</p>
<h4 id="fastjson">如何使用 FastJson</h4>
<p>（1）在 pom.xml 中添加 FastJson 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
    &lt;artifactId&gt;fastjson&lt;/artifactId&gt;
    &lt;version&gt;1.2.18&lt;/version&gt;
&lt;/dependency&gt; 
</code></pre>
<p>（2）在 springmvc.xml 中配置 FastJson。</p>
<pre><code class="xml language-xml">&lt;mvc:annotation-driven &gt;
     &lt;!-- 消息转换器 --&gt;
     &lt;mvc:message-converters register-defaults="true"&gt;
       &lt;bean class="org.springframework.http.converter.StringHttpMessageConverter"&gt;
         &lt;property name="supportedMediaTypes" value="text/html;charset=UTF-8"/&gt;
       &lt;/bean&gt;
       &lt;!-- 阿里 fastjson --&gt;
       &lt;bean class="com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter4"/&gt;
     &lt;/mvc:message-converters&gt;
&lt;/mvc:annotation-driven&gt;
</code></pre>
<p>运行代码。</p>
<p><img src="https://images.gitbook.cn/dd18bce0-96f5-11e8-9f54-b3cc9167c22b" width = "65%" /></p>
<p>前端传给后台的数据 age=22，后台对 age 进行修改，并将修改的结果返回给前端，我们在前端页面看到 age=32，修改成功。</p>
<h3 id="-5">总结</h3>
<p>本节课我们讲解了 Spring MVC 的数据绑定，数据绑定就是通过框架自动将客户端传来的参数绑定到业务方法的形参中。我们知道 HTTP 请求的参数全部是文本类型的，Spring MVC 框架可以根据 Controller 端业务方法的需求自动将文本类型的参数进行数据类型转换，进而为开发者省去参数转换的繁琐步骤。</p>
<h3 id="-6">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/Spring-MVC-DataBind.git">请单击这里下载源码</a></p></div></article>