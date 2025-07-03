from datetime import datetime
from utils.tools import builder 
from typing import List
from constant import INSERT_URL, TOKEN_EXPIRED_CODE, DESC_URL
from utils.tools import get_headers
from loguru import logger
import requests

@builder
class JobInfo:
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
    def __init__(self, userId: str, jobs: List[JobInfo], filterHash: str):
        self.userId = userId
        self.jobs = jobs
        self.filterHash = filterHash or ""
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
        response = requests.post(DESC_URL, json=params, headers=self.headers)
        if response.status_code == 200:
            result = response.json()["data"]
            return result
        elif response.status_code == TOKEN_EXPIRED_CODE:
            self.headers = get_headers(self.userId, reload=True)
            return self.get_result()
    
    