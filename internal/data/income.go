package data

import (
	"context"
	"gostock/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
)

type incomRepo struct {
	data *Data
	log  *log.Helper
}

func (r *incomRepo) Save(ctx context.Context, g *biz.Income) (*biz.Income, error) {
	return g, nil
}

func (r *incomRepo) Update(ctx context.Context, g *biz.Income) (*biz.Income, error) {
	return g, nil
}

func (r *incomRepo) FindByID(context.Context, int64) (*biz.Income, error) {
	return nil, nil
}

func (r *incomRepo) ListByHello(context.Context, string) ([]*biz.Income, error) {
	return nil, nil
}

func (r *incomRepo) ListAll(context.Context) ([]*biz.Income, error) {
	return nil, nil
}

// NewIncomeRepo .
func NewIncomeRepo(data *Data, logger log.Logger) biz.IncomeRepo {
	return &incomRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}
