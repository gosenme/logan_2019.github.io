---
title: gin项目开发
---

## go mod
- export GO111MODULE=on
- go mod init gin-case  初始化

## makefile
- vim makefile
- 输入内容
    ```makefile
    dev:
        go run main.go
    ```
- make dev 

## gin
- go get -u github.com/gin-gonic/gin
- 需要解决问题，拟 挂代理 
    ```go
    go: golang.org/x/net@v0.0.0-20190503192946-f4e77d36d62c: unrecognized import path "golang.org/x/net" (https fetch: Get https://golang.org/x/net?go-get=1: net/http: TLS handshake timeout)
    go: golang.org/x/sys@v0.0.0-20190222072716-a9d3bda3a223: unrecognized import path "golang.org/x/sys" (https fetch: Get https://golang.org/x/sys?go-get=1: net/http: TLS handshake timeout)
    go get: error loading module requirements
    ```
    - `export GOPROXY=https://mirrors.aliyun.com/goproxy/`

## init
- export GO111MODULE=on 打开go mod
- export GOPROXY=https://mirrors.aliyun.com/goproxy/ 设置代理    
- go mod tidy 手动处理依赖关系
- go mod vendor 生成vendor目录
