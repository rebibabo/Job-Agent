from datetime import datetime
from utils.tools import builder 
from typing import List
from constant import INSERT_URL, TOKEN_EXPIRED_CODE, DESC_URL
from utils.tools import get_headers
from loguru import logger
import requests

@builder
class JobInfo:
    # 职位信息类，跨三张表: job, company, user_job
    securityId: str = ""
    jobName: str = ""
    jobType: str = ""
    companyId: str = ""
    companyName: str = ""
    url: str = ""
    salary: str = ""
    salaryFloor: int = 0
    salaryCeiling: int = 0
    crawlDate: datetime = datetime.now()
    city: str = ""
    region: str = ""
    experience: str = ""
    degree: str = ""
    industry: str = ""
    title: str = ""
    skills: str = ""
    description: str = ""
    scale: str = ""
    stage: str = ""
    welfare: str = ""
    id: str = ""
    viewed: bool = False
    sentCv: bool = False
    
    def __post_init__(self):
        self.region = self.region.strip()
        self.degree = self.degree.strip()
        self.city = self.city.strip()
        self.companyName = self.companyName.strip()
        self.stage = self.stage.strip()
        self.scale = self.scale.strip()
        
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, js):
        # 工厂方法，从字典中创建对象
        allowed_keys = set(cls.__annotations__.keys())
        obj = cls.__new__(cls)  # 创建空实例，不调用 __init__
        for k, v in js.items():
            if k in allowed_keys:
                setattr(obj, k, v)
        return obj
    
    def __str__(self):
        str = self.__class__.__name__ + ':\n'
        for attr in self.__dict__:
            str += f'{attr}: {self.__dict__[attr]}\n'
        return str + '\n'

class InsertDTO:    
    # 插入数据库的数据传输类
    def __init__(self, userId: str, jobs: List[JobInfo], filterHash: str):
        self.userId = userId    # 用户id
        self.jobs = jobs        # 职位列表
        self.filterHash = filterHash or ""      # 过滤hash值
        self.headers = get_headers(userId)       
            
    def commit_to_db(self):
        params = {
            "userId": self.userId,
            "filterHash": self.filterHash,
            "jobs": [job.to_dict() for job in self.jobs],
        }
        response = requests.post(INSERT_URL, json=params, headers=self.headers)
        if response.status_code == 200:
            logger.success(response.json()["data"])
            return True
        elif response.status_code == TOKEN_EXPIRED_CODE:
            self.headers = get_headers(self.userId, reload=True)
            self.commit_to_db()
        return False
    
class WhetherAddDescDTO:
    # 是否需要插入岗位描述信息的传输类
    def __init__(self, userId: str):
        self.userId = str(userId)
        self.headers = get_headers(userId)
        
    def get_result(self, jobName, city, companyId) -> bool:
        params = {
            "userId": self.userId,
            "jobName": jobName,
            "city": city,
            "companyId": companyId
        }
        # 根据city, companyId, jobName定位唯一岗位，如果不存在，则需要插入，如果存在且描述为空，则需要更新，返回true，否则不需要更新，返回false。
        response = requests.post(DESC_URL, json=params, headers=self.headers)
        if response.status_code == 200:
            result = response.json()["data"]
            return result
        elif response.status_code == TOKEN_EXPIRED_CODE:
            self.headers = get_headers(self.userId, reload=True)
            return self.get_result()
    
    