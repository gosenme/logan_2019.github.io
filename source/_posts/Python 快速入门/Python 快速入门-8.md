---
title: Python 快速入门-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在前面介绍变量的文章中，我曾经提及：Python 是一门完全面向对象的编程语言，在 Python 中，数字、字符串、列表、元组、字典等都是对象。 </p>
<p>相较于函数，类则是更高级别的抽象结构，类（Class）是面向对象程序设计（OOP，Object-Oriented Programming）实现信息封装的基础。类是一种用户定义类型，也称类类型。每个类包含数据说明和一组操作数据或传递消息的函数。类的实例称为对象，类的实质是一种数据类型。</p>
<h3 id="">类的定义</h3>
<p>与其它面向对象编程语言类似，在 Python 中，类具有多态、封装、继承。不过，Python 中没有重载，类的定义细节也具有明显差异。定义类的一般形式如下：</p>
<pre><code class="Python language-Python">class ClassName:
    &lt;statement-1&gt;
    .
    .
    .
    &lt;statement-N&gt;
</code></pre>
<p>上面提到，类的本质是一种数据结构，一个类通常包含数据成员和函数成员。数据成员用于刻画类所描述的一类事物的属性，如描述人，一般用姓名、年龄、性别、学历等属性进行刻画，这就是数据成员；函数成员用于完成具体的任务，如查询、设置人名、打印基本信息等。如下实例：</p>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义类的数据成员：姓名，年龄
    name=''
    age=0

    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('person-info:{name:%s, age:%d}'%(self.name,self.age))
    #定义一个简单的函数
    def hello(self):
        print("hello world!")


#实例化，创建一个对象
p1 = Person()
#访问类的属性：数据成员,访问语法obj.X
print("name:",p1.name)
print("age:",p1.age)
#访问类的函数
p1.printPersonInfo()
p1.hello()
</code></pre>
<p>执行结果：</p>
<pre><code>name: 
age: 0
person-info:{name:, age:0}
hello world!
</code></pre>
<h3 id="self">self 参数</h3>
<p>上述实例中，Person 类定义了两个函数，其定义形式与上一篇介绍的函数存在明显区别：类中的函数必须有一个额外的参数 self，并且 self 参数必须放在第一个参数的位置。那么，对于一个实例化的对象，self 参数代表什么呢？来看一个例子。</p>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义类的数据成员：姓名，年龄
    name=''
    age=0

    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('name:',self.name)
        print('self:',self)
        print('self class:',self.__class__)


#实例化，创建一个对象
p1 = Person()
#访问类的函数
p1.printPersonInfo()
</code></pre>
<p>执行结果：</p>
<pre><code>name: 
self: &lt;__main__.Person object at 0x00000000067B5F98&gt;
self class: &lt;class '__main__.Person
</code></pre>
<p>从执行结果可以看出，self 的内容是一个地址，它代表当前实例，也就是当前对象的地址。需要说明的是，self 参数并不是 Python 的保留关键字，而是为了便于理解，按照惯例命名而来。事实上，换做其它名字也可以（须遵循规则：必须是类函数的第一个参数）。</p>
<h3 id="-1">实例化</h3>
<p>上面小节实例中，我们创建了一个 Person 类的对象：p1=Person()，通过对象可以访问类的属性和调用类的函数，语法形式为：obj.name，其中 name 代表类的属性名或函数名。</p>
<p>上述例子中存在一个疑点，不知读者是否注意到，例子中实例化对象的操作并不是显式调用构造函数完成的，如下代码：</p>
<pre><code> p1 = Person()
</code></pre>
<p>类中并没有定义名为 Person() 的函数，Person 是类名，在进行实例化创建对象的时候，会自动调用<code>__init()__</code>函数。该函数用于创建对象，并赋予所创建对象初始状态。</p>
<p>上述例子中，做了很多简化，创建的对象的所有属性都是默认值，在实际应用中，通常会采取更有效的方式来赋予对象初始状态。如下实例：</p>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义类的数据成员：姓名，年龄
    name=''
    age=0  
#定义构造函数，用于创建一个类实例，也就是类的具体对象
#通过参数传递，可以赋予对象初始状态
    def __init__(self,name,age):
        self.name = name
        self.age = age  
    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('person-info:{name:%s, age:%d}'%(self.name,self.age))


