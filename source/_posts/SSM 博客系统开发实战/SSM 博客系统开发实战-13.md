---
title: SSM 博客系统开发实战-13
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>正式开始本文内容前，我们先做下准备，即在 <code>WEB-INF</code> 下的 personal 文件夹下导入个人资料修改页面 profile.jsp 文件。</p>
<p>通过访问个人主页的修改个人资料进入个人资料修改页面，如图：</p>
<p><img src="http://images.gitbook.cn/503bc000-8067-11e8-b5ab-41e00ce48fd0" alt="" /></p>
<p>点击事件如下：</p>
<pre><code>&lt;a href="${ctx}/profile"&gt;&lt;i class="icon icon-edit"&gt;&lt;/i&gt;&lt;span style="margin-left: 10px"&gt;修改个人资料&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p>如果不想 a 标签出现下划线，可将 a 标签的 style 属性的 <code>text-decoration</code> 值设置为 none，如下：</p>
<pre><code>style="text-decoration: none"
</code></pre>
<p>因为个人资料页面 profile.jsp 在 <code>WEN-INF</code> 下，所以要经过 Controller 处理后跳转，在 PersonalController.java 内添加映射 URL 为 <code>/profile</code> 的方法，如下：</p>
<pre><code>    @Autowired
    private UserInfoService userInfoService;

    /**
     * 进入个人资料修改页面
     * @param model
     * @return
     */
    @RequestMapping("/profile")
    public String profile(Model model) {
        User user = (User)getSession().getAttribute("user");
        if(user==null){
            return "../login";
        }
        UserInfo userInfo =   userInfoService.findByUid(user.getId());
        model.addAttribute("user",user);
        model.addAttribute("userInfo",userInfo);

        return "personal/profile";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 中取出用户信息，判断用户是否登录，未登录则跳转登录。</p>
<p>（2）用户登录后，根据用户 id 查询出用户详细信息 userInfo，将 user 和 userInfo 都放入 model 中。</p>
<p>（3）返回到 personal 目录下的 profile.jsp 页面。</p>
<p>重启项目后，点击修改个人资料进入个人资料修改页面，效果如下：</p>
<p><img src="http://images.gitbook.cn/993d0520-8067-11e8-b887-ad9ea87ef533" alt="" /></p>
<p>个人资料修改页面准备分四部分来讲：</p>
<ol>
<li>修改个人头像</li>
<li>基本设置</li>
<li>账号设置</li>
<li>绑定设置</li>
</ol>
<h3 id="">修改个人头像</h3>
<p>思路就这样的：通过点击头像图片，弹出选择图片窗口，弹出选择窗口需要将 input 框的 type 设置为 file，选择好图片以后，触发 onchange 事件，发送AJAX，通过提交 form 表单将图片上传，success 回调函数返回上传图片路径，将原图片的 src 路径替换，完成修改个人头像。</p>
<p>个人头像 a 标签及 form 表单代码如下：</p>
<pre><code>     &lt;a  title="${user.nickName}" class="avatar"&gt;&lt;img id="img-change"  src="${user.imgUrl}" onclick="selectImg();" width="100" height="100" style="border-radius:50%;margin-top: 60px;margin-left: 90px"&gt;&lt;/a&gt;
     &lt;form id="upload-form"   style="width:auto;" &gt;
         &lt;input type="file"  id="change-img" name="uploadImg" onchange="changeImg();" style="display:none;"&gt;
      &lt;/form&gt;
</code></pre>
<p><strong>1.</strong> 事件源</p>
<p>头像的点击事件 onclick 具体方法如下：</p>
<pre><code>    //点击图片事件
    function selectImg() {
        document.getElementById("change-img").click();
    }
</code></pre>
<p>获取 id 为 <code>change-img</code> 的对象，触发其点击事件，即弹出图片选择窗口。图片选择完毕以后触发 onchange 事件，onchange 事件方法如下：</p>
<pre><code>    //图片选择后事件
    function changeImg() {
    var formData = new FormData($( "#upload-form" )[0]);
    $.ajax({
        url: '/fileUpload' ,
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            var msg = data["error"];
            if(msg==0){
                //上传成功
                var url = data["url"];
                document.getElementById("img-change").src = url;
                saveImg(url);
            }

        }
    });
    }

    //保存个人头像
    function saveImg(url) {
    $.ajax({
        type:'post',
        data: {"url":url},
        url: '/saveImage' ,
        dataType:'json',
        success: function (data) {
          // alert(data["msg"]);
        }
    });
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）根据 form 表单的 id 通过 new FormData 获取表单对象数据，赋值给 formData。</p>
<p>（2）发送 AJAX，映射 URL 为：<code>/fileUpload</code>，对应之前上传文件的 UploadController，上传方式为 post 方式，请求参数 data 为 formData。</p>
<p>（3）回调函数 success 返回数据 data，通过 <code>data["error"]</code> 获取上传状态，如果为0说明上传成功，根据 <code>data["url"]</code> 获取上传成功后的图片路径赋值给 URL，然后根据 id 获取 img 标签对象，将其 src 属性值重新赋值为 URL，实现更换头像。</p>
<p>（4）然后调用保存头像方法 saveImg，接收的参数是刚才回调函数返回的URL。</p>
<p>（5）保存头像的方法也是一个 AJAX 异步请求，请求参数 data 是图片的路径 URL，回调函数可返回保存头像的结果，成功还是失败。</p>
<p><strong>2.</strong> Java 后台</p>
<p>对应映射 URL 为 <code>/fileUpload</code> 的方法还是之前说过的 UploadController 内的上传文件方法，这里不再赘述。</p>
<p>在 PersonalController 内添加映射 URL 为 <code>/saveImage</code> 的方法：</p>
<pre><code>    @Autowired
    private UserService userService;
    /**
     * 保存个人头像
     * @param model
     * @param url
     * @return
     */
    @RequestMapping("/saveImage")
    @ResponseBody
    public  Map&lt;String,Object&gt;  saveImage(Model model,@RequestParam(value = "url",required = false) String url) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        user.setImgUrl(url);
        userService.update(user);
        map.put("msg","success");
        return map;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 中获取用户信息。</p>
<p>（2）将前台传过来的 URL 通过 set 方法赋值给 user 的 imgUrl 属性。</p>
<p>（3）调用 userService 的 update 方法更新用户信息。</p>
<p>（4）将 success 放入 map，返回给前台。</p>
<p><strong>3.</strong> 重新启动项目，点击更换头像，效果如下：</p>
<p><img src="http://images.gitbook.cn/56f7e1c0-8068-11e8-bdd3-732bf4517f33" alt="" /></p>
<h4 id="-1">发现</h4>
<p>个人头像修改之后，发现首页的文章作者头像并未改变。这是我之前挖的一个坑，肯定会有人和我想的一样，想着查询文章信息的时候把用户的昵称和头像也一起查出来，方便省事，事实证明这样做是不好的。因为用户更新了昵称或者个人头像时，都要去更新一遍 <code>user_content</code> 表的 <code>nick_name</code> 和 <code>img_url</code> 字段，这样频繁操作数据库太耗性能。应该怎么解决呢？</p>
<p>解决方法就是使用两表关联查询。查询文章的时候根据用户 id 关联查询用户表 uesr 和文章表 <code>user_content</code>。这里使用左连接查询：</p>
<pre><code>    select u1.*,u2.nick_name name,u2.img_url url from user_content u1 LEFT JOIN user u2 on u1.u_id = u2.id
</code></pre>
<p>代码解读如下：</p>
<p>（1）给 <code>user_content</code> 表起别名为 u1，给 user 表取别名为 u2，起别名主要用于区分和操作表。</p>
<p>（2）<code>select u1.*,u2.nick_name name,u2.img_url url</code>是指查询 <code>user_content</code> 表中的所有字段、user 表中的 <code>nick_name</code> 和 <code>img_url</code> 字段，并给 <code>nick_name</code> 起别名为 name，给 <code>img_url</code> 起别名为 url。</p>
<p>（3）<code>from user_content u1 LEFT JOIN user u2</code> 是指查询从 <code>user_content</code> 表左连接 user 表，LEFT JOIN 左连接，是指查询的结果以左表为主表，右表为副表，即以 <code>user_content</code> 表为主表，user 表为副表，副表没有数据的字段用 null 补充。</p>
<p>（4）<code>on u1.u_id = u2.id</code>是指连接条件：<code>user_content</code> 表的 <code>u_id</code> 和 user 表的 id 要相同。</p>
<p>查询效果演示如图：</p>
<p><img src="http://images.gitbook.cn/2e017910-8069-11e8-8db6-0d16f8c01663" alt="" /></p>
<p>具体步骤如下：</p>
<p><strong>1.</strong> 在 UserContentMapper 接口中增加连接查询方法：</p>
<pre><code>     /**
     * user_content与user连接查询
     * @return
     */
    List&lt;UserContent&gt; findByJoin(UserContent userContent);
</code></pre>
<p><strong>2.</strong> 在映射文件 <code>userContent.xml</code> 中增加查询 SQL：</p>
<pre><code>    &lt;!--user_content和user表连接查询--&gt;
    &lt;select id="findByJoin"  resultMap="joinMap"&gt;
       select u1.id,u1.u_id,u1.title,u1.category,u1.personal,u1.rpt_time,u1.upvote,u1.downvote,u1.comment_num,u1.content,u2.nick_name nickName,u2.img_url imgUrl from user_content u1 LEFT JOIN user u2 on u1.u_id = u2.id
       &lt;where&gt;
           &lt;choose&gt;
               &lt;when test='id!=null and id!=""'&gt;
                    u1.id = #{id}
               &lt;/when&gt;
               &lt;otherwise&gt;
                   &lt;if test='personal!=null and personal!=""'&gt;
                       u1.personal = #{personal}
                   &lt;/if&gt;
                   &lt;if test='personal==null or personal==""'&gt;
                       u1.personal = '0'
                   &lt;/if&gt;
               &lt;/otherwise&gt;
           &lt;/choose&gt;

       &lt;/where&gt;
        &lt;if test='uId!=null and uId!=""'&gt;
            and u1.u_id = #{uId}
        &lt;/if&gt;
      order by u1.rpt_time desc
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.UserContent" id="joinMap"&gt;
        &lt;!-- property 表示wang.dreamland.www.entity.UserContent； column 表示表中的列名 --&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="uId" column="u_id" /&gt;
        &lt;result property="title" column="title" /&gt;
        &lt;result property="category" column="category" /&gt;
        &lt;result property="personal" column="personal" /&gt;
        &lt;result property="rptTime" column="rpt_time" /&gt;
        &lt;result property="imgUrl" column="img_url" /&gt;
        &lt;result property="nickName" column="nick_name" /&gt;
        &lt;result property="upvote" column="upvote" /&gt;
        &lt;result property="downvote" column="downvote" /&gt;
        &lt;result property="commentNum" column="comment_num" /&gt;
        &lt;result property="content" column="content" /&gt;
    &lt;/resultMap&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）<code>id=findByJoin</code> 对应的是 UserContentMapper 接口中的方法名，joinMap 对应某个 resultMap 的唯一 id。</p>
<p>（2）查询 SQL 中没有使用 <code>select *</code>语句，<code>select *</code> 会降低查询效率，这里把需要查询的字段一一列举出来。注意
其中没有 <code>u1.img_url</code> 和 <code>u1.nick_name</code>，如果加上会覆盖我们的查询结果，我们要的是 user 表中的 imgUrl 和 nickName，还有别名 nickName、imgUrl 要和 UserContent 实体类中的属性对应，主要是通过属性的 setter 方法赋值，页面通过 getter 方法取值的。</p>
<p>（3）where 标签，当标签内条件成立时会形成 where 语句，choose 标签是一个整体，里面的 when 和 otherwise 标签相当于 if 和 else 的作用，如果文章 id 不为空则根据文章 id 查询，否则如果 personal 为空，则默认查询非私密的所有文章，如果 personal 属性不为空，则通过 <code>#{personal}</code> 以占位符的形式接收 personal 的值进行条件查询</p>
<p>（4）后面的 if 标签表示如果 uId 不为空，则增加查询条件，用 and 连接，并且根据用户 id 查询。</p>
<p>后面的 <code>order by u1.rpt_time desc</code> 是指按时间倒序。</p>
<p>（5）resultMap 标签是结果集的封装，其中 type 代表的是 UserContent 的实体类，给该 resultMap 取一个唯一的 id，供其他 SQL 语句引用。</p>
<p>result 标签中的 property 对应实体类的属性，column 对应表中的字段（列名），通过实体类属性的 setter 方法赋值。</p>
<p>其实这里可以将 <code>user_content</code> 表中的 <code>img_url</code> 和 <code>nick_name</code> 字段删除，将 UserContent 实体类中的 imgUrl 和 nickName 属性上加上 <code>@Transient</code> 注解，代表表中没有此字段。我这里就不操作了，你们可以试一下。</p>
<p><strong>3.</strong> 将自定义过滤器 IndexJspFilter 中的方法修改如下：</p>
<pre><code>     public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        System.out.println("===========自定义过滤器==========");
        ServletContext context = request.getServletContext();
        ApplicationContext ctx = WebApplicationContextUtils.getWebApplicationContext(context);
        UserContentMapper userContentMapper = ctx.getBean(UserContentMapper.class);
        PageHelper.startPage(null, null);//开始分页
        List&lt;UserContent&gt; list = userContentMapper.findByJoin(null);
        PageHelper.Page endPage = PageHelper.endPage();//分页结束
        request.setAttribute("page", endPage );
        chain.doFilter(request, response);
    }
