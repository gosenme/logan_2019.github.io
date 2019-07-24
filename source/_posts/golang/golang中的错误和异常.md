---
title: Go错误和异常
---

在Go中需要正确理解与处理错误和异常

### 在函数或方法返回的参数列表中，最后一个参数用来返回错误信息(如果有错误信息的话)
```go
func ReadAtLeast(r Reader, buf []byte, min int) (n int, err error)
```

### 将错误信息集中声明
```go
var ErrShortWrite = errors.New("short write")
var ErrShortBuffer = errors.New("short buffer")
var EOF = errors.New("EOF")
var ErrUnexpectedEOF = errors.New("unexpected EOF")
var ErrNoProgress = errors.New("multiple Read calls return no data or error")
```
- 在一个包中尽量使用且只使用一个包保存错误信息对象，且建议命名以Err开头

### 不是每个错误都需要返回错误信息
- 在一些有关建立连接的函数，在有重试机制下，可以在函数中规定达到重试上限未成功才返回错误信息，而不是出现错误就返回

### 不可能出现的情况可以用panic()主动抛出异常
```go
var t = "go"

switch t {
case "go42":
    fmt.Println("Ok")
default:
    panic("No")
}
```

### 不要轻易抛出异常
- 在包内部，应该用`recover()`对运行时异常进行捕获，同时函数向调用者要尽量返回错误值，而不是直接发出异常。

