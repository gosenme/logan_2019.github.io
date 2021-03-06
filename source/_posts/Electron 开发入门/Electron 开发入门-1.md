---
title: Electron 开发入门-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p><div class="toc">
<ul>
<li><ul>
<li><ul>
<li><a href="#">课程背景</a></li>
<li><a href="#electron">有哪些著名应用使用 Electron 开发的</a></li>
<li><a href="#electron-1">学习 Electron，成为更优秀的开发者</a></li>
<li><a href="#-1">课程结构</a></li>
<li><a href="#-2">课程寄语</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</p>
<p>大家好，我是李宁，网名“银河使者”，IT 图书作者（代表作《Python 从菜鸟到高手》，欧瑞科技创始人，领导和参与了欧瑞科技公众号，小程序（极客题库）的开发。现在正带领团队研发高效全平台开发工具 OriUnity，主要使用的技术包括 Electron 和 Go 语言。</p>
<h3 id="">课程背景</h3>
<p>可能有很多读者会有这样的疑问：为什么用 JavaScript 来开发桌面应用？</p>
<p>曾经的 JavaScript 脆弱、简陋、甚至有被边缘化的危险，不过 JavaScript 在经过了两次飞跃后（以 V8 为首的 JavaScript 引擎和 Node.js 的问世），不再受人欺负，早已升级为绿博士（复仇者联盟 4 中班纳博士和绿巨人的合体，强大而充满智慧）。 V8 引擎让 JavaScript 的运行速度飞快，Node.js 让 JavaScript 不仅仅能做 Web 前端页面，还能开发后端应用。</p>
<p>尽管有了 Node.js，JavaScript 可以开发服务端应用，但有一类重要的应用它还是无法胜任——桌面应用。目前 Web 应用和移动应用看似成为主流，但如果没有桌面应用，Web 应用和移动应用甚至都不会存在。所有的 Web 浏览器（IE、Chrome、Firefox、Safari 等）都是桌面应用，如果没有桌面应用，Web 页面根本没地方运行；用于开发移动应用的开发工具（IDE）也是桌面应用。而且 Windows 的开始菜单和 Mac OS X 的 Docker 中的每一个图标都对应一个桌面应用，可以说，桌面应用无处不在。</p>
<p>如果将 Web 应用和移动应用比作国王，那么桌面应用就是国王头上的那顶王冠，没有了王冠，国王什么都不是，而赐予 JavaScript 制作王冠之神力的正是 Electron。这是一个基于 V8 引擎和 Node.js 的开发框架，允许用 JavaScript 开发跨平台（Windows、Mac OS X 和 Linux）桌面应用。</p>
<p><img src="https://images.gitbook.cn/FonYrsKFBpIV5BXKhVn9b009oELZ" alt="avatar" /></p>
<h3 id="electron">有哪些著名应用使用 Electron 开发的</h3>
<p>目前有相当多的桌面应用是使用 Electron 开发的，例如，著名的 Visual Studio Code（微软推出的一个跨平台源代码编辑器）就是用 Electron 开发的；还有蚂蚁小程序（在支付宝中运行的小程序）的开发工具也是用 Electron 来开发的；以小米、华为为主的众多手机厂商推出的快应用（类似于微信小程序）的 IDE 也是用 Electron 开发的。</p>
<p>蚂蚁小程序 IDE：</p>
<p><img src="https://images.gitbook.cn/FuvKinsQDWcdf90EfP7UU8AjUIJ8" alt="avatar" /></p>
<blockquote>
  <p>此外，大家熟悉的 Slack、Atom、XMind ZEN、WebTorrent、Hyper 等都是基于 Electron 的应用。</p>
