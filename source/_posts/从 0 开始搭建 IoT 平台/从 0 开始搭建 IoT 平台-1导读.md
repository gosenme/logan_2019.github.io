---
title: 从 0 开始搭建 IoT 平台-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">导读</h3>
<p>大家好，我是付强，我现在是一家物联网 Startup 的联合创始人兼 CTO，在自己创业之前，我曾经在趋势科技和诺基亚工作过。从 2011 年我在硅谷参与的第一个物联网项目开始算起，到 2015 年开始在物联网方向创业并运营到现在，从 0 到 1，1 到盈利，我在物联网这个行业已经摸爬滚打快 8 年了。</p>
<p>我的上一门课程<a href="https://gitbook.cn/gitchat/column/5be4f4df2c33167c317beb8c">《MQTT 协议快速入门》</a>详细讲解了 MQTT 协议及其各种特性。在课程的交流群中，读者们也提了很多问题，除了关于 MQTT 协议本身的内容以及特性相关的问题之外，还有很多问题是<strong>关于物联网软件设计和架构</strong>方面的，比如：</p>
<ul>
<li>我应该如何管理我的设备和设备的状态？</li>
<li>业务服务端应该怎么接收、处理和存储来自设备的数据？</li>
<li>我的设备数量很多， Broker 端应该怎么架设来确保性能和扩展性？</li>
<li>我的设备处理能力有限，除了使用 MQTT 协议以外，还有没有其他的选择？</li>
<li>……</li>
</ul>
<p>这让我意识到，<strong>单单学会和熟悉 MQTT 协议，离开发和架构一个成熟的物联网产品还是有一段不小的距离</strong>，其实仔细想想，这也没有什么不对的：拿 Web 开发做一个类比，我们只学习 HTTP 协议，就能够开发一个成熟的网站或者基于 Web 的服务吗？ 答案也是否定的。</p>
<p>回想一下我们是怎么学习 Web 开发的。首先我们会了解一下 HTTP 协议，然后选择一个框架，比如 Java 的Spring Boot、 Python 的 Django、Ruby 的 Rails 等。这些框架提供固定的模式，对软件进行了高度的抽象和分层，比如集成了一些 Web 开发的 Good Practice； 你会知道在 Model 层处理业务的逻辑，用 ORM 来进行数据库操作，在 Controller 层处理输入输出和跳转，在 View 层渲染 HTML 页面，这样一个网站和 Web 服务就能够很快被开发出来，除了性能优化的时候，你几乎不用去想 HTTP 协议的细节。</p>
<p>回到物联网开发，抛开设备端的异构性，单说服务端的架构这块，并不像 Web 开发这块有一个 Well Known 的模式、架构或者开发框架。<strong>开发者往往还是需要从协议这一层慢慢往上搭积木</strong>，学习曲线还是比较陡的。</p>
<h4 id="-1">我的经历</h4>
<p>2015 年中的时候我开始在物联网方向创业，我的第一个决定就是先实现一个供业务系统和设备使用的物联网平台。当时阿里云的 IoT 平台已经上线，由于功能性和定制性方面暂时满足不了我们的需求，最后还是决定自行开发。</p>
<p>我们自行开发的物联网平台实现了设备的管理和接入，设备数据的存储和处理，并抽象和封装了基于 MQTT 协议的数据传输，比如设备的数据上报和服务端的指令下发等，提供了业务服务端使用的服务端 API，和设备端使用的设备端 SDK， 业务服务器和设备不再需要处理数据传输和接入等方面的细节，它们甚至不知道数据是通过 MQTT 协议传输的，这一切对业务服务器和设备都是透明的。</p>
<p>这个平台很好地支持了业务服务端和设备端的快速迭代，也支撑着业务从 0 到 1，从 1 再到盈利。同时，我也在密切地关注着各大云服务商（比如阿里云、AWS 等）提供的 IoT 平台，在一些功能上，我们的设计思路和实现逻辑是非常相似的，同时我也会把在云 IoT 平台上的新功能或者更好的实现集成到自研的物联网平台上。</p>
<p><img src="https://images.gitbook.cn/Fv8ie89691W2x7_ENZ6IcS1eILFu" alt="avatar" /></p>
<p>在这个过程中，我踩了很多坑，同时也积累了一些物联网平台在架构和设计模式等方面的经验。在这门课程中，我想把这些物联网平台架构以及设计方面的知识和经验分享给大家，这应该可以<strong>覆盖大家在物联网开发中 80% 的场景和可能遇到的设计和架构问题</strong>。</p>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=kpc0730">《从 0 开始搭建 IoT 平台》</a></p>
<h4 id="-2">如何学习</h4>
<p>2019 年的阿里云 IoT 平台功能已经非常强大了，在本门课程中，<strong>我们将使用开源的组件，从第一行代码开始，一步步地实现一个具有阿里云 IoT 平台大部分的功能的"物联网平台"</strong>，在这个过程中穿插讲解在物联网平台开发中可以用到的模式和架构的选择， Pros and Cons，以及一些 Best Practice 等。与<a href="https://gitbook.cn/gitchat/column/5be4f4df2c33167c317beb8c">《MQTT 协议快速入门》</a>侧重协议内容和理论不同，本门课程包含大量的实战代码，毕竟代码是程序员之间交流的最好语言。</p>
<blockquote>
  <p>这里给这个"物联网平台"起了一个 Codename: Maque IotHub，简称 IotHub。</p>
