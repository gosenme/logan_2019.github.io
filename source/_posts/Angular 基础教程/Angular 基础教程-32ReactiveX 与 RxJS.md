---
title: Angular 基础教程-32
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="reactivexrxjs">ReactiveX 与 RxJS</h3>
<p>ReactiveX 本身是一种编程范式，或者叫一种设计思想，目前有Java/C++/Python 等 18 种语言实现了 ReactiveX，RxJS 是其中的 JavaScript 版本。</p>
<p>ReactiveX 的官方网站在这里：<a href="http://reactivex.io/">http://reactivex.io/</a>，上面有详细介绍、入门文档、技术特性等。</p>
<p>这篇文章不会重复文档上已经有的内容，而是从另外一个视角，带你领略 RxJS 的核心用法。</p>
<h3 id="promise">回调地狱与 Promise</h3>
<p>在使用 Ajax 的过程中，经常会遇到这种情况：我们需要在一个 Ajax 里面嵌套另一个 Ajax 调用，有时候甚至需要嵌套好几层 Ajax 调用，于是就形成了所谓的“回调地狱”：</p>
<p><img width="80%" src="https://images.gitbook.cn/0113c240-cce5-11e9-9f23-07a3e2a236db"></p>
<p>这种代码最大的问题是可读性非常差，时间长了之后根本无法维护。</p>
<p>Promise 的出现主要就是为了解决这个问题，在 Promise 的场景下，我们可以这样写代码：</p>
<pre><code>new Promise(function(resolve,reject){
    //异步操作之后用 resolve 返回 data
})
.then(function(data){
    //依赖于 Promise 的第一个异步操作
})
.then(function(data){
    //依赖于 Promise 的第二个异步操作
})
.then(function(data){
    //依赖于 Promise 的第三个异步操作
})
.catch(function(reason){
    //处理异常
});
</code></pre>
<p>很明显，这样的代码可读性就强太多了，而且未来维护起来也很方便。</p>
<p>当然，Promise 的作用不止于此，如果你想更细致地研究 Promise，请看 MDN 上的这篇资料：</p>
<blockquote>
  <p><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise</a></p>
