---
title: SSM 博客系统开发实战-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在正式实现首页和分页功能之前，我们首先思考两个问题：</p>
<p>1.index.jsp 页面动态数据怎么获取？
2.如果用 AJAX 获取，点击下一页的时候又要怎么办？</p>
<h3 id="">前期准备</h3>
<p>引入 index.jsp 文件，将原 index.jsp 文件替换。</p>
<p>启动 Tomcat 后访问，效果如下：</p>
<p><img src="http://images.gitbook.cn/6200f600-7461-11e8-9ce0-8f87da4d301a" alt="" /></p>
<p><img src="http://images.gitbook.cn/68e9e990-7461-11e8-92f7-efdcca03d400" alt="" /></p>
<p>因为页面都是死数据，无法完成分页功能，所以先导入文章的数据 SQL，SQL 文件会放入文末的百度网盘链接中。</p>
<p><strong>说明：</strong>因为 <code>user_content</code> 表存在外键关系，所以要先解除外键约束，否则无法删除和修改表：</p>
<pre><code>SET FOREIGN_KEY_CHECKS=0; #解除外键约束
</code></pre>
<p>等插入数据之后，再设置外键约束：</p>
<pre><code>SET FOREIGN_KEY_CHECKS=1；#设置外键约束
</code></pre>
<p>导入 SQL 文件和之前一样，如图：</p>
<p><img src="http://images.gitbook.cn/af57d9a0-7461-11e8-92f7-efdcca03d400" alt="" /></p>
<p>再将 image 文件夹拷贝到 <code>dreamland\dreamland-web\target\dreamland-web\images\</code> 目录下，主要是网页用到的网页图片，image 文件夹也在文末的百度网盘链接中。</p>
<h3 id="index">index 页面</h3>
<h4 id="-1">右上角的登录、注册</h4>
<p>index.jsp 页面逻辑判断代码，如下所示：</p>
<pre><code>     &lt;div style="position: absolute;margin-left: 980px;margin-top: -40px;"&gt;
        &lt;c:if test="${empty user}"&gt;
            &lt;a name="tj_login" class="lb" href="login?error=login" style="color: black"&gt;[登录]&lt;/a&gt;
            &amp;nbsp;&amp;nbsp;
            &lt;a name="tj_login" class="lb" href="register" style="color: black"&gt;[注册]&lt;/a&gt;
        &lt;/c:if&gt;
        &lt;c:if test="${not empty user}"&gt;
            &lt;a name="tj_loginp" href="javascript:void(0);"   class="lb" onclick="personal('${user.id}');" style="color: black"&gt;&lt;font color="#9370db"&gt;${user.nickName}, 欢迎您！&lt;/font&gt;&lt;/a&gt;
            &amp;nbsp;&amp;nbsp;
            &lt;a name="tj_login" class="lb" href="${ctx}/loginout" style="color: black"&gt;[退出]&lt;/a&gt;
        &lt;/c:if&gt;

    &lt;/div&gt;
</code></pre>
<p>通过 EL 表达式判断：</p>
<ol>
<li>如果用户为空，则显示“登录”、“注册”；</li>
<li>如果不为空，则显示“xxx，欢迎您！”和“退出”。</li>
</ol>
<h4 id="-2">引入天气预报</h4>
<p>只需将最底下的 div，如下：</p>
<pre><code>     &lt;div class="col-md-3" style="background-color: #C6E2FF;position:absolute;top:0px;left: 873px;width: 268px"&gt;
            &lt;h2&gt;Sidebar&lt;/h2&gt;
            &lt;ul class="nav nav-tabs nav-stacked"&gt;
                &lt;li&gt;&lt;a href='#'&gt;Another Link 1&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a href='#'&gt;Another Link 2&lt;/a&gt;&lt;/li&gt;
                &lt;li&gt;&lt;a href='#'&gt;Another Link 3&lt;/a&gt;&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;
