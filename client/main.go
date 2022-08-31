package main

import (
	"context"
	"fmt"
	pb "gostock/api/stock/v1"

	"github.com/go-kratos/kratos/v2/errors"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	transgrpc "github.com/go-kratos/kratos/v2/transport/grpc"
)

func main() {
	conn, err := transgrpc.DialInsecure(
		context.Background(),
		transgrpc.WithEndpoint("127.0.0.1:9000"),
		transgrpc.WithMiddleware(
			recovery.Recovery(),
		),
	)
	if err != nil {
		panic(err)
	}
	defer conn.Close()
	client := pb.NewStockInfoServiceClient(conn)
	reply, err := client.GetStockInfo(context.Background(), &pb.GetStockInfoRequest{Id: 1})
	if err != nil {
		fmt.Printf("%T, %#v\n", err, err)
		trans_error := errors.FromError(err)
		fmt.Printf("%T, %#v\n", trans_error, trans_error)
	}
	fmt.Println(reply)
}
