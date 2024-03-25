import os

import openai
import tiktoken

from auto_resume.sdk.llms.base_llm import BaseLLM
from auto_resume.sdk.color_print_mixin import print


class OpenaiLLM(BaseLLM):
    llm_backend = 'openai'
    
    def __init__(self, llm_config, max_api_call_retries=3):
        super().__init__(llm_config, max_api_call_retries)
        api_key = os.getenv('OPENAI_API_KEY')
        assert api_key, 'Empty OPENAI_API_KEY'
        openai.api_key = api_key
        self.name = llm_config['model']
        self.ttl_tokens_used = 0  # TEMP

    def _request(self, params):
        # TEMP
        print(f"Requesting OpenAI API", style='bold red')
        print(params, style='red')
        res = openai.chat.completions.create(**params)
        # TEMP
        num_tokens = self.num_tokens_from_messages(params['messages'])
        self.ttl_tokens_used += num_tokens
        return res

    def run_function_call(self, messages, functions=[], function_call=None):
        params = {
            "messages": messages,
            "functions": functions,
            "function_call": function_call,
            **self.llm_config
        }
        res = self._try_request(params, openai_calls_retried=0)
        if res.choices[0].finish_reason == 'function_call':
            return res.choices[0].function_call
        else:
            return res.choices[0].message.content.strip()

    def run(self, messages):
        params = {
            "messages": messages,
            **self.llm_config
        }
        res = self._try_request(params, openai_calls_retried=0)
        return res.choices[0].message.content.strip()
        
    def num_tokens_from_messages(self, messages, model: str=None):
        """Returns the number of tokens used by a list of messages.
        Source: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        """
        if model is None:
            model = self.name
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
            return self.num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return self.num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

