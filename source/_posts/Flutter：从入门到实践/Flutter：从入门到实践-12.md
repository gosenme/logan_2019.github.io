---
title: Flutter：从入门到实践-12
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>这节课将继续讲解 Flutter 的常用基础组件的最后两个——TextField 和 Form 表单。通过基础组件的学习，大家可以尝试绘制一些基础页面，实现一些基础功能，例如注册页面、登录页面、简单的信息展示页面等。</p>
<p>TextField 相当于 Android 里的 EditText，HTML 的输入框等，不过 Flutter 的 TextField 可配置的功能要多一些，功能要强大一些，Form 表单和 HTML 的 Form 表单的作用基本一样，所以学习来应该很快。那么这节课就带领大家对 Flutter 的基础布局 Widget 中的这几个 Widget 进行详细分析讲解，并结合案例进行详细的用法讲解。</p>
<p>本文将主要介绍：</p>
<blockquote>
  <ul>
  <li>TextField Widget 用法详解</li>
  <li>Form 表单 Widget 用法详解</li>
  </ul>
</blockquote>
<h3 id="1textfieldwidget">1 TextField Widget 用法详解</h3>
<p>不同平台的输入框一般都需要以下功能，提示信息、输入框接收的数据类型、输入框监听事件等。Flutter 里的TextField 同样具有这些属性功能，TextField 属于 StatefulWidget，Flutter 中有两个 TextField，另一个叫TextFormField，顾名思义，这个 TextFormField 主要用于 Form 表单，我们看下要讲的 TextField 的构造方法：</p>
<pre><code class="dart language-dart">const TextField({
    Key key,
    // 输入框的控制器，监听器
    this.controller,
    // 焦点控制的，控制是否获取和取消焦点
    this.focusNode,
    // 输入框的装饰类（重要）
    this.decoration = const InputDecoration(),
    // 输入框输入类型，键盘显示类型
    TextInputType keyboardType,
    // 控制键盘上的动作按钮图标
    this.textInputAction,
    // 键盘大小写显示控制
    this.textCapitalization = TextCapitalization.none,
    // 输入文本的样式
    this.style,
    // 输入文本的对齐方式
    this.textAlign = TextAlign.start,
    // 输入文本的方向
    this.textDirection,
    // 是否自动获取焦点
    this.autofocus = false,
    // 是否是密码（是否遮盖输入内容，起保护作用）
    this.obscureText = false,
    // 是否自动更正
    this.autocorrect = true,
    // 最大行数
    this.maxLines = 1,
    // 输入文本最大长度
    this.maxLength,
    // 达到最大长度后：为true时会阻止输入，为false时不会阻止输入，但输入框会变红进行提示
    this.maxLengthEnforced = true,
    // 输入内容改变时的回调
    this.onChanged,
    // 输入完成，按回车时调用
    this.onEditingComplete,
    // 输入完成，按回车时回调，回调里有参数：参数为输入的内容
    this.onSubmitted,
    // 输入个事校验，如只能输入手机号
    this.inputFormatters,
    // 是否可用
    this.enabled,
    // 光标宽度
    this.cursorWidth = 2.0,
    // 光标圆角
    this.cursorRadius,
    // 光标颜色
    this.cursorColor,
    // 键盘样式，暗黑主题还是亮色主题
    this.keyboardAppearance,
    this.scrollPadding = const EdgeInsets.all(20.0),
    this.dragStartBehavior = DragStartBehavior.down,
    // 为true的时候长按会显示系统粘贴板的内容
    this.enableInteractiveSelection,
    // 点击事件
    this.onTap,
    this.buildCounter,
  })
