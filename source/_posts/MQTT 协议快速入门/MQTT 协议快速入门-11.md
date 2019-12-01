---
title: MQTT 协议快速入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在接下来的课程里，我们来完成一个 IoT+AI 的实战项目。本节课核心内容：</p>
<ul>
<li>如何在 MQTT 里面传输大文件</li>
<li>消息去重</li>
<li>消息数据编码</li>
<li>实现 Android 发布端</li>
<li>发布识别结果</li>
</ul>
<p>在我的另一门达人课<a href="https://gitbook.cn/gitchat/column/59f1a77a9343b255e38edd78">《物体识别：TensorFlow on Android》</a>里， 我们实现了一个可以识别出图片里的物体并标注其位置的 Android 应用。在这里我们可以把运行该 App 的 Android 设备当做一个物联网终端，它在完成识别之后，就会把图片和识别结果发布出去。用户可以在 Web 端查看结果，也就是打开浏览器，上面会实时显示来自该终端的识别结果和图片，这就是我们要做的。</p>
<p>这个功能并不复杂，而在这个架构上稍加扩展，一个成熟的应用就可以实现了。比如一个网络摄像头，当它在抓拍的照片里面识别到人的时候，可以把结果图片实时发布到云端的监控。</p>
<p>实际上运行 Android 的物联网设备已经很常见了，有兴趣的同学可以了解一下 Google 的 Android Things。</p>
<p>在开始 Coding 之前，我们先来讨论几个设计问题。</p>
<h3 id="101mqtt">10.1 如何在 MQTT 里面传输大文件</h3>
<p>我们前面提到过，一个 MQTT 数据包最大可以达到约 256M，所以对于传输图片的需求，最简单直接的方式就把图片数据直接包含在 PUBLISH 包里面进行传输。</p>
<p>还有一种更好的做法。在发布数据之前，先把图片上传到云端的某个图片存储里，然后 PUBLISH 包里面只包含图片的 URL，当订阅端接收这个数据之后，它再通过图片的 URL 来获取图片。这样的做法较前面有几个优点。</p>
<ul>
<li><strong>对订阅端来说，它可以在有需要的时候再下载图片数据</strong>，而第一种做法，每次都必须接收图片的全部数据。</li>
<li><strong>这种做法可以处理文件大于 256M 的情况</strong>，而第一种做法，必须把文件分割为多个 PUBLISH 包，订阅端接收后再重新组合，非常麻烦。</li>
<li><strong>节省带宽</strong>，如果图片数据直接放在 PUBLISH 包中，那么 Broker 就需要预留相对大的带宽。目前在中国，带宽还是比较贵的。PUBLISH 包中只包含 URL 的话，每一个 PUBLISH 包都很小，那么 Broker 的带宽需求就很小了。虽然上传图片也需要带宽，但是如果你使用云存储，比如阿里云 OSS、七牛等，从它们那里购买上传和下载图片的带宽要便宜很多。同时，这些云存储服务商建设了很多 CDN，通常上传和下载图片比直接通过 PUBLISH 包传输要快一些。</li>
<li><strong>节约存储和处理能力</strong>，因为 Broker 需要存储 Client 未接收的消息，所以如果图片包含在 PUBLISH 包里面，Broker 需要预留相当的存储空间；而使用云存储的话，存储的成本比自建要便宜得多。</li>
</ul>
<p>在这个实战项目里，我们用第二种方式来传输图片，使用<a href="https://www.qiniu.com/">七牛</a>作为图片存储。</p>
<h3 id="102">10.2 消息去重</h3>
<p>为了兼顾效率和可靠性，我们使用 QoS1 来传输消息。QoS1 有一个问题，就是可能会收到重复的消息，所以需要在应用里面手动对消息进行去重。</p>
<p>我们可以在消息数据里面带一个唯一的消息 ID，通常是 UUID。订阅端需要保存已接收消息的 ID，当收到新消息的时候，通过消息的 ID 来判断是否是重复的消息，如果是，则丢弃。</p>
<h3 id="103">10.3 消息数据编码</h3>
<p>我们需要对消息数据进行编码，方便订阅端对数据进行解析。通常可以使用 JSON 格式，如果设备的计算和存储能力有限，也可以使用 Protocol Buffer 这类对内存消耗更少、解析更快的编码方式。</p>
<p>这个项目里面，我们使用 JSON 作为数据编码格式。一个消息数据格式如下：</p>
<pre><code class="json language-json">{'id': &lt;消息 ID&gt;, timestamp:&lt;UNIX 时间戳&gt;, image_url: &lt;图片&gt;, objects:[图片中物体名称的数组]}
</code></pre>
<p>接下来我们先来实现数据的发布端。</p>
<h3 id="104android">10.4 实现 Android 发布端</h3>
<h4 id="1041broker">10.4.1 连接到 Broker</h4>
<p>首先包含 MQTT Android 库的依赖：</p>
<pre><code class="gradle language-gradle">repositories {
    maven {
        url "https://repo.eclipse.org/content/repositories/paho-snapshots/"
    }
}


