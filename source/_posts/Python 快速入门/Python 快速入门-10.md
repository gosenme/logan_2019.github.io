---
title: Python 快速入门-10
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在前面的章节中，已经介绍了 Python 大部分基本知识，本文我们将学习两个新的知识点：模块和标准库。</p>
<p>Python 的核心非常强大，提供了很多内建的工具，Python 标准安装中包括一组模块，如前面章节介绍过的 math、sys 等，称为标准库（Standard Library），同时，标准库也包含其它的模块。</p>
<h3 id="import">Import语句与模块</h3>
<p>通过前面章节所学，相信读者已经能够创建一个可以执行的 Python 程序。在此，我们重温一下怎么通过 import 语句从外部模块中获取函数并为自己的程序所用。</p>
<pre><code>#通过import导入math模块，如此就可以使用math模块中的函数
import math
#输入一个正数，并计算输出其平方根
x = int(input("Please enter a positive number:"))
#调用了math模块中的函数sqrt(x)
print(math.sqrt(x))
</code></pre>
<p>执行结果：</p>
<pre><code>Please enter a positive number:144
12.0
</code></pre>
<p>import 语句还可以一次导入多个模块，形式如下，注意模块名之间逗号隔开。</p>
<pre><code>import module1, module2,... moduleN
</code></pre>
<h3 id="">编写一个极简的模块</h3>
<p>任何一个 Python 程序都可以作为模块导入。举一个极简的例子：在同一个包中编写两个 Python 程序模块 hello.py 和 test.py（注意，要在同一个包中，否则需要添加路径，这个在下一节介绍）。</p>
<p><strong>Hello.py 代码如下：</strong></p>
<pre><code>#hello.py模块代码，打印hello world！
print('hello, world!')
</code></pre>
<p><strong>Test.py 代码如下：</strong></p>
<pre><code>#test.py模块代码，导入hello模块
import hello
</code></pre>
<p>运行 test.py 模块，执行结果如下：</p>
<pre><code>hello, world!
</code></pre>
<p>执行结果所示，在 test.py 中通过 import hello，执行了 hello.py 中的程序。但是，如果在 test.py 中添加两条 import hello，也只会打印一次“hello world!”。这是因为导入模块并不意味着在导入时执行某些操作（如，打印信息），导入的意义在于定义，如定义变量、函数等，既然是定义，只需要一次即可，导入模块多次和一次效果并没有什么不同。</p>
<p>再来看一个例子，我们在 hello.py 中编写以下代码：</p>
<pre><code>#hello.py模块代码
def printInfo():
    print('hello, world!')

def printSum(x,y):
    print(x+y)
</code></pre>
<p>在 test.py 中编写以下代码：</p>
<pre><code>#test.py模块中的代码
#导入hello模块
import hello
#调用hello模块中的函数
hello.printInfo()
hello.printSum(12, 13)
</code></pre>
<p>运行 test.py 模块，执行结果：</p>
<pre><code>hello, world!
25
</code></pre>
<p>执行结果所见，通过 import 导入 hello 模块，进而调用了 hello 模块中的函数，似曾相似吧？与导入 math 并调用 math.sqrt(x) 如出一辙。通过上述两个例子，不难理解模块的概念和用法。</p>
<h3 id="-1">模块的位置</h3>
<p>上一节的例子中，特意强调 hello.py 和 test.py 必须在同一个包中，这是因为在 test.py 中导入 hello 模块，但是并没有指明 hello 模块的位置，程序运行时，Python 解释器如何查找 hello 模块呢？有两种方式可以确保 Python 解释器查找到 hello 模块：第一，将 hello 模块放置于合适的位置（如，同一个包中）；第二，显式的告诉解释器 hello 模块的位置。</p>
<p><strong>1.将模块放置于正确的位置。</strong></p>
<p>所谓正确的位置，就是 Python 解释器查找模块的位置，只要知道 Python 解释器查找模块的路径，然后将自己的模块放置到对应的路径下即可。Python 解释器的搜索路径可以通过 sys 模块的 path 变量获取，如下代码：</p>
<pre><code>#通过下面的代码，打印搜索路径
import sys

for temp in sys.path:   
    print(temp)
