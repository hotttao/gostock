// Code generated by entc, DO NOT EDIT.

package ent

import (
	"gostock/internal/data/ent/schema"
	"gostock/internal/data/ent/stockinfo"
)

// The init function reads all schema descriptors with runtime code
// (default values, validators, hooks and policies) and stitches it
// to their package variables.
func init() {
	stockinfoFields := schema.StockInfo{}.Fields()
	_ = stockinfoFields
	// stockinfoDescID is the schema descriptor for id field.
	stockinfoDescID := stockinfoFields[0].Descriptor()
	// stockinfo.IDValidator is a validator for the "id" field. It is called by the builders before save.
	stockinfo.IDValidator = stockinfoDescID.Validators[0].(func(int) error)
}
