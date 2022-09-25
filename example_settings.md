
你需要设置的信息格式如下：

```json
{
    "cqupt" : {
        "username" : "<your username>",
        "password" : "<your password>"
    },
    "mail" : {
        "account" : "example@qq.com",
        "password" :  "<smtp password>",
        "smtp_host": "smtp.qq.com"
    },
    "address" : "详细居住地址" 
}
```

邮箱默认使用qq邮箱，因为提示比较方便。如果需要更改其他邮箱，`smtp_host`也需要换成对应的host。