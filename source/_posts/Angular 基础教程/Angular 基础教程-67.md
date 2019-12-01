---
title: Angular 基础教程-67
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>有一个常见的问题：既然组件是指令的子类，那么指令里面能干的事儿组件应该都能干，我可以在指令里面直接操作 DOM 吗？</p>
<p>答案是肯定的。</p>
<p>我们来修改一下上一课里面的例子，直接在组件里面来实现背景高亮效果，关键代码如下：</p>
<pre>
@Component({
  selector: 'test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent implements OnInit {
  @Input() 
  highlightColor: string;

  private containerEl:any;

  constructor(private el: ElementRef) {

  }

  ngOnInit() {
  }

  ngAfterContentInit() {
    console.log(this.el.nativeElement);
    console.log(this.el.nativeElement.childNodes);
    console.log(this.el.nativeElement.childNodes[0]);
    console.log(this.el.nativeElement.innerHTML);

    this.containerEl=this.el.nativeElement.childNodes[0];
  }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.highlightColor);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight(null);
  }

  private highlight(color: string) {
    this.containerEl.style.backgroundColor = color;
  }
}
</pre>
<p>组件的标签结构如下：</p>
<pre>
&lt;div class="my-container"&gt;
  鼠标移进来就会改变背景
&lt;/div&gt;
</pre>
<p>这个组件的使用方式如下：</p>
<pre>
&lt;div class="container"&gt;
    &lt;test highlightColor="#F2DEDE"&gt;&lt;/test&gt;
&lt;/div&gt;
</pre>
<p>可以看到，直接在组件里面操作 DOM 是可以的，但是一旦把操作 DOM 的这部分逻辑放在组件里面，就没法再在其他标签上面使用了。</p>
<h3 id="">小结</h3>
<p><a href="https://gitee.com/learn-angular-series/learn-directive">本课所有可运行的实例代码请单击这里</a>，代码在 test-component 分支上。</p></div></article>