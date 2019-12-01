---
title: SSM 博客系统开发实战-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前期准备</h3>
<p>本项目需要使用阿里大于的短信服务发送手机短信，所以我们首先要开通短信服务，记得再充点钱。</p>
<h4 id="-1">开通短信服务</h4>
<p>首先登录阿里云，开通阿里大于短信服务，如下图所示：</p>
<p><img src="http://images.gitbook.cn/b72cb820-6df0-11e8-9ab5-a93e1135abc8" alt="" /></p>
<p><img src="http://images.gitbook.cn/20d954e0-6df1-11e8-9a3a-91a7e0861642" alt="" /></p>
<p>注册成功后系统会自动生成 Access Key ID 和 Access Key Secret，在后面代码中会用到它们，需要记住。</p>
<p>也可以通过接口调用 -&gt; 获取 AK，查看 Access Key ID 和 Access Key Secret。</p>
<p><img src="http://images.gitbook.cn/57710ce0-6df2-11e8-9503-5f61421c20d6" alt="" /></p>
<p>发送短信的格式为：【短信签名名称】+ 短信模板内容（短信签名为自己的真实姓名，申请时较容易通过）。</p>
<p>如下是本项目采用的短信格式：</p>
<blockquote>
  <p>【梦境网】感谢您使用梦境网手机验证功能，您的验证码为：617760，为了您的账号安全，请勿泄露给他人。</p>
</blockquote>
<p>接下来，我们申请短信签名，如下图所示：</p>
<p><img src="http://images.gitbook.cn/cf1ba9d0-6df2-11e8-9503-5f61421c20d6" alt="" /></p>
<p>申请通过之后如下所示：</p>
<p><img src="http://images.gitbook.cn/e463f770-6df2-11e8-9a3a-91a7e0861642" alt="" /></p>
<p>申请短信模板，如下所示：</p>
<p><img src="http://images.gitbook.cn/f759f0a0-6df2-11e8-8a4e-4fcbf446a7ea" alt="" /></p>
<p>在上图中，按如下填写：</p>
<blockquote>
  <p>模板名称：梦境网，</p>
  <p>模板内容为：感谢您使用梦境网手机验证功能，您的验证码为：${code}，为了您的账号安全，请勿泄露给他人。</p>
  <p>申请说明：测试使用</p>
