---
title: MQTT 协议快速入门-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在这一课里我们来实现 Web 订阅端。本节课核心内容：</p>
<ul>
<li>MQTT over WebSocket</li>
<li>连接到 Broker</li>
<li>处理消息</li>
</ul>
<h3 id="111mqttoverwebsocket">11.1 MQTT over WebSocket</h3>
<p>我们要实现的是一个可以在浏览器里运行的 MQTT Client。MQTT 基于 TCP 协议，在目前主流的浏览器里面，使用 JavaScript 直接打开一个 TCP 连接是不可能的，所以在浏览器里面直接使用 MQTT 目前是没有办法的。</p>
<p>Socket API 可以解决这个问题，但是浏览器对 Socket API 的支持还非常有限。而我们可以应用 MQTT over WebSocket 来在浏览器中使用 MQTT，因为大部分主流浏览器都支持 WebSocket。MQTT over WebSocket 实现原理是把 MQTT 数据包封装在 WebSocket 帧里进行发送：</p>
<p><img src="https://images.gitbook.cn/8a8e8ce0-e7f2-11e8-802d-7d3566be2a1e" alt="enter image description here" /></p>
<p>MQTT over WebSocket 也需要 Broker 支持，不过目前大部分 Broker 都是支持的，包括本课程里面使用的 Public Broker。</p>
<h3 id="112broker">11.2 连接到 Broker</h3>
<p>首先需要在 HTML 里面加上支持 MQTT over WebSocket 的 JS 文件：</p>
<pre><code class="html language-html">&lt;script src="https://unpkg.com/mqtt@2.18.6/dist/mqtt.min.js"&gt;&lt;/script&gt;
</code></pre>
<p>然后连接到 Broker：</p>
<pre><code class="javascript language-javascript">var client = mqtt.connect("ws://iot.eclipse.org/ws")
</code></pre>
<p>注意这里 Broker 的 URL 中的协议部分变成了 “ws”。</p>
<p>在这里我们没有指定 Client Identifier，而 Client 库或 Broker 会为我们自动生成一个 Client Identifier。这样打开多个 Web 订阅端时，就不会发生冲突。但是这样是无法使用持久化会话的，所以在实际项目中，你应该为每一个 Web 订阅端分配一个唯一 Client Identifier，比如把用户 ID 作为 Client Identifier 的一部分。</p>
<p>接下来订阅相关主题：</p>
<pre><code class="javascript language-javascript">client.subscribe("front_door/detection/objects", {
                qos: 1
            }, function (err) {
                if (err != undefined) {
                    console.log("subscribe failed")
                } else {
                    console.log(`subscribe succeeded`)
                }
            })
</code></pre>
<h3 id="113">11.3 处理消息</h3>
<p>上一课中讲到，在接受消息的时候，我们需要对消息进行去重：</p>
<pre><code class="javascript language-javascript">var receivedMessages = new Set();
client.on("message", function (_, payload) {
        var jsonMessage = JSON.parse(payload.toString())
        if(!receivedMessages.has(jsonMessage.id)){
            receivedMessages.add(jsonMessage.id)
            //接下来把结果显示在页面上面
        }
    })
</code></pre>
<p>为了演示简单，这里使用了一个 Set 来保存已收到消息的 ID。实际项目中，可以用稍微复杂一点的数据结构，比如支持 Expiration 的缓存来存储已收到消息的 ID。</p>
<p>然后把接收到的结果在页面上显示出来（这里使用 Table 来显示）：</p>
<pre><code class="javascript language-javascript">var date = new Date(jsonMessage.timestamp * 1000)
$('#results tr:last').after(`&lt;tr&gt;&lt;td&gt;${date.toLocaleString()}&lt;/td&gt;&lt;td&gt;${jsonMessage.objects}&lt;/td&gt;&lt;td&gt;&lt;img src="${jsonMessage.image_url}" height="200"&gt;&lt;/td&gt;&lt;/tr&gt;`);
</code></pre>
<p>Web 订阅端的最终效果是这样的：</p>
<p><img src="https://images.gitbook.cn/f625ae50-a9a6-11e8-a631-83d8c23442de" alt="enter image description here" /></p>
<p>你可以在 <a href="https://github.com/sufish/mqtt_browser">https://github.com/sufish/mqtt_browser</a> 找到全部代码。</p>
<h3 id="114">11.4 小结</h3>
<p>我们花了两节课完成了一个 IoT+AI 的实战项目，在这个框架下还可以继续扩展新功能，比如将训练好的新模型从云端下发到设备端，以提升识别效率等。有兴趣的读者可以自行扩展。</p>
<p>下一课里我们来学习如何搭建自己的 Broker。</p>
<h3 id="">答疑与交流</h3>
<p>GitChat 编辑团队组织了一个《MQTT 协议快速入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「266」给<strong>小助手-伽利略</strong>获取入群资格。</p></div></article>