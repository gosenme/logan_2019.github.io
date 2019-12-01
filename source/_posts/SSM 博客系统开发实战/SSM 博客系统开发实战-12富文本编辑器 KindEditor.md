---
title: SSM 博客系统开发实战-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="kindeditor">富文本编辑器 KindEditor</h3>
<p>KindEditor 是一套开源的 HTML 可视化编辑器，可支持文字编辑、emoji 表情和图片上传等。主要用于让用户在网站上获得所见即所得编辑效果，兼容 IE、Firefox、Chrome、Safari、Opera 等主流浏览器。效果如图：</p>
<p><img src="http://images.gitbook.cn/bddab580-7e0a-11e8-bf76-9f4ed06c2591" alt="" /></p>
<h4 id="">准备</h4>
<p><strong>1.</strong> 在 WEB-INF 下新建文件夹 write，将与文章写作方面的 JSP 放入其中，引入 writedream.jsp 和 writesuccess.jsp 文件。</p>
<p><strong>2.</strong> 这里使用的是经过 ZUI 封装后的 KindEditor 富文本编辑器</p>
<p><img src="http://images.gitbook.cn/f1f99ac0-7e0a-11e8-be78-bb5c0f92d7f1" alt="" /></p>
<p>使用方法主要是引入 ZUI 框架下的 kindeditor.min.js：</p>
<pre><code>&lt;script src="${ctx}/css/zui/lib/kindeditor/kindeditor.min.js"&gt;&lt;/script&gt;
</code></pre>
<p>ZUI 框架文件之前已经给大家了，在 webapp/css下，如图：</p>
<p><img src="http://images.gitbook.cn/18d82a80-7e0b-11e8-be78-bb5c0f92d7f1" alt="" /></p>
<p>也可以去官网下载：</p>
<p><img src="http://images.gitbook.cn/2c450160-7e0b-11e8-be78-bb5c0f92d7f1" alt="" /></p>
<h4 id="-1">事件源</h4>
<p><strong>1.</strong> 通过点击个人主页导航栏的写梦或者是右侧的写文章小图标，都可进入写文章页面（writedream.jsp）：</p>
<p><img src="http://images.gitbook.cn/524c1ce0-7e0b-11e8-be78-bb5c0f92d7f1" alt="" /></p>
<pre><code class="      language-     ">&lt;li&gt;&lt;a href="${ctx}/writedream"&gt;写梦&lt;/a&gt;&lt;/li&gt;
</code></pre>
<p>因为 writedream.jsp  在 <code>WEB-INF</code> 目录下，受保护，不能直接访问，所以需要经过 Controller 层处理后跳转。</p>
<p><strong>2.</strong> 在 Controller 包下新建 WriteController 并继承 BaseController：</p>
<pre><code>    @Controller
    public class WriteController extends BaseController {
    private final static Logger log = Logger.getLogger(WriteController.class);
    @RequestMapping("/writedream")
    public String writedream(Model model) {
        User user = (User) getSession().getAttribute("user");
        model.addAttribute("user", user);
        return "writedream";
    }
    }
</code></pre>
<p>获取 Session 中的 user 信息，放入 model 中，返回 writedream.jsp 页面。</p>
<p><strong>3.</strong> 点击写梦进入 writedream.jsp 页面，效果如下：</p>
<p><img src="http://images.gitbook.cn/9ad049f0-8054-11e8-8e17-33d7842d205a" alt="" /></p>
<h4 id="-2">梦分类下拉框</h4>
<p>代码如下所示：</p>
<pre><code>     &lt;div style="margin-top: 20px;margin-left: 20px;position: absolute;"&gt;
        &lt;div class="dropdown dropdown-hover"&gt;
            &lt;button class="btn" type="button" data-toggle="dropdown" id="dream-diff" style="background-color:#EBEBEB"&gt;&lt;span id="fen" &gt;梦分类&lt;/span&gt; &lt;span class="caret"&gt;&lt;/span&gt;&lt;/button&gt;
            &lt;input id="hidden_cat" hidden="hidden" name="category"/&gt;
            &lt;ul class="dropdown-menu" id="dreamland-category"&gt;
                &lt;li&gt;&lt;a&gt;惊悚梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;爱情梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;武侠梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;美食梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;工作梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;动物梦&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a&gt;其他梦&lt;/a&gt;&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;
    &lt;/div&gt;
</code></pre>
<p>下拉框使用的是 ZUI 的 JS 插件，只要使用相应的 class 属性就能实现相应的效果。</p>
<p>通过点击 li 标签获取该 li 标签内的值，将其赋值给 id 为 fen 的 span 标签和 id 为 <code>hidden_cat</code> 的隐藏 input 标签，input 标签可通过 name 属性传给后台，li 标签的点击事件如下：</p>
<pre><code>     //li标签的点击事件
    $("#dreamland-category li").click(function(){//jquery的click事件
        var val = $(this).text();
        $("#fen").html(val);
        $("#hidden_cat").val(val);
    });