</blockquote>
<p>模板可以申请多个，申请通过后如下图所示：</p>
<p><img src="http://images.gitbook.cn/6c240d70-6df4-11e8-9503-5f61421c20d6" alt="" /></p>
<h4 id="activemq">ActiveMQ 简介</h4>
<p>ActiveMQ 是 Apache 旗下产品，是一款优秀的消息中间件。主要解决应用耦合，异步消息，流量削锋等问题，实现高性能，高可用。</p>
<p>你可以把 ActiveMQ 想象成一个大的容器，首先生产者把消息发送到这个大容器中，然后消费者监听，如果有消息就从这个大容器中消费消息，起到一个缓冲的作用。</p>
<h5 id="-2"><strong>下载并运行</strong></h5>
<p>ActiveMQ 压缩文件我已放在了文末的百度网盘中，也可自己<a href="http://activemq.apache.org/download.html">去官网下载</a>。</p>
<p>下载完成后进行解压，进入 <code>apache-activemq-5.15.3\bin\win64</code> 目录（32 为系统进入 Win32），然后点击运行 activemq.bat。</p>
<p>可以通过 http://localhost:8161/ 访问 ActiveMQ 消息管理后台页面，如下图所示：</p>
<p><img src="http://images.gitbook.cn/4289d8c0-6df7-11e8-9503-5f61421c20d6" alt="" /></p>
<p>点击 Manage ActiveMQ broker 进行登录，用户名和密码均为：admin。</p>
<p>登录后可以查看 Queues 消息队列等信息，如下图：</p>
<p><img src="http://images.gitbook.cn/5fb44700-6df7-11e8-9ab5-a93e1135abc8" alt="" /></p>
<h5 id="activemq-1"><strong>ActiveMQ 相关配置</strong></h5>
<p>ActiveMQ 生产者和消费者配置文件 applicationContext-activemq.xml 配置如下：</p>
<pre><code>    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:amq="http://activemq.apache.org/schema/core"
       xmlns:jms="http://www.springframework.org/schema/jms"
       xsi:schemaLocation="
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/jms
        http://www.springframework.org/schema/jms/spring-jms.xsd
        http://activemq.apache.org/schema/core
        http://activemq.apache.org/schema/core/activemq-core.xsd "&gt;

    &lt;!-- 扫瞄包--&gt;
    &lt;context:component-scan base-package="wang.dreamland.www.activemq" /&gt;
    &lt;!-- ActiveMQ 连接工厂 --&gt;
    &lt;!-- 真正可以产生Connection的ConnectionFactory，由对应的 JMS服务厂商提供--&gt;
    &lt;!-- 如果连接网络：tcp://ip:61616；未连接网络：tcp://localhost:61616 以及用户名，密码--&gt;
    &lt;amq:connectionFactory id="amqConnectionFactory" brokerURL="tcp://localhost:61616" userName="admin" password="admin"  /&gt;

    &lt;!-- Spring Caching连接工厂 --&gt;
    &lt;!-- Spring用于管理真正的ConnectionFactory的ConnectionFactory --&gt;
    &lt;bean id="connectionFactory" class="org.springframework.jms.connection.CachingConnectionFactory"&gt;
        &lt;!-- 目标ConnectionFactory对应真实的可以产生JMS Connection的ConnectionFactory --&gt;
        &lt;property name="targetConnectionFactory" ref="amqConnectionFactory"&gt;&lt;/property&gt;
        &lt;!-- 同上，同理 --&gt;
        &lt;!-- &lt;constructor-arg ref="amqConnectionFactory" /&gt; --&gt;
        &lt;!-- Session缓存数量 --&gt;
        &lt;property name="sessionCacheSize" value="100" /&gt;
    &lt;/bean&gt;

    &lt;!-- Spring JmsTemplate 的消息生产者 start--&gt;
    &lt;!-- 定义JmsTemplate的Queue类型 --&gt;
    &lt;bean id="jmsQueueTemplate" class="org.springframework.jms.core.JmsTemplate"&gt;
        &lt;!-- 这个connectionFactory对应的是我们定义的Spring提供的那个ConnectionFactory对象 --&gt;
        &lt;constructor-arg ref="connectionFactory" /&gt;
        &lt;!-- 非pub/sub模型（发布/订阅），即队列模式 --&gt;
        &lt;property name="pubSubDomain" value="false" /&gt;
    &lt;/bean&gt;

    &lt;!-- Spring JmsTemplate 的消息生产者 end --&gt;

    &lt;!-- 消息消费者 start--&gt;

    &lt;!-- 定义Queue监听器 --&gt;
    &lt;jms:listener-container destination-type="queue" container-type="default" connection-factory="connectionFactory" acknowledge="auto"&gt;
        &lt;!-- 默认注册bean名称，应该是类名首字母小写  --&gt;
        &lt;jms:listener destination="login_msg" ref="smsAuthenCode"/&gt;
    &lt;/jms:listener-container&gt;
    &lt;!-- 消息消费者 end --&gt;
    &lt;/beans&gt;
</code></pre>
<p>主要是 ActiveMQ 的连接配置以及生产者和消费者的配置。上面注释很详细，这里就不做重复介绍了。</p>
<h5 id="webxmlapplicationcontextactivemqxml"><strong>web.xml 引入 applicationContext-activemq.xml</strong></h5>
<p>代码如下：</p>
<pre><code>     &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;
      classpath*:spring-mybatis.xml,
      classpath*:applicationContext-redis.xml,
      classpath*:applicationContext-activemq.xml
    &lt;/param-value&gt;
      &lt;/context-param&gt;
