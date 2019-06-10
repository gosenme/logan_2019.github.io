---
title: start
---

### 编写Golang
- package 如果是编写可执行文件包名必须是 main, 如果是编写可被调用的包(库)可以自定义名字
- main函数 代码执行入口
- 使用import导包
- 函数规范 花括号
- 函数类型在变量的后面，使用"var"或者":="来定义变量

### 语言特性
- 垃圾回收
    内存自动回收，无需管理内存，开发人员可以专注业务实现
- 天然并发
    语言层面支持并发，基于CSP模型实现，可以创建很多的goroute(轻量级线程，协程)
- channel管道
    类型unix/linux中的pipe, 多个goroute之间通过channel进行通信
    支持任何类型  
- 函数支持多值返回
    一个函数可以返回多个指

### 执行
- 在同一个包下的文件相互调用
    
    比如在hello中调用test的goroute_test函数执行go run hello.go会发生错误
    
    # command-line-arguments
    
    ./hello.go:13:5: undefined: goroute_test
    
    原因是在运行的时候go没有去编译test.go导致无法调用test文件中的函数
    正常执行命令为`go run test.go hello.go`

### 注意
    不建议在文件中定义全局变量用于其他文件函数中完成变量共享
    应该使用参数传递的方式进行共享
    
### 包
- 把相同功能的代码放到同一个目录，称之为包
- 包可以被其他包引用
- main包是用来生成可执行文件的，每个程序只有一个main包
- 包的主要用途是提高代码的可复用性
- 从包中向外开放的函数必须要以大写开头