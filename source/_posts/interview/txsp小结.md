---
title: txsp笔试小结
---

### defer和panic
```go
package main

import "fmt"

func main() {
	defer_call()
}

// defer 栈 未进行 recover时 由于 panic与defer争夺资源造成 panic顺序异常
func defer_call() {
	defer func() { fmt.Println("打印前") }()
	defer func() { fmt.Println("打印中") }()
	defer func() { fmt.Println("打印后") }()
	panic("触发异常")
}

```

### 微服务 服务发现 负载均衡
- 我的回答
    - 服务发现，借助etcd
    - 负载均衡，算法，服务器，DNS
- [参考](https://studygolang.com/articles/13009?fr=sidebar)

### go 垃圾回收机制 及注意要点 
- 我的回答 不太了解
    - LRU
    - 全局变量和静态变量常驻内存，需合理使用
    
### 算法
- 两有序数组求中位数，时间复杂度为O(log(m+n)) `leetcode T4`
- 无向图判断有无环
- 最长上升子序列 `T300`