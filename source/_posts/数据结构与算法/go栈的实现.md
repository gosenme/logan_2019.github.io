---
title: go栈的实现
---

```go
type StackArray interface {
	Size() int
	Push(data interface{}) error
	Pop() (interface{}, error)
	IsFull() bool
	IsEmpty() bool
	Clear()
}

type Stack struct {
	DataScore   []interface{}
	CapSize     int //最大使用范围
	CurrentSize int // 实际使用范围
}

func NewStack(capSize int) *Stack {
	stk := new(Stack)
	stk.DataScore = make([]interface{}, 0, capSize)
	stk.CapSize = capSize
	stk.CurrentSize = 0
	return stk
}

func (self *Stack) Clear() {
	self.DataScore = make([]interface{}, 0, 10)
	self.CurrentSize = 0
	self.CapSize = 10
}

func (self *Stack) Size() int {
	return self.CurrentSize
}

func (self *Stack) IsFull() bool {
	return self.CurrentSize >= self.CapSize
}

func (self *Stack) IsEmpty() bool {
	return self.CurrentSize == 0
}

func (self *Stack) Pop() (interface{}, error) {
	if self.IsEmpty() {
		return nil, errors.New("栈为空")
	}
	data := self.DataScore[self.CurrentSize-1]
	self.DataScore = self.DataScore[:self.CurrentSize-1]
	self.CurrentSize --
	return data, nil
}

func (self *Stack) Push(data interface{}) error {
	if self.IsFull() {
		return errors.New("栈溢出")
	}
	self.DataScore = append(self.DataScore, data)
	self.CurrentSize ++
	return nil
}

```