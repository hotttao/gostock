package main

import (
	context "context"
	"fmt"

	"go_app/helloworld"

	http "github.com/go-kratos/kratos/v2/transport/http"
)

func main() {
	conn, err := http.NewClient(
		context.Background(),
		http.WithEndpoint("192.168.2.70:8001"),
	)
	if err != nil {
		return
	}

	greeter_client := helloworld.NewGreeterHTTPClient(conn)
	req := &helloworld.MultiRequest{
		Name: "tsong",
		Inner: &helloworld.Inner{
			InnerName: "inner_tsong",
			InnerId:   1,
		},
		Nums:     []int32{1, 2},
		Metadata: map[string]string{"path": "/about", "detail": "sky"},
		IsTrue:   true,
	}
	reply, err := greeter_client.SayMulti(context.Background(), req)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("%v", reply)
}
