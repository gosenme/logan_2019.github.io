---
title: 案例上手 Spring 全家桶-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上一讲我们学习了 Spring MVC 框架的使用，为了更好地理解这个框架，本讲来仿写一个 Spring MVC 框架，用到的技术比较简单，只需要 XML 解析 + 反射就可以完成，不需要 JDK 动态代理。</p>
<p>自己手写框架的前提是必须理解框架的底层原理和运行机制，因此我们还是先来回顾一下 Spring MVC 的实现原理。</p>
<h3 id="springmvc">Spring MVC 实现原理</h3>
<p>Spring MVC 的核心组件和工作流程的内容具体可以参考第 2-1 讲的内容，通过上一讲的分析，大致可以将 Spring MVC 流程理解如下：</p>
<p>首先需要一个前置控制器 DispatcherServlet，作为整个流程的核心，由它去调用其他组件，共同完成业务。</p>
<p>主要组件有两个：</p>
<p>一是 Controller，调用其业务方法 Method，执行业务逻辑。</p>
<p>二是 ViewResolver 视图解析器，将业务方法的返回值解析为物理视图 + 模型数据，返回客户端。</p>
<p>我们按照这个思路来自己写框架。</p>
<blockquote>
  <p><a href="https://gitbook.cn/gitchat/column/5d2daffbb81adb3aa8cab878?utm_source=springquan001">点击这里了解《Spring 全家桶》</a></p>
</blockquote>
<h3 id="-1">初始化工作</h3>
<ul>
<li>根据 Spring IoC 容器的特性，需要将参与业务的对象全部创建并保存到容器中，供流程调用。首先需要创建 Controller 对象，HTTP 请求是通过注解找到对应的 Controller 对象，因此我们需要将所有的 Controller 与其注解建立关联，很显然，使用 key-value 结构的 Map 集合来保存最合适不过了，这样就模拟了 IoC 容器。</li>
<li>Controller 的 Method 也是通过注解与 HTTP 请求映射的，同样的，我们需要将所有的 Method 与其注解建立关联， HTTP 直接通过注解的值找到对应的 Method，这里也用 Map 集合保存。</li>
<li>实例化视图解析器。</li>
</ul>
<p>初始化工作完成，接下来处理 HTTP 请求，业务流程如下：</p>
<p>（1）DispatcherServlet 接收请求，通过映射从 IoC 容器中获取对应的 Controller 对象；</p>
<p>（2）根据映射获取 Controller 对象对应的 Method；</p>
<p>（3）调用 Method，获取返回值；</p>
<p>（4）将返回值传给视图解析器，返回物理视图；</p>
<p>（5）完成页面跳转。</p>
<p>思路捋清楚了，接下来开始写代码，我们需要创建下面这四个类：</p>
<p>（1）MyDispatcherServlet，模拟 DispatcherServlet；</p>
<p>（2）MyController，模拟 Controller 注解；</p>
<p>（3）MyRequestMapping，模拟 RequestMapping 注解；</p>
<p>（4）MyViewResolver，模拟 ViewResolver 视图解析器。</p>
<p>首先创建 MyDispatcherServlet，init 方法完成初始化：</p>
<p>（1）将 Controller 与注解进行关联，保存到 iocContainer 中，哪些 Controller 是需要添加到 iocContainer 中的？</p>
<p>必须同时满足两点：</p>
<ul>
<li>springmvc.xml 中配置扫描的类</li>
<li>类定义处添加了注解</li>
</ul>
<p>注意这两点必须同时满足。</p>
<p><strong>代码思路：</strong></p>
<ul>
<li>解析 springmvc.xml</li>
<li>获取 component-scan 标签配置包下的所有类</li>
<li>判断这些类若添加了 @MyController 注解，则创建实例对象，并且保存到 iocContainer</li>
<li>@MyRequestMapping 的值为键，Controller 对象为值</li>
</ul>
<p>（2）将 Controller 中的 Method 与注解进行关联，保存到 handlerMapping 中。</p>
<p><strong>代码思路：</strong></p>
<ul>
<li>遍历 iocContainer 中的 Controller 实例对象</li>
<li>遍历每一个 Controller 对象的 Method</li>
<li>判断 Method 是否添加了 @MyRequestMapping 注解，若添加，则进行映射并保存</li>
<li>保存到 handlerMapping 中，@MyRequestMapping 的值为键，Method 为值</li>
</ul>
<p>（3）实例化 ViewResolver。</p>
<p><strong>代码思路：</strong></p>
<ul>
<li>解析 springmvc.xml</li>
<li>根据 bean 标签的 class 属性获取需要实例化的 MyViewResolver</li>
<li>通过反射创建实例化对象，同时获取 prefix 和 suffix 属性，以及 setter 方法</li>
<li>通过反射调用 setter 方法给属性赋值，完成 MyViewResolver 的实例化</li>
</ul>
<p>doPost 方法处理 HTTP 请求的流程：</p>
<p>（1）解析 HTTP，分别得到 Controller 和 Method 对应的 uri；</p>
<p>（2）通过 uri 分别在 iocContainer 和 handlerMapping 中获取对应的 Controller 及 Method；</p>
<p>（3）通过反射调用 Method，执行业务方法，获取结果；</p>
<p>（4）将结果传给 MyViewResolver 进行解析，返回真正的物理视图（JSP 页面）；</p>
<p>（5）完成 JSP 页面跳转。</p>
<p><img src="https://images.gitbook.cn/cf639960-9a12-11e8-bd2f-43e393597943" alt="enter image description here" /></p>
<h3 id="-2">代码实现</h3>
<p>（1）创建 MyController 注解，作用目标为类。</p>
<pre><code class="java language-java">/**
 * 自定义 Controller 注解
 * @author southwind
 *
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface MyController {
    String value() default "";
}
</code></pre>
<p>（2）创建 MyRequestMapping 注解，作用目标为类和方法。</p>
<pre><code class="java language-java">/**
 * 自定义 RequestMapping 注解
 * @author southwind
 *
 */
