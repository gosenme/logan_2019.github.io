---
title: SSM 博客系统开发实战-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>之前搭建框架时，pom.xml 中只依赖了可以启动项目的 jar 包。本文将会使用到更多的依赖，方便起见，请同学们将文末百度网盘中提供的 <code>dreamland\dreamland-web</code> 目录下的 pom.xml 中的依赖添加到项目中去。</p>
<h3 id="">前期准备</h3>
<h4 id="basecontroller">基类 BaseController 的封装</h4>
<p>上一篇中，我们每次都要写很长一串来代码来获取 Request 对象，比较麻烦，现在把通用的方法进行抽取，放在 BaseController.java 文件中，其他 Controller 只需要继承 BaseController 即可使用。</p>
<p>通用方法主要包括：获取 Request、获取 Response、获取 Session、查询分页等方法。在 Controller 包下导入 BaseController.java 文件，BaseController.java 文件我会放在文末的百度网盘链接中。</p>
<p>BaseController.java 中类上的 <code>@Component</code> 注解，是指如果不知道该类属于哪一层的时候，就把该类交给 Spring 管理。</p>
<h4 id="-1">引入前端页面</h4>
<p>login.jsp 页面放在 webapp 目录下，personal.jsp 页面放在 <code>WEB-INF/personal/</code> 目录下，这两个 JSP 我已放入文末百度网盘链接中。</p>
<p>像登录、注册页面，任何人都可以访问的页面放在 webapp 下，其他需要安全访问的页面放在 <code>WEB-INF</code> 下。</p>
<p>在 index.jsp 页面加入“点我登录”临时链接：</p>
<pre><code>&lt;a href="register.jsp"&gt;点我注册&lt;/a&gt;&lt;br/&gt;
&lt;a href="login.jsp"&gt;点我登录&lt;/a&gt;
</code></pre>
<p>验证码功能在上一篇已讲过，这里就不再赘述了。主要有一点样式上的区别，为了协调将验证码的 input 框改成和用户名、密码框相同的样式：</p>
<pre><code>&lt;div class="form-group"&gt;
      &lt;label for="code" class="sr-only"&gt;验证码&lt;/label&gt;
      &lt;input type="text" id="code"  name="code"  class="form-control" placeholder="验证码" onblur="checkCode()" &gt;
&lt;/div&gt;

&lt;div&gt;
      &lt;img id="captchaImg" style="CURSOR: pointer" onclick="changeCaptcha()" title="看不清楚?请点击刷新验证码!" align='absmiddle' src="${ctx}/captchaServlet" height="18" width="55"&gt;
    &lt;a href="javascript:;" onClick="changeCaptcha()" style="color: #666;"&gt;看不清楚&lt;/a&gt; &lt;span id="code_span" style="color: red"&gt;&lt;/span&gt;
&lt;/div&gt;
</code></pre>
<p>主要将验证码 input 框加了一个 div，并将它的 class 属性设置为 <code>form-group</code>，其他基本没变。</p>
<p>启动项目后点击 index 页面的“点我登录”链接，查看效果：</p>
<p><img src="http://images.gitbook.cn/f4111d50-6de9-11e8-9a3a-91a7e0861642" alt="" /></p>
<h3 id="-2">账号登录流程</h3>
<p>账号登录的基本流程为：</p>
<ol>
<li>校验用户名是否为空，为空提示输入用户名，返回 false，否则返回 true。</li>
<li>校验密码，为空或者低于6位，提示请输入密码或者密码长度低于6位，返回 false，否则返回 true。</li>
<li>检验验证码，为空或者不正确，提示验证码不能为空或者验证码不正确，返回 false，否则返回 true。</li>
<li>登录按钮点击事件，如果以上都为 true，则提交表单给后台，否则返回对应错误信息。</li>
</ol>
<p>这里的校验方法和注册页面类似，就不再赘述了。</p>
<h4 id="-3">前台页面</h4>
<p>接下来，我们开始搭建前台页面。</p>
<p><strong>登录页面 form 标签</strong></p>
<p>代码如下：</p>
<pre><code>&lt;form id="normal_form" name="form" role="form" class="login-form" action="${ctx}/doLogin" method="post"&gt;
</code></pre>
<p>action 对应后台映射 URL 为 <code>/doLogin</code>，请求方式是 post 请求，form 标签的 id 为 <code>normal_form</code>。</p>
<p><strong>登录按钮</strong></p>
<p>相应的 HTML 代码如下：</p>
<pre><code>&lt;button type="button" id="btn" class="btn btn-primary btn-block" onclick="normal_login();"&gt;登录&lt;/button&gt;
</code></pre>
<p>登录按钮对应的点击事件 normal_login 方法如下：</p>
<pre><code>function normal_login() {
  if(checkUserName() &amp;&amp; checkPassword() &amp;&amp; checkCode()) {
            $("#normal_form").submit();
  }
}
</code></pre>
<p>如果用户名、密码、验证码都校验正确之后，通过from 表单对象的 submit 方法提交表单。</p>
<p>普通登录的密码框和手机快捷登录的验证码框回车事件，如下：</p>
<pre><code>//密码框回车事件
$("#password").bind('keypress',function(event){
    if(event.keyCode == 13)
    {
       normal_login();
    }
});

