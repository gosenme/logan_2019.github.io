---
title: Java 面试全解析：核心知识点与典型面试题-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">线程介绍</h3>
<p>线程（Thread）是程序运行的执行单元，依托于进程存在。一个进程中可以包含多个线程，多线程可以共享一块内存空间和一组系统资源，因此线程之间的切换更加节省资源、更加轻量化，因而也被称为轻量级的进程。</p>
<h4 id="-1">什么是进程</h4>
<p>进程（Processes）是程序的一次动态执行，是系统进行资源分配和调度的基本单位，是操作系统运行的基础，通常每一个进程都拥有自己独立的内存空间和系统资源。简单来说，进程可以被当做是一个正在运行的程序。</p>
<h4 id="-2">为什么需要线程</h4>
<p>程序的运行必须依靠进程，进程的实际执行单元就是线程。</p>
<h4 id="-3">为什么需要多线程</h4>
<p>多线程可以提高程序的执行性能。例如，有个 90 平方的房子，一个人打扫需要花费 30 分钟，三个人打扫就只需要 10 分钟，这三个人就是程序中的“多线程”。</p>
<h3 id="-4">线程使用</h3>
<p>线程的创建，分为以下三种方式：</p>
<ul>
<li>继承 Thread 类，重写 run 方法</li>
<li>实现 Runnable 接口，实现 run 方法</li>
<li>实现 Callable 接口，实现 call 方法</li>
</ul>
<p>下面分别来看看线程创建和使用的具体代码。</p>
<h4 id="1thread">1）继承 Thread 类</h4>
<p>请参考以下代码：</p>
<pre><code class="java language-java">class ThreadTest {
    public static void main(String[] args) throws Exception {
        MyThread thread = new MyThread();
        thread.start();
    }
}
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread");
    }
}
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>Thread</p>
</blockquote>
<h4 id="2runnable">2）实现 Runnable 接口</h4>
<p>请参考以下代码：</p>
<pre><code class="java language-java">class ThreadTest {
    public static void main(String[] args) {
        MyRunnable runnable = new MyRunnable();
        new Thread(runnable).start();
    }
}
class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable");
    }
}
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>Runnable</p>
</blockquote>
<h4 id="3callable">3）实现 Callable 接口</h4>
<p>请参考以下代码：</p>
<pre><code class="java language-java">class ThreadTest {
    public static void main(String[] args) throws Exception {
        MyCallable callable = new MyCallable();
        // 定义返回结果
        FutureTask&lt;String&gt; result = new FutureTask(callable);
        // 执行程序
        new Thread(result).start();
        // 输出返回结果
        System.out.println(result.get());
    }
}
class MyCallable implements Callable {
    @Override
    public String call() {
        System.out.println("Callable");
        return "Success";
    }
}
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>Callable</p>
  <p>Success</p>