dependencies {
    compile 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.1.0'
}
</code></pre>
<p>接下来连接到 Broker，注意这里使用 AndriodID 作为 Client Identifier 的一部分，保证 Client Identifier 不会冲突：</p>
<pre><code class="java language-java">String clientId = "client_" + Settings.Secure.getString(getApplicationContext().getContentResolver(), Settings.Secure.ANDROID_ID);
            mqttAsyncClient = new MqttAsyncClient("tcp://iot.eclipse.org:1883", clientId, 
                    new MqttDefaultFilePersistence(getApplicationContext().getApplicationInfo().dataDir));
            mqttAsyncClient.connect(null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(), "已连接到 Broker", Toast.LENGTH_LONG).show();
                        }
                    });
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, final Throwable exception) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(), "连接 Broker 失败:" + exception.getMessage(), Toast.LENGTH_LONG).show();
                        }
                    });
                }
            });
</code></pre>
<h4 id="1042">10.4.2 上传图片</h4>
<p>首先包含七牛安卓库的依赖：</p>
<pre><code>compile 'com.qiniu:qiniu-android-sdk:7.3.+'
</code></pre>
<p>然后上传图片：</p>
<pre><code class="java language-java">uploadManager.put(getBytesFromBitmap(image), null, upToken, new UpCompletionHandler() {
            @Override
            public void complete(String key, ResponseInfo info, JSONObject response) {
                 if(info.isOK()){
                    //上传成功以后 PUBLISH
                 }
            }
        }, null);
</code></pre>
<h3 id="105">10.5 发布识别结果</h3>
<p>最后，在图片上传成功以后，将识别结果发布到“front_door/detection/objects”这个主题：</p>
<pre><code class="java language-java">JSONObject jsonMesssage = new JSONObject();
                         jsonMesssage.put("id", randomUUID());
                         jsonMesssage.put("timestamp", timestamp);
                         jsonMesssage.put("objects", objects);
                         jsonMesssage.put("image_url", "http://" + QINIU_DOMAIN + "\\" + response.getString("key"));
                         mqttAsyncClient.publish("front_door/detection/objects", new MqttMessage(jsonMesssage.toString().getBytes()));
</code></pre>
<h3 id="106">10.6 小结</h3>
<p>本节课我们完成了 Android 发布端的代码，你可以在 <a href="https://github.com/sufish/object_detection_mqtt">https://github.com/sufish/object_detection_mqtt</a> 找到全部代码。</p>
<p><strong>相关资料</strong></p>
<ul>
<li><a href="https://gitbook.cn/gitchat/column/59f1a77a9343b255e38edd78">《物体识别：TensorFlow on Android》</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<p>GitChat 编辑团队组织了一个《MQTT 协议快速入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「266」给<strong>小助手-伽利略</strong>获取入群资格。</p></div></article>