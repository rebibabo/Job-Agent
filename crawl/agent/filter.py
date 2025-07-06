from tqdm import trange
from typing import List
from utils.llm import get_response, get_llm
from database.jobinfo import JobInfo
from constant import DEFAULT_MODEL
from loguru import logger

class GPTFilter:
    def __init__(self, jobinfo: List[JobInfo], query: str, max_retries: int=3):
        self.jobinfo = jobinfo
        self.jobs = [(i, job) for i, job in enumerate(jobinfo)]
        self.query = query
        self.max_retries = max_retries
        
    def batch_filter(
        self,
        LLM, 
        batch_job: List[JobInfo],
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5, 
    ) -> List[JobInfo]:
        num = len(batch_job)
        messages = [
            {"role": "system", "content": "你是一个智能的职位筛选助手，能够根据用户的要求，筛选掉不符合#查询条件#的职位，包括学历要求、岗位描述、薪资范围、公司名称、地点要求等。"},
            {"role": "user", "content": f"我将提供给你{num}个招聘岗位信息，每一个岗位通过数字和[]标识，例如[1]。"},
            {"role": "assistant", "content": "好的，请提供各个岗位信息。"},
        ]
        for i, jobinfo in batch_job:
            job_text = (f"工作名称：{jobinfo.jobName}\n公司名称：{jobinfo.companyName}\n工作城市：{jobinfo.city}\n薪资范围：{jobinfo.salary}\n"
                    f"经验要求：{jobinfo.experience}\n学历要求：{jobinfo.degree}\n工作技能需求：{jobinfo.skills}\n行业：{jobinfo.industry}\n"
                    f"岗位分类：{jobinfo.title}\n人员规模：{jobinfo.scale}\n融资阶段：{jobinfo.stage}\n岗位描述：{jobinfo.description}\n")
            messages.append({"role": "user", "content": f"岗位[{i}]\n{job_text}"})
            messages.append({"role": "assistant", "content": f"收到岗位[{i}]"})
            
        messages.append({"role": "user", "content": f"以上一共{num}条岗位信息，#查询条件#如下：\n{self.query}"})
        messages.append({"role": "assistant", "content": "好的，我将根据你的要求进行岗位筛选。"})
        messages.append({"role": "user", "content": f"请对上面{num}个条招聘岗位进行筛选，返回不符合#查询条件#的岗位列表，输出的格式应该是数字列表, eg., [0, 3, 5]，如果都符合#查询条件#的岗位，则输出空列表[]。只要回答岗位列表，不要解释任何理由。"})

        for _ in range(self.max_retries):
            response = get_response(LLM, messages, model, temperature)
            try:
                return eval(response)
            except:
                logger.warning(f"Wrong response format: {response}, retry...")
        logger.warning(f"第{i+1}批次过滤失败，重试{self.max_retries}次")
        return []

    def filter(self, 
        batch_size: int=16, 
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5,
        status=None,
        repeat=3,
        threshold=2,
        api_key: str = None,
        base_url: str = None,
    ) -> List[JobInfo]:
        ans = []
        LLM = get_llm(api_key=api_key, base_url=base_url)
        for startIdx in trange(0, len(self.jobs), batch_size):
            selected_indices = None
            j = 0
            repeat_filter = []
            while j < repeat:
                if status and status["running"] == 0:
                    logger.info("停止过滤")
                    return ans
                batch_job = self.jobs[startIdx:startIdx+batch_size]
                selected_indices = self.batch_filter(LLM, batch_job, model=model, temperature=temperature)
                repeat_filter.extend(selected_indices)
                j += 1
            filter_freq = {}
            for idx in repeat_filter:
                filter_freq[idx] = filter_freq.get(idx, 0) + 1
            selected_job = [self.jobinfo[idx] for idx, freq in filter_freq.items() if freq >= threshold]
            ans.extend(selected_job)
            if status:
                status["percentage"] = (startIdx + batch_size) / len(self.jobs) * 100
                status["results"].extend([job.to_dict() for job in selected_job])
        if status:
            status["percentage"] = 100
            status["running"] = 0
        jobs = [job.to_dict() for job in ans]
        jobIds = [job["id"] for job in jobs]
        logger.info(f"被过滤的岗位：{jobIds}")
        logger.info(f"被过滤的岗位数量：{len(jobIds)}")
        return ans