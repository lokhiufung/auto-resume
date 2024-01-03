import time
import os
import hashlib

from auto_resume.sdk.logger import get_logger
# import agents
from auto_resume.sdk.agents.responsibility_extracting_agent.agent import ReponsibilityExtractingAgent
from auto_resume.sdk.agents.jd_parsing_agent.agent import JdParsingAgent
from auto_resume.sdk.agents.experience_tailoring_agent.agent import ExperienceTailoringAgent
from auto_resume.sdk.evaluate_resume import evaluate_resume


logger = get_logger('engine.log', logger_lv='debug')


class Engine:

    ENGINE_CONFIG = {}  # default config

    def __init__(self, engine_config, storage=None):
        self.agents = {}
        self.engine_config = {**self.ENGINE_CONFIG, **engine_config}  # engine_config always override the default configs
        self.storage = storage
        # initialize 
        self.agents = self.create_agents()

    def create_agents(self):
        # TODO: llm_config may be tunable parameters?
        llm_backend = 'openai'

        responsibility_extracting_agent = ReponsibilityExtractingAgent.from_llm_config(
            llm_config={
                'temperature': 0.3,
                'max_tokens': 2000,
                'model': 'gpt-3.5-turbo',
            }
        )
        experience_tailoring_agent = ExperienceTailoringAgent.from_llm_config(
            llm_config={
                'temperature': 0.3,
                'max_tokens': 2000,
                'model': 'gpt-4',
            }
        )
        jd_parsing_agent = JdParsingAgent.from_llm_config(
            llm_config={
                'temperature': 0.3,
                'max_tokens': 2000,
                'model': 'gpt-3.5-turbo'
            }
        )
        
        return {
            'responsibility_extracting_agent': responsibility_extracting_agent,
            'experience_tailoring_agent': experience_tailoring_agent,
            'jd_parsing_agent': jd_parsing_agent,
        }

    def start(self, save):
        base_resume = self.engine_config['base_resume']
        job_description = self.engine_config['job_description'].strip()

        jobs = []
        for job in base_resume['jobs']:
            job_details = self.agents['jd_parsing_agent'].act(job_description=job_description)
            job_title = job_details['job_title']
            responsibilities_and_highlights = self.agents['responsibility_extracting_agent'].act(job_title=job_title, jd=job_description, experience=job['desc'])
            updated_desc = self.agents['experience_tailoring_agent'].act(job_title=job_title, summary=responsibilities_and_highlights, experience=job['desc'])
            result = {
                **job,
                'desc': updated_desc['highlights']
            }
            jobs.append(result)

            # time.sleep(1)

        if save:
            job_title = job_details['title']
            job_title_formatted = '_'.join(job_title.lower().split(' '))
            # hash
            hash = hashlib.md5()
            hash.update(job_description.encode())
            jd_hashed = hash.hexdigest()  # 32 char string, 128-bit
            with open(os.path.join(self.storage, f'{job_title_formatted}-{jd_hashed}.txt'), 'w') as f:
                f.write(job_description)

        # # 5. update your experience
        updated_resume = {**base_resume, 'jobs': jobs}

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
        
        




