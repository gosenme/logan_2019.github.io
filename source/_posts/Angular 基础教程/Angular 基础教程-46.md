---
title: Angular 基础教程-46
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>Angular 5.0 引入的重要修改如下：</p>
<ul>
<li>编译器优化：根据官方说法，编译速度提升 95%；默认支持 AOT；支持删除空行、制表符等。</li>
<li>CLI 升级到 v1.5：默认打开编译优化选项，生成项目的时候默认使用 Angular 5.0 。</li>
<li>增强 Decorator：支持 lambda 表达式、使用对象字面值的时候支持 useValue、useFactory、data 配置项。</li>
<li>Zone 运行速度提升：大幅度优化了 Zone 相关的实现，提升运行效率。</li>
<li>服务端状态转换和 DOM 支持：可以更方便地在服务器端和客户端版之间共享状态，针对 Angular Universual。</li>
<li>国际化支持：Number、Date、货币符号相关的管道支持国际化。</li>
<li>注射器修改：废弃反射型注射器 ReflectiveInjector，使用全新的 StaticInjector，减小打包之后的体积。</li>
<li>新增 HttpClient：废弃原有的 HttpModule，新增 HttpClientModule。</li>
<li>支持 exportAs 语法：可以避免重名问题。</li>
<li>Form 相关的修改：可以在触发 blur 和 submit 事件的时候进行数据校验，支持更多语法糖细节。</li>
<li>升级 RxJS：升级 RxJS 到 5.5.2，在 import 的时候保持和其它模块的语法一致性。</li>
<li>新增 8 个路由事件：GuardsCheckStart、ChildActivationStart、ActivationStart、GuardsCheckEnd、ResolveStart, ResolveEnd、ActivationEnd、ChildActivationEnd。</li>
</ul>
<p><strong>笔者备注：Angular 5.0 引入的修改是非常平滑的，从 4.0 升级过来基本不需要改太多东西。</strong></p></div></article>