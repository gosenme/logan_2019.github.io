---
title: Java 面试全解析：核心知识点与典型面试题-20
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">线程池介绍</h3>
<p>线程池（Thread Pool）：把一个或多个线程通过统一的方式进行调度和重复使用的技术，避免了因为线程过多而带来使用上的开销。</p>
<h4 id="-1">为什么要使用线程池？</h4>
<ul>
<li>可重复使用已有线程，避免对象创建、消亡和过度切换的性能开销。</li>
<li>避免创建大量同类线程所导致的资源过度竞争和内存溢出的问题。</li>
<li>支持更多功能，比如延迟任务线程池（newScheduledThreadPool）和缓存线程池（newCachedThreadPool）等。</li>
</ul>
<h3 id="-2">线程池使用</h3>
<p>创建线程池有两种方式：ThreadPoolExecutor 和 Executors，其中 Executors 又可以创建 6 种不同的线程池类型，会在下节讲，本节重点来看看 ThreadPoolExecutor 的使用。</p>
<h4 id="threadpoolexecutor">ThreadPoolExecutor 的使用</h4>
<p>线程池使用代码如下：</p>
<pre><code class="java language-java">ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 10, 10L, TimeUnit.SECONDS, new LinkedBlockingQueue(100));
threadPoolExecutor.execute(new Runnable() {
    @Override
    public void run() {
        // 执行线程池
        System.out.println("Hello, Java.");
    }
});
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>Hello, Java.</p>
</blockquote>
<h4 id="threadpoolexecutor-1">ThreadPoolExecutor 参数说明</h4>
<p>ThreadPoolExecutor 构造方法有以下四个，如下图所示：</p>
<p><img src="https://images.gitbook.cn/ce89fc40-d2d4-11e9-b6c4-07be7ef1cd0f" alt="enter image description here" /></p>
<p>其中最后一个构造方法有 7 个构造参数，包含了前三个方法的构造参数，这 7 个参数名称如下所示：</p>
<pre><code class="java language-java">public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue&lt;Runnable&gt; workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler) {
    //...
}
</code></pre>
<p>其代表的含义如下：</p>
<h5 id="corepoolsize">① corePoolSize</h5>
<p>线程池中的核心线程数，默认情况下核心线程一直存活在线程池中，如果将 ThreadPoolExecutor 的 allowCoreThreadTimeOut 属性设为 true，如果线程池一直闲置并超过了 keepAliveTime 所指定的时间，核心线程就会被终止。</p>
<h5 id="maximumpoolsize">② maximumPoolSize</h5>
<p>线程池中最大线程数，如果活动的线程达到这个数值以后，后续的新任务将会被阻塞（放入任务队列）。</p>
<h5 id="keepalivetime">③ keepAliveTime</h5>
<p>线程池的闲置超时时间，默认情况下对非核心线程生效，如果闲置时间超过这个时间，非核心线程就会被回收。如果 ThreadPoolExecutor 的 allowCoreThreadTimeOut 设为 true 的时候，核心线程如果超过闲置时长也会被回收。</p>
<h5 id="unit">④ unit</h5>
<p>配合 keepAliveTime 使用，用来标识 keepAliveTime 的时间单位。</p>
<h5 id="workqueue">⑤ workQueue</h5>
<p>线程池中的任务队列，使用 execute() 或 submit() 方法提交的任务都会存储在此队列中。</p>
<h5 id="threadfactory">⑥ threadFactory</h5>
<p>为线程池提供创建新线程的线程工厂。</p>
<h5 id="rejectedexecutionhandler">⑦ rejectedExecutionHandler</h5>
<p>线程池任务队列超过最大值之后的拒绝策略，RejectedExecutionHandler 是一个接口，里面只有一个 rejectedExecution 方法，可在此方法内添加任务超出最大值的事件处理。ThreadPoolExecutor 也提供了 4 种默认的拒绝策略：</p>
<ul>
<li>new ThreadPoolExecutor.DiscardPolicy()：丢弃掉该任务，不进行处理</li>
<li>new ThreadPoolExecutor.DiscardOldestPolicy()：丢弃队列里最近的一个任务，并执行当前任务</li>
<li>new ThreadPoolExecutor.AbortPolicy()：直接抛出 RejectedExecutionException 异常</li>
<li>new ThreadPoolExecutor.CallerRunsPolicy()：既不抛弃任务也不抛出异常，直接使用主线程来执行此任务</li>
</ul>
<p>包含所有参数的 ThreadPoolExecutor 使用代码：</p>
<pre><code class="java language-java">public class ThreadPoolExecutorTest {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(1, 1,
                10L, TimeUnit.SECONDS, new LinkedBlockingQueue&lt;Runnable&gt;(2),
                new MyThreadFactory(), new ThreadPoolExecutor.CallerRunsPolicy());
        threadPool.allowCoreThreadTimeOut(true);
        for (int i = 0; i &lt; 10; i++) {
            threadPool.execute(new Runnable() {
                @Override
                public void run() {
                    System.out.println(Thread.currentThread().getName());
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}
class MyThreadFactory implements ThreadFactory {
    private AtomicInteger count = new AtomicInteger(0);
    @Override
    public Thread newThread(Runnable r) {
        Thread t = new Thread(r);
        String threadName = "MyThread" + count.addAndGet(1);
        t.setName(threadName);
        return t;
    }
}
</code></pre>
<h4 id="executevssubmit">线程池执行方法 execute() VS submit()</h4>
<p>execute() 和 submit() 都是用来执行线程池的，区别在于 submit() 方法可以接收线程池执行的返回值。</p>
<p>下面分别来看两个方法的具体使用和区别：</p>
<pre><code class="java language-java">// 创建线程池
ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 10, 10L, TimeUnit.SECONDS, new LinkedBlockingQueue(100));
// execute 使用
threadPoolExecutor.execute(new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello, Java.");
    }
});
// submit 使用
Future&lt;String&gt; future = threadPoolExecutor.submit(new Callable&lt;String&gt;() {
    @Override
    public String call() throws Exception {
        System.out.println("Hello, 老王.");
        return "Success";
    }
});
System.out.println(future.get());
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>Hello, Java.</p>
  <p>Hello, 老王.</p>
  <p>Success</p>
</blockquote>
<h4 id="-3">线程池关闭</h4>
<p>线程池关闭，可以使用 shutdown() 或 shutdownNow() 方法，它们的区别是：</p>
<ul>
<li>shutdown()：不会立即终止线程池，而是要等所有任务队列中的任务都执行完后才会终止。执行完 shutdown 方法之后，线程池就不会再接受新任务了。</li>
<li>shutdownNow()：执行该方法，线程池的状态立刻变成 STOP 状态，并试图停止所有正在执行的线程，不再处理还在池队列中等待的任务，执行此方法会返回未执行的任务。</li>
</ul>
<p>下面用代码来模拟 shutdown() 之后，给线程池添加任务，代码如下：</p>
<pre><code class="java language-java">threadPoolExecutor.execute(() -&gt; {
    for (int i = 0; i &lt; 2; i++) {
        System.out.println("I'm " + i);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }
});
threadPoolExecutor.shutdown();
threadPoolExecutor.execute(() -&gt; {
    System.out.println("I'm Java.");
});
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>I'm 0</p>
  <p>Exception in thread "main" java.util.concurrent.RejectedExecutionException: Task com.interview.chapter5.Section2<code>$$Lambda$2</code>/1828972342@568db2f2 rejected from java.util.concurrent.ThreadPoolExecutor@378bf509[Shutting down, pool size = 1, active threads = 1, queued tasks = 0, completed tasks = 0]</p>
  <p>I'm 1</p>
</blockquote>
<p>可以看出，shutdown() 之后就不会再接受新的任务了，不过之前的任务会被执行完成。</p>
<h3 id="-4">相关面试题</h3>
<h4 id="1threadpoolexecutor">1.ThreadPoolExecutor 有哪些常用的方法？</h4>
<p>答：常用方法如下所示：</p>
<ul>
<li>submit()/execute()：执行线程池</li>
<li>shutdown()/shutdownNow()：终止线程池</li>
<li>isShutdown()：判断线程是否终止</li>
<li>getActiveCount()：正在运行的线程数</li>
<li>getCorePoolSize()：获取核心线程数</li>
<li>getMaximumPoolSize()：获取最大线程数</li>
<li>getQueue()：获取线程池中的任务队列</li>
<li>allowCoreThreadTimeOut(boolean)：设置空闲时是否回收核心线程</li>
</ul>
<h4 id="2">2.以下程序执行的结果是什么？</h4>
<pre><code class="java language-java">ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 10, 10L, TimeUnit.SECONDS, new LinkedBlockingQueue());
threadPoolExecutor.execute(new Runnable() {
    @Override
    public void run() {
        for (int i = 0; i &lt; 2; i++) {
            System.out.println("I：" + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
});
threadPoolExecutor.shutdownNow();
System.out.println("Java");
</code></pre>
<p>答：程序执行的结果是：</p>
<blockquote>
  <p>I：0</p>
  <p>Java</p>
  <p>java.lang.InterruptedException: sleep interrupted（报错信息）</p>
  <p>I：1</p>
</blockquote>
<p>题目解析：因为程序中使用了 <code>shutdownNow()</code> 会导致程序执行一次之后报错，抛出 <code>sleep interrupted</code> 异常，又因为本身有 try/catch，所以程序会继续执行打印 <code>I：1</code> 。</p>
<h4 id="3threadpoolsubmitexecute">3.在 ThreadPool 中 submit() 和 execute() 有什么区别？</h4>
<p>答：submit() 和 execute() 都是用来执行线程池的，只不过使用 execute() 执行线程池不能有返回方法，而使用 submit() 可以使用 Future 接收线程池执行的返回值。</p>
<p>submit() 方法源码（JDK 8）如下：</p>
<pre><code>public &lt;T&gt; Future&lt;T&gt; submit(Callable&lt;T&gt; task) {
    if (task == null) throw new NullPointerException();
    RunnableFuture&lt;T&gt; ftask = newTaskFor(task);
    execute(ftask);
    return ftask;
}
</code></pre>
<p>execute() 源码（JDK 8）如下：</p>
<pre><code>public void execute(Runnable command) {
    if (command == null)
        throw new NullPointerException();
    //..... 其他
}
</code></pre>
<h4 id="4threadpoolexecutor">4.说一下 ThreadPoolExecutor 都需要哪些参数？</h4>
<p>答：ThreadPoolExecutor 最多包含以下七个参数：</p>
<ul>
<li>corePoolSize：线程池中的核心线程数</li>
<li>maximumPoolSize：线程池中最大线程数</li>
<li>keepAliveTime：闲置超时时间</li>
<li>unit：keepAliveTime 超时时间的单位（时/分/秒等）</li>
<li>workQueue：线程池中的任务队列</li>
<li>threadFactory：为线程池提供创建新线程的线程工厂</li>
<li>rejectedExecutionHandler：线程池任务队列超过最大值之后的拒绝策略</li>
</ul>
<p>更多详细介绍，请见正文。</p>
<h4 id="5shutdownnowshutdown">5.在线程池中 shutdownNow() 和 shutdown() 有什么区别？</h4>
<p>答：shutdownNow() 和 shutdown() 都是用来终止线程池的，它们的区别是，使用 shutdown() 程序不会报错，也不会立即终止线程，它会等待线程池中的缓存任务执行完之后再退出，执行了 shutdown() 之后就不能给线程池添加新任务了；shutdownNow() 会试图立马停止任务，如果线程池中还有缓存任务正在执行，则会抛出 java.lang.InterruptedException: sleep interrupted 异常。</p>
<h4 id="6">6.说一说线程池的工作原理？</h4>
<p>答：当线程池中有任务需要执行时，线程池会判断如果线程数量没有超过核心数量就会新建线程池进行任务执行，如果线程池中的线程数量已经超过核心线程数，这时候任务就会被放入任务队列中排队等待执行；如果任务队列超过最大队列数，并且线程池没有达到最大线程数，就会新建线程来执行任务；如果超过了最大线程数，就会执行拒绝执行策略。</p>
<h4 id="7">7.以下线程名称被打印了几次？</h4>
<pre><code class="java language-java">ThreadPoolExecutor threadPool = new ThreadPoolExecutor(1, 1,
                10L, TimeUnit.SECONDS, new LinkedBlockingQueue&lt;Runnable&gt;(2),
                new ThreadPoolExecutor.DiscardPolicy());
threadPool.allowCoreThreadTimeOut(true);
for (int i = 0; i &lt; 10; i++) {
    threadPool.execute(new Runnable() {
        @Override
        public void run() {
            // 打印线程名称
            System.out.println(Thread.currentThread().getName());
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    });
</code></pre>
<p>答：线程名被打印了 3 次。<br />题目解析：线程池第 1 次执行任务时，会新创建任务并执行；第 2 次执行任务时，因为没有空闲线程所以会把任务放入队列；第 3 次同样把任务放入队列，因为队列最多可以放两条数据，所以第 4 次之后的执行都会被舍弃（没有定义拒绝策略），于是就打印了 3 次线程名称。</p>
<h3 id="-5">总结</h3>
<p>ThreadPoolExecutor 是创建线程池最传统和最推荐使用的方式，创建时要设置线程池的核心线程数和最大线程数还有任务队列集合，如果任务量大于队列的最大长度，线程池会先判断当前线程数量是否已经到达最大线程数，如果没有达到最大线程数就新建线程来执行任务，如果已经达到最大线程数，就会执行拒绝策略（拒绝策略可自行定义）。线程池可通过 submit() 来调用执行，从而获得线程执行的结果，也可以通过 shutdown() 来终止线程池。</p>
<blockquote>
  <p><a href="https://github.com/vipstone/java-interview/tree/master/interview-code/src/main/java/com/interview">点击此处下载本文源码</a></p>
</blockquote></div></article>