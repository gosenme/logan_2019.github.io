---
title: SSM 博客系统开发实战-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="springsecurity">Spring Security 简介</h3>
<blockquote>
  <p>Spring Security 是一个能够为基于 Spring 的企业应用系统提供声明式的安全访问控制解决方案的安全框架。它提供了一组可以在 Spring 应用上下文中配置的 Bean，充分利用了 Spring IoC，DI（IoC：控制反转 Inversion of Control，DI：依赖注入 Dependency Injection）和 AOP（面向切面编程）功能，为应用系统提供声明式的安全访问控制功能，减少了为企业系统安全控制编写大量重复代码的工作。</p>
  <p>——来源百度百科</p>
</blockquote>
<p>在做 Spring Security 整合之前，先带大家看下 Spring Security 的源码，了解其实现原理。</p>
<h3 id="springsecurity-1">Spring Security 源码解读</h3>
<h4 id="springsecurity-2">Spring Security 源码下载</h4>
<p>Spring Security 源码下载地址见下：</p>
<blockquote>
  <p>https://github.com/spring-projects/spring-security</p>
</blockquote>
<p>大家可以用 Git 把项目克隆到本地或者直接下载 Zip 源码包，如图：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security-1.png" alt="" /></p>
<h4 id="">源码解读</h4>
<p>Spring Security 项目源码下载完成以后，用 IDE 打开该项目。</p>
<p><strong>1.</strong> 使用 Ctrl+Shift+N 组合键查找 UsernamePasswordAuthenticationFilter 过滤器，该过滤器是用来处理用户认证逻辑的，进入后如图：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security-3.png" alt="" /></p>
<p>（1）可以看到它默认的登录请求 URL 是 <code>/login</code>，并且只允许 POST 方式的请求。</p>
<p>（2）obtainUsername() 方法点进去发现它默认是根据参数名为 username 和 password 来获取用户名和密码的。</p>
<p>（3）通过构造方法实例化一个 UsernamePasswordAuthenticationToken 对象，此时调用的是 UsernamePasswordAuthenticationToken 的两个参数的构造函数，如果点击进不去，可直接用 Ctrl+Shift+N 查找（等依赖自动下载完成就可以跟进了），如图：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security-4.png" alt="" /></p>
<p>其中 super(null) 调用的是父类的构造方法，传入的是权限集合，因为目前还没有认证通过，所以不知道有什么权限信息，这里设置为 null，然后将用户名和密码分别赋值给 principal 和 credentials，同样因为此时还未进行身份认证，所以 setAuthenticated(false)。</p>
<p>（4）setDetails(request, authRequest) 是将当前的请求信息设置到 UsernamePasswordAuthenticationToken 中。</p>
<p>（5）通过调用 getAuthenticationManager() 来获取 AuthenticationManager，通过调用它的 authenticate 方法来查找支持该 token(UsernamePasswordAuthenticationToken) 认证方式的 provider，然后调用该 provider 的 authenticate 方法进行认证)。</p>
<p><strong>2.</strong> AuthenticationManager 是用来管理 AuthenticationProvider 的接口，通过查找后进入，然后使用 Ctrl+H 组合键查看它的继承关系，找到 ProviderManager 实现类，它实现了 AuthenticationManager 接口，查看它的 authenticate 方法，它里面有段这样的代码：</p>
<pre><code>    for (AuthenticationProvider provider : getProviders()) {
            if (!provider.supports(toTest)) {
                continue;
            }
        ...
        try {
                result = provider.authenticate(authentication);
        ...
        }
    }
</code></pre>
<p>通过 for 循环遍历 AuthenticationProvider 对象的集合，找到支持当前认证方式的 AuthenticationProvider，找到之后调用该 AuthenticationProvider 的 authenticate 方法进行认证处理：</p>
<pre><code>    result = provider.authenticate(authentication);
</code></pre>
<p><strong>3.</strong> AuthenticationProvider 接口，就是进行身份认证的接口，它里面有两个方法：authenticate 认证方法和 supports 是否支持某种类型 Token 的方法，通过 Ctrl+H 查看继承关系，找到 AbstractUserDetailsAuthenticationProvider 抽象类，它实现了 AuthenticationProvider 接口，它的 supports 方法如下：</p>
<pre><code>        public boolean supports(Class&lt;?&gt; authentication) {
            return (UsernamePasswordAuthenticationToken.class
                .isAssignableFrom(authentication));
            }
