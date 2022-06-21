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
	stock := &v1.StockInfo{
		Id:   g.Id,
		Name: g.Name,
	}
	return stock, nil
}
