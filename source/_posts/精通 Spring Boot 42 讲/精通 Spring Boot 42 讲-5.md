---
title: 精通 Spring Boot 42 讲-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>使用 Spring Boot 开发项目需要有两个基础环境和一个开发工具，这两个环境是指 Java 编译环境和构建工具环境，一个开发工具是指 IDE 开发工具。</p>
<p>Spring Boot 2.0 要求 Java 8 作为最低版本，需要在本机安装 JDK 1.8 并进行环境变量配置，同时需要安装构建工具编译 Spring Boot 项目，最后准备一个顺手的 IDE 开发工具即可。</p>
<p>构建工具是一个把源代码生成可执行应用程序的自动化工具，Java 领域中主要有三大构建工具：Ant、Maven 和 Gradle。</p>
<ul>
<li>Ant（AnotherNeatTool）的核心是由 Java 编写，采用 XML 作为构建脚本，这样就允许你在任何环境下运行构建。Ant 是 Java 领域最早的构建工具，不过因为操作复杂，慢慢的已经被淘汰了。</li>
<li>Maven，Maven 发布于 2004 年，目的是解决程序员使用 Ant 所带来的一些问题，它的好处在于可以将项目过程规范化、自动化、高效化以及强大的可扩展性。</li>
<li>Gradle，Gradle 是一个基于 Apache Ant 和 Apache Maven 概念的项目自动化建构工具。它使用一种基于 Groovy 的特定领域语言来声明项目设置，而不是传统的 XML。结合了前两者的优点，在此基础之上做了很多改进，它具有 Ant 的强大和灵活，又有 Maven 的生命周期管理且易于使用。</li>
</ul>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/build.jpg" alt="" /></p>
<p>Spring Boot 官方支持 Maven 和 Gradle 作为项目构建工具。Gradle 虽然有更好的理念，但是相比 Maven 来讲其行业使用率偏低，并且 Spring Boot 官方默认使用 Maven，因此本系列专栏选择使用 Maven 作为 Spring Boot 项目构建工具。</p>
<p>Java 领域最流行的 IDE 开发工具有 Eclipse 和 IDEA。Eclipse 是 Java 的集成开发环境（IDE），也是 Java 领域最流行的 IDE 开发工具之一，只是 Eclipse 这些年发展缓慢，慢慢的有些陈旧。IDEA（IntelliJ IDEA）是用于 Java 语言开发的集成环境，在业界被公认为是最好的 Java 开发工具之一，尤其在智能代码助手、代码自动提示、重构、J2EE 支持、创新的 GUI 设计等方面的功能可以说是超常的。因此强烈推荐大家使用 IntelliJ IDEA 开发 Spring Boot 项目。</p>
<p>接下来将介绍如何搭建基础环境以及 IntelliJ IDEA 的安装。</p>
<h3 id="jdk">安装 JDK</h3>
<h4 id="">下载安装</h4>
<p>首先打开 <a href="http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html">Oracle 官网 JDK 1.8 下载页面</a>，根据下图选择下载各系统对应的版本，这里以 Win10 64 位操作系统为例。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/jdk8.png" alt="" /></p>
<p>下载完成之后，双击鼠标进行安装，一直单击“下一步”按钮直至安装完毕。</p>
<h4 id="-1">环境变量配置</h4>
<p>JDK 安装完毕后，接下来配置 JDK 环境变量，选择“我的电脑” | “属性” | “高级系统设置” | “环境变量” | “新建”命令： </p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/jdk8_hj.png" alt="" /></p>
<p>在弹出的对话框中新建<code>JAVA_HOME</code>变量以及 Java 安装地址，如下图：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/java_home.png" alt="" /></p>
<p>单击“确定”按钮后，回到环境变量界面，双击<code>Path</code>变量，添加两条 JDK 路径，如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/jdk8_path.png" alt="" /></p>
<p>以上，Java 环境变量配置完毕！</p>
<h4 id="-2">测试</h4>
<p>配置完成之后，测试一下 JDK 是否配置正确，Win10 下使用快捷 window+r 输入 cmd 命令，进入运行窗口，执行命令<code>java -version</code>，若出现如下结果，则表示安装成功！</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/jdk8_v.png" alt="" /></p>
<h3 id="maven">安装 Maven</h3>
<p>安装 Maven 的前提是完成 Java 环境安装，Maven 依赖于 Java 环境。</p>
<h4 id="-3">下载安装</h4>
<p>访问 <a href="http://maven.apache.org/download.cgi">Maven 官网</a>下载 Maven 对应的压缩包，如下：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/mvn_install.png" alt="" /></p>
<p>选择 Maven 的 zip 压缩包（apache-maven-3.5.4.zip），下载完成后解压到本机目录下。例如，路径：<code>D:\Common Files\apache-maven-3.5.4</code>：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/mvn_ml.png" alt="" /></p>
<blockquote>
  <p>Maven 为绿色软件解压后即可使用。</p>
