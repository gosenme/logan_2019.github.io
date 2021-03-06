---
title: 攻克 Linux 系统编程-9
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>对任何计算机系统来说，数据都是非常重要的资产，计算机中的数据通常是以文件的形式保存在磁盘上的。对大多数的计算机用户来说，通常只需要关心文件呈现出来的组织方式，而不需要关心它们在磁盘上保存和管理的技术细节。但是对某些特殊应用的开发人员来说，仅仅了解到这种程度是远远不够的，还需要对数据在磁盘上的组织方式的细节有更深入地理解，有时甚至还需要针对特定的应用场景设计自己的文件系统。</p>
<p>本节课我们就以历史悠久而又应用广泛的 <strong>Ext 文件系统</strong>为例，<strong>深入到它底层的数据结构细节，来看看它是如何组织和使用磁盘的存储空间的</strong>。通过对它的理解，希望读者可以<strong>对文件系统的设计方法和实现思路有基本的理解和认识</strong>，主要包括以下几方面内容：</p>
<ul>
<li>Ext 文件系统概述</li>
<li>Ext2 文件系统的总体结构</li>
<li>每个块组中存储块数量的确定</li>
<li>超级块与组描述符</li>
<li>数据位图与索引位图</li>
<li>索引节点</li>
<li>日志功能</li>
</ul>
<h3 id="81ext">8.1 Ext 文件系统概述</h3>
<p>Linux 上最早的比较成熟的文件系统是 1994 年引入的 Ext2，它比其前代 Ext 文件系统更加高效和稳定，从而得到了广泛的使用。再到后来，增加了日志操作支持的 Ext3 文件系统，把异常状态下文件系统的一致性检查恢复时间从数小时减少到数十秒，从而使其变得更加实用。</p>
<p>目前，<strong>大多数主流 Linux 发行版采用的 Ext4 文件系统</strong>，是对 Ext2 和 Ext3 的进一步改进，提供了更大容量的支持，更大的单个文件的支持，提高了大文件操作的效率，以及其他一些扩展性和性能方面的改进。但是其基础仍然是 Ext2 和 Ext3，所以，从相对比较简单的 Ext2 和 Ext3 开始入手，能帮助我们更快地理解文件系统设计的核心思想。</p>
<h3 id="82ext2">8.2 Ext2 文件系统的总体结构</h3>
<p>文件系统最重要的核心功能，就是在磁盘上存储文件数据，所以，理解它的第一步就是看它是<strong>如何管理整个磁盘存储空间的</strong>。</p>
<p>在 Ext2 文件系统中，磁盘的整个空间是<strong>以块为单位被管理</strong>的，块也是被分配来存储数据的最小单位，一个文件即使只有 1 字节，也会至少占用一个存储块。类似于内存中使用地址标记每个字节，文件系统用存储块的块号来标记每个存储块。</p>
<p>在 Ext2 文件系统中，可选的块大小有 1 KB、2 KB 或 4 KB，系统管理员可以根据磁盘中存储的文件的特点选择不同的块大小，如果要存储的文件大多数是几 KB 的小文件，那么选择 1 KB 的块尺寸能提高磁盘存储空间的利用率；而如果系统中大多数的文件都比较大，那么就应该选择更大的块大小，这样一方面可以提高读写效率，另一方面也可以减少需要的索引节点数量，本节后面对此会有更详细地解读。</p>
<p>文件系统管理的磁盘存储空间的范围，是除了保留给引导程序用的一个扇区之外的所有剩余空间。Ext2 文件系统把它<strong>所管理的存储空间进一步分成了很多大小相同的块组，每个块组包含了固定数量的存储块</strong>。</p>
<p>如果用一所学校来类比整个磁盘，那么学校中的每个教室就类比于一个存储块组，教室里的每一个座位就对应一个磁盘存储块；座位和教室都会被按顺序编号，从一个座位的编号，就可以计算出它所在的教室，以及在第几排第几列。</p>
<p>要完成持久化地存储文件数据的功能，文件系统除了要保存文件的数据之外，还<strong>需要保存一些元数据</strong>，用于记录每块数据存放在何处，磁盘中已用的和空闲的存储空间有哪些，以及文件的访问属性、访问时间等；另外，文件系统还需要记录被指定的块大小、索引节点数量等信息。<strong>文件系统的设计核心就在于如何组织这些信息</strong>。</p>
<p>在 Ext2 文件系统中，这些元数据被分别存储在几类特殊的块组中，它们的组织结构如下图所示：</p>
<p><img src="https://images.gitbook.cn/e2499e10-1eda-11e9-bf7f-7392878b9190" alt="" /></p>
<p>上图中，每一行标识一个存储块组，它会包含一些固定数量的存储块，每个块组的开头都会包含几类特殊的存储块，有的占有一个单独的存储块，而有的会横跨多个存储块。</p>
<p>那么：</p>
<ul>
<li>每个块组是按照什么标准划分的呢？</li>
<li>每个块组内组描述符和索引节点表的数量（m 和 n）是如何确定的呢？</li>
<li>每一类存储块中分别保存了哪些信息？</li>
</ul>
<p>下面我们就来详细解答这几个问题。</p>
<h3 id="83">8.3 每个块组中存储块数量的确定</h3>
<p>想想学校中同一个年级为什么要分成不同的班？主要是因为人数太多的话，一个班主任就管不过来了。</p>
<p>文件系统也与之类似，每个块组中会有一个存储块（数据位图）负责标记本组内所有存储块的使用状态，这个存储块就类似于学校里一个班的班主任。所以，<strong>一个块组中存储块的数量是由数据位图的标记范围来确定的</strong>。</p>
<p>位图结构是一个比特数组，每个比特用于标记一个存储块的使用状态，所以，一个存储块包含多少比特，那么一个存储块就最多包含多少个存储块。而存储块的大小是在创建文件系统的时候由系统管理员指定的，可以是 1 KB、2 KB 或者 4 KB，一旦这个大小确定了，每个块组中的存储块数量就确定了。</p>
<p>拿 256 GB 的存储空间为例，如果使用默认 4 KB 的存储块大小。那么一个数据位图块可以有 8 * 4 KB = 32 KB 个比特，可以标记 32 KB 个存储块。所以，Ext2 文件系统就会把每 32 KB 个存储块划分为一个块组，每个块组的总容量为 32 KB * 4 KB = 128 MB，整个 256 GB 的存储空间会被分成大约 2048 个块组。</p>
<h3 id="84">8.4 超级块与组描述符</h3>
<p>每个块组的开始部分都是超级块与组描述符，它们之中<strong>记录的是整个文件系统的信息</strong>，比如，超级块中会存储整个文件系统的类型、大小，文件系统中索引节点的总数量，当前文件系统的空间占用量、空闲块数量，存储块的大小，文件系统的最近一次检查时间等信息。</p>
<p><strong>组描述符中会包含每个块组的总体信息</strong>，如数据位图的块号、索引节点位图的块号、索引节点表的起始块号、空闲数据块和 inode 的个数等。每个组描述符会占用 32 字节的空间，所以，上面实例中，2048 个块组一共需要 2048 * 32 = 64 KB 的空间来存储所有的组描述符，也就是会占用 16 个存储块。</p>
<p>在 Ext2 文件系统中，超级块和组描述符虽然在每个块组里面都有一份数据，但是<strong>实际上内核只使用第 0 块</strong>，其他块组中的数据被用作第 0 块数据的备份，用于在异常状态下磁盘状态的检查和恢复。</p>
<h3 id="85">8.5 数据位图与索引位图</h3>
<p>位图的数据结构很单纯，就是一连串的比特位，每个位标记一个目标对象的当前状态。在文件系统中，比特 0 表示空闲，1 表示被占用。被位图标记的对象一般都大小固定并且连续存储，所以根据比特位的位置就可以计算出被标记对象的存储位置。</p>
<ul>
<li>数据位图的标记对象是当前块组内的每个存储块。</li>
<li>索引位图的标记对象是每个索引节点。</li>
</ul>
<p>一个数据位图会占用一个单独的存储块，前面确定块组数量的时候也提到过，一个数据位图中比特的数量决定了一个块组最多可以有多少个存储块。那么<strong>一个数据位图为什么只使用一个存储块</strong>呢？如果根据块组的数量动态确定需要的数据位图大小岂不是可以更加灵活吗？</p>
<p>其实，这里主要的原因，<strong>在于简化内核的实现，同时提高文件状态一致性的概率</strong>。内核中内存的换入换出是以页为单位的，如果一个数据位图占用多于一个内存页，那么当一个文件的内容修改就可能引起多个内存页内容的更新，这就需要内核仔细处理各种可能的出错的情况。</p>
<p>比如，如果当前要更新的内存页，有其中几块还没有换入内存，就需要先执行换入逻辑，一来这需要额外的时间，增加了数据不一致的风险；二来，如果遇到换入失败怎么办？以前写入的内容要怎么处理？是不是还需要回滚来保持文件状态的一致性？所以，为了避免实现上的这些复杂性，Ext2 文件系统在设计上就让数据位图最多占用一个存储块，规避掉这些复杂的异常情况。</p>
<p>与数据位图类似，索引位图也占用一个单独的存储块。</p>
<h3 id="86inode">8.6 索引节点（inode）</h3>
<p>索引节点的大名相信很多人都听说过，每个索引节点的标记对象是一个广义的文件。上面的几种结构都像是幕后工作人员，一般的 Linux 用户甚至可能不知道它们的存在，而索引节点就可以算是前台工作人员了，它里面存储的信息都是普通用户经常用到的。比如，ls 命令的输出中，文件的大小、访问权限、属主、修改时间等， 以及一个文件占用的所有的存储块也是在索引节点中被记录的。</p>
<p><strong>索引节点的使用状态是用索引位图标记的</strong>，为了使用位图结构，索引节点的大小需要是固定的，所有的索引节点依次保存在 N 个连续的存储块内。在 Ext2 文件系统中，索引节点的大小是 128 字节，一个 4 KB 的存储块可以容纳 32 个索引节点。</p>
<p>如果我们为每个存储块都预留一个索引节点的话，那么一个 128 M 的块组就需要 32 KB 个索引节点，也就是需要 1 KB 个存储块，所以，整个磁盘存储空间的 3% 左右需要预留出来给索引节点使用。</p>
<p>但是一般的系统中不会所有的文件都是几 KB 的小文件，所以索引节点通常不需要预留这么多。<strong>大多数 Linux 发行版的默认的存储块大小是 4 KB，每 4 个存储块预留一个索引节点</strong>，那么索引节点占用的磁盘存储空间比例就可以降低到 0.8% 左右，后期的 Ext4 文件系统中，随着文件属性的扩展，每个索引节点的大小增大了一倍，达到了 256 字节，那么索引节点占用的存储空间比例就变成了 1.56%。这就是很多文章中提到的索引节点会占用大约 1% 的磁盘存储空间的由来。其实这个比例是可变的，取决于系统管理员对系统的规划。</p>
<p>那么，另外一个问题，索引节点固定的 128 字节的结构，是如何索引不定数量的存储块的呢？每个存储块最大也只有 4KB 的大小，一个几 M 的文件，需要的存储块数量也要以千计，这么多的块号记录是如何塞进这 128 个字节之内的呢?</p>
<p>这其中的奥秘在于，索引节点使用了多级存储结构，如下图所示：</p>
<p><img src="https://images.gitbook.cn/667cd940-1edb-11e9-8e27-6579184c7916" alt="inode layout" /></p>
<p>在每个索引节点中用固定包含 15 个整数的指针数组来记录数据占用的所有存储块，其中前 12 个指针直接指向数据的存储块。</p>
<ul>
<li><p>如果文件需要的存储块数量多于 12 个，就开始动用第 13 个指针，这个指针指向的存储块中存放的不是文件数据，而是一组指针，每个指针都指向一个数据存储块。每个指针 4 个字节，一个存储块内最多可存放 256（1 KB 的存储块）到 1024（4 KB 的存储块）个存储块。</p></li>
<li><p>如果这还不够，那就动用第14个指针，这个指针是个二级指针。最多可以有 256 * 256 （1 KB 的存储块）或 1024 * 1024（4 KB 的存储块）个存储块。</p></li>
<li><p>如果还不够，就用第 15 个指针，这是个三级指针，可以索引的数据块数量可以达到 256 * 256 * 256（1 KB 的存储块）或 1024 * 1024 * 1024（4 KB 的存储块）。这样的数量级，对大多数的应用来说都足够用了。</p></li>
</ul>
<p><strong>这种存储结构使得从索引数据中可以一次定位到存储数据的多个存储块</strong>，而不像 FAT 文件系统那样，需要从一个文件簇中读取到下一个文件簇的位置。这种组织方式<strong>也方便系统把一个文件的内容分散在磁盘的不同位置</strong>，而不影响文件的读取和追加效率，这也是 <strong>Linux 很少使用磁盘碎片整理程序的原因之一</strong>。</p>
<h3 id="87">8.7 日志功能</h3>
<p>在 Ext2 文件系统中，如果遭遇突然断电，系统重启之后需要遍历整个磁盘来执行一致性检查和恢复。这在硬盘容量比较小的过去还不是什么太大问题，即使遍历整理磁盘，通常可以在几分钟内完成。但是当磁盘容量变得越来越大时，问题开始变得越来越严重，现在动辄以几百 GB 计的硬盘，完成整个磁盘的检查通常需要几个小时的时间。这对高可用服务器和生产环境服务器都是<strong>完全不可接受</strong>的。</p>
<p>所以，我们需要一种机制，在不需要遍历整个磁盘的情况下也能确保磁盘中数据的一致性。</p>
<p><strong>Linux 的 Ext3 文件系统实现了日志记录功能</strong>，它的实现思路来源于数据库技术，其基本思想是，在系统对文件系统执行任何元数据更新之前，先把要执行的操作日志记录到文件系统一块专用的日志分区内，当元数据更新完成之后，再从日志记录分区内移除该条操作记录。</p>
<p>这样，当系统重启时，只需要使用该日志分区内的信息就足以把磁盘数据恢复到一个一致的状态：</p>
<ul>
<li>如果日志分区中没有任何记录，说明系统上次停止运行时没有中途打断任何文件系统更新操作，磁盘一定是处在一致状态的；</li>
<li>如果日志分区中有操作记录，那根据记录内容重新更新一次磁盘就可以了。</li>
</ul>
<p>引入日志功能之后，磁盘的每次一致性检查最多也不过几秒钟。</p>
<p>但是，需要知道的是，日志功能<strong>保证的只是文件系统中元数据的一致性，但是并不能保证数据的完整性</strong>。也就是说，如果系统断电的时候正在写入一个体积很大的文件，那么重启之后这个文件可能会丢掉一些数据。虽然 Ext3 文件系统也可以配置为把每次写操作的数据计入日志内，以保证数据的一致性，但是这会导致非常大的性能损失，所以并不常用。</p>
<h3 id="88">8.8 总结</h3>
<p>本节课我们主要以设计精巧的 Ext2 文件系统的磁盘数据结构为主线，来学习一个<strong>文件系统的设计思路</strong>。通过对 Ext2 文件系统各种类型节点的量化分析，读者可以<strong>更加清晰地知道磁盘的存储空间是如何被组织和使用的</strong>。</p>
<h3 id="89">8.9交流与答疑</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
</blockquote></div></article>