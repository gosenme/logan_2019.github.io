---
title: 从 0 开始搭建 IoT 平台-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在本课中，我们将安装开发物联网平台时使用到的组件，并把物联网平台的开发环境搭建起来。</p>
<h3 id="">安装组件</h3>
<p>首先在开发机上面安装开发需要的组件。</p>
<h4 id="mongodb">MongoDB</h4>
<p>MongDB 是一个基于分布式文件存储的数据库，我们会把 MongoDB 作为物联网平台主要的数据存储工具。</p>
<p>可以在<a href="https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials">这里</a>找到 MongoDB 的安装文档，根据文档在对应的系统上安装和运行 MongoDB。</p>
<h4 id="redis">Redis</h4>
<p>Redis 是一个高效的内存数据库，物联网平台会使用 Redis 来实现缓存和简单的队列功能。</p>
<p>请根据<a href="https://redis.io/download">这里</a>的文档，在对应的系统上安装和运行 Redis。</p>
<h4 id="nodejs">Node.js</h4>
<p>Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境，我们会使用 Node.js 来开发物联网平台的主要功能。</p>
<p>请根据<a href="https://nodejs.org/en/download/">这里</a>的文档在对应的系统上面安装 Node.js。</p>
<h4 id="rabbitmq">RabbitMQ</h4>
<p>RabbitMQ 是使用 Erlang 编写的 AMQP Broker，物联网平台使用 RabbitMQ 作为队列系统实现物联网平台内部以及物联网平台到业务系统的异步通信。</p>
<p>请根据<a href="https://www.rabbitmq.com/download.html">这里</a>在对应的系统上按照和运行 RabbitMQ。</p>
<h4 id="emqx">EMQ X</h4>
<p>EMQ X 是一个使用 Erlang 编写的 MQTT Broker，物联网平台使用 EMQ X 来实现 MQTT/CoAP 协议接入，并使用 EMQ X 的一些高级功能来简化和加速开发。</p>
<p>可以在<a href="https://developer.emqx.io/docs/broker/v3/cn/install.html">这里</a>找到 EMQ X 的安装文档，安装完毕之后，在控制台运行：</p>
<pre><code>&lt;EMQ X 安装目录&gt;/bin/emqx start
</code></pre>
<p>如果命令行输出为 <code>emqx 3.2.0 is started successfully!</code> 那说明 EMQ X 已经成功安装并运行了。</p>
<blockquote>
  <p>本课程在编写时，使用的版本为EMQ X Broker V 3.2.0。
  EMQ X Enterprise为 EMQ X 的付费版本，注意不要安装错了。</p>
</blockquote>
<p>那么开发物联网平台需要的组件就安装完了，接下来我们简单介绍一下物联网平台的各个组成部分。</p>
<p>首先给这个物联网平台取一个代号，就叫它 Maque IotHub 吧，寓意麻雀虽小，五脏俱全。 接下来我们把后续课程中会出现的实体都定义一下：</p>
<ul>
<li><strong>Maque IotHub：</strong>我们将要开发的物联网平台，简称 IotHub。</li>
<li><strong>Maque IotHub Server API：</strong>Maque IotHub 的服务端 API，以 Restful API 的形式将功能提供给外部业务系统调用，简称 Server API。</li>
<li><strong>Maque IotHub Server</strong>：Maque IotHub 的服务端，包含了 Server API 和主要的 IotHub 服务端功能代码，简称为 IotHub Server。</li>
<li><strong>业务系统：</strong>指实现特定物联网应用服务端的业务逻辑系统，它通过调用 Maque IotHub Server API 的方式来控制设备/使用设备上报的数据，Maque IotHub 为它屏蔽了和设备交互的细节。</li>
<li><strong>Maque IotHub DeviceSDK：</strong> Maque IotHub 提供的设备端 SDK，设备通过调用 SDK 提供的 API 接入 Maque IotHub，并和业务系统进行交互，简称 DeviceSDK。</li>
<li><strong>设备应用代码：</strong>实现设备具体功能的代码，比如打开灯、在屏幕上显示温度等，它调用 Maque IotHub DeviceSDK 来使用 Maque IotHub 提供的功能。</li>
</ul>
<p>在后续的课程中就用 IotHub 来指代我们开发的这个物联网平台，用 DeviceSDK 来指代设备端的 SDK 代码，用 IotHub Server 来指代物联网平台的服务端代码。</p>
<h3 id="-1">项目结构</h3>
<p>本课程会使用两个 Node.js 的项目来进行开发，分别是物联网平台的服务端代码 IotHub Server 和设备端代码 DeviceSDK。</p>
<h4 id="maqueiothubserver">Maque IotHub Server</h4>
<p>服务端代码以一个 <a href="https://expressjs.com/">Express</a> 项目作为开始， Express 是一个 Node.js 轻量级的 Web 开发框架，非常适合开发 Restful API，项目的结构如下图所示：</p>
<p><img src="https://images.gitbook.cn/FgMYlCCFkWhM34MSsGNormq-d0te" alt="avatar" /></p>
<p>这个项目包含了 Maque IotHub Server API 以及 Maque IotHub 服务端的一些其他功能。</p>
<h4 id="maqueiothubdevicesdk">Maque IotHub DeviceSDK</h4>
<h5 id="mqtt">测试 MQTT 连接</h5>
<p>首先我们来验证一下 EMQ X Broker 是否已经配置正确，并可以接受 MQTT 连接了。</p>
<p>同样地，这里使用一个 Node.js 项目开发 Maque IotHub DeviceSDK 代码。</p>
<p>在 <code>package.json</code> 中添加 MQTT 的 Node.js 库：</p>
<pre><code class="javascript language-javascript">"dependencies": {
    "mqtt": "^2.18.8"
  }
