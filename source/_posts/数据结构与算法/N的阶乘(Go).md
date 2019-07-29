---
title: N的阶乘(Go)
---

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	f := factorial(5)
	fmt.Println(f)
}

func factorial(n int) string {

	tmp := []string{"1",}
	for i := 1; i <= n; i++ {
		fmt.Println(i)
		tmp = append(tmp, mulBigData(tmp[i-1], strconv.Itoa(i)))
	}
	fmt.Println(tmp)
	return tmp[n]
}

func mulBigData(a, b string) (s string) {
	lengthA := len(a)
	lengthB := len(b)
	L := lengthA + lengthB
	tmp := make([]int, L)
	//fmt.Println(tmp)

	ra := ""
	for i := 0; i < lengthA; i++ {
		ra += string(a[lengthA-1-i])
	}
	rb := ""
	for i := 0; i < lengthB; i++ {
		rb += string(b[lengthB-1-i])
	}

	for i := 0; i < lengthA; i++ {
		for j := 0; j < lengthB; j++ {
			tmp[i+j] += int(ra[i]-'0') * int(rb[j]-'0')
		}
	}

	//进位
	k := 0
	ts := ""
	for k < L-1 {
		ts += strconv.Itoa(tmp[k] % 10)
		tmp[k+1] += tmp[k] / 10
		k += 1
	}
	if tmp[L-1] > 0 {
		ts += strconv.Itoa(tmp[L-1])
	}
	s = ""
	lts := len(ts)
	for h := 0; h < lts; h++ {
		s += string(ts[lts-1-h])
	}

	return
}

```