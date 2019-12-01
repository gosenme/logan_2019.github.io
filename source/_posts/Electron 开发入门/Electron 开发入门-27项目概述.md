---
title: Electron 开发入门-27
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">项目概述</h3>
<p>在本课中将会结合多种技术实现一款支持以太防网络的云笔记，主要功能是在本地编写富文本格式的笔记，然后可以将云笔记保存到本地（SQLite 数据库），并可以同步到服务端（MySQL）数据库，同时，在服务端会启动一个扫描程序，将新提交的数据同步到以太坊网络上，也就是说，这款云笔记可以将数据同时同步到服务端的 MySQL 数据库和云笔记中，并且在云笔记客户端还可以选择从以太坊恢复云笔记。</p>
<p>本系统涉及到的技术包括（包括两类技术）：</p>
<ul>
<li>JavaScript 语言、Web、Node.js、Express、Electron、SQLite、MySQL</li>
<li>区块链和以太坊理论、Web3.js、Solidity 语言（编写智能合约，用于在以太坊网络上保存云笔记数据，以及获取云笔记数据）</li>
</ul>
<p>通过本系统不仅可以学到如何使用 Web 栈技术开发跨平台桌面应用，开可以学到如何在以太坊上保存和获取富文本数据。</p>
<p>下面是本系统的主界面：</p>
<p><img src="https://images.gitbook.cn/Fvk2pjrVOAmtVqXJXF3-LWWxsyM5" width = "75%" /></p>
<p>接下来会介绍本系统主要功能的实现，完整的代码请读者参考本课提供的源代码。</p>
<h3 id="-1">注册用户</h3>
<p>本系统会将用户信息保存到 MySQL 数据库中，表名为 t_users。下面是用于注册用户的客户端代码，通过 ajax 技术访问服务端的路由。</p>
<pre><code class="index.js language-index.js">$(".btn2").click(function () {
    var name=$(".rusername").val();
    var password=$(".rpassword").val();
    //通过 AJAX 代码访问服务端用于注册用户的路由
    $.ajax({
        url:'http://localhost:3000/register',
        data:{name:name,password:password},
        dataType: "json",
        type:'post',
        success: function (result) {
            if(result=='1'){
                alert('注册成功！请登录');
            }
        },
        error:function (err) {
            console.log("123");
        }
    });
});
</code></pre>
<h3 id="-2">集成百度富文本编辑器</h3>
<p>本系统的一个关键点就是可以编辑富文本，而富文本编辑器是不需要自己写的，有很多现成的可以利用个，如百度富文本编辑器，本节会将这个编辑器集成到系统中。百度富文本编辑器就是几个 js 文件，引用即可。</p>
<pre><code class="index.html language-index.html">&lt;script type="text/javascript" charset="utf-8" src="editor/ueditor.config.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" charset="utf-8" src="editor/ueditor.all.min.js"&gt; &lt;/script&gt;

&lt;div class="right"&gt;
    &lt;div id="editor" style="width:100%;height:100%;margin:0 auto;display:block;"&gt;&lt;/div&gt;
&lt;/div&gt;

&lt;script type="text/javascript"&gt;
    var ue = UE.getEditor('editor');
&lt;/script&gt;
</code></pre>
<h3 id="sqlite">将笔记保存到客户端（SQLite 数据库）</h3>
<p>云笔记可以将数据保存到本地，本地使用 SQLite 数据库，保存数据的代码如下所示。</p>
<pre><code class="event.js language-event.js">$("#btn_save").click(function(){
    var title=treeflag.treeDemo.name;
    var mid=treeflag.treeDemo.id;
    //从百度富文本编辑器中获得富文本内容
    var text=UE.getEditor('editor').getContent();
    //用于操作 SQLite 数据库的类
    var db=new dataBase();
    db.addNote(title,mid,text);
});
</code></pre>
<h3 id="sqlite-1">从 SQLite 数据库装载笔记</h3>
<p>这里实现从 SQLite 数据库中读取笔记的内容。</p>
<pre><code class="event.js language-event.js">function onClick(event, treeId, treeNode, clickFlag) {//树插件里面的方法，点击节点
     treeflag.treeDemo=treeNode;
     var db=new dataBase();
     //装载云笔记的内容
     var text=db.loadNote(treeNode.id);
     //将读取到的内容显示在富文本编辑器中
     if(text['text']=='Null'){
         UE.getEditor('editor').setContent('');
     }else{
         UE.getEditor('editor').setContent(text['text']);
     }

}
</code></pre>
<h3 id="-3">编写用于同步云笔记的路由</h3>
<p>本案例还需要使用 Node.js 和 Express（Node.js 的框架，用于编写 Web 应用）编写服务端的路由，也就是 Web 服务程序，编写的方式类似，这里给出一个将数据更新到服务器的代码，其他完整代码请读者参考源代码。</p>
<pre><code class="conn.js language-conn.js">//更新数据库
index.js
router.post('/update', function(req, res, next) {
    console.log("更新目录");
    //获取客户端发过来的数据
    var data=req.body.data;
    console.log(data);
    var pool=new Database();
    pool.update(res,data);
});
</code></pre>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a>。</p></div></article>