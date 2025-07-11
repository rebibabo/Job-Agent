from playwright.sync_api import sync_playwright
from loguru import logger
import os

def wait_for_disappear(page, cssselector, message=None, timeout=30):
    # 等待CSS选择器消失
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if page.locator(cssselector).count() == 0:
                return True
        except:
            if message is None:
                logger.info("等待元素消失超时")
            else:
                logger.info(message)
            pass
        time.sleep(1)
    return False

def login(browser, cache_dir):
    # 登录Boss直聘，并获取登录状态上下文信息
    if os.path.exists(f"{cache_dir}/state.json"): # 如果存在缓存，则直接使用缓存登录
        logger.info(f"使用缓存登录，缓存目录：{cache_dir}")
        context = browser.new_context(storage_state=f"{cache_dir}/state.json")
    else:
        context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.zhipin.com/guangzhou/?seoRefer=index", wait_until="networkidle")

    if not wait_for_disappear(page, '.yidun_intelli-tips', "发现登录异常，需要手动验证"):       # 此时需要手动验证（反反爬手段之一），点击按钮方可登录
        logger.error("验证失败")
        exit()
            
    if page.locator(".header-login-btn[ka=header-login]").count() > 0:  # 没有登录，可以使用微信扫码登录
        page.goto("https://www.zhipin.com/web/user/?ka=header-login")
        page.wait_for_timeout(3000)
        # if page.locator(".mini-app-login").count() == 0:
        #     logger.info("使用微信扫码登录")
        #     page.locator(".wx-login-btn").click()       # 选择微信扫码登录
        
        if wait_for_disappear(page, '.mini-app-login', "等待登录中..."):
            context.storage_state(path=f"{cache_dir}/state.json")       # 保存登录状态，下一次登录不需要扫码
            logger.info(f"登录成功, 保存状态至缓存目录：{cache_dir}")
        else:
            logger.error("登录失败")
            
    return context
    
    
class TokenFetcher:    
    # 获取用户访问Boss网站的__zp_stoken__，此token用户反爬系统，需要定期更新来反反爬
    def __init__(self, user_id: str):
        self.playwright = sync_playwright().start()  # 手动启动，不自动关闭
        self.browser = self.playwright.chromium.launch(headless=False)
        cache_dir = f"cache/{user_id}"
        self.context = login(self.browser, cache_dir)

    def get_token(self):
        page = self.context.new_page()
        page.set_default_timeout(120000)
        page.goto("https://www.zhipin.com/guangzhou/?seoRefer=index", wait_until="networkidle")
        cookies = page.context.cookies()
        stoken = next(c["value"] for c in cookies if c["name"] == "__zp_stoken__")
        print(stoken)
        page.close()
        return stoken
    
    def shutdown(self):
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            print(f"playwright shutdown error: {e}")

if __name__ == '__main__':       
    fetcher = TokenFetcher()
    print(fetcher.get_token())
    print(fetcher.get_token())