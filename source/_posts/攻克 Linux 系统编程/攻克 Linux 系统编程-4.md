---
title: 攻克 Linux 系统编程-4
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本文将<strong>探讨程序的静态布局和动态布局</strong>。静态布局指可执行文件在硬盘上的内部布局，而动态布局，则是程序被系统加载到内存之后的布局。主要包括以下几部分内容：</p>
<ul>
<li>可执行文件里有什么</li>
<li>影响程序静态布局的因素</li>
<li>如何控制程序的动态布局</li>
<li>检查地址范围</li>
</ul>
<h3 id="31">3.1 可执行文件里有什么</h3>
<p>对于这个问题，相信有经验的开发人员都能给出这样的回答：可执行文件包含了源文件编译生成的可执行指令和数据。在日常开发中，理解到这个程度已经足够，但本文会做更深入的探究，以帮助读者扩展在某些方向上的技术基础，比如黑客技术。</p>
<p>在 Linux 中，<strong>二进制可执行文件的标准格式叫做 ELF</strong>（Executable and Linkable Format）。从名字可以看出，它同时<strong>兼容可执行文件和可链接文件</strong>。本文重点关注可执行文件，可链接文件将在后面课程中讨论动态链接库时再深入讲解。</p>
<h4 id="311elf">3.1.1 ELF 文件的两大组成部分</h4>
<p>概括地讲，一个 ELF 文件<strong>包含一个固定长度的文件头和多个可扩展的数据块</strong>。其中，文件头是整个可执行文件的总地图，描述了整个文件的组织结构。可扩展数据块分为两类，对应着不同的视图——在链接视图下，数据块的单位是节（Section），用<strong>多个节区头索引所有内容</strong>；而在执行视图下，数据块的单位是段（Segment），用<strong>程序头（Program Header）索引所有的段</strong>。如下图所示：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/9d25ec40-149d-11e9-a7eb-e97b85bf6ba0" width="600px" />
</div>
<p><center>图 1 ELF 文件在不同视图下的结构</center></p>
<p>我们用日常生活中一个更直观的例子做下类比，帮大家加深理解。城市里满大街的车，从用户视角来看，可以分成家用车、商务车、警车、工程车、公交车等。而在汽车动力工程师眼里，就会被分成汽油车、柴油车和电动车。这两类人的不同视角就好比 ELF 文件的不同视图，从不同视角对车的分类就好比 ELF 文件中的节和段。</p>
<h4 id="312">3.1.2 组成部分之文件头</h4>
<p>下面用一个实际程序近距离观察下 ELF 的文件头。示例代码如下：</p>
<pre><code>#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

static char static_data[16] = "I'm Static Data";
static char raw_static_data[40960];
static const char const_data[16] = "I'm Const Data";

int main(int args,char ** argv)
{
    printf("Message In Main\n");

    return 0;
}
</code></pre>
<p>通过 gcc -o elfdemo elfdemo.c 命令编译链接该程序，接着使用 readelf -h 命令查看生成的可执行文件的文件头，可看到如下信息：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/3d9fb4d0-0b1b-11e9-9130-41b9fd18af28" width="600px" />
</div>
<p><center>图 2 可执行文件 ELF 头信息</center></p>
<p>我们对图中信息做下解读。</p>
<ul>
<li>生成的可执行文件的大小是 6836 字节，文件格式是 64 位的 Linux 标准可执行文件（ELF 64-bit LSB Executable），目标平台是 x86-64。</li>
<li>程序的入口地址是 0x4003c0，该文件的 ELF 头的大小是 64 字节。</li>
<li>文件中有 8 个 Program Header，每个 Program Header 的长度是 56 字节 ，信息存放在从文件头算起 64 字节的位置。</li>
<li>另外还有 29 个 Section Header，每个 Section Header 的大小是 64 字节，信息位于从文件头算起 2632 字节的位置。</li>
</ul>
<p>根据这些信息，就可以依次定位到每个 Header，再根据 Header 中对每个段的描述，便可解析出文件内容。</p>
<h4 id="313">3.1.3 组成部分之程序头和节区头</h4>
<p><strong>使用 readelf 命令的 -S 和 -l 选项可分别列出程序头和节区头的内容</strong>，结果如下（如果你是第一次接触这些内容，请先关注输出信息的总体结构，不要陷入到输出列表的信息细节中去）：</p>
<pre><code>[root@localhost elf]# readelf -S elfdemo
There are 29 section headers, starting at offset 0xa48:

