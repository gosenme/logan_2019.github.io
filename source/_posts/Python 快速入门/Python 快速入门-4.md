---
title: Python 快速入门-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>经过前面章节的学习，我们了解了数字和运算符。本文将要引入一个另一个重要概念：数据结构，包括字符串、列表、元组、字典、栈、队列和集合。在正式介绍之前，先简要介绍一下数据结构的概念，读者可以选择跳过，不影响阅读后文。</p>
<h3 id="">数据结构</h3>
<p>一般认为，一个数据结构是由数据元素依据某种逻辑联系组织起来的。对数据元素间逻辑关系的描述称为数据的逻辑结构；数据必须在计算机内存储，数据的存储结构是数据结构的实现形式，是其在计算机内的表示；此外讨论一个数据结构必须同时讨论在该类数据上执行的运算才有意义。一个逻辑数据结构可以有多种存储结构，且各种存储结构影响数据处理的效率。</p>
<p>在许多类型的程序的设计中，数据结构的选择是一个基本的设计考虑因素。许多大型系统的构造经验表明，系统实现的困难程度和系统构造的质量都严重的依赖于是否选择了最优的数据结构。许多时候，确定了数据结构后，算法就容易得到了。有些时候事情也会反过来，我们根据特定算法来选择数据结构与之适应。不论哪种情况，选择合适的数据结构都是非常重要的。</p>
<p>选择了数据结构，算法也随之确定，是数据而不是算法是系统构造的关键因素。这种洞见导致了许多种软件设计方法和程序设计语言的出现，面向对象的程序设计语言就是其中之一。</p>
<h3 id="-1">字符串</h3>
<p>在各类编程语言中，字符串都是高频使用的数据类型，因此，各类编程语言为字符串的操作提供了大量的内建函数，几乎涵盖所有应用场景，Python 也不例外，其字符串同样具有极为丰富的内建函数，约四十种，本文将介绍其中常用的几种。</p>
<h4 id="-2">创建字符串</h4>
<p>创建字符串非常简单，只需要为变量赋值即可。</p>
<pre><code class="python language-python">str1 = "Hello world!"
str2 = "ABCDEFG"
</code></pre>
<h4 id="-3">访问字符串中的元素</h4>
<p>一个字符串可以看成若干个字符元素组成，Python 中可以通过索引来访问字符串中的元素，也可以访问子串。</p>
<pre><code class="python language-python">str1 = "Hello world!"
#访问字符串中的单个字符或者子串
print('str1:',str1)
print('str1[0]:',str1[0])
print('str1[0:4]:',str1[0:5])
print('str1[5:9]:',str1[6:11])
</code></pre>
<p>执行结果：</p>
<pre><code>str1: Hello world!
str1[0]: H
str1[0:4]: Hello
str1[5:9]: world
</code></pre>
<h4 id="-4">修改字符串</h4>
<p>Python 字符串修改需要通过内建 replace(old,new) 方法，不支持直接通过索引对已有内容的修改，此外，还支持对字符串拼接。如下例子：</p>
<pre><code class="python language-python">str1 = "Hi!"
str2 = "Jack"
#通过拼接修改字符串
str1 = str1 + str2
print('After splicing str1:',str1)
#通过替换修改字符串:replace(old,new)
str1 = str1.replace(str2, "Tom")
print('After replacement str1:',str1)
</code></pre>
<p>执行结果：</p>
<pre><code>After splicing str1: Hi!Jack
After replacement str1: Hi!Tom
</code></pre>
<h4 id="-5">字符串运算符</h4>
<p>字符串是一种非常灵活的数据结构，可以进行拼接、剪切、复制等操作。如下例子：</p>
<pre><code class="python language-python">str1 = "Hello world!"
str2 = "Jack"
#字符串拼接
print('str1+str2:',str1+str2)
#字符串截取
print('str1[0:6]:',str1[0:6])
#字符串复制
print('str2*2:',str2*3)
#成员运算：判断一个字符串是否包含某成员
print('world in str1?','world' in str1)
print('word in str1?','word' in str1)
</code></pre>
<p>执行结果：</p>
<pre><code>str1+str2: Hello world!Jack
str1[0:6]: Hello 
str2*2: JackJackJack
world in str1? True
word in str1? False
</code></pre>
<h4 id="-6">字符串格式化</h4>
<p>和 C/C++、Java 一样，Python 也支持字符串的格式化输出，格式化的语法与 C 语言基本是一样的，有 C 语言基础的读者，可以直接跳过本小节内容。</p>
<pre><code class="python language-python">#格式化为十进制:%d
print('PI is approximately equal to %d (I)'%(3.1415926))
#格式化字符串:%s
print('PI is approximately equal to %s (II)'%(3.1415926))
#格式化浮点数字，可指定小数点后的精度,默认为6位小数:%f
print('PI is approximately equal to %f (III)'%(3.1415926))
#格式化浮点数字，指定n位小数:%.nf
print('PI is approximately equal to %.2f (IV)'%(3.1415926))
#用科学计数法格式化浮点数:%e
print('PI is approximately equal to %e (V)'%(3.1415926))
#格式化为十进制:%d
print('The road is about %d meters long (VI)'%(1234))
#格式化无符号八进制数:%d
print('The road is about %o meters long (VII)'%(1234))
#格式化无符号十六进制数:%x
print('The road is about %x meters long (VIII)'%(1234))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">PI is approximately equal to 3 (I)
PI is approximately equal to 3.1415926 (II)
PI is approximately equal to 3.141593 (III)
PI is approximately equal to 3.14 (IV)
PI is approximately equal to 3.141593e+00 (V)
The road is about 1234 meters long (VI)
The road is about 2322 meters long (VII)
The road is about 4d2 meters long (VIII)
</code></pre>
<h4 id="-7">字符串内建函数</h4>
<p>Python 为字符串提供了40余个内建函数，在此，我只介绍常用的几个方法，读者在实际应用中可根据需要调用对应的方法。</p>
<pre><code class="python language-python">str1 = "  Hello world! Hello"
str2 = "Hello"

