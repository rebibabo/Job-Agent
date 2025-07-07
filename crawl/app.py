from agent.ranker import GPTRanker
from agent.filter import GPTFilter
from crawler.api import get_job_list, get_job_list_with_desc, send_cv
from crawler.query import JobQuery
from database.connector import db_pool
from database.jobinfo import JobInfo
from utils.cache import CachedIterator
from flask import Flask, request, jsonify, Response
from constant import ALREADY_RUN_CODE, DEFAULT_MODEL
from loguru import logger
import time
import os
import json
from crawler.requestHelper import Request
from multiprocessing import Process, Manager
from resume_routes import resume_bp

app = Flask(__name__)
app.register_blueprint(resume_bp)

# 本地跑
def crawl():
    user_id = "1"
    titles = ["数据开发", "数据分析师", "Python"]
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
        
        insertDTO.commit_to_db()
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
    limit = data.get('limitNum', 30)
    keyword = data.get('keyword', '')
    scale = data.get('scale', [])
    stage = data.get('stage', [])
    filterHash = data.get('filterHash', '')
    return user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash

def run_crawler(data, status):
    user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash = parse_data(data)
        
    print(limit)
        
    cache_path = f'cache/{user_id}/crawl/crawl_{filterHash}.json'
    iterator = CachedIterator([cities, titles], cache_path)
    progress = iterator.index / iterator.total * 100
    status["running"] = 1
    status["percentage"] = progress
    
    try:
        for city, title in iterator:
            query = JobQuery(
                userId=user_id, city=city, industry=industry, jobType=jobType,
                title=title, experience=experience, degree=degree, salary=salary,
                limit=limit, keyword=keyword, scale=scale, stage=stage,
            )
            insertDTO = get_job_list(query, user_id, status, filterHash)
            insertDTO.commit_to_db()
            progress = iterator.index / iterator.total * 100
            status["percentage"] = progress
            if status.get('running', 1) == 0:
                logger.info("终止循环")
                return

            time.sleep(2)
            
        status["running"] = 0
        status["percentage"] = 100
    except Exception as e:
        logger.error(e)
        status["running"] = 0
        status["percentage"] = 0
        status["error"] = str(e)
    finally:
        Request.fetcher.shutdown()
        
def run_crawler_with_desc(data, status):
    user_id, industry, jobType, cities, titles, experience, degree, salary, \
        limit, keyword, scale, stage, filterHash = parse_data(data)
    
    cache_path = f'cache/{user_id}/crawl/crawl_with_desc_{filterHash}.json'
    iterator = CachedIterator([cities, titles], cache_path)
    progress = iterator.index / iterator.total * 100
    status["running"] = 1
    status["percentage"] = progress
    increment = 100 / iterator.total / limit
    try:
        for city, title in iterator:
            query = JobQuery(
                userId=user_id, city=city, industry=industry, jobType=jobType,
                title=title, experience=experience, degree=degree, salary=salary,
                limit=limit, keyword=keyword, scale=scale, stage=stage,
            )
            insertDTO = get_job_list_with_desc(query, user_id, status=status, filter_hash=filterHash, increment=increment)
            insertDTO.commit_to_db()
            progress = iterator.index / iterator.total * 100
            status["percentage"] = progress
            if status.get('running', 1) == 0:
                logger.info("终止循环")
                return

            time.sleep(2)
            
        status["running"] = 0
        status["percentage"] = 100
    except Exception as e:
        logger.error(e)
        status["running"] = 0
        status["percentage"] = 0
        status["error"] = str(e)
    finally:
        Request.fetcher.shutdown()