</blockquote>
<h4 id="-4">环境变量配置</h4>
<p>按照上面步骤打开环境变量设置页面，双击 Path 变量，将上一步解压的目录添加到 Path 中。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/mvn_path.png" alt="" /></p>
<p>以上，Maven 环境配置完毕！</p>
<h4 id="-5">测试</h4>
<p>Win10 下使用快捷 window+r 输入 cmd 命令，弹出“运行”对话框，执行命令 mvn -v，若出现如下结果，则表示安装成功！</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/mvn_v.png" alt="" /></p>
<h4 id="settingsxml">settings.xml 设置</h4>
<p>Maven 解压后目录下会有一个 settings.xml 文件，位置：<code>${M2_HOME}/conf/settings.xml</code>，用来配置 Maven 的仓库和本地 Jar 包存储地址。Maven 仓库地址代表从哪里去下载项目中的依赖包 Jar 包；Maven 会将所有的 Jar 包统一存储到一个地址下，方便各个项目复用。</p>
<p>localRepository 设置本地存放 Jar 包地址，可以根据自己的情况改动：</p>
<pre><code>&lt;localRepository&gt;D:\Common Files\maven\repository&lt;/localRepository&gt;
</code></pre>
<p>mirrors 为仓库列表配置的下载镜像列表：</p>
<pre><code>&lt;mirrors&gt;
    &lt;mirror&gt;  
        &lt;id&gt;repo2&lt;/id&gt;  
        &lt;mirrorOf&gt;central&lt;/mirrorOf&gt;  
        &lt;name&gt;spring2.0 for this Mirror.&lt;/name&gt;  
        &lt;url&gt;https://repo.spring.io/libs-milestone&lt;/url&gt;  
    &lt;/mirror&gt;
    ...
