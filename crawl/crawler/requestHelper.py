import requests
from functools import wraps
from crawler.token import TokenFetcher
from loguru import logger
import json

def list_all_cookies(cache_dir):
    with open(f"{cache_dir}/state.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        cookies = data.get("cookies", [])
        return {cookie["name"]: cookie["value"] for cookie in cookies}

def retry(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    # 如果返回的是Response对象，检查状态码或JSON
                    if hasattr(response, 'json'):
                        data = response.json()
                        user_id = kwargs.get("user_id", args[0] if args else None)
                        if isinstance(data, dict) and data.get("code") != 0:
                            logger.warning(f"Error occurred: {response.text}. Retry {i+1}/{max_retries}...")
                            Request.update_zp_token(user_id)
                            continue
                    return response
                except Exception as e:
                    logger.warning(f"Error occurred: {e}. Retry {i+1}/{max_retries}...")
                    if i == max_retries - 1:  # 最后一次重试仍然失败
                        raise
            logger.error(f"Failed to fetch data after {max_retries} retries.")
            return None
        return wrapper
    return decorator
    
class Request:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
        "priority": "u=1, i",
        "referer": "https://www.zhipin.com/web/geek/jobs?query=&city=101280100",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceid": "F-6ff9c2Auy65AiOPl",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = list_all_cookies("cache/1")

    fetcher = None
    max_retry = 50
    request_cnt = max_retry

    @classmethod
    def get_fetcher(cls, user_id):
        if cls.fetcher is None:
            cls.fetcher = TokenFetcher(user_id)
        return cls.fetcher
    
    @staticmethod
    def update_zp_token(user_id):
        fetcher = Request.get_fetcher(user_id)
        Request.cookies["__zp_stoken__"] = fetcher.get_token()
        
    
    @staticmethod
    @retry(max_retries=3)
    def get(user_id, url, params=None, headers=None, cookies=None):
        if Request.request_cnt == Request.max_retry:
            Request.update_zp_token(user_id)
            Request.request_cnt = 0
        Request.request_cnt += 1
        if headers is None:
            headers = Request.headers
        if cookies is None:
            cookies = Request.cookies
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        return response
    
    
    @staticmethod
    @retry(max_retries=3)
    def post(user_id, url, data=None, json=None, headers=None, cookies=None):
        if Request.request_cnt == Request.max_retry:
            Request.update_zp_token(user_id)
            Request.request_cnt = 0
        Request.request_cnt += 1
        if headers is None:
            headers = Request.headers
        if cookies is None:
            cookies = Request.cookies
        response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        return response
    
    