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