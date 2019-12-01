---
title: SSM 博客系统开发实战-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前期准备</h3>
<p>首先在 webapp 目录下引入 JSP 和 CSS、JS、images 等资源文件，资源文件已放入文末的百度网盘链接中。</p>
<ol>
<li><p>register.jsp 和资源文件直接放在项目目录下，即 webapp 目录下。</p></li>
<li><p>activeFail.jsp、activeSuccess.jsp 和 registerSuccess.jsp 放在 WEB-INF 下的 regist 文件夹下（WEB-INF 下文件安全，不可直接访问）。</p></li>
</ol>
<p>然后打开 register.jsp，在顶部引入 jstl 标签库，以方便我们对后台获取的数据进行条件判断、遍历等操作。</p>
<pre><code>    &lt;%@ page contentType="text/html;charset=UTF-8"%&gt; &lt;%--设置文档类型  防止页面中文乱码--%&gt;
    &lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;         &lt;%--引入jstl核心标签库--%&gt;
    &lt;%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %&gt;   &lt;%--引入jstl函数标签库--%&gt;
    &lt;c:set var="ctx" value="${pageContext.request.contextPath }"/&gt;           &lt;%--用于设置变量值和对象属性--%&gt;
</code></pre>
<p>在 head 标签内引入 CSS 和 JS 文件：</p>
<pre><code>    &lt;link type="text/css" rel="stylesheet" href="${ctx}/css/dreamland.css"&gt;
    &lt;script type="text/javascript" src="${ctx}/js/jquery.min.js"&gt;&lt;/script&gt;
</code></pre>
<p>在 index.jsp 页面 H2 标签内下加入 a 标签（记得引入 page 标签，设置编码格式，否则会中文乱码）：</p>
<pre><code>    &lt;a href="register.jsp"&gt;点我注册&lt;/a&gt;
</code></pre>
<p>然后运行项目点击链接“点我注册”查看效果：</p>
<p><img src="http://images.gitbook.cn/f337f2b0-6807-11e8-8d09-2b69210772e4" alt="" /></p>
<p>样式没问题，接下来制作验证码。</p>
<h4 id="-1">验证码</h4>
<p>1.在 id 为 nickName_span 的 span 标签下加入 input 输入框和验证码图片（src 属性引入图片）：</p>
<pre><code>    &lt;span id="nickName_span" style="color: red"&gt;&lt;/span&gt;
</code></pre>
<pre><code>     &lt;input id="code" name="code" type="text" class="kuang_txt yanzm" placeholder="验证码" onblur="checkCode()"&gt;
     &lt;div&gt;
        &lt;img id="captchaImg" style="CURSOR: pointer" onclick="changeCaptcha()"
           title="看不清楚?请点击刷新验证码!" align='absmiddle' src="${ctx}/captchaServlet"
                           height="18" width="55"&gt;
                      &lt;a href="javascript:;"
                         onClick="changeCaptcha()" style="color: #666;"&gt;看不清楚&lt;/a&gt; &lt;span id="code_span" style="color: red"&gt;&lt;/span&gt;
      &lt;/div&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）其中 onclick 点击事件 changeCaptcha，点击之后更换验证码，具体方法如下：</p>
<pre><code>     //更换验证码
    function changeCaptcha() {
        $("#captchaImg").attr('src', '${ctx}/captchaServlet?t=' + (new Date().getTime()));
    }
</code></pre>
<p>根据 id(captchaImg) 获取 image 标签对象，将它的 src 属性值替换成新的验证码图片。</p>
<p>（2）src 属性值对应的是一个 Servlet，Servlet 对应的URL是 <code>/captchaServlet</code>，当页面加载的时候它会调用该 Servlet 的方法，返回一个验证码图片。</p>
<p>2.在 web.xml 文件中配置 captchaServlet。</p>
<pre><code>    &lt;!--验证码--&gt;
      &lt;servlet&gt;
    &lt;servlet-name&gt;CaptchaServlet&lt;/servlet-name&gt;
    &lt;servlet-class&gt;
      wang.dreamland.www.common.CodeCaptchaServlet
    &lt;/servlet-class&gt;
      &lt;/servlet&gt;
      &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;CaptchaServlet&lt;/servlet-name&gt;
    &lt;url-pattern&gt;/captchaServlet&lt;/url-pattern&gt;
      &lt;/servlet-mapping&gt;    
</code></pre>
<p>我们看下调用 captchaServlet 的过程：</p>
<p>（1）根据 URL <code>/captchaServlet</code> 找到名为 CaptchaServlet 的 Servlet。</p>
<p>（2）然后根据名字 CaptchaServlet 找到具体的 Servlet 位置，就可以调用其中的方法返回验证码图片。</p>
<p>3.在 common 包下引入 CodeCaptchaServlet.java，制作验证码的类，主要是通过 Graphics 设置图片大小，然后随机生成干扰点和4位随机验证码，并保存到 Session 中，用于注册时验证。生成验证码的 CodeCaptchaServlet.java 文件我已放在了文末的百度网盘链接中，可以当作工具类来直接使用。</p>
<p>4.重新启动 Tomcat，点击 index.jsp 内的链接“点我注册”查看效果：</p>
<p><img src="http://images.gitbook.cn/5fae6860-6809-11e8-b87e-87b76270ed83" alt="" /><br />
验证码制作完成！    </p>
<h3 id="-2">注册</h3>
<h4 id="-3">页面表单校验</h4>
<p><img src="http://images.gitbook.cn/727429d0-6809-11e8-9a37-f5d3ad5c8a4a" alt="" /></p>
<p>这里主要说下手机号的校验、验证码的校验、勾选用户协议的校验和表单提交，其他校验方法参考源码中的方法。</p>
<h5 id="1"><strong>1.手机号的校验：</strong></h5>
<pre><code>      &lt;input id="phone" name="phone" type="text" class="kuang_txt phone" placeholder="手机号" onblur="checkPhone();"&gt;&lt;span id="phone_ok"&gt;&lt;/span&gt;
       &lt;br/&gt;
       &lt;span id="phone_span" style="color: red"&gt;&lt;/span&gt;
