---
title: rpcx 用例
---

### example
```go
package example

import "context"

type Args struct {
	A int
	B int
}

type Reply struct {
	C int
}

type Arith int

func (t *Arith) Mul(ctx context.Context, args *Args, reply *Reply) error {
	reply.C = args.A * args.B
	return nil
}

```

### server
```go
package main

import (
	"github.com/smallnest/rpcx/server"
	"rpcx-case/example"
)


func main() {
	s := server.NewServer()
	s.RegisterName("Arith", new(example.Arith), "")
	s.Serve("tcp", ":8972")
}

```

### client
```go
package main

import (
	"context"
	"github.com/smallnest/rpcx/client"
	"log"
	"rpcx-case/example"
)

func main() {

	addr := "127.0.0.1:8972"
	// #1
	d := client.NewPeer2PeerDiscovery("tcp@"+addr, "")
	// #2
	xclient := client.NewXClient("Arith", client.Failtry, client.RandomSelect, d, client.DefaultOption)
	defer xclient.Close()

	// #3
	args := &example.Args{
		A: 10,
		B: 20,
	}

	// #4
	reply := &example.Reply{}

	// #5
	err := xclient.Call(context.Background(), "Mul", args, reply)
	if err != nil {
		log.Fatalf("failed to call: %v", err)
	}

	log.Printf("%d * %d = %d", args.A, args.B, reply.C)
}

```