---
title: Angular 基础教程-81
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">先看运行效果</h3>
<p>本节课用 NiceFish 这个开源项目来演示国际化的用法，<a href="https://gitee.com/mumu-osc/NiceFish">代码在这里</a>。</p>
<p>这是默认中文情况下，用户注册界面：</p>
<p><img width="60%" src="https://images.gitbook.cn/09cbb600-f387-11e8-aeb7-01d6aed3aa05"></p>
<p>打开 Chrome 的设置界面，把默认语言设置成“英语”：</p>
<p><img width="60%" src="https://images.gitbook.cn/18d84000-f387-11e8-8426-b15c0859cf17"></p>
<p>刷新一下，可以看到界面变成了英文状态：</p>
<p><img width="70%" src="https://images.gitbook.cn/274ad3f0-f387-11e8-8426-b15c0859cf17"></p>
<h3 id="-1">解释具体做法</h3>
<p>第一步：在项目的 package.json 里面的 dependencies 配置项中加上"ng2-translate": "5.0.0" 。</p>
<p>第二步：在 app.module.ts 里面导入需要使用的模块：</p>
<pre><code>import { TranslateModule, TranslateLoader, TranslateStaticLoader } from 'ng2-translate';
</code></pre>
<p>在 imports 配置项里面加上以下内容：</p>
<pre><code>TranslateModule.forRoot({
    provide: TranslateLoader,
    useFactory: (http: Http) =&gt; new TranslateStaticLoader(http,'./assets/i18n', '.json'),
    deps: [Http]
})
</code></pre>
<p>第三步：在 app.component.ts 中的 ngOnInit 钩子里面加上以下内容：</p>
<pre><code>this.translate.addLangs(["zh", "en"]);
this.translate.setDefaultLang('zh');
const browserLang = this.translate.getBrowserLang();
this.translate.use(browserLang.match(/zh|en/) ? browserLang : 'zh');
</code></pre>
<p>第四步：在 HTML 模板里面通过管道的方式来编写需要进行国际化的 Key：</p>
<p><img width="70%" src="https://images.gitbook.cn/38fbf110-f387-11e8-8426-b15c0859cf17"></p>
<p>可以看到，国际化插件本质上是利用了 Angular 的“管道”机制。</p>
<p>第五步：用来编写国际化字符串的 json 文件是这样的：</p>
<p><img width="70%" src="https://images.gitbook.cn/49164190-f387-11e8-aeb7-01d6aed3aa05"></p>
<h3 id="-2">小结</h3>
<p><a href="https://github.com/ngx-translate/core">ng2-translate 的主页可点击这里查看</a>，它是一个第三方提供的 i18n 库，和 Angular 结合得比较好，ngx-translate 是后来改的名字。</p>
<p><a href="https://gitee.com/mumu-osc/NiceFish">本节课可运行的完整实例代码可参见这里</a>，代码在 master 分支上。</p></div></article>