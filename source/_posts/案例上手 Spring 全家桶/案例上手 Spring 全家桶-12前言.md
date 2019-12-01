---
title: 案例上手 Spring 全家桶-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>Spring MVC 框架作为一个实现 MVC 设计模式的框架，很重要的一项工作是在控制器获取业务数据并返回给客户端，即在 JSP 页面展示业务数据，使用的技术是通过 EL 表达式从域对象中取值。</p>
<p>在 Servlet 中，我们可以直接调用 Web 资源给域对象传值，在 Spring MVC 框架中，如何完成这个操作？这一讲我们就来学习 Spring MVC 框架的业务数据绑定。</p>
<p>首先来理解这句话，业务数据的绑定是指将业务数据绑定给 JSP 域对象，首先回顾一下域对象都有哪些。</p>
<p>JSP 四大作用域对应的四个内置对象分别是：pageContext、request、session 和 application。</p>
<p>业务数据的绑定是由 ViewResolver 来完成的，开发时，我们先添加业务数据，再交给 ViewResolver 来绑定，因此学习的重点在于如何添加业务数据，Spring MVC 提供了以下几种方式添加业务数据：</p>
<ul>
<li>Map</li>
<li>Model</li>
<li>ModelAndView</li>
<li>@SessionAttributes</li>
<li>@ModelAttribute</li>
</ul>
<p>开发中经常用到的域对象是 request 和 session，我们就针对这两个域对象进行讲解，pageContext 和 application 可以通过获取原生 Servlet 资源的方式进行绑定，实际开发中使用不多。</p>
<h3 id="request">业务数据绑定到 request 域对象</h3>
<h4 id="map">Map</h4>
<p>Spring MVC 在内部使用 Model 接口存储业务数据，在调用业务方法前会创建一个隐含对象作为业务数据的存储容器。设置业务方法的入参为 Map 类型，Spring MVC 会将隐含对象的引用传递给入参。开发者可以对模型中的所有数据进行管理，包括访问和添加。我们只需要在业务方法添加 Map 类型的入参，方法体中便可通过对入参的操作来完成业务数据的添加。</p>
<pre><code class="java language-java">@RequestMapping("/mapTest")
public String mapTest(Map&lt;String,Object&gt; map){
  User user = new User();
  user.setId(1);
  user.setName("张三");
  map.put("user", user);
  return "index";
}
</code></pre>
<p>业务方法完成，返回业务数据和视图信息给 DispatcherServlet，DispatcherServlet 通过 ViewResolver 对视图信息进行解析，逻辑视图映射到物理视图，同时将业务数据绑定到 JSP 的 request 域对象中，在 JSP 页面可直接通过 EL 表达式取值。</p>
<pre><code class="jsp language-jsp">&lt;body&gt;
    ${user.name }
&lt;/body&gt;
</code></pre>
<p>启动 Tomcat，运行，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/f7db3ec0-9959-11e8-8d3d-23404c5d9030" width = "60%" /></p>
<h4 id="model">Model</h4>
<p>Model 与 Map 类似，业务方法通过入参来完成业务数据的绑定。</p>
<pre><code class="java language-java">@RequestMapping("/modelTest")
public String modelTest(Model model){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    model.addAttribute("user", user);
    return "index";
}
</code></pre>
<h4 id="modelandview">ModelAndView</h4>
<p>与 Map 或者 Model 不同的是，ModelAndView 不但包含业务数据，同时也包含了视图信息，如果使用 ModelAndView 来处理业务数据，业务方法的返回值必须是 ModelAndView 对象。</p>
<p>业务方法中对 ModelAndView 进行两个操作：填充业务数据、绑定视图信息。</p>
<p>关于 ModelAndView 的使用有 8 种方式，具体操作如下所示。</p>
<pre><code class="java language-java">@RequestMapping("/modelAndViewTest1")
public ModelAndView modelAndViewTest1(){
    ModelAndView modelAndView = new ModelAndView();
    User user = new User();
    user.setId(1);
    user.setName("张三");
    modelAndView.addObject("user", user);
    modelAndView.setViewName("index");
    return modelAndView;
}

