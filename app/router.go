// 路由配置

package app

import (
	"github.com/gin-gonic/gin"
	"github.com/hotttao/gostock/app/blueprints"
)

// NewRouter create router
func NewRouter() *gin.Engine {
	r := gin.Default()

	v1 := r.Group("/beta")
	{
		v1.GET("/industries", blueprints.GetIndustries)
	}
	return r
}