//验证码框回车事件
$("#code").bind('keypress',function(event){

    if(event.keyCode == 13)
    { 
       normal_login();
    }
});
</code></pre>
<p><code>keyCode == 13</code> 代表的是回车按键，如果点击回车按键则调用登录方法提交表单。注意，是在普通登录的密码框或者在手机快捷登录的验证码框按回车才触发（根据 id 可看出）。</p>
<h4 id="java">Java 后台</h4>
<p>前台页面写好后，我们开始搭建 Java 后台。</p>
<p>在 controller 包下新建 LoginController.java 并继承 BaseController，创建映射 URL 为 <code>/doLogin</code> 的方法，如下：</p>
<pre><code class="     language-    ">@Controller
public class loginController extends BaseController {
    private final static Logger log = Logger.getLogger( loginController.class);

    @Autowired
    private UserService userService;

    @RequestMapping("/doLogin")
    public String doLogin(Model model, @RequestParam(value = "username",required = false) String email,
                          @RequestParam(value = "password",required = false) String password,
                          @RequestParam(value = "code",required = false) String code,
                          @RequestParam(value = "state",required = false) String state,
                          @RequestParam(value = "pageNum",required = false) Integer pageNum ,
                          @RequestParam(value = "pageSize",required = false) Integer pageSize) {
        if (StringUtils.isBlank(code)) {
            model.addAttribute("error", "fail");
            return "../login";
        }
        int b = checkValidateCode(code);
        if (b == -1) {
            model.addAttribute("error", "fail");
            return "../login";
        } else if (b == 0) {
            model.addAttribute("error", "fail");
            return "../login";
        }
        password = MD5Util.encodeToHex(Constants.SALT+password);
        User user =  userService.login(email,password);
        if (user!=null){
           if("0".equals(user.getState())){
               //未激活
               model.addAttribute("email",email);
               model.addAttribute("error","active");
               return "../login";
           }
          log.info("用户登录登录成功");
           model.addAttribute("user",user);
           return "/personal/personal";
       }else{
           log.info("用户登录登录失败");
           model.addAttribute("email",email);
           model.addAttribute( "error","fail" );
           return "../login";
       }
    }