</code></pre>
<p>执行结果：</p>
<pre><code>D:\Users\userName\workspace1\PythonLearning\testI
D:\Users\userName\workspace1\PythonLearning
D:\Program_file\Python\Python36\DLLs
D:\Program_file\Python\Python36\lib
D:\Program_file\Python\Python36
D:\Program_file\Python\Python36\lib\site-packages
D:\Program_file\Python\Python36\lib\site-packages\win32
D:\Program_file\Python\Python36\lib\site-packages\win32\lib
D:\Program_file\Python\Python36\lib\site-packages\Pythonwin
D:\Program_file\Python\Python36\python36.zip
</code></pre>
<p>上面的路径中，PythonLearning 是本课程示例代码所在的 project 名，testI 是本课程示例代码所在的 package 名，hello.py 和 test.py 就是在这个包中。除此以外，搜索路径列表里面还有标准库路径、插件路径，只要将用户自己编写的模块放置到上述路径下，Python 解释器就可以搜索到。</p>
<p>正因为搜索路径列表的存在，在使用标准库模块和同一个包中的模块时，直接通过 import 导入即可，不必显式声明模块所在的路径。</p>
<p><strong>2.告诉解释器去哪里找。</strong></p>
<p>“将模块放置到正确的位置”虽然简单，但在一些特殊的场景下并不适用：</p>
<ol>
<li>没有在 Python 解释器目录中存放文件的权限；</li>
<li>希望将模块放到自定义的位置。</li>
</ol>
<p>关于“告诉解释器去哪里找”，有两种方式：编辑 sys.path 或者编辑 PYTHONPATH 环境变量。</p>
<ul>
<li>编辑 sys.path，如下实例：</li>
</ul>
<pre><code>import sys

#添加路径/home/python/test到path中
sys.path.append('/home/python/test')
</code></pre>
<ul>
<li>编辑 PYTHONPATH 环境变量。</li>
</ul>
<p>环境变量并不是 Python 解释器的组成，而是操作系统的元素，因此，编辑环境变量的操作会因操作系统的不同而有所差异，以 Linux 操作系统为例，添加环境变量的命令如下，可将命令写入 shell 脚本中，在需要时，执行脚本即可。</p>
<pre><code>#添加路径/home/python/test到环境变量中，注意冒号隔开
export PYTHONPATH=$PYTHONPATH:/home/python/test
</code></pre>
<h3 id="fromimport">from…import 语句</h3>
<p>如果一个模块很大（如，包含几百个函数），而我们只需要使用其中一小部分，那么将整个模块导入就很不划算，这种场景下，我们可以使用 from…import 语句来指定要导入的部分，一般形式如下：</p>
<pre><code>from modname import name1, name2, ... nameN
</code></pre>
<p>再来看一个实例。</p>
<p>在 hello.py 中编写以下代码：</p>
<pre><code>#hello.py模块代码
def printInfo():
    print('hello, world!')

def printSum(x,y):
    print(x+y)