#实例化，创建两个对象，默认调用构造函数：__init__()
p1 = Person("Zhang San",12)
p2 = Person("Li Si",13)
#访问类的属性：数据成员,访问语法obj.X
print("name:",p1.name)
print("age:",p1.age)
#调用函数
p1.printPersonInfo()
p2.printPersonInfo()
</code></pre>
<p>运行结果：</p>
<pre><code>name: Zhang San
age: 12
person-info:{name:Zhang San, age:12}
person-info:{name:Li Si, age:13}
</code></pre>
<h3 id="pythonjavac">Python 中类定义与 Java、C++ 的差别</h3>
<p>从上面的例子中可以发现，Python 中类的定义与 Java 和 C++ 的区别：</p>
<ul>
<li>定义形式，Python 没有修饰符，只有关键词 class，Java 和 C++ 则有修饰符（非必须）；</li>
<li>构造函数，Python 没有重载特性，只能定义一个构造函数，且函数名为 <code>__init__</code>，若不定义构造函数，则默认为 <code>__init__(self)</code>，Java、C++ 则具有重载特性，可定义多个构造函数，且构造函数名必须与类名一致；</li>
<li>形参定义形式不同，Python 类的方法，self 参数为必须参数；</li>
<li>不必声明域，上面的例子中，声明了域 (name，age)，事实上，Python 可以不声明域，例子如下：</li>
</ul>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义构造函数，用于创建一个类实例，也就是类的具体对象
    def __init__(self,name,age):
        self.name = name
        self.age = age  
    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('person-info:{name:%s, age:%d}'%(self.name,self.age))
</code></pre>
<h3 id="-2">继承</h3>
<p>继承可谓一种带有褒义的懒惰行为，一个最直观的好处就是减少编写重复代码，通过继承，子类可以重用父类中的函数和数据成员。当然，继承的意义远不止于此，这里就不展开了。</p>
<p>关于继承，通常将实施继承行为的类称为子类（Child Class）或者派生类（Derived Class），被继承的类称为父类（Parent Class）或者基类（Base Class)。与 Java、C++ 相比，Python 中继承的一般形式颇为简洁：</p>
<pre><code>class childClassName(parentClassName):
    &lt;statement-1&gt;
    .
    .
    .
    &lt;statement-N&gt;
</code></pre>
<p>下面结合实例来看一下，定义一个类 Occupation 和一个继承 Occupation 的类 Person，继承的定义形式为：Person(Occupation)，无需关键词声明。</p>
<pre><code>#定义一个类Occupation，描述职业
class Occupation:
    #定义构造函数
    def __init__(self,salary,industry):
        self.salary = salary
        self.industry = industry
    def printOccupationInfo(self):
        print('Occupation-info:{salary:%d, industry:%s}'%(self.salary,self.industry)) 

#定义一个简单的类Person,继承自类Occupation     
class Person(Occupation):
    def __init__(self,name,age):
        self.name = name
        self.age = age  
    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('person-info:{name:%s, age:%d}'%(self.name,self.age))

#创建一个子类对象
temp = Person('Wu-Jing',38)
#访问父类的数据成员
temp.salary = 21000
temp.industry = "IT"
#分别调用本身和父类的函数
temp.printOccupationInfo()
temp.printPersonInfo()
</code></pre>
<p>执行结果：</p>
<pre><code>Occupation-info:{salary:21000, industry:IT}
person-info:{name:Wu-Jing, age:38}
</code></pre>
<h3 id="-3">多继承</h3>
<p>一些场景下，一个子类可能需要继承多个父类，举个例子：有三个类分别描述职业信息，购物信息，银行账户信息，现在定义一个类Person来描述一个人，显然，Person涉及上述三个类的信息，为了重复利用代码，降低开发难度，可以直接继承上述三个类，这便是多继承的应用。如上所述，多继承定义形式如下：</p>
<pre><code>class childClassName(parentClassName1，parentClassName2，…):
    &lt;statement-1&gt;
    .
    .
    .
    &lt;statement-N&gt;
</code></pre>
<p>关于多继承，实例如下：</p>
<pre><code>#定义一个类BankAccount，描述银行账户
class BankAccount:
    def __init__(self,number, balance):
        self.number = number
        self.balance = balance  
    #计算并返回年利息
    def getAnnualInterest (self):
        return self.balance*0.042  

#定义一个类Occupation，描述职业
class Occupation:
    def __init__(self,salary,industry):
        self.salary = salary
        self.industry = industry
    def printOccupationInfo(self):
        print('Occupation-info:{salary:%d, industry:%s}'%(self.salary,self.industry)) 

#定义一个类Person,继承自类BankAccount和BankAccount      
class Person(Occupation,BankAccount):
    def __init__(self,name,age):
        self.name = name
        self.age = age  
    #定义一个函数：打印类实例的基本信息    
    def printPersonInfo(self):
        print('person-info:{name:%s, age:%d}'%(self.name,self.age))