</blockquote>
<h3 id="rxjspromise">RxJS 与 Promise 的共同点</h3>
<p>RxJS 与 Promise 具有相似的地方，请看以下两个代码片段：</p>
<pre><code>let promise = new Promise(resolve =&gt; {
    setTimeout(() =&gt; {
        resolve('---promise timeout---');
    }, 2000);
});
promise.then(value =&gt; console.log(value));
</code></pre>
<pre><code>let stream1$ = new Observable(observer =&gt; {
    let timeout = setTimeout(() =&gt; {
        observer.next('observable timeout');
    }, 2000);

    return () =&gt; {
        clearTimeout(timeout);
    }
});
let disposable = stream1$.subscribe(value =&gt; console.log(value));
</code></pre>
<p>可以看到，RxJS 和 Promise 的基本用法非常类似，除了一些关键词不同。Promise 里面用的是 then() 和 resolve()，而 RxJS 里面用的是 next() 和 subscribe()。</p>
<h3 id="rxjspromise3">RxJS 与 Promise 的 3 大重要不同点</h3>
<p>任何一种技术或者框架，一定要有自己的特色，如果跟别人完全一样，解决的问题也和别人一样，那存在的意义和价值就会遭到质疑。</p>
<p>所以，RxJS 一定有和 Promise 不一样的地方，最重要的不同点有 3 个，请看下图：</p>
<p><img width="60%" src="https://images.gitbook.cn/366bead0-cce5-11e9-beb5-a53251e30de8"></p>
<p>依次给 3 块代码来示范一下：</p>
<pre><code>let promise = new Promise(resolve =&gt; {
    setTimeout(() =&gt; {
        resolve('---promise timeout---');
    }, 2000);
});
promise.then(value =&gt; console.log(value));
</code></pre>
<pre><code>let stream1$ = new Observable(observer =&gt; {
    let timeout = setTimeout(() =&gt; {
        observer.next('observable timeout');
    }, 2000);

    return () =&gt; {
        clearTimeout(timeout);
    }
});
let disposable = stream1$.subscribe(value =&gt; console.log(value));
setTimeout(() =&gt; {
    disposable.unsubscribe();
}, 1000);
</code></pre>
<p>从以上代码可以看到，Promise 的创建之后，动作是无法撤回的。Observable 不一样，动作可以通过 unsbscribe() 方法中途撤回，而且 Observable 在内部做了智能的处理，如果某个主题的订阅者为 0，RxJS 将不会触发动作。</p>
<pre><code>let stream2$ = new Observable&lt;number&gt;(observer =&gt; {
    let count = 0;
    let interval = setInterval(() =&gt; {
        observer.next(count++);
    }, 1000);

    return () =&gt; {
        clearInterval(interval);
    }
});
stream2$.subscribe(value =&gt; console.log("Observable&gt;"+value));
</code></pre>
<p>以上代码里面我们用 setInterval 每隔一秒钟触发一个新的值，源源不断，就像流水一样。</p>
<p>这一点 Promise 是做不到的，对于 Promise 来说，最终结果要么 resole（兑现）、要么 reject（拒绝），而且都只能触发一次。如果在同一个 Promise 对象上多次调用 resolve 方法，则会抛异常。而 Observable 不一样，它可以不断地触发下一个值，就像 next() 这个方法的名字所暗示的那样。</p>
<pre><code>let stream2$ = new Observable&lt;number&gt;(observer =&gt; {
    let count = 0;
    let interval = setInterval(() =&gt; {
        observer.next(count++);
    }, 1000);

    return () =&gt; {
        clearInterval(interval);
    }
});
stream2$
.pipe(
    filter(val =&gt; val % 2 == 0)
)
.subscribe(value =&gt; console.log("filter&gt;" + value));

stream2$
.pipe(
    map(value =&gt; value * value)
)
.subscribe(value =&gt; console.log("map&gt;" + value));
</code></pre>
<p>在上述代码里面，我们用到了两个工具函数：filter 和 map。</p>
<ul>
<li>filter 的作用就如它的名字所示，可以对结果进行过滤，在以上代码里面，我们只对偶数值有兴趣，所以给 filter 传递了一个箭头函数，当这个函数的返回值为 true 的时候，结果就会留下来，其它值都会被过滤掉。</li>
<li>map 的作用是用来对集合进行遍历，比如例子里面的代码，我们把 Observable 返回的每个值都做了一次平方，然后再传递给监听函数。</li>
</ul>
<p>类似这样的工具方法在 Observable 里面叫做 operator（操作符），所以有人说 Observable 就相当于异步领域的 Underscore 或者 lodash，这样的比喻是非常贴切的。这也是 Observable 比较强的地方，Promise 里面就没有提供这些工具函数。</p>
<p>Observable 里面提供了数百个这样的“操作符”，完整的列表和 API 文档请参考这里：</p>
<blockquote>
  <p><a href="http://reactivex.io/documentation/operators.html">http://reactivex.io/documentation/operators.html</a></p>
</blockquote>
<p>RxJS 官方的 GitHub 仓库在这里：</p>
<blockquote>
  <p><a href="https://github.com/ReactiveX/rxjs.git">https://github.com/ReactiveX/rxjs.git</a></p>
