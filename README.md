# cqupt每日健康打卡

设置github actions，进行每日打卡。默认每日运行两次。

# Usage

1. fork此仓库
2. 设置账号信息，信息格式参考[exmaple](./example_settings.md)。然后把信息放到secret中，参考如下：

![1664259210288](image/README/1664259210288.png)

> note: secret名字应该为`SETTINGS`，除非自己更改workflow中的变量。

# 结果图

+ 打卡成功

![1664259623620](image/README/1664259623620.png)

+ 已打卡

![1664259658807](image/README/1664259658807.png)
