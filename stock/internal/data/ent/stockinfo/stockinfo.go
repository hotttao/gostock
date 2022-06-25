// Code generated by entc, DO NOT EDIT.

package stockinfo

import (
	"fmt"
)

const (
	// Label holds the string label denoting the stockinfo type in the database.
	Label = "stock_info"
	// FieldID holds the string denoting the id field in the database.
	FieldID = "id"
	// FieldTsCode holds the string denoting the ts_code field in the database.
	FieldTsCode = "ts_code"
	// FieldSymbol holds the string denoting the symbol field in the database.
	FieldSymbol = "symbol"
	// FieldName holds the string denoting the name field in the database.
	FieldName = "name"
	// FieldArea holds the string denoting the area field in the database.
	FieldArea = "area"
	// FieldIndustry holds the string denoting the industry field in the database.
	FieldIndustry = "industry"
	// FieldFullname holds the string denoting the fullname field in the database.
	FieldFullname = "fullname"
	// FieldEnname holds the string denoting the enname field in the database.
	FieldEnname = "enname"
	// FieldCnspell holds the string denoting the cnspell field in the database.
	FieldCnspell = "cnspell"
	// FieldMarket holds the string denoting the market field in the database.
	FieldMarket = "market"
	// FieldExchange holds the string denoting the exchange field in the database.
	FieldExchange = "exchange"
	// FieldCurrType holds the string denoting the curr_type field in the database.
	FieldCurrType = "curr_type"
	// FieldListStatus holds the string denoting the list_status field in the database.
	FieldListStatus = "list_status"
	// FieldListDate holds the string denoting the list_date field in the database.
	FieldListDate = "list_date"
	// FieldDelistDate holds the string denoting the delist_date field in the database.
	FieldDelistDate = "delist_date"
	// FieldIsHs holds the string denoting the is_hs field in the database.
	FieldIsHs = "is_hs"
	// FieldIsLeader holds the string denoting the is_leader field in the database.
	FieldIsLeader = "is_leader"
	// FieldLabelIndustry holds the string denoting the label_industry field in the database.
	FieldLabelIndustry = "label_industry"
	// Table holds the table name of the stockinfo in the database.
	Table = "stock_infos"
)

// Columns holds all SQL columns for stockinfo fields.
var Columns = []string{
	FieldID,
	FieldTsCode,
	FieldSymbol,
	FieldName,
	FieldArea,
	FieldIndustry,
	FieldFullname,
	FieldEnname,
	FieldCnspell,
	FieldMarket,
	FieldExchange,
	FieldCurrType,
	FieldListStatus,
	FieldListDate,
	FieldDelistDate,
	FieldIsHs,
	FieldIsLeader,
	FieldLabelIndustry,
}

// ValidColumn reports if the column name is valid (part of the table columns).
func ValidColumn(column string) bool {
	for i := range Columns {
		if column == Columns[i] {
			return true
		}
	}
	return false
}

var (
	// DefaultIsLeader holds the default value on creation for the "is_leader" field.
	DefaultIsLeader bool
)

// ListStatus defines the type for the "list_status" enum field.
type ListStatus string

// ListStatusL is the default value of the ListStatus enum.
const DefaultListStatus = ListStatusL

// ListStatus values.
const (
	ListStatusL ListStatus = "L"
	ListStatusD ListStatus = "D"
	ListStatusP ListStatus = "P"
)

func (ls ListStatus) String() string {
	return string(ls)
}

// ListStatusValidator is a validator for the "list_status" field enum values. It is called by the builders before save.
func ListStatusValidator(ls ListStatus) error {
	switch ls {
	case ListStatusL, ListStatusD, ListStatusP:
		return nil
	default:
		return fmt.Errorf("stockinfo: invalid enum value for list_status field: %q", ls)
	}
}