</code></pre>
<p>其中 br 标签代表换行，给手机号的 input 框添加一个离焦事件 <code>onblur="checkPhone();"</code>， 具体方法如下：</p>
<pre><code>    //校验手机号
    var v = 0;
    var flag2 = false;
    function checkPhone(){
        var phone = $("#phone").val();
        phone = phone.replace(/^\s+|\s+$/g,"");
        if(phone == ""){
            $("#phone_span").text("请输入手机号码！");
            $("#phone_ok").text("");
            var hgt = $("#regist-left").height();

            if(v==0){
                $("#regist-left").height(hgt+30);
                $("#regist-right").height(hgt+30);
                v++;
            }

            flag2 =  false;
        }
        if(!(/^1[3|4|5|8|7][0-9]\d{8}$/.test(phone))){
            $("#phone_span").text("手机号码非法，请重新输入！");
            $("#phone_ok").text("");
            var hgt = $("#regist-left").height();
            if(v==0){
                $("#regist-left").height(hgt+30);
                $("#regist-right").height(hgt+30);
                v++;
            }
            flag2 = false;
        }else{
            $.ajax({
                type:'post',
                url:'/checkPhone',
                data: {"phone":phone},
                dataType:'json',
                success:function(data){
                    var val = data['message'];
                    if(val=="success"){
                        $("#phone_span").text("");
                        $("#reg_span").text("");
                        $("#phone_ok").text("√").css("color","green");

                        var content = $("#phone_ok").text();
                        if(content=="√" ){
                            var hgt = $("#regist-left").height();
                            if(v==1){
                                $("#regist-left").height(hgt-30);
                                $("#regist-right").height(hgt-30);
                            }
                            v=0;
                        }
                        flag2 =  true;

                    }else{

                        $("#phone_span").text("该手机号已经注册！");
                        $("#phone_ok").text("");
                        var hgt = $("#regist-left").height();
                        if(v==0){
                            $("#regist-left").height(hgt+30);
                            $("#regist-right").height(hgt+30);
                            v++;
                        }
                        flag2 =  false;
                    }
                }
            });

        }

        return flag2;
    }


     //根据内容增加而增加高度
    function increaseHeight() {

           var hgt = $("#regist-left").height();
            $("#regist-left").height(hgt+30);
            $("#regist-right").height(hgt+30);

    }
    //根据内容减少而减少高度
    function reduceHeight() {
        var hgt = $("#regist-left").height();
        $("#regist-left").height(hgt-30);
        $("#regist-right").height(hgt-30);
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 var 定义两个变量，一个变量 v 赋初始值为0，方法中可以根据 v 的值控制外部 div 的高度。另一个变量 flag2 赋初始值 false，代表手机号 input 框的状态，false 情况下不能提交表单。</p>
<p>（2）jQuery 获取对象的方式为：<code>$("#phone")</code>，根据 <code>$+("#id")</code> 的方式获取该 id 的标签对象，记得通过 id 获取对象要加 <code>#</code>，通过 class 获取标签对象要加 <code>.</code>，还有其他获取对象的方法，不会的同学可搜索 CSS 标签选择器进行学习。</p>
<p>（3）获取 input 框对象之后，可通过对象 <code>.val()</code> 方法获取该对象的值，即鼠标离焦后该 input 框内的值，赋值给变量 phone。</p>
<p>（4）接下来通过 replace 方法去掉前后空格，该方法的第一个参数是一个正则表达式，表示以空格开头或者以空格结尾。</p>
<p>（5）判断该手机号是否为空，如果为空则在 <code>id=phone_span</code> 的 span 标签中进行提示，span 标签中有内容后，整个 div 会向下扩张，所以要动态增加外部 div 的高度，通过 <code>id=regist-left</code> 获取左边 div 的高度，右边的 div 和左边一样，如果变量 v=0，则将左边和右边的 div 高度都加30，v 自增1。</p>
<p>（6）对手机号进行正则匹配，判断手机号是否正确合法，如果不正确给予错误提示，动态增加外部 div 高度，原理同上。</p>
<p>（7）手机号码判断正确以后，发送 AJAX 请求到后台，请求方式为 post ，请求 URL 为 <code>/checkPhone</code>，映射后台的某个 Controller 的方法，请求参数 data 是手机号，数据类型是 JSON 格式，success 回调函数返回后台处理结果，放在 data 中，通过 <code>data['message']</code> 取出放在 data 中的数据，如果是“success”，说明该手机号未被注册，则在 input 后的 span 标签中打“√”，并且如果 v=1，则将外部 div 减去30，动态缩短 div 高度，将变量 v 重置为0，并将 flag2 赋值为 true，表示手机号的 input 框状态已正确。</p>
<p>（8）如果返回结果不是“success”，说明该手机号已被注册，则给予提示，然后将外部 div 高度动态增加30，v自增 1，将 flag2 赋值为 false，表示 input 框状态错误，不能提交表单。</p>
<p>（9）最后将 flag2 返回。</p>
<p>（10）后面两个方法是将动态增加和缩短 div 的高度封装成了方法，直接调用方法即可。</p>
<p>其中 <code>$("#reg_span").text("")</code> 用来对点击注册时出现的错误进行错误提示，默认情况下都为空。</p>
<h5 id="ajax"><strong>手机号校验 AJAX 请求对应的后台代码：</strong></h5>
<p>在 wang.dreamland.www.controller 包下新建 RegisterController.java，将关于注册的方法都放在此 Controller 下：</p>
<pre><code>    @Controller
    public class RegisterController {
    private final static Logger log = Logger.getLogger(RegisterController.class);
    @Autowired
    private UserService userService;
    @RequestMapping("/checkPhone")
    @ResponseBody
    public Map&lt;String, Object&gt; checkPhone(Model model, @RequestParam(value = "phone", required = false) String phone) {
        log.debug("注册-判断手机号" + phone + "是否可用");
        Map map = new HashMap&lt;String, Object&gt;();
        User user = userService.findByPhone(phone);
        if (user == null) {
            //未注册
            map.put("message", "success");
        } else {
            //已注册
            map.put("message", "fail");
        }

        return map;
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）在类上加上 <code>@Controller</code> 注解代表这是 Controller 层。</p>
<p>（2）通过 Logger.getLogger 方法获取日志对象 Logger，参数就是要打印的类的字节码文件。</p>
<p>（3）通过 <code>@Autowired</code> 注解注入 UserService 对象，可调用其中的方法。</p>
<p>（4）<code>@RequestMapping</code> 注解映射前端访问的 URL 路径，这里对应的就是 AJAX 请求的 URL。</p>
<p>（5）<code>@ResponseBody</code> 注解作用是返回 JSON 格式的数据。</p>
<p>（6）<code>@RequestParam</code> 注解接收前台传来的参数，value 对应参数的名字，<code>required=false</code> 代表该参数是非必须的，可以没有，后面的 String phone 用来接收参数的值，类型为 String 类型。</p>
<p>（7）打印 Log 日志。</p>
<p>（8）new 一个 HashMap 集合，将数据以 key-value 的形式存入 map 中。</p>
<p>（9）根据手机号码查询用户，如果用户为 null 则代表未注册，则以“message”为键，“success”为值存入 map 集合。</p>
<p>（10）如果用户不为 null，则代表该手机号已被注册，则把“fail”作为值存入 map 集合，最后将 map 集合返回。</p>
<h5 id="2"><strong>2.验证码的校验</strong></h5>
<pre><code>     &lt;input id="code" name="code" type="text" class="kuang_txt yanzm" placeholder="验证码" onblur="checkCode()"&gt;
</code></pre>
<p>验证码 input 框的离焦事件 checkCode 方法如下：</p>
<pre><code>    //验证码校验
    var flag_c = false;
    function checkCode() {
        var code = $("#code").val();
        code = code.replace(/^\s+|\s+$/g,"");
        if(code == ""){
            $("#code_span").text("请输入验证码！").css("color","red");
            flag_c = false;
        }else{
            $.ajax({
                type: 'post',
                url: '/checkCode',
                data: {"code": code},
                dataType: 'json',
                success: function (data) {
                    var val = data['message'];
                    if (val == "success") {
                        $("#code_span").text("√").css("color","green");
                        $("#reg_span").text("");
                        flag_c = true;
                    }else {
                        $("#code_span").text("验证码错误！").css("color","red");
                        flag_c = false;
                    }
                }
            });

        }
        return flag_c;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）定义一个变量 <code>flag_c = false</code>，默认状态为错误状态，不可提交表单。</p>
<p>（2）根据标签 id 获取标签对象，通过对象的 val() 方法取得该标签对象的值，即用户输入的验证码。</p>
<p>（3）将验证码去空格后，判断该验证码是否为空，为空则给予错误提示，因为错误提示是加在验证码右侧，所以不用增加 div 高度。</p>
<p>（4）如果验证码不为空，则发送 AJAX 请求给后台，后台将处理后的结果放在 data 中，通过 <code>data["message"]</code> 获取放入 data 中的数据，如果是“success”，则代表验证码正确，打个“√”，<code>flag_c</code> 赋值为 true，代表该 input 框状态正确。</p>
<p>（5）如果 AJAX 返回的结果不是“success”，则说明输入的验证码错误，则给出错误提示，<code>flag_c</code> 赋值为 flase，代表状态错误。</p>
<p>（6）最后将 <code>flag_c</code> 返回。</p>
<h5 id="ajax-1"><strong>验证码校验 AJAX 请求对应的后台代码：</strong></h5>
<p>在 RegisterController.java 中添加如下方法：</p>
<pre><code>    @RequestMapping("/checkCode")
    @ResponseBody
    public Map&lt;String, Object&gt; checkCode(Model model, @RequestParam(value = "code", required = false) String code) {
        log.debug("注册-判断验证码" + code + "是否可用");
        Map map = new HashMap&lt;String, Object&gt;();
        ServletRequestAttributes attrs = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        String vcode = (String) attrs.getRequest().getSession().getAttribute(CodeCaptchaServlet.VERCODE_KEY);

         if (code.equals(vcode)) {
            //验证码正确
            map.put("message", "success");
        } else {
            //验证码错误
            map.put("message", "fail");
        }

        return map;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 ServletRequestAttributes 获取 Request 对象，然后通过 Request 获取 Session 对象。</p>
<p>（2）通过 session.getAttribute 方法获取之前生成验证码时存入 session 中的验证码，赋值给 vcode。</p>
<p>（3）判断前台传来的验证码和 Session 中存入的验证码是否相同。如果相同则代表验证码输入正确，将“success”返回给前台，否则代表验证码输入错误，将“fail”返回给前台。</p>
<h5 id="-4"><strong>勾选用户协议的校验：</strong></h5>
<pre><code>    &lt;input id="protocol" type="checkbox" onclick="checkProtocol();"&gt;&lt;span&gt;已阅读并同意&lt;a href="#" target="_blank" &gt;&lt;span class="lan"&gt;《梦境网用户协议》&lt;/span&gt;&lt;/a&gt;&lt;/span&gt;
</code></pre>
<p>选择框 checkbox 的点击事件 checkProtocol 方法如下：</p>
<pre><code>    //勾选用户协议校验
    function checkProtocol() {
        if($('#protocol').prop("checked"))
        {
            $("#reg_span").text("");
            return true;
        }
        else{
            return false;
        }

    }
</code></pre>
<p>如上面的代码，通过 id 获取 input 框对象，通过该对象的 prop 方法返回 checked 属性的值，如果为 true 则将 <code>id=reg_span</code> 的 span 标签的错误内容清空，返回 true，否则返回 false。</p>
<h5 id="-5"><strong>表单提交</strong></h5>
<p>所有的 input 框被 form 标签包裹着，成功提交表单后，后台通过 input 框的 name 属性获取 value 中的值。</p>
<pre><code>     &lt;form action="${ctx}/doRegister" method="post" id="registerForm"&gt;
</code></pre>
<p>action 对应后台 Controller 中的映射 URL，method 请求方式是 post 请求，form 表单的 id 是 registerForm。</p>
<p>通过点击注册按钮提交表单：</p>
<pre><code>     &lt;input name="注册" type="button" class="btn_zhuce" id ="to_register" value="注册"&gt;
</code></pre>
<p>注册按钮的点击事件如下：</p>
<pre><code>     //提交注册信息
    $("#to_register").click (function(){
        if(!checkProtocol()){
            $("#protocol_span").text("请勾选\"阅读并接受梦境网用户协议\"！").css("color","red");
        }else{
            $("#protocol_span").text("");
        }

        if(checkPhone()  &amp;&amp;  checkPassword()&amp;&amp; checkEmail() &amp;&amp; checkNickName()&amp;&amp; checkCode() &amp;&amp; checkProtocol()){
            $("#registerForm").submit();
        }else {
            $("#reg_span").text("请将信息填写完整！").css("color","red");
        }

    });
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 id 获取对象，<code>对象.click(function(){});</code> 即该对象的点击事件函数。</p>
<p>（2）判断是否勾选用户协议，没有的话给予错误提示，勾选则将 span 标签内容清空。</p>
<p>（3）判断手机号、密码、邮箱、昵称、验证码、勾选用户协议都正确后，则通过 form 表单对象的 submit() 方法提交表单，否则有一个错误，则提示错误信息。</p>
<h4 id="-6">注册后端流程</h4>
<p>流程如下图所示：</p>
<p><img src="http://images.gitbook.cn/9aa94180-680c-11e8-af77-43c8fbf31a49" alt="" /></p>
<ul>
<li><p>1. 用户点击注册提交。根据 URL 映射到具体的 Controller 的具体方法。</p></li>
<li><p>2. 后台再次判断验证码是否正确，错误则返回注册页面，提示错误。</p></li>
<li><p>3. 验证码正确后：</p>
<ul>
<li>3.1 将 MD5 随机生成的激活码保存到 Redis 中，key 为 email，value 为激活码，并且设置保存时间为24小时；</li>
<li>3.2 将用户的信息封装到 user 对象以后保存到 MySQL 数据库中；</li>
<li>3.3 然后给注册用户发送激活邮件，并跳转到注册成功页面。</li></ul></li>
<li>4. 用户激活：

<ul>
<li>4.1 在24小时内激活，跳转到激活成功页面；</li>
<li>4.2 在24小时内激活，激活码错误跳转到激活失败页面（比如网页链接上自行修改激活码测试）；</li>
<li>4.3 超过24小时，Redis 删除用户激活码信息。</li>
<li>4.4 超过24小时激活，激活失败，MySQL 删除用户未激活注册信息。</li></ul>

</li>
</ul>
<p>根据流程可知需要用到 Redis 和发送邮件功能，这里先简单介绍下 Redis 及如何开通邮箱的 POP3/SMTP 服务。</p>
<h5 id="redis"><strong>Redis 简介</strong></h5>
<p>Redis 是一个高性能的 key-value 型数据库。Redis 支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。</p>
<p>Redis 不仅仅支持简单的 key-value 类型的数据，同时还提供 List、Set、Zset、Hash等数据结构的存储。    </p>
<p>Redis 支持数据的备份，即 master-slave 模式的数据备份。</p>
<p>我已将 Redis 压缩包放在了文末的百度网盘链接中，也可自己下载。</p>
<p>Redis 压缩包解压后，进入目录，点击 redis-server.exe，启动 Redis，然后在同目录下启动 redis-cli.exe 从而启动 Redis 客户端，命令如下：</p>
<p>输入：</p>
<pre><code>    set name wly
</code></pre>
<p>通过：</p>
<pre><code>    get name
</code></pre>
<p>即可获得存入 name 中的值，如图：</p>
<p><img src="http://images.gitbook.cn/83f8bbe0-680d-11e8-b87e-87b76270ed83" alt="" /></p>
<p>Java 中是通过 Redis 模板操作 Redis 的，pom.xml 中已经导入了依赖包。这里主要将 Spring 和 Redis 的整合配置文件 <code>applicationContext-redis.xml</code> 和 Redis 的配置文件 <code>redis.properties</code> 进行配置。</p>
<p>1.applicationContext-redis.xml 配置如下：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd"&gt;

    &lt;bean id="poolConfig" class="redis.clients.jedis.JedisPoolConfig"&gt;
        &lt;property name="maxIdle" value="300" /&gt;
        &lt;property name="maxWaitMillis" value="3000" /&gt;
        &lt;property name="testOnBorrow" value="true" /&gt;
    &lt;/bean&gt;
    &lt;!-- 从外部配置文件获取redis相关信息 --&gt;
    &lt;bean id="redisConnectionFactory" class="org.springframework.data.redis.connection.jedis.JedisConnectionFactory"&gt;
        &lt;property name="hostName" value="${redis.ip}" /&gt;
        &lt;property name="port" value="${redis.port}" /&gt;
        &lt;property name="database" value="${redis.database}" /&gt;
        &lt;property name="poolConfig" ref="poolConfig"/&gt;
    &lt;/bean&gt;
    &lt;!-- redis模板配置 --&gt;
    &lt;bean id="redisTemplate" class="org.springframework.data.redis.core.RedisTemplate"&gt;
        &lt;property name="connectionFactory" ref="redisConnectionFactory"&gt;&lt;/property&gt;
        &lt;!-- 对于中文的存储 需要进行序列化操作存储  --&gt;
        &lt;property name="keySerializer"&gt;
            &lt;bean class="org.springframework.data.redis.serializer.StringRedisSerializer" /&gt;
        &lt;/property&gt;
        &lt;property name="valueSerializer"&gt;
            &lt;bean class="org.springframework.data.redis.serializer.StringRedisSerializer"&gt;
            &lt;/bean&gt;
        &lt;/property&gt;
    &lt;/bean&gt;
    &lt;/beans&gt;
</code></pre>
<p>代码解读如下：</p>
<p>（1）连接池的配置。</p>
<p>获取最大空闲连接数：    </p>
<pre><code>    &lt;property name="maxIdle" value="300" /&gt;
</code></pre>
<p>获取连接时的最大等待毫秒数：</p>
<pre><code>    &lt;property name="maxWaitMillis" value="3000" /&gt;
</code></pre>
<p>在获取连接的时候检查有效性：</p>
<pre><code>    &lt;property name="testOnBorrow" value="true" /&gt;
</code></pre>
<p>（2）Redis 连接工厂配置。</p>
<p>主机名：</p>
<pre><code>    &lt;property name="hostName" value="${redis.ip}" /&gt;
</code></pre>
<p>端口号：</p>
<pre><code>    &lt;property name="port" value="${redis.port}" /&gt;
</code></pre>
<p>选用的数据库：</p>
<pre><code>    &lt;property name="database" value="${redis.database}" /&gt;
</code></pre>
<p>连接池名称，引用上面配置的连接池：</p>
<pre><code>    &lt;property name="poolConfig" ref="poolConfig"/&gt;
</code></pre>
<p>（3）redisTemplate 模板配置，主要是将 Redis 模板交给 Spring 管理、引入上面配置的 Redis 连接工厂，对中文存储进行序列化操作等。</p>
<p>2.redis.properties 配置如下：</p>
<pre><code>    redis.pool.maxActive=1024
    redis.pool.maxIdle=200
    redis.pool.maxWait=1000
    redis.ip=localhost
    redis.port=6379
    redis.database=2
</code></pre>
<p>redis.properties 就是属性配置文件，<code>applicationContext-redis.xm</code> 中连接池的配置就是从这里取的值，其中 <code>redis.database=2</code> 代表选用第二个数据库。</p>
<p>3.Redis 相关配置文件配置好以后，引入项目中：</p>
<pre><code>web.xml中引入applicationContext-redis.xml：

    &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;
      classpath*:spring-mybatis.xml,
      classpath*:applicationContext-redis.xml
    &lt;/param-value&gt;
     &lt;/context-param&gt;
</code></pre>
<p>spring-mybatis.xml 中引入 redis.properties：</p>
<pre><code>     &lt;bean id="configProperties" class="org.springframework.beans.factory.config.PropertiesFactoryBean"&gt;
        &lt;property name="locations"&gt;
            &lt;list&gt;
                &lt;value&gt;classpath:jdbc.properties&lt;/value&gt;
                &lt;value&gt;classpath:redis.properties&lt;/value&gt;
            &lt;/list&gt;
        &lt;/property&gt;
        &lt;property name="fileEncoding" value="UTF-8"/&gt;
    &lt;/bean&gt;
</code></pre>
<p>classpath 表示只会到你的 class 路径中查找文件。</p>
<p><code>classpath*</code>：不仅在 class 路径，还会在 jar 文件中（class 路径）进行查找。</p>
<p>所以 <code>classpath*</code> 的加载速度要慢，通常情况下使用 classpath，找不到文件的情况时才使用 <code>classpath*</code>。</p>
<h5 id="pop3smtp"><strong>开通邮箱的 POP3/SMTP 服务</strong></h5>
<p>这里以网易163邮箱为例。</p>
<p>登入163邮箱后，点击设置中的 <code>POP3/SMTP/IMAP</code> 开通 <code>POP3/SMTP</code> 服务，然后点击客户端授权密码，获取一个授权密码，之后的发送邮件功能中需要用到，如下图：</p>
<p><img src="http://images.gitbook.cn/a3fa7090-680e-11e8-8d09-2b69210772e4" alt="" /></p>
<p>项目中还会用到 MD5 加密，在 common 包下引入 MD5Util 工具类，该工具类我也放在了百度网盘链接中。</p>
<h4 id="-7">注册后台代码</h4>
<p>在 RegisterController.java 中创建映射 URL 为 <code>/doRegister</code> 的方法：</p>
<pre><code class="         language-        ">    @Autowired// redis数据库操作模板
    private RedisTemplate&lt;String, String&gt; redisTemplate;
    @RequestMapping("/doRegister")
    public String doRegister(Model model, @RequestParam(value = "email", required = false) String email,
                             @RequestParam(value = "password", required = false) String password,
                             @RequestParam(value = "phone", required = false) String phone,
                             @RequestParam(value = "nickName", required = false) String nickname,
                             @RequestParam(value = "code", required = false) String code) {

        log.debug("注册...");
        if (StringUtils.isBlank(code)) {
            model.addAttribute("error", "非法注册，请重新注册！");
            return "../register";
        }

        int b = checkValidateCode(code);
        if (b == -1) {
            model.addAttribute("error", "验证码超时，请重新注册！");
            return "../register";
        } else if (b == 0) {
            model.addAttribute("error", "验证码不正确,请重新输入!");
            return "../register";
        }


        User user = userService.findByEmail(email);
        if (user != null) {
            model.addAttribute("error", "该用户已经被注册！");
            return "../register";
        } else {
            user = new User();
            user.setNickName(nickname);

            user.setPassword(MD5Util.encodeToHex("salt"+password));
            user.setPhone(phone);
            user.setEmail(email);
            user.setState("0");
            user.setEnable("0");
            user.setImgUrl("/images/icon_m.jpg");
            //邮件激活码
            String validateCode = MD5Util.encodeToHex("salt"+email + password);
            redisTemplate.opsForValue().set(email, validateCode, 24, TimeUnit.HOURS);// 24小时 有效激活 redis保存激活码

            userService.regist(user);

            log.info("注册成功");
            SendEmail.sendEmailMessage(email, validateCode);
            String message = email + "," + validateCode;
            model.addAttribute("message", message);
            return "/regist/registerSuccess";

        }
    }
        // 匹对验证码的正确性

    public int checkValidateCode(String code) {
        ServletRequestAttributes attrs = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        Object vercode = attrs.getRequest().getSession().getAttribute("VERCODE_KEY");
        if (null == vercode) {
            return -1;
        }
        if (!code.equalsIgnoreCase(vercode.toString())) {
            return 0;
        }
        return 1;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入 RedisTemplate 模板，用于操作 Redis。</p>
<p>（2）判断验证码是否为空，如果为空，通过 <code>model.addAttribute</code> 方法将错误信息添加到 model 中，前台可通过键“error”获取对应的值，并返回到注册页面。</p>
<p>这里<code>return "../register"</code> 是根据之前 spring-mvc.xml 中配置的规则转发的，如下：</p>
<pre><code>    &lt;!-- 定义跳转的文件的前后缀 ，视图模式配置 --&gt;
    &lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
        &lt;property name="prefix" value="/WEB-INF/" /&gt;
        &lt;property name="suffix" value=".jsp"/&gt;
    &lt;/bean&gt;
</code></pre>
<p>前缀为<code>/WEB-INF/</code>，<code>../</code> 代表退回到上一层，即到了 <code>/webapp/register</code> 下，后缀是<code>.jsp</code>。</p>
<p>那么最终结果就是 return 到了 <code>/webapp/register.jsp</code> 注册页面。</p>
<p>（3）这里封装了匹配验证码正确性的方法 checkValidateCode，如果 Session 中不存在验证码，则返回-1，提示超时错误，如果存在验证码但是和前台传入的验证码不一致则返回0，提示验证码错误，否则返回1，验证码正确，不提示。</p>
<p>（4）根据前台传来的 email 查询用户是否存在，如果存在说明已经注册，否则给予错误提示，返回注册页面。</p>
<p>（5）用户不存在，这里新创建一个 User，将前台传来的信息赋值给 User，通过 MD5 工具类对密码进行加密，其中 salt 用来增加密码的复杂度，将 state 和 enable 赋初始值0，state 用于用户的激活，激活后变为1，enable 属性以后会说，给用户设置一个默认的头像。</p>
<p>（6）通过 MD5 加密工具生成唯一的邮件激活码赋值给 validateCode。</p>
<p>（7）通过 <code>redisTemplate.opsForValue().set</code> 方法将激活码 validateCode 存入 Redis，以 email 为键，validateCode 为值，设置有效时间为24，单位为小时，即激活码时效为一天。</p>
<p>（8）调用 userService 的 regist 方法将用户插入数据库。</p>
<p>（9）调用发送邮件的方法发送邮件，参数是发送邮件的目的地和激活码。</p>
<p>（10）将邮箱和激活码用 <code>,</code> 号拼接后赋值给 message，将 message 添加到 model 中。</p>
<p>（11）返回注册成功页面 registerSuccess.jsp。</p>
<h5 id="-8"><strong>发送邮件类</strong></h5>
<p>在 wang.dreamland.www 路径下新建 mail 包并引入发送邮件的相关类，mail 包我也放在了文末的百度网盘链接中，主要有三个类：</p>
<ol>
<li>MailExample.java 用于测试；</li>
<li>MyAuthenticator.java 用于验证邮箱和授权码的正确性；</li>
<li>SendEmail.java 用于发送邮件的，主要注意将发件人的邮箱改成你的邮箱，还有输入你的授权码。</li>
</ol>
<p><strong>注意：</strong> 启动项目前如果 Redis 没有启动，请先启动 redis-server.exe。</p>
<p>重新启动项目，注册一个账号，注册成功后跳转到注册成功页面，如下图：</p>
<p><img src="http://images.gitbook.cn/ba726f20-680f-11e8-9a37-f5d3ad5c8a4a" alt="" />  </p>
<h3 id="-9">激活流程</h3>
<p><strong>1.点击立即查看邮箱，可根据不同邮箱跳转到不同邮箱主页。</strong></p>
<pre><code>    &lt;div class="register-active"&gt;
           &lt;span style="font-size: 15px;font-weight: bold;padding: 20px;line-height: 100px"&gt;激活邮件已经发送到您的注册邮箱${message.split(",")[0]},点击邮件里的链接即可激活账号。&lt;/span&gt;&lt;br/&gt;
            &lt;button style="margin-left: 20px;" class="btn btn-primary" type="button" onclick="lookEmail('${message}');"&gt;立即查看邮件&lt;/button&gt;
     &lt;/div&gt;
</code></pre>
<p>根据键 message 取出后台存入 model 中的值，然后根据 <code>,</code> 号切割，取第一个元素就是邮箱了。</p>
<p>查看邮箱的点击事件 lookEmail 方法如下：</p>
<pre><code>    function lookEmail(message) {
        var arr = message.split(",");
        var email = arr[0];
        var opt = email.split("@")[1];
        if("qq.com"==opt){
            location.href = "https://mail.qq.com/";
        }else if("163.com"==opt){
                location.href = "https://mail.163.com/";
        }else if("162.com"==opt){
            location.href = "https://mail.162.com/";
        }else if("sina.com"==opt){
            location.href = "http://mail.sina.com.cn/";
        }else if("sohu"==opt){
            location.href = "https://mail.sohu.com";
        }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）参数 message 是邮箱和激活码通过 <code>,</code> 号拼接的字符串，根据 <code>,</code> 号切割取出邮箱。</p>
<p>（2）根据 <code>@</code> 切割取出邮箱 <code>@</code> 后面部分，主要根据 <code>@</code> 后面的信息进行跳转。</p>
<p>（3）如果后面部分是 qq.com 则链接到 QQ 邮箱，其他同理。</p>
<p><strong>2.点击重新发送邮件，可重新发送激活邮件。</strong></p>
<pre><code>    onclick="reSendEmail('${message}')" 
</code></pre>
<p>点击事件 reSendEmail 方法如下：</p>
<pre><code>     function reSendEmail(message) {
       var arr = message.split(",");
       var email = arr[0];
       var code = arr[1];
        $.ajax({
            type:'post',
            url:'/sendEmail',
            data: {"email":email,"validateCode":code},
            dataType:'json',
            success:function(data){
                //alert(data["success"])
                var s = data["success"];
                if(s=="success"){
                    alert("发送成功！");
                }
            }
        });
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>,</code> 号切割分别拿到邮箱和激活码。</p>
<p>（2）发送 AJAX 请求，映射 URL 为 <code>/sendEmail</code>，请求参数 data 是邮箱和激活码。</p>
<p>（3）success 回调函数返回后台处理结果。如果是“success”代表发送成功，给予提示。</p>
<p>后台 RegisterController.java 中映射 URL 为 <code>/sendEmail</code> 的方法如下：</p>
<pre><code>    @RequestMapping("/sendEmail")
    @ResponseBody
    public  Map&lt;String,Object&gt; sendEmail(Model model) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        ServletRequestAttributes attrs = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        String validateCode = attrs.getRequest().getParameter( "validateCode" );
        String email = attrs.getRequest().getParameter( "email" );
        SendEmail.sendEmailMessage(email,validateCode);
        map.put( "success","success" );
        return map;
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）这里我使用的是另一种获取参数的方式，通过 request.getParameter() 方法也可以获取前台传来的参数，参数是要获取的参数名称。</p>
<p>（2）调用发送邮件的方法即可，然后将“success”放入 map 集合，返回给前台。</p>
<p><strong>3.重新注册，跳转到注册页面。</strong></p>
<p>点击事件 reRegist 方法如下：</p>
<pre><code>     function reRegist() {
         location.href = "../register.jsp";
    }
</code></pre>
<p>通过 location.href 属性链接到 register.jsp 页面。</p>
<p>也可以通过后台 Controller 跳转：</p>
<pre><code>    function reRegist() {
         location.href = "${ctx}/register";
    }
</code></pre>
<p>RegisterController.java 写上对应 URL 的方法：</p>
<pre><code>    @RequestMapping("/register")
    public String register(Model model) {

        log.info("进入注册页面");

        return "../register";
    }
</code></pre>
<p><strong>4.进入邮箱进行激活。</strong></p>
<p>（1）登录邮箱打开收到的激活邮件，点击“请于24小时内点击激活”链接：</p>
<p><img src="http://images.gitbook.cn/ab9d5360-6810-11e8-9a37-f5d3ad5c8a4a" alt="" /></p>
<p>点击后获得的链接也就是我们发送邮件方法里面写的链接：</p>
<pre><code>     message.setContent( "&lt;a href=\"http://localhost:8080/activecode?email="+email+"&amp;validateCode="+validateCode+"\" target=\"_blank\"&gt;请于24小时内点击激活&lt;/a&gt;","text/html;charset=gb2312");
</code></pre>
<p>在 RegisterController.java 创建映射 URL 为 <code>/activecode</code> 的方法如下：</p>
<pre><code class="     language-    ">    @Autowired
    private RoleUserService roleUserService;
    @RequestMapping("/activecode")
    public String active(Model model) {
        log.info( "==============激活验证==================" );
        //判断   激活有无过期 是否正确
        //validateCode=
        ServletRequestAttributes attrs = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        String validateCode = attrs.getRequest().getParameter( "validateCode" );
        String email = attrs.getRequest().getParameter( "email" );
        String code = redisTemplate.opsForValue().get( email );
        log.info( "验证邮箱为："+email+",邮箱激活码为："+code+",用户链接的激活码为："+validateCode );
        //判断是否已激活

        User userTrue = userService.findByEmail( email );
        if(userTrue!=null &amp;&amp; "1".equals( userTrue.getState() )){
            //已激活
            model.addAttribute( "success","您已激活,请直接登录！" );
            return "../login";
        }

        if(code==null){
            //激活码过期
            model.addAttribute( "fail","您的激活码已过期,请重新注册！" );
            userService.deleteByEmail( email );
            return "/regist/activeFail";
        }

        if(StringUtils.isNotBlank( validateCode ) &amp;&amp; validateCode.equals( code )){
            //激活码正确
            userTrue.setEnable( "1" );
            userTrue.setState( "1" );
            userService.update( userTrue );
            model.addAttribute( "email",email );
            return "/regist/activeSuccess";
        }else {
            //激活码错误
            model.addAttribute( "fail","您的激活码错误,请重新激活！" );
            return "/regist/activeFail";
        }

    }
</code></pre>
<p>代码解读如下：</p>
<p>A. 这里通过 request.getParameter 方法获取请求参数：邮箱和激活码。</p>
<p>B. 通过键 email 去 Redis 中取出之前存入 Redis 中的激活码，赋值给 code。</p>
<p>C. 根据邮箱查询用户，如果用户不为 null 并且激活状态 <code>state=1</code> 说明该用户已经激活，将“success”添加到 model 中并跳转到登录页面。</p>
<p>D. 如果从 Redis 中取出的激活码为 null，说明激活码已经超过24小时，将“fail”添加到 model 中，然后
根据用户 email 删除用户，返回注册页面。</p>
<p>E. 如果前台传来的激活码不为空并且和 Redis 中取出的激活码相同说明激活码正确，更新用户激活状态 state 和 enable 为1，将 email 添加到 model 中，返回到激活成功页面，否则将“fail”添加到 model 中并返回到激活失败页面。</p>
<p>重新启动项目，注册 -&gt; 注册成功 -&gt; 进入邮箱点击激活链接。</p>
<p>（2）激活成功页面效果如下：</p>
<p><img src="http://images.gitbook.cn/88ea2860-6811-11e8-af77-43c8fbf31a49" alt="" /></p>
<p>（3）激活失败页面效果如下：</p>
<p><img src="http://images.gitbook.cn/9d524f30-6811-11e8-9a37-f5d3ad5c8a4a" alt="" /></p>
<p><strong>注意：</strong></p>
<p>激活成功后，发现数据库中 state 和 enable 字段并未更新，因为 User 实体类的 id 我们没有给它标识为主键，所以没有根据主键来更新字段。</p>
<p>在 id 字段上加上以下注解：</p>
<pre><code>    @Id//标识主键
    @GeneratedValue(strategy = GenerationType.IDENTITY) //自增长策略
</code></pre>
<p>顺便将其他实体类一并加上这两个注解，然后再启动项目，点击激活链接，查看数据库，字段已更新！</p>
<blockquote>
  <p>第05课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1zAUhMWPonrfnEvwW8QdrfA 
  密码：8len</p>
</blockquote></div></article>