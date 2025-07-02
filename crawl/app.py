from crawler.api import get_job_list, get_job_list_with_desc
from crawler.query import JobQuery
from database.connector import db_pool
from utils.cache import CachedIterator
from flask import Flask, request, jsonify
from constant import ALREADY_RUN_CODE
from loguru import logger
import time
from multiprocessing import Process, Manager
from resume_routes import resume_bp

app = Flask(__name__)
app.register_blueprint(resume_bp)

# 本地跑
def crawl():
    user_id = "1"
    # titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    # titles = [x[0] for x in titles]
    titles = ["数据开发", "数据分析师", "Python"]
    # cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
    cities = ["北京", "上海", "深圳", "广州",]
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl/crawl.json')
    jobList = []
    for city, title in iterator:
        query = JobQuery(
            userId=user_id, city=city, industry=["互联网"],
            jobType="全职", title=title, limit=60
        )
        insertDTO = get_job_list(query, user_id=user_id)
        jobList.extend(insertDTO.jobs)
        
        # insertDTO.commit_to_db()
        time.sleep(2)
        
def crawl_with_desc():
    user_id = "1"
    titles = ["数据开发", "数据分析师", "Python"]
    cities = ["北京", "上海"]
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl/crawl_with_desc.json')
    jobList = []
    for city, title in iterator:
        query = JobQuery(
            userId=user_id, city=city, industry=["互联网"],
            jobType="全职", title=title, limit=5
        )
        insertDTO = get_job_list_with_desc(query, user_id=user_id)
        jobList.extend(insertDTO.jobs)
        
        insertDTO.commit_to_db()
        time.sleep(2)


def parse_data(data):
    user_id = data.get('userId')
    industry = data.get('industry', [])
    jobType = data.get('jobType', '全职')
    cities = data.get('city', [])
    if not cities:
        cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
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
    filterHash = data.get('filterHash', '')
    return user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash

def run_crawler(data, job_status):
    user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash = parse_data(data)
    job_status[user_id] = {'percentage': 0.0, 'running': 1}
        
    cache_path = f'cache/{user_id}/crawl/crawl_{filterHash}.json'
    iterator = CachedIterator([cities, titles], cache_path)
    progress = iterator.index / iterator.total * 100
    job_status[user_id] = {     # 需要完整赋值，job_status[user_id]['percentage']是不会进程共享的
        'running': 1,
        'percentage': progress
    }
    
    try:
        for city, title in iterator:
            query = JobQuery(
                userId=user_id, city=city, industry=industry, jobType=jobType,
                title=title, experience=experience, degree=degree, salary=salary,
                limit=limit, keyword=keyword, scale=scale, stage=stage,
            )
            insertDTO = get_job_list(query, user_id, job_status, filterHash)
            insertDTO.commit_to_db()
            progress = iterator.index / iterator.total * 100
            job_status[user_id] = {
                **job_status[user_id],      # 这里需要共享进程的job_status，相当于update，当stop时，会更新running为0
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
    except Exception as e:
        logger.error(e)
        job_status[user_id] = {
            'running': 0,
            'percentage': -1,
            'error': str(e)
        }
        
def run_crawler_with_desc(data, job_status):
    user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash = parse_data(data)
    job_status[user_id] = {'percentage': 0.0, 'running': 1}
    
    cache_path = f'cache/{user_id}/crawl/crawl_with_desc_{filterHash}.json'
    iterator = CachedIterator([cities, titles], cache_path)
    progress = iterator.index / iterator.total * 100
    job_status[user_id] = {     # 需要完整赋值，job_status[user_id]['percentage']是不会进程共享的
        'running': 1,
        'percentage': progress
    }
    increment = 100 / iterator.total / limit
    try:
        for city, title in iterator:
            query = JobQuery(
                userId=user_id, city=city, industry=industry, jobType=jobType,
                title=title, experience=experience, degree=degree, salary=salary,
                limit=limit, keyword=keyword, scale=scale, stage=stage,
            )
            insertDTO = get_job_list_with_desc(query, user_id, job_status=job_status, filter_hash=filterHash, increment=increment)
            insertDTO.commit_to_db()
            progress = iterator.index / iterator.total * 100
            job_status[user_id] = {
                **job_status[user_id],      # 这里需要共享进程的job_status，相当于update，当stop时，会更新running为0
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
    except Exception as e:
        logger.error(e)
        job_status[user_id] = {
            'running': 0,
            'percentage': -1,
            'error': str(e)
        }

def create_app(job_status):
    @app.route('/joblist/start', methods=['POST'])
    def start_job():
        data = request.get_json()
        user_id = data.get('userId')
        get_desc = data.get('getDesc', False)
        if not user_id:
            return jsonify({'success': False, 'message': 'userId 必填'}), 400
        if job_status.get(user_id, {}).get('running', 0) == 0:
            if not get_desc:
                p = Process(target=run_crawler, args=(data, job_status))
            else:
                p = Process(target=run_crawler_with_desc, args=(data, job_status))
            p.start()
            return jsonify({"message": "Job started"}), 200
        else:
            return jsonify({"message": "Job already running"}), ALREADY_RUN_CODE

    @app.route('/joblist/progress', methods=['POST'])
    def get_progress():
        data = request.get_json()
        
        user_id = data.get('userId')
        if not user_id:
            return jsonify({'success': False, 'message': 'userId 必填'}), 400
        state = job_status.get(user_id, {'percentage': 0})
        if 'percentage' in state and state['percentage'] < 0:
            return jsonify({
                "percentage": -1,
                "error": state.get('error', 'Unknown error')
            })
        return jsonify({
            "percentage": round(state.get('percentage', 0), 1)
        })

    @app.route('/joblist/stop', methods=['POST'])
    def stop_job():
        data = request.get_json()
        user_id = data.get('userId')
        if not user_id:
            return jsonify({'success': False, 'message': 'userId 必填'}), 400
        if user_id in job_status:
            job_status[user_id] = {
                **job_status[user_id],
                'running': 0,
            }
        return jsonify({"message": "Job stopped"}), 200
    
    return app
    
if __name__ == '__main__':
    # crawl()
    # crawl_with_desc()
    manager = Manager()
    job_status = manager.dict()
    app = create_app(job_status)
    app.run(debug=False, host='0.0.0.0', port=5000)