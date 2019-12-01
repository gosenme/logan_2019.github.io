---
title: 从 0 开始搭建 IoT 平台-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在本节中，我们将设计 IotHub 的设备认证机制。</p>
<h3 id="">设备三元组</h3>
<p>EMQ X 在默认的情况是允许匿名连接的，所以在上一节课程中，<code>IotDevice</code>类在连接 MQTT Broker 的时候没有指定 username 和 password 也能成功。</p>
<p>当然，我们肯定不希望任意一个设备都能连接到 Maque IotHub。首先我们需要到 Maque IotHub 注册一个设备，然后设备再通过由 Maque IotHub 下发的 username/password 连接到 Maque IotHub，以实现一机一密。</p>
<p><strong>阿里云 IoT 平台用一个三元组（ProductKey, DeviceName, Secret）来标识一个逻辑上的设备</strong>，ProductKey 是指设备所属的产品，DeviceName 用来标识这个设备的唯一名称，Secret 是指这个设备连接物联网平台使用的密码。我认为这是一个很好的设计，因为即使在同一家公司内部，往往也会有多个服务不同业务的物联网产品需要接入，所以多一个 ProductKey 对后续的主题名、数据存储和分发等进行一个区分是很有必有的。</p>
<p><strong>Maque IotHub 将使用类似的三元组（ProductName, DeviceName, Secret）来标识逻辑上的一台设备</strong>。ProductName由业务系统提供，可以是一个有意义的 ASCII 字符串，DeviceName 由 IotHub 自动生成，（ProductName, DeviceName）应该是全局唯一的。</p>
<p>这里我们约定，对一个设备（ProductName1, DeviceName1, Secret1），它接入 Maque IotHub 的 username 为 <code>ProductName1/DeviceName1</code>，password 为 <code>Secret1</code>。</p>
<blockquote>
  <p>为什么说三元组标识的是逻辑上的一台设备而不是物理上的一台设备？
  比如说：移动应用接入 Maque IotHub 来订阅某个主题，假如有一个用户在多个移动设备上用同一个账号登录，他使用的应该是同一个三元组，因为他订阅的消息在每个设备上都应该能收到，那么在这种情况下一个三元组实际上是对应多个物理设备。后面我们再来讲怎么来区分物理设备。</p>
  <p>为什么要用"/"做分隔符，这里先不作说明，在讲到下行数据处理的部分再来解释。</p>
