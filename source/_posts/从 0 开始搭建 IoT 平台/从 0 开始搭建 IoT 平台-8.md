---
title: 从 0 开始搭建 IoT 平台-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在这一节中，我们会按照上一节的设计，编写代码来实现 IotHub 的设备在线状态管理功能。</p>
<p>首先来设计一下设备状态管理功能。</p>
<ol>
<li>设备不保存在线与否这个 boolean 值，而是保存一个 connection 的列表，包含了所有用这个设备的三元组接入的 connection，connection 的信息由 WebHook 捕获的 client_connected 事件提供。</li>
<li>当 client_connected 时，通过 username 里面 ProductName 和 DeviceName 查找到 Device 记录，然后用 ClientID 查找 Device 的 connection 列表，如果不存在该 ClientID 的 connection 记录，就新增一条 connection 记录；如果存在，则更新这条 connection 记录，状态为 connected。</li>
<li>当 client_disconnected时，通过 username 里面 ProductName 和 DeviceName 查找到 Device 记录，然后用 ClientID 查找 Device 的 connection 列表，如果存在该 ClientID 的 connection 记录，则更新这条connection 记录，状态为 disconnected。</li>
<li>业务系统可以通过查询设备详情来获取设备的连接状态。</li>
</ol>
<p>通过这样的设计，我们不仅可以知道一个设备是否在线，还能知道其连接的具体信息。</p>
<h3 id="connection">Connection模型</h3>
<p>我们定义一个 Connection 模型来存储连接信息：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/connection.js

const connectionSchema = new Schema({
    connected: Boolean,
    client_id: String,
    keepalive: Number,
    ipaddress: String,
    proto_ver: Number,
    connected_at: Number,
    disconnect_at: Number,
    conn_ack: Number,
    device: {type: Schema.Types.ObjectId, ref: 'Device'}
})

const Connection = mongoose.model("Connection", connectionSchema);
</code></pre>
<h3 id="hook">实现 Hook</h3>
<p>我们在 Device 类里用两个方法来实现处理 connect 和 disconnect 事件：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/device.js

//connected
deviceSchema.statics.addConnection = function (event) {
    var username_arr = event.username.split("/")
    this.findOne({product_name: username_arr[0], device_name: username_arr[1]}, function (err, device) {
        if (err == null &amp;&amp; device != null) {
            Connection.findOneAndUpdate({
                client_id: event.client_id,
                device: device._id
            }, {
                connected: true,
                client_id: event.client_id,
                keepalive: event.keepalive,
                ipaddress: event.ipaddress,
                proto_ver: event.proto_ver,
                connected_at: event.connected_at,
                conn_ack: event.conn_ack,
                device: device._id
            }, {upsert: true, useFindAndModify: false, new: true}).exec()
        }
    })

}
//disconnect
deviceSchema.statics.removeConnection = function (event) {
    var username_arr = event.username.split("/")
    this.findOne({product_name: username_arr[0], device_name: username_arr[1]}, function (err, device) {
        if (err == null &amp;&amp; device != null) {
            Connection.findOneAndUpdate({client_id: event.client_id, device: device._id},
                {
                    connected: false,
                    disconnect_at: Math.floor(Date.now() / 1000)
                }, {useFindAndModify: false}).exec()
        }
    })
}
</code></pre>
<p>接着在对应事件的时候调用上面现实的方法：</p>
<pre><code class="javascript language-javascript">//IotHub_Server/routes/emqx_web_hook

router.post("/", function (req, res) {
    if (req.body.action == "client_connected") {
        Device.addConnection(req.body)
    }else if(req.body.action == "client_disconnected"){
        Device.removeConnection(req.body)
    }
    res.status(200).send("ok")
})
</code></pre>
<p>然后我们修改一下设备详情接口，返回 connection 信息：</p>
<pre><code class="javascript language-javascript">// IotHub_Server/models/connection.js
connectionSchema.methods.toJSONObject = function () {
    return {
        connected: this.connected,
        client_id: this.client_id,
        ipaddress: this.ipaddress,
        connected_at: this.connected_at,
        disconnect_at: this.disconnect_at
    }
}
</code></pre>
<pre><code class="javascript language-javascript">// IotHub_Server/routes/devices.js
router.get("/:productName/:deviceName", function (req, res) {
    var productName = req.params.productName
    var deviceName = req.params.deviceName
    Device.findOne({"product_name": productName, "device_name": deviceName}).exec(function (err, device) {
        if (err) {
            res.send(err)
        } else {
            if (device != null) {
                Connection.find({device: device._id}, function (_, connections) {
                    res.json(Object.assign(device.toJSONObject(), {
                        connections: connections.map(function (conn) {
                            return conn.toJSONObject()
                        })
                    }))
                })
            } else {
                res.status(404).json({error: "Not Found"})
            }
        }
    })
})
</code></pre>
<p>这个时候运行<code>IotHub_Device/samples/connect_to_server.js</code>，然后调用设备详情接口<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq</code>，会得到以下输出：</p>
<pre><code>{"product_name":"IotApp","device_name":"c-jOc-2qq","secret":"m0PfE0DcNC","connections":[{"connected":true,"client_id":"IotApp/c-jOc-2qq","ipaddress":"127.0.0.1","connected_at":1558354603}]}
</code></pre>
<p>然后关闭<code>connect_to_server.js</code>，再一次调用设备详情接口<code>curl http://localhost:3000/devices/IotApp/c-jOc-2qq</code>，会得到以下输出：</p>
<pre><code>{"product_name":"IotApp","device_name":"c-jOc-2qq","secret":"m0PfE0DcNC","connections":[{"connected":false,"client_id":"IotApp/c-jOc-2qq","ipaddress":"127.0.0.1","connected_at":1558354603,"disconnect_at":1558355260}]}
</code></pre>
<blockquote>
  <p>由于 DeviceName 是随机生成的，在使用 curl 时，应该用电脑上生成的 DeviceName 替代相应参数或者路径。</p>
</blockquote>
<p>这样我们就完成了设备状态管理，业务系统通过查询设备详情，就可以知道设备是否在线了（有 connected==true 的 connection 记录），以及设备连接的一些附加信息。</p>
<p>细心的读者也许已经发现了，我们这样的解决方案是有一点瑕疵的：</p>
<ul>
<li>性能问题，每次设备上下线，包括 Publish/Subscribe 等，EMQ X 都发起一个 HTTP POST，这肯定是有损耗的，至于多大损耗以及能不能接受这损耗，取决于你的业务和数据量；</li>
<li>由于 Web 服务是并发的，所以说有可能出现在很短时间内发生的一对 connect/disconnect 事件， disconnect 会比 connect 先处理，导致设备的连接状态不正确；</li>
<li>设备下线时间我们取的是处理这个事件的时间，不准确。</li>
</ul>
<p>在本课程的后面，我们会实现一个基于 RabbitMQ 的插件来替换 WebHook， 在那个时候，我们再来尝试解决这些问题，在这之前，我们都将用 WebHook 来完成功能验证。</p>
<hr />
<p>这一节我们完成设备在线状态管理的全部功能，接下来我们完成设备的禁用和删除。</p></div></article>