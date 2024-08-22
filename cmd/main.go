package main

import (
	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
	"net/http"
	"os"
)

func main() {
	router := gin.Default()

	metrics := ginmetrics.GetMonitor()
	metrics.SetMetricPath("/metrics")
	metrics.Use(router)

	router.GET("/api/v1/gin", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello " + os.Getenv("USERNAME") + " from " + os.Getenv("MY_POD_NAME") + " with log level " + os.Getenv("LOG_LEVEL"))
	})

	router.Run(":8000")
}
