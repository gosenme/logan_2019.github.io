---
title: Angular 基础教程-70
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">路由的基本用法</h3>
<p>我们从最简单的例子开始，第一个例子的运行效果如下：</p>
<p><img width="50%" src="https://images.gitbook.cn/d587aae0-f2e9-11e8-9048-db873aaf0d56"></p>
<p>代码结构：</p>
<p><img width="35%" src="https://images.gitbook.cn/eb7d4f80-f2e9-11e8-9048-db873aaf0d56"></p>
<p>app.routes.ts 里面就是路由规则配置，内容如下：</p>
<pre><code>import { RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {JokesComponent} from './jokes/jokes.component';

export const appRoutes=[
    {
        path:'',
        redirectTo:'home',
        pathMatch:'full'
    },
    {
        path:'home',
        component:HomeComponent
    },
    {
        path:'jokes',
        component:JokesComponent
    },
    {
        path:'**',//通配符匹配必须写在最后一个
        component:HomeComponent
    }
];
</code></pre>
<p>app.module.ts 里面首先需要 import 这份路由配置文件：</p>
<pre><code>import { appRoutes } from './app.routes';
</code></pre>
<p>然后 @NgModule 里面的 imports 配置项内容如下：</p>
<pre><code>import { appRoutes } from './app.routes';
</code></pre>
<pre><code>imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes,{enableTracing:true})
]
</code></pre>
<p>HTML 模板里面的写法：</p>
<p><img width="60%" src="https://images.gitbook.cn/01f6fbc0-f2eb-11e8-846c-655c5a3d2587"></p>
<p>这个例子的看点如下。</p>
<ul>
<li>整个导航过程是通过 RouterModule、app.routes.ts、routerLink、router-outlet 这几个东西一起配合完成的。</li>
<li>请单击顶部导航条，观察浏览器地址栏里面 URL 的变化，这里体现的是 Router 模块最重要的作用，就是对 URL 和对应界面状态的管理。</li>
<li>请注意路由配置文件 app.routes.ts 里面的写法，里面全部用的 component 配置项，这种方式叫“同步路由”。也就是说，@angular/cli 在编译的时候不会把组件切分到独立的 chunk（块）文件里面去，当然也不会异步加载，所有的组件都会被打包到一份 js 文件里面去，请看下图：</li>
</ul>
<p><img width="80%" src="https://images.gitbook.cn/4bc83b10-f2eb-11e8-9961-6b220aaaecc1"></p>
<p>你可能会问，如果想要做成异步模块应该怎么做呢？不要着急，下一段里面会举例子。</p>
<ul>
<li>注意文件的切分，我看到很多开发者会把路由配置直接写在 app.module.ts 里面，这样做不太好。因为随着项目功能越加越多，路由配置也会变得越来越多，全部写在一起未来不好维护。配置归配置，代码归代码，文件尽量切清晰一些，坑谁也别坑自己对吧？</li>
<li>通配符配置必须写在最后一项，否则会导致路由无效。</li>
</ul>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请点击这里下载</a>，这个例子对应的代码在 basic 分支上。</p>
<h3 id="-1">路由与懒加载模块</h3>
<p><img width="60%" src="https://images.gitbook.cn/8e135c70-f2eb-11e8-87c8-f50ecfad80b5"></p>
<p>为什么要做模块的懒加载？</p>
<p>目的很简单：提升 JS 文件的加载速度、提升 JS 文件的执行效率。</p>
<p>对于一些大型的后台管理系统来说，里面可能会有上千份 JS 文件，如果把所有 JS 全部都压缩到一份文件里面，那么这份文件的体积可能会超过 5M，这是不能接受的，尤其对于移动端应用。</p>
<p>因此，一个很自然的想法就是：我们能不能按照业务功能把这些 JS 打包成多份 JS 文件，当用户导航到某个路径的时候，再去异步加载对应的 JS 文件。对于大型的系统来说，用户在使用的过程中不太可能会用到所有功能，所以这种方式可以非常有效地提升系统的加载和运行效率。</p>
<p>我们来把上面这个简单的例子改成异步模式，把“主页”和“段子”切分成两个独立的模块，并且做成异步加载的模式。</p>
<p>整体代码结构改成这样：</p>
<p><img width="25%" src="https://images.gitbook.cn/db839470-f2eb-11e8-9961-6b220aaaecc1"></p>
<p>我们给 home 和 jokes 分别加了一个 module 文件和一个 routes 文件。</p>
<p>home.module.ts 里面的内容如下：</p>
<pre><code>import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';
import { homeRoutes } from './home.routes';

