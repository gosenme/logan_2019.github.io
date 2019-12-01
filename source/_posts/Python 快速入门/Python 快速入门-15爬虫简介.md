---
title: Python 快速入门-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">爬虫简介</h3>
<p>百度百科对网络爬虫的解释：</p>
<blockquote>
  <p>网络爬虫（又被称为网页蜘蛛，网络机器人，在 FOAF 社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。另外一些不常使用的名字还有蚂蚁、自动索引、模拟程序或者蠕虫。</p>
</blockquote>
<p>通俗解释：</p>
<blockquote>
  <p>互联网存在大量网页，这些网页作为信息的载体包含大量的数据，通过一定技术，我们可以设计一种程序来自动访问网页，并提取网页中的数据，这便是狭义的网络爬虫。</p>
</blockquote>
<p>网络爬虫分类：</p>
<blockquote>
  <p>网络爬虫按照系统结构和实现技术，大致可以分为以下几种类型：通用网络爬虫（General Purpose Web Crawler）、聚焦网络爬虫（Focused Web Crawler）、增量式网络爬虫（Incremental Web Crawler）、深层网络爬虫（Deep Web Crawler）。 实际的网络爬虫系统通常是几种爬虫技术相结合实现的 。</p>
</blockquote>
<h3 id="chat">设计一个简易的爬虫爬取最热 Chat 基本信息</h3>
<h4 id="-1">设计目标</h4>
<p>首先来看一下，我们要爬取的网页长什么样子。</p>
<p><img src="http://images.gitbook.cn/2e9a4b80-5789-11e8-9a3b-29bcc897d0d6" alt="enter image description here" /></p>
<p>从页面中可以看出，每场 Chat 都包含四种信息：Chat 简介、订阅人数、作者及作者简介。本节将设计一个简易的爬虫程序，爬取这些信息，并将爬取到的信息写入 Excel 文件。</p>
<p>根据设计目标，我们可以列出以下基本步骤：</p>
<ul>
<li>获取网页；</li>
<li>解析网页，提取我们需要的信息；</li>
<li>将提取出来的信息写入 Excel 文件。</li>
</ul>
<h4 id="-2">准备工作</h4>
<h5 id="python"><strong>Python 工具模块安装</strong></h5>
<p>根据上述步骤，我们需要安装必要的工具模块：Requests（获取目标网页）、BeautifulSoup（提取网页信息）、xlwt（将信息写入 Excel 文件）。模块的安装比较简单，上一章已经介绍过，建议采用 Python pip 工具，使用简单的命令便可以完成安装，如：<code>pip install requests</code>。</p>
<h5 id="-3"><strong>网页元素分析</strong></h5>
<p>最热 Chat 网页中有大量的元素，而我们需要提取的信息只是其中一部分，因此，我们需要找到筛选特征，将有效信息筛选出来。采用 Chrome 浏览器，查看页面，如下所示：</p>
<p><img src="http://images.gitbook.cn/8b284760-5790-11e8-80a9-2b40ec71fa5f" alt="enter image description here" /></p>
<p>很明显，通过特定标签和属性就可以筛选出本页的最热 Chat。其中，可作为筛选条件的标签有：div 和 span；可作为筛选条件的属性有：<code>class=“col-md-12”</code>（筛选Chat）、<code>class="item-author-ndV2"</code>（作者）、<code>class="item-titleV2"</code>（标题）、<code>class="item-author-descV2</code>（作者简介）、<code>class="text"</code>（订阅人数）。</p>
<h4 id="-4">编写代码</h4>
<p>第一部分，获取网页，代码如下：</p>
<pre><code>#url='http://gitbook.cn/gitchat/hot'
#获取最热Chat网页文本信息
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as err:
        print(err)