</code></pre>
<p>通过 <code>$("#dreamland-category li")</code> 获取 id 为 <code>dreamland-category</code> 的 ul 标签的所有 li 对象，click 为单击事件，</p>
<p><code>$(this)</code> 获取该 li 对象，通过 <code>.text()</code> 方法获取 li 标签内的文本，将其赋值给变量 val。</p>
<p>然后将id为fen的对象的文本设置为该li标签内的文本，主要是选择分类内容</p>
<p>将 val 赋值给 id 为 <code>hidden_cat</code> 的对象的 value 属性，主要是为了通过 name 属性传值给后台。</p>
<h4 id="-3">富文本编辑器的图片上传</h4>
<p><strong>1.</strong> 创建可视化编辑器的方法，如下所示：</p>
<pre><code>       $(function () {
       editor =  KindEditor.create('#content', {
           basePath: 'css/zui/lib/kindeditor/',
           uploadJson : '${ctx}/fileUpload',
           fileManagerJson : '${ctx}/fileManager',
           allowFileManager : true,
           bodyClass : 'article-content',
           items : ['source', '|', 'undo', 'redo', '|', 'preview', 'template', 'cut', 'copy', 'paste',
                                'plainpaste', 'wordpaste', '|', 'justifyleft', 'justifycenter', 'justifyright',
                                 'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
                                 'superscript', 'clearhtml', 'quickformat', 'selectall', '|', 'fullscreen', '/',
                                'formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
                                'italic', 'underline', 'strikethrough', 'lineheight', 'removeformat', '|', 'image','multiimage',
                                 'flash', 'media', 'insertfile', 'table', 'hr', 'emoticons', 'baidumap', 'pagebreak',
                                 'anchor', 'link', 'unlink']

       });

       KindEditor.sync();

    });
</code></pre>
<p>代码解读如下：</p>
<p>（1）<code>$(function(){})</code> 代表页面加载完成后执行的方法。</p>
<p>（2）KindEditor.create() 方法创建可视化编辑器。</p>
<p>（3）参数说明如下：</p>
<ul>
<li>basePath：指定 kindEditor 的路径。</li>
<li>uploadJson：指定上传文件的后台映射 URL 路径。</li>
<li>fileManagerJson：指定浏览远程图片的后台映射 URL 路径。</li>
<li>allowFileManager：true 表示显示浏览远程服务器按钮。</li>
<li>bodyClass：指定编辑器的 className。</li>
<li>items：配置编辑器的工具栏。</li>
</ul>
<p>（4）KindEditor.sync() 方法：同步 KindEditor 的值到 textarea 文本框，将编辑器的内容设置到原来的 textarea 控件里。</p>
<p><strong>2.</strong> Java 后台，在 controller 包下新建 UploadControlle.java，创建与 URL 为 <code>/fileUpload</code> 和 <code>/fileManager</code> 映射的方法，由于代码过长，这里就不粘贴了，之后我会将代码放在最下方的百度网盘中。</p>
<p><strong>3.</strong> 重启 Tomcat，进入 writedream.jsp 页面，然后点击上传图片，查看效果：</p>
<p><img src="http://images.gitbook.cn/978484e0-8055-11e8-8db6-0d16f8c01663" alt="" /></p>
<p>通过日志打印可看出图片存储路径。</p>
<p>上传图片，保存路径为：<code>D:\git\dreamland\dreamland-web\target\dreamland-web\images/</code>，文件 URL 为：<code>/images/</code>。</p>
<p>可进入该目录查看：</p>
<p><img src="http://images.gitbook.cn/c676f3a0-8055-11e8-bdd3-732bf4517f33" alt="" /></p>
<p>除了支持本地上传图片，还支持网络图片和服务器空间图片，如下图：</p>
<p><img src="http://images.gitbook.cn/d816d2b0-8055-11e8-af1e-c555b432e64c" alt="" /></p>
<p>还支持多图片上传，如图：</p>
<p><img src="http://images.gitbook.cn/e9586520-8055-11e8-8db6-0d16f8c01663" alt="" /></p>
<h4 id="-4">切换按钮和表单提交</h4>
<p><img src="http://images.gitbook.cn/f92a13e0-8055-11e8-9572-45e498171798" alt="" /></p>
<p><strong>1.</strong> 私密梦的切换按钮使用的是 ZUI 的开关控件。</p>
<p><img src="http://images.gitbook.cn/10caa960-8056-11e8-8db6-0d16f8c01663" alt="" /></p>
<p>使用方法很简单，只要引入 ZUI 框架的 JS 和 CSS 文件之后，将 div 的 class 属性设置为 switch 就可以了。</p>
<pre><code>     &lt;div class="switch" style="float: left;margin-top: 670px;margin-left: 20px;position: absolute"&gt;
        &lt;input type="checkbox" name="private_dream" id="private_dream" value="off"&gt;
        &lt;label&gt;私密梦&lt;/label&gt;
        &lt;span style="color: red"&gt;${error}&lt;/span&gt;
    &lt;/div&gt;
</code></pre>
<p>因为需要传值给后台，所以给 div 一个 name 属性，后台根据 name 属性，获取 value 属性的值，切换开关点击事件如下：</p>
<pre><code>    //私密梦开关点击事件
    $(".switch").click(function () {
    var pd = document.getElementById('private_dream');
    if(pd.checked == true){
        $("#private_dream").val("on");
    }else{
        $("#private_dream").val("off");
    }
    });
</code></pre>
<p>主要是根据 class 属性获取切换开关对象，开关对象的点击事件是 <code>click(function{});</code>。</p>
<p>然后根据元素 id 获取元素对象，如果该元素的 checked 属性等于 true，代表被选中状态，则将 on 赋值给该 inputk 框的 value 属性，否则将 off 赋值给 input 框的 value 属性。</p>
<p><strong>2.</strong> 返回按钮。</p>
<pre><code>    &lt;button class="btn btn-primary" id="go_back" type="button" &gt;返回&lt;/button&gt;
</code></pre>
<p>对应的点击事件：</p>
<pre><code>       $("#go_back").click(function () {
       location.href ="javascript:history.go(-1);"
    });
