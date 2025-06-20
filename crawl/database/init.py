from database.connector import db_pool
from utils.tools import md5_encrypt
from loguru import logger


import json

def init_city_table(tables):
    
    if 'city' not in tables:
        logger.info('创建 city 表')
        db_pool.execute('''
            CREATE TABLE city (
                province VARCHAR(20) NOT NULL COMMENT '省份',
                city VARCHAR(20) NOT NULL COMMENT '城市',
                region VARCHAR(20) NOT NULL COMMENT '区域',
                city_id VARCHAR(20) NOT NULL COMMENT '城市id',
                province_code VARCHAR(20) NOT NULL COMMENT '省份代码',
                city_code VARCHAR(20) NOT NULL COMMENT '城市代码',
                region_code VARCHAR(20) NOT NULL COMMENT '区域代码/邮编',
                longitude FLOAT NOT NULL COMMENT '经度',
                latitude FLOAT NOT NULL COMMENT '纬度',
                PRIMARY KEY (province, city, region),
                CHECK (longitude >= -180 AND longitude <= 180),
                CHECK (latitude >= -90 AND latitude <= 90)
            )'''
        )
    else:
        logger.info('city 表已存在')
        
    cities = db_pool.execute("SELECT * FROM city")
    if len(cities) == 0:
        logger.info('插入城市信息')
        with open('metadata/city.json', 'r', encoding='utf-8') as f:
            province_list = json.load(f)["cityList"]
        for province in province_list:
            province_name = province["name"]
            province_code = province["regionCode"]
            for city in province["subLevelModelList"]:
                city_name = city["name"]
                city_id = city["code"]
                city_code = city["regionCode"]
                if not city["subLevelModelList"]:
                    continue
                for region in city["subLevelModelList"]:
                    region_name = region["name"]
                    region_code = region["regionCode"]
                    region_center_geo = region["centerGeo"]
                    longitude = region_center_geo.split(",")[0]
                    latitude = region_center_geo.split(",")[1]
                    db_pool.execute('''
                        INSERT INTO city (province, city, province_code, region, city_code, city_id, region_code, longitude, latitude)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''', (province_name, city_name, province_code, region_name, city_code, city_id, region_code, longitude, latitude)
                    )
    else:
        logger.info('city 数据已存在')

def init_industry_table(tables):
    
    if 'industry' not in tables:
        logger.info('创建 industry 表')
        db_pool.execute('''
            CREATE TABLE industry (
                type VARCHAR(20) NOT NULL COMMENT '行业类型',
                subtype VARCHAR(20) NOT NULL COMMENT '行业细分类型',
                code VARCHAR(20) NOT NULL COMMENT '行业代码',
                PRIMARY KEY (code)
            )'''
        )
    else:
        logger.info('industry 表已存在')
        
    industries = db_pool.execute("SELECT * FROM industry")
    if len(industries) == 0:
        logger.info('插入行业信息')
        with open('metadata/industry.json', 'r', encoding='utf-8') as f:
            industry_list = json.load(f)["zpData"]
        for industry in industry_list:
            industry_type = industry["name"]
            for sub_industry in industry["subLevelModelList"]:
                industry_subtype = sub_industry["name"]
                industry_code = sub_industry["code"]
                db_pool.execute('''
                    INSERT INTO industry (type, subtype, code)
                    VALUES (%s, %s, %s)
                    ''', (industry_type, industry_subtype, industry_code)
                )
    else:
        logger.info('industry 数据已存在')

def init_title_table(tables):
    if 'title' not in tables:
        logger.info('创建 title 表')
        db_pool.execute('''
            CREATE TABLE title (
                type VARCHAR(20) NOT NULL COMMENT '岗位类型',
                name VARCHAR(20) NOT NULL COMMENT '岗位名称',
                code VARCHAR(20) NOT NULL COMMENT '岗位代码',
                description VARCHAR(200) NOT NULL COMMENT '岗位描述'
            )'''
        )
    else:
        logger.info('title 表已存在')
        
    titles = db_pool.execute("SELECT * FROM title")
    if len(titles) == 0:
        logger.info('插入职位类型信息')
        with open('metadata/title.json', 'r', encoding='utf-8') as f:
            title_list = json.load(f)["zpData"]
        for title in title_list:
            title_type = title["name"]
            for sub_title in title["subList"]:
                title_name = sub_title["name"]
                title_code = sub_title["positionCode"]
                title_description = sub_title["level2Description"]
                db_pool.execute('''
                    INSERT INTO title (type, name, code, description)
                    VALUES (%s, %s, %s, %s)
                    ''', (title_type, title_name, title_code, title_description)
                    )
    else:
        logger.info('title 数据已存在')

def init_company_table(tables):
    if 'company' not in tables:
        logger.info('创建 company 表')
        db_pool.execute('''
            CREATE TABLE company (
                id VARCHAR(40) NOT NULL COMMENT '公司id',
                name VARCHAR(100) NOT NULL COMMENT '公司名称',
                stage VARCHAR(20) COMMENT '公司融资阶段',
                scale VARCHAR(30) COMMENT '公司人员规模',
                welfare VARCHAR(200) COMMENT '公司福利'
            )'''
        )
    else:
        logger.info('company 表已存在')
                

