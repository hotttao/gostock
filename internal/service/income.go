package service

import (
	"context"

	pb "gostock/api/evaluate/v1"
	"gostock/internal/biz"
)

type IncomeService struct {
	pb.UnimplementedIncomeServer
	uc *biz.IncomeUsecase
}

func NewIncomeService(uc *biz.IncomeUsecase) *IncomeService {
	return &IncomeService{uc: uc}
}

func (s *IncomeService) CreateIncome(ctx context.Context, req *pb.CreateIncomeRequest) (*pb.CreateIncomeReply, error) {
	return &pb.CreateIncomeReply{}, nil
}
func (s *IncomeService) UpdateIncome(ctx context.Context, req *pb.UpdateIncomeRequest) (*pb.UpdateIncomeReply, error) {
	return &pb.UpdateIncomeReply{}, nil
}
func (s *IncomeService) DeleteIncome(ctx context.Context, req *pb.DeleteIncomeRequest) (*pb.DeleteIncomeReply, error) {
	return &pb.DeleteIncomeReply{}, nil
}
func (s *IncomeService) GetIncome(ctx context.Context, req *pb.GetIncomeRequest) (*pb.GetIncomeReply, error) {
	return &pb.GetIncomeReply{}, nil
}
func (s *IncomeService) ListIncome(ctx context.Context, req *pb.ListIncomeRequest) (*pb.ListIncomeReply, error) {
	return &pb.ListIncomeReply{}, nil
}
