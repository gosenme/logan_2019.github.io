---
title: 从 0 开始搭建 IoT 平台-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在本节中，我们将设计 IotHub 的设备在线状态管理功能。</p>
<p>如何得知一个设备是在线或离线，是大家经常问到的问题，也是在实际生产中非常必要的一个功能。</p>
<h3 id="poormanssolution">Poor man's Solution</h3>
<p>MQTT 协议并没有在协议级别约定如何对 Client 的在线状态进行管理，在<a href="https://gitbook.cn/gitchat/column/5be4f4df2c33167c317beb8c">《MQTT 协议快速入门》</a>里我介绍过一个解决思路：</p>
<ul>
<li>Client 在连接成功时向 TopicA 发送一个消息，指明 Client 已经上线；</li>
<li>Client 在连接时指定 LWT，Client 在离线时向 TopicA 发送一个 Retained 消息，表示已经离线；</li>
<li>只要订阅 TopicA 就可以获取 Client 上线和离线的状态了。</li>
</ul>
<p>这个解决方案在实际上是可行的，但是有一个问题就是，你始终需要保持一个接入 Broker 的 Client 来订阅 TopicA，如果说设备的数量往十万甚至几十万上去了，这个订阅 TopicA 的 Client 就很容易成为单点故障点，所以说这种解决方案的可扩展性比较差。</p>
<h3 id="emqx">使用 EMQ X 的解决方案</h3>
<p>EMQ X 提供了丰富的管理功能和接口，所以我们会使用 EMQ X 提供的功能来实现 IotHub 的设备连接状态管理功能。</p>
<h4 id="">系统主题</h4>
<p>EMQ X 使用许多系统主题发布 Broker 内部的状态和事件，你可以在<a href="https://developer.emqx.io/docs/broker/v3/cn/guide.html#sys">这里</a>看到系统主题的列表。</p>
<p>其中，订阅 <code>$SYS/brokers/${node}/clients/${clientid}/connected</code>可以获取 Client 上线的事件；订阅<code>$SYS/brokers/${node}/clients/${clientid}/disconnected</code>可以获取 Client 离线的事件。</p>
<blockquote>
  <p>其中<code>${node}</code>是指 EMQ X 的节点名，你可以在<code>&lt; EMQ X 安装目录&gt;/etc/emqx.conf</code> 里找的 node.name 配置项，默认为 emqx@127.0.0.1。</p>
</blockquote>
<p>那么，我们只需要订阅<code>$SYS/brokers/+/clients/+/connected</code>和<code>$SYS/brokers/+/clients/+/disconnected</code>就可以获取到所有的上线和离线事件了。接下来写一点代码实验一下：</p>
<pre><code class="javascript language-javascript">// IotHub_Device/samples/sys_topics.js
var mqtt = require('mqtt')
var jwt = require('jsonwebtoken')
require('dotenv').config()
var password = jwt.sign({
    username: "jwt_user",
    exp: Math.floor(Date.now() / 1000) + 10
}, process.env.JWT_SECRET)
var client = mqtt.connect('mqtt://127.0.0.1:1883', {
    username: "jwt_user",
    password: password
})
client.on('connect', function () {
    console.log("connected")
    client.subscribe("$SYS/brokers/+/clients/+/connected")
    client.subscribe("$SYS/brokers/+/clients/+/disconnected")
})