#创建一个子类对象
temp = Person('Wu-Jing',38)
#访问父类数据成员
temp.number = 622202050201
temp.balance = 1000000.99
temp.salary = 21000
temp.industry = "IT"
#分别调用本身和父类的函数
temp.printOccupationInfo()
temp.printPersonInfo()
print('Annual interest:',temp.getAnnualInterest())
</code></pre>
<p>执行结果：</p>
<pre><code>Occupation-info:{salary:21000, industry:IT}
person-info:{name:Wu-Jing, age:38}
Annual interest: 42000.041580000005
</code></pre>
<p>需要注意的是，多继承中，子类继承了不同父类中的属性和函数，这些属性和函数可能存在同名的情况，在子类使用这些同名的函数或属性时，在没有指定的情况下，Python 将根据一定顺序进行搜索：首先搜索子类，如果未找到则根据多继承定义的顺序，从左至右在父类中查找。</p>
<p>如下实例：</p>
<pre><code>#定义一个类 BankAccount，描述银行账户
class BankAccount: 
    def printInfo(self):
        print('BankAccount-info')  

#定义一个类 Occupation，描述职业
class Occupation:
    def printInfo(self):
        print('Occupation-info') 

#定义一个类 Person,继承自类 BankAccount 和 BankAccount      
class Person(Occupation,BankAccount):
    def __init__(self,name,age):
        self.name = name
        self.age = age  

    def printPersonInfo(self):
        print('person-info')

#创建一个子类对象
temp = Person('Wu-Jing',38)
#调用父类中的函数
temp.printInfo()
</code></pre>
<p>执行结果：</p>
<pre><code>Occupation-info
</code></pre>
<p>很明显，根据定义顺序，优先调用父类 Occupation 中的 printInfo()。</p>
<h3 id="-4">函数的重写</h3>
<p>一些场景下，从父类继承来的函数并不能完全满足需求，需要在子类中对其进行修改，这就是重写的概念：在子类中重写父类中的函数，当子类对象调用该名称的函数时，会调用子类中重写的函数，父类中的同名函数将被覆盖。</p>
<p>实例如下：</p>
<pre><code>#定义一个类Occupation，描述职业
class Occupation:
    #定义构造函数
    def __init__(self,salary,industry):
        self.salary = salary
        self.industry = industry
    def printInfo(self):
        print('salary:%d, industry:%s}'%(self.salary,self.industry)) 

#定义一个简单的类Person,继承自类Occupation     
class Person(Occupation):
    def __init__(self,name,age):
        self.name = name
        self.age = age  
    #定义一个函数：打印类实例的基本信息    
    def printInfo(self):
        print('name:%s, age:%d'%(self.name,self.age))
        print('salary:%d, industry:%s'%(self.salary,self.industry))

#创建一个子类对象
temp = Person('Wu-Jing',38)
#访问父类的数据成员
temp.salary = 21000
temp.industry = "IT"
#分别调用函数printInfo()
temp.printInfo()
</code></pre>
<p>执行结果：</p>
<pre><code>name:Wu-Jing, age:38
salary:21000, industry:IT
</code></pre>
<h3 id="-5">私有属性与私有方法</h3>
<p>前面几节的实例中，类的属性和函数都是“公有”的，可以通过类对象直接访问。但是，在某些场景下，我们并不希望对外暴露类的内部细节，为了限制外部访问，我们可以将对应的属性和函数设置为私有。将类的属性和函数设置为私有的一般形式为以下两种。</p>
<p><strong>1.定义私有属性</strong></p>
<p><code>__attribute</code>：属性名前面加两个下划线，即声明该属性为私有，不能在类的外部直接访问，在类内部访问时用 <code>self.__attribute</code>。</p>
<p><strong>2.定义私有函数</strong></p>
<p><code>__function</code>：函数名前面加两个下划线，即声明该函数为私有，不能在类的外部直接访问，在类内部访问时用 <code>self.__ function</code>。</p>
<p>实例如下：</p>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义两个私有属性name,age
    def __init__(self,name,age):
        self.__name = name
        self.__age = age  
    #定义公有函数，在类外部可以访问    
    def getName(self):
        self.__fun()
        return self.__name
    def getAge(self):
        return self.__age
    #定义一个私有函数，只能在类内部使用
    def __fun(self):
        print('hello')

#实例化
p1 = Person("Zhang San",12)
#访问类的私有属性和私有函数，将会报错
print("name:",p1.__age)
print("age:",p1.__name)
p1.__fun()
</code></pre>
<p>对于私有属性和私有函数，如果需要在类外访问，可以通过公有函数实现，这与 Java 和 C++ 是一致的。</p>
<p>如下实例：</p>
<pre><code>#定义一个简单的类，描述一个人的基本信息        
class Person:
    #定义两个私有属性name,age
    def __init__(self,name,age):
        self.__name = name
        self.__age = age  
    #定义公有函数，在类外部可以访问    
    def getName(self):
        self.__fun()
        return self.__name
    def getAge(self):
        return self.__age
    #定义一个私有函数，只能在类内部使用
    def __fun(self):
        print('hello')

#实例化
p1 = Person("Zhang San",12)
#访问类的公有函数
print("name:",p1.getName())
</code></pre>
<p>执行结果：</p>
<pre><code>hello
name: Zhang San
</code></pre></div></article>