</code></pre>
<p>然后运行 <code>npm install</code>。</p>
<p>我们可以写一小段代码来测试一下 MQTT 连接：</p>
<pre><code class="javascript language-javascript">//test_mqtt.js
var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://127.0.0.1:1883')
client.on('connect', function (connack) {
    console.log(`return code: ${connack.returnCode}`)
    client.end()
})
</code></pre>
<p>如果不出意外的话，控制台会输出：<code>return code: 0</code>。</p>
<h5 id="-2">重新组织代码</h5>
<p>为了方便设备应用代码的开发， DeviceSDK 会把和 MQTT 相关代码，以及同Maque IotHub Server交互的相关的代码进行封装，这里我们实现一个类 <code>IotDevice</code>作为 DeviceSDK 的入口：</p>
<pre><code class="javascript language-javascript">//iot_device.js
"use strict";
var mqtt = require('mqtt')
const EventEmitter = require('events');

class IotDevice extends EventEmitter {
    constructor(serverAddress = "127.0.0.1:8883") {
        super();
        this.serverAddress = `mqtts://${serverAddress}`
    }

    connect() {
        this.client = mqtt.connect(this.serverAddress, {
            rejectUnauthorized: false
        })
        var self = this
        this.client.on("connect", function () {
            self.emit("online")
        })
        this.client.on("offline", function () {
            self.emit("offline")
        })
        this.client.on("error", function (err) {
            self.emit("error", err)
        })
    }

    disconnect() {
        if (this.client != null) {
            this.client.end()
        }
    }
}


module.exports = IotDevice;
</code></pre>
<p>这段代码做了这几件事。</p>
<ul>
<li>封装了 MQTT Client 的 connect 和 disconnect 。</li>
<li>通过设定 MQTT 连接地址为 <code>mqtts://127.0.0.1:8883</code> 的方式，在传输层使用 SSL。 EMQ X 默认使用一个自签署的的证书，所以我们需要设定 <code>rejectUnauthorized: false</code>。</li>
<li>通过 Events 和设备应用代码进行交互。</li>
</ul>
<p>那么使用 <code>IotDevice</code> 类进行连接设备应用代码如下：</p>
<pre><code class="javascript language-javascript">var device = new IotDevice()
device.on("online", function () {
    console.log("device is online")
    device.disconnect()
})
device.on("offline", function () {
    console.log("device is offline")
})
device.connect()
</code></pre>
<p>Maque IotHub DeviceSDK 项目结构如下图所示：</p>
<p><img src="https://images.gitbook.cn/FgyZmtjnUefFwkOfHe74LSDXemsw" alt="avatar" /></p>
<ul>
<li>在 sdk 目录中是 DeviceSDK 的代码。</li>
<li>在 samples 目录中是调用 DeviceSDK 的示例代码。</li>
</ul>
<p>工作台准备完毕！ 准备好开发环境以后，下面就开始实现第一个功能：<strong>设备注册</strong>。</p>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=sd0730">《从 0 开始搭建 IoT 平台》</a></p>
<blockquote>
  <p>注意！！！
  为了方便学习和技术交流，特意创建了读者群，入群方式放在 第 1-5 课 文末，欢迎已购本课程的同学入群交流。</p>
</blockquote></div></article>