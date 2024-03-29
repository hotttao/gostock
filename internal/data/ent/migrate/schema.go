// Code generated by entc, DO NOT EDIT.

package migrate

import (
	"entgo.io/ent/dialect/sql/schema"
	"entgo.io/ent/schema/field"
)

var (
	// StockInfosColumns holds the columns for the "stock_infos" table.
	StockInfosColumns = []*schema.Column{
		{Name: "id", Type: field.TypeInt, Increment: true},
		{Name: "ts_code", Type: field.TypeString, Unique: true},
		{Name: "symbol", Type: field.TypeString},
		{Name: "name", Type: field.TypeString},
		{Name: "area", Type: field.TypeString, Nullable: true},
		{Name: "industry", Type: field.TypeString, Nullable: true},
		{Name: "fullname", Type: field.TypeString, Nullable: true},
		{Name: "enname", Type: field.TypeString, Nullable: true},
		{Name: "cnspell", Type: field.TypeString, Nullable: true},
		{Name: "market", Type: field.TypeString},
		{Name: "exchange", Type: field.TypeString, Nullable: true},
		{Name: "curr_type", Type: field.TypeString, Nullable: true},
		{Name: "list_status", Type: field.TypeEnum, Enums: []string{"L", "D", "P"}, Default: "L"},
		{Name: "list_date", Type: field.TypeTime, SchemaType: map[string]string{"mysql": "datetime"}},
		{Name: "delist_date", Type: field.TypeTime, Nullable: true, SchemaType: map[string]string{"mysql": "datetime"}},
		{Name: "is_hs", Type: field.TypeString, Nullable: true},
		{Name: "is_leader", Type: field.TypeBool, Default: false},
		{Name: "label_industry", Type: field.TypeString, Nullable: true},
	}
	// StockInfosTable holds the schema information for the "stock_infos" table.
	StockInfosTable = &schema.Table{
		Name:       "stock_infos",
		Columns:    StockInfosColumns,
		PrimaryKey: []*schema.Column{StockInfosColumns[0]},
	}
	// Tables holds all the tables in the schema.
	Tables = []*schema.Table{
		StockInfosTable,
	}
)

func init() {
}
