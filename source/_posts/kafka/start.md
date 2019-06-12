---
title: kafka start
---

### kafka-docker
[项目地址](git@github.com:wurstmeister/kafka-docker.git)
- Start a cluster: `docker-compose up -d`
- Add more brokers: `docker-compose scale kafka=3`
- Destroy a cluster: `docker-compose stop`

### kafka-manager-docker
[项目地址](git@github.com:sheepkiller/kafka-manager-docker.git)
- Quick Start
    `docker run -it --rm  -p 9000:9000 -e ZK_HOSTS="your-zk.domain:2181" -e APPLICATION_SECRET=letmein sheepkiller/kafka-manager`