</code></pre>
<p>直接调用 userContentMapper 的 findByJoin方法，参数为null，默认查询非私密文章。</p>
<p><strong>4.</strong> 将实现类 UserContentServiceImpl 中的三个方法修改如下：</p>
<pre><code>     public Page&lt;UserContent&gt; findAll(UserContent content, Integer pageNum, Integer pageSize) {
        //分页查询
        System.out.println("第"+pageNum+"页");
        System.out.println("每页显示："+pageSize+"条");
        PageHelper.startPage(pageNum, pageSize);//开始分页
        List&lt;UserContent&gt; list = userContentMapper.findByJoin(content);
        Page endPage = PageHelper.endPage();//分页结束
        List&lt;UserContent&gt; result = endPage.getResult();
        return endPage;
    }

     public Page&lt;UserContent&gt; findAll(Integer pageNum, Integer pageSize) {
        //分页查询
        PageHelper.startPage(pageNum, pageSize);//开始分页
        List&lt;UserContent&gt; list = userContentMapper.findByJoin(null);
        Page endPage = PageHelper.endPage();//分页结束
        return endPage;
    }

    //根据文章id查询
    public UserContent findById(long id) {
        UserContent userContent = new UserContent();
        userContent.setId( id );
        List&lt;UserContent&gt; list = userContentMapper.findByJoin(userContent);
        if(list!=null &amp;&amp; list.size()&gt;0){
            return list.get(0);
        }else {
            return null;
        }
    }
