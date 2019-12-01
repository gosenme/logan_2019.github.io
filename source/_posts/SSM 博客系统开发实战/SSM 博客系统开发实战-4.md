---
title: SSM 博客系统开发实战-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>SSM 框架搭建好以后，接下来我们就可以开启博客系统的开发实战了。</p>
<p>本篇文章，我们将根据项目所要实现功能来完成表结构的设计。主要包括确定项目中会用到哪些表，各表之间的关系是怎样的，然后根据表生成相对应的实体类。</p>
<p>项目中计划实现的功能主要包括以下几点：</p>
<ol>
<li>用户注册与激活，激活方式通过邮件激活；</li>
<li>用户的登录和退出，包括账号登录和手机快捷登录；</li>
<li>用户账号登录和注册时需要输入验证码验证；</li>
<li>首页展示及分页，主要展示文章内容，可进行搜索，将搜索结果高亮显示；</li>
<li>首页文章的点赞、踩和评论功能；</li>
<li>个人主页模块，包括个人的基本信息，梦分类，发布梦，管理梦以及热梦推荐等；</li>
<li>书写文章功能；</li>
<li>文章管理功能，包括文章的查看、修改和删除；</li>
<li>个人信息修改功能；</li>
<li>安全框架 spring-security 的整合，对不符合条件的用户或者 URL 进行拦截；</li>
<li>记录用户登录信息，包括登录的时间、IP 等；</li>
</ol>
<p>因此需设计相应的表包括：用户表 user、角色表 role、资源表 resource，角色用户中间表 <code>role_user</code>，角色资源中间表 <code>role_resource</code>，用户详细信息表 <code>user_info</code>、文章表 <code>user_content</code>、评论表 comment、点赞表 upvote、登录日志表 <code>login_log</code>。</p>
<h3 id="">表结构设计</h3>
<h4 id="powerdesigner">表结构设计工具：PowerDesigner</h4>
<p>Power Designer 是一款强大的数据建模工具，可以制作数据流程图、概念数据模型、物理数据模型，还可以为数据仓库制作结构模型等。本文将使用其进行数据表结构的设计，具体操作步骤如下。</p>
<p>大家先自行下载 PowerDesigner。</p>
<p>打开软件后，通过这一系列的操作过程：File -&gt; New Modle -&gt; Model types -&gt; Physical Data Model -&gt;Physical Diagram，新建物理数据模型，然后输入模型名称，并选择相应数据库，如下图所示：</p>
<p><img src="http://images.gitbook.cn/a54f1400-5e5e-11e8-b82c-e1d608026a45" alt="" /></p>
<p>如上图，Model name，我们采用默认的 PhysicalDiagram_1；DBMS，我们选择 MySQL5.0。</p>
<p>然后，点击右侧的 Toolbox 面板下的表格小图标，即可在 PhysicalDiagram_1 视图中创建表，每点一次创建一张表，选择 Toolbox 面板中的第一个小图标可选中表，双击进行编辑，如下图所示。</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-1.png" alt="" /></p>
<p>在下图所示的表格编辑页面中，通过以下几个选题卡可对表格进行各项编辑操作：</p>
<ul>
<li>General 选项卡中可输入表的描述及表名；</li>
<li>Columns 选项卡中添加表的列；</li>
<li>Indexes 选项卡中可创建索引，键入描述和索引名称后，双击改行或者点击下图中的黄色小图标可添加索引字段；</li>
<li>Physical Options 选项卡中可添加自增长和增长基数；</li>
<li>Preview 选项卡中可查看 SQL 语句。</li>
</ul>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-2.png" alt="" /></p>
<p>点击下图中的小图标，添加 Identity 列，勾选后可实现主键自增长。</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-6.png" alt="" /></p>
<h4 id="-1">十大表格结构设计</h4>
<h5 id="-2"><strong>权限控制表</strong></h5>
<p>用户表 user、角色表 role、资源表 resource 三个基表，及角色用户中间表 <code>role_user</code>，角色资源中间表 <code>role_resource</code>两个中间表，这五个表主要用权限控制。</p>
<p>每个基表和中间表中所包括的字段、数据类型，以及五个表格间的关系如下图所示，其中 pk 代表主键，fk 代表外键。</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-3.png" alt="" /></p>
<p>外键生成方法为：通过点击右侧 Toolbox 面板中小表格图标右侧第二个 Reference 图标，点击需要创建外键的表指向外键来源的表，可生成一个带指向的箭头，双击该箭头可修改 Joins 选项卡中的外键来源。</p>
<h5 id="-3"><strong>其余的表格</strong></h5>
<p>余下5张表分别是用户详细信息表 <code>user_info</code>、文章表 <code>user_content</code>、评论表 comment、点赞表：<code>upvote</code>、登录日志表：<code>login_log</code></p>
<p>各个表格的功能如下：</p>
<ul>
<li>用户详细信息表：主要是把常用字段放在 user 表中，不常用字段放在详细信息表中，提高查询效率；</li>
<li>文章表：主要包含文章的分类、文章标题、点赞数、评论数等；</li>
<li>评论表：主要是文章的评论模块，包含评论者 ID、被评论者 ID、评论内容、点赞等；</li>
<li>点赞表：主要是控制用户点赞的频率，每天只允许用户点赞一次等；</li>
<li>登录日志表：主要记录用户登录的时间、IP 等。</li>
</ul>
<p>下面我们看下这十张表结构关系，如下表所示：</p>
<p><img src="https://images.gitbook.cn/Fr9f2AvDyymsmaFOU8wzltCZp5IH" alt="avatar" /></p>
<h4 id="-4">新表的创建</h4>
<h5 id="sql"><strong>导出 SQL 文件</strong></h5>
<p>接下来，我们利用 PowerDesigner 将这些表格导出为 SQL 文件，方便之后向数据库中导入数据。</p>
<p>PowerDesigner 中，点击顶部的 Database（注意选中 PhysicalDiagram_1 视图），进行操作： Database -&gt; Generate Database，填写好导出的路径以及 SQL 文件名称，其他默认，然后点击确定。</p>
<p>然后对导出的文件进行简单修改，删除顶部 <code>drop index xxx on xxx</code> 语句，因为一开始表还未创建，这条语句会报错，为了方便，可将顶部的 drop 语句全部删除掉（包括 <code>drop table if exists xxx</code>）。</p>
<h5 id="sql-1"><strong>创建数据库及导入 SQL</strong></h5>
<p>这里我选用了数据库管理工具 Navicate，SQLYog 也可以。</p>
<p>我们首先新建一个数据库，操作过程为：localhost -&gt; 右键 -&gt; 新建数据库。</p>
<p>键入或者勾选：</p>
<blockquote>
  <p>数据库名：dream_db</p>
  <p>字符集：utf8 -- UTF-8 Unicode</p>
  <p>排序规则：<code>utf8_general_ci</code></p>
