---
title: 案例上手 Spring 全家桶-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>在正式开始学习本讲内容之前，先来思考一个问题，为什么要使用 Spring MVC 表单标签库？答案很简单，使用它是为了简化代码的开发，提高我们的开发效率，其实我们使用任何一款框架或者工具都是出于这个目的，为了实现快捷开发。</p>
<p>Spring MVC 表单标签库是如何来提高我们的开发效率呢？首先来做一个对比，业务场景：控制层返回业务数据到视图层，视图层需要使用 EL 将业务数据绑定到 JSP 页面表单中。</p>
<p>（1）实体类</p>
<pre><code class="java language-java">public class Student {
    private int id;
    private String name;
    private int age;
    private String gender;
}
</code></pre>
<p>（2）Handler</p>
<pre><code class="java language-java">@Controller
@RequestMapping("/hello")
public class HelloHandler {

    @RequestMapping(value="/get")
    public String get(Model model) {
        Student student = new Student(1,"张三",22,"男");
        model.addAttribute("student", student);
        return "index";
    }

}
</code></pre>
<p>（3）JSP</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;修改学生信息&lt;/h1&gt;
&lt;form action="" method="post"&gt;
     学生编号：&lt;input type="text" name="id" value=${student.id } readonly="readonly"/&gt;&lt;br/&gt;
     学生姓名：&lt;input type="text" name="name" value=${student.name } /&gt;&lt;br/&gt;
     学生年龄：&lt;input type="text" name="age" value=${student.age } /&gt;&lt;br/&gt;
     学生性别：&lt;input type="text" name="gender" value=${student.gender } /&gt;&lt;br/&gt;
     &lt;input type="submit" value="提交"/&gt;&lt;br/&gt;
&lt;/form&gt;
</code></pre>
<p>使用 Spring MVC 表单标签可以直接将业务数据绑定到 JSP 表单中，非常简单。</p>
<p>（1）在 JSP 页面导入 Spring MVC 标签库，与导入 JSTL 标签库的语法非常相似，前缀 prefix 可以自定义，通常定义为 form。</p>
<pre><code>&lt;%@ taglib prefix="form" uri="http://www.springframework.org/tags/form"%&gt;
</code></pre>
<p>（2）将 form 表单与业务数据进行绑定，通过 modelAttribute 属性完成绑定，将 modelAttribute 的值设置为控制器向 model 对象存值时的 name 即可。</p>
<p><img src="https://images.gitbook.cn/367c9950-9a1b-11e8-992f-9dfb28d2b53f" width = "65%" /></p>
<p><img src="https://images.gitbook.cn/3e7b1b90-9a1b-11e8-992f-9dfb28d2b53f" width = "65%" /></p>
<p>（3）form 表单与业务数据完成绑定之后，接下来就是将业务数据中的值取出绑定到不同的标签中，通过设置标签的 path 属性完成，将 path 属性的值设置为业务数据对应的属性名即可。</p>
<p><img src="https://images.gitbook.cn/47ce5860-9a1b-11e8-bd2f-43e393597943" width = "65%" /></p>
<p>完整代码如下。</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;修改学生信息&lt;/h1&gt;
&lt;form:form modelAttribute="student"&gt;
     学生编号：&lt;form:input path="id" readonly=""/&gt;&lt;br/&gt;
     学生姓名：&lt;form:input path="name" /&gt;&lt;br/&gt;
     学生年龄：&lt;form:input path="age" /&gt;&lt;br/&gt;
     学生性别：&lt;form:input path="gender" /&gt;&lt;br/&gt;
     &lt;input type="submit" value="提交"/&gt;&lt;br/&gt;
