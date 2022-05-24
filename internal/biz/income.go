package biz

import (
	"context"

	"github.com/go-kratos/kratos/v2/log"
)

// Greeter is a Greeter model.
type Income struct {
	stock_id int
}

// GreeterRepo is a Greater repo.
type IncomeRepo interface {
	Save(context.Context, *Income) (*Income, error)
	Update(context.Context, *Income) (*Income, error)
	FindByID(context.Context, int64) (*Income, error)
	ListByHello(context.Context, string) ([]*Income, error)
	ListAll(context.Context) ([]*Income, error)
}

// GreeterUsecase is a Greeter usecase.
type IncomeUsecase struct {
	repo IncomeRepo
	log  *log.Helper
}

// NewGreeterUsecase new a Greeter usecase.
func NewIncomeUsecase(repo IncomeRepo, logger log.Logger) *IncomeUsecase {
	return &IncomeUsecase{repo: repo, log: log.NewHelper(logger)}
}

// CreateGreeter creates a Greeter, and returns the new Greeter.
func (uc *GreeterUsecase) CreateIncome(ctx context.Context, g *Greeter) (*Greeter, error) {
	uc.log.WithContext(ctx).Infof("CreateGreeter: %v", g.Hello)
	return uc.repo.Save(ctx, g)
}
