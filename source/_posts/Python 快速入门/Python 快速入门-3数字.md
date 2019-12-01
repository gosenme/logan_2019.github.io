---
title: Python 快速入门-3
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">数字</h3>
<p>Python 提供了三种数字类型，即 int（整型），float（浮点型），complex（复数）。</p>
<ol>
<li>int：通常被称为整型或者整数，如100、99、1、3都属于整型；</li>
<li>float：浮点数包含整数和小数部分，如3.1415，12.578712；</li>
<li>complex：复数包含实数部分和虚数部分，形如 a+bj，其实部和虚部都是浮点类型。</li>
</ol>
<p>需要注意的是，Python3 已经废弃了 Python2 的 Long（长整型），在 Python3 中，int 的大小没有限制，可以作为 Long 使用。</p>
<h4 id="-1">数字类型转换</h4>
<p>Python 的三种数字类型可以进行相互转换，转换方式为：数字类型+圆括号，如下实例：</p>
<pre><code class="python language-python">a = 123
b = 3.1415926

print("int(b)=",int(b))
print("float(a)=",float(a))
print("complex(a)=",complex(a))
print("complex(a,b)=",complex(a,b))
</code></pre>
<p>执行结果：</p>
<pre><code>int(b)= 3
float(a)= 123.0
complex(a)= (123+0j)
complex(a,b)= (123+3.1415926j)
</code></pre>
<h4 id="-2">常用的数学函数</h4>
<p>Python 提供了丰富的数学函数以降低编程实现的难度，本节将介绍一些常用的函数。</p>
<pre><code class="python language-python">import math
#求绝对值:abs(x)
print("abs(-12)=",abs(-12))

#向上取整:ceil(x)
print("ceil(3.1415)=",math.ceil(3.1415))

#向下取整:floor(x)
print("floor(3.678)=",math.floor(3.678))

#四舍五入:round(x)
print("round(3.678)=",round(3.678))

#乘方运算:pow(x,y),x的y次方
print("pow(3,4)=",pow(3,4))

