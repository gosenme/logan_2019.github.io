---
title: N的阶乘
---


### 代码
```python
def mul_big_num(a: str, b: str):
    ar = [int(i) for i in reversed(a)]
    br = [int(i) for i in reversed(b)]

    tmp = [0] * (len(a) + len(b))
    for i, ai in enumerate(ar):
        for j, bj in enumerate(br):
            tmp[i + j] += ai * bj

    # 进位
    s = ''
    index = 0
    while index < len(tmp) - 1:
        tmp[index + 1] += tmp[index] // 10
        tmp[index] = tmp[index] % 10
        s += str(tmp[index])
        index += 1
    s += str(tmp[-1])
    s = s[::-1]
    if s[0] == '0':
        s = s[1:]
    return s


def factorial(n):
    a = [1]
    for x in range(1, n + 1):
        a.append(mul_big_num(str(a[-1]), str(x)))
    return a[-1]

```

### 验证
```python
def test(n):                                           
    if n > 15:                                         
        raise Exception("验证数过大")                       
    a = [1]                                            
    for x in range(1, n + 1):                          
        a.append(a[-1] * x)                            
    return a[-1]                                       
    
    
print(int(factorial(5)) == test(5) and int(factorial(15)) == test(15))
# True 
```