---
title: Java 面试全解析：核心知识点与典型面试题-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">基本数据类型</h3>
<p>Java 基本数据按类型可以分为四大类：布尔型、整数型、浮点型、字符型，这四大类包含 8 种基本数据类型。</p>
<ul>
<li>布尔型：boolean</li>
<li>整数型：byte、short、int、long</li>
<li>浮点型：float、double</li>
<li>字符型：char</li>
</ul>
<p>8 种基本类型取值如下：</p>
<table>
<thead>
<tr>
<th>数据类型</th>
<th>代表含义</th>
<th>默认值</th>
<th>取值</th>
<th>包装类</th>
</tr>
</thead>
<tbody>
<tr>
<td>boolean</td>
<td>布尔型</td>
<td>false</td>
<td>0(false) 到 1(true)</td>
<td>Boolean</td>
</tr>
<tr>
<td>byte</td>
<td>字节型</td>
<td>(byte)0</td>
<td>﹣128 到 127</td>
<td>Byte</td>
</tr>
<tr>
<td>char</td>
<td>字符型</td>
<td>'\u0000'(空)</td>
<td>'\u0000' 到 '\uFFFF'</td>
<td>Character</td>
</tr>
<tr>
<td>short</td>
<td>短整数型</td>
<td>(short)0</td>
<td>-$2^{15}$ 到 $2^{15}$-1</td>
<td>Short</td>
</tr>
<tr>
<td>int</td>
<td>整数型</td>
<td>0</td>
<td>﹣$2^{31}$ 到 $2^{31}$-1</td>
<td>Integer</td>
</tr>
<tr>
<td>long</td>
<td>长整数型</td>
<td>0L</td>
<td>﹣$2^{63}$ 到 $2^{63}$-1</td>
<td>Long</td>
</tr>
<tr>
<td>float</td>
<td>单浮点型</td>
<td>0.0f</td>
<td>1.4e-45 到 3.4e+38</td>
<td>Float</td>
</tr>
<tr>
<td>double</td>
<td>双浮点型</td>
<td>0.0d</td>
<td>4.9e-324 到 1.798e+308</td>
<td>Double</td>
</tr>
</tbody>
</table>
<p>除 char 的包装类 Character 和 int 的包装类 Integer 之外，其他基本数据类型的包装类只需要首字母大写即可。包装类的作用和特点，本文下半部分详细讲解。</p>
<p>我们可以在代码中，查看某种类型的取值范围，代码如下：</p>
<pre><code>public static void main(String[] args) {
    // Byte 取值：-128 ~ 127
    System.out.println(String.format("Byte 取值：%d ~ %d", Byte.MIN_VALUE, Byte.MAX_VALUE));
    // Int 取值：-2147483648 ~ 2147483647
    System.out.println(String.format("Int 取值：%d ~ %d", Integer.MIN_VALUE, Integer.MAX_VALUE));
}
</code></pre>
<h3 id="-1">包装类型</h3>
<p>我们知道 8 种基本数据类型都有其对应的包装类，因为 Java 的设计思想是万物既对象，有很多时候我们需要以对象的形式操作某项功能，比如说获取哈希值（hashCode）或获取类（getClass）等。</p>
<p>那包装类特性有哪些？</p>
<p><strong>1. 功能丰富</strong></p>
<p>包装类本质上是一个对象，对象就包含有属性和方法，比如 hashCode、getClass 、max、min 等。</p>
<p><strong>2. 可定义泛型类型参数</strong></p>
<p>包装类可以定义泛型，而基本类型不行。</p>
<p>比如使用 Integer 定义泛型，代码：</p>
<pre><code>List&lt;Integer&gt; list = new ArrayList&lt;&gt;();
</code></pre>
<p>如果使用 int 定义就会报错，代码：</p>
<pre><code>List list = new ArrayList&lt;&gt;();  // 编译器代码报错
</code></pre>
<p><strong>3. 序列化</strong></p>
<p>因为包装类都实现了 Serializable 接口，所以包装类天然支持序列化和反序列化。比如 Integer 的类图如下：</p>
<p><img src="https://images.gitbook.cn/cb8c6a80-baa8-11e9-8bd3-43e1fddff917" alt="Integer 类图" /></p>
<p><strong>4. 类型转换</strong></p>
<p>包装类提供了类型转换的方法，可以很方便的实现类型之间的转换，比如 Integer 类型转换代码：</p>
<pre><code>String age = "18";
int ageInt = Integer.parseInt(age) + 2;
// 输出结果：20
System.out.println(ageInt);
</code></pre>
<p><strong>5. 高频区间的数据缓存</strong></p>
<p>此特性为包装类很重要的用途之一，用于高频区间的数据缓存，以 Integer 为例来说，在数值区间为 -128~127 时，会直接复用已有对象，在这区间之外的数字才会在堆上产生。</p>
<p>我们使用 == 对 Integer 进行验证，代码如下：</p>
<pre><code>public static void main(String[] args) {
        // Integer 高频区缓存范围 -128~127
        Integer num1 = 127;
        Integer num2 = 127;
        // Integer 取值 127 == 结果为 true（值127 num1==num2 =&gt; true）
        System.out.println("值127 num1==num2 =&gt; " + (num1 == num2));
        Integer num3 = 128;
        Integer num4 = 128;
        // Integer 取值 128 == 结果为 false（值128 num3==num4 =&gt; false）
        System.out.println("值128 num3==num4 =&gt; " + (num3 == num4));
    }
