---
title: SSM 博客系统开发实战-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">基础环境安装及配置</h3>
<h4 id="jdk">JDK 下载及环境变量配置</h4>
<p>在官网上，根据自己的系统配置（32/64位）选择相应的版本进行下载（附：<a href="http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html">下载地址</a>）。下载完成后安装到自己喜欢的目录下。</p>
<p>安装完成后，我们进行环境变量配置。按该步骤进行操作：电脑 -&gt; 属性 -&gt; 高级系统设置 -&gt; 环境变量 -&gt; 系统变量 -&gt;新建。在对应输入框内填入以下内容：</p>
<blockquote>
  <p>变量名：<code>JAVA_HOME</code>，变量值：<code>D:\softs\java\jdk1.8.0_111</code>
  变量名：CLASSPATH，变量值：<code>.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;</code></p>
</blockquote>
<p>点击已有的 path 变量打开，Win10 系统直接新建，输入：</p>
<pre><code class="     language-    ">%JAVA_HOME%\bin  
</code></pre>
<p>再新建，输入：</p>
<pre><code>%JAVA_HOME%\jre\bin   
</code></pre>
<p>其他系统直接在 path 变量值的最后添加以下内容，注意与前面的配置要用“;”隔开：</p>
<pre><code>%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;
</code></pre>
<p>最后通过 cmd 打开命令提示符，键入：</p>
<pre><code class="     language-    ">java -version
</code></pre>
<p>查看版本号，若出现 Java 版本信息，说明安装并配置成功！</p>
<h4 id="maven">Maven下载并配置环境变量</h4>
<p>这里给出它的下载地址，请访问<a href="http://maven.apache.org/download.cgi">这里</a>。下载完成后解压到自己喜欢的目录下</p>
<p>接下来进行环境变量配置。</p>
<p>配置步骤同上，这次在“新建系统变量”对话框中键入的内容请见下：</p>
<blockquote>
  <p>变量名：<code>MAVEN_HOME</code>，变量值：<code>D:\softs\java\apache-maven-3.3.9</code></p>
</blockquote>
<p>在 path 变量中加入 MAVEN_HOME：</p>
<pre><code class="     language-    ">%MAVEN_HOME%\bin
</code></pre>
<p>最后重新打开 cmd 命令提示符，键入：</p>
<pre><code class="     language-    ">mvn -version
</code></pre>
<p>查看 Maven版本，如出现 Maven 版本信息，说明配置成功！</p>
<h3 id="maven-1">Maven 创建父子工程</h3>
<h4 id="maven-2">创建 Maven 父工程</h4>
<p>如果 IDEA 已打开其他项目，可通过这一操作：File -&gt; Close Project，关闭现有项目，然后通过：Create New Project -&gt; Maven，创建父工程，直接点击 next，父工程就是空的工程，不需要勾选骨架。如下图所示。</p>
<p><img src="http://images.gitbook.cn/1568e0c0-5821-11e8-a6ee-37cda6a3c12b" alt="" /></p>
<p>填写好 GroupId、ArtifactId、Version 并选择好项目目录后点击 Finish，父工程就创建好了，我们命名为“dreamland”。</p>
<h4 id="maven-3">创建 Maven 子工程</h4>
<p>点击刚创建的父工程 dreamland，然后进行如下操作：File -&gt; New -&gt; Moudle -&gt; Maven，见下图所示：</p>
<p><img src="http://images.gitbook.cn/61346970-5821-11e8-af46-6927e96ff1fc" alt="" /></p>
<p>勾选 Web 骨架后点击 Next，填写好 ArtifactId 后点击 Next。</p>
<p>在这里要选择一个自己的 Maven 路径和仓库位置，还有要添加一个属性：</p>
<blockquote>
  <p>archetypeCatalog=internal</p>
</blockquote>
<p>这个参数的意义是让该 Maven 项目的骨架不要到远程下载而是从本地获取，以提高加载速度。</p>
<p><img src="http://images.gitbook.cn/9c9c1580-5821-11e8-a6ee-37cda6a3c12b" alt="" /></p>
<p>创建好的整体目录结构如下：</p>
<p><img src="http://images.gitbook.cn/e5e008f0-5821-11e8-8d22-65464154359e" alt="" /></p>
<p>可以看到我们的 dreamland-web 子工程没有 java、resources 和 test 目录，我们需要手动创建一下，操作过程如下：</p>
<blockquote>
  <p>main -&gt; New -&gt; Directory ==&gt; 创建 java</p>
  <p>main -&gt; New -&gt; Directory ==&gt; 创建 resources</p>
  <p>src -&gt; New -&gt; Directory ==&gt; 创建 test</p>
  <p>test -&gt; New -&gt; Directory ==&gt; 创建 java</p>
  <p>test -&gt; New -&gt; Directory ==&gt; 创建 resources</p>
</blockquote>
<p>然后对创建好的 java、resources 和 test/java、test/resourcs 目录均右键选择 Mark Diretory as，然后分别进行如下操作：</p>
<blockquote>
  <p>java -&gt; Sources Root //java源码根目录</p>
  <p>resources -&gt; Resources Root//java 配置文件目录</p>
  <p>test/java -&gt; Test Sources Root//java 测试源码目录</p>
  <p>test/java -&gt; Test Sources Root//java 测试配置文件目录</p>
</blockquote>
<p>如下图所示：</p>
<p><img src="http://images.gitbook.cn/cba746f0-5822-11e8-af46-6927e96ff1fc" alt="" /></p>
<p>最后整体的目录结构如下：</p>
<p><img src="http://images.gitbook.cn/dadda010-5822-11e8-af46-6927e96ff1fc" alt="" /></p>
<p>这样 Maven 父子工程就创建好了！</p></div></article>