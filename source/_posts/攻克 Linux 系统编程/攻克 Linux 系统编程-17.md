---
title: 攻克 Linux 系统编程-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>文件系统监控功能在很多系统软件中都有重要的应用，如各种云同步软件、安全防护软件、多种开发工具，以及一些资产监控软件，等等。在本节课中，我们就来讨论一下 Linux 中的<strong>文件系统监控功能</strong>，包括它的<strong>使用方法</strong>和<strong>实现原理</strong>等，主要包括以下几方面内容：</p>
<ul>
<li>文件系统监控概述</li>
<li>相关的系统调用<ul>
<li>创建初始 inotify 对象</li>
<li>控制监控目标和事件</li>
<li>读取发生的事件通知</li>
<li>关闭监控对象</li></ul></li>
<li>底层实现原理</li>
<li>系统限制</li>
</ul>
<h3 id="161">16.1 文件系统监控概述</h3>
<p>文件系统监控指的是，当任意文件或目录的内容或属性发生变化时，以某种形式发出通知的机制。这项机制在很多不同种类的软件中都有广泛的应用，例如下面这几种软件。</p>
<ul>
<li><strong>云同步软件</strong>：很多云同步软件都允许用户设置需要同步到云端的目录，当手动或自动进行同步时，软件会比较指定的目录自上次同步以来发生的变化，从而把变化的部分同步更新到云端上去。</li>
<li><strong>安全防护软件</strong>：很多安全软件会对系统重要目录的修改事件执行监控，比如，当有程序试图向系统目录拷贝新的动态链接库文件时，记录下该事件，或询问管理员执行授权。</li>
<li><strong>多种开发工具</strong>：比如游戏开发用的 Unity 引擎，当工程目录内有任何源码或资源文件在外部被修改，或者有文件被新增或删除，再回到 Unity 的时候，编辑器会重新导入有改动的资源文件，并重新编译发生变化的源码文件。</li>
<li><strong>资产监控软件</strong>：有些公司内部，为了保护重要的数据资产，会在员工的工作电脑上安装监控软件，防止员工把属于公司的数字资产随意拷贝和外传。</li>
</ul>
<p>以上这些软件功能在系统内核提供的文件系统监控的基础上都能比较方便地实现。如果完全依赖应用层进行文件变化的比较，不仅需要消耗更多的存储空间，而且在运行效率上也会大打折扣。</p>
<p>此外，利用文件系统的监控通知功能，还可以<strong>实现一些非常实用的功能</strong>，比如：</p>
<ul>
<li>游戏或 App 的服务器程序，可以监控配置文件的内容，当检测到发生内容更新时动态重新加载，实现服务器配置的不停机更新；</li>
<li>游戏客户端也可以增加重要配置文件和可执行文件的监控功能，实现对部分游戏破解或修改行为的感知和应对；</li>
<li>在对文件 I/O 操作比较密集的应用中，开发者可以用它制作文件访问行为的跟踪记录工具，用于调试验证程序使用外部文件的行为，和识别可能的 I/O 操作瓶颈。</li>
</ul>
<p><strong>在 Linux 中，有两种监控文件系统变化的机制，分别是 dnotify 和 inotify。</strong></p>
<ul>
<li>dnotify 是上一代监控技术，使用信号来通知应用层发生的文件系统事件，而且对每个监控目标都需要建立单独的文件描述符。</li>
<li>inotify 是 dnotify 的改进版本，抛弃了信号通知的方式，并且不再需要打开被监控的目标文件。</li>
</ul>
<p>接下来，我们就来看看在 Linux 系统中，<strong>如何利用 inotify 机制实现文件系统变化的监控。</strong></p>
<h3 id="162">16.2 相关的系统调用</h3>
<p>在 Linux 中，<strong>使用 inotify 实现文件系统监控需要如下三个步骤</strong>：</p>
<ol>
<li>使用 <strong>inotify_init()</strong> 系统调用创建一个代表被监控对象的文件描述符，我们把它叫做 <strong>inotify 对象</strong>；</li>
<li>使用 <strong>inotify_add_watch()</strong> 系统调用向 inotify 对象内添加被监控的目标，并指定对监控目标的监控事件列表；</li>
<li>在 inotify 对象上执行 <strong>read()</strong> 操作，如果监控的目标对象上有任何事件发生，就可以读到一个或多个 <strong>inotify_event</strong> 结构，每个结构都记录了监控目标的一个事件。</li>
</ol>
<p>最后，在监控结束之后，用 <strong>close 系统调用关闭 inotify 对象</strong>就可以了。</p>
<p>下面依次详细介绍每一步中用到的系统调用。</p>
<h4 id="1621inotify">16.2.1 创建初始 inotify 对象</h4>
<p>创建 inotify 对象的系统调用原型为：</p>
<pre><code>int inotify_init(void);
</code></pre>
<p>该系统调用成功后会<strong>返回一个代表被监测对象的文件描述符</strong>，后续的增删监控对象与事件，以及监听事件等操作，都会在这个文件操作符上进行。返回 -1 表示创建失败。</p>
<h4 id="1622">16.2.2 控制监控目标和事件</h4>
<p>创建了上述监控描述符之后，<strong>下一步就要告诉它具体要监控哪些目标</strong>，被监控的目标可以是单个文件，也可以是一个文件夹。添加监控目标的系统调用定义为：</p>
<pre><code>int inotify_add_watch(int fd, const char *pathname, uint32_t mask);
</code></pre>
<p>各参数的释义说明如下。</p>
<ul>
<li>参数 fd 为第一步中创建的代表被监控对象的文件描述符。</li>
<li>pathname 指定添加的监控目标文件或目录，进程需要拥有目标文件的读权限。</li>
<li>mask 参数指定感兴趣的事件，只有在掩码列表内的事件发生时，才会有相应的通知消息产生。mask 的取值包含了文件创建、打开、删除、修改、移动等，详细信息请读者查看该系统调用的帮助手册。</li>
</ul>
<p>如果传入的 pathname 是一个已经添加到监控对象上的条目，它会更新该条目的监控内容为新的 mask 指定的事件。</p>
<p><strong>如果执行成功，该系统调用会返回一个代表该监控目标条目的监控描述符</strong>，应用中需要自行维护一个监控描述符与被监控目标的对应关系列表，以便于在事件通知产生时，用来确定触发通知的对象。</p>
<p>此外，<strong>当需要删除监控项时，也需要用这个监控描述符来指代操作目标</strong>。删除监控项的接口定义如下，第二个参数 wd 就是指代预删除项的监控描述符：</p>
<pre><code>int inotify_rm_watch(int fd, uint32_t wd);
</code></pre>
<blockquote>
  <p>需要注意的是，当把目录添加为监控项时，它并不是递归的，也就是说，当需要监控某个指定文件夹以及其下的所有子文件夹内的变化事件时，需要程序自行递归地遍历该目录下的所有子目录，并把它们都添加为监控项。</p>
