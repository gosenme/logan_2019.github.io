---
title: Angular 基础教程-71
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我们在前面的实例基础上继续修改，为了方便接下来演示“模块预加载”，我们增加了一个一级导航菜单叫做“图片”：</p>
<p><img width="50%" src="https://images.gitbook.cn/fcbc9e60-f2f1-11e8-9048-db873aaf0d56"></p>
<p>现在有 3 个独立的模块：首页、段子、图片，只有当用户单击这些模块的时候，路由才会去异步加载对应的 chunk（块），就像这样：</p>
<p><img width="60%" src="https://images.gitbook.cn/8c4db370-f2f2-11e8-87c8-f50ecfad80b5"></p>
<p>一切看起来都那么完美！但是，产品经理又妖娆地走过来了，他对你说：小伙子干得不错！但是我有一个想法，你看能不能实现？虽然这种异步加载的方式确实能提升加载和执行的效率，但是用户体验并没有做到极致，你看啊，咱们是一个段子站，根据我们的统计数据，这 3 个模块用户都是一定会点的。因此，在首页模块加载完成之后，如果能把“段子”和“图片”这两个模块预先加载到客户端就好了。这样当用户单击这两个菜单的时候，看起来就像“秒开”一样，这才叫“极致体验”对吧？怎么样，有没有技术上的困难？下班之前能改好吧？</p>
<p>你一听就来劲了：看你说的，在我这儿从来不存在什么“技术上的困难”，下班之前保证搞定！</p>
<p>在这个场景下，“预加载”就派上用场了，你需要修改一下 app.module.ts，相关的内容要改成这样：</p>
<pre><code>import { RouterModule, PreloadAllModules } from '@angular/router';
</code></pre>
<pre><code>RouterModule.forRoot(appRoutes,{preloadingStrategy:PreloadAllModules})
</code></pre>
<p>改完之后刷一下浏览器，效果看起来挺不错，所有模块都预加载进来了：</p>
<p><img width="60%" src="https://images.gitbook.cn/8c4db370-f2f2-11e8-87c8-f50ecfad80b5"></p>
<p>Angular 内置了两种预加载策略：PreloadAllModules 和 NoPreloading，PreloadAllModules 的意思是：预加载所有模块，不管有没有被访问到。也就是说，要么就一次预加载所有异步模块，要么就彻底不做预加载。</p>
<p>本来到这里产品经理的要求已经达成了，但是你是一个有情怀的人，一想到产品经理说的“极致体验”，还有他每次走过来的时候那种妖娆的姿势，你的热情又被点燃了起来。</p>
<p>你仔细看了一下上面的代码，总感觉这种“一次预加载所有模块”的方式太简单粗暴了一点儿。而且根据你自己的预测，将来这个系统还会开发更多的模块，如果总是一次性全部预加载，总感觉怪怪的。于是，你想进一步做一些优化，希望实现自己的预加载策略，最好能在路由配置里面加入一些自定义的配置项，让某些模块预加载、某些模块不要进行预加载，就像这样：</p>
<pre><code>{
    path:'jokes',
    data:{preload:true},
    loadChildren:'./jokes/jokes.module#JokesModule'
},
{
    path:'picture',
    data:{preload:false},
    loadChildren:'./picture/picture.module#PictureModule'
}
</code></pre>
<p>当 preload 这个配置项为 true 的时候，就去预加载对应的模块，否则什么也不做，于是你实现了一个自己的预加载策略：</p>
<p><img width="30%" src="https://images.gitbook.cn/1e3eb180-f2f3-11e8-9048-db873aaf0d56"></p>
<p>my-preloading-strategy.ts 里面的内容如下：</p>
<pre><code>import { Route,PreloadingStrategy } from '@angular/router';
import { Observable } from "rxjs";
import "rxjs/add/observable/of";

export class MyPreloadingStrategy implements PreloadingStrategy {
    preload(route: Route, fn: () =&gt; Observable&lt;any&gt;): Observable&lt;any&gt;{
        return route.data&amp;&amp;route.data.preload?fn():Observable.of(null);
    }
}
</code></pre>
<p>当然，别忘记修改一下 app.module.ts 里面的配置，换成你自己的预加载策略：</p>
<pre><code>RouterModule.forRoot(appRoutes,{preloadingStrategy:MyPreloadingStrategy})
</code></pre>
<p>OK，这样一来，模块预加载的控制权就完全交到你自己的手里了，你可以继续修改这个预加载策略，比如用加个延时，或者根据其他某个业务条件来决定是不是要执行预加载，如此等。</p>
<p>产品经理笑嘻嘻地跟你说：你看，我就知道你是我们这里最棒的，一出手分分钟搞定。</p>
<p>你乐呵呵地说：那必须啊，老将出马，一个顶俩。</p>
<p>而你心里的实际想法是：哎，真是站着说话不腰疼，反正不用你写代码，你知不知道为了搞这个破东西害得我改了一大堆东西！幸亏小爷我比较机智，这次还超前做了一些灵活的配置项，就等你小子下回再来改需求了。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码在这里</a>，这个例子对应的代码在 preload-module 分支上。</p></div></article>