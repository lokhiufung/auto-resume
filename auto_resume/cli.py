import argparse
import json
import time

# import llm
from auto_resume.sdk.llms.openai_llm import OpenaiLLM
# import required agents
from auto_resume.sdk.agents.experience_enhancing_agent.agent import ExperienceEnhancingAgent
from auto_resume.sdk.agents.jd_parsing_agent.agent import JdParsingAgent
from auto_resume.sdk.agents.keyword_injecting_agent.agent import KeywordInjectingAgent
from auto_resume.sdk.agents.skill_injecting_agent.agent import SkillInjectingAgent
# import utility functions
from auto_resume.sdk.create_resume import create_resume


LLM_BACKEND = 'openai'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--jd', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--output', type=str, default='resume-updated.docx', help="the file path to your output resume")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="the model name of openai model, i.e gpt-3.5-turbo, gpt-4... etc. default to gpt-3.5-turbo")
    return parser.parse_args()


def cli():
    args = parse_args()
    
    # 1. load base resume and jd
    with open(args.resume, 'r') as f:
        base_resume = json.load(f)
    with open(args.jd, 'r') as f:
        job_description = f.read()
    output_file_path = args.output

    # 2. initialize the llm engine (TEMP: shared llm config now)
    llm_config={
        'temperature': 0.3,
        'max_tokens': 2000,
        'model': 'gpt-3.5-turbo'
    }

    # 3. initialize all agents
    experience_enhancing_agent = ExperienceEnhancingAgent.from_llm_config(llm_config, llm_backend=LLM_BACKEND)
    jd_parsing_agent = JdParsingAgent.from_llm_config(llm_config, llm_backend=LLM_BACKEND)
    skill_injecting_agent = SkillInjectingAgent.from_llm_config(llm_config, llm_backend=LLM_BACKEND)
    keyword_injecting_agent = KeywordInjectingAgent.from_llm_config(llm_config, llm_backend=LLM_BACKEND)


    # 4. multi-agent interaction logic: update job experiences
    jobs = []
    job_details = jd_parsing_agent.act(job_description=job_description)
    for job in base_resume['jobs']:
        updated_desc = skill_injecting_agent.act(skills=job_details['skills'], experiences=job['desc'])
        updated_desc = keyword_injecting_agent.act(keywords=job_details['keywords'], experiences=updated_desc['experiences'])
        updated_desc = experience_enhancing_agent.act(experiences=updated_desc['experiences'])
        
        result = {
            **job,
            'desc': updated_desc['experiences']
        }
        jobs.append(result)

        time.sleep(1)

    # 5. update your experience
    updated_resume = {**base_resume, 'jobs': jobs}

    # 6. create resume in doc
    doc = create_resume(updated_resume)
    doc.save(output_file_path)

