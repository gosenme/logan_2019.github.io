---
title: Angular 基础教程-72
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在实际的业务开发过程中，我们经常需要限制某些 URL 的可访问性，比如，对于系统管理界面，只有那些拥有管理员权限的用户才能打开。</p>
<p>我看到过一些简化的处理方案，比如把菜单隐藏起来，但是这样做是不够的，因为用户还可以自己手动在地址栏里面尝试输入，或者更暴力一点，可以通过工具来强行遍历 URL。</p>
<blockquote>
  <p>请特别注意：前端代码应该默认被看成是不安全的，安全的重头戏应该放在 Server 端，而前端只是做一些基本的防护。</p>
</blockquote>
<p>在 Angular 里面，权限控制的任务由“路由守卫”来负责，路由守卫的典型用法：</p>
<ul>
<li>控制路由能否激活</li>
<li>控制路由的能否退出</li>
<li>控制异步模块能否被加载</li>
</ul>
<h3 id="">控制路由能否激活</h3>
<p>代码结构：</p>
<p><img width="30%" src="https://images.gitbook.cn/3e6efad0-f2f5-11e8-87c8-f50ecfad80b5"></p>
<p>auth.guard.ts 里面这样写：</p>
<pre><code>import { Injectable } from '@angular/core';
import { CanLoad, CanActivate, CanActivateChild } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable()
export class AuthGuard implements CanLoad,CanActivate,CanActivateChild{

    constructor(private authService:AuthService){

    }

    /**
     * 验证路由是否可以激活
     */
    canActivate(){
        //在真实的应用里面需要写一个 Service 到后端去验证权限
        return this.authService.canActivate();
    }

    /**
     * 验证子路由是否可以激活
     */
    canActivateChild(){
        //在真实的应用里面需要写一个 Service 到后端去验证权限
        return true;
    }
}
</code></pre>
<p>别忘记把相关的服务放到 app.module.ts 里面去：</p>
<pre><code>providers: [AuthService,AuthGuard]
</code></pre>
<p>然后 app.routes.ts 里面这样配置：</p>
<pre><code>{
    path:'jokes',
    data:{preload:true},
    canActivate:[AuthGuard],
    loadChildren:'./jokes/jokes.module#JokesModule'
}
</code></pre>
<p>这里的 canActivate 配置项就是用来控制路由是否能被激活的，如果 AuthGuard 里面对应的 canActivate 方法返回 false，jokes 这个路由就无法激活。</p>
<p>在所有子模块的路由里面也可以做类似的配置。</p>
<h3 id="-1">控制路由的退出</h3>
<p>有时候，我们还需要控制路由能否退出。</p>
<p>比如，当用户已经在表单里面输入了大量的内容，如果不小心导航到了其他 URL，那么输入的内容就会全部丢失。很显然，这会让用户非常恼火。</p>
<p>因此，我们需要做一定的防护，避免这种意外的情况。</p>
<p>这个例子的运行界面如下：</p>
<p><img width="60%" src="https://images.gitbook.cn/63da99a0-f2f5-11e8-846c-655c5a3d2587"></p>
<p>我们给 jokes 模块单独写了以守卫：</p>
<p><img width="30%" src="https://images.gitbook.cn/82171420-f2f5-11e8-9048-db873aaf0d56"></p>
<p>jokes-guard.ts 里面的内容如下：</p>
<pre><code>import { Injectable } from '@angular/core';
import { CanDeactivate } from '@angular/router';
import { JokesComponent } from './jokes.component';

@Injectable()
export class JokesGuard implements CanDeactivate&lt;any&gt;{
   canDeactivate(component:JokesComponent){
       console.log(component);
       if(!component.saved){
           return window.confirm("确定不保存吗？");
       }
       return true;
   }
}
</code></pre>
<blockquote>
  <p>注意 jokes.module.ts 和 jokes.routes.ts 里面相关的配置。</p>
</blockquote>
<h3 id="-2">控制模块能否被加载</h3>
<p>除了可以控制路由能否被激活之外，还可以控制模块能否被加载，处理方式类似，在 AuthGuard 里面增加一个处理方法：</p>
<pre><code>/**
 * 验证是否有权限加载一个异步模块
 */
canLoad(){
    //在真实的应用里面需要写一个 Service 到后端去验证权限
    return this.authService.canLoad();
}
</code></pre>
<p>如果 canLoad 方法返回 false，模块就根本不会被加载到浏览器里面了。</p>
<h3 id="-3">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-router">完整可以运行的示例代码请参见这里下载</a>，代码在 guard 分支上。</p></div></article>