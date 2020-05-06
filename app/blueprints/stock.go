package blueprints

import "github.com/gin-gonic/gin"

// GetStocks get stock list
func GetStocks(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "get stocks",
	})
}
