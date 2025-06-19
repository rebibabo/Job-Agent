import redis
from yaml.tokens import Token
from crawler.api import get_job_list
from crawler.query import JobQuery
from crawler.token import TokenFetcher
from database.connector import db_pool, redis_connector
from utils.cache import CachedIterator
from utils.tools import set_user_id, get_user_id
from flask import Flask, request, jsonify
from constant import USER_ID_NAME, DEFAULT_USER_ID
import os
import time
from multiprocessing import Process

app = Flask(__name__)


# 本地跑
def main():
    user_id = set_user_id()
    TokenFetcher.userId = user_id
    redis_connector.hset(user_id, "percentage", 0)
    redis_connector.hset(user_id, "running", 1)
    titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    titles = [x[0] for x in titles]
    cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl.json')
    for city, title in iterator:
        query = JobQuery(
            userId='1',
            city=city,
            industry=["互联网"],
            jobType="全职",
            title=title,
            limit=60
        )
        get_job_list(query, user_id)
        time.sleep(2)

# 开端口跑
@app.route('/api/crawl', methods=['POST'])
def run_crawler(data):
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    if not user_id:
        return jsonify({'success': False, 'message': 'userId 必填'}), 400

    industry = data.get('industry', [])
    jobType = data.get('jobType', '全职')
    cities = data.get('city', ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"])
    titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    titles = [x[0] for x in titles]
    titles = data.get('title', titles)
    experience = data.get('experience', [])
    degree = data.get('degree', [])
    salary = data.get('salary', [])
    limit = data.get('limit', 30)
    keyword = data.get('keyword', '')
    scale = data.get('scale', [])
    stage = data.get('stage', [])
    
    os.environ[USER_ID_NAME] = user_id
    TokenFetcher.userId = user_id
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl.json')
    progress = iterator.index / iterator.total * 100
    redis_connector.hset(user_id, "percentage", progress)
    for city, title in iterator:
        query = JobQuery(
            userId=user_id,
            city=city,
            industry=industry,
            jobType=jobType,
            title=title,
            experience=experience,
            degree=degree,
            salary=salary,
            limit=limit,
            keyword=keyword,
            scale=scale,
            stage=stage
        )
        get_job_list(query, user_id)
        progress = iterator.index / iterator.total * 100
        redis_connector.hset(user_id, "percentage", progress)
        status = int(redis_connector.hget(user_id, "running").decode())
        if status == 0:
            print("终止循环")
            return
        time.sleep(2)
        
    redis_connector.hset(user_id, "percentage", 100)
    redis_connector.hset(user_id, "running", 0)


# def background_job(status):
#     """模拟后台长任务"""
    
#     while status["running"] and status["percentage"] < 100:
#         print(status)
#         time.sleep(1)  # 模拟耗时
#         status["percentage"] += 5
#     if status["percentage"] >= 100:
#         status[0] = False

@app.route('/joblist/start', methods=['POST'])
def start_job():
    data = request.get_json()
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    status = int(redis_connector.hget(user_id, "running").decode())
    if not status:
        redis_connector.hset(user_id, "percentage", 0)
        redis_connector.hset(user_id, "running", 1)
        
        p = Process(target=run_crawler, args=(data,))
        p.start()
        return jsonify({"message": "Job started"}), 200
    else:
        return jsonify({"message": "Job already running"}), 410

@app.route('/joblist/progress', methods=['POST'])
def get_progress():
    data = request.get_json()
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    percentage = redis_connector.hget(user_id, "percentage")
    if percentage is not None:
        percentage = round(float(percentage.decode('utf-8')), 1)  # 转成字符串再转int
    else:
        percentage = 0  # 或者其他默认值
    return jsonify({
        "percentage": percentage,
    })

@app.route('/joblist/stop', methods=['POST'])
def stop_job():
    data = request.get_json()
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    redis_connector.hset(user_id, "running", 0)
    return jsonify({"message": "Job stopped"}), 200

    
if __name__ == '__main__':
    # main()
    app.run(debug=False, host='0.0.0.0', port=5000)