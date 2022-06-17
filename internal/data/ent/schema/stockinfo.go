package schema

import (
	"entgo.io/ent"
	"entgo.io/ent/schema/field"
)

// StockInfo holds the schema definition for the StockInfo entity.
type StockInfo struct {
	ent.Schema
}

// Fields of the StockInfo.
func (StockInfo) Fields() []ent.Field {
	return []ent.Field{
		field.Int("id").Positive(),
		field.String("name"),
	}
}

// Edges of the StockInfo.
func (StockInfo) Edges() []ent.Edge {
	return nil
}
