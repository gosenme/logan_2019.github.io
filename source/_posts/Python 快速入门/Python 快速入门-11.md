---
title: Python 快速入门-11
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>一些场景下，程序需要和外部进行交互，在前面文章中用到了 input、print 函数与外部进行交互，本文将更进一步，介绍两种新的交互方式：文件和流。</p>
<h3 id="">打开文件</h3>
<p>open(name[,mode[,buffering]]) 用于打开文件并返回一个文件对象，open 函数的参数中，文件名 name 是强制参数，模式（mode）和缓冲（buffering）都是可选的。如下实例：</p>
<pre><code>#打开文件读取其中全部内容
f = open("D:/Users/data.txt")
print(f.read())
</code></pre>
<p>输出结果（data.txt 中的全部内容）：</p>
<pre><code>just for testing1
just for testing2
just for testing3
</code></pre>
<h3 id="-1">文件模式</h3>
<p>如上面例子所示，open 函数只带一个文件名参数，可以顺利读取文件的内容，但如果向文件中写入内容则会报错，欲写入内容，必须提供一个写模式参数（w）。除此以外，文件模式参数还有：</p>
<table>
<thead>
<tr>
<th>参数</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>r</td>
<td>读模式</td>
</tr>
<tr>
<td>a</td>
<td>追加模式</td>
</tr>
<tr>
<td>b</td>
<td>二进制模式</td>
</tr>
<tr>
<td>+</td>
<td>读写模式</td>
</tr>
</tbody>
</table>
<p>读、写、追加模式简单易懂，不再赘述，关于二进制模式，则有必要说明一下。在没有特别说明的情况下，Python 处理的文件默认是文本文件，如果处理二进制文件（如声音或者图像），则需要在模式参数中增加 b，如 rb 可用于读取一个二进制文件。</p>
<p><strong>例子1：</strong></p>
<pre><code>#打开文件，写入文本
f = open("D:/Users/data.txt",'w')
f.write('12345-12345-12345')

#打开文件，读取文本
f = open("D:/Users/data.txt",'r')
print(f.read())
#关闭文件
f.close()
</code></pre>
<p>执行结果：</p>
<pre><code>12345-12345-12345
</code></pre>
<p><strong>例子2：</strong></p>
<pre><code>#打开文件，在现有文件后追加信息并换行
f = open("D:/Users/data.txt",'a')
f.write('\nappend information')
f.close()
#打开文件，读取文本
f = open("D:/Users/data.txt",'r')
print(f.read())
#关闭文件
f.close()
</code></pre>
<p>执行结果：</p>
<pre><code>12345-12345-12345
append information
</code></pre>
<h3 id="-2">缓冲</h3>
<p>open 函数的第三个参数控制着文件缓冲，如果该参数为0（或者 False），对文件读写操作都是无缓冲的，直接读写硬盘；如果该参数为1（或者 True），对文件的读写操作就是有缓冲的，数据将缓冲于内存中，只有当调用 flush 或者 close 函数时，才会更新硬盘上的数据。</p>
<p>需要说明的是，该参数可以大于1（代表缓冲区的大小，单位为字节），也可以为负数（代表使用默认的缓冲区大小）。</p>
<h3 id="-3">读写文件</h3>
<p>open 函数返回的只是一个文件对象，读写文件需要调用 read 函数和 write 函数，完成读写后，需要调用 close 函数。</p>
<p>read 函数可以带参数，指定读取的字节数，不带参数则默认读取文件全部内容。write 函数参数为字符串类型，即写入文件的内容。</p>
<pre><code>#打开文件，在现有文件后追加信息并换行
f = open("D:/Users/data.txt",'a')
f.write('\nappend information')
f.close()

#打开文件，读取文件前4个字节
f = open("D:/Users/data.txt",'r')
print(f.read(4))
#关闭文件
f.close()
</code></pre>
<p>执行结果：</p>
<pre><code>app
</code></pre>
<h3 id="-4">读写行</h3>
<p>file.readline()，读取文件中单独的一行内容（从当前位置开始直到一个换行符出现），不带参数时，默认读取一整行；带参数（非负整数）则表示 readline 可以读取当前行内容的最大字节数。此外，可以通过 readline 函数来遍历文件，如下实例：</p>
<p><strong>例子1：不带参数</strong></p>
<pre><code>#打开文件，写入信息并换行
f = open("D:/Users/data.txt",'w')
f.write('append information1\n')
f.write('append information2\n')
f.write('append information3\n')
f.close()

#打开文件，按行读取文件内容
f = open("D:/Users/data.txt",'r')
while True:
    line = f.readline()
    #读取完毕退出
    if(not line):
        break
    print('content:',line)
