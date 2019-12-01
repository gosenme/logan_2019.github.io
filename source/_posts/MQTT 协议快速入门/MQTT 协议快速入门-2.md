---
title: MQTT 协议快速入门-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在这一课中，让我们来学习 MQTT 协议的基本概念和术语，同时也会介绍一下本课程中代码的开发环境搭建。本节课核心内容包括：</p>
<ul>
<li>MQTT 协议的通信模型</li>
<li>MQTT Client</li>
<li>MQTT Broker</li>
<li>MQTT 协议数据包</li>
</ul>
<h3 id="11mqtt">1.1 MQTT 协议的通信模型</h3>
<p>就像我们在之前提到的，MQTT 的通信是通过发布/订阅的方式来实现的，消息的发布方和订阅方通过这种方式来进行解耦，它们没有直接地连接，它们需要一个中间方。在 MQTT 里面我们称之为 Broker，用来进行消息的存储和转发。一次典型的 MQTT 消息通信流程如下所示：</p>
<p><img src="https://images.gitbook.cn/4c2c9a40-9f7d-11e8-98d1-e12fb7305527" alt="enter image description here" /></p>
<ol>
<li>发布方将消息发送到 Broker；</li>
<li>Broker 接收到消息以后，检查下都有哪些订阅方订阅了此类消息，然后将消息发送到这些订阅方；</li>
<li>订阅方从 Broker 获取该消息。</li>
</ol>
<p>在之后的课程里面，我们将发送方称为 Publisher，将订阅方称为 Subscriber。</p>
<h3 id="12mqttclient">1.2 MQTT Client</h3>
<p>任何终端，嵌入式设备也好，服务器也好，只要运行了 MQTT 的库或者代码，我们都称为 MQTT 的 Client。Publisher 和 Subscriber 都属于 Client，Pushlisher 或者 Subscriber 只取决于该 Client 当前的状态——是在发布还是在订阅消息。当然，一个 Client 可以同时是 Publisher 和 Subscriber。</p>
<p>MQTT Client 库在很多语言中都有实现，包括 Android、Arduino、Ruby、C、C++、C#、Go、iOS、Java、JavaScript，以及 .NET 等。如果你要查看相应语言的库实现，可以在<a href="https://github.com/mqtt/mqtt.github.io/wiki/libraries">这里</a>找到。</p>
<p>本课程中，我们主要使用 Node.js 的 MQTT Client 库来进行演示，所以需要先安装 Node.js，然后安装 MQTT Client 的 Node.js 包：</p>
<pre><code>npm install mqtt -g
</code></pre>
<h3 id="13mqttbroker">1.3 MQTT Broker</h3>
<p>如前面所讲的，Broker 负责接收 Publisher 的消息，并发送给相应的 Subscriber，它是整个 MQTT 订阅/发布的核心。在实际应用中，一个 MQTT Broker 还应该提供以下一些功能：</p>
<ul>
<li>可以横向扩展，比如集群，来满足大量的 Client 接入；</li>
<li>可以扩展接入业务系统；</li>
<li>易于监控，满足高可用性。</li>
</ul>
<p>我们在导读里面提到的阿里云、腾讯云、青云之类的云服务商提供的 MQTT 服务，其实就可以理解为他们提供了满足上述要求的 MQTT Broker。</p>
<p>在本课程中，我们使用一个公共的 MQTT Broker —— iot.eclipse.org 做演示，同时也会学习如何搭建一个 MQTT Broker。</p>
<h3 id="14mqtt">1.4 MQTT 协议数据包</h3>
<p>MQTT 协议的数据包格式非常简单，一个 MQTT 协议数据包由下面三个部分组成：</p>
<ul>
<li>固定头（Fixed header）：存在于所有的 MQTT 数据包中，用于表示数据包类型及对应标识，表明数据包大小；</li>
<li>可变头（Variable header）：存在于部分类型的 MQTT 数据包中，具体内容由相应类型的数据包决定；</li>
<li>消息体（Payload）：存在于部分 MQTT 数据包中，存储消息的具体数据。</li>
</ul>
<p>接下来看一下固定头的格式，可变头和消息体我们将在讲解各种具体类型的 MQTT 协议数据包的时候 case by case 地讨论。</p>
<p>固定头格式：</p>
<table border="1px">
   <tr>
      <td>Bit</td>
      <td>7</td>
      <td>6</td>
      <td>5</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
   </tr>
   <tr>
      <td>字节 1</td>
      <td colspan="4">MQTT 数据包类型</td>
      <td colspan="4">MQTT 数据包 Flag， 内容由数据包类型指定</td>
   </tr>
   <tr>
      <td>字节 2……</td>
      <td colspan="8">数据包剩余长度</td>
   </tr>
