---
title: Python 快速入门-7
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在实际应用中，通常以函数作为一个基本的代码单元，对一组需求进行抽象，用于完成一项具体的任务。函数能提高应用的模块性和代码的重复利用率。在前面的文章中，我们已经接触到了 Python 提供的一些内建函数，比如 print()、sqrt()、append()、pop()。除了 Python 提供的内建函数，我们也可以自己创建函数，这种函数被称为用户自定义函数。</p>
<h3 id="">函数的定义与调用</h3>
<p>在 C/C++、Java 中，函数（方法）的定义形式如下：</p>
<pre><code class="java language-java">修饰符1，修饰符2，…，返回值类型，函数名（参数列表）
public static String getPath(String basePath, String fileName)
</code></pre>
<p>Python 中函数的定义则“简洁”得多，Python 函数无需声明返回值类型，也无需修饰符，一般地，函数的定义形式如下：</p>
<pre><code class="python language-python">函数定义符，函数名（参数列表）
def getPath(basePath, fileName):
def getName():
</code></pre>
<p>基于前一篇文章 Python 基础的知识储备，在此，直接以一个简单的比较函数 compare() 来举例介绍，下面的代码中定义了一个比较函数，并执行了3次调用。</p>
<pre><code class="python language-python">#定义函数
def compare(parameter1, parameter2):
    if (parameter1 &gt; parameter2):
        print(1)
    elif (parameter1 == parameter2):
        print(0)
    else:
        print(-1)

#调用函数
compare(123,456)
compare(3.14,1.5)
compare(12,12.1)
</code></pre>
<p>执行结果：</p>
<pre><code>-1
1
-1
</code></pre>
<h3 id="-1">参数传递</h3>
<h4 id="-2">变量与引用</h4>
<p>在 Python 中，所有类型：函数、模块、数字、字符串、列表、元组、字典等等都是对象，<strong>而变量是没有类型的</strong>，怎么理解呢？请看如下实例：</p>
<pre><code>a = 12
print("a=", a)
a = "ABCDE"
print("a=", a)
a = [1,2,3,4,5]
print("a=", a)
a = (1,2,3,4)
print("a=", a)
a = {'key':12,'key1':13}
print("a=", a)
</code></pre>
<p>执行结果：</p>
<pre><code>a= 12
a= ABCDE
a= [1, 2, 3, 4, 5]
a= (1, 2, 3, 4)
a= {'key': 12, 'key1': 13}
</code></pre>
<p>从上面的例子可以看出，同一段代码中，同一个变量 a 先后被赋值整数、字符串、列表等多种类型，这是因为变量本身没有类型，它仅仅只是一个对象的引用（指针），它可以引用任何类型，上面例子中，变量 a 先后引用多种数据类型，本质上也仅仅是改变指向而已。</p>
<h4 id="-3">不可变类型</h4>
<p>上文提及，变量没有类型，仅仅作为对象的引用，我们可以在深化一下，如下例子：</p>
<pre><code>a = 12
a = 15
</code></pre>
<p>上述过程的实质就是：首先创建一个对象 12，让 a 指向它，然后再创建一个对象 15，再让 a 指向后者，而前者12就被丢弃。这个过程是通过创建新的对象来实现的，并不是直接改变 a 的值，一定要理解其中区别。</p>
<p>这种只能通过创建新的对象才能改变对变量的赋值的数据类型，称为<strong>不可变类型</strong>，如整数、字符串、元组都是不可变类型。再来看一个例子：</p>
<pre><code>def change(x):
    x = 10

a = 5
change(a)
print("a=",a)
</code></pre>
<p>执行结果：</p>
<pre><code>a= 5
</code></pre>
<p>调用 change() 函数并没有改变变量 a 的内容，这是因为，定义了一个变量 a，a 指向数字 5，然后执行 change 函数，是复制 a 到 x，刚开始 x 也指向数字5，在函数体内执行 x=10，由于整数是不可变对象，所以将创建一个新的对象 10，并将 10 赋值给 x 变量，此时 x 指向10，而 a 本身并没有发生改变，仍然指向5。</p>
<p>在 Python 中，对于不可变对象，调用自身的任意方法，并不会改变对象自身的内容，这些方法会创建新的对象并返回，保证了不可变对象本身是永远不可变的。</p>
<h4 id="-4">可变类型</h4>
<p>与不可变类型相对就是可变类型，包括列表、字典、集合、队列等。如下例子：</p>
<pre><code>def change(x):
    x.append(2012)

