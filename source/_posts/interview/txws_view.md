---
title: 腾讯微视面试 
---


## 程序设计部分
### 算法
- 找出一个有序列表中两个不同数所得和等于目标值

    1. 转为二分查，n*log(n)
    2. 左右指针 log(n)
    
- n!
    
        动归+大数相乘

- 判断链表是否成环
    
        使用快慢指针，能否相遇

- 查找链表的倒数第K个元素
        
        使用快慢指针，快K步，在快指针到达尾部(None)时，慢指针即为所得
        

### 程序设计 交替打印
```go
package main

import "fmt"

func main() {

	aString := "abcdefg"
	iString := "1234567"

	UserPrint(aString, iString)
}

func UserPrint(a string, b string)  {

	for i:=0; i<len(a); i++ {
		fmt.Print(string(a[i]))
		fmt.Print(b[i] - '0')
	}
}
```
    
## 操作系统
- Linux内存管理
- 进程和线程
- 进程通信
- 协程

## 中间件
- Redis
- MySQL

## 数据结构
- [跳表](https://www.jianshu.com/p/dd01e8dc4d1f)
- B+树

## 通信协议
- HTTP头部信息
- TCP拥塞
- TCP四次挥手

## 其他
- go channel实现原理