#关闭文件
f.close()
</code></pre>
<p>执行结果（省略空行）：</p>
<pre><code>content: append information1 
content: append information2 
content: append information3
</code></pre>
<p><strong>例子2：带参数</strong></p>
<pre><code>#打开文件，并写入信息
f = open("D:/Users/data.txt",'w')
f.write('append information1\n')
f.write('append information2')
f.close()

#打开文件，按行及参数限制读取文件内容
f = open("D:/Users/data.txt",'r')
while True:
    line = f.readline(10)
    #读取完毕退出
    if(not line):
        break
    print('content:',line)
#关闭文件
f.close()
</code></pre>
<p>执行结果（省略空行）：</p>
<pre><code>content: append inf
content: ormation1
content: append inf
content: ormation2
</code></pre>
<p>readline 函数每次读取一行，与之对应的 readlines 则可一次读取整个文件的所有行。如下实例：</p>
<pre><code>#打开文件，并写入信息
f = open("D:/Users/data.txt",'w')
f.write('append information1\n')
f.write('append information2')
f.close()

#打开文件，并一次读取所有行
f = open("D:/Users/data.txt",'r')
for line in f.readlines():
    print('content:',line)
#关闭文件
f.close()
</code></pre>
<p>执行结果（省略空行）：</p>
<pre><code>content: append information1
content: append information2
</code></pre>
<p>通过 writelines 函数。可以一次向文件写入多行内容，如下实例：</p>
<pre><code>#打开文件，一次写入多行内容
f = open("D:/Users/data.txt",'w')
content = ['append information1\n','append information2']
f.writelines(content)
f.close()
</code></pre>
<h3 id="fileinput">使用 fileinput 进行迭代</h3>
<p>fileinput 模块可以对一个或多个文件中的内容进行迭代、遍历等操作。该模块的 input() 函数有点类似文件 readlines 函数，但区别明显：readlines 是一次性读取文件中的全部内容，如果文件较大的话，会占用大量内存；input 返回的则是一个迭代对象，结合 for 循环使用，典型用法如下：</p>
<pre><code>import fileinput

for line in fileinput.input(filename):
    process(line)
</code></pre>
<p><strong>实例：</strong></p>
<pre><code>import fileinput

for line in fileinput.input("D:/Users/data.txt"):
    print(line)
</code></pre>
<p>注意，input函数有多个参数：分别设置读取文件路径、读写模式、编码方式、缓冲区大小、备份文件扩展名等。</p>
<p>此外，fileinput 模块还有很多常用的函数，这里介绍几个最常用的，其余读者可根据前一篇文章中介绍的模块分析方法自行挖掘。</p>
<table>
<thead>
<tr>
<th>函数名</th>
<th>说明</th>
</tr>
</thead>
<tbody>
<tr>
<td>fileinput.input()</td>
<td>返回能够用于for循环遍历的对象</td>
</tr>
<tr>
<td>fileinput.filename()</td>
<td>返回当前文件的名称</td>
</tr>
<tr>
<td>fileinput.lineno()</td>
<td>返回当前已经读取的行的数量（或者序号）</td>
</tr>
<tr>
<td>fileinput.filelineno()</td>
<td>回当前读取的行的行号</td>
</tr>
<tr>
<td>fileinput.isfirstline()</td>
<td>检查当前行是否是文件的第一行</td>
</tr>
<tr>
<td>fileinput.isstdin()</td>
<td>判断最后一行是否从stdin中读取</td>
</tr>
<tr>
<td>fileinput.close()</td>
<td>关闭队列</td>
</tr>
</tbody>
</table>
<h3 id="-5">文件迭代器</h3>
<p>本文最后介绍一个优雅的特性：文件迭代器。在 Python 中，如果该特性出现早一点，前面介绍的 readlines 等函数可能就不会出现了，Python 从2.2开始，文件对象具备可迭代特性。</p>
<p>先来看一个例子：</p>
<pre><code>#打开文件，一次写入多行内容
f = open("D:/Users/data.txt",'w')
content = ['append information1\n','append information2']
f.writelines(content)
f.close()

#打开文件，通过文件迭代器遍历文件
f = open("D:/Users/data.txt",'r')
for line in f:
    print('content:',line)
#关闭文件
f.close()
</code></pre>
<p>执行结果（省略空行）：</p>
<pre><code>content: append information1
content: append information2
</code></pre>
<p>借助文件迭代器，我们可以执行和普通迭代器相同的操作，比如，将读取内容转化为字符串列表（效果类似前面介绍的 readlines）。</p>
<pre><code>#打开文件，一次写入多行内容
f = open("D:/Users/data.txt",'w')
content = ['append information1\n','append information2']
f.writelines(content)
f.close()

#打开文件，将读取内容转换为字符串列表
f = open("D:/Users/data.txt",'r')
lines = list(f)
print(lines)
#关闭文件
f.close()
</code></pre>
<p>执行结果：</p>
<pre><code>['append information1\n', 'append information2']
</code></pre></div></article>