from agent.ranker import GPTRanker
from crawler.api import get_job_list
from crawler.query import JobQuery
from crawler.token import TokenFetcher
from database.connector import db_pool
from utils.cache import CachedIterator
from utils.tools import set_user_id
from flask import Flask, request, jsonify
from constant import DEFAULT_USER_ID, ALREADY_RUN_CODE
from loguru import logger
import time
import os
from multiprocessing import Process, Manager
from agent.resume import ResumeLoader
from agent.filter import GPTFilter

app = Flask(__name__)

# 本地跑
def main():
    user_id = set_user_id()
    resume = ResumeLoader("cache/1/resume/实习简历_袁忠升/实习简历_袁忠升.pdf")
    # titles = db_pool.execute('SELECT name FROM title WHERE type="互联网/AI"')
    # titles = [x[0] for x in titles]
    titles = ["数据开发", "数据分析师", "Python"]
    # cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "西安", "长沙", "南京", "苏州", "重庆"]
    cities = ["北京"]
    iterator = CachedIterator([cities, titles], f'cache/{user_id}/crawl/crawl.json')
    jobList = []
    for city, title in iterator:
        query = JobQuery(
            userId=user_id,
            city=city,
            industry=["互联网"],
            jobType="全职",
            title=title,
            limit=5
        )
        insertDTO = get_job_list(query, user_id=user_id, get_desc=True)
        jobList.extend(insertDTO.jobs)
        
        insertDTO.commit_to_db()
        time.sleep(2)
        
    search_input = "数据开发岗位"
    filter = GPTFilter(jobList, search_input)
    jobList = filter.filter(batch_size=3)
    print("过滤后的条数：", len(jobList))
    ranker = GPTRanker(jobList, resume.file_path)
    jobList = ranker.rank(window_length=3, step=1)
    for job in jobList:
        print(job.description)
        print('=====================================')

# 开端口跑
@app.route('/api/crawl', methods=['POST'])
def run_crawler(data, job_status):
    user_id = str(data.get('userId', DEFAULT_USER_ID))
    job_status[user_id] = {'percentage': 0.0, 'running': 1}
    if not user_id:
        return jsonify({'success': False, 'message': 'userId 必填'}), 400

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
                stage=stage,
            )
            insertDTO = get_job_list(query, job_status, user_id, filterHash)
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
        user_id = str(data.get('userId', DEFAULT_USER_ID))
        if user_id in job_status:
            job_status[user_id] = {
                **job_status[user_id],
                'running': 0,
            }
        return jsonify({"message": "Job stopped"}), 200

    @app.route('/resume/<user_id>', methods=['POST'])
    def upload_resume(user_id):
        # 检查文件
        if 'file' not in request.files:
            return jsonify({"message": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "Empty filename"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"message": "Only PDF allowed"}), 400

        pdf_name = os.path.splitext(file.filename)[0]
        save_dir = os.path.join("cache", user_id, "resume", pdf_name)
        os.makedirs(save_dir, exist_ok=True)
        
        save_path = os.path.join(save_dir, file.filename)
        file.save(save_path)
        
        return jsonify({"message": "Upload success", "path": save_path}), 200

    return app
    
if __name__ == '__main__':
    main()
    # manager = Manager()
    # job_status = manager.dict()
    # app = create_app(job_status)
    # app.run(debug=False, host='0.0.0.0', port=5000)