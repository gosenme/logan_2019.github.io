---
title: MQTT 协议快速入门-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>接下来我们来学习 MQTT 协议中的消息订阅与发布。本节课核心内容：</p>
<ul>
<li>订阅与发布模型</li>
<li>PUBLISH</li>
<li>代码实践：发布消息</li>
</ul>
<h3 id="41">4.1 订阅与发布模型</h3>
<p>在第一课中，我们介绍了 MQTT 基于订阅与发布的消息模型，MQTT 协议的订阅与发布是基于主题的（Topic），一个典型的 MQTT 消息发送与接收的流程如下：</p>
<ol>
<li>ClientA 连接到 Broker；</li>
<li>ClientB 连接到 Broker，并订阅主题 Topic1；</li>
<li>ClientA 发送给 Broker 一条消息，主题为 Topic1；</li>
<li>Broker 收到 ClientA 的消息，发现 ClientB 订阅了 Topic1，然后将消息转发到 ClientB；</li>
<li>ClientB 从 Broker 接收到该消息。</li>
</ol>
<p>和传统的队列有点不同，如果 ClientB 在 ClientA 发布消息之后再订阅 Topic1，ClientB 不会收到该条消息。</p>
<p>MQTT 通过订阅与发布模型对消息的发布者和订阅者进行解耦，发布者在发布消息时并不需要订阅方也连接到 Broker，只要订阅方之前订阅过相应主题，那么它在连接到 Broker 之后就可以收到发布方在它离线期间发布的消息。为了方便起见，在本课程中我们称这种消息为离线消息。 </p>
<p>接收离线的消息需要 Client 使用持久化会话，且发布时消息的 QoS 不小于 1。</p>
<p>在我们往下继续学习之前，很有必要搞清楚两组概念：发布者（Publisher）和订阅者（Subscriber），发送方（Sender）和接收方（Recevier）。弄清楚这两个概念才能很好理解订阅和发布的流程，以及之后 QoS 的概念。</p>
<h4 id="411publishersubscriber">4.1.1 Publisher 和 Subscriber</h4>
<p>Publisher 和 Subscriber 是相对于 Topic 来说的身份，如果一个 Client 向某个 Topic 发布消息，那么它就是 Publisher；如果一个 Client 订阅了某个 Topic，那么它就是 Subscriber。在上面的例子中，ClientA 是 Publisher， ClientB 是 Subscriber。</p>
<h4 id="412senderreceiver">4.1.2 Sender 和 Receiver</h4>
<p>Sender 和 Receiver 是相对于消息传输方向的身份，仍然是上面的例子：</p>
<ul>
<li>当 ClientA 发布消息时，它发送给 Broker 一条消息，那么 ClientA 是 Sender，Broker 是 Receiver；</li>
<li>当 Broker 转发消息给 ClientB 时，Broker 是 Sender，ClientB 是 Receiver。</li>
</ul>
<p>Publisher/Subscriber、Sender/Receiver 这两组概念最大的区别就是，Publisher 和 Subscriber 只可能是 Client。而 Sender/Receiver 有可能是 Client 和 Broker。解释清楚这两个不同的概念之后，我们接下来看一下 PUBLISH 消息包。</p>
<h3 id="42publish">4.2 PUBLISH</h3>
<p>PUBLISH 数据包是用于在 Sender 和 Receiver 之间传输消息数据的，也就是说，当 Publisher 要向某个 Topic 发布一条消息的时候，Publisher 会向 Broker 发送一个 PUBLISH 数据包；当 Broker 要将一条消息转发给订阅了某条主题的 Subscriber 时，Broker 也会向 Subscriber 发送一条 PUBLISH 数据包。PUBLISH 数据包的内容如下。</p>
<h4 id="421">4.2.1 固定头</h4>
<p><strong>消息重复标识（DUP flag）</strong>：1bit，0 或者 1，当 DUP flag = 1 的时候，代表该消息是一条重发消息，因 Receiver 没有确认收到之前的消息而重新发送的。这个标识只在 QoS 大于 0 的消息中使用。</p>
<p><strong>QoS</strong>：2bit，0、1 或者 2，代表 PUBLISH 消息的 QoS level，我们在 QoS 课程再详细讲解。</p>
<p><strong>Retain 标识（Retain flag）</strong>：1bit，0 或者 1，在从 Client 发送到 Broker 的 PUBLISH 消息中被设为 1 的时候，Broker 应该保存该条消息，当之后有任何新的 Subscriber 订阅 PUBLISH 消息中指定的主题时，都会先收到该条消息，这种消息也叫 Retained 消息；在从 Broker 发送到 Client 的 PUBLISH 消息中被设为 1 的时候，代表该条消息是一条 Retained 消息。</p>
<h4 id="422">4.2.2 可变头</h4>
<p><strong>数据包标识（ Packet Identifier）</strong>：2bit，用来标识一个唯一数据包，数据包标识只需要保证在从 Sender 到 Receiver 的一次消息交互（比如发送、应答为一次交互）中保持唯一。只在 QoS 不小于 1 的消息中使用，因为只有 QoS 不小于 1 的消息有应答流程，我们会在《第06课：QoS0 和 QoS1》详细讲解。</p>
<p><strong>主题名称（Topic Name）</strong>：主题名称是一个 UTF-8 编码的字符串，用来命名该消息发布到哪一个主题，Topic Name 可以是长度大于等于 1 任何一个字符串（可包含空格），但是在实际项目中，我们最好还是遵循以下一些最优方法。</p>
<ul>
<li>主题名称应该包含层级，不同的层级用 <code>/</code> 划分，比如，2 楼 201 房间的温度感应器可以用这个主题：“home/2ndfloor/201/temperature”。</li>
<li>主题名称开头不要使用 <code>/</code>，例如：“/home/2ndfloor/201/temperature”。</li>
<li>不要在主题中使用空格。</li>
<li>只使用 ASCII 字符。</li>
<li>主题名称在可读的前提下尽量短。</li>
<li>主题是大小写敏感的，“Home” 和 “home” 是两个不同的主题。</li>
<li>可以将设备的唯一标识加到主题中，比如：“warehouse/shelf/shelf1_ID/status”。</li>
<li>主题尽量精确，不要使用泛用的主题，例如在 201 房间有三个传感器，温度、亮度和湿度，那么你应该使用三个主题名称：“home/2ndfloor/201/temperature”、“home/2ndfloor/201/brightness”和“home/2ndfloor/201/humidity”，而不是让三个传感器都使用“home/2ndfloor/201”。</li>
<li>以 <code>$</code> 开头的主题属于 Broker 预留的系统主题，通常用于发布 Broker 的内部统计信息，比如 <code>$SYS/broker/clients/connected</code>，应用程序不要使用 <code>$</code> 开头的主题收发数据。</li>
</ul>
<h4 id="423payload">4.2.3 消息体（Payload）</h4>
<p>PUBLISH 消息的消息体中包含的是该消息要发送的具体数据，数据可以是任何格式的，二进制数据、文本、JSON 等，由应用程序来定义。在实际生产中，我们可以使用 JSON、Protocol Buffer 等对数据进行编码。 </p>
<p>当 Receiver 收到来自 Sender 的 PUBLISH 消息时，根据 QoS 的不同，还有后续的应答流程。我们在 QoS 课程再详细讲解。</p>
<p>当 PUBLISH 消息的 QoS=0 时， Receiver 不做任何应答。</p>
<h3 id="43">4.3 代码实践：发布消息</h3>
<p>接下来我们写一小段代码，向一个主题发布一条 QoS 为 1 的使用 JSON 编码的数据，然后退出：</p>
<pre><code>//publisher.js

