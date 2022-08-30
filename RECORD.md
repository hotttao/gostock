# 项目创建过程记录

## 1. 项目初始化
```bash
# go module init
go mod init github.com/hotttao/gostock

# cobra init
cobra init --pkg-name github.com/hotttao/gostock
cobra add web


# module install
go get -u github.com/gin-gonic/gin
go get -u github.com/joho/godotenv
go get -u github.com/jmoiron/sqlx
```