</code></pre>
<p>说明它是支持 UsernamePasswordAuthenticationToken 类型的 AuthenticationProvider。</p>
<p>再看它的 authenticate 认证方法，其中有一段这样的代码：</p>
<pre><code>    boolean cacheWasUsed = true;
        UserDetails user = this.userCache.getUserFromCache(username);

        if (user == null) {
            cacheWasUsed = false;

            try {
                user = retrieveUser(username,
                        (UsernamePasswordAuthenticationToken) authentication);
            }
        ...
        }
</code></pre>
<p>如果从缓存中没有获取到 UserDetails，那么它调用 retrieveUser 方法来获取用户信息 UserDetails，这里的 retrieveUser 是抽象方法，等一会我们看它的子类实现。</p>
<p>用户信息 UserDetails 是个接口，我们进入查看，它包含以下6个接口方法：</p>
<pre><code class="     language-    ">    Collection&lt;? extends GrantedAuthority&gt; getAuthorities();//获取权限集合
    String getPassword();  //获取密码
    String getUsername();   //获取用户名
    boolean isAccountNonExpired(); //账户未过期
    boolean isAccountNonLocked();   //账户未锁定
    boolean isCredentialsNonExpired(); //密码未过期
    boolean isEnabled();    //账户可用
</code></pre>
<p>查看它的继承关系发现 User 类实现了该接口，并实现了该接口的所有方法。</p>
<p>接着 AbstractUserDetailsAuthenticationProvider 往下看，找到下面的代码：</p>
<pre><code>        preAuthenticationChecks.check(user);
        additionalAuthenticationChecks(user,
                    (UsernamePasswordAuthenticationToken) authentication);
</code></pre>
<p>preAuthenticationChecks 预检查，在最下面的内部类 DefaultPreAuthenticationChecks 中可以看到，它会检查上面提到的三个 Boolean 方法，即检查账户未锁定、账户可用、账户未过期，如果上面的方法只要有一个返回 false，就会抛出异常，那么认证就会失败。</p>
<p>additionalAuthenticationChecks 是附加检查，是个抽象方法，等下看子类的具体实现。</p>
<p>下面还有个 postAuthenticationChecks.check(user) 后检查，在最下面的 DefaultPostAuthenticationChecks 内部类中可以看到，它会检查密码未过期，如果为 false 就会抛出异常。</p>
<p>如果上面的检查都通过并且没有异常，表示认证通过，会调用下面的方法：</p>
<pre><code>    createSuccessAuthentication(principalToReturn, authentication, user);
</code></pre>
<p>跟进发现此时通过构造方法实例化对象 UsernamePasswordAuthenticationToken 时，调用的是三个参数的构造方法:</p>
<pre><code>        public UsernamePasswordAuthenticationToken(Object principal, Object credentials,
            Collection&lt;? extends GrantedAuthority&gt; authorities) {
        super(authorities);
        this.principal = principal;
        this.credentials = credentials;
        super.setAuthenticated(true); // must use super, as we override
    }