</code></pre>
<p>替换成下面的代码，即可：</p>
<pre><code>     &lt;div class="col-md-3" style="position:absolute;top:0px;left: 880px;width: 268px;"&gt;
            &lt;div style="background-color: white;width: 250px;height: 440px"&gt;
                &lt;iframe name="weather_inc" src="http://i.tianqi.com/index.php?c=code&amp;id=82" width="250" height="440" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"&gt;&lt;/iframe&gt;
            &lt;/div&gt;
        &lt;/div&gt;
</code></pre>
<p>这个只是简单的引用，且必须联网才能使用。效果如下：</p>
<p><img src="http://images.gitbook.cn/1e8e2810-7462-11e8-a58c-b35f5fcc908a" alt="" /></p>
<h4 id="index-1">关于 index 页面的数据获取</h4>
<p>首先，通过 AJAX 请求获取数据，JavaScript 代码大概是这样的（看看就好，不建议）：</p>
<pre><code>    &lt;script language=javascript&gt;
    $.ajax({
        type: "post",
        dataType: "json",
        url: '${ctx}/index',
        success: function (data) {

            var Data=data;
            var content = null;
            var page =null;
            for(var key in Data) {
                if(key == "page"){
                    page = Data[key];
                }
                if(key == "content"){
                    content = Data[key];
                }
            }

            if (data!=null &amp;&amp; data != "" ) {
               $(content).each(function () {
                   var ll = this.title;
                  // alert(ll);
                  // alert(0);
                   $("#content_col").append("&lt;div class='content-text' &gt;&lt;div class='author clearfix'&gt;&lt;div&gt;"
                       +"&lt;a href='#' target='_blank' rel='nofollow' style='height: 35px' onclick=''&gt;"
                       +"&lt;img src='"+this.imgUrl+"'&gt;&lt;/a&gt;&lt;/div&gt;&lt;a href='' target='_blank' onclick=''&gt;"
                       +"&lt;h2 class='author-h2'&gt;"+this.nickName+"&lt;/h2&gt;&lt;/a&gt;&lt;/div&gt;"
                       +"&lt;h2&gt;"+this.title+"&lt;/h2&gt;"+this.content+
                       "&lt;div style='height: 5px'&gt;&lt;/div&gt;&lt;div class='stats'&gt;&lt;span class='stats-vote'&gt;&lt;i class='number'&gt;"+this.upvote+"&lt;/i&gt; 赞&lt;/span&gt;"
                      +"&lt;span class='stats-comments'&gt;&lt;span class='dash'&gt; · &lt;/span&gt;"
                   +"&lt;a href='#' class='comments' target='_blank' onclick=''&gt;"
                       +"&lt;i class='number'&gt;"+this.commentNum+"&lt;/i&gt; 评论 &lt;/a&gt;&lt;/span&gt; &lt;/div&gt;&lt;div style='height: 5px'&gt;&lt;/div&gt;"
                     +"&lt;div class='stats-buttons bar clearfix'&gt;&lt;a&gt;&lt;i class='icon icon-thumbs-o-up icon-2x'&gt;&lt;/i&gt;&lt;span class='number hidden'&gt;"+this.upvote+"&lt;/span&gt;&lt;/a&gt;"
                       +"&amp;nbsp;&amp;nbsp;&amp;nbsp;&lt;a&gt;&lt;i class='icon icon-thumbs-o-down icon-2x'&gt;&lt;/i&gt;&lt;span class='number hidden'&gt;"+this.downvote+"&lt;/span&gt;&lt;/a&gt;&amp;nbsp;&amp;nbsp;&amp;nbsp;&lt;a&gt;&lt;i class='icon icon-comment-alt icon-2x'&gt;&lt;/i&gt;&lt;/a&gt;"
                       +"&lt;/div&gt;&lt;div class='single-share'&gt;&lt;a class='share-wechat' data-type='wechat' title='分享到微信' rel='nofollow' style='margin-left:18px;color: grey'&gt;"
                       +"&lt;i class='icon icon-wechat icon-2x'&gt;&lt;/i&gt;&lt;/a&gt;&lt;a class='share-qq' data-type='qq' title='分享到QQ' rel='nofollow' style='margin-left:18px;color: grey'&gt;"
                       +"&lt;i class='icon icon-qq icon-2x'&gt;&lt;/i&gt; &lt;/a&gt;&lt;a class='share-weibo' data-type='weibo' title='分享到微博' rel='nofollow' style='margin-left:18px;color: grey'&gt;"
                       +"&lt;i class='icon icon-weibo icon-2x'&gt;&lt;/i&gt;&lt;/a&gt;&lt;/div&gt;&lt;br/&gt;&amp;nbsp;&lt;div class='single-clear'&gt;&lt;/div&gt;&lt;/div&gt;"
                       +"&lt;div style='position: absolute;width:900px;background-color: #EBEBEB;height: 10px;left: 0px'&gt;&lt;/div&gt;"
                   );

               });

                var cnt = "&lt;ul class='pager pager-loose'&gt;";
                if(page.pageNum &lt;= 1){
                    cnt += "&lt;li&gt;&lt;a href='javascript:void(0);'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                }else {
                    var pNum = page.pageNum-1;
                    cnt += "&lt;li class='previous'&gt;&lt;a href='${ctx}/index_list?pageNum="+pNum+"&amp;&amp;id=${user.id}'&gt;« 上一页&lt;/a&gt;&lt;/li&gt;";
                }
                for(var i=1;i&lt;=page.pages;i++){
                    if(page.pageNum == i){
                     cnt += "&lt;li class='active'&gt;&lt;a href='javascript:void(0);'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                    }else{
                        cnt += "&lt;li &gt;&lt;a href='${ctx}/index_list?pageNum="+i+"&amp;&amp;id=${user.id}'&gt;"+i+"&lt;/a&gt;&lt;/li&gt;";
                    }
                }

                if(page.pageNum &gt;= page.pages){
                    cnt += "&lt;li&gt;&lt;a href='javascript:void(0);'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;";
                }else {
                    var pNum = page.pageNum+1;
                    cnt += "&lt;li&gt;&lt;a href='${ctx}/index_list?pageNum="+pNum+"&amp;&amp;id=${user.id}'&gt;下一页 »&lt;/a&gt;&lt;/li&gt;&lt;/ul&gt;";
                }

               //分页
                $("#page-info").append(cnt);

            }
        }
    });
    &lt;/script&gt;
