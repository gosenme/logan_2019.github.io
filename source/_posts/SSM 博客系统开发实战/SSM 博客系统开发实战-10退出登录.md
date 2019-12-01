---
title: SSM 博客系统开发实战-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">退出登录</h3>
<p>我们首先写出退出登录的 a 标签，代码如下：</p>
<pre><code>&lt;a name="tj_login" class="lb" href="${ctx}/loginout" style="color: black"&gt;[退出]&lt;/a&gt;
</code></pre>
<p>之后，在 Java 后台，LoginController.java 内创建映射 URL 为<code>/loginout</code> 的方法，如下：</p>
<pre><code>    @RequestMapping("/loginout")
    public String exit(Model model) {
        log.info( "退出登录" );
        getSession().removeAttribute( "user" );
        getSession().invalidate();
        return "../login";
    }
</code></pre>
<p>代码很简单，主要是将存储在 Session 内的用户信息移除。</p>
<p>getSession().invalidate() 使 Session 失效，释放资源。</p>
<h3 id="-1">点赞、踩</h3>
<p>点赞、踩的流程图如下所示：</p>
<p><img src="http://images.gitbook.cn/8535a490-75f6-11e8-b9a0-850e12cc69e8" alt="" /></p>
<p><img src="http://images.gitbook.cn/98df3650-75f6-11e8-b9a0-850e12cc69e8" alt="" /></p>
<h4 id="javascript">JavaScript 代码</h4>
<p>我们首先在前端页面写出点赞 a 标签，代码如下：</p>
<pre><code>     &lt;a style="cursor: pointer;" onclick="upvote_click(${cont.id},1);"&gt;
         &lt;i class="icon icon-thumbs-o-up icon-2x"&gt;&lt;/i&gt;
         &lt;span class="number hidden" id="up_${cont.id}"&gt;${cont.upvote}&lt;/span&gt;
     &lt;/a&gt;
</code></pre>
<p>对应的点击事件 <code>upvote_click</code> 如下：</p>
<pre><code>    //点赞或踩
    function upvote_click(id,cont) {

        $.ajax({
            type:'post',
               url:'/upvote',
            data: {"id":id,"uid":'${user.id}',"upvote":cont},
            dataType:'json',
            success:function(data){
               var up =  data["data"];
               /*alert(up);*/
               if(up == "success"){
                   if (cont == -1){
                       var down = document.getElementById("down_"+id);
                       var num = down.innerHTML;
                       var value = parseInt(num) + cont;
                       down.innerHTML = value;
                   } else {
                       var num = document.getElementById(id).innerHTML;
                       var value = parseInt(num) + cont;
                       document.getElementById(id).innerHTML = value;
                       document.getElementById("up_"+id).innerHTML = value;
                   }
               }else if(up == "done"){
                    alert("已点赞！")

               }else if(up == "down"){
                   alert("已踩！")
               } else {
                   window.location.href = "/login.jsp";
               }
            }
        });
    }
</code></pre>
<p>代码解析：</p>
<p>（1）<code>upvote_click</code> 函数接收两个参数：（1）文章 id；（2）常量1（赞）或者-1（踩）。</p>
<p>（2）发起 AJAX 请求，请求类型为 POST 请求，请求 URL 为 <code>/upvote</code>，请求参数为文章 id、用户 id、1或者-1，返回 JSON 类型数据。</p>
<p>（3）success 回调函数返回 JSON 类型数据，取出 data 中的数据赋值给 up，如果为“success”，cont为-1说明是踩，则将踩的数量+1，否则 cont 为1则将赞的数量+1。</p>
<p>（4）如果 up 为“done”则提示已点赞，如果为“down”则为已踩，否则跳转到登录页面。</p>
<h4 id="-2">后台代码</h4>
<p>后台相应的代码，如下所示：</p>
<pre><code>    @Autowired
    private UserContentService userContentService;
    @Autowired
    private UpvoteService upvoteService;
    /**
     * 点赞或踩
     * @param model
     * @param id
     * @param uid
     * @param upvote
     * @return
     */
    @RequestMapping("/upvote")
    @ResponseBody
    public Map&lt;String,Object&gt; upvote(Model model, @RequestParam(value = "id",required = false) long id,
                                     @RequestParam(value = "uid",required = false) Long uid,
                                     @RequestParam(value = "upvote",required = false) int upvote) {
        log.info( "id="+id+",uid="+uid+"upvote="+upvote );
        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");

        if(user == null){
            map.put( "data","fail" );
            return map;
        }
        Upvote up = new Upvote();
        up.setContentId( id );
        up.setuId( user.getId() );
        Upvote upv = upvoteService.findByUidAndConId( up );
        if(upv!=null){
            log.info( upv.toString()+"============" );
        }
        UserContent userContent =   userContentService.findById( id );
        if(upvote == -1){
            if(upv != null ){
                if( "1".equals( upv.getDownvote() ) ){
                    map.put( "data","down" );
                    return map;
                }else {
                    upv.setDownvote( "1" );
                    upv.setUpvoteTime( new Date(  ) );
                    upv.setIp( getClientIpAddress() );
                    upvoteService.update(upv);
                }

            }else {
                up.setDownvote( "1" );
                up.setUpvoteTime( new Date(  ) );
                up.setIp( getClientIpAddress() );
                upvoteService.add(up);
            }

            userContent.setDownvote( userContent.getDownvote()+upvote);
        }else {
            if(upv != null){
                if( "1".equals( upv.getUpvote() ) ){
                    map.put( "data","done" );
                    return map;
                }else {
                    upv.setUpvote( "1" );
                    upv.setUpvoteTime( new Date(  ) );
                    upv.setIp( getClientIpAddress() );
                    upvoteService.update(upv);
                }

            }else {
                up.setUpvote( "1" );
                up.setUpvoteTime( new Date(  ) );
                up.setIp( getClientIpAddress() );
                upvoteService.add(up);
            }


            userContent.setUpvote( userContent.getUpvote() + upvote );
        }
        userContentService.updateById( userContent );
        map.put( "data","success" );
        return map;

    }
</code></pre>
<p>代码解读：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入 UserContentService 和 UpvoteService 对象。</p>
<p>（2）从 Session 中取出用户，判断是否为空，为空则将“fail”添加到 map 集合并返回 map。</p>
<p>（3）根据文章 id 和用户 id 查找 Upvote 对象，根据文章 id 查找 UserContent 对象。</p>
<p>（4）根据 Upvote 判断是赞还是踩。</p>
<p>如果 upvote=-1 则踩，判断 Upvote 对象是否为 null。</p>
<ul>
<li><p>Upvote 不为 null，判断 Upvote.downvote 是否为1，如果为1则已踩，返回“down”；如果 Upvote.downvote 不为1，则将其值设置为1，并设置点赞时间等其它属性，更新 upvote。</p></li>
<li><p>Upvote 为 null，则 new 一个 Upvote，设置 downvote 的值为1，表示已踩，并设置点赞时间等其它属性，更新 upvote。</p></li>
<li><p>最后文章对象的 downvote 的值+1。</p></li>
</ul>
<p>如果 upvote=1 则赞，判断 Upvote 对象是否为 null。</p>
<ul>
<li><p>Upvote 不为 null，判断 Upvote.upvote 是否为1，如果为1则已赞，返回“done”；如果 Upvote.upvote 不为1，则将其值设置为1，并设置点赞时间等其它属性，更新 upvote。</p></li>
<li><p>Upvote为 null，则 new 一个 Upvote，设置 upvote 的值为1，表示已赞，并设置点赞时间等其它属性，更新 upvote。</p></li>
<li><p>最后文章对象的 upvote 的值+1。</p></li>
</ul>
<p>（5）更新文章 userContent，将 “success” 添加到 map 中并返回。</p>
<h4 id="mysqlupvote">MySQL 每天定时清空表 upvote</h4>
<p>打开 Navicat 或者其它数据库管理工具。</p>
<p><strong>1.</strong> 创建 event 每天 00:00:00 清空一次该表。</p>
<pre><code>    DROP EVENT IF EXISTS e_delete_upvote;
     CREATE  EVENT e_delete_upvote   
     ON SCHEDULE EVERY 1 day STARTS date_add(concat(current_date(), ' 00:00:00'), interval 0 second)
     ON COMPLETION PRESERVE ENABLE
     DO
     TRUNCATE TABLE dream_db.upvote;
