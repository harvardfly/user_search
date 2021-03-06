# 技术选型
```
web框架：Tornado
数据库：MySQL
ORM：peewee
搜索：ElasticSearch
表单验证：wtform
异步：协程、aiomysql、peewee-async、Celery
部署：Docker
```

# Docker 部署

### 创建日志目录
这个日志路径配置在settings - LOGGING - handlers
```
$ sudo mkdir -p /var/log/user_search
$ sudo chmod -R 777 /var/log/user_search
```

### redis image
```
$ cd user_search
$ sudo docker build -t user_search_redis -f docker/redis/Dockerfile .
```

### 配置redis
```
$ cp redis.conf.example redis.conf
```
按需配置文件：
1. daemonize no
2. port
3. bind
4. databases
5. maxmemory
6. requirepass

注：保证配置里面的端口号与docker-compose.yml里面的port对应上。

### web image
```
$ cd user_search
$ sudo docker build -t user_search -f docker/app/Dockerfile .
```

### nginx image
```
$ cd user_search
$ sudo docker build -t user_search_nginx -f docker/nginx/Dockerfile .
```

### 配置nginx
```
$ cp user_search_conf.example user_search_conf
```
按需配置文件：
1. listen

注：保证配置里面的端口号与docker-compose.yml里面的port对应上。

### 部署
```
$ cp docker-compose.yml.example docker-compose.yml

$ sudo docker-compose up -d
```
