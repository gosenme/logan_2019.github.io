---
title: SSM 搭建精美实用的管理系统-1
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">课程背景</h3>
<p>让我们从某招聘网站上发布的数个 Java 工程师招聘信息来开始本达人课。</p>
<blockquote>
  <p>Java 实习生 [3k-5k]</p>
  <p>岗位要求：</p>
  <ol>
  <li>热爱技术并有钻研精神，Java 基础扎实，熟悉 Spring 、Spring MVC 、MyBatis 、MySQL 、Linux；</li>
  <li>熟悉 JavaScript，有 JavaScript 框架使用经验优先；</li>
  <li>具备良好的沟通能力、抗压能力和团队合作精神。</li>
  </ol>
  <p>Java 研发工程师 [6k-12k]</p>
  <p>岗位职责：</p>
  <ol>
  <li>熟练 Java 语言基础，熟悉 J2EE 体系架构，具有 JSP 、JavaScript 、jQuery 、BootStrap 、Servlet 、Spring 、MyBatis 、XML 等开发经验；</li>
  <li>熟练 Oracle 、MySQL 等数据库设计与开发，并熟练掌握 SQL；</li>
  <li>熟悉使用 Tomcat 、Eclipse 、IntelliJ 、Jetty 等应用服务器软件及开发工具；</li>
  <li>根据项目分配，快速完成开发任务。    </li>
  </ol>
  <p>Java 开发工程师 [10k-15k]</p>
  <p>岗位要求：</p>
  <ol>
  <li>计算机相关专业本科毕业，2 年以上 Java 开发经验；</li>
  <li>熟练掌握 Spring 、Spring MVC 、Mybatis 主流开发框架；</li>
  <li>精通一种以上关系数据库，如 MySQL；</li>
  <li>熟悉分布式缓存，如 Redis 。</li>
  </ol>
</blockquote>
<p>这里，暂且不谈 Spring 的辉煌历史，也不过多谈论 ORM 框架给广大开发人员带来的便捷，我们着眼于现实。通过上面几则招聘信息，相信大家应该都能从中直观地感受到，不管你是初学者，或者是刚入行的实习生，亦或是已经有了几年工作经验的开发者，都不能忽视这样一个事实：</p>
<p><strong>Spring MVC+Spring+Mybatis 这套技术栈是绝大部分公司明确要求掌握的技术，而 Spring MVC+Spring+Mybatis 的组合搭配已经渐渐成为 Java Web 开发者必备的技能，虽然不是全部，但目前的趋势即是如此，掌握 SSM 技能栈刻不容缓。</strong></p>
<p>前几年工作中，我一直使用 Spring MVC+Spring+Mybatis 的组合进行开发，平时也会対其做一些研究和体验。在这个过程中发现，网上关于 Spring MVC+Spring+Mybatis 组合的介绍文章和教程虽然很多，但很多难以满足学习者的需要 —— 要么只有简单的介绍没有详细教程，要么有较为详细的教程却没有源码，要么有源码但源码不全，很难上手使用，还有的提供了详细的源码但却没有与之对应的界面和 Demo，为学习者提供实际的操作体验。</p>
<p>这些情况对于有经验的开发者来说并不是大问题，但对于初学者来说如同一面厚实的砖墙堵在了学习的道路上。</p>
<p>于是，自 2017 年年初起，我开始在网络上连载了 Spring MVC+Spring+Mybatis 组合的系列文章，源码也开放在 GitHub 和 Gitee 开源网站上，并且每一个教程都有对应的演示网站供读者体验和学习，这种教程+源码+实际体验的模式受到许多网友的喜欢和关注。</p>
<p>2018 年年中，与 GitChat 达人课策划编辑达成协议将这套教学系列文章重新整理和优化，以达人课的形式呈现给各位读者。</p>
<p><strong>该课对整体内容进行了更为合理的划分，同时，增加了针对初学者的详细教程。不仅如此，对于有经验的朋友，在教程后半部分增添了优化提升课程，让你更为直观、真实地体验网站的优化过程，对系统优化中集群部署及分布式开发不再迷茫。同时，也更新了项目的视觉效果，优化了网站的交互体验，在原来的基础上更贴近于企业网站，让你切身体会如何使用 Spring MVC+Spring+Mybatis 开发并且可以真实应用到实际的开发工作中。</strong></p>
<blockquote>
  <p>十三温馨提示：文中有部分 Gif 图片，可能因为文章格式问题导致有些模糊，放大即可，都是高清无码版本，学习起来更舒适！</p>
