---
title: 案例上手 Spring 全家桶-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在 Web 项目中，文件上传功能几乎是必不可少的，实现的技术有很多，这节课我们来学习如何使用 Spring MVC 框架完成文件的上传以及下载。</p>
<p>首先我们来学习文件上传，这里介绍两种上传方式：单文件上传和多文件批量上传。</p>
<h3 id="-1">单文件上传</h3>
<p>（1）底层使用的是 Apache fileupload 组件完成上传功能，Spring MVC 只是对其进行了封装，让开发者使用起来更加方便，因此首先需要在 pom.xml 中引入 fileupload 组件依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
    &lt;groupId&gt;commons-io&lt;/groupId&gt;
    &lt;artifactId&gt;commons-io&lt;/artifactId&gt;
    &lt;version&gt;1.3.2&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
    &lt;groupId&gt;commons-fileupload&lt;/groupId&gt;
    &lt;artifactId&gt;commons-fileupload&lt;/artifactId&gt;
    &lt;version&gt;1.2.1&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>（2）JSP 页面做如下处理：</p>
<ul>
<li>input 的 type 设置为 file</li>
<li>form 表单的 method 设置为 post（get 请求只会将文件名传给后台）</li>
<li>form 表单的 enctype 设置为 multipart/form-data，以二进制的形式传输数据</li>
</ul>
<pre><code class="jsp language-jsp">&lt;form action="upload" method="post" enctype="multipart/form-data"&gt;
    &lt;input type="file" name="img"&gt;
    &lt;input type="submit" name="提交"&gt;
&lt;/form&gt;&lt;br /&gt; 
&lt;c:if test="${filePath!=null }"&gt;
    &lt;h1&gt;上传的图片&lt;/h1&gt;&lt;br /&gt; 
    &lt;img width="300px" src="&lt;%=basePath %&gt;${filePath}"/&gt;
&lt;/c:if&gt;
</code></pre>
<p>如果上传成功，返回当前页面，展示上传成功的图片，这里需要使用 JSTL 标签进行判断，在 pom.xml 中引入 JSTL 依赖。</p>
<pre><code class="xml language-xml">&lt;dependency&gt;
     &lt;groupId&gt;jstl&lt;/groupId&gt;
     &lt;artifactId&gt;jstl&lt;/artifactId&gt;
     &lt;version&gt;1.2&lt;/version&gt;
&lt;/dependency&gt;
&lt;dependency&gt;
     &lt;groupId&gt;taglibs&lt;/groupId&gt;
     &lt;artifactId&gt;standard&lt;/artifactId&gt;
     &lt;version&gt;1.1.2&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>
<p>（3）完成业务方法，使用 MultipartFile 对象作为参数，接收前端发送过来的文件，并完成上传操作。</p>
<pre><code class="java language-java">@RequestMapping(value="/upload", method = RequestMethod.POST)
public String upload(@RequestParam(value="img")MultipartFile img, HttpServletRequest request)
  throws Exception {
  //getSize() 方法获取文件的大小来判断是否有上传文件
  if (img.getSize() &gt; 0) {
    //获取保存上传文件的 file 文件夹绝对路径
    String path = request.getSession().getServletContext().getRealPath("file");
    //获取上传文件名
    String fileName = img.getOriginalFilename();
    File file = new File(path, fileName);
    img.transferTo(file);
    //保存上传之后的文件路径
    request.setAttribute("filePath", "file/"+fileName);
    return "upload";
  }
  return "error";
}
</code></pre>
<p>（4）在 springmvc.xml 中配置 CommonsMultipartResolver</p>
<pre><code class="xml language-xml">&lt;!-- 配置 CommonsMultipartResolver bean，id 必须是 multipartResolver --&gt;
&lt;bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver"&gt;
    &lt;!-- 处理文件名中文乱码 --&gt;
    &lt;property name="defaultEncoding" value="utf-8"/&gt;
    &lt;!-- 设置多文件上传，总大小上限，不设置默认没有限制，单位为字节，1M=1*1024*1024 --&gt;
    &lt;property name="maxUploadSize" value="1048576"/&gt;
    &lt;!-- 设置每个上传文件的大小上限 --&gt;
    &lt;property name="maxUploadSizePerFile" value="1048576"/&gt;
&lt;/bean&gt;

&lt;!-- 设置异常解析器 --&gt;
&lt;bean class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver"&gt;
    &lt;property name="defaultErrorView" value="/error.jsp"/&gt;
