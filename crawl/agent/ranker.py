from typing import List
from agent.resume import ResumeLoader
from database.jobinfo import JobInfo
from utils.llm import get_response
import re

class GPTRanker:
    def __init__(self, jobinfo: List[JobInfo], cv_path: str):
        self.jobinfo = jobinfo
        self.jobs = [(i, job.description) for i, job in enumerate(jobinfo)]
        self.cv = ResumeLoader(cv_path).summary
        
    def batch_ranker(
        self,
        jobs: tuple[int, str],     
        model: str = "gpt-4o-mini-2024-07-18", 
        temperature: float = 0.5, 
    ) -> List[int]:
        ''' Query OpenAI API to generate a response to a given input. '''
        
        num = len(jobs)
        messages = [
            {"role": "system", "content": "你是一个智能的排序助手，能够根据用户的个人简历，对招聘岗位进行匹配度排名，排名依据包括但不限于学历要求、工作经验、技能、项目经历、工作经历等。"},
            {"role": "user", "content": f"我将提供给你{num}个招聘岗位信息，每一个岗位通过数字和[]标识，根据简历对岗位需求的匹配程度来进行排序"},
            {"role": "assistant", "content": "好的，请提供各个岗位"},
        ]
        
        for i, job in jobs:
            messages.append({"role": "user", "content": f"[{i}] {job}"})
            messages.append({"role": "assistant", "content": f"收到岗位[{i}]"})
            
        messages.append({"role": "user", "content": f"用户个人简历如下\n{self.cv}"})
        messages.append({"role": "assistant", "content": "收到简历"})
        messages.append({"role": "user", "content": f"请根据用户个人简历对上面{num}个招聘岗位进行匹配度排名，岗位需要使用他们的标识符按照降序排列，最相关的岗位应该排在前面，输出的格式应该是 [] > [], eg., [0] > [2]。只要回答排名结果，不要解释任何理由。"})
            
        response = get_response(messages, model, temperature)
        
        ans = []
        for each in response.split(">"):
            pattern = r"\[(\d+)\]"
            numbers = re.findall(pattern, each)
            if len(numbers) == 1:
                ans.append(int(numbers[0]))
            else:
                return []
        return ans
        
    def rank(self, 
        window_length=4, 
        step=2,
        model: str = "gpt-4o-mini-2024-07-18", 
    ) -> List[JobInfo]:
        ans = []

        left = max(len(self.jobs)-window_length, 0)
        batch_jobs = self.jobs[left+step:] 

        while left >= 0:
            left = max(left, 0)
            batch_jobs.extend(self.jobs[left:left+step])
            for _ in range(3):
                rank = self.batch_ranker(batch_jobs, model=model)
                if rank:
                    print(rank)
                    break
            if not rank:
                print("Max retries reached, skipping...")
                continue
            i = step
            while i > 0 and rank:
                ans.append(rank.pop())
                i -= 1
            left -= step
            batch_jobs = [self.jobs[i] for i in rank]

        while batch_jobs:
            ans.append(batch_jobs.pop()[0])

        return [self.jobinfo[i] for i in ans[::-1] if 0<=i<len(self.jobinfo)]