---
title: 排序
---

### 冒泡排序

    func Bsort(a []int) {
        c := 1
        for i := 0; i < len(a)-1; i++ {
            for j := 1; j < len(a)-i; j++ {
                c ++
                if a[j-1] > a[j] {
                    a[j-1], a[j] = a[j], a[j-1]
                }
            }
        }
        fmt.Println(c)
    }

    
### 选择排序

    func Ssort(a []int) {
        c := 1
        for i := 0; i < len(a)-1; i++ {
            for j := i + 1; j < len(a); j++ {
                c ++
                if a[i] > a[j] {
                    a[i], a[j] = a[j], a[i]
                }
            }
        }
        fmt.Println(c)
    }

    
### 插入排序
    
    func Isort(a []int)  {
        // 4,8,5,2,1,9
        // 4 | 8 5 2 1 9
        // 4 8 | 5 2 1 9
        // 4 5 8 | 2 1 9
        for i:=1; i < len(a); i++ {
            for j := i; j>=0; j-- {
                //if a[j-1] < a[j]{
                if a[j] > a[j-1]{
                    break
                }
                a[j-1], a[j] = a[j], a[j-1]
            }
        }
    }


### 快速排序
