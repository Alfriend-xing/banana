# banana

监控服务器运行状况
Monitor server running state

### 使用工具
后端：python,flask,psutil,requests,sqlite3
前端:semantic-ui,jquery

### 功能
监控服务器运行状态，记录CPU，内存，硬盘和网卡的实时数据和历史数据
可以为服务器指定标签和描述

### 安装
```shell
# 安装python3

# 安装依赖
$ git clone https://github.com/Alfriend-xing/banana.git
$ cd banana
$ pip install -r requirements.txt

# 服务端
$ python bananainstall.py server
$ vim banana.conf
# 修改服务端IP
server_ip=127.0.0.1 #改为服务端IP

# 客户端
$ python bananainstall.py client

# 启动
$ python banana.py
```

### demo
#### 上下线
![](https://ws3.sinaimg.cn/large/005BYqpgly1g3rirn2t3hg30y20hpe6g.jpg)
#### 查看历史记录
![](https://ws3.sinaimg.cn/large/005BYqpgly1g3rirbvo3wg30y20hpqtl.jpg)
#### 编辑标签
![](https://ws3.sinaimg.cn/large/005BYqpgly1g3riqnkyudg30y20hpx1x.jpg)
#### 删除记录
![](https://ws3.sinaimg.cn/large/005BYqpgly1g3ripevtf2g30y20hpb29.jpg)

### 已找到的同类项目
- https://github.com/k3oni/pydash
- https://github.com/hypersport/sysinfo

### 

### todo
- 主机过多时的分页显示
- 显示服务器系统的logo
- 只显示在线主机的过滤器(目前统一显示为centos的logo)
- 根据标签、描述、IP查找主机的搜索框
- 修改表结构，支持过去一个月、一周的历史数据查询
