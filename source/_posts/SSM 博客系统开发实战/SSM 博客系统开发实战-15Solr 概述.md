---
title: SSM 博客系统开发实战-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="solr">Solr 概述</h3>
<p>Solr 是一个独立的企业级搜索应用服务器，它对外提供类似于 Web Service 的 API 接口。用户可以通过 HTTP 请求，向搜索引擎服务器提交一定格式的 XML 文件，生成索引；也可以通过 HTTP Get 操作提出查找请求，并得到 XML 格式的返回结果。</p>
<p>它具有以下特点（来自百度百科）：</p>
<blockquote>
  <p>Solr是一个高性能，采用 Java 5 开发，基于 Lucene 的全文搜索服务器。同时对其进行了扩展，提供了比 Lucene 更为丰富的查询语言，同时实现了可配置、可扩展，并对查询性能进行了优化，且提供了一个完善的功能管理界面，是一款非常优秀的全文搜索引擎。</p>
</blockquote>
<p>我们使用将 Solr 达到什么样的效果呢？</p>
<p>首先能根据搜索条件进行分词，查询出需要的结果，然后将分词高亮显示。</p>
<p>比如查询：“SSM 框架实战”，分词的结果可能是：“SSM 框架 实战”或者“S S M 框 架 实战”等。</p>
<p>我们将根据分词的结果去数据库查询，将查询结果以高亮显示在页面。</p>
<p>本文主要分三部分来介绍：</p>
<ol>
<li>Solr 单元测试；</li>
<li>Solr 在项目中的应用；</li>
<li>Tomcat 服务器运行 Solr。</li>
</ol>
<h3 id="solr-1">Solr单元测试</h3>
<p>Solr 单元测试步骤如下：</p>
<ol>
<li>开启 Solr 服务；</li>
<li>添加 Java 操作 Solr 的依赖；</li>
<li>编写测试代码。</li>
</ol>
<h4 id="solr-2">下载和启动 Solr</h4>
<h5 id="solr-3"><strong>下载 Solr</strong></h5>
<p>我将 Solr 压缩包放在本课程最后的百度网盘中，大家也可从 Solr 官网中下载.</p>
<ul>
<li><a href="https://lucene.apache.org/solr/mirrors-solr-latest-redir.html">下载地址</a></li>
</ul>
<p>等待3秒自动跳转到下载页面，如图：</p>
<p><img src="https://images.gitbook.cn/7afcfe20-867b-11e8-956e-f528114b28bd" alt="" /></p>
<p>我下载的时候版本是 7.3.1。</p>
<p>点击链接进入后总共有三个版本包：</p>
<ol>
<li><code>solr-7.3.1-src.tgz</code> 含有 Lucene 源码 tgz 包；</li>
<li><code>solr-7.3.1.tgz</code> 不含源码 tgz 包；</li>
<li><code>solr-7.3.1.zip</code> 不含源码 zip 包；</li>
</ol>
<p>我们下载后面两个，tgz 包用于 Linux 系统，zip 包用于 Windows 系统。</p>
<h5 id="solr-4"><strong>启动 Solr</strong></h5>
<p>下载完成后，将 zip 后缀压缩包解压到自定义目录，进入到 <code>solr-7.3.1\bin</code> 目录下，shift+鼠标右键，点击在此处打开命令窗口，如果是 Windows 10 系统先 shift+鼠标右键打开 PowerShell 窗口，然后输入 start cmd，打开命令窗口，在命令窗口中输入：</p>
<pre><code>    solr start
</code></pre>
<p>启动 Solr 服务，如图：</p>
<p><img src="https://images.gitbook.cn/af2c41a0-867c-11e8-b4e5-25aeb7ae7f28" alt="" /></p>
<p>访问端口为8983，我们可以通过 <code>localhost:8983</code> 或者 <code>127.0.0.1:8983</code> 访问 Solr 网页。</p>
<p>进入网页后发现提示“no cores avaiable”，即没有可用的内核，其实就是没有 Solr 的索引库，如图：</p>
<p><img src="https://images.gitbook.cn/fd8727c0-867c-11e8-9b0d-95de449dc107" alt="" /></p>
<p>那我们就创建一个 core，还是在刚才的命令窗口中输入：<code>solr create -c mycore</code>。其中 mycore 为 core 的名字，如图</p>
<p><img src="https://images.gitbook.cn/24400710-867d-11e8-8214-0fdd430af3ce" alt="" /></p>
<p>在 <code>solr-7.3.1\server\solr</code> 目录下发现多一个文件夹 mycore，然后再重新进入 Solr 网页查看，发现已经有了我们刚才创建的 mycore。选择mycore，点击后出现一个列表，点击 Query，执行 Execute Query，查询出了一条数据，这是 Solr 默认的。</p>
<blockquote>
  <p>补充：Solr 重启命令</p>
