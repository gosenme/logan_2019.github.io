---
title: Python 快速入门-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>没有完美的程序，就如同没有完美的人，程序执行时有可能出错。一旦出错，严重可导致程序崩溃，造成不可预期的破坏。不过，并不是所有的错误都是致命的，我们并不希望自己的程序因一些非致命错误而终止，而是希望能用一种相对“和谐”的方式来处理这些错误。在 Python 中，可以将出错归为两类：错误（Errors）和异常（Exceptions）。</p>
<h3 id="">错误</h3>
<p>从软件方面来说，一般将错误分为两种：语法错误、逻辑错误。</p>
<p><strong>语法错误</strong>，指的是程序不符合编程语言的语法规范，进而导致不能被解释器解释或者编译器无法编译。这些错误违背了语法规则，必须在程序执行前纠正，属于比较低级的错误，在编写程序时，可借助 IDE 进行语法检测，避免错误流到下游。举一个官网提供的例子：</p>
<pre><code>#少了一个冒号：
while True
    print("hello world!")
</code></pre>
<p>运行结果：</p>
<pre><code>    while True
             ^
SyntaxError: invalid syntax
</code></pre>
<p><strong>逻辑错误</strong>，在编程时没有充分考虑应用场景，导致程序逻辑不完整，或者输入不合法等。这类错误通常会导致程序无法达成期望的结果，在编程前应该通过周密的设计进行避免。</p>
<pre><code>#比较两个数，返回较大值，漏掉了相等的情况
def compare(num1, num2):
    if (num1 &gt; num2):
        return num1
    elif (num1 &lt; num2):
        return num2

print("result:",compare(12, 12))
</code></pre>
<p>运行结果：</p>
<pre><code>result: None
</code></pre>
<h3 id="-1">异常</h3>
<p>异常是在程序运行中产生的，大多数的异常都不会被程序处理，并以错误信息的形式抛出，Python 中常见的异常有：</p>
<table>
<thead>
<tr>
<th>异常名称</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>ZeroDivisionError</td>
<td>除数为0</td>
</tr>
<tr>
<td>AttributeError</td>
<td>试图访问一个对象没有的属性，比如foo.x，但是foo没有属性x</td>
</tr>
<tr>
<td>IOError</td>
<td>输入/输出异常；常见原因是无法打开文件</td>
</tr>
<tr>
<td>ImportError</td>
<td>无法引入模块或包；常见原因是路径问题或名称错误</td>
</tr>
<tr>
<td>IndentationError</td>
<td>语法错误（的子类）；常见原因是代码没有正确对齐</td>
</tr>
<tr>
<td>IndexError</td>
<td>下标索引超出序列边界，比如当x只有三个元素，却试图访问x[5]</td>
</tr>
<tr>
<td>KeyError</td>
<td>试图访问字典里不存在的键</td>
</tr>
<tr>
<td>KeyboardInterrupt</td>
<td>Ctrl+C被按下</td>
</tr>
<tr>
<td>NameError</td>
<td>使用一个还未被赋予对象的变量</td>
</tr>
<tr>
<td>TypeError</td>
<td>传入对象类型与要求的不符合</td>
</tr>
<tr>
<td>UnboundLocalError</td>
<td>试图访问一个还未被设置的局部变量，常见原因是由于另有一个同名的全局变量，导致你以为正在访问它</td>
</tr>
<tr>
<td>ValueError</td>
<td>传入一个调用者不期望的值，即使值的类型是正确的</td>
</tr>
</tbody>
</table>
<p><strong>举个例子：</strong></p>
<pre><code>num_list = [12,34,56,78,90]
print(num_list[14])
</code></pre>
<p>执行结果：</p>
<pre><code>    print(num_list[14])
IndexError: list index out of range
</code></pre>
<h3 id="-2">异常的处理</h3>
<p>对于非致命异常，可以不终止程序，取代以“和谐”的处理方式来解决：捕获程序运行中出现的异常，并针对这种异常进行特定的处理，使程序得以继续执行而不至于终止。实例如下：</p>
<pre><code>def compare(num1, num2):
    try:           
        if(num1 &gt;= num2):
            return num1
        else:
            return num2
    except:
        return "ERROR"

#正确的调用
print("compare(12,34):",compare(12,34))
#异常的调用
print("compare(12,'ab'):",compare(12,'ab'))
print("compare('12',34):",compare('12',34))
</code></pre>
<p>执行结果：</p>
<pre><code>compare(12,34): 34
compare(12,'ab'): ERROR
compare('12',34): ERROR
</code></pre>
<p>很明显，程序没有因异常调用而终止，因为我们使用 try-except 语句捕获了 TypeError，从而避免程序异常终止。try-except 这种异常处理机制可以让程序在不牺牲可读性的前提下增强健壮性和容错性，try-except 语句的一般形式如下。</p>
<pre><code>#指定捕获某种异常，并对其进行处理(except子句负责处理)
try:
    &lt;statement-1&gt;
    .
    &lt;statement-N&gt;
