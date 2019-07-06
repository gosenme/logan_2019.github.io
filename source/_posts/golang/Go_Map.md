---
title: Go Map
---

### go map 判断值存在
- KeyExist
    ```go
    func KeyExist() {
        m := map[string]int{
            "a": 0,
        }
        ma, oka := m["a"]
        mb, okb := m["b"]
        if ma == mb {
            fmt.Println("键`a`存在于map`m`中", oka)
            fmt.Println("键`b`存在于map`m`中", okb)
        }
    }
    ```
- 键`a`存在于map`m`中 true
- 键`b`存在于map`m`中 false

### go map 实现set
- RealizeSet
    ```go
    func RealizeSet() {
    
        mySet := map[interface{}]bool{
            "a": true,
        }
        k := "a"
        if mySet[k] {
            fmt.Println(k, " is existing")
        } else {
            fmt.Println(k, " is not existing")
        }
    
    }
    ```
- len(mySet)求长度
- delete(mySet,key)


### 使用map实现工厂模式
```go
func G() {

	factory := map[string]func(op int) int{
		"a": func(op int) int {
			return op
		},
		"b": func(op int) int {
			return op * op
		},
		"c": func(op int) int {
			return op * op * op
		},
	}

	fmt.Println(factory["a"](10))
	fmt.Println(factory["b"](10))
	fmt.Println(factory["c"](10))
}
```