#求平方根:sqrt(x)
print("sqrt(144)=",math.sqrt(144))
</code></pre>
<p>执行结果：</p>
<pre><code>abs(-12)= 12
ceil(3.1415)= 4
floor(3.678)= 3
round(3.678)= 4
pow(3,4)= 81
sqrt(144)= 12.0
</code></pre>
<h3 id="-3">运算符</h3>
<p>计算机的最基本用途之一就是执行数学运算，作为一门计算机语言，Python 也提供了一套丰富的运算符来满足各种运算需求。</p>
<p>Python 运算符大致可分为7种，即算术运算符、比较运算符、赋值运算符、逻辑运算符、位运算符、成员运算符以及身份运算符。</p>
<h4 id="-4">算术运算符</h4>
<p>对算术运算，大家并不陌生，常用的加减乘除就是算术运算。不过，在编程语言里，算术运算的符号特殊一些，Python 中的算术运算有7种：加（+）、减（-）、乘（ * ）、除（/）、取模（%）、幂运算（ ** ）和取整预算（//）。以下通过实例演示算术运算符的用法。</p>
<pre><code class="python language-python">#初始化测试数据
X = 24
Y = 5
Z = 0
#分别进行7种算术运算
Z = X + Y 
print("X + Y =", Z)
Z = X - Y 
print("X - Y =", Z)
Z = X * Y 
print("X * Y =", Z)
Z = X / Y 
print("X / Y =", Z)
Z = X % Y 
print("X % Y =", Z)
Z = X ** Y 
print("X ** Y =", Z)
Z = X // Y 
print("X // Y =", Z)
</code></pre>
<p>执行结果：</p>
<pre><code>X + Y = 29
X - Y = 19
X * Y = 120
X / Y = 4.8
X % Y = 4
X ** Y = 7962624
X // Y = 4
</code></pre>
<h4 id="-5">比较运算符</h4>
<p>比较无处不在，大于、小于、等于、不等于……和 C/C++、Java 等编程语言一样，Python 也提供了6种比较运算符：&gt;（大于），<（小于），==（等于），！=（不等于)，>=（大于等于），&lt;=（小于等于）。比较运算的结果是一个布尔值，True 或者 False，如下实例：</p>
<pre><code class="python language-python">#初始化测试数据
X = 24
Y = 5
#分别进行7种比较运算
print("X == Y:", X == Y)
print("X != Y:", X != Y)
print("X &gt; Y:", X &gt; Y)
print("X &lt; Y:", X &lt; Y)
print("X &gt;= Y:", X &gt;= Y)
print("X &lt;= Y:", X &lt;= Y)
</code></pre>
<p>执行结果：</p>
<pre><code>X == Y: False
X != Y: True
X &gt; Y: True
X &lt; Y: False
X &gt;= Y: True
X &lt;= Y: False
</code></pre>
<h4 id="-6">赋值运算</h4>
<p>在前文的实例中已经用到赋值运算，如 X = 25，就是一个最简单的赋值运算，“=”就是最简单的赋值运算符。将简单的赋值运算与算术运算结合，Python 形成了丰富的赋值运算符：+=、-=、<em>=、/=、%=、</em>*=、//=。实例如下：</p>
<pre><code class="python language-python">#初始化测试数据
X = 2
Y = 3
#分别进行7种赋值运算
Y = X 
print("Y = X, Y =", Y)
Y += X 
print("Y += X, Y =", Y)
Y -= X 
print("Y -= X, Y =", Y)
Y *= X 
print("Y *= X, Y =", Y)
Y /= X 
print("Y /= X, Y =", Y)
Y **= X 
print("Y **= X, Y =", Y)
Y //= X 
print("Y //= X, Y =", Y)
</code></pre>
<p>执行结果：</p>
<pre><code>Y = X, Y = 2
Y += X, Y = 4
Y -= X, Y = 2
Y *= X, Y = 4
Y /= X, Y = 2.0
Y **= X, Y = 4.0
Y //= X, Y = 2.0
</code></pre>
<h4 id="-7">逻辑运算</h4>
<p>所谓逻辑运算，就是：与、或、非。Python 中3种逻辑运算符分别为：and（与），or（或），not（非），逻辑运算的结果是布尔值：True 或者 False。</p>
<ol>
<li>A and B：当 A 为 False 时，运算结果为 False；否则返回 B 的值；</li>
<li>A or B：当 A 为 True 时，运算结果为 A 的值，否则返回 B 的值；</li>
<li>not A：当 A 为 True 时，返回 False，否则返回 True。</li>
</ol>
<p>如下实例：</p>
<pre><code class="python language-python">#初始化测试数据
X = 2
Y = 3
Z = 5
#分别执行3种逻辑运算
print("X&gt;Y and X&lt;Z :", X&gt;Y and X&lt;Z)
print("X&lt;Y and Z :", X&lt;Y and Z)
print("X&gt;Y or Z :", X&gt;Y or X&lt;Z)
print("X&lt;Y or Z :", X&lt;Y or Z)
print("X or X&lt;Z :", X or X&lt;Z)
print("not X :", not X)
print("not X&lt;Y :", not X&lt;Y)
</code></pre>
<p>执行结果：</p>
<pre><code>X&gt;Y and X&lt;Z : False
X&lt;Y and Z : 5
X&gt;Y or Z : True
X&lt;Y or Z : True
X or X&lt;Z : 2
not X : False
not X&lt;Y : False
</code></pre>
<h4 id="-8">位运算</h4>
<p>程序中的所有数在计算机内存中都是以二进制的形式储存的。位运算就是直接对整数在内存中的二进制位进行操作。Python 中有6种位运算符：</p>
<ol>
<li>&amp;：按位与运算符，参与运算的两个值，如果两个相应位都为1，则该位的结果为1，否则为0；</li>
<li>|：按位或运算符，只要对应的二个二进位有一个为1时，结果位就为1；</li>
<li>^：按位异或运算符，当两对应的二进位相异时，结果为1；</li>
<li>~：按位取反运算符，对数据的每个二进制位取反，即把1变为0，把0变为1；</li>
<li><code>&gt;&gt;</code>：右移动运算符，把 <code>&gt;&gt;</code> 左边的运算数的各二进位全部右移若干位，<code>&gt;&gt;</code> 右边的数指定移动的位数；</li>
<li><code>&lt;&lt;</code>：左移动运算符，运算数的各二进位全部左移若干位，由 <code>&lt;&lt;</code> 右边的数指定移动的位数，高位丢弃，低位补0。</li>
</ol>
<p>举个例子：a=21，b=6，将两个数转换为二进制形式进行位运算。</p>
<pre><code class="python language-python">a = 0001 0101
b = 0000 0110

a&amp;b = 0000 0100
a|b = 0001 0111
a^b = 0001 0011
~a = 1110 1010
a&lt;&lt;2 = 01010100
a&gt;&gt;2 = 0000 0101
</code></pre>
<h4 id="-9">成员运算</h4>
<p>除了上文介绍的5种运算符，Python 还支持成员运算符。介绍成员运算符之前，我们需要提前了解一个概念：<strong>数据结构</strong>，如字符串、列表、元组、字典。在接下来的章节中我们将详细介绍这些基础的数据结构。字符串、列表、字典，它们就像一个集合，其中包含若干元素，这些元素就是集合的成员；对于一个给定的元素，它有可能在一个给定的集合中，也可能不在，Python 中采用成员运算符来判断元素是否属于成员，成员运算的结果为布尔值，True 或者 False。</p>
<p>如下实例：</p>
<pre><code class="python language-python">#初始化一个字符串和列表
temp1 = "ABCDEFG"
temp2 = [4,2,3,5,8,9]
a = "CDE"
b = 5
c = "CDF"
print("a in temp1?", a in temp1)
print("b in temp2?", b in temp2)
print("c in temp1?", c in temp1)
</code></pre>
<p>执行结果：</p>
<pre><code>a in temp1? True
b in temp2? True
c in temp1? False
</code></pre>
<h4 id="-10">身份运算符</h4>
<p>身份运算符用于比较两个标识符所引用对象的存储单元，计算结果为布尔值，包含两个运算符：is 和 is not，分别用于判断两个标识符是否引用自一个对象。关于存储单元的比较，涉及到对内存模型的理解，本节不做详述，留到后面章节介绍。</p></div></article>