</code></pre>
<p>主要是通过 AJAX 获取数据后再添加到 div 中，这样只是解决了 index 页面的首次正常访问，有动态数据，但当点击下一页的时候就会产生新问题。这时可以新建一个和 index.jsp 一样的页面 index2.jsp，只不过这次不是用 AJAX 从后台获取数据，而是通过点击下一页或者其他页码，先经过 Controller，将分页数据封装后返回到 index2.jsp。这样做费时费力还耗资源，所以也不可取。</p>
<p>推荐的解决办法是：在进入 index.jsp 之前进行过滤器拦截，先获取页面数据，之后再返回 index.jsp 页面。</p>
<p>实现步骤如下：</p>
<p>（1）在 web.xml 中，引入自定义过滤器 filter：</p>
<pre><code>    &lt;!--自定义过滤器--&gt;
      &lt;filter&gt;
        &lt;filter-name&gt;dispatcherDemoFilter&lt;/filter-name&gt;
        &lt;filter-class&gt;wang.dreamland.www.interceptor.IndexJspFilter&lt;/filter-class&gt;
      &lt;/filter&gt;
      &lt;filter-mapping&gt;
        &lt;filter-name&gt;dispatcherDemoFilter&lt;/filter-name&gt;
        &lt;url-pattern&gt;/index.jsp&lt;/url-pattern&gt;
      &lt;/filter-mapping&gt;
</code></pre>
<p>在访问 index.jsp 之前进入自定义过滤器 dispatcherDemoFilter，通过该名字找到自定义过滤器具体路径 <code>wang.dreamland.www.interceptor.IndexJspFilter</code>。</p>
<p>（2）在 wang.dreamland.www 下新建包 interceptor，在 interceptor 包下新建 IndexJspFilter.java：</p>
<pre><code>    public class IndexJspFilter implements Filter{
        public void init(FilterConfig filterConfig) throws ServletException {

        }

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        System.out.println("===========自定义过滤器==========");
        ServletContext context = request.getServletContext();
        ApplicationContext ctx = WebApplicationContextUtils.getWebApplicationContext(context);
        UserContentMapper userContentMapper = ctx.getBean(UserContentMapper.class);
        PageHelper.startPage(null, null);//开始分页
        List&lt;UserContent&gt; list =  userContentMapper.select( null );
        PageHelper.Page endPage = PageHelper.endPage();//分页结束
        request.setAttribute("page", endPage );
        chain.doFilter(request, response);
    }

    public void destroy() {

        }
    }