Section Headers:
  [Nr] Name          Type       Address           Offset     Size              EntSize          Flags  Link  Info  Align
  [ 0]               NULL       0000000000000000  00000000   0000000000000000  0000000000000000           0     0     0
  [ 1] .interp       PROGBITS   0000000000400200  00000200   000000000000001c  0000000000000000   A       0     0     1
  [ 2] .note.ABI-tag NOTE       000000000040021c  0000021c   0000000000000020  0000000000000000   A       0     0     4
  [ 3] .hash         HASH       0000000000400240  00000240   0000000000000024  0000000000000004   A       4     0     8
  [ 4] .dynsym       DYNSYM     0000000000400268  00000268   0000000000000060  0000000000000018   A       5     1     8
  [ 5] .dynstr       STRTAB     00000000004002c8  000002c8   000000000000003d  0000000000000000   A       0     0     1
  [ 6] .gnu.version  VERSYM     0000000000400306  00000306   0000000000000008  0000000000000002   A       4     0     2
  [ 7] .gnu.version_r VERNEED   0000000000400310  00000310   0000000000000020  0000000000000000   A       5     1     8
  [ 8] .rela.dyn     RELA       0000000000400330  00000330   0000000000000018  0000000000000018   A       4     0     8
  [ 9] .rela.plt     RELA       0000000000400348  00000348   0000000000000030  0000000000000018   A       4    11     8
  [10] .init        PROGBITS    0000000000400378  00000378   0000000000000018  0000000000000000  AX       0     0     4
  [11] .plt         PROGBITS    0000000000400390  00000390   0000000000000030  0000000000000010  AX       0     0     4
  [12] .text        PROGBITS    00000000004003c0  000003c0   0000000000000268  0000000000000000  AX       0     0     16
  [13] .fini        PROGBITS    0000000000400628  00000628   000000000000000e  0000000000000000  AX       0     0     4
  [14] .rodata      PROGBITS    0000000000400640  00000640   0000000000000030  0000000000000000   A       0     0     16
  [15] .eh_frame_hdr PROGBITS   0000000000400670  00000670   0000000000000024  0000000000000000   A       0     0     4
  [16] .eh_frame    PROGBITS    0000000000400698  00000698   000000000000007c  0000000000000000   A       0     0     8
  [17] .ctors       PROGBITS    0000000000600718  00000718   0000000000000010  0000000000000000  WA       0     0     8
  [18] .dtors       PROGBITS    0000000000600728  00000728   0000000000000010  0000000000000000  WA       0     0     8
  [19] .jcr         PROGBITS    0000000000600738  00000738   0000000000000008  0000000000000000  WA       0     0     8
  [20] .dynamic     DYNAMIC     0000000000600740  00000740   0000000000000190  0000000000000010  WA       5     0     8
  [21] .got         PROGBITS    00000000006008d0  000008d0   0000000000000008  0000000000000008  WA       0     0     8
  [22] .got.plt     PROGBITS    00000000006008d8  000008d8   0000000000000028  0000000000000008  WA       0     0     8
  [23] .data        PROGBITS    0000000000600900  00000900   0000000000000020  0000000000000000  WA       0     0     16
  [24] .bss         NOBITS      0000000000600920  00000920   000000000000a020  0000000000000000  WA       0     0     32
  [25] .comment     PROGBITS    0000000000000000  00000920   000000000000003e  0000000000000001  MS       0     0     1
  [26] .shstrtab    STRTAB      0000000000000000  0000095e   00000000000000e7  0000000000000000           0     0     1
  [27] .symtab      SYMTAB      0000000000000000  00001188   00000000000006a8  0000000000000018          28    50     8
  [28] .strtab      STRTAB      0000000000000000  00001830   0000000000000284  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