#返回字符串的长度:len(str)
print('str1的长度:',len(str1))

#对字符串进行分割:split(str),分割符为str，此处以空格进行分割
print('str1以空格分割的结果:',str1.split(' '))

#删除字符串字符串首尾的空格
print('str1删除首尾空格:',str1.strip())

#count(str2, beg&gt;=0,end&lt;=len(str1))
#返回 str2 在 str1 里面出现的次数,如果 beg 或者 end 指定则返回指定范围内 str2出现的次数
print('str2在str1中出现的次数:',str1.count(str2))
print('str2在str1中出现的次数(指定范围):',str1.count(str2,10,20))

#检查字符串是否以 obj 结束，如果beg 或者 end 指定则检查指定的范围内是否以 obj 结束
#如果是，返回 True,否则返回 False.
print('str1是否以 str2结尾:',str1.endswith(str2))
print('str1是否以 str2结尾(指定范围):',str1.endswith(str2,10,19))

#检测 str2是否包含在字符串str1中，如果指定范围 beg 和 end ，则检查是否包含在指定范围内，
#如果包含返回开始的索引值，否则返回-1
print('str1中是否包含str2:',str1.find(str2))
print('str1中是否包含str2(指定范围):',str1.find(str2,10,20))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">str1的长度: 20
str1以空格分割的结果: ['', '', 'Hello', 'world!', 'Hello']
str1删除首尾空格: Hello world! Hello
str2在str1中出现的次数: 2
str2在str1中出现的次数(指定范围): 1
str1是否以 str2结尾: True
str1是否以 str2结尾(指定范围): False
str1中是否包含str2: 2
str1中是否包含str2(指定范围): 15
</code></pre>
<h3 id="-8">列表</h3>
<p>列表是 Python 最基本，也是最重要的一种数据结构。列表用方括号 <code>[]</code> 定义，方括号括起的部分就是一个列表。Python 为列表提供了很多非常有用的内建方法，使用起来非常简单。</p>
<h4 id="-9">创建列表</h4>
<pre><code class="python language-python">#随意创建3个列表，同一个列表中可以存放任意基本数据类型
list1 = [3.14, 5.96, 1897, 2020, "China",3+4j];
list2 = [1, 2, 3, 4, 5 ];
list3 = ["BeiJing", "ShangHai", "NanJing", "GuangZhou"]; 
list4 = [] 
</code></pre>
<p>如上所示，列表中的数据项可以是不同的数据类型，如 list1，同时包含浮点型、整型、长整型、字符串和复数；也可以创建一个空列表，如 list4。</p>
<h4 id="-10">访问列表中的元素</h4>
<p>通过索引下标访问列表中的元素，可以一次访问一个或多个元素。</p>
<pre><code class="python language-python">#通过索引下标访问列表中的单个元素
print("list1[2]: ",list1[2]) 
print("list2[2]: ",list2[2])
print("list3[2]: ",list3[2])
#通过索引下标一次访问多个元素
print("list1[0:2]:",list1[0:2])
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">list1[2]:  1897
list2[2]:  3
list3[2]:  NanJing
list1[0:2]: [3.14, 5.96]
</code></pre>
<h4 id="-11">更改列表中的元素</h4>
<pre><code class="python language-python">list1 = [3.14, 5.96, 1897, 2020, "China",3+4j];
print("before list1[3]: ",list1[3]) 
list1[3] = "Change"
print("after list1[3]: ",list1[3])
</code></pre>
<p>执行结果：</p>
<pre><code>before list1[3]:  2020
after list1[3]:  Change
</code></pre>
<h4 id="-12">删除列表中的元素</h4>
<p>Python 提供三种删除列表中元素的方法：del、remove(obj)、clear()，分别用于删除列表中的元素和清空列表。如下例子:</p>
<pre><code class="python language-python">list1 = [3.14, 5.96, 1897, 2020, "China",3+4j];
print("Before the operation:",list1) 
del list1[3]
list1.remove(3+4j)
print("After deleting the element:",list1)
list1.clear()
print("After the emptying of the list:",list1)
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">Before the operation: [3.14, 5.96, 1897, 2020, 'China', (3+4j)]
After deleting the element: [3.14, 5.96, 1897, 'China']
After the emptying of the list: []
</code></pre>
<h4 id="-13">向列表中添加新元素</h4>
<p>有两个内建方法可以用于添加新元素：</p>
<ol>
<li>append(object)：添加新元素将新元素添加到列表末尾；</li>
<li>insert(index,object)：插入新元素到指定索引位置。</li>
</ol>
<p>如下例子：</p>
<pre><code class="python language-python">list1 = [3.14, 5.96, 1897, 2020, "China",3+4j];
print("before list1: ",list1) 
list1.append("New Ele-I")
list1.insert(2, "New Ele-II")
print("after list1: ",list1)
</code></pre>
<p>执行结果：</p>
<pre><code>before list1:  [3.14, 5.96, 1897, 2020, 'China', (3+4j)]
after list1:  [3.14, 5.96, 'New Ele-II', 1897, 2020, 'China', (3+4j), 'New Ele-I']
</code></pre>
<h4 id="-14">列表常用内建方法</h4>
<p>上面介绍了关于列表的“增、删、改、查”基本操作，除此之外，Python 列表还有很多内建函数和有趣的操作，接下来一一介绍。</p>
<pre><code class="python language-python">list1 = [2012, 1949, 1897, 2050, 1945, 1949];