</blockquote>
<p>创建好数据库后，双击打开，右键表 -&gt; 运行 SQL 文件 -&gt; 选择你 SQL 文件的存储位置 -&gt;点击开始：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-5.png" alt="" /></p>
<p>运行结束后，右键刷新表就可看见所有表已经创建成功！</p>
<h3 id="-5">反向生成实体类</h3>
<p>表建好以后，需要创建对应的实体类，要把存入表中的字段与实体类中的属性相对应。如果手动创建的话，不仅速度慢，还可能会出错，通过 MyBatis 反向生成实体类，只要简单配置一下，即可一次性生成所有实体类，而且实体类属性是根据驼峰命名的，不会出错。</p>
<p>如表中字段 <code>nick_name</code>，根据驼峰命名生成对应的属性是 nickName，关于驼峰命名更详细介绍请自行百度。</p>
<h4 id="jar">所需 Jar 包及配置文件</h4>
<p>要完成反向生成实体类功能，需要依赖相关 Jar 包，包括 Mybatis 框架的 Jar 包，数据库驱动程序 Jar 包以及 MyBatis 生成器 Jar
 包，通过 Jar 包中的相关方法操作数据库中的表，生成对应的实体类（这些包已放在百度云盘的 mybatis-generator-core-1.3.2.zip 中，大家可根据文末提供的链接访问下载）。</p>
