---
title: 攻克 Linux 系统编程-16
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在《第08课：理解文件系统设计思想，站在巨人肩上》一节课中，我们了解到文件通用和固定的属性信息是保存在索引节点中的。为了保持索引节点结构紧凑的同时，能够实现对文件属性的灵活扩展，Linux 内核从 2.6 开始添加了对扩展属性的支持。</p>
<p>在本节课中，我们就来详细了解一下<strong>文件的扩展属性</strong>，包括它的使用和实现方式，同时还将讨论其在访问控制中的应用，以及其他可能的应用场景，主要包括以下几方面内容：</p>
<ul>
<li>文件扩展属性概述</li>
<li>操作扩展属性的系统调用</li>
<li>文件扩展属性的实现方式</li>
<li>访问控制列表（ACL）</li>
<li>扩展属性的其他应用</li>
<li>注意事项</li>
</ul>
<h3 id="151">15.1 文件扩展属性概述</h3>
<p>文件扩展属性的设计目标是允许用户灵活地为文件设置自定义属性。</p>
<p>在 Linux 中，它是以键—值对的形式与文件索引节点（inode）关联起来的，其中键值可以是任意的自定义格式，键名需要符合 namespace.name 的命名规范。</p>
<p>在当前的 Linux 实现中，name 可以是长度不超过 256 字节的任意字符串，而 namespace 可在如下四种中选择，它们具有不同的访问控制规则。</p>
<ul>
<li><strong>user</strong>：对于该命名空间下的扩展属性，需要拥有文件的读权限来执行读取，需要写权限来执行属性的修改。</li>
<li><strong>trusted</strong>：需要特权进程才能存取该命名空间下的扩展属性。</li>
<li><strong>system</strong>：仅供操作系统内核使用，当前内核中用它实现了访问控制列表 ACL。</li>
<li><strong>security</strong>：最初设计供安全强化版 Linux（SELinux）使用。</li>
</ul>
<p>在应用层，经常使用 <strong>user</strong> 和 <strong>trusted</strong> 命名空间。</p>
<p>Linux 提供了操作文件扩展属性的 shell 命令：setfattr 和 getfattr，如下所示的命令序列展示了为指定文件 test.txt 设置名为 user.comments 的扩展属性并查看的过程：</p>
<pre><code>[root]$ setfattr -n user.comments -v "Created to demo extend attribute" test.txt
[root]$ getfattr -d test.txt
# file: test.txt
user.comments="Created to demo extend attribute"
</code></pre>
<h3 id="152">15.2 操作扩展属性的系统调用</h3>
<p>Linux 中提供了 12 个系统调用来支持对文件扩展属性的操作，按照功能可以把它们分为四组：</p>
<ul>
<li>创建或修改</li>
<li>获取</li>
<li>删除</li>
<li>查看属性名列表</li>
</ul>
<h4 id="1521">15.2.1 创建或修改</h4>
<p>与很多执行文件操作的系统调用一样，每组中的三个系统调用分别用来操作文件、符号链接和文件描述符。</p>
<p>例如，执行创建或修改扩展属性的系统调用分别为（传入新的属性名，则创建；属性名已存在，则修改）：</p>
<pre><code>int setxattr(const char *pathname, const char * name, const void *value, size_t size, int flags);
int lsetxattr(const char *pathname, const char *name, const void *vlaue, size_t size, int flags);
int fsetxattr(int fd, const char *name, const void *value, size_t size, int flags);
</code></pre>
<p>这三个系统调用从第二个参数往后都是完全一样的，功能也完全一致，**差别仅仅在于对指定操作目标文件的第一个参数的解释上：</p>
<ul>
<li>setxattr 操作 pathnane 指定的文件，如果指定的文件是一个符号链接，则对其解引用；</li>
<li>lsetxattr 系统调用中，如果 pathname 指定的文件是符号链接，则不会对其解引用，直接操作符号链接文件本身；</li>
<li>fsetxattr 的第一个参数 fd 接收一个已经打开的文件描述符。</li>
</ul>
<p>我们再看其他参数：</p>
<ul>
<li>name 参数是 namespace.name 格式的扩展属性名称；</li>
<li>value 参数指向存放有扩展属性数据的开始地址；</li>
<li>size 参数指定扩展属性数据的字节数；</li>
<li>flags 参数可以取值 XATTR_CREATE（新建属性，如果属性已经存在，则失败）或 XATTR_REPLACE（更新已有属性，如果属性不存在，则失败）。</li>
</ul>
<p>其他三组操作函数也分别具有三种不同的前缀形式，下面仅分别列出它们的普通形式。</p>
<h4 id="1522">15.2.2 获取</h4>
<p>获取扩展属性的系统调用为：</p>
<pre><code>ssize_t getxattr(const char *pathname, const char *name, void *value, size_t size);
</code></pre>
<p>其中：</p>
<ul>
<li>pathname 和 name 分别指定要查看的目标文件和目标属性名；</li>
<li>vlaue 和 size 指定接收查到的扩展属性数据的缓冲区位置和大小。</li>
</ul>
<p>如果把 size 指定为 0，则表示忽略 value 值，只查询指定属性需要的缓冲区大小。如果指定的属性找不到，或者指定的缓冲区太小，则该系统调用会失败。</p>
<h4 id="1523">15.2.3 删除扩展属性</h4>
<p>删除扩展属性的系统调用为：</p>
<pre><code>int removexattr(const char *pathname, const char *name);
</code></pre>
<p>该系统调用会把 pathname 指定的文件的名为 name 的扩展属性删除，如果指定的扩展属性不存在，则会返回 ENODATA 错误。</p>
<h4 id="1524">15.2.4 查看属性名列表</h4>
<p>查看属性名列表的系统调用为：</p>
<pre><code>ssize_t listxattr(const char *pathname, char *list, size_t size);
</code></pre>
<p>该系统调用会将 pathname 指定的文件的所有扩展属性名拷贝到指定的缓冲区中，缓冲区的地址和大小分别由 list 和 size 指定，每个属性名会用空字符分开，并返回复制到缓冲区中的字节数。应用程序可以用如下的方式遍历所有的属性名：</p>
<pre><code>#define BUFF_SIZE 4096

