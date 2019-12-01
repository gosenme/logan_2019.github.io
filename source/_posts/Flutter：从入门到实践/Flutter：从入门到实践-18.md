---
title: Flutter：从入门到实践-18
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将是 Flutter 常用组件的最后一节课程，相信通过前面这些课程的讲解和学习，大家已经掌握了 Flutter 的组件学习的方法和特点，适应了学习节奏。本节课主要讲解 Flutter 里的表格绘制组件的用法。</p>
<p>在 Flutter 中主要通过 Table 和 DataTable 组件来实现表格的绘制。本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>Table Widget 用法详解</li>
  <li>DataTable Widget 用法详解</li>
  <li>PaginatedDataTable Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="tablewidget">Table Widget 用法详解</h3>
<p>我们先看下表格绘制的第一种实现组件：Table。Table 的继承关系：</p>
<p>Table -&gt; RenderObjectWidget -&gt; Widget</p>
<p>Table 中的每一行用 TableRow 组件，列数用 columnWidths 属性控制。</p>
<p>我们看下 Table 的构造方法：</p>
<pre><code class="dart language-dart">Table({
    Key key,
    // 每行的TableRow集合
    this.children = const &lt;TableRow&gt;[],
    // 设置每列的宽度
    this.columnWidths,
    // 默认每列宽度值，默认情况下均分
    this.defaultColumnWidth = const FlexColumnWidth(1.0),
    // 文字方向
    this.textDirection,
    // 表格边框设置
    this.border,
    // 默认垂直方向的对齐方式
    this.defaultVerticalAlignment = TableCellVerticalAlignment.top,
    // defaultVerticalAlignment为baseline的时候，配置生效
    this.textBaseline,
  })
</code></pre>
<p>通过实例来学习 Table 的用法：</p>
<pre><code class="dart language-dart">... ...

