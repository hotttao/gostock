// Code generated by entc, DO NOT EDIT.

package stockinfo

const (
	// Label holds the string label denoting the stockinfo type in the database.
	Label = "stock_info"
	// FieldID holds the string denoting the id field in the database.
	FieldID = "id"
	// FieldName holds the string denoting the name field in the database.
	FieldName = "name"
	// Table holds the table name of the stockinfo in the database.
	Table = "stock_infos"
)

// Columns holds all SQL columns for stockinfo fields.
var Columns = []string{
	FieldID,
	FieldName,
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
	// IDValidator is a validator for the "id" field. It is called by the builders before save.
	IDValidator func(int) error
)