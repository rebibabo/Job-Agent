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
    cookies = {
        "lastCity": "101280100",
        "ab_guid": "8414e985-90be-46a1-a608-66e102e1e653",
        "__zp_seo_uuid__": "7d078ad1-392d-485b-b01e-dd3c46de87c2",
        "__g": "-",
        "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1750060305,1751160840",
        "HMACCOUNT": "9F2B10F1A9B9D90B",
        "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a": "1751160857",
        "__l": "r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fuser%2F%3Fka%3Dheader-login&s=3&friend_source=0&s=3&friend_source=0",
        "__zp_stoken__": "1a7bfwrk5CjgEWHVcCl1zTMK5wrlUecK3VMKlwoHCrnzCv1BsdlxpX3teRsK1wqLCu07Cr2fCrcKww7NpwqPClcK7S8KcwqXCo17DvcKTwpPElsOnwqnFgcKew4DCucKcOTEGAwcICAoPCwwMCw4HCAgIBQkGBhEMEA8POS3DtcOlwpI3MzoyJE1QTARQXFpFYUQCVERFMjgJCQoROC81MjI0wrs1wr1Kwr45wrpKw4A0wr7ClTI6NDnCtsOxJyLCsz5XwrLCoAXCtsORDmoFwrXCiAbDhGFVwpNQwrdBMTg4wrTEuDo5FDoyNjs5N0E2OSQ3E8OFWlLClUvCth0pNBI%2BOTk%2BNDY5OUAyPCU5Py4kOTIkPgYLCggRJzzCtsKVwrnDoDk5",
        "__c": "1751155114",
        "__a": "11520517.1722925713.1750060305.1751155114.304.11.12.70"
    }

    fetcher = None
    max_retry = 10
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
    
    