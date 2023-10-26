from auto_resume.sdk.agents.base_agent import BaseAgent
from auto_resume.sdk.agents.keyword_injecting_agent.prompt_templates import *


class KeywordInjectingAgent(BaseAgent):
    NAME = 'keyword_injecting_agent'
    def get_messages(self, experiences: str, keywords: list[str]):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': KEYWORD_INJECTING_PROMPT_TEMPLATE.format(experiences=experiences, keywords=keywords)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)