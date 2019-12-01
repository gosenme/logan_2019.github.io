---
title: SSM 博客系统开发实战-14
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>使用 QQ 第三方登录时要调用第三方接口，需要 AppID 和 AppKey 等信息，所以首先要申请注册一下。</p>
<h3 id="">申请注册</h3>
<p>首先在百度搜索 QQ 互联或者点击下面链接进入 QQ 互联官网：</p>
<blockquote>
  <p>https://connect.qq.com/index.html</p>
</blockquote>
<p>往下滚动鼠标找到网站应用，然后点击开始创建，如下图：</p>
<p><img src="https://images.gitbook.cn/bac39390-85e3-11e8-b961-fbe741e59414" alt="" /></p>
<p>之后会进入个人资料填写页面，选择“个人接入”，填写好个人信息后点击下一步，注意身份证照片是手持身份证正面拍摄的照片。如图：</p>
<p><img src="https://images.gitbook.cn/ef212f80-85e3-11e8-874c-05f8b45d1ec0" alt="" /></p>
<p>接着会让你去邮箱激活，点击邮件内的激活链接，会提示恭喜注册成功，然后点击前往管理中心，可看到开发者提交审核的状态，如下图：</p>
<p><img src="https://images.gitbook.cn/10aab220-85e4-11e8-a763-1bea49a489d8" alt="" /></p>
<p>上面提示说审核要7个工作日，我直接找的在线客服，结果很快就审核通过了。</p>
<p>审核通过之后点击“创建应用”，选择“创建网站应用”，填写资料后，点击“创建应用”，如下图：</p>
<p><img src="https://images.gitbook.cn/4419f670-85e4-11e8-a763-1bea49a489d8" alt="" /></p>
<p>进入到完善资料页面，需要填写网站域名、回调域等，填写完成之后点击创建应用。其中回调域多写一个用于本地测试，以 <code>http://localhost</code> 开头，以后还可以修改。没有提供方和备案号的同学可随便填，能创建应用就行，主要是为了获取 AppID 和 AppKey，如下图：</p>
<p><img src="https://images.gitbook.cn/83aed170-85e4-11e8-874c-05f8b45d1ec0" alt="" /></p>
<p>到此，创建应用就成功了，前往管理中心查看，如图：</p>
<p><img src="https://images.gitbook.cn/b01a2020-85e4-11e8-82dd-f91cad43af13" alt="" /></p>
<p>状态处于审核中，找在线客户，审核会很快。</p>
<p>点击查看可以看到你的 AppID 和 AppKey，这两个信息是我们程序中要使用的，记得要保密，不要透露给他人。</p>
<h3 id="qq">QQ 快捷登录</h3>
<p>用户在没有账号的情况下允许第三方 QQ 登录。我们接下来看下具体实现步骤。</p>
<h4 id="qq-1">在注册页面、登录页面添加 QQ 登录图标</h4>
<p>QQ 图标可从 QQ 互联官网下载，我会将 QQ 图标放在百度网盘，大家可以在 <code>webapp/images</code> 目录下找到。</p>
<p>这里以注册页面为例，将注册页面的右侧 div 修改如下：</p>
<pre><code>    &lt;div id="regist-right" class="bj_right" style="height: 468px"&gt;
        &lt;p&gt;使用以下账号直接登录&lt;/p&gt;
        &lt;div&gt;
          &lt;a href="to_login"&gt;&lt;img src="${ctx}/images/Connect_logo_3.png" /&gt;&lt;/a&gt;
        &lt;/div&gt;
        &lt;p&gt;已有账号？&lt;a href="login.html"&gt;立即登录&lt;/a&gt;&lt;/p&gt;

     &lt;/div&gt;
</code></pre>
<p>修改后效果如图：</p>
<p><img src="https://images.gitbook.cn/05cbfde0-85e5-11e8-a3b4-1ffc1e78d8d5" alt="" /></p>
<h4 id="sdk">下载 SDK</h4>
<p>SDK 的下载地址请见下：</p>
<blockquote>
  <p>http://wiki.connect.qq.com/sdk%E4%B8%8B%E8%BD%BD</p>