@NgModule({
  declarations: [
    HomeComponent
  ],
  imports: [
    RouterModule.forChild(homeRoutes)
  ],
  providers: [],
  bootstrap: []
})
export class HomeModule { }
</code></pre>
<p>home.routes.ts 里面的内容如下：</p>
<pre><code>import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';

export const homeRoutes=[
    {
        path:'',
        component:HomeComponent
    }
];
</code></pre>
<p>jokes 模块相关的代码类似。</p>
<p>最重要的修改在 app.routes.ts 里面，路由的配置变成了这样：</p>
<pre><code>import { RouterModule } from '@angular/router';

export const appRoutes=[
    {
        path:'',
        redirectTo:'home',
        pathMatch:'full'
    },
    {
        path:'home',
        loadChildren:'./home/home.module#HomeModule'
    },
    {
        path:'jokes',
        loadChildren:'./jokes/jokes.module#JokesModule'
    },
    {
        path:'**',
        loadChildren:'./home/home.module#HomeModule'
    }
];
</code></pre>
<p>我们把原来的 component 配置项改成了 loadChildren。</p>
<p>来看运行效果：</p>
<p><img width="60%" src="https://images.gitbook.cn/1ed5c590-f2ec-11e8-9048-db873aaf0d56"></p>
<p>请按 F12 打开浏览器里面的开发者工具，查看网络面板，然后单击顶部的导航条，会看到 0.e7bf37b9868f1788a067.chunk.js 是异步加载进来的。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请单击这里下载</a>，这个例子对应的代码在 async-module 分支上。</p>
<h3 id="n">N 层嵌套路由</h3>
<p>在真实的系统中，菜单肯定不止一层，我们继续修改上面的例子，给它加一个二级菜单，就像这样：</p>
<p><img width="40%" src="https://images.gitbook.cn/7b7e0460-f2ec-11e8-846c-655c5a3d2587"></p>
<p>于是 home 模块的代码结构变成了这样：</p>
<p><img width="25%" src="https://images.gitbook.cn/a8468e40-f2ec-11e8-9961-6b220aaaecc1"></p>
<p>重点的变化在 home.routes.ts 里面：</p>
<pre><code>import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';
import { PictureComponent } from './picture/picture.component';
import { TextComponent } from './text/text.component';

