---
title: day_5
---

### 结构体
- 用来自定义复杂的数据结构
- struct里面可以包含多个字段
- struct类型可以定义方法，与函数不同
- struct类型是值类型
- struct类型可以被嵌套
- Golang没有class类型

### 定义struct
```go
type YourStructName struct{
    YourName string
    YourAge  int
}
```

### 访问struct 使用`.`
```go
var stu Student

stu.Name = "tony”
stu.Age = 18
stu.Score=20

fmt.Printf("name=%s age=%d score=%d”, 
            stu.Name, stu.Age, stu.Score)

```

### 链表
```go
package main

import (
	"fmt"
	"math/rand"
)

type Student struct {
    Name  string
    Age   int
    Score float32
    next  *Student
}

func trans(p *Student) {
    for p != nil {
        fmt.Println(*p)
        p = p.next
    }
    
    fmt.Println()
}

func insertTail(p *Student) {
    var tail = p
    for i := 0; i < 10; i++ {
        stu := Student{
            Name:  fmt.Sprintf("stu%d", i),
            Age:   rand.Intn(100),
            Score: rand.Float32() * 100,
        }
    
        tail.next = &stu
        tail = &stu
    }
}

func insertHead(p **Student) {
    //var tail = p
    for i := 0; i < 10; i++ {
        stu := Student{
            Name:  fmt.Sprintf("stu%d", i),
            Age:   rand.Intn(100),
            Score: rand.Float32() * 100,
        }
    
        stu.next = *p
        *p = &stu
    }
}

func delNode(p *Student) {

    var prev *Student = p
    for p != nil {
        if p.Name == "stu6" {
            prev.next = p.next
            break
        }
        prev = p
        p = p.next
    }
}

func addNode(p *Student, newNode *Student) {

    for p != nil {
        if p.Name == "stu9" {
            newNode.next = p.next
            p.next = newNode
            break
        }
    
        p = p.next
    }
}

func main() {
    var head *Student = new(Student)
    
    head.Name = "hua"
    head.Age = 18
    head.Score = 100
    
    //insertTail(head)
    //trans(head)
    insertHead(&head)
    trans(head)
    
    delNode(head)
    trans(head)
    
    var newNode *Student = new(Student)
    
    newNode.Name = "stu1000"
    newNode.Age = 18
    newNode.Score = 100
    addNode(head, newNode)
    trans(head)
}

```

### 二叉树
- `前序遍历` 根 -> 左 -> 右 
- `中序遍历` 左 -> 根 -> 右 
- `后序遍历` 左 -> 右 -> 根
- 左节点在右节点前，根的位置决定了遍历模式
```go
func TreePrint(x *TreeCase) {

    if x == nil {
        return
    }
    
    fmt.Println(x.Val) // 在前面为前序遍历
    TreePrint(x.Left)
    // fmt.Println(x.Val) // 中序遍历
    TreePrint(x.Right)
    // fmt.Println(x.Val) // 后序遍历
}
```

### Type
- Type出来的类型尽管字段都一样但是是不同的类型
- Type用于自定义类型

### struct中的tag
- 在struct的每个字段 如`Age int "this is age field"`
- 常被用于json序列化和反序列化
    ```go
    package main
    
    import (
        "encoding/json"
        "fmt"
    )
    
    type Student struct {
        Name  string `json:"student_name"`     // 取别名
        Age   int    `json:"age"`
        Score int    `json:"score"`
    }
    
    func main() {
        var stu Student = Student{
            Name:  "stu01",
            Age:   18,
            Score: 80,
        }
        
        data, err := json.Marshal(stu)
        if err != nil {
            fmt.Println("json encode stu failed, err:", err)
            return
        }
        
        fmt.Println(string(data))
    }
    ```
### 匿名字段
- 结构体中的字段可以只有类型，没有名字，即匿名字段
    ```go
    type Cart1 struct {
        name string
        age  int
    }
    
    type Cart2 struct {
        name string
        age  int
    }
    
    type Train struct {
        Cart1   // 匿名字段
        Cart2
    }
    ```
- 访问匿名字段，通过访问匿名字段的类型来访问
    ```go
    var t Train
    
    t.Cart1.name = "train"  // 匿名字段产生冲突，通过类型访问
    t.Cart1.age = 100
    
    fmt.Println(t)
    ```

### 方法
- Golang中的方法是作用在特定类型的变量上
- 定义 `func (recevier type) methodName (参数列表)(返回值列表) {}`
    ```go
    type Student struct {
        Name  string
        Age   int
        Score int
        sex   int
    }
    
    func (p *Student) init(name string, age int, score int) {
        p.Name = name
        p.Age = age
        p.Score = score
        fmt.Println(p)
    }
    ```

### 继承
- 通过 匿名字段来继承


### 组合
- 一个结构体嵌套到另一个结构体

### 接口
- String()接口的实现，通过遵循规范来进行调用
- Interface类型可以定义一组方法，但是这些方法不需要实现，并且Interface不能包含任何变量
- 多态