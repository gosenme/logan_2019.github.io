---
title: 高可用 Elasticsearch 集群 21 讲-17
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在上一课中，我们解决了身份认证的问题，现在，我们能够保证访问集群的是合法用户，但是任何用户都可以访问集群的全部索引，在多个业务使用同一个集群时，可能某个业务的数据不希望被其他人看到，也不希望被其他人写入，删除数据，这就需要控制用户的权限，让某个用户只能访问某些索引。</p>
<p>在 X-Pack 中，这通过 RBAC 实现，他支持字段级别的权限配置，并且可以限制用户对集群本身的管理操作。</p>
<p><strong>X-Pack 中对用户进行授权包括两个步骤：</strong></p>
<ul>
<li>创建一个角色，为角色赋予某些权限。</li>
<li>将用户映射到角色下。</li>
</ul>
<h3 id="1">1. 内置角色</h3>
<p>如同内置用户一样，X-Pack 中内置一些预定义角色，这些角色是只读的，不可修改。内置用户与角色的映射关系如下图所示：</p>
<p><img src="https://images.gitbook.cn/FsJW9j7QwD6qzLc-ycUwJkC-aawj" alt="avatar" /></p>
<p><strong>下面介绍一些常用的内置角色：</strong></p>
<ul>
<li><p><strong>superuser</strong></p>
<p>对集群具有完全的访问权限，包括集群管理、所有的索引，模拟其他用户，并且可以管理其他用户和角色。默认情况下，只有 elastic 用户具有此角色。</p></li>
<li><p><strong>kibana_system</strong></p>
<p>具有读写Kibana索引，管理索引模板，检查集群可用性等权限，对 <code>.monitoring-*</code>  索引具有读取权限，对 <code>.reporting-*</code> 索引具有读写权限。</p></li>
<li><p><strong>logstash_system</strong></p>
<p>允许向 Elasticsearch 发送系统级数据，例如监控数据等。</p></li>
</ul>
<h3 id="2securityprivilege">2. Security privilege</h3>
<p>我们首先需要了解一下对 Elasticsearch 中的资源都有哪些权限，例如在 Linux 文件系统中，对文件有读/写，执行等权限，Elasticsearch 中资源的权限也有特定的名称，下面列出一些常用的 privilege，完整的列表请参考官方手册。</p>
<h4 id="21clusterprivileges">2.1 Cluster privileges</h4>
<p>对集群的操作权限常见的有下列类型：</p>
<ul>
<li><p><strong><code>all</code></strong></p>
<p>所有集群管理操作，如快照、节点关闭/重启、更新设置、reroute 或管理用户和角色。</p></li>
<li><p><strong><code>monitor</code></strong></p>
<p>所有的对集群的只读操作，例如集群健康，集群状态，热点线程，节点信息、节点状态、集群状态，挂起的集群任务等。</p></li>
<li><p><strong><code>manage</code></strong></p>
<p>基于 monitor 权限，并增加了一些对集群的修改操作，例如快照，更新设置，reroute，获取快照及恢复状态，但不包括安全相关管理权限。</p></li>
<li><p><strong><code>manage_index_templates</code></strong></p>
<p>对索引模块的所有操作</p></li>
<li><p><strong><code>manage_rollup</code></strong></p>
<p>所有的 rollup 操作，包括创建、启动、停止和删除 rollup 作业。</p></li>
<li><p><strong><code>manage_security</code></strong></p>
<p>所有与安全相关的操作，如用户和角色上的 CRUD 操作和缓存清除。</p></li>
<li><p><strong><code>transport_client</code></strong></p>
<p>传输客户端所需的所有权限，在启用跨集群搜索时会用到。</p></li>
</ul>
<h4 id="22indicesprivileges">2.2 Indices privileges</h4>
<ul>
<li><p><strong><code>all</code></strong></p>
<p>对索引的所有操作。</p></li>
<li><p><strong><code>create</code></strong></p>
<p>索引文档，以及更新索引映射的权限。</p></li>
<li><p><strong><code>create_index</code></strong></p>
<p>创建索引的权限。创建索引请求可能包含添加到别名的信息。在这种情况下，请求还需要对相关索引和别名的 <strong>manage</strong> 权限。</p></li>
<li><p><strong><code>delete</code></strong></p>
<p>删除文档的权限。</p></li>
<li><p><strong><code>delete_index</code></strong></p>
<p>删除索引。</p></li>
<li><p><strong><code>index</code></strong></p>
<p>索引，及更新文档，以及更新索引映射的权限。</p></li>
<li><p><strong><code>monitor</code></strong></p>
<p>监控所需的所有操作（recovery, segments info, index stats and status）。</p></li>
<li><p><strong><code>manage</code></strong></p>
<p>在 <strong>monitor</strong> 权限基础上增加了索引管理权限（aliases, analyze, cache clear, close, delete, exists, flush, mapping, open, force merge, refresh, settings, search shards, templates, validate）。</p></li>
<li><p><strong><code>read</code></strong></p>
<p>只读操作（count, explain, get, mget, get indexed scripts, more like this, multi percolate/search/termvector, percolate, scroll, clear_scroll, search, suggest, tv）</p></li>
<li><p><strong><code>read_cross_cluster</code></strong></p>
<p>对来着远程集群的只读操作。</p></li>
<li><p><strong><code>view_index_metadata</code></strong></p>
<p>对索引元数据的只读操作（aliases, aliases exists, get index, exists, field mappings, mappings, search shards, type exists, validate, warmers, settings, ilm）此权限主要给 Kibana 用户使用。</p></li>
<li><p><strong>write</strong></p>
<p>对索引的所有写操作，包括索引，更新，删除文档，bulk 操作，更新索引映射。</p></li>
</ul>
<h4 id="23runasprivilege">2.3 Run as privilege</h4>
<p>该权限允许一个已经进行了身份认证的合法用户代表另一个用户提交请求。取值可以是一个用户名，或用户名列表。</p>
<h4 id="24applicationprivileges">2.4 Application privileges</h4>
<p>应用程序权限在 Elasticsearch 管理，但是与 Elasticsearch 中的资源没有任何关系，他的目的是让应用程序在 Elasticsearch 的角色中表示和存储自己的权限模型。</p>
<h3 id="3">3. 定义新角色</h3>
<p>你可以在 Kibana中 创建一个新角色，也可以用 REST API 来创建，为了比较直观的演示，我们先来看一下 Kibana 中创建角色的界面，如下图所示。</p>
<p><img src="https://images.gitbook.cn/FhIXy4wjTNTmdCqdqYqdeIxKFxFK" alt="avatar" /></p>
<p>需要填写的信息包括：</p>
<p>角色名称：此处我们定义为 weblog_user；</p>
<p>集群权限：可以多选，此处我们选择 monitor，让用户可以查看集群信息，也可以留空；</p>
<p>Run As 权限：不需要的话可以留空；</p>
<p>索引权限：填写索引名称，支持通配，再从索引权限下拉列表选择权限，可以多选。如果要为多个索引授权，通过 “Add index privilege” 点击按钮来添加。</p>
<p>如果需要控制字段级权限，在字段栏中填写字段名称，可以填写多个。</p>
<p>如果希望角色只能访问索引的部分文档怎么办？可以通过定义一个查询语句，让角色只能访问匹配查询结果的文档。</p>
<p>类似的，通过 REST API 创建新角色时的语法基本上就是上述要填写的内容：</p>
<pre><code>{
  "run_as": [ ... ], 
  "cluster": [ ... ], 
  "global": { ... }, 
  "indices": [ ... ], 
  "applications": [ ... ] 
}
</code></pre>
<p>其中 global 只在 applications 权限中才可能会使用，因此暂时不用关心 global 字段与 applications 字段。indices 字段中需要描述对哪些索引拥有哪些权限，他有一个单独的语法结构：</p>
<pre><code>{
  "names": [ ... ], 
  "privileges": [ ... ], 
  "field_security" : { ... }, 
  "query": "..." 
}
</code></pre>
<p>names：要对那些索引进行授权，支持索引名称表达式；</p>
<p>privileges：权限列表；</p>
<p>field_security：指定需要授权的字段；</p>
<p>query：指定一个查询语句，让角色只能访问匹配查询结果的文档；</p>
<p>引用官方的一个的例子如下：</p>
<pre><code>POST /_xpack/security/role/clicks_admin
{
  "run_as": [ "clicks_watcher_1" ],
  "cluster": [ "monitor" ],
  "indices": [
    {
      "names": [ "events-*" ],
      "privileges": [ "read" ],
      "field_security" : {
        "grant" : [ "category", "@timestamp", "message" ]
      },
      "query": "{\"match\": {\"category\": \"click\"}}"
    }
  ]
}
</code></pre>
<ul>
<li>创建的角色名称为 <code>clicks_admin</code>；</li>
<li>以 <code>clicks_watcher_1</code> 身份执行请求；</li>
<li>对集群有 <code>monitor</code> 权限；</li>
<li>对索引 <code>events-*</code> 有 read 权限；</li>
<li>查询语句指定，在匹配的索引中，只能读取 <code>category</code> 字段值为 <code>click</code> 的文档；</li>
<li>在匹配的文档中只能读取  <code>category</code>，<code>@timestamp message</code> 三个字段；</li>
</ul>
<p>除了使用 REST API 创建角色，你也可以把将新建的角色放到本地配置文件 <code>$ES_PATH_CONF/roles.yml</code> 中，配置的例子如下：</p>
<pre><code>click_admins:
  run_as: [ 'clicks_watcher_1' ]
  cluster: [ 'monitor' ]
  indices:
    - names: [ 'events-*' ]
      privileges: [ 'read' ]
      field_security:
        grant: ['category', '@timestamp', 'message' ]
      query: '{"match": {"category": "click"}}'
