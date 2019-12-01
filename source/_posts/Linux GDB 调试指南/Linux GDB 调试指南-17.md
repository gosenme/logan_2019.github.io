---
title: Linux GDB 调试指南-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>接着上一课的内容继续分析。</p>
<h3 id="fdfdepfd">侦听 fd 与客户端 fd 是如何挂载到 epfd 上去的</h3>
<p>同样的方式，要把一个 fd 挂载到 EPFD 上去，需要调用系统 API epoll_ctl ，搜索一下这个函数名。在文件 ae_epoll.c 中我们找到 aeApiAddEvent 函数：</p>
<pre><code>static int aeApiAddEvent(aeEventLoop *eventLoop, int fd, int mask) {
    aeApiState *state = eventLoop-&gt;apidata;
    struct epoll_event ee = {0}; /* avoid valgrind warning */
    /* If the fd was already monitored for some event, we need a MOD
     * operation. Otherwise we need an ADD operation. */
    int op = eventLoop-&gt;events[fd].mask == AE_NONE ?
            EPOLL_CTL_ADD : EPOLL_CTL_MOD;

    ee.events = 0;
    mask |= eventLoop-&gt;events[fd].mask; /* Merge old events */
    if (mask &amp; AE_READABLE) ee.events |= EPOLLIN;
    if (mask &amp; AE_WRITABLE) ee.events |= EPOLLOUT;
    ee.data.fd = fd;
    if (epoll_ctl(state-&gt;epfd,op,fd,&amp;ee) == -1) return -1;
    return 0;
}
</code></pre>
<p>当把一个 fd 绑定到 EPFD 上去的时候，先从 eventLoop（ aeEventLoop类型 ）中寻找是否存在已关注的事件类型，如果已经有了，说明使用 epoll_ctl 是更改已绑定的 fd 事件类型（ EPOLL_CTL_MOD ），否则就是添加 fd 到 EPFD 上。</p>
<p>在 aeApiAddEvent 加个断点，再重启下 redis-server。触发断点后的调用堆栈如下：</p>
<pre><code>#0  aeCreateFileEvent (eventLoop=0x7ffff083a0a0, fd=15, mask=1, proc=0x437f50 &lt;acceptTcpHandler&gt;, clientData=0x0) at ae.c:145
#1  0x000000000042f83b in initServer () at server.c:1927
#2  0x0000000000423803 in main (argc=1, argv=0x7fffffffe588) at server.c:3857
</code></pre>
<p>同样在 initServer 函数中，结合上文分析的侦听 fd 的创建过程，去掉无关代码，抽出这个函数的主脉络得到如下伪代码：</p>
<pre><code>void initServer(void) {

    //记录程序进程 ID   
    server.pid = getpid();

    //创建程序的 aeEventLoop 对象和 epfd 对象
    server.el = aeCreateEventLoop(server.maxclients+CONFIG_FDSET_INCR);

    //创建侦听 fd
    listenToPort(server.port,server.ipfd,&amp;server.ipfd_count) == C_ERR)

    //创建 Redis 的定时器，用于执行定时任务 cron
    /* Create the timer callback, this is our way to process many background
     * operations incrementally, like clients timeout, eviction of unaccessed
     * expired keys and so forth. */
    aeCreateTimeEvent(server.el, 1, serverCron, NULL, NULL) == AE_ERR

    //将侦听 fd 绑定到 epfd 上去
    /* Create an event handler for accepting new connections in TCP and Unix
     * domain sockets. */
     aeCreateFileEvent(server.el, server.ipfd[j], AE_READABLE, acceptTcpHandler,NULL) == AE_ERR

    //创建一个管道，用于在需要时去唤醒 epoll_wait 挂起的整个 EventLoop
    /* Register a readable event for the pipe used to awake the event loop
     * when a blocked client in a module needs attention. */
    aeCreateFileEvent(server.el, server.module_blocked_pipe[0], AE_READABLE, moduleBlockedClientPipeReadable,NULL) == AE_ERR)
}
</code></pre>
<blockquote>
  <p>注意：这里所说的“主脉络”是指我们关心的网络通信的主脉络，不代表这个函数中其他代码就不是主要的。</p>