</code></pre>
<p><strong>2.</strong> 设置开启事件调度器 event scheduler，代码如上：</p>
<pre><code>    SET GLOBAL event_scheduler=1;
</code></pre>
<h3 id="-3">评论、回复</h3>
<p>评论、回复模块比较复杂，我们一步一步分开来说。</p>
<h4 id="-4">准备</h4>
<p>我们看下前端日期格式化函数 index.jsp 中的代码：</p>
<pre><code>    function FormatDate (strTime) {
        var date = new Date(strTime);
        var h=date.getHours();       //获取当前小时数(0-23)
        var m=date.getMinutes();     //获取当前分钟数(0-59)
        if(m&lt;10) m = '0' + m;
        var s=date.getSeconds();
        if(s&lt;10) s = '0' + s;
        return date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+" "+h+':'+m+":"+s;
    }
</code></pre>
<p>该方法主要是将日期字符串转换成固定格式的日期字符串返回。</p>
<p>另外，现在通用 mapper 方法已经不能满足我们的需要的，所以需要手写 SQL，比如：</p>
<ol>
<li>查询评论的时候需要将用户信息也查询出来，需要使用联合查询；</li>
<li>插入评论的时候需要返回主键 id。</li>
</ol>
<p>打开 CommentMapper.java，增加以下方法：</p>
<pre><code>      //根据文章id查询所有评论
    List&lt;Comment&gt; selectAll(@Param("cid")long cid);
    //根据文章id查询所有一级评论
    List&lt;Comment&gt; findAllFirstComment(@Param("cid")long cid);
    //根据文章id和二级评论ids查询出所有二级评论
    List&lt;Comment&gt; findAllChildrenComment(@Param("cid")long cid,@Param("children")String children);
    //插入评论并返回主键id 返回值是影响行数  id在Comment对象中
    int insertComment(Comment comment);
</code></pre>
<p>打开 CommentServiceImpl.java，将其中的 add、findAll 等方法修改如下：</p>
<pre><code>     public int add(Comment comment) {
        return commentMapper.insertComment(comment);
    }

     public List&lt;Comment&gt; findAll(Long cid) {
        return commentMapper.selectAll(cid);
    }

      public List&lt;Comment&gt; findAllFirstComment(Long cid)
    {
        return commentMapper.findAllFirstComment(cid);
    }

     public List&lt;Comment&gt; findAllChildrenComment(Long cid, String children) {
        return commentMapper.findAllChildrenComment(cid,children);
    }
