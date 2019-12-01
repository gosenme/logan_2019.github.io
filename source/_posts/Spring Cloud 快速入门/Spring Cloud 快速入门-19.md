---
title: Spring Cloud 快速入门-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>接口开发完成并且测试通过后，就可以进行发布，系统发布可以有很多方式，本文将目前主要的发布方式一一列举出来，供大家参考。</p>
<h3 id="java">Java 命令行启动</h3>
<p>这种方式比较简单，由于 Spring Boot 默认内置了 Tomcat，我们只需要打包成 Jar，即可通过 Java 命令启动 Jar 包，即我们的应用程序。</p>
<p>首先，news 下面的每个子工程都加上（Client 除外）：</p>
<pre><code class="xml language-xml">&lt;packaging&gt;jar&lt;/packaging&gt;
</code></pre>
<p>此表示我们打包成 Jar 包。</p>
<p>其次，我们在每个 Jar 工程（除去 Commmon）的 pom.xml 中都加入以下内容：</p>
<pre><code class="xml language-xml">&lt;build&gt;
        &lt;!-- jar包名字，一般和我们的工程名相同 --&gt;
        &lt;finalName&gt;user&lt;/finalName&gt;
        &lt;sourceDirectory&gt;${project.basedir}/src/main/java&lt;/sourceDirectory&gt;
        &lt;testSourceDirectory&gt;${project.basedir}/src/test/java&lt;/testSourceDirectory&gt;
        &lt;resources&gt;
            &lt;resource&gt;
                &lt;directory&gt;src/main/resources&lt;/directory&gt;
                &lt;filtering&gt;true&lt;/filtering&gt;
            &lt;/resource&gt;
        &lt;/resources&gt;
        &lt;plugins&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
                &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
                &lt;configuration&gt;
                    &lt;fork&gt;true&lt;/fork&gt;
                    &lt;mainClass&gt;com.lynn.${project.build.finalName}.Application&lt;/mainClass&gt;
                &lt;/configuration&gt;
                &lt;executions&gt;
                    &lt;execution&gt;
                        &lt;goals&gt;
                            &lt;goal&gt;repackage&lt;/goal&gt;
                        &lt;/goals&gt;
                    &lt;/execution&gt;
                &lt;/executions&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;artifactId&gt;maven-resources-plugin&lt;/artifactId&gt;
                &lt;version&gt;2.5&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;encoding&gt;UTF-8&lt;/encoding&gt;
                    &lt;useDefaultDelimiters&gt;true&lt;/useDefaultDelimiters&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-surefire-plugin&lt;/artifactId&gt;
                &lt;version&gt;2.18.1&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;skipTests&gt;true&lt;/skipTests&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-compiler-plugin&lt;/artifactId&gt;
                &lt;configuration&gt;
                    &lt;source&gt;1.8&lt;/source&gt;
                    &lt;target&gt;1.8&lt;/target&gt;
                &lt;/configuration&gt;
                &lt;executions&gt;
                    &lt;!-- 替换会被 maven 特别处理的 default-compile --&gt;
                    &lt;execution&gt;
                        &lt;id&gt;default-compile&lt;/id&gt;
                        &lt;phase&gt;none&lt;/phase&gt;
                    &lt;/execution&gt;
                    &lt;!-- 替换会被 maven 特别处理的 default-testCompile --&gt;
                    &lt;execution&gt;
                        &lt;id&gt;default-testCompile&lt;/id&gt;
                        &lt;phase&gt;none&lt;/phase&gt;
                    &lt;/execution&gt;
                    &lt;execution&gt;
                        &lt;id&gt;java-compile&lt;/id&gt;
                        &lt;phase&gt;compile&lt;/phase&gt;
                        &lt;goals&gt; &lt;goal&gt;compile&lt;/goal&gt; &lt;/goals&gt;
                    &lt;/execution&gt;
                    &lt;execution&gt;
                        &lt;id&gt;java-test-compile&lt;/id&gt;
                        &lt;phase&gt;test-compile&lt;/phase&gt;
                        &lt;goals&gt; &lt;goal&gt;testCompile&lt;/goal&gt; &lt;/goals&gt;
                    &lt;/execution&gt;
                &lt;/executions&gt;
            &lt;/plugin&gt;
        &lt;/plugins&gt;
    &lt;/build&gt;
</code></pre>
<p>然后执行 <code>maven clean package</code> 命名打包：</p>
<p><img src="https://images.gitbook.cn/61566270-83e9-11e8-9df7-79b51aa97c78" alt="enter image description here" /></p>
<p><img src="https://images.gitbook.cn/69173f70-83e9-11e8-81e8-9d5996b3268d" alt="enter image description here" /></p>
<p>第一次运行可能需要花点时间，因为需要从 Maven 仓库下载所有依赖包，以后打包就会比较快，等一段时间后，打包完成：</p>
<p><img src="https://images.gitbook.cn/a3a27160-83ed-11e8-ab7e-29061e94f1ab" alt="enter image description here" /></p>
<p>最后，我们将 Jar 包上传到服务器，依次启动 register.jar、config.jar、gateway.jar、article.jar、comment.jar、index.jar、user.jar 即可，启动命令是：</p>
<pre><code class="shell language-shell">nohup java -server -jar xxx.jar &amp;
</code></pre>
<p>用 nohup 命令启动 Jar 才能使 Jar 在后台运行，否则 shell 界面退出后，程序会自动退出。</p>
<h3 id="tomcat">Tomcat 启动</h3>
<p>除了 Spring Boot 自带的 Tomcat，我们同样可以自己安装 Tomcat 来部署。</p>
<p>首先改造工程，将所有 <code>&lt;packaging&gt;jar&lt;/packaging&gt;</code> 改为 <code>&lt;packaging&gt;war&lt;/packaging&gt;</code>，去掉内置的 Tomcat：</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-tomcat&lt;/artifactId&gt;
            &lt;scope&gt;provided&lt;/scope&gt;
        &lt;/dependency&gt;
