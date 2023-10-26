from abc import ABC, abstractmethod
from auto_resume.sdk.color_print_mixin import ColorPrintMixin
from auto_resume.sdk.text_parser_mixin import TextParserMixin
from auto_resume.sdk.errors import AgentMaxRetryError, LLMMaxRetryError


class BaseAgent(ABC, ColorPrintMixin, TextParserMixin):
    NAME = None

    def __init__(self, llm, debug=True, max_agent_act_retries=1, version="stable"):
        self.name = self.NAME
        if not self.name:
            raise ValueError('Must provide a NAME when creating the agent class')
        self.max_agent_act_retries = max_agent_act_retries
        self.llm = llm

        self.debug = debug  # TODO: fung: add a debug mode for color print in console
        self.version = version

    def _try_act(self, agent_act_retried, **kwargs):
        try:
            return self._act(**kwargs)
        except LLMMaxRetryError as err:
            # if there are problems when calling llm, raise an error immediately
            raise LLMMaxRetryError(calls_retried=err.calls_retried)  # tmp: fung: may not be a good practice to handle error again in the agent layer
        except Exception as err:
            if agent_act_retried < self.max_agent_act_retries:
                print(f"Error when parsing agent output. {err}\nRetrying {agent_act_retried} of {self.max_agent_act_retries}...")
                return self._try_act(agent_act_retried=agent_act_retried+1, **kwargs)
            else:
                raise AgentMaxRetryError(agent_act_retried)

    def _act(self, **kwargs):
        # get prompts
        prompts = self.get_messages(**kwargs)
        # call llm
        self.print_user_message('kwargs', kwargs)
        self.print_user_message('prompts', prompts)
        llm_output = self.llm.run(
            messages=prompts
        )
        self.print_agent_message(self.name, str(llm_output))
        agent_action = self.get_action(llm_output)
        return agent_action

    def act(self, **kwargs):
        return self._try_act(**kwargs, agent_act_retried=0)

    @abstractmethod
    def get_messages(self, *kwargs):
        """"""

    @abstractmethod
    def get_action(self, generated_text):
        """"""
    
    @classmethod
    def from_llm_config(cls, llm_config, llm_backend='openai', max_api_call_retries=3, max_agent_act_retries=1, *args, **kwargs):
        if llm_backend == 'openai':
            from auto_resume.sdk.llms.openai_llm import OpenaiLLM

            llm = OpenaiLLM(llm_config, max_api_call_retries)
        else:
            raise ValueError(f'{llm_backend} is not supported now')
        
        # build an agent
        agent = cls(llm=llm, max_agent_act_retries=max_agent_act_retries, *args, **kwargs)
        return agent