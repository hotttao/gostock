package server

import (
	evaluate_v2 "gostock/api/evaluate/v1"
	v1 "gostock/api/helloworld/v1"
	stock_v1 "gostock/api/stock/v1"
	"gostock/internal/conf"
	"gostock/internal/service"

	prom "github.com/go-kratos/kratos/contrib/metrics/prometheus/v2"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/middleware/metrics"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/transport/http"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// NewHTTPServer new a HTTP server.
func NewHTTPServer(c *conf.Server, greeter *service.GreeterService, income *service.IncomeService,
	stock *service.StockService, logger log.Logger) *http.Server {
	var opts = []http.ServerOption{
		http.Middleware(
			metrics.Server(
				metrics.WithSeconds(prom.NewHistogram(_metricSeconds)),
				metrics.WithRequests(prom.NewCounter(_metricRequests)),
			),
			recovery.Recovery(),
		),
	}
	if c.Http.Network != "" {
		opts = append(opts, http.Network(c.Http.Network))
	}
	if c.Http.Addr != "" {
		opts = append(opts, http.Address(c.Http.Addr))
	}
	if c.Http.Timeout != nil {
		opts = append(opts, http.Timeout(c.Http.Timeout.AsDuration()))
	}
	srv := http.NewServer(opts...)
	srv.Handle("/metrics", promhttp.Handler())
	v1.RegisterGreeterHTTPServer(srv, greeter)
	evaluate_v2.RegisterIncomeHTTPServer(srv, income)
	stock_v1.RegisterStockServiceHTTPServer(srv, stock)
	return srv
}