</code></pre>
<p><center>输出列表 1 节区头信息</center></p>
<p><strong>输出列表 1 列出了节区头信息</strong>。[Nr] 列是 Section 的编号，Name 列是段名，Type 列表示节区的类型，Address 表示该节区占据的虚拟内存起始地址，Offset 表示该节区在可执行文件中的存放位置（相对文件开始的偏移量），Size 列说明了该节区的大小。</p>
<p>从上面输出中可以看到，示例 ELF 文件包含了 29 个不同类型的节区，以及每个节区在文件中的位置和大小等信息。其中，.text 中存放的是源程序编译生成的可执行机器指令，.rodata、.data 和 .bss 中存放的是程序数据。</p>
<pre><code>[root@localhost elf]# readelf -l elfdemo
Elf file type is EXEC (Executable file)
Entry point 0x4003c0
There are 8 program headers, starting at offset 64

Program Headers:
  Type           Offset             VirtAddr           PhysAddr            FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000400040 0x0000000000400040  0x00000000000001c0 0x00000000000001c0  R E    8
  INTERP         0x0000000000000200 0x0000000000400200 0x0000000000400200  0x000000000000001c 0x000000000000001c  R      1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000  0x0000000000000714 0x0000000000000714  R E    200000
  LOAD           0x0000000000000718 0x0000000000600718 0x0000000000600718  0x0000000000000208 0x000000000000a228  RW     200000
  DYNAMIC        0x0000000000000740 0x0000000000600740 0x0000000000600740  0x0000000000000190 0x0000000000000190  RW     8
  NOTE           0x000000000000021c 0x000000000040021c 0x000000000040021c  0x0000000000000020 0x0000000000000020  R      4
  GNU_EH_FRAME   0x0000000000000670 0x0000000000400670 0x0000000000400670  0x0000000000000024 0x0000000000000024  R      4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000  0x0000000000000000 0x0000000000000000  RW     8

 Section to Segment mapping:
  Segment Sections...
   00
   01     .interp
   02     .interp .note.ABI-tag .hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .text .fini .rodata .eh_frame_hdr .eh_frame
   03     .ctors .dtors .jcr .dynamic .got .got.plt .data .bss
   04     .dynamic
   05     .note.ABI-tag
   06     .eh_frame_hdr
   07
