---
title: day_4
---

### 内置函数
- close 主要用来关闭chanel
- len 用来求长度，如string、array、slice、map、chan(channel)
- new 用来分配内存，返回的是指针。主要用来分配值类型，如int、struct
- make 用来分配内存，返回的是值，主要用来分配引用类型，如chan、map、slice
- append 用来追加元素到数组、slice中
    ```go
    var a []int
    a = append(a, 10, 20, 383)  // [10, 20, 383]
    a = append(a, a...)     // [10, 20, 383, 10, 20, 383]
    fmt.Println(a)
    ```
- panic、recover 用来做错误处理
    ```go
    // recover 捕获异常
    defer func() {
        if err := recover(); err != nil {
            fmt.Println(err)
        }
    }()
    ```
    ```go
    // 抛出异常    
    func initConfig() (err error) {
        return errors.New("init config failed")
    }
    err := initConfig()
    if err != nil {
        panic(err)
    }
    ```
    
### new跟make的区别
```go
    func test() {
    
        s1 := new([]int)
        fmt.Println(s1)     // &[]
    
        s2 := make([]int, 10)   
        fmt.Println(s2)     // [0,0,0,0,0,0,0,0,0,0]
        
        // (*s1)[0] = 100   // 会报越界错误，原因是没有初始化长度
        
        *s1 = make([]int, 5)    // 初始化长度
        (*s1)[0] = 100
        s2[0] = 100
        fmt.Println(s1)
        return
    }
```

### 闭包
```go
    package main
    
    import (
        "fmt"
        "strings"
    )
    
    func Adder() func(int) int {
        var x int
        f := func(d int) int {
            x += d
            return x
        }
        return f
    }
    
    func makeSuffix(suffix string) func(string) string {
        f := func(name string) string {
    
            if strings.HasSuffix(name, suffix) == false {
                return name + suffix
            }
            return name
        }
    
        return f
    }
    
    func main() {
        /*
            f := Adder()
            fmt.Println(f(1))   // 1
            fmt.Println(f(100))     // 101
            fmt.Println(f(1000))    // 1101
        */
        f1 := makeSuffix(".bmp")
        fmt.Println(f1("test"))
        fmt.Println(f1("pic"))
    
        f2 := makeSuffix(".jpg")
        fmt.Println(f2("test"))
        fmt.Println(f2("pic"))
    }

```

### 数组
- 是同一种数据类型的固定长度的序列，且长度一旦定义就不能改变
    ```go
    // 初始化数组
    var a0 [5]int = [5]int{1, 2, 3} // int类型默认值为0
    var a1 = [5]int{1, 2, 3}
    var a2 = [...]int{1, 2, 3, 4, 50}
    var s0 = [5]string{3: "hello", 4: "tom"}	// string类型默认值是空字符串
    fmt.Println(a0)
    fmt.Println(a1)
    fmt.Println(a2)
    fmt.Println(s0)
    
    //多维数组
    var age [5][3]int
    var f [2][3]int = [...][3]int{{1,2,3}, {7,8,9}}
    ```

