package biz

import (
	"context"
	v1 "gostock/api/stock/v1"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

// 1. 定义 StockInfo 对应的数据模型

type StockInfo struct {
	Id            int32     // ID
	TsCode        string    // Y	TS代码
	Symbol        string    //	Y	股票代码
	Name          string    //	Y	股票名称
	Area          string    //	Y	地域
	Industry      string    //	Y	所属行业
	Fullname      string    //	N	股票全称
	Enname        string    //	N	英文全称
	Cnspell       string    //	N	拼音缩写
	Market        string    //	Y	市场类型（主板/创业板/科创板/CDR）
	Exchange      string    //	N	交易所代码
	CurrType      string    //	N	交易货币
	ListStatus    string    //	N	上市状态 L上市 D退市 P暂停上市
	ListDate      time.Time //	Y	上市日期
	DelistDate    time.Time //	N	退市日期
	IsHs          string    //	N	是否沪深港通标的，N否 H沪股通 S深股通
	IsLeader      bool      //	N	是否为龙头
	LabelIndustry string    //	N 自定义行业标签
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
	// return uc.repo.FindByID(ctx, id)

	return nil, v1.ErrorStockNotFound("%v stock not found", 123)
	// return nil, fmt.Errorf("%v stock not found", 123)
}
