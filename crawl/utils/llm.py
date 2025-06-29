from openai import OpenAI
from typing import List, Dict, Literal, TypeAlias
from constant import DEFAULT_MODEL

Message: TypeAlias = Dict[Literal["role", "content"], str]

def get_llm(api_key: str=None, base_url: str=None):
    LLM = OpenAI(api_key=api_key, base_url=base_url)
    return LLM

def get_response(
    LLM: OpenAI, 
    messages: List[Message], 
    model: str = DEFAULT_MODEL, 
    temperature: float = 0.5, 
    max_tokens: int = 2000, 
) -> str:
    ''' Query OpenAI API to generate a response to a given input. '''
    completion = LLM.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,  
        temperature=temperature
    )

    return completion.choices[0].message.content