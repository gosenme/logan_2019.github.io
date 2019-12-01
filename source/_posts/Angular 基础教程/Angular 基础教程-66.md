---
title: Angular 基础教程-66
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这是官方文档里面的一个例子，运行效果如下：</p>
<p><img width="60%" src="https://images.gitbook.cn/5e0102f0-f2e4-11e8-87c8-f50ecfad80b5"></p>
<p>核心代码如下：</p>
<pre><code>import { Directive, ElementRef,HostListener,HostBinding,Input } from '@angular/core';

@Directive({
  selector: '[my-high-light]'
})
export class MyHighLightDirective {
  @Input() 
  highlightColor: string;

  constructor(private el: ElementRef) {
  }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.highlightColor);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight(null);
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
}
</code></pre>
<p>以上指令的用法如下：</p>
<pre>
&lt;p my-high-light highlightColor="#ff3300"&gt;内容高亮显示！&lt;/p&gt;
</pre>
<h3 id="">自定义结构型指令</h3>
<p>这个例子会动态创建 3 个组件，每个延迟 500 毫秒，运行效果如下：</p>
<p><img width="20%" src="https://images.gitbook.cn/97438510-f2e4-11e8-846c-655c5a3d2587"></p>
<p>指令代码如下：</p>
<pre><code>import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
    selector: '[appDelay]'
})
export class DelayDirective {
    constructor(
        private templateRef: TemplateRef&lt;any&gt;,
        private viewContainerRef: ViewContainerRef
    ) { }

    @Input() set appDelay(time: number) {
        setTimeout(() =&gt; {
            this.viewContainerRef.createEmbeddedView(this.templateRef);
        }, time);
    }
}
</code></pre>
<p>指令的用法核心代码：</p>
<pre>
&lt;div *ngFor="let item of [1,2,3]"&gt;
    &lt;card *appDelay="500 * item"&gt;
        第 {{item}} 张卡片
    &lt;/card&gt;
&lt;/div&gt;
</pre>
<p>此时读者应该注意到了，结构性指令在使用的时候前面都会带上星号，即使是你自定义的结构性指令，也是一样的。</p>
<h3 id="-1">小结</h3>
<p>强烈建议仔细阅读官方文档里面的关于 Directive 的细节描述，<a href="https://angular.io/guide/attribute-directives">点击这里详见详情</a>。</p>
<p><a href="https://gitee.com/learn-angular-series/learn-directive">本课所有可运行的实例代码请单击这里</a>，代码在 master 分支上。</p></div></article>