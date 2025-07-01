from constant import *
from typing import List
from database.connector import db_pool

class JobQuery:
    def __init__(self, 
        userId: int,                # 用户ID    
        keyword: str='',            # 搜索关键词
        city: List[str]=[],         # 城市名称
        experience: List[str]=[],   # 经验要求
        degree: List[str]=[],       # 学历要求
        industry: List[str]=[],     # 行业
        scale: List[str]=[],        # 公司人员规模
        stage: List[str]=[],        # 融资情况
        jobType: str='',            # 职位性质
        title: str='',              # 职位类型
        salary: List[str]=[],       # 薪资范围
        areaBusiness: str='',       # 区域商圈
        limit: int=300,             # 最大返回数量
    ):
        self.userId = userId
        expereinces = []
        for exp in experience:
            exp_id = EXPERIENCE.get(exp, '')
            if exp_id:
                expereinces.append(exp_id)
        self.experience = ','.join(expereinces)
        if isinstance(city, str):
            city = [city]
        self.title = title
        
        self.jobType = JOBTYPE.get(jobType, '')
        self.limit = limit
                
        salaries = []
        for sal in salary:
            sal_id = SALARY.get(sal, '')
            if sal_id:
                salaries.append(sal_id)
        self.salary = ','.join(salaries)
                
        degrees = []
        for deg in degree:
            deg_id = DEGREE.get(deg, '')
            if deg_id:
                degrees.append(deg_id)
        self.degree = ','.join(degrees)
        
        scales = []
        for sc in scale:
            sc_id = SCALE.get(sc, '')
            if sc_id:
                scales.append(sc_id)
        self.scale = ','.join(scales)
        
        stages = []
        for st in stage:
            st_id = STAGE.get(st, '')
            if st_id:
                stages.append(st_id)
        self.stage = ','.join(stages)
        
        self.query = keyword
        
        if title:
            results = db_pool.execute("SELECT DISTINCT code FROM title WHERE name=%s", (title,))
            if results and len(results):
                self.position = results[0][0]
            
        cities = []
        if not city:
            self.cities = "100010000"  # 全国
        else:
            for city in city:
                results = db_pool.execute("SELECT DISTINCT city_id FROM city WHERE city=%s", (city,))
                if results and len(results):
                    cities.append(results[0][0])
            self.city = ','.join(cities)
        
        if areaBusiness:
            results = db_pool.execute("SELECT DISTINCT region_code FROM city WHERE city=%s AND region=%s", (city, areaBusiness))
            if results and len(results):
                self.areaBusiness = results[0][0]
                
        industries = []
        for industry in industry:
            results = db_pool.execute("SELECT DISTINCT code FROM industry WHERE subtype=%s", (industry,))
            if results and len(results):
                industries.append(results[0][0])
        self.industry = ','.join(industries)

    def to_url(self):
        base_url = "https://www.zhipin.com/web/geek/job?"
        params = '&'.join([f'{k}={v}' for k, v in self.to_dict().items() if v])
        return base_url + params
    
    def to_dict(self):
        return self.__dict__
    
    def __str__(self):
        str = self.__class__.__name__ + ':\n'
        for attr in self.__dict__:
            str += f'{attr}: {self.__dict__[attr]}\n'
        return str + '\n'
    