</code></pre>
<p>第二部分，从网页中提取需要的信息，代码如下：</p>
<pre><code>#通过BeautifulSoup解析网页，提取我们需要的数据
def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    ChatList=soup.find('div',attrs={'class':'mazi-activity-container item-container'})
    datalist=[]#用于存放提取到全部Chat信息
    #遍历每一条Chat
    for Chat in ChatList.find_all('div',attrs={'class':'col-md-12'}):
        data = []
        #提取Chat标题
        chatTile=Chat.find('div',attrs={'class':'item-titleV2'}).getText()
        data.append(chatTile)    

        #提取订阅人数
        bookingNum = Chat.find('span', attrs={'class': 'text'})
        data.append(str(bookingNum.getText()).lstrip())

        #提取作者姓名
        authorName=Chat.find('div',attrs={'class':'item-author-nameV2'}).getText()
        data.append(authorName)

        #提取作者简介
        authorDesc=Chat.find('div',attrs={'class':'item-author-descV2'}).getText()
        data.append(authorDesc)
        datalist.append(data)
    return datalist
</code></pre>
<p>第三部分，将信息写入 Excel 文件，代码如下：</p>
<pre><code>#保存数据到Excel中
def saveData(datalist,path):
    #标题栏背景色
    styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue; font: bold on;'); # 80% like
    #创建一个工作簿
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    #创建一张表
    sheet=book.add_sheet('最热ChatTop20',cell_overwrite_ok=True)
    #标题栏
    titleList=('Chat标题','订阅人数','作者','作者简介')
    #设置第一列尺寸
    first_col = sheet.col(0)
    first_col.width=256*40
    #写入标题栏
    for i in range(0,4):
        sheet.write(0,i,titleList[i], styleBlueBkg)
    #写入Chat信息  
    for i in range(0,len(datalist)):
        data=datalist[i]
        for j in range(0,4):
            sheet.write(i+1,j,data[j])
    #保存文件到指定路径
    book.save(path)
</code></pre>
<h3 id="-5">完整代码及运行结果</h3>
<pre><code># -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlwt

#获取网页文本信息
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as err:
        print(err)
#通过BeautifulSoup解析网页，提取我们需要的数据
def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    ChatList=soup.find('div',attrs={'class':'mazi-activity-container item-container'})
    datalist=[]#用于存放提取到全部Chat信息
    #遍历每一条Chat
    for Chat in ChatList.find_all('div',attrs={'class':'col-md-12'}):
        data = []
        #提取Chat标题
        chatTile=Chat.find('div',attrs={'class':'item-titleV2'}).getText()
        data.append(chatTile)    

        #提取订阅人数
        bookingNum = Chat.find('span', attrs={'class': 'text'})
        data.append(str(bookingNum.getText()).lstrip())

        #提取作者姓名
        authorName=Chat.find('div',attrs={'class':'item-author-nameV2'}).getText()
        data.append(authorName)

        #提取作者简介
        authorDesc=Chat.find('div',attrs={'class':'item-author-descV2'}).getText()
        data.append(authorDesc)
        datalist.append(data)
    return datalist

#保存数据到Excel中
def saveData(datalist,path):
    #标题栏背景色
    styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue; font: bold on;'); # 80% like
    #创建一个工作簿
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    #创建一张表
    sheet=book.add_sheet('最热ChatTop20',cell_overwrite_ok=True)
    #标题栏
    titleList=('Chat标题','订阅人数','作者','作者简介')
    #设置第一列尺寸
    first_col = sheet.col(0)
    first_col.width=256*40
    #写入标题栏
    for i in range(0,4):
        sheet.write(0,i,titleList[i], styleBlueBkg)
    #写入Chat信息  
    for i in range(0,len(datalist)):
        data=datalist[i]
        for j in range(0,4):
            sheet.write(i+1,j,data[j])
    #保存文件到指定路径
    book.save(path)

#网页地址
chatUrl='http://gitbook.cn/gitchat/hot'
html=getHTMLText(chatUrl)  
datalist=getData(html)
saveData(datalist,str("topChat.xls"))
</code></pre>
<p>运行结果：</p>
<p><img src="http://images.gitbook.cn/56e56290-5794-11e8-80a9-2b40ec71fa5f" alt="enter image description here" /></p></div></article>