char xattrbuff[BUFF_SIZE];
int listlen = listxattr(pathname, xattrbuff, BUFF_SIZE);
for(int pos = 0; pos &lt; listlen; pos += (strlen(&amp;xattrbuff[pos]) + 1))
{
    char * xattrname = xattrbuff + pos;
    ...
}
</code></pre>
<h3 id="153">15.3 文件扩展属性的实现方式</h3>
<p>在《第08课：理解文件系统设计思想，站在巨人肩上》一节课中，我们了解过，文件的通用属性信息是保存在索引节点（inode）中的。在 Ext 文件系统的设计中，索引节点的大小需要是固定的，以便于从索引编号直接定位到磁盘上的保存位置。</p>
<p>此外，索引节点的大小需要尽量紧凑，以尽量提高磁盘中存储有效数据的空间的比例。因此，索引节点显然不适合用来保存能灵活扩展的扩展属性信息。</p>
<p>实际上，Linux 的文件扩展属性是保存在一个单独的数据块上的，通过索引节点中的字段 i_file_acl 索引到保存扩展属性的磁盘存储块。这个字段之所以叫做 acl，是因为扩展属性最初就是为了支持文件访问控制而引入的。</p>
<p>考虑到键名与键值都是不定长度的结构，Linux 采用了让它们各自从不同方向向中心增长的形式来存储，就像进程中堆与栈的内存使用一样。在每个磁盘存储块中，扩展属性的存储结构如下图所示：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/dc1447a0-2b52-11e9-befe-d7337e22fa57" width="400px" />
</div>
<p>在 Ext2 文件系统中，属性节点的结构定义为：</p>
<pre><code>struct ext2_xattr_entry {
    __u8    e_name_len;     /* length of name */
    __u8    e_name_index;   /* attribute name index */
    __le16  e_value_offs;   /* offset in disk block of value */
    __le32  e_value_block;  /* disk block attribute is stored on (n/i) */
    __le32  e_value_size;   /* size of attribute value */
    __le32  e_hash;         /* hash value of name and value */
    char    e_name[0];      /* attribute name */
};
</code></pre>
<p>可以看到，属性节点使用位于末尾的 e_name 配合 e_name_len 字段标记的属性名长度，实现对变长属性名的支持。</p>
<p>这里 <strong>e_name 数组在结构中定义的长度是 0，也就是不占用结构本身的存储空间，而只是一个地址位置的占位符，这是一个支持变长数据的常见技巧</strong>。这样定义之后，就可以使用如下所示的代码进行节点的内存分配与内容设置：</p>
<pre><code>char * keyname = "user.keynamex";
int keylen = strlen(keyname) + 1;
struct ext2_xattr_entry * entry = (struct ext2_xattr_entry *)malloc(sizeof(struct ext2_xattr_entry) + keylen);
entry-&gt;e_name_len = keylen;
strncpy(entry-&gt;e_name, keyname, keylen);
</code></pre>
<p>对键值，则会把它们从存储块的末尾开始依次向上排列，并用 entry 结构中的 e_value_offs 和 e_value_size 字段索引到存储位置和记录键值的长度，以此实现对变长键值的支持。</p>
<h3 id="154acl">15.4 访问控制列表（ACL）</h3>
<p>通用的文件权限控制，只能依据文件所有者、文件所有者所在的组、其他组这三个不同的层次分别设置，要达到更加详细的区分控制就无能为力了。</p>
<p>比如，如果只想给某个组中的一个或几个用户开放访问权限，或者需要对某个组内的不同成员设置不同的访问权限，通用的三级访问控制是做不到的。</p>
<p><strong>为了实现更加精细地控制，Linux 以文件扩展属性为基础，实现了文件访问控制列表（ACL）的功能</strong>，它允许最小以单个用户为单位，分别控制文件的访问权限。</p>
<p>例如，如下的命令，会让用户 apache 对 test.sh 文件具有读权限，而用户 mysql 对 test.sh 文件具有读与执行权限，其他用户（除所有者之外）都没有访问权限：</p>
<pre><code>[root]$ setfacl -m u:apache:r,u:james:rx,g::-,o::- test.sh
[root]$ getfacl --omit-header test.sh
user::rwx
user:mysql:r-x
user:apache:r--
group::---
mask::r-x
other::---
</code></pre>
<p>在 Ext2 文件系统中，ACL 由一系列权限记录组成，每条记录都定义了单个用户或用户组的文件访问权限，其数据结构定义为：</p>
<pre><code>typedef struct {
    __le16      e_tag;     //标记类型
    __le16      e_perm;    //控制权限
    __le32      e_id;      //标记附加参数
} ext2_acl_entry;
</code></pre>
<p>从如下所示的示例图中就可以很容易地理解整个 ACL 记录数组的组织方式和表达的意义：</p>
<p><img src="https://images.gitbook.cn/4e0e46f0-2b74-11e9-befe-d7337e22fa57" alt="" /></p>
<p>在这个访问控制列表里，黑色加粗的三种标记类型是与传统权限位相对应的，当没有为文件添加额外的访问控制记录时，这三个字段的信息在 inode 的文件权限字段中就可以存下，所以是不需要使用这一扩展属性的，因此也不会额外占用一块磁盘存储块，这时把它叫做最小化的 ACL。</p>
<p>当为文件给特定用户设置了访问控制权限之后，才会开始使用扩展属性来保存扩展的 ACL 信息，绑定有扩展 ACL 记录的文件，在 ls 的命令输出中，会在权限位的末尾显示 + 标记：</p>
<pre><code>[root]$ ls -l test.sh
-rwxr-x---+ 1 root root 0 Feb  7 21:12 test.sh
</code></pre>
<p>文件 ACL 记录是在扩展属性的基础上实现的，所以 Linux 内核中并没有专门操作 ACL 信息的系统调用，而是以库函数的形式提供的，ACL(5) 帮助手册（访问命令：<code>man 5 acl</code>）对这些接口进行了详细说明，这里就不再一一列出了。</p>
<h3 id="155">15.5 扩展属性的其他应用</h3>
<p>虽然文件扩展属性最早是为了实现文件访问控制列表而引入的，但就其方便而灵活的特性而言，其能力远不仅限于此。比如，还可以使用扩展属性来记录文件的作者或版权信息、文本文件的编码格式信息，等等。在 SELinux 中，使用扩展属性记录了文件的一些额外属性信息，并据此实现对文件的高级访问和能力控制。</p>
<p>另外，还可以在可执行文件的扩展属性信息中包含一些加密信息，达到让可执行文件被移动或非法拷贝之后无法使用的效果。具体的实现方案希望读者充分调动想象力，去自由发挥了，也欢迎读者在课程的讨论群中自由讨论。</p>
<h3 id="156">15.6 注意事项</h3>
<p>其实，只要了解了扩展属性在底层的实现方式，在使用中一些可能产生的问题就都能提前预见到了。这里只是作为一个总结，列出几个常见的问题。</p>
<p><strong>第一个问题的来源在于</strong>，在 Ext 文件系统中，一个文件的所有扩展属性，包括 ACL 记录，所占的总空间不能超过一个磁盘数据块的长度，而数据块的大小取决于系统管理员对系统的规划，可以是 1K、2K 或 4K 的大小，所以，如果有应用依赖超过 1K 大小的扩展属性数据的时候，就要考虑在不同配置的系统上的通用性。</p>
<p>此外，在不同的文件系统上，扩展属性名与值的总字节数上限是不一样的，在 XFS 文件系统中，这个上限甚至可以达到上百 KB。所以，依赖扩展属性的应用还需要考虑在不同文件系统上的移植性问题。</p>
<p><strong>第二个需要注意的问题在于</strong>，默认的文件拷贝命令是不会拷贝扩展属性信息的，而扩展属性信息是与 inode 绑定的，新拷贝的文件会使用新的 inode，所以，如果没有显式地指定，那么拷贝后新文件上的扩展属性会丢失。Linux 的 cp 命令的 -p 和 -a 选项都可以用来指定在拷贝时保留所有属性。</p>
<h3 id="157">15.7 总结</h3>
<p>在本节课中，我们详细介绍了 Linux 中的一种简单、灵活而且功能强大的功能：<strong>文件的扩展属性</strong>，详细介绍了<strong>它的各种操作方法</strong>，以及<strong>底层的实现方式</strong>，并且介绍了它的一项非常实用的应用 <strong>ACL</strong>，还简单讨论了<strong>扩展属性其他可能的应用方式</strong>。</p>
<p>相信通过本节课的学习，读者一定能够掌握这项强大而实用的功能，并灵活应用在自己的项目中。</p>
<h3 id="158">15.8 答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
</blockquote></div></article>