</code></pre>
<p><center>输出列表 2 程序头信息</center></p>
<p><strong>输出列表 2 展示了程序头信息</strong>。该表指出 ELF 文件有八个段，并且列出了每个段在文件中的起始地址（Offset 列）、程序加载后占据的虚拟地址（VirtAddr 列）、物理地址（PhysAddr 列）、在文件中占据的空间大小（FileSiz 列）、在内存中占据的空间大小（MemSiz 列）等信息。另外，还列出了节区与段的映射关系，指出了哪些节区在运行时会归入哪个段。通过段和节区的位置和大小信息，也可以进一步核对这些映射关系。</p>
<h4 id="314elf">3.1.4 ELF 文件的细节结构</h4>
<p>至此，虽然还没有探究每块数据的具体含义，但是一个可执行文件的结构骨架已经展示在我们面前了。现在我们已经可以更加细致地回答“可执行文件里有什么？”这个问题了。以上面的示例程序为例，它的细节结构描述如下。</p>
<ul>
<li><strong>首先是 64 字节的 ELF 文件头</strong>，其中记录了该文件的类型、目标平台等信息，而且索引了整个文件需要的节区头和段头信息，详细信息如图 2 所示。</li>
<li><strong>接下来是 8 个程序头</strong>，每个 56 字节，占据了接下来的 448 字节，详细信息如输出列表 2 所示。</li>
<li><strong>紧接着是多个节区</strong>，从第 512 字节（0x00000200）开始，依次存放着从 .interp 到 .shstrtab 的 26 个节区，一直占据到了文件 2628 字节的位置（.shstrtab 节区的偏移 0x0000095e + 大小 0xe7），详细信息如输出列表 1 所示。</li>
<li><strong>然后从 2632 字节的位置开始存放节区头</strong>，一共有 29 个节区头，每个 64 字节，一共占据 1856 字节的空间，所以一直占据到文件 4487（0x1187）字节的位置。程序头的起始地址从 2632 开始而不是节区结束的 2629 字节开始，这是源于地址对齐的要求。</li>
<li><strong>最后，从 4488（0x1188）字节的位置开始，依次放置 .symtab 和 .strtab 节区</strong>，这两个节区分别占据了 1704 字节（0x6a8）和 644（0x0284）字节。</li>
</ul>
<p>至此，整个文件的所有 6836 个字节就被填满了。</p>
<h3 id="32">3.2 影响程序静态布局的因素</h3>
<p>认识了可执行文件的整体结构，我们继续<strong>讨论影响静态布局（节区信息）的因素</strong>。输出列表 1 所示的 29 个节区中，有几个节区与源程序的关系非常密切，下面就详细说说这几个节区。</p>
<h4 id="321text">3.2.1 .text 节区</h4>
<p>该节区存储了<strong>源文件编译生成的机器指令</strong>。对开发者来说，这可能是最重要的一个节区，<strong>所有的程序逻辑都放在这里</strong>。但开发者对该节区能做的控制却很少，能影响它的因素只有开发者写的程序逻辑，以及编译时使用的选项。比如，使用 -O1 优化选项编译程序可以生成尽量紧凑的 .text 节区，而用 -O2 优化选项会使编译器倾向于生成执行速度更快的指令组合，但有可能让 .text 节区的体积轻微地增大。</p>
<h4 id="322rodata">3.2.2 .rodata 节区</h4>
<p>该节区存储了程序中的<strong>常量数据</strong>。比如示例程序中的常量数组：</p>
<pre><code>static const char const_data[16] = "I'm Const Data"
</code></pre>
<p>以及 printf 语句中的常量字符串 Message In Main。有 objdump 的结果为证：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/6c1899f0-0a6f-11e9-818b-29d006bce549" width="600px" />
</div>
<p><br/>
另外，通过输出列表 2 还可以看到，程序运行时，.rodata 节区会被加载到与 .text 节区相同的段内，而且该段的属性如 Flags 列所显示的，只有 R（读）和 E（执行），而没有 W（写）权限，当程序试图修改该地址处的内容时，会因触发 Segment Violation 而令程序终止，由此实现对该节区内数据的保护。</p>
<p><font color="#F39800">但需要注意的是，只有静态和全局的 const 数据才能享受这样的待遇。</font>在某函数内声明的局部常量，只能靠编译器的语义检查报告错误或警告，而不会通过设置存储区权限来防止修改。例如，某函数内的如下代码片段，会被编译器认为存在语法错误而编译失败：</p>
<pre><code>const int const_value = 100;
const_value = 200;
</code></pre>
<p>但是，并不能阻止使用下面代码修改已经用 const 修饰过的变量值：</p>
<pre><code>const int const_value = 100;
int * ptr = (int *)&amp;const_value;
*ptr = 200;
</code></pre>
<p>因为在函数内部声明的 const_value，其本质上还是一个函数内的局部变量，存储区在该函数的栈帧内，而程序对该内存区拥有修改的权限。</p>
<p>相应地，用同样方法试图修改全局或静态常量数据的值，如下所示：</p>
<pre><code>char * pc = (char *)const_data;
*pc = 'X';
</code></pre>
<p>编译器并不会报告任何错误，编译可以通过。但当程序运行到第二行代码时，就会<strong>因为 Segment Violation 而崩溃，原因在于程序对该位置的内存区没有修改权限</strong>。</p>
<h4 id="323data">3.2.3 .data 节区</h4>
<p>所有的<strong>全局和静态的已初始化变量</strong>会存放在这个节区中，比如下面示例程序中的 static_data。</p>
<pre><code>static char static_data[16] = "I'm Static Data";
</code></pre>
<p>同样有 objdump 的结果为证：</p>
<div style="text-align:center">
    <img src="https://images.gitbook.cn/72720240-0a70-11e9-915a-ed6502011c51" width="600px" />
