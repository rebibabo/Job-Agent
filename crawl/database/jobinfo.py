from datetime import datetime
from utils.tools import builder, md5_encrypt 
from typing import List
from constant import INSERT_URL, LOGIN_URL
from utils.configLoader import inject_config
from loguru import logger
import requests

@builder
class JobInfo:
    securityId: str   
    jobName: str
    jobType: str
    companyId: str
    companyName: str
    url: str
    salary: str
    salaryFloor: int
    salaryCeiling: int
    crawlDate: datetime
    city: str
    region: str
    experience: str
    degree: str
    industry: str
    title: str
    skills: str
    description: str
    scale: str
    stage: str
    welfare: str
    id: str
    viewed: bool
    sentCv: bool
    
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
        obj.__post_init__()  # 调用清理方法
        return obj
    
    def __str__(self):
        str = self.__class__.__name__ + ':\n'
        for attr in self.__dict__:
            str += f'{attr}: {self.__dict__[attr]}\n'
        return str + '\n'

@inject_config("application.yml", "user")
class InsertDTO:
    token: str
    
    def __init__(self, userId: str, jobs: List[JobInfo], filterHash: str, token: str=None):
        self.userId = userId
        self.jobs = jobs
        self.filterHash = filterHash or ""
        self.get_token()
            
    def get_token(self):
        response = requests.post(LOGIN_URL, json={"username": self.config["username"], "password": md5_encrypt(self.config["password"])})
        InsertDTO.token = response.json()["data"]["token"]
            
    def commit_to_db(self):
        params = {
            "userId": self.userId,
            "filterHash": self.filterHash,
            "jobs": [job.to_dict() for job in self.jobs],
        }
        headers = {
            "token": InsertDTO.token
        }
        response = requests.post(INSERT_URL, json=params, headers=headers)
        if response.status_code == 200:
            logger.success(response.json()["data"])
            return True
        elif response.status_code == 401:
            print("登录已过期，重新登录")
            self.get_token()
            self.commit_to_db()
        return False