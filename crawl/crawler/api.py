from re import DEBUG
from crawler.requestHelper import Request
from crawler.query import JobQuery
from agent.resume import ResumeLoader
from crawler.token import login
from playwright.sync_api import sync_playwright
from database.jobinfo import InsertDTO, JobInfo, WhetherAddDescDTO
from uiautomation import WindowControl
from typing import List
from loguru import logger
from constant import LIST_URL, TOKEN_EXPIRED_CODE, SETSTATUS_URL
from utils.configLoader import inject_config
from crawler.requestHelper import list_all_cookies
from utils.tools import generate_random_id, get_headers
from agent.filter import GPTFilter
from agent.polisher import polish_message
import datetime
import requests
import random
import time
import json

def get_job_detail(securityId, user_id):
    url = "https://www.zhipin.com/wapi/zpgeek/job/detail.json"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Referer": "https://www.zhipin.com/web/geek/jobs",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "traceId": "F-02158feHPbzT4n6W"
    }
    params = {
        "securityId": securityId,
    }
    cookies = list_all_cookies(f"cache/{user_id}")
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    data = response.json()
    if data["code"] == 0:
        jobDetail = data["zpData"]["jobInfo"]["postDescription"]
        logger.info(json.dumps(jobDetail, indent=4, ensure_ascii=False))
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
    
    if jobinfo.companyId == "":
        jobinfo.companyId = generate_random_id(28)
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
    

def get_job_list(query: JobQuery, user_id: str, status=None, filter_hash: str=None) -> InsertDTO:
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    # url = "https://www.zhipin.com/wapi/zpgeek/pc/recommend/job/list.json"
    num = 0
    jobInfoList: List[JobInfo] = []
    params = query.to_params(page=random.randint(1, 10))
    while True:
        if status and status.get('running', 1) == 0:
            logger.info("停止运行")
            return InsertDTO(user_id, jobInfoList, filter_hash)
        logger.info(params)
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
                    return InsertDTO(user_id, jobInfoList, filter_hash)
            if zpData["hasMore"] == False:
                params["page"] = random.randint(1, max(2, params["page"]-5))        # 使用随机页数避免重复抓取
            else:
                params["page"] = random.randint(1, params["page"]+10)
        else:
            break
        if status and status.get('running', 1) == 0:
            logger.info("停止运行")
            return InsertDTO(user_id, jobInfoList, filter_hash)
        time.sleep(3)
    return InsertDTO(user_id, jobInfoList, filter_hash)

def get_job_list_with_desc(query: JobQuery, user_id: str, status=None, increment: float=0, filter_hash: str=None) -> InsertDTO:
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    num = 0
    jobInfoList: List[JobInfo] = []
    maxNum = query.limit
    wad = WhetherAddDescDTO(user_id)
    params = query.to_params(page=1)
    
    while True:
        if status and status.get('running', 1) == 0:
            logger.info("停止运行")
            return InsertDTO(user_id, jobInfoList, filter_hash)
        logger.info(params)
        response = Request.get(user_id, url, params=params)
        try:
            data = response.json()
        except:
            logger.error(f"获取岗位列表失败，params: {params}")
            return
        if data["code"] == 0:
            zpData = data["zpData"]
            jobList = zpData["jobList"]
            for job in jobList:
                jobinfo = convert_json_to_job(query.title, job)
                # 判断是否存在岗位且description不为空且没有发送过简历
                if not wad.get_result(jobinfo.jobName, jobinfo.city, jobinfo.companyId):
                    logger.info("跳过该岗位")
                    continue 
                # 获取岗位描述信息
                description = get_job_detail(jobinfo.securityId, user_id)
                time.sleep(0.5)
                if description:
                    jobinfo.description_(description)
                    jobInfoList.append(jobinfo)
                    num += 1
                    status["percentage"] += increment
                    if num >= maxNum:
                        return InsertDTO(user_id, jobInfoList, filter_hash)
                    
                if status and status.get('running', 1) == 0:
                    logger.info("停止运行")
                    return InsertDTO(user_id, jobInfoList, filter_hash)
                
            if zpData["hasMore"] == True:
                params["page"] += 1
            else:        # 没有更多数据，退出循环
                break
        else:
            break
        
        time.sleep(3)
    return InsertDTO(user_id, jobInfoList, filter_hash)

@inject_config("application.yml", "user")
class GetJobs:    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.headers = get_headers(user_id)
    
    def get_jobs_by_ids(self, job_ids: List[int], max_num: int=100) -> List[JobInfo]:
        params = {
            "jobIds": ",".join(map(str, job_ids)),
            "maxNum": max_num,
            "userId": self.user_id
        }
        response = requests.post(LIST_URL, json=params, headers=self.headers)
        if response.status_code == 200:
            jobList = []
            data = response.json()
            for job in data["data"]["items"]:
                jobinfo = JobInfo.from_dict(job)
                jobList.append(jobinfo)
            return jobList
        elif response.status_code == TOKEN_EXPIRED_CODE:
            logger.info("token失效，重新登录")
            self.headers = get_headers(self.user_id, reload=True)
            return self.get_jobs_by_ids(job_ids, max_num)

def set_sent_status(user_id, job_id):
    params = {
        "job_id": job_id,
        "user_id": user_id
    }
    headers = get_headers(user_id, reload=True)
    requests.post(SETSTATUS_URL, json=params, headers=headers)
    
def send_cv(user_id, jobs: List[JobInfo], cv_path, message, polish, model, temperature, status=None):
    cache_dir = f"cache/{user_id}"
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    resume = ResumeLoader(cv_path)
    png_path = resume.picture_path
    context = login(browser, cache_dir)
    page = context.new_page()
    for i, job in enumerate(jobs):
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
        if polish:
            message = polish_message(message, resume.summary, job, model=model, temperature=temperature)
        logger.info(f"正在发送简历到{job.companyName}的{job.title}岗位，消息：{message}")
        # input_box.fill(message)
        # page.wait_for_timeout(2000)
        # page.locator("button[type=send]").click()
        # page.wait_for_timeout(2000)
        # page.locator(".toolbar-btn-content [type=file]").click()            # 点击发送简历照片
        # page.wait_for_timeout(1000)
        # openWindow = WindowControl(name='打开')
        # openWindow.SwitchToThisWindow()
        # openWindow.EditControl(Name='文件名(N):').SendKeys(png_path)
        # time.sleep(1)
        # openWindow.ButtonControl(Name='打开(O)').Click()
        # page.wait_for_selector(".item-image")       # 等待发送图片出去再退出
        set_sent_status(user_id, job.id)
        percentage = (i+1)/len(jobs) * 100
        if status:
            status["percentage"] = percentage
        logger.info(f"已发送{i+1}/{len(jobs)}个岗位，进度{percentage:.2f}%")
    if status:
        status["percentage"] = 100
        status["running"] = 0
    context.close()
    browser.close()
    playwright.stop()