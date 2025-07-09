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
├── web/                         # 🌐 前端代码（基于 Vue）
│   ├── vue.config.js            # Vue 配置文件
│   └── src/                     # 前端源码目录
│       ├── App.vue              # 应用主组件入口
│       ├── views/               # 各个页面视图（如主页、详情页等）
│       ├── utils/               # 通用工具函数（如时间格式化、请求封装等）
│       ├── store/               # Vuex 状态管理（用户信息、全局状态等）
│       ├── router/              # 路由配置文件（页面跳转规则）
│       ├── components/          # 通用组件（按钮、弹窗、表格等）
│       └── api/                 # 与后端通信的 API 封装模块

├── crawl/                       # 🐍 后端 Python 模块（含爬虫与接口服务）
│   ├── app.py                   # Flask 主程序入口
│   ├── application.yml          # 后端配置文件
│   ├── resume_routes.py         # 简历上传/解析等接口定义
│   ├── utils/                   # Python 工具函数
│   ├── database/                # 数据库操作封装（连接池、模型等）
│   ├── crawler/                 # Playwright 自动化爬虫模块
│   ├── cache/                   # 本地缓存（简历、任务队列等）
│   └── agent/                   # 与 OpenAI 模型交互逻辑（问答、摘要等）

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
│                   ├── entity/                    # 实体类（数据库表结构映射）
│                   ├── exception/                 # 全局异常处理
│                   ├── handle/                    # 通用处理器（如响应封装、拦截器处理）
│                   ├── interceptor/               # 拦截器（如登录校验、日志记录）
│                   ├── mapper/                    # MyBatis 映射接口（与数据库交互）
│                   ├── service/                   # 业务逻辑层
│                   │   └── impl/                  # 业务实现类
│                   ├── utils/                     # 工具类（如加解密、Token处理）
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
