---
title: go链表栈的实现
---

```go
package main

import "fmt"

func main() {

	// 虚假链表头
	node0 := NewNode(nil)
	for i := 1; i <= 100; i++ {
		node0.Push(NewNode(i))
		fmt.Println(i)
	}
	//fmt.Println(node0.pNext.pNext.pNext.data)
	//node0.Pop()
	//fmt.Println(node0.pNext.data)
	fmt.Println(node0.IsEmpty())
	fmt.Println(node0.Length())
}

type Node struct {
	data  interface{}
	pNext *Node
}

type LinkStack interface {
	IsEmpty() bool
	Length() int
	Push(data interface{})
	Pop() interface{}
}

func NewNode(data interface{}) *Node {
	return &Node{data: data}
}

// Stack 先进后出
func (self *Node) Push(data interface{}) {
	d := NewNode(data)
	// 在虚假链表头和第一个节点之间插入 新的节点
	d.pNext = self.pNext
	self.pNext = d
}

func (self *Node) Pop() interface{} {
	if self.pNext == nil {
		return nil
	}
	res := self.pNext.data
	self.pNext = self.pNext.pNext
	return res
}

func (self *Node) Length() int {
	// dn 为实际的链表节点
	dn := self.pNext	
	c := 0
	for dn != nil {
		c++
		dn = dn.pNext
	}
	return c
}

func (self *Node) IsEmpty() bool {
	return self.Length() == 0
}

```