- `var a [5]int` 与 `var a [10]int` 不是同一种类型
- 元素默认初始化为0
- 数组是值类型，改变副本数组的值不会改变原数组的值，需要修改则要传递地址
    ```go
    package main
    
    import "fmt"
    
    func test1() {
        var a [10]int
    
        //j := 10
        a[0] = 100
        //a[j] = 200
    
        fmt.Println(a)
    
        for i := 0; i < len(a); i++ {
            fmt.Println(a[i])
        }
    
        for index, val := range a {
            fmt.Printf("a[%d]=%d\n", index, val)
        }
    }
    
    func test3(arr *[5]int) {
        (*arr)[0] = 1000
    }
    
    func test2() {
        var a [10]int
        b := a
    
        b[0] = 100
        fmt.Println(a)
    }
    
    func main() {
    
        //test1()
        test2()
        var a [5]int
        test3(&a)
        fmt.Println(a)
    }
    
    ```
 - 使用非递归的方式实现斐波那契数列，打印前10个数
     ```go
    func Fib(n int) {
        if n <= 2 {
            n = 2
        }
        //var res [n]int64          // non-constant array bound n
        res := make([]int64, n)	// 实例化动态数组(切片)要使用make
        res[0] = 1
        fmt.Println(res[0])
        res[1] = 1
        fmt.Println(res[0])
        for i := 2; i < n; i++ {
            res[i] = res[i-1] + res[i-2]
            fmt.Println(res[i])
        }
    }
     ```
 
 
 ### slice切片
 - 是数组的一个引用，因此切片是引用类型
 - 切片的长度可以改变，因此切片是一个可变数组
 - cap()用来求得切片的最大容量 0<=len(slice)<=len(array), 其中array是被引用的数组
 - 切片的定义 `var 变量名 []类型` 和数组定义区别于不指定数组长度
 - 可以使用make来创建切片
 - 可以使用append函数操作切片
 - 切片扩容，在原切片容量不够的时候，会额外开辟一片有足够容量的内存，将原切片的数据拷贝进来
     ```go
     func testSlice() {
        var a [5]int = [...]int{1, 2, 3, 4, 5}
        s := a[1:]
        fmt.Printf("before len[%d] cap[%d]\n", len(s), cap(s))
        s[1] = 100
        fmt.Printf("s=%p a[1]=%p\n", s, &a[1])
        fmt.Println("before a:", a)
    
        s = append(s, 10)
        s = append(s, 10)
        fmt.Printf("after len[%d] cap[%d]\n", len(s), cap(s))
        s = append(s, 10)
        s = append(s, 10)
        s = append(s, 10)
    
        s[1] = 1000
        fmt.Println("after a:", a)
        fmt.Println(s)
        fmt.Printf("s=%p a[1]=%p\n", s, &a[1])
    }
     ```
 - 拷贝copy()
     ```go
     func testCopy() {
    
        var a []int = []int{1, 2, 3, 4, 5, 6}
        b := make([]int, 1)
    
        copy(b, a)
    
        fmt.Println(b)
    }
     ```
 - string的修改要使用rune()来转换而不是使用[]byte(), 否则不能很好地处理中文字符串
     ```go
     func testModifyString() {
        s := "我hello world"
        s1 := []rune(s)
    
        s1[0] = 200
        s1[1] = 128
        s1[2] = 64
        str := string(s1)
        fmt.Println(str)
    }
     ```
     
 ### 排序与查找
 - 排序
     ```go
     func SortCase(){
        var a  = [...]int{1,2,58,88,4}
        sort.Ints(a[:])
        fmt.Println(a)
    }
     ```
 - 查找，二分查找, 如果是对无序数组进行查找则会先对数组进行排序
     ```go
     func SearchCase(){
        var a  = [...]int{1,2,58,88,4}
        sort.Ints(a[:])
        index := sort.SearchInts(a[:], 88)
        fmt.Println(index)
    }
     ```
     
     