&lt;/form:form&gt;
</code></pre>
<p>重新运行程序，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/57d63250-9a1b-11e8-8334-9bfa28241acd" width = "50%" /></p>
<p>完成数据的绑定。</p>
<p>接下来我们详细讲解常用标签的使用方法。</p>
<p>（1）form 标签  </p>
<pre><code class="jsp language-jsp">&lt;form:form modelAttribute="student" method="post"&gt;
</code></pre>
<p>渲染的是 HTML 中的 <code>&lt;form&gt;&lt;/form&gt;</code>，通过 modelAttribute 属性绑定具体的业务数据。</p>
<p>（2）input 标签</p>
<pre><code class="jsp language-jsp">&lt;form:input path="name" /&gt;
</code></pre>
<p>渲染的是 HTML 中的 <code>&lt;input type="text"/&gt;</code>，form 标签绑定的是业务数据，input 标签绑定的就是业务数据中的属性值，通过 path 与业务数据的属性名对应，并支持级联属性。</p>
<p>创建 Address 实体类。</p>
<pre><code class="java language-java">public class Address {
    private int id;
    private String name;
}
</code></pre>
<p>修改 Student 实体类，添加 Address 属性。</p>
<pre><code class="java language-java">public class Student {
    private int id;
    private String name;
    private int age;
    private String gender;
    private Address address;
}
</code></pre>
<p>模型对象添加 Address。</p>
<pre><code class="java language-java">@RequestMapping(value="/get")
public String get(Model model) {
    Student student = new Student(1,"张三",22,"男");
    Address address = new Address(1,"科技路");
    student.setAddress(address);
    model.addAttribute("student", student);
    return "index";
}
</code></pre>
<p>修改 JSP 页面，设置级联。</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;修改学生信息&lt;/h1&gt;
&lt;form:form modelAttribute="student"&gt;
     学生编号：&lt;form:input path="id" readonly=""/&gt;&lt;br/&gt;
     学生姓名：&lt;form:input path="name" /&gt;&lt;br/&gt;
     学生年龄：&lt;form:input path="age" /&gt;&lt;br/&gt;
     学生性别：&lt;form:input path="gender" /&gt;&lt;br/&gt;
     学生住址：&lt;form:input path="address.name" /&gt;&lt;br/&gt;
     &lt;input type="submit" value="提交"/&gt;&lt;br/&gt;
&lt;/form:form&gt;
</code></pre>
<p>（3）password 标签</p>
<pre><code class="jsp language-jsp">&lt;form:password path="password" /&gt;
</code></pre>
<p>渲染的是 HTML 中的 <code>&lt;input type="password"/&gt;</code>，通过 path 与业务数据的属性名对应，password 标签的值不会在页面显示。</p>
<p><img src="https://images.gitbook.cn/901eeb20-9a1b-11e8-8334-9bfa28241acd" width = "50%" /></p>
<p>（4）checkbox 标签：</p>
<pre><code class="jsp language-jsp">&lt;form:checkbox path="hobby" value="读书" /&gt;读书
</code></pre>
<p>渲染的是 HTML 中的 <code>&lt;input type="checkbox"/&gt;</code>，通过 path 与业务数据的属性名对应，可以绑定 boolean、数组和集合。</p>
<p>如果绑定 boolean 类型的变量，该变量值为 true，则表示选择，false 表示不选中。</p>
<pre><code>student.setFlag(true);

checkbox：&lt;form:checkbox path="flag" /&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/a55fbeb0-9a1b-11e8-992f-9dfb28d2b53f" width = "50%" /></p>
<p>如果绑定数组或集合类型，集合中的元素等于 checkbox 的 vlaue 值，则该项选中，否则不选中。</p>
<pre><code>student.setHobby(Arrays.asList("读书","看电影","旅行"));

&lt;form:checkbox path="hobby" value="读书" /&gt;读书
&lt;form:checkbox path="hobby" value="看电影" /&gt;看电影
&lt;form:checkbox path="hobby" value="打游戏" /&gt;打游戏
&lt;form:checkbox path="hobby" value="听音乐" /&gt;听音乐
&lt;form:checkbox path="hobby" value="旅行" /&gt;旅行&lt;br/&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/b5faff00-9a1b-11e8-8334-9bfa28241acd" width = "50%" /></p>
<p>（5）checkboxs 标签：</p>
<pre><code class="jsp language-jsp">&lt;form:checkboxes items="${student.hobby }" path="selectHobby" /&gt;
</code></pre>
<p>渲染的是 HTML 中的一组 <code>&lt;input type="checkbox"/&gt;</code>，这里需要结合 items 和 path 两个属性来使用，items 绑定被遍历的集合或数组，path 绑定被选中的集合或数组，可以这样理解，items 为全部选型，path 为默认选中的选型。</p>
<pre><code>student.setHobby(Arrays.asList("读书","看电影","打游戏","听音乐","旅行"));
student.setSelectHobby(Arrays.asList("读书","看电影"));