except ErrorType:
    &lt;statement-x&gt;
    .
    &lt;statement-y&gt;

#同时捕获多种指定异常，多个异常需要用括号括起来
try:
    &lt;statement-1&gt;
    .
    &lt;statement-N&gt;
except (ErrorType1,ErrorType2,…,ErrorTypeN):
    &lt;statement-x&gt;
    .
    &lt;statement-y&gt;
#不指定异常，默认捕获所有异常，如果对于一段代码，你不清楚会出现什么异常，或者出现多种异常而不需要分别处理，可以采用这种方式，捕获所有异常。
try:
    &lt;statement-1&gt;
    .
    &lt;statement-N&gt;
except:
    &lt;statement-x&gt;
    .
    &lt;statement-y&gt;
</code></pre>
<p><strong>try-except处理异常的流程为：</strong></p>
<ol>
<li>首先，try 和 except 之间的语句会被执行；</li>
<li>如果没有异常发生，except 后面的语句会被忽略；</li>
<li>如果有异常发生，try 后面的其它语句就会被跳过，如果异常的类型与 except 关键词后面的异常匹配，这个 except 后面的语句就会被执行；</li>
<li>如果没有异常发生，else 子句存在的话，else 子句将被执行；</li>
<li>finally 子语会在 try 子句执行完毕之后执行，不管 try 子句是否出现异常。如果一个异常发生在 try 子句中却未被处理（捕获），或者发生在 except 或者 else 子句中时，finally 子句执行完后会再次抛出该异常。</li>
</ol>
<p><strong>补充说明：</strong></p>
<ol>
<li>try 与 else，finally 结合使用的内容将在后面进一步详细说明；</li>
<li>一次性捕获多个异常时，多个异常需要用括号括起来；</li>
<li>最后一个 except 子句可以不带异常类型，这样就会捕获所有异常；</li>
<li>当一个异常发生时，可能它还有一些异常参数，except 语句异常名称后面可以跟一个参数，这个参数会与异常实例绑定，存储在 instance.args 中，如果异常中 <code>__str__()</code> 定义过了，就可以直接打印出参数。</li>
</ol>
<h3 id="tryelse">Try 与 else 语句结合使用</h3>
<p>Try 语句可以结合 else 一起使用，如果 try 子句没有异常发生，else 子句存在的话，else 子句将被执行。</p>
<p>如下实例：</p>
<pre><code>def compare(num1, num2):
    try: 
        if(num1 &gt;= num2):
            result = num1
        else:
            result = num2
    except:
        return "ERROR"
    else:
        print("OK")
        return result

#正确的调用
print("compare(12,34):",compare(12,34))
#异常的调用
print("compare(12,'ab'):",compare(12,'ab'))
print("compare('12',34):",compare('12',34))
</code></pre>
<p>执行结果：</p>
<pre><code>OK
compare(12,34): 34
compare(12,'ab'): ERROR
compare('12',34): ERROR
</code></pre>
<h3 id="tryfinally">try 与 finally 语句结合使用</h3>
<p>不管 try 子句是否出现异常，finally 子语都会执行。适用场景：不管 try 是否出现异常，都需要做某种处理，比如，打开一个文件并读取内容，不管这个过程是否出现异常，都需要关闭文件，关闭文件的动作就可以放在 finally 中。</p>
<p>实例如下：</p>
<pre><code>import sys
#在该Python源文件同目录下新建一个文件myfile.txt，写入内容“user-name: Jack”作为测试
try:
    #打开文件，读取第一行
    f = open('myfile.txt')
    s = f.readline()
    print("result",s)
except:
    print("ERROR") 
finally:
    print("close file")
    f.close()
</code></pre>
<p>执行结果：</p>
<pre><code>result user-name: Jack
close file
</code></pre>
<p>如果一个异常发生在 try 子句中却未被处理（捕获），或者发生在 except 或者 else 子句中时，finally子句执行完后会再次抛出该异常。</p>
<p>如下实例：</p>
<pre><code>import sys

try:
    #打开一个不存在的文件
    f = open('file.txt')
    s = f.readline()
    print("result",s)
except TypeError:
    print("ERROR") 
finally:
    print("close file")
</code></pre>
<p>执行结果：没有捕获的异常会被 finally 再次抛出。</p>
<pre><code>close file
Traceback (most recent call last):
  File "D:\User\testI\__init__.py", line 28, in &lt;module&gt;
    f = open('file.txt')
