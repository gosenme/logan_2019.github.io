---
title: Angular 基础教程-85
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="injectable">自动档——@Injectable</h3>
<p>在上一课里面， UserListService 服务直接返回了一个数组字面值。在真实的应用中，我们需要到服务端去加载数据，这就需要用到 Angular 提供的 HttpClient 服务了，这里我们需要把 HttpClient 服务注射到 UserListService 服务里面去，做法如下：</p>
<p><img src="https://images.gitbook.cn/b43344e0-f450-11e8-9460-178de39eb82c" width = "45%" /></p>
<p>别忘记在 app.module 里面 import 一下 HttpClientModule：</p>
<p><img src="https://images.gitbook.cn/d332e850-f450-11e8-a018-a3bc43149496" width = "45%" /></p>
<p>我们注意到，在以上第一段代码里面，UserListService 顶部有一个 @Injectable 装饰器。那么 @Injectable 到底对 UserListService 做了什么事情呢？</p>
<p>我们来看 ng build 之后生成的代码：</p>
<p><img src="https://images.gitbook.cn/fcb9dbc0-f450-11e8-b435-7f45fd734750" width = "70%" /></p>
<p>可以看到，编辑器生成了一些奇怪的东西，看起来像是保留了一些类型信息。</p>
<p>如果我们把 @Injectable 装饰器会怎么样呢？来看最终编译出来的代码：</p>
<p><img src="https://images.gitbook.cn/2ec34e80-f451-11e8-9460-178de39eb82c" width = "60%" /></p>
<p>可以看到，去掉 @Injectable 装饰器之后，生成出来的代码发生了很大的变化，而且运行会报错：</p>
<p><img src="https://images.gitbook.cn/4b19f200-f451-11e8-a977-e1307f4c402a" width = "70%" /></p>
<p>OK，我们大概可以猜到 @Injectable 装饰器的作用了：如果存在 @Injectable 装饰器，TS 编译器就会在最终生成的代码里面保留类型元数据，然后 Angular 在运行时就可以根据这些信息来注射指定的对象。否则，运行时就无法解析参数类型了。</p>
<p><strong>简而言之：如果一个 Service 里面需要依赖其他 Service，需要使用 @Injectable 装饰器进行装饰。</strong></p>
<p><strong>为了不给自己找麻烦，最好所有 Service 都加上 @Injectable 装饰器，这是一种良好的编码风格。用 @angular/cli 生成的 Service 会自动在头部加上 @Injectable 装饰器，不需要操心。</strong></p>
<h3 id="inject">手动档——利用 @Inject 自己指定类型信息</h3>
<p>除了在 UserListService 顶部添加 @Injectable 装饰器之外，还有一种非常不常用的方法，利用 @Inject 装饰器手动指定类型信息，代码如下：</p>
<p><img src="https://images.gitbook.cn/cecc1650-f451-11e8-b435-7f45fd734750" width = "50%" /></p>
<p>编译之后生成的代码如下：</p>
<p><img src="https://images.gitbook.cn/24df26e0-f452-11e8-b435-7f45fd734750" width = "70%" /></p>
<p>可以看到，我们自己使用 @Inject 装饰器编译之后也生成了对应的类型元数据，并且运行起来也不会报错。</p>
<p><strong>仔细观察你就会发现，用 @Inject 和用 @Injectable 最终编译出来的代码是不一样的。用 @Inject 生成的代码多了很多东西，如果出现大量这种代码，最终编译出来的文件体积会变大。</strong></p>
<h3 id="inject-1">@Inject 的其他用法</h3>
<p>在以上例子里面，我们注入的都是强类型的对象。</p>
<p>有人就会问了：如果我想注入弱类型的对象字面值可不可以呢？</p>
<p>当然可以，但是稍微麻烦一点。</p>
<p>比如想把这样一个配置对象注入给 LiteralService 服务：</p>
<p><img src="https://images.gitbook.cn/6d0f9000-f469-11e8-8321-9399b4917b1a" width = "70%" /></p>
<p>app.module 里面是这样配置的：</p>
<p><img src="https://images.gitbook.cn/81dc6c10-f469-11e8-9194-6f914b6fd4f7" width = "70%" /></p>
<p>在 LiteralService 里面使用 @Inject 来注入：</p>
<p><img src="https://images.gitbook.cn/95c095d0-f469-11e8-8bb4-954392f55535" width = "50%" /></p>
<p>运行起来的结果：</p>
<p><img src="https://images.gitbook.cn/ab98a050-f469-11e8-8321-9399b4917b1a" width = "70%" /></p>
<p><strong>特别注意：这种玩法非常罕见，除非你想自己实现一些特别的功能才用得到。比如上面这个例子，可以直接利用 TypeScript 的 import 机制，直接把配置文件 import 进来完事。</strong></p>
<h3 id="">总结</h3>
<p>简而言之，@Injectable 与@Inject 之间的关系，就像自动档和手动档的区别，如果不是有奇怪的癖好，当然是自动档开起来舒服，老司机都懂的。</p>
<ul>
<li>我们可以自己手动用 @Inject 装饰器来让 TypeScript 编译器保留类型元数据，但是一般来说不需要这么干（也就是说，@Inject 装饰器一般是用不到的，除非你想做一些其他的事情）。</li>
<li>保留类型元数据的另一个简便方法是使用 @Injectable 装饰器，@Injectable 并没有什么神奇的作用，它只是告诉 TS 编译器：请生成类型元数据，然后 Angular 在运行时就知道应该注射什么类型的对象了。</li>
<li>这是 TypeScript 强加的一个规则，如果不加 @Injectable 装饰器，TS 编译器会把参数类型元数据丢弃。</li>
<li><strong>对于 Angular 中的 Service 来说，最好都加上 @Injectable 装饰器，这是一种良好的编码风格。</strong></li>
</ul>
<h3 id="-1">参考资源</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-dependency-injection">本节课的实例代码请单击这里下载</a>，在 injectable-decorator 分支上。</p></div></article>