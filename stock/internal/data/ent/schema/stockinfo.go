package schema

import (
	"entgo.io/ent"
	"entgo.io/ent/dialect"
	"entgo.io/ent/schema/field"
)

// StockInfo holds the schema definition for the StockInfo entity.
type StockInfo struct {
	ent.Schema
}

// Fields of the StockInfo.
func (StockInfo) Fields() []ent.Field {
	return []ent.Field{
		field.String("ts_code").Unique(), // Y	TS代码
		field.String("symbol"),           //	Y	股票代码
		field.String("name"),             //	Y	股票名称
		field.String("area").
			Optional(), //	Y	地域
		field.String("industry").
			Optional(), // Y	所属行业
		field.String("fullname").
			Optional(), //	N	股票全称
		field.String("enname").
			Optional(), //	N	英文全称
		field.String("cnspell").
			Optional(), //	N	拼音缩写
		field.String("market"), //	Y	市场类型（主板/创业板/科创板/CDR）
		field.String("exchange").
			Optional(), //	N	交易所代码
		field.String("curr_type").
			Optional(), //	N	交易货币
		field.Enum("list_status").
			Default("L").
			Values("L", "D", "P"), //	N	上市状态 L上市 D退市 P暂停上市
		field.Time("list_date").
			SchemaType(map[string]string{
				dialect.MySQL: "datetime",
			}), //	Y	上市日期
		field.Time("delist_date").
			Optional().
			SchemaType(map[string]string{
				dialect.MySQL: "datetime",
			}), //	N	退市日期
		field.String("is_hs").
			Optional(), //	N	是否沪深港通标的，N否 H沪股通 S深股通

		field.Bool("is_leader").Default(false), //	N 是否为龙头企业
		field.String("label_industry").
			Optional(), //	N 自定义行业标签
	}
}

// Edges of the StockInfo.
func (StockInfo) Edges() []ent.Edge {
	return nil
}
