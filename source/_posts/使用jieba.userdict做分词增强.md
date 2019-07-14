---
title: 使用jieba.userdict做分词增强
---

### 使用
```python
@decorator_load_user_room_keys()
@add_filter()
def room_cut_words(text):
    return [w for w in jieba.cut(text) if not is_none_or_null(w)]

```


### @decorator_load_user_room_keys()的实现
```python
from functools import wraps

import jieba

State = False  # 变动状态

# 选择通过读文件方式
def decorator_load_user_room_keys():
    def decorator(func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            path = kwargs.get("path") or 'test_load.txt'
            # print(path)

            # 如果变动，则更新
            if State:
                upd_user_room_file(path)
                # global State
                # State = False  # 设置 已同步 return
                # print("更新完毕")
            # os.remove("/var/folders/vf/zznd3m1j4tjbs7kt3w8dxg6c0000gn/T/jieba.cache")
            # import jieba
            jieba.load_userdict(path)
            return func(*args, **kwargs)

        return _wraps

    return decorator

```

### upd_user_room_file的实现
```python

def upd_user_room_file(path=None):
    conn.execute("SELECT `room_key_rep` FROM room_keys")
    data_obj = conn.fetchall()
    if path is None:
        path = 'load_user_room_key'

    data_iter = sorted([data["room_key_rep"] for data in data_obj],
                       key=len, reverse=True)

    with open(path, mode='w') as f:
        for data in data_iter:
            f.write(data + '\n')
```

### @add_filter()的实现
```python
from functools import wraps

def add_filter():
    def decorate(func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            text = str_filter_plus(kwargs.get("text") or args[0])
            return func(text)

        return _wrap

    return decorate
```

### str_filter_plus的实现
```python

import re

def str_filter_plus(a_string, character_pairs=None):
    # 字符串`...`后面的数据可以忽略
    a_string = a_string.split('...')[0]

    # 过滤供应商携程拼接的属性
    if SplCtripIdentifier in a_string.lower():
        a_string = SplCtripSplit.join(a_string.split(SplCtripSplit)[:-1])
    if SplCtripIdentifierCN in a_string:
        a_string = SplCtripSplit.join(a_string.split(SplCtripSplit)[:-1])

    # 去掉指定字符之间的字符串
    a_string = remove_strings_between_specified_characters(a_string, character_pairs)

    # 要保留需要的字符
    def before_str_filter(before_string: str) -> str:
        maybe_dict = {
            '|': ' or ',
            ' ': 'oyjx',
            '&': ' and ',
            '/': ' or ',
            "\\": ' or ',
            '(': 'oyjx',
            ')': 'oyjx',
            "（": 'oyjx',
            "）": 'oyjx',
            "-": 'oyjx',
            "_": 'oyjx',
            ',': ' ',
            '，': ' ',
        }
        maybe_map = str.maketrans(maybe_dict)

        # key_list = ['&', '/', '\\', ' ', '-', '(', ')', "（", "）", "_"]
        # for key in key_list:
        #     if key in before_string:
        #         before_string = before_string.replace(key, maybe_dict[key])
        # print(before_string)

        # 使用 str 内置的 translate
        return before_string.translate(maybe_map)

    # 替换回空格字符 ' '， 并将多个空格字符压缩为一个空格字符
    def after_str_filter(after_string: str) -> str:
        after_string = after_string.replace('oyjx', ' ')
        return re.sub(' +', ' ', after_string)

    # step_1, 去掉变音字符
    a_string = dewinize(shave_makes(a_string))

    # step_2, 进行字符保留
    before_string = before_str_filter(a_string.lower())
    # print(string)

    # step_3, 过滤
    return after_str_filter(re.sub('[^\w\u4e00-\u9fff]+', '', before_string)).strip()

```

### dewinize和shave_makes的实现
```python
import unicodedata

# 去掉全部的变音符号
def shave_makes(txt) -> str:
    txt = txt or ''
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)


# 处理西文字符
# BEGIN ASCIIZE
single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",  # <1>
                           """'f"*^<''""---~>""")

multi_map = str.maketrans({  # <2>
    '€': '<euro>',
    '…': '...',
    'Œ': 'OE',
    '™': '(TM)',
    'œ': 'oe',
    '‰': '<per mille>',
    '‡': '**',
})


# 一些常见西文字符转换
def dewinize(txt: str) -> str:
    txt = txt or ''
    """Replace Win1252 symbols with ASCII chars or sequences"""
    return txt.translate(multi_map)  # <4>

```