</code></pre>
<p>代码解读如下:</p>
<p>filter 初始化时，注解的 bean 还没初始化，加 <code>@Autowired</code> 注解不会起作用，所以通过 ApplicationContext 手动获取 UserContentMapper 对象。</p>
<pre><code>UserContentMapper userContentMapper = ctx.getBean(UserContentMapper.class);
</code></pre>
<p>在开始分页和结束分页之间查询数据，PageHelper 会对分页开始之后的第一个查询语句进行分页，封装在 Page 对象中。</p>
<pre><code>PageHelper.startPage(null, null);//开始分页
List&lt;UserContent&gt; list =  userContentMapper.select( null );
PageHelper.Page endPage = PageHelper.endPage();//分页结束
</code></pre>
<p>pageNum 如果为 Null 则默认为第一页，pageSize 为 null 则默认每页显示7条数据，在 PageHelper 中有设默认值：</p>
<pre><code>public Page(Integer pageNum, Integer pageSize) {
    if (pageNum == null || pageNum &lt; 1) {
        pageNum = 1;
    }
    if (pageSize == null || pageSize &lt; 1) {
        pageSize = 7;
    }
    this.pageNum = pageNum;
    this.pageSize = pageSize;
}
</code></pre>
<p>然后将 Page 对象放在 request 域中，前台可通过 EL 表达式 <code>${page}</code> 获取：</p>
<pre><code>request.setAttribute("page", endPage );
</code></pre>
<p>（3）index.jsp 页面获取数据的代码如下：</p>
<pre><code>     &lt;c:forEach var="cont" items="${page.result}" varStatus="i"&gt;
                    &lt;!-- 正文开始 --&gt;

                    &lt;div class="content-text"&gt;

                        &lt;div class="author clearfix"&gt;
                            &lt;div&gt;
                                &lt;a href="#" target="_blank" rel="nofollow" style="height: 35px"&gt;
                                     &lt;img src="${cont.imgUrl}"&gt;
                                &lt;/a&gt;
                            &lt;/div&gt;
                            &lt;a href="#" target="_blank"&gt;
                                &lt;h2 class="author-h2"&gt;
                                    ${cont.nickName}
                                &lt;/h2&gt;
                            &lt;/a&gt;
                        &lt;/div&gt;

                       &lt;h2&gt;${cont.title}&lt;/h2&gt;
                            ${cont.content}
                        &lt;div style="height: 5px"&gt;&lt;/div&gt;
                        &lt;div class="stats"&gt;
                            &lt;!-- 笑脸、评论数等 --&gt;
                            &lt;span class="stats-vote"&gt;&lt;i id="${cont.id}" class="number"&gt;${cont.upvote}&lt;/i&gt; 赞&lt;/span&gt;
                            &lt;span class="stats-comments"&gt;
                    &lt;span class="dash"&gt; · &lt;/span&gt;
                         &lt;a  onclick="reply(${cont.id},${cont.uId});"&gt;
                              &lt;i class="number" id="comment_num_${cont.id}"&gt;${cont.commentNum}&lt;/i&gt; 评论
                          &lt;/a&gt;
                    &lt;/span&gt;
                        &lt;/div&gt;
                        &lt;div style="height: 5px"&gt;&lt;/div&gt;
                        &lt;div class="stats-buttons bar clearfix"&gt;
                            &lt;a style="cursor: pointer;" onclick="upvote_click(${cont.id},1);"&gt;
                                &lt;i class="icon icon-thumbs-o-up icon-2x"&gt;&lt;/i&gt;
                                &lt;span class="number hidden" id="up_${cont.id}"&gt;${cont.upvote}&lt;/span&gt;
                            &lt;/a&gt;
                            &amp;nbsp;
                            &lt;a style="cursor: pointer;" onclick="upvote_click(${cont.id},-1);"&gt;
                                &lt;i class="icon icon-thumbs-o-down icon-2x"&gt;&lt;/i&gt;
                                &lt;span class="number hidden" id="down_${cont.id}"&gt;${cont.downvote}&lt;/span&gt;
                            &lt;/a&gt;
                            &amp;nbsp;
                            &lt;a style="cursor: pointer;" onclick="reply(${cont.id},${cont.uId});" title="点击打开或关闭"&gt;
                                &lt;i class="icon icon-comment-alt icon-2x"&gt;&lt;/i&gt;
                            &lt;/a&gt;
                        &lt;/div&gt;
                        &lt;div class="single-share"&gt;
                            &lt;a class="share-wechat" data-type="wechat" title="分享到微信" rel="nofollow" style="margin-left:18px;color: grey;cursor: pointer; text-decoration:none;"&gt;
                                &lt;i class="icon icon-wechat icon-2x"&gt;&lt;/i&gt;
                            &lt;/a&gt;
                            &lt;a class="share-qq" data-type="qq" title="分享到QQ" rel="nofollow" style="margin-left:18px;color: grey;cursor: pointer; text-decoration:none;"&gt;
                                &lt;i class="icon icon-qq icon-2x"&gt;&lt;/i&gt;
                            &lt;/a&gt;
                            &lt;a  class="share-weibo" data-type="weibo" title="分享到微博" rel="nofollow" style="margin-left:18px;color: grey;cursor: pointer; text-decoration:none;"&gt;
                                &lt;i class="icon icon-weibo icon-2x"&gt;&lt;/i&gt;
                            &lt;/a&gt;
                        &lt;/div&gt;
                        &lt;br/&gt;
                        &amp;nbsp;
                        &lt;div class="commentAll" style="display:none" id="comment_reply_${cont.id}"&gt;
                            &lt;!--评论区域 begin--&gt;
                            &lt;div class="reviewArea clearfix"&gt;
                                &lt;textarea class="content comment-input" placeholder="Please enter a comment&amp;hellip;" onkeyup="keyUP(this)"&gt;&lt;/textarea&gt;
                                &lt;a class="plBtn" id="comment_${cont.id}" onclick="_comment(${cont.id},${user.id==null?0:user.id},${cont.uId})" style="color: white;cursor: pointer;"&gt;评论&lt;/a&gt;
                            &lt;/div&gt;
                            &lt;!--评论区域 end--&gt;
                            &lt;div class="comment-show-first" id="comment-show-${cont.id}"&gt;

                            &lt;/div&gt;

                        &lt;/div&gt;

                        &lt;div class="single-clear"&gt;

                        &lt;/div&gt;
                    &lt;/div&gt;
                    &lt;!-- 正文结束 --&gt;
                    &lt;div style="position: absolute;width:900px;background-color: #EBEBEB;height: 10px;left: 0px"&gt;
                    &lt;/div&gt;
                &lt;/c:forEach&gt;
