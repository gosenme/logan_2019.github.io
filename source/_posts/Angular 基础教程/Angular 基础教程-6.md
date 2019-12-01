---
title: Angular 基础教程-6
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>模板是编写 Angular 组件最重要的一环，你必须深入理解以下知识点才能玩转 Angular 模板：</p>
<ul>
<li>对比各种 JS 模板引擎的设计思路</li>
<li>Mustache（八字胡）语法</li>
<li>模板内的局部变量</li>
<li>属性绑定、事件绑定、双向绑定</li>
<li>在模板里面使用结构型指令 *ngIf、*ngFor、ngSwitch</li>
<li>在模板里面使用属性型指令 NgClass、NgStyle、NgModel</li>
<li>在模板里面使用管道格式化数据</li>
<li>一些小 feature：安全导航、非空断言</li>
</ul>
<p><strong>“深入理解”的含义是：你需要很自如地运用这些 API，写代码的时候不翻阅 API 文档。</strong></p>
<p><strong>因为很多新手之所以编码效率不高，其中一个主要的原因就是在编码过程中不停翻文档、查资料。</strong></p>
<h3 id="js">对比各种 JS 模板引擎的设计思路</h3>
<p>几乎每一款前端框架都会提供自己的模板语法：</p>
<ul>
<li>在 jQuery 如日中天的时代，有 Handlebars 那种功能超强的模板</li>
<li>React 推崇 JSX 模板语法</li>
<li>当然还有 Angular 提供的那种与“指令”紧密结合的模板语法</li>
</ul>
<p>综合来说，无论是哪一种前端模板，大家都比较推崇“轻逻辑”（logic-less）的设计思路。</p>
<p>何为“轻逻辑”？</p>
<p>简而言之，所谓“轻逻辑”就是说，你不能在模板里面编写非常复杂的 JavaScript 表达式。比如，Angular 的模板语法就有规定：</p>
<ul>
<li>你不能在模板里面 new 对象</li>
<li>不能使用 =、+=、-= 这类的表达式</li>
<li>不能用 ++、-- 运算符</li>
<li>不能使用位运算符</li>
</ul>
<p>为什么要“轻逻辑”？</p>
<p><strong>最重要的原因是怕影响运行性能，因为模板可能会被执行很多次。</strong></p>
<p>比如你编写了以下 Angular 模板：</p>
<pre>
&lt;ul&gt;
    &lt;li *ngFor="let race of races"&gt;
        {{race.name}}
    &lt;/li&gt;
&lt;/ul&gt;
</pre>
<p>很明显，浏览器不认识 *ngFor 和 {{...}} 这种语法，因此必须在浏览器里面进行“编译”，获得对应的模板函数，然后再把数据传递给模板函数，最终结合起来获得一堆 HTML 标签，然后才能把这一堆标签插入到 DOM 树里面去。</p>
<p>如果启用了 AOT，处理的步骤有一些变化，@angular/cli 会对模板进行“静态编译”，避免在浏览器里面动态编译的过程。</p>
<p>而 Handlebars 这种模板引擎完全是运行时编译模板字符串的，你可以编写以下代码：</p>
<pre>
//定义模板字符串
var source=`
&lt;ul&gt;
    {{#each races}}
        &lt;li&gt;{{name}}&lt;/li&gt;
    {{/each}}
&lt;/ul&gt;
`;

//在运行时把模板字符串编译成 JS 函数
var templateFn=Handlebars.compile(source);

