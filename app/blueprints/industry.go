package blueprints

import "github.com/gin-gonic/gin"

// GetIndustries get industries list
func GetIndustries(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "get industry",
	})
}
