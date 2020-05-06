package cmd

import (
	"github.com/hotttao/gostock/app"
	"github.com/spf13/cobra"
)

var envPath string

// webCmd represents the web command
var webCmd = &cobra.Command{
	Use:   "web",
	Short: "run gostock web serve",
	Long:  `run gostock web serve`,
	Run: func(cmd *cobra.Command, args []string) {
		RunWebServer()
	},
}

func init() {
	rootCmd.AddCommand(webCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// webCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// webCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	webCmd.Flags().StringVarP(&envPath, "env", "e", ".env", "web enviroment config")
}

// RunWebServer start web server
func RunWebServer() {
	router := app.NewRouter()
	router.Run(":6080")
}