@Target({ElementType.TYPE,ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface MyRequestMapping {
    String value() default "";
}
</code></pre>
<p>（3）创建 MyDispatcherServlet，核心控制器，init 完成初始化工作，doPost 处理 HTTP 请求。</p>
<pre><code class="java language-java">/**
 * DispatcherServlet
 * @author southwind
 *
 */
public class MyDispatcherServlet extends HttpServlet{

    //模拟 IOC 容器，保存 Controller 实例对象
    private Map&lt;String,Object&gt; iocContainer = new HashMap&lt;String,Object&gt;();
    //保存 handler 映射
    private Map&lt;String,Method&gt; handlerMapping = new HashMap&lt;String,Method&gt;();
    //自定视图解析器
    private MyViewResolver myViewResolver;

    @Override
    public void init(ServletConfig config) throws ServletException {
        // TODO Auto-generated method stub
        //扫描 Controller，创建实例对象，并存入 iocContainer
        scanController(config);
        //初始化 handler 映射
        initHandlerMapping();
        //加载视图解析器
        loadViewResolver(config);
    }

    /**
     * 扫描 Controller
     * @param config
     */
    public void scanController(ServletConfig config){
        SAXReader reader = new SAXReader();
        try {
            //解析 springmvc.xml
            String path = config.getServletContext().getRealPath("")+"\\WEB-INF\\classes\\"+config.getInitParameter("contextConfigLocation");   
            Document document = reader.read(path);
            Element root = document.getRootElement();
            Iterator iter = root.elementIterator();
            while(iter.hasNext()){
                Element ele = (Element) iter.next();
                if(ele.getName().equals("component-scan")){
                    String packageName = ele.attributeValue("base-package");
                    //获取 base-package 包下的所有类名
                    List&lt;String&gt; list = getClassNames(packageName);
                    for(String str:list){
                        Class clazz = Class.forName(str);
                        //判断是否有 MyController 注解
                        if(clazz.isAnnotationPresent(MyController.class)){
                            //获取 Controller 中 MyRequestMapping 注解的 value
                            MyRequestMapping annotation = (MyRequestMapping) clazz.getAnnotation(MyRequestMapping.class);
                            String value = annotation.value().substring(1);
                            //Controller 实例对象存入 iocContainer
                            iocContainer.put(value, clazz.newInstance());
                        }
                    }
                }
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * 获取包下的所有类名
     * @param packageName
     * @return
     */
    public List&lt;String&gt; getClassNames(String packageName){
        List&lt;String&gt; classNameList = new ArrayList&lt;String&gt;();
        String packagePath = packageName.replace(".", "/");  
        ClassLoader loader = Thread.currentThread().getContextClassLoader();  
        URL url = loader.getResource(packagePath);  
        if(url != null){
            File file = new File(url.getPath());  
            File[] childFiles = file.listFiles();
            for(File childFile : childFiles){
                String className = packageName+"."+childFile.getName().replace(".class", "");
                classNameList.add(className);
            }
        }
        return classNameList;
    }

    /**
     * 初始化 handler 映射
     */
    public void initHandlerMapping(){
        for(String str:iocContainer.keySet()){
            Class clazz = iocContainer.get(str).getClass();
            Method[] methods = clazz.getMethods();
               for (Method method : methods) {
                 //判断方式是否添加 MyRequestMapping 注解
                 if(method.isAnnotationPresent(MyRequestMapping.class)){
                     //获取 Method 中 MyRequestMapping 注解的 value
                     MyRequestMapping annotation = method.getAnnotation(MyRequestMapping.class);
                     String value = annotation.value().substring(1);
                     //method 存入 methodMapping
                     handlerMapping.put(value, method);
                 }
             }
        }
    }

    /**
     * 加载自定义视图解析器
     * @param config
     */
    public void loadViewResolver(ServletConfig config){
        SAXReader reader = new SAXReader();
        try {
            //解析 springmvc.xml
            String path = config.getServletContext().getRealPath("")+"\\WEB-INF\\classes\\"+config.getInitParameter("contextConfigLocation");   
            Document document = reader.read(path);
            Element root = document.getRootElement();
            Iterator iter = root.elementIterator();
            while(iter.hasNext()){
                Element ele = (Element) iter.next();
                if(ele.getName().equals("bean")){
                    String className = ele.attributeValue("class");
                    Class clazz = Class.forName(className);
                    Object obj = clazz.newInstance();
                    //获取 setter 方法
                    Method prefixMethod = clazz.getMethod("setPrefix", String.class);
                    Method suffixMethod = clazz.getMethod("setSuffix", String.class);
                    Iterator beanIter = ele.elementIterator();
                    //获取 property 值
                    Map&lt;String,String&gt; propertyMap = new HashMap&lt;String,String&gt;();
                    while(beanIter.hasNext()){
                        Element beanEle = (Element) beanIter.next();
                        String name = beanEle.attributeValue("name");
                        String value = beanEle.attributeValue("value");
                        propertyMap.put(name, value);
                    }
                    for(String str:propertyMap.keySet()){
                        //反射机制调用 setter 方法，完成赋值
                        if(str.equals("prefix")){
                            prefixMethod.invoke(obj, propertyMap.get(str));
                        }
                        if(str.equals("suffix")){
                            suffixMethod.invoke(obj, propertyMap.get(str));
                        }
                    }
                    myViewResolver = (MyViewResolver) obj;
                }
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // TODO Auto-generated method stub
        this.doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // TODO Auto-generated method stub
        //获取请求
        String handlerUri = req.getRequestURI().split("/")[2];
        //获取 Controller 实例
        Object obj = iocContainer.get(handlerUri);
        String methodUri = req.getRequestURI().split("/")[3];
        //获取业务方法
        Method method = handlerMapping.get(methodUri);
        try {
            //反射机制调用业务方法
            String value = (String) method.invoke(obj);
            //视图解析器将逻辑视图转换为物理视图
            String result = myViewResolver.jspMapping(value);
            //页面跳转
            req.getRequestDispatcher(result).forward(req, resp);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } 
    }
}
</code></pre>
<p>（4）创建视图解析器 MyViewResolver。</p>
<pre><code class="java language-java">/**
 * 自定义视图解析器
 * @author southwind
 *
 */
public class MyViewResolver {
    private String prefix;
    private String suffix;
    public String getPrefix() {
        return prefix;
    }
    public void setPrefix(String prefix) {
        this.prefix = prefix;
    }
    public String getSuffix() {
        return suffix;
    }
    public void setSuffix(String suffix) {
        this.suffix = suffix;
    }

    public String jspMapping(String value){
        return this.prefix+value+this.suffix;
    }
}
</code></pre>
<p>（5）创建 TestController，处理业务请求。</p>
<pre><code class="java language-java">@MyController
@MyRequestMapping(value = "/testController")
public class TestController {
    @MyRequestMapping(value = "/test")
    public String test(){
        System.out.println("执行test相关业务");
        return "index";
    }
}
</code></pre>
<p>（6）测试。</p>
<p><img src="https://images.gitbook.cn/61d14180-9a13-11e8-992f-9dfb28d2b53f" width = "60%" /></p>
<p><img src="https://images.gitbook.cn/6631dc80-9a13-11e8-992f-9dfb28d2b53f" width = "60%" /></p>
<p>跳转 index.jsp，同时控制台打印业务日志，访问成功。</p>
<h3 id="-3">总结</h3>
<p>本节课我们讲解了 Spring MVC 的底层原理，同时仿照 Spring MVC 手写了一个简单的框架，目的不是让大家自己去写框架，在实际开发中也不需要自己写框架，直接使用成熟的第三方框架即可。手写框架的目的在于让大家更透彻地理解 Spring MVC 的底层流程、学习优秀框架的编程思想，理解了原理，才能更熟练地应用。</p>
<h3 id="-4">分享交流</h3>
<p>我们为本课程付费读者创建了微信交流群，以方便更有针对性地讨论课程相关问题。入群方式请到第 1-4 课末尾添加小助手的微信号。</p>
<p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手微信后需要截已购买的图来验证~</p>
</blockquote>
<p><a href="https://github.com/southwind9801/SpringMVCImitate.git">请单击这里下载源码</a></p>
<blockquote>
  <p><a href="https://gitbook.cn/gitchat/column/5d2daffbb81adb3aa8cab878?utm_source=springquan001">点击这里了解《Spring 全家桶》</a></p>
</blockquote></div></article>