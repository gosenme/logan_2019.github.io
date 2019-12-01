---
title: Python 快速入门-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">元组</h3>
<p>在上一篇文章中我们介绍了列表，本文将介绍与列表类似的一种数据结构：元组。Python 的元组与列表有很多类似的地方，但区别也是很明显的：</p>
<ol>
<li>定义方式不一样：列表采用方括号 <code>[]</code>，元组采用圆括号 <code>()</code>；</li>
<li>元组中的元素不能改变，元组一旦创建就不能再对其中的元素进行增、删、改，只能访问。</li>
</ol>
<h4 id="-1">创建元组</h4>
<pre><code class="python language-python">#创建3个元组，和列表类似，同一个元组中可以存放任意数据类型
tuple1 = ()
tuple2 = (12,)
tuple3 = (1, 2, 3, 4, 5)
tuple4 = (3.14, 5.96, 1897, 2020, "China",3+4j) 
tuple5 = 4,5,6,7
</code></pre>
<p>如上所示，元组和列表类似，同一个元组中可以没有数据，也可以有多种数据，非常灵活。</p>
<p>不过需要注意：</p>
<ol>
<li>如果元组只有一个元素，那么这个元素后面要加逗号，如 tuple2，否则将被认为是一个基本数据类型，而不是元组；</li>
<li>创建元组，可以没有括号，元素之间用逗号分隔开即可。</li>
</ol>
<h4 id="-2">访问元组中的元素</h4>
<p>元组和列表都是一种序列，因此，也可以通过索引来访问，方法是一样的，如下例子：</p>
<pre><code class="python language-python">tuple1 = (3.14, 5.96, 1897, 2020, "China",3+4j) 
print("tuple1[2]:",tuple1[2])
print("tuple1[1:3]:",tuple1[1:3])
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">tuple1[2]: 1897
tuple1[1:3]: (5.96, 1897)
</code></pre>
<h4 id="-3">元组相关的常用内建方法</h4>
<pre><code class="python language-python">tuple1 = (3.14, 5.96, 1897, 2020, 1949) 

#求元组长度，即元组中元素的个数:len(tuple)
print("The length of the tuple: ", len(tuple1))

#求元组中元素的最大值：max(tuple)
print("The largest element in the tuple: ", max(tuple1))

#求元组中元素的最小值：min(tuple)
print("The smallest element in the tuple: ", min(tuple1))

#统计某个元素在元组中出现的次数：tuple.count(obj)
print("The number of times 1949 appears: ", tuple1.count(1949))

#从元组中找出某个值第一个匹配项的索引位置：tuple.index(obj)
print("The index of the first location of 1949: ", tuple1.index(1949))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">The length of the tuple:  5
The largest element in the tuple:  2020
The smallest element in the tuple:  3.14
The number of times 1949 appears:  1
The index of the first location of 1949:  4
</code></pre>
<h4 id="-4">元组常用的操作</h4>
<p>元组常用的运算操作与列表相同，包括：元组拼接、元组乘法、迭代、嵌套等。简要举例如下：</p>
<pre><code class="python language-python">tuple1 = (1,2,3,4)
tuple2 = (5,6,"BeiJin",7,8)

#元组拼接
print("tuple1 + tuple2:",tuple1 + tuple2)

#元组乘法
print("tuple1*2:",tuple1*2)

#判断元素是否存在于元组中
print("3 in tuple1?",3 in tuple1)
print("100 in tuple1?",100 in tuple1)

#迭代
for element in tuple1:
print(element)

#元组嵌套
tuple3 = [tuple1, tuple2]
print("tuple3:", tuple3)
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">tuple1 + tuple2: (1, 2, 3, 4, 5, 6, 'BeiJin', 7, 8)
tuple1*2: (1, 2, 3, 4, 1, 2, 3, 4)
3 in tuple1? True
100 in tuple1? False
1
2
3
4
tuple3: [(1, 2, 3, 4), (5, 6, 'BeiJin', 7, 8)]
</code></pre>
<h3 id="-5">字典</h3>
<p>Python 的字典可以理解为一种映射表，存储 key-value（键值对）类型数据的容器。关于字典有三点需要注意：</p>
<ol>
<li>同一个字典中，键必须是唯一的，不存在两个相同的键，键的值不能改变，数据类型可以是数字，字符串或者元组；</li>
<li>同一个字典中，值不必唯一，值可以是任意数据类型；</li>
<li>字典定义采用花括号 {}，键值之间用冒号隔开，键值对之间用逗号隔开；</li>
</ol>
<h4 id="-6">创建字典</h4>
<pre><code class="python language-python">#创建几个字典
dict1 = {"ID0012":"ZhangSan", "ID0019":"LiSi", "ID0015":"WangWu"}
dict2 = {1:"BeiJin",3:"ShangHai",5:"HangZhou"}
dict3 = {"Excellent":100, "Good":80, "Pass":60, "Fail":50}
#字典也可以嵌套
dict4 = {"A":["LiTong","XiaoMing"], "B":["XiaoHong","XiaoHua"]}
</code></pre>
<h4 id="-7">访问字典中的元素</h4>
<p>与列表和元组不同，访问字典中的元素不能通过索引，字典中键和值是成对的，而键是唯一的，那么，通过键就可以访问对应的值。</p>
<p>访问有两种方式：</p>
<ol>
<li>直接通过键来访问；</li>
<li>通过内建 get(key) 方法访问。</li>
</ol>
<p>如下例子：</p>
<pre><code class="python language-python">dict1 = {"Excellent":100, "Good":80, "Pass":60, "Fail":50}
dict2 = {1:"BeiJin",3:"ShangHai",5:"HangZhou"}
print("dict1['Good']:", dict1['Good'])
print("dict2[1]:", dict2[1])
print("dict1.get('Good'):", dict1.get('Good'))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">dict1['Good']: 80
dict2[1]: BeiJin
dict1.get('Good'): 80
</code></pre>
<h4 id="-8">修改字典中的元素</h4>
<pre><code class="python language-python">dict1 = {"Excellent":100, "Good":80, "Pass":60, "Fail":50}
dict1['Good'] = 85
print("dict1['Good']:", dict1.get('Good'))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">dict1['Good']: 85
</code></pre>
<h4 id="-9">删除字典中的元素或字典</h4>
<p>和列表一样，可以通过 del 语句删除字典中的元素或者删除整个字典，可以通过内建方法 clear() 清空字典，还可以通过内建方法 pop(key) 删除指定的元素，如下例子：</p>
<pre><code class="python language-python">dict1 = {"Excellent":100, "Good":80, "Pass":60, "Fail":50}

