---
title: 案例上手 Spring 全家桶-31
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上节课我们已经成功搭建起来 MongoDB 服务器，本节课我们来介绍 MongoDB 数据库的常用命令。</p>
<p>MongoDB 的命令比传统 SQL 更加简便，使用起来更加方便，它的操作更贴近面向对象思想，这是因为 MongoDB 的存储结构是 BSON 格式，类似于 JSON 的一种数据格式，所以 MongoDB 操作起来非常灵活，不会像传统的关系型数据库那样有很多限制。</p>
<p>我们要介绍的常用命令大致分为以下 3 种。</p>
<ul>
<li>对数据库的操作，包括创建、查看、删除。</li>
<li>对数据表（集合）的操作，包括创建、删除。</li>
<li>对数据的操作，包括添加、修改、删除、各种查询。</li>
</ul>
<p>接下来详细学习每一条命令。</p>
<h3 id="-1">对数据库的操作</h3>
<p>（1）创建数据库。</p>
<pre><code>use mongotest
</code></pre>
<p>这个语法放在关系型数据库中是选择数据库的意思，在 MongoDB 中，如果该数据库存在，则直接选择该数据库，如果不存在，则先创建，再选择，就是这么简单方便。</p>
<p>如图，终端打印 <code>switched to db mongotest</code>，表示 mongotest 数据库已经创建完毕，并且系统已经切换到了该数据库中。</p>
<p><img src="https://images.gitbook.cn/1b4196f0-bb4d-11e9-8b7d-b7dd9ffab41a" width = "60%" /></p>
<p>（2）查看数据库。</p>
<pre><code>show dbs
</code></pre>
<p><img src="https://images.gitbook.cn/7aa91cd0-bb4d-11e9-9c35-9730454d953c" width = "60%" /></p>
<p>我们并没有在结果列表中看到刚才创建的 mongotest 数据库，这是因为 mongotest 只是创建，还没有添加数据，空的数据库不会在 show dbs 中显示。</p>
<p>（3）查看当前切换的数据库。</p>
<pre><code>db
</code></pre>
<p><img src="https://images.gitbook.cn/96af0840-bb4d-11e9-9098-7f652ba8c5a9" width = "60%" /></p>
<p>（4）删除数据库。</p>
<p>先切换到要删除的数据库 use db，再执行删除操作 db.dropDatabase()，比如，删除 mongotest 数据库。</p>
<pre><code>use mongotest
db.dropDatabase()
</code></pre>
<p>如图，终端打印 <code>{"ok":1}</code>，表示删除成功。</p>
<p><img src="https://images.gitbook.cn/ac3d5f90-bb4d-11e9-9c35-9730454d953c" width = "60%" /></p>
<h3 id="-2">对集合的操作</h3>
<p>（5）创建集合。</p>
<p>集合的创建和数据库的创建类似，不需要先创建，再操作，创建和操作可以用一条命令同时完成，比如，我们现在再 mongotest 中创建一个 user 集合，并且给集合中添加数据 <code>{id:1,name:"小明",age:22}</code>。</p>
<pre><code>db.user.insert({id:1,name:"小明",age:22})
</code></pre>
<p><img src="https://images.gitbook.cn/c3590da0-bb4d-11e9-9098-7f652ba8c5a9" width = "50%" /></p>
<p>如图，终端打印 <code>WriteResult({"nInserted":1})</code> 表示添加成功，使用 <code>db.user.save({id:1,name:"小明",age:22})</code> 也可以完成添加功能。</p>
<p>（6）查看集合。</p>
<p>show collections 或者 show tables，都是查看当前数据库全部集合的命令。</p>
<pre><code>show tables
show collections
</code></pre>
<p><img src="https://images.gitbook.cn/f1f7b710-bb4d-11e9-8b7d-b7dd9ffab41a" width = "50%" /></p>
<p>（7）清空集合。</p>
<p>如果 remove() 方法参数为空，会删除集合中所有数据。</p>
<pre><code>db.user.remove({})
</code></pre>
<p><img src="https://images.gitbook.cn/04d37180-bb4e-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>（8）删除集合。</p>
<pre><code>db.user.drop()
</code></pre>
<p><img src="https://images.gitbook.cn/1a924eb0-bb4e-11e9-9c35-9730454d953c" width = "60%" /></p>
<p>返回 true，表示删除成功。</p>
<h3 id="-3">对数据的操作</h3>
<p>（9）查询全部数据。</p>
<pre><code>db.user.find()
</code></pre>
<p><img src="https://images.gitbook.cn/32bf93d0-bb4e-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>如图，查询出了全部数据，我们可以看到每一条数据除了 id、name、age 属性之外，还有一个 _id 属性，并且其类型为 ObjectId，该属性是 MongoDB 自动添加的，相当于主键，并且不会重复，所以我们就不需要设置自增来保证主键的唯一性了。</p>
<p>（10）精确查找，比如，查找 id=1 的数据。</p>
<pre><code>db.user.find({id:1})
</code></pre>
<p><img src="https://images.gitbook.cn/5b4fa420-bb4e-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>（11）查询结果集合中的第 1 条数据。</p>
<p>如果同时查询出多条符合条件的数据，可以使用 findOne 来获取第 1 条结果。</p>
<pre><code>db.user.findOne({age:22})
</code></pre>
<p><img src="https://images.gitbook.cn/b91d0200-bb4e-11e9-9c35-9730454d953c" width = "60%" /></p>
<p>（12）分页查询。</p>
<p>MongoDB 的分页查询很简单，语法类似于 MySQL，使用 limit 关键字完成，比如，查询前 3 条记录。</p>
<pre><code>db.user.find().limit(3)
</code></pre>
<p><img src="https://images.gitbook.cn/ceeb6f90-bb4e-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>如果要查询第 2 页的 3 条记录，结合 skip() 方法，skip(num) 是跳过前 num 条记录。</p>
<pre><code>db.user.find().skip(3).limit(3)
</code></pre>
<p><img src="https://images.gitbook.cn/e151abe0-bb4e-11e9-a9cb-6dccb8815b89" width = "50%" /></p>
<p>查询的结果是第 4 条到第 6 条记录。</p>
<p>（13）查询排序。</p>
<p>根据 age 的值进行升序排列。</p>
<pre><code>db.user.find().sort({age:1})
</code></pre>
<p><img src="https://images.gitbook.cn/f0aaa830-bb4e-11e9-9098-7f652ba8c5a9" width = "50%" /></p>
<p>根据 age 的值进行降序排列。</p>
<pre><code>db.user.find().sort({age:-1})
</code></pre>
<p><img src="https://images.gitbook.cn/fecd6e70-bb4e-11e9-a9cb-6dccb8815b89" width = "50%" /></p>
<p>（14）修改。</p>
<p>将 id:1 的数据 name 值修改为 Tom。</p>
<pre><code>db.user.update({id:1},{id:1,name:"Tom",age:22})
</code></pre>
<p><img src="https://images.gitbook.cn/15c62b30-bb4f-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>修改完成之后，再查询，可以看到 name 已经改为了 Tom。</p>
<p>（15）如果修改一条不存在的数据，不会报错，对数据没有做出修改，并给出信息。</p>
<pre><code>db.user.update({id:11},{id:11,name:"Tom",age:22})
</code></pre>
<p><img src="https://images.gitbook.cn/29c4bac0-bb4f-11e9-8b7d-b7dd9ffab41a" width = "50%" /></p>
<p>nMatched 表示匹配成功为 0 条，nModified 表示修改的数据为 0 条。</p>
<p>（16）我们给 update 方法添加一个参数，结果就不一样了。</p>
<pre><code>db.user.update({id:11},{id:11,name:"Tom",age:22},true)
</code></pre>
<p><img src="https://images.gitbook.cn/3a99cfc0-bb4f-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>nUpserted 表示如果数据不存在，先创建，再修改，所以 update 方法的第 3 个 boolean 类型参数表示的是如果数据不存在，是否要创建，默认值为 false，表示不创建。</p>
<p>（17）如果同时存在多条匹配的数据，默认只修改第一条。</p>
<pre><code>db.user.update({age:22},{id:22,name:"David",age:18},false)
</code></pre>
<p><img src="https://images.gitbook.cn/4b739fb0-bb4f-11e9-a9cb-6dccb8815b89" width = "50%" /></p>
<p>如图，只有一条 age:22 的数据被修改了，如果需要多 age:22 的数据全部进行修改，添加一个参数即可，同样是 boolean 类型的参数，默认 false 表示只修改第一条，true 表示全部修改，需要注意的是最后一个参数为 true 时的时候必须使用 <code>{$set:}</code> 进行更新。</p>
<pre><code>db.user.update({age:22},{$set:{id:22,name:"Jack",age:16}},false,true)
</code></pre>
<p><img src="https://images.gitbook.cn/5a28bae0-bb4f-11e9-9c35-9730454d953c" width = "50%" /></p>
<p>（18）删除数据。</p>
<p>将 age:16 的数据删除，集合中所有满足 age:16 的数据都会被删除。</p>
<pre><code>db.user.remove({age:16})
</code></pre>
<p><img src="https://images.gitbook.cn/69886df0-bb4f-11e9-8b7d-b7dd9ffab41a" width = "50%" /></p>
<h3 id="-4">总结</h3>
<p>本节课我们讲解了 MongoDB 数据库的常用命令，完成对数据的 CRUD 操作，与传统关系型数据库的 SQL 语句有类似之处，但是 MongoDB 命令的特点是更加简单灵活。</p>
<h3 id="-5">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote>
<p><a href="https://github.com/southwind9801/springmvc-dataconverter.git">请单击这里下载源码</a></p></div></article>