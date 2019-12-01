---
title: SSM 搭建精美实用的管理系统-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="81">8.1 什么是分页</h3>
<p>其实分页是一个网站系统中非常重要的功能，在各类电商网站、新闻网站、音乐网站、各类后台管理系统等等网站中都会存在，分页功能也是十分常见的功能，我们来看一下比较常见及常用的分页功能的展现形式。</p>
<h4 id="1">1. 百度分页</h4>
<p>在百度首页搜索框中输入 “ Java ” 查询相关信息之后跳转到搜索结果页面，页面中大致会有 10 条左右的数据列表，此时展示的是第 1 页的数据，如果想看后面的搜索内容点击页面下方的分页信息即可，比如点击第 6 页或者下一页的按钮就可以看到更多的信息了。</p>
<p><img src="https://images.gitbook.cn/f6bfa9d0-8e1a-11e8-bd0f-f38f8b899327" alt="baidu-page" /></p>
<h4 id="2">2. 商品列表分页</h4>
<p>点击全部商品可以看到商品列表，此时页面中展示的是第一页数据，并没有将所有数据全部展示，想要看到更多商品可以点击下方的分页信息即可。</p>
<p><img src="https://images.gitbook.cn/06aa10b0-8e1b-11e8-80d1-2d51ff7e1c55" alt="shop-page" /></p>
<h4 id="3">3. 博客后台分页</h4>
<p>博客后台的文章管理页面，也并没有把所有的文章信息都展示出来，而是通过分页功能分别展示出来。</p>
<p><img src="https://images.gitbook.cn/1372ec40-8e1b-11e8-a3e9-3b5653895392" alt="13blog-page" /></p>
<h3 id="82">8.2 分页的作用</h3>
<p>不仅仅是常见，分页功能在一个系统中也是不可缺少的。</p>
<p>分页功能的作用，有以下几点：</p>
<ul>
<li>减少系统资源的消耗，数据查询出来后会放在内存中。如果数据量很大，一次性将所有内容都查询出来，将会占用过多的内存，通过分页可以减少这种消耗；</li>
<li>提高性能，应用与数据库间通过网络传输数据，一次传输 10 条数据结果集与一次传输 20000 条数据结果集相比，肯定是前者消耗更少的网络资源；</li>
<li>提升访问速度，浏览器与应用间的传输也是通过网络，返回 10 条数据明显要比返回 20000 条数据速度更快，因为数据包的大小有差别；</li>
<li>符合用户习惯，比如搜索结果或者商品展示，通常用户可能只看最近前 30 条，将所有数据都查询出来比较浪费；</li>
<li>基于展现层面的考虑，由于设备屏幕的大小比较固定，一个屏幕能够展示的信息并不是特别多，如果一次展现太多的数据，不管是排版还是页面美观度都会受到影响，一个屏幕的范围就是那么大，展示信息条数有限。</li>
</ul>
<p>分页功能的使用可以提升系统性能，也比较符合用户习惯，符合页面设计规范，这也是为什么大部分系统都会有分页功能的原因。</p>
<h3 id="83">8.3 分页设计</h3>
<h4 id="1-1">1. 前端页面设计</h4>
<p>通过前文中提到的几个案例，我们可以看到使用分页功能的页面，一般包括两个主要的区域：数据展示区、分页信息区。</p>
<p><img src="https://images.gitbook.cn/20065ff0-8e1b-11e8-b410-a75e1f0acd2c" alt="page-design1" /></p>
<p><img src="https://images.gitbook.cn/28414ef0-8e1b-11e8-b410-a75e1f0acd2c" alt="page-design2" /></p>
<p><img src="https://images.gitbook.cn/3093bd90-8e1b-11e8-80d1-2d51ff7e1c55" alt="page-design3" /></p>
<p>分页信息区的设计和展示如上图所示，前端分页区比较重要的几个信息包括：</p>
<ul>
<li>总页数；</li>
<li>页码展示；</li>
<li>当前页码；</li>
<li>每页条数。</li>
</ul>
<p>当然，有些页面也会加上首页、尾页、跳转页码等功能，这些信息可以根据功能需要和页面设计去做增加和删减。</p>
<h4 id="2-1">2. 后端功能设计</h4>
<p>前端页面的工作是渲染数据和分页信息展示，而后端则需要按照前端传输过来的请求将分页所需的数据正确地查询出来并返回给前端。</p>
<p>两端的侧重点并不相同，比如前端需要展示所有页码，而后端则只需要提供总页数即可，并不需要对这个总页码进行其他操作，比如前端需要根据用户操作记录当前页码这个参数以便对页码信息进行调整和限制，而后端并不是关注当前页码，只需要接收前端传输过来的页码进行相应的判断和查询操作即可。</p>
<p>对于后端来说，必不可少的两个参数是：</p>
<ul>
<li>页码（需要第几页的数据）；</li>
<li>每页条数（每次查询多少条数据。一般默认 10 条或者 20 条) 。</li>
</ul>
<p>因此数据库查询语句可以这样写：</p>
<pre><code>//不同数据库使用的关键字会有些差别，比如 SQL Server 是通过 top 关键字、Oracle通过 rownum 关键字

