from auto_resume.sdk.agents.base_agent import BaseAgent
from auto_resume.sdk.agents.experience_enhancing_agent.prompt_templates import *


class ExperienceEnhancingAgent(BaseAgent):
    NAME = 'experience_enhancing_agent'
    def get_messages(self, experiences: str):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': EXPERIENCE_ENHANCING_PROMPT_TEMPLATE.format(experiences=experiences)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)