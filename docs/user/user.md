## 1. <a name="register">创建用户</a>
POST {{HOST_NAME}}/register/
request
```json
{
	"username":"john",
	"first_name":"ss",
	"last_name":"dd",
	"birthday":"1994-05-15",
	"description":"查询",
	"address":"上海市宝山区"
}
```
response
```json
{
    "id": 15,
    "content": "创建用户成功"
}
```

## 2. <a name="search">搜索用户信息</a>
GET {{HOST_NAME}}/search?keyword=上海&full_name=bb aa&start_birth=1993-05-15&end_birth=1995-05-15

搜索条件：
    keyword：address和description
    id：用户ID
    start_time：用户创建时间
    end_time：用户更新时间
    username：用户名 支持模糊搜索
    start_birth：起始生日
    end_birth：截止生日
    page_size：每页多少条数据
    page：哪一页
    first_name：名字
    last_name：姓氏
    full_name：全名，只做搜索，不做存储
response
```json
{
    "current_page": 1,
    "total": 1,
    "pages": 1,
    "data": [
        {
            "first_name": "bb",
            "es_id": "FqlJlWgBkwfc6axuRsQe",
            "create_time": 1548692833811,
            "address": "上海市静安区",
            "birthday": "1993-05-15",
            "username": "bob",
            "last_name": "aa",
            "description": "描述qqqqqqqqqqqqqqqqq",
            "id": 14,
            "update_time": 1548692833811
        }
    ]
}
```