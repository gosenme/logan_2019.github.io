---
title: Gin
---

# Gin

## main

### conf.Init() 初始化配置

### r := server.NewRouter(); r.Run(":yourPort") 装载路由

## 数据配置 conf/conf.go

### Init()

- 获取本地环境变量

	- godotenv.Load() 从本地读取环境变量默认读 .env

- 读取翻译文件i18n.go  LoadLocales("conf/locales/zh-cn.yaml")
- 连接数据库

	- model.Database(os.Getenv("MYSQL_DSN"))

- 连接Redis

	- cache.Redis()

## 路由配置 server/router.go

### NewRouter

- 实例化路由对象 r := gin.Defaute()
- 注册中间件 r.Use(中间件)

	- Session
	- Cors
	- CurrentUser

- 注册路由组，组对象以及版本控制 v1 := r.Group("relativePath")

	- 增v1.POST
	- 查v1.GET
	- 改v1.PUT
	- 删v1.DELETE

- 返回路由对象return r