</code></pre>
<p>跳转到之前链接过来的地址。</p>
<p><strong>3.</strong>发表梦按钮。</p>
<p>即提交表单按钮，中间内容是一个大的 form 表单，包裹着文章分类、文章标题、富文本编辑器和私密梦部分。form 标签如下：</p>
<pre><code>    &lt;form id="write_form" name="w_form" role="w_form" class="writedream-form" action="doWritedream" method="post"&gt;
</code></pre>
<p>action 对应后台映射的 URL 原来：<code>/doWritedream</code>。</p>
<p>method 对应的是请求方式，这里是 post 请求。一般 post 请求是提交表单数据，而 get 请求一般是获取数据。</p>
<p>post 请求信息放在 header 中，相对较安全，没有长度限制。get 请求信息会出现在 URL 中，暴露请求信息，相对不安全，而且还有长度限制。</p>
<p>发表梦按钮 Button，如下代码所示：</p>
<pre><code>      &lt;button class="btn btn-primary"  type="button" id="sub_dream"&gt;发表梦&lt;/button&gt;
</code></pre>
<p>通过 id 获取 button 对象，其 click 点击事件如下：</p>
<pre><code>     //发表梦
    $("#sub_dream").click (function(){
      var val =  $("#fen").html();
       if(val.trim()=='梦分类'){
           alert("请选择梦分类！");
           return;
       }

       var tit = $("#txtTitle").val();
       if(tit == null || tit.trim() == ""){
           alert("请输入文章标题！");
           return;
       }
       editor.sync();
       var v1 = $("#content").val();
       if(v1 == null || v1.trim() == ""){
           alert("文章内容为空！");
           return;
       }
           $("#write_form").submit();

    });
</code></pre>
<p>代码解读如下：</p>
<p>（1）如果没有选择梦分类则提示其进行选择；</p>
<p>（2）如果文章标题为空，则提示输入文章标题；</p>
<p>（3）调用之前创建可视化编辑器返回的 editor，调用其 sync 方法，使编辑器内的文本同步到 Textarea 文本框。</p>
<p>（4）获取 Textarea 文本框内容赋值给 v1，如果文章内容为空则提示其输入内容。</p>
<p>（5）前面都没问题后，根据 form 表单的 id 获取 form 表单对象，调用其 submit 方法提交表单。</p>
<p>Java后台，由于插入文章需要返回主键 id，所以这里通用 mapper 方法已不能满足要求，需手写 XML。</p>
<p>（1）在 UserContentMapper 接口内新建方法 inserContent：</p>
<pre><code>     /**
     *  插入文章并返回主键id 返回类型只是影响行数  id在UserContent对象中
     * @param userContent
     * @return
     */
    int inserContent(UserContent userContent);