</code></pre>
<p>通过 web.xml 加载刚才配置的 applicationContext-activemq.xml。</p>
<h5 id="activemq-2"><strong>ActiveMQ 消息监听器的创建（消费者）</strong></h5>
<p>配置文件配置完成并引入后，创建消息监听器，监听消息的存在。</p>
<p>在 wang.dreamland.www 包下新建 activemq 包，在 activemq 包下新建消息监听器类 SmsAuthenCode.java：</p>
<pre><code>    @Component
    public class SmsAuthenCode implements MessageListener {
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;
        // 调用SMS服务发送短信   SmsSystem阿里大于发送短信给客户手机实现类

        try {
            // 大于发送短信 Map 来自ActiveMQ 生成者
            SendMessage.sendMessages( mapMessage.getString("code"), mapMessage.getString("telephone") );
            System.out.println( "-----发送消息成功..."+mapMessage.getString("code"));
        } catch (Exception e) {//JMS
            e.printStackTrace();
        }
    }
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）不知道属于哪一层时使用 <code>@Component</code> 注解，将对象交给 Spring 管理；</p>
<p>（2）消息监听类实现消息监听接口 MessageListener 重写 onMessage 方法；</p>
<p>（3）将消息 message 强制转换为 MapMessage；</p>
<p>（4）从 MapMessage 中取出手机验证码和手机号，调用发送短信的方法将短信发送给用户，下文将对这一部分做解释。</p>
<h4 id="sendmessage">阿里大于发送短信类 SendMessage 的创建</h4>
<p>创建过程主要包括以下四步。</p>
<p>1.首先，<a href="https://help.aliyun.com/document_detail/55359.html?spm=a2c4g.11186623.2.8.2bNpLw">下载阿里大于 SDK</a>，选择 Java下载。</p>
<p>2.然后，将 aliyun-java-sdk-core-3.3.1.jar 和 aliyun-java-sdk-dysmsapi-1.0.0.jar 打包到本地 Maven 仓库。</p>
<p>这两个文件分别在解压目录的 <code>java/api_sdk/aliyun-java-sdk-core</code> 和 <code>java/api_sdk/aliyun-java-sdk-dysmsapi</code> 下。</p>
<p>打开 CMD，输入：</p>
<pre><code>    mvn install:install-file -Dfile=D:\安装包\alidayu\java\api_sdk\aliyun-java-sdk-core\aliyun-java-sdk-core-3.3.1.jar -DgroupId=wang.dreamland.www -DartifactId=dayu-sdk-core -Dversion=3.3.1 -Dpackaging=jar -DgeneratePom=true -DcreateChecksum=true
</code></pre>
<p>回车，再输入下面的代码，回车：</p>
<pre><code>    mvn install:install-file -Dfile=D:\安装包\alidayu\java\api_sdk\aliyun-java-sdk-dysmsapi\aliyun-java-sdk-dysmsapi-1.0.0.jar -DgroupId=wang.dreamland.www -DartifactId=dayu-sdk-dysmsapi -Dversion=1.0.0 -Dpackaging=jar -DgeneratePom=true -DcreateChecksum=true
</code></pre>
<p><strong>注意：</strong> <code>-Dfile</code> 是你的 jar 包所在路径。</p>
<p>在本地仓库的包路径下可查看打包好的 jar 包，如下图所示：</p>
<p><img src="http://images.gitbook.cn/5763b7b0-6df8-11e8-9ab5-a93e1135abc8" alt="" /></p>
<p>3.接着，在 pom.xml 中引入刚才打包好的阿里大于依赖：</p>
<pre><code>        &lt;!-- 阿里大于依赖 --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;wang.dreamland.www&lt;/groupId&gt;
            &lt;artifactId&gt;dayu-sdk-core&lt;/artifactId&gt;
            &lt;version&gt;3.3.1&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;wang.dreamland.www&lt;/groupId&gt;
            &lt;artifactId&gt;dayu-sdk-dysmsapi&lt;/artifactId&gt;
            &lt;version&gt;1.0.0&lt;/version&gt;
        &lt;/dependency&gt;