</code></pre>
<p>接下来着重介绍 TextField 的几个属性。</p>
<ul>
<li><strong>InputDecoration</strong></li>
</ul>
<p>我们看下 InputDecoration 的构造方法：</p>
<pre><code class="dart language-dart">const InputDecoration({
    //左侧显示的图标
    this.icon,
    // 输入框顶部提示信息
    this.labelText,
    // 提示信息样式
    this.labelStyle,
    // 输入框底部提示信息
    this.helperText,
    this.helperStyle,
    // 输入框内提示信息
    this.hintText,
    this.hintStyle,
    this.hintMaxLines,
    // 输入框底部错误提示信息
    this.errorText,
    this.errorStyle,
    this.errorMaxLines,
    this.hasFloatingPlaceholder = true,
    this.isDense,
    // 输入内容边距
    this.contentPadding,
    // 输入框内部左侧图标
    this.prefixIcon,
    // 输入框内部左侧自定义提示Widget
    this.prefix,
    // 输入框内部左侧提示文本
    this.prefixText,
    this.prefixStyle,
    // 输入框内部后缀图标
    this.suffixIcon,
    this.suffix,
    this.suffixText,
    this.suffixStyle,
    // 输入框右下角字数统计信息
    this.counter,
    this.counterText,
    this.counterStyle,
    // 是否填充颜色
    this.filled,
    // 输入框填充颜色
    this.fillColor,
    this.errorBorder,
    this.focusedBorder,
    this.focusedErrorBorder,
    this.disabledBorder,
    this.enabledBorder,
    // 输入框边框样式
    this.border,
    this.enabled = true,
    this.semanticCounterText,
    this.alignLabelWithHint,
  })
</code></pre>
<p>通过 InputDecoration 我们可以个性化定制和配置我们的 TextField，是不是很强大，很方便？</p>
<ul>
<li><strong>TextInputType</strong></li>
</ul>
<p>用来控制我们的输入内容类型：text、multiline（多行文本）、number、phone、datetime、emailAddress、url，其中 number 还可以详细设置为 signed 或 decimal，这些输入类型和其他平台基本一样。</p>
<ul>
<li><strong>controller</strong></li>
</ul>
<p>这里使用的是 TextEditingController，一般用于获取输入框值、输入框清空、选择、监听等操作的作用：</p>
<pre><code class="dart language-dart">TextEditingController _controller= TextEditingController();
// 监听文本变化
_controller.addListener(() {
      print('input ${_controller.text}');
    });
// 或者用onChange属性也可以监听文本变化
onChanged: (text) {
      print("onChange: $text");
    }

// 在任何时候想获取输入框文本内容就直接调用：_controller.text
//设置默认值
_controller.text="我在学习Flutter!";
// 设置文本选中，下面这句代码设置从第三个字符到最后一个字符选中
_controller.selection=TextSelection(
        baseOffset: 3,
    extentOffset: _controller.text.length
    );
</code></pre>
<ul>
<li><strong>focusNode</strong></li>
</ul>
<p>focusNode 用于控制输入框焦点，如我们点击回车时候，让某个输入框获取焦点等类似操作或者监听焦点变化。</p>
<pre><code class="dart language-dart">FocusNode focusNode1 = new FocusNode();
FocusScopeNode focusScopeNode;

...

// 实例化FocusScopeNode
focusScopeNode = FocusScope.of(context);

...

TextField(
    focusNode: focusNode1,
),

...

// 操作焦点
focusScopeNode.requestFocus(focusNode1);

focusScopeNode.autofocus(focusNode1);
</code></pre>
<p>那么接下来看一下最基本的 TextField 的用法：</p>
<pre><code class="dart language-dart">TextField(
    decoration: InputDecoration(
        hintText: "输入用户名",
        icon: Icon(Icons.person)
    ),
)
</code></pre>
<p><img src="https://images.gitbook.cn/FubctQJEY-jOiR3cI7cDpO28okpM" alt="TextField" /></p>
<p>是不是很简单？</p>
<p>接下来我们写一个简单的登录页面，代码如下：</p>
<pre><code class="dart language-dart">@override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('TextField Widget'), primary: true),
      body: Column(
        children: &lt;Widget&gt;[
          Padding(
              padding: EdgeInsets.all(10),
              child: TextField(
                maxLines: 1,
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(5.0)),
                        borderSide: BorderSide(color: Colors.grey)),
                    labelText: '用户名',
                    hintText: "输入用户名",
                    icon: Icon(Icons.email)),
              )),
          Padding(
              padding: EdgeInsets.all(10),
              child: TextField(
                textInputAction: TextInputAction.done,
                maxLines: 1,
                keyboardType: TextInputType.text,
                obscureText: true,
                decoration: InputDecoration(
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(5.0)),
                        borderSide: BorderSide(color: Colors.grey)),
                    labelText: '密码',
                    hintText: "输入密码",
                    icon: Icon(Icons.lock)),
              )),
        ],
      ),
    );
  }