&lt;mirrors&gt;
</code></pre>
<p>为了方便大家使用，我已经配好了一份 settings.xml 模板，可下载后直接覆盖默认的 settings.xml 文件，覆盖完成后需要修改 localRepository 路径。</p>
<p><a href="https://github.com/ityouknow/spring-boot-leaning/blob/gitbook_column2.0/settings.xml">模板 settings.xml 文件地址，详见这里。</a></p>
<h3 id="intellijidea">IntelliJ IDEA 安装</h3>
<h4 id="-6">下载</h4>
<p>打开 IntelliJ IDEA 2018 <a href="https://www.jetbrains.com/idea/download/#section=windows">官方下载地址</a>，IDEA 分为两种版本，即社区版和商业版，商业版是付费的，其功能多，社区版是免费的，功能相对较少。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/idea1.png" alt="" /></p>
<h4 id="-7">安装</h4>
<p>下载完成后，双击安装包开始安装，一直单击 Next 按钮：</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/idea2.png" alt="" /></p>
<p>安装过程中会选择安装路径，展示 32 或者 64 位的启动快捷键，最后单击 Finish 按钮，安装完成。</p>
<h4 id="-8">配置</h4>
<p>安装完成后，第一次会提示选择配置设置，选择下面一个，单击 OK 按钮。</p>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/idea3.png" alt="" /></p>
<p>后面选择同意协议，输入“License server”激活软件，根据自己的习惯选择白色或者黑色的默认主题，然后选择 IntelliJ IDEA 支持的扩展功能，也可以使用默认选项，然后直接单击“下一步”按钮，最后单击 Start using IntelliJ IDEA 按钮完成配置。</p>
<p>以上，开发工具安装完毕！</p>
<h3 id="-9">构建项目</h3>
<p>我们有两种方式来构建 Spring Boot 项目基础框架，第一种是使用 Spring 官方提供的构建页面；第二种是使用 IntelliJ IDEA 中的 Spring 插件来创建。</p>
<p><strong>使用 Spring 官方提供页面构建</strong></p>
<ul>
<li>访问 http://start.spring.io/ 网址。  </li>
<li>选择构建工具 Maven Project，编程语言选择 Java、Spring Boot 版本 2.0.5 以及一些工程基本信息，具体可参考下图。</li>
</ul>
<p><img src="http://www.ityouknow.com/assets/images/2018/springboot/sb_start.png" alt="" /></p>
<ul>
<li>单击 Generate Project 下载项目压缩包。</li>
<li>解压后，使用 IDEA 导入项目，选择 File | New | Model from Existing Source.. | 选择解压后的文件夹 | OK 命令，选择 Maven，一路单击 Next 按钮，OK done! </li>
<li>如果使用的是 Eclipse，选择 Import | Existing Maven Projects | Next | 选择解压后的文件夹 | Finsh 按钮，OK done! </li>
</ul>
<p><strong>使用 IDEA 构建</strong></p>
<ul>
<li>选择 File | New | Project... 命令，弹出新建项目的对话框。</li>
<li>选择 Spring Initializr，Next 也会出现上述类似的配置界面，IDEA 帮我们做了集成。</li>
</ul>
<p><img src="http://www.ityouknow.com/assets/images/2018/it/idea4.png" alt="" /></p>
<ul>
<li>填写相关内容后，单击 Next 按钮，选择依赖的包再单击 Next 按钮，最后确定信息无误单击 Finish 按钮。</li>
</ul>
<p>对上面的配置做如下解释。</p>
<ul>
<li>第一个选择框选择创建以 Maven 构建项目，还是以 Gradle 构建项目，这是两种不同的构建方式，其中 Gradle 配置内容更简洁一些，并且包含了 maven 的使用，但我们日常使用 maven 居多。   </li>
<li>第二个选择框选择编程语言，现在支持 Java、Kotlin 和 Groovy。</li>
<li>第三个选择框选择 Spring Boot 版本，可以看出 Spring Boot 2.0 的最新版本是 2.0.5。</li>
</ul>
<p>下面就是项目的配置信息了。</p>
<ul>
<li>Group，一般填写公司域名，比如百度公司就会填：com.baidu，演示使用 com.neo。</li>
<li>Artifact，可以理解为项目的名称了，可以根据实际情况来填，本次演示填 hello。</li>
<li>Dependencies，在这块添加我们项目所依赖的 Spring Boot 组件，可以多选，本次选择 Web、Devtools 两个模块。</li>
</ul>
<h3 id="-10">项目结构介绍</h3>
<p><img src="https://images.gitbook.cn/FktcuZJEMOOLhWyOg_VPdp1zmwc_" alt="avatar" /></p>
<p>如上图所示，Spring Boot 的基础结构共三个文件，具体如下：</p>
<ul>
<li>src/main/java：程序开发以及主程序入口；</li>
<li>src/main/resources：配置文件；</li>
<li>src/test/java：测试程序。</li>
</ul>
<p>另外，Spring Boot 建议的目录结构如下。</p>
<p>com.example.myproject 目录下：</p>
<pre><code>myproject
 +-src
    +- main
         +- java
              +- com.example.myproject
                    +- comm
                    +- model
                    +- repository
                    +- service
                    +- web
                    +- Application.java
         +- resources
              +- static
              +- templates
              +- application.properties
    +- test
 +-pom.xml
</code></pre>
<p>com.example.myproject 目录下：</p>
<ul>
<li>Application.java，建议放到根目录下面，是项目的启动类，Spring Boot 项目只能有一个 main() 方法；</li>
<li>comm 目录建议放置公共的类，如全局的配置文件、工具类等；</li>
<li>model 目录主要用于实体（Entity）与数据访问层（Repository）；</li>
<li>repository 层主要是数据库访问层代码；</li>
<li>service 层主要是业务类代码；</li>
<li>web 层负责页面访问控制。</li>
</ul>
<p>resources 目录下：</p>
<ul>
<li>static 目录存放 web 访问的静态资源，如 js、css、图片等；</li>
<li>templates 目录存放页面模板；</li>
<li>application.properties 存放项目的配置信息。</li>
</ul>
<p>test 目录存放单元测试的代码；pom.xml 用于配置项目依赖包，以及其他配置。</p>
<p>采用默认配置可以省去很多设置，也可以根据公司的规范进行修改，至此一个 Java 项目搭建好了！</p>
<h3 id="pom">Pom 包介绍</h3>
<p>pom.xml 文件主要描述了项目包的依赖和项目构建时的配置，在默认的 pom.xml 包中分为四大块。</p>
<p>第一部分为项目的描述信息：</p>
<pre><code class="xml language-xml">&lt;groupId&gt;com.neo&lt;/groupId&gt;
&lt;artifactId&gt;hello&lt;/artifactId&gt;
&lt;version&gt;2.0.5.RELEASE&lt;/version&gt;
&lt;packaging&gt;jar&lt;/packaging&gt;

