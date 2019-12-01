---
title: Angular 基础教程-89
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Host 这个单词有“宿主”的意思，就像病毒和 OS 之间的关系。</p>
<p>读者可以意会一下 @Host 这个装饰器的特性。</p>
<h3 id="host">@Host 的基本用法</h3>
<p>默认情况下，@Host 装饰器会指示注射器在组件自己内部去查找所依赖的类型，就像这样：</p>
<p><img src="http://images.gitbook.cn/d7409d00-2018-11e8-a225-ad40c4dffe6a"  width = "60%" /></p>
<p>如果 @Host 只有这一个特性的话，它就没什么存在的必要了，实际上它更核心的功能与所谓的 Content Projection（内容投影）机制有关。</p>
<h3 id="contentprojection">Content Projection（内容投影）</h3>
<p>有时候，组件内部放什么内容并不固定，而是需要调用方在使用组件的时候去指定，这是 Content Projection 最核心的一个作用。</p>
<p>我们继续修改 ChildComponent 这个组件，在上面使用 @Host 装饰器，但是不配置 UserListService ，就像这样：</p>
<p><img src="http://images.gitbook.cn/dc47d840-2018-11e8-a225-ad40c4dffe6a"  width = "60%" /></p>
<p>父层组件 UserListComponent 的改动幅度比较大，首先还是给它配置了 UserListService，就像这样：</p>
<p><img src="http://images.gitbook.cn/e1240be0-2018-11e8-a225-ad40c4dffe6a"  width = "60%" /></p>
<p>然后还修改了 UserListComponent 的 HTML 模板代码，这里跟前面的例子都不一样，我们不再把&lt;child&gt; 写死在模板内部，而是在模板里面使用了一个 &lt;ng-content&gt; 标签。ng-content 的本质是一个占位符，这个占位符会被真正投影进来的内容替换掉。</p>
<p>现在 UserListComponent 的模板代码如下：</p>
<p><img src="http://images.gitbook.cn/e5df7110-2018-11e8-a225-ad40c4dffe6a"  width = "60%" /></p>
<p>在 AppComponent 的 HTML 模板里面，使用 UserListComponent 的方式也发生了改变，&lt;user-list&gt; 标签的内部嵌套了一个子层标签，这在之前的例子里面是没有出现过的，就像这样：</p>
<p><img src="http://images.gitbook.cn/eb6f8b60-2018-11e8-a225-ad40c4dffe6a"  width = "50%" /></p>
<p>运行起来的效果是这样的：</p>
<p><img src="http://images.gitbook.cn/f014f790-2018-11e8-a225-ad40c4dffe6a"  width = "60%" /></p>
<p>可以看到，投影进来的子组件和父层的宿主组件共用了同一个 UserListService 实例。</p>
<p>用 Augury 图形化展示出来是这样的：</p>
<p><img src="http://images.gitbook.cn/0079be90-2019-11e8-a225-ad40c4dffe6a"  width = "70%" /></p>
<p>“内容投影”的优点在于：UserListComponent 的 HTML 模板没有和 ChildComponent 紧密耦合在一起，因为 ChildComponent 是被“投影”进来的，未来如果你觉得不爽，可以投影一个另外的组件实例进来（当然这里的代码还得小改一番才能实现）。于是，两个组件都变得比较灵活了，而不会出现谁也离不开谁的情况。</p>
<p>@Host 装饰器会提示注射器：要么在组件自己内部查找需要的依赖，要么到 Host（宿主）上去查找。</p>
<p>怎么样，能理解这里 Host 一词的意味了吧？</p>
<p><strong>简而言之：@Host 装饰器是用来在被投影的组件和它的宿主之间构建联系的。</strong></p>
<p>“内容投影”机制还有很多非常重要的作用，在前面的内容中已经有非常琐碎的描述了，如果你还没有深入理解它，请移步过去阅读。</p>
<h3 id="hostoptional">@Host 和 @Optional 组合使用</h3>
<p>如上所述，@Host 会尝试到宿主组件上去查找依赖，那么问题就来了，如果宿主上面并没有所需要的东西，怎么办呢？</p>
<p>借着上面的例子，我们把 UserListComponent 里面配置的 UserListService 注释掉：</p>
<p><img src="http://images.gitbook.cn/f4c6e6e0-2018-11e8-a225-ad40c4dffe6a"  width = "70%" /></p>
<p>然后理所当然就报错了，因为现在宿主上并没有所需要对象：</p>
<p><img src="http://images.gitbook.cn/f98ecf30-2018-11e8-a225-ad40c4dffe6a"  width = "70%" /></p>
<p>如果不想出现这种报错，而且你认为对于 ChildComponent 来说，UserListService 并不是在构造的时候就必须的，@Optional 装饰器就可以派上用场了：</p>
<pre><code>@Host() @Optional() public userListService: UserListService
</code></pre>
<h3 id="">参考资源</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-dependency-injection">本节课的实例代码请单击这里下载</a>，在 host-decorator 分支上。</p></div></article>