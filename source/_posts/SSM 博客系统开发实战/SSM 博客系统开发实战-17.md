---
title: SSM 博客系统开发实战-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过上一篇的源码分析得知 Spring Security 提供的默认认证方式是根据用户名和密码进行认证的。要想通过手机登录认证就得制定自己的认证策略、认证逻辑以及获取用户信息的逻辑等。</p>
<h3 id="phonenotfoundexception">自定义异常 PhoneNotFoundException</h3>
<p>因为账号登录异常抛的是 UsernameNotFoundException 异常，那么手机登录认证失败我们就抛 PhoneNotFoundException。</p>
<p>在 <code>security.phone</code> 包下新建 PhoneNotFoundException 并继承 AuthenticationException，代码如下：</p>
<pre><code>    public class PhoneNotFoundException extends AuthenticationException {
    public PhoneNotFoundException(String msg, Throwable t) {
        super( msg, t );
    }

    public PhoneNotFoundException(String msg) {
        super( msg );
    }
    }
</code></pre>
<p>主要是两个构造方法。里面调用的是父类的构造方法。接着往上查看会发现都继承自 RuntimeException 运行时异常。</p>
<h3 id="phoneauthenticationtoken">自定义认证令牌 PhoneAuthenticationToken</h3>
<p>账号登录使用的令牌是 UsernamePasswordAuthenticationToken，我们模仿它制定自己的 Token。</p>
<p>在 <code>security.phone</code> 包下新建 PhoneAuthenticationToken 并继承 AbstractAuthenticationToken：</p>
<pre><code>    public class PhoneAuthenticationToken extends AbstractAuthenticationToken {
    private final Object principal;

    public PhoneAuthenticationToken(Object principal) {
        super((Collection)null);
        this.principal = principal;
        this.setAuthenticated(false);
    }

    public PhoneAuthenticationToken(Object principal, Collection&lt;? extends GrantedAuthority&gt; authorities) {
        super(authorities);
        this.principal = principal;
        super.setAuthenticated(true);
    }

    public Object getCredentials() {
        return null;
    }

    public Object getPrincipal() {
        return this.principal;
    }

    public void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException {
        if(isAuthenticated) {
            throw new IllegalArgumentException("Cannot set this token to trusted - use constructor which takes a GrantedAuthority list instead");
        } else {
            super.setAuthenticated(false);
        }
    }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）一个参数的构造方法是将手机号赋值给 principal，然后权限设置为 null，认证状态为 false。</p>
<p>（2）两个参数的构造方法是传入权限集合、用户信息并将认证状态置为 true。</p>
<p>（3）因为我们没有用到密码。所以 getCredentials 返回 null。</p>
<h3 id="phoneauthenticationfilter">自定义认证逻辑过滤器 PhoneAuthenticationFilter</h3>
<p>在 <code>security.phone</code> 包下新建 PhoneAuthenticationFilter 并继承 AbstractAuthenticationProcessingFilter：</p>
<pre><code>    public class PhoneAuthenticationFilter extends AbstractAuthenticationProcessingFilter {
    public static final String phoneParameter = "telephone";
    public static final String codeParameter = "phone_code";
    @Autowired
    private RedisTemplate&lt;String, String&gt; redisTemplate;

    protected PhoneAuthenticationFilter( ) {
        super( new AntPathRequestMatcher("/phoneLogin") );
    }

    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException {
            String phone = this.obtainPhone(request);
            String phone_code = this.obtainValidateCode(request);
            if(phone == null) {
                phone = "";
            }
            if(phone_code == null) {
                phone_code = "";
            }

            phone = phone.trim();
            String cache_code = redisTemplate.opsForValue().get( phone );
            boolean flag = CodeValidate.validateCode(phone_code,cache_code);
            if(!flag){
                throw new PhoneNotFoundException( "手机验证码错误" );
            }
            PhoneAuthenticationToken authRequest = new PhoneAuthenticationToken(phone);
            this.setDetails(request, authRequest);
            return this.getAuthenticationManager().authenticate(authRequest);

    }

    protected void setDetails(HttpServletRequest request, PhoneAuthenticationToken authRequest) {
        authRequest.setDetails(this.authenticationDetailsSource.buildDetails(request));
    }

    protected String obtainPhone(HttpServletRequest request) {
        return request.getParameter(phoneParameter);
    }
    protected String obtainValidateCode(HttpServletRequest request) {
        return request.getParameter(codeParameter);
    }

    }
</code></pre>
<p>代码解读：</p>
<p>（1）将手机号和手机验证码的请求参数名分别赋值给 phoneParameter 和 codeParameter。</p>
<p>（2）通过 <code>@Autowired</code> 注解注入 RedisTemplate 对象。</p>
<p>（3）通过构造方法指定手机登录时的登录 URL 为 <code>/phoneLogin</code>。</p>
<p>（4）通过自定义的 obtainPhone 和 obtainValidateCode 方法获取前台传来的手机号和手机验证码。</p>
<p>（5）获取 Redis 中存储的手机验证码并赋值给 <code>cache_code</code>，然后调用 CodeValidate 类中的 validateCode 方法判断用户输入的手机验证码是否正确。</p>
<p>（6）如果用户输入的手机验证码和 Redis 中存储的不一致则直接报 PhoneNotFoundException 异常，认证失败。</p>
<p>（7）实例化一个 PhoneAuthenticationToken 对象，然后设置请求信息，最后调用认证管理器找到支持该 Token 的 AuthenticationProvider 进行认证，并将认证的结果 Authentication 返回。</p>
<h3 id="phoneuserdetailsservice">自定义获取用户信息逻辑的 PhoneUserDetailsService</h3>
<p>在 <code>security.phone</code> 包下新建 PhoneUserDetailsService 并实现 UserDetailsService 接口：</p>
<pre><code>    public class PhoneUserDetailsService implements UserDetailsService {
    @Autowired
    private UserService userService;
    @Autowired
    private RoleService roleService;

    public UserDetails loadUserByUsername(String phone) throws PhoneNotFoundException {
        User user = userService.findByPhone(phone);
        if(user == null){
            throw new PhoneNotFoundException("手机号码错误");
        }
        List&lt;Role&gt; roles = roleService.findByUid(user.getId());
        user.setRoles(roles);
        return user;
    }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）通过 Autowired 注解注入 UserService 和 RoleService 对象。</p>
<p>（2）根据手机号查询用户 User，如果为 null 则直接抛 PhoneNotFoundException 异常，认证失败。</p>
<p>（3）用户不为 null，通过用户 id 获取用户的角色列表，将角色列表添加到用户 user 中，最后将 user 返回。</p>
<h3 id="phoneauthenticationprovider">自定义手机登录认证策略 PhoneAuthenticationProvider</h3>
<p>在 <code>security.phone</code> 包下新建 PhoneAuthenticationProvider 并实现 AuthenticationProvider 接口：</p>
<pre><code>    public class PhoneAuthenticationProvider implements AuthenticationProvider {

    private UserDetailsService userDetailsService;

    public Authentication authenticate(Authentication authentication) throws AuthenticationException {

        PhoneAuthenticationToken authenticationToken = (PhoneAuthenticationToken) authentication;
        UserDetails userDetails = userDetailsService.loadUserByUsername((String) authenticationToken.getPrincipal());

        if (userDetails == null) {

            throw new PhoneNotFoundException("手机号码不存在");

        } else if (!userDetails.isEnabled()) {

            throw new DisabledException("用户已被禁用");

        } else if (!userDetails.isAccountNonExpired()) {

            throw new AccountExpiredException("账号已过期");

        } else if (!userDetails.isAccountNonLocked()) {

            throw new LockedException("账号已被锁定");

        } else if (!userDetails.isCredentialsNonExpired()) {

            throw new LockedException("凭证已过期");
        }

        PhoneAuthenticationToken result = new PhoneAuthenticationToken(userDetails,
                userDetails.getAuthorities());

        result.setDetails(authenticationToken.getDetails());

        return result;
    }

    public boolean supports(Class&lt;?&gt; authentication) {
        return PhoneAuthenticationToken.class.isAssignableFrom(authentication);
    }

    public UserDetailsService getUserDetailsService() {
        return userDetailsService;
    }

    public void setUserDetailsService(UserDetailsService userDetailsService) {
        this.userDetailsService = userDetailsService;
    }

    }
</code></pre>
<p>代码解读：</p>
<p>（1）获取配置文件中配置的 UserDetailsService 对象。</p>
<p>（2）将 authenticationToken 对象强转为 PhoneAuthenticationToken 对象。</p>
<p>（3）调用 userDetailsService 对象的 loadUserByUsername 方法获取用户信息 UserDetails。</p>
<p>（4）如果报异常则认证失败。</p>
<p>（5）如果没有异常，则调用 PhoneAuthenticationToken 两个参数的构造方法，设置权限等，到这里则认证成功，
然后设置请求信息，并将认证结果返回。</p>
<p>（6）下面的 supports 方法中说明该 AuthenticationProvider 支持 PhoneAuthenticationToken 类型的 Token。</p>
<h3 id="springsecurityxml">spring-security.xml 配置文件修改</h3>
<p>在 spring-security.xml 配置文件中加入自定义的认证策略、认证逻辑过滤器等。部分配置如下，且未按顺序，具体配置请参考百度网盘中的配置文件：</p>
<pre><code>     &lt;security:custom-filter after="FORM_LOGIN_FILTER" ref="phoneAuthenticationFilter"/&gt;
     &lt;bean id="phoneAuthenticationFilter" class="wang.dreamland.www.security.phone.PhoneAuthenticationFilter"&gt;
        &lt;property name="filterProcessesUrl" value="/phoneLogin"&gt;&lt;/property&gt;
        &lt;property name="authenticationManager" ref="authenticationManager"&gt;&lt;/property&gt;
        &lt;property name="sessionAuthenticationStrategy" ref="sessionStrategy"&gt;&lt;/property&gt;
        &lt;property name="authenticationSuccessHandler"&gt;
            &lt;bean class="org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler"&gt;
                &lt;property name="defaultTargetUrl" value="/list"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
        &lt;property name="authenticationFailureHandler"&gt;
            &lt;bean class="org.springframework.security.web.authentication.SimpleUrlAuthenticationFailureHandler"&gt;
                &lt;property name="defaultFailureUrl" value="/login?error=fail"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
    &lt;/bean&gt;

     &lt;!-- 认证管理器，使用自定义的accountService，并对密码采用md5加密 --&gt;
    &lt;security:authentication-manager alias="authenticationManager"&gt;
        &lt;security:authentication-provider user-service-ref="accountService"&gt;
            &lt;security:password-encoder hash="md5"&gt;
                &lt;security:salt-source user-property="username"&gt;&lt;/security:salt-source&gt;
            &lt;/security:password-encoder&gt;
        &lt;security:authentication-provider ref="phoneAuthenticationProvider"&gt;
        &lt;/security:authentication-provider&gt;
    &lt;/security:authentication-manager&gt;
    &lt;bean id="phoneService" class="wang.dreamland.www.security.phone.PhoneUserDetailsService"/&gt;
     &lt;bean id="phoneAuthenticationProvider" class="wang.dreamland.www.security.phone.PhoneAuthenticationProvider"&gt;
        &lt;property name="userDetailsService" ref="phoneService"&gt;&lt;/property&gt;
    &lt;/bean&gt;
</code></pre>
<p>关于配置的说明之前已经介绍过。这里就不再赘述。</p>
<h3 id="tomcat">重新启动 Tomcat 测试</h3>
<p><strong>注意将登陆页面的手机登录 URL 改为 phoneLogin。</strong></p>
<pre><code>     &lt;!--手机登录--&gt;
     &lt;div class="tab-pane fade" id="phone-login"&gt;
       &lt;form role="form" class="login-form form-horizontal" id="phone_form" action="${ctx}/phoneLogin" method="post"&gt;
        ...
</code></pre>
<p>输入手机号和验证码后点击登录，手机登录认证测试成功！</p>
<p>如果输入错误的手机验证码，登录失败后跳转到了登录页面，但它跳转到的是账号登录选项卡。如果想让它跳转到手机登录选项卡，可自定义登录失败处理器。</p>
<p><strong>1.</strong> 在 security.phone 包下新建 PhoneAuthenticationFailureHandler 并继承 SimpleUrlAuthenticationFailureHandler：</p>
<pre><code>    public class PhoneAuthenticationFailureHandler extends SimpleUrlAuthenticationFailureHandler {

    private String defaultFailureUrl;

    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {
        String phone = request.getParameter("telephone");
        request.setAttribute("phoneError", "phone");
        request.setAttribute("phoneNum", phone);
        request.getRequestDispatcher(defaultFailureUrl).forward(request, response);
    }

    @Override
    public void setDefaultFailureUrl(String defaultFailureUrl) {
        this.defaultFailureUrl = defaultFailureUrl;
    }

    public String getDefaultFailureUrl() {
        return defaultFailureUrl;
    }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）获取配置中配置的手机登录认证失败跳转 URL 赋值给 defaultFailureUrl。</p>
<p>（2）根据请求参数获取手机号。</p>
<p>（3）将 <code>key="phoneError"，value="phone"</code> 设置到 Request 域中，由前台获取。</p>
<p>（4）将 <code>key="phoneNum"，value=phone</code> 设置到 Request 域中，由前台获取。</p>
<p>（5）转发请求到 defaultFailureUrl。</p>
<p><strong>2.</strong> 在 <code>spring-security.xml</code> 中配置自定义的认证失败处理器：</p>
<pre><code>        &lt;bean id="phoneAuthenticationFilter" class="wang.dreamland.www.security.phone.PhoneAuthenticationFilter"&gt;
        &lt;property name="filterProcessesUrl" value="/phoneLogin"&gt;&lt;/property&gt;
        &lt;property name="authenticationManager" ref="authenticationManager"&gt;&lt;/property&gt;
        &lt;property name="sessionAuthenticationStrategy" ref="sessionStrategy"&gt;&lt;/property&gt;
        &lt;property name="authenticationSuccessHandler"&gt;
            &lt;bean class="org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler"&gt;
                &lt;property name="defaultTargetUrl" value="/list"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
        &lt;!--自定义登录失败处理器--&gt;
        &lt;property name="authenticationFailureHandler"&gt;
            &lt;bean class="wang.dreamland.www.security.phone.PhoneAuthenticationFailureHandler"&gt;
                &lt;property name="defaultFailureUrl" value="/login?error=fail"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
    &lt;/bean&gt;
</code></pre>
<p><strong>3.</strong> 在 login.jsp 中创建页面加载完成函数：</p>
<pre><code>    //页面加载完成函数
    $(function () {
        var msg = "${phoneError}";
        var phone = "${phoneNum}";
        if(msg == "phone"){
            $("#phone-login").attr("class","tab-pane fade in active")
            $("#p_login").attr("class","active");
            $("#account-login").attr("class","tab-pane fade");
            $("#a_login").attr("class","");
            $("#phone_span").text("短信验证码错误").css("color","red");
            $("#phone").val(phone);
        }
    });
</code></pre>
<p>代码解读：</p>
<p>（1）页面加载完成执行此函数，用 EL 表达式获取后台传来的 msg 和手机号。</p>
<p>（2）判断 msg 是不是字符串“phone”，如果是则显示手机登录选项 Tab，并且提示短信验证码错误，将用户的手机号回显到页面。</p>
<p>效果如图：</p>
<p><img src="https://images.gitbook.cn/af016000-8c2d-11e8-b9de-5bb0fbe09c97" alt="" /></p>
<h3 id="404500">404、500错误页面配置</h3>
<p>如果访问不存在的资源时会出现404错误，如果系统后台服务器出错会报500错误等待，如图404错误：</p>
<p><img src="https://images.gitbook.cn/c4501640-8c2d-11e8-bcba-83e934a0ba0f" alt="" /></p>
<p>出现上面的页面对用户来说很不友好，我们配置自己的错误页面。</p>
<p><strong>1.</strong> 在 web.xml 中引入404、500错误页面：</p>
<pre><code>      &lt;!-- 404页面 --&gt;
    &lt;error-page&gt;
        &lt;error-code&gt;404&lt;/error-code&gt;
        &lt;location&gt;/WEB-INF/404.jsp&lt;/location&gt;
    &lt;/error-page&gt;
    &lt;!-- 500页面 --&gt;
    &lt;error-page&gt;
        &lt;error-code&gt;500&lt;/error-code&gt;
        &lt;location&gt;/WEB-INF/500.jsp&lt;/location&gt;
    &lt;/error-page&gt;
</code></pre>
<p><strong>2.</strong> 在 <code>webapp/WEB-INF/</code> 下引入 404.jsp 和 500.jsp 文件。</p>
<p><strong>3.</strong> 将500错误页面用到的背景图片 bj.png 和图标 500.png 添加到 <code>webapp/images</code> 目录下，JSP 文件还有图片在百度网盘中下载。</p>
<p>404错误页面效果如下图：</p>
<p><img src="https://images.gitbook.cn/4b25e8c0-8c2e-11e8-b9de-5bb0fbe09c97" alt="" /></p>
<p>500错误页面效果如下图：</p>
<p><img src="https://images.gitbook.cn/5b3b7e50-8c2e-11e8-a5a7-69760200eb00" alt="" /></p>
<blockquote>
  <p>第16课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1wJ93NTVkD_eKLB-rx1xjrg </p>
  <p>密码：oihe</p>
</blockquote></div></article>