</code></pre>
<p>代码解读如下：</p>
<ul>
<li>通过 <code>&lt;c:forEach&gt;&lt;/c:forEach&gt;</code> 循环获取文章内容 Content。</li>
<li><code>items="${page.result}"</code> 中，item 是 <code>List&lt;Content&gt;</code> 集合。</li>
<li><code>“var="cont"</code> 中，cont 是每一个 Content，通过 <code>${cont.属性}</code> 即可获得对应的属性值。</li>
<li><code>varStatus="i"</code> 中，i.index 就是从0开始的迭代索引，i.count 就是从1开始迭代计数。</li>
</ul>
<p>（4）分页信息如下：</p>
<pre><code>            &lt;div id="page-info" style="position: absolute;width:900px;background-color: #EBEBEB;height: 80px;left: 0px;"&gt;
                &lt;ul class="pager pager-loose"&gt;
                    &lt;c:if test="${page.pageNum &lt;= 1}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum &gt; 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a href="${ctx}/index_list?pageNum=${page.pageNum-1}&amp;&amp;id=${user.id}"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:forEach begin="1" end="${page.pages}" var="pn"&gt;
                        &lt;c:if test="${page.pageNum==pn}"&gt;
                            &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                        &lt;c:if test="${page.pageNum!=pn}"&gt;
                            &lt;li &gt;&lt;a href="${ctx}/index_list?pageNum=${pn}&amp;&amp;id=${user.id}"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                    &lt;/c:forEach&gt;

                    &lt;c:if test="${page.pageNum&gt;=page.pages}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum&lt;page.pages}"&gt;
                        &lt;li&gt;&lt;a href="${ctx}/index_list?pageNum=${page.pageNum+1}&amp;&amp;id=${user.id}"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;

                &lt;/ul&gt;
            &lt;/div&gt;