</code></pre>
<p>主要是将原来使用 Mapper 的通用方法改成我们自定义的连接查询的方法。</p>
<p>根据文章 id 查询的时候如果有返回结果，只会有一个，所以这里取 list 集合的第一个元素，没有则返回 null。</p>
<h3 id="-2">　基本设置</h3>
<p>首先说下，这里点击 tab 切换的原理和之前的个人主页的切换原理是一样的。都是通过显示和隐藏来达到切换的效果。比如点击基本设置对应的点击事件如下：</p>
<pre><code>    function base_set() {
    document.getElementById("base").style.backgroundColor = "white";
    document.getElementById("account").style.backgroundColor = "#D1D1D1";
    document.getElementById("binding").style.backgroundColor = "#D1D1D1 ";

    document.getElementById("set_title").innerHTML = "基本设置";

    document.getElementById("base_content").style.display = "";
    document.getElementById("account_content").style.display = "none";
    document.getElementById("binding_content").style.display = "none";

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）将“基本设置”的背景色设置为白色，“账号设置”和“绑定设置”的背景色设置为 <code>#D1D1D1</code>，和左边背景色一致。</p>
<p>（2）将右侧的标题改为“基本设置”。</p>
<p>（3）将“基本设置”的 display 属性设置为空，即可见。“账号设置”和“绑定设置”的 display 属性设置为 none，即不可见。</p>
<p>右边 div 是一个普通的 form 表单，很简单，这里只说下生日对应的 input 框，我们点击 input 框后弹出日期插件，可供我们选择日期。</p>
<h4 id="-3">日期插件</h4>
<p>这里使用的是 ZUI 提供的日期插件，</p>
<p><img src="http://images.gitbook.cn/8bcc4970-806a-11e8-8db6-0d16f8c01663" alt="" /></p>
<p>使用方法说的很明白，主要做三件事情。</p>
<p><strong>1.</strong> 单独引入日期插件的 CSS 和 JS 文件。</p>
<pre><code>     &lt;link href="${ctx}/css/zui/lib/datetimepicker/datetimepicker.min.css" rel="stylesheet"&gt;
     &lt;script src="${ctx}/css/zui/lib/datetimepicker/datetimepicker.min.js"&gt;&lt;/script&gt;
</code></pre>
<p><strong>2.</strong> 给 input 框加上指定的 class 属性 <code>form-control form-date</code>。</p>
<pre><code>     &lt;input  style="width: 198px;float: right;margin-right: 484px;margin-top: -4px" class="form-control form-date"  readonly="readonly" placeholder="选择一个日期：yyyy-MM-dd" type="text" id="txtEndDate"  name="birthday" value="${userInfo.formateBirthday==null?"":userInfo.formateBirthday}"/&gt;&lt;br/&gt;&lt;br/&gt;
</code></pre>
<p>其它的样式是我加上去的，一个靠右浮动，调整 input 框的长度，以及距离右边的距离，主要是为了与页面协调。</p>
<p>value 中的 EL 表达式是判断 userInfo 的生日是否为空，如果不为空则显示其生日，主要是一个生日信息回显的作用。因为 UserInfo 实体类中没有 getFormateBirthday 方法，所以创建此方法：</p>
<pre><code>     public String getFormateBirthday(){
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        return simpleDateFormat.format(birthday);
    }
</code></pre>
<p>主要是将日期类型 birthday 转成字符串类型。</p>
<p><code>readonly="readonly"</code> 是只读属性，只允许用户选择日期，不可手动输入。</p>
<p><strong>3.</strong> 手动调用初始化函数。</p>
<pre><code>    // 仅选择日期
    $(".form-date").datetimepicker(
        {
            language:  "zh-CN",
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            minView: 2,
            forceParse: 0,
            format: "yyyy-mm-dd"
        });
</code></pre>
<p>主要是根据 class 属性获取对象，然后调用 datetimepicker 方法进行一些初始化操作。</p>
<p>查看页面效果如下：</p>
<p><img src="http://images.gitbook.cn/cde7cf50-806a-11e8-9572-45e498171798" alt="" /></p>
<p>感觉还不错！因为我们是做 Java 后台的，页面效果这块肯定没有前端写的好，所以我们要学会利用一些前端框架，将一些组件和插件直接拿来使用。开发时间长了之后，慢慢的也会掌握一些前端开发技能。</p>
<h4 id="-4">保存个人信息</h4>
<p><strong>1.</strong> 首先看下 form 标签：</p>
<pre><code>       &lt;form id="userInfo_form" action="${ctx}/saveUserInfo" method="post"&gt;
</code></pre>
<p>action 对应的后台映射 URL 为 <code>saveUserInfo</code>，请求方式为 post 请求。</p>
<p><strong>2.</strong> 点击保存对应的点击事件如下：</p>
<pre><code>    function saveUserInfo() {
        $("#userInfo_form").submit();
    }
</code></pre>
<p>很简单，只有一行代码，就是获取 form 表单对象之后，调用它的 submit 方法进行提交表单。</p>
<p><strong>3.</strong> PersonalController.java 中创建映射 URL <code>saveUserInfo</code> 的方法：</p>
<pre><code>    @Autowired
    private UserInfoService userInfoService;
    @Autowired
    private UserService userService;
    @RequestMapping("/saveUserInfo")
    public String saveUserInfo(Model model, @RequestParam(value = "name",required = false) String name ,
                               @RequestParam(value = "nick_name",required = false) String nickName,
                               @RequestParam(value = "sex",required = false) String sex,
                               @RequestParam(value = "address",required = false) String address,
                               @RequestParam(value = "birthday",required = false) String birthday){
        User user = (User) getSession().getAttribute("user");
        if(user==null){
            return "../login";
        }
        UserInfo userInfo = userInfoService.findByUid(user.getId());
        boolean flag = false;
        if(userInfo == null){
            userInfo = new UserInfo();
        }else {
            flag = true;
        }
        userInfo.setName(name);
        userInfo.setAddress(address);
        userInfo.setSex(sex);
        Date bir =  DateUtils.StringToDate(birthday,"yyyy-MM-dd");
        userInfo.setBirthday(bir);
        userInfo.setuId(user.getId());
        if(!flag){
            userInfoService.add(userInfo);
        }else {
            userInfoService.update(userInfo);
        }

        user.setNickName(nickName);
        userService.update(user);

        model.addAttribute("user",user);
        model.addAttribute("userInfo",userInfo);
        return "personal/profile";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）首先从 Session 中取出 User，判断是否为空，如果为空，跳转到登录页面。</p>
<p>（2）User 不为空后，根据用户 id 查询出 UserInfo 信息，如果信息不存在，则 new 一个 UserInfo，默认 flag 为 flase，信息存在则 flag 置为 true。</p>
<p>（3）通过set方法将前台传来的参数封装到UserInfo对象中，如果flag 为 false，则代表是插入用户详细信息。如果 flag 为 true 则代表是更新用户详细信息。</p>
<p>（4）更新用户表的昵称信息。</p>
<p>（5）将 user 和 userInfo 对象添加到 model 中，然后返回到个人信息修改页面。</p>
<p>重新启动项目，填写个人信息保存后效果如图：</p>
<p><img src="http://images.gitbook.cn/4b4be080-806b-11e8-af1e-c555b432e64c" alt="" /></p>
<h3 id="-5">账号设置</h3>
<p>点击“账号设置”切换 tab 和改变右边信息这里就不说了，和上面的原理一样，页面效果如下：</p>
<p><img src="http://images.gitbook.cn/6a866a10-806b-11e8-b5ab-41e00ce48fd0" alt="" /></p>
<h4 id="-6">修改密码</h4>
<p>首先在 <code>WEB-INF/personal/</code> 目录下引入 repassword.jsp 和 passwordSuccess.jsp，分别是修改密码页面和密码修改成功页面。</p>
<p>修改密码对应的 a 标签：</p>
<pre><code>    &amp;nbsp;&amp;nbsp;&lt;a href="${ctx}/repassword"&gt;&lt;span id="password_span" style="color: grey" onmouseover="changeColor(this);" onmouseout="backColor(this);" &gt;修改&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p>其中，<code>&amp;nbsp;</code> 代表一个空格。onmouseover 鼠标悬浮改变字体颜色为紫色，onmouseout 鼠标移除时字体颜色变为灰色。</p>
<p>a 标签的 href 属性链接的 URL 为 <code>/repassword</code>，在 PersonalController 中创建与之对应的方法，如下：</p>
<pre><code>    @RequestMapping("/repassword")
    public String repassword(Model model) {
        User user = (User) getSession().getAttribute("user");
        if(user!=null) {
            model.addAttribute("user",user);
            return "personal/repassword";
        }
        return "../login";
    }
</code></pre>
<p>主要是从 Session 获取用户 User，判断如果不为空，则把 user 添加到 model 然后返回到修改密码页面，否则跳转到登录页面。</p>
<p>重新启动项目，进入个人信息修改页面，点击密码的“修改”进入修改密码页面，如下：</p>
<p><img src="http://images.gitbook.cn/0a5ab460-806c-11e8-b7a5-0d4f4dafcc53" alt="" /></p>
<p>需要对密码框做如下校验：</p>
<ol>
<li>密码长度不能小于6位；</li>
<li>旧密码和新密码不能一样；</li>
<li>新密码和确认密码输入必须一致。</li>
</ol>
<p><strong>1.</strong> 旧密码 input 框的离焦事件如下：</p>
<pre><code>    var f1 = false;
    function oldPassword() {
    var old =  $("#old_password").val();
    if(old==null || old.trim()==''){
       document.getElementById("old_span").innerHTML = "请输入密码！";
       f1 = false;
    }else if(old.length &lt; 6){
       document.getElementById("old_span").innerHTML = "密码长度少于6位，请重新输入！";
       f1 = false;
    }
    else {
       document.getElementById("old_span").innerHTML = "";
       f1 = true;
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）定义变量 f1 赋初始值为 false，表示该 input 框状态错误，不可提交表单。</p>
<p>（2）获取旧密码框输入的值，如果为空则提示请输入密码，如果密码长度低于6位则提示密码长度少于6位，请重新输入，f1 都为 false。</p>
<p>（3）否则清空 span 标签内内容，f1 置为true。</p>
<p><strong>2.</strong> 新密码 input 框的离焦事件如下：</p>
<pre><code>    var f2 = false;
    function newPassword() {
    var p = $("#password").val();
    var old =  $("#old_password").val();
    if(p==null || p.trim()==''){
        document.getElementById("old_span").innerHTML = "请输入密码！";
        f2 = false;
    }else if(p.length &lt; 6){

            $("#old_span").text("密码长度少于6位，请重新输入！").css("color","red");
            f2 =  false;

    }else if(p==old){
        $("#old_span").text("新密码与旧密码一致，请重新输入！").css("color","red");
        f2 = false;
    }

    else {
        document.getElementById("old_span").innerHTML = "";
        f2 = true
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）定义变量 f2 赋初始值为 false，表示该 input 框状态错误，不可提交表单。</p>
<p>（2）获取旧密码框和新密码框输入的值，如果新密码为空则提示请输入密码，如果新密码长度低于6位则提示密码长度少于6位，请重新输入，如果新密码和旧密码一致，则提示相应错误，f2 都为false。</p>
<p>（3）否则清空 span 标签内内容，f2 置为 true。</p>
<p><strong>3.</strong> 确认密码 input 框的离焦事件如下：</p>
<pre><code>     var f3 = false;
    function rePassword() {
        var p = $("#repassword").val();
        var p1 = $("#password").val();
        if(p==null || p.trim()==''){
            document.getElementById("old_span").innerHTML = "请输入密码！";
            f3 = false;
        }else if(p!=p1){
            document.getElementById("old_span").innerHTML = "两次密码不一致！";
            f3 = false;
        }
        else {
            document.getElementById("old_span").innerHTML = "";
            f3 = true
        }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）定义变量 f3 赋初始值为 false，表示该 input 框状态错误，不可提交表单。</p>
<p>（2）获取新密码框和确认密码框输入的值，如果确认密码为空则提示请输入密码，如果确认密码和新密码不一致，则提示相应错误，f3 都为 false。</p>
<p>（3）否则清空 span 标签内内容，f3 置为true。</p>
<p><strong>4.</strong> 提交表单</p>
<p>form 标签如下：</p>
<pre><code>     &lt;form action="${ctx}/updatePassword" method="post" id="update_password"&gt;
</code></pre>
<p>action 对应的请求 URL 为 <code>/updatePassword</code>，请求方式为 post 请求。</p>
<p>确认按钮的点击事件 surePost 方法如下：</p>
<pre><code>    function surePost() {
    if(f1 &amp;&amp; f2 &amp;&amp; f3){
        $("#update_password").submit();

    }else {
        $("#old_span").text("请重新输入密码！").css("color","red");
    }
    }
</code></pre>
<p>如果上面的校验都成功则提交表单，否则提示错误“请重新输入密码!”。</p>
<p>在 PersonalController 中创建映射 URL 为 <code>/updatePassword</code> 的方法如下：</p>
<pre><code>    @RequestMapping("/updatePassword")
    public String updatePassword(Model model, @RequestParam(value = "old_password",required = false) String oldPassword,
                                 @RequestParam(value = "password",required = false) String password){

        User user = (User) getSession().getAttribute("user");
        if(user!=null) {
                oldPassword = MD5Util.encodeToHex(Constants.SALT + oldPassword);
                if (user.getPassword().equals(oldPassword)) {
                    password = MD5Util.encodeToHex(Constants.SALT + password);
                    user.setPassword(password);
                    userService.update(user);
                    model.addAttribute("message", "success");
                } else {
                    model.addAttribute("message", "fail");
                }
        }
        model.addAttribute("user",user);
        return "personal/passwordSuccess";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 Session 获取用户 User。</p>
<p>（2）如果用户不为空，则根据旧密码进行 MD5 加密后与数据库中的密码进行比较，如果相同则说明密码输入正确，将新密码进行 MD5 加密后替换掉旧密码，然后更新用户信息，并将“success”添加到 model 中，如果不相同则说明密码输入错误，则将“fail”添加到 model 中。</p>
<p>（3）将 user 添加到 model 中，返回修改密码成功页面。</p>
<p>重启项目，修改密码，第一次输入错误密码，修改失败后效果如图：</p>
<p><img src="http://images.gitbook.cn/a76caa60-806c-11e8-b5ab-41e00ce48fd0" alt="" /></p>
<p>点击返回按钮，返回到修改密码页面。</p>
<p>第二次输入正确的密码，修改成功后效果如图：</p>
<p><img src="http://images.gitbook.cn/ba5f9650-806c-11e8-9572-45e498171798" alt="" /></p>
<p>点击重新登录（<code>/loginout</code>），即先退出登录然后返回到登录页面。</p>
<h4 id="-7">修改手机号</h4>
<p>修改手机号这里就不实现了，具体思路如下：</p>
<ol>
<li>点击手机号“修改”后首先进行密码确认或者手机验证码确认。</li>
<li>输入正确密码或者手机验证码后进入更换手机号页面。</li>
<li>输入手机号，手机号必须是非注册手机号，然后点击获取验证码，输入验证码正确则更换手机号成功！</li>
</ol>
<p>绑定设置，我们将在下一课中介绍。</p>
<blockquote>
  <p>第12课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1WnKCHBFewqEfqljVRU947Q 密码：wfmm</p>
</blockquote></div></article>