<pre><code class="     language-    ">   solr restart -p 8983
</code></pre>
  <p>-p 后面指定端口号</p>
</blockquote>
<h4 id="javasolrsolrj">添加 Java 操作 Solr 的依赖——SolrJ</h4>
<p>Java 就是通过 Solrj 来操作 Solr 的。它提供了一些增、删、改、查的方法。使用起来很方便。</p>
<h5 id="pomxmlsolrsolrj"><strong>在 pom.xml 中引入依赖 <code>solr-solrj</code></strong></h5>
<pre><code>    &lt;dependency&gt;
      &lt;groupId&gt;org.apache.solr&lt;/groupId&gt;
      &lt;artifactId&gt;solr-solrj&lt;/artifactId&gt;
      &lt;version&gt;7.3.0&lt;/version&gt;
    &lt;/dependency&gt;
</code></pre>
<p>通过 Solr 客户端对象调用相关方法，操作 Solr，测试类中会介绍。</p>
<h5 id="solrspring"><strong>Solr 与 Spring 的整合</strong></h5>
<p>在 <code>src/main/resources</code> 目录下新建 <code>applicationContext-solr.xml</code>，主要是将 Solr 客户端对象交给 Spring 来管理，配置内容如下：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd"&gt;

    &lt;bean id="httpSolrClient" class="org.apache.solr.client.solrj.impl.HttpSolrClient"&gt;
        &lt;constructor-arg name="builder" value="http://localhost:8983/solr/mycore"/&gt;
    &lt;/bean&gt;

    &lt;/beans&gt;
