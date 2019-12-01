---
title: SSM 搭建精美实用的管理系统-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="41">4.1 简介</h3>
<p>前文中只是做了一个项目的脚手架，并没有实质的功能实现，那么这一篇十三将使用这个脚手架实现基础的框架整合和功能体验。</p>
<h3 id="42tomcat">4.2 Tomcat 安装</h3>
<p>前文中将项目骨架完善后，并没有介绍项目部署的相关事宜，限于篇幅原因，将部分内容放到了本节课程。</p>
<p>首先，根据系统选择需要下载的安装包，本文将介绍 Windows 64 位系统下的 Tomcat 8 安装，如果已经安装本版本或者其他版本的话可以跳过。</p>
<h4 id="1">1. 下载安装包</h4>
<p>首先到 Tomcat 8 的官方下载页面，链接如下：</p>
<ul>
<li><a href="https://tomcat.apache.org/download-80.cgi">Tomcat 8 官方下载链接</a></li>
</ul>
<p>选择对应的安装包进行下载，过程如下图：</p>
<p><img src="https://images.gitbook.cn/5a732d90-8a73-11e8-974b-497483da0812" alt="tomcat-download" /></p>
<h4 id="2">2. 安装</h4>
<p>之后，选择目录进行安装，十三选择的是 D:\tomcat 目录，解压后，Tomcat 的安装目录为 D:\tomcat\apache-tomcat-8.5.31 ，过程如下图：</p>
<p><img src="https://images.gitbook.cn/c4f6d4f0-8a69-11e8-8838-3badd92eb83e" alt="tomcat-unzip" /></p>
<p>打开安装目录，可以看到 Tomcat 的目录结构：</p>
<ul>
<li>bin 目录主要是用来存放 Tomcat 的命令，主要有两大类，一类是以 .sh 结尾（Linux 命令），另一类是以 .bat 结尾（Windows 命令）；</li>
<li>conf 目录主要用来存放 Tomcat 的一些配置文件；</li>
<li>lib 目录是 Tomcat 的类库，里面是 Jar 包文件；</li>
<li>logs 目录用来存放 Tomcat 在运行过程中产生的日志文件，非常重要的是在控制台输出的日志，清空不会对 Tomcat 运行带来影响；</li>
<li>temp 目录用来存放 Tomcat 的临时文件，这个目录下的东西可以在停止 Tomcat 后删除。</li>
<li>webapps 目录用来存放 Web 项目的目录；</li>
<li>work 目录用来运行时生成的文件，最终运行的文件都在这个目录。</li>
</ul>
<h4 id="3">3. 环境变量</h4>
<p>同设置 JDK 环境变量过程一样，首先，新增 CATALINA<em>HOME 变量，变量值为安装目录 D:\tomcat\apache-tomcat-8.5.31 ，之后，编辑 PATH 变量，添加 %CATALINA</em>HOME%\bin; ，完成。</p>
<p>不过，这个步骤并不是必要的，Tomcat 的环境变量配置与否都可以，JDK 环境配置正常即可，十三的建议是不用配置。</p>
<h4 id="4">4. 验证</h4>
<p>安装的成功与否需要验证一下，到 Tomcat 安装目录 bin 目录下，可以看到基本都是命令文件。因为是 Windows 系统，所以找到 startup.bat 文件并双击即可启动 Tomcat 服务器。</p>
<p>过程中没有报错，控制台也没有退出，并且控制台上有 Server startup in xxx s 的日志输出时即证明 Tomcat 启动成功。Tomcat 的默认端口号是 8080 ，打开浏览器并输入  localhost:8080 即可看到 Tomcat 的默认页面，整个过程如下图：</p>
<p><img src="https://images.gitbook.cn/06185880-8a6c-11e8-8838-3badd92eb83e" alt="tomcat-startup" /></p>
<p>前一篇中提到的 ssm-demo 该如何部署呢？</p>
<p>首先，需要将 ssm-demo.war 文件复制到 Tomcat 的 webapp 目录中，之后几秒可以看到 Tomcat 自动将其解压部署，并生成  ssm-demo 项目目录，这时在浏览器输入  localhost:8080/ssm-demo 就可以看到我们的第一个 ssm-demo 成功部署了。过程如下图：</p>
<p><img src="https://images.gitbook.cn/adb4abc0-8a6c-11e8-baa3-d3bd3f3e5753" alt="hello-ssm-startup" /></p>
<h3 id="43ssmdemo">4.3 ssm-demo 完善</h3>
<p>当然，本篇文章肯定不会只是讲述 Tomcat 的使用，我们先将项目改造一下，加上一点小功能，使其丰满一些，毕竟只有骨架的话还是比较 “ 吓人 ” 的。</p>
<p>前文中只是做了项目工程搭建，并没有进行功能代码的编写与整合，因此，在这篇文章中会对原 ssm-demo 项目进行小小的功能改造，增加一个功能：<strong>在浏览器输入一个 URL 地址，Spring MVC 接收到请求后通过 MyBatis 读取数据库中的数据跳转到对应的 JSP 页面并将读取的数据显示在 JSP 页面上。</strong></p>
<h4 id="1-1">1. 表结构设计</h4>
<p>如下所示：</p>
<pre><code>DROP TABLE IF EXISTS `tb_class_four`;
CREATE TABLE `tb_class_four` (
`id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
`description` varchar(100) NOT NULL DEFAULT '''''' COMMENT '描述',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
</code></pre>
<p>其中 description 是我们需要读取的字段。</p>
<h4 id="2-1">2. 实体类</h4>
<p>DescriptionDao.java，代码如下：</p>
<pre><code>package com.ssm.demo.entity;
import java.io.Serializable;
import java.sql.Date;
/**
* Created by 13 on 2018/6/27.
*/
public class Description implements Serializable {

/**
* 主键
*/
private Long id;

/**
* 描述
*/
private String description;

/**
* 添加时间
*/
private Date createTime;

...
</code></pre>
<h4 id="3dao">3. Dao 层</h4>
<p>DescriptionDao.java 代码如下：</p>
<pre><code>public interface DescriptionDao {

/**
* 获取最新一条描述
*
* @return
*/
Description getLastDescription();
}
</code></pre>
<p>DescriptionDao.xml，代码如下：</p>
<pre><code>&lt;mapper namespace="com.ssm.demo.dao.DescriptionDao"&gt;
&lt;resultMap type="com.ssm.demo.entity.Description" id="DescriptionResult"&gt;
&lt;result property="id" column="id"/&gt;
&lt;result property="description" column="description"/&gt;
&lt;result property="createTime" column="create_time"/&gt;
&lt;/resultMap&gt;

&lt;select id="getLastDescription" resultMap="DescriptionResult"&gt;
select id,description,create_time from
tb_class_four ORDER BY  id DESC limit 1
&lt;/select&gt;
&lt;/mapper&gt;
</code></pre>
<h4 id="4service">4. Service 层</h4>
<p>DescriptionService.java，代码如下：</p>
<pre><code>public interface DescriptionService {
/**
* 获取最新一条描述
*
* @return
*/
Description getLastDescription();
}
</code></pre>
<p>DescriptionServiceImpl.java，代码如下：</p>
<pre><code>//@Service注解一定不能忘记
@Service("descriptionService")
public class DescriptionServiceImpl implements DescriptionService {

@Autowired
private DescriptionDao descriptionDao;

@Override
public Description getLastDescription() {
return descriptionDao.getLastDescription();
}
}
</code></pre>
<h4 id="5controller">5. Controller 层</h4>
<p>DescriptionControler.java，代码如下：</p>
<pre><code>//@Controller 注解一定不能忘记
@Controller
//@RequestMapping表示类中的所有响应请求的方法都是以该地址作为父路径
@RequestMapping("/description")
public class DescriptionControler {

@Autowired
private DescriptionService descriptionService;

/**
* 通过ModelAndView对象获取信息
*/
@RequestMapping("/infoByMV")
public ModelAndView infoByMV() {
Description description = descriptionService.getLastDescription();
Map&lt;String, Object&gt; model = new HashMap&lt;String, Object&gt;();
model.put("description", description);
return new ModelAndView("description", model);
}

/**
* 通过HttpServletRequest对象获取信息
*/
@RequestMapping("/infoByRequest")
public String infoByRequest(HttpServletRequest request) {
Description description = descriptionService.getLastDescription();
request.setAttribute("description", description);
return "description";
}
}
</code></pre>
<h4 id="6view">6. View 层</h4>
<p>description.jsp，代码如下：</p>
<pre><code>&lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;
&lt;%@ page contentType="text/html;charset=UTF-8" language="java" %&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;ssm-demo&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;c:if test="${not empty description}"&gt;
${description.description}
&lt;/c:if&gt;
&lt;c:if test="${empty description}"&gt;
数据为空，请检查数据！
&lt;/c:if&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>到这里，一个简单的 SSM 整合的小功能就实现了，代码和 SQL 语句已经放到百度云盘，直接下载使用即可。</p>
<p>下面是这些代码成功部署后的效果和返回结果。</p>
<p>infoByMV.do：</p>
<p><img src="https://images.gitbook.cn/6a1e4bc0-8bd7-11e8-8998-e3cb09ec2904" alt="infoByMV" /></p>
<p>infoByRequest.do：</p>
<p><img src="https://images.gitbook.cn/60e72a20-8a71-11e8-affa-b587dc6ff574" alt="infoByRequest" /></p>
<h3 id="44ideatomcatssmdemo">4.4 IDEA 整合 Tomcat 部署 ssm-demo</h3>
<p>一般在开发过程中部署时，项目的部署是不会使用上面提到的这种方式（比较麻烦），而是通过 IDEA 或者 MyEclipse 等开发工具集成 Tomcat 服务器并直接部署到 Tomcat 服务器中，这种方式更加智能，相比较于前面提到的复制方法稍微自动化一些，本节将讲一下通过 IDEA 发布项目到 Tomcat 服务器的过程。</p>
<h4 id="1sdk">1. 设置 SDK</h4>
<p>这一步是个小插曲，忘记设置 SDK 了，打开项目后报错，设置步骤也很简单，点击 “ Set SDK ” ，然后添加 “ JDK ” ，将安装 JDK 的主目录填上就好，十三的 JDK 目录是  F:\Java\jdk1.8.0_171 ，步骤如下图：</p>
<p><img src="https://images.gitbook.cn/1fcd1940-8a72-11e8-8e15-d7b3f4327e66" alt="idea-set-jdk" /></p>
<h4 id="2tomcat">2. 设置 Tomcat 目录</h4>
<p>记得在第 02 课中提到下载 IDEA 时下载 Ultimate 收费版本，不建议朋友们下载社区版本，是因为社区版本里没有 Tomcat 插件。</p>
<p>点击 IDEA 上方的设置工具栏，点击 “ Edit Configurations... ” 按钮弹出设置框，点击左上角的 “ + ” 按钮，找到 “ Tomcat Server ”，选择 “ Local ” 即添加本地 Tomcat 服务器，跳到 Tomcat 服务器设置面板，这时可以设置一下 Tomcat 名称，不设置也可以，默认是 “ Unnamed ”，之后点击 “ Configure ” 按钮添加 Tomcat 目录，填上安装目录即可，十三的 JDK 目录是 D:\tomcat\apache-tomcat-8.5.31 ，步骤如下图：</p>
<p><img src="https://images.gitbook.cn/7df05f50-8a72-11e8-974b-497483da0812" alt="idea-set-tomcat" /></p>
<h4 id="3war">3. War 包设置</h4>
<p>Tomcat 目录设置完成后，到了最重要的一步，就是选择部署内容，此时的右下角会出现一个按钮 “ Fix ”，点击后会出现一个选择框 “ Select an artifact to deploy ”，选择 ssm-demo:war 即可。由于是 Maven 项目，因此不需要特别复杂的步骤，之后可以设置一下 Tomcat 的端口号，默认是 8080，整个过程如下图：</p>
<p><img src="https://images.gitbook.cn/c6cb57c0-8a72-11e8-a3f8-ff18634ae51e" alt="set-war" /></p>
<h4 id="4-1">4. 部署</h4>
<p>以上设置都完成后，就到了最激动人心的时刻，开始部署项目吧！</p>
<p>点击 IDEA 上方工具栏 ssm-demo 服务器右边的启动按钮，之后就可以静静地等待服务器启动了，可以看到下方的控制台一直在输出 Tomcat 日志，启动成功后就可以打开浏览器访问  ssm-demo 项目了，十三在前面写了一个简单的 SSM 框架整合的功能，启动后可以直接在浏览器上输入地址访问了：</p>
<blockquote>
  <p>http://localhost:8080/description/infoByRequest.do</p>
  <p>http://localhost:8080/description/infoByMV.do</p>
</blockquote>
<p>整个过程如下图：</p>
<p><img src="https://images.gitbook.cn/f3f56290-8a72-11e8-affa-b587dc6ff574" alt="idea-tomcat-startup" /></p>
<p>十三在这里提醒朋友们需要注意的是，一定要先把 SQL 语句导入到 MySQL 里，不然过程中可能会报错，SQL 文件和本节课程的源码，十三已经传到百度云盘里去了，请见文末，下载后稍作修改就能使用了。</p>
<h3 id="45">4.5 总结</h3>
<p>前四篇文章可能是较为基础的教程，基本上是基础环境的搭建和较为基础的 Java Web 知识，主要针对一些新入门的朋友，大部分都是安装和设置之类的教程，主要是希望学习本课程的朋友不要因为一些环境配置的小问题卡住，而导致后续的课程无法顺利进行。大家不要觉得十三啰嗦，面面俱到很难但是也要尽量保证所有人都能学到想要掌握的知识，过程应该还算比较详细的，希望大家都有收获。</p>
<p>基础部分到这里就告一段落了，接下来将开始准备本课程的实战部分。</p>
<blockquote>
  <p>本篇课程所用到的代码和安装包都已上传至百度云盘，提取地址如下：</p>
  <p>链接: https://pan.baidu.com/s/135-T54crMJBEYfD5VcOC6A </p>
  <p>密码: c5c6</p>
</blockquote></div></article>