#删除字典中的一个元素
del dict1['Good']
print("dict1:", dict1)

#使用内建方法pop(key)删除指定元素
dict1.pop('Pass')
print("dict1:", dict1)

#清空字典
dict1.clear()
print("dict1:", dict1)

#删除字典
del dict1
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">dict1: {'Excellent': 100, 'Pass': 60, 'Fail': 50}
dict1: {'Excellent': 100, 'Fail': 50}
dict1: {}
</code></pre>
<h4 id="-10">字典的常用内建方法</h4>
<pre><code class="python language-python">dict1 = {"Excellent":100, "Good":80, "Pass":60, "Fail":50}

#计算字典的长度
print("The length of the dict1: ", len(dict1))

#获取字典中所有的键
print("Get all the keys in dict1:\n", dict1.keys())

#获取字典中所有的值
print("Get all the values in dict1:\n", dict1.values())

#获取字典中所有的键值对
print("Get all the key-value pairs in dict1:\n", dict1.items())
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">The length of the dict1:  4
Get all the keys in dict1:
 dict_keys(['Excellent', 'Good', 'Pass', 'Fail'])
Get all the values in dict1:
 dict_values([100, 80, 60, 50])
Get all the key-value pairs in dict1:
 dict_items([('Excellent', 100), ('Good', 80), ('Pass', 60), ('Fail', 50)])
</code></pre>
<h3 id="-11">集合</h3>
<p>集合（set）是一个数学概念，是由一个或多个确定的元素所构成的整体。</p>
<p>集合具有三个特点：</p>
<ol>
<li>确定性，集合中的元素必须是确定的； </li>
<li>互异性，集合中的元素互不相同；</li>
<li>无序性，集合中的元素没有先后之分。</li>
</ol>
<p>根据集合的特点，Python 中集合的基本功能包括关系测试和消除重复元素。</p>
<h4 id="-12">创建集合</h4>
<p>可以用大括号（{}）创建集合。但需要注意，如果要创建一个空集合，必须用 set() 而不是 {} ；后者创建一个空的字典。</p>
<pre><code>country1 = {'China', 'America', 'German'}
country2 = set('China')
country3 = set()

print("country1:",country1)
print("country2:",country2)
print("country3:",country3)
</code></pre>
<p>执行结果：</p>
<pre><code>('country1:', set(['German', 'America', 'China']))
('country2:', set(['i', 'h', 'C', 'a', 'n']))
('country3:', set([]))
</code></pre>
<h4 id="-13">操作集合中的元素</h4>
<p>我们可以访问集合中的元素，也可增加，移除元素。</p>
<pre><code>setA = {'A', 'B', 'C'}

print("setA:",setA)
setA.add('D')
print("setA.add('D'):",setA)
setA.add('A')
print("setA.add('A'):",setA)
setA.remove('A')
print("setA.remove('A'):",setA)
</code></pre>
<p>执行结果：</p>
<pre><code>('setA:', set(['A', 'C', 'B']))
("setA.add('D'):", set(['A', 'C', 'B', 'D']))
("setA.add('A'):", set(['A', 'C', 'B', 'D']))
("setA.remove('A'):", set(['C', 'B', 'D']))
</code></pre>
<h4 id="-14">集合运算</h4>
<p>对于集合，我们可以计算交集、并集、补集。</p>
<pre><code>setA = {'A', 'B', 'C'}
setB = {'D', 'C', 'E'}

#交集
print("setA &amp; setB:",setA&amp;setB)

#并集
print("setA | setB:",setA|setB)

#差集
print("setA - setB:",setA-setB)
</code></pre>
<p>执行结果：</p>
<pre><code>('setA &amp; setB:', set(['C']))
('setA | setB:', set(['A', 'C', 'B', 'E', 'D']))
('setA - setB:', set(['A', 'B']))
</code></pre>
<h3 id="-15">队列</h3>
<p>前面已经介绍过列表，结合其内建函数 append(obj) 和 pop()，可以直接将列表作为栈使用。本节将介绍另一种数据结构——队列，即“先进先出”，就像排队打饭，队头的人先打到饭，队尾的人最后。Python 中有专门的队列模块 Queue，本节介绍一种用列表实现的队列，如下例子：</p>
<pre><code>from collections import deque

#基于列表初始化一个队列
queue = deque(['A','B','C'])
#队尾添加元素
queue.append('D')
print('queue',queue)
#队头出列
queue.popleft()
print('queue',queue)
#队头出列
queue.popleft()
print('queue',queue)
</code></pre>
<p>执行结果：</p>
<pre><code>('queue', deque(['A', 'B', 'C', 'D']))
('queue', deque(['B', 'C', 'D']))
('queue', deque(['C', 'D']))
</code></pre></div></article>