</code></pre>
<p>修改 build：</p>
<pre><code class="xml language-xml">&lt;build&gt;
        &lt;!-- 文件名 --&gt;
        &lt;finalName&gt;register&lt;/finalName&gt;
        &lt;resources&gt;
            &lt;resource&gt;
                &lt;directory&gt;src/main/resources&lt;/directory&gt;
                &lt;filtering&gt;true&lt;/filtering&gt;
            &lt;/resource&gt;
        &lt;/resources&gt;
        &lt;plugins&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
                &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;artifactId&gt;maven-resources-plugin&lt;/artifactId&gt;
                &lt;version&gt;2.5&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;encoding&gt;UTF-8&lt;/encoding&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-surefire-plugin&lt;/artifactId&gt;
                &lt;version&gt;2.18.1&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;skipTests&gt;true&lt;/skipTests&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
        &lt;/plugins&gt;
    &lt;/build&gt;
</code></pre>
<p>然后修改启动类 Application.java：</p>
<pre><code class="java language-java">public class Application extends SpringBootServletInitializer{

    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(Application.class);
    }
}
</code></pre>
<p>这样打包后就会生成 War 包，打包方式同上。</p>
<p>我们将 War 上传到服务器的 Tomcat 上即可通过 Tomcat 启动项目。</p>
<h3 id="jenkins">Jenkins 自动化部署</h3>
<p>我们搭建的是一套微服务架构，真实环境可能有成百上千个工程，如果都这样手动打包、上传、发布，工作量无疑是巨大的。这时，我们就需要考虑自动化部署了。</p>
<p>Jenkins 走进了我们的视野，它是一个开源软件项目，是基于 Java 开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。</p>
<p>下面，我们就来看看如果通过 Jenkins 实现系统的自动化部署。</p>
<h4 id="">安装</h4>
<p>Jenkins 的安装方式请自行百度，本文不做详细说明。</p>
<p><strong>注：</strong> 安装好后，至少需要安装 Maven、SSH、Git、SVN 插件。</p>
<h4 id="-1">创建任务</h4>
<p>安装好后，访问 Jenkins，登录后，即可看到如下界面：</p>
<p><img src="https://images.gitbook.cn/6c202290-83fd-11e8-a776-a97be0899301" alt="enter image description here" /></p>
<p>（1）点击系统管理 -&gt; 系统设置，添加服务器 SSH 信息：</p>
<p><img src="https://images.gitbook.cn/4f665b00-83fe-11e8-9149-dd330c2a1b31" alt="enter image description here" /></p>
<p>（2）点击系统管理 -&gt; 全局工具配置，配置好 JDK 和 Maven：</p>
<p><img src="https://images.gitbook.cn/93292840-83fe-11e8-aac1-63307eeea99f" alt="enter image description here" /></p>
<p>（3）点击新建任务，输入任务名，选择构建一个 Maven 风格的软件：</p>
<p><img src="https://images.gitbook.cn/a5f8f140-83fd-11e8-81e8-9d5996b3268d" alt="enter image description here" /></p>
<p>（4）点击确定，进入下一步：</p>
<p><img src="https://images.gitbook.cn/b5a0db70-83fe-11e8-ab7e-29061e94f1ab" alt="enter image description here" /></p>
<p>这里以 SVN 为例说明（如果代码在 Git上，操作类似），将源码的 SVN 地址、SVN 账号信息依次填入文本框。</p>
<p><img src="https://images.gitbook.cn/f6865250-83fe-11e8-889e-a3559e13e7b0" alt="enter image description here" /></p>
<p>Build 下面填入 Maven 的构建命令。</p>
<p>在“构建后操作”里按要求填入如图所示内容：</p>
<p><img src="https://images.gitbook.cn/4c960780-83ff-11e8-9df7-79b51aa97c78" alt="enter image description here" /></p>
<p>其中，启动脚本示例如下：</p>
<pre><code class="shell language-shell">kill -9 $(netstat -tlnp|grep 8080|awk '{print $7}'|awk -F '/' '{print $1}')
cd /app/hall
java -server -jar hall.jar &amp;
</code></pre>
<p>点击保存。</p>
<h4 id="-2">手动构建</h4>
<p>任务创建好后，点击“立即构建”即可自动构建并启动我们的应用程序，并且能够实时看到构建日志：</p>
<p><img src="https://images.gitbook.cn/aa466780-83ff-11e8-ab7e-29061e94f1ab" alt="enter image description here" /></p>
<h4 id="-3">自动构建</h4>
<p>我们每次都手动点击“立即构建”也挺麻烦，程序猿的最高进阶是看谁更懒，我都不想点那个按钮了，就想我提交了代码能自动构建，怎么做呢？很简单，进入任务配置界面，找到构建触发器选项：</p>
<p><img src="https://images.gitbook.cn/0c6ee220-8400-11e8-9df7-79b51aa97c78" alt="enter image description here" /></p>
<p>保存后，Jenkins 会每隔两分钟对比一下 SVN，如果有改动，则自动构建。</p>
<h3 id="-4">总结</h3>
<p>系统发布方式很多，我们可以根据自身项目特点选择适合自己的方式，当然还有很多方式，比如 K8S、Docker 等等，这里就不再赘述了 ，关于 K8S+Docker 的方式，我会在第20课讲解。</p></div></article>