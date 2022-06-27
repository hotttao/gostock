package data

import (
	"context"
	"gostock/internal/conf"
	"gostock/internal/data/ent"
	"gostock/internal/data/ent/migrate"

	"entgo.io/ent/dialect"
	"entgo.io/ent/dialect/sql"

	"ariga.io/sqlcomment"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-redis/redis/extra/redisotel"
	"github.com/go-redis/redis/v8"
	"github.com/google/wire"

	_ "github.com/go-sql-driver/mysql"
)

// ProviderSet is data providers.
var ProviderSet = wire.NewSet(
	NewData,

	NewEntClient,
	NewRedisClient,

	NewGreeterRepo,
	NewIncomeRepo,
	NewStockInfoRepo,
)

// Data .
type Data struct {
	// TODO wrapped database client
	db  *ent.Client
	rdb *redis.Client
	log *log.Helper
}

// NewData .
func NewData(entClient *ent.Client, redisClient *redis.Client, logger log.Logger) (*Data, func(), error) {
	l := log.NewHelper(log.With(logger, "module", "data/logger-service"))
	d := &Data{
		db:  entClient,
		rdb: redisClient,
		log: l,
	}
	cleanup := func() {
		l.Info("message", "closing the data resources")
		if err := d.db.Close(); err != nil {
			l.Error(err)
		}
	}
	return d, cleanup, nil
}

// Redis.
func NewRedisClient(conf *conf.Data, logger log.Logger) *redis.Client {
	l := log.NewHelper(log.With(logger, "module", "redis/data/logger-service"))

	rdb := redis.NewClient(&redis.Options{
		Addr:         conf.Redis.Addr,
		Password:     conf.Redis.Password,
		DB:           int(conf.Redis.Db),
		DialTimeout:  conf.Redis.DialTimeout.AsDuration(),
		WriteTimeout: conf.Redis.WriteTimeout.AsDuration(),
		ReadTimeout:  conf.Redis.ReadTimeout.AsDuration(),
	})
	if rdb == nil {
		l.Fatalf("failed opening connection to redis")
	}
	rdb.AddHook(redisotel.TracingHook{})

	return rdb
}

// NewEntClient 创建数据库客户端
func NewEntClient(conf *conf.Data, logger log.Logger) *ent.Client {
	l := log.NewHelper(log.With(logger, "module", "ent/data/logger-service"))

	db, err := sql.Open(
		conf.Database.Driver,
		conf.Database.Source,
	)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	// Create sqlcomment driver which wraps sqlite driver.
	commentedDriver := sqlcomment.NewDriver(dialect.Debug(db),
		sqlcomment.WithTagger(
			// add tracing info with Open Telemetry.
			sqlcomment.NewOTELTagger(),
			// use your custom commenter
			// CustomCommenter{},
		),
		// add `db_driver` version tag
		sqlcomment.WithDriverVerTag(),
		// add some global tags to all queries
		sqlcomment.WithTags(sqlcomment.Tags{
			sqlcomment.KeyApplication: "stock",
			sqlcomment.KeyFramework:   "go-chi",
		}))
	// Create and configure ent client
	client := ent.NewClient(ent.Driver(commentedDriver))

	// Run the auto migration tool.
	if err := client.Schema.Create(context.Background(), migrate.WithForeignKeys(false)); err != nil {
		l.Fatalf("failed creating schema resources: %v", err)
	}
	return client
}
