// 数据库初始化等配置

package app

import (
	"log"
	"os"

	_ "github.com/go-sql-driver/mysql" // import mysql driver
	"github.com/jmoiron/sqlx"
	"github.com/joho/godotenv"
)

// DB sqlx.DB connection
var DB *sqlx.DB

// CreateDBConnect init sqlx.DB connect
func CreateDBConnect(connString string) *sqlx.DB {
	DB, error := sqlx.Connect("mysql", connString)
	if error != nil {
		log.Fatal(error)
	}
	return DB
}

func init() {
	godotenv.Load("app/.env")
	mysqlConn := os.Getenv("MYSQL_DSN")
	// fmt.Println(mysqlConn)
	CreateDBConnect(mysqlConn)
}
