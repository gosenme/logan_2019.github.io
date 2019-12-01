---
title: MQTT 协议快速入门-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="mqtt">为什么要学 MQTT</h3>
<p>物联网曾被认为是继计算机、互联网之后，信息技术行业的第三次浪潮。随着基础通讯设施的不断完善，尤其是 5G 的出现，进一步降低了万物互联的门槛和成本。物联网本身也是 AI 和区块链应用很好的落地场景之一，各大云服务商也在纷纷上架物联网平台和服务。在 AI 和区块链的热潮过去之后，物联网很有可能成为下一个风口，在风口到来之前，提前进行一些知识储备，是很有必要的。</p>
<p>物联网通讯是物联网的一个核心内容，目前物联网的通讯协议并没有一个统一的标准，比较常见的有 MQTT、CoAP、DDS、XMPP 等，在这其中，MQTT（消息队列遥测传输协议）应该是应用最广泛的标准之一。我们可以来看一下各大云服务商提供的物联网套件服务：</p>
<p>阿里云</p>
<p><img src="https://images.gitbook.cn/a7ccfa80-9ec3-11e8-8e5d-ef0460a9dd5a" alt="enter image description here" /></p>
<p>腾讯云</p>
<p><img src="https://images.gitbook.cn/257e1a40-9ec4-11e8-8324-45c28b509596" alt="enter image description here" /></p>
<p>青云</p>
<p><img src="https://images.gitbook.cn/733df8e0-9ec4-11e8-991f-1fa5582600fd" alt="enter image description here" /></p>
<p>所以入门物联网，掌握 MQTT 是一个非常必要的步骤。</p>
<h3 id="mqtt-1">MQTT 是什么</h3>
<p>MQTT 的全称为 Message Queue Telemetry Transport，是在 1999 年，由 IBM 的 Andy Stanford-Clark 和 Arcom 的 Arlen Nipper 为了一个通过卫星网络连接输油管道的项目开发的。为了满足低电量消耗和低网络带宽的需求，MQTT 协议在设计之初就包含了以下一些特点：</p>
<ol>
<li>实现简单</li>
<li>提供数据传输的 QoS</li>
<li>轻量、占用带宽低</li>
<li>可传输任意类型的数据</li>
<li>可保持的会话（session）</li>
</ol>
<p>之后 IBM 一直将 MQTT 作为一个内部协议在其产品中使用，直到 2010 年，IBM 公开发布了 MQTT 3.1 版本。在 2014 年，MQTT 协议正式成为了 OASIS（结构化信息标准促进组织）的标准协议。随着多年的发展，MQTT 协议的重点也不再只是嵌入式系统，而是更广泛的物联网（Internet of Things）世界了。</p>
<p>MQTT 协议是什么？简单地来说 MQTT 协议有以下特性：</p>
<ul>
<li>基于 TCP 协议的应用层协议；</li>
<li>采用 C/S 架构；</li>
<li>使用订阅/发布模式，将消息的发送方和接受方解耦；</li>
<li>提供 3 种消息的 QoS（Quality of Service）: 至多一次，最少一次，只有一次；</li>
<li>收发消息都是异步的，发送方不需要等待接收方应答。</li>
</ul>
<p>虽然 MQTT 协议名称有 Message Queue 两个词，但是它并不是一个像 RabbitMQ 那样的一个消息队列，这是初学者最容易搞混的一个问题。MQTT 跟传统的消息队列相比，有以下一些区别：</p>
<ol>
<li>在传统消息队列中，在发送消息之前，必须先创建相应的队列；在 MQTT 中，不需要预先创建要发布的主题（可订阅的 Topic）；</li>
<li>在传统消息队列中，未被消费的消息总是会被保存在某个队列中，直到有一个消费者将其消费；在 MQTT 中，如果发布一个没有被任何客户端订阅的消息，这个消息将被直接扔掉；</li>
<li>在传统消息队列中，一个消息只能被一个客户端获取，在 MQTT 中，一个消息可以被多个订阅者获取，MQTT 协议也不支持指定消息被单一的客户端获取。</li>
</ol>
<p>MQTT 协议可以为大量的低功率、工作网络环境不可靠的物联网设备提供通讯保障。而它的应用范围也不仅如此，在移动互联网领域也大有作为：很多 Android App 的推送功能，都是基于 MQTT 实现的，也有一些 IM 的实现，是基于 MQTT 的。 </p>
<h3 id="mqtt-2">怎么学习 MQTT</h3>
<p>在本课程中，我们将逐一学习 MQTT 协议的每一个特性以及其最佳实践，并辅以实际的代码来进行讲解。</p>
<p>在学习完 MQTT 协议的所有特性以后，我们将做一个 IoT+AI 实战——将<a href="https://gitbook.cn/gitchat/column/59f1a77a9343b255e38edd78">《物体识别：TensorFlow on Android》</a>一课中的 App 改造成可以实时发布识别结果。在这个过程中，读者将学习：</p>
<ul>
<li>MQTT 数据包、数据收发流程详细解析</li>
<li>如何在 Web 端和移动端正确地使用 MQTT</li>
<li>如何搭建自己的 MQTT Broker</li>
<li>如何增强 MQTT 平台的安全性</li>
<li>使用 MQTT 设计和开发 IoT 产品和平台的最佳实践</li>
<li>MQTT 5.0 的新特性</li>
</ul>
<p>在学习完本课程以后，读者将具备独立架设和开发基于 MQTT 协议的 IoT 平台、实时通信系统，及相关物联网产品的能力；同时也可以将本课程当做 MQTT 协议的参考文档，对协议内容有疑问的时候可随时查询。</p>
<p>课程中使用的 MQTT 协议版本为 3.1.1，代码主要使用 MQTT 的 Node.js 实现来进行演示。</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5be4f4df2c33167c317beb8c&utm_source=fqsd001">点击了解更多《MQTT 协议快速入门》</a></p>
</blockquote></div></article>