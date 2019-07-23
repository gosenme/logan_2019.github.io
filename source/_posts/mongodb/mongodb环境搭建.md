---
title: mongodb环境搭建
---

### mongodb-docker
- docker-compose
```yml
# docker-compose.yml文件的版本
version: "3"
# 管理的服务
services:
  mongodb:
    image: mongo:latest
    ports:
    - "27017:27017"
    volumes:
    - "${MONGODB_DIR}/data:/data/db"
    - "${MONGODB_DIR}/etc/localtime:/etc/localtime"

```

### 可视化mongoAdmin
```yml
version: "2"
services:
  adminmongo:
    image: mrvautin/adminmongo
    ports:
      - 1234:1234
    environment:
      - HOST=0.0.0.0
```