javascript
var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://iot.eclipse.org', {
    clientId: "mqtt_sample_publisher_1",
    clean: false
})

client.on('connect', function (connack) {
    if(connack.returnCode == 0){
        client.publish("home/2ndfloor/201/temperature", JSON.stringify({current: 25}), {qos: 1}, function (err) {
            if(err == undefined) {
                console.log("Publish finished")
                client.end()
            }else{
                console.log("Publish failed")
            }
        })
    }else{
        console.log(`Connection failed: ${connack.returnCode}`)
    }
})
</code></pre>
<p>运行 <code>node publisher.js</code>，会得到以下输出：</p>
<pre><code>Publish finished
</code></pre>
<h3 id="44">4.4 小结</h3>
<p>在本节课我们学习了 MQTT 订阅和发布的模型，弄清楚了 Publisher/Subscriber、Sender/Receiver 的区别，并编写了发布消息的代码。接下来我们学习如何接收刚刚发布的消息。</p>
<h3 id="">答疑与交流</h3>
<p>为了让订阅课程的读者更快更好地掌握课程的重要知识点，我们为每个课程配备了课程学习答疑群服务，邀请作者定期答疑，尽可能保障大家学习效果。同时帮助大家克服学习拖延问题！</p>
<p>GitChat 编辑团队组织了一个《MQTT 协议快速入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「266」给<strong>小助手-伽利略</strong>获取入群资格。</p></div></article>