---
title: 从 0 开始搭建 IoT 平台-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在这一节中，我们来设计和实现设备生命周期管理中的禁用和删除功能。</p>
<h3 id="">设备禁用</h3>
<p>设备禁用的逻辑很简单，业务系统可以通过一个接口暂停设备的接入认证，被禁用的设备无法接入 IotHub；业务系统也可以通过一个接口恢复设备的接入认证，使设备可以重新接入 IotHub，这里还暗含着另外一个操作，在禁用设备的时候，如果这个设备已经接入 IotHub，且是在线状态，那么需要将这个设备踢下线。接下来我们来一步一步实现这些功能。</p>
<h4 id="serverapi">Server API</h4>
<p>首先在 Device 模型里加一个字段，来标识设备当前是否可以接入 IotHub：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/Device.js
const deviceSchema = new Schema({
    //ProductName
    product_name: {
        type: String,
        required: true
    },
    //DeviceName
    device_name: {
        type: String,
        required: true,
    },
    //接入EMQX时使用的username
    broker_username: {
        type: String,
        required: true
    },
    //secret
    secret: {
        type: String,
        required: true,
    },

    //可接入状态
    status: String
})
</code></pre>
<p>创建设备时默认状态为 active：</p>
<pre><code class="javascript language-javascript">//IotHub_Server/routes/device.js
router.post("/", function (req, res) {
    ...

    var device = new Device({
        product_name: productName,
        device_name: deviceName,
        secret: secret,
        broker_username: brokerUsername,
        status: "active"
    })

    ...
})
</code></pre>
<p>然后添加两个 Server API 来设置设备的接入状态，禁用/恢复：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/device.js

router.put("/:productName/:deviceName/suspend", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOneAndUpdate({"product_name": productName, "device_name": deviceName},
        {status: "suspended"}, {useFindAndModify: false}).exec(function (err) {
        if (err) {
            res.send(err)
        } else {
            res.status(200).send("ok")
        }
    })
})

router.put("/:productName/:deviceName/resume", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOneAndUpdate({"product_name": productName, "device_name": deviceName},
        {status: "active"}, {useFindAndModify: false}).exec(function (err) {
        if (err) {
            res.send(err)
        } else {
            res.status(200).send("ok")
        }
    })
})
</code></pre>
<h4 id="mongodb">配置 MongoDB 认证插件</h4>
<p>我们需要配置一下 MongoDB 认证，使它在认证接入的设备时会判断 Device 的 active 字段：</p>
<pre><code># &lt;EMQ X 安装目录&gt;/etc/plugins/emqx_auth_mongo.conf

auth.mongo.auth_query.selector = broker_username=%u, status=active
</code></pre>
<p>重新加载 MongoDB 认证插件：<code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins reload emqx_auth_mongo</code>。</p>
<p>这个时候我们可以来试一下，首先暂停设备的接入认证：
<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq/suspend -X PUT</code></p>
<p>然后运行 <code>IotHub_Device/samples/connect_to_server.js</code>，控制台的输出如下：</p>
<pre><code>Error: Connection refused: Not authorized
...
</code></pre>
<p>然后恢复这个设备的接入认证：
<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq/resume -X PUT</code>，控制台的输出如下：</p>
<pre><code>device is online
</code></pre>
<h4 id="-1">主动断开设备连接</h4>
<h5 id="emqxapi">EMQ X 监控管理 API</h5>
<p>当禁用设备的时候，如果设备已经连入了 IotHub，我们应该主动断开和这个设备的连接，MQTT 协议并没有在协议级别约定 Broker 如何来管理 Client 的连接，EMQ X Broker 提供了一套 Restful 的 API 来监控和管理 Broker，可以在<a href="https://developer.emqx.io/docs/broker/v3/cn/rest.html">这里</a>看到这些 API 的文档，我们通过调用 EMQ X 提供的 API 来主动和设备断开连接。</p>
<p>EMQ X 使用 HTTP Basic 的认证方式对 API 的调用者进行认证，在调用这些 API 之前，需要创建一个账号，在EMQ X中称为创建一个 Application，创建 Application 的命令格式为：<strong>mgmt insert <AppId> <Name></strong>，这里我们用 iothub 作为 AppId，Name 设为 MaqueIotHub:</p>
<p><code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl mgmt insert iothub MaqueIotHub</code></p>
<p>控制台输出为：</p>
<pre><code>AppSecret: Mjg3NDc3MDc1MjgxNTM3OTg2MTYwNjYwMjMyOTU2ODA1MTC
</code></pre>
<p>我们需要记录下这个 AppSecret。</p>
<p>EMQ X RestAPI 是通过插件的方式实现的，默认的访问地址是：<code>http(s)://&lt;host&gt;:8080/api/v3/</code>，可以在 <code>etc/plugins/emqx_management.conf</code> 进行配置，这个插件是默认加载的。</p>
<p>然后把这些信息都放入 .env 文件中：</p>
<pre><code># IotHub_Server/.env
EMQX_APP_ID=iothub
EMQX_APP_SECRET=Mjg3NDc3MDc1MjgxNTM3OTg2MTYwNjYwMjMyOTU2ODA1MTC
EMQX_API_URL=http://127.0.0.1:8080/api/v3/
</code></pre>
<h5 id="emqxapi-1">调用 EMQ X API</h5>
<p>EMQ X 断开 Client 连接的 API：</p>
<p><code>DELETE api/v3/connections/${clientid}</code></p>
<p>需要提供 ClientID 作为参数，在设备连接状态管理里面已经保存了设备的 ClientID，所以只用按需调用这个接口就可以了。</p>
<p>首先把对 EMQ X API 的调用进行一个封装：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/services/emqx_service.js
"use strict";
const request = require('request');

