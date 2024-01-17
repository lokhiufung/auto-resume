import time
import os
import hashlib

from auto_resume.sdk.logger import get_logger
# import agents
from auto_resume.sdk.agents.experience_enhancing_agent.agent import ExperienceEnhancingAgent
from auto_resume.sdk.agents.jd_parsing_agent.agent import JdParsingAgent
from auto_resume.sdk.agents.keyword_injecting_agent.agent import KeywordInjectingAgent
from auto_resume.sdk.agents.skill_injecting_agent.agent import SkillInjectingAgent
from auto_resume.sdk.evaluate_resume import evaluate_resume


logger = get_logger('engine.log', logger_lv='debug')


def clean_job_title(job_title: str):
    job_title = job_title.replace('/', '_')
    return job_title


class Engine:

    ENGINE_CONFIG = {}  # default config

    def __init__(self, engine_config, storage=None):
        self.agents = {}
        self.engine_config = {**self.ENGINE_CONFIG, **engine_config}  # engine_config always override the default configs
        self.storage = storage
        self.resume_storage_path = os.path.join(self.storage, 'resume')
        self.jd_storage_path = os.path.join(self.storage, 'jd')
        # initialize 
        self.agents = self.create_agents()
        if not os.path.exists(self.resume_storage_path):
            os.makedirs(self.resume_storage_path)
        if not os.path.exists(self.jd_storage_path):
            os.makedirs(self.jd_storage_path)

    def create_agents(self):
        # TODO: llm_config may be tunable parameters?
        llm_config={
            'temperature': 0.3,
            'max_tokens': 2000,
            'model': 'gpt-3.5-turbo'
        }
        llm_backend = 'openai'

        experience_enhancing_agent = ExperienceEnhancingAgent.from_llm_config(
            llm_config={
                'temperature': 0.3,
                'max_tokens': 2000,
                'model': 'gpt-4'
            },
            llm_backend=llm_backend
        )
        jd_parsing_agent = JdParsingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        skill_injecting_agent = SkillInjectingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        keyword_injecting_agent = KeywordInjectingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        
        return {
            'experience_enhancing_agent': experience_enhancing_agent,
            'jd_parsing_agent': jd_parsing_agent,
            'skill_injecting_agent': skill_injecting_agent,
            'keyword_injecting_agent': keyword_injecting_agent,
        }

    def start(self, save):
            
        base_resume = self.engine_config['base_resume']
        job_description = self.engine_config['job_description'].strip()
        
        jobs = []
        job_details = self.agents['jd_parsing_agent'].act(job_description=job_description)
        for job in base_resume['jobs']:
            updated_desc = self.agents['skill_injecting_agent'].act(skills=job_details['skills'], experiences=job['desc'])
            updated_desc = self.agents['keyword_injecting_agent'].act(keywords=job_details['keywords'], experiences=updated_desc['experiences'])
            updated_desc = self.agents['experience_enhancing_agent'].act(experiences=updated_desc['experiences'])
            
            result = {
                **job,
                'desc': updated_desc['experiences']
            }
            jobs.append(result)

            time.sleep(1)

        # 5. update your experience
        updated_resume = {**base_resume, 'jobs': jobs}

        if save:
            job_title = job_details['job_title']
            job_title_formatted = '_'.join(job_title.lower().split(' '))
            job_title_formatted = clean_job_title(job_title_formatted)
            # hash
            hash = hashlib.md5()
            hash.update(job_description.encode())
            jd_hashed = hash.hexdigest()  # 32 char string, 128-bit
            with open(os.path.join(self.jd_storage_path, f'{job_title_formatted}-{jd_hashed}.txt'), 'w') as f:
                f.write(job_description)
            with open(os.path.join(self.resume_storage_path, f'{job_title_formatted}-{jd_hashed}.txt'), 'w') as f:
                f.write(job_description)

        # 6. evaluate the resume
        # reminder: now evaluating the resume requires the keywords extracted by jd_parsing_agent. Can you decouple the evalution from engine.start()?
        updated_metrics = evaluate_resume(updated_resume, job_details['keywords'])
        base_metrics = evaluate_resume(base_resume, job_details['keywords'])

        return {
            'result': updated_resume,
            'metrics': {
                'base_metrics': base_metrics,
                'updated_metrics': updated_metrics,
            }
        }
        
        