</blockquote>
<p>找到 Java 的 SDK 进行下载，下载完成后进行解压，将解压目录的 Sdk4J.jar 打包到 Maven 仓库，和之前方法一样，打开命令窗口输入：</p>
<pre><code>mvn install:install-file -Dfile=D:\sdk\Sdk4J.jar -DgroupId=wang.dreamland.www -DartifactId=Sdk4J -Dversion=1.0.0 -Dpackaging=jar -DgeneratePom=true -DcreateChecksum=true
</code></pre>
<p>引入刚刚打包的依赖：</p>
<pre><code>&lt;!--qq--&gt;
&lt;dependency&gt;
    &lt;groupId&gt;wang.dreamland.www&lt;/groupId&gt;
    &lt;artifactId&gt;Sdk4J&lt;/artifactId&gt;
    &lt;version&gt;1.0.0&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>然后将解压目录的 qqconnectconfig.properties 配置文件复制到项目的 resources 资源目录下，修改其中前三项，将 <code>app_ID</code>、<code>app_KEY</code> 和回调地址 <code>redirect_URI</code> 替换成自己刚才注册申请的。</p>
<h4 id="qq-2">QQ 授权登录流程</h4>
<p>QQ 授权登录流程如下图所示：</p>
<p><img src="https://images.gitbook.cn/564a1220-85e5-11e8-9017-15174b84fe15" alt="" /></p>
<p>主要包括四大步：</p>
<ol>
<li><p>用户点击 QQ 登录按钮（<code>/to_login"</code>）；</p></li>
<li><p>后台 LoginController 收到请求后，根据配置文件获取 AppID、Scope 和回调地址等参数信息，然后重定向到 QQ 授权登录页面并携带上述参数；</p></li>
<li><p>进入授权登录页面之后，用户扫码或者点击头像授权后，会跳向我们配置的回调地址 <code>http://localhost:8080/qq_login</code>，并携带上述参数；</p></li>
<li><p>后台 LoginController 收到登录请求（<code>/qq_login</code>）后，通过上述参数调用第三方 API 获取 AccessToken 对象，该对象就包含了用户唯一标识 OpenID、AccessToken 和 QQ 昵称、QQ 头像等。将我们需要的信息存入数据库中之后返回到个人主页，完成 QQ 授权登录。</p></li>
</ol>
<h4 id="-1">实现步骤</h4>
<p>首先设计一张 <code>open_user</code> 表，用于储存第三方登录用户信息，包括以下字段：</p>
<pre><code>    id              //主键        
    u_id            //用户id
    open_id         //用户唯一标识
    access_token    //授权令牌
    nick_name       //qq昵称
    avatar          //qq头像
    open_type       //第三方类型，比如QQ、WEIXIN、WEIBO
    expired_time    //授权令牌过期时间，默认为三个月
</code></pre>
<p><code>open_user.sql</code> 文件已放入文末的百度网盘中。</p>
<p>接着，生成对应实体类 OpenUser，然后书写 OpenUserService 接口、OpenUserServiceImpl 实现类和 OpenUserMapper 接口。</p>
<p>这里就不再介绍生成过程了，我会直接将相关文件放在文末的百度网盘中。</p>
<p>然后，在 common 包下的 Constants 类下新增第三方类型常量：</p>
<pre><code>    public static final String OPEN_TYPE_QQ = "QQ";
    public static final String OPEN_TYPE_WEIXIN = "WEIXIN";
    public static final String OPEN_TYPE_WEIBO = "WEIBO";
</code></pre>
<p>紧接着，在 LoginController.java 中创建映射 URL 为 <code>/to_login</code> 的方法：</p>
<pre><code>    @RequestMapping("/to_login")
    public String toLogin(Model model) {
        HttpServletRequest request = getRequest();
        String url = "";
        try {
            url = new Oauth().getAuthorizeURL(request);
        } catch (QQConnectException e) {
            e.printStackTrace();
        }
        return "redirect:"+url;
    }