@RequestMapping("/modelAndViewTest2")
public ModelAndView modelAndViewTest2(){
    ModelAndView modelAndView = new ModelAndView();
    User user = new User();
    user.setId(1);
    user.setName("张三");
    modelAndView.addObject("user", user);
    View view = new InternalResourceView("/index.jsp");
    modelAndView.setView(view);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest3")
public ModelAndView modelAndViewTest3(){
    ModelAndView modelAndView = new ModelAndView("index");
    User user = new User();
    user.setId(1);
    user.setName("张三");
    modelAndView.addObject("user", user);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest4")
public ModelAndView modelAndViewTest4(){
    View view = new InternalResourceView("/index.jsp");
    ModelAndView modelAndView = new ModelAndView(view);
    User user = new User();
    user.setId(1);
    user.setName("张三");
    modelAndView.addObject("user", user);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest5")
public ModelAndView modelAndViewTest5(){
    Map&lt;String,Object&gt; map = new HashMap&lt;String,Object&gt;();
    User user = new User();
    user.setId(1);
    user.setName("张三");
    map.put("user", user);
    ModelAndView modelAndView = new ModelAndView("index", map);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest6")
public ModelAndView modelAndViewTest6(){
    Map&lt;String,Object&gt; map = new HashMap&lt;String,Object&gt;();
    User user = new User();
    user.setId(1);
    user.setName("张三");
    map.put("user", user);
    View view = new InternalResourceView("/index.jsp");
    ModelAndView modelAndView = new ModelAndView(view, map);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest7")
public ModelAndView modelAndViewTest7(){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    ModelAndView modelAndView = new ModelAndView("index", "user", user);
    return modelAndView;
}

@RequestMapping("/modelAndViewTest8")
public ModelAndView modelAndViewTest8(){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    View view = new InternalResourceView("/index.jsp");
    ModelAndView modelAndView = new ModelAndView(view, "user", user);
    return modelAndView;
}
</code></pre>
<h4 id="httpservletrequest">HttpServletRequest</h4>
<p>Spring MVC 可以在业务方法直接获取到 Servlet 原生 Web 资源，只需在方法定义时添加 HttpServletRequest 入参即可，在方法体中可直接对 request 对象进行操作，如下所示。</p>
<pre><code class="java language-java">@RequestMapping("requestTest")
public String requestTest(HttpServletRequest request){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    request.setAttribute("user", user);
    return "index";
}
</code></pre>
<h4 id="modelattribute">@ModelAttribute</h4>
<p>Spring MVC 还可以通过 @ModelAttribute 注解的方式添加业务数据，具体使用有如下两个步骤：</p>
<ul>
<li>定义一个方法，该方法用来返回要填充到业务数据中的对象；</li>
<li>给该方法添加 @ModelAttribute 注解，注意，该方法并不是响应请求的业务方法。</li>
</ul>
<pre><code class="java language-java">@RequestMapping("/modelAttributeTest")
public String modelAttributeTest(){
    return "index";
}

@ModelAttribute
public User getUser(){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    return user;
}
</code></pre>
<p>添加 @ModelAttribute 注解的方法，会在 Spring MVC 调用任何一个业务方法之前自动调用。因此在执行 modelAttributeTest 业务方法之前，会首先调用 getUser 方法，获取返回值 user 对象，Spring MVC 会自动将该对象填充到业务数据中，进而绑定到域对象中。</p>
<p>我们知道域对象中的数据都是以键值对 (key-value) 的形式保存的，那么此时的 key 是什么呢？默认取业务数据对应类的首字母小写之后的类名，如 User 类首字母小写之后为 "user"，因此 JSP 页面中，可以直接通过 "user" 取值。</p>
<p>若 getUser 没有返回值，则必须手动在该方法中填充业务数据，使用 Map 或者 Model 均可。</p>
<pre><code class="java language-java">@ModelAttribute
public void getUser2(Map&lt;String,Object&gt; map){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    map.put("user", user);
}

@ModelAttribute
public void getUser3(Model model){
    User user = new User();
    user.setId(1);
    user.setName("张三");
    model.addAttribute("user", user);
}
</code></pre>
<h3 id="session">业务数据绑定到 session 域对象</h3>
<p>上述方式全部是将业务数据绑定到 request 对象中，如果需要将业务数据绑定到 session 对象中，只需要在类定义处添加 @SessionAttributes(value="user") 注解即可，如下所示。</p>
<pre><code class="java language-java">@Controller
@SessionAttributes(value="user")
public class HelloHandler {
//省略代码
}
</code></pre>
<p>此时，无论通过上述哪种方式来执行业务代码，将业务数据绑定到 request 对象中的同时，也会将业务数据绑定到 session 对象中，也就是说 request 和 session 对象会同时存在业务数据。</p>
<p>@SessionAttributes 除了可以通过 key 值绑定，也可以通过业务数据的数据类型进行绑定，如下所示。</p>
<pre><code class="java language-java">@Controller
@SessionAttributes(types=User.class)
public class HelloHandler {
//省略代码
}
</code></pre>
<p>@SessionAttributes 可同时绑定多个业务数据，如下所示。</p>
<pre><code class="java language-java">@Controller
@SessionAttributes(value={"user","address"})
public class HelloHandler {
//省略代码
}
</code></pre>
<pre><code class="java language-java">@Controller
@SessionAttributes(types={User.class,Address.class})
public class HelloHandler {
//省略代码
}
</code></pre>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring MVC 的业务数据解析，具体是指将控制器的业务方法处理结果响应给客户端的过程，即 C（Controller）—— V（View）的映射，可以使用 Spring MVC 自带的 ModelAndView 组件同时将业务数据和视图信息进行绑定，这种方式是我们开发中常用的，同时也可以使用 Model、Map 来完成业务数据的解析。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/Spring-MVC-4.git">请单击这里下载源码</a></p></div></article>