</code></pre>
<p>在 <code>resources/mapping</code> 包下新建 comment.xml 映射文件，写上 CommentMapper 接口中对应方法的 SQL:</p>
<pre><code class="     language-    ">    &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
    &lt;!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt;
    &lt;mapper namespace="wang.dreamland.www.dao.CommentMapper"&gt;

    &lt;select id="selectAll"  resultMap="commentMap"&gt;
        select c.id,c.children,c.con_id,c.com_id,c.by_id,c.upvote,c.comm_time,c.com_content,u.id as uid,u.email,u.password,u.nick_name,u.phone,u.state,u.img_url,u.enable
        from comment c,user u WHERE con_id = #{cid} and c.com_id = u.id order by id desc
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.Comment" id="commentMap"&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="children" column="children" /&gt;
        &lt;result property="conId" column="con_id" /&gt;
        &lt;result property="comId" column="com_id" /&gt;
        &lt;result property="byId" column="by_id" /&gt;
        &lt;result property="upvote" column="upvote" /&gt;
        &lt;result property="commTime" column="comm_time" /&gt;
        &lt;result property="comContent" column="com_content" /&gt;
        &lt;!-- property 表示wang.dreamland.www.entity.Comment中的属性； column 表示表中的列名 --&gt;
            &lt;association property="user" javaType="User"&gt;
                &lt;id column="uid" property="id" /&gt;
                &lt;result column="email" property="email" /&gt;
                &lt;result column="password" property="password" /&gt;
                &lt;result column="nick_name" property="nickName" /&gt;
                &lt;result column="phone" property="phone" /&gt;
                &lt;result column="state" property="state" /&gt;
                &lt;result column="img_url" property="imgUrl" /&gt;
                &lt;result column="enable" property="enable" /&gt;
            &lt;/association&gt;
    &lt;/resultMap&gt;

    &lt;insert id="insertComment" parameterType="comment" useGeneratedKeys="true" keyProperty="id"&gt;
        &lt;!--&lt;selectKey keyProperty="id" resultType="java.lang.Long" order="AFTER"&gt;
            SELECT LAST_INSERT_ID()
        &lt;/selectKey&gt;--&gt;
        insert into comment(id, con_id, com_id, by_id, com_content, upvote, comm_time,children) values(#{id}, #{conId},#{comId}, #{byId},#{comContent},#{upvote}, #{commTime},#{children})
    &lt;/insert&gt;

    &lt;select id="findAllFirstComment"  resultMap="firstCommentMap"&gt;
        select c.id,c.children,c.con_id,c.com_id,c.by_id,c.upvote,c.comm_time,c.com_content,u.id as uid,u.email,u.password,u.nick_name,u.phone,u.state,u.img_url,u.enable
        from comment c,user u WHERE con_id = #{cid} and by_id is null and c.com_id = u.id order by id desc
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.Comment" id="firstCommentMap"&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="children" column="children" /&gt;
        &lt;result property="conId" column="con_id" /&gt;
        &lt;result property="comId" column="com_id" /&gt;
        &lt;result property="byId" column="by_id" /&gt;
        &lt;result property="upvote" column="upvote" /&gt;
        &lt;result property="commTime" column="comm_time" /&gt;
        &lt;result property="comContent" column="com_content" /&gt;
        &lt;!-- property 表示wang.dreamland.www.entity.Comment中的属性； column 表示表中的列名 --&gt;
        &lt;association property="user" javaType="User"&gt;
            &lt;id column="uid" property="id" /&gt;
            &lt;result column="email" property="email" /&gt;
            &lt;result column="password" property="password" /&gt;
            &lt;result column="nick_name" property="nickName" /&gt;
            &lt;result column="phone" property="phone" /&gt;
            &lt;result column="state" property="state" /&gt;
            &lt;result column="img_url" property="imgUrl" /&gt;
            &lt;result column="enable" property="enable" /&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt;

    &lt;!--查询所有子评论--&gt;
    &lt;select id="findAllChildrenComment"  resultMap="childCommentMap"&gt;
        select c.id,c.children,c.con_id,c.com_id,c.by_id,c.upvote,c.comm_time,c.com_content,u.id as uid,u.email,u.password,u.nick_name,u.phone,u.state,u.img_url,u.enable
        from comment c,user u WHERE con_id = #{cid}
        &lt;if test='children!=null and children!=""'&gt;
            AND c.id in (${children})
        &lt;/if&gt;

          and c.com_id = u.id order by id desc
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.Comment" id="childCommentMap"&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="children" column="children" /&gt;
        &lt;result property="conId" column="con_id" /&gt;
        &lt;result property="comId" column="com_id" /&gt;
        &lt;result property="byId" column="by_id" /&gt;
        &lt;result property="upvote" column="upvote" /&gt;
        &lt;result property="commTime" column="comm_time" /&gt;
        &lt;result property="comContent" column="com_content" /&gt;
        &lt;!-- property 表示wang.dreamland.www.entity.Comment中的属性； column 表示表中的列名 --&gt;
        &lt;association property="user" javaType="User"&gt;
            &lt;id column="uid" property="id" /&gt;
            &lt;result column="email" property="email" /&gt;
            &lt;result column="password" property="password" /&gt;
            &lt;result column="nick_name" property="nickName" /&gt;
            &lt;result column="phone" property="phone" /&gt;
            &lt;result column="state" property="state" /&gt;
            &lt;result column="img_url" property="imgUrl" /&gt;
            &lt;result column="enable" property="enable" /&gt;
        &lt;/association&gt;
    &lt;/resultMap&gt;

    &lt;/mapper&gt;
</code></pre>
<p>我们可以使用 select、insert、update、delete 标签进行查询、插入、更新和删除。</p>
<p>接下来，我们看下上面代码中几个重要的标签。</p>
<p><strong>1.</strong> mapper 标签</p>
<pre><code>    &lt;mapper namespace="wang.dreamland.www.dao.CommentMapper"&gt;
</code></pre>
<p>其中，名称空间 namespace 对应 mapper 接口的位置。</p>
<p><strong>2.</strong> select 标签</p>
<pre><code>    &lt;select id="selectAll"  resultMap="commentMap"&gt;
</code></pre>
<p>其中，id 是唯一标识，应该和 CommentMapper 中的某个方法名一致。resultMap 的值是某个 resultMap 标签的 id。</p>
<p><strong>3.</strong> resultMap 标签</p>
<pre><code>    &lt;resultMap type="wang.dreamland.www.entity.Comment" id="firstCommentMap"&gt;
</code></pre>
<p>其中，type 是返回值类型，这里是 Comment对象，id 是 resultMap 的唯一标识，可通过 id 引用某个 resultMap。</p>
<p><strong>4.</strong> resultMap 标签内的 id 代表主键 property 对应属性字段，column 对应数据库中的列名。</p>
<p><strong>5.</strong> result 标签和 id 标签类似，也是映射实体类属性和数据库表中列名的。但是 id 标签为唯一标识，可以映射主键。</p>
<pre><code>     &lt;result property="conId" column="con_id" /&gt;
</code></pre>
<p>上面代码中 conId 代表 Comment 中的属性字段 conId，<code>con_id</code> 代表数据库表 comment 中的列 <code>con_id</code>，把实体类中属性和表中字段映射起来。</p>
<p><strong>6.</strong> 一个评论对应一个评论者，所以是一对一的关系，使用 association 标签：</p>
<pre><code>     &lt;association property="user" javaType="User"&gt;
</code></pre>
<p>property 对应 Comment 实体类中 user 属性，javaType 代表类型，返回类型 User。</p>
<p>association 标签内的 id 标签和 result 标签与上面说的一样，不再赘述。</p>
<p>接下来看下查询 SQL 语句:</p>
<pre><code>    select c.id,c.children,c.con_id,c.com_id,c.by_id,c.upvote,c.comm_time,c.com_content,u.id as uid,u.email,u.password,u.nick_name,u.phone,u.state,u.img_url,u.enable
        from comment c,user u WHERE con_id = #{cid} and c.com_id = u.id order by id desc
</code></pre>
<p>其中：</p>
<p><strong>1.</strong> comment c 和 user u 分别是给 comment 表和 user 表起的别名。</p>
<p><strong>2.</strong> 这条 SQL 是对 comment 表和 user 表进行联合查询，把指定文章 id 并且评论者 id 与用户表中 id 相同的所有评论查询出来。将结果集封装在 resultMap 中。</p>
<p><strong>3.</strong> 注意 <code>#{cid}</code> 表示占位符，与传入的参数字段 cid 相对应。</p>
<pre><code>     List&lt;Comment&gt; selectAll(@Param("cid")long cid);
</code></pre>
<p><strong>扩展：</strong> <code>#{}</code> 与 <code>${}</code> 异同点如下：</p>
<ul>
<li>相同点：两者都可以接收参数；</li>
<li>不同点：<code>#{}</code> 解析后是占位符 <code>?</code> 可以防止 SQL 注入。</li>
</ul>
<p><code>#{}</code> 解析后相当于:</p>
<pre><code>select * from user where id = ?
</code></pre>
<p>而 <code>${}</code> 则是直接赋值，解析后相当于:</p>
<pre><code>select * from user where id = 1
</code></pre>
<p><strong>4.</strong> order by id desc 表示根据 id 降序排列，默认为升序排列。order by id asc 则表示根据 id 升序排列。</p>
<h4 id="-5">点击评论或者回复小图标</h4>
<p><img src="http://images.gitbook.cn/1882c120-7600-11e8-9def-35cb75b6091c" alt="" /></p>
<p>这两者分别对应两个 a 标签，但对应着相同的 onclik 事件，参数为文章的 id 和该文章的作者 id：</p>
<pre><code>     &lt;a  onclick="reply(${cont.id},${cont.uid});"&gt;
        &lt;i class="number" id="comment_num_${cont.id}"&gt;${cont.commentNum}&lt;/i&gt; 评论
     &lt;/a&gt;


       &lt;a  onclick="reply(${cont.id},${cont.uid});"&gt;
             &lt;i class="number" id="comment_num_${cont.id}"&gt;${cont.commentNum}&lt;/i&gt; 评论
       &lt;/a&gt;
</code></pre>
<p>该点击事件的函数如下：</p>
<pre><code>    //点击评论或者回复图标
    function reply(id,uid) {
        $("div").remove("#comment_reply_"+id+" .comment-show");
        $("div").remove("#comment_reply_"+id+" .comment-show-con");
        if(showdiv_display = document.getElementById('comment_reply_'+id).style.display=='none'){//如果show是隐藏的

            document.getElementById('comment_reply_'+id).style.display='block';//show的display属性设置为block（显示）
            $.ajax({
                type:'post',
                url:'/reply',
                data: {"content_id":id},
                dataType:'json',
                success:function(data){
                    var list =  data["list"];

                    var okHtml;
                    if(list!=null &amp;&amp; list!=""){
                        $(list).each(function () {
                            var chtml = "&lt;div class='comment-show'&gt;"+
                                "&lt;div class='comment-show-con clearfix'&gt;"+
                                "&lt;div class='comment-show-con-img pull-left'&gt;&lt;img src='"+this.user.imgUrl+"' alt=''&gt;&lt;/div&gt;"+
                                "&lt;div class='comment-show-con-list pull-left clearfix'&gt;"+
                                "&lt;div class='pl-text clearfix'&gt;"+
                                "&lt;a  class='comment-size-name'&gt;"+this.user.nickName+" :&lt;/a&gt;"+
                                "&lt;span class='my-pl-con'&gt;&amp;nbsp;"+this.comContent+"&lt;/span&gt;"+
                                "&lt;/div&gt; &lt;div class='date-dz'&gt;&lt;span class='date-dz-left pull-left comment-time'&gt;"+FormatDate(this.commTime)+"&lt;/span&gt;"+
                                "&lt;div class='date-dz-right pull-right comment-pl-block'&gt;"+
                                "&lt;a onclick='deleteComment("+id+","+uid+","+this.id+",null)' id='comment_dl_"+this.id+"' style='cursor:pointer' class='removeBlock'&gt;删除&lt;/a&gt;"+
                                "&lt;a style='cursor:pointer' onclick='comment_hf("+id+","+this.id+","+null+","+this.user.id+","+uid+")' id='comment_hf_"+this.id+"' class='date-dz-pl pl-hf hf-con-block pull-left'&gt;回复&lt;/a&gt;"+
                                "&lt;span class='pull-left date-dz-line'&gt;|&lt;/span&gt;"+
                                "&lt;a onclick='reply_up("+this.id+")' style='cursor:pointer' class='date-dz-z pull-left' id='change_color_"+this.id+"'&gt;&lt;i class='date-dz-z-click-red'&gt;&lt;/i&gt;赞 (&lt;i class='z-num' id='comment_upvote_"+this.id+"'&gt;"+this.upvote+"&lt;/i&gt;)&lt;/a&gt;"+
                                "&lt;/div&gt; &lt;/div&gt; &lt;div class='hf-list-con' id='hf-list-con-"+this.id+"'&gt;";


                            var ehtml =   "&lt;/div&gt; &lt;/div&gt; &lt;/div&gt;&lt;/div&gt;";
                            var parentComm_id = this.id;

                            okHtml = chtml;
                            //alert(this.children)
                            if(this.children != null &amp;&amp; this.children != ''){
                                var commentList = this.comList;
                                $(commentList).each(function () {
                                    // alert(this.id);
                                    var oHtml = "&lt;div class='all-pl-con'&gt;&lt;div class='pl-text hfpl-text clearfix'&gt;"+
                                        "&lt;a class='comment-size-name'&gt;"+this.user.nickName+"&lt;a class='atName'&gt;@"+this.byUser.nickName+" :&lt;/a&gt; &lt;/a&gt;"+
                                        "&lt;span class='my-pl-con'&gt;"+this.comContent+"&lt;/span&gt;"+
                                        "&lt;/div&gt;&lt;div class='date-dz'&gt; &lt;span class='date-dz-left pull-left comment-time'&gt;"+FormatDate(this.commTime)+"&lt;/span&gt;"+
                                        "&lt;div class='date-dz-right pull-right comment-pl-block'&gt;"+
                                        "&lt;a style='cursor:pointer' onclick='deleteComment("+id+","+uid+","+this.id+","+parentComm_id+")' id='comment_dl_"+this.id+"' class='removeBlock'&gt;删除&lt;/a&gt;"+
                                        "&lt;a onclick='comment_hf("+id+","+this.id+","+parentComm_id+","+this.user.id+","+uid+")' id='comment_hf_"+this.id+"' style='cursor:pointer' class='date-dz-pl pl-hf hf-con-block pull-left'&gt;回复&lt;/a&gt; &lt;span class='pull-left date-dz-line'&gt;|&lt;/span&gt;"+
                                        "&lt;a onclick='reply_up("+this.id+")' id='change_color_"+this.id+"' style='cursor:pointer' class='date-dz-z pull-left'&gt;&lt;i class='date-dz-z-click-red'&gt;&lt;/i&gt;赞 (&lt;i class='z-num' id='comment_upvote_"+this.id+"'&gt;"+this.upvote+"&lt;/i&gt;)&lt;/a&gt;"+
                                        "&lt;/div&gt;&lt;/div&gt; &lt;/div&gt;";

                                    okHtml = okHtml + oHtml;
                                });


                            }

                            okHtml = okHtml+ehtml;
                            $("#comment-show-" + id).append(okHtml);

                        });
                    }

                }
            });


        }else{//如果show是显示的

            document.getElementById('comment_reply_'+id).style.display='none';//show的display属性设置为none（隐藏）

        }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）每次展开都要先移除评论列表，然后再添加评论列表到 div，否则会发现每次展开都会增加一倍的评论。自己可以试一下。移除评论列表方法如下：</p>
<pre><code>      $("div").remove("#comment_reply_"+id+" .comment-show");
    $("div").remove("#comment_reply_"+id+" .comment-show-con");
</code></pre>
<p>（2）判断评论回复列表是显示还是隐藏的，如果显示就将其隐藏，如果隐藏的就将其显示。</p>
<p>（3）发送 AJAX 请求。请求参数就是文章 id。</p>
<p>（4）success 回调函数返回 JSON 数据，取出数据赋值给 list，list即包含了所有评论列表。如果评论列表 list 不为空，对其进行遍历：</p>
<pre><code>      $(list).each(function () {}
</code></pre>
<p>将其结果拼装在 div 中，其中 okHtml(chml) 代表的是一级评论列表，oHtml 是二级评论列表（或者说子评论列表），一个一级评论可能有多个子评论。我们需要判断该一级评论是否有子评论，如果有就对子评论列表集合进行遍历，获取每个子评论。ehtml 是 div 结束标签。最后的评论列表拼装起来就是：</p>
<pre><code>    okHtml = okHtml + ehtml
</code></pre>
<p>（5）将评论回复列表 div 追加在当前文章的可添加评论内容的空 div 下。该 div 的 id 根据文章 id 区分：</p>
<pre><code>    $("#comment-show-" + id).append(okHtml);
</code></pre>
<p>（6）评论区域包含评论输入框和评论按钮，之后是可添加评论内容的空 div，如下：</p>
<pre><code>    &lt;div class="commentAll" style="display:none" id="comment_reply_${cont.id}"&gt;
           &lt;!--评论区域 begin--&gt;
           &lt;div class="reviewArea clearfix"&gt;
               &lt;textarea id="comment_input_${cont.id}"  class="content comment-input" placeholder="Please enter a comment&amp;hellip;" onkeyup="keyUP(this)"&gt;&lt;/textarea&gt;
                &lt;a class="plBtn" id="comment_${cont.id}" onclick="_comment(${cont.id},${user.id==null?0:user.id},${cont.uId})" style="color: white;cursor: pointer;"&gt;评论&lt;/a&gt;
           &lt;/div&gt;
           &lt;!--评论区域 end--&gt;
           &lt;!--添加评论内容的空div--&gt;
           &lt;div class="comment-show-first" id="comment-show-${cont.id}"&gt;

           &lt;/div&gt;

    &lt;/div&gt;
</code></pre>
<p>上面有一个 keyUp 事件，键盘弹起时触发，主要是限制输入内容的长度，函数如下：</p>
<pre><code>     //限制字数
    function keyUP(t){
        var len = $(t).val().length;
        if(len &gt; 139){
            $(t).val($(t).val().substring(0,140));
        }
    }
</code></pre>
<p>我们再看下 Java 后台代码。</p>
<p><strong>1.</strong> 评论回复实体类 Comment 包含评论者、被评论者和子评论列表，我们对 Comment 类修改如下：</p>
<pre><code>    @Transient
    private User user;

    @Transient
    private User byUser;

    @Transient
    private List&lt;Comment&gt; comList;

     public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public User getByUser() {
        return byUser;
    }

    public void setByUser(User byUser) {
        this.byUser = byUser;
    }

     public List&lt;Comment&gt; getComList() {
        return comList;
    }

    public void setComList(List&lt;Comment&gt; comList) {
        this.comList = comList;
    }
</code></pre>
<p>增加三个属性 User 评论者、byUser 被评论者和 comList 子评论列表，并生成 getter 和 setter 方法，其中 <code>@Transient</code> 注解 在添加表中不存在字段时使用。</p>
<p><strong>2.</strong> index 页面控制层 IndexJspController.java 代码如下：</p>
<pre><code>    @Autowired
    private CommentService commentService;
    @Autowired
    private UserService userService;

    @RequestMapping("/reply")
    @ResponseBody
    public Map&lt;String,Object&gt; reply(Model model, @RequestParam(value = "content_id",required = false) Long content_id) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        List&lt;Comment&gt; list = commentService.findAllFirstComment(content_id);
        if(list!=null &amp;&amp; list.size()&gt;0){
            for(Comment c:list){
                List&lt;Comment&gt; coments = commentService.findAllChildrenComment( c.getConId(), c.getChildren() );
                if(coments!=null &amp;&amp; coments.size()&gt;0){
                    for(Comment com:coments){
                       if(com.getById()!=null ){
                           User byUser = userService.findById( com.getById() );
                           com.setByUser( byUser );
                       }

                    }
                }
                c.setComList( coments );
            }
        }

        map.put( "list",list );

        return map;

    }
</code></pre>
<p>代码解析：</p>
<p>（1）先根据文章 id 查找出所有的一级评论列表。</p>
<p>（2）遍历一级评论列表，根据文章 id 和一级评论的子评论 id（多个id用 <code>,</code> 号隔开）字符串查询子评论列表。</p>
<p>（3）遍历子评论列表，如果评论者 id 不为 null，则根据该 id 查询 User，注入子评论的 byUser 属性中。</p>
<p>（4）将子评论列表注入到一级评论的 comList 属性中。</p>
<p>（5）将 list 放入 map 中，返回 map。</p>
<h4 id="-6">点击评论回复模块的评论按钮</h4>
<p><img src="http://images.gitbook.cn/2f455d40-7601-11e8-9c7a-43197c8c6da2" alt="" /></p>
<p>输入内容后，点击评论按钮，前端代码如下：</p>
<pre><code>    &lt;a class="plBtn" id="comment_${cont.id}" onclick="_comment(${cont.id},${user.id==null?0:user.id},${cont.uId})" style="color: white;cursor: pointer;"&gt;评论&lt;/a&gt;
</code></pre>
<p>每个评论按钮都有唯一的一个 id，即：</p>
<pre><code>    id="comment_${cont.id}"
</code></pre>
<p>点击事件 onclick 参数有：文章 id、评论者 id、被评论者id：</p>
<pre><code>     onclick="_comment(${cont.id},${user.id==null?0:user.id},${cont.uId})"
</code></pre>
<p><code>_comment</code> 方法如下：</p>
<pre><code>    //点击评论按钮
    function _comment(content_id,uid,cuid) {
        var myDate = new Date();
        //获取当前年
        var year=myDate.getFullYear();
        //获取当前月
        var month=myDate.getMonth()+1;
        //获取当前日
        var date=myDate.getDate();
        var h=myDate.getHours();       //获取当前小时数(0-23)
        var m=myDate.getMinutes();     //获取当前分钟数(0-59)
        if(m&lt;10) m = '0' + m;
        var s=myDate.getSeconds();
        if(s&lt;10) s = '0' + s;
        var now=year+'-'+month+"-"+date+" "+h+':'+m+":"+s;
        //获取输入内容
        var oSize = $("#comment_input_"+content_id).val();
        console.log(oSize);
        //动态创建评论模块

        if(oSize.replace(/(^\s*)|(\s*$)/g, "") != ''){


            $.ajax({
                type:'post',
                url:'/comment',
                data: {"content_id":content_id,"uid":uid,"oSize":oSize,"comment_time":now},
                dataType:'json',
                success:function(data){
                    var comm_data =  data["data"];
                    //alert(comm_data);
                    if(comm_data=="fail"){
                        window.location.href = "/login.jsp";
                    }else {
                        var id = comm_data.id;
                        //alert(id)
                        oHtml = '&lt;div class="comment-show-con clearfix"&gt;&lt;div class="comment-show-con-img pull-left"&gt;&lt;img src="${user.imgUrl}" alt=""&gt;&lt;/div&gt; &lt;div class="comment-show-con-list pull-left clearfix"&gt;&lt;div class="pl-text clearfix"&gt; &lt;a  class="comment-size-name"&gt;${user.nickName} : &lt;/a&gt; &lt;span class="my-pl-con"&gt;&amp;nbsp;'+ oSize +'&lt;/span&gt; &lt;/div&gt; &lt;div class="date-dz"&gt; &lt;span class="date-dz-left pull-left comment-time"&gt;'+now+'&lt;/span&gt; &lt;div class="date-dz-right pull-right comment-pl-block"&gt;&lt;a style="cursor:pointer"  onclick="deleteComment('+content_id+','+cuid+','+id+','+null+')" id="comment_dl_'+id+'"  class="removeBlock"&gt;删除&lt;/a&gt; &lt;a style="cursor:pointer" onclick="comment_hf('+content_id+','+id+','+null+','+comm_data.user.id+','+cuid+')" id="comment_hf_'+id+'" class="date-dz-pl pl-hf hf-con-block pull-left"&gt;回复&lt;/a&gt; &lt;span class="pull-left date-dz-line"&gt;|&lt;/span&gt; &lt;a onclick="reply_up('+id+')" id="change_color_'+id+'" style="cursor:pointer"  class="date-dz-z pull-left" &gt;&lt;i class="date-dz-z-click-red"&gt;&lt;/i&gt;赞 (&lt;i class="z-num" id="comment_upvote_'+id+'"&gt;0&lt;/i&gt;)&lt;/a&gt; &lt;/div&gt; &lt;/div&gt;&lt;div class="hf-list-con"&gt;&lt;/div&gt;&lt;/div&gt; &lt;/div&gt;';
                        $("#comment_"+content_id).parents('.reviewArea ').siblings('.comment-show-first').prepend(oHtml);
                        $("#comment_"+content_id).siblings('.flex-text-wrap').find('.comment-input').prop('value','').siblings('pre').find('span').text('');

                        $("#comment_input_"+content_id).val('');

                        var num = document.getElementById("comment_num_"+content_id).innerHTML;
                        document.getElementById("comment_num_"+content_id).innerHTML = (parseInt(num) + 1)+"";
                    }
                }
            });
        }

    }
</code></pre>
<p>代码解读：</p>
<p>（1）获取评论的时间赋值给 now。</p>
<p>（2）获取评论内容赋值给 oSize。</p>
<p>（3）发送 AJAX 请求，请求参数有：文章 id、评论用户 id、评论内容 oSize、评论时间 now：</p>
<pre><code>     data: {"content_id":content_id,"uid":uid,"oSize":oSize,"comment_time":now},
</code></pre>
<p>（4）success回调函数返回结果，将数据取出赋值给 <code>comm_data</code>，如果是 fail 则跳转登录页面。</p>
<p>（5）如果不为 fail 则创建 div，赋值给 oHtml。将 oHtml 动态添加到评论列表中。</p>
<p>（6）获取评论数，将其值+1，动态添加到页面上。</p>
<p>我们继续写 Java 后台代码。</p>
<p><strong>1.</strong> 在 common 包下添加日期工具类 DateUtils.java：</p>
<pre><code>    public class DateUtils {
    public static Date StringToDate(String dateStr, String formatStr){
        DateFormat dd=new SimpleDateFormat(formatStr);
        Date date=null;
        try {
            date = dd.parse(dateStr);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }
    }
</code></pre>
<p>主要是根据传入的日期字符串和日期格式字符串，返回格式化后的日期。</p>
<p><strong>2.</strong> 控制层 IndexJspController.java，代码如下：</p>
<pre><code>    @RequestMapping("/comment")
    @ResponseBody
    public Map&lt;String,Object&gt; comment(Model model, @RequestParam(value = "id",required = false) Long id ,
                                      @RequestParam(value = "content_id",required = false) Long content_id ,
                                      @RequestParam(value = "uid",required = false) Long uid ,
                                      @RequestParam(value = "by_id",required = false) Long bid ,
                                      @RequestParam(value = "oSize",required = false) String oSize,
                                      @RequestParam(value = "comment_time",required = false) String comment_time,
                                      @RequestParam(value = "upvote",required = false) Integer upvote) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        if(user == null){
            map.put( "data","fail" );
            return map;
        }
        if(id==null ){

            Date date = DateUtils.StringToDate( comment_time, "yyyy-MM-dd HH:mm:ss" );

            Comment comment = new Comment();
            comment.setComContent( oSize );
            comment.setCommTime( date );
            comment.setConId( content_id );
            comment.setComId( uid );
            if(upvote==null){
                upvote = 0;
            }
            comment.setById( bid );
            comment.setUpvote( upvote );
            User u = userService.findById( uid );
            comment.setUser( u );
            commentService.add( comment );
            map.put( "data",comment );

            UserContent userContent = userContentService.findById( content_id );
            Integer num = userContent.getCommentNum();
            userContent.setCommentNum( num+1 );
            userContentService.updateById( userContent );

        }else {
            //点赞
            Comment c = commentService.findById( id );
            c.setUpvote( upvote );
            commentService.update( c );


        }

        return map;

    }
</code></pre>
<p>代码解读：</p>
<p>（1）判断用户是否登录，未登录直接跳转到登录页面。</p>
<p>（2）判断评论 id 是否为 null，为 null 则说明是添加评论，不为 null 则为点赞或取消赞（评论里的点赞）。</p>
<p>（3）添加评论后将评论返回，注意这里的添加评论需要返回主键 id，所以插入方法需要手写 XML。</p>
<p>（4）根据文章 id 查询 UserContent，将其评论数+1，然后更新 userContent。</p>
<p>（5）如果评论 id 不为 null，则是点赞或取消赞，根据 id 查询评论 Comment，更新 upvote 的值。</p>
<p>重新启动访问 index.jsp，然后登陆后进行评论看是否成功！</p>
<p><img src="http://images.gitbook.cn/0cdbbe60-7602-11e8-9c7a-43197c8c6da2" alt="" /></p>
<p>上面的评论数和点赞等数据是之前插入的，可以进入数据库将其清零。</p>
<p>注意，如果报错：</p>
<blockquote>
  <p>Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Column 'id' cannot be null</p>
</blockquote>
<p>可能是 comment 表主键没有自增长，我们可以修改下 comment 表主键自增长来解决这个问题，如下：</p>
<pre><code>alter table comment change id id bigint(20) not null auto_increment; 
</code></pre>
<h4 id="-7">评论块的删除、回复、点赞操作</h4>
<h5 id="-8"><strong>删除操作</strong></h5>
<p>1.删除的点击事件。</p>
<p>在之前写好的 reply 函数内有删除的点击事件：</p>
<pre><code>    &lt;a onclick='deleteComment("+id+","+uid+","+this.id+",null)' id='comment_dl_"+this.id+"' style='cursor:pointer' class='removeBlock'&gt;删除&lt;/a&gt;
</code></pre>
<p>这里 deleteComment 函数需要四个参数：文章 id，文章作者 id，评论 id 和父评论 id（没有父评论，这里传入 null）。</p>
<p>具体实现方法如下：</p>
<pre><code>    //删除评论块
    function deleteComment(con_id,uid,id,fid) {
        // alert(uid)
        if('${user.id}'==uid){

            if (!confirm("确认要删除？")) {
                window.event.returnValue = false;
            }else{

                //发送ajax请求
                $.ajax({
                    type:'post',
                    url:'/deleteComment',
                    data: {"id":id,"uid":uid,"con_id":con_id,"fid":fid},
                    dataType:'json',
                    success:function(data){
                        var comm_data =  data["data"];
                        //alert(comm_data);
                        if(comm_data=="fail"){
                            window.location.href = "/login.jsp";
                        }else if(comm_data=="no-access"){
                            //alert("没有权限！");
                        }else {
                            //alert(comm_data)
                            var oThis = $("#comment_dl_"+id);
                            var oT = oThis.parents('.date-dz-right').parents('.date-dz').parents('.all-pl-con');
                            if(oT.siblings('.all-pl-con').length &gt;= 1){
                                oT.remove();
                            }else {
                                oThis.parents('.date-dz-right').parents('.date-dz').parents('.all-pl-con').parents('.hf-list-con').css('display','none')
                                oT.remove();
                            }
                            oThis.parents('.date-dz-right').parents('.date-dz').parents('.comment-show-con-list').parents('.comment-show-con').remove();


                            //评论数comment_num_con_id
                            document.getElementById("comment_num_"+con_id).innerHTML = parseInt(comm_data)+"";

                        }
                    }
                });
            }
        }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）判断用户是否是文章作者，如果不是就不做处理，如果是则提示是否确认删除（想让评论者本人也可删除评论，有兴趣同学可尝试下）。</p>
<p>（2）如果用户点击确认则发送 AJAX 请求，请求参数主要有评论 id、文章作者 uid、文章 <code>con_id</code> 和父评论 fid。</p>
<pre><code>    data: {"id":id,"uid":uid,"con_id":con_id,"fid":fid},
</code></pre>
<p>（3）success 回调函数会返回 JSON 格式数据，通过 <code>data["data"]</code> 取出 Java 后台放入 data 内的数据。如果用户未登录则返回 fail，如果用户不是文章作者则返回 <code>no-access</code>，成功删除则返回的是文章评论数。</p>
<p>（4）如果用户未登录则跳转到登录页面，用户没有权限则不做处理，成功删除则移除评论列表。</p>
<p>（5）将删除后的最新评论数更新到页面中。</p>
<p>2.删除评论的后台代码。</p>
<p>控制层 IndexJspController.java 删除评论代码如下：</p>
<pre><code>    @RequestMapping("/deleteComment")
    @ResponseBody
    public Map&lt;String,Object&gt;  deleteComment(Model model, @RequestParam(value = "id",required = false) Long id,@RequestParam(value = "uid",required = false) Long uid,
                                            @RequestParam(value = "con_id",required = false) Long con_id,@RequestParam(value = "fid",required = false) Long fid) {
        int num = 0;
        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        if(user==null){
            map.put( "data","fail" );
        }else{
            if(user.getId().equals( uid )){
                Comment comment = commentService.findById( id );
                if(StringUtils.isBlank( comment.getChildren() )){
                    if(fid!=null){
                        //去除id
                        Comment fcomm = commentService.findById( fid );
                        String child = StringUtil.getString( fcomm.getChildren(), id );
                        fcomm.setChildren( child );
                        commentService.update( fcomm );
                    }
                    commentService.deleteById(id);
                    num = num + 1;
                }else {
                    String children = comment.getChildren();
                    commentService.deleteChildrenComment(children);
                    String[] arr = children.split( "," );

                    commentService.deleteById( id );

                    num = num + arr.length + 1;

                }
                UserContent content = userContentService.findById( con_id );
                if(content!=null){
                    if(content.getCommentNum() - num &gt;= 0){
                        content.setCommentNum( content.getCommentNum() - num );
                    }else {
                        content.setCommentNum( 0 );
                    }

                    userContentService.updateById( content );
                }
                map.put( "data",content.getCommentNum() );
            }else {
                map.put( "data","no-access" );
            }
        }

        return  map;
    }
</code></pre>
<p>代码解读：</p>
<p>（1）从 Session 中取出 user 信息，判断用户是否登录，未登录，则将 fail 放入 map，键为“data”，值为“fail”。</p>
<p>（2）用户登录，则判断该用户是否是文章作者，不是则将 <code>no-access</code> 放入 map，键为“data”，值为 <code>no-access</code>。</p>
<p>（3）是文章作者，则根据评论 id 查询出评论对象 Comment，然后判断该评论是否含有子评论。</p>
<p>（4）如果该评论没有子评论，判断该评论有没有父评论，有父评论，则将该评论 id 从父评论的子评论列表中移除。</p>
<p>然后根据评论 id 删除该评论，将删除的评论数赋值给 num。</p>
<p>（5）如果该评论有子评论，删除所有子评论，然后删除该评论，将删除的评论数赋值给 num：</p>
<pre><code>num = num + arr.length + 1;//0 + 所有子评论数（arr.length） + 该评论(1)
</code></pre>
<p>（6）然后根据文章 id 查询出文章对象 UserContent，该对象不为空后，进行判断：如果删除的评论数在该文章总评论数范围之内，则更新删除评论之后的评论数，如果删除的评论数比文章总评论数还多，则更新为0。将删除后的文章评论数放入 map 中，key 为“data”，值为最新评论数。</p>
<p>（7）将 map 返回。</p>
<p>其中第4点用到了自定义字符串处理函数，返回删除子评论列表中指定 id 后的字符串，参数是以逗号分隔的子评论 id 字符串和要删除的 id。在 common 包下 StringUtil.java，具体方法如下：</p>
<pre><code>    public class StringUtil {
    public static String getString(String str,Long id){
            String[] arr = str.split( "," );
            String s = "";
            if(arr!=null &amp;&amp; arr.length&gt;0){
                for(int i = 0; i&lt;arr.length;i++){
                    System.out.println(id.toString().equals( arr[i] ));
                    if(id.toString().equals( arr[i] )){
                        System.out.println(arr[i]);
                        continue;
                    }else {
                        if(i == arr.length - 1){
                            s = s + arr[i] ;
                        }else {
                            s = s + arr[i] + ",";
                        }
                    }


                }
            }
        if (s.endsWith( "," )){
                s = s.substring( 0,s.length()-1 );
        }
        return s;
    }
    }
</code></pre>
<p>启动 Tomcat，访问网页，鼠标悬浮到评论上会显示删除字样，删除评论看是否成功。</p>
<p><strong>注意：</strong>因为我们现在还没有写文章，所以如果文章作者 id 和你登录的用户 id 不一样，会删不了，也没有提示。可以对数据库进行修改，将文章作者 id 改为你的用户 id，这样就可以删除了。</p>
<h5 id="-9"><strong>回复操作</strong></h5>
<p>在之前写好的 reply 函数内有回复的点击事件：</p>
<pre><code>&lt;a style='cursor:pointer' onclick='comment_hf("+id+","+this.id+","+null+","+this.user.id+","+uid+")' id='comment_hf_"+this.id+"' class='date-dz-pl pl-hf hf-con-block pull-left'&gt;回复&lt;/a&gt;
</code></pre>
<p>这里 <code>comment_hf</code> 函数内需要传入5个参数，分别是：文章 id、评论 id、一级评论 id（这里为 null，因为一级评论没有父评论)、被评论者 id、评论者 id，具体实现方法如下：</p>
<pre><code>     //一级评论  点击回复创建回复块
    function comment_hf(content_id,comment_id,fid,by_id,cuid) {
        // alert(cuid)
        //获取回复人的名字
        var oThis = $("#comment_hf_"+comment_id);
        var fhName = oThis.parents('.date-dz-right').parents('.date-dz').siblings('.pl-text').find('.comment-size-name').html();
        //回复@
        var fhN = '回复@' + fhName;
        var fhHtml = '&lt;div class="hf-con pull-left"&gt; &lt;textarea id="plcaceholder_'+comment_id+'"  class="content comment-input " placeholder="'+fhN+'" onkeyup="keyUP(this)"&gt;&lt;/textarea&gt; &lt;a id="comment_pl_'+comment_id+'" onclick="comment_pl('+content_id+','+comment_id+','+fid+','+by_id+','+cuid+')" class="hf-pl" style="color: white;cursor:pointer"&gt;评论&lt;/a&gt;&lt;/div&gt;';
        //显示回复
        if (oThis.is('.hf-con-block')) {
            oThis.parents('.date-dz-right').parents('.date-dz').append(fhHtml);
            oThis.removeClass('hf-con-block');
            $('.content').flexText();
            oThis.parents('.date-dz-right').siblings('.hf-con').find('.pre').css('padding', '6px 15px');

            //input框自动聚焦
            oThis.parents('.date-dz-right').siblings('.hf-con').find('.hf-input').val('').focus().val(fhN);
        } else {
            oThis.addClass('hf-con-block');
            oThis.parents('.date-dz-right').siblings('.hf-con').remove();
        }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）根据回复块对象的父节点的父节点获取之前评论人的名字，赋值给 fhName。</p>
<p>（2）将“回复@”与被回复人的名字进行拼接，赋值给 fhN。</p>
<p>（3）创建回复 input 框和评论按钮 div，赋值给 fhHtml，input 框内显示 回复@被回复人名字。</p>
<p>（4）if 和 else 主要判断是显示还是隐藏。点击回复 显示 input 框和评论按钮，再次点击则隐藏。</p>
<p>点击回复效果如下图：</p>
<p><img src="http://images.gitbook.cn/815813e0-7604-11e8-9c7a-43197c8c6da2" alt="" /></p>
<h5 id="-10">　<strong>点赞操作</strong></h5>
<p><strong>1.</strong> 页面点击事件。</p>
<p>在之前写好的 reply 函数内有回复的点击事件：</p>
<pre><code>    &lt;a onclick='reply_up("+this.id+")' style='cursor:pointer' class='date-dz-z pull-left' id='change_color_"+this.id+"'&gt;&lt;i class='date-dz-z-click-red'&gt;&lt;/i&gt;赞 (&lt;i class='z-num' id='comment_upvote_"+this.id+"'&gt;"+this.upvote+"&lt;/i&gt;)&lt;/a&gt;
</code></pre>
<p>这里的点击事件 <code>reply_up</code> 函数内接收一个参数：评论id，具体点击事件方法如下：</p>
<pre><code>    //点赞
    function reply_up(id) {
        var num = document.getElementById("comment_upvote_"+id).innerHTML;
        if($("#change_color_"+id).is('.date-dz-z-click')){
            num--;
            $("#change_color_"+id).removeClass('date-dz-z-click red');
            $("#change_color_"+id).find('.z-num').html(num);
            $("#change_color_"+id).find('.date-dz-z-click-red').removeClass('red');

        }else {
            num++;
            $("#change_color_"+id).addClass('date-dz-z-click');
            $("#change_color_"+id).find('.z-num').html(num);
            $("#change_color_"+id).find('.date-dz-z-click-red').addClass('red');
        }

        $.ajax({
            type:'post',
            url:'/comment',
            data: {"id":id,"upvote":num},
            dataType:'json',
            success:function(data){
                var comm_data =  data["data"];
                if(comm_data=="fail"){
                    window.location.href = "/login.jsp";
                }
            }
        });
    }
</code></pre>
<p>代码解读：</p>
<p>（1）获取点赞数赋值给 num。</p>
<p>（2）如果已经点赞，再次点击则点赞数-1，移除文字和点赞红心效果。</p>
<p>（3）如果没有点赞，或取消赞后再次点击，则点赞数+1，添加文字和点赞红心效果。</p>
<p>（4）发送 AJAX 请求，请求 URL 为 <code>/comment</code>，请求参数为评论 id 和点赞数。</p>
<pre><code>data: {"id":id,"upvote":num}
</code></pre>
<p>（5）数据类型为 JSON 格式。</p>
<p>（6）success 回调函数，如果返回的数据是 fail 则返回到登录页面。</p>
<p><strong>2.</strong> 后台 IndexJspController.java 代码，就是之前的 comment 方法，如果评论 id 不为 null 则使用下面的代码：</p>
<pre><code>      //点赞
      Comment c = commentService.findById( id );
      c.setUpvote( upvote );
      commentService.update( c );
</code></pre>
<p>根据评论 id 查找 Comment 对象，更新评论数。</p>
<p><strong>3.</strong> 重新启动程序，点击点赞效果如下：</p>
<p><img src="http://images.gitbook.cn/e1bd6540-7605-11e8-9def-35cb75b6091c" alt="" /></p>
<p>如果再次点击，则红心效果消失，点赞数为0，每次刷新网页点赞数可累加。</p>
<h4 id="-11">评论块的评论操作</h4>
<p><img src="http://images.gitbook.cn/f31b3240-7605-11e8-b9a0-850e12cc69e8" alt="" /></p>
<p>输入回复内容后点击回复按钮，评论按钮的点击事件在之前写的创建回复块的 <code>comment_hf</code> 函数内：</p>
<pre><code>    &lt;a id="comment_pl_'+comment_id+'" onclick="comment_pl('+content_id+','+comment_id+','+fid+','+by_id+','+cuid+')" class="hf-pl" style="color: white;cursor:pointer"&gt;评论&lt;/a&gt;
</code></pre>
<p>onclick 点击事件 <code>comment_pl</code> 函数，需要传入的参数有5个，分别是：文章 id、评论 id、一级评论 id、被评论者 id和评论者 id。<code>comment_pl</code> 函数具体方法如下：</p>
<pre><code>    //点击一级评论块的评论按钮
    function comment_pl(content_id,comment_id,fid,by_id,cuid) {
        if(fid==null){
            fid = comment_id
        }
        var oThis = $("#comment_pl_"+comment_id);
        var myDate = new Date();
        //获取当前年
        var year=myDate.getFullYear();
        //获取当前月
        var month=myDate.getMonth()+1;
        //获取当前日
        var date=myDate.getDate();
        var h=myDate.getHours();       //获取当前小时数(0-23)
        var m=myDate.getMinutes();     //获取当前分钟数(0-59)
        if(m&lt;10) m = '0' + m;
        var s=myDate.getSeconds();
        if(s&lt;10) s = '0' + s;
        var now=year+'-'+month+"-"+date+" "+h+':'+m+":"+s;
        //获取输入内容
        var oHfVal = oThis.siblings('.flex-text-wrap').find('.comment-input').val();
        console.log(oHfVal)
        var oHfName = oThis.parents('.hf-con').parents('.date-dz').siblings('.pl-text').find('.comment-size-name').html();
        //alert(oHfName)
        var oAllVal = '回复@'+oHfName;

        if(oHfVal.replace(/^ +| +$/g,'') == '' || oHfVal == oAllVal){

        }else {
            $.ajax({
                type:'post',
                url:'/comment_child',
                data: {"content_id":content_id,"uid":'${user.id}',"oSize":oHfVal,"comment_time":now,"by_id":by_id,"id":fid},
                dataType:'json',
                success:function(data){
                    var comm_data =  data["data"];
                    //alert(comm_data);
                    if(comm_data=="fail"){
                        window.location.href = "/login.jsp";
                    }else {
                        var id = comm_data.id;
                        //alert(id)
                        var oAt = '回复&lt;a class="atName"&gt;@'+oHfName+'&lt;/a&gt;  '+oHfVal;
                        var oHtml = '&lt;div class="all-pl-con"&gt;&lt;div class="pl-text hfpl-text clearfix"&gt;&lt;a class="comment-size-name"&gt;${user.nickName} : &lt;/a&gt;&lt;span class="my-pl-con"&gt;'+oAt+'&lt;/span&gt;&lt;/div&gt;&lt;div class="date-dz"&gt; &lt;span class="date-dz-left pull-left comment-time"&gt;'+now+'&lt;/span&gt; &lt;div class="date-dz-right pull-right comment-pl-block"&gt; &lt;a style="cursor:pointer" onclick="deleteComment('+content_id+','+cuid+','+id+','+fid+')" id="comment_dl_'+id+'" class="removeBlock"&gt;删除&lt;/a&gt; &lt;a onclick="comment_hf('+content_id+','+id+','+fid+','+comm_data.user.id+','+cuid+')" id="comment_hf_'+id+'" style="cursor:pointer" class="date-dz-pl pl-hf hf-con-block pull-left"&gt;回复&lt;/a&gt; &lt;span class="pull-left date-dz-line"&gt;|&lt;/span&gt; &lt;a onclick="reply_up('+id+')" id="change_color_'+id+'" style="cursor:pointer" class="date-dz-z pull-left"&gt;&lt;i class="date-dz-z-click-red"&gt;&lt;/i&gt;赞 (&lt;i class="z-num" id="comment_upvote_'+id+'"&gt;0&lt;/i&gt;)&lt;/a&gt; &lt;/div&gt; &lt;/div&gt;&lt;/div&gt;';
                        $("#comment_pl_"+comment_id).parents('.hf-con').parents('.comment-show-con-list').find('.hf-list-con').css('display','block').prepend(oHtml) &amp;&amp; oThis.parents('.hf-con').siblings('.date-dz-right').find('.pl-hf').addClass('hf-con-block') &amp;&amp; oThis.parents('.hf-con').remove();

                        var num = document.getElementById("comment_num_"+content_id).innerHTML;
                        document.getElementById("comment_num_"+content_id).innerHTML = (parseInt(num) + 1)+"";
                    }
                }
            });
        }
    }
</code></pre>
<p>代码解读：</p>
<p>（1）判断一级评论 fid 是否为 null，为 null 则把评论 <code>id(comment_id)</code> 赋值给 fid，即当前评论 id 就是一级评论 id。</p>
<p>（2）获取评论的时间，赋值给 now。</p>
<p>（3）获取评论内容，赋值给 oHfVal。</p>
<p>（4）获取被回复者名字，赋值给 oHfName。</p>
<p>（5）如果回复内容为空，点击评论无效。</p>
<p>（6）回复内容不为空，发送  AJAX 请求，请求参数为：</p>
<pre><code>      data: {"content_id":content_id,"uid":'${user.id}',"oSize":oHfVal,"comment_time":now,"by_id":by_id,"id":fid},
</code></pre>
<p>分别是：文章 id、评论用户 id、回复内容 oHfVal、评论时间 now、被评论者 id和一级评论 id。</p>
<p>（7）success 回调函数将返回数据取出赋值给 <code>comm_data</code>，如果是 fail 则跳转到登录页面，否则创建评论块赋值给 oHtml，然后添加在第一行。</p>
<p>（8）获取评论数，将评论数+1，赋值到页面上。</p>
<p>Java后台 IndexJspController.java 对应的方法如下：</p>
<pre><code>    @RequestMapping("/comment_child")
    @ResponseBody
    public Map&lt;String,Object&gt; addCommentChild(Model model, @RequestParam(value = "id",required = false) Long id ,
                                              @RequestParam(value = "content_id",required = false) Long content_id ,
                                              @RequestParam(value = "uid",required = false) Long uid ,
                                              @RequestParam(value = "by_id",required = false) Long bid ,
                                              @RequestParam(value = "oSize",required = false) String oSize,
                                              @RequestParam(value = "comment_time",required = false) String comment_time,
                                              @RequestParam(value = "upvote",required = false) Integer upvote) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        if(user == null){
            map.put( "data","fail" );
            return map;
        }

        Date date = DateUtils.StringToDate( comment_time, "yyyy-MM-dd HH:mm:ss" );

        Comment comment = new Comment();
        comment.setComContent( oSize );
        comment.setCommTime( date );
        comment.setConId( content_id );
        comment.setComId( uid );
        if(upvote==null){
            upvote = 0;
        }
        comment.setById( bid );
        comment.setUpvote( upvote );
        User u = userService.findById( uid );
        comment.setUser( u );
        commentService.add( comment );

        Comment com = commentService.findById( id );
        if(StringUtils.isBlank( com.getChildren() )){
            com.setChildren( comment.getId().toString() );
        }else {
            com.setChildren( com.getChildren()+","+comment.getId() );
        }
        commentService.update( com );
        map.put( "data",comment );

        UserContent userContent = userContentService.findById( content_id );
        Integer num = userContent.getCommentNum();
        userContent.setCommentNum( num+1 );
        userContentService.updateById( userContent );
        return map;

    }
</code></pre>
<p>代码解读：</p>
<p>（1）从 Session 中取出用户信息，判断用户是否登录，未登录，则返回 fail。</p>
<p>（2）将日期字符串转成自定义格式的日期 Date，如果 upvote 为 null，则赋初始值0，将 comment 信息设置完毕之后插入数据库，返回主键 id，此时该 comment 中 id 是有值的。</p>
<p>（3）根据评论 id 查询出评论对象 com，判断该评论对象 com 是否有子评论，如果没有，将刚才添加的子评论 id 添加到 Comment 的 children 字段中。</p>
<p>（4）如果该评论对象 com 已有子评论了，则将刚才添加的子评论的 id 以逗号形式拼接在子评论 id 后面。</p>
<p>（5）更新该评论对象 com。</p>
<p>（6）将评论对象 comment 放入 map。</p>
<p>（7）根据文章 id 查询出文章对象 userContent，获取评论数，将其值加1，更新 userContent。</p>
<p>（8）最后将 map 返回给页面。</p>
<p>重新启动项目，点击评论块的评论按钮，查看效果如下：</p>
<p><img src="http://images.gitbook.cn/b9789950-7606-11e8-9def-35cb75b6091c" alt="" /></p>
<p>到这里评论回复模块就讲完了，主要注意点击事件内接收的参数，容易弄混。</p>
<blockquote>
  <p>第09课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1gFBhVTlPvKxm77zyMTL1jQ 密码：en41</p>
</blockquote></div></article>