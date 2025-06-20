from crawler.api import get_job_list
from crawler.query import JobQuery
from crawler.token import TokenFetcher
from database.connector import db_pool
from utils.cache import CachedIterator
from utils.tools import set_user_id, get_param_hash
from flask import Flask, request, jsonify
from constant import USER_ID_NAME, DEFAULT_USER_ID, ALREADY_RUN_CODE
import os
import time
from multiprocessing import Process, Manager

app = Flask(__name__)

# 本地跑
def main():
    user_id = set_user_id()
    TokenFetcher.userId = user_id
    titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    titles = [x[0] for x in titles]
    cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl.json')
    for city, title in iterator:
        query = JobQuery(
            userId=user_id,
            city=city,
            industry=["互联网"],
            jobType="全职",
            title=title,
            limit=60
        )
        insertDTO = get_job_list(query, user_id=user_id)
        insertDTO.commit_to_db()
        time.sleep(2)

# 开端口跑
@app.route('/api/crawl', methods=['POST'])
def run_crawler(data, job_status):
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    job_status[user_id] = {'percentage': 0.0, 'running': 1}
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
    
    h = get_param_hash(industry, jobType, titles, experience, degree, salary, limit, keyword, scale, stage)
    os.environ[USER_ID_NAME] = user_id
    TokenFetcher.userId = user_id
    cache_path = f'cache/{user_id}/crawl_{h}.json'
    iterator = CachedIterator([cities, titles], cache_path)
    progress = iterator.index / iterator.total * 100
    job_status[user_id] = {     # 需要完整赋值，job_status[user_id]['percentage']是不会进程共享的
        'running': 1,
        'percentage': progress
    }
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
        insertDTO = get_job_list(query, job_status, user_id)
        insertDTO.commit_to_db()
        progress = iterator.index / iterator.total * 100
        job_status[user_id] = {
            'running': 1,
            'percentage': progress
        }
        status = job_status.get(user_id, {}).get('running', 1)
        if status == 0:
            print("终止循环")
            return

        time.sleep(2)
        
    job_status[user_id] = {
        'running': 0,
        'percentage': 100
    }

def create_app(job_status):
    @app.route('/joblist/start', methods=['POST'])
    def start_job():
        data = request.get_json()
        user_id = str(data.get('userId', DEFAULT_USER_ID))
        if job_status.get(user_id, {}).get('running', 0) == 0:
            p = Process(target=run_crawler, args=(data, job_status))
            p.start()
            return jsonify({"message": "Job started"}), 200
        else:
            return jsonify({"message": "Job already running"}), ALREADY_RUN_CODE

    @app.route('/joblist/progress', methods=['POST'])
    def get_progress():
        data = request.get_json()
        
        user_id = str(data.get('userId', DEFAULT_USER_ID))
        state = job_status.get(user_id, {'percentage': 0})
        return jsonify({
            "percentage": round(state.get('percentage', 0), 1)
        })

    @app.route('/joblist/stop', methods=['POST'])
    def stop_job():
        data = request.get_json()
        user_id = str(data.get('userId', DEFAULT_USER_ID))
        if user_id in job_status:
            job_status[user_id] = {
                **job_status[user_id],
                'running': 0,
            }
        return jsonify({"message": "Job stopped"}), 200

    return app
    
if __name__ == '__main__':
    # main()
    manager = Manager()
    job_status = manager.dict()
    app = create_app(job_status)
    app.run(debug=False, host='0.0.0.0', port=5000)