class TableSamplesState extends State&lt;TableSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Table Demo'), primary: true),
        body: Padding(
          padding: EdgeInsets.all(10),
          // 使用Table绘制表格
          child: Table(
            // 有很多种设置宽度方式
            columnWidths: {
              ///固定列宽度
              0: FixedColumnWidth(50),

              ///弹性列宽度
              1: FlexColumnWidth(1),

              ///宽度占所在容器的百分比（0-1）
              2: FractionColumnWidth(0.5),
              3: IntrinsicColumnWidth(flex: 0.2),
              4: MaxColumnWidth(
                  FixedColumnWidth(100.0), FractionColumnWidth(0.1)),

              ///大于容器10%宽度，但小于等于100px
              5: MinColumnWidth(
                  FixedColumnWidth(100.0), FractionColumnWidth(0.1)),
            },
            // 设置表格边框
            border: TableBorder.all(color: Colors.black, width: 1),
            children: &lt;TableRow&gt;[
              // 每行内容设置
              TableRow(children: &lt;Widget&gt;[
                // 每个表格单元
                TableCell(
                  verticalAlignment: TableCellVerticalAlignment.middle,
                  child: Center(
                    child: Text(
                      'Title1',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                TableCell(
                  verticalAlignment: TableCellVerticalAlignment.middle,
                  child: Center(
                    child: Text(
                      'Title2',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                TableCell(
                  verticalAlignment: TableCellVerticalAlignment.middle,
                  child: Center(
                    child: Text(
                      'Title3',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              ]),
              TableRow(children: &lt;Widget&gt;[
                TableCell(
                  child: Text('data1'),
                ),
                TableCell(
                  child: Text('data2'),
                ),
                TableCell(
                  child: Text('data3'),
                ),
              ]),
              TableRow(children: &lt;Widget&gt;[
                TableCell(
                  child: Text('data1'),
                ),
                TableCell(
                  child: Text('data2'),
                ),
                TableCell(
                  child: Text('data3'),
                ),
              ]),
              TableRow(children: &lt;Widget&gt;[
                TableCell(
                  child: Text('data1'),
                ),
                TableCell(
                  child: Text('data2'),
                ),
                TableCell(
                  child: Text('data3'),
                ),
              ]),
              TableRow(children: &lt;Widget&gt;[
                TableCell(
                  child: Text('data1'),
                ),
                TableCell(
                  child: Text('data2'),
                ),
                TableCell(
                  child: Text('data3'),
                ),
              ]),
            ],
          ),
        ));
  }
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/Fi24EEY0m967WhzFZKVQFt9L9cEM" alt="Table" /></p>
<p>可见，Table 的用法很简单。</p>
<h3 id="datatablewidget">DataTable Widget 用法详解</h3>
<p>下面我们学习一下绘制表格的另一个组件：DataTable，这个功能更加强大，比较常用。</p>
<p>DataTable 继承自 StatelessWidget，是一个无状态组件。</p>
<p>我们看下 DataTable 的构造方法：</p>
<pre><code class="dart language-dart">DataTable({
    Key key,
    // 设置表头
    @required this.columns,
    // 列排序索引
    this.sortColumnIndex,
    // 是否升序排序，默认为升序
    this.sortAscending = true,
    // 点击全选
    this.onSelectAll,
    // 表格每行内容
    @required this.rows,
  })
</code></pre>
<p>在 DataTable 中 columns 属性里放置的是 DataColumn 来设置列属性，我们看下 DataColumn 的构造方法：</p>
<pre><code class="dart language-dart">const DataColumn({
    // 标签，可使用文本或者尺寸为18的图标
    @required this.label,
    // 工具提示
    this.tooltip,
    // 是否包含数字
    this.numeric = false,
    // 排序时调用
    this.onSort,
  })
</code></pre>
<p>在 DataTable 中 rows 属性里放置的是 DataRow 来设置行内容和属性，我们看下 DataRow 的构造方法：</p>
<pre><code class="dart language-dart">const DataRow({
    this.key,
    // 是否选中
    this.selected = false,
    // 选中状态改变时回调
    this.onSelectChanged,
    // 子表格单元
    @required this.cells,
  })
</code></pre>
<p>这里的每个子表格单元使用的是 DataCell 来设置内容和属性，看看 DataCell 的构造方法：</p>
<pre><code class="dart language-dart">const DataCell(
    // 子控件,一般为Text或DropdownButton
    this.child, {
    // 是否为占位符，若子控件为Text，显示占位符文本样式
    this.placeholder = false,
    // 是否显示编辑图标，配合onTab使用
    this.showEditIcon = false,
    // 点击回调
    this.onTap,
  })
</code></pre>
<p>接下来我们通过一个实例来看下 DataTable 的用法：</p>
<pre><code class="dart language-dart">... ...

class DataTableState extends State&lt;DataTableSamples&gt; {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('DataTable Demo'), primary: true),
        body: DataTable(
          // 行
          rows: &lt;DataRow&gt;[
            // 每行内容设置
            DataRow(
              cells: &lt;DataCell&gt;[
                // 子表格单元
                DataCell(Text('data1'), onTap: onTap),
                DataCell(Text('data2'), onTap: onTap),
                DataCell(Text('data3'), onTap: onTap),
              ],
            ),
            DataRow(
              cells: &lt;DataCell&gt;[
                DataCell(Text('data1'), onTap: onTap),
                DataCell(Text('data2'), onTap: onTap),
                DataCell(Text('data3'), onTap: onTap),
              ],
            ),
            DataRow(
              cells: &lt;DataCell&gt;[
                DataCell(Text('data1'), onTap: onTap),
                DataCell(Text('data2'), onTap: onTap),
                DataCell(Text('data3'), onTap: onTap),
              ],
            ),
            DataRow(
              cells: &lt;DataCell&gt;[
                DataCell(Text('data1'), onTap: onTap),
                DataCell(Text('data2'), onTap: onTap),
                DataCell(Text('data3'), onTap: onTap),
              ],
            ),
            DataRow(
              cells: &lt;DataCell&gt;[
                DataCell(Text('data1'), onTap: onTap),
                DataCell(Text('data2'), onTap: onTap),
                DataCell(Text('data3'), onTap: onTap),
              ],
            ),
          ],

          // 列
          columns: &lt;DataColumn&gt;[
            DataColumn(label: Text('DataColumn1')),
            DataColumn(label: Text('DataColumn2')),
            DataColumn(label: Text('DataColumn3')),
          ],
        ));
  }
}

void onTap() {
  print('data onTap');
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/FmQchek9zwGWD1zHDsI38qsx69VR" alt="avatar" /></p>
<h3 id="paginateddatatablewidget">PaginatedDataTable Widget 用法详解</h3>
<p>这里拓展一下，PaginatedDataTable 也是一个 DataTable，主要用来绘制有分页类型的表格。</p>
<p>PaginatedDataTable 继承自 StatefulWidget，是一个有状态组件。</p>
<p>PaginatedDataTable 的构造方法如下：</p>
<pre><code class="dart language-dart">PaginatedDataTable({
    Key key,
    // 表名，通常为Text，也可以是ButtonBar/FlatButton
    @required this.header,
    // 动作，List&lt;Widget&gt;集合，内部子控件大小宽高要24.0，padding为8.0
    this.actions,
    // 列集合
    @required this.columns,
    // 列排序索引
    this.sortColumnIndex,
    // 是否升序排序
    this.sortAscending = true,
    // 点击全选回调
    this.onSelectAll,
    // 初始索引
    this.initialFirstRowIndex = 0,
    // 页数更改监听，左右箭头点击时
    this.onPageChanged,
    // 默认一页显示的行数，默认为10
    this.rowsPerPage = defaultRowsPerPage,
    // 可选择页数
    this.availableRowsPerPage = const &lt;int&gt;[defaultRowsPerPage, defaultRowsPerPage * 2, defaultRowsPerPage * 5, defaultRowsPerPage * 10],
    // 点击可选择页数下拉监听
    this.onRowsPerPageChanged,
    this.dragStartBehavior = DragStartBehavior.down,
    // 表格数据源DataTableSource
    @required this.source
  })
</code></pre>
<p>PaginatedDataTable 在使用时，外层要是一个 ListView 或 ScrollView 这种可滚动容器才可以使用。</p>
<p>在使用 PaginatedDataTable 时，最重要的一个不同就是要设置 DataTableSource，我们需要编写提供一个 DataTableSource 表格数据源提供给表格数据。</p>
<p>PaginatedDataTable 的用法实例：</p>
<pre><code class="dart language-dart">class PaginatedDataTableState extends State&lt;PaginatedDataTableSamples&gt; {
  TableDataSource _dataSource = TableDataSource();
  int _defalutRowPageCount = 8;
  int _sortColumnIndex;
  bool _sortAscending = true;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('PaginatedDataTable Demo'), primary: true),
        // 外层用ListView包裹
        body: ListView(
          padding: EdgeInsets.all(10),
          children: &lt;Widget&gt;[
            // PaginatedDataTable
            PaginatedDataTable(
              // 表格数据源
              source: _dataSource,
              // 默认为0
              initialFirstRowIndex: 0,
              // 全选操作
              onSelectAll: (bool checked) {
                _dataSource.selectAll(checked);
              },
              // 每页显示的行数
              rowsPerPage: _defalutRowPageCount,
              // 每页显示数量改变后的回调
              onRowsPerPageChanged: (value) {
                setState(() {
                  _defalutRowPageCount = value;
                });
              },
              // 设置每页可以显示的行数值列表选项
              availableRowsPerPage: [5, 8],
              // 翻页操作回调
              onPageChanged: (value) {
                print('$value');
              },
              // 是否升序排序
              sortAscending: _sortAscending,
              sortColumnIndex: _sortColumnIndex,
              // 表格头部
              header: Text('Data Header'),
              // 列
              columns: &lt;DataColumn&gt;[
                DataColumn(label: Text('名字')),
                DataColumn(
                    label: Text('价格'),
                    // 加入排序操作
                    onSort: (int columnIndex, bool ascending) {
                      _sort&lt;num&gt;((Shop p) =&gt; p.price, columnIndex, ascending);
                    }),
                DataColumn(label: Text('类型')),
              ],
            ),
          ],
        ));
  }

  //排序关联_sortColumnIndex,_sortAscending
  void _sort&lt;T&gt;(Comparable&lt;T&gt; getField(Shop s), int index, bool b) {
    _dataSource._sort(getField, b);
    setState(() {
      this._sortColumnIndex = index;
      this._sortAscending = b;
    });
  }
}

class Shop {
  final String name;
  final int price;
  final String type;

  // 默认为未选中
  bool selected = false;
  Shop(this.name, this.price, this.type);
}

class TableDataSource extends DataTableSource {
  final List&lt;Shop&gt; shops = &lt;Shop&gt;[
    Shop('name', 100, '家电'),
    Shop('name2', 130, '手机'),
    Shop('三星', 130, '手机'),
    Shop('三星', 130, '手机'),
    Shop('三星', 130, '手机'),
    Shop('海信', 100, '家电'),
    Shop('TCL', 100, '家电'),
  ];
  int _selectedCount = 0;

  ///根据位置获取内容行
  @override
  DataRow getRow(int index) {
    Shop shop = shops.elementAt(index);
    return DataRow.byIndex(
        cells: &lt;DataCell&gt;[
          DataCell(
            Text('${shop.name}'),
            placeholder: true,
          ),
          DataCell(Text('${shop.price}'), showEditIcon: true),
          DataCell(Text('${shop.type}'), showEditIcon: false),
        ],
        selected: shop.selected,
        index: index,
        onSelectChanged: (bool isSelected) {
          if (shop.selected != isSelected) {
            _selectedCount += isSelected ? 1 : -1;
            shop.selected = isSelected;
            notifyListeners();
          }
        });
  }

  @override

  ///行数是否不确定
  bool get isRowCountApproximate =&gt; false;

  @override

  ///行数
  int get rowCount =&gt; shops.length;

  @override

  ///选中的行数
  int get selectedRowCount =&gt; _selectedCount;

  void selectAll(bool checked) {
    for (Shop shop in shops) {
      shop.selected = checked;
    }
    _selectedCount = checked ? shops.length : 0;
    notifyListeners();
  }

  //排序,
  void _sort&lt;T&gt;(Comparable&lt;T&gt; getField(Shop shop), bool b) {
    shops.sort((Shop s1, Shop s2) {
      if (!b) {
        //两个项进行交换
        final Shop temp = s1;
        s1 = s2;
        s2 = temp;
      }
      final Comparable&lt;T&gt; s1Value = getField(s1);
      final Comparable&lt;T&gt; s2Value = getField(s2);
      return Comparable.compare(s1Value, s2Value);
    });
    notifyListeners();
  }
}

void onTap() {
  print('data onTap');
}
</code></pre>
<p>运行效果如图：</p>
<p><img src="https://images.gitbook.cn/lvke7bZe4lmfTq3IBBaCWoTQ7Xka" alt="avatar" /></p>
<p>本节课实例地址：</p>
<p><a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_16">flutter_16</a></p>
<h3 id="">总结</h3>
<p>本节课主要是给大家讲解了 Flutter 的表格绘制组件的用法和特点。</p>
<ul>
<li>重点掌握 DataTable 和 PaginatedDataTable 的用法。</li>
<li>实践一下这几个 Widget 使用方法，尝试写一个课程表表格页面。</li>
</ul></div></article>