//下面是mysql的实现语句：

select * from tb_xxxx limit 10,20
</code></pre>
<p>分页功能的最终实现既是如此，通过页码和条数确定数据库需要查询的是从第几条到第几条的数据，比如查询第 1 页，每页 20 条数据，就是查询数据库中从 0 到 20 条数据，查询第 4 页，每页 10 条数据，就是查询数据库中第 30 到 40 条数据，因此对于后端来说页码和条数两个参数就显得特别重要，缺少这两个参数根本无法继续之后的查询逻辑，分页数据也就无从查起。</p>
<p>虽然如此，为了前端分页区展示还要将数据总量或者总页数返回给前端。数据总量是必不可少的，而总页数可以计算出来，即数据总量除以每页条数。数据总量的获取方式如下：</p>
<pre><code>select count(*) from tb_xxxx
</code></pre>
<p>之后将数据封装，返回给前端即可。</p>
<h4 id="3-1">3. 数据交互总结</h4>
<p>这里，我们总结下数据交互的过程，如下：</p>
<ul>
<li>前端将页码和条数两个参数通过 HTTP 请求传输给后端；</li>
<li>后端获取到这两个参数后进行参数验证，查询后将当前页的所有数据实体和数据总量封装；</li>
<li>后端将封装数据返回给前端；</li>
<li>前端获取到数据和数据量后分别对当前页数据进行渲染和展示，同时完成分页信息区的计算和展示。</li>
</ul>
<h3 id="84jqgrid">8.4 JqGrid 分页插件介绍</h3>
<p>ssm-demo 教程中选用了 JqGrid 分页插件。JqGrid 是一个用来显示网格数据的 jQuery 插件，通过使用 jqGrid 可以轻松实现前端页面与后台数据的 AJAX 异步通信，特点如下：</p>
<ul>
<li>兼容目前所有流行的 Web 浏览器；</li>
<li>有完善强大的分页功能；</li>
<li>支持多种数据格式解析，如 XML 、JSON 、数组等形式；</li>
<li>提供丰富的选项配置及方法事件接口；</li>
<li>支持表格排序，支持拖动列、隐藏列；</li>
<li>支持滚动加载数据；</li>
<li>开源免费。</li>
</ul>
<blockquote>
  <p><a href="https://github.com/tonytomov/jqGrid/tree/master">JqGrid in GitHub</a></p>
  <p><a href="https://github.com/tonytomov/jqGrid/releases">点击获取：下载地址</a></p>
</blockquote>
<p>JqGrid 正式包的目录结构如下：</p>
<p><img src="https://images.gitbook.cn/4149b1d0-8e1b-11e8-91f2-2b35ab59bab9" alt="jqgrid-5.3" /></p>
<p>使用 JqGrid 时，必需要有的文件如下：</p>
<pre><code>jquery.jqGrid.js
grid.locale-cn.js
jquery.jqGrid.js

