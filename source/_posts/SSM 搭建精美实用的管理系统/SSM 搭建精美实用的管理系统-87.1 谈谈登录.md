---
title: SSM 搭建精美实用的管理系统-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="71">7.1 谈谈登录</h3>
<h4 id="1">1. 什么是登录</h4>
<p>这里说的是互联网范畴的登录，通常供多人使用的网站或程序应用系统为每位用户配置了一套独特的用户名和密码，用户可以使用各自的用户名和密码进入系统，以便系统能识别该用户的身份，从而保持该用户的使用习惯或使用数据。用户使用这套用户名和密码进入系统，以及系统验证进入是成功或失败的过程，称为 “ 登录 ” 。</p>
<p><img src="https://images.gitbook.cn/364fe230-8e21-11e8-80d1-2d51ff7e1c55" alt="login-page" /></p>
<p>登录成功之后，用户就可以合法地使用该账号具有的各项能力，例如，淘宝用户可以正常浏览商品和完成购买行为等；论坛用户可以查看/更改资料，收发帖子等等；OA 等系统管理员用户可以正常地处理各种数据和信息，从最简单的角度来说就是输入你的用户名和密码就可以进入一个 “ 系统 ” 进行访问和操作了。</p>
<h4 id="2">2. 用户登录状态</h4>
<p>客户端（通常是浏览器）在连上 Web 服务器后，若想获得 Web 服务器中的各种资源，需要遵守一定的通讯格式。Web 项目通常使用的是 HTTP 协议，HTTP 协议用于定义客户端与 Web 服务器通讯的格式。而 HTTP 协议又是无状态的协议，也就是说，这个协议是无法记录用户访问状态的，其每次请求都是独立的没有任何关联的，一个请求就是一个请求。</p>
<p>以我们将要开发的后台管理系统来说，这个管理系统是拥有多个页面的，在页面跳转过程中和通过接口进行数据交互时我们需要知道用户的状态，尤其是用户登录的状态，以便我们知道这是否是一个正常的用户，这个用户是否处于合法的登录状态，这样才能在页面跳转和接口请求时知道是否可以让当前用户来操作一些功能或是获取一些数据。</p>
<p>因此需要在每个页面对用户的身份进行验证和确认，但现实情况是，不可能让用户在每个页面上都输入用户名和密码，这是一个多么反人类的设计啊，应该不会有用户想要去使用这种系统，所以在设计时，要求用户进行一次登录操作即可。为了实现这一功能就需要一些辅助技术，用得最多的技术就是浏览器的 Cookie，而在 Java Web 开发中，用的比较多的是 Session，将用户登录的信息存放其中，这样就可以通过读取 Cookie 或者 Session 中的数据获得用户的登录信息，从而达到记录状态、验证用户这一目的。</p>
<h4 id="3">3. 用户眼中的登录</h4>
<p>用户系统是很多产品最基础的构成之一，在设计和规划系统时首先应该想到的就是登陆功能，账号密码优先是最常见的一种登录注册设计，适用于普遍场景，这种方式也有利于产品引导用户完善更多的资料，留存自己的用户信息。淘宝以淘宝账号密码登录为最优先，京东则以京东账号密码登录为最优先，知乎也是以账号密码登录为最优先，且会隐藏第三方授权登录，QQ 是以 QQ 号和密码为登录形式。</p>
<p>由身边比较常用的例子也可以看出账密登录是多么普遍的形式，账号可以是用户名，可以是手机号，可以是 QQ 号码等多种形式，但是最终在功能实现中它们都被称作账号，账号+密码构成了最常见的登录形式。</p>
<p><img src="https://images.gitbook.cn/419ea0e0-8e21-11e8-91f2-2b35ab59bab9" alt="taobao-login-page" /></p>
<h3 id="72">7.2 登录流程设计</h3>
<p>前文中简单地介绍了登录是怎么一回事，这一节将会进行本系统的登录流程设计。通过前文的叙述也可以得出登录的本质，即身份验证和登录状态的保持，在实际编码中是如何实现的呢？</p>
<p>首先，在数据库中查询这条用户记录，伪代码如下：</p>
<pre><code>select * from xxx_user where account_number = 'xxxx';
</code></pre>
<p>如果不存在这条记录则表示身份验证失败，登录流程终止；如果存在这条记录，则表示身份验证成功，接下来则需要进行登录状态的存储和验证了，存储伪代码如下：</p>
<pre><code>//通过 Cookie 存储
Cookie cookie = new Cookie("userName",xxxxx);