</code></pre>
<p><strong>总结一下 X-Pack 中创建角色的三种途径：</strong></p>
<ul>
<li><p>通过 REST API 来创建和管理，称为 Role management API，角色信息保存到 Elasticsearch 的一个名为 <code>.security-</code> 的索引中。这种方式的优点是角色集中存储，管理方便，缺点是如果需要维护的角色非常多，并且需要频繁操作时，REST 接口返回可能会比较慢，毕竟每个角色都需要一次单独的 REST 请求。</p></li>
<li><p>通过记录到本地配置文件 <code>roles.yml</code> 中，然后自己用 Ansible 等工具同步到各个节点，Elasticsearch 会定期加载这个文件。</p>
<p>这种方式的优点是适合大量的角色更新操作，缺点是由于需要自己将 <code>roles.yml</code> 同步到集群的各个节点，同步过程中个别节点遇到的异常可能会导致部分节点的角色更新不够及时，最终表现是用户访问某些节点可以操作成功，而某些访问节点返回失败。</p></li>
<li><p>通过 Kibana 界面来创建和管理，实际上是基于 Role management API 来实现的。</p></li>
</ul>
<p>你也可以将角色信息存储到 Elasticsearch 之外的系统，例如存储到 S3，然后编写一个 Elasticsearch 插件来使用这些角色，这种方式的优点是角色集中存储，并且适合大量角色更新操作，缺点是你需要自己动手开发一个插件，并且对引入了新的外部依赖，对外部系统稳定性也有比较高的要求。</p>
<h3 id="4">4. 将用户映射到角色</h3>
<p>经过上面步骤，我们已经创建了一个新角色 weblog_user，现在需要把某个用户映射到这个角色下。仍然以 Kibana 图形界面为例，我们可以直接在 Roles 的下拉列表中为用户选取角色，可以多选。</p>
<p><img src="media/15474561832698/15498900722741.jpg" alt="" /></p>
<p>这是一个非常简单的映射关系，但是映射方法很多：</p>
<ul>
<li><p>对于 native 或 file 两种类型 realms 进行验证的用户，需要使用  User Management APIs 或 users 命令行来映射。</p></li>
<li><p>对于其他 realms ，需要使用 role mapping API 或者 一个本地文件 <code>role_mapping.yml</code> 来管理映射关系（早期的版本中只支持本地配置文件方式）。</p></li>
<li><p>role mapping API ：基于 REST 接口，映射信息保存到 Elasticsearch 的索引中。</p></li>
<li><p>本地角色映射文件 <code>role_mapping.yml</code>：需要自行同步到集群的各个节点，Elasticsearch 定期加载。</p></li>
</ul>
<p>通过REST API 或 <code>role_mapping.yml</code> 本地配置文件进行映射的优缺点与创建角色时使用 API 或本地文件两种方式优缺点相同，不再赘述。</p>
<p>使用角色映射文件时，需要在 <code>elasticsearch.yml</code> 中配置  <code>role_mapping.yml</code> 文件的路径，例如：</p>
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
<p>在 <code>role_mapping.yml</code> 配置中简单地描述某个角色下都有哪些用户，以 LDAP 用户为例：</p>
<pre><code>monitoring: 
  - "cn=admins,dc=example,dc=com" 
