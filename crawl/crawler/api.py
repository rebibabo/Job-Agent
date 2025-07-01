from crawler.requestHelper import Request
from crawler.query import JobQuery
from agent.resume import ResumeLoader
from crawler.token import login
from playwright.sync_api import sync_playwright
from database.jobinfo import InsertDTO, JobInfo
from uiautomation import WindowControl
from utils.tools import get_user_id
from typing import List
from loguru import logger
from constant import LOGIN_URL, QUERY_URL, LIST_URL
from utils.configLoader import inject_config
from utils.tools import md5_encrypt
import datetime
import requests
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
        jobDetail = data["zpData"]["jobInfo"]["postDescription"]
        print(json.dumps(jobDetail, indent=4, ensure_ascii=False))
        return jobDetail
    else:
        return None
    
def convert_json_to_job(title: str, js: dict, user_id=None, get_desc: bool=False) -> JobInfo:
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
    if get_desc:
        description = get_job_detail(jobinfo.securityId, user_id)
        time.sleep(0.5)
        if description:
            jobinfo.description_(description)
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
                jobinfo = convert_json_to_job(query.title, job, user_id)
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

def get_job_list_with_desc(query: JobQuery, job_status=None, user_id: str=None, filter_hash: str=None, token: str=None) -> InsertDTO:
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
                jobinfo = convert_json_to_job(query.title, job, user_id)
                jobInfoList.append(jobinfo)
                num += 1
                if num >= query.limit:
                    return InsertDTO(user_id, jobInfoList, filter_hash, token)
            if zpData["hasMore"] == False:
                params["page"] += 1
            else:
                break
        else:
            break
        if job_status:
            status = job_status.get(user_id, {}).get('running', 1)
            if status == 0:
                print("停止运行")
                return InsertDTO(user_id, jobInfoList, filter_hash, token)
        time.sleep(3)
    return InsertDTO(user_id, jobInfoList, filter_hash, token)

@inject_config("application.yml", "user")
class GetJobs:    
    def __init__(self):
        response = requests.post(LOGIN_URL, json={"username": self.config["username"], "password": md5_encrypt(self.config["password"])})
        self.headers = {"token": response.json()["data"]["token"]}
    
    def get_jobs_by_ids(self, job_ids: List[int], user_id: str=None, max_num: int=100) -> List[JobInfo]:
        params = {
            "jobIds": ",".join(map(str, job_ids)),
            "maxNum": max_num,
            "userId": user_id or get_user_id()
        }
        response = requests.post(LIST_URL, json=params, headers=self.headers)
        if response.status_code == 200:
            jobList = []
            data = response.json()
            for job in data["data"]["items"]:
                jobinfo = JobInfo.from_dict(job)
                jobList.append(jobinfo)
            return jobList
        else:
            return []

def send_cv(user_id, jobs: List[JobInfo], cv_path, message):
    cache_dir = f"cache/{user_id}"
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    loader = ResumeLoader(cv_path)
    png_path = loader.picture_path
    context = login(browser, cache_dir)
    page = context.new_page()
    for job in jobs:
        if job.sentCv:     # 跳过已发送的岗位
            continue
        page.goto(job.url, wait_until="networkidle")
        if page.locator(".btn-more").count() > 0:       # 该职位已关闭
            continue        
        page.locator(".btn-container .btn-startchat").click()       # 立即沟通
        page.wait_for_timeout(1000)
        if page.locator(".dialog-title .icon-close").count() > 0:
            page.locator(".dialog-title .icon-close").click()       # 关闭弹窗
            page.locator(".btn-container .btn-startchat").click()   # 再次点击立即沟通
        page.wait_for_selector("#chat-input")
        input_box = page.locator("#chat-input")
        input_box.fill(message)
        page.wait_for_timeout(2000)
        page.locator("button[type=send]").click()
        page.wait_for_timeout(2000)
        page.locator(".toolbar-btn-content [type=file]").click()            # 点击发送简历照片
        page.wait_for_timeout(1000)
        openWindow = WindowControl(name='打开')
        openWindow.SwitchToThisWindow()
        openWindow.EditControl(Name='文件名(N):').SendKeys(png_path)
        time.sleep(1)
        openWindow.ButtonControl(Name='打开(O)').Click()
        page.wait_for_selector(".item-image")       # 等待发送图片出去再退出
    context.close()
    browser.close()
    playwright.stop()