a = [1,2,3,4]
change(a)
print("a=",a)
</code></pre>
<p>执行结果：</p>
<pre><code>a= [1, 2, 3, 4, 2012]
</code></pre>
<p>很明显，a 发生了改变，原因分析：执行 change() 方法时，x 指向列表 <code>[1,2,3,4]</code>，因为列表是可变对象，执行 x.append(5) 时，并不会产生新的对象，而是直接作用在原来列表对象 <code>[1,2,3,4]</code>上，进而列表对象改变为 <code>[1，2,3,4,5]</code>。</p>
<h3 id="-5">函数的参数类型</h3>
<p>Python 中，函数的参数有四种类型：必须参数、关键字参数、默认参数和不定长参数。</p>
<h4 id="-6">必须参数</h4>
<p>函数在定义的时候，已经声明了参数的数量，我们在调用函数的时候，参数的数量必须与声明时一致，且要注意顺序。</p>
<p>实例1：参数数量要对应。</p>
<pre><code>#声明参数为一个
def update(arg):
    arg = arg + 1

#正确
update(12)
#不正确，参数缺失
update()
#不正确，参数多余
update(1,2)
</code></pre>
<p>实例2：参数顺序要一致。</p>
<pre><code>def printInfo(name, sex, age):
    print("name:",name)
    print("sex:",sex)
    print("age:",age)

#正确
printInfo("Jack","female", 18)
#错误，参数顺序不对应
printInfo(18,"Jack","female")
</code></pre>
<h4 id="-7">关键字参数</h4>
<p>上面已经提到，调用函数时，不仅参数数量要相等，还要顺序匹配。在 Python 中，还有一种方式可以更灵活的匹配参数：函数调用使用关键字参数来确定传入的参数值。</p>
<p>如下实例：</p>
<pre><code>def printInfo(name, sex, age):
    print("name:",name)
    print("sex:",sex)
    print("age:",age)

#都是正确的
printInfo(name="Jack",sex="female",age=18)
printInfo(sex="female",name="Jack",age=18)
printInfo(sex="female",age=18,name="Jack")
</code></pre>
<h4 id="-8">默认参数</h4>
<p>有些场景下，如果调用函数时，参数错误可能会导致不可预期的严重后果，因此，为了增强函数的适应性和容错性，可以采取一种策略：调用函数时，如果没有传递参数，则会使用默认参数。如下实例：</p>
<pre><code>#声明参数为一个
def printInfo(name, sex, age=0):
    print("name:",name)
    print("sex:",sex)
    print("age:",age)

#正确
printInfo(name="Jack",sex="female")
</code></pre>
<h4 id="-9">不定长参数</h4>
<p>有些场景下，我们希望设计一个参数数量不确定的函数，如任意个整数求和，调用形式可以是：sum(a)、sum(a,b,c)、sum(a,b,c,d)……，这时候我们需要使用一种不定长参数，一般定义形式如下：</p>
<pre><code>def functionname([formal_args,] *var_args_tuple ):
    functionbody
</code></pre>
<p>加了（*）的变量名会存放所有未命名的变量参数。如果在函数调用时没有指定参数，它就是一个空元组。我们也可以不向函数传递未命名的变量。如下实例：</p>
<pre><code>#定义一个求和函数
def sum(num, *num_list):
    sum = num
    for element in num_list:
        sum += element
    print("sum=",sum)

sum(1)
sum(1,2,3,4)
</code></pre>
<p>执行结果：</p>
<pre><code>sum= 1
sum= 10
</code></pre>
<h3 id="return">Return 语句</h3>
<p>return [表达式] 语句用于退出函数，选择性地向调用方返回一个表达式。不带参数值的 return 语句返回 None，表示没有任何值。如果函数没有显式的使用 return 语句，Python 函数也会默认返回 None 对象。</p>
<pre><code>#定义比较函数
def compare(parameter1, parameter2):
    if (parameter1 &gt; parameter2):
        return 1
    elif (parameter1 == parameter2):
        return 0
    else:
        return -1

result = compare(123,456)
print("result=",result)
</code></pre>
<p>执行结果：</p>
<pre><code>result= -1
</code></pre>
<h4 id="-10">变量作用域</h4>
<p>在前面章节的学习中，读者应该注意到一个问题，变量的使用非常多，有些地方甚至同名，那么，它们会不会冲突呢？实例如下：</p>
<pre><code>#这里的 a 是全局变量
a = 123
def function():
    a = 10 #这里的 a 是局部变量
    print("I a=",a)

function()
print("II a=",a)
</code></pre>
<p>执行结果：</p>
<pre><code>I a= 10
II a= 123
</code></pre>
<p>上述实例可见，同名的变量并没有发生冲突，这是因为它们的“作用域”不同，变量只在自己的作用域内有效，a=123 处属于全局变量，function() 函数内部 a=10 属于局部变量，作用域不同，因此并不会冲突。</p>
<p><strong>作用域分类</strong></p>
<p>按作用域不同，变量可分为四种类型：L（Local），局部作用域；E（Enclosing），闭包函数外的函数中；G（Global），全局作用域；B（Built-in），内建作用域；</p>
<p>使用变量时，会根据作用域进行查找，优先级顺序为：L –&gt; E –&gt; G –&gt;B，即在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内建中找。关于变量作用域的更多内容可查看<a href="https://www.jianshu.com/p/3bb277c2935c">博文《Python 变量作用域》</a>。</p></div></article>