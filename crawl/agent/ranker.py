from typing import List
from agent.resume import ResumeLoader
from database.jobinfo import JobInfo
from utils.llm import get_response, get_llm
from tqdm import trange
from constant import DEFAULT_MODEL
import re
import numpy as np

class GPTRanker:
    def __init__(self, jobinfo: List[JobInfo], cv_path: str):
        self.jobinfo = jobinfo
        self.jobs = [(i, job.description) for i, job in enumerate(jobinfo)]
        self.cv = ResumeLoader(cv_path).content
        
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
            
        response = get_response(LLM, messages, model, temperature)
        
        try:
            return eval(response)
        except:
            print("error in parsing response: ", response)
            return None
    
    def rank(self, 
        batch_size: int=16, 
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5,
        repeat: int = 5,
        api_key: str = None,
        base_url: str = None,
    ) -> List[JobInfo]:
        total_scores = []
        LLM = get_llm(api_key=api_key, base_url=base_url)
        for i in trange(0, len(self.jobinfo), batch_size):
            repeat_scores = []
            j = 0
            while j < repeat:
                batch_job = self.jobs[i:i+batch_size]
                scores = self.batch_ranker(LLM, batch_job, model=model, temperature=temperature)
                if scores and len(scores) == len(batch_job):
                    j += 1
                    repeat_scores.append(scores)
            if scores is None:
                print("Max retries reached, skipping...")
                total_scores.extend([0]*batch_size)
                continue
                
            repeat_scores = np.array(repeat_scores)
            median_scores = np.median(repeat_scores, axis=0)
            print(median_scores)
            total_scores.extend(median_scores)
            
        res = []
        for i, score in enumerate(total_scores):
            self.jobinfo[i].score = score
            res.append(self.jobinfo[i])
            
        res = sorted(res, key=lambda x: x.score, reverse=True)
        return res
    
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
                