</code></pre>
<p>此时会调用父类的构造方法设置权限信息，并调用父类的 setAuthenticated(true) 方法，到这里就表示认证通过了。</p>
<p>下面我们看看 AbstractUserDetailsAuthenticationProvider 的子类，同样 Ctrl+H 可查看继承关系，找到 DaoAuthenticationProvider。</p>
<p><strong>4.</strong> DaoAuthenticationProvider 类。</p>
<p>（1）查看 additionalAuthenticationChecks 附加检查方法，它主要是检查用户密码的正确性，如果密码为空或者错误都会抛出异常。</p>
<p>（2）获取用户信息 UserDetails 的 retrieveUser 方法，主要看下面这段代码：</p>
<pre><code>    UserDetails loadedUser = this.getUserDetailsService().loadUserByUsername(username);
</code></pre>
<p>它调用了 getUserDetailsService 先获取到 UserDetailsService 对象，通过调用 UserDetailsService 对象的 loadUserByUsername 方法获取用户信息 UserDetails。</p>
<p>找到 UserDetailsService，发现它是一个接口，查看继承关系，有很多实现，都是 Spring Security 提供的实现类，并不能满足我们的需要，我们想自己制定获取用户信息的逻辑，所以我们可以实现这个接口。比如从我们的数据库中查找用户信息。</p>
<p><strong>5.</strong> SecurityContextPersistenceFilter 过滤器。</p>
<p>那么用户认证成功之后，又是怎么保存认证信息的呢，在下一次请求过来时如何判断该用户是否已经认证了呢？</p>
<p>请求进来时会经过 SecurityContextPersistenceFilter 过滤器，进入 SecurityContextPersistenceFilter 过滤器并找到以下代码：</p>
<pre><code>    SecurityContext contextBeforeChainExecution = repo.loadContext(holder);
</code></pre>
<p>从 Session 中获取 SecurityContext 对象，如果没有就实例化一个 SecurityContext 对象：</p>
<pre><code>    SecurityContextHolder.setContext(contextBeforeChainExecution);
</code></pre>
<p>将 SecurityContext 对象设置到 SecurityContextHolder 中：</p>
<pre><code>    chain.doFilter(holder.getRequest(), holder.getResponse());
</code></pre>
<p>表示放行，执行下一个过滤器。</p>
<p>执行完后面的过滤并经过 Servlet 处理之后，响应给浏览器之前再次经过此过滤器。查看以下代码：</p>
<pre><code>    SecurityContext contextAfterChainExecution = SecurityContextHolder.getContext();
    SecurityContextHolder.clearContext();
    this.repo.saveContext(contextAfterChainExecution, holder.getRequest(), holder.getResponse());
</code></pre>
<p>通过 SecurityContextHolder 获取 SecurityContext 对象，然后清除 SecurityContext，最后将获取的 SecurityContext 对象放入 Session 中。</p>
<p>其中 SecurityContextHolder 是与 ThreadLocal 绑定的，即本线程内所有的方法都可以获得 SecurityContext 对象，而 SecurityContext 对象中包含了 Authentication 对象，即用户的认证信息，Spring Security 判断用户是否认证主要是根据 SecurityContext 中的 Authentication 对象来判断。Authentication 对象的详细信息如图：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security.png" alt="" /></p>
<p>最后整个过程的流程大致如下图：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/spring-securityx.png" alt="" /></p>
<h3 id="springsecurity-3">Spring Security 在项目中的应用</h3>
<p>本节课主要介绍账号登录的认证授权。</p>
<p>为了提高代码的可读性以及可维护性，我们将不同方式的认证授权放在不同的包下。</p>
<p>首先在 wang.dreamland.www 包下新建 security 包，然后在 security 包下新建 account、phone 和 open ，分别代表账号登录、手机登录和第三方登录的认证授权。</p>
<h4 id="-1">账号登录认证授权</h4>
<p><strong>1.</strong> 实现 UserDetails 接口。</p>
<p>通过上面的源码分析，框架需要的是 UserDetails 类型的实体，所以我们要将实体类 User 实现 UserDetails 接口，然后重写它的所有方法：</p>
<pre><code>    public class User implements UserDetails{

    @Override
    public Collection&lt;? extends GrantedAuthority&gt; getAuthorities() {
        if(roles == null || roles.size()&lt;=0){
            return null;
        }
        List&lt;SimpleGrantedAuthority&gt; authorities = new ArrayList&lt;SimpleGrantedAuthority&gt;();
        for(Role r:roles){
            authorities.add(new SimpleGrantedAuthority(r.getRoleValue()));
        }
        return authorities;
    }

    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
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
        if(StringUtils.isNotBlank(state) &amp;&amp; "1".equals(state) &amp;&amp; StringUtils.isNotBlank(enable) &amp;&amp; "1".equals(enable)){
            return true;
        }
        return false;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof User) {
            return getEmail().equals(((User)obj).getEmail())||getUsername().equals(((User)obj).getUsername());
        }
        return false;
    }
    @Override
    public int hashCode() {
        return getUsername().hashCode();
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", email='" + email + '\'' +
                ", password='" + password + '\'' +
                ", phone='" + phone + '\'' +
                ", nickName='" + nickName + '\'' +
                ", state='" + state + '\'' +
                ", imgUrl='" + imgUrl + '\'' +
                ", enable='" + enable + '\'' +
                ", roles=" + roles +
                '}';
    }

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）其中 getAuthorities 方法是获取用户角色信息的方法，用于授权。不同的角色可以拥有不同的权限。</p>
<p>（2）账户未过期、账户未锁定和密码未过期我们这里没有用到，直接返回 True，你也可以根据自己的应用场景写自己的业务逻辑。</p>
<p>（3）为了区分是否是同一个用户，重写 equals 和 hashCode 方法。</p>
<h4 id="userdetailsservice">实现 UserDetailsService 接口</h4>
<p>通过上面的源码分析知道，Spring Security 提供的获取用户信息的方式不满足我们的需求，所以我们自己制定获取用户信息的方式。</p>
<p><strong>1.</strong> 准备。</p>
<p>（1）因为不仅要获取用户的基本信息，还要获取用户的角色信息，所以在 RoleService 中添加根据用户 id 获取角色列表的方法：</p>
<pre><code>     /**
     * 根据用户id查询所有角色
     * @param uid
     * @return
     */
    List&lt;Role&gt; findByUid(Long uid);
