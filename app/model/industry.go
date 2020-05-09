package model

const (
	sqlQueryByID   = "SELECT * FROM stock.industry WHERE id IN (?)"
	sqlQueryByName = ""
)

// IndustryEntity industry table data model
type IndustryEntity struct {
}

// QueryByID query industry by id
func (industry *IndustryEntity) QueryByID(id ...int) {

}

// QueryByName query industry by name
func (industry *IndustryEntity) QueryByName(name ...string) {

}