//把数据传给模板函数，获得最终的 HTML
var html=templateFn([
    {name:'人族'},
    {name:'神族'},
    {name:'虫族'}
]);
</pre>
<p>注意到 Handlebars.compile 这个调用了吧？这个地方的本质是在运行时把模板字符串“编译”成了一个 JS 函数。</p>
<p>鉴于 JS 解释执行的特性，你可能会担忧这里会有性能问题。这种担忧是合理的，但是 Handlebars 是一款非常优秀的模板引擎，它在内部做了各种优化和缓存处理。模板字符串一般只会在第一次被调用的时候编译一次，Handlebars 会把编译好的函数缓存起来，后面再次调用的时候会从缓存里面获取，而不会多次进行“编译”。</p>
<p>上面我们多次提到了“编译”这个词，因此很显然这里有一个东西是无法避免的，那就是我们必须提供一个 JS 版的“编译器”，让这个“编译器”运行在浏览器里面，这样才能在运行时把用户编写的模板字符串“编译”成模板函数。</p>
<p>有一些模板引擎会真的去用 JS 编写一款“编译器”出来，比如 Angular 和 Handlebars，它们都真的编写了一款 JS（TS）版的编译器。而有一些简单的模板引擎，例如 Underscore 里面的模板函数，只是用正则表达式做了字符串替换而已，显得特别简陋。这种简陋的模板引擎对模板的写法有非常多的限制，因为它不是真正的编译器，能支持的语法特性非常有限。</p>
<p>因此，评估一款模板引擎的强弱，最核心的东西就是评估它的“编译器”做得怎么样。但是不管怎么说，毕竟是 JS 版的“编译器”，我们不可能把它做得像 G++ 那么强大，也没有必要做得那么强大，因为这个 JS 版的编译器需要在浏览器里面运行，搞得太复杂浏览器拖不动！</p>
<p>以上就是为什么大多数模板引擎都要强调“轻逻辑”的最根本原因。</p>
<p>对于 Angular 来说，强调“轻逻辑”还有另一个原因：在组件的整个生命周期里面，模板函数会被执行很多次。你可以想象，Angular 每次要刷新组件外观的时候，都需要去调用一下模板函数，如果你在模板里面编写了非常复杂的代码，一定会增加渲染时间，用户一定会感到界面有“卡顿”。</p>
<p>人眼的视觉延迟大约是 100ms 到 400ms 之间，如果整个页面的渲染时间超过 400ms，界面基本上就卡得没法用了。有一些做游戏的开发者会追求 60fps 刷新率的细腻感觉，60 分之 1 秒约等于 16.7ms，如果 UI 整体的渲染时间超过了 16.7ms，就没法达到这个要求了。</p>
<p>轻逻辑（logic-less）带来了效率的提升，也带来了一些不方便，比如很多模板引擎都实现了 if 语句，但是没有实现 else，因此开发者们在编写复杂业务逻辑的时候模板代码会显得非常啰嗦。</p>
<p>目前来说，并没有完美的方案能同时兼顾运行效率和语法表现能力，这里只能取一个平衡。</p>
<h3 id="mustache">Mustache 语法</h3>
<p>Mustache 语法也就是你们说的双花括号语法 {{...}}，老外觉得它像八字胡子，很奇怪啊，难道老外喜欢侧着头看东西？</p>
<p>好消息是，很多模板引擎都接受了 Mustache 语法，这样一来学习量又降低了不少，开心吧？</p>
<p>关于 Mustache 语法，你需要掌握 3 点：</p>
<ul>
<li>它可以获取到组件里面定义的属性值</li>
<li>它可以自动计算简单的数学表达式，如加减乘除、取模</li>
<li>它可以获得方法的返回值</li>
</ul>
<p>请依次看例子。</p>
<p>插值语法关键代码实例：</p>
<pre>
&lt;h3&gt;
    欢迎来到{{title}}！