</code></pre>
<p>（2）因为要通过子查询的方式查询角色信息，所以通用 mapper 满足不了需求，需要手写 XML，在 RoleMapper 中添加下面的接口方法：</p>
<pre><code>    /**
     * 根据用户id查询角色信息
     * @param uid
     * @return
     */
    List&lt;Role&gt; findByUid(@Param("uid")Long uid);
</code></pre>
<p>（3）在 <code>resources/mapping</code> 下新建 role.xml 文件，配置如下：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
    &lt;!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt;
    &lt;mapper namespace="wang.dreamland.www.dao.RoleMapper"&gt;
    &lt;select id="findByUid"  resultMap="roleListMap"&gt;
      select id,role_name,role_value,enabled from role where id in(select r.r_id from user u, role_user r where u.id = r.u_id and r.u_id = #{uid}) and enabled =1
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.Role" id="roleListMap"&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="roleName" column="role_name" /&gt;
        &lt;result property="roleValue" column="role_value" /&gt;
        &lt;result property="enabled" column="enabled" /&gt;
    &lt;/resultMap&gt;
    &lt;/mapper&gt;
</code></pre>
<p>查询 SQL 语句，如下：</p>
<pre><code>    select id,role_name,role_value,enabled from role where id in(select r.r_id from user u, role_user r where u.id = r.u_id and r.u_id = #{uid}) and enabled =1
</code></pre>
<p>其中括号内的是根据两表关联查询，根据用户 id 查询出所有角色的 id，然后将查询结果当作外层查询语句的查询条件，根据所有角色 id 查询出角色列表，其中 enabled=1 代表查询出可用的角色。其它标签含义之前已经介绍过，这里不再赘述。</p>
<p>（4）在 RoleServiceImpl 实现类中，实现 RoleService 接口中的方法：</p>
<pre><code>    @Override
    public List&lt;Role&gt; findByUid(Long uid) {
        return roleMapper.findByUid(uid);
    }
</code></pre>
<p><strong>2.</strong> 在 account 包下新建 AccountDetailsService 并实现 UserDetailsService 接口：</p>
<pre><code>    public class AccountDetailsService implements UserDetailsService{
    @Autowired
    private UserService userService;
    @Autowired
    private RoleService roleService;
    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        User user = userService.findByEmail(email);
        if(user == null){
            throw new UsernameNotFoundException("用户名或密码错误");
        }
        List&lt;Role&gt; roles = roleService.findByUid(user.getId());
        user.setRoles(roles);

        return user;
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 Autowired 注解注入 UserService 和 RoleService 对象。</p>
<p>（2）根据 email 查询用户，如果为 null 直接抛出异常。</p>
<p>（3）如果不为 null，则根据用户 id 查询角色列表，将角色信息添加到 User 中。</p>
<p>（4）将 user 返回。</p>
<h4 id="3usernamepasswordauthenticationfilter">3.继承 UsernamePasswordAuthenticationFilter 过滤器</h4>
<p>通过源码分析得知 UsernamePasswordAuthenticationFilter 是处理用户认证逻辑的过滤器，继承它可制定自己的认证逻辑，比如加上验证码的验证。</p>
<p>在 account 包下新建 AccountAuthenticationFilter 并继承 UsernamePasswordAuthenticationFilter：</p>
<pre><code>    public class AccountAuthenticationFilter extends UsernamePasswordAuthenticationFilter {
    private String codeParameter = "code";
    @Override
    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException {
        String username = this.obtainUsername(request);
        String password = this.obtainPassword(request);
        String code = this.obtainCode(request);
        String caChecode = (String)request.getSession().getAttribute("VERCODE_KEY");
        boolean flag = CodeValidate.validateCode(code,caChecode);
        if(!flag){
            throw new UsernameNotFoundException("验证码错误");
        }
        if(username == null) {
            username = "";
        }

        if(password == null) {
            password = "";
        }
        username = username.trim();
        UsernamePasswordAuthenticationToken authRequest = new UsernamePasswordAuthenticationToken(username, password);
        this.setDetails(request, authRequest);
        return this.getAuthenticationManager().authenticate(authRequest);
    }

    protected String obtainCode(HttpServletRequest request) {
        return request.getParameter(this.codeParameter);
    }

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）调用父类的方法获取用户名和密码，默认请求参数是 username 和 password。</p>
<p>（2）调用自定义方法 obtainCode 获取验证码 code，请求参数是 code。</p>
<p>（3）获取 Session 中存入的验证码 caCheCode，key 是 <code>VERCODE_KEY</code>。</p>
<p>（4）为了实现可重用，我将判断验证码是否以正确的方法封装到了common 包下的 CodeValidate 类中了，方法很简单：</p>
<pre><code>     public static boolean validateCode(String code,String cacheCode){
        if(StringUtils.isNotBlank(code) &amp;&amp; code.equals(cacheCode)){
            return true;
        }
        return false;
    }
</code></pre>
<p>（5）如果验证码校验失败则直接抛出异常，认证失败。</p>
<p>（6）下面的代码和源码中一致，将用户名和密码封装到 UsernamePasswordAuthenticationToken 对象中，然后设置请求信息，找到支持的 AuthenticationProvider 进行认证。</p>
<h4 id="accessdeniedhandler">实现 AccessDeniedHandler 接口</h4>
<p>用户在未登录的情况下访问受保护资源时，会直接跳转到登录页面（不包含 AJAX 请求），这种情况不用考虑。</p>
<p>但是当用户登录之后访问未保护资源时，它默认会返回403的错误页面，这不是我们想要的结果。我们通过实现 AccessDeniedHandler 接口可以让它跳转到指定页面，比如跳转到 accessDenied.jsp，提示用户没有访问权限等。</p>
<p>在 account 包下新建 MyAccessDeniedHandler 并实现 AccessDeniedHandler 接口：</p>
<pre><code>    public class MyAccessDeniedHandler implements AccessDeniedHandler {
    private String errorPage;
    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException e) throws IOException, ServletException {
        boolean isAjax = "XMLHttpRequest".equals(request.getHeader("X-Requested-With"));
        if (isAjax) {
            String jsonObject = "{\"message\":\"Access is denied！\",\"access-denied\":true}";
            String contentType = "application/json";
            response.setContentType(contentType);
            PrintWriter out = response.getWriter();
            out.print(jsonObject);
            out.flush();
            out.close();
            return;
        } else {
            if (!response.isCommitted()) {
                if (this.errorPage != null) {
                    request.setAttribute("SPRING_SECURITY_403_EXCEPTION", e);
                    response.setStatus(403);
                    RequestDispatcher dispatcher = request.getRequestDispatcher(this.errorPage);
                    dispatcher.forward(request, response);

                } else {
                    response.sendError(403, e.getMessage());
                }
            }
        }
    }

    public void setErrorPage(String errorPage) {
        if(errorPage != null &amp;&amp; !errorPage.startsWith("/")) {
            throw new IllegalArgumentException("errorPage must begin with '/'");
        } else {
            this.errorPage = errorPage;
        }
    }
    }
</code></pre>
<p>代码解读，如下：</p>
<p>（1）主要通过 set 方法获取配置文件中配置的 errorPage 路径。</p>
<p>（2）根据请求头中 <code>X-Requested-With</code> 的属性值是否是 XMLHttpRequest 来判断是不是 AJAX 请求。</p>
<p>（3）如果是 AJAX 请求则返回 JSON 格式数据，并结束方法。</p>
<p>（4）如果不是 AJAX 请求。再判断 errorPage 是否为空，如果不为空，则设置状态码为403，并转发到配置的错误页面，如果 errorPage 为空，则直接返回403错误页面。</p>
<h4 id="springsecurityxml">spring-security.xml 配置文件的配置</h4>
<p>spring-security.xml 配置文件内容很多。这里就不粘贴了，详见百度网盘，说几个重点配置（未按照顺序）。</p>
<p><strong>1.</strong> 对静态资源和都可以访问的资源不拦截，比如：CSS、JS 等静态资源，登录、注册等都可以访问的路径。</p>
<pre><code>    &lt;security:http security="none" pattern="/css/**" /&gt;
    &lt;security:http security="none" pattern="/login*" /&gt;
    &lt;security:http security="none" pattern="/register*" /&gt;
</code></pre>
<p><strong>2.</strong> 对访问路径不拦截的还有下面的配置，permitAll 允许所有，但是它会经过过滤器，可以获取到用户信息。上面的 none 不经过过滤器直接放行，所以获取不到用户信息：</p>
<pre><code>    &lt;security:intercept-url pattern="/index**" access="permitAll"/&gt;
</code></pre>
<p><strong>3.</strong> 除了设置为 none 和 permitAll 的访问路径，其它都会进行拦截，并且必须具备 <code>ROLE_USER</code> 权限才能访问，注意 Spring Security 的角色信息要以 <code>ROLE_</code> 开头。</p>
<pre><code>    &lt;security:intercept-url pattern="/**" access="hasRole('ROLE_USER')"/&gt;
</code></pre>
<p><strong>4.</strong> AccessDecisionManager 访问决策管理器是一组投票器的集合，默认的策略是使用一个 AffirmativeBased，既只要有一个投票器通过验证就允许用户访问。</p>
<pre><code>    &lt;security:http auto-config="false" access-decision-manager-ref="accessDecisionManager"
                    use-expressions="true" entry-point-ref="loginEntryPoint"&gt;


    &lt;/security:http&gt;

    &lt;bean id="accessDecisionManager" class="org.springframework.security.access.vote.AffirmativeBased"&gt;
        &lt;constructor-arg&gt;
            &lt;list&gt;
                &lt;ref local="roleVoter"/&gt;
                &lt;ref local="authenticatedVoter"/&gt;
                &lt;ref local="expressionVoter"/&gt;
            &lt;/list&gt;
        &lt;/constructor-arg&gt;
    &lt;/bean&gt;
</code></pre>
<p><strong>5.</strong> 将 <code>frame-options</code> 设置为禁用，否则浏览器拒绝当前页面加载任何 Frame 页面。如果不加如下设置，上传图片时会超时：</p>
<pre><code>     &lt;security:headers&gt;
            &lt;security:frame-options disabled="true"&gt;&lt;/security:frame-options&gt;
     &lt;/security:headers&gt;
</code></pre>
<p><strong>6.</strong> 配置登录页信息，分别为登录 URL、认证失败跳转 URL、认证成功跳转 URL、登录 URL、password 和 username 请求参数名称：</p>
<pre><code>    &lt;security:form-login login-page="/login" authentication-failure-url="/login?error=1"
                              default-target-url="/list" login-processing-url="/doLogin"
                             password-parameter="password" username-parameter="username" /&gt;
</code></pre>
<p><strong>7.</strong> 配置我们上面实现的 MyAccessDeniedHandler 处理器：</p>
<pre><code>     &lt;security:access-denied-handler ref="accessDeniedHandler" /&gt;
     &lt;bean id="accessDeniedHandler"
                class="wang.dreamland.www.security.account.MyAccessDeniedHandler"&gt;
        &lt;property name="errorPage" value="/accessDenied.jsp" /&gt;
    &lt;/bean&gt;
</code></pre>
<p>errorPage 我配置的是 accessDenied.jsp，在 webapp 目录下新建 accessDenied.jsp，我只简单提示无访问权限：</p>
<pre><code>    &lt;%@ page contentType="text/html;charset=UTF-8"%&gt;
    &lt;html&gt;
    &lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;
    &lt;/head&gt;
    &lt;body&gt;
    &lt;span style="color: red"&gt;无访问权限&lt;/span&gt;
    &lt;/body&gt;
    &lt;/html&gt;
</code></pre>
<p><strong>8.</strong> 在用户未登录时，如果访问受保护资源，会跳转到下面配置的默认登录页：</p>
<pre><code>     &lt;bean id="loginEntryPoint"
        class="org.springframework.security.web.authentication.LoginUrlAuthenticationEntryPoint"&gt;
        &lt;!-- 默认登录页的url --&gt;
        &lt;constructor-arg value="/login?error=login"/&gt;
    &lt;/bean&gt;
</code></pre>
<p><strong>9.</strong> 认证管理器 authenticationManager，使用自定义的 accountService，并对密码采用 MD5 加密，注意这里使用的是 Spring Security 提供的 MD5 加密工具，盐 salt 改为对应的用户名。</p>
<pre><code>    &lt;security:authentication-manager alias="authenticationManager"&gt;
        &lt;security:authentication-provider user-service-ref="accountService"&gt;
            &lt;security:password-encoder hash="md5"&gt;
                &lt;security:salt-source user-property="username"&gt;&lt;/security:salt-source&gt;
            &lt;/security:password-encoder&gt;
        &lt;/security:authentication-provider&gt;
    &lt;/security:authentication-manager&gt;

    &lt;bean id="accountService" class="wang.dreamland.www.security.account.AccountDetailsService"/&gt;
</code></pre>
<p><strong>10.</strong> 配置我们上面自定义的过滤器 AccountAuthenticationFilter，属性依次为登录 URL、认证管理器、Session策略、认证成功处理器和认证失败处理器。认证成功默认跳转 <code>/list</code>，认证失败跳转到登录。</p>
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
            &lt;bean class="org.springframework.security.web.authentication.SimpleUrlAuthenticationFailureHandler"&gt;
                &lt;property name="defaultFailureUrl" value="/login?error=fail"&gt;&lt;/property&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
    &lt;/bean&gt;
</code></pre>
<p>其它未列出的请参考配置文件中的注释。</p>
<h4 id="webxml">web.xml 配置</h4>
<p><strong>1.</strong> 在 web.xml 中配置 Spring Security 的权限过滤器链：</p>
<pre><code>    &lt;filter&gt;
        &lt;filter-name&gt;springSecurityFilterChain&lt;/filter-name&gt;
        &lt;filter-class&gt;org.springframework.web.filter.DelegatingFilterProxy&lt;/filter-class&gt;
    &lt;/filter&gt;
    &lt;filter-mapping&gt;
        &lt;filter-name&gt;springSecurityFilterChain&lt;/filter-name&gt;
        &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
    &lt;/filter-mapping&gt;
</code></pre>
<p><strong>2.</strong> 在 web.xml 中引入 spring-security.xml：</p>
<pre><code>    &lt;context-param&gt;
        &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
        &lt;param-value&gt;
          classpath:spring-mybatis.xml,
          classpath:applicationContext-redis.xml,
          classpath:applicationContext-activemq.xml,
          classpath:applicationContext-solr.xml,
          classpath:spring-security.xml
        &lt;/param-value&gt;
    &lt;/context-param&gt;
</code></pre>
<h4 id="-2">启动测试</h4>
<p>现在我们配置的是根据 Spring Security 提供的 MD5 加密方式生成的密码，如果测试登录肯定会失败。我们可以通过单元测试或者 main 方法根据用户名生成对应的 MD5 密码。</p>
<p><strong>1.</strong> 生成 MD5 密码。</p>
<pre><code>        public static void main(String[] args) {
            String password = new Md5PasswordEncoder().encodePassword("123456", "123456@qq.com");
            System.out.println(password);
    }
</code></pre>
<p>比如我的数据库中有个 <code>123456@qq.com</code> 的用户，根据 Spring Security 提供的 MD5 加密工具生成对应的密码，原密码是：123456 ， 盐salt是用户邮箱即：123456@qq.com，加密后的密码就是：</p>
<blockquote>
  <p>794ad2ea7aab3848080cffcd2968a212</p>
</blockquote>
<p>将此密码替换掉数据库该用户对应的密码，目前只是测试使用，之后用户注册的时候加密方式也要替换成 Spring Security 提供的 MD5 加密方式。</p>
<p><strong>2.</strong> 启动 Tomcat，点击登录，输入错误的密码会发现又跳转到了登录页面。输入正确的密码后跳转到了无访问权限页面。因为我们之前配置中除了放行的路径，其它访问路径都需要 <code>ROLE_USER</code> 角色才能访问。</p>
<p><strong>3.</strong> 给登录用户赋予 <code>ROLE_USER</code> 角色。</p>
<p>首先在 role 表中添加一条数据，如下：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security-5.png" alt="" /></p>
<p>然后在中间表 <code>role_user</code> 添加用户和角色对应信息，即用户 id 为1的用户对应的角色 id 为1的角色：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/security-6.png" alt="" /></p>
<p>这样用户 id 为1的用户就用了 <code>ROLE_USER</code> 角色所拥有的权限。</p>
<p><strong>4.</strong> 再次输入正确的密码访问，这次没有跳转到无访问权限页面而是跳转到了登录页面。原因是之前从 Session 中取的用户，判断为空后又跳转到了登录页面。</p>
<p>解决方法是：我们知道现在用户的认证信息都存在了 SecurityContext 中，我们可以通过 SecurityContext 获取，在 BaseController 中添加获取当前用户的方法：</p>
<pre><code>    /**
     * 获取当前用户
     * @return
     */
    public User getCurrentUser(){
        User user = null;
        Authentication authentication = null;
        SecurityContext context = SecurityContextHolder.getContext();
        if(context!=null){
            authentication = context.getAuthentication();
        }
        if(authentication!=null){
            Object principal = authentication.getPrincipal();
            //如果是匿名用户
            if(authentication.getPrincipal().toString().equals( "anonymousUser" )){
                return null;
            }else {
                user = (User)principal;
            }

        }
        return user;
    }
</code></pre>
<p>方法很简单，就是从 SecurityContextHolder 中拿到 SecurityContext 对象，然后从 SecurityContext 中拿到 Authentication 对象，通过 Authentication 对象的 getPrincipal() 就可以获取到用户信息。中间做了一些非空判断等。</p>
<p>用户登录成功默认是跳转到 <code>/list</code> 的路径，所以在 PersonalController 中找到该映射 URL 对应的方法，将获取用户的方法改成如下：</p>
<pre><code>    User user = getCurrentUser();
</code></pre>
<p>注意其他获取用户的方法都要改成上面的形式，否则获取不到用户信息。</p>
<p>重新启动程序，输入正确的密码后发现已经可以成功访问个人主页。认证授权成功！</p>
<p><strong>5.</strong> 之前提到过，用户未登录时如果访问受保护资源会自动跳转到登录页面，但如果是 AJAX 请求就失效了，比如未登录的情况下点击首页的点赞时，后台会报 AccessDeniedException 异常，但是页面不跳转。我们想让用户跳转到登录页面可以这样做：</p>
<pre><code>    //点赞或踩
    function upvote_click(id,cont) {
        var uid = "${user.id}";
        if(uid==''||uid==null){
            window.location.href = "/login.jsp";
            return
        }
        $.ajax({
        ...
</code></pre>
<p>在 <code>upvote_click</code> 方法中先获取用户的 id，如果用户 id 不存在则说明未登录，直接跳转到登录页面。</p>
<p>像校验邮箱、校验手机号等的 AJAX 我是直接放行的。</p>
<p><strong>6.</strong> 用户登录成功以后，如果访问：<code>http://localhost:8080/index.jsp</code> 或者：<code>http://localhost:8080</code> 会发现页面获取不到用户信息，因为在自定义 IndexJspFilter 过滤器中没有保存用户 user，部分代码修改如下：</p>
<pre><code>    public class IndexJspFilter extends BaseController implements Filter{
        ...
        User user = getCurrentUser();
        request.setAttribute("user",user);
        ...
    }
</code></pre>
<p>将 IndexJspFilter 继承 BaseController，然后调用它的 getCurrentUser() 方法获取当前用户信息，然后保存到 Request 域中。这样前端页面就可以通过 EL 表达式获取用户信息了。</p>
<blockquote>
  <p>第15课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1Bzsisjf2DtsFK5LX8_dgqg 密码：3irw</p>
</blockquote></div></article>