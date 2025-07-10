# Job-Agent


## 项目概述

**Job Agent**是一款基于多技术栈的智能求职分析系统，主要功能包括： 

- 实时爬取BOSS直聘等招聘平台数据 
- 可视化展示行业趋势和薪资分布 
- 智能分析职位需求与简历匹配度 
- 自动化批量投递简历，AI润色和Boss的聊天话术

设计理念：通过自动化技术减轻求职过程中的重复劳动，用数据驱动决策，用AI助力求职



## 核心功能模块

1. **爬虫系统**

   - 基于playwright自动化工具，绕过反爬机制，获取用户token
   - 结合requests工具，高效获取大批量岗位信息
   - 持久化爬虫遍历的索引，支持断点恢复操作
   - 向Boss发送问候语，并发送简历图片，实现批量自动化投递简历

2. **前端展示**

   - 基于Vue2 + javascript + Element Plus组件库实现界面展示
   - 通过axios向后端发送异步请求
   - 使用ECharts数据可视化，展现岗位分析结果

3. **后端服务**

   - 使用SpringBoot框架实现著业务逻辑
   - 使用MyBatis + MySQL持久化岗位数据
   - Java后端实现用户模块、岗位模块、图表绘制模块等接口

   - Python后端使用flask框架，实现简历模块、爬虫模块、AI服务模块接口



**技术架构**