//通过 Session 存储
session.setAttribute("userName",xxxxx);
</code></pre>
<p>验证逻辑的伪代码如下：</p>
<pre><code>//通过 Cookie 获取需要验证的数据并进行比对校验
Cookie cookies[] = request.getCookies();
if (cookies != null){
    for (int i = 0; i &lt; cookies.length; i++)
           {
               Cookie cookie = cookies[i];
               if (name.equals(cookie.getName()))
               {
                    return cookie;
               }
           }
}

//通过session获取需要验证的数据并进行比对校验
session.getAttribute("userName");
</code></pre>
<p>以上就是通用的登录流程设计，十三以前也做过具体的代码实现，如下面两个项目，朋友们可以自行下载并体验：</p>
<ul>
<li><p><a href="https://github.com/ZHENFENG13/ssm-demo">ssm-demo in Github</a></p></li>
<li><p><a href="https://github.com/ZHENFENG13/ssm-cluster">ssm-cluster in Github</a></p></li>
</ul>
<p>登录的本质就是身份验证和登录状态的保持，不过还有一点不能忽略，就是登录功能的安全验证设计，一般的做法是将密码加密存储，不过千万不要在 Cookie 中存放用户密码，加密的密码也不行。因为这个密码可以被人获取并尝试离线穷举，同样的，有些网站会在 Cookie 中存储一些用户的其他敏感信息，这些都是不安全的行为，十三在前面列举的两个项目的登录功能都有这种问题。在本课程的实战项目中将对登录功能进行优化改造，通过生成用户令牌 Token 的形式进行用户状态的保持和验证，Token 通过一些无状态的数据生成并不包含用户敏感信息。</p>
<p>简版流程图如下：</p>
<p><img src="https://images.gitbook.cn/55f05980-8e21-11e8-aa21-25f031a4e022" alt="login-check-simple" /></p>
<p>当然，还有一些验证操作是必须的，比如前端在发送数据时需要验证数据格式及有效性，后端接口在访问之前也需要验证用户信息是否有效，因此完整版的登录验证流程如下：</p>
<p><img src="https://images.gitbook.cn/6129bb70-8e21-11e8-aa21-25f031a4e022" alt="login-check-detail" /></p>
<h3 id="73">7.3 前端实现</h3>
<h4 id="1-1">1. 页面</h4>
<p>登录功能的流程设计完成之后，我们就要开始登录页面的前端实现了。正如前面介绍，我们选用了 AdminLTE3 作为模板，直接改造其登录页面即可，AdminLTE3 的登录页面如下：</p>
<p><img src="https://images.gitbook.cn/78a9d0a0-8e21-11e8-9d8f-6d52f659a2b6" alt="adminlte-login" /></p>
<p>将文案修改为中文，并微调了一下页面布局，ssm-demo 的登录页面就完成了，页面效果如下：</p>
<p><img src="https://images.gitbook.cn/88670d00-8e21-11e8-bd0f-f38f8b899327" alt="ssm-demo-login" /></p>
<h4 id="2-1">2. 交互</h4>
<ul>
<li>布局。</li>
</ul>
<p><img src="https://images.gitbook.cn/914715a0-8e21-11e8-aa21-25f031a4e022" alt="login-design" /></p>
<p>如上图所示，登录页而包括 “ 标题栏、错误提示区、信息输入区、表单提交区域 ” 。</p>
<ul>
<li>操作。</li>
</ul>
<p>共有两种操作，即 “ 信息输入和请求提交 ” 。</p>
<ul>
<li>反馈效果。</li>
</ul>
<p>根据用户与界面之间发生的交互操作，会产生对应的反馈效果，本页面有两种反馈，一是错误提示区的显示，二是登陆成功后会弹出 Alert 框，以提醒用户进行其他操作。</p>
<ul>
<li>页面跳转。</li>
</ul>
<p>页面跳转有以下三种可能：</p>
<p>跳入：通过前文中的流程设计图可得出本页面的跳入逻辑为 “ 登录状态验证失败则跳转至登录页 ” ；</p>
<p>无操作：未点击登录按钮或者输入信息错误则不跳转；</p>
<p>跳出：登录成功后会跳转至系统首页。</p>
<h4 id="3-1">3. 功能逻辑</h4>
<ul>
<li>参数验证。</li>
</ul>
<p>实现参数验证功能，可参看下面这段代码：</p>
<pre><code>/**
 * 判空
 *
 * @param obj
 * @returns {boolean}
 */
