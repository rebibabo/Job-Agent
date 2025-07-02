from tqdm import trange
from typing import List
from utils.llm import get_response, get_llm
from database.jobinfo import JobInfo
from constant import DEFAULT_MODEL
from loguru import logger

class GPTFilter:
    def __init__(self, jobinfo: List[JobInfo], query: str, max_retries: int = 3):
        self.jobinfo = jobinfo
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
            {"role": "system", "content": "你是一个智能的职位筛选助手，能够根据用户的要求，筛选掉不符合过滤要求的职位，包括实习/全职、学历要求、岗位要求、公司要求、地点要求等。"},
            {"role": "user", "content": f"我将提供给你{num}个招聘岗位信息，每一个岗位通过数字和[]标识，例如[1]。"},
            {"role": "assistant", "content": "好的，请提供各个岗位信息。"},
        ]
        for i, jobinfo in enumerate(batch_job):
            job_text = (f"工作名称：{jobinfo.jobName}\n公司名称：{jobinfo.companyName}\n工作城市：{jobinfo.city}\n薪资范围：{jobinfo.salary}\n"
                    f"经验要求：{jobinfo.experience}\n学历要求：{jobinfo.degree}\n工作技能需求：{jobinfo.skills}\n行业：{jobinfo.industry}\n"
                    f"岗位分类：{jobinfo.title}\n融资状态：{jobinfo.stage}\n人员规模：{jobinfo.scale}")
            messages.append({"role": "user", "content": f"岗位[{i}]\n{job_text}"})
            messages.append({"role": "assistant", "content": f"收到岗位[{i}]"})

        messages.append({"role": "user", "content": f"以上一共{num}条岗位信息，过滤要求如下：\n{self.query}"})
        messages.append({"role": "assistant", "content": "好的，我将根据你的要求进行岗位筛选。"})
        messages.append({"role": "user", "content": f"请对上面{num}个条招聘岗位进行筛选，返回符合条件的岗位列表，输出的格式应该是数字列表, eg., [0, 3, 5]。只要回答岗位列表，不要解释任何理由。"})

        for _ in range(self.max_retries):
            response = get_response(LLM, messages, model, temperature)
            try:
                indices = eval(response)
                return [batch_job[i] for i in indices]
            except:
                logger.warning(f"Wrong response format: {response}, retry...")

    def filter(self, 
        batch_size: int=16, 
        model: str = DEFAULT_MODEL, 
        temperature: float = 0.5,
        status=None,
        api_key: str = None,
        base_url: str = None,
    ) -> List[JobInfo]:
        ans = []
        LLM = get_llm(api_key=api_key, base_url=base_url)
        for i in trange(0, len(self.jobinfo), batch_size):
            selected_job = None
            for _ in range(self.max_retries):
                batch_job = self.jobinfo[i:i+batch_size]
                selected_job = self.batch_filter(LLM, batch_job, model=model, temperature=temperature)
                if selected_job:
                    ans.extend(selected_job)
                    break
            if selected_job is None:
                logger.warning("Max retries reached, skipping...")
                continue
        return ans