def create_app(status):
    @app.route('/start/joblist', methods=['POST'])
    def start_job():
        data = request.get_json()
        status["percentage"] = 0
        get_desc = data.get('getDesc', False)
        if status.get('running', 0) == 0:
            if not get_desc:
                p = Process(target=run_crawler, args=(data, status))
            else:
                p = Process(target=run_crawler_with_desc, args=(data, status))
            p.start()
            return jsonify({"message": "Job started"}), 200
        else:
            return jsonify({"message": "Job already running"}), ALREADY_RUN_CODE

    @app.route('/progress', methods=['GET'])
    def get_progress():        
        if 'percentage' in status and status['percentage'] < 0:
            return jsonify({
                "percentage": -1,
                "error": status.get('error', 'Unknown error')
            })
        json_str = json.dumps({
            "percentage": round(status.get('percentage', 0), 1),
            "results": list(status.get('results', []))
        }, ensure_ascii=False)

        return Response(json_str, content_type="application/json; charset=utf-8")

    @app.route('/stop', methods=['GET'])
    def stop_job():
        status["running"] = 0
        return jsonify({"message": "Job stopped"}), 200
    
    @app.route('/start/filter', methods=['POST'])
    def start_filter():
        data = request.get_json()
        user_id = data.get('userId')
        jobs = data.get('jobs')
        filter_query = data.get('filterQuery')
        batch_size = data.get('batchSize', 10)
        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.5)
        
        jobList = []
        for job in jobs:
            jobList.append(JobInfo.from_dict(job))
        filter = GPTFilter(jobList, filter_query)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'userId 必填'}), 400
        if status.get('running', 0) == 0:
            status["running"] = 1
            status["results"] = manager.list()
            status["percentage"] = 0
            p = Process(target=filter.filter, args=(batch_size, model, temperature, status))
            p.start()
            return jsonify({"message": "Filter started"}), 200
        else:
            return jsonify({"message": "Filter already running"}), ALREADY_RUN_CODE

        
    @app.route('/start/rank', methods=['POST'])
    def start_rank():
        data = request.get_json()
        user_id = str(data.get('userId'))
        jobs = data.get('jobs')
        resumeName = data.get('resumeName')
        cv_path = os.path.join("cache", user_id, "resume", resumeName, resumeName + ".pdf")
        batch_size = data.get('batchSize', 10)
        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.5)
        
        jobList = []
        for job in jobs:
            jobList.append(JobInfo.from_dict(job))
        ranker = GPTRanker(jobList, cv_path)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'userId 必填'}), 400
        if status.get('running', 0) == 0:
            status["running"] = 1
            status["results"] = manager.list()
            status["percentage"] = 0
            p = Process(target=ranker.rank, args=(batch_size, model, temperature, status))
            p.start()
            return jsonify({"message": "Rank started"}), 200
        else:
            return jsonify({"message": "Rank already running"}), ALREADY_RUN_CODE
    
    @app.route('/start/sendcv', methods=['POST'])
    def start_sentcv():
        status["percentage"] = 0
        data = request.get_json()
        user_id = str(data.get('userId'))
        jobs = data.get('jobs')
        jobs = [JobInfo.from_dict(job) for job in jobs]
        resume_name = data.get('resumeName')
        message = data.get('message')
        model = data.get('model', DEFAULT_MODEL)
        temperature = data.get('temperature', 0.5)
        polish = data.get('polish', True)
        cv_path = os.path.join("cache", user_id, "resume", resume_name, resume_name + ".pdf")
        if not user_id or not jobs or not resume_name or not message:
            return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        if status.get('running', 0) == 0:
            p = Process(target=send_cv, args=(user_id, jobs, cv_path, message, polish, model, temperature, status))
            p.start()
            return jsonify({"message": "Send CV started"}), 200
        else:
            return jsonify({"message": "Send CV already running"}), ALREADY_RUN_CODE
    return app
    
if __name__ == '__main__':
    # crawl()
    # crawl_with_desc()
    manager = Manager()
    status = manager.dict()
    status["percentage"] = 0.0
    status["running"] = 0
    status["results"] = manager.list()
    app = create_app(status)
    app.run(debug=False, host='0.0.0.0', port=5000)