</blockquote>
<p>可以看出，Callable 的调用是可以有返回值的，它弥补了之前调用线程没有返回值的情况，它是随着 JDK 1.5 一起发布的。</p>
<h4 id="4jdk8">4）JDK 8 创建线程</h4>
<p>JDK 8 之后可以使用 Lambda 表达式很方便地创建线程，请参考以下代码：</p>
<pre><code class="java language-java">new Thread(() -&gt; System.out.println("Lambda Of Thread.")).start();
</code></pre>
<h3 id="-5">线程高级用法</h3>
<h5 id="-6">线程等待</h5>
<p>使用 wait() 方法实现线程等待，代码如下：</p>
<pre><code class="java language-java">System.out.println(LocalDateTime.now());
Object lock = new Object();
Thread thread = new Thread(() -&gt; {
    synchronized (lock){
        try {
            // 1 秒钟之后自动唤醒
            lock.wait(1000);
            System.out.println(LocalDateTime.now());
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
});
thread.start();
</code></pre>
<p>以上程序执行结果如下：</p>
<blockquote>
  <p>2019-06-22T20:53:08.776</p>
  <p>2019-06-22T20:53:09.788</p>
</blockquote>
<p>注意：当使用 wait() 方法时，必须先持有当前对象的锁，否则会抛出异常 java.lang.IllegalMonitorStateException。</p>
<h5 id="-7">线程唤醒</h5>
<p>使用 notify()/notifyAll() 方法唤醒线程。</p>
<ul>
<li>notify() 方法随机唤醒对象的等待池中的一个线程；</li>
<li>notifyAll() 唤醒对象的等待池中的所有线程。</li>
</ul>
<p>使用如下：</p>
<pre><code class="java language-java">Object lock = new Object();
lock.wait();
lock.notify();
// lock.notifyAll();
</code></pre>
<h5 id="-8">线程休眠</h5>
<pre><code class="java language-java">// 休眠 1 秒
Thread.sleep(1000);
</code></pre>
<h5 id="-9">等待线程执行完成</h5>
<pre><code class="java language-java">Thread joinThread = new Thread(() -&gt; {
    try {
        System.out.println("执行前");
        Thread.sleep(1000);
        System.out.println("执行后");
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
});
joinThread.start();
joinThread.join();
System.out.println("主程序");
</code></pre>
<p>以上程序执行结果：</p>
<blockquote>
  <p>执行前</p>
  <p>执行后</p>
  <p>主程序</p>
</blockquote>
<h5 id="yieldcpu">yield 交出 CPU 执行权</h5>
<pre><code class="java language-java">new Thread(){
    @Override
    public void run() {
        for (int i = 1; i &lt; 10; i++) {
            if (i == 5) {
                // 让同优先级的线程有执行的机会
                this.yield();
            }
        }
    }
}.start();
</code></pre>
<p>注意：yield 方法是让同优先级的线程有执行的机会，但不能保证自己会从正在运行的状态迅速转换到可运行的状态。</p>
<h5 id="-10">线程中断</h5>
<p>使用 <code>System.exit(0)</code> 可以让整个程序退出；要中断单个线程，可配合 <code>interrupt()</code> 对线程进行“中断”。<br />使用代码如下：</p>
<pre><code class="java language-java">Thread interruptThread = new Thread() {
    @Override
    public void run() {
        for (int i = 0; i &lt; Integer.MAX_VALUE; i++) {
            System.out.println("i：" + i);
            if (this.isInterrupted()) {
                break;
            }
        }
    }
};
interruptThread.start();
Thread.sleep(10);
interruptThread.interrupt();
</code></pre>
<h5 id="-11">线程优先级</h5>
<p>在 Java 语言中，每一个线程有一个优先级，默认情况下，一个线程继承它父类的优先级。可以使用 setPriority 方法设置（1-10）优先级，默认的优先级是 5，数字越大表示优先级越高，优先级越高的线程可能优先被执行的概率就越大。<br />设置优先级的代码如下：</p>
<pre><code class="java language-java">Thread thread = new Thread(() -&gt; System.out.println("Java"));
thread.setPriority(10);
thread.start();
</code></pre>
<h3 id="-12">死锁</h3>
<p>死锁是指两个或两个以上的进程在执行过程中，由于竞争资源或者由于彼此通信而造成的一种阻塞的现象，若无外力作用，它们都将无法推进下去。<br />比如，当线程 A 持有独占锁 a，并尝试去获取独占锁 b 的同时，线程 B 持有独占锁 b，并尝试获取独占锁 a 的情况下，就会发生 A B 两个线程由于互相持有对方需要的锁，而发生的阻塞现象，我们称为死锁。<br />死锁示意图如下所示：<br /><img src="https://images.gitbook.cn/65072410-d2d3-11e9-a6f3-5b822f50de09" alt="enter image description here" /><br />死锁代码：</p>
<pre><code class="java language-java">Object obj1 = new Object();
Object obj2 = new Object();
// 线程1拥有对象1，想要等待获取对象2
new Thread() {
    @Override
    public void run() {
        synchronized (obj1) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            synchronized (obj2) {
                System.out.println(Thread.currentThread().getName());
            }
        }
    }
}.start();
// 线程2拥有对象2，想要等待获取对象1
new Thread() {
    @Override
    public void run() {
        synchronized (obj2) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            synchronized (obj1) {
                System.out.println(Thread.currentThread().getName());
            }
        }
    }
}.start();
</code></pre>
<h3 id="-13">相关面试题</h3>
<h4 id="1">1.线程和进程有什么区别和联系？</h4>
<p>答：从本质上来说，线程是进程的实际执行单元，一个程序至少有一个进程，一个进程至少有一个线程，它们的区别主要体现在以下几个方面：</p>
<ul>
<li>进程间是独立的，不能共享内存空间和上下文，而线程可以；</li>
<li>进程是程序的一次执行，线程是进程中执行的一段程序片段；</li>
<li>线程占用的资源比进程少。</li>
</ul>
<h4 id="2">2.如何保证一个线程执行完再执行第二个线程？</h4>
<p>答：使用 join() 方法，等待上一个线程的执行完之后，再执行当前线程。<br />示例代码：</p>
<pre><code class="java language-java">Thread joinThread = new Thread(() -&gt; {
    try {
        System.out.println("执行前");
        Thread.sleep(1000);
        System.out.println("执行后");
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
});
joinThread.start();
joinThread.join();
System.out.println("主程序");
</code></pre>
<h4 id="3">3.线程有哪些常用的方法？</h4>
<p>答：线程的常用方法如下：</p>
<ul>
<li>currentThread()：返回当前正在执行的线程引用</li>
<li>getName()：返回此线程的名称</li>
<li>setPriority()/getPriority()：设置和返回此线程的优先级</li>
<li>isAlive()：检测此线程是否处于活动状态，活动状态指的是程序处于正在运行或准备运行的状态</li>
<li>sleep()：使线程休眠</li>
<li>join()：等待线程执行完成</li>
<li>yield()：让同优先级的线程有执行的机会，但不能保证自己会从正在运行的状态迅速转换到可运行的状态</li>
<li>interrupted()：是线程处于中断的状态，但不能真正中断线程</li>
</ul>
<h4 id="4waitsleep">4.wait() 和 sleep() 有什么区别？</h4>
<p>答：wait() 和 sleep() 的区别主要体现在以下三个方面。</p>
<ul>
<li>存在类的不同：sleep() 来自 Thread，wait() 来自 Object。</li>
<li>释放锁：sleep() 不释放锁；wait() 释放锁。</li>
<li>用法不同：sleep() 时间到会自动恢复；wait() 可以使用 notify()/notifyAll() 直接唤醒。</li>
</ul>
<h4 id="5">5.守护线程是什么？</h4>
<p>答：守护线程是一种比较低级别的线程，一般用于为其他类别线程提供服务，因此当其他线程都退出时，它也就没有存在的必要了。例如，JVM（Java 虚拟机）中的垃圾回收线程。</p>
<h4 id="6">6.线程有哪些状态？</h4>
<p>答：在 JDK 8 中，线程的状态有以下六种。</p>
<ul>
<li>NEW：尚未启动</li>
<li>RUNNABLE：正在执行中</li>
<li>BLOCKED：阻塞（被同步锁或者 IO 锁阻塞）</li>
<li>WAITING：永久等待状态</li>
<li>TIMED_WAITING：等待指定的时间重新被唤醒的状态</li>
<li>TERMINATED：执行完成</li>
</ul>
<p>题目分析：JDK 8 线程状态的源码如下图所示：<br /><img src="https://images.gitbook.cn/bfa90b90-d2d3-11e9-9a2b-37838cbf8b11" alt="enter image description here" /></p>
<h4 id="7startrun">7.线程中的 start() 和 run() 有那些区别？</h4>
<p>答：start() 方法用于启动线程，run() 方法用于执行线程的运行时代码。run() 可以重复调用，而 start() 只能调用一次。</p>
<h4 id="8">8.产生死锁需要具备哪些条件？</h4>
<p>答：产生死锁的四个必要条件：</p>
<ul>
<li>互斥条件：一个资源每次只能被一个线程使用；</li>
<li>请求与保持条件：一个线程因请求资源而阻塞时，对已获得的资源保持不放；</li>
<li>不剥夺条件：线程已获得的资源，在末使用完之前，不能强行剥夺；</li>
<li>循环等待条件：若干线程之间形成一种头尾相接的循环等待资源关系；</li>
</ul>
<p>这四个条件是死锁的必要条件，只要系统发生死锁，这些条件必然成立，而只要上述条件之一不满足，就不会发生死锁。</p>
<h4 id="9">9.如何预防死锁？</h4>
<p>答：预防死锁的方法如下：</p>
<ul>
<li>尽量使用 tryLock(long timeout, TimeUnit unit) 的方法 (ReentrantLock、ReentrantReadWriteLock)，设置超时时间，超时可以退出防止死锁；</li>
<li>尽量使用 Java. util. concurrent 并发类代替自己手写锁；</li>
<li>尽量降低锁的使用粒度，尽量不要几个功能用同一把锁；</li>
<li>尽量减少同步的代码块。</li>
</ul>
<h4 id="10threadwaitthreadwait0">10.thread.wait() 和 thread.wait(0) 有什么区别？代表什么含义？</h4>
<p>答：thread.wait() 和 thread.wait(0) 是相同的，使用 thread.wait() 内部其实是调用的 thread.wait(0)，源码如下：</p>
<pre><code class="java language-java">public final void wait() throws InterruptedException {
    wait(0);
}
</code></pre>
<p>wait() 表示进入等待状态，释放当前的锁让出 CPU 资源，并且只能等程序执行 notify()/notifyAll() 方法才会被重写唤醒。</p>
<h4 id="11112233">11.如何让两个程序依次输出 11/22/33 等数字，请写出实现代码？</h4>
<p>答：使用思路是在每个线程输出信息之后，让当前线程等待一会再执行下一次操作，具体实现代码如下：</p>
<pre><code class="java language-java">new Thread(() -&gt; {
    for (int i = 1; i &lt; 4; i++) {
        System.out.println("线程一：" + i);
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}).start();
new Thread(() -&gt; {
    for (int i = 1; i &lt; 4; i++) {
        System.out.println("线程二：" + i);
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}).start();
</code></pre>
<p>程序执行结果如下：</p>
<blockquote>
  <p>线程一：1</p>
  <p>线程二：1</p>
  <p>线程二：2</p>
  <p>线程一：2</p>
  <p>线程二：3</p>
  <p>线程一：3</p>
</blockquote>
<h4 id="12">12.说一下线程的调度策略？</h4>
<p>答：线程调度器选择优先级最高的线程运行，但是如果发生以下情况，就会终止线程的运行：</p>
<ul>
<li>线程体中调用了 yield() 方法，让出了对 CPU 的占用权；</li>
<li>线程体中调用了 sleep() 方法，使线程进入睡眠状态；</li>
<li>线程由于 I/O 操作而受阻塞；</li>
<li>另一个更高优先级的线程出现；</li>
<li>在支持时间片的系统中，该线程的时间片用完。</li>
</ul>
<h3 id="-14">总结</h3>
<p>程序的运行依靠的是进程，而进程的执行依靠的是多个线程，多线程之间可以共享一块内存和一组系统资源，而多进程间通常是相互独立的。线程的创建有三种方式：继承 Thread 重写 run 方法，实现 Runnable 或 Callable 接口，其中 Callable 可以允许线程的执行有返回值，JDK 8 中也可以使用 Lambda 来更加方便的使用线程，线程是有优先级的，优先级从 1-10 ，数字越大优先级越高，也越早被执行。如果两个线程各自拥有一把锁的同时，又同时等待获取对方的锁，就会造成死锁。可以降低锁的粒度或减少同步代码块的范围或使用 Java 提供的安全类，来防止死锁的产生。</p>
<blockquote>
  <p><a href="https://github.com/vipstone/java-interview/tree/master/interview-code/src/main/java/com/interview">点击此处下载本文源码</a></p>
</blockquote></div></article>