function isNull(obj) {
    if (obj == null || obj == undefined || obj.trim() == "") {
        return true;
    }
    return false;
}

/**
 * 参数长度验证
 *
 * @param obj
 * @param length
 * @returns {boolean}
 */
function validLength(obj, length) {
    if (obj.trim().length &lt; length) {
        return true;
    }
    return false;
}

/**
 * 用户名称验证 4到16位（字母，数字，下划线，减号）
 *
 * @param userName
 * @returns {boolean}
 */
function validUserName(userName) {
    var pattern = /^[a-zA-Z0-9_-]{4,16}$/;
    if (pattern.test(userName.trim())) {
        return (true);
    } else {
        return (false);
    }
}

/**
 * 用户密码验证 最少6位，最多20位字母或数字的组合
 *
 * @param password
 * @returns {boolean}
 */
function validPassword(password) {
    var pattern = /^[a-zA-Z0-9]{6,20}$/;
    if (pattern.test(password.trim())) {
        return (true);
    } else {
        return (false);
    }
}
</code></pre>
<p>运行以上代码，一旦 JavaScript 验证参数有误则会在错误提示区显示对应的错误标示。如下图所示：</p>
<p><img src="https://images.gitbook.cn/86463df0-8e23-11e8-80d1-2d51ff7e1c55" alt="js-check" /></p>
<ul>
<li>发送 AJAX 请求。</li>
</ul>
<p>下面这段代码完成了 AJAX 请求的发送：</p>
<pre><code>    var userName = $("#userName").val();
    var password = $("#password").val();
    var data = {"userName": userName, "password": password}
    $.ajax({
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "users/login",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (result) {
        }
    });
</code></pre>
<ul>
<li>保存 Token 并跳转页面。</li>
</ul>
<p>通过 AJAX 请求获取到返回的数据，然后对数据进行存储：</p>
<pre><code>setCookie("token", result.data.userToken);
alert("登录成功");
window.location.href = "/";
</code></pre>
<p>setCookie() 方法实现如下：</p>
<pre><code>/**
 * 写入cookie
 *
 * @param name
 * @param value
 */
function setCookie(name, value) {
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + ";path=/";

}
</code></pre>
<h3 id="74">7.4 后端实现</h3>
<h4 id="1-2">1. 表结构设计</h4>
<p>用户模块表结构设计如下，直接导入 tb<em>admin</em>user.sql 即可：</p>
<pre><code># tb_admin_user.sql

DROP TABLE IF EXISTS `tb_admin_user`;

