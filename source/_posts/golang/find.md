---
title: 查找
---

```go

func BFind(v int, a []int) (mid int) {
	low := 0
	high := len(a) - 1
	for low < high{
		mid = (low + high) >> 1
		if v == a[mid] {
			return mid
		} else if v > a[mid] {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}
	mid = -1
	return
}


```