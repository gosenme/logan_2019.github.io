---
title: Angular 基础教程-8
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>我不打算在这里罗列 API，在官方网站上面有更详细的描述和例子：</p>
<blockquote>
  <p><a href="https://angular.io/guide/lifecycle-hooks">https://angular.io/guide/lifecycle-hooks</a></p>
</blockquote>
<p>在这一节里面我们只讨论以下 4 件事：</p>
<ul>
<li>什么是 UI 组件的生命周期？</li>
<li>Angular 组件的生命周期有什么特别的地方？</li>
<li>OnPush 策略的使用方式。</li>
<li>简要介绍脏检查的实现原理。</li>
</ul>
<h3 id="1ui">1. UI 组件的生命周期</h3>
<p><img width="30%" src="https://images.gitbook.cn/56550980-b8d1-11e9-a88b-c93a5ea3d618"></p>
<p>无论使用什么样的前端框架，只要编写 UI 组件，生命周期都是必须要考虑的重要内容。请展开你的想象，如果让你来设计 UI 系统，组件有几个重要的阶段一定是绕不开的，比如：</p>
<ul>
<li>初始化（init）阶段：在这个阶段你需要把组件 new 出来，把一些属性设置上去，等等这些操作。</li>
<li>渲染（render）阶段：在这个阶段需你要把组件的模板和数据结合起来，生成 HTML 标签结构，并且要整合到现有的 DOM 树里面去。</li>
<li>存活阶段：既然带有 UI，那么在组件的存活期内就一定会和用户进行交互。一般来说，带有 UI 的系统都是通过事件机制进行用户交互的。也就是说，这个阶段将会处理大量的用户事件：鼠标点击、键盘按键、手指触摸。</li>
<li>销毁（destory）阶段：最后，组件使用完了，需要把一些资源释放掉。最典型的操作：需要把组件上的所有事件全部清理干净，避免造成内存泄漏。</li>
</ul>
<p>在组件生命的不同阶段，框架一般会暴露出一些“接口”，开发者可以利用这些接口来实现一些自己的业务逻辑。这种接口在有些框架里面叫做“事件”，在 Angular 里面叫做“钩子”，但其底层的本质都是一样的。</p>
<h3 id="2angular">2. Angular 组件的生命周期钩子</h3>
<p><img width="100%" src="https://images.gitbook.cn/fbf2cda0-b8d1-11e9-a88b-c93a5ea3d618"></p>
<ul>
<li>Angular 一共暴露了 8 个“钩子”，构造函数不算。</li>
<li>并没有组件或者指令会实现全部钩子。</li>
<li>绿色的 1357 会被执行很多次，2468 只会执行一次。</li>
<li>Content 和 View 相关的 4 个钩子只对组件有效，指令上不能使用。因为在新版本的 Angular 里面，指令不能带有 HTML 模板。指令没有自己的 UI，当然就没有 View 和 Content 相关的“钩子”了。</li>
<li>请不要在生命周期钩子里面实现复杂的业务逻辑，尤其是那 4 个会被反复执行的钩子，否则一定会造成界面卡顿。</li>
<li>对于 @Input 型的属性，在构造函数里面是取不到值的，在 ngOnInit 里面才有值。</li>
<li>在 ngAfterViewChecked 这个钩子里面不可以再修改组件内部被绑定的值，否则会抛出异常。</li>
</ul>
<p><strong>特别注意：对于业务开发者来说，一般只用到 ngOnInit 这个钩子，其它几个钩子在日常业务开发中是用不到的。</strong></p>
<h3 id="3onpush">3. OnPush 策略</h3>
<p>在真实的业务系统中，组件会构成 Tree 型结构，就像这样：</p>
<p><img width="35%" src="https://images.gitbook.cn/2634fac0-b8d2-11e9-8b62-c350e3466c22"></p>
<p>当某个叶子组件上的数据模型发生变化之后，就像这样：</p>
<p><img width="35%" src="https://images.gitbook.cn/2e36b150-b8d2-11e9-a88b-c93a5ea3d618"></p>
<p><strong>这时候，Angular 将会从根组件开始，遍历整颗组件树，把所有组件上的 ngDoCheck() 方法都调用一遍：</strong></p>
<p><img width="35%" src="https://images.gitbook.cn/3df57450-b8d2-11e9-ba33-51636d56aead"></p>
<p><strong>请注意，默认情况下，无论哪个叶子组件上发生了变化，都会把整个组件树遍历一遍。</strong>如果组件树非常庞大，嵌套非常深，很明显会有效率问题。在绝大部分时间里面，并不会出现每个组件都需要刷新的情况，根本没有必要每次都去全部遍历。所以 Angular 提供了一种叫做 OnPush 的策略，只要把某个组件上的检测策略设置为 OnPush，就可以忽略整个子树了，就像这样：</p>
<p><img width="40%" src="https://images.gitbook.cn/582abe70-b8d2-11e9-a88b-c93a5ea3d618"></p>
<p>很明显，使用了 OnPush 策略之后，检查效率将会获得大幅度的提升，尤其在组件的数量非常多的情况下：</p>
<p><img width="60%" src="https://images.gitbook.cn/5f786740-b8d2-11e9-ba33-51636d56aead"></p>
<p>Angular 内置的两种变更检测策略：</p>
<ul>
<li>Default：无论哪个组件发生了变化，从根组件开始全局遍历，调用每个组件上的 ngDoCheck() 钩子。</li>
<li>OnPush：<strong>只有当组件的 @Input 属性发生变化的时候才调用本组件的 ngDoCheck() 钩子。</strong></li>
</ul>
<p>有一些开发者建议 Angular 项目组把 OnPush 作为默认策略，但是目前还没有得到官方支持，或许在未来的某个版本里面会进行修改。</p>
<h3 id="4">4. 了解一点点原理</h3>
<p>如果你不想看到扯原理的内容，可以跳过这一小段。</p>
<p><img width="55%" src="https://images.gitbook.cn/78b3c100-b8d2-11e9-8b62-c350e3466c22"></p>
<p>大家都知道，AngularJS 是第一个把“双向数据绑定”这种设计带到前端领域来的框架，“双向数据绑定”最典型的场景就是对表单的处理。</p>
<p>双向数据绑定的目标很明确：数据模型发生变化之后，界面可以自动刷新；用户修改了界面上的内容之后，数据模型也会发生自动修改。</p>
<p>很明显，这里需要一种同步机制，在 Angular 里面这种同步机制叫做“变更检测”。</p>
<p>在老版本 AgnularJS 里面，变更检测机制实现得不太完善，经常会出现检测不到变更的情况，所以才有了让大家很厌烦的 $apply() 调用。</p>
<p>在新版本的 Angular 里面不再存在这个问题了，因为新版本的 Angular 使用 Zone.js 这个库，它会把所有可能导致数据模型发生变更的情况全部拦截掉，从而在数据发生变化的时候去通知 Angular 进行刷新。</p>
<p>有一些朋友可能会觉得奇怪，Zone.js 怎么这么牛叉？它内部到底是怎么玩的呢？</p>
<p>实际上要做到这一点并不复杂，因为在浏览器环境下，有可能导致数据模型发生变化的情况只有 3 种典型的回调：</p>
<ul>
<li>事件回调：鼠标、键盘、触摸</li>
<li>定时器回调：setTimeout 和 setInterval</li>
<li>Ajax 回调</li>
</ul>
<p>Zone.js 覆盖了所有原生实现，当开发者在调用这些函数的时候，并不是调用的原生方法，而是调用的 Zone.js 自己的实现，因此 Zone.js 就可以做一些自己的处理了。</p>
<p>也就是说 Zone.js 会负责通知 Angular：“数据模型发生变化了”！然后 Angular 的 ChangeDetector 就会在下一次 dirty check 的周期里面来检查哪些组件上的值发生了变化，然后做出相应的处理。</p>
<p>如果你的好奇心特别旺盛，这里有一篇非常长的文章，大约二十多页，详细解释了这一话题：</p>
<blockquote>
  <p><a href="https://blog.thoughtram.io/angular/2016/02/22/angular-2-change-detection-explained.html">https://blog.thoughtram.io/angular/2016/02/22/angular-2-change-detection-explained.html</a></p>
</blockquote>
<h3 id="5">5. 小结</h3>
<p>本节完整可运行的实例代码请参见 <a href="https://gitee.com/learn-angular-series/learn-component">https://gitee.com/learn-angular-series/learn-component</a>，请检出 lifecycle 分支。</p>
<h3 id="">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>