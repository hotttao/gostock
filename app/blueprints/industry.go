package blueprints

import "github.com/gin-gonic/gin"

// GetIndustry get industries list
func GetIndustries(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "get industry",
	})
}