</blockquote>
<p>如何验证这个断点处挂载到 EPFD 上的 fd 就是侦听 fd 呢？很简单，创建侦听 fd 时，用 GDB 记录下这个 fd 的值。例如，当我的电脑某次运行时，侦听 fd 的值是 15 。如下图（ 调试工具用的是 CGDB ）：</p>
<p><img src="https://images.gitbook.cn/ef8ec9e0-f209-11e8-b37f-7bcfd20d5d3a"  width = "70%" /></p>
<p>然后在运行程序至绑定 fd 的地方，确认一下绑定到 EPFD 上的 fd 值：</p>
<p><img src="https://images.gitbook.cn/0fbd7770-f20a-11e8-a886-5157ca7834b5"  width = "70%" /></p>
<p>这里的 fd 值也是 15 ，说明绑定的 fd 是侦听 fd 。当然在绑定侦听 fd 时，同时也指定了只关注可读事件，并设置事件回调函数为 acceptTcpHandler 。对于侦听 fd ，一般只要关注可读事件就可以了，当触发可读事件，说明有新的连接到来。</p>
<pre><code>aeCreateFileEvent(server.el, server.ipfd[j], AE_READABLE, acceptTcpHandler,NULL) == AE_ERR
</code></pre>
<p>acceptTcpHandler 函数定义如下（ 位于文件 networking.c 中 ）：</p>
<pre><code>void acceptTcpHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    int cport, cfd, max = MAX_ACCEPTS_PER_CALL;
    char cip[NET_IP_STR_LEN];
    UNUSED(el);
    UNUSED(mask);
    UNUSED(privdata);

    while(max--) {
        cfd = anetTcpAccept(server.neterr, fd, cip, sizeof(cip), &amp;cport);
        if (cfd == ANET_ERR) {
            if (errno != EWOULDBLOCK)
                serverLog(LL_WARNING,
                    "Accepting client connection: %s", server.neterr);
            return;
        }
        serverLog(LL_VERBOSE,"Accepted %s:%d", cip, cport);
        acceptCommonHandler(cfd,0,cip);
    }
}
</code></pre>
<p>anetTcpAccept 函数中调用的就是我们上面说的 anetGenericAccept 函数了。</p>
<pre><code>int anetTcpAccept(char *err, int s, char *ip, size_t ip_len, int *port) {
    int fd;
    struct sockaddr_storage sa;
    socklen_t salen = sizeof(sa);
    if ((fd = anetGenericAccept(err,s,(struct sockaddr*)&amp;sa,&amp;salen)) == -1)
        return ANET_ERR;

    if (sa.ss_family == AF_INET) {
        struct sockaddr_in *s = (struct sockaddr_in *)&amp;sa;
        if (ip) inet_ntop(AF_INET,(void*)&amp;(s-&gt;sin_addr),ip,ip_len);
        if (port) *port = ntohs(s-&gt;sin_port);
    } else {
        struct sockaddr_in6 *s = (struct sockaddr_in6 *)&amp;sa;
        if (ip) inet_ntop(AF_INET6,(void*)&amp;(s-&gt;sin6_addr),ip,ip_len);
        if (port) *port = ntohs(s-&gt;sin6_port);
    }
    return fd;
}
</code></pre>
<p>至此，这段流程总算连起来了，在 acceptTcpHandler 上加个断点，然后重新运行一下 redis-server ，再开个 redis-cli 去连接 redis-server。看看是否能触发该断点，如果能触发该断点，说明我们的分析是正确的。</p>
<p>经验证，确实触发了该断点。</p>
<p><img src="https://images.gitbook.cn/6aa23450-f20a-11e8-a886-5157ca7834b5"  width = "70%" /></p>
<p>在 acceptTcpHandler 中成功接受新连接后，产生客户端 fd ，然后调用 acceptCommonHandler 函数，在该函数中调用 createClient 函数，在 createClient 函数中先将客户端 fd 设置成非阻塞的，然后将该 fd 关联到 EPFD 上去，同时记录到整个程序的 aeEventLoop 对象上。</p>
<blockquote>
  <p>注意：这里客户端 fd 绑定到 EPFD 上时也只关注可读事件。将无关的代码去掉，然后抽出我们关注的部分，整理后如下（ 位于 networking.c 文件中 ）：</p>