&lt;form:checkboxes items="${student.hobby }" path="selectHobby" /&gt;
</code></pre>
<p>需要注意的是 path 可以直接绑定业务数据的属性，items 则需要通过 EL 的方式从域对象中取值，不能直接写属性名。</p>
<p><img src="https://images.gitbook.cn/cb1dc340-9a1b-11e8-9724-fb3ff7de9e38" width = "50%" /></p>
<p>（6）radiobutton 标签</p>
<pre><code class="jsp language-jsp">&lt;form:radiobutton path="radioId" value="0" /&gt;
</code></pre>
<p>渲染的是 HTML 中的一个 <code>&lt;input type="radio"/&gt;</code>，绑定的数据与标签的 value 值相等为选中状态，否则为不选中状态。</p>
<pre><code>student.setRadioId(1);

&lt;form:radiobutton path="radioId" value="0" /&gt;男
&lt;form:radiobutton path="radioId" value="1" /&gt;女
</code></pre>
<p><img src="https://images.gitbook.cn/e76153f0-9a1b-11e8-9724-fb3ff7de9e38" width = "60%" /></p>
<p>（7）radiobuttons 标签</p>
<pre><code class="jsp language-jsp">&lt;form:radiobuttons items="${student.grade }" path="selectGrade" /&gt;
</code></pre>
<p>渲染的是 HTML 中的一组 <code>&lt;input type="radio"/&gt;</code>，这里需要结合 items 和 path 两个属性来使用，items 绑定被遍历的集合或数组，path 绑定被选中的值，可以这样理解，items 为全部选型，path 为默认选中的选型，用法与 <code>&lt;form:checkboxs /&gt;</code> 一致。</p>
<pre><code>Map&lt;Integer,String&gt; gradeMap=new HashMap&lt;Integer,String&gt;();
gradeMap.put(1, "一年级");
gradeMap.put(2, "二年级");
gradeMap.put(3, "三年级");
gradeMap.put(4, "四年级");
gradeMap.put(5, "五年级");
gradeMap.put(6, "六年级");
student.setGrade(gradeMap);
student.setSelectGrade(3);

&lt;form:radiobuttons items="${student.grade }" path="selectGrade" /&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/fa9e8f50-9a1b-11e8-8334-9bfa28241acd" width = "60%" /></p>
<p>（8）select 标签</p>
<pre><code class="jsp language-jsp">&lt;form:select items="${student.citys }" path="selectCity" /&gt;
</code></pre>
<p>渲染的是 HTML 中的一个 <code>&lt;select/&gt;</code>，这里需要结合 items 和 path 两个属性来使用，items 绑定被遍历的集合或数组，path 绑定被选中的值，用法与 <code>&lt;form:radiobuttons/&gt;</code> 一致。</p>
<pre><code>Map&lt;Integer,String&gt; cityMap=new HashMap&lt;Integer,String&gt;();
cityMap.put(1, "北京");
cityMap.put(2, "上海");
cityMap.put(3, "广州");
cityMap.put(4, "深圳");
cityMap.put(5, "西安");
cityMap.put(6, "武汉");
student.setCitys(cityMap);
student.setSelectCity(5);

&lt;form:select items="${student.citys }" path="selectCity" /&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/13683b80-9a1c-11e8-9724-fb3ff7de9e38" width = "60%" /></p>
<p>（9）form:select 结合 form:options 的使用，form:select 只定义 path 属性，在 form:select 标签内部添加一个子标签 form:options，设置 items 属性，获取被遍历的集合。</p>
<pre><code class="jsp language-jsp">&lt;form:select path="selectCity"&gt;
    &lt;form:options items="${student.citys }"&gt;&lt;/form:options&gt;