### map(字典)
- key-value的数据结构，又叫字典或关联数组
- 声明, 不会分配内存，初始化需要make。`var mapCase map[keyType][valueType]`
    ```go
    package main
    
    import "fmt"
    
    // 插入和更新
    func testMap() {
        var a map[string]string = map[string]string{
            "key": "value",
        }
        //a := make(map[string]string, 10)
        
        a["abc"] = "efg"
        a["abc"] = "efg"
        a["abc1"] = "efg"
    
        fmt.Println(a)
    }

    // 二维map
    func testMap2() {
    
        a := make(map[string]map[string]string, 100)
        a["key1"] = make(map[string]string)
        a["key1"]["key2"] = "abc"
        a["key1"]["key3"] = "abc"
        a["key1"]["key4"] = "abc"
        a["key1"]["key5"] = "abc"
        fmt.Println(a)
    
    }

    // 查找
    func modify(a map[string]map[string]string) {
        _, ok := a["zhangsan"]
        if !ok {
            a["zhangsan"] = make(map[string]string)
        }
    
        a["zhangsan"]["passwd"] = "123456"
        a["zhangsan"]["nickname"] = "pangpang"
    
        return
    }

    
    func testMap3() {
    
        a := make(map[string]map[string]string, 100)
    
        modify(a)
    
        fmt.Println(a)
    }
    
    // 遍历
    func trans(a map[string]map[string]string) {
        for k, v := range a {
            fmt.Println(k)
            for k1, v1 := range v {
                fmt.Println("\t", k1, v1)
            }
        }
    }
    
    // 删除
    func testMap4() {
    
        a := make(map[string]map[string]string, 100)
        a["key1"] = make(map[string]string)
        a["key1"]["key2"] = "abc"
        a["key1"]["key3"] = "abc"
        a["key1"]["key4"] = "abc"
        a["key1"]["key5"] = "abc"
    
        a["key2"] = make(map[string]string)
        a["key2"]["key2"] = "abc"
        a["key2"]["key3"] = "abc"
    
        trans(a)
        delete(a, "key1")
        fmt.Println()
        trans(a)
    
        fmt.Println(len(a))
    }
    
    func testMap5() {
        var a []map[int]int
        a = make([]map[int]int, 5)
    
        if a[0] == nil {
            a[0] = make(map[int]int)
        }
        a[0][10] = 10
        fmt.Println(a)
    }
    
    func main() {
        //testMap()
        //testMap2()
        //testMap3()
        //testMap4()
        testMap5()
    }
    ```
- map排序，go未提供直接用于map排序的方法
    
    排序思路，先获取所有的key，对key进行排序，然后根据排好序的key进行遍历
    ```go
    package main
    
    import (
        "fmt"
        "sort"
    )
    
    // 排序
    func testMapSort() {
        var a map[int]int
        a = make(map[int]int, 5)
    
        a[8] = 10
        a[3] = 10
        a[2] = 10
        a[1] = 10
        a[18] = 10
    
        var keys []int
        for k, _ := range a {
            keys = append(keys, k)
            //fmt.Println(k, v)
        }
    
        sort.Ints(keys)
    
        for _, v := range keys {
            fmt.Println(v, a[v])
        }
    }
    
    // 反转
    func testMapReverse() {
        var a map[string]int
        var b map[int]string
    
        a = make(map[string]int, 5)
        b = make(map[int]string, 5)
    
        a["abc"] = 101
        a["efg"] = 10
    
        for k, v := range a {
            b[v] = k
        }
    
        fmt.Println(b)
    }
    
    func main() {
        testMapSort()
        testMapReverse()
    }
    ```

### 线程同步
- sync包
- 互斥锁 `var mu sync.Mutex`
- 读写锁 `var mu snyc.RWMutex`, 适用于读多写少的应用场景
- 原子操作 atomic
    ```go
    package main
    
    import (
        "fmt"
        "math/rand"
        "sync"
        "sync/atomic"
        "time"
    )
    
    var lock sync.Mutex
    var rwLock sync.RWMutex
    
    func testRWLock() {
        var a map[int]int
        a = make(map[int]int, 5)
        var count int32
        a[8] = 10
        a[3] = 10
        a[2] = 10
        a[1] = 10
        a[18] = 10
    
        for i := 0; i < 2; i++ {
            go func(b map[int]int) {
                //rwLock.Lock() // 读写锁
                lock.Lock()  // 互斥锁
                b[8] = rand.Intn(100)
                time.Sleep(10 * time.Millisecond)
                lock.Unlock()
                //rwLock.Unlock()
            }(a)
        }
    
        for i := 0; i < 100; i++ {
            go func(b map[int]int) {
                for {
                    lock.Lock()	
                    //rwLock.RLock()
                    time.Sleep(time.Millisecond)
                    //fmt.Println(a)
                    //rwLock.RUnlock()
                    lock.Unlock()
                    atomic.AddInt32(&count, 1)
                }
            }(a)
        }
        time.Sleep(time.Second * 3)
        fmt.Println(atomic.LoadInt32(&count))
    }
    
    func main() {
        testRWLock()
    }
    
    ```

### 使用 go get 安装三方包
