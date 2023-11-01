import json

from auto_resume.sdk.metrics import *


def evaluate_resume(resume, keywords):
    resume = json.dumps(resume)  # make it to json string first
    keyword_score = get_keyword_score(resume, keywords)
    return {
        'keyword_score': keyword_score
    }