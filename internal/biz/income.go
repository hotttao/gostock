package biz

import (
	"context"

	"github.com/go-kratos/kratos/v2/log"
)

// 1. 定义 income 对应的数据模型
// Income is a Income model.
type Income struct {
	stock_id int
}

// 2. 定义 income 的数据获取接口
// IncomeRepo is a income repo.
type IncomeRepo interface {
	Save(context.Context, *Income) (*Income, error)
	Update(context.Context, *Income) (*Income, error)
	FindByID(context.Context, int64) (*Income, error)
	ListByHello(context.Context, string) ([]*Income, error)
	ListAll(context.Context) ([]*Income, error)
}

// 3. 实现 income 的业务逻辑
// IncomeUsecase is a IncomeUsecase usecase.
type IncomeUsecase struct {
	repo IncomeRepo
	log  *log.Helper
}

// 4. IncomeUsecase 的工厂函数
// NewIncomeUsecase new a Income usecase.
func NewIncomeUsecase(repo IncomeRepo, logger log.Logger) *IncomeUsecase {
	return &IncomeUsecase{repo: repo, log: log.NewHelper(logger)}
}

// 5. 实现 Income 的具体业务逻辑，依据业务逻辑定义
// CreateGreeter creates a Greeter, and returns the new Greeter.
func (uc *IncomeUsecase) CreateIncome(ctx context.Context, g *Income) (*Income, error) {
	uc.log.WithContext(ctx).Infof("CreateGreeter: %v", g.stock_id)
	return uc.repo.Save(ctx, g)
}
