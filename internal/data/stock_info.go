package data

import (
	"context"
	"gostock/internal/biz"
	"gostock/internal/data/ent"

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

func (r *stockInfoRepo) ToStockInfo(s *ent.StockInfo) *biz.StockInfo {
	return &biz.StockInfo{
		Id:            int32(s.ID),
		TsCode:        s.TsCode,
		Symbol:        s.Symbol,
		Name:          s.Name,
		Area:          s.Area,
		Industry:      s.Industry,
		Fullname:      s.Fullname,
		Enname:        s.Enname,
		Cnspell:       s.Cnspell,
		Market:        s.Market,
		Exchange:      s.Exchange,
		CurrType:      s.CurrType,
		ListStatus:    string(s.ListStatus),
		ListDate:      s.ListDate,
		DelistDate:    s.DelistDate,
		IsHs:          s.IsHs,
		IsLeader:      s.IsLeader,
		LabelIndustry: s.LabelIndustry,
	}
}

func (repo *stockInfoRepo) FindByID(ctx context.Context, id int32) (*biz.StockInfo, error) {
	s, err := repo.data.db.StockInfo.Get(ctx, int(id))
	if err != nil {
		return nil, err
	}
	return repo.ToStockInfo(s), nil
}