weblog_user:
  - "cn=John Doe,cn=contractors,dc=example,dc=com" 
  - "cn=users,dc=example,dc=com"
  - "cn=admins,dc=example,dc=com"
</code></pre>
<p>上面的例子中，admins 组被映射到了 monitoring 和 <code>weblog_user</code> 两个角色，users 组和 John Doe 用户被映射到了 <code>weblog_user</code> 角色。这个例子使用角色映射 API 的话则需要执行以下两个：</p>
<pre><code>PUT _xpack/security/role_mapping/admins
{
  "roles" : [ "monitoring", "weblog_user" ],
  "rules" : { "field" : { "groups" : "cn=admins,dc=example,dc=com" } },
  "enabled": true
}
</code></pre>
<pre><code>PUT _xpack/security/role_mapping/basic_users
{
  "roles" : [ "user" ],
  "rules" : { "any" : [
      { "field" : { "dn" : "cn=John Doe,cn=contractors,dc=example,dc=com" } },
      { "field" : { "groups" : "cn=users,dc=example,dc=com" } }
  ] },
  "enabled": true
}
</code></pre>
<h3 id="">总结</h3>
<p>本章重点介绍了 X-Pack 中创建角色，已经将用户映射到角色下的方法和注意事项，无论使用 REST API还是使用本地配置文件，每种方式都有它的优缺点，如果你的环境中已经有一些文件同步任务，那么可以统一使用同步本地配置文件的方式，或者无论创建角色，还是映射角色，全都使用 REST API。</p>
<p>X-Pack 中无法为用户指定特定的索引模板权限，用户要么可以读写所有的模板，要么无法读写模板。而通常来说对于日志等按日期滚动生成索引的业务都需要先创建自己的索引模板，这可能是因为无法预期用户创建索引模板的时候会将模板匹配到哪些索引。</p>
<p>因此推荐不给业务分配索引模板写权限，由管理员角色的用户来检查索引模板规则，管理索引模板。</p>
<p>下一节我们介绍一下节点间的通讯如何加密，在早期版本中，这是一个可选项，现在的版本中要求必须开启。</p>
<h3 id="-1">参考</h3>
<p><a href="https://www.elastic.co/guide/en/elastic-stack-overview/6.5/defining-roles.html">Defining roles</a></p>
<p><a href="https://www.elastic.co/guide/en/elastic-stack-overview/current/security-privileges.html">Security privileges</a></p>
<p><a href="https://www.elastic.co/guide/en/elastic-stack-overview/6.5/mapping-roles.html">Mapping users and groups to roles</a></p>
<p><a href="https://www.elastic.co/guide/en/elastic-stack-overview/6.5/custom-roles-provider.html">Custom roles provider extension</a></p>
<p><a href="https://www.elastic.co/guide/en/elastic-stack-overview/6.5/field-and-document-access-control.html">Setting up field and document level security</a></p></div></article>