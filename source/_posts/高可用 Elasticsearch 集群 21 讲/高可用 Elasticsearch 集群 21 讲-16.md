---
title: 高可用 Elasticsearch 集群 21 讲-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>先前的版本中，X-Pack 作为 Elasticsearch 插件的形式存在，在 6.x 中，已经做为一个内部模块默认携带。要开启身份认证，需要将下列两个配置设置为 true：</p>
<pre><code>xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
</code></pre>
<p>早期的版本中，身份认证可以单独开启，现在的版本中，会强制要求开启集群节点间的通讯加密，关于通讯加密请参考《通讯加密》</p>
<p>开启上述配置后重启集群，安全机制生效，必须使用正确的用户名和密码才能访问集群。早期版本中，可以使用使用超级用户: elastic 和密码：changeme 来登录系统，从 6.0 开始，默认密码被禁用，用户必须首先初始化内置用户的密码才能使用安全模块。 </p>
<h3 id="1">1. 初始化内置账号</h3>
<p>X-Pack 中有几个内置用户，其中 elastic 为超级用户，其他更多可以参考官方手册。</p>
<p>使用下面的命令来初始化所有内置用户的密码：</p>
<pre><code>bin/elasticsearch-setup-passwords interactive
</code></pre>
<p>该命令以交互的方式要求为每个内置账号输入两次密码来初始化，如下图所示：</p>
<p><img src="https://images.gitbook.cn/Fu7cfkr8bZU77fOrAzNEhfPmZTnY" alt="avatar" /></p>
<p>注意，该命令只能执行一次，后续可以通过 Kibana 或者 API 来管理用户和角色。</p>
<p>在 Elasticsearch 6.x 的版本中，这些内置用户以及加密后的密码存储在 Elasticsearch 的索引 <code>.security-6</code>  中。</p>
<h3 id="2">2. 配置基于文件的用户身份认证</h3>
<p>基于文件的用户身份认证类似 Linux 操作系统默认的身份认证，将用户名和密码记录到本地磁盘文件中，然后通过一些命令管理用户。</p>
<p>也正因为这种特点，他需要管理员来自行保证每个节点上的用户名密码文件保持同步， X-Pack 本身不会做这个工作。如果你在 A 节点添加了一个用户，但在 B 节点上没有添加，结果将会在 A 节点认证成功，而 B 节点认证失败。</p>
<p>虽然有这种明显的缺点，但他仍然是一种非常重要的认证：唯一不依赖其他系统的认证方式。因此当认证系统出现异常时他可以用做故障恢复。通过下面的命令，我们添加一个超级管理员用户 admin：</p>
<pre><code>bin/elasticsearch-users useradd admin -r superuser
</code></pre>
<p>根据提示输入两次密码，新用户创建成功。如果有一天你忘记了密码，可以简单地通过下面的命令重设：</p>
<pre><code>bin/elasticsearch-users passwd admin
</code></pre>
<p>重设密码时不会用到旧密码，直接输入新密码即可修改。基于文件的用户认证会将用户名和密码存储到文件：<code>config/users</code> 中，将用户所属的角色记录到文件 ：<code>config/users_roles</code> 中。在这个例子中，两个文件的内容为：</p>
<pre><code>cat  config/users
admin:$2a$10$UJa7OKDinHjO0Pu4S9xHfO/oV5vr793.mV2JXGcgD1spnkhFHe9nS
</code></pre>
<pre><code>cat  config/users_roles
superuser:admin
</code></pre>
<p>X-Pack 内置的两种 Realm 默认开启，因此我们无需再 elasticsearch.yml  中添加额外的配置。添加完新用户后，无需重启集群，用户或密码会稍后生效（默认 5 秒钟重新加载一次这两个文件，可以通过配置项：<code>resource.reload.interval.high</code> 来调整），现在你可以使用新创建的用户访问集群。</p>
<h3 id="3ldap">3. 配置 LDAP 身份认证</h3>
<p>LDAP 以分层的方式存储用户和用户组，类似文件系统的树形结构。DN 用户标识一条纪录，他描述了一条数据的详细路径。例如，有如下 DN：</p>
<pre><code>"cn=admin,dc=example,dc=com"
</code></pre>
<p>按照文件系统树形结构的理解方式，该 DN 的结构为：</p>
<pre><code>com/example/admin
</code></pre>
<p>其中，com 、example 可以理解为文件夹，admin 为文件，因此，cn 通常代表用户名或组名，dc 为路径。</p>
<p>LDAP 支持用户组，当客户端传递用户名和密码过来的时候，并不携带用户组信息，因此服务器需要找到这个用户所属组的完整 DN，然后再进行验证。X-Pack 的 ldap realm 支持两种模式：</p>
<h4 id="31usersearchmode">3.1 User search mode</h4>
<p>用户搜索模式是最常见的方式，这种模式需要配置一个具有搜索 LDAP 目录权限的用户，来搜索待认证用户的 DN，然后用找到的 DN 和用户提交的密码，到配置的 LDAP 服务器进行身份认证。</p>
<p>下面是一个用户搜索模式的配置案例 elasticsearch.yml ：</p>
<pre><code>xpack:
  security:
    authc:
      realms:
        ldap1:
          type: ldap
          order: 0
          url: "ldap://ldap.xxx.com:389"
          bind_dn: "cn=admin,dc=sys,dc=example, dc=com"
          user_search:
            base_dn: "dc=sys,dc=example,dc=com"
            filter: "(cn={0})"
          group_search:
            base_dn: "dc=sys,dc=example,dc=com"
          files:
            role_mapping: "ES_PATH_CONF/role_mapping.yml"
          unmapped_groups_as_roles: false