ui.jqgrid-bootstrap-ui.css
ui.jqgrid-bootstrap.css
ui.jqgrid.css
</code></pre>
<p>从中可以看出，主要的是 JS 文件和样式文件。果想使用 JqGrid 其他特性，只需对应地引入其 JS 文件即可。</p>
<p><img src="https://images.gitbook.cn/4d518750-8e1b-11e8-80d1-2d51ff7e1c55" alt="jqgrid-page" /></p>
<p>本课程的实战 Demo <a href="http://gitchat-ssm.13blog.site">gitchat-ssm</a> 所有模块的分页功能都是使用 JqGrid 插件实现的。其分页功能十分强大，使用和学习起来都比较简单，还有其他优秀的特性，本系统只使用了其部分特性，感兴趣的朋友可以继续学习其相关知识。</p>
<h3 id="85">8.5 分页功能实现</h3>
<h4 id="1-2">1. 前端实现</h4>
<p>首先，新建用户管理页面 user.html ，引入 JqGrid 所需文件：</p>
<pre><code>&lt;link href="plugins/jqgrid-5.3.0/ui.jqgrid-bootstrap4.css" rel="stylesheet"/&gt;
&lt;!-- JqGrid依赖jquery，因此需要先引入jquery.min.js文件 --&gt;
&lt;script src="plugins/jquery/jquery.min.js"&gt;&lt;/script&gt;

&lt;script src="plugins/jqgrid-5.3.0/grid.locale-cn.js"&gt;&lt;/script&gt;
&lt;script src="plugins/jqgrid-5.3.0/jquery.jqGrid.min.js"&gt;&lt;/script&gt;
</code></pre>
<p>分页信息区，代码如下：</p>
<pre><code>&lt;!-- JqGrid必要DOM,用于创建表格展示列表数据 --&gt;  
&lt;table id="jqGrid" class="table table-bordered"&gt;&lt;/table&gt;
&lt;!-- JqGrid必要DOM,分页信息区域 --&gt; 
&lt;div id="jqGridPager"&gt;&lt;/div&gt;  
</code></pre>
<p>下面代码完成了数据交互过程：</p>
<pre><code>$("#jqGrid").jqGrid({
        //请求后台 JSON 数据的 URL
        url: 'users/list',   
        //后台返回的数据格式
        datatype: "json",   
        //列表信息，包括表头、宽度、是否显示、渲染参数等属性
        colModel: [          
            {label: 'id', name: 'id', index: 'id', width: 50, hidden: true, key: true},
            {label: '登录名', name: 'userName', index: 'userName', sortable: false, width: 80},
            {label: '添加时间', name: 'createTime', index: 'createTime', sortable: false, width: 80}
        ],
        //表格高度，可自行调节
        height: 485,
        //默认一页显示多少条数据，可自行调节
        rowNum: 10,
        //翻页控制条中，每页显示记录数可选集合
        rowList: [10, 30, 50],
        //主题，这里选用的是 Bootstrap 主题
        styleUI: 'Bootstrap',
        //数据加载时显示的提示信息
        loadtext: '信息读取中...',
        //是否显示行号，默认值是 false，不显示
        rownumbers: true,
        //行号列的宽度
        rownumWidth: 35,
        //宽度是否自适应
        autowidth: true,
        //是否可以多选
        multiselect: true,
        //分页信息 DOM
        pager: "#jqGridPager",
        jsonReader: {
            root: "data.list",           //数据列表模型
            page: "data.currPage",       //数据页码
            total: "data.totalPage",     //数据总页码
            records: "data.totalCount"   //数据总记录数
        },
        // 向后台请求的参数
        prmNames: {
            page: "page",
            rows: "limit",
            order: "order"
        },
        // 数据加载完成并且 DOM 创建完毕之后的回调函数
        gridComplete: function () {
            //隐藏 Grid 底部滚动条
            $("#jqGrid").closest(".ui-jqgrid-bdiv").css({"overflow-x": "hidden"});
        }
    });
</code></pre>
<h4 id="2-2">2. 后端实现</h4>
<p>在前端实现中有如下代码：</p>
<pre><code>jsonReader: {
  root: "data.list", //数据列表模型
  page: "data.currPage", //当前页码
  total: "data.totalPage", //数据总页码
  records: "data.totalCount" //数据总记录数
  }
