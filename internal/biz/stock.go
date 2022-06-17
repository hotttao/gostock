package biz

import (
	"context"

	"github.com/go-kratos/kratos/v2/log"
)

// 1. 定义 StockInfo 对应的数据模型
type StockInfo struct {
	Id   int32
	Name string
}

// 2. 定义 StockInfo 的数据获取接口
type StockInfoRepo interface {
	FindByID(context.Context, int32) (*StockInfo, error)
}

// 3. 实现 StockInfo 的业务逻辑
type StockInfoUsecase struct {
	repo StockInfoRepo
	log  *log.Helper
}

// 4. StockInfoUsecase 的工厂函数
func NewStockInfoUsecase(repo StockInfoRepo, logger log.Logger) *StockInfoUsecase {
	return &StockInfoUsecase{repo: repo, log: log.NewHelper(logger)}
}

func (uc *StockInfoUsecase) GetStockInfo(ctx context.Context, id int32) (*StockInfo, error) {
	return uc.repo.FindByID(ctx, id)
}
