---
title: grpc hello world
---

### 依赖安装
- git clone https://github.com/grpc/grpc-go.git $GOPATH/src/google.golang.org/grpc
- git clone git@github.com:googleapis/go-genproto.git $GOPATH/src/google.golang.org/genproto

### 同步器
- helloworld.proto 
```text
syntax = "proto3"; //语法声明

package helloworld; //包名

// Greeter 微服务
service Greeter {
    // Sends a greeting
    rpc SayHello (HelloRequest) returns (HelloReply) {}
    rpc SayHello2 (HelloRequest) returns (HelloReply) {}
}

// HelloRequest 请求数据格式
message HelloRequest {
    string name = 1;
}

// HelloReply 响应数据格式
message HelloReply {
    string message = 1;
}

```
- 使用 gogo/protobuf 编译`protoc --gofast_out=plugins=grpc:. helloworld.proto`

### 服务端
```go
package main

import (
    "context"
    "log"
    "net"
    
    "google.golang.org/grpc"
    pb "google.golang.org/grpc/examples/helloworld/helloworld"
    "google.golang.org/grpc/reflection"
)

const (
    port = ":50051"
)

type server struct{} //服务对象

// SayHello 实现服务的接口 在proto中定义的所有服务都是接口
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
    return &pb.HelloReply{Message: "Hello " + in.Name}, nil
}

func main() {
    lis, err := net.Listen("tcp", port)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    s := grpc.NewServer() //起一个服务
    pb.RegisterGreeterServer(s, &server{})
    // 注册反射服务 这个服务是CLI使用的 跟服务本身没有关系
    reflection.Register(s)
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

### 客户端
```go
package main

import (
    "context"
    "log"
    "os"
    "time"
    
    "google.golang.org/grpc"
    pb "google.golang.org/grpc/examples/helloworld/helloworld"
)

const (
    address     = "localhost:50051"
    defaultName = "world"
)

func main() {
    //建立链接
    conn, err := grpc.Dial(address, grpc.WithInsecure())
    if err != nil {
        log.Fatalf("did not connect: %v", err)
    }
    defer conn.Close()
    c := pb.NewGreeterClient(conn)
    
    // Contact the server and print out its response.
    name := defaultName
    if len(os.Args) > 1 {
        name = os.Args[1]
    }
    // 1秒的上下文
    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()
    r, err := c.SayHello(ctx, &pb.HelloRequest{Name: name})
    if err != nil {
        log.Fatalf("could not greet: %v", err)
    }
    log.Printf("Greeting: %s", r.Message)
}

```