![image-20250709205022741](https://github.com/user-attachments/assets/5363aff2-bf19-42e4-aa97-255a0058fb93)



## 项目结构

```
JobAgent/                        # 项目根目录
├── web/                         # 🌐 前端代码（基于 Vue2）
│   ├── vue.config.js            # Vue 配置文件
│   └── src/                     # 前端源码目录
│       ├── App.vue              # 应用主组件入口
│       ├── views/               # 各个页面视图
│       ├── utils/               # 通用工具函数
│       ├── store/               # Vuex 状态管理用户信息
│       ├── router/              # 路由配置文件
│       ├── components/          # 通用组件（按钮、弹窗、表格等）
│       └── api/                 # 与后端通信的 API 封装模块

├── crawl/                       # 🐍 后端 Python 模块（含爬虫与接口服务）
│   ├── app.py                   # Flask 主程序入口
│   ├── application.yml          # 后端配置文件
│   ├── resume_routes.py         # 简历上传/解析等接口定义
│   ├── utils/                   # Python 工具函数
│   ├── database/                # 数据库操作封装
│   ├── crawler/                 # Playwright 自动化爬虫模块
│   ├── cache/                   # 本地缓存
│   └── agent/                   # 与 OpenAI 模型交互逻辑

├── src/                         # ☕ Java 后端目录（Spring Boot 项目）
│   └── main/
│       ├── resources/           # 配置文件目录
│       │   ├── application.yml              # 主配置文件
│       │   └── application-dev.yml          # 开发环境配置
│       └── java/
│           └── com/
│               └── jobagent/
│                   ├── JobAgentApplication.java   # Java 后端启动类
│                   ├── controller/                # 控制层（处理 HTTP 请求）
│                   ├── dto/                       # 数据传输对象（前后端交互结构）
│                   ├── entity/                    # 实体类
│                   ├── exception/                 # 全局异常处理
│                   ├── handle/                    # 异常捕获
│                   ├── interceptor/               # 登录校验拦截器
│                   ├── mapper/                    # MyBatis 映射接口
│                   ├── service/                   # 业务逻辑层
│                   │   └── impl/                  # 业务实现类
│                   ├── utils/                     # 工具类
│                   └── vo/                        # 视图对象（后端向前端返回的数据封装）


```



## 界面展示

主界面

![image-20250709172153713](https://github.com/user-attachments/assets/0eda5940-0be2-48d9-bc10-5862062a21b9)


爬取岗位信息界面

![image-20250709173312893](https://github.com/user-attachments/assets/6ee6ba85-a228-4b73-b796-bbe816a2a9c8)


职位查询界面

![image-20250709173441829](https://github.com/user-attachments/assets/ce5f5997-614f-469d-b71e-e385d4807fe7)


岗位薪资分析界面

![image-20250709173529019](https://github.com/user-attachments/assets/7eb553ba-dc1e-4b1d-9c50-7cb759b52098)


智能岗位匹配度打分界面

![image-20250709173826313](https://github.com/user-attachments/assets/4d735c62-a84b-463f-b7e4-040f7e1b6258)






## 环境要求

- JDK 11+
- Python 3.12+
- Node.js 10.9+
- MySQL 5.7+
- Maven 3.9+

- Java工具包：pom.xml
- Vue工具包：package.json
- Python工具包：requirements.txt



## 安装搭建

**mysql安装**

首先切换到root用户`sudo su`

依次执行下面命令

```
mkdir mysql && cd mysql
wget https://downloads.mysql.com/archives/get/p/23/file/mysql-8.4.0-linux-glibc2.17-x86_64-minimal.tar.xz
groupadd mysql
useradd -r -g mysql -s /bin/false mysql
tar -xvf mysql*.tar.xz -C /usr/local
cd /usr/local
mv mysql*/ mysql
cd mysql
mkdir mysql-files
chown mysql:mysql mysql-files
chmod 750 mysql-files
apt-get install libaio1 libncurses5
bin/mysqld_safe --user=mysql
export PATH=$PATH:/usr/local/mysql/bin
mkdir -p /data/mysql
chown mysql:mysql -R /data/mysql
chown mysql:mysql -R /tmp
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
```

然后添加配置文件

```
vi /etc/my.cnf
```

内容如下

```
[mysqld]
bind-address=0.0.0.0
port=3306
user=mysql
basedir=/usr/local/mysql
datadir=/data/mysql
socket=/tmp/mysql.sock
log-error=/data/mysql/mysql.err
pid-file=/data/mysql/mysql.pid
#character config
character_set_server=utf8mb4
symbolic-links=0
explicit_defaults_for_timestamp=true
```

然后进入bin目录下运行下面命令初始化

```
sudo ./mysqld --defaults-file=/etc/my.cnf --basedir=/usr/local/mysql/ --datadir=/data/mysql/ --user=mysql --initialize
```

查看初始密码

```
cat /data/mysql/mysql.err | grep localhost
```

![image-20250710103916981](https://github.com/user-attachments/assets/ceaaf550-a147-4484-81f7-6fd8e9d2b240)


运行`mysql -u root -p`，输入显示的默认密码，进入之后修改root密码

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
```



**创建用户和数据库**

```sql
CREATE USER 'rebibabo'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'rebibabo'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE jobagent;
```



**安装Java11**

```
apt update
apt install openjdk-11-jdk -y
java -version
```



**安装mvn**

```
apt install maven -y
mvn -v
```



**安装nodejs和npm**

```
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
node -v
npm -v
```



**下载源代码**

```
git clone https://github.com/rebibabo/Job-Agent.git
```



**Python安装配置**

在crawl目录下执行以下命令

```shell
pip install -r requirements.txt
```



**数据库建表**

在crawl目录下执行以下命令

```shell
python -m database.init
```

表说明：

- city：各省市区的城市和编码
- industry：行业分类和编码
- title：岗位分类和编码
- company：公司信息，包括融资阶段、规模人数、福利等
- job：岗位信息，包括名称、公司id（外键company）、地点、薪资、学历要求、经验要求、行业等
- user：员工信息，即用户名和密码
- user_job：用户岗位查询表，员工id（外键user），岗位id（外键job）、过滤规则哈希值、查看状态和投递状态
- user_rule：保存用户搜索规则



**环境变量配置**

向系统环境变量中添加以下变量，分别表示OpenAI的api_key以及镜像地址

```
OPENAI_API_KEY
OPENAI_BASE_URL
```



**前端环境安装**

进入web目录下执行以下命令

```
npm install
```



**Java环境安装**

进入根目录执行以下命令，安装环境

```
mvn install
```

然后执行下面命令生成jar包

```
mvn clean package
```





## 项目启动

**前端启动**

在web目录下执行以下命令

```
npm run serve
```



**Java后端启动**

在根目录下执行以下命令

```
java -jar target/JobAgent-0.0.1-SNAPSHOT.jar
```



**Python后端启动**

在crawl目录下执行下面命令

```
python app.py
```







