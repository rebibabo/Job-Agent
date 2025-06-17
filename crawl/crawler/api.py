from crawler.requestHelper import Request
from crawler.query import JobQuery
from database.job import Job
from database.company import Company
from utils.tools import generate_random_id
from loguru import logger
import datetime
import time
import json

def get_job_detail(securityId):

    url = "https://www.zhipin.com/wapi/zpgeek/job/detail.json"
    params = {
        "securityId": securityId,
    }
    response = Request.get(url, params=params)
    data = response.json()
    if data["code"] == 0:
        jobDetail = data["zpData"]
        print(json.dumps(jobDetail, indent=4, ensure_ascii=False))
        return jobDetail
    else:
        return None
    
def save_job_to_db(title: str, js: dict) -> Job:
    if Job.from_db(js["lid"]):
        logger.warning(f"岗位已存在，lid: {js['lid']}.")
        return None
    
    job = Job()
    job.securityId_(js["securityId"]).lid_(js["lid"]).jobName_(js["jobName"]).jobType_(js["jobType"]).salary_(js["salaryDesc"])\
        .crawlDate_(datetime.datetime.now().strftime("%Y-%m-%d")).city_(js["cityName"]).region_(js["areaDistrict"]).experience_(js["jobExperience"])\
        .degree_("jobDegree").industry_(js["brandIndustry"]).title_(title).skills_(','.join(js["skills"]))
        
    companyId = js["encryptBrandId"]
    if not companyId:
        companyId = generate_random_id(28)
    job.companyId_(companyId)
    
    company = Company()
    company.id_(companyId).name_(js["brandName"]).stage_(js["brandStageName"]).scale_(js["brandScaleName"]).welfare_(','.join(js["welfareList"]))
    company.commit_to_db()
    
    job.url_(f'https://www.zhipin.com/job_detail/{js["encryptJobId"]}.html')
    salary = job.salary
    try:
        if '面议' in salary:      # 计算不准确薪资，跳过
            salary = '薪资面议'
            salaryFloor = 0
            salaryCeiling = 0
        elif '天' in salary:
            salaryFloor = int(salary.split('-')[0])*30
            salaryCeiling = int(salary.split('-')[1].split('元')[0])*30
        else:
            if '薪' in salary:
                months = int(salary.split('·')[1][:-1])     # 月薪 * (12 - 18)
            else:
                months = 12
            if 'K' in salary:       # 薪资单位为K
                prefix = salary.split('K')[0]
                salaryFloor = int(prefix.split('-')[0])*months*1000      # 最低薪资
                salaryCeiling = int(prefix.split('-')[1])*months*1000      # 最高薪资
            elif '元' in salary:    # 薪资单位为元
                prefix = salary.split('元')[0]
                salaryFloor = int(prefix.split('-')[0])*months
                salaryCeiling = int(prefix.split('-')[1])*months
            else:
                salary = '薪资未知'
                salaryFloor = 0
                salaryCeiling = 0
    except:
        salary = '薪资未知'
        salaryFloor = 0
        salaryCeiling = 0
        
    job.salaryCeiling_(int(salaryCeiling)).salaryFloor_(int(salaryFloor))
    job.commit_to_db()
    logger.success(f"岗位信息保存成功 ==> {title} | {job.jobName} | {job.city} | {company.name}")
    
    return job
    

def get_job_list(query: JobQuery, max_num=1000):
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    num = 0
    while True:
        params = {
            "page": 1,
            "pageSize": "30",       # 最大是30
            "city": query.city,
            "jobType": query.jobType,
            "salary": query.salary,
            "experience": query.experience,
            "degree": query.degree,
            "industry": query.industry,
            "scale": query.scale,
            "query": query.query,
            "position": query.position
        }
        response = Request.get(url, params=params)
        try:
            data = response.json()
        except:
            logger.error(f"获取岗位列表失败，url: {url}, params: {params}")
            return
        if data["code"] == 0:
            zpData = data["zpData"]
            jobList = zpData["jobList"]
            for job in jobList:
                save_job_to_db(query.title, job)
                num += 1
                if num >= max_num:
                    return
            if zpData["hasMore"] == False:
                break
            else:
                params["page"] += 1
        else:
            break
        
        time.sleep(3)
        