---
title: 高可用 Elasticsearch 集群 21 讲-5
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="1mapping">1 映射 （mapping） 基础</h3>
<p>mapping 定义了文档的各个字段如何被索引以及如何存储。我们可以把 Elasticsearch 的 mapping 看做 RDBMS 的 schema。</p>
<p>虽然 Elasticsearch 可以根据索引的数据动态的生成 mapping，我们仍然建议在创建索引时明确的定义自己的 mapping，不合理的 mapping 会引发索引和查询性能降低，磁盘占用空间变大。错误的 mapping 会导致与预期不符的查询结果。</p>
<h3 id="2">2 选择合适的数据类型</h3>
<h4 id="21textkeyword">2.1 分清 text 和 keyword</h4>
<p><strong>text 类型</strong></p>
<ul>
<li>用于存储全文搜索数据，例如：邮箱内容、地址、代码块、博客文章内容等。</li>
<li>默认结合 standard analyzer（标准解析器）对文本进行分词、倒排索引。</li>
<li>默认结合标准分析器进行词命中、词频相关度打分。</li>
</ul>
<p><strong>keyword 类型</strong></p>
<ul>
<li>用于存储需要精确匹配的数据。例如手机号码、主机名、状态码、邮政编码、标签、年龄、性别等数据。</li>
<li>用于筛选数据（如 <code>select * from x where status=‘open’</code>）、排序、聚合（统计）。</li>
<li>直接将完整的文本保存到倒排索引中，并不会对字段的数据进行分词。</li>
</ul>
<p>如果 keyword 能满足需求，尽量使用 keyword 类型。</p>
<h3 id="3mappingindexing">3 mapping 和 indexing</h3>
<p>mapping 定义得是否合理，将直接影响 indexing 性能，也会影响磁盘空间的使用。</p>
<h4 id="31mapping">3.1 mapping 无法修改</h4>
<p>Ealsticsearch 的 mapping 一旦创建，只能增加字段，不能修改已有字段的类型。</p>
<h4 id="32metafield">3.2 几个重要的 meta field</h4>
<p><strong>1. <code>_all</code></strong></p>
<p>虽然在 Elasticsearch 6.x 中，<code>_all</code> 已经是 deprecated，但是考虑到 6.x 之前的版本创建的索引 <code>_all</code> 字段是默认启用的，这里有必要详细说说明下该字段的含义。</p>
<p><code>_all</code> 字段是一个 text 字段，它将你索引的单个文档的所有字段连接成一个超级串，之后进行分词、索引。如果你不指定字段，<code>query_string</code> 查询和 <code>simple_query_string</code> 查询默认查询 <code>_all</code> 字段。</p>
<p><code>_all</code> 字段不是“免费”的，索引过程会占用额外的 CPU 资源，根据测试，在我们的数据集上，禁用 <code>_all</code> 字段后，索引性能可以提高 30%+，所以，如果您在没有明确 <code>_all</code> 含义的情况下，历史索引没有禁用 <code>_all</code> 字段，建议您重新审视该字段，看是否需要禁用，并 reindex，以获取更高的索引性能以及占用更少的磁盘空间。如果 <code>_all</code> 提供的功能对于您的业务必不可少，考虑使用 <code>copy_to</code> 参数代替 <code>_all</code> 字段。</p>
<p><strong>2. <code>_source</code></strong> </p>
<p><code>_source</code> 字段存储了你的原始 JSON 文档 <code>_source</code> 
并不会被索引，也就是说你并不能直接查询 <code>_source</code> 字段，它主要用于查询结果展示。所以启用该字段并不会对索引性能造成很大的影响。</p>
<p>除了用于查询结果展示，Ealsticsearch 的很多功能诸如 Reindex API、高亮、<code>update_by_query</code> 都依赖该字段。</p>
<p>所以实践中，我们不建议禁用该字段。如果磁盘空间是瓶颈，我们建议优先考虑禁用 <code>_all</code> 字段，<code>_all</code> 禁用达不到预期后，考虑提高索引的压缩级别，并合理使用 <code>_source</code> 字段的 <code>includes</code> 和 <code>excludes</code> 属性。</p>
<h4 id="33mapping">3.3 几个重要的 mapping 参数</h4>
<p><strong>1. index 和 store</strong></p>
<p>首先明确一下，index 属性关乎该字段是否可以用于查询，而 store 属性关乎该字段是否可以在查询结果中单独展示出来。<strong>通过跟一些业务开发人员接触，发现经常有对这两个属性不明确的情况。</strong></p>
<p>index 后的字段可以用于 search，默认你定义到 mapping 里的字段该属性的值都为 “true”。indexing 过程耗费 cpu 资源，不需要查询的字段请将该属性值设为 “false”，<strong>在业务部门使用过程中，常见的一个问题是一半以上的字段不会用于查询，但是并没有明确设置该属性，导致索引性能下降。</strong></p>
<p>由于 Elasticsearch 默认提供了 <code>_source</code> 字段，所以，大部分情况下，你无须关心 <code>store</code> 属性，默认的 “false” 能满足需求。</p>
<h5 id="enabled"><strong>enabled</strong></h5>
<p>对于不需要查询，也不需要单独 <code>fetch</code> 的字段，<code>enable</code> 可以简化 mapping 的定义。</p>
<p>例如：</p>
<pre><code>"session_data": { 
    "enabled": false
}
</code></pre>
<p>等同于</p>
<pre><code>"session_data": { 
    "type": "text",
    "index": false,
    "store": false
}
</code></pre>
<h5 id="fielddata"><strong>不要使用 <code>fielddata</code></strong></h5>
<p>自从 Elasticsearch 加入 <code>doc_value</code> 特性后，fielddata 已经没有使用的必要了。</p>
<p>有两点原因，首先，对于非 text 字段，<code>doc_value</code> 可以实现同样的功能，但是占用的内存资源更少。</p>
<p>其次，对于 <code>text</code> 字段启用 <code>fielddata</code>，由于 <code>text</code> 字段会被分词，即使启用了 <code>fielddata</code>，在其上进行聚合、排序通常是没有意义的，得到的结果也并不是期望的结果。如果确实需要对 <code>text</code> 字段进行聚合，通常使用 <code>fields</code> 会得到你想要的结果。</p>
<pre><code>PUT my_index
{
    "mappings": {
    "my_type": {
            "properties": {
                "city": {
                    "type": "text",
                    "fields": {
                        "raw": { 
                            "type":  "keyword"
                    }
                    }
                }
            }
        }
    }
}
</code></pre>
<p>之后通过 <code>city</code> 字段进行全文查询，通过 <code>city.raw</code> 字段进行聚合和排序。</p>
<p><strong>2. <code>doc_values</code></strong></p>
<p>Elasticsearch 默认对所有支持 <code>doc_values</code> 的类型启用了该功能，<strong>对于不需要聚合、排序的字段，建议禁用以节省磁盘空间。</strong></p>
<pre><code>PUT my_index
{
  "mappings": {
    "_doc": {
      "properties": {
        "session_id": { 
          "type":       "keyword",
          "doc_values": false
        }
      }
    }
  }
}
</code></pre>
<h4 id="34null_value">3.4 <code>null_value</code></h4>
<p>null 不能索引，也不能用于检索。null_value 可以让你明确的指定 null 用什么值代替，之后可以用该替代的值进行检索。</p>
<h3 id="4mappingsearching">4 mapping 和 searching</h3>
<h4 id="41globalordinals">4.1 预热 global ordinals</h4>
<p>global ordinals 主要用于加快 keyword 类型的 terms 聚合，由于 global ordinals 占用内存空间比较大，Elasticsearch 并不知道要对哪些字段进行聚合，所以默认情况下，Elasticsearch 不会加载所有字段的 global ordinals。可以通过修改 mapping 进行预加载。如下所示：</p>
<pre><code>PUT index
{
  "mappings": {
    "type": {
      "properties": {
        "foo": {
          "type": "keyword",
          "eager_global_ordinals": true
        }
      }
    }
  }
}
</code></pre>
<h4 id="42keyword">4.2 将数字标识映射成 keyword 类型</h4>
<p>Elasticsearch 在索引过程中，numbers 类型对 range 查询进行了优化，keyword 类型对 terms 查询进行了优化，如果字段字面上看是 numbers 类型，但是并不会用于 range 查询，只用于 terms 查询，将字段映射成 keyword 类型。例如 isbn、邮政编码、数据库主键等。</p>
<h3 id="">总结</h3>
<p>mapping 定义的是否合理，关系到索引性能、磁盘使用效率、查询性能，本章着重讨论了影响这些的关键 mapping 参数和 Elasticsearch 的 meta fileds，深入理解本章的内容后，mapping 应该不会成为系统瓶颈的主因。</p>
<p>第一部分的内容到此结束，这部分内容的目的介绍如何“合理地”使用 Elasticsearch，只要使用方式合理，Elasticsearch 本身问题并不多。很多时候遇到的问题都是初期的规划，使用不当造成的。</p>
<hr />
<h3 id="-1">交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《高可用 Elasticsearch 集群 21 讲》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「244」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>