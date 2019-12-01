---
title: Python 快速入门-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>通过前面两篇内容，我们学习了 Python 的基础知识。基于 Python 提供的数据结构和一些内建函数，我们已经可以实现一些简单的功能，但还不足以编写一个优雅的程序，这个问题将在本文得到解答。本文我们将学习 Python 的重要语句：if-else、for、while 等。</p>
<h3 id="ifelse">条件控制语句 if-else</h3>
<p>首先来看一个简单的例子：设计一个程序比较两个数 A 和 B 的大小，如果 A 和 B 不相等则打印较大数的值，如果相等则打印 A。</p>
<p>Python 代码如下：</p>
<pre><code class="python language-python">if A &gt;= B:
    print('The larger number is:',A) 
else:
    print('The larger number is:',B)
</code></pre>
<p>上面只是一个很简单的实例，一般地，Python 条件控制语句的形式为：</p>
<pre><code class="python language-python">if Condition1:
    Action1 
elif Condition2:
    Action2
else:
    Action3  
</code></pre>
<p>上面的代码表示：</p>
<ol>
<li>如果 Condition1 为True，将执行 Action1；</li>
<li>如果 Condition1 为False，将继续判断 Condition2；</li>
<li>如果 Condition2 为True，将执行 Action2；</li>
<li>如果 Condition2 为False，将执行 Action3。</li>
</ol>
<p><strong>注意要点</strong></p>
<ol>
<li>每个条件后面要使用冒号 <code>:</code>，冒号后的内容表示满足条件后要执行的语句块。</li>
<li>使用缩进来划分语句块，相同缩进数的语句在一起组成一个语句块（IDE 会自动缩进）。</li>
<li>在 Python 中没有 switch–case 语句。</li>
</ol>
<h3 id="">条件控制语句实例</h3>
<p>实例1：从控制台输入两个数字 A、B，判断大小后输出较大数字，如果相等则输出提示和数值。</p>
<pre><code class="python language-python">#从控制台输入数据默认为字符串类型，需要强制转换为int类型
A = int(input("Please enter the number A:"))
B = int(input("Please enter the number B:"))
if A &gt; B:
    print('The larger number is:',A) 
elif A == B:
    print('A and B are equal to ',A)  
else:
    print('The larger number is:',B) 
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">Please enter the number A:123
Please enter the number B:456
The larger number is: 456
</code></pre>
<p>实例2：从控制台输入学号，如果学号正确则输出考试成绩；如果学号有误，输出报错提示。</p>
<pre><code class="python language-python">#创建一个“学号-成绩”字典
exam_results = {'2018002':95,'2018013':'90','2018023':87}
#接收从控制台输入的学号，默认为字符串类型
stu_num = input("Please enter the student number:")
#删除输入学号首尾空格，避免影响查询
stu_num = stu_num.strip()
#判断输入的学号是否存在于“学号-成绩”字典中
if stu_num in exam_results.keys():
    print('Your score is :',exam_results.get(stu_num)) 
else:
    print('The student number you entered is incorrect!')  
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">Please enter the student number:2018002
Your score is : 95
</code></pre>
<h3 id="for">for 循环语句</h3>
<p>Python 中有两种循环语句，for 循环和 while 循环，本节先介绍 for 循环。一般，我们通过 for 循环来遍历序列中的项目，这里序列包括但不限于字符串、列表、元组、字典。</p>
<p>for循环的一般形式如下：</p>
<pre><code class="python language-python">for &lt;item&gt; in &lt;sequence&gt;:
    &lt;actions&gt;
</code></pre>
<p>当 <code>&lt;item&gt; in &lt;sequence&gt;</code> 为 True 时，执行 <code>&lt;actions&gt;</code>。</p>
<p>实例1：求一组数据的平均值。</p>
<pre><code class="python language-python">#测试数据集
num_set = [98,94,82,67,58,90,86]
sumOfNum = 0
#遍历列表中的元素，求和
for element in num_set:
    sumOfNum += element
#求平均值并打印结果    
average = sumOfNum/len(num_set)
print("The average is:%f"%(average))
</code></pre>
<p>执行结果：</p>
<pre><code class="python language-python">The average is:82.142857
</code></pre>
<p>实例2：通过 range() 函数遍历数据序列，range() 函数可以生成数列，将生成的数列作为索引，我们可以遍历数字序列。range() 函数的参数是可变的：</p>
<ol>
<li>range(n)：生成步长为1的数列：1，2，3……n；</li>
<li>range(m, n)：生成步长为1的数列：m，m+1，m+2，……，n；</li>
<li>range(m, n, s)：生成步长为s的数列：m，m+s，m+2s，……，X(&lt;=n)</li>
</ol>
<pre><code class="python language-python">for index in range(4):
    print("index:",index)