&lt;/bean&gt;
</code></pre>
<p>（5）运行，如下图所示：</p>
<p><img src="https://images.gitbook.cn/8d0b9800-9a18-11e8-9724-fb3ff7de9e38" width = "50%" /></p>
<p>上传成功如下图所示：</p>
<p><img src="https://images.gitbook.cn/91b8cc60-9a18-11e8-bd2f-43e393597943" width = "50%" /></p>
<h3 id="-2">多文件上传</h3>
<p>（1）JSP</p>
<pre><code class="jsp language-jsp">&lt;form action="uploads" method="post" enctype="multipart/form-data"&gt;
    file1:&lt;input type="file" name="imgs"&gt;&lt;br /&gt;
    file2:&lt;input type="file" name="imgs"&gt;&lt;br /&gt; 
    file3:&lt;input type="file" name="imgs"&gt;&lt;br /&gt;  
    &lt;input type="submit" name="提交"&gt;
&lt;/form&gt;
&lt;c:if test="${filePaths!=null }"&gt;
    &lt;h1&gt;上传的图片&lt;/h1&gt;&lt;br /&gt; 
    &lt;c:forEach items="${filePaths }" var="filePath"&gt;
        &lt;img width="300px" src="&lt;%=basePath %&gt;${filePath}"/&gt;
    &lt;/c:forEach&gt;
&lt;/c:if&gt;
</code></pre>
<p>（2）业务方法，使用 MultipartFile 数组对象接收上传的多个文件</p>
<pre><code class="java language-java">@RequestMapping(value="/uploads", method = RequestMethod.POST)
public String uploads(@RequestParam MultipartFile[] imgs, HttpServletRequest request)
  throws Exception {
  //创建集合，保存上传后的文件路径
  List&lt;String&gt; filePaths = new ArrayList&lt;String&gt;();
  for (MultipartFile img : imgs) {
    if (img.getSize() &gt; 0) {
      String path = request.getSession().getServletContext().getRealPath("file");
      String fileName = img.getOriginalFilename();
      File file = new File(path, fileName);
      filePaths.add("file/"+fileName);
      img.transferTo(file);
    }
  }
  request.setAttribute("filePaths", filePaths);
  return "uploads";
}
</code></pre>
<p>（3）运行，如下图所示</p>
<p><img src="https://images.gitbook.cn/a8614640-9a18-11e8-9724-fb3ff7de9e38" width = "60%" /></p>
<p>上传成功如下图所示</p>
<p><img src="https://images.gitbook.cn/ac7e6fa0-9a18-11e8-9724-fb3ff7de9e38" width = "60%" /></p>
<p>完成了文件上传，接下来我们学习文件下载的具体使用。</p>
<p>（1）在 JSP 页面中使用超链接，下载之前上传的 logo.png。</p>
<pre><code class="jsp language-jsp">&lt;a href="download?fileName=logo.png"&gt;下载图片&lt;/a&gt;
</code></pre>
<p>（2）业务方法。</p>
<pre><code class="java language-java">@RequestMapping("/download")
public void downloadFile(String fileName,HttpServletRequest request,
                         HttpServletResponse response){
  if(fileName!=null){
    //获取 file 绝对路径
    String realPath = request.getServletContext().getRealPath("file/");
    File file = new File(realPath,fileName);
    OutputStream out = null;
    if(file.exists()){
      //设置下载完毕不打开文件 
      response.setContentType("application/force-download");
      //设置文件名 
      response.setHeader("Content-Disposition", "attachment;filename="+fileName);
      try {
        out = response.getOutputStream();
        out.write(FileUtils.readFileToByteArray(file));
        out.flush();
      } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
      }finally{
        if(out != null){
          try {
            out.close();
          } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
          }
        }
      }                    
    }           
  }           
}
</code></pre>
<p>（3）运行，如下所示。</p>
<p><img src="https://images.gitbook.cn/b6a92b40-9a19-11e8-8334-9bfa28241acd" width = "70%" /></p>
<p>下载成功如下所示。</p>
<p><img src="https://images.gitbook.cn/bb561180-9a19-11e8-992f-9dfb28d2b53f" width = "70%" /></p>
<h3 id="-3">总结</h3>
<p>本节课我们讲解了 Spring MVC 框架对于文件上传和下载的支持，文件上传和下载底层是通过 IO 流完成的，上传就是将客户端的资源通过 IO 流写入服务端，下载刚好相反，将服务端资源通过 IO 流写入客户端。Spring MVC 提供了一套完善的上传下载机制，可以有效地简化开发步骤。</p>
<h3 id="-4">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/Spring-MVC-UploadDownload.git">请单击这里下载源码</a></p></div></article>