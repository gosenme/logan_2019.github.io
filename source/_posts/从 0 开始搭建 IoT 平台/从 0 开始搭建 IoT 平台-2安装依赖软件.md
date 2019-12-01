---
title: 从 0 开始搭建 IoT 平台-2
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">安装依赖软件</h3>
<p>首先确保你的电脑已安装并运行以下软件</p>
<ul>
<li>MongoDB</li>
<li>Redis</li>
<li>InfluxDB</li>
<li>RabbitMQ</li>
</ul>
<p>以上软件可以使用默认配置运行。</p>
<h3 id="emqx">安装运行 EMQ X</h3>
<h4 id="-1">编译和安装</h4>
<p>请按照 5-6 节中的步骤编译和安装带有 emqx_rabbitmq_hook 的插件的 EMQ X。</p>
<h4 id="emqx-1">配置 EMQ X</h4>
<p>以下是需要配置的 EMQ X 配置项：</p>
<p><code>&lt;EMQ X 安装目录&gt;/etc/emqx.conf</code>:</p>
<pre><code>allow_anonymous = false
zone.external.mqueue_store_qos0 = false
module.subscription = on
module.subscription.1.topic = cmd/%u/+/+/+/#
module.subscription.1.qos = 1
module.subscription.2.topic = rpc/%u/+/+/+/#
module.subscription.2.qos = 1
module.subscription.3.topic = m2m/%u/+/+
module.subscription.3.qos = 1
</code></pre>
<p>如果是在开发环境，建议修改下面两项：</p>
<pre><code>enable_acl_cache = off 
acl_deny_action = disconnect
</code></pre>
<p>一个是让 ACL 列表的改动可以马上生效，一个是能方便发现 ACL 权限错误的情况。</p>
<p><code>&lt;EMQ X 安装目录&gt;/etc/plugins/emqx\_auth\_jwt.js</code>:</p>
<pre><code>auth.jwt.verify_claims = on
auth.jwt.verify_claims.username = %u
</code></pre>
<p><code>&lt;EMQ X 安装目录&gt;/etc/plugins/emqx\_auth\_mongo.js</code>:</p>
<pre><code>auth.mongo.database = iothub
auth.mongo.auth_query.collection = devices
auth.mongo.auth_query.password_field = secret
auth.mongo.auth_query.password_hash = plain
auth.mongo.auth_query.selector = broker_username=%u, status=active
auth.mongo.super_query = off
auth.mongo.acl_query.collection = device_acl
auth.mongo.acl_query.selector = broker_username=%u
</code></pre>
<p><code>&lt;EMQ X 安装目录&gt;/etc/plugins/emqx\_web\_hook.js</code>:</p>
<pre><code>web.hook.api.url = http://127.0.0.1:3000/emqx_web_hook
web.hook.encode_payload = base64
</code></pre>
<p>然后运行<code>&lt;EMQ X 安装目录&gt;/bin/emqx start</code></p>
<h4 id="-2">加载插件</h4>
<pre><code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_auth_mongo
&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_auth_jwt
</code></pre>
<p>选择使用 Web Hook：</p>
<pre><code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_web_hook
</code></pre>
<p>选择使用 RabbmitMQ Hook：</p>
<pre><code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_rabbitmq_hook
</code></pre>
<blockquote>
  <p>Web Hook 和 RabbitMQ Hook 只能二选一。</p>
</blockquote>
<h3 id="iothubserver">IotHub Server</h3>
<p>可以在<a href="https://github.com/sufish/IotHub_Server">这里</a>找到 IotHub Server 端的代码：</p>
<pre><code>git clone https://github.com/sufish/IotHub_Server
cd IotHub_Server
npm install
cp .env.sample .env
</code></pre>
<p>根据你的环境和配置修改.env：</p>
<pre><code>###运行IotHub Server需要的配置项
#API端口
PORT=3000
#Mongodb地址
MONGODB_URL=mongodb://iot:iot@localhost:27017/iothub
#需要和&lt;EMQ X 安装目录&gt;/etc/emqx_auth_jwt.conf中一致
JWT_SECRET=emqxsecret

#使用EMQ X REST API的账号，可通过bin/emqx_ctl mgmt insert &lt;APP_ID&gt; Maque IotHub添加
EMQX_APP_ID=
EMQX_APP_SECRET=

#EMQ X REST API地址
EMQX_API_URL=http://127.0.0.1:8080/api/v3/

#Redis
REDIS_URL=redis://127.0.0.1:6379

#RabbitMQ
RABBITMQ_URL=amqp://localhost

#InfluxDB
INFLUXDB=localhost

###运行Sample Code需要的环境变量
TARGET_DEVICE_NAME=#设备名DeviceName
TARGET_PRODUCT_NAME=#设备的产品名ProductName
</code></pre>
<p>最后运行 <code>nf start</code></p>
<h3 id="devicesdk">DeviceSDK</h3>
<p>可以在<a href="https://github.com/sufish/IotHub_Device">这里</a>找到 DeviceSDK 的代码：</p>
<pre><code>git clone https://github.com/sufish/IotHub_Device
cd IotHub_Device
npm install
cd samples
cp .env.sample .env
</code></pre>
<p>根据你的环境和配置修改.env：</p>
<pre><code>### 运行sample code需要的环境变量

#设备的ProductName, DeviceName和Secret, 调用IotHub Server API的对应接口创建
PRODUCT_NAME=
DEVICE_NAME=
SECRET=

#需要和&lt;EMQ X 安装目录&gt;/etc/emqx_auth_jwt.conf中一致
JWT_SECRET=emqxsecret

##执行设备间通信示例代码时，对端设备的DeviceName和Secret, 调用IotHub Server API的对应接口创建
DEVICE_NAME2=
SECRET2=
</code></pre>
<p>环境变量配置好以后，可以运行 IotHub_Server/samples 和 IotHub_Device/samples 里面的示例代码，具体请查看各节的内容。</p>
<h3 id="emqx32emqxemqx_rabbitmq_hook">在 EMQ X 3.2+ 上编译 EMQ X 以及 emqx_rabbitmq_hook 插件</h3>
<p>首先根据 <a href="https://www.rebar3.org/docs/getting-started#section-installing-from-source">rebar3 安装文档</a> 安装编译工具 rebar3</p>
<p>然后：</p>
<pre><code>git clone https://github.com/emqx/emqx-rel
cd emqx-rel
</code></pre>
<p>修改<code>rebar.config</code>:</p>
<pre><code>{deps,
    [
    ...
    , {emqx_rabbitmq_hook, {git, "https://github.com/sufish/emqx_rabbitmq_hook", {branch, "master"}}}
    ]}.

relx,
    [ 
    , {release, {emqx, git_describe},
        [ ...
        , {emqx_rabbitmq_hook, load}
        ]}    
</code></pre>
<p>然后运行 <code>make</code>, 编译完成以后生成的 EMQ X 和插件位于<code>./_build/emqx/rel/emqx/</code>。</p></div></article>