class EMQXService {
    static disconnectClient(clientId) {
        const apiUrl = `${process.env.EMQX_API_URL}/connections/${clientId}`
        request.delete(apiUrl, {
            "auth": {
                'user': process.env.EMQX_APP_ID,
                'pass': process.env.EMQX_APP_SECRET,
                'sendImmediately': true
            }
        }, function (error, response, body) {
            console.log('statusCode:', response &amp;&amp; response.statusCode);
            console.log('body:', body);
        })
    }
}

module.exports = EMQXService
</code></pre>
<p>在 Device 模型里实现断开 Device 所有连接的功能：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/device.js

deviceSchema.methods.disconnect = function(){
    Connection.find({device: this._id}).exec(function (err, connections) {
        connections.forEach(function (conn) {
            emqxService.disconnectClient(conn.client_id)
        })
    })
}
</code></pre>
<p>然后在 suspend 接口里调用 disconnect 方法：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/devices.js
...
router.put("/:productName/:deviceName/suspend", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOneAndUpdate({"product_name": productName, "device_name": deviceName},
        {status: "suspended"}, {useFindAndModify: false}).exec(function (err, device) {
        if (err) {
            res.send(err)
        } else {
            if (device != null) {
                device.disconnect()
            }
            res.status(200).send("ok")
        }
    })
})
</code></pre>
<p>这时我们再运行<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq/suspend -X PUT</code>，在运行<code>connect_to_server.js</code>的终端上会有以下输出：</p>
<pre><code>device is online
device is offline
Error: Connection refused: Not authorized
...
</code></pre>
<ol>
<li>设备连接上 IotHub 之后，输出<code>device is online</code>。</li>
<li>被禁用以后，连接被 IotHub 断开，输出<code>device is offline</code>。</li>
<li>DeviceSDK 的自动重连功能触发，因为设备已被禁用，所以在连接时输出：<code>Error: Connection refused: Not authorized</code>。</li>
</ol>
<h3 id="-2">删除设备</h3>
<p>完成了禁用设备的功能以后，删除设备对我们来说就非常简单了，基本上依葫芦画瓢就可以了。</p>
<ol>
<li>将设备的所有连接断开；</li>
<li>删除设备；</li>
<li>删除设备的连接信息。</li>
</ol>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/device.js

router.delete("/:productName/:deviceName", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOne({"product_name": productName, "device_name": deviceName}).exec(function (err, device) {
        if (err) {
            res.send(err)
        } else {
            if (device != null) {
                device.disconnect()
                device.remove()
                res.status(200).send("ok")
            } else {
                res.status(404).json({error: "Not Found"})
            }
        }
    })
})
</code></pre>
<p>同时，在删除设备时，删除所有的连接信息：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/device.js

deviceSchema.post("remove", function (device, next) {
    Connection.deleteMany({device: device._id}).exec()
    next()
})
</code></pre>
<p>可以运行<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq -X DELETE</code> 来看下效果。</p>
<hr />
<p>这一节我们完成了设备的禁用和删除，下一节，我们来讨论一下设备的权限管理。</p></div></article>