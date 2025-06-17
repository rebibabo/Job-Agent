from datetime import datetime
from database.entity import Entity
from utils.tools import builder

@builder
class Job(Entity):
    securityId: str   
    lid: str          
    jobName: str
    jobType: str
    companyId: str
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
    table_name:str = "job"
    key_name : str= "lid"
    
    def __post_init__(self):
        self.region = self.region.strip()
        self.degree = self.degree.strip()
        self.city = self.city.strip()
        
    