</code></pre>
<p>从上面的代码很明显可以看出，Integer 为 127 时复用了已有对象，当值为 128 时，重新在堆上生成了新对象。</p>
<p>为什么会产生高频区域数据缓存？我们查看源码就能发现“线索”，源码版本 JDK8，源码如下：</p>
<pre><code>public static Integer valueOf(int i) {
  if (i &gt;= IntegerCache.low &amp;&amp; i &lt;= IntegerCache.high)
    return IntegerCache.cache[i + (-IntegerCache.low)];
  return new Integer(i);
}
</code></pre>
<p>由此可见，高频区域的数值会直接使用已有对象，非高频区域的数值会重新 new 一个新的对象。</p>
<p>各包装类高频区域的取值范围：</p>
<ul>
<li>Boolean：使用静态 final 定义，就会返回静态值</li>
<li>Byte：缓存区 -128~127</li>
<li>Short：缓存区 -128~127</li>
<li>Character：缓存区 0~127</li>
<li>Long：缓存区 -128~127</li>
<li>Integer：缓存区 -128~127</li>
</ul>
<h3 id="-2">包装类的注意事项</h3>
<ul>
<li><p>int 的默认值是 0，而 Integer 的默认值是 null。</p></li>
<li><p>推荐所有包装类对象之间的值比较使用 <code>equals()</code> 方法，因为包装类的非高频区数据会在堆上产生，而高频区又会复用已有对象，这样会导致同样的代码，因为取值的不同，而产生两种截然不同的结果。代码示例：</p></li>
</ul>
<pre><code>public static void main(String[] args) {
    // Integer 高频区缓存范围 -128~127
    Integer num1 = 127;
    Integer num2 = 127;
    // Integer 取值 127 == 结果为 true（值127 num1==num2 =&gt; true）
    System.out.println("值127 num1==num2 =&gt; " + (num1 == num2));
    Integer num3 = 128;
    Integer num4 = 128;
    // Integer 取值 128 == 结果为 false（值128 num3==num4 =&gt; false）
    System.out.println("值128 num3==num4 =&gt; " + (num3 == num4));
    // Integer 取值 128 equals 结果为 true（值128 num3.equals(num4) =&gt; true）
    System.out.println("值128 num3.equals(num4) =&gt; " + num3.equals(num4));
}
</code></pre>
<ul>
<li><p>Float 和 Double 不会有缓存，其他包装类都有缓存。</p></li>
<li><p>Integer 是唯一一个可以修改缓存范围的包装类，在 VM optons 加入参数：</p></li>
</ul>
<blockquote>
  <p>-XX:AutoBoxCacheMax=666
  即修改缓存最大值为 <code>666</code> 。</p>
