from typing import List
from agent.resume import ResumeLoader
from database.jobinfo import JobInfo
from utils.llm import get_response, get_llm
from tqdm import trange
from constant import DEFAULT_MODEL
from loguru import logger
import numpy as np

class GPTRanker:
    def __init__(self, jobinfo: List[JobInfo], cv_path: str, max_retries: int=3):
        self.jobinfo = jobinfo
        self.jobs = [(i, job.description) for i, job in enumerate(jobinfo)]
        self.cv = ResumeLoader(cv_path).content
        self.max_retries = max_retries
        
    def batch_ranker(
        self,
        LLM,
        jobs: tuple[int, str],     
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5, 
    ) -> List[int]:
        ''' Query OpenAI API to generate a response to a given input. '''
        
        num = len(jobs)
        messages = [
            {"role": "system", "content": "你是一个拥有丰富大厂经验的hr，能够根据用户的个人简历和岗位介绍，对招聘岗位进行匹配度打分，打分依据包括但不限于简历中的学历要求、工作经验、技能要求、项目经历、工作经历等。"},
            {"role": "user", "content": f"我将提供给你{num}个招聘岗位信息，每一个岗位通过数字和[]标识，根据简历对岗位需求的匹配程度来进行打分。"},
            {"role": "assistant", "content": "好的，请提供各个岗位，我将为你进行匹配度打分。"},
        ]
        
        for i, job in jobs:
            messages.append({"role": "user", "content": f"岗位[{i}]\n{job}"})
            messages.append({"role": "assistant", "content": f"收到岗位[{i}]"})
            
        messages.append({"role": "user", "content": f"用户个人简历如下\n{self.cv}"})
        messages.append({"role": "assistant", "content": "收到简历"})
        messages.append({"role": "user", "content": f"请根据用户个人简历对上面{num}个招聘岗位进行匹配度打分，输出的格式是整数列表，长度和岗位数量相同，第i个元素表示第i个岗位的匹配度打分，满分10分。 eg., [number1, number2, ..., numberx]。只要回答排名结果，不要解释任何理由。"})
        
        for _ in range(self.max_retries):
            response = get_response(LLM, messages, model, temperature)
            try:
                return eval(response)
            except:
                print("error in parsing response: ", response)
                return None
        
    def get_result(self, total_scores: List[int]):
        res = []
        for i, score in enumerate(total_scores):
            self.jobinfo[i].score = score
            res.append(self.jobinfo[i])
        res = sorted(res, key=lambda x: x.score, reverse=True)
        return [job.to_dict() for job in res]
    
    def rank(self, 
        batch_size: int=16, 
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5,
        status=None,
        repeat: int = 5,
        api_key: str = None,
        base_url: str = None,
    ) -> List[JobInfo]:
        total_scores = []
        LLM = get_llm(api_key=api_key, base_url=base_url)
        for startIdx in trange(0, len(self.jobinfo), batch_size):
            repeat_scores = []
            j = 0
            while j < repeat:
                if status and status["running"] == 0:
                    logger.info("停止排序")
                    return self.get_result(total_scores)
                batch_job = self.jobs[startIdx:startIdx+batch_size]
                scores = self.batch_ranker(LLM, batch_job, model=model, temperature=temperature)
                if scores and len(scores) == len(batch_job):
                    j += 1
                    repeat_scores.append(scores)
                
            repeat_scores = np.array(repeat_scores)
            median_scores = np.median(repeat_scores, axis=0)
            total_scores.extend(median_scores)
            
            if status:
                status["percentage"] = (startIdx+batch_size / len(self.jobs)) * 100
                status["results"] = self.get_result(total_scores)
        if status:
            status["percentage"] = 100
            status["running"] = 0
        logger.info(f"排序完成，共计{len(total_scores)}个岗位")
        return self.get_result(total_scores)
    
    def test_stability(self,
        batch_size: int=16, 
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5,
        api_key: str = None,
        base_url: str = None,
        repeat: int = 5
    ):
        LLM = get_llm(api_key=api_key, base_url=base_url)
        for i in range(0, len(self.jobinfo), batch_size):
            scores = None
            j = 0
            repeat_scores = []
            while j < repeat:
                batch_job = self.jobs[i:i+batch_size]
                scores = self.batch_ranker(LLM, batch_job, model=model, temperature=temperature)
                print(scores)
                if scores and len(scores) == len(batch_job):
                    j += 1
                    repeat_scores.append(scores)
            repeat_scores = np.array(repeat_scores)
            mean_scores = np.mean(repeat_scores, axis=0)
            std_scores = np.std(repeat_scores, axis=0)
            median_scores = np.median(repeat_scores, axis=0)
            print(f"Median scores: {median_scores}")
            print(f"Mean scores: {mean_scores}")
            print(f"Std scores: {std_scores}")
                