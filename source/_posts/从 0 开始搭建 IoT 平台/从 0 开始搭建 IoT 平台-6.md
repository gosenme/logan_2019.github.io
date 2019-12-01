---
title: 从 0 开始搭建 IoT 平台-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这一节，我们将对设备注册接入的细节进行完善。</p>
<h3 id="">添加数据库索引</h3>
<p>我们需要对 Devices 的 product_name 和 device_name 做一个索引，因为在后面会经常通过这两个字段对 devices 进行查询，在 MongoDB shell 里面输入：</p>
<pre><code>use iothub
db.devices.createIndex({
    "production_name" : 1,
    "device_name" : 1
}, { unique: true })
</code></pre>
<blockquote>
  <p>MongoDB 插件在每次设备接入的时候都会使用 broker_name 来查询 Devices Collectiion， 所以我们也需要在 broker_name 上加一个索引：</p>
</blockquote>
<pre><code>use iothub
db.devices.createIndex({
    "broker_username" : 1
})
</code></pre>
<h3 id="-1">使用持久化连接</h3>
<p>细心的读者可能已经发现了， DeviceSDK 在连接到 Broker 的时候并没有指定 Client Identifier。没错，到目前为止，我们使用的都是在连接时自动分配的 Client Identifer， 没有办法很好地使用 QoS1 和 QoS2 的消息。</p>
<p>Client Identifier 是用来唯一标识 MQTT Client 的，由于我们之前的设计保证了(ProductName, DeviceName)是全局唯一的，所以一般来说用这个二元组作为 Client Identifier 就足够了。 但是，之前我也提到过，在某些场景下，可能会出现多个设备使用同样的设备三元组接入 Maque IotHub，综合这些情况，我们这样来设计 Maque IotHub 里的 Client Identifier。</p>
<p>设备提供一个可选的 ClientID 来标识自己，可以是硬件编号、AndroidID 等，如果设备提供 ClientID，那么使用 ProductName/DeviceName/ClientID 作为连接 Broker 的Client Identifier，否则使用ProductName/DeviceName。 根据这个规则对 DeviceSDK 进行修改。</p>
<pre><code class="javascript language-javascript">// IotHub_Device/sdk/iot_devices.js
...
class IotDevice extends EventEmitter {
    constructor({serverAddress = "127.0.0.1:8883", productName, deviceName, secret, clientID} = {}) {
        super();
        this.serverAddress = `mqtts://${serverAddress}`
        this.productName = productName
        this.deviceName = deviceName
        this.secret = secret
        this.username = `${this.productName}/${this.deviceName}`
        //根据 ClientID 设置
        if(clientID != null){
            this.clientIdentifier = `${this.username}/${clientID}`
        }else{
            this.clientIdentifier = this.username
        }
    }

    connect() {
        this.client = mqtt.connect(this.serverAddress, {
            rejectUnauthorized: false,
            username: this.username,
            password: this.secret,
            //设置 ClientID 和 clean session
            clientId: this.clientIdentifier,
            clean: false
        })
        ...
   }
 ... 
</code></pre>
<p>之后你可以再运行一次<code>samples/connect_to_server.js</code>看下效果。</p>
<blockquote>
  <p>Node.js 的 MQTT 库自带了断线重连功能，所以这里就不用我们来实现了。</p>
</blockquote>
<h3 id="serverapi">更多的 Server API</h3>
<p>我们还需要几个接口来完善注册流程.</p>
<h4 id="-2">获取某个设备的信息</h4>
<p>当业务系统查询设备信息的时候，我们并不是把 Device 的所有字段都返回。首先定义下返回内容：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/device.js
//定义 device.toJSONObject
deviceSchema.methods.toJSONObject = function () {
    return {
        product_name: this.product_name,
        device_name: this.device_name,
        secret: this.secret
    }
}
</code></pre>
<p>然后进行接口实现：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/devices.js
router.get("/:productName/:deviceName", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOne({"product_name": productName, "device_name": deviceName}, function (err, device) {
        if (err) {
            res.send(err)
        } else {
            if (device != null) {
                res.json(device.toJSONObject())
            } else {
                res.status(404).json({error: "Not Found"})
            }
        }
    })
})
</code></pre>
<pre><code>curl http://localhost:3000/devices/IotApp/V5MyuncRK