def init_job_table(tables):
    if 'job' not in tables:
        logger.info('创建 job 表')
        db_pool.execute('''
            CREATE TABLE job (
                id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, -- 自增主键，方便关联
                securityId VARCHAR(200) NOT NULL COMMENT '职位id' UNIQUE,
                jobName VARCHAR(100) NOT NULL COMMENT '职位名称',
                jobType VARCHAR(20) NOT NULL COMMENT '职位性质',
                companyId VARCHAR(50) NOT NULL COMMENT '公司id',
                url VARCHAR(500) COMMENT '职位链接',
                salary VARCHAR(40) COMMENT '薪水',
                salaryFloor INTEGER COMMENT '最低薪水',
                salaryCeiling INTEGER COMMENT '最高薪水',
                crawlDate DATE COMMENT '获取职位时的日期',
                city VARCHAR(20) NOT NULL COMMENT '城市',
                region VARCHAR(20) COMMENT '城市区域',
                experience VARCHAR(20) COMMENT '工作经验要求',
                degree VARCHAR(20) COMMENT '学历要求',
                industry VARCHAR(20) COMMENT '行业',
                title VARCHAR(30) COMMENT '职位类型',    
                skills VARCHAR(300) COMMENT '工作技能需求标签',
                description TEXT COMMENT '职位描述',
                UNIQUE KEY unique_job (jobName, city, companyId)
                FOREIGN KEY (companyId) REFERENCES company(id)
            )'''
        )
    else:
        logger.info('job 表已存在')
        
def init_search_job_table(tables):
    if'search_job' not in tables:
        logger.info('创建 search_job 表')
        db_pool.execute('''
            CREATE TABLE search_job (
                id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                userId VARCHAR(50) NOT NULL COMMENT '用户id',
                securityId VARCHAR(200) NOT NULL COMMENT '职位id' UNIQUE,
                jobName VARCHAR(100) NOT NULL COMMENT '职位名称',
                jobType VARCHAR(20) NOT NULL COMMENT '职位性质',
                companyId VARCHAR(50) NOT NULL COMMENT '公司id',
                url VARCHAR(500) COMMENT '职位链接',
                salary VARCHAR(40) COMMENT '薪水',
                salaryFloor INTEGER COMMENT '最低薪水',
                salaryCeiling INTEGER COMMENT '最高薪水',
                crawlDate DATE COMMENT '获取职位时的日期',
                city VARCHAR(20) NOT NULL COMMENT '城市',
                region VARCHAR(20) COMMENT '城市区域',
                experience VARCHAR(20) COMMENT '工作经验要求',
                degree VARCHAR(20) COMMENT '学历要求',
                industry VARCHAR(20) COMMENT '行业',
                title VARCHAR(30) COMMENT '职位类型',    
                skills VARCHAR(300) COMMENT '工作技能需求标签',
                description TEXT COMMENT '职位描述',
                companyName VARCHAR(100) NOT NULL COMMENT '公司名称',
                stage VARCHAR(20) COMMENT '公司融资阶段',
                scale VARCHAR(30) COMMENT '公司人员规模',
                welfare VARCHAR(200) COMMENT '公司福利',
                UNIQUE KEY unique_job (jobName, city, companyId)
            )'''
        )
    else:
        logger.info('job 表已存在')

def init_other_tables(tables):
    if 'user' not in tables:
        logger.info('创建 user 表')
        db_pool.execute('''
            CREATE TABLE user (
                id INT NOT NULL AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL,
                PRIMARY KEY (id)
            )'''
        )
    else:
        logger.info('user 表已存在')
        
    result = db_pool.execute("SELECT * FROM user where username='admin'")
    if len(result) == 0:
        password = md5_encrypt('123456')
        db_pool.execute(f'''
            INSERT INTO user (username, password)
            VALUES ('admin', %s)
            ''', (password,)
        )
        
    if 'user_job' not in tables:
        logger.info('创建 user_job 表')
        db_pool.execute('''
            CREATE TABLE user_job (
                id INT NOT NULL AUTO_INCREMENT,
                user_id INT NOT NULL,
                job_id BIGINT NOT NULL,
                viewed BOOLEAN NOT NULL DEFAULT 0,
                sent_cv BOOLEAN NOT NULL DEFAULT 0,
                UNIQUE KEY unique_user_job (user_id, job_id),
                PRIMARY KEY (id),
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (job_id) REFERENCES job(id)
            )'''
        )
    else:
        logger.info('user_job 表已存在')
        
    if 'user_rule' not in tables:
        logger.info('创建 user_rule 表')
        db_pool.execute('''
            CREATE TABLE user_rule (
                id INT NOT NULL AUTO_INCREMENT,
                rule_name VARCHAR(50) NOT NULL UNIQUE,
                rule_description TEXT,
                user_id INT NOT NULL,
                keyword VARCHAR(300),
                city VARCHAR(300),
                degree VARCHAR(300),
                industry VARCHAR(300),
                title VARCHAR(300),
                experience VARCHAR(300),
                scale VARCHAR(300),
                stage VARCHAR(300),
                limit_num INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        ''')
    else:
        logger.info('user_rule 表已存在')

def create_tables():
    databases = db_pool.execute("SHOW DATABASES")
    if databases is None:
        logger.error('无法连接数据库')
        return

    try:
        tables = db_pool.execute("SHOW TABLES")
        tables = [x[0] for x in tables]
        init_city_table(tables)
        init_industry_table(tables) 
        init_title_table(tables)   
        init_job_table(tables) 
        init_company_table(tables)
        init_other_tables(tables)
            
    except Exception as e:
        logger.error(e)
        
    logger.success('数据库初始化完成')