export const homeRoutes=[
    {
        path:'',
        component:HomeComponent,
        children:[
            {
                path:'',
                redirectTo:'pictures',
                pathMatch:'full'
            },
            {
                path:'pictures',
                component:PictureComponent
            },
            {
                path:'text',
                component:TextComponent
            }
        ]
    }
];
</code></pre>
<p>理论上，路由可以无限嵌套，而实际上不可能嵌套得特别深。系统里面有一级、二级、三级菜单很正常，如果你的系统做出了十几级菜单，用户还怎么使用呢？</p>
<p><a href="https://gitee.com/learn-angular-series/learn-router">以上例子完整可运行的代码可单击这里下载</a>，代码在 nested-router 分支上。</p>
<h3 id="-2">共享模块</h3>
<p>刚把嵌套路由的问题搞定，本来以为万事大吉了，这时候产品经理又妖娆地走了过来，他跟你说客户需求改了，需要在页面的侧边栏上面加一个展示用户资料的 Panel（面板），就像这样：</p>
<p><img width="40%" src="https://images.gitbook.cn/a6617330-f2ef-11e8-9048-db873aaf0d56"></p>
<p>同时还提了另一个要求，这个展示用户资料的 Panel 在“段子”这个模块里面也要用，而且未来还可能在其他地方也要使用。</p>
<p>这时候，该轮到“共享模块”机制出场了。因为根据 Angular 的规定：组件必须定义在某个模块里面，但是不能同时属于多个模块。</p>
<p>如果你把这个 UserInfo 面板定义在 home.module 里面，jokes.module 就不能使用了，反之亦然。</p>
<p>当然，你可能说，这还不简单，把 UserInfo 定义在根模块 app.module 里面不就好了嘛。</p>
<p>不错，确实可以这样做。但是这样会造成一个问题：如果系统的功能不断增多，你总不能把所有共用的组件都放到 app.module 里面吧？如果真的这样搞，app.module 最终打包出来会变得非常胖。</p>
<p>所以，更优雅的做法是切分一个“共享模块”出来，就像这样：</p>
<p><img width="60%" src="https://images.gitbook.cn/d9bfc790-f2ef-11e8-846c-655c5a3d2587"></p>
<p>对于所有想使用 UserInfo 的模块来说，只要 import 这个 SharedModule 就可以了。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请单击这里下载</a> ，这个例子对应的代码在 shared-module 分支上。</p>
<h3 id="-3">处理路由事件</h3>
<p>Angular 的路由上面暴露了 7 个事件：NavigationStart 、RoutesRecognized、RouteConfigLoadStart 、RouteConfigLoadEnd、NavigationEnd、NavigationCancel、NavigationError，<a href="https://angular.io/guide/router#router-events">详细的描述可参见这里</a>。</p>
<p>我们可以监听这些事件，来实现一些自己的业务逻辑，示例如下：</p>
<pre><code>import { Component, OnInit } from '@angular/core';
import { Router,NavigationStart } from '@angular/router';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router) {

  }

  ngOnInit() {
    this.router.events.subscribe((event) =&gt; {
      console.log(event);
      //可以用instanceof来判断事件的类型，然后去做你想要做的事情
      console.log(event instanceof NavigationStart);
    });
  }
}
</code></pre>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请单击这里下载</a>，这个例子对应的代码在 router-events 分支上。</p>
<h3 id="-4">如何传递和获取路由参数</h3>
<p>在路由上面传递参数是必备的功能，Angular 的 Router 可以传递两种类型的参数：简单类型的参数、“矩阵式”参数。</p>
<p>请注意以下 routerLink 的写法：</p>
<pre>
&lt;ul class="nav navbar-nav"&gt;
    &lt;li routerLinkActive="active" class="dropdown"&gt;
        &lt;a [routerLink]="['home','1']"&gt;主页&lt;/a&gt;
    &lt;/li&gt;
    &lt;li routerLinkActive="active" class="dropdown"&gt;
        &lt;a [routerLink]="['jokes',{id:111,name:'damo'}]"&gt;段子&lt;/a&gt;
    &lt;/li&gt;
&lt;/ul&gt;
</pre>
<p>在 HomeComponent 里面，我们是这样来获取简单参数的：</p>
<pre><code>constructor(
    public router:Router,
    public activeRoute: ActivatedRoute) { 

}

ngOnInit() {
    this.activeRoute.params.subscribe(
        (params)=&gt;{console.log(params)}
    );
}
</code></pre>
<p>在 JokesComponent 里面，我们是这样来接受“矩阵式”参数的：</p>
<pre><code>constructor(
    public router: Router,
    public activeRoute: ActivatedRoute) {

}

ngOnInit() {
    this.activeRoute.params.subscribe(
        (params) =&gt; { console.log(params) }
    );
}
</code></pre>
<p>“矩阵式”传参 [routerLink]="['jokes',{id:111,name:'damo'}]" 对应的 URL 是这样一种形态：</p>
<pre><code>http://localhost:4200/jokes;id=111;name=damo
</code></pre>
<p>这种 URL 形态不常见，很多开发者应该没有看到过，但是它确实是合法的。它不是 W3C 的规范，但是互联网之父 Tim Berners-Lee 在 1996 年的文档里面有详细的解释，主流浏览器都是支持的，<a href="https://www.w3.org/DesignIssues/MatrixURIs.html">单击这里查看详情</a>。这种方式的好处是，我们可以传递大块的参数，因为第二个参数可以是一个 JSON 格式的对象。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请单击这里下载</a>，这个例子对应的代码在 router-params 分支上。</p>
<h3 id="-5">用代码触发路由导航</h3>
<p>除了通过 &lt;a routerLink="home"&gt; 主页 &lt;/a&gt; 这种方式进行导航之外，还可以通过代码的方式来手动进行导航：</p>
<pre><code>this.router.navigate(["/jokes"],{ queryParams: { page: 1,name:222 } });
</code></pre>
<p>接受参数的方式如下：</p>
<pre><code>this.activeRoute.queryParams.subscribe(
    (queryParam) =&gt; { console.log(queryParam) }
);
</code></pre>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可运行的代码请单击这里下载</a>，这个例子对应的代码在 router-params 分支上。</p></div></article>