&lt;/h3&gt;
</pre>
<pre>
public title = '假的星际争霸2'; 
</pre>
<p>简单的数学表达式求值：</p>
<pre>
&lt;h3&gt;1+1={{1+1}}&lt;/h3&gt;
</pre>
<p>调用组件里面定义的方法：</p>
<pre>
&lt;h3&gt;可以调用方法{{getVal()}}&lt;/h3&gt;
</pre>
<pre>
public getVal():any{
    return 65535;
}
</pre>
<h3 id="">模板内的局部变量</h3>
<pre>
&lt;input #heroInput&gt;
&lt;p&gt;{{heroInput.value}}&lt;/p&gt;
</pre>
<p>有一些朋友会追问，如果我在模板里面定义的局部变量和组件内部的属性重名会怎么样呢？</p>
<p>如果真的出现了重名，Angular 会按照以下优先级来进行处理：</p>
<pre><code>模板局部变量 &gt; 指令中的同名变量 &gt; 组件中的同名属性。
</code></pre>
<p>这种优先级规则和 JSP 里面的变量取值规则非常类似，对比一下很好理解对不对？你可以自己写代码测试一下。</p>
<h3 id="-1">值绑定</h3>
<p>值绑定是用方括号来做的，写法：</p>
<pre>
&lt;img [src]="imgSrc" /&gt;
</pre>
<pre>
public imgSrc:string="./assets/imgs/1.jpg";
</pre>
<p>很明显，这种绑定是单向的。</p>
<h3 id="-2">事件绑定</h3>
<p>事件绑定是用圆括号来做的，写法：</p>
<pre>
&lt;button class="btn btn-success" (click)="btnClick($event)"&gt;测试事件&lt;/button&gt;
</pre>
<p>对应 Component 内部的方法定义：</p>
<pre>
public btnClick(event):void{
    alert("测试事件绑定！");
}
</pre>
<h3 id="-3">双向绑定</h3>
<p>双向绑定是通过方括号里面套一个圆括号来做的，模板写法：</p>
<pre>
&lt;font-resizer [(size)]="fontSizePx"&gt;&lt;/font-resizer&gt;
</pre>
<p>对应组件内部的属性定义：</p>
<pre>
public fontSizePx:number=14;
</pre>
<p>AngularJS 是第一个把“双向数据绑定”这个特性带到前端来的框架，这也是 AngularJS 当年最受开发者追捧的特性，之一。</p>
<p>根据 AngularJS 团队当年讲的故事，“双向数据绑定”这个特性可以大幅度压缩前端代码的规模。大家可以回想一下 jQuery 时代的做法，如果要实现类似的效果，是不是要自己去编写大量的代码？尤其是那种大规模的表单，一大堆的赋值和取值操作，都是非常丑陋的“面条”代码，而有了“双向数据绑定”特性之后，一个绑定表达式就搞定。</p>
<p>目前，主流的几款前端框架都已经接受了“双向数据绑定”这个特性。</p>
<p>当然，也有一些人不喜欢“双向数据绑定”，还有人专门写了文章来进行批判，也算是前端一景。</p>
<h3 id="-4">在模板里面使用结构型指令</h3>
<p>Angular 有 3 个内置的结构型指令：*ngIf、*ngFor、ngSwitch。ngSwitch 的语法比较啰嗦，使用频率小一些。</p>
<p>*ngIf 代码实例：</p>
<pre>
&lt;p *ngIf="isShow" style="background-color:#ff3300"&gt;显示还是不显示？&lt;/p&gt;
&lt;button class="btn btn-success" (click)="toggleShow()"&gt;控制显示隐藏&lt;/button&gt;
</pre>
<pre>
public isShow:boolean=true;

public toggleShow():void{
    this.isShow=!this.isShow;
}
</pre>
<p>*ngFor 代码实例：</p>
<pre>
&lt;li *ngFor="let race of races;let i=index;"&gt;
    {{i+1}}-{{race.name}}
&lt;/li&gt;
</pre>
<pre>
public races:Array<any>=[
    {name:"人族"},
    {name:"虫族"},
    {name:"神族"}
];
</pre>
<p>*ngSwitch 代码实例：</p>
<pre>
&lt;div [ngSwitch]="mapStatus"&gt;
    &lt;p *ngSwitchCase="0"&gt;下载中...&lt;/p&gt;
    &lt;p *ngSwitchCase="1"&gt;正在读取...&lt;/p&gt;
    &lt;p *ngSwitchDefault&gt;系统繁忙...&lt;/p&gt;