</code></pre>
<p>groupId 对应上面的 <code>-DgroupId</code>，artifactId 对应上面的 <code>-DartifactId</code>，version 对应上面的 <code>-Dversion</code>。</p>
<p>4.最后，在 activemq 包下新建发送短信类 SendMessage.java：</p>
<pre><code>    public class SendMessage {
    private static String accessKeyId = "你的accessKeyId";//你的accessKeyId,参考本文档步骤2
    private static String accessKeySecret = "你的accessKeySecret";//你的accessKeySecret，参考本文档步骤2
    private static String setSignName = "你的短信签名名称";
    private static String dayutemplateCode = "你的短信模板CODE";

    public static void sendMessages(String code,String phone){
        //设置超时时间-可自行调整
        System.setProperty("sun.net.client.defaultConnectTimeout", "10000");
        System.setProperty("sun.net.client.defaultReadTimeout", "10000");
        //初始化ascClient需要的几个参数
        final String product = "Dysmsapi";//短信API产品名称
        final String domain = "dysmsapi.aliyuncs.com";//短信API产品域名
        //替换成你的AK
        //初始化ascClient,暂时不支持多region
        IClientProfile profile = DefaultProfile.getProfile("cn-hangzhou", accessKeyId,
                accessKeySecret);
        try {
            DefaultProfile.addEndpoint("cn-hangzhou", "cn-hangzhou", product, domain);
        } catch (ClientException e) {
            e.printStackTrace();
        }
        IAcsClient acsClient = new DefaultAcsClient(profile);
        //组装请求对象
        SendSmsRequest request = new SendSmsRequest();
        //必填:待发送手机号。支持以逗号分隔的形式进行批量调用，批量上限为20个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
        request.setPhoneNumbers(phone);
        //必填:短信签名-可在短信控制台中找到
        request.setSignName(setSignName);
        //必填:短信模板-可在短信控制台中找到
        request.setTemplateCode(dayutemplateCode);
        //可选:模板中的变量替换JSON串,如模板内容为"亲爱的${name},您的验证码为${code}"时,此处的值为
        //"{\"number\":\"" + code + "\"}"
        request.setTemplateParam("{\"code\":\"" + code + "\"}");
        //可选:outId为提供给业务方扩展字段,最终在短信回执消息中将此值带回给调用者
        request.setOutId("yourOutId");
        //请求失败这里会抛ClientException异常
        SendSmsResponse sendSmsResponse = null;
        try {
            sendSmsResponse = acsClient.getAcsResponse(request);
        } catch (ServerException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (ClientException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        if(sendSmsResponse.getCode() != null &amp;&amp; sendSmsResponse.getCode().equals("OK")) {
            //请求成功
        }
    }
    }
</code></pre>
<p>在 <code>\java\api_demo\alicom-dysms-api\src\main\java\com\alicom\dysms\api</code> 目录下有一个 SmsDemo.java 文件，为发送短信的模板文件，和上面的内容差不多，主要注意上面四个参数改成你自己的，还有模板参数不一样：</p>
<pre><code>request.setTemplateParam("{\"code\":\"" + code + "\"}");
</code></pre>
<h3 id="-3">手机快捷登录流程</h3>
<p>手机快捷登录的流程，主要包括下面几步。</p>
<p>1.手机号 input 框离焦事件判断。</p>
<ul>
<li>判断该手机号是否合法；</li>
<li>如果手机号合法，则判断该手机号是否是已激活用户。</li>
</ul>
<p>2.获取验证码点击事件。</p>
<ul>
<li>判断步骤1是否返回 true；</li>
<li>返回 true 则发送获取验证码并同时设置倒计时 60s；</li>
<li>倒计时60s结束才能点击重新获取。</li>
</ul>
<p>3.验证码 input 框离焦事件。</p>
<ul>
<li>判断验证码是否为6位纯数字（防止恶意登录），是则返回 true。</li>
</ul>
<p>4.登录点击事件</p>
<ul>
<li>判断手机号和验证码均返回 true 时则提交表单。</li>
</ul>
<h4 id="jsp">前端 JSP 页面</h4>
<p>前端页面，如下图所示：</p>
<p><img src="http://images.gitbook.cn/d1d67550-6df8-11e8-8a4e-4fcbf446a7ea" alt="" /></p>
<p><strong>这里主要说下获取验证码点击事件，其他的和之前的原理一样：</strong></p>
<pre><code>    //获取验证码
    $(function () {
        var go = document.getElementById('go');

        go.onclick = function (ev){
            if(!flag2){
                $("#phone_span").text("手机号码非法或者未注册！").css("color","red");
            }else {
                //  发送短信给用户手机..
                // 1 发送一个HTTP请求，通知服务器 发送短信给目标用户
                var telephone =$("input[name='telephone']").val();// 用户输入的手机号
                    // 用户输入手机号校验通过
                    $("#go").attr("disabled", "disabled");
                    countDown(60);

                    $.ajax({
                        method: 'POST',
                        url: '${ctx}/sendSms',
                        data : {
                            telephone : telephone
                        },
                        success:function(data) {
                            var tt = data["msg"];
                            if(tt){
                                 alert("发送短信成功!");

                            }else{
                                alert("发送短信出错，请联系管理员");
                            }
                        }
                    });
                }


            var oEvent = ev || event;
            //js阻止链接默认行为，没有停止冒泡
            oEvent.preventDefault();

        }
    });

    //倒计时
    function countDown(s){
        if(s &lt;= 0){
            $("#go").text("重新获取");
            $("#go").removeAttr("disabled");
            return;
        }
        /* $("#go").val(s + "秒后重新获取");*/
        $("#go").text(s + "秒后重新获取");
        setTimeout("countDown("+(s-1)+")",1000);
    }
</code></pre>
<p>代码解读如下：</p>
<p>（1） <code>$(function () {});</code> 代表页面加载完成函数；</p>
<p>（2）通过 document.getElementById 获取文档对象 DOM，赋值给 go；</p>
<p>（3）给 go 绑定一个 onclick 点击事件函数；</p>
<p>（4）如果检验手机号返回的是 flag2=false，则给予错误提示；</p>
<p>（5）如果检验手机号成功后，通过属性过滤选择器获取 input 框对象，并通过对象的 val() 方法获取手机号；</p>
<p>（6）通过 <code>$("#go").attr("disabled", "disabled")</code> 方法将获取验证码按钮设置成不可点击；</p>
<p>（7）调用 countDown 倒计时方法，如果倒计时到0秒后，按钮显示重新获取，并移除 disabled 属性，按钮可再次点击，如果 <code>0&lt;s&lt;=60</code> 则按钮上显示 s 秒后重新获取，不可点击，每秒 s-1；</p>
<p>（8）发送 AJAX 请求，映射 URL 为 <code>/sendSms</code>，请求参数是手机号；</p>
<p>（9）success 回调函数返回的结果如果是true，则提示发送成功。否则提示发送失败，联系管理员；</p>
<p>（10）oEvent.preventDefault() 阻止链接默认行为。主要是为了返回错误信息时停留在手机快捷登录标签。</p>
<p><strong>后台创建映射 URL 为 <code>/sendSms</code> 的方法，如下：</strong></p>
<pre><code>    @Autowired
    private UserService userService;
    @Autowired// redis数据库操作模板
    private RedisTemplate&lt;String, String&gt; redisTemplate;// jdbcTemplate HibernateTemplate

    @Autowired
    @Qualifier("jmsQueueTemplate")
    private JmsTemplate jmsTemplate;// mq消息模板.

    /**
     * 发送手机验证码
     * @param model
     * @param telephone
     * @return
     */
    @RequestMapping("/sendSms")
    @ResponseBody
    public Map&lt;String,Object&gt; index(Model model, @RequestParam(value = "telephone",required = false) final String telephone ) {
        Map map = new HashMap&lt;String,Object&gt;(  );
        try { //  发送验证码操作
            final String code = RandStringUtils.getCode();
            redisTemplate.opsForValue().set(telephone, code, 60, TimeUnit.SECONDS);// 60秒 有效 redis保存验证码
            log.debug("--------短信验证码为："+code);
            // 调用ActiveMQ jmsTemplate，发送一条消息给MQ
            jmsTemplate.send("login_msg", new MessageCreator() {
                public Message createMessage(javax.jms.Session session) throws JMSException {
                    MapMessage mapMessage = session.createMapMessage();
                    mapMessage.setString("telephone",telephone);
                    mapMessage.setString("code", code);
                    return mapMessage;
                }
            });
        } catch (Exception e) {
            map.put( "msg",false );
        }
        map.put( "msg",true );
        return map;

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）通过 <code>@Autowired</code> 注解注入 UserService、RedisTemplate，通过 <code>@Autowired</code> 和 <code>@Qualifier</code> 结合注入 JmsTemplate，参数是配置文件中配置的队列 ID，主要是为了区分有多个类型的情况，指定注入（这里可以不指定），比如，如果再定义一个订阅模式就需要加 <code>@Qualifier</code> 注解进行指定注入：</p>
<pre><code>&lt;!-- 定义JmsTemplate的Topic类型 --&gt;
      &lt;bean id="jmsTopicTemplate" class="org.springframework.jms.core.JmsTemplate"&gt;
       &lt;!-- 这个connectionFactory对应的是我们定义的Spring提供的那个ConnectionFactory对象 --&gt;
          &lt;constructor-arg ref="connectionFactory" /&gt;
           &lt;!-- pub/sub模型（发布/订阅） --&gt;
           &lt;property name="pubSubDomain" value="true" /&gt;
       &lt;/bean&gt;
</code></pre>
<p>（2）通过 RandStringUtils 工具类随机生成六位数字验证码，该工具类也放在了文末的百度网盘链接中。</p>
<p>（3）将6位随机验证码保存到 Redis 中，时效为60秒，key=手机号，value=验证码。</p>
<p>（4）调用 ActiveMQ 消息模板对象生产一条消息，发送给 MQ。</p>
<p><strong>注意：</strong>第一个参数 <code>login_msg</code> 是配置文件中配置的目的地：</p>
<pre><code>&lt;jms:listener-container destination-type="queue" container-type="default" connection-factory="connectionFactory" acknowledge="auto"&gt;
        &lt;!-- 默认注册bean名称，应该是类名首字母小写  --&gt;
        &lt;jms:listener destination="login_msg" ref="smsAuthenCode"/&gt;
    &lt;/jms:listener-container&gt;
</code></pre>
<p>监听器 smsAuthenCode 监听到消息之后就会调用发送短信功能。</p>
<p>第二个参数是接口 MessageCreator，这里传入的是匿名内部类，通过 new 接口的形式并实现接口方法。</p>
<p>（5）如果有异常则把 false 放入 map，否则把 true 放入 map，最后返回 map。</p>
<h4 id="-4">登录流程</h4>
<p><img src="http://images.gitbook.cn/5b72a8e0-6dfb-11e8-9ab5-a93e1135abc8" alt="" /></p>
<p>如上图所示，登录流程主要包括以下几个步骤：</p>
<ol>
<li>用户点击获取验证码，后台生成6位随机验证码，一份存入 Redis 数据库中，<code>key="手机号"</code>，<code>value="验证码"</code>；</li>
<li>ActiveMQ 生产者发送消息给 ActiveMQ 中间件，等待消费者消费；</li>
<li>ActiveMQ 消费者监听到消息之后发送短信给用户；</li>
<li>输入验证码点击登录；</li>
<li>后台获取用户的手机号以及验证码，根据用户的手机号去 Redis 数据库中取对应的验证码，然后与用户输入的验证码进行比对，一致则登录成功，跳转到 personal.jsp，否则跳转到 login.jsp。</li>
</ol>
<p><strong>用户输入手机验证码后点击登录，对应的点击事件如下：</strong></p>
<pre><code>     //登录
    $("#phone_btn").click(function () {

        if(checkPhone()&amp;&amp; checkPhoneCode()){
            // 校验用户名和密码
            $("#phone_span").text("").css("color","red");
            $("#phone_form").submit();
        }else {
            alert("请输入手机号和6位验证码!");
        }

    });
</code></pre>
<p>以上代码用于检验手机号和手机验证码，正确后提交表单，否则提示错误！</p>
<p><strong>修改 doLogin 方法如下：</strong>    </p>
<pre><code>    @RequestMapping("/doLogin")
    public String doLogin(Model model, @RequestParam(value = "username",required = false) String email,
                          @RequestParam(value = "password",required = false) String password,
                          @RequestParam(value = "code",required = false) String code,
                          @RequestParam(value = "telephone",required = false) String telephone,
                          @RequestParam(value = "phone_code",required = false) String phone_code,
                          @RequestParam(value = "state",required = false) String state,
                          @RequestParam(value = "pageNum",required = false) Integer pageNum ,
                          @RequestParam(value = "pageSize",required = false) Integer pageSize) {

        //判断是否是手机登录
        if (StringUtils.isNotBlank(telephone)) {
            //手机登录
            String yzm = redisTemplate.opsForValue().get( telephone );//从redis获取验证码
            if(phone_code.equals(yzm)){
                //验证码正确
                User user = userService.findByPhone(telephone);
                getSession().setAttribute("user", user);
                model.addAttribute("user", user);
                log.info("手机快捷登录成功");
                return "/personal/personal";

            }else {
                //验证码错误或过期
                model.addAttribute("error","phone_fail");
                return  "../login";
            }

        } else {
            //账号登录

        if (StringUtils.isBlank(code)) {
            model.addAttribute("error", "fail");
            return "../login";
        }
        int b = checkValidateCode(code);
        if (b == -1) {
            model.addAttribute("error", "fail");
            return "../login";
        } else if (b == 0) {
            model.addAttribute("error", "fail");
            return "../login";
        }
        password = MD5Util.encodeToHex(Constants.SALT + password);
        User user = userService.login(email, password);
        if (user != null) {
            if ("0".equals(user.getState())) {
                //未激活
                model.addAttribute("email", email);
                model.addAttribute("error", "active");
                return "../login";
            }
            log.info("用户登录登录成功");
            getSession().setAttribute("user", user);
            model.addAttribute("user", user);
            return "/personal/personal";
        } else {
            log.info("用户登录登录失败");
            model.addAttribute("email", email);
            model.addAttribute("error", "fail");
            return "../login";
        }

    }

    }
</code></pre>
<p>代码解读如下：</p>
<p>（1）主要是根据手机号是否为空判断是手机登录还是账号登录，如果手机号不为空则为手机快捷登录；</p>
<p>（2）根据手机号从 Redis 中获取手机验证码，如果 Redis 中的验证码和用户输入的验证码一致，则登录成功，根据手机号查询用户，将用户 user 存入 Session 和 model 中，返回个人中心页面；</p>
<p>（3）如果不一致，说明验证码错误或者过期，将 <code>phone_fail</code> 添加到 model 中，并返回到登录页面。</p>
<p>最后重新启动项目测试，手机快捷登录成功！</p>
<blockquote>
  <p>第07课百度网盘地址：</p>
  <p>链接：https://pan.baidu.com/s/1lm25TwWulc8l8tFaI1wo9A 密码：aozj</p>
</blockquote></div></article>