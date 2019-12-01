---
title: SSM 博客系统开发实战-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>个人主页主要包括左侧的个人信息展示、梦分类和右侧的博客管理和热梦推荐四大模块。</p>
<h3 id="">个人信息展示</h3>
<p><img src="http://images.gitbook.cn/ef5e3d50-7952-11e8-b70e-bb13c5652b61" alt="" /></p>
<p>主要根据 EL 表达式 <code>${}</code> 取出用户的昵称、头像等信息，展示在页面，代码如下：</p>
<pre><code>&lt;div class="avatar-container-80 center"&gt;
    &lt;a href="#" title="${user.nickName}" class="avatar" target="_blank"&gt;
        &lt;img src="${user.imgUrl}" width="80" height="80" alt=""&gt;
    &lt;/a&gt;
&lt;/div&gt;
</code></pre>
<p>这里除了昵称和头像是从后台动态获取的，其他的都是死数据。由于时间
关系，这里不做实现了，同学们应该可以自行完成（没有的字段，需要
添加字段或者新建表）。</p>
<h3 id="-1">梦分类</h3>
<p>登录成功后，之前是直接跳转到 personal.jsp 页面，现在需要修改一下，让用户登录成功之后，先经过一个 Controller，将我们需要的信息查询出来之后再跳转到 personal.jsp 页面。在 LoginController.java 的 doLogin 方法中将两处以下代码：</p>
<pre><code>     return "/personal/personal";
</code></pre>
<p>都改成：</p>
<pre><code>    return "redirect:/list";
</code></pre>
<p><code>redirect:/list</code> 意思是重定向到 Controller 中 url 映射为 <code>/list</code>的方法上（用 forward 转发也可以）。</p>
<p>接着，我们需要根据梦分类名称和用户 id 进行分页查询，根据 category 进行分组查询，分组查询需要手写 XML。首先在 UserContentService.java 中增加两个查询方法：</p>
<pre><code>    /**
     * 根据用户id查询出梦分类
     * @param uid
     * @return
     */
    List&lt;UserContent&gt; findCategoryByUid(Long uid);

     /**
     * 根据文章分类查询所有文章
     * @param category
     *  @param pageNum
     * @param pageSize
     * @return
     */
    PageHelper.Page&lt;UserContent&gt; findByCategory(String category, Long uid ,Integer pageNum, Integer pageSize);
</code></pre>
<p>在实现类 UserContentServiceImpl.java 中实现上述方法：</p>
<pre><code>    @Override
    public List&lt;UserContent&gt; findCategoryByUid(Long uid) {
        return userContentMapper.findCategoryByUid(uid);
    }

     @Override
    public Page&lt;UserContent&gt; findByCategory(String category,Long uid,Integer pageNum, Integer pageSize) {
        UserContent userContent = new UserContent();
        if(StringUtils.isNotBlank(category) &amp;&amp; !"null".equals(category)){
            userContent.setCategory(category);
        }
        userContent.setuId(uid);
        userContent.setPersonal("0");
        PageHelper.startPage(pageNum, pageSize);//开始分页
        userContentMapper.select(userContent);
        Page endPage = PageHelper.endPage();//分页结束
        return endPage;
    }
</code></pre>
<p>分页查询方法 findByCategory 中，如果分类名称 category 为空或者是 null 字符串时则查询所有分类，userContent.setPersonal("0") 表示查询出非私密的文章。</p>
<p>之后，分组查询方法 findCategoryByUid 需要在 UserContentMapper.java 中创建 findCategoryByUid 方法，参数为用户 ID（UID）：</p>
<pre><code>    public interface UserContentMapper extends Mapper&lt;UserContent&gt; {
    /**
     * 根据用户id查询出梦分类
     * @param uid
     * @return
     */
    List&lt;UserContent&gt; findCategoryByUid(@Param("uid")long uid);
    }
</code></pre>
<p>在 <code>resources/mapping/</code> 下新建对应的 userContent.xml 文件:</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
    &lt;!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt;
    &lt;mapper namespace="wang.dreamland.www.dao.UserContentMapper"&gt;

    &lt;select id="findCategoryByUid"  resultMap="categoryMap"&gt;
        select category,count(1) as num from user_content where u_id = #{uid} and personal = '0' group by category order by num desc
    &lt;/select&gt;

    &lt;resultMap type="wang.dreamland.www.entity.UserContent" id="categoryMap"&gt;
        &lt;!-- property 表示wang.dreamland.www.entity.UserContent； column 表示表中的列名 --&gt;
        &lt;id property="id" column="id" /&gt;
        &lt;result property="category" column="category" /&gt;
        &lt;result property="num" column="num" /&gt;
    &lt;/resultMap&gt;
    &lt;/mapper&gt;