</blockquote>
<p><strong>特别注意</strong>：Angular 5.0之后，修改了 RxJS 的 import 方式，与其它模块的引入格式进行了统一。</p>
<pre><code>import { Observable, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, map, filter } from 'rxjs/operators';
</code></pre>
<p>我也看到有一些朋友在抱怨，说 RxJS 太过复杂，操作符（operator）的数量又特别多，不知道在什么场景下面应该用什么操作符。</p>
<p>实际上这种担心是多余的，因为在 RxJS 里面最常用的操作符不超过 10 个，不常用的操作符都可以在使用的时候再去查阅文档。</p>
<p>RxJS 和你自己开发的系统一样，常用的功能只有其中的 20%，而剩余  80% 的功能可能永远不会被用到。所以，RxJS 并不像很多人说的那么玄乎，你一定能学会，我相信你。</p>
<h3 id="rxjsangular1http">RxJS 在 Angular 的典型应用场景 1：HTTP 服务</h3>
<pre><code>this.http
.get(url, { search: params })
.pipe(
    map((res: Response) =&gt; {
        let result = res.json();
        console.log(result);
        return result;
    }),
    catchError((error: any) =&gt; Observable.throw(error || 'Server error'))
);
</code></pre>
<p>在新版本的 Angular 里面，HTTP 服务的返回值都是 Observable 类型的对象，所以我们可以 subscribe（订阅）这个对象。当然，Observable 所提供的各种“操作符”都可以用在这个对象上面，比如上面这个例子就用到了 map 操作符。</p>
<h3 id="rxjsangular2">RxJS 在 Angular 的典型应用场景 2：事件处理</h3>
<pre><code>this.searchTextStream
.pipe(
    debounceTime(500),
    distinctUntilChanged()
)
.subscribe(searchText =&gt; {
    console.log(this.searchText);
    this.loadData(this.searchText)
});
</code></pre>
<p>这个例子里面最有意思的部分是 debounceTime 方法和 distinctUntilChanged 方法，这是一种“去抖动”效果。“去抖动”这个场景非常能体现 Observable 的优势所在，有一些朋友可能没遇到过这种场景，我来解释一下，以防万一。</p>
<p>在搜索引擎里面，我们经常会看到这样的效果：</p>
<p><img width="70%" src="https://images.gitbook.cn/c6b83990-cce5-11e9-8d89-4fa271cb1633"></p>
<p>这种东西叫做“动态搜索建议”，在用户敲击键盘的过程中，浏览器已经向后台发起了请求，返回了一些结果，目的是给用户提供一些建议。</p>
<p>效果看起来很简单，但是如果没有这个 debounceTime 工具函数，我们自己实现起来是非常麻烦的。这里的难点在于：用户敲击键盘的过程是源源不断的，我们并不知道用户什么时候才算输入完成。所以，如果让你自己来从零开始实现这种效果，你将会不得不使用定时器，不停地注册、取消，自己实现延时，还要对各种按键码做处理。</p>
<p>在 Observable 里面，处理这种情况非常简单，只要一个简单的 debounceTime 加 distinctUntilChanged 调用就可以了。</p>
<h3 id="">小结</h3>
<ul>
<li>ReactiveX 本身是一种编程范式，或者叫一种设计思想，RxJS 是其中的一种实现，其它还有 Java/C++/Python 等15种语言的实现版本。ReactiveX 本身涉及到的内容比较多，特别是一些设计思想层面的内容，如果你对它特别有兴趣，请参考官方的站点：<a href="http://reactivex.io">http://reactivex.io</a>。</li>
<li>关于 RxJS 目前已经有专门的书籍来做介绍，但是还没有中文版。在网络上有各种翻译和文章，如果你想深入研究，请自行搜索。</li>
<li>RxJS 是 Angular 内核的重要组成部分，它和 Zone.js 一起配合实现了“变更检测”机制，所以在编写 Angular 应用的过程中应该优先使用 RxJS 相关的 API。</li>
<li>RxJS 可以独立使用，它并不一定要和 Angular 一起使用。</li>
<li>本节所有的实例代码都在这里：<a href="https://gitee.com/mumu-osc/NiceFish">https://gitee.com/mumu-osc/NiceFish</a>，这篇文章里面涉及到的完整案例代码在 postlist.component.ts 和 postlist.service.ts 这两份文件里面。</li>
</ul></div></article>