</code></pre>
<p>运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/Fq6AVMukAgRG9btlr1PwtIwgnaSb" alt="TextField" /></p>
<h3 id="2formwidget">2 Form 表单 Widget 用法详解</h3>
<p>Form 和 HTML 里的 Form 表单作用和用法基本一致，所以很好理解，主要用于提交一系列表单信息，如注册、登录信息表单的提交等操作。</p>
<p>Form 继承自 StatefulWidget，Form 的里面每一个子元素必须是 FormField 类型。就像我们表单里每一条信息都要用 FormField 包装和管理，所以一般 Form 和 TextFormField 搭配使用。我们分别看下它们的构造方法：</p>
<pre><code class="dart language-dart">const Form({
    Key key,
    // 子元素
    @required this.child,
    // 是否自动校验子元素输入的内容
    this.autovalidate = false,
    // 返回按键处理
    this.onWillPop,
    // Form的任意一个子FormField内容发生变化时触发此回调
    this.onChanged,
  })
</code></pre>
<p>FormField 构造方法：</p>
<pre><code class="dart language-dart">const FormField({
    Key key,
    @required this.builder,
    // 保存回调
    this.onSaved,
    // 验证回调
    this.validator,
    // 初始值
    this.initialValue,
    // 是否自动校验
    this.autovalidate = false,
    // 是否可用
    this.enabled = true,
  })
</code></pre>
<p>TextFormField 构造方法，继承自 FormField：</p>
<pre><code class="dart language-dart">// 大部分属性前面都介绍过
TextFormField({
    Key key,
    this.controller,
    String initialValue,
    FocusNode focusNode,
    InputDecoration decoration = const InputDecoration(),
    TextInputType keyboardType,
    TextCapitalization textCapitalization = TextCapitalization.none,
    TextInputAction textInputAction,
    TextStyle style,
    TextDirection textDirection,
    TextAlign textAlign = TextAlign.start,
    bool autofocus = false,
    bool obscureText = false,
    bool autocorrect = true,
    bool autovalidate = false,
    bool maxLengthEnforced = true,
    int maxLines = 1,
    int maxLength,
    VoidCallback onEditingComplete,
    // 提交数据
    ValueChanged&lt;String&gt; onFieldSubmitted,
    FormFieldSetter&lt;String&gt; onSaved,
    FormFieldValidator&lt;String&gt; validator,
    List&lt;TextInputFormatter&gt; inputFormatters,
    bool enabled = true,
    double cursorWidth = 2.0,
    Radius cursorRadius,
    Color cursorColor,
    Brightness keyboardAppearance,
    EdgeInsets scrollPadding = const EdgeInsets.all(20.0),
    bool enableInteractiveSelection = true,
    InputCounterWidgetBuilder buildCounter,
  })
</code></pre>
<p>那么我们的 Form 和 FormField 是如何管理和通信的呢？答案就是通过 key 和 FormState。</p>
<pre><code class="dart language-dart">GlobalKey&lt;FormState&gt; _formKey = new GlobalKey&lt;FormState&gt;();
FormState _formState;
... 

_formState = _formKey.currentState;

