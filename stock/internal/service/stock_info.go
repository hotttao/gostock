package service

import (
	"context"
	v1 "gostock/api/stock/v1"
	"gostock/internal/biz"
)

type StockService struct {
	v1.UnimplementedStockInfoServiceServer
	uc *biz.StockInfoUsecase
}

func NewStockInfoService(uc *biz.StockInfoUsecase) *StockService {
	return &StockService{
		uc: uc,
	}
}

func (s *StockService) GetStockInfo(ctx context.Context, in *v1.GetStockInfoRequest) (*v1.StockInfo, error) {
	g, err := s.uc.GetStockInfo(ctx, in.Id)
	if err != nil {
		return nil, err
	}
	// return nil, v1.ErrorStockNotFound("stock: %v", in.Id)
	stock := &v1.StockInfo{
		TsCode:        g.TsCode,
		Symbol:        g.Symbol,
		Name:          g.Name,
		Area:          g.Area,
		Industry:      g.Industry,
		Fullname:      g.Fullname,
		Enname:        g.Enname,
		Cnspell:       g.Cnspell,
		Market:        g.Market,
		Exchange:      g.Exchange,
		CurrType:      g.CurrType,
		ListStatus:    string(g.ListStatus),
		ListDate:      g.ListDate.Format("2006-01-02 15:04:05"),
		DelistDate:    g.DelistDate.Format("2006-01-02 15:04:05"),
		IsHs:          g.IsHs,
		IsLeader:      g.IsLeader,
		LabelIndustry: g.LabelIndustry,
	}
	return stock, nil
}