<p>generatorConfig.xml 配置文件，配置了生成实体类后保存的包路径，数据库相关信息：数据库名称、用户名和密码等，表名、实体类名称等，主要文件如下图所示（lib目录下）：</p>
<p><img src="http://images.gitbook.cn/24d1e480-5e75-11e8-b82b-ffbb9d1e8856" alt="" /></p>
<p>generatorConfig.xml 详细配置如下：</p>
<pre><code class="     language-    ">    &lt;?xml version="1.0" encoding="UTF-8"?&gt;    
    &lt;!DOCTYPE generatorConfiguration    
      PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"    
      "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd"&gt;    
    &lt;generatorConfiguration&gt;    
    &lt;!-- mysql-connector文件路径 --&gt;  
    &lt;classPathEntry  location="mysql-connector-java-5.1.25-bin.jar"/&gt;    
    &lt;context id="DB2Tables"  targetRuntime="MyBatis3"&gt;    
        &lt;commentGenerator&gt;    
            &lt;property name="suppressDate" value="true"/&gt;    

            &lt;property name="suppressAllComments" value="true"/&gt;    
        &lt;/commentGenerator&gt;    
        &lt;!-- 链接配置 输入你的数据库名及密码 --&gt;  
        &lt;jdbcConnection driverClass="com.mysql.jdbc.Driver"   
        connectionURL="jdbc:mysql://127.0.0.1:3306/dream_db"   
        userId="root" password="root"&gt;    
        &lt;/jdbcConnection&gt;    
        &lt;javaTypeResolver&gt;    
            &lt;property name="forceBigDecimals" value="false"/&gt;    
        &lt;/javaTypeResolver&gt;    
        &lt;!-- 生成实体类的路径，wang.dreamland.www.entity 这个路径可以自动生成，但是必须有src这个路径--&gt;  
        &lt;javaModelGenerator targetPackage="wang.dreamland.www.entity"   
        targetProject="src"&gt;    
            &lt;property name="enableSubPackages" value="true"/&gt;    
            &lt;property name="trimStrings" value="true"/&gt;    
        &lt;/javaModelGenerator&gt;    
       &lt;!-- 生成映射的路径，这个路径可以自动生成，但是必须有src这个路径--&gt;  
       &lt;sqlMapGenerator targetPackage="wang.dreamland.www.mapping" targetProject="src"&gt;    
            &lt;property name="enableSubPackages" value="true"/&gt;    
        &lt;/sqlMapGenerator&gt;    
           &lt;!-- 生成接口的路径，这个路径可以自动生成，但是必须有src这个路径--&gt;  
        &lt;javaClientGenerator type="XMLMAPPER" targetPackage="wang.dreamland.www.dao"   
        targetProject="src"&gt;    
            &lt;property name="enableSubPackages" value="true"/&gt;    
        &lt;/javaClientGenerator&gt;    

        &lt;!-- 表名、实体类名称 --&gt;
        &lt;table tableName="user" domainObjectName="User" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="user_info" domainObjectName="UserInfo" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="resource" domainObjectName="Resource" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="user_content" domainObjectName="UserContent" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="comment" domainObjectName="Comment" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="login_log" domainObjectName="LoginLog" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="role" domainObjectName="Role" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="role_resource" domainObjectName="RoleResource" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="role_user" domainObjectName="RoleUser" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
        &lt;table tableName="upvote" domainObjectName="Upvote" enableCountByExample="false" enableUpdateByExample="false" enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false"&gt;&lt;/table&gt;
    &lt;/context&gt;    
&lt;/generatorConfiguration&gt;  
</code></pre>
<pre><code>
</code></pre>
<h4 id="-6">具体实现步骤</h4>
<p>按照上图目录结构放置好以后，直接在当前目录下 shift+右键，点击在此处打开命令行窗口（Win10 打开 powerShell 窗口）。</p>
<p>输入以下命令即可执行成功：</p>
<pre><code class="         language-        ">java -jar mybatis-generator-core-1.3.2.jar -configfile generatorConfig.xml -overwrite
</code></pre>
<p>在当前目录的 src 目录下就会生成对应的实体类、映射文件和接口文件，注意得有 src 文件夹，结果如下三张图所示。</p>
<p><img src="http://images.gitbook.cn/1907cd90-5e70-11e8-b82c-e1d608026a45" alt="" /></p>
<p><img src="http://images.gitbook.cn/2e82eb00-5e70-11e8-a448-a1a9e71da8da" alt="" /></p>
<p><img src="http://images.gitbook.cn/3b5144d0-5e70-11e8-b82c-e1d608026a45" alt="" /></p>
<h4 id="-7">将实体类导入项目</h4>
<p>最后，我们将上面生成的实体类导入项目中。</p>
<ol>
<li>新建包路径。</li>
</ol>
<blockquote>
  <p>java -&gt; 右键new -&gt; Package -&gt; wang.dreamland.www.entity -&gt; OK</p>
</blockquote>
<p>2.复制刚才创建的实体类，粘贴到 entity 路径下。</p>
<p>3.最后的目录结构如下：</p>
<p><img src="https://raw.githubusercontent.com/wiki/wanglinyong/wanglinyong.github.io/pd-7.png" alt="" /></p>
<blockquote>
  <p>之后我会将每节课的资料上传到百度云盘。供大家下载。</p>
  <p>链接：https://pan.baidu.com/s/1m4hw8BuJMbXDVJN_TAvSIQ，密码：5yud。</p>
</blockquote>
<p><img src="https://images.gitbook.cn/Fj4yr0XZ0pjMtKnjMiDPN-M_aEpH" alt="avatar" />
<img src="https://images.gitbook.cn/Fj4yr0XZ0pjMtKnjMiDPN-M_aEpH" alt="avatar" /></p></div></article>