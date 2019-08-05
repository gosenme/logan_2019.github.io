---
title: Go链表队列的实现
---

```go
package main

import "fmt"

func main() {
	hd := NewQueueNode()
	fmt.Println("L", hd.Length())
	for i := 0; i < 10; i++ {
		hd.EnQueue(i)
	}
	fmt.Println(hd.Length())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println("L", hd.Length())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println(hd.DeQueue())
	fmt.Println("L", hd.Length())
}

type Node struct {
	pNext *Node
	data  interface{}
}

type QueueNode struct {
	front *Node
	rear  *Node
}

type LinkQueue interface {
	Length() int
	EnQueue(data interface{})
	DeQueue() interface{}
}

func NewQueueNode() *QueueNode {
	return &QueueNode{}
}

func (self *QueueNode) EnQueue(data interface{}) {
	nn := &Node{data: data}
	// 队列为空时
	if self.front == nil {
		self.front = nn
		self.rear = nn
	} else {
		self.rear.pNext = nn
		self.rear = self.rear.pNext
	}
}

func (self *QueueNode) DeQueue() interface{} {
	// 队列为空
	if self.front == nil {
		return nil
	}
	// 头节点 值
	res := self.front.data

	if self.front == self.rear {
		// 只剩下一个时
		self.front = nil
		self.rear = nil
	} else {
		// 将头指针右移
		self.front = self.front.pNext
	}
	return res
}

func (self *QueueNode) Length() int {
	if self.front == nil{
		return 0
	}
	c := 1
	nd := self.front
	for nd.pNext != nil {
		c++
		nd = nd.pNext
	}
	return c
}

```