import time

from auto_resume.sdk.logger import get_logger
# import agents
from auto_resume.sdk.agents.experience_enhancing_agent.agent import ExperienceEnhancingAgent
from auto_resume.sdk.agents.jd_parsing_agent.agent import JdParsingAgent
from auto_resume.sdk.agents.keyword_injecting_agent.agent import KeywordInjectingAgent
from auto_resume.sdk.agents.skill_injecting_agent.agent import SkillInjectingAgent
from auto_resume.sdk.evaluate_resume import evaluate_resume


logger = get_logger('engine.log', logger_lv='debug')


class Engine:

    ENGINE_CONFIG = {}  # default config

    def __init__(self, engine_config):
        self.agents = {}
        self.engine_config = {**self.ENGINE_CONFIG, **engine_config}  # engine_config always override the default configs
        # initialize 
        self.agents = self.create_agents()

    def create_agents(self):
        # TODO: llm_config may be tunable parameters?
        llm_config={
            'temperature': 0.3,
            'max_tokens': 2000,
            'model': 'gpt-3.5-turbo'
        }
        llm_backend = 'openai'

        experience_enhancing_agent = ExperienceEnhancingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        jd_parsing_agent = JdParsingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        skill_injecting_agent = SkillInjectingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        keyword_injecting_agent = KeywordInjectingAgent.from_llm_config(llm_config, llm_backend=llm_backend)
        
        return {
            'experience_enhancing_agent': experience_enhancing_agent,
            'jd_parsing_agent': jd_parsing_agent,
            'skill_injecting_agent': skill_injecting_agent,
            'keyword_injecting_agent': keyword_injecting_agent,
        }

    def start(self):
        base_resume = self.engine_config['base_resume']
        job_description = self.engine_config['job_description']

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
        
        




