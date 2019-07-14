---
title: 项目配置
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

### 新建 docker-compose.yml
```yml
# docker-compose.yml文件的版本
version: "3"
# 管理的服务
services:
  redis:
    # 指定镜像
    image: redis:latest
    ports:
    # 端口映射
    - 6379:6379
    volumes:
    # 目录映射
    - "${REDIS_DIR}/conf:/usr/local/etc/redis"
    - "${REDIS_DIR}/data:/data"
    command:
      # 执行的命令
      redis-server

  mysql:
    image: mysql:latest
    ports:
    - 3306:3306
    volumes:
    - "${MYSQL_DIR}/data:/var/lib/mysql"
    - "${MYSQL_DIR}/conf.d:/etc/mysql/conf.d"
    environment:
    # 环境变量
    - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
```

### 手动创建 test 数据库
- 借助可视化工具进行操作
- 使用命令

### 容器管理可视化 
- [文档](https://portainer.readthedocs.io/en/stable/deployment.html#quick-start)
- docker volume create portainer_data
- docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer

### LVS负载均衡

### DNS负载均衡


### 使用腾讯云容器服务

### ssh-copy-id

### 阿里云容器管理

### 交叉编译

### i18n国际化