</blockquote>
<h4 id="1623">16.2.3 读取发生的事件通知</h4>
<p>设置了监听事件之后，就可以<strong>用通用的 read 系统调用从监控对象上读取发生的事件了</strong>。</p>
<p>默认情况下，<strong>当没有任何感兴趣的事件发生时，程序会阻塞在 read 系统调用上</strong>。也可以把监控对象的文件描述符设置为非阻塞模式，然后使用 I/O 复用技术，在收到目标文件描述符上发生可读事件时，再用 read 系统调用读取接收到的事件通知。</p>
<p><strong>当有感兴趣的文件事件发生时，read 系统调用会读到一块包含一个或多个 inotify_event 结构的数据</strong>，每个结构内都包含一个被通知到的事件。inotify_event 结构的定义为：</p>
<pre><code>struct inotify_event {
  int         wd;         //事件发生的监控项描述符
  uint32_t    mask;       //标志发生的事件的掩码
  uint32_t    cookie;     //与事件有关的 cookie，比如在文件重命名时产生的两个事件会具有相同的 cookie
  uint32_t    len;        //可选的名字字段的长度
  char        name[0];    //可选字段，标记发生事件的文件名、空字符结尾的字符串
};
</code></pre>
<h4 id="1624">16.2.4 关闭监控对象</h4>
<p>当完成对目标的监控之后，在监控对象上<strong>使用通用的 close() 系统调用，内核就会清理掉所有相关的监控项</strong>，并释放监控对象占用的所有资源。</p>
<h3 id="163">16.3 底层实现原理</h3>
<p>不管是单个文件，还是某个目录，在 Linux 的文件系统上，都会对应一个索引节点（inode），所以，不管是在某个目录下新建或修改文件，或者修改某个文件对应的内容，都会执行 inode 信息的更新。所以，<strong>inode 是理想的文件系统事件的监测点。</strong></p>
<p>在 inode 的数据结构中，有两个字段用来记录当前的文件事件观察者：</p>
<pre><code>__u32    i_fsnotify_mask;         //对当前节点感兴趣的所有事件掩码
struct hlist_head    i_fsnotify_marks;    //监控当前节点的所有监控对象，fsnotify_mark 结构的链表  
</code></pre>
<p>在执行 inotify_add_watch() 时，就是在上面的监控列表对象上追加或更新项目。</p>
<p>在 fsnotify_mark 结构中，比较重要的字段包括：</p>
<pre><code>struct fsnotify_mark {
    __u32 mask;         // 感兴趣的事件掩码
    struct fsnotify_group *group;   //指向包含本监控项的监控对象
    union {
        struct fsnotify_inode_mark i;      //索引到相关的 inode
        struct fsnotify_vfsmount_mark m;
    };
    ......
};
</code></pre>
<p>其中的 group 字段，就是在 inotify_init() 创建监控对象时生成的内核数据结构，其中包含了添加到这个监控对象上的所有监控项的列表、阻塞 read() 系统调用的读队列，以及产生的通知事件列表，等等。</p>
<pre><code>struct fsnotify_group {
  struct list_head notification_list;    //要发到用户空间的事件列表
  wait_queue_head_t notification_waitq;    //阻塞 read() 系统调用的等待队列
  unsigned int q_len;    //等待队列长度
  unsigned int max_events; //队列中允许保存的事件的最大数量
 atomic_t num_marks;                //监控目标数量
 struct list_head marks_list;        //监控目标列表
  ......
};
</code></pre>
<p>用一个示例表示上面各个结构间的关系：</p>
<p><img src="https://images.gitbook.cn/144b2ee0-2e00-11e9-8f0e-e3c20e76ed5c" alt="" /></p>
<p>在这个例子中，有两个监控对象，分别创建了对应的内核对象结构：</p>
<ul>
<li>fsnotify_group1</li>
<li>fsnotify_group2</li>
</ul>
<p>其中 fsnotify_group1 只有一个监控目标 inode1，而 fsnotify_group2 有两个监控目标：inode1 和 inode2。</p>
<p>当 inode1 或 inode2 上发生了文件系统事件时，分别沿着绿色和蓝色的箭头就可以定位到需要唤醒并通知的阻塞 read()。</p>
<h3 id="164">16.4 系统限制</h3>
<p>可以看到，某个 inode 被添加为监控目标后，当在该 inode 上发生任何文件事件时，是可以 O(1) 地定位到相关的阻塞 read()，从而向应用层发出事件通知的。</p>
<p>虽然如此，但是我们同时也能看到，每个监控对象和监控目标都需要分配相应的内核数据结构，这会占用内核空间的内存。</p>
<p>为了保护系统，Linux 对系统中的文件系统监控实例的数量，以及每个实例中可以监控的目标的数量都做了限制，<strong>实际的限制值可以在位于目录 /proc/sys/fs/inotify 下的几个文件中查看和设置</strong>，每个文件代表的意义见下说明。</p>
<ul>
<li><p><strong>max_user_instances</strong>：允许用 inotify_init() 创建的监控对象的最大数量，默认为 128。</p></li>
<li><p><strong>max_user_watches</strong>：每个监控对象中，可以用 inotify_add_watch() 添加的监控目标的最大数量，默认为 8192。</p></li>
<li><p><strong>max_queued_events</strong>：每个监控对象上，在调用 read() 之前能够排队的事件的最大数量，超出这个数量的事件会被丢弃，默认值为 16384。</p></li>
</ul>
<p>读者可以根据自己的应用的具体应用场景和需求，来合理调整这些限制值。</p>
<h3 id="165">16.5 总结</h3>
<p>在本节课中，我们<strong>详细介绍了 Linux 中用 inotify 实现文件系统监控的应用场景和详细使用步骤</strong>，并简单<strong>介绍了其在内核中的实现思路</strong>。</p>
<p>通过本节课的学习，希望读者能够掌握这一实用的系统特性，使其能合理地应用在自己正在开发的系统中。</p>
<h3 id="166">16.6 答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
</blockquote></div></article>