    // 匹对验证码的正确性
    public int checkValidateCode(String code) {
        Object vercode = getRequest().getSession().getAttribute("VERCODE_KEY");
        if (null == vercode) {
            return -1;
        }
        if (!code.equalsIgnoreCase(vercode.toString())) {
            return 0;
        }
        return 1;
    }

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）判断验证码是否为空，为空则把“fail”添加到 model 中，并返回到登录页面。</p>
<p>（2）调用匹配验证码正确性的方法，根据不同结果，给出相应提示，和上一篇文章中介绍的相似。</p>
<p>（3）注册时使用了 MD5 对密码进行加密，所以登陆这里也要用同样的方式对密码进行加密，然后再去数据库进行匹配。其中 salt “加盐”，提高密码复杂度，和注册时的 salt 要一致。项目常量一般都放在一个类里，便于项目其他包之间相互调用，在 common 包下新建 Constants.java:</p>
<pre><code>public class Constants {
  public static final String SALT = "salt";
}
</code></pre>
<p>（4）根据用户名和加密后的密码查询用户是否存在。</p>
<p>（5）如果用户存在，则判断用户是否已激活，如果未激活则把 email 和 active 添加到 model 中并返回登录页面，提示用户激活，如果用户已激活则把用户 user 添加到 model 中，返回到个人中心页面。</p>
<p>（6）如果用户不存在，则把 email 和 fail 添加到 model 中并返回登录页面。</p>
<p>重启 Tomcat，点击登陆，输入错误的用户名或密码，会跳转到登录页面，显示错误信息，并回显用户名，通过 EL 表达式 <code>${email}</code> 获取并赋值给 value。</p>
<pre><code>value="${email}" 
</code></pre>
<p>执行结果页面如下：</p>
<p><img src="http://images.gitbook.cn/51440890-6ded-11e8-9ab5-a93e1135abc8" alt="" /></p>
<p>输入正确的用户名、密码（未激活的账号），也会跳转到登录页面，会提示您的账号未激活，请先激活！如下图所示：</p>
<p><img src="http://images.gitbook.cn/71b42bf0-6ded-11e8-9ab5-a93e1135abc8" alt="" /></p>
<p>输入正确的用户名和密码（已激活账号），跳转到个人主页。如下图所示：</p>
<p><img src="http://images.gitbook.cn/8f4c0200-6ded-11e8-9a3a-91a7e0861642" alt="" /></p>
<p>通过EL表达式 <code>${user.nickName}</code> 获取用户昵称：剑随风。</p>
<h3 id="15">15分钟内免登录</h3>
<p>现在重新访问：http://localhost:8080/，并点击登录发现还是跳转到了登录页面，而我们并未退出登录。</p>
<p>15分钟内免登录实现原理：用户登录成功后，将用户信息保存在 Session 中，并设置失效时间为15分钟，是指15分钟内用户没有操作浏览器，如果15分钟内操作浏览器后重新计时。用户退出登录则删除 Session 保存的信息。</p>
<p>实现过程主要包括以下6步。</p>
<p>1.在 web.xml 的最后我们配置了 Session 的失效时间：</p>
<pre><code>&lt;!-- session配置 --&gt;
&lt;session-config&gt;
    &lt;session-timeout&gt;15&lt;/session-timeout&gt;
&lt;/session-config&gt;
</code></pre>
<p>2.在 <code>/doLogin</code> 映射方法内，用户登录成功后，return 语句之前将用户信息保存到 Session 中：</p>
<pre><code>getSession().setAttribute( "user",user ); model.addAttribute("user",user);
</code></pre>
<p>3.增加 <code>/login</code> 映射 URL 方法:</p>
<pre><code>@RequestMapping("/login")
public String login(Model model) {
    User user = (User)getSession().getAttribute("user");
    if(user!=null){
        return "/personal/personal";
    }
    return "../login";
}
</code></pre>
<p>获取 Session 中的User，如果 User 不为 null 则直接跳转到个人主页，如果为 null，则跳转到 login.jsp 登录页面。</p>
<p>4.修改 index.jsp 页面的登录链接：</p>
<pre><code>&lt;a href="/login"&gt;点我登录&lt;/a&gt;
</code></pre>
<p>5.重新启动 Tomcat，点击“点我登录”链接，输入用户名密码后跳转到个人主页。</p>
<p>6.重新访问：http://localhost:8080/，再次点击“点我登录”链接，发现直接跳转到了个人主页。15分钟内免登录成功！</p>
<blockquote>
  <p>本课程所开发的项目，大部分功能已经完成并发布，大家可以访问下面链接查看：http://www.dreamland.wang/。</p>
  <p>第06课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1m4OPZ-Gb96ZeC0ImwRiS0Q 密码：gl17</p>
</blockquote></div></article>