</code></pre>
<p>判断过程如下：</p>
<ol>
<li>页数 &lt;=1 显示上一页，但是不能点击（点击无效）；</li>
<li>页数 &gt;1 显示上一页，点击返回上一页；</li>
<li>页数 &gt;= 最后一页 ，显示下一页，但是点击无效；</li>
<li>页数 &lt; 最后一页，显示下一页，点击跳转到下一页。</li>
</ol>
<p>（5）中间页数循环。</p>
<p>代码如下：</p>
<pre><code>    &lt;c:forEach begin="1" end="${page.pages}" var="pn"&gt;
</code></pre>
<p>从第一页开始，最后一页结束，变量 pn=当前页数。</p>
<p>（6）如果 pageNum 等于当前页 pn，说明被选中，不能被再次点击（点击无效）：</p>
<pre><code>     &lt;c:if test="${page.pageNum==pn}"&gt;
          &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
     &lt;/c:if&gt;
</code></pre>
<p>（7）如果 pageNum 不是当前页，既不是被选中页，可以被点击，点击后跳转到该页：</p>
<pre><code>      &lt;c:if test="${page.pageNum!=pn}"&gt;
           &lt;li &gt;&lt;a href="${ctx}/index_list?pageNum=${pn}&amp;&amp;id=${user.id}"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
      &lt;/c:if&gt;
</code></pre>
<p>重启 Tomcat，访问：http://localhost:8080/，页面已经有动态数据了，但是点击下一页或者其他页还没实现。</p>
<h3 id="indexjspcontroller">IndexJspController</h3>
<p>在 wang.dreamland.www 包下新建 IndexJspController.java，并继承 BaseController，将关于首页有关的方法都放在这里，创建映射 URL 为 <code>/index_list</code> 的方法：</p>
<pre><code>    @Controller
    public class IndexJspController extends BaseController {
    private final static Logger log = Logger.getLogger(IndexJspController.class);

    @RequestMapping("/index_list")
    public String findAllList(Model model, @RequestParam(value = "id",required = false) String id ,
                                    @RequestParam(value = "pageNum",required = false) Integer pageNum ,
                                    @RequestParam(value = "pageSize",required = false) Integer pageSize) {

         log.info( "===========进入index_list=========" );
        User user = (User)getSession().getAttribute("user");
        if(user!=null){
            model.addAttribute( "user",user );
        }
        Page&lt;UserContent&gt; page =  findAll(null,pageNum,  pageSize);
        model.addAttribute( "page",page );
        return "../index";
    }

    }
</code></pre>
<p>代码解读如下：</p>
<ol>
<li><p>通过 Session 获取 User 信息，如果不为空则把 User 添加到 Model 中；</p></li>
<li><p>调用 BaseController 中的 findAll 方法查询分页并将结果封装到 Page 对象中，参数分别是 null 代表查询所有、pageNum 当前页、pageSize 每页显示条数；</p></li>
<li><p>将 Page 对象添加到 Model 中，并返回到 index.jsp 页面。</p></li>
</ol>
<p>最后重启 Tomcat 访问：http://localhost:8080/，分页完成！</p>
<p><img src="http://images.gitbook.cn/ed473aa0-7464-11e8-9ce0-8f87da4d301a" alt="" /></p>
<blockquote>
  <p>第08课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1iyTbvLepD07MUeFVbpMxRw 密码：1xxw</p>
</blockquote></div></article>