</code></pre>
<p>这里 group by category 是根据 category 分组，order by num desc 是根据查询分类的数量 num 降序排列。</p>
<p>因为我们只要查询梦分类和数量，所以只要查两个字段就可以了，一个是 category 分类名称，另一个是分类数量 num，count(1) 就是分类的数量，num 是起的别名。将数量赋值给 num。</p>
<pre><code>     &lt;result property="num" column="num" /&gt;
</code></pre>
<p>上面的 result 标签意思是对应的实体属性是 num，表中字段是 num，表中已经起了别名了，有了 num 字段，可是实体类中并没有 num 属性，所以这里要在 UserContent 实体类中加上 num 属性，并生成 setter 和 getter 方法：</p>
<pre><code>    @Transient
    private  Integer num;

    public Integer getNum() {
        return num;
    }

    public void setNum(Integer num) {
        this.num = num;
    }
</code></pre>
<p>这样查询语句和 XML 就写好了。可以供 Controller 进行调用了。</p>
<p>紧接着，在 controller 包下新建 PersonalController.java 并继承 BaseController，别忘记加 <code>@Controller</code> 注解，表示是 Controller 层，具体方法如下：</p>
<pre><code>    @Controller
    public class PersonalController extends BaseController{
    private final static Logger log = Logger.getLogger(PersonalController.class);
    @Autowired
    private UserContentService userContentService;
    /**
     * 初始化个人主页数据
     * @param model
     * @param id
     * @param pageNum
     * @param pageSize
     * @return
     */
    @RequestMapping("/list")
    public String findList(Model model, @RequestParam(value = "id",required = false) String id,
                           @RequestParam(value = "pageNum",required = false) Integer pageNum ,
                           @RequestParam(value = "pageSize",required = false) Integer pageSize) {
        User user = (User)getSession().getAttribute("user");
        UserContent content = new UserContent();
        UserContent uc = new UserContent();
        if(user!=null){
            model.addAttribute( "user",user );
            content.setuId( user.getId() );
            uc.setuId(user.getId());
        }else{
            return "../login";
        }
        log.info("初始化个人主页信息");
        //查询梦分类
        List&lt;UserContent&gt; categorys = userContentService.findCategoryByUid(user.getId());
        model.addAttribute( "categorys",categorys );
        //发布的梦 不含私密梦
        content.setPersonal("0");
        pageSize = 4; //默认每页显示4条数据
        PageHelper.Page&lt;UserContent&gt; page =  findAll(content,pageNum,  pageSize); //分页

        model.addAttribute( "page",page );

        //查询私密梦
        uc.setPersonal("1");
        PageHelper.Page&lt;UserContent&gt; page2 =  findAll(uc,pageNum,  pageSize);
        model.addAttribute( "page2",page2 );

        //查询热梦
        UserContent uct = new UserContent();
        uct.setPersonal("0");      
        PageHelper.Page&lt;UserContent&gt; hotPage =  findAllByUpvote(uct,pageNum,  pageSize);
        model.addAttribute( "hotPage",hotPage );
        return "personal/personal";
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）获取 PersonalController 类的 log 对象，可进行日志打印。</p>
<p>（2）通过 Autowired 注解注入 userContentService 对象，可调用其对象中的查询方法。</p>
<p>（3）从 Session 获取用户信息判断用户是否登录，未登录则跳转登录，已登录则将信息存入 Model 中。</p>
<p>（4）log.info("初始化个人主页信息")，用来打印日志信息。</p>
<p>（5）根据用户 ID 查询梦分类（不包含私密梦），将查询结果放入 Model。</p>
<p>（6）查询所有梦（不含私密梦）并分页，且默认每页显示4条数据（主要用于测试分页），将其放入 Model。</p>
<p>（7）查询所有私密梦并分页，且默认每页显示4条数据（主要用于测试分页），将其放入 Model。</p>
<p>（8）查询热梦，根据用户点赞数降序排列并分页，且默认每页显示4条数据（主要用于测试分页），将其分页结果放入 Model。</p>
<p>（9）返回到 personal.jsp 页。</p>
<p>再接下来，我们写出 personal.jsp 页面的梦分类模块 div 中的代码：</p>
<pre><code>        &lt;div class="dreamland-diff"&gt;
        &lt;div class="customer" style="height: 40px;background-color:#262626;line-height: 40px "&gt;
            &lt;font color="white" size="2.8" face="黑体" style="margin-top: 10px;margin-left: 10px"&gt;梦分类&lt;/font&gt;
        &lt;/div&gt;
        &lt;div class="list-group"&gt;
            &lt;a onclick="changeToActive('category_x',null,null)" class="list-group-item active" id="category_x"&gt;全部(${page.total})&lt;/a&gt;
            &lt;c:forEach items="${categorys}" var="category" varStatus="sta"&gt;
                &lt;a onclick="changeToActive('category_${sta.index}','${category.category}',null)" class="list-group-item" id="category_${sta.index}"&gt;${category.category}(${category.num})&lt;/a&gt;
            &lt;/c:forEach&gt;

        &lt;/div&gt;
    &lt;/div&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）分类列表选中状态默认为“全部”，即包含所有分类，它的 ID 用 <code>category_x</code> 标识，数量就是分页查询的总数量，通过 EL 表达式 <code>${page.total}</code> 获取。</p>
<p>（2）通过 <code>&lt;c:forEach&gt;</code> 标签进行迭代，遍历出每一个 UserContent，其中 items 接收集合，通过 EL 表达式 <code>${categorys}</code> 获取我们存入 Model 中的集合 categorys，var 接收的是集合中的每一个元素，即每一个 UserContent，赋值给 category，varStatus 接收当前遍历状态，赋值给 sta，然后通过 <code>${sta.index}</code> 就可以获取下标，下标从0开始。</p>
<p>（3）通过 <code>${category.category}</code> 取出分类名称，通过 <code>${category.num}</code> 取出该分类数量，将 <code>category_</code> 和 下标 <code>${sta.index}</code> 组合成唯一 ID。</p>
<pre><code>    id="category_${sta.index}"
</code></pre>
<p>梦分类效果如下图（默认“全部”是选中状态且按数量降序）：</p>
<p><img src="http://images.gitbook.cn/5812ac80-7955-11e8-8c9c-d1cbf75a4c88" alt="" /></p>
<p>（4）每个列表的 onclick 点击事件如下:</p>
<pre><code>    onclick="changeToActive('category_x',null,null)"//默认的全部列表a标签中的onclick

    onclick="changeToActive('category_${sta.index}','${category.category}',null)"//循环遍历出的其他a标签中的onclick
</code></pre>
<p>changeToActive 函数接收三个参数：该 a 标签的 id，分类名称和页码。</p>
<p>其中“全部”列表 a 标签的分类名称为 null，代表查询所有，页码都为 null，代表默认页码为1。</p>
<p>我们接着写列表的点击事件函数 changeToActive，具体方法如下：</p>
<pre><code>    //梦分类点击事件
     function changeToActive(id,category,pageNum) {
       var ulist_id = "";
       if(typeof (id)=="object"){
           ulist_id = id.id;
       }else{
           ulist_id = id;
       }
       $("ul").remove("#release-dreamland-ul");
       $("ul").remove("#release-dreamland-fy");
       $(".list-group-item").attr("class","list-group-item");
       $("#"+ulist_id).attr("class","list-group-item active");
       $.ajax({
           type: 'post',
           url: '/findByCategory',
           data: {"category": category,"pageNum":pageNum},
           dataType: 'json',
           success: function (data) {
               var pageCate = data["pageCate"];
               if(pageCate=="fail"){
                   window.location.href = "/login.jsp";
               }else{

               var ucList = pageCate.result;
               var startHtml = "&lt;ul style='font-size: 12px' id='release-dreamland-ul'&gt;";
               var endHtml = "&lt;/ul&gt;";
               if(ucList!=null){
                  $(ucList).each(function () {
                      var contHtml = "&lt;li class='dreamland-fix'&gt;&lt;a&gt;"+this.title+"&lt;/a&gt; &lt;span class='bar-read'&gt;评论 ("+this.commentNum+")&lt;/span&gt;"
                          +"&lt;span class='bar-commend'&gt;"+this.upvote+"人阅读&lt;/span&gt;&lt;hr/&gt;&lt;/li&gt;";
                      startHtml = startHtml + contHtml;
                  });
                var okHtml = startHtml + endHtml;

                //分页
                var stPageHtml = " &lt;ul id='release-dreamland-fy' class='pager pager-loose'&gt;";
                if(pageCate.pageNum&lt;=1){
                    stPageHtml = stPageHtml + " &lt;li class='previous'&gt;&lt;a href='javascript:void(0);'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                }else if(pageCate.pageNum&gt;1){
                    var num = parseInt(pageCate.pageNum) -1;
                     stPageHtml = stPageHtml + "&lt;li class='previous'&gt;&lt;a onclick='changeToActive("+ulist_id+",\""+category+"\","+num+")'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                }

                var foHtml = "";
                for(var i = 1 ;i&lt;= pageCate.pages;i++){
                    if(pageCate.pageNum==i){
                        foHtml = foHtml+ "&lt;li class='active'&gt;&lt;a href='javascript:void(0);'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                    }else{
                        foHtml = foHtml+ "&lt;li &gt;&lt;a onclick='changeToActive("+ulist_id+",\""+category+"\","+i+")'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                    }
                }

                 var teHtml = "";
                 if(pageCate.pageNum&gt;=pageCate.pages){
                     teHtml = " &lt;li&gt;&lt;a href='javascript:void(0);'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                 }else if(pageCate.pageNum&lt;pageCate.pages){
                     var num = parseInt(pageCate.pageNum) + 1;
                        teHtml = "&lt;li&gt;&lt;a onclick='changeToActive("+ulist_id+",\""+category+"\","+num+")'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                 }
                var endPageHtml = "&lt;/ul&gt;";

               var pageOkHtml = stPageHtml + foHtml + teHtml +endPageHtml;
               }

               $("#release-dreamland").append(okHtml);
               $("#release-dreamland-div").append(pageOkHtml);
           }
           }

       });
    }
</code></pre>
<p>代码解读：</p>
<p>（1）定义一个空变量 <code>ulist_id</code>，如果 id 类型为 object 时，将 <code>id.id</code> 赋值给 <code>ulist_id</code>，否则将 id 赋值给 <code>ulist_id</code>。</p>
<p>（2）每次点击梦分类列表项时，先移除右侧的“发布的梦”模块的内容，包括文章主题列表和分页，因为移除的是 ul 标签，所以通过 ul 的 jQuery 对象 <code>$("ul").remove</code> 方法移除指定 id 的 ul 标签。</p>
<p>（3）获取 class 属性为 <code>list-group-item</code> 的所有对象，将其属性设置为普通状态，即没有背景色。</p>
<p>（4）通过传进来的列表 id（即 <code>ulist_id</code>），获取该列表对象，将其属性设置为激活状态，即设置背景色，这样就可以实现点击变色了。</p>
<p>（5）发送 AJAX 请求，请求参数为 category 分类名称和 pageNum 页码，请求 url 为：<code>/findByCategory</code>。</p>
<pre><code>    data: {"category": category,"pageNum":pageNum}
</code></pre>
<p>（6）success 回调函数返回查询分页结果，将结果取出赋值给 pageCate，如果 <code>pageCate==fail</code> 则跳转登录页面。</p>
<p>（7）如果不是 fail，则通过 pageCate.result 就可以获取文章集合，赋值给 ucList。</p>
<p>（8）之前把右边模块的 ul 标签已经移除，这里需要动态创建，先把 ul 标签的开始标签和结束标签写好后分别赋值给 startHtml 和 endHtml。</p>
<p>（9）判断如果 ucList 不为 null，则对其进行遍历，动态创建每一个 li 标签，并赋值给变量 contHtml，然后和开始标签进行拼接：<code>startHtml = startHtml + contHtml;</code>。</p>
<p>（10）最后定义变量 okHtml，将已经拼接好后的 startHtml 和 endHtml 进行拼接，即：<code>okHtml = startHtml + endHtml;</code>，这样文章列表标签 ul 就创建完成了。</p>
<p>（11）之后是创建分页标签 ul，先定义开始 ul 的开始标签 stPageHtml，然后根据 pageNum 判断当前页是 &gt;1 还是 &lt;=1 来生成可点击或不可点击的上一页，然后将其拼接在开始标签 stPageHtml 后面。</p>
<p>（12）定义一个空变量 foHtml，用于接收 for 循环中生成的分页 HTML，其中 pageCate.pages 就是总页数，如果当前页 pageNum 等于循环的 i 时，则该页为选中状态，其他页为未选中状态。</p>
<p>（13）定义一个空变量 teHtml，然后根据 pageNum 判断当前页是 &gt;= 总页数还是 &lt; 总页数来生成不可点击的或可点击的下一页。</p>
<p>（14）定义变量 endPageHtml 来接收 ul 的结束标签。</p>
<p>（15）定义变量 pageOkHtml，将分页的各部分变量进行拼接，即：</p>
<pre><code>    pageOkHtml = stPageHtml + foHtml + teHtml +endPageHtml;
</code></pre>
<p>这样分页的 ul 标签就创建完成了。</p>
<p>（16）最后将文章标题的 ul 标签 okHtml 和分页的 ul 标签 pageOkHtml 动态的添加到相应的 div 中：</p>
<pre><code>       $("#release-dreamland").append(okHtml);
       $("#release-dreamland-div").append(pageOkHtml);
</code></pre>
<p>以上完成后，我们再来完成 Java 后台 PersonalController 中映射 <code>url:/findByCategory</code> 的方法：</p>
<pre><code>    /**
     * 根据分类名称查询所有文章
     * @param model
     * @param category
     * @return
     */
    @RequestMapping("/findByCategory")
    @ResponseBody
    public Map&lt;String,Object&gt; findByCategory(Model model, @RequestParam(value = "category",required = false) String category,@RequestParam(value = "pageNum",required = false) Integer pageNum ,
                                             @RequestParam(value = "pageSize",required = false) Integer pageSize) {

        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        if(user==null) {
            map.put("pageCate","fail");
            return map;
        }
        pageSize = 4; //默认每页显示4条数据
        PageHelper.Page&lt;UserContent&gt; pageCate = userContentService.findByCategory(category,user.getId(),pageNum,pageSize);
        map.put("pageCate",pageCate);
        return map;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 中获取用户信息，如果为 null，则返回 fail。</p>
<p>（2）设置每页显示4条数据，主要是为了演示分页效果。</p>
<p>（3）根据分类名称、用户 ID、页码和每页显示记录数查询出分页数据，存入 map 中。</p>
<p>（4）返回 map。</p>
<p>重新启动项目，点击分类列表效果如下：</p>
<p><img src="http://images.gitbook.cn/deeca840-7956-11e8-8985-b17fa96df47a" alt="" /></p>
<p><img src="http://images.gitbook.cn/e67d7490-7956-11e8-b06c-81deae508e47" alt="" /></p>
<p>AJAX 异步请求的优点之一便是点击分页的时候不会刷新整个页面，而是局部数据刷新。</p>
<h3 id="-2">博客管理</h3>
<p>关注和被关注模块这里没有实现，都是死数据，有兴趣的同学可以自己实现下。</p>
<p>右侧的博客管理模块如图：</p>
<p><img src="http://images.gitbook.cn/11792db0-7957-11e8-b06c-81deae508e47" alt="" /></p>
<p>这里的“发布的梦”已经实现了。现在要做的是：通过点击不同的 div 切换不同的内容，比如点击“管理梦”，则“管理梦”为选中状态，背景色为红色，其他为未选中状态，同时下面显示管理梦相关信息。实现方式主要是通过点击事件将选中的选项显示，其他选项隐藏。</p>
<p>“管理梦”列表的 div 代码如下：</p>
<pre><code>             &lt;div id="update-dreamland" style="height: 700px;margin-top: 50px;width: 100%;display: none" &gt;
            &lt;ul style="font-size: 12px" id="update-dreamland-ul"&gt;
                &lt;c:forEach var="cont" items="${page.result}" varStatus="i"&gt;
                &lt;li class="dreamland-fix"&gt;
                    &lt;a&gt;${cont.title}&lt;/a&gt;
                    &lt;span class="bar-delete"&gt;删除&lt;/span&gt;
                    &lt;span class="bar-update"&gt;修改&lt;/span&gt;


                    &lt;hr/&gt;
                &lt;/li&gt;
                &lt;/c:forEach&gt;

            &lt;/ul&gt;


            &lt;div style="float: left;position: absolute;bottom: 1080px;margin-left: 20px" id="update-dreamland-div"&gt;
                &lt;ul class="pager pager-loose" id="update-dreamland-fy"&gt;
                    &lt;c:if test="${page.pageNum &lt;= 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a href="javascript:void(0);"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum &gt; 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a onclick="turnPage(${page.pageNum-1})"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:forEach begin="1" end="${page.pages}" var="pn"&gt;
                        &lt;c:if test="${page.pageNum==pn}"&gt;
                            &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                        &lt;c:if test="${page.pageNum!=pn}"&gt;
                            &lt;li &gt;&lt;a onclick="turnPage(${pn})"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                    &lt;/c:forEach&gt;

                    &lt;c:if test="${page.pageNum&gt;=page.pages}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum&lt;page.pages}"&gt;
                        &lt;li&gt;&lt;a onclick="turnPage(${page.pageNum+1})"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;

                &lt;/ul&gt;

            &lt;/div&gt;
        &lt;/div&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>&lt;c:forEach&gt;</code> 遍历得到每一个列表标签 li，其中 items 等属性之前已经说过，这里不再赘述。</p>
<p>（2）就是分页，根据当前页判断上一页是否可点击。</p>
<p>（3）通过 <code>&lt;c:forEach&gt;</code> 遍历总页数，属性 begin 代表从1开始，end 属性代表到总页数结束，var 设置变量 pn，通过 <code>${pn}</code> 可获得遍历的当前值，如果遍历的当前值等于当前页，则当前页为选中状态，否则为未选中状态。</p>
<p>（4）根据当前页判断下一页是否可点击.</p>
<p>“管理梦”分页的点击事件为 turnPage，传入的参数是需要跳转的页码，具体方法如下：</p>
<pre><code>    //管理梦分页点击事件
    function turnPage(pageNum) {
        $("ul").remove("#update-dreamland-ul");
        $("ul").remove("#update-dreamland-fy");
        $.ajax({
            type: 'post',
            url: '/findByCategory',
            data: {"pageNum": pageNum},
            dataType: 'json',
            success: function (data) {
                var pageCate = data["pageCate"];
                if(pageCate=="fail"){
                    window.location.href = "/login.jsp";
                }else{
                    var ucList = pageCate.result;
                    var startHtml = " &lt;ul style='font-size: 12px' id='update-dreamland-ul'&gt;";
                    var endHtml = "&lt;/ul&gt;";
                    if(ucList!=null) {
                        $(ucList).each(function () {
                            var contHtml = " &lt;li class='dreamland-fix'&gt; &lt;a&gt;"+this.title+"&lt;/a&gt; &lt;span class='bar-delete'&gt;删除&lt;/span&gt;"
                                +"&lt;span class='bar-update'&gt;修改&lt;/span&gt;&lt;hr/&gt;&lt;/li&gt;";
                            startHtml = startHtml + contHtml;
                        });
                        var okHtml = startHtml + endHtml;

                        //分页
                        var stPageHtml = "&lt;ul class='pager pager-loose' id='update-dreamland-fy'&gt;";
                        if(pageCate.pageNum&lt;=1){
                            stPageHtml = stPageHtml + "  &lt;li class='previous'&gt;&lt;a href='javascript:void(0);'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                        }else if(pageCate.pageNum&gt;1){
                            var num = parseInt(pageCate.pageNum) -1;
                            stPageHtml = stPageHtml + "&lt;li class='previous'&gt;&lt;a onclick='turnPage("+num+")'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                        }

                        var foHtml = "";
                        for(var i = 1 ;i&lt;= pageCate.pages;i++){
                            if(pageCate.pageNum==i){
                                foHtml = foHtml+ "  &lt;li class='active'&gt;&lt;a href='javascript:void(0);'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                            }else{
                                foHtml = foHtml+ "&lt;li &gt;&lt;a onclick='turnPage("+i+")'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                            }
                        }

                        var teHtml = "";
                        if(pageCate.pageNum&gt;=pageCate.pages){
                            teHtml = " &lt;li&gt;&lt;a href='javascript:void(0);'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                        }else if(pageCate.pageNum&lt;pageCate.pages){
                            var num = parseInt(pageCate.pageNum) + 1;
                            teHtml = "&lt;li&gt;&lt;a onclick='turnPage("+num+")'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                        }
                        var endPageHtml = "&lt;/ul&gt;";

                        var pageOkHtml = stPageHtml + foHtml + teHtml +endPageHtml;
                    }

                    $("#update-dreamland").append(okHtml);
                    $("#update-dreamland-div").append(pageOkHtml);
                }
            }
        });
    }
</code></pre>
<p>该方法和梦分类点击事件大同小异。请参考梦分类点击事件的代码解读。</p>
<p>“管理梦”选项的 div 代码如下:</p>
<pre><code>     &lt;div id="manage-dreamland" style="background-color: #F0F0F0;width: 120px;text-align: center;height: 40px;line-height: 40px;float: left;margin-left: 20px" onclick="manage_dreamland();"&gt;

                &lt;span id="manage-span" style="color: black"&gt;管理梦&lt;/span&gt;

      &lt;/div&gt;
</code></pre>
<p>该 div 的 onclick 事件方法 <code>manage_dreamland()</code>的具体代码如下：</p>
<pre><code>     //管理梦点击事件
     function manage_dreamland() {
        document.getElementById("fa-dreamland").style.backgroundColor = "#F0F0F0";
        document.getElementById("fa-span").style.color = "black";

        document.getElementById("personal-div").style.backgroundColor = "#F0F0F0";
        document.getElementById("personal-span").style.color = "black";

        document.getElementById("manage-dreamland").style.backgroundColor = "#B22222";
        document.getElementById("manage-span").style.color = "white";

        document.getElementById("release-dreamland").style.display = "none";
        document.getElementById("personal-dreamland").style.display = "none";
        document.getElementById("update-dreamland").style.display = "";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）根据 id 获取“发布梦”选项的 div 对象，将其背景色设置为白色，字体颜色设置为黑色。</p>
<p>（2）根据 id 获取“私密梦”选项的 div 对象，将其背景色设置为白色，字体颜色设置为黑色。</p>
<p>（3）根据 id 获取“管理梦”选项的 div 对象，将其背景色设置为红色，字体颜色设置为白色。</p>
<p>（4）根据 id 获取“发布梦”列表的 div 对象，将 display 属性设置 none，将其隐藏。</p>
<p>（5）根据 id 获取“私密梦”列表的 div 对象，将 display 属性设置 none，将其隐藏。</p>
<p>（6）根据 id 获取“管理梦”列表的 div 对象，将 display 属性设置为<code>""</code>，将其显示。</p>
<p>“发布梦”和“私密梦”选项的点击事件和上面的点击事件类似，不再赘述。直接给出代码：</p>
<pre><code>    //发布梦点击事件
    function release_dreamland() {
    document.getElementById("fa-dreamland").style.backgroundColor = "#B22222";
    document.getElementById("fa-span").style.color = "white";

    document.getElementById("manage-dreamland").style.backgroundColor = "#F0F0F0";
    document.getElementById("manage-span").style.color = "black";

    document.getElementById("personal-div").style.backgroundColor = "#F0F0F0";
    document.getElementById("personal-span").style.color = "black";

    document.getElementById("release-dreamland").style.display = "";
    document.getElementById("personal-dreamland").style.display = "none";
    document.getElementById("update-dreamland").style.display = "none";

    }
    //私密梦点击事件
    function personal_dreamland() {
        document.getElementById("fa-dreamland").style.backgroundColor = "#F0F0F0";
        document.getElementById("fa-span").style.color = "black";

        document.getElementById("personal-div").style.backgroundColor = "#B22222";
        document.getElementById("personal-span").style.color = "white";

        document.getElementById("manage-dreamland").style.backgroundColor = "#F0F0F0";
        document.getElementById("manage-span").style.color = "black";

        document.getElementById("release-dreamland").style.display = "none";
        document.getElementById("personal-dreamland").style.display = "";
        document.getElementById("update-dreamland").style.display = "none";


    }
</code></pre>
<p>我们再来看，“私密梦”列表的 div 代码：</p>
<pre><code>            &lt;div id="personal-dreamland" style="height: 700px;margin-top: 50px;width: 100%;display: none"&gt;
            &lt;ul style="font-size: 12px" id="personal-dreamland-ul"&gt;
                &lt;c:forEach var="cont" items="${page2.result}" varStatus="i"&gt;
                &lt;li class="dreamland-fix"&gt;
                    &lt;a&gt;${cont.title}&lt;/a&gt;
                    &lt;span class="bar-delete"&gt;删除&lt;/span&gt;
                    &lt;span class="bar-update"&gt;修改&lt;/span&gt;
                    &lt;hr/&gt;
                &lt;/li&gt;
                &lt;/c:forEach&gt;

            &lt;/ul&gt;

            &lt;div id="personal-dreamland-div" style="float: left;position: absolute;bottom: 1080px;margin-left: 20px"&gt;
                &lt;ul class="pager pager-loose" id="personal-dreamland-fy"&gt;
                    &lt;c:if test="${page2.pageNum &lt;= 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a href="javascript:void(0);"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page2.pageNum &gt; 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a onclick="personTurnPage(${page2.pageNum-1})"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:forEach begin="1" end="${page2.pages}" var="pn"&gt;
                        &lt;c:if test="${page2.pageNum==pn}"&gt;
                            &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                        &lt;c:if test="${page2.pageNum!=pn}"&gt;
                            &lt;li &gt;&lt;a onclick="personTurnPage(${pn})"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                    &lt;/c:forEach&gt;

                    &lt;c:if test="${page2.pageNum&gt;=page2.pages}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page2.pageNum&lt;page2.pages}"&gt;
                        &lt;li&gt;&lt;a onclick="personTurnPage(${page2.pageNum+1})"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;

                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/div&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>&lt;c:forEach&gt;</code> 遍历得到每一个列表标签 li。</p>
<p>（2）分页，根据当前页判断上一页是否可点击，<code>href="javascript:void(0);</code> 表示点击无效。</p>
<p>（3）通过 <code>&lt;c:forEach&gt;</code> 遍历总页数，属性 begin 代表从1开始，end 属性代表到总页数结束，var 设置变量 pn，通过 <code>${pn}</code> 可获得遍历的当前值，如果遍历的当前值等于当前页，则当前页为选中状态，否则为未选中状态。</p>
<p>（4）根据当前页判断下一页是否可点击。</p>
<p>“私密梦”分页的点击事件为 personTurnPage，传入的参数是需要跳转的页码，具体方法如下：</p>
<pre><code>     //私密梦分页点击事件
    function personTurnPage(pageNum) {
        $("ul").remove("#personal-dreamland-ul");
        $("ul").remove("#personal-dreamland-fy");
        $.ajax({
            type: 'post',
            url: '/findPersonal',
            data: {"pageNum": pageNum},
            dataType: 'json',
            success: function (data) {
                var pageCate = data["page2"];
                if(pageCate=="fail"){
                    window.location.href = "/login.jsp";
                }else{
                    var ucList = pageCate.result;
                    var startHtml = " &lt;ul style='font-size: 12px' id='personal-dreamland-ul'&gt;";
                    var endHtml = "&lt;/ul&gt;";
                    if(ucList!=null) {
                        $(ucList).each(function () {
                            var contHtml = " &lt;li class='dreamland-fix'&gt; &lt;a&gt;"+this.title+"&lt;/a&gt; &lt;span class='bar-delete'&gt;删除&lt;/span&gt;"
                                +"&lt;span class='bar-update'&gt;修改&lt;/span&gt;&lt;hr/&gt;&lt;/li&gt;";
                            startHtml = startHtml + contHtml;
                        });
                        var okHtml = startHtml + endHtml;

                        //分页
                        var stPageHtml = "&lt;ul class='pager pager-loose' id='personal-dreamland-fy'&gt;";
                        if(pageCate.pageNum&lt;=1){
                            stPageHtml = stPageHtml + "  &lt;li class='previous'&gt;&lt;a href='javascript:void(0);'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                        }else if(pageCate.pageNum&gt;1){
                            var num = parseInt(pageCate.pageNum) -1;
                            stPageHtml = stPageHtml + "&lt;li class='previous'&gt;&lt;a onclick='personTurnPage("+num+")'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                        }

                        var foHtml = "";
                        for(var i = 1 ;i&lt;= pageCate.pages;i++){
                            if(pageCate.pageNum==i){
                                foHtml = foHtml+ "  &lt;li class='active'&gt;&lt;a href='javascript:void(0);'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                            }else{
                                foHtml = foHtml+ "&lt;li &gt;&lt;a onclick='personTurnPage("+i+")'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                            }
                        }

                        var teHtml = "";
                        if(pageCate.pageNum&gt;=pageCate.pages){
                            teHtml = " &lt;li&gt;&lt;a href='javascript:void(0);'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                        }else if(pageCate.pageNum&lt;pageCate.pages){
                            var num = parseInt(pageCate.pageNum) + 1;
                            teHtml = "&lt;li&gt;&lt;a onclick='personTurnPage("+num+")'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                        }
                        var endPageHtml = "&lt;/ul&gt;";

                        var pageOkHtml = stPageHtml + foHtml + teHtml +endPageHtml;
                    }

                    $("#personal-dreamland").append(okHtml);
                    $("#personal-dreamland-div").append(pageOkHtml);
                }
            }
        });
    }
</code></pre>
<p>该方法和梦分类点击事件大同小异。请参考梦分类点击事件的代码解读。注意这里的请求url是: <code>'/findPersonal'</code>。</p>
<p>接下来，我们再遍写 Java 后台 PersonalController 创建与 <code>url:/findPersonal</code> 映射的方法：</p>
<pre><code>    /**
     * 根据用户id查询私密梦
     * @param model
     * @param pageNum
     * @param pageSize
     * @return
     */
    @RequestMapping("/findPersonal")
    @ResponseBody
    public Map&lt;String,Object&gt; findPersonal(Model model,@RequestParam(value = "pageNum",required = false) Integer pageNum , @RequestParam(value = "pageSize",required = false) Integer pageSize) {

        Map map = new HashMap&lt;String,Object&gt;(  );
        User user = (User)getSession().getAttribute("user");
        if(user==null) {
            map.put("page2","fail");
            return map;
        }
        pageSize = 4; //默认每页显示4条数据
        PageHelper.Page&lt;UserContent&gt; page = userContentService.findPersonal(user.getId(),pageNum,pageSize);
        map.put("page2",page);
        return map;
    }
</code></pre>
<p>代码解读：</p>
<p>（1）从 Session 中取出用户信息，判断是否为空，为空则以 page2 为键，将 fail 放入 map 中。</p>
<p>（2）设置默认每页显示4条记录，主要为了测试分页。</p>
<p>（3）根据用户 id、分页数据查询分页，将查询结果放入 map，键为 page2，值为 page，为什么以 page2 为键呢？因为页面私密模块都是通过 <code>${page2.xx}</code> 来取值的，所以用和之前一样的键。</p>
<p>（4）返回 map。</p>
<p>发现没有 findPersonal 方法。这就是之前设计接口方法考虑不周造成的。所以我们要新增 findPersonal 方法。</p>
<p>在 UserContentService 接口中增加如下方法：</p>
<pre><code>     /**
     * 根据用户id查询所有文章私密并分页
     * @param uid
     * @param pageNum
     * @param pageSize
     * @return
     */
    PageHelper.Page&lt;UserContent&gt; findPersonal(Long uid ,Integer pageNum, Integer pageSize);
</code></pre>
<p>在实现类 UserContentServiceImpl 中实现 UserContentService 接口中的方法：</p>
<pre><code>    @Override
    public Page&lt;UserContent&gt; findPersonal(Long uid, Integer pageNum, Integer pageSize) {
        UserContent userContent = new UserContent();
        userContent.setuId(uid);
        userContent.setPersonal("1");
        PageHelper.startPage(pageNum, pageSize);//开始分页
        userContentMapper.select(userContent);
        Page endPage = PageHelper.endPage();//分页结束
        return endPage;
    }
</code></pre>
<p>personal 字段值为0表示为非私密文章，值为1则为私密文章。</p>
<p>到此博客管理模块就完成了。其中博客文章的查看、修改和删除下一节课来讲。看一下最后效果：</p>
<p><img src="http://images.gitbook.cn/bfd74800-7958-11e8-8c9c-d1cbf75a4c88" alt="" /></p>
<h3 id="-3">热梦推荐</h3>
<p><img src="http://images.gitbook.cn/d0b7f5c0-7958-11e8-b06c-81deae508e47" alt="" /></p>
<p>原理和上面说的是一样的，这里就不再多说了。希望同学们自己练习一下。我会把本节课的相关代码放在最文末的百度网盘链接中。</p>
<p>最后，提醒大家，梦分类列表和分页使用的是 ZUI 上面的组件。</p>
<p><img src="http://images.gitbook.cn/ecf8ee60-7958-11e8-b70e-bb13c5652b61" alt="" /></p>
<p><a href="http://zui.sexy/">ZUI</a> 提供了丰富的组件、控件和视图等，不仅美观而且使用起来也方便。文档中对它们的使用方法都有说明。</p>
<p><img src="http://images.gitbook.cn/23810b70-7959-11e8-8985-b17fa96df47a" alt="" /></p>
<blockquote>
  <p>第10课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1Xo-tdvj4Rr_fVJd5fuX95A 密码：h7y0</p>
</blockquote></div></article>