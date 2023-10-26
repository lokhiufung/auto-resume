from auto_resume.sdk.agents.base_agent import BaseAgent
from auto_resume.sdk.agents.skill_injecting_agent.prompt_templates import *


class SkillInjectingAgent(BaseAgent):
    NAME = 'skill_injecting_agent'

    def get_messages(self, experiences, skills):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': SKILL_INJECTING_PROMPT_TEMPLATE.format(experiences=experiences, skills=skills)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)