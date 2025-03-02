from auto_resume.sdk.agents.base_agent import BaseAgent
from auto_resume.sdk.agents.jd_parsing_agent.prompt_templates import *


class JdParsingAgent(BaseAgent):
    NAME = 'jd_parsing_agent'

    def get_messages(self, job_description):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': JD_PARSING_PROMPT_TEMPLATE.format(job_description=job_description)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)
        