Form(
    key: _formKey,
... 
// 然后通过调用FormState相关方法，就可以它来对Form的子元素FormField进行统一操作。例如：
// 保存
_formState.save();
// 清空重置
_formState.reset();
// 验证
_formState.validate();

// 调用这几个方法后，会调用Form子元素FormField的对应的方法回调，这样就达到了控制和管理操作
</code></pre>
<p>接下来我们看一个实例：</p>
<pre><code class="dart language-dart">class FormSamplesState extends State&lt;FormSamples&gt; {
  GlobalKey&lt;FormState&gt; _formKey = new GlobalKey&lt;FormState&gt;();
  FormState _formState;
  String _name;
  String _password;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Form Widget'), primary: true),
      body: Form(
        key: _formKey,
        child: Column(
          children: &lt;Widget&gt;[
            ///TextFormField主要用于Form表单，TextField是普通输入框
            TextFormField(
              decoration: const InputDecoration(
                  icon: Icon(Icons.person),
                  hintText: '请输入用户名',
                  labelText: '用户名',
                  prefixText: '用户名：'),
              onSaved: (String value) {
                _name = value;
              },
              validator: (String value) {
                return value.contains('@') ? '用户名里不要使用@符号' : null;
              },
            ),
            TextFormField(
              decoration: InputDecoration(
                  labelText: '密码',
                  icon: Icon(Icons.lock),
                  hintText: '请输入用户名',
                  prefixText: '密码：'),
              maxLines: 1,
              maxLength: 32,
              obscureText: true,
              keyboardType: TextInputType.numberWithOptions(),
              validator: (value) {},
              onSaved: (value) {
                _password = value;
              },
              onFieldSubmitted: (value) {},
            ),

            ///被Tooltip包裹的控件长按弹出tips
            Tooltip(
              message: '表单提交',
              child: RaisedButton(
                child: Text('登录'),
                onPressed: () {
                  onSubmit();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void onSubmit() {
    final _formState = _formKey.currentState;
    if (_formState.validate()) {
      _formState.save();
      showDialog&lt;void&gt;(
          context: context,
          barrierDismissible: false,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text("提示"),
              content: Column(
                children: &lt;Widget&gt;[
                  Text(
                    'Name: $_name',
                    style: TextStyle(
                        fontSize: 18, decoration: TextDecoration.none),
                  ),
                  Text(
                    'Password: $_password',
                    style: TextStyle(
                        fontSize: 18, decoration: TextDecoration.none),
                  ),
                ],
              ),
              actions: &lt;Widget&gt;[
                new FlatButton(
                    onPressed: () =&gt; Navigator.of(context).pop(false),
                    child: new Text("取消")),
                new FlatButton(
                    onPressed: () {
                      Navigator.of(context).pop(true);
                    },
                    child: new Text("确定")),
              ],
            );
          });
    }
  }
}
</code></pre>
<p>运行效果如下图：</p>
<p><img src="https://images.gitbook.cn/FsHDG5lQkID2rN9jZ1t-QM-Gcyl0" alt="TextField" /></p>
<p>本节课实例地址：
<a href="https://github.com/jaychou2012/flutter_studys/tree/master/lib/flutter_11">flutter_11</a></p>
<h3 id="">总结</h3>
<p>本节课主要是在讲解了 Flutter 的 TextField、Form 表单 Widget 的用法和特点之后，也扩展了 TextFormField 的相关知识。注意点和建议如下：</p>
<ul>
<li>要注意 TextField 和 TextFormField 的区别和使用场景，自己动手写一个注册页面，并提交显示输入的信息。</li>
</ul>
<hr />
<p>我们为本课程付费读者创建了《Flutter：从入门到实践》的微信交流群，方便读者更有针对性地讨论课程相关问题，以及分享 Flutter 技术。</p>
<p>入群请添加「GitChat 小助手泰勒」：识别下方二维码，或者添加 GitChatty5，注明「Flutter」。</p>
<blockquote>
  <p>温馨提示：需购买才可入群哦，加小助手后需要<strong>截图已购买页面</strong>来发给小助手验证一下~</p>
</blockquote>
<p><img src="https://images.gitbook.cn/FtkDbtI-hx5hlJERoW0MGan1I8Ax" width = "40%" hspace="40" /></p></div></article>