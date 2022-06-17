package data

import (
	"context"
	"gostock/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
)

type stockInfoRepo struct {
	data *Data
	log  *log.Helper
}

func NewStockInfoRepo(data *Data, logger log.Logger) biz.StockInfoRepo {
	return &stockInfoRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

func (repo *stockInfoRepo) FindByID(context.Context, int32) (*biz.StockInfo, error) {
	s := &biz.StockInfo{
		Id:   1,
		Name: "闻泰科技",
	}
	return s, nil
}
