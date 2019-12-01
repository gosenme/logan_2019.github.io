---
title: 从 0 开始搭建 IoT 平台-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在本节课中，我们将<strong>设计和实现从设备注册到接入 IotHub 的主要流程</strong>。</p>
<p>首先我们定义一下设备注册到接入 IotHub 的流程。</p>
<h3 id="">注册流程</h3>
<ol>
<li>业务系统调用 Maque IotHub Server API 的设备注册 API，提供要注册设备的 ProductName。</li>
<li>Maque IotHub Server 根据业务系统提供的参数生成一个三元组（ProductName, DeviceName, Secret），然后将该三元组存储到 MongoDB，同时存储到 MongoDB 的还有该设备接入 EMQ X 的用户名： ProductName/DeviceName。</li>
<li>Maque IotHub Server API 将生成的三元组返回给业务系统，业务系统应该保存这个三元组，以后调用 Maque IotHub Server API 时需要使用。</li>
<li>业务系统通过某种方式，例如烧写 Flash，将这个三元组"写"到物联网设备上。</li>
<li>设备应用代码调用 Maque IotHub DeviceSDK，传入三元组。</li>
<li>Maque IotHub DeviceSDK 使用 username: ProductName/DeviceName, password: Secret连接到 EMQ X Broker。</li>
<li>EMQ X Broker 到 MongoDB 里面查询 ProductName/DeviceName 和 Secret，如果匹配，则允许连接。</li>
</ol>
<p>注册流程如下图所示。</p>
<p><img src="https://images.gitbook.cn/Fk6KxeeiJKVwktIe6OrXxNP53wK0" alt="avatar" /></p>
<h3 id="api">设备注册 API</h3>
<p>接下在 IotHub_Server 项目里实现 <strong>Maque IotHub Server API</strong> 的设备注册 API：</p>
<p>我们在 MongoDB 里创建一个名为 IotHub 的数据来存储设备信息。</p>
<h4 id="-1">定义设备模型</h4>
<p>这里，我们使用 <a href="https://mongoosejs.com/">mongoose</a> 来做 MongoDB 相关的操作，首先定义 Device 模型：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/device.js
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
    //接入 EMQ X 时使用的 username
    broker_username: {
        type: String,
        required: true
    },
    //secret
    secret: {
        type: String,
        required: true,
    }
})
</code></pre>
<h4 id="restfulapi">Restful API 实现</h4>
<p>每次在生成新设备的时候，由系统自动生成 DeviceName 和 Secret，DeviceName 和 Secret 应该是随机且唯一的字符串，例如 UUID，这里，我们用 <a href="https://github.com/dylang/shortid">shortid</a> 来生成稍短一点的随机唯一字符:</p>
<pre><code class="javascript language-javascript">// routes/devices.js
...
router.post("/", function (req, res) {
    var productName = req.body.product_name
    var deviceName = shortid.generate();
    var secret = shortid.generate();
    var brokerUsername = `${productName}/${deviceName}`

    var device = new Device({
        product_name: productName,
        device_name: deviceName,
        secret: secret,
        broker_username: brokerUsername
    })

    device.save(function (err) {
        if(err){
            res.status(500).send(err)
        }else{
            res.json({product_name: productName, device_name: deviceName, secret: secret})
        }
    })
})

...
</code></pre>
<p>接着我们将这个 router 挂载到 /devices 下面，并连接到 MongoDB：</p>
<pre><code class="javascript language-javascript">//app.js
...
mongoose.connect('mongodb://iot:iot@localhost:27017/iothub', { useNewUrlParser: true })
var deviceRouter = require('./routes/devices');
app.use('/devices', deviceRouter);
...
</code></pre>
<p>运行 <code>bin/www</code> 启动 Web 服务器，然后在命令行用 curl 调用这个接口：</p>
<pre><code>curl -d "product_name=IotApp" -X POST http://localhost:3000/devices
</code></pre>
<p>输出为：<code>{"product_name":"IotApp","device_name":"V5MyuncRK","secret":"GNxU20VYTZ"}</code></p>
<blockquote>
  <p>ProductName 包含的字符是有限制的，不能包含<code># / +</code>以及 IotHub 预留的一些字符，为了演示，这里跳过了输入参数的校验，但是在实际项目中，是需要加上的。</p>
</blockquote>
<p>到这里，设备注册就成功了，我们需要记录下这个三元组。</p>
<h3 id="emqx_auth_mongoconf">修改 emqx_auth_mongo.conf</h3>
<p>接下来需要按照我们定义的数据库结构来修改 EMQ X MongoDB 认证插件的配置，下面是需要在上一节内容上修改的项：</p>
<pre><code># 存储用户名和密码的 database
auth.mongo.database = iothub

# 存储用户名和密码的 collection
auth.mongo.auth_query.collection = devices

# 密码字段
auth.mongo.auth_query.password_field = secret

# 查询记录时的 selector
auth.mongo.auth_query.selector = broker_username=%u
</code></pre>
<p>编辑完成以后重载下 MongDB 认证插件： 
<code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins reload emqx_auth_mongo</code>。</p>
<h3 id="devicesdk">修改 DeviceSDK</h3>
<p>接下在 <strong>IoTHub_Device</strong> 项目里对 DeviceSDK 进行修改，接受三元组作为初始化参数：</p>
<pre><code class="javascript language-javascript">// sdk/iot_device.js

...
class IotDevice extends EventEmitter {
    constructor({serverAddress = "127.0.0.1:8883", productName, deviceName, secret} = {}) {
        super();
        this.serverAddress = `mqtts://${serverAddress}`
        this.productName = productName
        this.deviceName = deviceName
        this.secret = secret
        this.username = `${this.productName}/${this.deviceName}`
    }
    connect() {
        this.client = mqtt.connect(this.serverAddress, {
            rejectUnauthorized: false
            username: this.username,
            password: this.secret
        })
        ...
    }

    ...
}   
...
</code></pre>
<p>然后我们用刚才记录下的三元组作为参数调用 DeviceSDK 接入 Maque IotHub:</p>
<pre><code class="javascript language-javascript">// samples/connect_to_server.js
...
var device = new IotDevice({productName: "IotApp", deviceName: "V5MyuncRK", secret: "GNxU20VYTZ"})
...
</code></pre>
<p>然后再运行<code>samples/connect_to_server.js</code>，会得到以下输出：</p>
<pre><code>device is online
</code></pre>
<p>这说明设备已经完成注册并成功接入 IotHub 了。</p>
<hr />
<p>这一节我们完成了<strong>设备注册到接入的主要流程</strong>，下一节，我们将继续完善细节。</p>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=sd0730">《从 0 开始搭建 IoT 平台》</a></p>
<blockquote>
  <p>注意！！！
  为了方便学习和技术交流，特意创建了读者群，入群方式放在 第 1-5 课 文末，欢迎已购本课程的同学入群交流。</p>
</blockquote></div></article>