</code></pre>
<p>修改配置文件后需要重启集群使他生效，各个字段的含义如下：</p>
<ul>
<li><p><strong><code>type</code></strong></p>
<p>realm 类型必须设置为 ldap</p></li>
<li><p><strong><code>order</code></strong></p>
<p>X-Pack 允许配置多个 realm，此配置用于指定当前 realm 的顺序，0为最先执行</p></li>
<li><p><strong><code>url</code></strong></p>
<p>LDAP 服务器地址，为了灾备和负载均衡的考虑，可以按数组的形式配置多个地址：[ "ldaps://server1:636", "ldaps://server2:636" ]。</p>
<p>当配置了多个地址，X-Pack 默认会使用第一个地址进行认证，如果 LDAP 服务器连接失败，再尝试第二个。你可以通过修改 <code>load_balance.type</code> 配置来调整使用故障转移，还是轮询方式。</p></li>
<li><p><strong><code>bind_dn</code></strong></p>
<p>通过哪个用户搜索 LDAP，这个选项用于配置该用户的 DN</p></li>
<li><p><strong><code>user_search.base_dn</code></strong></p>
<p>用于指定到哪个路径进行搜索</p></li>
<li><p><strong><code>filter</code></strong></p>
<p>过滤器中的 {0} 会替换为待认证用户的用户名。</p></li>
<li><p><strong><code>files.role_mapping</code></strong></p>
<p>指定 <code>role_mapping</code> 文件的位置，默认为：<code>ES_PATH_CONF/role_mapping.yml</code> 该文件中描述了某个角色下都有哪些用户，当用户登录成功后，根据这个文件计算用户都有哪些角色。</p></li>
</ul>
<p>除此之外，我们还需要为 <code>bind_dn</code> 配置密码，密码不适合明文配置到文件中，Elasticsearch 设计了一种称为安全配置的方式，将敏感配置信息加密存储到 Elasticsearch keystore，在这个例子中，我们使用下面的命令为 <code>bind_dn</code> 添加密码配置：</p>
<pre><code>bin/elasticsearch-keystore add \
xpack.security.authc.realms.ldap1.secure_bind_password
</code></pre>
<p>根据提示输入密码完成设置。这里要注意一点，当你需要删除 ldap 配置时，从 elasticsearch.yml 删除 ldap1 的相关配置后，同时也需要执行 elasticsearch-keystore remove 从 keystore 中删除密码配置，否则 Elasticsearch 会认为 ldap1 的配置不完整，无法启动节点。</p>
<p>X-Pack 内置的两种 realms 无需单独配置，默认会启用，但是当你在 elasticsearch.yml 明确配置了 realms，那么身份认证过程只会使用你配置的 realms， native 以及 file 不再生效，不过系统内置账户除外，如 elastic。</p>
<p>如果需要同时使用 native 或 file，需要明确配置。我们建议将 file 作为第一验证方式，下面的例子中，先使用 file 进行认证，如果认证失败，再使用 ldap 进行认证：</p>
<pre><code>xpack:
  security:
    authc:
      realms:
        file:
          type: file
          order: 0
        ldap1:
          type: ldap
          order: 1
          ....
</code></pre>
<h4 id="32dntemplatesmode">3.2 DN templates mode</h4>
<p>如果你的 LDAP 环境定义了标准的命名规则，那么可以考虑使用 DN 模板方式，这种方式的优点是不用执行搜索就可以找到用户 DN，但是，可能需要多个绑定操作来找到正确的用户 DN。</p>
<p>DN 模板方式的配置示例如下：</p>
<pre><code>xpack:
  security:
    authc:
      realms:
        ldap1:
          type: ldap
          order: 0
          url: "ldap://ldap.xxx.com:389"
          user_dn_templates:
            - "cn={0},dc=sys,dc=example,dc=com"
            - "cn={0},dc=ops,dc=example,dc=com"
          group_search:
            base_dn: "dc=example,dc=com"
          files:
            role_mapping: "ES_PATH_CONF/role_mapping.yml"
          unmapped_groups_as_roles: false
</code></pre>
<p>该配置与用户搜索模式的区别很少：</p>
<ul>
<li>删除了用不到的 <code>bind_dn</code>，<code>user_search</code> 两个字段</li>
<li>增加了 <code>user_dn_templates</code> 配置</li>
</ul>
<p><code>user_dn_templates</code> 至少需要指定一个。DN 模板将会使用待认证的用户名替换字符串 {0}</p>
<h3 id="">总结</h3>
<p>身份认证是保护集群的基础措施，除了身份认证之外，还可以配合 IP 黑名单、白名单等方式来进行基于 IP 地址或子网的过滤， X-Pack 提供了非常全面的集群安全防护措施。</p>
<p>在识别了用户的合法身份之后，我们就可以在用户的基础上限制各种操作和资源，下一节我们介绍用户鉴权。</p>
<h3 id="-1">参考</h3>
<p>[1] <a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.5/configuring-ldap-realm.html">Configuring an LDAP realm</a></p>
<p>[2] <a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.5/security-settings.html">Security settings in Elasticsearch</a></p></div></article>