</blockquote>
<h3 id="emqx">EMQ X 认证方式</h3>
<p>EMQ X 通过插件提供了多种灵活的认证方式，你可以在<a href="https://developer.emqx.io/docs/broker/v3/cn/plugins.html#">这里</a>找到 EMQ X 自带的插件列表，Maque IotHub 使用 MongoDB 作为数据存储，所以这里我们选择 <a href="https://github.com/emqx/emqx-auth-mongo">MongoDB 认证插件</a>。除了使用 MongoDB 认证以外，我们还会使用 JWT 的认证方式来提供一种临时性的接入认证。</p>
<p>在启用认证插件之前，我们需要关闭 EMQ X 的默认匿名认证。</p>
<p>编辑 <code>&lt;EMQ X 安装目录&gt;/etc/emqx.conf</code>，修改以下配置项：</p>
<pre><code>allow_anonymous = false
</code></pre>
<p>然后重新启动 EMQ X <code>&lt;EMQ X 安装目录&gt;/bin/emqx restart</code>。</p>
<h4 id="mongodb">MongoDB 认证</h4>
<p>MongoDB 的认证插件功能逻辑很简单：将设备的 username、password 存储在 MongoDB 的某个 Collection 中，当设备发起 Connect 的时候，Broker 再查找这个 Collection，如果 username/password 能匹配得上，则允许连接，否则拒绝连接。</p>
<p>在<code>&lt;EMQ X 安装目录&gt;/etc/plugins/emqx_auth_mongo.conf</code> 可以对 MongoDB 认证进行配置，配置项很多，在这里我们看几个关键的配置项。</p>
<ul>
<li><strong>MongoDB 地址：</strong> <code>auth.mongo.server = 127.0.0.1:27017</code> 。</li>
<li><strong>用于认证的数据库：</strong> <code>auth.mongo.database = mqtt</code> 存储设备 username 和 password 的数据库，这里暂时用默认值。</li>
<li><strong>用于认证的 Collection：</strong> <code>auth.mongo.auth_query.collection = mqtt_user</code> 存储设备 username 和password 的 Collection， 这里暂时使用默认值。</li>
<li><strong>password 字段名：</strong> <code>auth.mongo.auth_query.password_field = password</code>。</li>
<li><strong>password 加密方式：</strong> <code>auth.mongo.auth_query.password_hash = plain</code>， password 字段的加密方式，这里选择不加密。</li>
<li><strong>是否打开超级用户查询：</strong> <code>auth.mongo.super_query = off</code>，设置为关闭。</li>
<li><strong>是否打开权限查询：</strong> <code>auth.mongo.acl_query = off</code>，这里我们暂时不打开 Publish 和 Subscribe 的权限控制。</li>
</ul>
<p>然后我们在 MongoDB 插入一条记录，在 MongoDB Shell 中运行：</p>
<pre><code class="javascript language-javascript">use mqtt
db.createCollection("mqtt_user")
db.mqtt_user.insert({username: "test", password: "123456"})
</code></pre>
<p>然后加载 MongoDB 认证插件：</p>
<p><code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_auth_mongo</code></p>
<p>不出意外的话控制台会输出：</p>
<pre><code>Start apps: [emqx_auth_mongo]
Plugin emqx_auth_mongo loaded successfully.
</code></pre>
<p>这个时候如果我们运行 test_mqtt.js，会得到以下输出：
<code>Error: Connection refused: Bad username or password</code></p>
<p>接下来，我们在连接的时候指定刚才存储在 MongoDB 的 username/password: test/123456</p>
<pre><code class="javascript language-javascript">...

var client = mqtt.connect('mqtt://127.0.0.1:1883', {
    username: "test",
    password: "123456"
})

...
</code></pre>
<p>重新运行 test_mqtt.js，如果</p>
<pre><code>return code: 0
</code></pre>
<p>说明基于 MongoDB 的认证方式已经生效了。</p>
<p>如果返回的是<code>Error: Connection refused: Bad username or password</code>，你需要检查：</p>
<ul>
<li>插件的配置文件是否按照课程中的方式进行配置；</li>
<li>MongoDB 插件是否成功加载，可通过运行 <code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins load emqx_auth_mongo</code> 查看；</li>
<li>对应的设备数据是否添加到 MongoDB 对应的 collection 中。</li>
</ul>
<blockquote>
  <p>可以通过运行<code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins list</code>方式查看插件列表，已加载的插件会显示 active=true。</p>
</blockquote>
<h4 id="jwtjsonwebtoken">JWT (JSON Web Token) 认证</h4>
<p>使用 MongoDB 认证插件已经能够满足我们对设备注册的需求，但是我在这里还想再引入一种新的认证方式：JWT 认证。为什么呢？考虑以下两个场景：</p>
<ul>
<li>在浏览器中，使用 WebSocket 方式进行接入时，你需要将接入 Maque IotHub 的 username 和 password 传给前端的 js 的代码，那么在浏览器的 Console 里就可以看见 username 和 password，这非常不安全。如果使用 JWT 认证方式，你只需要将一段有效期很短的 JWT  传给前端的 js 代码，即使泄露了，可以操作的时间窗口也很短。</li>
<li>有时候你需要绕过注册设备这个流程来连接到 Maque IotHub，EMQ X 会在一些内部的系统主题上发布与 Broker 相关的状态信息，比如连接数、消息数等。如果你需要用一个 Client 连接到 Maque IotHub 并订阅这些主题的话，先创建一个 Device 并不是很好的选择，这种情况下，用 JWT 作为一次性的密码为这些系统内部的接入做认证就会非常好。</li>
</ul>
<blockquote>
  <p>JSON Web Token（JWT，读作 [/dʒɒt/]），是一种基于 JSON 的、用于在网络上声明某种主张的令牌（Token），更详细的介绍可以参考 <a href="https://jwt.io/">jwt.io</a></p>
