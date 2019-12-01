---
title: MQTT 协议快速入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>感谢订阅课程的读者们对作者的信任和支持。为方便大家学习和交流，我们特地收集并整理了《MQTT 协议快速入门》读者交流群中大家经常提到的问题及作者的解答，作为附录补充到课程中。</p>
<p><strong>1. 目前 MQTT 5.0 会马上普及吗？</strong></p>
<blockquote>
  <p>暂时不会，目前 Broker 以及 Client 实现的支持还都比较有限。</p>
</blockquote>
<p><strong>2. MQTT 模块如何实现持续的超低功耗连接？</strong></p>
<blockquote>
  <p>MQTT 建立的是 TCP 长连接，所以功耗会高一些，如果满足不了低功耗的要求，还可以选择基于 UDP 的 CoAP 协议。</p>
</blockquote>
<p><strong>3. 如何正确地理解 Retained 消息？</strong></p>
<blockquote>
  <p>Broker 收到 Retained 消息后，会单独保存一份，再向当前的订阅者发送一份普通的消息（Retained 标识为 0）。当有新订阅者的时候， Broker 会把保存的这条消息发给新订阅者（Retained 标识为 1）。</p>
</blockquote>
<p><strong>4. 怎么能让发送数据的一方快速收到指定设备的回应数据？</strong></p>
<blockquote>
  <p>只要发送的数据 Payload 里面包含发送方订阅的主题，接收方收到消息之后向这个主题发布一个消息，发送方就能收到了。 </p>
</blockquote>
<p><strong>5. 请问我部署好 Broker 后，怎么实现 Broker 和 Client 的通讯？</strong></p>
<blockquote>
  <p>根据你使用的语言选择一个 Client 的实现就可以了，在<a href="https://www.eclipse.org/paho/">这里</a>可以找到一些主流语言的 Client 库。 </p>
</blockquote>
<p><strong>6. 我的设备已经按照 MQTT 的协议在发数据，我在服务器部署的是 Mosquitto 代理，我现在不知道怎么设置 Mosquitto 才能将我的设备数据打印出来？</strong> </p>
<blockquote>
  <p>在服务器端创建一个 Subscriber 订阅相应主题，然后打印收到的消息。</p>
</blockquote>
<p><strong>7. 如果订阅者重复订阅一个主题，也会被当作新的订阅者。那何时会被当作旧的订阅者？</strong> </p>
<blockquote>
  <p>在下一次主动订阅这个主题之前，都会被当做旧的订阅者。</p>
</blockquote>
<p><strong>8. 100 台以内少量设备使用 MQTT，是自己搭还是用各种云提供的物联网服务？</strong> </p>
<blockquote>
  <p>看价格，使用云服务器一般比自建要便宜。</p>
</blockquote>
<p><strong>9. 有哪些开源的比较好的 MQTT Broker？</strong> </p>
<blockquote>
  <p>我使用过的有 EMQTT 和 Mosquitto，我推荐 EMQTT。</p>
</blockquote>
<p><strong>10. 目前国内的智慧社区具体案例有哪些？</strong> </p>
<blockquote>
  <p>应该不少了， 推荐一个我公司的<a href="https://www.toutiao.com/i6449177449455419917/?tt_from=weixin&utm_campaign=client_share&from=timeline&app=news_article&utm_source=weixin&isappinstalled=0&iid=12871462153&utm_medium=toutiao_android&wxshare_count=4&pbid=6628350828547933703">成都保障房智慧小区</a>。</p>
</blockquote>
<p><strong>11. MQTT 必须在 Linux 系统上开发吗？</strong> </p>
<blockquote>
  <p>不用，各个 OS 都有现成的 Client 实现。</p>
</blockquote>
<p><strong>12. AI+IoT 具体有哪些应用场景？</strong> </p>
<blockquote>
  <p>有很多，除了我在课程里面提到的，拿我公司做个例子：通过摄像头和智能门禁作为前端的数据采集，在后端对采集到的数据进行学习，可以做出一些分析。比如，发现哪栋楼、哪个单元可能存在群租等。</p>
</blockquote>
<h3 id="">答疑与交流</h3>
<p>GitChat 编辑团队组织了一个《MQTT 协议快速入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「266」给<strong>小助手-伽利略</strong>获取入群资格。</p></div></article>