</table>
<p>固定头的第一个字节的高 4 位 bit 用于指定该数据包的类型，MQTT 的数据包有以下一些类型：</p>
<table border="1px">
   <tr>
      <td>名称</td>
      <td>值</td>
      <td>方向</td>
      <td>描述</td>
   </tr>
   <tr>
      <td>Reserved</td>
      <td>0</td>
      <td>不可用</td>
      <td>保留位</td>
   </tr>
   <tr>
      <td>CONNECT</td>
      <td>1</td>
      <td>Client 到 Broker</td>
      <td>Client 请求连接到 Broker</td>
   </tr>
   <tr>
      <td>CONNACK</td>
      <td>2</td>
      <td>Broker 到 Client</td>
      <td>连接确认</td>
   </tr>
   <tr>
      <td>PUBLISH</td>
      <td>3</td>
      <td>双向</td>
      <td>发布消息</td>
   </tr>
   <tr>
      <td>PUBACK</td>
      <td>4</td>
      <td>双向</td>
      <td>发布确认</td>
   </tr>
   <tr>
      <td>PUBREC</td>
      <td>5</td>
      <td>双向</td>
      <td>发布收到</td>
   </tr>
   <tr>
      <td>PUBREL</td>
      <td>6</td>
      <td>双向</td>
      <td>发布释放</td>
   </tr>
   <tr>
      <td>PUBCOMP</td>
      <td>7</td>
      <td>双向</td>
      <td>发布完成</td>
   </tr>
   <tr>
      <td>SUBSCRIBE</td>
      <td>8</td>
      <td>Client 到 Broker</td>
      <td>Client 请求订阅</td>
   </tr>
   <tr>
      <td>SUBACK</td>
      <td>9</td>
      <td>Broker 到 Client</td>
      <td>订阅确认</td>
   </tr>
   <tr>
      <td>UNSUBSCRIBE</td>
      <td>10</td>
      <td>Client 到 Broker</td>
      <td>Client 请求取消订阅</td>
   </tr>
   <tr>
      <td>UNSUBACK</td>
      <td>11</td>
      <td>Broker 到 Client</td>
      <td>取消订阅确认</td>
   </tr>
   <tr>
      <td>PINGREQ</td>
      <td>12</td>
      <td>Client 到 Broker</td>
      <td>PING 请求</td>
   </tr>
   <tr>
      <td>PINGRESP</td>
      <td>13</td>
      <td>Broker 到 Client</td>
      <td>PING 应答</td>
   </tr>
   <tr>
      <td>DISCONNECT</td>
      <td>14</td>
      <td>Client 到 Broker</td>
      <td>Client 主动中断连接</td>
   </tr>
   <tr>
      <td>Reserved</td>
      <td>15</td>
      <td>不可用</td>
      <td>保留位</td>
   </tr>
</table>
<p>固定头的低 4 位 bit 用于指定数据包的 Flag，不同的数据包类型，其 Flag 的定义是不一样的，每种数据包对应的 Flag 如下：</p>
<table border="1px">
   <tr>
      <td>数据包</td>
      <td>标识位</td>
      <td>Bit 3</td>
      <td>Bit 2</td>
      <td>Bit 1</td>
      <td>Bit 0</td>
   </tr>
   <tr>
      <td>CONNECT</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>CONNACK</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PUBLISH</td>
      <td>MQTT 3.1.1 使用</td>
      <td>DUP</td>
      <td>QoS</td>
      <td>QoS</td>
      <td>RETAIN</td>
   </tr>
   <tr>
      <td>PUBACK</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PUBREC</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PUBREL</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PUBCOMP</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>SUBSCRIBE</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>SUBACK</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>UNSUBSCRIBE</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>UNSUBACK</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PINGREQ</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>PINGRESP</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>DISCONNECT</td>
      <td>保留位</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
   </tr>
</table>
<blockquote>
  <p>注意：DUP、QOS、RETAIN 标识的使用将在后续的课程中详细讲解。</p>
</blockquote>
<p>从固定头的第 2 字节开始是用于标识 MQTT 数据包长度的字段，最少一个字节，最大四个字节，每一个字节的低 7 位用于标识值，范围为 0~127。最高位的 1 位是标识位，用来说明是否有后续字节来标识长度。例如：标识为 0，代表为没有后续字节；标识为 1，代表后续还有一个字节用于标识包长度。MQTT 协议规定最多可以用四个字节来标识包长度。</p>
<p>所以这四个字节最多可以标识的包长度为：(0xFF, 0xFF, 0xFF, 0x7F) = 268435455 字节，约 256M，这个是 MQTT 协议中数据包的最大长度。</p>
<blockquote>
  <p>注意：Remain Length 的值不包含固定头的大小，包括第 1 字节和 Remain Length 字段。</p>
</blockquote>
<h3 id="15">1.5 小结</h3>
<p>我们在这一课中学习了 MQTT 的通信模型，以及 Client 和 Broker 的概念，同时也学习了 MQTT 数据包的格式。接下来我们开始收发数据的第一步：从 Client 连接到 Broker。</p>
<p><strong>相关资料：</strong></p>
<ul>
<li><a href="https://github.com/mqtt/mqtt.github.io/wiki/libraries">MQTT Client 库在多种语言中的库实现</a></li>
</ul>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5be4f4df2c33167c317beb8c&utm_source=fqsd001">点击了解更多《MQTT 协议快速入门》</a></p>
</blockquote></div></article>