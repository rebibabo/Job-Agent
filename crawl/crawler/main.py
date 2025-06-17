from crawler.api import get_job_list
from crawler.query import JobQuery
from database.connector import db_pool
from utils.cache import CachedIterator
from constant import *
import time

def main():
    titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    titles = [x[0] for x in titles]
    cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
    iterator = CachedIterator([cities, titles], 'cache/crawl.json')
    for city, title in iterator:
        query = JobQuery(
            city=city,
            industry=["互联网"],
            jobType="全职",
            title=title
        )
        get_job_list(query, max_num=60)
        time.sleep(2)