</code></pre>
<p>（2）在 <code>mapping/userContent.xml</code> 文件内写入对应的 SQL：</p>
<pre><code>    &lt;insert id="inserContent" parameterType="userContent" useGeneratedKeys="true" keyProperty="id"&gt;
        insert into user_content(id, u_id, title, category, content, personal,rpt_time ,img_url,nick_name,upvote,downvote,comment_num) values(#{id}, #{uId},#{title}, #{category},#{content},#{personal},#{rptTime}, #{imgUrl},#{nickName},#{upvote},#{downvote},#{commentNum})
    &lt;/insert&gt;
</code></pre>
<p>其中 inserContent 对应的是接口中的方法名，userContent 对应的是实体类别名，默认为 javabean 的首字母小写，<code>useGeneratedKeys="true"</code> 代表使用自增主键，<code>keyProperty="id"</code> 代表主键为 id，<code>user_content</code>为表名，插入语句的左侧为表中字段名，右侧 <code>#{}</code> 中为实体类中的属性名。</p>
<p>（3）UserContentService 接口中 addContent 方法修改如下：</p>
<pre><code>    /**
     * 添加文章
     * @param content
     */
    int addContent(UserContent content);
</code></pre>
<p>（4）UserContentServiceImpl 实现类中 addContent 方法修改如下：</p>
<pre><code>     public int addContent(UserContent content) {
       return userContentMapper.inserContent(content);
    }
</code></pre>
<p>WriteController 内创建映射 URL 为 <code>/doWritedream</code> 的方法：</p>
<pre><code>    @Autowired
    private UserContentService userContentService;
    @RequestMapping("/doWritedream")
    public String doWritedream(Model model, @RequestParam(value = "id",required = false) String id,
                               @RequestParam(value = "category",required = false) String category,
                               @RequestParam(value = "txtT_itle",required = false) String txtT_itle,
                               @RequestParam(value = "content",required = false) String content,
                               @RequestParam(value = "private_dream",required = false) String private_dream) {
        log.info( "进入写梦Controller" );
        User user = (User)getSession().getAttribute("user");
        if(user == null){
            //未登录
            model.addAttribute( "error","请先登录！" );
            return "../login";
        }
        UserContent userContent = new UserContent();
        userContent.setCategory( category );
        userContent.setContent( content );
        userContent.setRptTime( new Date(  ) );
        String imgUrl = user.getImgUrl();
        if(StringUtils.isBlank( imgUrl )){
            userContent.setImgUrl( "/images/icon_m.jpg" );
        }else {
            userContent.setImgUrl( imgUrl );
        }
        if("on".equals( private_dream )){
            userContent.setPersonal( "1" );
        }else{
            userContent.setPersonal( "0" );
        }
        userContent.setTitle( txtT_itle );
        userContent.setuId( user.getId() );
        userContent.setNickName( user.getNickName() );

        userContent.setUpvote( 0 );
        userContent.setDownvote( 0 );
        userContent.setCommentNum( 0 );
        userContentService.addContent( userContent );
        model.addAttribute("content",userContent);
        return "write/writesuccess";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 Autowired 注解注入 UserContentService 对象。</p>
<p>（2）通过 RequestMapping 注解映射到 URL：<code>/doWritedream</code>。</p>
<p>（3）通过 RequestParam 注解接收前台传来的参数，通过 value 属性接收，<code>required = false</code> 代表非必须，没有这个值也可以</p>
<p>（4）从 Session 获取用户信息，判断其是否登录，未登录则跳转到登录页面。</p>
<p>（5）创建对象 UserContent，将从前台接收的参数，通过 set 方法设置参数，如果没有个人头像，则设置默认头像，如果私密梦开关为 on 则代表是私密文章，将其 personal 属性设置为 1，否则设置为 0，初始化点赞数、踩数和评论数都为 0。</p>
<p>（6）调用 UserContentService 对象的 addContent 方法，将文章对象插入数据库。</p>
<p>（7）将含有主键 id 的 UserContent 对象添加到 model 中。</p>
<p>（8）跳转到写文章成功页面 writesuccess.jsp。</p>
<h4 id="-5">查看文章、编辑文章和删除文章</h4>
<p>写文章成功页面如图：</p>
<p><img src="http://images.gitbook.cn/9b650880-8057-11e8-9572-45e498171798" alt="" /></p>
<p>很简单，三个按钮对应的点击事件分别是：</p>
<h5 id="-6"><strong>写新梦：</strong></h5>
<pre><code>     //写新梦
    $("#new-dreamland").click(function () {
        location.href ="${ctx}/writedream"
    });
</code></pre>
<p>经过后台 Controller 处理后跳转到写文章页面。</p>
<h5 id="-7"><strong>管理梦：</strong></h5>
<pre><code>     //管理梦
    $("#manage-dreamland").click(function () {
        location.href ="${ctx}/list?manage=manage"
    });
</code></pre>
<p>这里需要对 personal.jsp 和 PersonalController.java 文件做下修改，判断如果 manage 有值的话默认“管理梦”标签被选中。</p>
<p>（1）PersonalController.java 加上以下代码：</p>
<pre><code>@RequestParam(value = "manage",required = false) String manage 
</code></pre>
<p>上面 RequestParam 注解用于接收 manage 的值：</p>
<pre><code>     if(StringUtils.isNotBlank(manage)){
            model.addAttribute("manage",manage);
      }
</code></pre>
<p>判断如果 manage 不为空，则将 manage 放入 model 中，一起返回给 personal.jsp 页面。</p>
<p>（2）personal.jsp 页面加上以下代码：</p>
<pre><code>      $(function () {
       var val = "${manage}";
       if(val=="manage"){
           manage_dreamland();
       }
    });
</code></pre>
<p>页面加载完成方法，通过 EL 表达式 <code>${manage}</code> 获取后台传过来的 manage 的值，如果 manage 的值为 manage 的话，则调用点击“管理梦”的方法，使管理梦默认为选中。</p>
<h5 id="-8"><strong>查看梦：</strong></h5>
<pre><code>     //查看梦
    $("#watch-dreamland").click(function () {
        location.href ="${ctx}/watch?cid=${content.id}"
    });
</code></pre>
<p>查看梦点击事件，将文章 id 作为参数传递给后台。</p>
<p>在 WriteController 中新建映射 URL 为 <code>/watch</code> 的方法：</p>
<pre><code>    /**
     * 根据文章id查看文章
     * @param model
     * @param cid
     * @return
     */
    @RequestMapping("/watch")
    public String watchContent(Model model, @RequestParam(value = "cid",required = false) Long cid){
        User user = (User)getSession().getAttribute("user");
        if(user == null){
            //未登录
            model.addAttribute( "error","请先登录！" );
            return "../login";
        }
        UserContent userContent = userContentService.findById(cid);
        model.addAttribute("cont",userContent);
        return "personal/watch";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 获取用户信息，首先判断登陆，未登录则跳转到登陆页面。</p>
<p>（2）根据文章 id 查询文章对象 UserContent，将其放入 model。</p>
<p>（3）跳转到 <code>/personal/watch.jsp</code> 查看文章页面。</p>
<p>效果如图：</p>
<p><img src="http://images.gitbook.cn/e140d870-805c-11e8-bdd3-732bf4517f33" alt="" /></p>
<p>为个人主页的所有标题、修改和删除添加 a 标签，并添加 href 属性，如图：</p>
<p><img src="http://images.gitbook.cn/f46e5c60-805c-11e8-b887-ad9ea87ef533" alt="" /></p>
<p>修改的代码如下：</p>
<pre><code>     &lt;a href="${ctx}/watch?cid=${cont.id}"&gt;${cont.title}&lt;/a&gt;
     &lt;a href="${ctx}/deleteContent?cid=${cont.id}"&gt;&lt;span class="bar-delete"&gt;删除&lt;/span&gt;&lt;/a&gt;
     &lt;a href="${ctx}/writedream?cid=${cont.id}"&gt;&lt;span class="bar-update"&gt;修改&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p>为 AJAX 回调函数拼接的标题、修改和删除添加 a 标签和 href，如下：</p>
<pre><code>    &lt;a href='${ctx}/watch?cid="+this.id+"'&gt;"+this.title+"&lt;/a&gt;&lt;a href='${ctx}/deleteContent?cid="+this.id+"'&gt;&lt;span class='bar-delete'&gt;删除&lt;/span&gt;&lt;/a&gt;"+"&lt;a href='${ctx}/writedream?cid="+this.id+"'&gt;&lt;span class='bar-update'&gt;修改&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p>这样点击标题也能查看文章了。</p>
<h4 id="-9">编辑文章</h4>
<p><strong>1.</strong> 事件源</p>
<p>点击上面的编辑或者个人主页的修改，对应的点击事件如下。</p>
<p>点击编辑对应的代码，如下：</p>
<pre><code>     &lt;c:if test="${cont.uId == user.id}"&gt;
        &lt;div class="update-dream"&gt;
            &lt;a href="${ctx}/writedream?cid=${cont.id}"&gt;&lt;span style="color: #9370db;font-size: 14px"&gt;编辑&lt;/span&gt; &lt;/a&gt;
        &lt;/div&gt;
        &lt;/c:if&gt;
</code></pre>
<p>如果不是文章作者本人，只能查看文章不可编辑，所以只有是文章作者才显示编辑。这里用一个 <code>c:if</code> 做下判断。</p>
<p>点击修改对应的代码，如下：</p>
<pre><code>     &lt;a href="${ctx}/writedream?cid=${cont.id}"&gt;&lt;span class="bar-update"&gt;修改&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p><strong>2.</strong> Java 后台</p>
<p>此时需要对 WriteController 的映射方法做下修改，让它接收一个 cid 的参数，修改如下：</p>
<pre><code>    /**
     * 进入writedream
     * @param model
     * @return
     */
    @RequestMapping("/writedream")
    public String writedream(Model model,@RequestParam(value = "cid",required = false) Long cid) {
        User user = (User) getSession().getAttribute("user");
        if(cid!=null){
            UserContent content = userContentService.findById(cid);
            model.addAttribute("cont",content);
        }
        model.addAttribute("user", user);
        return "write/writedream";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）查询用户信息，存入 model。</p>
<p>（2）判断文章 id 是否为 null，不为 null，则根据文章 id 查询文章对象，放入 model，代表修改文章，否则就是写文章。</p>
<p>（3）返回到 writedream.jsp。</p>
<p><strong>3.</strong> writedream.jsp 页面回显内容</p>
<p>（1）梦分类回显，代码如下：</p>
<pre><code>       &lt;c:if test="${cont.category != null}"&gt;
          ${cont.category}
        &lt;/c:if&gt;
       &lt;c:if test="${cont.category == '' || cont.category == null}"&gt;
          梦分类
       &lt;/c:if&gt;

       &lt;/span&gt; &lt;span class="caret"&gt;&lt;/span&gt;&lt;/button&gt;
       &lt;input id="hidden_cat" hidden="hidden" name="category" value="${cont.category}"/&gt;
</code></pre>
<p>用 <code>c:if</code> 标签判断：如果从后台取出的分类名称不为空，则将该分类名称进行回显，否则使用默认的“梦分类”。</p>
<p>然后在 input 隐藏标签的 value 属性上用 EL 表达式获取后台传过来的分类名称，如果用户不切换，则直接将这个值再次传递给后台。</p>
<p>（2）文章标题回显，代码如下：</p>
<pre><code>     &lt;input type="text" id="txtTitle" name="txtT_itle" value="${cont.title}" class="input-file-title" maxlength="100" placeholder="&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;输入文章标题"  style="height: 33px;width: 1080px;background-color:#EBEBEB;border: 0px" &gt;
</code></pre>
<p>直接在 input 框的 value 属性上用 EL 表达式进行回显：</p>
<pre><code>    value="${cont.title}" 
</code></pre>
<p>（3）文章内容回显，代码如下：</p>
<pre><code>      &lt;textarea id="content" name="content" class="form-control kindeditor" style="height:600px;width: 1170px"&gt;${cont.content}&lt;/textarea&gt;
</code></pre>
<p>直接在 textarea 的标签内用 EL 表达式获取。</p>
<p>（4）私密梦开关回显，代码如下：</p>
<pre><code>    //私密开关回显
    $(function () {
       var v = '${cont.personal}';
       if(v == "1"){
           var pd = document.getElementById('private_dream');
           pd.checked = true;
       }
    });
</code></pre>
<p>通过 EL 表达式 <code>${cont.personal}</code> 取出 personal 的值，判断 personal 是否为 1，是则代表是私密梦。</p>
<p>然后根据 id 获取元素对象，然后将其 checked 属性设置为 true，代表被选中。</p>
<p>查看回显效果：</p>
<p><img src="http://images.gitbook.cn/bbde2100-8061-11e8-9304-6379ade2eaf9" alt="" /></p>
<p>点击发表梦提交时，需要对 form 表单的 action 做下修改，将文章 id 传递给后台：</p>
<pre><code>    &lt;form id="write_form" name="w_form" role="w_form" class="writedream-form" action="doWritedream?cid=${cont.id}" method="post"&gt;
</code></pre>
<p>其中 cid 应该放在 input 隐藏域中上传，即将 input 标签的 hidden 属性设置为 hidden，页面上不会显示 input 框，用于传值，如下：</p>
<pre><code>    &lt;input hidden="hidden" name="cid" value="${cont.cid}"/&gt;
</code></pre>
<p>放在隐藏域中更安全，随 form 表单一起提交，地址栏中不会出现类似 <code>localhost:8080/doWritedream?cid=1</code> 情况，这样用户很容易修改 cid 的值。我这里为了做演示就使用了第一种形式。</p>
<p><strong>4.</strong> Java后台</p>
<p>进入后台 Controller，需要对 WriteController 的 doWritedream 方法做下修改，使其能够判断文章 id 是否为空做插入或修改操作：</p>
<pre><code>    @RequestMapping("/doWritedream")
    public String doWritedream(Model model, @RequestParam(value = "id",required = false) String id,
                               @RequestParam(value = "cid",required = false) Long cid,
                               @RequestParam(value = "category",required = false) String category,
                               @RequestParam(value = "txtT_itle",required = false) String txtT_itle,
                               @RequestParam(value = "content",required = false) String content,
                               @RequestParam(value = "private_dream",required = false) String private_dream) {
        log.info( "进入写梦Controller" );
        User user = (User)getSession().getAttribute("user");
        if(user == null){
            //未登录
            model.addAttribute( "error","请先登录！" );
            return "../login";
        }
        UserContent userContent = new UserContent();
        if(cid!=null){
            userContent = userContentService.findById(cid);
        }
        userContent.setCategory( category );
        userContent.setContent( content );
        userContent.setRptTime( new Date(  ) );
        String imgUrl = user.getImgUrl();
        if(StringUtils.isBlank( imgUrl )){
            userContent.setImgUrl( "/images/icon_m.jpg" );
        }else {
            userContent.setImgUrl( imgUrl );
        }
        if("on".equals( private_dream )){
            userContent.setPersonal( "1" );
        }else{
            userContent.setPersonal( "0" );
        }
        userContent.setTitle( txtT_itle );
        userContent.setuId( user.getId() );
        userContent.setNickName( user.getNickName() );

        if(cid ==null){
            userContent.setUpvote( 0 );
            userContent.setDownvote( 0 );
            userContent.setCommentNum( 0 );
            userContentService.addContent( userContent );
        }else {
            userContentService.updateById(userContent);
        }
        model.addAttribute("content",userContent);
        return "write/writesuccess";
    }
</code></pre>
<p>代码解读如下:</p>
<p>（1）从 Session 获取用户信息，判断其是否登录，未登录则跳转到登录页面。</p>
<p>（2）创建对象 UserContent，并判断前台传过来的文章 id（即 cid）是否为空，不为空则根据文章 id 查询出文章对象，赋值给 userContent。</p>
<p>（3）设置从前台传过来的参数，判断从前台传过来的 cid 是否为 null，为 null，则代表是插入操作，将点赞数、踩数和评论数初始化为0，然后插入到数据库中。</p>
<p>（4）如果从前台传过来的 cid 不为 null，则代表是修改操作，根据文章 id 进行修改，调用 updateById 方法。</p>
<p>（5）调用 UserContentService 对象的 addContent 方法，将文章对象插入数据库。</p>
<p>（6）将 UserContent 对象添加到 model 中。</p>
<p>（7）跳转到写文章成功页面 writesuccess.jsp。</p>
<p>这样编辑文章就完成了！重新启动项目，自己测试下。</p>
<h4 id="-10">删除文章</h4>
<p><strong>1.</strong> 事件源</p>
<p>点击个人主页的删除，对应的点击事件如下：</p>
<pre><code>      &lt;a href="${ctx}/deleteContent?cid=${cont.id}"&gt;&lt;span class="bar-delete"&gt;删除&lt;/span&gt;&lt;/a&gt;
</code></pre>
<p><strong>2.</strong> Java 后台</p>
<p>因为之前设计接口时失误，没有设计删除文章的方法，这里补充这个接口方法，在 UserContentService 接口中定义删除方法：</p>
<pre><code>    /**
     * 根据文章id删除文章
     * @param cid
     */
    void deleteById(Long cid);
</code></pre>
<p>在实现类 UserContentServiceImpl 中实现这个方法：</p>
<pre><code>    @Override
    public void deleteById(Long cid) {
       userContentMapper.deleteByPrimaryKey(cid);
    }
</code></pre>
<p>然后在 PersonalController 中创建映射 URL 为：<code>/deleteContent</code> 的方法（其中根据文章 id 删除 Upvote 和 Comment 自己实现下）：</p>
<pre><code class="     language-    ">    @Autowired
    private CommentService commentService;

    @Autowired
    private UpvoteService upvoteService;
    @RequestMapping("/deleteContent")
    public String deleteContent(Model model, @RequestParam(value = "cid",required = false) Long cid) {

        User user = (User)getSession().getAttribute("user");
        if(user==null) {
            return "../login";
        }
        commentService.deleteByContentId(cid);
        upvoteService.deleteByContentId(cid);
        userContentService.deleteById(cid);
        return "redirect:/list?manage=manage";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）判断用户是否登录，未登录则跳转登录页面。</p>
<p>（2）因为存在外键关系，删除文章之前先将 upvote 和 comment 表中与此文章 id 相关数据删除。</p>
<p>（3）根据文章 id 删除文章。</p>
<p>（4）重定向到映射 URL 为：<code>/list</code> 的方法，刷新个人主页数据，参数 manage=manage 主要是为了返回个人主页时切换到“管理梦”选项卡。</p>
<p>如果想判断是从“管理梦”还是“私密梦”点击删除，然后返回个人主页时，切换到对应的选项卡，则只需要增加一个判断条件即可，自己可以尝试下。</p>
<p>重新启动项目，测试删除功能成功！</p>
<h4 id="-11">发现</h4>
<p>最后访问首页和个人主页的时候发现三个问题：</p>
<p><strong>1.</strong> 最新发布的文章在最后，而且上面没有显示发布时间。</p>
<p><strong>2.</strong> 分页的页码没有上限，如图：</p>
<p><img src="http://images.gitbook.cn/c027e330-8062-11e8-af1e-c555b432e64c" alt="" /></p>
<p><strong>3.</strong> 分类列表的长度是固定的，列表内容过长会被隐藏，如图：</p>
<p><img src="http://images.gitbook.cn/d61152d0-8062-11e8-b887-ad9ea87ef533" alt="" /></p>
<p>代码解读如下：</p>
<p><strong>1.</strong> 第一个问题将查询结果按时间倒排序就可以了，有两个地方需要修改：</p>
<p>（1）进入首页之前的自定义过滤器，在 <code>wang.dreamland.www.interceptor.IndexJspFilter</code> 中：</p>
<pre><code>     public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        System.out.println("===========自定义过滤器==========");
        ServletContext context = request.getServletContext();
        ApplicationContext ctx = WebApplicationContextUtils.getWebApplicationContext(context);
        UserContentMapper userContentMapper = ctx.getBean(UserContentMapper.class);
        PageHelper.startPage(null, null);//开始分页
        Example e = new Example(UserContent.class);
        e.setOrderByClause("rpt_time DESC");
        List&lt;UserContent&gt; list = userContentMapper.selectByExample(e);
        PageHelper.Page endPage = PageHelper.endPage();//分页结束
        request.setAttribute("page", endPage );
        chain.doFilter(request, response);
    }
</code></pre>
<p>主要增加了根据上传时间倒排序的条件：</p>
<p>通过 Example 的有参构造获取 Example 对象，参数就是你要操作的对象的 class 文件，通过 <code>e.setOrderByClause("rpt_time DESC")</code> 设置排序的字段和排序规则，如果不写，默认是 ASC 升序的。</p>
<p>然后通过 <code>userContentMapper.selectByExample(e)</code> 方法将查询条件 example 对象传入即可实现根据发布时间倒排序。</p>
<p>（2）用户登录后进入个人主页，然后点击首页访问时，会进入 IndexJspController 的映射 URL 为 <code>/index_list</code> 的方法，然后会调用  findAll 方法，所以将 findAll 方法做下修改，只接受两个参数：</p>
<pre><code>      Page&lt;UserContent&gt; page =  findAll(pageNum,pageSize);
</code></pre>
<p>会报错，没有这个方法，然后在 BaseController 增加方法：</p>
<pre><code>      public Page&lt;UserContent&gt; findAll(Integer pageNum, Integer pageSize){
        Page&lt;UserContent&gt; page = userContentService.findAll(pageNum ,pageSize);
        return page;
    }
</code></pre>
<p>接着报错 userContentService 没有这个方法，在 wang.dreamland.www.service.UserContentService 增加如下方法：</p>
<pre><code>     /**
     * 根据发布时间倒排序并分页
     * @param pageNum
     * @param pageSize
     * @return
     */
    PageHelper.Page&lt;UserContent&gt; findAll(Integer pageNum, Integer pageSize);
</code></pre>
<p>然后在 wang.dreamland.www.service.impl.UserContentServiceImpl 实现刚才创建的方法：</p>
<pre><code>     @Override
    public Page&lt;UserContent&gt; findAll(Integer pageNum, Integer pageSize) {
        //分页查询
        PageHelper.startPage(pageNum, pageSize);//开始分页
        Example e = new Example(UserContent.class);
        e.setOrderByClause("rpt_time DESC");
        List&lt;UserContent&gt; list =  userContentMapper.selectByExample(e);
        Page endPage = PageHelper.endPage();//分页结束
        return endPage;
    }
</code></pre>
<p>实现倒排序的原理和第一点一样。这里不再赘述。</p>
<p>接下来，我们看显示发布时间如何实现。</p>
<p>（1）在 UserContent 实体类中创建日期格式化方法，如果不格式化日期，在页面上显示的是格林威治时间（GMT），如图：</p>
<p><img src="http://images.gitbook.cn/88070840-8063-11e8-b7a5-0d4f4dafcc53" alt="" /></p>
<p>格式化日期方法，如下：</p>
<pre><code>    @Transient
    public String getFormatDate(){
        return DateUtils.formatDate(getRptTime(),"yyyy-MM-dd HH:mm:ss");
    }
</code></pre>
<p>EL 表达式取值就是根据实体属性的 get 方法取值的，所以在页面上只要用 <code>${对象.formatDate}</code> 即可获取格式化后的日期。</p>
<p>其中 formatDate 方法是将日期 Date 根据指定格式转换成日期字符串，在 common 包下的 DateUtils 中创建该方法：</p>
<pre><code>    /**
     * 将日期根据指定根式转成字符串
     * @param date
     * @param format
     * @return
     */
    public static String formatDate(Date date,String format){
        if(date == null){
            return null;
        }
        SimpleDateFormat formatter = new SimpleDateFormat(format);
        String dateString = formatter.format(date);
        return dateString;
    }
</code></pre>
<p>（2）index.jsp 页面做如下修改：</p>
<pre><code>     &lt;div class="author-h2"&gt;
          &lt;div style="float: left;font-size: 15px;color: #9b8878"&gt;
               ${cont.nickName}
           &lt;/div&gt;
           &lt;div style="float: left;margin-left: 10px;color: grey;margin-top: 2px;font-size: 12px"&gt;
                 ${cont.formatDate}
            &lt;/div&gt;
    &lt;/div&gt;
</code></pre>
<p>通过 <code>${cont.formatDate}</code> 获取格式化后的日期，其他主要是一些样式的设置。float 属性是将 div 浮动，margin-left 是距离左边 div 距离，margin-top 是指距离顶部 div 距离。</p>
<p>重启项目后，查看效果如下：</p>
<p><img src="http://images.gitbook.cn/c3435e90-8063-11e8-b887-ad9ea87ef533" alt="" /></p>
<p><strong>2.</strong> 分页的问题，我们需要优化分页工具 PageHelper，使得页码数为10，即前四后五的效果。待会完成后查看效果。</p>
<p>关键是确定开始页码和结束页码，主要增加了一下内容：</p>
<pre><code>    private int startPage;//开始页码（按钮上的数字）
        private int endPage;//结束页码（按钮上的数字）

        public int getStartPage() {
            return startPage;
        }

        public void setStartPage(int startPage) {
            this.startPage = startPage;
        }

        public int getEndPage() {
            return endPage;
        }

        public void setEndPage(int endPage) {
            this.endPage = endPage;
        }
        public void setTotal(long total) {
            //计算总页码数：
            int totalCount = Integer.parseInt(total+"");
            pages=(totalCount+pageSize-1)/pageSize;
            //计算页面的页码中“显示”的起始页码和结束页码
            //一般显示的页码较好的效果是最多显示10个页码
            //算法是前5后4，不足补10
            //计算显示的起始页码（根据当前页码计算）：当前页码-5
            startPage = pageNum - 5;
            if(startPage &lt; 1){
                startPage = 1;//页码修复
            }

            //计算显示的结束页码（根据开始页码计算）：开始页码+9
            endPage = startPage + 9;
            if(endPage &gt; pages){//页码修复
                endPage = pages;
            }

            //起始页面重新计算（根据结束页码计算）：结束页码-9
            startPage = endPage - 9;
            if(startPage &lt; 1){
                startPage = 1;//页码修复
            }

            System.out.println(startPage +"和" +endPage);

            this.total = total;
        }
</code></pre>
<p>代码解读如下：</p>
<p>（1）增加两个属性，分别是开始页码和结束页码，然后生成 setter 和 getter 方法。</p>
<p>（2）计算总页码数，<code>pages=(totalCount+pageSize-1)/pageSize</code>。</p>
<p>主要考虑 pageSize 为1的情况，所以减去1，然后除以每页记录数取整数。</p>
<p>比如：</p>
<blockquote>
  <p>（总记录数为18+每页显示记录数5-1）/5 = 4</p>
  <p>（总记录数为18+每页显示记录数1-1)/1 = 18 </p>
</blockquote>
<p>如果不减去1总页数就是21页了.</p>
<p>（3）根据前四后五原则，起始页码 = 当前页面 -5，如果起始页码&lt;1，则赋值为1。</p>
<p>（4）结束页码 = 开始页码 + 9 ，如果结束页码 &gt; 总页码数，则将总页码数赋值给结束页码.</p>
<p>（5）确保正确，起始页码再次计算：起始页码 = 结束页码 - 9，如果起始页码小于1，则赋值为1。</p>
<p>（6）将 total 赋值给 this.total。</p>
<p>主要是在 setTotal 方法中做了计算开始页码和结束页码的操作。</p>
<p>然后回到 index.jsp 页面，将原来的从1开始改为 startPage，将原来的以 pages 结束改为 endPage，如下：</p>
<pre><code>       &lt;c:forEach begin="${page.startPage}" end="${page.endPage}" var="pn"&gt;
                        &lt;c:if test="${page.pageNum==pn}"&gt;
                            &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                        &lt;c:if test="${page.pageNum!=pn}"&gt;
                            &lt;li &gt;&lt;a href="${ctx}/index_list?pageNum=${pn}&amp;&amp;id=${user.id}"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
         &lt;/c:forEach&gt;
</code></pre>
<p>除了 index.jsp 页面需要修改，其他需要分页的页面都修改一下，比如 personal.jsp，其他的自行修改一下。修改后效果如下图：</p>
<p><img src="http://images.gitbook.cn/7fff1ab0-8064-11e8-9304-6379ade2eaf9" alt="" /></p>
<p><strong>3.</strong> 让梦分类的列表长度随着分类数量变化而变化。</p>
<p>思路是：分类数量越多，长度越长，下面“关注”div 标签距离顶部 div 的距离越大，反之越小。</p>
<p>获取“关注”div 标签的 margin-top 的值，然后根据分类数量的变化而变化。</p>
<p>实现步骤如下：</p>
<p>（1）首先给“关注”div 标签加上 id 和初始 margin-top 的值，如下：</p>
<pre><code>     &lt;div class="dreamland-see" id="dreamland-see" style="margin-top: 510px"&gt;
</code></pre>
<p>注意：虽然 head 标签内的 style 标签已定义了 margin-top 的值，但是它是页面加载完成后才渲染，所以页面加载完成函数是获取不到 margin-top 的值的，可以自己加打印试一下。</p>
<p>（2）将页面加载完成函数修改如下：</p>
<pre><code>    //页面加载完成函数
    $(function () {
        var num = "${categorys.size()}";
        var tomVal = document.getElementById("dreamland-see").style.marginTop;
        var hgt = parseInt(num)*40+parseInt(tomVal.split("px")[0]);
        document.getElementById("dreamland-see").style.marginTop = hgt + "px";

       var val = "${manage}";
       if(val=="manage"){
           manage_dreamland();
       }
    });
</code></pre>
<p>代码解读如下：</p>
<p>（1）将后台传来的集合的长度赋值给 num。</p>
<p>（2）获取“关注” div 的 margin-top 的值，赋值给 tomVal。</p>
<p>（3）每一个列表的长度为40px，所以将列表数量 <code>num*40</code>，然后加上“关注”div 的 margin-top 的初始值，因为获取到的 <code>tomval = 510px</code>，所以要对其进行切割，得到数字510，将相加之和赋值给hgt。</p>
<p>（4）最后将 <code>hgt+"px"</code>重新赋值给“关注”div 的 margin-top 属性。</p>
<p>之后的代码前面已经说过，不再赘述！</p>
<p>刷新页面效果如下：</p>
<p><img src="http://images.gitbook.cn/0a9b6b10-8065-11e8-9304-6379ade2eaf9" alt="" /></p>
<p>希望大家能够接受我这种：设置问题 -&gt; 发现问题 -&gt;解决问题的讲解方式。</p>
<blockquote>
  <p>第11课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1mQLBznQNsXcg6dD8JD8Mmw 密码：9av9</p>
</blockquote></div></article>