</code></pre>
<p>在 test.py 中编写以下代码：</p>
<pre><code>#test.py模块中的代码
#从hello模块中导入printInfo函数
from hello import printInfo
#调用hello模块中的printInfo函数
printInfo()
</code></pre>
<p>运行 test.py 模块，执行结果：</p>
<pre><code>hello, world!
</code></pre>
<p><strong>备注：</strong> from…import 语句还有一种特殊的用法：<code>from…import*</code>，即导入一个模块中的所有不以下划线开头的全局名称到当前的命名空间，后文将予以说明。</p>
<h3 id="-2">深入模块</h3>
<p>Python 中除了标准库提供的模块以外，还有大量的第三方模块，并且模块的数量还在不断增长，现有模块也在不断迭代改进，因此，掌握分析模块的方法十分必要，将有助于理解和使用模块。</p>
<p><strong>dir() 函数</strong></p>
<p>可以通过 dir() 函数查看模块中包含的内容，它会将模块中所有的函数，类变量等列出。如下例子：</p>
<pre><code>import math
print(dir(math))
</code></pre>
<p>执行结果（截取了一部分）：</p>
<pre><code>['__doc__', '__loader__', '__name__', '__package__', '__spec__', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos',…,'trunc']
</code></pre>
<p>其中，一些名字以下划线开始，表示它们并不是为模块外部使用而准备的（可狭义地理解为非对外接口）。</p>
<p><strong><code>__name__</code> 属性</strong></p>
<p>每个模块都有一个 <code>__name__</code> 属性，当其值是 <code>__main__</code> 时，表明该模块自身在运行，否则是被引入。一个模块被另一个程序第一次引入时，其主程序将运行。如果我们想在模块被引入时，模块中的某一程序块不执行，我们可以用 <code>__name__</code> 属性来使该程序块仅在该模块自身运行时执行。如下实例：</p>
<p>在 hello.py 中编写以下代码：</p>
<pre><code>#hello.py模块代码
def printInfo():
    print('hello, world!')

if __name__ == '__main__':
    print('native')
else:
    print('external')
</code></pre>
<p>在test.py中编写以下代码：</p>
<pre><code>#test.py模块中的代码
#导入hello模块
import hello
#调用hello模块中的printInfo函数
hello.printInfo()
</code></pre>
<p>运行 test.py 模块，执行结果：</p>
<pre><code>external
hello, world!
</code></pre>
<p>运行 hello.py 模块，执行结果：</p>
<pre><code>native
</code></pre>
<p><strong><code>__all__</code> 变量</strong></p>
<p>一个模块中有很多变量和函数，但有些变量和函数仅被期望于模块内部使用，而不是作为对外公有接口。一个模块对外的公有接口可以通过 <code>__all__</code> 变量来定义，在导入模块的时候，通过 <code>__all__</code> 变量可以指定可导入的部分。如下实例：</p>
<p>在 hello.py 中编写以下代码：</p>
<pre><code>#hello.py模块代码
def printInfo():
    print('hello, world!')

def printSum(x,y):
    print(x+y)
#内部函数，不期望被导出
def __fun__():
    print("just for test!")    
#通过__all__变量定义模块的公有接口
__all__=['printInfo','printSum']
</code></pre>
<p>在 test.py 中编写以下代码：</p>
<pre><code>#test.py模块中的代码
#导入hello模块
from hello import *
#调用hello模块中的函数
printInfo()
printSum(123,12)
__fun__()
</code></pre>
<p>运行 test.py 模块，执行结果：</p>
<pre><code>hello, world!
135
Traceback (most recent call last):
  File "D:\Users\xxx\testI\test.py", line 11, in &lt;module&gt;
    __fun__()
NameError: name '__fun__' is not defined
</code></pre>
<p>出现了报错，由于 hello 模块的公有接口定义变量 <code>__all__</code> 中没有包含 <code>__fun__()</code> 函数，使用 <code>from hello import*</code> 语句无法将其导入，因而报错。</p>
<h3 id="help">用 help 获取帮助</h3>
<p>对于一个的模块，可以借助标准函数 help 获取其信息，以 math 模块为例：</p>
<pre><code>import math 
#获取math模块的信息
help(math)
</code></pre>
<p>执行结果：</p>
<pre><code>NAME
    math
DESCRIPTION
    This module is always available.  It provides access to the
    mathematical functions defined by the C standard.
FUNCTIONS
    acos(...)
        acos(x)
        Return the arc cosine (measured in radians) of x.
……
</code></pre>
<h3 id="__doc__">文档 <code>__doc__</code></h3>
<p>文档用于存放一个模块的描述信息，在开发中遇到不清楚的问题，可以通过文档获取必要信息，阅读文档获取第一手资料是一个开发人员必备的技能。如下例子：</p>
<pre><code>import sys 
#获取sys模块的文档
print(sys.__doc__)
</code></pre>
<p>执行结果：</p>
<pre><code>This module provides access to some objects used or maintained by the
interpreter and to functions that interact strongly with the interpreter.

Dynamic objects:
argv -- command line arguments; argv[0] is the script pathname if known
path -- module search path; path[0] is the script directory, else ''
modules -- dictionary of loaded modules
……
</code></pre>
<h3 id="-3">标准库</h3>
<p>Python 安装包提供的模块总称为标准库，在前面的章节举例中已经使用过一些标准库中的模块，如 math、sys、os。Python 的标准库非常强大，不可能一一列举，在此，介绍几个常用的模块，更多的内容读者可自行学习。</p>
<ul>
<li>sys 模块：通过它可以访问多个与 Python 解释器联系紧密的函数和变量； </li>
<li>os：通过它可以访问多个与操作系统联系紧密的函数和变量； </li>
<li>fileinput：通过它可以轻松遍历多个文件和流中的所有行；</li>
<li>time：通过它可以获取当前时间，并可以进行时间日期操作及格式化；    </li>
<li>random：通过它可以产生随机数，从序列中选取随机元素及打乱列表元素；</li>
<li>re：通过它可以轻松使用正则表达式。</li>
</ul></div></article>