</code></pre>
<p>通过 Ctrl+鼠标右键点击 HttpSolrClient，查看源码。Ctrl+F 搜索 Builder，发现它有一个构造方法，接收的参数名正是 builder，这里就是构造方法注入，它的参数 <code>name="builder"</code> 是固定格式，value 就是 builder 对应的值，是一个 solrCore 的远程地址，mycore 就是我们刚才创建的。</p>
<h4 id="">编写测试代码</h4>
<p>单元测试代码都放在了 <code>src/test</code> 目录下。</p>
<h5 id="testjavatestsolrjjava"><strong>在 <code>test/java</code> 目录下新建 TestSolrJ.java</strong></h5>
<p>代码如下：</p>
<pre><code>    @ContextConfiguration(locations = {"classpath:applicationContext-solr.xml"})
    public class TestSolrJ extends AbstractJUnit4SpringContextTests {
    @Autowired
    private SolrClient solrServer;

    @Test
    public void testSave() throws Exception {   

        //1.创建一个文档对象
        SolrInputDocument inputDocument = new SolrInputDocument();
        inputDocument.addField( "id", "32" );
        inputDocument.addField( "item_title", "ssm项目开发实战" );
        inputDocument.addField( "item_image", "www.ssm.png" );
        inputDocument.addField( "author", "wly" );
        //2.将文档写入索引库中
        solrServer.add( inputDocument );
        //3.提交
        solrServer.commit();
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）<code>@ContextConfiguration</code> 注解表示加载配置文件，就是我们之前配置的 Solr 与 Spring 的整合配置文件，如果有多个配置文件用逗号隔开，如：</p>
<pre><code>locations = {"classpath:applicationContext-solr.xml","classpath:spring-mvc.xml"}
</code></pre>
<p>（2）测试类要继承 AbstractJUnit4SpringContextTests 测试基类，否则注入不了对象。</p>
<p>（3）通过 <code>@Autowired</code> 注解注入 Solr 客户端对象 SolrClient。</p>
<p>（4）<code>@Test</code>注解，代表这是一个测试方法。</p>
<p>（5）创建文档对象 SolrInputDocument。</p>
<p>（6）向文档中添加字段和对应的值。</p>
<p>（7）通过客户端对象的 add 方法将文档写入索引库中。</p>
<p>（8）提交（一定要提交，否则添加不成功）。</p>
<p>启动单元测试，点击 testSave，右键选择 Run testSave，启动完成后再次访问 Solr 网页。</p>
<p>执行 Execute Query 发现多了一条数据，就是刚才我们插入的，如下图：</p>
<p><img src="https://images.gitbook.cn/b338de50-867e-11e8-9b0d-95de449dc107" alt="" /></p>
<p>Solr 单元测试完成，通过单元测试说明操作 Solr 成功！</p>
<p>但是发现一个问题，查询出来的结果除了 id 都是 ArrayList 集合形式 <code>[]</code>，如果取值的话转换起来会很麻烦。怎么解决这个问题呢？</p>
<p>主要就是对 <code>solr-7.3.1\server\solr\mycore\conf\</code> 下的配置文件managed-schema进行修改，配置对应的字段以及字段类型，如下：</p>
<pre><code>    &lt;field name="id" type="string" multiValued="false" indexed="true" required="true" stored="true"/&gt;
    &lt;field name="item_image" type="string" stored="false" docValues="false"/&gt;
    &lt;field name="item_title" type="string" /&gt;
    &lt;field name="item_content" type="string"/&gt;
    &lt;field name="author" type="string"/&gt;
</code></pre>
<p>之前对应的 <code>type="text_general"</code> 是 Solr 自动生成的，其中</p>
<ul>
<li>name：字段的名字；</li>
<li>type：字段的数据类型；</li>
<li>multiValued：是否有多值，有多值时设置为 true，否则设置为 false；</li>
<li>indexed：是否创建索引；</li>
<li>required：是否必须；</li>
<li>stored：是否存储数据，如果设置为 false 则不存储，结合 <code>docValues="false"</code> 使得查询不返回结果。</li>
</ul>
<p>将 <code>item_image</code> 字段设置 <code>stored="false"</code> 和 <code>docValues="false"</code> 进行测试。</p>
<p>在命令窗口输入：</p>
<pre><code>    solr restart -p 8983
</code></pre>
<p>重启 Solr，重启成功后刷新网页，点击 Documents，然后选择 XML，在Document(s) 文本域内输入：</p>
<pre><code>    &lt;delete&gt;&lt;id&gt;33&lt;/id&gt;&lt;/delete&gt;
</code></pre>
<p>然后点击按钮 Submit Document，删除 id=33 的数据，如图：</p>
<p><img src="https://images.gitbook.cn/212f32b0-867f-11e8-87de-d910a3ee087e" alt="" /></p>
<p>点击 Query -&gt; Execute Query 查看，数据已删除。</p>
<p>然后再运行单元测试，执行 Execute Query 查看结果，如下，需要的字段已不包含中括号并且 <code>item_image</code> 字段没有返回查询结果，如图：</p>
<p><img src="https://images.gitbook.cn/61923320-867f-11e8-8675-5537a701ae7d" alt="" /></p>
<p>其中 <code>item_content_str</code> 和 <code>author_str</code> 等是复制域，在配置文件 <code>managed-schema</code> 的最后可以找到，它可以将某一个 Field 中的数据复制到另一个域中，比如将 <code>item_content</code> 中的数据复制到 <code>item_content_str</code> 中。</p>
<p>当两个域都有可能包含某个关键字，不知道查询的结果在哪个域中的时候，可以将这两个域中的内容复制到一个复制域中，从复制域中进行查找，我们将配置文件中的 <code>item_title</code> 和 <code>item_content</code> 都复制到 <code>item_title_str</code> 域中进行测试，配置如下：</p>
<pre><code>    &lt;copyField source="item_title" dest="item_title_str" maxChars="256"/&gt;
    &lt;copyField source="item_content" dest="item_title_str" maxChars="256"/&gt;
</code></pre>
<p>重启 Solr，将测试类中的 id 改为34，然后运行单元测试，查看结果如下：</p>
<p><img src="https://images.gitbook.cn/91faee30-867f-11e8-930b-fd70fc00d14d" alt="" /></p>
<p>id=34 的 <code>item_title_str</code> 复制域中包含了 <code>item_title</code> 和 <code>item_content</code> 两个域中的内容。</p>
<p>接下来就是将 Solr 应用到项目中，通过 Solr 搜索并将结果高亮显示。</p>
<h3 id="solr-5">Solr 在项目中的应用</h3>
<h4 id="ikanalyzer">IKAnalyzer 分词器</h4>
<p>Solr 可通过自带的分词器 smartcn 或者第三方分词器 IKAnalyzer 来实现，IKAnalyzer 分词效果较好，所以这里使用 IKAnalyzer 分词器。</p>
<p>使用 IKAnalyzer 分词器需要以下几个步骤：</p>
<p><strong>1.</strong> 下载 IKAnalyzer 分词器 Jar 包，我已将 <code>ikanalyzer-solr5.zip</code> 文件放入了百度网盘中。</p>
<p><strong>2.</strong> 压缩包解压后，将其中的两个 Jar 包放入 <code>solr-7.3.1\server\solr-webapp\webapp\WEB-INF\lib</code> 下。</p>
<p><strong>3.</strong> 配置 <code>solr-7.3.1\server\solr\mycore\conf</code> 下的 <code>managed-schema</code> 文件，添加分词器和需要分词的字段。</p>
<pre><code>    &lt;!-- 添加ik分词器 --&gt;
    &lt;fieldType name="text_ik" class="solr.TextField"&gt; 
      &lt;analyzer type="index" isMaxWordLength="false" class="org.wltea.analyzer.lucene.IKAnalyzer"/&gt; 
      &lt;analyzer type="query" isMaxWordLength="true"  class="org.wltea.analyzer.lucene.IKAnalyzer"/&gt; 
    &lt;/fieldType&gt;
</code></pre>
<p><code>type="index"</code> 代表创建索引时分词，<code>type="query"</code> 代表查询时分词。</p>
<pre><code>    &lt;!-- 需要分词的字段 --&gt;
    &lt;field name="title" type="text_ik" indexed="true" stored="true" required="true" multiValued="false" /&gt;
</code></pre>
<p>我们对文章标题进行分词查询。</p>
<p><strong>4.</strong> 配置其它字段名和类型，否则会查询出集合类型的数据。</p>
<pre><code>    &lt;field name="comment_num" type="string"/&gt;
    &lt;field name="downvote" type="string"/&gt;
    &lt;field name="upvote" type="string"/&gt;
    &lt;field name="nick_name" type="string"/&gt;
    &lt;field name="img_url" type="string"/&gt;
    &lt;field name="rpt_time" type="pdate"/&gt;
    &lt;field name="content" type="text_general"/&gt;
    &lt;field name="category" type="string"/&gt;
    &lt;field name="u_id" type="string"/&gt;
    &lt;field name="personal" type="string"/&gt;
</code></pre>
<p>注意：content 字段不能设置为 String 类型，否则内容过多会超出范围，报异常。除了日期和 content 字段外其它都设置为 String类型。</p>
<p><strong>5.</strong> 重新启动 Solr。</p>
<p>代码如下：</p>
<pre><code>    solr restart -p 8983
</code></pre>
<p><strong>6.</strong> 刷新网页，点击 Analysis，输入查询内容，选择分词字段，然后点击 Analyse Values 开始分词，查看结果，如下图：</p>
<p><img src="https://images.gitbook.cn/1adb36b0-8680-11e8-9b0d-95de449dc107" alt="" /></p>
<p>其中：</p>
<ul>
<li>Field Value (Index)：索引分词的值；</li>
<li>Field Value (Query)：查询分词的值。</li>
</ul>
<h4 id="webxmlapplicationcontextsolrxml">在 web.xml 中引入 <code>applicationContext-solr.xml</code> 配置文件</h4>
<p>代码如下：</p>
<pre><code>     &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;
      classpath:spring-mybatis.xml,
      classpath:applicationContext-redis.xml,
      classpath:applicationContext-activemq.xml,
      classpath:applicationContext-solr.xml
    &lt;/param-value&gt;
    &lt;/context-param&gt;
</code></pre>
<h4 id="solrservice">创建 SolrService 接口</h4>
<p>在 wang.dreamland.www.service 包下新建 SolrService 接口，接口方法如下：</p>
<pre><code>    public interface SolrService {
    /**
     * 根据关键字搜索文章并分页
     * @param keyword
     * @return
     */
     Page&lt;UserContent&gt; findByKeyWords(String keyword, Integer pageNum, Integer pageSize);
    }
</code></pre>
<p>提供根据关键字搜索文章并分页的接口方法。</p>
<h4 id="solrserviceimpl">创建 SolrServiceImpl 实现类</h4>
<p>代码如下：</p>
<pre><code>    @Autowired
    HttpSolrClient solrClient;
    @Override
     public Page&lt;UserContent&gt; findByKeyWords(String keyword, Integer pageNum, Integer pageSize) {
        SolrQuery solrQuery = new SolrQuery( );
        //设置查询条件
        solrQuery.setQuery( "title:"+keyword );
        //设置高亮
        solrQuery.setHighlight( true );
        solrQuery.addHighlightField( "title" );
        solrQuery.setHighlightSimplePre( "&lt;span style='color:red'&gt;" );
        solrQuery.setHighlightSimplePost( "&lt;/span&gt;" );

        //分页
        if (pageNum == null || pageNum &lt; 1) {
            pageNum = 1;
        }
        if (pageSize == null || pageSize &lt; 1) {
            pageSize = 7;
        }
        solrQuery.setStart( (pageNum-1)*pageSize );
        solrQuery.setRows( pageSize );
        solrQuery.addSort("rpt_time", SolrQuery.ORDER.desc);
        //开始查询

        try {
            QueryResponse response = solrClient.query( solrQuery );
            //获得高亮数据集合
            Map&lt;String, Map&lt;String, List&lt;String&gt;&gt;&gt; highlighting = response.getHighlighting();
            //获得结果集
            SolrDocumentList resultList = response.getResults();
            //获得总数量
            long totalNum = resultList.getNumFound();
            List&lt;UserContent&gt; list = new ArrayList&lt;UserContent&gt;(  );
            for(SolrDocument solrDocument:resultList){
                //创建文章对象
                UserContent content = new UserContent();
                //文章id
                String id = (String) solrDocument.get( "id" );
                Object content1 = solrDocument.get( "content" );
                Object commentNum = solrDocument.get( "comment_num" );
                Object downvote = solrDocument.get( "downvote" );
                Object upvote = solrDocument.get( "upvote" );
                Object nickName = solrDocument.get( "nick_name" );
                Object imgUrl = solrDocument.get( "img_url" );
                Object uid = solrDocument.get( "u_id" );
                Object rpt_time = solrDocument.get( "rpt_time" );
                Object category = solrDocument.get( "category" );
                Object personal = solrDocument.get( "personal" );
                //取得高亮数据集合中的文章标题
                Map&lt;String, List&lt;String&gt;&gt; map = highlighting.get( id );
                String title = map.get( "title" ).get( 0 );

                content.setId( Long.parseLong( id ) );
                content.setCommentNum( Integer.parseInt( commentNum.toString() ) );
                content.setDownvote( Integer.parseInt( downvote.toString() ) );
                content.setUpvote( Integer.parseInt( upvote.toString() ) );
                content.setNickName( nickName.toString() );
                content.setImgUrl( imgUrl.toString() );
                content.setuId( Long.parseLong( uid.toString() ) );
                content.setTitle( title );
                content.setPersonal( personal.toString() );
                Date date = (Date)rpt_time;
                content.setRptTime(date);
                List&lt;String&gt; clist = (ArrayList)content1;
                content.setContent( clist.get(0).toString() );
                content.setCategory( category.toString() );
                list.add( content );
            }
            PageHelper.startPage(pageNum, pageSize);//开始分页
            PageHelper.Page page = PageHelper.endPage();//分页结束
            page.setResult(list);
            page.setTotal(totalNum);
            return page;
        } catch (SolrServerException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）<code>@Service</code> 注解代表这是 Service 层。</p>
<p>（2）通过 <code>@Autowired</code> 注解，注入 Solr 客户端对象 HttpSolrClient。</p>
<p>（3）新建 SolrQuery 对象，然后设置查询条件，title 为要查询的字段，keyword 为要查询的字段值。</p>
<p>（4）高亮显示必须设置 highlight 属性为 true。</p>
<p>（5）设置高亮的字段 tilte。</p>
<p>（6）设置高亮的标签头，可看出 style 的 color 属性值为 red，即红色高亮显示，也可自定义别的颜色。</p>
<p>（7）设置高亮的标签尾。</p>
<p>（8）分页，设置开始索引和每页显示记录数，按照时间倒序。</p>
<p>（9）Solr 客户端对象根据查询条件查询 Solr 索引库，将查询结果放入 QueryResponse 对象中。</p>
<p>（10）下面就是根据 QueryResponse 对象获取高亮结果集和所有数据结果集，然后遍历所有数据结果集，获取 Solr 索引库中的数据，将数据设置到文章对象中；然后遍历高亮结果集，主要是 title 属性，将 title 设置到文章对象中，每遍历一次将结果添加到 list 集合，这样 list 集合就包含了所有的查询结果。</p>
<p>（11）使用 PageHelper 分页工具开始分页，将 list 集合和总记录数等设置到 Page 中，最后将 page 对象返回。</p>
<p>（12）如果发生异常则返回 null。</p>
<p>这样 Service 层方法就写完了，等待 Controller 层的调用。</p>
<h4 id="-1">事件源</h4>
<p>index.jsp 页面的搜索对应的 form 表单，如下：</p>
<pre><code>      &lt;form method="post" action="${ctx}/index_list"  id="indexSearchForm"  class="navbar-form navbar-right" role="search" style="margin-top: -35px;margin-right: 10px"&gt;
            &lt;div class="form-group"&gt;
                &lt;input type="text" id="keyword" name="keyword" value="${keyword}" class="form-control" placeholder="搜索"&gt;
            &lt;/div&gt;
            &amp;nbsp; &amp;nbsp;&lt;i onclick="searchForm();" class="icon icon-search" style="color: white"&gt;&lt;/i&gt;
        &lt;/form&gt;
</code></pre>
<p>action 对应的映射 URL 为：<code>/index_list</code>，搜索对应的点击事件 searchForm 方法如下：</p>
<pre><code>    //搜索
    function searchForm(){
        var keyword =  $("#keyword").val();
        if(keyword!=null &amp;&amp; keyword.trim()!=""){
            $("#indexSearchForm").submit();
        }
    }
</code></pre>
<p>如果查询条件不为空，则提交表单。</p>
<h4 id="indexjspcontrollerurlindex_list">在 IndexJspController 中修改映射 URL 为 <code>index_list</code> 的方法</h4>
<p>修改如下：</p>
<pre><code>    @RequestMapping("/index_list")
    public String findAllList(Model model, @RequestParam(value = "keyword",required = false) String keyword,
                                    @RequestParam(value = "pageNum",required = false) Integer pageNum ,
                                    @RequestParam(value = "pageSize",required = false) Integer pageSize) {
        log.info( "===========进入index_list=========" );
        User user = (User)getSession().getAttribute("user");
        if(user!=null){
            model.addAttribute( "user",user );
        }
        if(StringUtils.isNotBlank(keyword)){
            Page&lt;UserContent&gt; page = solrService.findByKeyWords( keyword ,pageNum,pageSize);
            model.addAttribute("keyword", keyword);
            model.addAttribute("page", page);
        }else {
            Page&lt;UserContent&gt; page =  findAll(pageNum,pageSize);
            model.addAttribute( "page",page );
        }
        return "../index";
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）从 Session 获取用户信息，如果不为 null 则添加到 model 中。</p>
<p>（2）如果关键字不为空则根据关键字进行 Solr 高亮搜索，并将返回结果 page 添加到 model 中，将关键字 keyword 也添加到 model 中，用于回显和分页查询条件。</p>
<p>（3）如果关键字为空则进行普通的分页查询，将 page 添加到 model 中。</p>
<p>（4）最后返回到 index.jsp 页面。</p>
<p>运行 Tomcat，输入查询条件后，发现什么都没有，跟我们预期的结果不一样？</p>
<p>这是因为 Solr 索引库中现在还没有数据，所以什么都没查到。我们需要在添加、修改和删除文章时将信息同步到 Solr 索引库中，数据发生变化，Solr 索引库要跟着变化，否则会出现数据不统一的现象。</p>
<h4 id="solr-6">同步信息到 Solr 索引库</h4>
<p><strong>1.</strong> 在 SolrService 接口中增加增、删、改方法，如下：</p>
<pre><code>     /**
     * 添加文章到solr索引库中
     * @param userContent
     */
    void addUserContent(UserContent userContent);

    /**
     * 根据solr索引库
     * @param userContent
     */
    void updateUserContent(UserContent userContent);

    /**
     * 根据文章id删除索引库
     * @param userContent
     */
    void deleteById(Long id);
</code></pre>
<p><strong>2.</strong> 在 SolrServiceImpl 中实现上述方法：</p>
<pre><code>    @Override
    public void addUserContent(UserContent cont) {
        if(cont!=null){
            addDocument(cont);
        }
    }

    @Override
    public void updateUserContent(UserContent cont) {
        if(cont!=null){
            addDocument(cont);
        }
    }

    @Override
    public void deleteById(Long id) {
        try {
            solrClient.deleteById(id.toString());
            solrClient.commit();
        } catch (SolrServerException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public void addDocument(UserContent cont){
        try {
            SolrInputDocument inputDocument = new SolrInputDocument();
            inputDocument.addField( "comment_num", cont.getCommentNum() );
            inputDocument.addField( "downvote", cont.getDownvote() );
            inputDocument.addField( "upvote", cont.getUpvote() );
            inputDocument.addField( "nick_name", cont.getNickName());
            inputDocument.addField( "img_url", cont.getImgUrl() );
            inputDocument.addField( "rpt_time", cont.getRptTime() );
            inputDocument.addField( "content", cont.getContent() );
            inputDocument.addField( "category", cont.getCategory());
            inputDocument.addField( "title", cont.getTitle() );
            inputDocument.addField( "u_id", cont.getuId() );
            inputDocument.addField( "id", cont.getId());
            inputDocument.addField( "personal", cont.getPersonal());
            solrClient.add( inputDocument );
            solrClient.commit();
        } catch (SolrServerException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
</code></pre>
<p>主要是通过 Solr 客户端对象 SolrCient 操作 Solr，这里的添加和更新方法一样，id 存在时就是根据 id 更新字段。还有就是别忘了 commit 提交。</p>
<p><strong>3.</strong> 在 WriteController 中更新如下：</p>
<pre><code>      if(cid ==null){
            userContent.setUpvote( 0 );
            userContent.setDownvote( 0 );
            userContent.setCommentNum( 0 );
            userContentService.addContent( userContent );
            solrService.addUserContent(userContent);

        }else {
            userContentService.updateById(userContent);
            solrService.updateUserContent(userContent);
        }
</code></pre>
<p>在添加和更新文章之后分别同步 Solr 索引库信息。注意记得注入 SolrService 对象。</p>
<p><strong>4.</strong> 在 PersonalController 中更新如下：</p>
<pre><code>    userContentService.deleteById(cid);
    solrService.deleteById(cid);
</code></pre>
<p>在删除文章的时候删除索引库对应的信息。注意记得注入 SolrService 对象。</p>
<h4 id="-2">首页关键词搜索高亮显示</h4>
<p>现在 Solr 索引库没有数据，我们直接在单元测试中把所有文章都查询出来，然后批量添加到 Solr 索引库中。</p>
<p>在单元测试类 TestSolrJ 中新建方法 testSaveAll，并将所需要的配置文件都进行加载：</p>
<pre><code>    @ContextConfiguration(locations = {"classpath:applicationContext-redis.xml","classpath:spring-mybatis.xml","classpath:applicationContext-activemq.xml","classpath:applicationContext-solr.xml"})    
</code></pre>
<p>具体方法如下：</p>
<pre><code>    @Autowired
    private UserContentService userContentService;
    @Test
    public void testSaveAll() throws IOException, SolrServerException {
        List&lt;UserContent&gt; list = userContentService.findAll();
        if(list!=null &amp;&amp; list.size()&gt;0){
            for (UserContent cont : list){
                SolrInputDocument inputDocument = new SolrInputDocument();
                inputDocument.addField( "comment_num", cont.getCommentNum() );
                inputDocument.addField( "downvote", cont.getDownvote() );
                inputDocument.addField( "upvote", cont.getUpvote() );
                inputDocument.addField( "nick_name", cont.getNickName());
                inputDocument.addField( "img_url", cont.getImgUrl() );
                inputDocument.addField( "rpt_time", cont.getRptTime() );
                inputDocument.addField( "content", cont.getContent() );
                inputDocument.addField( "category", cont.getCategory());
                inputDocument.addField( "title", cont.getTitle() );
                inputDocument.addField( "u_id", cont.getuId() );
                inputDocument.addField( "id", cont.getId());
                inputDocument.addField( "personal", cont.getPersonal());
                solrServer.add( inputDocument );
            }
        }

        solrServer.commit();
    }
</code></pre>
<p>上面代码将所有文章查询出来之后进行遍历，然后将每篇文章的信息都添加到文档对象中，然后通过 Solr 客户端对象将其添加到 Solr 索引库中，最后提交。</p>
<p>现在 Solr 索引库中已经有数据了，重新启动 Tomcat，然后输入查询条件进行搜索，比如搜索“Solr 高亮显示功能”，查询结果如下图：</p>
<p><img src="https://images.gitbook.cn/e1070cd0-8688-11e8-b4e5-25aeb7ae7f28" alt="" /></p>
<p>先对搜索条件进行分词，然后根据分词后的结果进行查询并将结果高亮显示。</p>
<p>最后，如果查询结果不止一页，想要点击下一页或者指定页码后还能高亮显示，则要将查询条件带上，如下：</p>
<pre><code>              &lt;div id="page-info" style="position: absolute;width:900px;background-color: #EBEBEB;height: 80px;left: 0px;"&gt;
                &lt;ul class="pager pager-loose"&gt;
                    &lt;c:if test="${page.pageNum &lt;= 1}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum &gt; 1}"&gt;
                        &lt;li class="previous"&gt;&lt;a href="${ctx}/index_list?pageNum=${page.pageNum-1}&amp;&amp;keyword=${keyword}"&gt;« 上一页&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:forEach begin="${page.startPage}" end="${page.endPage}" var="pn"&gt;
                        &lt;c:if test="${page.pageNum==pn}"&gt;
                            &lt;li class="active"&gt;&lt;a href="javascript:void(0);"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                        &lt;c:if test="${page.pageNum!=pn}"&gt;
                            &lt;li &gt;&lt;a href="${ctx}/index_list?pageNum=${pn}&amp;&amp;keyword=${keyword}"&gt;${pn}&lt;/a&gt;&lt;/li&gt;
                        &lt;/c:if&gt;
                    &lt;/c:forEach&gt;

                    &lt;c:if test="${page.pageNum&gt;=page.pages}"&gt;
                        &lt;li&gt;&lt;a href="javascript:void(0);"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;
                    &lt;c:if test="${page.pageNum&lt;page.pages}"&gt;
                        &lt;li&gt;&lt;a href="${ctx}/index_list?pageNum=${page.pageNum+1}&amp;&amp;keyword=${keyword}"&gt;下一页 »&lt;/a&gt;&lt;/li&gt;
                    &lt;/c:if&gt;

                &lt;/ul&gt;
            &lt;/div&gt;
</code></pre>
<p>在请求 URL 上拼接 keyword：</p>
<pre><code>    href="${ctx}/index_list?pageNum=${page.pageNum-1}&amp;&amp;keyword=${keyword}"
</code></pre>
<h3 id="tomcatsolr">Tomcat 服务器运行 Solr</h3>
<p>上面的 Solr 是在 Jetty 服务器下运行的，下面介绍 Solr 如何在 Tomcat 服务器上运行。</p>
<h4 id="-3">准备</h4>
<p><strong>1.</strong> 将 <code>solr-7.3.1\server\solr-webapp</code> 下的 webapp 文件复制到 Tomcat 的 webapps 目录下，并重命名为 Solr，如下图：</p>
<p><img src="https://images.gitbook.cn/33fab4f0-8689-11e8-8a91-d70bc2d847c5" alt="" /></p>
<p><strong>2.</strong> 将 <code>solr-7.3.1\server\lib\ext</code> 目录下的所有 Jar 包复制到刚才重命名的 <code>solr\WEB-INF\lib</code> 下。</p>
<p><strong>3.</strong> 将 <code>solr-7.3.1\server\lib</code> 下以 metrics 开头的5个 Jar 包也复制到刚才重命名的 <code>solr\WEB-INF\lib</code> 下。</p>
<p><strong>4.</strong> 在刚才重命名的 <code>solr\WEB-INF</code> 下新建 classes 文件夹，并将 <code>solr-7.3.1\server\resources</code> 下的 log4j.properties 文件复制到刚刚新建的 classes 文件夹下。</p>
<p><strong>5.</strong> 将 <code>solr-7.3.1\server</code> 目录下的 Solr 文件夹复制到自定义路径下，我这里直接放在了 <code>D:/</code> 下，然后重命名为 <code>solr_home</code>。</p>
<p><strong>6.</strong> 修改之前重命名的 <code>solr\WEB-INF</code> 下的 <code>web.xml</code> 文件。</p>
<p>找到如下图的注释，将其解开，并将路径替换成自己刚才重命名的 <code>solr_home</code> 的路径，如下</p>
<p><img src="https://images.gitbook.cn/9fcec590-8689-11e8-9b0d-95de449dc107" alt="" /></p>
<pre><code>&lt;env-entry&gt;
   &lt;env-entry-name&gt;solr/home&lt;/env-entry-name&gt;
   &lt;env-entry-value&gt;D:/solr_home&lt;/env-entry-value&gt;
   &lt;env-entry-type&gt;java.lang.String&lt;/env-entry-type&gt;
&lt;/env-entry&gt;
</code></pre>
<p>然后将最下面的 <code>security-constraint</code> 标签内的内容注释掉，如下图：</p>
<p><img src="https://images.gitbook.cn/bb2bede0-8689-11e8-956e-f528114b28bd" alt="" /></p>
<h4 id="tomcat">启动 Tomcat</h4>
<p>先介绍下 Tomcat 下的 ROOT 文件夹和 Solr 文件夹。</p>
<p>以 ROOT 命名的文件夹，Tomcat 启动后可以通过 <code>localhost:8080</code> 直接访问项目，不用加项目名。</p>
<p>而其他要部署的项目如果不是以 ROOT 命名，比如 Solr，访问的时候需要通过 <code>localhost:8080/solr</code> 的方式访问，即需要加上项目名。</p>
<p>接下来把我们的 <code>dreamland-web</code> 项目打 War包，我是直接用 Maven 命令 install 并跳过测试，如下图：</p>
<p><img src="https://images.gitbook.cn/00905d30-868a-11e8-8a91-d70bc2d847c5" alt="" /></p>
<p>如果出现 BUILD SUCCESS 即代表成功，然后在 <code>dreamland\dreamland-web\target</code> 目录下可以找到 <code>dreamland-web.war</code> 文件，这就是我们刚刚打包好的 War 包。</p>
<p>紧接着，我们将 <code>dreamland-web.war</code> 复制到 Tomcat 的 webapps 目录下，并重命名为 ROOT.war，将原来的 ROOT 文件夹删除，启动 Tomcat 后，会自动将 ROOT.war 文件解压。</p>
<p>启动Tomcat之前，需先启动 Redis 和 ActiveMQ，然后进入 Tomcat 安装目录下的 bin 目录，我的是：<code>D:\softs\java\apache-tomcat-8.5.9\bin</code>，双击 startup.bat 文件启动 Tomcat，此时就可以通过下面链接访问 Solr 网页了：</p>
<blockquote>
  <p>http://localhost:8080/solr/index.html#/</p>
</blockquote>
<p>访问我们自己的 Web 项目就是：http://localhost:8080，如果想通过 Solr 高亮搜索，则要将 <code>applicationContext-solr.xml</code> 中的端口修改成8080，然后重新打包部署。</p>
<pre><code>     &lt;constructor-arg name="builder" value="http://localhost:8080/solr/mycore"/&gt;
</code></pre>
<blockquote>
  <p>第14课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/18rDZpLx-3x-4iOSoyEqxqw 密码：y192</p>
</blockquote></div></article>