</blockquote>
<pre><code>client *createClient(int fd) {
    //将客户端 fd 设置成非阻塞的
    anetNonBlock(NULL,fd);
    //启用 tcp NoDelay 选项
    anetEnableTcpNoDelay(NULL,fd);
    //根据配置，决定是否启动 tcpkeepalive 选项
    if (server.tcpkeepalive)
        anetKeepAlive(NULL,fd,server.tcpkeepalive);
    //将客户端 fd 绑定到 epfd，同时记录到 aeEventLoop 上，关注的事件为 AE_READABLE，回调函数为
    //readQueryFromClient
    aeCreateFileEvent(server.el,fd,AE_READABLE, readQueryFromClient, c) == AE_ERR

    return c;
}
</code></pre>
<h3 id="fd">如何处理 fd 可读事件</h3>
<p>客户端 fd 触发可读事件后，回调函数是 readQueryFromClient，该函数实现如下（ 位于 networking.c 文件中）：</p>
<pre><code>void readQueryFromClient(aeEventLoop *el, int fd, void *privdata, int mask) {
    client *c = (client*) privdata;
    int nread, readlen;
    size_t qblen;
    UNUSED(el);
    UNUSED(mask);

    readlen = PROTO_IOBUF_LEN;
    /* If this is a multi bulk request, and we are processing a bulk reply
     * that is large enough, try to maximize the probability that the query
     * buffer contains exactly the SDS string representing the object, even
     * at the risk of requiring more read(2) calls. This way the function
     * processMultiBulkBuffer() can avoid copying buffers to create the
     * Redis Object representing the argument. */
    if (c-&gt;reqtype == PROTO_REQ_MULTIBULK &amp;&amp; c-&gt;multibulklen &amp;&amp; c-&gt;bulklen != -1
        &amp;&amp; c-&gt;bulklen &gt;= PROTO_MBULK_BIG_ARG)
    {
        int remaining = (unsigned)(c-&gt;bulklen+2)-sdslen(c-&gt;querybuf);

        if (remaining &lt; readlen) readlen = remaining;
    }

    qblen = sdslen(c-&gt;querybuf);
    if (c-&gt;querybuf_peak &lt; qblen) c-&gt;querybuf_peak = qblen;
    c-&gt;querybuf = sdsMakeRoomFor(c-&gt;querybuf, readlen);
    nread = read(fd, c-&gt;querybuf+qblen, readlen);
    if (nread == -1) {
        if (errno == EAGAIN) {
            return;
        } else {
            serverLog(LL_VERBOSE, "Reading from client: %s",strerror(errno));
            freeClient(c);
            return;
        }
    } else if (nread == 0) {
        serverLog(LL_VERBOSE, "Client closed connection");
        freeClient(c);
        return;
    } else if (c-&gt;flags &amp; CLIENT_MASTER) {
        /* Append the query buffer to the pending (not applied) buffer
         * of the master. We'll use this buffer later in order to have a
         * copy of the string applied by the last command executed. */
        c-&gt;pending_querybuf = sdscatlen(c-&gt;pending_querybuf,
                                        c-&gt;querybuf+qblen,nread);
    }

    sdsIncrLen(c-&gt;querybuf,nread);
    c-&gt;lastinteraction = server.unixtime;
    if (c-&gt;flags &amp; CLIENT_MASTER) c-&gt;read_reploff += nread;
    server.stat_net_input_bytes += nread;
    if (sdslen(c-&gt;querybuf) &gt; server.client_max_querybuf_len) {
        sds ci = catClientInfoString(sdsempty(),c), bytes = sdsempty();

        bytes = sdscatrepr(bytes,c-&gt;querybuf,64);
        serverLog(LL_WARNING,"Closing client that reached max query buffer length: %s (qbuf initial bytes: %s)", ci, bytes);
        sdsfree(ci);
        sdsfree(bytes);
        freeClient(c);
        return;
    }

    /* Time to process the buffer. If the client is a master we need to
     * compute the difference between the applied offset before and after
     * processing the buffer, to understand how much of the replication stream
     * was actually applied to the master state: this quantity, and its
     * corresponding part of the replication stream, will be propagated to
     * the sub-slaves and to the replication backlog. */
    if (!(c-&gt;flags &amp; CLIENT_MASTER)) {
        processInputBuffer(c);
    } else {
        size_t prev_offset = c-&gt;reploff;
        processInputBuffer(c);
        size_t applied = c-&gt;reploff - prev_offset;
        if (applied) {
            replicationFeedSlavesFromMasterStream(server.slaves,
                    c-&gt;pending_querybuf, applied);
            sdsrange(c-&gt;pending_querybuf,applied,-1);
        }
    }
}
</code></pre>
<p>给这个函数加个断点，然后重新运行下 redis-server ，再启动一个客户端，然后尝试给服务器发送一个命令“set hello world”。但是在我们实际调试的时候会发现，只要 redis-cli 一连接成功，GDB 就触发该断点，此时并没有发送我们预想的命令。单步调试 readQueryFromClient 函数，将收到的数据打印出来，得到如下字符串：</p>
<pre><code>(gdb) p c-&gt;querybuf 
$8 = (sds) 0x7ffff09b8685 "*1\r\n$7\r\nCOMMAND\r\n"
</code></pre>
<p>c → querybuf 是什么呢？这里 c 的类型是 client 结构体，它是上文中连接接收成功后产生的新客户端 fd 绑定回调函数时产生的、并传递给 readQueryFromClient 函数的参数。可以在 server.h 中找到它的定义：</p>
<pre><code>* With multiplexing we need to take per-client state.
 * Clients are taken in a linked list. */
