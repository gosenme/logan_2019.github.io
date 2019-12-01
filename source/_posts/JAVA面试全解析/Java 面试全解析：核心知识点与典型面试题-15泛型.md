---
title: Java 面试全解析：核心知识点与典型面试题-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">泛型</h3>
<h4 id="1">1）为什么要用泛型？</h4>
<p>在泛型没有诞生之前，我们经常会遇到这样的问题，如以下代码所示：</p>
<pre><code>ArrayList arrayList = new ArrayList();
arrayList.add("Java");
arrayList.add(24);
for (int i = 0; i &lt; arrayList.size(); i++) {
    String str = (String) arrayList.get(i);
    System.out.println(str);
}
</code></pre>
<p>看起来好像没有什么大问题，也能正常编译，但真正运行起来就会报错：</p>
<blockquote>
  <p>Exception in thread "main" java.lang.ClassCastException: java.lang.Integer cannot be cast to java.lang.String</p>
  <p>at xxx(xxx.java:12)</p>
  <p>类型转换出错，当我们给 ArrayList 放入不同类型的数据，却使用一种类型进行接收的时候，就会出现很多类似的错误，可能更多的时候，是因为开发人员的不小心导致的。那有没有好的办法可以杜绝此类问题的发生呢？这个时候 Java 语言提供了一个很好的解决方案——“泛型”。</p>