client.on("message", function (_, message) {
    console.log(message.toString())
})
</code></pre>
<p>然后先运行<code>sys_topics.js</code>，随后运行<code>connect_to_server.js</code>，接着关闭<code>connect_to_server.js</code>，我们会看到以下输出：</p>
<pre><code>{"clean_start":false,"clientid":"IotApp/V5MyuncRK","connack":0,"ipaddress":"127.0.0.1","keepalive":60,"proto_name":"MQTT","proto_ver":4,"ts":1558335733,"username":"IotApp/V5MyuncRK"}
{"clientid":"IotApp/V5MyuncRK","username":"IotApp/V5MyuncRK","reason":"closed","ts":1558335752}
</code></pre>
<p>第一行是 Client connected 事件的信息，第二行是 Client disconnected 的信息，这些信息包含 ClientID、IP 地址、连接时间等，非常详细。</p>
<p>不过这种解决方案的缺点也很明显，和上面提到的一样，订阅这 2 个主题的 Client 很容易成为单点故障点。</p>
<h4 id="hook">基于 Hook 的解决方案</h4>
<p>我比较喜欢 EMQ X 的一点就是，<strong>它设计了一套 Hook 系统，你可以通过这个 Hook 来捕获 Broker 内部的事件并进展处理</strong>。EMQ X 中 Hook 的定义如下图所示。</p>
<p><img src="https://images.gitbook.cn/FhoemUdMQwyCtNrw2sDbwZJD7rwE" alt="avatar" /></p>
<p>通常你需要编写一个插件来捕获并处理这些事件，不过 EMQ X 自带了一个 <a href="https://github.com/emqx/emqx-web-hook">WebHook 插件</a>，它的原理很简单，当像 Client 上线或下线之类的事件发生时，EMQ X 为把事件的信息 Post 到一个事先指定好的 URL 上，我们就可以进行处理了。</p>
<p>如何避免一个 Web 服务成为单点故障点，我想大家都应该很熟悉了，所以在这里我们使用基于 WebHook 的方式来实现设备的在线状态管理。</p>
<h5 id="webhook">开启 WebHook</h5>
<p>首先需要编辑 WebHook 的配置文件，将回调的 URL 指向本地运行 Express 应用：</p>
<pre><code>#&lt; EMQ X 安装目录&gt;/etc/plugins/emqx_web_hook.conf
web.hook.api.url = http://127.0.0.1:3000/emqx_web_hook
</code></pre>
<p>运行 <code>&lt; EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_web_hook</code></p>
<p>然后我们简单地实现一下这个 Hook， 把请求的参数打印出来：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/emqx_web_hook.js
var express = require('express');
var router = express.Router();

router.post("/", function (req, res) {
    console.log(req.body)
    res.status(200).send("ok")
})

module.exports = router
</code></pre>
<pre><code class="javascript language-javascript">// IotHub_Server/app.js
var webHookeRouter = require('./routes/emqx_web_hook')
app.use('/emqx_web_hook', webHookeRouter)
</code></pre>
<p>运行<code>samples/connect_to_server</code>，接着关闭，我们可以发现：</p>
<p>当 Client 连接时，EMQ X 会把以下的 JSON Post 到指定的 URL 上：</p>
<pre><code>{ 
  action: 'client_connected',
  client_id: 'IotApp/V5MyuncRK',
  username: 'IotApp/V5MyuncRK',
  keepalive: 60,
  ipaddress: '127.0.0.1',
  proto_ver: 4,
  connected_at: 1558338318,
  conn_ack: 0 
}
</code></pre>
<p>当 Client 断开连接时，EMQ X 会把以下的 JSON Post 到指定URL：</p>
<pre><code>{ 
  action: 'client_disconnected',
  client_id: 'IotApp/V5MyuncRK',
  username: 'IotApp/V5MyuncRK',
  reason: 'closed' 
}
</code></pre>
<blockquote>
  <p><code>connected_at</code> 是指连接的时刻的 unix 时间戳。
  这里要说明的是，<code>/emq_web_hook</code> 这个接口是在 Maque IotHub 内部使用的，不应该暴露给业务系统，本课程中为了让内容更紧凑，尽量跳过了这些属于 Web 编程的内容，但在实际项目中，是需要考虑的。</p>
</blockquote>
<p>在 Client connect 和 disconnect 事件里面，包含了 Client 连接时使用 username， 而 username 里面包含了(ProductName, DeviceName)，所以我们可以通过这些信息定位到是具体哪一个设备 connect 或者 disconnect，从而更新设备的连接状态。</p>
<hr />
<p>在这一节里，我们讨论了设备状态管理的几种实现方式，并选择了目前最优的一种方式，下一节，我们来实现具体的功能。</p>
<hr />
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《从 0 开始搭建 IoT 平台》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「214」给小助手-伽利略获取入群资格。</strong></p>
</blockquote></div></article>