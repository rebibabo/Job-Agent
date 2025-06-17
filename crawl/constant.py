import json

code_json = json.load(open('metadata/code.json', 'r', encoding='utf-8'))

DEGREE = {x["name"]: x["code"] for x in code_json["degreeList"]}
SALARY = {x["name"]: x["code"] for x in code_json["salaryList"]}
EXPERIENCE = {x["name"]: x["code"] for x in code_json["experienceList"]}
SCALE = {x["name"]: x["code"] for x in code_json["scaleList"]}
STAGE = {x["name"]: x["code"] for x in code_json["stageList"]}
JOBTYPE = {x["name"]: x["code"] for x in code_json["jobTypeList"]}

WAIT_FOR_LOAD = "networkidle"