&lt;/div&gt;
</pre>
<pre>
public mapStatus:number=1;
</pre>
<p><strong>特别注意：一个 HTML 标签上只能同时使用一个结构型的指令。</strong></p>
<p>因为“结构型”指令会修改 DOM 结构，如果在一个标签上使用多个结构型指令，大家都一起去修改 DOM 结构，到时候到底谁说了算？</p>
<p>那么需要在同一个 HTML 上使用多个结构型指令应该怎么办呢？有两个办法：</p>
<ul>
<li>加一层空的 div 标签</li>
<li>加一层 &lt;ng-container&gt;</li>
</ul>
<h3 id="-5">在模板里面使用属性型指令</h3>
<p>使用频率比较高的 3 个内置指令是：NgClass、NgStyle、NgModel。</p>
<p>NgClass 使用案例代码：</p>
<pre>
&lt;div [ngClass]="currentClasses"&gt;同时批量设置多个样式&lt;/div&gt;
&lt;button class="btn btn-success" (click)="setCurrentClasses()"&gt;设置&lt;/button&gt;
</pre>
<pre>
public currentClasses: {};

public canSave: boolean = true;
public isUnchanged: boolean = true;
public isSpecial: boolean = true;

setCurrentClasses() {
    this.currentClasses = {
        'saveable': this.canSave,
        'modified': this.isUnchanged,
        'special': this.isSpecial
    };
}
</pre>
<pre>
.saveable{
    font-size: 18px;
} 
.modified {
    font-weight: bold;
}
.special{
    background-color: #ff3300;
}
</pre>
<p>NgStyle 使用案例代码：</p>
<pre>
&lt;div [ngStyle]="currentStyles"&gt;
    用NgStyle批量修改内联样式！
&lt;/div&gt;
&lt;button class="btn btn-success" (click)="setCurrentStyles()"&gt;设置&lt;/button&gt;
</pre>
<pre>
public currentStyles: {}
public canSave:boolean=false;
public isUnchanged:boolean=false;
public isSpecial:boolean=false;

setCurrentStyles() {
    this.currentStyles = {
        'font-style':  this.canSave      ? 'italic' : 'normal',
        'font-weight': !this.isUnchanged ? 'bold'   : 'normal',
        'font-size':   this.isSpecial    ? '36px'   : '12px'
    };
}
</pre>
<p>ngStyle 这种方式相当于在代码里面写 CSS 样式，比较丑陋，违反了注意点分离的原则，而且将来不太好修改，非常不建议这样写。</p>
<p>NgModel 使用案例代码：</p>
<pre>
&lt;p class="text-danger"&gt;ngModel只能用在表单类的元素上面&lt;/p&gt;
    &lt;input [(ngModel)]="currentRace.name"&gt;
&lt;p&gt;{{currentRace.name}}&lt;/p&gt;
</pre>
<pre>
public currentRace:any={name:"随机种族"};
</pre>
<p>请注意，如果你需要使用 NgModel 来进行双向数据绑定，必须要在对应的模块里面 import FormsModule 。</p>
<h3 id="-6">管道</h3>
<p>管道的一个典型作用是用来格式化数据，来一个最简单的例子：</p>
<pre>
{{currentTime | date:'yyyy-MM-dd HH:mm:ss'}}
</pre>
<pre>
public currentTime: Date = new Date();
</pre>
<p>Angular 里面一共内置了 17 个指令（有一些已经过时了）：</p>
<p><img src="https://images.gitbook.cn/9572e7e0-ad2d-11e9-8f3f-792c82c0addc" alt="enter image description here" /></p>
<p>在复杂的业务场景里面，17 个指令肯定不够用，如果需要自定义指令，请查看这里的例子： https://angular.io/guide/pipes 。</p>
<p>管道还有另一个典型的作用，就是用来做国际化，后面有一个独立的小节专门演示 Angular 的国际化写法。</p>
<h3 id="-7">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-component">本节完整可运行的实例代码请参见这里</a>，请检出 template 分支。</p>
<h3 id="-8">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Angular 基础教程》读者交流群，添加小姐姐-泰勒微信：「GitChatty5」，回复关键字「123」给小姐姐-泰勒获取入群资格。</strong></p>
</blockquote></div></article>