</code></pre>
<p>jsonReader 对象定义了如何对后端返回的 JSON 数据进行解析，比如数据列表为何读取 data.list ，当前页码为何读取  data.currPage ，这些都是由后端返回的数据格式所决定的，后端响应结果的数据格式定义在 Result.java 类中，代码如下：</p>
<pre><code>public class Result&lt;T&gt; implements Serializable {
    //响应码 200为成功
    private int resultCode;
    //响应msg
    private String message;
    //返回数据
    private T data;
}
</code></pre>
<p>即所有的数据都会被设置到 data 属性中，分页结果集的数据格式定义如下：</p>
<pre><code>public class PageResult implements Serializable {
    //总记录数
    private int totalCount;
    //每页记录数
    private int pageSize;
    //总页数
    private int totalPage;
    //当前页数
    private int currPage;
    //列表数据
    private List&lt;?&gt; list;
}
</code></pre>
<p>以上即为前后端进行数据交互时的格式定义。</p>
<p>AdminUserDao.xml 中增加查询用户列表和查询用户总数的代码语句：</p>
<pre><code>    &lt;!-- 查询用户列表 --&gt;
    &lt;select id="findAdminUsers" parameterType="Map" resultMap="AdminUserResult"&gt;
        select id,user_name,create_time from tb_admin_user
        where is_deleted=0
        order by id desc
        &lt;if test="start!=null and limit!=null"&gt;
            limit #{start},#{limit}
        &lt;/if&gt;
    &lt;/select&gt;

    &lt;!-- 查询用户总数 --&gt;
    &lt;select id="getTotalAdminUser" parameterType="Map" resultType="int"&gt;
        select count(*) from tb_admin_user
        where is_deleted=0
    &lt;/select&gt;
</code></pre>
<p>业务层代码，如下：</p>
<pre><code>    public PageResult getAdminUserPage(PageUtil pageUtil) {
        //当前页的用户列表
        List&lt;AdminUser&gt; users = adminUserDao.findAdminUsers(pageUtil);
        //用户总数
        int total = adminUserDao.getTotalAdminUser(pageUtil);
        //分页信息封装
        PageResult pageResult = new PageResult(users, total, pageUtil.getLimit(), pageUtil.getPage());
        return pageResult;
    }
</code></pre>
<p>控制层代码，如下：</p>
<pre><code>@RequestMapping(value = "/list", method = RequestMethod.GET)
    public Result list(@RequestParam Map&lt;String, Object&gt; params) {
        //检查参数
        if (StringUtils.isEmpty(params.get("page")) || StringUtils.isEmpty(params.get("limit"))) {
            return ResultGenerator.genErrorResult(Constants.RESULT_CODE_PARAM_ERROR, "参数异常！");
        }
        //查询列表数据
        PageUtil pageUtil = new PageUtil(params);
        return ResultGenerator.genSuccessResult(adminUserService.getAdminUserPage(pageUtil));
    }
</code></pre>
<p>数据库表结构在前一篇文章中已经给出，这里就不贴 SQL 语句了，至此，使用 JqGrid 插件实现的用户列表功能就完成了。</p>
<p><img src="https://images.gitbook.cn/5c61e1e0-8e1b-11e8-aa21-25f031a4e022" alt="jqgrid-page" /></p>
<h3 id="86">8.6 总结</h3>
<p>文中所涉及到的代码和 SQL 语句，十三都已经压缩且上传到百度云，提取地址如下：</p>
<blockquote>
  <p>链接：https://pan.baidu.com/s/1HuCfP50ugxoJkAU8yzwS_w </p>
  <p>密码：pyhe</p>
</blockquote>
<p>下载后将数据库文件导入数据库，代码解压后直接打开即可使用，步骤如下：</p>
<ul>
<li>导入 tb<em>admin</em>user.sql 文件；</li>
<li>使用 IDEA 打开 ssm-demo 项目；</li>
<li>修改数据库连接（默认是本地，如果不是的话请修改）；</li>
<li>部署 ssm-demo 项目，如下图所示：</li>
</ul>
<p><img src="https://images.gitbook.cn/6834ebc0-8e1b-11e8-aa21-25f031a4e022" alt="ssm-demo" /></p>
<ul>
<li>查看用户列表页面：</li>
</ul>
<p><img src="https://images.gitbook.cn/70674f40-8e1b-11e8-91f2-2b35ab59bab9" alt="ssm-demo-user" /></p>
<p>项目中已经实现了后台系统的页面布局和导航栏，这些都是由 AdminLTE3 模板中的 index.html 文件直接修改而来。</p></div></article>