from constant import DEFAULT_MODEL
from utils.llm import get_response, get_llm
from database.jobinfo import JobInfo

def polish_message(
        message: str, 
        resume_summary: str,
        jobinfo: JobInfo, 
        api_key: str=None, 
        base_url: str=None,
        model: str=DEFAULT_MODEL,
        temperature: float=0.5
    ) -> str:
    # 根据岗位信息，对问候语进行润色
    LLM = get_llm(api_key=api_key, base_url=base_url)
    job_text = (f"工作名称：{jobinfo.jobName}\n公司名称：{jobinfo.companyName}\n"
                f"岗位分类：{jobinfo.title}\n岗位介绍：{jobinfo.description}\n")
    messages = [
        {"role": "system", "content": "你是一个拥有丰富经验的大厂hr，你能够根据岗位的信息，定制化的润色用户发给你的问候语，使他表现得和岗位非常匹配，对这份工作十分热情，在茫茫人海中脱颖而出。"},
        {"role": "user", "content": f"我的问候语如下：{message}\n\n岗位信息如下：{job_text}。我的简历摘要如下：{resume_summary}。\n请你帮我润色问候语，根据我的简历摘要和岗位信息，让问候语更加符合岗位要求。润色后的问候语不要超过60字。只返回润色后的问候语结果，不要返回任何理由或其他内容。"},
    ]
    
    response = get_response(LLM, messages, model, temperature)
    return response