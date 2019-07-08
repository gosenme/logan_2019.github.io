---
title: Giligili项目学习
---

### 初始化配置文件
```go
// Init 初始化配置项
func Init() {
	// 从本地读取环境变量
	godotenv.Load()

	// 读取翻译文件
	if err := LoadLocales("conf/locales/zh-cn.yaml"); err != nil {

		panic(err)
	}

	// 连接数据库 从 .env中读数据
	model.Database(os.Getenv("MYSQL_DSN"))
	cache.Redis()
}

```

### i18n国际化