&lt;/form:select&gt;
</code></pre>
<p>（10）form:select 结合 form:option 的使用，form:select 定义 path 属性，给每一个 form:option 设置 values 属性，path 与哪个 value 相等，该项默认选中。</p>
<pre><code class="jsp language-jsp">&lt;form:select path="selectCity"&gt;
    &lt;form:option value="5"&gt;杭州&lt;/form:option&gt;
    &lt;form:option value="6"&gt;成都&lt;/form:option&gt;
    &lt;form:option value="7"&gt;南京&lt;/form:option&gt;
&lt;/form:select&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/29c26e50-9a1c-11e8-992f-9dfb28d2b53f" width = "60%" /></p>
<p>（11）textarea 标签</p>
<p>渲染的是 HTML 中的一个 <code>&lt;textarea/&gt;</code>，path 绑定业务数据的属性值，作为文本输入域的默认值。</p>
<pre><code>student.setIntroduce("你好，我叫...");

&lt;form:textarea path="introduce"/&gt;
</code></pre>
<p><img src="https://images.gitbook.cn/3af9c790-9a1c-11e8-992f-9dfb28d2b53f" width = "60%" /></p>
<p>（12）hidden 标签</p>
<p>渲染的是 HTML 中的一个 <code>&lt;input type="hidden"/&gt;</code>，path 绑定业务数据的属性值。</p>
<p>（13）errors 标签</p>
<p>该标签需要结合 Spring MVC 的 Validator 验证器来使用，将验证结果的 error 信息渲染到 JSP 页面中。</p>
<p>创建验证器，实现 Validator 接口。</p>
<pre><code class="java language-java">public class StudentValidator implements Validator{

    public boolean supports(Class&lt;?&gt; clazz) {
        // TODO Auto-generated method stub
        return Student.class.equals(clazz);
    }

    public void validate(Object target, Errors errors) {
        // TODO Auto-generated method stub
        ValidationUtils.rejectIfEmpty(errors, "name", null, "姓名不能为空"); 
        ValidationUtils.rejectIfEmpty(errors, "password", null, "密码不能为空");
    }

}
</code></pre>
<p>springmvc.xml 中添加 Validator 配置。</p>
<pre><code class="xml language-xml">&lt;mvc:annotation-driven validator="studentValidator"/&gt;

&lt;bean id="studentValidator" class="com.southwind.validator.StudentValidator"/&gt;
</code></pre>
<p>创建业务方法，第一个 login 方法用来生成业务数据，跳转到 login.jsp，第二个 login 方法用来做验证判断。</p>
<pre><code class="java language-java">@GetMapping(value = "/login")
public String login(Model model){
     model.addAttribute(new Student());
     return "login";
}

@PostMapping(value="/login")
public String register(@Validated Student student,BindingResult br) {
    if (br.hasErrors()) {
        return "login";
    }
    return "success";
}
</code></pre>
<p>login.jsp</p>
<pre><code class="jsp language-jsp">&lt;h1&gt;修改学生信息&lt;/h1&gt;
&lt;form:form modelAttribute="student" action="login" method="post"&gt;
    学生姓名：&lt;form:input path="name" /&gt;&lt;form:errors path="name"/&gt;&lt;br/&gt;
    学生密码：&lt;form:password path="password" /&gt;&lt;form:errors path="password"/&gt;&lt;br/&gt;
    &lt;input type="submit" value="提交"/&gt;
&lt;/form:form&gt;
</code></pre>
<p>运行，结果如下图所示，不输入学生姓名和学生密码，直接点击提交按钮。</p>
<p><img src="https://images.gitbook.cn/5c4ca9d0-9a1c-11e8-8334-9bfa28241acd" width = "50%" /></p>
<p>直接将错误信息绑定到 JSP 页面，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/609e29a0-9a1c-11e8-992f-9dfb28d2b53f" width = "50%" /></p>
<h3 id="-1">总结</h3>
<p>本节课我们讲解了 Spring MVC 表单标签库的使用，Spring MVC 表单标签库相较于 JSP 标准标签库 JSTL 更加方便快捷，简化了很多操作，同时可以自动完成数据的绑定，将业务数据绑定到视图层的对应模块进行展示。</p>
<h3 id="-2">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc_taglib.git">请单击这里下载源码</a></p></div></article>