</blockquote>
<h4 id="2">2）泛型介绍</h4>
<p><strong>泛型</strong>：泛型本质上是类型参数化，解决了不确定对象的类型问题。<br />泛型的使用，请参考以下代码：</p>
<pre><code>ArrayList&lt;String&gt; arrayList = new ArrayList();
arrayList.add("Java");
</code></pre>
<p>这个时候如果给 arrayList 添加非 String 类型的元素，编译器就会报错，提醒开发人员插入相同类型的元素。</p>
<p>报错信息如下图所示：</p>
<p><img src="https://images.gitbook.cn/83dce010-cdeb-11e9-932d-6123ff488b55" alt="enter image description here" /></p>
<p>这样就可以避免开头示例中，类型不一致导致程序运行过程中报错的问题了。</p>
<h4 id="3">3）泛型的优点</h4>
<p>泛型的优点主要体现在以下三个方面。</p>
<ul>
<li>安全：不用担心程序运行过程中出现类型转换的错误。</li>
<li>避免了类型转换：如果是非泛型，获取到的元素是 Object 类型的，需要强制类型转换。</li>
<li>可读性高：编码阶段就明确的知道集合中元素的类型。</li>
</ul>
<h3 id="iterator">迭代器（Iterator）</h3>
<h4 id="1-1">1）为什么要用迭代器？</h4>
<p>我们回想一下，在迭代器（Iterator）没有出现之前，如果要遍历数组和集合，需要使用方法。</p>
<p>数组遍历，代码如下：</p>
<pre><code>String[] arr = new String[]{"Java", "Java虚拟机", "Java中文社群"};
for (int i = 0; i &lt; arr.length; i++) {
    String item = arr[i];
}
</code></pre>
<p>集合遍历，代码如下：</p>
<pre><code>List&lt;String&gt; list = new ArrayList&lt;String&gt;() {{
    add("Java");
    add("Java虚拟机");
    add("Java中文社群");
}};
for (int i = 0; i &lt; list.size(); i++) {
    String item = list.get(i);
}
</code></pre>
<p>而迭代器的产生，就是为不同类型的容器遍历，提供标准统一的方法。</p>
<p>迭代器遍历，代码如下：</p>
<pre><code>Iterator iterator = list.iterator();
while (iterator.hasNext()) {
    Object object = iterator.next();
    // do something
}
</code></pre>
<p><strong>总结</strong>：使用了迭代器就可以不用关注容器的内部细节，用同样的方式遍历不同类型的容器。</p>
<h4 id="2-1">2）迭代器介绍</h4>
<p>迭代器是用来遍历容器内所有元素对象的，也是一种常见的设计模式。</p>
<p>迭代器包含以下四个方法。</p>
<ul>
<li>hasNext():boolean —— 容器内是否还有可以访问的元素。</li>
<li>next():E —— 返回下一个元素。</li>
<li>remove():void —— 删除当前元素。</li>
<li>forEachRemaining(Consumer<? super E>):void —— JDK 8 中添加的，提供一个 lambda 表达式遍历容器元素。</li>
</ul>
<p>迭代器使用如下：</p>
<pre><code>List&lt;String&gt; list = new ArrayList&lt;String&gt;() {{
    add("Java");
    add("Java虚拟机");
    add("Java中文社群");
}};
Iterator iterator =  list.iterator();
// 遍历
while (iterator.hasNext()){
    String str = (String) iterator.next();
    if (str.equals("Java中文社群")){
        iterator.remove();
    }
}
System.out.println(list);
</code></pre>
<p>程序执行结果：</p>
<pre><code>[Java, Java虚拟机]
</code></pre>
<p>forEachRemaining 使用如下：</p>
<pre><code>List&lt;String&gt; list = new ArrayList&lt;String&gt;() {{
    add("Java");
    add("Java虚拟机");
    add("Java中文社群");
}};
// forEachRemaining 使用
list.iterator().forEachRemaining(item -&gt; System.out.println(item));
</code></pre>
<h3 id="-1">相关面试题</h3>
<h4 id="1nextobject">1.为什么迭代器的 next() 返回的是 Object 类型？</h4>
<p>答：因为迭代器不需要关注容器的内部细节，所以 next() 返回 Object 类型就可以接收任何类型的对象。</p>
<h4 id="2hashmap">2.HashMap 的遍历方式都有几种？</h4>
<p>答：HashMap 的遍历分为以下四种方式。</p>
<ul>
<li>方式一：entrySet 遍历</li>
<li>方式二：iterator 遍历</li>
<li>方式三：遍历所有的 key 和 value</li>
<li>方式四：通过 key 值遍历</li>
</ul>
<p>以上方式的代码实现如下：</p>
<pre><code>Map&lt;String, String&gt; hashMap = new HashMap();
hashMap.put("name", "老王");
hashMap.put("sex", "你猜");
// 方式一：entrySet 遍历
for (Map.Entry item : hashMap.entrySet()) {
  System.out.println(item.getKey() + ":" + item.getValue());
}
// 方式二：iterator 遍历
Iterator&lt;Map.Entry&lt;String, String&gt;&gt; iterator = hashMap.entrySet().iterator();
while (iterator.hasNext()) {
  Map.Entry&lt;String, String&gt; entry = iterator.next();
  System.out.println(entry.getKey() + ":" + entry.getValue());
}
// 方式三：遍历所有的 key 和 value
for (Object k : hashMap.keySet()) {
  // 循环所有的 key
  System.out.println(k);
}
for (Object v : hashMap.values()) {
  // 循环所有的值
  System.out.println(v);
}
// 方式四：通过 key 值遍历
for (Object k : hashMap.keySet()) {
  System.out.println(k + ":" + hashMap.get(k));
}
</code></pre>
<h4 id="3-1">3.以下关于泛型说法错误的是？</h4>
<p>A：泛型可以修饰类<br />B：泛型可以修饰方法<br />C：泛型不可以修饰接口<br />D：以上说法全错</p>
<p>答：选 C，泛型可以修饰类、方法、接口、变量。<br />例如：</p>
<pre><code>public interface Iterable&lt;T&gt; {
}
</code></pre>
<h4 id="4">4.以下程序执行的结果是什么？</h4>
<pre><code class="java language-java">List&lt;String&gt; list = new ArrayList&lt;&gt;();
List&lt;Integer&gt; list2 = new ArrayList&lt;&gt;();
System.out.println(list.getClass() == list2.getClass());
</code></pre>
<p>答：程序的执行结果是 <code>true</code>。<br />题目解析：Java 中泛型在编译时会进行类型擦除，因此 <code>List&lt;String&gt; list</code> 和 <code>List&lt;Integer&gt; list2</code> 类型擦除后的结果都是 java.util.ArrayLis ，进而 list.getClass() == list2.getClass() 的结果也一定是 true。</p>
<h4 id="5listobjectlist">5. <code>List&lt;Object&gt;</code> 和 <code>List&lt;?&gt;</code> 有什么区别？</h4>
<p>答：<code>List&lt;?&gt;</code> 可以容纳任意类型，只不过 <code>List&lt;?&gt;</code> 被赋值之后，就不允许添加和修改操作了；而 <code>List&lt;Object&gt;</code> 和 <code>List&lt;?&gt;</code> 不同的是它在赋值之后，可以进行添加和修改操作，如下图所示：</p>
<p><img src="https://images.gitbook.cn/b3a90d00-cdeb-11e9-932d-6123ff488b55" alt="enter image description here" /></p>
<h4 id="6liststringlistobject">6.可以把 <code>List&lt;String&gt;</code> 赋值给 <code>List&lt;Object&gt;</code> 吗？</h4>
<p>答：不可以，编译器会报错，如下图所示：</p>
<p><img src="https://images.gitbook.cn/cb2aa8d0-cdeb-11e9-b572-5118f14310d8" alt="enter image description here" /></p>
<h4 id="7listlistobject">7. <code>List</code> 和 <code>List&lt;Object&gt;</code> 的区别是什么？</h4>
<p>答： <code>List</code> 和 <code>List&lt;Object&gt;</code> 都能存储任意类型的数据，但 <code>List</code> 和 <code>List&lt;Object&gt;</code> 的唯一区别就是，<code>List</code> 不会触发编译器的类型安全检查，比如把 <code>List&lt;String&gt;</code> 赋值给 <code>List</code> 是没有任何问题的，但赋值给 <code>List&lt;Object&gt;</code> 就不行，如下图所示：</p>
<p><img src="https://images.gitbook.cn/e34947f0-cdeb-11e9-932d-6123ff488b55" alt="enter image description here" /></p>
<h4 id="8">8.以下程序执行的结果是？</h4>
<pre><code>List&lt;String&gt; list = new ArrayList&lt;&gt;();
list.add("Java");
list.add("Java虚拟机");
list.add("Java中文社群");
Iterator iterator = list.iterator();
while (iterator.hasNext()) {
    String str = (String) iterator.next();
    if (str.equals("Java中文社群")) {
        iterator.remove();
    }
}
while (iterator.hasNext()) {
    System.out.println(iterator.next());
}
System.out.println("Over");
</code></pre>
<p>答：程序打印结果是 <code>Over</code>。<br />题目解析：因为第一个 while 循环之后，iterator.hasNext() 返回值就为 false 了，所以不会进入第二个循环，之后打印最后的 Over。</p>
<h4 id="9">9.泛型的工作原理是什么？为什么要有类型擦除？</h4>
<p>答：泛型是通过类型擦除来实现的，类型擦除指的是编译器在编译时，会擦除了所有类型相关的信息，比如 <code>List&lt;String&gt;</code> 在编译后就会变成 <code>List</code> 类型，这样做的目的就是确保能和 Java 5 之前的版本（二进制类库）进行兼容。</p>
<h3 id="-2">总结</h3>
<p>通过本文知道了泛型的优点：安全性、避免类型转换、提高了代码的可读性。泛型的本质是类型参数化，但编译之后会执行类型擦除，这样就可以和 Java 5 之前的二进制类库进行兼容。本文也介绍了迭代器（Iterator）的使用，使用迭代器的好处是不用关注容器的内部细节，用同样的方式遍历不同类型的容器。</p>
<blockquote>
  <p><a href="https://github.com/vipstone/java-interview/tree/master/interview-code/src/main/java/com/interview">点击此处下载本文源码</a></p>
</blockquote></div></article>