</blockquote>
<p>EMQ X 提供了 <a href="https://github.com/emqx/emqx-auth-jwt">JWT 认证插件</a>来提供 JWT 方式的认证，在<code>&lt;EMQ X 安装目录&gt;/etc/plugins/emqx_auth_jwt.conf</code> 可以对 JWT 认证插件进行配置：</p>
<ul>
<li><strong>JWT Secret:</strong>  <code>auth.jwt.secret = emqxsecret</code>, 这里我们使用默认值，当然在实际生产中你需要使用一个长且复杂的字符串。</li>
<li><strong>是否开启 Claim 验证：</strong> <code>auth.jwt.verify_claims = on</code> 打开 Claim 验证。</li>
<li><strong>Claim 验证字段：</strong> <code>auth.jwt.verify_claims.username = %u</code> 需要验证 Claim 中的 username 字段。</li>
</ul>
<p>下面我们来看下如何使用 JWT 来接入 Maque IotHub：</p>
<pre><code class="javascript language-javascript">...

var jwt = require('jsonwebtoken')
var password = jwt.sign({
    username: "jwt_user",
    exp: Math.floor(Date.now() / 1000) + 10
}, "emqxsecret")
var client = mqtt.connect('mqtt://127.0.0.1:1883', {
    username: "jwt_user",
    password: password
})

...
</code></pre>
<p>在这里我们使用 EMQ X 预设的 JWT Secret 签发了一个有效期为 10 秒的 JWT token 进行连接，重新运行 test_mqtt.js，如果输出为：</p>
<pre><code>return code: 0
</code></pre>
<p>说明基于 JWT 的认证方式已经生效了。</p>
<p>如果返回的是<code>Error: Connection refused: Bad username or password</code>，你需要检查：</p>
<ul>
<li>插件的配置文件是否按照课程中的方式进行配置；</li>
<li>JWT插件是否成功加载，可通过运行 <code>&lt;EMQ X 安装目录&gt;/bin/emqx_ctl plugins list</code> 查看；</li>
<li>是否是使用课程中指定的 payload 来生成 JWT 的。</li>
</ul>
<h4 id="-1">认证链</h4>
<p>我们加载了 MongoDB 和 JWT 两个认证插件，EMQ X 就可以用这两个插件组成的认证链来对接入的 Client 进行认证。简单来说，设备既可以使用存储在 MongoDB 里的 username 和 password，也可以使用 JWT 来接入 EMQ X Broker。</p>
<blockquote>
  <p>EMQ X 在加载一个插件后，会把这个插件的名字写入 <code>&lt;EMQ X 安装目录&gt;/data/loaded_plugins</code>， EMQ X 在每次启动时都会自动加载这个文件里面包含的插件，所以我们只需要手动加载一次这两个插件就可以了。</p>
</blockquote>
<hr />
<p>在这一节我们讨论了 Maque IotHub 中设备的认证方式，以及 EMQ X 是如何支持这些认证方式的。下一节我们会写一些代码，把这些功能集成到 Maque IotHub 的设备注册流程中去。</p>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=sd0730">《从 0 开始搭建 IoT 平台》</a></p>
<p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《从 0 开始搭建 IoT 平台》读者交流群，添加编辑小姐姐微信：「GitChatty6」，回复关键字「214」给编辑小姐姐获取入群资格。</p></div></article>