</blockquote>
<p>示例代码如下：</p>
<pre><code>public static void main(String[] args) {
    Integer num1 = -128;
    Integer num2 = -128;
    System.out.println("值为-128 =&gt; " + (num1 == num2));
    Integer num3 = 666;
    Integer num4 = 666;
    System.out.println("值为666 =&gt; " + (num3 == num4));
    Integer num5 = 667;
    Integer num6 = 667;
    System.out.println("值为667 =&gt; " + (num5 == num6));
}
</code></pre>
<p>执行结果如下：</p>
<pre><code>值为-128 =&gt; true
值为666 =&gt; true
值为667 =&gt; false
</code></pre>
<p>由此可见将 Integer 最大缓存修改为 666 之后，667 不会被缓存，而 -128~666 之间的数都被缓存了。</p>
<h3 id="-3">相关面试题</h3>
<h4 id="1integer">1. 以下 Integer 代码输出的结果是？</h4>
<pre><code class="java language-java">Integer age = 10;
Integer age2 = 10;
Integer age3 = 133;
Integer age4 = 133;
System.out.println((age == age2) + "," + (age3 == age4));
</code></pre>
<p>答：<code>true,false</code></p>
<h4 id="2double">2. 以下 Double 代码输出的结果是？</h4>
<pre><code>Double num = 10d;
Double num2 = 10d;
Double num3 = 133d;
Double num4 = 133d;
System.out.println((num == num2) + "," + (num3 == num4));
</code></pre>
<p>答：<code>false,false</code></p>
<h4 id="3">3. 以下程序输出结果是？</h4>
<pre><code class="java language-java">int i = 100;
Integer j = new Integer(100);
System.out.println(i == j);
System.out.println(j.equals(i));
</code></pre>
<p>A：true,true<br />B：true,false<br />C：false,true<br />D：false,false<br /></p>
<p>答：A</p>
<p>题目分析：有人认为这和 Integer 高速缓存有关系，但你发现把值改为 10000 结果也是 <code>true,true</code>，这是因为 Integer 和 int 比较时，会自动拆箱为 int 相当于两个 int 比较，值一定是 <code>true,true</code>。</p>
<h4 id="4">4. 以下程序执行的结果是？</h4>
<pre><code class="java language-java">final int iMax = Integer.MAX_VALUE;
System.out.println(iMax + 1);
</code></pre>
<p>A：2147483648<br />B：-2147483648<br />C：程序报错<br />D：以上都不是</p>
<p>答：B</p>
<p>题目解析：这是因为整数在内存中使用的是补码的形式表示，最高位是符号位 0 表示正数，1 表示负数，当执行 +1 时，最高位就变成了 1，结果就成了 -2147483648。</p>
<h4 id="5">5. 以下程序执行的结果是？</h4>
<pre><code class="java language-java">Set&lt;Short&gt; set = new HashSet&lt;&gt;();
for (short i = 0; i &lt; 5; i++) {
    set.add(i);
    set.remove(i - 1);
}
System.out.println(set.size());
</code></pre>
<p>A：1<br />B：0<br />C：5<br />D：以上都不是<br /></p>
<p>答：5</p>
<p>题目解析：Short 类型 -1 之后转换成了 Int 类型，remove() 的时候在集合中找不到 Int 类型的数据，所以就没有删除任何元素，执行的结果就是 5。</p>
<h4 id="6shorts2ss1shorts2s1">6. <code>short s=2;s=s+1;</code> 会报错吗？<code>short s=2;s+=1;</code> 会报错吗？</h4>
<p>答：s=s+1 会报错，s+=1 不会报错，因为 s=s+1 会导致 short 类型升级为 int 类型，所以会报错，而 s+=1 还是原来的 short 类型，所以不会报错。</p>
<h4 id="7floatf34">7. <code>float f=3.4;</code> 会报错吗？为什么？</h4>
<p>答：会报错，因为值 3.4 是 double 类型，float 类型级别小于 double 类型，所以会报错。如下图所示：</p>
<p><img src="https://images.gitbook.cn/1cab8440-baaa-11e9-8bd3-43e1fddff917" alt="报错示例图" /></p>
<h4 id="8">8. 为什么需要包装类？</h4>
<p>答：需要包装类的原因有两个。</p>
<p>① Java 的设计思想是万物既对象，包装类体现了面向对象的设计理念；<br />② 包装类包含了很多属性和方法，比基本数据类型功能多，比如提供的获取哈希值（hashCode）或获取类（getClass）的方法等。</p>
<h4 id="9intinteger128127">9. 基本类 int 和包装类 Integer，在 -128~127 之间都会复用已有的缓存对象，这种说法正确吗？</h4>
<p>答：不正确，只有包装类高频区域数据才有缓存。</p>
<h4 id="10doubleinteger">10. 包装类 Double 和 Integer 一样都有高频区域数据缓存，这种说法正确吗？</h4>
<p>答：不正确，基本数据类型的包装类只有 Double 和 Float 没有高频区域的缓存。</p>
<h4 id="11">11. 包装类的值比较要使用什么方法？</h4>
<p>答：包装类因为有高频区域数据缓存，所以推荐使用 equals() 方法进行值比较。</p>
<h4 id="12">12. 包装类有哪些功能？</h4>
<p>答：包装类提供的功能有以下几个。</p>
<ul>
<li>功能丰富：包装类包含了有 hashCode、getClass 、max、min 等方法；</li>
<li>可定义泛型类型参数：例如 <code>List&lt;Integer&gt; list = new ArrayList&lt;&gt;();</code> ;</li>
<li>序列化：包装类实现了 Serializable 接口，所以包装类天然支持序列化和反序列化；</li>
<li>类型转换：包装类提供了方便的类型转换方法，比如 Integer 的 parseInt() 方法；</li>
<li>高频区域数据缓存：高频区域可使用已有的缓存对象。</li>
</ul>
<p>详见正文“包装类型”部分内容。</p>
<h4 id="13">13. 泛型可以为基本类型吗？为什么？</h4>
<p>答：泛型不能使用基本数据类型。泛型在 JVM（Java虚拟机）编译的时候会类型檫除，比如代码 <code>List&lt;Integer&gt; list</code>  在 JVM 编译的时候会转换为 <code>List list</code> ，因为泛型是在 JDK 5 时提供的，而 JVM 的类型檫除是为了兼容以前代码的一个折中方案，类型檫除之后就变成了 Object，而 Object 不能存储基本数据类型，但可以使用基本数据类型对应的包装类，所以像 <code>List&lt;int&gt; list</code>  这样的代码是不被允许的，编译器阶段会检查报错，而 <code>List&lt;Integer&gt; list</code> 是被允许的。</p>
<h4 id="14">14. 选择包装类还是基本类的原则有哪些？</h4>
<p>答：我们知道正确的使用包装类，可以提供程序的执行效率，可以使用已有的缓存，一般情况下选择基本数据类型还是包装类原则有以下几个。</p>
<p>① 所有 POJO 类属性必须使用包装类；<br />② RPC 方法返回值和参数必须使用包装类；<br />③ 所有局部变量推荐使用基本数据类型。</p>
<h4 id="15jvm">15. 基本数据类型在 JVM 中一定存储在栈中吗？为什么？</h4>
<p>答：基本数据类型不一定存储在栈中，因为基本类型的存储位置取决于声明的作用域，来看具体的解释。</p>
<ul>
<li>当基本数据类型为局部变量的时候，比如在方法中声明的变量，则存放在方法栈中的，当方法结束系统会释放方法栈，在该方法中的变量也会随着栈的销毁而结束，这也是局部变量只能在方法中使用的原因；</li>
<li>当基本数据类型为全局变量的时候，比如类中的声明的变量，则存储在堆上，因为全局变量不会随着某个方法的执行结束而销毁。</li>
</ul>
<h4 id="16">16. 以下程序执行的结果是？</h4>
<pre><code class="java language-java">Integer i1 = new Integer(10);
Integer i2 = new Integer(10);
Integer i3 = Integer.valueOf(10);
Integer i4 = Integer.valueOf(10);
System.out.println(i1 == i2);
System.out.println(i2 == i3);
System.out.println(i3 == i4);
</code></pre>
<p>A：false,false,false<br />B：false,false,true<br />C：false,true,true<br />D：true,false,false</p>
<p>答：B</p>
<p>题目解析：new Integer(10) 每次都会创建一个新对象，Integer.valueOf(10) 则会使用缓存池中的对象。</p>
<h4 id="1730103">17. 3*0.1==0.3 返回值是多少？</h4>
<p>答：返回值为：false。</p>
<p>题目解析：因为有些浮点数不能完全精确的表示出来，如下代码：</p>
<blockquote>
  <p>System.out.println(3 * 0.1);</p>
</blockquote>
<p>返回的结果是：0.30000000000000004。</p>
<hr />
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《GitChat|老王课程交流群》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「234」给小助手获取入群资格。</p>
</blockquote></div></article>