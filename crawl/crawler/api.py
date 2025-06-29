from crawler.requestHelper import Request
from crawler.query import JobQuery
from database.jobinfo import InsertDTO, JobInfo
from utils.tools import get_user_id
from typing import List
from loguru import logger
import datetime
import random
import time
import json

def get_job_detail(securityId, user_id=None):
    if user_id is None:
        user_id = get_user_id()
    url = "https://www.zhipin.com/wapi/zpgeek/job/detail.json"
    params = {
        "securityId": securityId,
    }
    response = Request.get(user_id, url, params=params)
    data = response.json()
    if data["code"] == 0:
        jobDetail = data["zpData"]
        print(json.dumps(jobDetail, indent=4, ensure_ascii=False))
        return jobDetail
    else:
        return None
    
def convert_json_to_job(title: str, js: dict) -> JobInfo:
    jobinfo = JobInfo()
    jobinfo.securityId_(js["securityId"]).jobName_(js["jobName"]).jobType_(js["jobType"]).salary_(js["salaryDesc"])\
        .crawlDate_(datetime.datetime.now().strftime("%Y-%m-%d")).city_(js["cityName"]).region_(js["areaDistrict"]).experience_(js["jobExperience"])\
        .degree_(js["jobDegree"]).industry_(js["brandIndustry"]).title_(title).skills_(','.join(js["skills"])).companyId_(js["encryptBrandId"])\
        .companyName_(js["brandName"]).stage_(js["brandStageName"]).scale_(js["brandScaleName"]).welfare_(','.join(js["welfareList"]))\
        .url_(f'https://www.zhipin.com/job_detail/{js["encryptJobId"]}.html')
    
    salary = jobinfo.salary
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
        
    jobinfo.salaryCeiling_(int(salaryCeiling)).salaryFloor_(int(salaryFloor))
    logger.info(f"{jobinfo.title} | {jobinfo.jobName} | {jobinfo.city} | {jobinfo.companyName}")
    return jobinfo
    

def get_job_list(query: JobQuery, job_status=None, user_id: str=None, filter_hash: str=None, token: str=None) -> InsertDTO:
    # url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    url = "https://www.zhipin.com/wapi/zpgeek/pc/recommend/job/list.json"
    num = 0
    jobInfoList: List[JobInfo] = []
    while True:
        if job_status:
            status = job_status.get(user_id, {}).get('running', 1)
            if status == 0:
                print("停止运行")
                return InsertDTO(user_id, jobInfoList, filter_hash, token)
        params = {
            "page": random.randint(1, 10),
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
        if user_id is None:
            user_id = get_user_id()
        response = Request.get(user_id, url, params=params)
        try:
            data = response.json()
        except:
            logger.error(f"获取岗位列表失败，url: {url}, params: {params}")
            return
        if data["code"] == 0:
            zpData = data["zpData"]
            jobList = zpData["jobList"]
            for job in jobList:
                jobinfo = convert_json_to_job(query.title, job)
                jobInfoList.append(jobinfo)
                num += 1
                if num >= query.limit:
                    return InsertDTO(user_id, jobInfoList, filter_hash, token)
            if zpData["hasMore"] == False:
                params["page"] = random.randint(1, max(2, params["page"]-5))        # 使用随机页数避免重复抓取
            else:
                params["page"] = random.randint(1, params["page"]+10)
        else:
            break
        if job_status:
            status = job_status.get(user_id, {}).get('running', 1)
            if status == 0:
                print("停止运行")
                return InsertDTO(user_id, jobInfoList, filter_hash, token)
        time.sleep(3)
    return InsertDTO(user_id, jobInfoList, filter_hash, token)