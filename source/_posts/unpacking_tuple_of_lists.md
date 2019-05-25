---
title: unpacking tuple of list
---

[原文地址](https://www.geeksforgeeks.org/python-unpacking-tuple-of-lists/)

第四种方法
```python
def unpack_tuple(tups):
    res = list()
    for lst in tups:
        res.extend(lst)
    return res
```