</blockquote>
<p>本课程属于实战性课程，所以不会再详细地讲解 MQTT 协议的概念和特性了，<strong>预先学习和熟悉 MQTT 协议的基本概念和特性，对阅读本课程有非常大的帮助</strong>。你可以访问 <a href="http://mqtt.org/">mqtt.org</a> 查阅协议的文档，也可以通过阅读我的<a href="https://gitbook.cn/gitchat/column/5be4f4df2c33167c317beb8c">《MQTT 协议快速入门》</a>来进行快速学习。</p>
<h3 id="-3">课程特色</h3>
<p>目前物联网开发的的实战课程，特别是成体系的实战课程是很少的，本课程涵盖了从物联网平台到设备端开发的大量场景和设计模式，并不像其他教程那样只是罗列知识点。本课程各节内容之间就像搭积木一样关联性很强，从第一行代码开始搭建一个物联网平台，轻理论而重实战，专注于你无法在互联网上找到参考的实战内容，干货十足。</p>
<ul>
<li>大量实战代码，从第一行开始手把手讲解</li>
<li>来自实际运营的物联网项目的开发/架构经验</li>
<li>覆盖 80% 物联网开发场景</li>
<li>在互联网其他地方找不到的原创课程</li>
</ul>
<h3 id="-4">课程介绍</h3>
<h4 id="fontcolororangemqttfont"><font color=orange>开篇词：开发物联网应用，光会 MQTT 还不够</font></h4>
<h4 id="fontcolororangemaqueiothubfont"><font color=orange>附录：如何运行 Maque IotHub</font></h4>
<h4 id="fontcolororange1119font"><font color=orange>第一部分（第 1-1 ～ 1-9 课）：设备生命周期管理</font></h4>
<p>作为课程的第一部分，我们会<strong>设计和开发 IotHub 的最基础功能</strong>，对设备的创建、接入、 上线/下线、 禁用/恢复和删除的整个生命周期进行管理，引入设备的发布订阅权限管理。同时也会<strong>把服务端代码和设备端代码的框架搭建起来</strong>，便于后续的迭代开发。这部分最后也会讲解<strong>如何横向和纵向地扩展 EMQ X</strong>。</p>
<h4 id="fontcolororange2126font"><font color=orange>第二部分（第 2-1 ～ 2-6 课）：上行数据处理</font></h4>
<p>在课程的第二部分，我们会<strong>设计和实现 IotHub 的上行数据处理功能</strong>，在这部分我们会学习 EMQ X 的 Hook 机制，以及它如何为 IotHub 的开发带来便利性，同时也会第一次对 IotHub 中的 MQTT 主题名进行规划，把 MQTT 的 Broker-Client 模式转换为 Server-Client 模式。</p>
<h4 id="fontcolororange3135font"><font color=orange>第三部分（第 3-1 ～ 3-5 课）：下行数据处理</font></h4>
<p>在课程的第三部分，我们会<strong>设计和实现 IotHub 的指令下发功能</strong>，在这部分我们会学习使用 EMQ X 的监控管理 API，并对指令下发的主题进行规划，实现可靠的指令下发流程。</p>
<h4 id="fontcolororange41415font"><font color=orange>第四部分（第 4-1 ～ 4-15 课）：进一步抽象</font></h4>
<p>在第四部分的课程中，我们会利用第二部分和第三部分实现的上行和下行通道，来<strong>实现物联网应用中一些常见的功能</strong>，比如 OTA 升级、设备分组等。我们会学习如果将这些功能抽象出来放入 IotHub 中，使多个物联网应用可以通过 IotHub 复用这些功能。最后我们还会学习和实现在各大云服务商提供的 IoT 平台中非常常见的<strong>设备影子</strong>功能。</p>
<h4 id="fontcolororange5156emqxfont"><font color=orange>第五部分（第 5-1 ～ 5-6 课）：扩展 EMQ X</font></h4>
<p>在前面的课程中，我们使用大量的 EMQ X 自带插件功能来完善 IotHub， 在这部分课程中，我们将<strong>学习如何编写一个 EMQ X 插件</strong>。通过这部分的学习，读者将会掌握根据自己的业务逻辑来扩展 EMQ X 的能力。</p>
<h4 id="fontcolororange6162coapfont"><font color=orange>第六部分（第 6-1 ～ 6-2 课）：CoAP</font></h4>
<p>在课程的最后一部分，我们会将目光暂时从 MQTT 上移开，讨论 MQTT 在某些场景下的缺陷，并<strong>学习另外一种物联网协议 CoAP</strong>。最后我们会将 CoAP 无缝地接入现有 IotHub 的设备体系。</p>
<h3 id="-5">适合阅读的人群</h3>
<p>本课程适合以下人群阅读：</p>
<ul>
<li>物联网应用开发者</li>
<li>物联网架构师</li>
<li>物联网平台开发者</li>
</ul>
<p><strong><font color=orange>推荐阅读 👉</font></strong><a href="http://gitbook.cn/m/mazi/comp/column?columnId=5d3a7c335cb084142168b3fc&giftCode=rNnOR4vZV&utm_source=kpc0730">《从 0 开始搭建 IoT 平台》</a></p>
<h3 id="-6">课程寄语</h3>
<p>在我的另一篇达人课《<a href="https://gitbook.cn/gitchat/column/5be4f4df2c33167c317beb8c">MQTT 协议快速入门</a>》，我尝试着用一门课来解答大家在物联网应用设计和开发上遇到的问题，在交流中发现，大家的问题不只局限在协议上。这是也促成我编写这篇课程的原因之一。</p>
<p>物联网应用开发不像 Web 开发那样有固定的模式和框架可以学习，本课程实现阿里云 Iothub 的部分功能，并结合我在设计和实现一个已上线运行多年的物联网平台的经验，来阐述在物联网应用中常用的设计模式和思路，目的也是希望大家在学习本课程之后，可以<strong>少走点弯路、少踩点坑</strong>。如果你不需要实现一个物联网平台（比如直接使用云服务商提供的物联网平台）也没关系，<strong>这门课所体现的架构和思路也能帮助你更好地设计物联网应用</strong>。</p>
<p>我希望读者在学习完本课的内容后，能够将学到的设计思路和模式运用到实际工作中去，希望本课程能够解答你在物联网应用开发中能遇到大部分设计和实现的问题。毕竟 5G 时代已经来临，物联网的发展势头会越来越快。</p>
<h3 id="-7">学完后的收获</h3>
<ul>
<li>熟悉物联网应用的<strong>常用架构和设计模式</strong></li>
<li>学会<strong>独立设计和开发可以用于支撑多个物联网应用的物联网平台</strong></li>
<li>学会<strong>使用和编写 EMQ X 的插件</strong></li>
<li><strong>获得一套完整的、可运行的物联网平台代码</strong>，包括服务端和设备端 SDK</li>
</ul></div></article>