</blockquote>
<p>从 Electron 的主要用户来看，很多都是大厂，如蚂蚁金服、小米、华为、GitHub（Electron 就是 GitHub 推出的）、微软等，由于现在 GitHub 被微软收购了，因而目前 Electron 的后台是微软。因此学习 Electron 不用担心以后没市场，毕竟，各大厂都在用 Electron。</p>
<p>可能有很多读者以前开发过桌面应用，认为桌面应用也有缺点。比如，桌面应用很难做到实时更新，维护相对于 Web 应用费时费力，不过这个缺点是针对传统桌面应用的，而基于 Electron 的应用没有这个缺点。</p>
<p>Electron 之所以这么多人用，并不仅仅是因为它基于 Web 技术，而且它还能调用很多本地 API，在实现很多功能时与本地应用非常接近。</p>
<h3 id="electron-1">学习 Electron，成为更优秀的开发者</h3>
<p>作为一名开发者，学会开发桌面应用，会非常显著地提升自己的核心竞争力，而且 Electron 开发桌面应用使用的是 Web 技术，可以考虑将 Web 应用与桌面应用作为一个应用来开发，这样会大大提升开发效率。</p>
<p>本课程笔者团队也正在使用 Electron 开发一款跨平台的开发工具 OriUnity，可以使用 JavaScript 同时开发桌面应用、Web 应用、移动 App 和小程序，而且可以将客户端与服务端融为一体。</p>
<p>这个项目具有大量的创新技术点，以及大量的发明专利，包括改进的增强版 JavaScript，JS 与 SQL 融合、客户端和服务端一体化、虚拟组件、异构组件嫁接等，通过这些创新的技术，可以将开发效率提高 10 倍以上。</p>
<p>在开发产品的过程中，我们也积累了很多 Electron 的实践经验。因此正好借着达人课的机会，将 Electron 的一些开发经验总结出来，希望对想入门 Electron  的读者有一定的借鉴作用。</p>
<h3 id="-1">课程结构</h3>
<p>Electron 功能众多，但这些功能基本上可分为基础知识（开发环境安装、开发步骤、IDE 的选择等）、窗口、菜单、高级 API（数据库、托盘、摄像头、拖拽、剪贴板等）以及发布应用程序，本课程将会结合这些知识点详细讲解如何用 Electron 开发桌面应用。</p>
<p>课程目的是培养大家解决实际问题的能力，每一课的知识点既相互独立、又有联系，比如，在创建托盘时需要用到上下文菜单的知识。大多数文章（除了配置开发环境和简介外）都配有完整的实现代码，并且在最后还提供了两个实战案例：基于 Electron 的云笔记和数据库管理系统，把离散的知识点结合起来完成非常复杂的桌面应用项目。</p>
<p>本课程分为七大部分，共 29 篇（含开篇词）。</p>
<p>第一部分（第 01 ~ 04 课）：Electron 基础知识</p>
<p>这部分主要介绍了用 Electron 开发跨平台桌面应用的原因、桌面应用的优势、Electron 应用的基本开发步骤、如何搭建集成开发环境、用 Git 管理 Electron 应用等内容，这一部分是 Electron 学习的开胃菜，大餐请继续往后看。</p>
<p>第二部分（第 05 ~ 09 课）：用 Electron 创建窗口</p>
<p>这部分详细介绍了用 Electron 创建各种类型窗口的方式，主要内容包括只针对 Mac OS X 系统的文件展示窗口、打开对话框窗口、保存对话框窗口、显示消息对话框窗口、使用 HTML 5 API 创建子窗口、用 open 方法打开的子窗口交互、在窗口中嵌入 Web 页面等。</p>
<p>第三部分（第 10 ~ 12 课）：创建各种类型菜单</p>
<p>菜单是桌面应用程序的重要部分，这一部分详细介绍了在 Electron 中如何创建各种类型的菜单，主要内容包括使用模板创建窗口菜单、如何设置菜单项的角色、菜单项的类型、为菜单添加图标、创建动态菜单、上下文菜单。</p>
<p>第四部分（第 13 ~ 21 课）：常用的核心 API</p>
<p>这一部分是本系列课程的核心内容，讲解了 Electron 中常用的核心 API，主要包括创建托盘应用、拖拽操作、使用摄像头、根据操作系统定制样式、用纯 JavaScript API 操作 SQLite 数据库、用 Node.js 模块操作 SQLite 数据库、访问 MySQL 数据库、使用剪贴板、注册全局键、测试等。</p>
<p>第五部分（第 22 ~ 23 课）：发布应用程序</p>
<p>由于基于 Electron 的桌面应用需要依赖 Node.js、Electron 以及众多的模块才能运行，这些东西肯定不能让用户自己一个个安装，最好的解决方案就是把这些东西与开发的桌面应用一起打包，然后将一个安装包发放给用户，用户只需要双击安装包就可以搞定，因而学会发布 Electron 桌面应用非常必要。</p>
<p>因此，这部分内容主要介绍了如何用各种工具发布基于 Electron 的应用，主要包括使用 electron-packager 和 electron-builder 创建安装包及制作安装程序（dmg、exe 等）。</p>
<p>第六部分（第 24 ~ 26 课）：项目实战</p>
<p>这一部分是本系列课程的画龙点睛之笔，需要把前面五部分介绍的知识点连接起来完成复杂的桌面应用，这里提供了两个完整的案例，一个是云笔记系统，该系统可以将本地的笔记保存到服务端，只是这里的服务端是以太坊，而不是传统的数据库；第二个项目是基于 Electron 的 MySQL 数据库管理系统，可以做本地管理 MySQL 数据库，而且还可以将数据上传到以太坊进行备份。</p>
<p>第七部分（第 27 ~ 28 课）：模块分析</p>
<p>这一部分主要介绍了 Node.js 和 Electron 模块的相关知识，包括使用 JavaScript 开发 Node.js 和 Electron 模块以及使用 C++ 开发 Node.js 和 Electron 的本地模块。通过这一部分的内容，可以让 C++ 与 Electron 完美融合在一起，让 Electron 拥有无限扩展性。</p>
<h3 id="-2">课程寄语</h3>
<p>Node.js 和 Electron 堪称 JavaScript 的左右护法，前者让 JavaScript 可以轻而易举地跨越不同类型应用的界限，后者让 JavaScript 可以进入服务端和桌面应用领域。有了这两个护法，JavaScript 可以真正成为唯一的全栈开发语言，从 Web 到移动，再到服务端，再到桌面应用，甚至是终端程序，无所不能。</p>
<p>本课程并不是单纯讲解 Electron 的知识，而是想要教会大家开发 Electron 桌面应用的思想，提高动手能力，今后无论遇到多复杂的桌面应用需求都能得心应手，轻松应对。</p>
<p>最后，预祝大家学习愉快，Good  Luck！</p>
<blockquote>
  <p><a href="https://gitbook.cn/m/mazi/comp/column?columnId=5c3168154fcd483b02710425&utm_source=lnsd002">点击了解更多《Electron 开发入门》</a></p>
</blockquote></div></article>