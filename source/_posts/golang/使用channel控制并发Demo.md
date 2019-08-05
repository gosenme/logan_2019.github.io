---
title: 使用channel控制并发Demo
---

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

var wg sync.WaitGroup

func main() {
	count := 3
	ids := make([]int, 100)
	ch := make(chan int, count)
	wg.Add(len(ids))
	var c int32
	for i, v := range ids{
		ch <- i
		go func(ii, vv int) {
			defer func() {
				<- ch
			}()
			fmt.Println(ii, vv)
			atomic.AddInt32(&c, 1)
			wg.Done()
		}(i, v)
	}

	for i:=0; i<count; i++ {
		ch <- 100
	}
	wg.Wait()
	fmt.Println(c)
}

```