</blockquote>
<h3 id="-1">课程目的</h3>
<p>花了几天的时间，做了一个网站小 Demo，最终效果也与此网站类似。以下是这次实战项目的 Demo 演示。</p>
<p><strong>登录页：</strong></p>
<p><img src="https://images.gitbook.cn/1689c590-89af-11e8-b84d-8905759e9115" alt="log-in" /></p>
<p><strong>富文本编辑页：</strong></p>
<p><img src="https://images.gitbook.cn/39481eb0-89af-11e8-adda-414d0af9d022" alt="rich-text-manage" /></p>
<p><strong>图片上传：</strong></p>
<p><img src="https://images.gitbook.cn/4b52f490-89af-11e8-99ef-49a6453ec514" alt="images-manage" /></p>
<p><strong>退出登录：</strong></p>
<p><img src="https://images.gitbook.cn/5f317900-89af-11e8-b84d-8905759e9115" alt="log-out" /></p>
<p>课程目的也很简单，希望通过此课程，学员可以自己动手实现一个精美且实用的 Java Web 后台管理系统。</p>
<p>为了达成这一目的，我对课程做了如下规划：</p>
<ul>
<li>课程开始，为针对于初学者的详细教程，介绍 Spring MVC+Spring+Mybatis 的基础整合及如何进行快速开发；</li>
<li>接着，开启后台管理系统的设计及开发过程，进行实战演练；</li>
<li>最后，优化提升的技巧和实战分享，让你学会如何在企业开发中有一个良好的开发习惯以及如何对系统进行优化升级。</li>
</ul>
<p><strong>通过本课程，不仅仅让你学会开发，也会让你学会网站优化，进一步提升技术能力和技术积累。</strong></p>
<h3 id="-2">学员定位</h3>
<p>该达人课适合以下人群阅读：</p>
<ul>
<li>从事 Java 相关领域的开发或者有一定 Java Web 基础的人员；</li>
<li>需要 SSM 源码练习的人员；</li>
<li>传统开发领域，急迫想打破原有开发模式的开发人员；</li>
<li>对系统优化缺乏实战经验的开发人员。</li>
</ul>
<p>在学习本课程之前，需要了解 Java 开发及 Java Web 相关知识等基础技能。</p>
<h3 id="-3">课程介绍</h3>
<h4 id="-4">开发环境</h4>
<ul>
<li>Windows/Linux</li>
<li>IntelliJ IDEA</li>
<li>JDK 1.8</li>
<li>MySQL 8</li>
<li>Tomcat </li>
</ul>
<h4 id="-5">收获</h4>
<p>通过本课程，您将学习到以下内容：</p>
<ul>
<li>Spring+Spring MVC+MyBatis 框架的整合及运用；</li>
<li>MySQL8 数据库的基本使用方法；</li>
<li>Maven 的配置及使用；</li>
<li>Tomcat 8 的配置及使用；</li>
<li>Druid 数据库连接池；</li>
<li>AJAX 异步技术；</li>
<li>AdminLTE3 、Bootstrap 4 、SweetAlert 、JqGrid 、JQuery 等前端框架组件及控件的使用；</li>
<li>多图上传技术；</li>
<li>大文件上传与文件的断点续传；</li>
<li>文件导入导出功能；</li>
<li>Linux 系统部署及发布项目；</li>
<li>Redis 缓存数据库的配置及使用方法；</li>
<li>前后端分离；</li>
<li>Nginx 的配置及使用；</li>
<li>Tomcat 集群的搭建及负载均衡；</li>
<li>使用 Nginx 实现动静分离部署；</li>
<li>Java Web 性能优化的基本技巧。</li>
</ul>
<h4 id="-6">演示站点</h4>
<blockquote>
  <p>点击这里查看：<a href="http://gitchat-ssm.13blog.site/">gitchat-ssm</a></p>
</blockquote></div></article>