---
title: SSM 博客系统开发实战-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Spring Security 登陆认证的核心思想都是一样的：首先经过我们配置的认证逻辑处理过滤器，封装成某种类型的 Token，交给 AuthenticationManager 认证管理器，由认证管理器找到支持该 Token 的 AuthenticationProvider，由该 AuthenticationProvider 进行具体的认证处理。认证过程中会调用 UserDetailsService 接口获取用户信息进行认证。我们将围绕这几个点展开分享。</p>
<h3 id="openuseruserdetails">OpenUser 实现 UserDetails 接口</h3>
<p>这次和之前的用户登录认证不一样，进行认证的不再是 User 对象，而是第三方用户 OpenUser 对象，所以我们将 OpenUser 对象实现 UserDetails 接口，这样做是因为 UserDetailsService 接口的 loadUserByUsername 方法返回的是 UserDetails 类型的对象。如下：</p>
<pre><code>    public interface UserDetailsService {
        UserDetails loadUserByUsername(String var1) throws UsernameNotFoundException;
    }
</code></pre>
<p><strong>1.</strong> OpenUser 实体类修改如下：</p>
<pre><code>    public class OpenUser implements UserDetails{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long uId;

    private String openId;

    private String accessToken;

    private String nickName;

    private String avatar;

    private String openType;

    private Long expiredTime;

    private Date lastLoginTime;

    @Transient
    private User user;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getuId() {
        return uId;
    }

    public void setuId(Long uId) {
        this.uId = uId;
    }

    public String getOpenId() {
        return openId;
    }

    public void setOpenId(String openId) {
        this.openId = openId;
    }

    public String getAccessToken() {
        return accessToken;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    public String getNickName() {
        return nickName;
    }

    public void setNickName(String nickName) {
        this.nickName = nickName;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public String getOpenType() {
        return openType;
    }

    public void setOpenType(String openType) {
        this.openType = openType;
    }

    public Long getExpiredTime() {
        return expiredTime;
    }

    public void setExpiredTime(Long expiredTime) {
        this.expiredTime = expiredTime;
    }

    public Date getLastLoginTime() {
        return lastLoginTime;
    }

    public void setLastLoginTime(Date lastLoginTime) {
        this.lastLoginTime = lastLoginTime;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public Collection&lt;? extends GrantedAuthority&gt; getAuthorities() {
        List&lt;SimpleGrantedAuthority&gt; authorities = new ArrayList&lt;SimpleGrantedAuthority&gt;();
        if(user==null){
            return authorities;
        }
        List&lt;Role&gt; roles = user.getRoles();
        if(roles == null || roles.size()&lt;=0){
            return null;
        }
        for(Role r:roles){
            authorities.add(new SimpleGrantedAuthority(r.getRoleValue()));
        }
        return authorities;
    }

    @Override
    public String getPassword() {
        return getAccessToken();
    }

    @Override
    public String getUsername() {
        return getOpenId();
    }

    @Override
    public boolean isAccountNonExpired() {
        return ValidateUtils.isAccountNonExpired(new Date(),getLastLoginTime(),getExpiredTime());
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return isAccountNonExpired();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof OpenUser) {
            return getOpenId().equals(((OpenUser)obj).getOpenId())||getUsername().equals(((OpenUser)obj).getUsername());
        }
        return false;
    }
    @Override
    public int hashCode() {
        return getUsername().hashCode();
    }

    @Override
    public String toString() {
        return "OpenUser{" +
                "id=" + id +
                ", uId=" + uId +
                ", openId='" + openId + '\'' +
                ", accessToken='" + accessToken + '\'' +
                ", nickName='" + nickName + '\'' +
                ", avatar='" + avatar + '\'' +
                ", openType='" + openType + '\'' +
                ", expiredTime=" + expiredTime +
                ", lastLoginTime=" + lastLoginTime +
                ", user=" + user +
                '}';
    }
</code></pre>
<p>代码解读：</p>
<p>（1）我在 OpenUser 实体类中添加了一个 lastLoginTime 属性，用来记录第三方用户最后一次登录的时间，可以根据当前时间、最后一次登录时间和过期时间来判断该用户是否过期。</p>
<pre><code>private Date lastLoginTime;
</code></pre>
<p>（2）一个或多个第三方应用对应一个 User，所以这里添加了一个 User 属性，User 属性上加了 <code>@Transient</code> 注解，代表表中没有此字段。添加 User 属性的目的有两点，一个是为了获取该第三方用户的角色信息，我们从 User 里获取；另一个目的就是第三方用户经过认证授权之后，我们要从 OpenUser 中取出 User 对象，返回给页面，因为页面需要取 User 对象里的值。</p>
<p>（3）可以看到 getAuthorities() 获取权限的方法，我们是从 User 中获取的，如果没有就返回 null。</p>
<p>（4）getUsername() 方法返回第三方用户的唯一标识 openId，getPassword() 方法返回第三方用户的 accessToken 授权令牌。</p>
<p>（5）isAccountNonExpired() 方法判断账号是否过期，调用的是我封装的一个方法，在 common 包下新建 ValidateUtils.java，方法如下：</p>
<pre><code>    public class ValidateUtils {
    public static boolean isAccountNonExpired(Date now,Date lastTime,Long expiredTime){
        long nowTime = now.getTime()/1000;
        long lastLoginTime = lastTime.getTime()/1000;
        if(nowTime-lastLoginTime&lt;=expiredTime){
            return true;
        }
        return false;
    }
    }
</code></pre>
<p>第一个参数是当前时间，第二个参数是最后一次登录时间，第三个参数是过期时间（单位是秒）。</p>
<p>（6）账号未锁定、密码未过期默认返回 true，账号可用 isEnabled() 方法，我们根据账号是否过期来判断，直接返回 isAccountNonExpired() 的结果。</p>
<p>（7）最后重写 equals、hashcode 和 toString 方法。</p>
<p><strong>2.</strong> 在 <code>open_user</code> 表中添加字段 <code>last_login_time</code>：</p>
<pre><code>alter table resource add COLUMN last_login_time datetime
</code></pre>
<h3 id="openusernotfoundexception">自定义 OpenUserNotFoundException 异常</h3>
<p>如果第三方登录认证过程中抛出异常，我们抛出自定义的 OpenUserNotFoundException 异常，在 wang.dreamland.www.security.open 包下新建 OpenUserNotFoundException 并继承 AuthenticationException：</p>
<pre><code>    public class OpenUserNotFoundException extends AuthenticationException {
    public OpenUserNotFoundException(String msg, Throwable t) {
        super( msg, t );
    }

    public OpenUserNotFoundException(String msg) {
        super( msg );
    }
    }
</code></pre>
<p>和上一节一样，不在赘述</p>
<h3 id="openauthenticationtoken">自定义 OpenAuthenticationToken</h3>
<p>自定义第三方登录认证的令牌，在 wang.dreamland.www.security.open 包下新建 OpenAuthenticationToken 并继承 AbstractAuthenticationToken：</p>
<pre><code>    public class OpenAuthenticationToken extends AbstractAuthenticationToken {
    private final Object principal;

    public OpenAuthenticationToken(Object principal) {
        super((Collection)null);
        this.principal = principal;
        this.setAuthenticated(false);
    }

    public OpenAuthenticationToken(Object principal, Collection&lt;? extends GrantedAuthority&gt; authorities) {
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
<p>（1）一个参数的构造方法是将用户唯一标识 openId 赋值给 principal，然后权限设置为 null，认证状态为 false。</p>
<p>（2）两个参数的构造方法是传入权限集合、用户信息并将认证状态置为 true。</p>
<p>（3）因为我们没有用到密码。所以 getCredentials 我们返回 null。</p>
<p>（4）setAuthenticated 方法其实是调用 super.setAuthenticated(false)，父类的方法。</p>
<h3 id="openauthenticationfilter">自定义认证逻辑过滤器 OpenAuthenticationFilter</h3>
<p>在 wang.dreamland.www.security.open 包下新建 OpenAuthenticationFilter 并继承 AbstractAuthenticationProcessingFilter：</p>
<pre><code>    public class OpenAuthenticationFilter extends AbstractAuthenticationProcessingFilter {

    private Logger log = LoggerFactory.getLogger( OpenAuthenticationFilter.class );
    @Autowired
    private OpenUserService openUserService;
    @Autowired
    private RoleUserService roleUserService;
    @Autowired
    private UserService userService;

    protected OpenAuthenticationFilter( ) {
        super( new AntPathRequestMatcher(Constants.QQ_LOGIN_URL) );
    }

    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException, IOException, ServletException {
        OpenUser openUser = getOpenUser( request, response );
        if(openUser.getOpenId()==null){
            throw new OpenUserNotFoundException("第三方用户OpenId为空");
        }
        OpenUser openUserDB = openUserService.findByOpenId( openUser.getOpenId());
        openUser.setLastLoginTime(new Date());
        if(openUserDB==null){
            User user = new User();
            user.setNickName( openUser.getNickName() );
            user.setEmail( openUser.getOpenId() );
            user.setImgUrl( openUser.getAvatar() );
            userService.regist( user );
            addRoleUser( user.getId() );
            openUser.setuId( user.getId() );
            openUserService.add( openUser );
        }else {
            //是否过期
            boolean accountNonExpired = ValidateUtils.isAccountNonExpired( new Date(), openUserDB.getLastLoginTime(), openUserDB.getExpiredTime() );
            if(!accountNonExpired){
                //过期
                openUser.setId( openUserDB.getId() );
                openUser.setuId(openUser.getuId());
                openUserService.update( openUser );
            }
        }
        OpenAuthenticationToken authRequest = new OpenAuthenticationToken(openUser.getOpenId());
        this.setDetails(request, authRequest);
        return this.getAuthenticationManager().authenticate(authRequest);
    }

    protected void setDetails(HttpServletRequest request, OpenAuthenticationToken authRequest) {
        authRequest.setDetails(this.authenticationDetailsSource.buildDetails(request));
    }

    public void addRoleUser(Long uid){
        RoleUser roleUser = new RoleUser();
        roleUser.setuId( uid );
        roleUser.setrId( Constants.ROLE_USER );
        roleUserService.add( roleUser );
    }

    public OpenUser getOpenUser(HttpServletRequest request,HttpServletResponse response){
        OpenUser openUser = new OpenUser();
        response.setContentType("text/html; charset=utf-8");
        try {
            AccessToken accessTokenObj = (new Oauth()).getAccessTokenByRequest(request);
            String accessToken   = null;
            String openID   = null;
            long tokenExpireIn = 0L;

            if (accessTokenObj.getAccessToken().equals("")) {
                //用户取消了授权
                log.info("没有获取到响应参数");
            } else {
                accessToken = accessTokenObj.getAccessToken();
                tokenExpireIn = accessTokenObj.getExpireIn();//失效时间
                // 利用获取到的accessToken 去获取当前用的openid
                OpenID openIDObj =  new OpenID(accessToken);
                openID = openIDObj.getUserOpenID();
                UserInfo qzoneUserInfo = new UserInfo(accessToken, openID);//根据用户openId和accessToken获取用户的qq信息
                UserInfoBean userInfoBean = qzoneUserInfo.getUserInfo();
                if (userInfoBean.getRet() == 0) {
                    openUser.setOpenType( Constants.OPEN_TYPE_QQ );
                    openUser.setNickName( userInfoBean.getNickname() );
                    openUser.setAvatar( userInfoBean.getAvatar().getAvatarURL50() );
                    openUser.setOpenId( openID );
                    openUser.setAccessToken( accessToken );
                    openUser.setExpiredTime( tokenExpireIn );
                } else {
                    log.info("未能正确获取QQ用户信息，原因是： " + userInfoBean.getMsg());
                }

            }
        } catch (Exception e) {
            throw new RuntimeException( "获取QQ用户信息失败",e );
        }

        return openUser;
    }

    }
</code></pre>
<p>代码解读：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入相关 Bean 对象。</p>
<p>（2）在构造方法中指定第三方 QQ 登录时的登录 URL，这里我把它定义在了 common 包下的 Constants 类中，方便以后修改：</p>
<pre><code>    public static final String QQ_LOGIN_URL = "/qq_login";
</code></pre>
<p>（3）在 attemptAuthentication 方法中，我把获取 OpenUser 的方法封装到了 getOpenUser 方法中，getOpenUser 中的方法就是之前我们做 QQ 第三方登录时写的方法，这里就不再赘述了。</p>
<p>（4）如果 openId 为空直接抛出我们自定义的 OpenUserNotFoundException 异常。</p>
<p>（5）如果 openId 不为空，我们根据用户的唯一标识 openId 去查询数据库，将查询结果赋值给 openUserDB，设置登录时间。如果 openUserDB 为 null 则代表该 QQ 用户是第一次登录我们的网站，此时我们创建一个临时用户，设置 QQ 昵称、QQ 头像、openId 为临时 Email 等，这里密码不设置，然后调用 regist 方法将数据插入 user 表中。</p>
<p>（6）addRoleUser 也是自己封装的一个方法，是给第三方登录用户默认的角色 <code>ROLE_USER</code>，关于角色对应的 id 也放在了 Constants类中，方便修改：</p>
<pre><code>public static final Long ROLE_USER = 1L;
public static final Long ROLE_ADMIN = 2L;
</code></pre>
<p>因为 id 是 Long 类型的，所以加上 L 后缀。注意你的 role 角色表中得有这个 id，如图：</p>
<p><img src="http://images.gitbook.cn/8a6bd770-805c-11e8-8db6-0d16f8c01663" alt="enter image description here" /></p>
<p>（7）将获取的第三方用户 OpenUser 对应的 UID 设置进去，然后添加到数据库中。</p>
<p>（8）如果 openUserDB 不为 null 则代表该 QQ 用户之前已经登录过，判断该用户是否登录过期（QQ 默认过期时间3个月=7776000秒），如果过期，则将查询出来的 openUserDB 对象的 ID 和 UID 赋值给刚登录的 OpenUser，然后根据主键 ID 更新数据。如果未过期则直接进行下一步认证。</p>
<p>（9）后面的代码和之前一样，将用户唯一标识 openId 封装到 OpenAuthenticationToken 对象中，通过 AuthenticationManager 认证管理器找到支持该 Token 的 AuthenticationProvider 进行具体的认证。</p>
<h3 id="openuserdetailsservice">自定义获取用户信息逻辑的 OpenUserDetailsService</h3>
<p>在 wang.dreamland.www.security.open 包下新建 OpenUserDetailsService 并实现 UserDetailsService 接口：</p>
<pre><code>    public class OpenUserDetailsService implements UserDetailsService {

    @Autowired
    private OpenUserService openUserService;
    @Autowired
    private UserService userService;
    @Autowired
    private RoleService roleService;

    public UserDetails loadUserByUsername(String openId) throws OpenUserNotFoundException {
        OpenUser openUser = openUserService.findByOpenId( openId);
        if(openUser == null){
            throw new OpenUserNotFoundException("第三方用户openId不存在");
        }
        User user = userService.findById( openUser.getuId() );//修改直接根据用户id查询
        List&lt;Role&gt; roles = roleService.findByUid( user.getId() );
        user.setRoles( roles );
        openUser.setUser( user );
        return openUser;
    }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入相关 Bean 对象。</p>
<p>（2）重写 loadUserByUsername 方法，根据用户唯一标识 openId 查询 OpenUser 对象，如果为空直接抛出 OpenUserNotFoundException 异常。</p>
<p>（3）OpenUser 不为空则根据 OpenUser 中的 UID 查询 User 表获取用户对象 User，通过用户 ID 查询出该用户所对应的角色集合，将角色集合设置到 User 中，然后将 User 设置到 OpenUser 对象中，最后返回 OpenUser 对象，此时 OpenUser 就拥有了 User 对象以及对应的角色信息。</p>
<h3 id="openauthenticationprovider">自定义第三方登录认证策略 OpenAuthenticationProvider</h3>
<p>在 wang.dreamland.www.security.open 包下新建 OpenAuthenticationProvider 并实现 AuthenticationProvider 接口：</p>
<pre><code>    public class OpenAuthenticationProvider implements AuthenticationProvider {

    private UserDetailsService userDetailsService;

    public Authentication authenticate(Authentication authentication) throws AuthenticationException {

        OpenAuthenticationToken authenticationToken = (OpenAuthenticationToken) authentication;
        UserDetails userDetails = userDetailsService.loadUserByUsername((String) authenticationToken.getPrincipal());

        if (userDetails == null) {

            throw new OpenUserNotFoundException("第三方OpenId不存在");

        } else if (!userDetails.isEnabled()) {

            throw new DisabledException("第三方用户已被禁用");

        } else if (!userDetails.isAccountNonExpired()) {

            throw new AccountExpiredException("第三方账号已过期");

        } else if (!userDetails.isAccountNonLocked()) {

            throw new LockedException("第三方账号已被锁定");

        } else if (!userDetails.isCredentialsNonExpired()) {

            throw new LockedException("第三方凭证已过期");
        }

        OpenAuthenticationToken result = new OpenAuthenticationToken(userDetails,
                userDetails.getAuthorities());

        result.setDetails(authenticationToken.getDetails());

        return result;
    }

    public boolean supports(Class&lt;?&gt; authentication) {
        return OpenAuthenticationToken.class.isAssignableFrom(authentication);
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
<p>（1）获取配置文件中配置的 UserDetailsService 对象（主要是通过 setter 方法）。</p>
<p>（2）将 authenticationToken 对象强转为 OpenAuthenticationToken 对象。</p>
<p>（3）调用 userDetailsService 对象的 loadUserByUsername 方法获取用户信息 UserDetails 即 OpenUser 对象。</p>
<p>（4）如果报异常则认证失败。</p>
<p>（5）如果没有异常，则调用 OpenAuthenticationToken 两个参数的构造方法，设置权限等，到这里则认证成功，
然后设置请求信息，并将认证结果返回。</p>
<p>（6）下面的 supports 方法中说明该 AuthenticationProvider 支持 OpenAuthenticationToken 类型的 Token。</p>
<h3 id="springsecurityxml">spring-security.xml 配置文件修改</h3>
<p>在 spring-security.xml 配置文件中加入自定义的认证策略、认证逻辑过滤器等。</p>
<p>相关过滤器及实现写完以后，我们要将其配置到配置文件中去，启动项目时实例化相关对象。</p>
<p>主要配置如下，具体的配置内容请参加百度网盘中的配置文件。</p>
<p><strong>1.</strong> 将点击 QQ 图标的访问路径放行：</p>
<pre><code>&lt;security:http security="none" pattern="/to_login" /&gt;
</code></pre>
<p><strong>2.</strong> 配置认证逻辑过滤器 OpenAuthenticationFilter：</p>
<pre><code>      &lt;security:custom-filter after="CAS_FILTER" ref="openAuthenticationFilter" /&gt;
</code></pre>
<p>这里 <code>after="CAS_FILTER"</code> 是把我们写的过滤器配置在 <code>CAS_FILTER</code> 过滤器后面，可点击进入查看 <code>CAS_FILTER</code> 过滤器：</p>
<p><img src="https://images.gitbook.cn/46e58960-818d-11e8-98de-7b1752b6623c" alt="enter image description here" /></p>
<p>我们把关于登录认证的过滤器都放在一起。</p>
<p>该过滤器的 ref 属性对应的 Bean 如下：</p>
<pre><code>      &lt;bean id="openAuthenticationFilter" class="wang.dreamland.www.security.open.OpenAuthenticationFilter"&gt;
        &lt;property name="filterProcessesUrl" value="/qq_login"&gt;&lt;/property&gt;
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
</code></pre>
<p>和之前介绍的一样，包含默认的登录 URL、登录成功跳转 URL 和登录失败跳转 URL 等。</p>
<p><strong>3.</strong> 在认证管理器 <code>authentication-manager</code> 中加入第三方认证策略：</p>
<pre><code>     &lt;security:authentication-provider ref="openAuthenticationProvider"&gt;
     &lt;/security:authentication-provider&gt;
</code></pre>
<p>ref 对应的 Bean 如下：</p>
<pre><code>     &lt;bean id="openAuthenticationProvider" class="wang.dreamland.www.security.open.OpenAuthenticationProvider"&gt;
        &lt;property name="userDetailsService" ref="openUserDetailsService"&gt;&lt;/property&gt;
     &lt;/bean&gt;
</code></pre>
<p>在第三方认证策略中注入自己的获取用户逻辑的方式。userDetailsService 对应的 Bean 如下：    </p>
<pre><code>    &lt;bean id="openUserDetailsService" class="wang.dreamland.www.security.open.OpenUserDetailsService"/&gt;
</code></pre>
<p>配置文件配置完成以后，启动 Tomcat 进行 QQ 登录测试。</p>
<h3 id="">优化注册、绑定业务逻辑</h3>
<h4 id="-1">注册</h4>
<p>之前我们注册的时候没有考虑到给用户分配角色，登录以后访问不了需要 <code>ROLE_USER</code> 角色的 URL，所以这里我们修改如下。</p>
<p>在 RegisterController 中找到 doRegister 方法，在 userService.regist(user) 方法之后（因为我们需要用户 ID），加入以下代码：</p>
<pre><code>     RoleUser roleUser = new RoleUser();
     roleUser.setuId(user.getId());
     roleUser.setrId(Constants.ROLE_USER);
     roleUserService.add(roleUser);
</code></pre>
<p>在中间表中插入一条数据，表示该用户对应 <code>ROLE_USER</code> 角色。</p>
<p>重新启动 Tomcat，注册一个账号，激活后登陆，发现后台报 BadCredentialsException 异常：</p>
<pre><code>    org.springframework.security.authentication.BadCredentialsException: Bad credentials
</code></pre>
<p>而登陆页面却没有提示。</p>
<p><strong>1.</strong> 没有错误提示，不够友好，我们自定义自己的登录失败处理器。</p>
<p>在 wang.dreamland.www.security.account 包下新建 AccountAuthenticationFailureHandler 并继承 SimpleUrlAuthenticationFailureHandler：</p>
<pre><code>    public class AccountAuthenticationFailureHandler extends SimpleUrlAuthenticationFailureHandler {

    private String defaultFailureUrl;

    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {
        if("User is disabled".equals(exception.getMessage())){
            request.setAttribute("error","active");
        }else {
            request.setAttribute("error", "fail");
        }
        String email = request.getParameter("username");
        request.setAttribute("email", email);
        request.getRequestDispatcher(defaultFailureUrl).forward(request, response);
    }

    @Override
    public void setDefaultFailureUrl(String defaultFailureUrl) {
        this.defaultFailureUrl = defaultFailureUrl;
    }

    public String getDefaultFailureUrl() {
        return defaultFailureUrl;
    }
</code></pre>
<p>代码解读：</p>
<p>（1）通过 setter 方法注入 defaultFailureUrl 登录失败跳转 URL。</p>
<p>（2）如果报 <code>User is disabled</code>，则说明该用户还未激活，将 active 设置到 Request 域中。</p>
<p>（3）其他异常将 fail 保存到 Request 域中。</p>
<p>（4）根据请求参数获取用户登录的 Email，将 Email 保存到 Request 域中，前台根据相应的 EL 表达式获取相应的值。</p>
<p>（5）将请求转发到设置的默认登录失败 URL。</p>
<p>然后在配置文件中配置自定义的登录失败处理器：</p>
<pre><code>       &lt;bean id="authenticationFilter" class="wang.dreamland.www.security.account.AccountAuthenticationFilter"&gt;
        &lt;property name="filterProcessesUrl" value="/doLogin"&gt;&lt;/property&gt;
        &lt;property name="authenticationManager" ref="authenticationManager"&gt;&lt;/property&gt;
        &lt;property name="sessionAuthenticationStrategy" ref="sessionStrategy"&gt;&lt;/property&gt;
        &lt;property name="authenticationSuccessHandler"&gt;
            &lt;bean class="org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler"&gt;
                &lt;property name="defaultTargetUrl" value="/list"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
        &lt;property name="authenticationFailureHandler"&gt;
            &lt;bean class="wang.dreamland.www.security.account.AccountAuthenticationFailureHandler"&gt;
                &lt;property name="defaultFailureUrl" value="/login?error=fail"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
    &lt;/bean&gt;
</code></pre>
<p>重新启动项目进行登录，发现已有相应错误提示，并回显了登录用户的邮箱账号。</p>
<p>密码错误时，有如下图所示的提示信息：</p>
<p><img src="https://images.gitbook.cn/ab171970-8198-11e8-878d-d106b6fbe32a" alt="enter image description here" /></p>
<p><strong>2.</strong> 报 BadCredentialsException 异常是因为注册时我们使用的是自己的 MD5 加密工具，我们把它替换成 Sping Security 提供的加密工具。</p>
<p>在 doRegister 方法中将：</p>
<pre><code>     user.setPassword(MD5Util.encodeToHex("salt"+password));
</code></pre>
<p>替换为：</p>
<pre><code>     user.setPassword(new Md5PasswordEncoder().encodePassword(password,email));
</code></pre>
<p>重新启动项目，然后重新注册一个账号，登录。</p>
<p>账号未激活时给出相应错误提示：</p>
<p><img src="https://images.gitbook.cn/0075bf60-819f-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>激活后登录成功！</p>
<p><strong>注意：</strong> 还有一处要修改加密方式的地方是在 PersonalController 的 profile 方法中：</p>
<pre><code>    if(StringUtils.isBlank(user.getPassword()) &amp;&amp; StringUtils.isBlank(password)){
            return "redirect:/list";
        }
     if(StringUtils.isNotBlank(email)){
     user.setEmail(email);
     user.setPassword(new Md5PasswordEncoder().encodePassword(password,email));
     ...
    }
</code></pre>
<p>判断用户是否登录的代码可以删除了，框架已经帮我们做了，添加判断用户密码是否为空的代码，如果当前用户密码和前台传过来的密码都为空，我们将其重定向到 <code>/list</code> 路径，防止用户直接通过地址栏访问 <code>http://localhost:8080/profile</code>。</p>
<h4 id="-2">绑定</h4>
<p><img src="https://images.gitbook.cn/95ff41f0-81a9-11e8-878d-d106b6fbe32a" alt="enter image description here" /></p>
<p>用户点击“立即绑定”时也会走 QQ 登录认证流程，唯一的区别是此时我们知道已经认证的用户信息。可以根据当前用户是否为空来判断是进行登录认证还是进行绑定。我们将 OpenAuthenticationFilter 的 attemptAuthentication 方法修改如下：</p>
<pre><code>        @Autowired
        private BaseController baseController;
        public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException, IOException, ServletException {

        OpenUser openUser = getOpenUser( request, response );
        if(openUser.getOpenId()==null){
            throw new OpenUserNotFoundException("第三方用户OpenId为空");
        }
        OpenUser openUserDB = openUserService.findByOpenId( openUser.getOpenId());
        openUser.setLastLoginTime(new Date());
        if(openUserDB==null){
            User user = null;
            if(baseController.getCurrentUser()!=null){
                user = baseController.getCurrentUser();
            }else {
                user =new User();
                user.setNickName( openUser.getNickName() );
                user.setEmail( openUser.getOpenId() );
                user.setImgUrl( openUser.getAvatar() );
                userService.regist( user );
                addRoleUser( user.getId() );
            }
            openUser.setuId( user.getId() );
            openUserService.add( openUser );
        }else {
            //是否过期
            boolean accountNonExpired = ValidateUtils.isAccountNonExpired( new Date(), openUserDB.getLastLoginTime(), openUserDB.getExpiredTime() );
            if(!accountNonExpired){
                //过期
                openUser.setId( openUserDB.getId() );
                openUser.setuId(openUser.getuId());
                openUserService.update( openUser );
                openUserDB = openUser;
            }
            if(baseController.getCurrentUser()!=null){
                //绑定 判断是否有创建临时用户
                User user = userService.findById(openUserDB.getuId());
                if(user!=null &amp;&amp; user.getPassword()==null){
                    //删除临时用户
                    roleUserService.deleteByUid(user.getId());
                    userService.deleteByEmail(user.getEmail());
                }
                //绑定
                openUserDB.setuId(baseController.getCurrentUser().getId());
                openUserService.update(openUserDB);
            }
        }
        OpenAuthenticationToken authRequest = new OpenAuthenticationToken(openUser.getOpenId());
        this.setDetails(request, authRequest);
        return this.getAuthenticationManager().authenticate(authRequest);
    }
</code></pre>
<p>代码解读：</p>
<p>（1）增加一个 <code>@Autowired</code> 注解，注入 BaseController 对象，用来获取当前用户。</p>
<p>（2）通过封装的 getOpenUser 方法获取第三方登录用户 OpenUser。</p>
<p>（3）如果 openId 不为 null，则根据 openId 查询数据库中是否已经存在该第三方对象，设置登录时间。</p>
<p>（4）如果数据库中不存在该第三方对象。判断当前用户是否为空，如果不为空说明是做绑定操作，将当前用户赋值给 User；如果当前用户为空，说明是做登录操作，创建一个临时用户，设置相关属性，插入数据库，添加角色信息等，然后将第三方对象保存到数据库中。</p>
<p>（5）如果数据库中已经存在该第三方对象，首先判断该第三方对象是否已经过期，如果已经过期则更新第三方对象相关信息。然后将更新后的第三方对象赋值给 openUserDB。然后判断当前用户是否为空，如果不为空，说明是做绑定操作，如果该第三方对象之前登录过，说明创建过临时用户，我们将临时用户删除。然后将当前用户的 ID 赋值给第三方对象 openUserDB，更新该第三方对象，绑定操作完成。</p>
<p>（6）后面的认证操作和之前一样，不再赘述。</p>
<h3 id="-3">登录成功监听器，记录登录成功日志</h3>
<p><strong>1.</strong> 在 controller 包下新建 LoginSuccessListener 并实现 ApplicationListener 接口：</p>
<pre><code>    @Component
    public class LoginSuccessListener implements ApplicationListener {

    private final static Logger log = Logger.getLogger(LoginSuccessListener.class);

    @Autowired
    private LoginLogService loginLogService;

    public void onApplicationEvent(ApplicationEvent event) {
        if (event instanceof AuthenticationSuccessEvent) {
            AuthenticationSuccessEvent authEvent = (AuthenticationSuccessEvent) event;
            WebAuthenticationDetails webDetail = (WebAuthenticationDetails) authEvent.getAuthentication().getDetails();
            Object principal = authEvent.getAuthentication().getPrincipal();
            User user = null;
            if(principal instanceof OpenUser){
                user = ((OpenUser) principal).getUser();
            }else {
                user = (User)principal;
            }
            LoginLog loginLog = new LoginLog();
            loginLog.setIp(webDetail.getRemoteAddress());
            loginLog.setCreateTime(new Date());
            loginLog.setuId(user.getId());
            loginLogService.add(loginLog);
            log.info(user.getNickName()+",IP:"+webDetail.getRemoteAddress()+" 登录成功");
        }
    }

    }
</code></pre>
<p>解读：</p>
<p>（1）通过 <code>@Component</code> 注解将 LoginSuccessListener 交给 Spring 管理，由 Spring 实例化该对象。</p>
<p>（2）通过 <code>@Autowired</code> 注解注入 LoginLogService 对象。</p>
<p>（3）如果该 event 是 AuthenticationSuccessEvent 类型的话，将该 event 强转为 AuthenticationSuccessEvent 对象。</p>
<p>（4）通过 AuthenticationSuccessEvent 获取 WebAuthenticationDetails 对象。</p>
<p>（5）通过 AuthenticationSuccessEvent 对象获取 Object 类型的 principal，然后根据 principal 的实例类型获取 User 对象。</p>
<p>（6）将相关属性设置到 LoginLog 登录日志对象中，最后将数据插入到数据库中。</p>
<p><strong>2.</strong> 我们再看下其他登录监听事件。</p>
<p><img src="https://images.gitbook.cn/c44012f0-81b4-11e8-b718-fd519f27386c" alt="enter image description here" /></p>
<p>按顺序依次是：</p>
<ol>
<li>登录成功监听事件。</li>
<li>账户不可用登录失败监听事件。</li>
<li>账户过期登录失败监听事件。</li>
<li>账户锁定登录失败监听事件。</li>
<li>账户密码错误登录失败监听事件。</li>
<li>账户密码过期登录失败监听事件。</li>
</ol>
<p>根据判断不同的监听事件就可以监听不同的登录状态：</p>
<pre><code>    if (event instanceof 监听事件) {
</code></pre>
<p><strong>3.</strong> 解除 <code>login_log</code> 表的外键关系。</p>
<p>因为插入登录日志之后，会插入用户 ID，之前我们建立了外键约束，如果删除某用户的话，要先删除该用户 ID 对应的所有登录日志信息，如果不想删除的话就要解除外键约束，查看 <code>login_log</code> 表的外键名称：</p>
<p><img src="https://images.gitbook.cn/6536de10-81d2-11e8-9d71-995acabbbf78" alt="enter image description here" /></p>
<p>解除外键约束 SQL 语句：</p>
<pre><code>    alter table login_log drop foreign key FK_Reference_12;
</code></pre>
<p>如果不想解除外键约束的话，记得在删除用户之前先删除关联的表中信息。</p>
<blockquote>
  <p>第17课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1MW04zTVPG9xkLc-MFBE28Q </p>
  <p>密码：vkpn</p>
</blockquote></div></article>