#求列表长度，即列表中元素的个数:len(obj)
print("The length of the list: ", len(list1))

#求列表中元素的最大值：max(list)
print("The largest element in the list: ", max(list1))

#求列表中元素的最小值：min(list)
print("The smallest element in the list: ", min(list1))

#统计某个元素在列表中出现的次数：list.count(obj)
print("The number of times 1949 appears: ", list1.count(1949))

#从列表中找出某个值第一个匹配项的索引位置：list.index(obj)
print("The index of the first location of 1949: ", list1.index(1949))

#复制一个已有的表:list.copy()
list2 = list1.copy()
print("list2:", list2)

#反转一个已有的表:list.reverse()
list1.reverse()
print("After reversing :", list1)
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">The length of the list:  6
The largest element in the list:  2050
The smallest element in the list:  1897
The number of times 1949 appears:  2
The index of the first location of 1949:  1
list2: [2012, 1949, 1897, 2050, 1945, 1949]
After reversing : [1949, 1945, 2050, 1897, 1949, 2012]
</code></pre>
<h4 id="-15">列表常用操作</h4>
<p>为了高效的使用列表，Python 支持一些常用的操作：列表拼接、列表乘法、迭代、嵌套等。</p>
<pre><code class="python language-python">list1 = [1,2,3,4]
list2 = [5,6,"BeiJin",7,8]

#列表拼接
print("list1 + list2:",list1 + list2)

#列表乘法
print("list1*2:",list1*2)

#判断元素是否存在于列表中
print("3 in list1?",3 in list1)
print("100 in list1?",100 in list1)

#迭代
for element in list1:
print(element)

#列表嵌套
list3 = [list1, list2]
print("list3:", list3)
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">list1 + list2: [1, 2, 3, 4, 5, 6, 'BeiJin', 7, 8]
list1*2: [1, 2, 3, 4, 1, 2, 3, 4]
3 in list1? True
100 in list1? False
1
2
3
4
list3: [[1, 2, 3, 4], [5, 6, 'BeiJin', 7, 8]]
</code></pre>
<h3 id="-16">栈</h3>
<p>在上面“列表”小节中，我们介绍了列表，其中列表有两个内建函数：</p>
<ol>
<li>append(obj)：添加元素到列表尾部；</li>
<li>pop()：从列表尾部取出元素。</li>
</ol>
<p>不难理解，通过 append(obj) 函数最后添加的元素，可以通过 pop() 函数最先取出来，也就是“后进先出”，这种数据结构称为“栈”。利用列表的两个内建方法，很容易实现“栈”这种数据结构。</p>
<p>如下例子：</p>
<pre><code class="python language-python">#初始化一个列表
stack1 = [1, 2, 3, 4, 5 ]
#向表尾添加元素
stack1.append(123)  
print("stack1:",stack1)
#从表尾取出元素
print("stack1.pop():",stack1.pop())
</code></pre>
<p>执行结果：</p>
<pre><code>('stack1:', [1, 2, 3, 4, 5, 123])
('stack1.pop():', 123)
</code></pre></div></article>