typedef struct client {
    uint64_t id;            /* Client incremental unique ID. */
    int fd;                 /* Client socket. */
    redisDb *db;            /* Pointer to currently SELECTed DB. */
    robj *name;             /* As set by CLIENT SETNAME. */
    sds querybuf;           /* Buffer we use to accumulate client queries. */
    //省略掉部分字段
} client;
</code></pre>
<p>client 实际上是存储每个客户端连接信息的对象，其 fd 字段就是当前连接的 fd，querybuf 字段就是当前连接的接收缓冲区，也就是说每个新客户端连接都会产生这样一个对象。从 fd 上收取数据后就存储在这个 querybuf 字段中。</p>
<p>贴一下完整的 createClient 函数的代码：</p>
<pre><code>client *createClient(int fd) {
    client *c = zmalloc(sizeof(client));

    /* passing -1 as fd it is possible to create a non connected client.
     * This is useful since all the commands needs to be executed
     * in the context of a client. When commands are executed in other
     * contexts (for instance a Lua script) we need a non connected client. */
    if (fd != -1) {
        anetNonBlock(NULL,fd);
        anetEnableTcpNoDelay(NULL,fd);
        if (server.tcpkeepalive)
            anetKeepAlive(NULL,fd,server.tcpkeepalive);
        if (aeCreateFileEvent(server.el,fd,AE_READABLE,
            readQueryFromClient, c) == AE_ERR)
        {
            close(fd);
            zfree(c);
            return NULL;
        }
    }

    selectDb(c,0);
    uint64_t client_id;
    atomicGetIncr(server.next_client_id,client_id,1);
    c-&gt;id = client_id;
    c-&gt;fd = fd;
    c-&gt;name = NULL;
    c-&gt;bufpos = 0;
    c-&gt;querybuf = sdsempty();
    c-&gt;pending_querybuf = sdsempty();
    c-&gt;querybuf_peak = 0;
    c-&gt;reqtype = 0;
    c-&gt;argc = 0;
    c-&gt;argv = NULL;
    c-&gt;cmd = c-&gt;lastcmd = NULL;
    c-&gt;multibulklen = 0;
    c-&gt;bulklen = -1;
    c-&gt;sentlen = 0;
    c-&gt;flags = 0;
    c-&gt;ctime = c-&gt;lastinteraction = server.unixtime;
    c-&gt;authenticated = 0;
    c-&gt;replstate = REPL_STATE_NONE;
    c-&gt;repl_put_online_on_ack = 0;
    c-&gt;reploff = 0;
    c-&gt;read_reploff = 0;
    c-&gt;repl_ack_off = 0;
    c-&gt;repl_ack_time = 0;
    c-&gt;slave_listening_port = 0;
    c-&gt;slave_ip[0] = '\0';
    c-&gt;slave_capa = SLAVE_CAPA_NONE;
    c-&gt;reply = listCreate();
    c-&gt;reply_bytes = 0;
    c-&gt;obuf_soft_limit_reached_time = 0;
    listSetFreeMethod(c-&gt;reply,freeClientReplyValue);
    listSetDupMethod(c-&gt;reply,dupClientReplyValue);
    c-&gt;btype = BLOCKED_NONE;
    c-&gt;bpop.timeout = 0;
    c-&gt;bpop.keys = dictCreate(&amp;objectKeyPointerValueDictType,NULL);
    c-&gt;bpop.target = NULL;
    c-&gt;bpop.numreplicas = 0;
    c-&gt;bpop.reploffset = 0;
    c-&gt;woff = 0;
    c-&gt;watched_keys = listCreate();
    c-&gt;pubsub_channels = dictCreate(&amp;objectKeyPointerValueDictType,NULL);
    c-&gt;pubsub_patterns = listCreate();
    c-&gt;peerid = NULL;
    listSetFreeMethod(c-&gt;pubsub_patterns,decrRefCountVoid);
    listSetMatchMethod(c-&gt;pubsub_patterns,listMatchObjects);
    if (fd != -1) listAddNodeTail(server.clients,c);
    initClientMultiState(c);
    return c;
}
</code></pre></div></article>