</code></pre>
<p>执行结果：</p>
<pre><code>index: 0
index: 1
index: 2
index: 3
</code></pre>
<p>实例3：for 循环结合 range() 遍历数据序列。</p>
<pre><code class="python language-python">#测试数据集
city_set = ['BeiJin','TianJin','ShangHai','HangZhou','SuZhou']
#索引从0开始，以步长2遍历
for index in range(0,len(city_set),2):
    print("city_set[%d]:%s"%(index,city_set[index]))
</code></pre>
<p>执行结果：</p>
<pre><code>city_set[0]:BeiJin
city_set[2]:ShangHai
city_set[4]:SuZhou
</code></pre>
<h3 id="while">while 循环</h3>
<p>与 for 循环不同，while 循环不是采用遍历数据序列的方式来进行循环操作的，其循环的依据是条件判断，while 循环的一般形式如下，即当 condition 为 True，则执行 Action，否则退出。</p>
<pre><code>while Conditon:
    Action
</code></pre>
<p>实例1：求一组数据的平均值。</p>
<pre><code class="python language-python">#初始化测试数据
num_set = [98,94,82,67,58,90,86]
sumOfNum = 0
index = 0

while index &lt; len(num_set):
    sumOfNum += num_set[index]
    index += 1
#求平均值并打印结果    
average = sumOfNum/len(num_set)
print("The average is:%f"%(average))
</code></pre>
<p>执行结果：</p>
<pre><code>The average is:82.142857
</code></pre>
<h3 id="break">break 语句</h3>
<p>break 语句用于跳出 for 和 while 循环体，也就意味着循环结束。</p>
<p>如下例子：检测数据集中是否存在小于60的数字，存在则打印提示信息并终止。</p>
<pre><code>#初始化测试数据
num_set = [98,94,82,67,58,90,86]
for i in range(len(num_set)):
    if num_set[i] &lt; 60:
        print("Someone failed!")
        break
    else:
        print(num_set[i])
</code></pre>
<p>执行结果：</p>
<pre><code>98
94
82
67
Someone failed!
</code></pre>
<p>在实际应用中，break 语句经常和 while 语句结合使用，当条件满足的时候跳出循环。如下例子：</p>
<pre><code>while True:
    a = input('Please enter a number:')
    if int(a) &gt; 100:
        print('error!!!')
        break
    else:
        print(a)
</code></pre>
<p>执行结果：</p>
<pre><code>Please enter a number:23
23
Please enter a number:45
45
Please enter a number:101
error!!!
</code></pre>
<h3 id="continue">continue 语句</h3>
<p>与 break 不同，continue 不会退出循环体，而是跳过当前循环块的剩余语句，继续下一轮循环。</p>
<p>如下例子：遍历数据集，遇到小于60的数据打印提示。</p>
<pre><code>#初始化测试数据
num_set = [98,94,82,67,58,90,86]
for i in range(len(num_set)):
    if num_set[i] &lt; 60:
        print("Someone failed!")
        continue
    print(num_set[i])
</code></pre>
<p>执行结果：</p>
<pre><code>98
94
82
67
Someone failed!
90
86
</code></pre>
<h3 id="pass">Pass 语句</h3>
<p>Python pass 是空语句，一般用做占位，不执行任何实际的操作，只是为了保持程序结构的完整性。为了直观，举一个不是很恰当的实例：</p>
<pre><code>#初始化测试数据
num_set = [98,82,67,58,90]
for i in range(len(num_set)):
    if num_set[i] &lt; 60:
        print("Someone failed!")
        pass
    print(num_set[i])
</code></pre>
<p>执行结果：</p>
<pre><code>98
82
67
Someone failed!
58
90
</code></pre>
<p>上面的例子可以看出，pass 语句没有执行任何操作。不过，在实际应用中，我们不会这样写代码，没有任何意义，pass 语句用于占位，如下例子，else 语句本来可以不写，但写上更为完整，这时候 pass 占位的意义就体现出来了。</p>
<pre><code>#初始化测试数据
num_set = [98,94,82,67,58,90,86]
for i in range(len(num_set)):
    if num_set[i] &lt; 60:
        print("Someone failed!")
    else:
        pass
</code></pre></div></article>