&lt;name&gt;hello&lt;/name&gt;
&lt;description&gt;Demo project for Spring Boot&lt;/description&gt;
</code></pre>
<ul>
<li>groupId，项目的包路径；</li>
<li>artifactId，项目名称；</li>
<li>version，项目版本号；</li>
<li>packaging，一般有两个值：jar、war，表示使用 Maven 打包时构建成 Jar 包还是 War 包；</li>
<li>name，项目名称；</li>
<li>description，项目描述。</li>
</ul>
<p>第二部分为项目的依赖配置信息：</p>
<pre><code class="xml language-xml">&lt;parent&gt;
  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
  &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
  &lt;version&gt;2.0.5.RELEASE&lt;/version&gt;
  &lt;relativePath/&gt; &lt;!-- lookup parent from repository --&gt;
&lt;/parent&gt;

&lt;dependencies&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-devtools&lt;/artifactId&gt;
    &lt;scope&gt;runtime&lt;/scope&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-test&lt;/artifactId&gt;
    &lt;scope&gt;test&lt;/scope&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<ul>
<li>parent，标签内配置 Spring Boot 父级版本 spring-boot-starter-parent，Maven 支持项目的父子结构，引入父级后会默认继承父级的配置；</li>
<li>dependencies，标签内配置项目所需要的依赖包，Spring Boot 体系内的依赖组件不需要填写具体版本号，spring-boot-starter-parent 维护了体系内所有依赖包的版本信息。</li>
</ul>
<p>第三部分为构建时需要的公共变量：</p>
<pre><code class="xml language-xml">&lt;properties&gt;
  &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt;
  &lt;project.reporting.outputEncoding&gt;UTF-8&lt;/project.reporting.outputEncoding&gt;
  &lt;java.version&gt;1.8&lt;/java.version&gt;
&lt;/properties&gt;
</code></pre>
<p>上面配置了项目构建时所使用的编码，输出所使用的编码，最后指定了项目使用的 JDK 版本。</p>
<p>第四部分为构建配置：</p>
<pre><code class="xml language-xml">&lt;build&gt;
  &lt;plugins&gt;
    &lt;plugin&gt;
      &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
      &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
    &lt;/plugin&gt;
  &lt;/plugins&gt;
&lt;/build&gt;
</code></pre>
<p>使用 Maven 构建 Spring Boot 项目必须依赖于 spring-boot-maven-plugin 组件，spring-boot-maven-plugin 能够以 Maven 的方式为应用提供 Spring Boot 的支持，即为 Spring Boot 应用提供了执行 Maven 操作的可能。spring-boot-maven-plugin 能够将 Spring Boot 应用打包为可执行的 jar 或 war 文件，然后以简单的方式运行 Spring Boot 应用。</p>
<p>以上即为 pom.xml 文件基础内容，几乎所有的 Spring Boot 项目都会用到以上配置信息。</p>
<h3 id="-11">总结</h3>
<p>这一讲我们介绍了 Spring Boot 所依赖的基础环境，如何去搭建 JDK、Maven 环境，安装开发工具 IDEA；对 Spring Boot 项目结构进行了解读，介绍了 pom.xml 文件内容的含义。通过本讲的学习，我们发现构建 Spring Boot 项目更简单方便，相比传统项目，Spring Boot 项目配置更加灵活。</p>
<blockquote>
  <p><a href="https://github.com/ityouknow/spring-boot-leaning/tree/gitbook_column2.0">点击这里下载源码</a>。</p>
</blockquote></div></article>