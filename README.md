# flight-search

## 1. 爬虫

ip池借用项目：[Python爬虫代理IP池(proxy pool)](https://github.com/jhao104/proxy_pool)

## 2. 数据说明

d开头表示出发地，a开头表示到达地

dairport_code   机场三字码  
dairport        机场名
dterminal       航站楼
dcity_code      城市三字码
dcity           城市名
aairport_code   
aairport
aterminal
acity_code
acity
airline_code    航空公司二字码
airline         航空公司
flight_num      航班号
plane_code      飞机三字码
plane_kind      飞机类型
plane           飞机名
dtime           出发时间
atime           到达时间
price           价格
discount        折扣
class           舱位等级
punctuality     准点率（%）
stop            经停（次数）

## 3. web应用模块（api）

[查看API说明](http://192.168.101.83:5000/api)

## 4. 运行环境

### 4.1 Web应用运行环境

- 操作系统：Ubuntu 18.04
- 数据库：MySQL 5.7.30
- Python 后端：Flask 1.1.2，PyMySQL 0.9.3

### 4.2 爬虫

- 爬虫：requests 2.20.0，ip池：[Python爬虫代理IP池(proxy pool)](https://github.com/jhao104/proxy_pool)

### 4.3 数据处理

- 数据处理：Hadoop 2.9.2，Hive 2.3.7，MySQL 5.7.30