{"product_name":"IotApp","device_name":"V5MyuncRK","secret":"GNxU20VYTZ"}
</code></pre>
<h4 id="-3">列出某个产品下的所有设备</h4>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/devices.js
router.get("/:productName", function (req, res) {
    var productName = req.params.productName
    Device.find({"product_name": productName}, function (err, devices) {
        if (err) {
            res.send(err)
        } else {
            res.json(devices.map(function (device) {
                return device.toJSONObject()
            }))

        }
    })
})
</code></pre>
<pre><code>curl http://localhost:3000/devices/IotApp
[{"product_name":"IotApp","device_name":"V5MyuncRK","secret":"GNxU20VYTZ"}]
</code></pre>
<h4 id="brokerjwt">获取接入 Broker 的一次性密码（JWT）</h4>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/tokens.js

var express = require('express');
var router = express.Router();
var shortid = require("shortid")
var jwt = require('jsonwebtoken')

//这个值应该和 EMQ X etc/plugins/emqx_auth_jwt.conf 中的保存一致
const jwtSecret = "emqxsecret"

router.post("/", function (_, res) {
    var username = shortid.generate()
    var password = jwt.sign({
        username: username,
        exp: Math.floor(Date.now() / 1000) + 10 * 60
    }, jwtSecret)
    res.json({username: username, password: password})
})

module.exports = router
</code></pre>
<pre><code class="javascript language-javascript">// IotHub_Server/app.js
var tokensRouter = require('./routes/tokens')
app.use('/tokens', tokensRouter)
</code></pre>
<p>通过这个接口，可以签发一个有效期为 1 分钟的 username/password：</p>
<pre><code>curl http://localhost:3000/tokens -X POST
{"username":"apmE_JPll","password":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFwbUVfSlBsbCIsImV4cCI6MTU2ODMxNjk2MSwiaWF0IjoxNTU4MzE2OTYxfQ.-SnqvBGdO3wjSu7IHR91Bo58gb-VLFuQ28BeN6hlTLk"}
</code></pre>
<blockquote>
  <p>大家可能还发现了，在 ServerAPI 里面没有对调用者的身份进行认证和权限控制，也没有对输入参数进行校验，输出列表时也没有进行分页等的处理，当然在实际的项目中，这些都是有必要的。 但是这些属于 Web 编程的范畴，我想大家应该都非常熟悉了，所以在本课程中就跳过了，让课程的内容紧贴主题。</p>
</blockquote>
<h3 id="-4">从环境变量中读取配置</h3>
<p>根据 <a href="https://12factor.net/">The Twelve-Factor App</a> 的理念，从环境变量中读取配置项是一个非常好的 Practice，在我们的项目中有两个地方要用到配置：</p>
<ul>
<li>ServerAPI，比如 mongoDB 的地址；</li>
<li>DeviceSDK 端的 samples 里的代码会经常使用到预先注册的三元组（ProductName, DeviceName, Secret）。</li>
</ul>
<p>这里我们使用 <a href="https://www.npmjs.com/package/dotenv">dotenv</a> 来管理环境变量，它可以从一个 .env 文件中读取并设置环境变量。</p>
<pre><code class="javascript language-javascript">// IotHub_Server/app.js 
require('dotenv').config()
mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true })
</code></pre>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/tokens.js
const jwtSecret = process.env.JWT_SECRET
</code></pre>
<pre><code># IotHub_Server/.env
MONGODB_URL=mongodb://iot:iot@localhost:27017/iothub
JWT_SECRET=emqxsecret
</code></pre>
<pre><code class="javascript language-javascript">// IotHub_Device/samples/connect_to_server.js
require('dotenv').config()
var device = new IotDevice({
    productName: process.env.PRODUCT_NAME,
    deviceName: process.env.DEVICE_NAME,
    secret: process.env.SECRET
})
</code></pre>
<pre><code># otHub_Device/samples/.env
PRODUCT_NAME=注册接口获取的 ProductName
DEVICE_NAME=注册接口获取的 DeviceName
SECRET=注册接口获取的 Secret
</code></pre>
<hr />
<p>在这一节里，我们补全了设备注册流程的所有功能，完善了细节，接下来我们看如何实现监控设备的在线状态。</p>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=sd0730">《从 0 开始搭建 IoT 平台》</a></p>
<p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《从 0 开始搭建 IoT 平台》读者交流群，添加编辑小姐姐微信：「GitChatty6」，回复关键字「214」给编辑小姐姐获取入群资格。</p></div></article>