</div>
<p><br/>
该节区运行时会被加载到标号为 03 的段内，权限设置为 R（可读）和 W（可写）。</p>
<h4 id="324bss">3.2.4 .bss 节区</h4>
<p>该节区存储了所有<strong>未初始化或初始化为 0 的全局和静态变量</strong>。比如示例程序中的如下变量，就会被放入这个节区中。</p>
<pre><code>static char raw_static_data[40960];
</code></pre>
<p>仔细观察这个节区的信息，就会发现，虽然该节区的大小是 0xa020 字节，但它之后的 .comment 节区与该节区有相同的 Offset 值，也就是说，.bss 节区在可执行文件中不占据任何空间，加载到内存区之后才会被分配内存。</p>
<p>仔细观察程序头信息，也可以进一步验证这个结果。在程序头信息中，.bss 在标号 03 的段中，而该段的 FileSiz 值为 0x0208，MemSiz 值为 0xa228，其差值刚好是 .bss 节区的大小。</p>
<p><font color="#F39800">该节区的设计初衷就是为了节省目标文件的存储空间。</font>变量未被初始化，或者虽被初始化了，但值为 0，就没必要浪费空间，再在目标文件中存储大量的 0 值。</p>
<h4 id="325gotplt">3.2.5 .got 和 .plt 节区</h4>
<p>这两个节区<strong>存储了动态链接用到的全局入口表和跳转表</strong>。当你的程序中用到动态链接库中的某个函数时，会在该节区内记录相应的数据。详细内容将在后面课程中深入介绍动态链接库时再展开。</p>
<h4 id="326">3.2.6 用扩展属性指定节区</h4>
<p>除了变量类型会影响数据的存储节区以外，GCC 还支持用 GUN C 的一个扩展属性指定数据的存储节区。</p>
<pre><code>__attribute__((section("personal"))) char g_array[1024];
</code></pre>
<p>例如上面代码，就会把 g_array 放到新的 personal 节区中。但使用该特性时，应该清楚如此声明的全局或静态变量，不管有没有初始化，都会在可执行文件中占据相应的存储空间，<strong>不能再享受 .bss 段所带来的节省存储空间的好处</strong>。</p>
<h3 id="33">3.3 控制程序的动态布局</h3>
<p>控制程序的动态布局，就是<strong>控制 ELF 文件中程序头的信息</strong>，而这些信息由链接器（LD）负责组装。所以，控制了链接器的组装行为，即可控制程序的动态布局。</p>
<p>控制链接器的组装行为由链接控制脚本（后缀通常为 lds）负责。该脚本描述了如何把输入文件中的各部分组装到生成文件中，并控制输出文件中的每个段在内存中的排布。开发人员平时很少接触到该脚本，是因为 GCC 提供的默认链接脚本已经能够满足绝大多数需求了。</p>
<h4 id="331">3.3.1 链接控制脚本</h4>
<p>生硬地讲解链接脚本的语法和功能是很无趣的，所以我决定先抛出一个具体的需求，通过这个需求<strong>探索链接脚本的功能和用法</strong>。</p>
<p>需求是这样的，在应用中，有一块静态长度的数据非常重要，我们需要保护这块数据，确保它不会被意料之外的数组溢出或者错误的指针修改。如果真发生意料之外的修改，那么就让程序崩溃，以让该逻辑错误尽早地暴露出来。同时，该数据块又不是完全只读的，某些特定情况下，还需修改这块数据的内容。需要长期稳定运行的软件产品，其配置数据通常会有这样的需求。</p>
<p>我们分析下这个需求。当意料之外的修改发生时，要实现程序崩溃功能，这块数据首先应该被<strong>设置为只读</strong>。当遇到特定情况，要对数据内容修改时，又需要为这块内存<strong>添加修改权限</strong>。可以<strong>使用系统调用 mprotect 来实现</strong>，但要使用这个系统调用，还需要把这块受保护数据的存储地址按照内存页的大小对齐。</p>
<p>同时想到可以用 GUN C 的扩展特性自定义节区，于是我们有了如下解决方案：</p>
<ul>
<li>把受保护的变量<strong>放入一个自定义的节区</strong>，让该节区的加载地址按照内存页大小对齐，并让它之后的其他节区从新的内存页开始布局；</li>
<li>受保护的内容初始化完毕之后，用 mprotect 系统调用将受保护内容所占的内存页都<strong>设置为写保护</strong>；</li>
<li>为受保护变量添加专门的数据修改 API，API 中先为要修改的内存页<strong>添加写权限</strong>，修改完成后<strong>马上移除写权限</strong>。</li>
</ul>
<p>把数据放入自定义的节区很简单，只要使用 GUN C 的属性标记就可以了：</p>
<pre><code>__attribute__((section(".protect"))) SecurityDataStruct g_secData;
</code></pre>
<p>如何控制它的内存地址呢？想想默认生成的可执行文件，.text 和 .rodata 节区的数据会被放入同一个段，并被设置为 RE（Read）权限。接下来，会排布 .data 和 .bss 等节区所在的数据段，并将权限设置为 RW（Read &amp; Write），所以数据段的地址一定是从一个新的内存页开始的。默认脚本是怎么实现这个效果的呢？</p>
<h4 id="332sections">3.3.2 脚本中的 SECTIONS 块</h4>
<p>我们<strong>用 ld --verbose 命令查看下默认链接脚本的内容</strong>，看看能发现什么。输出结果如下（实际输出的内容很多，为了方便讲解，只保留了一部分结果，并添加了行标号）：</p>
<pre><code>1  OUTPUT_FORMAT("elf64-x86-64")
2  ENTRY(_start)
3  SEARCH_DIR("/usr/local/lib64"); SEARCH_DIR("/lib64"); SEARCH_DIR("/usr/lib64");
4  SECTIONS
5  {
6    
7    PROVIDE (__executable_start = SEGMENT_START("text-segment", 0x400000)); 
8    . = SEGMENT_START("text-segment", 0x400000) + SIZEOF_HEADERS;
9    .init           :  {  KEEP (*(.init))  } =0x90909090
10   .text           :
11   {
12     *(.text.unlikely .text.*_unlikely)
13     *(.text .stub .text.* .gnu.linkonce.t.*)
14   } =0x90909090
15   .fini           :  {  KEEP (*(.fini)) } =0x90909090
16   PROVIDE (etext = .);
17   .rodata         : { *(.rodata .rodata.* .gnu.linkonce.r.*) }
18   . = ALIGN (CONSTANT (MAXPAGESIZE)) - ((CONSTANT (MAXPAGESIZE) - .) &amp; (CONSTANT (MAXPAGESIZE) - 1)); 
19   . = DATA_SEGMENT_ALIGN (CONSTANT (MAXPAGESIZE), CONSTANT (COMMONPAGESIZE));
20   .data           :
21   {
22     *(.data .data.* .gnu.linkonce.d.*)
23     SORT(CONSTRUCTORS)
24   }
25   _edata = .; PROVIDE (edata = .);
26   __bss_start = .;
27   .bss            :
28   {
29    *(.dynbss)
30    *(.bss .bss.* .gnu.linkonce.b.*)
31   }
32   . = ALIGN(64 / 8);
33   _end = .; PROVIDE (end = .);
     ......
</code></pre>
<p>可以看到，<strong>一个链接脚本中最主要的部分是 SECTIONS 块，里面定义了生成的节区的映射关系</strong>，基本格式为：</p>
<pre><code>.output : { *(.input)}
</code></pre>
<p>它表示把输入文件中名字为 xxx.input 的节区内容合并到输出文件的 .output 节区。另外，第 8、18、19 行出现了：</p>
<pre><code>. = xxxx
</code></pre>
<p>表示把当前的组装地址定位到内存地址 xxxx 处。18、19 行表示组装完 .rodata 节区之后，对 .  执行的一些计算，即把当前的组装地址移动到下一个内存页的开始位置，这样 .data 的开始地址便从下一个内存页开始了。</p>
<p>仿照其内容，我们可以在 .bss 节区之前增加我们自定义的 .protect 节区：</p>
<pre><code>. = . - (. &amp; (CONSTANT (COMMONPAGESIZE) - 1)) + (CONSTANT (COMMONPAGESIZE));
.protect        : { *(.protect)}
. = . - (. &amp; (CONSTANT (COMMONPAGESIZE) - 1)) + (CONSTANT (COMMONPAGESIZE));
</code></pre>
<p>使用这个自定义 lds 脚本重新编译源程序（使用 GCC 的 -Wl 选项为 linker 传递自定义参数 -T protect.lds，指定使用的自定义链接控制脚本）：</p>
<pre><code>gcc -o elfdemo elfdemo.c -Wl,-T protect.lds
</code></pre>
<p>用 readelf -S 查看生成的可执行文件，其中可以看到新加的 .protect 节区，如下图所示：</p>
<p><img src="https://images.gitbook.cn/cc723610-0a71-11e9-9dab-af44651d2dfb" alt="" /></p>
<p>从中可以发现，新加的 .protect 节区放在了 .data 节区之后，加载地址从一个新的内存页 0x602000 开始，虽然其大小只有 0x404 字节，但独占了一个内存页，其后的 .bss 节区从新的内存页地址 0x603000 位置开始。这样，我们就<strong>可以自由地对保护数据所在的内存页执行权限修改操作</strong>，而不影响其他节区内的数据。</p>
<h3 id="34">3.4 检查地址范围</h3>
<p>细心的读者可能还会发现，在默认链接文件的输出内容中有如下这样的内容：</p>
<pre><code>25   _edata = .; PROVIDE (edata = .);
26   __bss_start = .;
</code></pre>
<p>它们有什么用呢？</p>
<p>实际上，它们<strong>是在链接脚本中定义的一些符号</strong>。在这里，这些标号用来记录当前的组装地址。在程序中我们可以这样使用：</p>
<pre><code>int main()
{
   extern char __bss_start;
   printf(".bss Start Address: %p\n", &amp;__bss_start);
   return 0;
}
</code></pre>
<p>仿照此方法，可以给我们的保护数据段也增加两个范围标号：</p>
<pre><code>  . = . - (. &amp; (CONSTANT (COMMONPAGESIZE) - 1)) + (CONSTANT (COMMONPAGESIZE));
  __protect_start = .;
  .protect        : { *(.protect)}
  __protect_end = .;
  . = . - (. &amp; (CONSTANT (COMMONPAGESIZE) - 1)) + (CONSTANT (COMMONPAGESIZE));
</code></pre>
<p>程序可以通过这两个标号的地址，精确地判定给定的地址是不是有效的保护区地址：</p>
<pre><code>#define IS_PROTECT_ADDRESS(ptr)  (((char *)ptr &gt;= &amp;__protect_start &amp;&amp; (char *)ptr &lt; &amp;__protect_end) ? 1 : 0)
</code></pre>
<p><font color="#F39800">需要注意的是，链接脚本中定义的标号只是用来标定一个地址，并不会为它准备额外的存储空间</font>，也就是说，&amp;__protect_start 和 &amp;g_secData 会得到相同的地址。所以，永远不要对 __protect_start 执行赋值操作。</p>
<p>默认的链接脚本中还提供了 __executable_start、__etext、_edata、__bss_start 等导出标号，分别用于标记代码段的开始地址、代码段的结束地址、数据段的结束地址、bss 段的开始地址等，应用程序可以按需选用。当需要更多标记地址时，在链接控制脚本里自定义添加就可以了。</p>
<h3 id="35">3.5 总结</h3>
<p>本文带领读者深入到了 Linux 平台上可执行文件的内部，着重<strong>了解了可执行文件内部的信息是如何组织的</strong>，以及程序中<strong>不同类型的变量在可执行文件中是如何存放</strong>的，然后通过一个真实需求<strong>窥探了链接控制脚本的功能</strong>。</p>
<p>通过本文的学习，读者应该对可执行文件的底层运作细节有更深刻的理解，同时有能力实现下面这些需求，至少会有实现思路：</p>
<ul>
<li>如果手上有某个英文版应用的可执行程序，如何对其进行汉化？</li>
<li>若要将可执行文件中的某些资源提取出来，该如何写程序？</li>
<li>如何实现程序自检，也就是确认自己的代码段数据没有被人暴力修改过？</li>
<li>一旦程序被外部修改，将无法正确执行，该如何实现？</li>
<li>如何保护保存在可执行文件中的资源或敏感数据？</li>
</ul>
<p>总之，了解越深入，对应用的控制能力也就越强，也就能实现更酷的功能！</p>
<h3 id="36">3.6 答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《攻克 Linux 系统编程》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「208」给小助手-伽利略获取入群资格。</strong></p>
  <p><strong>参考资料</strong></p>
  <p>GitHub 源代码网址：</p>
  <p><a href="https://github.com/boswelyu/GitChatLesson-LinuxDevInDepth/tree/master/Lesson3">https://github.com/boswelyu/GitChatLesson-LinuxDevInDepth/tree/master/Lesson3</a></p>
</blockquote></div></article>