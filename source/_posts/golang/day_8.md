---
title: day_8
---

### MPG
- M 进程
- P 运行的上下文
- G go routine


### 设置Golang运行的CPU核数
- 1.8以上默认设置了使用多核
- runtime.GOMAXPROCS()设置多核

### go routine通信
- 全局变量与锁同步, 读多写少使用读写锁，写多读少使用互斥锁
- channel

### channel
- 默认情况下管道是阻塞的，即管道容量满了就不支持数据继续写入
- 使用channel进行通信，使用channel进行同步
- 只读 <-chan; 只写 chan<-
- 使用select解决阻塞的问题


### time
- time.After() 超时控制