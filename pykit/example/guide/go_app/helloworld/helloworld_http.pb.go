// Code generated by protoc-gen-go-http. DO NOT EDIT.
// versions:
// protoc-gen-go-http v2.2.2

package helloworld

import (
	context "context"
	http "github.com/go-kratos/kratos/v2/transport/http"
	binding "github.com/go-kratos/kratos/v2/transport/http/binding"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the kratos package it is being compiled against.
var _ = new(context.Context)
var _ = binding.EncodeURL

const _ = http.SupportPackageIsVersion1

type GreeterHTTPServer interface {
	Echo(context.Context, *MultiRequest) (*HelloReply, error)
	SayHello(context.Context, *HelloRequest) (*HelloReply, error)
	SayMulti(context.Context, *MultiRequest) (*HelloReply, error)
}

func RegisterGreeterHTTPServer(s *http.Server, srv GreeterHTTPServer) {
	r := s.Route("/")
	r.POST("/say_hello", _Greeter_SayHello0_HTTP_Handler(srv))
	r.GET("/helloworld/{name:test}", _Greeter_SayHello1_HTTP_Handler(srv))
	r.POST("/say_multi", _Greeter_SayMulti0_HTTP_Handler(srv))
	r.GET("/app/{inner.inner_name}", _Greeter_SayMulti1_HTTP_Handler(srv))
	r.POST("/echo_post/{inner.inner_name:echo/.*}", _Greeter_Echo0_HTTP_Handler(srv))
	r.GET("/echo/{inner.inner_name:echo/.*}", _Greeter_Echo1_HTTP_Handler(srv))
}

func _Greeter_SayHello0_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in HelloRequest
		if err := ctx.Bind(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/SayHello")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.SayHello(ctx, req.(*HelloRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

func _Greeter_SayHello1_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in HelloRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/SayHello")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.SayHello(ctx, req.(*HelloRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

func _Greeter_SayMulti0_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in MultiRequest
		if err := ctx.Bind(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/SayMulti")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.SayMulti(ctx, req.(*MultiRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

func _Greeter_SayMulti1_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in MultiRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/SayMulti")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.SayMulti(ctx, req.(*MultiRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

func _Greeter_Echo0_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in MultiRequest
		if err := ctx.Bind(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/Echo")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.Echo(ctx, req.(*MultiRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

func _Greeter_Echo1_HTTP_Handler(srv GreeterHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in MultiRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		if err := ctx.BindVars(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, "/helloworld.Greeter/Echo")
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.Echo(ctx, req.(*MultiRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*HelloReply)
		return ctx.Result(200, reply)
	}
}

type GreeterHTTPClient interface {
	Echo(ctx context.Context, req *MultiRequest, opts ...http.CallOption) (rsp *HelloReply, err error)
	SayHello(ctx context.Context, req *HelloRequest, opts ...http.CallOption) (rsp *HelloReply, err error)
	SayMulti(ctx context.Context, req *MultiRequest, opts ...http.CallOption) (rsp *HelloReply, err error)
}

type GreeterHTTPClientImpl struct {
	cc *http.Client
}

func NewGreeterHTTPClient(client *http.Client) GreeterHTTPClient {
	return &GreeterHTTPClientImpl{client}
}

func (c *GreeterHTTPClientImpl) Echo(ctx context.Context, in *MultiRequest, opts ...http.CallOption) (*HelloReply, error) {
	var out HelloReply
	pattern := "/echo/{inner.inner_name:echo/.*}"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation("/helloworld.Greeter/Echo"))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, err
}

func (c *GreeterHTTPClientImpl) SayHello(ctx context.Context, in *HelloRequest, opts ...http.CallOption) (*HelloReply, error) {
	var out HelloReply
	pattern := "/helloworld/{name:test}"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation("/helloworld.Greeter/SayHello"))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, err
}

func (c *GreeterHTTPClientImpl) SayMulti(ctx context.Context, in *MultiRequest, opts ...http.CallOption) (*HelloReply, error) {
	var out HelloReply
	pattern := "/app/{inner.inner_name}"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation("/helloworld.Greeter/SayMulti"))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, err
}