</code></pre>
<p>调用第三方接口 API 获取 URL，URL 中携带了 <code>client_id</code> 即 AppID、Scope 和回调地址等，然后重定向到该 URL。</p>
<p>关于各个参数的含义 QQ 互联官方文档上有详细说明，这里就不做介绍了。</p>
<p>用户扫码或者点击 QQ 头像登录后，会跳至我们配置的回调地址，在 LoginController 中创建映射 URL 为 <code>qq_login</code> 的方法：</p>
<pre><code>    @Autowired
    private OpenUserService openUserService;
    @RequestMapping("/qq_login")
    public String qqLogin(Model model) {
        User user = null;
        try {
            AccessToken accessTokenObj = (new Oauth()).getAccessTokenByRequest(getRequest());
            String accessToken   = null, openID   = null;
            long tokenExpireIn = 0L;
            if (accessTokenObj.getAccessToken().equals("")) {
                System.out.print("没有获取到响应参数");
            } else {
                accessToken = accessTokenObj.getAccessToken();//授权令牌token
                tokenExpireIn = accessTokenObj.getExpireIn();//过期时间

                // 利用获取到的accessToken 去获取当前用的openid -------- start
                OpenID openIDObj =  new OpenID(accessToken);
                openID = openIDObj.getUserOpenID();//用户唯一标识
                // 利用获取到的accessToken 去获取当前用户的openid --------- end

                UserInfo qzoneUserInfo = new UserInfo(accessToken, openID);
                UserInfoBean userInfoBean = qzoneUserInfo.getUserInfo();
                if (userInfoBean.getRet() == 0) {
                    OpenUser openUser =  openUserService.findByOpenId( openID );
                    if(openUser == null){
                        redisTemplate.opsForValue().set(openID, accessToken, 90, TimeUnit.DAYS);// 有效期三个月
                        openUser = new OpenUser();
                        user = new User();
                        user.setEmail( openID );
                        user.setPassword(MD5Util.encodeToHex(Constants.SALT+accessToken) );
                        user.setEnable( "0" );
                        user.setState("1");
                        user.setNickName( userInfoBean.getNickname() );//设置qq昵称
                        user.setImgUrl( userInfoBean.getAvatar().getAvatarURL50() );//设置qq头像
                        userService.regist( user );
                        openUser.setOpenId( openID );
                        openUser.setAccessToken( accessToken );
                        openUser.setAvatar( userInfoBean.getAvatar().getAvatarURL50() );
                        openUser.setExpiredTime( tokenExpireIn);
                        openUser.setNickName( userInfoBean.getNickname() );
                        openUser.setOpenType( Constants.OPEN_TYPE_QQ );
                        openUser.setuId( user.getId());
                        openUserService.add( openUser );
                    }else {
                         String token = redisTemplate.opsForValue().get( openID );//从redis获取accessToken
                        if(token==null){
                            //已过期
                            openUser.setAccessToken( accessToken );
                            openUser.setAvatar( userInfoBean.getAvatar().getAvatarURL50() );
                            openUser.setExpiredTime( tokenExpireIn);
                            openUser.setNickName( userInfoBean.getNickname() );
                            openUserService.update(openUser);
                        }
                        user = userService.findById( openUser.getuId() );
                    }

                } else {
                    log.info("很抱歉，我们没能正确获取到您的信息，原因是： " + userInfoBean.getMsg());
                }

            }
        } catch (QQConnectException e) {
            e.printStackTrace();
        }
        getSession().setAttribute("user",user);
        return "redirect:/list";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）Autowired 通过 <code>@Autowired</code> 注入 OpenUserService 对象。</p>
<p>（2）调用第三方 API 获取 AccessToken 对象，根据 AccessToken 对象获取授权令牌和令牌过期时间。</p>
<p>（3）调用第三方 API 根据授权令牌获取 OpenID 对象，根据 OpenID 获取用户唯一标识 OpenID。</p>
<p>（4）根据授权令牌 AccessToken 和用户唯一标识 OpenID 获取 UserInfo 对象，注意这里的 UserInfo 是第三方的实体类，注意导包：</p>
<pre><code>import com.qq.connect.api.qzone.UserInfo;
</code></pre>
<p>（5）根据 UserInfo 对象调用 getUserInfo 获取 QQ 用户信息对象 UserInfoBean，该对象包含了 QQ 用户的基本信息：昵称、头像、性别等。</p>
<p>（6）根据用户唯一标识 OpenID 查询 <code>open_user</code> 表，判断该 QQ 用户是否存在，如果不存在则将 AccessToken 保存到 Redis 中，有效期为三个月，key 为 OpenID，然后创建 OpenUser 对象。因为是 QQ 第三方临时登录，此时还没有 User 信息，所以先创建 User 对象，给它分配一个账号和密码，账号就用 OpenID，密码就用经过 MD5 加密后的 AccessToken，当然这里的 Email 账号是不正确的，这里只是临时让用户使用，以后引导用户修改相关信息，然后再设置 state、nickName 等信息，设置完以后插入 user 表中，然后将 OpenID、AccessToken 等其他信息保存到 <code>open_user</code> 表中。</p>
<p>（7）如果查询结果不为空，说明该 QQ 用户已经登录过，根据 OpenID 从 Redis 中查询 AccessToken，判断是否为 null，为 null 则代表授权令牌已过期，则更新 OpenUser 相关信息，然后根据用户 id 查询出用户 User。</p>
<p>（8）最后将用户 user 保存到 Session 中，返回用户个人主页。</p>
<p>重新启动项目，测试第三方 QQ 登录成功！</p>
<p>但是进入修改资料查看，发现账号显示的是 OpenID：</p>
<p><img src="https://images.gitbook.cn/05524f20-85e7-11e8-b961-fbe741e59414" alt="" /></p>
<p>这样肯定是不行的。</p>
<p>所以在进入 profile.jsp 之前进行判断，如果用户 Email 不包含 <code>@</code> 则认为是第三方登录，引导其进行账号设置。</p>
<h3 id="qq-3">QQ 账号绑定</h3>
<p><img src="https://images.gitbook.cn/279d4d00-85e7-11e8-913e-e3a36745e310" alt="" /></p>
<h4 id="-2">引导用户设置信息</h4>
<p>我们先梳理下思路。其过程是这样：点击修改个人资料时，判断用户是否是第三方登录且没有绑定账号，如果是则弹出设置账号信息的窗口，引导其进行账号设置。如果已经绑定账号则直接跳转到 profile.jsp 页面。</p>
<p>整个过程主要包括以下几个步骤。</p>
<p><strong>1.</strong> 点击修改个人资料，触发点击事件 updateProfile，方法如下：</p>
<pre><code>function updateProfile(email) {
  if(email.indexOf("@")!=-1){
  window.location.href = "${ctx}/profile";
  }else{
   $('#myModal').modal('toggle', 'center');
  }

}
</code></pre>
<p>判断是否包含 <code>@</code>，如果有则认为已经是注册用户或者是已绑定账号用户，直接跳转到个人资料修改页面。</p>
<p>如果不包含 <code>@</code>，则认为是第三方登录且未绑定账号的用户，弹出信息设置页面，引导其进行设置。</p>
<p><strong>2.</strong> 在 personal.jsp 中引入弹窗 div，弹窗来自 ZUI，经过改造而成，如下：</p>
<pre><code>    &lt;!-- 弹出设置信息对话框 --&gt;
    &lt;div class="modal fade" id="myModal"&gt;
    &lt;div class="modal-dialog" style="width: 0px;margin-left: 550px;"&gt;
        &lt;div class="modal-content"&gt;
            &lt;div class="tab-pane fade in active" id="account-login"&gt;
                &lt;div class="content" &gt;
                    &lt;div class="col-sm-6 col-sm-offset-3 col-md-4 col-sm-offset-4 login-box" style="width: 450px;height: 260px;"&gt;
                        &lt;span id="update-span" style="color: red"&gt;&lt;/span&gt;
                        &lt;form id="normal_form" name="form" role="form" class="login-form" action="${ctx}/profile" method="post"&gt;
                            &lt;div class="form-group"&gt;
                                &lt;label for="email" class="sr-only"&gt;用户名&lt;/label&gt;
                                &lt;input type="text" id="email" name="email" onblur="checkEmail();" class="form-control" placeholder="邮箱账号"&gt;
                            &lt;/div&gt;
                            &lt;div class="form-group"&gt;
                                &lt;label for="password" class="sr-only"&gt;密码&lt;/label&gt;
                                &lt;input type="password" id="password" onblur="checkPassword();" name="password" class="form-control" placeholder="密码"&gt;
                            &lt;/div&gt;
                            &lt;div class="form-group"&gt;
                                &lt;label for="phone" class="sr-only"&gt;手机号&lt;/label&gt;
                                &lt;input type="text" id="phone" name="phone" onblur="checkPhone();" class="form-control" placeholder="手机号"&gt;
                            &lt;/div&gt;
                        &lt;/form&gt;
                        &lt;div class="form-group" style="margin-top: 30px "&gt;
                            &lt;div style="width: 80px;float: left"&gt;
                                &lt;button type="button" id="btn" onclick="sure();"  class="btn btn-primary btn-block"&gt;确定&lt;/button&gt;
                            &lt;/div&gt;
                            &lt;div style="width: 80px;float: left;margin-left: 30px"&gt;
                                &lt;button type="button" id="cancle" onclick="cancle();" class="btn btn-primary btn-block"&gt;取消&lt;/button&gt;
                            &lt;/div&gt;


                        &lt;/div&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;/div&gt;
</code></pre>
<p><strong>3.</strong> 设置 CSS 样式:</p>
<pre><code>    .login-box {
            background: white;
            box-shadow: 0 0 0 15px rgba(255, 255, 255, .1);
            border-radius: 5px;
            padding: 40px;
        }
</code></pre>
<p><strong>4.</strong> 启动访问效果如下：</p>
<p><img src="https://images.gitbook.cn/d4663dd0-85e7-11e8-8c2b-23cfc86b8cf2" alt="" /></p>
<p><strong>5.</strong> 对表单分别进行离焦校验，判断其正确性，这里的校验和之前一样，就不再赘述了。</p>
<p><strong>6.</strong> 如果用户点击取消，则隐藏弹窗，取消按钮点击事件如下：</p>
<pre><code>//取消
function cancle() {
    $('#myModal').modal('hide');
}
</code></pre>
<p><strong>7.</strong> 以上校验都正确之后便提交表单，确定按钮点击事件如下：</p>
<pre><code>//确定
function sure() {
    if(checkEmail() &amp;&amp; checkPassword() &amp;&amp; checkPhone()){
        $("#normal_form").submit();
        alert("激活邮件已发送，请前往邮箱查看并激活账号！");
    }else{
        $("#update-span").text("请将信息填写完整！");
    }
}
</code></pre>
<p><strong>8.</strong> 修改后台 PersonalController 的 profile 方法，如下：</p>
<pre><code>@Autowired
private OpenUserService openUserService;
@RequestMapping("/profile")
public String profile(Model model, @RequestParam(value = "email",required = false) String email,
                      @RequestParam(value = "password",required = false) String password,
                      @RequestParam(value = "phone",required = false) String phone) {
    User user = (User)getSession().getAttribute("user");
    if(user==null){
        return "../login";
    }

    if(StringUtils.isNotBlank(email)){
        user.setEmail(email);
        user.setPassword(MD5Util.encodeToHex(Constants.SALT+password));
        user.setPhone(phone);
        userService.update(user);
    }
    List&lt;OpenUser&gt; openUsers = openUserService.findByUid(user.getId());
    if(openUsers!=null &amp;&amp; openUsers.size()&gt;0){
        for(OpenUser openUser:openUsers){
            if(Constants.OPEN_TYPE_QQ.equals(openUser.getOpenType())){
                    model.addAttribute("qq",openUser.getOpenType());
                }else if(Constants.OPEN_TYPE_WEIBO.equals(openUser.getOpenType())){
                    model.addAttribute("weibo",openUser.getOpenType());
                }else if(Constants.OPEN_TYPE_WEIXIN.equals(openUser.getOpenType())){
                    model.addAttribute("weixin",openUser.getOpenType());
                }
            }
        }     
        UserInfo userInfo =   userInfoService.findByUid(user.getId());
        model.addAttribute("user",user);
        model.addAttribute("userInfo",userInfo);

        return "personal/profile";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入 OpenUserService 对象。</p>
<p>（2）判断用户是否为 null，如果是则跳转到登录页面。</p>
<p>（3）判断 Email 是否为空，如果不为空，说明用户进行了信息设置，则将相关信息添加到 user 对象中，最后更新用户表信息。</p>
<p>（4）根据用户 id 查询 <code>open_user</code> 表，会得到一个 List 集合，如果 List 不为空并且长度大于0，则至少是某一种第三方登录，遍历集合，如果是 QQ 第三方登录，则将 QQ 添加到 model 中，其他同理，主要用于后续的账号绑定判断。</p>
<p>（5）查询用户详细信息并添加到 model 中，将 user 也添加到 model 中，最后返回个人资料修改页面。</p>
<p><strong>9.</strong> 修改 profile.jsp 页面，判断是否已绑定第三方账号，以 QQ 为例：</p>
<pre><code>     &lt;c:if test="${empty qq}"&gt;
          &lt;div style="float: left;"&gt;
              Q Q：未绑定
           &lt;/div&gt;
           &lt;div style="float: left;margin-left: 150px"&gt;
                   &lt;span id="qq_span" style="color: grey" onmouseover="changeColor(this);" onmouseout="backColor(this);"&gt;立即绑定&lt;/span&gt;
           &lt;/div&gt;
      &lt;/c:if&gt;
      &lt;c:if test="${not empty qq}"&gt;
          &lt;div style="float: left;"&gt;
              Q Q：已绑定
           &lt;/div&gt;
           &lt;div style="float: left;margin-left: 150px"&gt;
                            &lt;span id="qq_span_remove" style="color: grey" onmouseover="changeColor(this);" onmouseout="backColor(this);"&gt;解除绑定&lt;/span&gt;
            &lt;/div&gt;
       &lt;/c:if&gt;
</code></pre>
<p>上面代码，根据 EL 表达式判断 QQ 是否为空，为空，则显示“未绑定——立即绑定”，不为空则显示“已绑定——解除绑定”。</p>
<p>效果如图：</p>
<p><img src="https://images.gitbook.cn/bcc516a0-85e8-11e8-a763-1bea49a489d8" alt="" /></p>
<h4 id="-3">绑定与解除绑定</h4>
<h5 id="qq-4"><strong>QQ 绑定</strong></h5>
<p>假如现在是一个已有账号的用户，点击立即绑定 QQ，会触发和刚开始点击 QQ 快捷登录一样的事件：</p>
<pre><code>//qq绑定
function binding_qq() {
    window.location.href = "${ctx}/to_login";
}
</code></pre>
<p>返回到授权登录页面后，用户点击授权，进入 LoginController 中映射 URL 为 <code>qq_login</code> 的方法，将其方法修改如下：</p>
<pre><code>@RequestMapping("/qq_login")
public String qqLogin(Model model) {
    User user = (User)getSession().getAttribute("user");
    boolean flag =false;
    try {
        AccessToken accessTokenObj = (new Oauth()).getAccessTokenByRequest(getRequest());
        String accessToken   = null, openID   = null;
        long tokenExpireIn = 0L;
        if (accessTokenObj.getAccessToken().equals("")) {
            System.out.print("没有获取到响应参数");
        } else {
            accessToken = accessTokenObj.getAccessToken();//授权令牌token
            tokenExpireIn = accessTokenObj.getExpireIn();//过期时间

            // 利用获取到的accessToken 去获取当前用的openid -------- start
            OpenID openIDObj =  new OpenID(accessToken);
            openID = openIDObj.getUserOpenID();//用户唯一标识
            // 利用获取到的accessToken 去获取当前用户的openid --------- end

            UserInfo qzoneUserInfo = new UserInfo(accessToken, openID);
            UserInfoBean userInfoBean = qzoneUserInfo.getUserInfo();
            if (userInfoBean.getRet() == 0) {
                OpenUser openUser =  openUserService.findByOpenId( openID );
                if(openUser == null){
                    redisTemplate.opsForValue().set(openID, accessToken, 90, TimeUnit.DAYS);// 有效期三个月
                    openUser = new OpenUser();
                    if(user==null){
                        flag = true;
                        user = new User();
                        user.setEmail( openID );
                            user.setPassword(MD5Util.encodeToHex(Constants.SALT+accessToken) );
                        user.setEnable( "1" );
                        user.setState("0");
                        user.setNickName( userInfoBean.getNickname() );//设置qq昵称
                        user.setImgUrl( userInfoBean.getAvatar().getAvatarURL50() );//设置qq头像
                        userService.regist( user );
                    }
                    openUser.setOpenId( openID );
                    openUser.setAccessToken( accessToken );
                    openUser.setAvatar( userInfoBean.getAvatar().getAvatarURL50() );
                    openUser.setExpiredTime( tokenExpireIn);
                    openUser.setNickName( userInfoBean.getNickname() );
                    openUser.setOpenType( Constants.OPEN_TYPE_QQ );
                    openUser.setuId( user.getId());
                    openUserService.add( openUser );
                }else {
                    String token = redisTemplate.opsForValue().get( openID );//从redis获取accessToken
                    if(token==null){
                        //已过期
                        openUser.setAccessToken( accessToken );
                        openUser.setAvatar( userInfoBean.getAvatar().getAvatarURL50() );
                        openUser.setExpiredTime( tokenExpireIn);
                        openUser.setNickName( userInfoBean.getNickname() );
                        openUserService.update(openUser);
                    }
                    user = userService.findById( openUser.getuId() );
                }

            } else {
                    log.info("很抱歉，我们没能正确获取到您的信息，原因是： " + userInfoBean.getMsg());
            }

        }
    } catch (QQConnectException e) {
        e.printStackTrace();
    }
    getSession().setAttribute("user",user);
    if(flag){
        return "redirect:/list";
    }else {
        model.addAttribute("qq",Constants.OPEN_TYPE_QQ );
        wang.dreamland.www.entity.UserInfo userInfo =   userInfoService.findByUid(user.getId());
        model.addAttribute("user",user);
        model.addAttribute("userInfo",userInfo);
        return "personal/profile";
    }
}
</code></pre>
<p>主要修改如下：</p>
<p>（1）从 Session 中获取用户 User。</p>
<p>（2）设置标志位 flag。</p>
<p>（3）判断如果用户为 null 则将 flag 置为 true 并创建 user，然后设置临时账号、密码等，如果已存在则不进行操作，直接将用户 id 赋值给 OpenUser 对象。</p>
<p>（4）根据标志位 flag 判断跳转页面，如果为 false 则说明用户进行 QQ 绑定设置，将相关信息添加到 model 中，然后返回到个人资料修改页面，如果为 true 则跳转到个人主页。其他的代码和之前一样。</p>
<p>最后启动测试，QQ 账号绑定设置成功！</p>
<h5 id="-4"><strong>解除绑定</strong></h5>
<p>QQ 解除绑定 div 的点击事件如下：</p>
<pre><code>//qq解除绑定
function qq_span_remove() {
    if(confirm("确定解除qq绑定吗？")){
           window.location.href = "${ctx}/remove_qq";
    }
}
</code></pre>
<p>在后台 PersonalController 中创建映射 URL 为 <code>/remove_qq</code> 的方法：</p>
<pre><code>    @RequestMapping("/remove_qq")
    public String removeQQ(Model model){
        User user = (User) getSession().getAttribute("user");
        if(user == null){
            return "../login";
        }
        openUserService.deleteByUidAndType(user.getId(),Constants.OPEN_TYPE_QQ);
        List&lt;OpenUser&gt; openUsers = openUserService.findByUid(user.getId());
        setAttribute(openUsers,model);
        UserInfo userInfo =   userInfoService.findByUid(user.getId());
        model.addAttribute("user",user);
        model.addAttribute("userInfo",userInfo);
        return "personal/profile";
    }

    public void setAttribute(List&lt;OpenUser&gt; openUsers,Model model){
        if(openUsers!=null &amp;&amp; openUsers.size()&gt;0){
            for(OpenUser openUser:openUsers){
                if(Constants.OPEN_TYPE_QQ.equals(openUser.getOpenType())){
                    model.addAttribute("qq",openUser.getOpenType());
                }else if(Constants.OPEN_TYPE_WEIBO.equals(openUser.getOpenType())){
                    model.addAttribute("weibo",openUser.getOpenType());
                }else if(Constants.OPEN_TYPE_WEIXIN.equals(openUser.getOpenType())){
                    model.addAttribute("weixin",openUser.getOpenType());
                }
            }
        }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 中取出 User，判断如果为空直接跳转到登录页面。</p>
<p>（2）根据用户 id 和第三方登录类型删除 OpenUser 对象。</p>
<p>（3）根据用户 id 查询 <code>open_user</code> 表，把其他第三方登录信息查询出来，添加到 model 中，这里将相同方法封装了一下（setAttribute 方法）。</p>
<p>（4）根据用户 id 查询出用户详细信息并添加到 model 中，将 user 页添加到 model 中，然后返回到个人资料修改页面。</p>
<p>最后重启项目测试，解除 QQ 绑定成功！</p>
<blockquote>
  <p>第13课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1TaqfnWfmj9boeobo7fF9Og 密码：oqap</p>
</blockquote>
<p><strong>本课程所开发的项目已经完成，完整代码已托管 Github，大家可通过下面地址下载：</strong></p>
<ul>
<li><a href="https://github.com/wanglinyong/dreamland.git">Github</a></li>
</ul></div></article>