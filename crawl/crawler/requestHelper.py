import requests
from functools import wraps
from crawler.token import TokenFetcher
from loguru import logger

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
                        if isinstance(data, dict) and data.get("code") != 0:
                            logger.warning(f"Error occurred: {response.text}. Retry {i+1}/{max_retries}...")
                            Request.update_zp_token()
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
        "referer": "https://www.zhipin.com/web/geek/jobs?city=101280100&query=%E5%A4%A7%E6%95%B0%E6%8D%AE%E5%BC%80%E5%8F%91",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "token": "xGC7UnpJmhYrN1l9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "x-requested-with": "XMLHttpRequest",
        "zp_token": "V2R98hEu3101tiVtRuyhwZKiyy7DrexSQ~|R98hEu3101tiVtRuyhwZKiyy7DrRwSU~"
    }
    cookies = {
        "lastCity": "101280100",
        "ab_guid": "8414e985-90be-46a1-a608-66e102e1e653",
        "__zp_seo_uuid__": "7d113f5a-e8b2-42c9-9b4c-0e5679162283",
        "__g": "sem_bingpc",
        "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1750060305",
        "HMACCOUNT": "9F2B10F1A9B9D90B",
        "wt2": "D2x5uJQUk5xuU49_j3BYnfoy6Jm72BLBNsutiH9kMWvOpUP97N4vkUZysTKEcfUIvqRmtgWfUM2GuyA_nWhsuHg~~",
        "wbg": "0",
        "zp_at": "y6LvMWV785CNYzJavy9FDyj-HDaYeinEqvCS5KcKUPc~",
        "__l": "r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fjob_detail%2Fd96867ae46f018e703B53t20EFRS.html&s=3&g=%2Fwww.zhipin.com%2Fsem%2F10.html%3F_ts%3D1750060303777%26sid%3Dsem_bingpc%26qudao%3Dbing_pc_H120003UY5%26plan%3DBOSS-%25E5%25BF%2585%25E5%25BA%2594-%25E5%2593%2581%25E7%2589%258C%26unit%3D%25E7%25B2%25BE%25E5%2587%2586%26keyword%3Dboss%25E7%259B%25B4%25E8%2581%2598%26msclkid%3Da3ec79b2f43618c9146a11fd393be347&friend_source=0&s=3&friend_source=0",
        "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a": "1750061909",
        "__zp_stoken__": "3638fw4%2FDpsOLFUEUFAsZExVUU8OGalLCv2zDgsKyfsOAfVN4ZltUwrvCumpnYmLCs8KzwqzCnsK5wrVnwrNTwrZ0wqJWwqdKwrlQwopPwpzEn8Otw4DCpsKvw4jCu8KiQzYNCwwYDQ4QDxMODhASDhMSFBMPEhEPEBQRQDbCjT0%2BP0Q%2FNlRUUgpKZWZLZ1YLYEpLSEENExMQQTNJRkg9w4Irw4Egw4I9w4HDrMK%2FPcK%2Fw6s8QD09w4HDnzUrwr7DuC3Dgy4RwrvCnxR5YMK7woxlw41laxBpwr3Cpzc%2BQsK9xLxEPyZDPkBFQz5FQD82PivDi2R4EVzCu8SEMz0eSD9DR0BAP0NJPkIrQ0V6Kj9ILUIUEhEUEzFCw4TDhsK9w6g%2FQw%3D%3D",
        "bst": "V2R98hEu3101tiVtRuyhwZKiyy7DrexSQ~|R98hEu3101tiVtRuyhwZKiyy7DrRwSU~",
        "__c": "1750060305",
        "__a": "11520517.1722925713.1738760655.1750060305.250.10.16.16"
    }

    fetcher = TokenFetcher()
    max_retry = 5
    request_cnt = max_retry

    @staticmethod
    def update_zp_token():
        _headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Origin": "https://www.zhipin.com",
            "Referer": "https://www.zhipin.com/web/geek/jobs",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "traceId": "F-a4ee0dM9V15eOYNY"
        }
        _cookies = {
            "lastCity": "101280100",
            "ab_guid": "8414e985-90be-46a1-a608-66e102e1e653",
            "__zp_seo_uuid__": "7d113f5a-e8b2-42c9-9b4c-0e5679162283",
            "__g": "sem_bingpc",
            "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1750060305",
            "HMACCOUNT": "9F2B10F1A9B9D90B",
            "wt2": "D2x5uJQUk5xuU49_j3BYnfoy6Jm72BLBNsutiH9kMWvOpUP97N4vkUZysTKEcfUIvqRmtgWfUM2GuyA_nWhsuHg~~",
            "wbg": "0",
            "zp_at": "y6LvMWV785CNYzJavy9FDyj-HDaYeinEqvCS5KcKUPc~",
            "bst": "V2R98hEu3101tiVtRuyhwZKiyy7DrfzCw~|R98hEu3101tiVtRuyhwZKiyy7DrfxSs~",
            "__c": "1750060305",
            "__l": "r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fjob_detail%2Fd96867ae46f018e703B53t20EFRS.html&s=3&g=%2Fwww.zhipin.com%2Fsem%2F10.html%3F_ts%3D1750060303777%26sid%3Dsem_bingpc%26qudao%3Dbing_pc_H120003UY5%26plan%3DBOSS-%25E5%25BF%2585%25E5%25BA%2594-%25E5%2593%2581%25E7%2589%258C%26unit%3D%25E7%25B2%25BE%25E5%2587%2586%26keyword%3Dboss%25E7%259B%25B4%25E8%2581%2598%26msclkid%3Da3ec79b2f43618c9146a11fd393be347&friend_source=0&s=3&friend_source=0",
            "__a": "11520517.1722925713.1738760655.1750060305.244.10.7.7",
        }
        url = "https://www.zhipin.com/wapi/zppassport/set/zpToken"
        response = requests.post(url, headers=_headers, cookies=_cookies)

        bst_cookie = response.cookies.get('bst')

        Request.cookies["bst"] = bst_cookie
        Request.headers["zp_token"] = bst_cookie
        Request.cookies["__zp_stoken__"] = Request.fetcher.get_token()
        
    
    @staticmethod
    @retry(max_retries=3)
    def get(url, params=None, headers=None, cookies=None):
        if Request.request_cnt == Request.max_retry:
            Request.update_zp_token()
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
    def post(url, data=None, json=None, headers=None, cookies=None):
        if Request.request_cnt == Request.max_retry:
            Request.update_zp_token()
            Request.request_cnt = 0
        Request.request_cnt += 1
        if headers is None:
            headers = Request.headers
        if cookies is None:
            cookies = Request.cookies
        response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        return response
    
    