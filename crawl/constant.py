import json

code_json = json.load(open('metadata/code.json', 'r', encoding='utf-8'))

DEGREE = {x["name"]: str(str(x["code"])) for x in code_json["degreeList"]}
SALARY = {x["name"]: str(x["code"]) for x in code_json["salaryList"]}
EXPERIENCE = {x["name"]: str(x["code"]) for x in code_json["experienceList"]}
SCALE = {x["name"]: str(x["code"]) for x in code_json["scaleList"]}
STAGE = {x["name"]: str(x["code"]) for x in code_json["stageList"]}
JOBTYPE = {x["name"]: str(x["code"]) for x in code_json["jobTypeList"]}
ALREADY_RUN_CODE = 410
TOKEN_EXPIRED_CODE = 401

WAIT_FOR_LOAD = "networkidle"
USER_ID_NAME = "USER_ID"

# 修改为后端的接口url
INSERT_URL = "http://localhost:8081/job/insert"     
LOGIN_URL = "http://localhost:8081/user/login"
QUERY_URL = "http://localhost:8081/job/page"
LIST_URL = "http://localhost:8081/job/list"
DESC_URL = "http://localhost:8081/job/desc"

DEFAULT_MODEL = "gpt-4o-mini"