CREATE TABLE `tb_admin_user` (
  `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `user_name` varchar(20) NOT NULL DEFAULT '' COMMENT '用户名',
  `password_md5` varchar(50) NOT NULL DEFAULT '' COMMENT '密码',
  `user_token` varchar(50) NOT NULL DEFAULT '' COMMENT 'token值',
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否已删除 0未删除 1已删除',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `tb_admin_user` (`id`, `user_name`, `password_md5`, `user_token`, `is_deleted`, `create_time`)
VALUES    (1,'admin','e10adc3949ba59abbe56e057f20f883e','6f1d93269e8bfdcd2066a248bfdafee6',0,'2018-07-04 11:21:14');
</code></pre>
<h4 id="2-2">2. 功能实现</h4>
<p>通过用户名和密码查询用户记录，在 AdminUserDao.xml 添加以下代码：</p>
<pre><code>    &lt;select id="getAdminUserByUserNameAndPassword" resultMap="AdminUserResult"&gt;
        select id,user_name,user_token
        from tb_admin_user
        where user_name = #{userName} and password_md5 = #{passwordMD5}
        and is_deleted = 0
        ORDER BY  id DESC limit 1
    &lt;/select&gt;
</code></pre>
<p>业务层代码如下：</p>
<pre><code>    public AdminUser updateTokenAndLogin(String userName, String password) {
        AdminUser adminUser = adminUserDao.getAdminUserByUserNameAndPassword(userName, MD5Util.MD5Encode(password, "UTF-8"));
        if (adminUser != null) {
            //登录后即执行修改token的操作
            String token = getNewToken(System.currentTimeMillis() + "", adminUser.getId());
            if (adminUserDao.updateUserToken(adminUser.getId(), token) &gt; 0) {
                //返回数据时带上token
                adminUser.setUserToken(token);
                return adminUser;
            }
        }
        return null;
    }
</code></pre>
<p>我们再来看控制层代码。首先对参数进行校验，之后调用 adminUserService 业务层代码查询用户对象，接着将其封装到 Result 对象中并返回给前端，代码如下：</p>
<pre><code>    @RequestMapping(value = "/login", method = RequestMethod.POST)
    public Result login(@RequestBody AdminUser user) {
        Result result = ResultGenerator.genFailResult("登录失败");
        if (StringUtils.isEmpty(user.getUserName()) || StringUtils.isEmpty(user.getPassword())) {
            result.setMessage("请填写登录信息！");
        }
        AdminUser loginUser = adminUserService.updateTokenAndLogin(user.getUserName(), user.getPassword());
        if (loginUser != null) {
            result = ResultGenerator.genSuccessResult(loginUser);
        }
        return result;
    }
</code></pre>
<p>至此，登录功能完成，前端页面获取用户输入的账户和密码并提交至后端控制器。后端进行逻辑判断，不成功则返回登录失败，成功则生成新的 Token 值并更新数据库，同时将 Token 返回至前端，前端再进行存储保存。</p>
<p><img src="https://images.gitbook.cn/9e12d760-8e21-11e8-80d1-2d51ff7e1c55" alt="login-success-token" /></p>
<h4 id="3-2">3. 登录状态保持</h4>
<p>完成登录功能后，则需要对用户的登录状态进行验证，这里所说的登录状态保持即 “ Token 值是否存在及 Token 值是否有效 ” 。</p>
<p>Token 值是否存在的判断，我们在前端实现，代码如下：</p>
<pre><code>/**
 * 检查cookie
 */
function checkCookie() {
    if (getCookie("token") == null) {
        $('#tip').html("正在跳转至登录页面...");
        alert("未登录！");
        window.location.href = "login.html";
    }
}
</code></pre>
<p>登录页面不需要判断 Cookie 中是否存在 Token 值，但是其他页面都需要判断，如果不存在则为未登录状态，我们将此抽取出公共的 JavaScript 方法进行验证，在每个页面执行  onLoad() 方法时进行判断。</p>
<p>而 Token 值是否有效则通过后端代码实现，由于大部分接口都需要进行登录验证，如果每个方法都添加查询用户数据的语句则有些多余，因此对方法做了抽取，通过注解切面的形式来返回用户信息。</p>
<p>我们自定义 TokenToUser 注解，使用注解和 AOP 方式将用户对象注入到方法中：</p>
<pre><code># TokenToUser.java

@Target({ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface TokenToUser {

    /**
     * 当前用户在request中的名字
     *
     * @return
     */
    String value() default "user";

}
</code></pre>
<p>TokenToUser 注解切面方法的实现如下：</p>
<pre><code># TokenToUserMethodArgumentResolver.java

public class TokenToUserMethodArgumentResolver implements HandlerMethodArgumentResolver {
    @Resource
    private AdminUserService adminUserService;

    public TokenToUserMethodArgumentResolver() {
    }

    public boolean supportsParameter(MethodParameter parameter) {
        if (parameter.hasParameterAnnotation(TokenToUser.class)) {
            return true;
        }
        return false;
    }

    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
        if (parameter.getParameterAnnotation(TokenToUser.class) instanceof TokenToUser) {
            AdminUser user = null;
            String token = webRequest.getHeader("token");
            if (null != token &amp;&amp; !"".equals(token)) {
                user = adminUserService.getAdminUserByToken(token);
            }
            return user;
        }
        return null;
    }

}
</code></pre>
<p>Spring MVC 配置文件中增加如下配置使 TokenToUser 注解生效：</p>
<pre><code>&lt;mvc:argument-resolvers&gt;
  &lt;bean class="com.ssm.demo.controller.handler.TokenToUserMethodArgumentResolver"/&gt;
&lt;/mvc:argument-resolvers&gt;
</code></pre>
<p>这样，需要进行登录判断的接口加上 @TokenToUser 注解即可，之后再进行相应的逻辑判断，十三也增加了两个接口进行状态保持的测试，请看下面代码：</p>
<pre><code># TestLoginController.java
@RequestMapping(value = "/test1", method = RequestMethod.GET)
    public Result test1(@TokenToUser AdminUser user) {
        //此接口含有@TokenToUser注解，即需要登陆验证的接口。
        Result result = null;
        if (user == null) {
            //如果通过请求header中的token未查询到用户的话即token无效，登陆验证失败，返回未登录错误码。
            result = ResultGenerator.genErrorResult(Constants.RESULT_CODE_NOT_LOGIN, "未登录！");
        } else {
            //登陆验证通过。
            result = ResultGenerator.genSuccessResult("登陆验证通过");
        }
        return result;
    }

    @RequestMapping(value = "/test2", method = RequestMethod.GET)
    public Result test2() {
        //此接口不含@TokenToUser注解，即访问此接口无需登陆验证，此类接口在实际开发中应该很少，为了安全起见应该所有接口都会做登陆验证。
        Result result = ResultGenerator.genSuccessResult("此接口无需登陆验证，请求成功");
        //直接返回业务逻辑返回的数据即可。
        return result;
    }
</code></pre>
<p>打开 login-status-test.html 页面即可进行简单的测试，过程如下：</p>
<p><img src="https://images.gitbook.cn/b59e8550-8e21-11e8-aa21-25f031a4e022" alt="no-valid" /></p>
<p>首先测试无需身份验证的接口，可以看到，由于不需要登录验证，接口直接返回了数据。</p>
<p><img src="https://images.gitbook.cn/bf05e660-8e21-11e8-bd0f-f38f8b899327" alt="token-valid" /></p>
<p>之后是测试需要身份验证的接口，可以看到，如果请求中不存在 Token 或者 Token 值是错误的，则验证身份失败，返回错误码 402，而如果填入正确的 Token 值，则返回登录验证成功。</p>
<blockquote>
  <p>返回的 resultCode 为自定义的值，与 HTTP 状态码不是同一个含义，其定义在 Constants.java 类中，可自行定义，只要前后端保持一致即可。</p>
</blockquote>
<h3 id="75">7.5 总结</h3>
<p>文中所涉及到的代码和 SQL 语句，十三都已经压缩且上传到百度云，提取地址如下：</p>
<blockquote>
  <p>链接：https://pan.baidu.com/s/15lzIb35vJ2X3yjsXQskScQ </p>
  <p>密码：6ko4</p>
</blockquote>
<p>下载后将数据库文件导入数据库即可，代码解压后直接打开即可使用。</p></div></article>