FileNotFoundError: [Errno 2] No such file or directory: 'file.txt'
</code></pre>
<h3 id="exception">Exception 万能异常</h3>
<p>上面已经介绍了类似“万能异常”的方式：try-except，不指明捕获异常的类型时，默认捕获所有异常。那么，为什么还需要 Exception 万能异常呢？很多场景下，当异常发生时，我们希望能够记录下更多的异常信息，以便定位问题。</p>
<p>如下实例：</p>
<pre><code>import sys

try:
    #打开一个不存在的文件,将抛出异常
    f = open('file.txt')
    s = f.readline()
    print("result",s)
except FileNotFoundError as err:
    print("Exception info:",err) 
finally:
    print("close file")
</code></pre>
<p>执行结果：</p>
<pre><code>Exception info: [Errno 2] No such file or directory: 'file.txt'
close file
</code></pre>
<p>不仅捕获了异常，而且记录下了异常的详细信息，对于定位问题十分有用。上面例子指定捕获 FileNotFoundError 异常，前提是，开发者十分清楚代码可能出现的异常类别，如果不清楚异常的类别，我们可以使用万能异常。</p>
<p>如下实例：</p>
<pre><code>import sys

try:
    #打开一个不存在的文件,将抛出异常
    f = open('file.txt')
    s = f.readline()
    print("result",s)
except Exception as err:
    print("Exception info:",err) 
finally:
    print("close file")
</code></pre>
<p>执行结果：</p>
<pre><code>Exception info: [Errno 2] No such file or directory: 'file.txt'
close file
</code></pre>
<h3 id="-3">主动抛出异常</h3>
<p>前面几节介绍的都是处理异常的方法，在实际应用中，开发者有些时候还需要主动抛出异常，如外部输入不合法，文件路径不正确等场景，开发者主动抛出异常，调用者根据抛出的异常做针对性处理。</p>
<p>如下实例：</p>
<pre><code>import sys

try:
    #输入一个文件名
    fileName = input("please input file name:")
    splitList = fileName.split('.')
    fileType = splitList[splitList.__len__()-1]
    #判断文件格式，如果不是doc则抛出异常
    if (fileType != "doc"):
        raise NameError("the file type:%s is not expected."%(fileType))

    f = open(fileName)
    s = f.readline()
    print("result",s)
except FileNotFoundError as err:
    print("Exception info:",err) 
finally:
    print("close file")
</code></pre>
<p>执行结果：NameError 没有被捕获，因此抛出。</p>
<pre><code>please input file name:file.txt
close file
Traceback (most recent call last):
  File "D:\Users\ testI\__init__.py", line 33, in &lt;module&gt;
    raise NameError("the file type:%s is not expected."%(fileType))
NameError: the file type:txt is not expected.
</code></pre>
<h3 id="-4">自定义异常</h3>
<p>所谓自定义异常，就是通过直接继承或者间接继承 Exception 类，来创建自己的异常。</p>
<p>如下实例：</p>
<pre><code>#自定义异常，继承自Exception
class MyException(Exception):
    def __init__(self, *args):
        self.args = args

try:  
    raise MyException("the file type is not expected.")
except MyException1 as err:
    print(err)
</code></pre>
<p>执行结果：</p>
<pre><code>the file type is not expected.
</code></pre>
<p>在上面的例子中，类 Exception 默认的 <code>__init__()</code> 被覆盖。</p>
<p>当创建一个模块有可能抛出多种不同的异常时，一种通常的做法是为这个包建立一个基础异常类，然后基于这个基础类为不同的错误情况创建不同的子类。</p>
<p>如下实例：</p>
<pre><code>#自定义一个基础异常类
class MyException(Exception):
    def __init__(self, *args):
        self.args = args
#定义不同种类的业务异常，继承基础异常类
class loginError(MyException):
    def __init__(self, code = 100, message = 'login error', args = ('Internal Server Error','http:500')):
        self.args = args
        self.message = message
        self.code = code

class loginoutError(MyException):
    def __init__(self):
        self.args = ('Internal Server Error',)
        self.message = 'login out error'
        self.code = 200

#raise loginError()，使用默认参数
try:
    raise loginError()
except loginError as e:
    print(e) #输出异常
    print(e.code) #输出错误代码
    print(e.message)#输出错误信息

#raise loginError()，传入参数
try:
    raise loginError(400,'password is wrong!',('Internal Server Error',))
except loginError as e:
    print(e) #输出异常
    print(e.code) #输出错误代码
    print(e.message)#输出错误信息
</code></pre>
<p>执行结果：</p>
<pre><code>('Internal Server Error', 'http:500')
100
login error
Internal Server Error
400
</code></pre></div></article>