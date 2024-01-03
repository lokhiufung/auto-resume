from auto_resume.sdk.agents.base_agent import BaseAgent


SYSTEM_PROMPT_TEMPLATE = """
You are an expert resume writer with over 20 years of experience working with job seekers trying to land a role in {job_title}.
You will be given a job advertisement and a job experience. Highlight the 5 most important responsibilities in the following job advertisement, and write down 5 highlights of skills or experience match with this position based on the job experience:

You should only return answer in JSON format. Here is an example answer:
{{
    "responsibilities": [
        <responsibilty 1>,
        <responsibilty 2>,
        ...
    ],
    "highlights": [
        <highlight 1>,
        <highlight 2>,
        ...
    ]
}}
"""

USER_PROMPT_TEMPLATE = """
Here is the job advertisement:
###
{jd}
###

Here is the job experience:
###
{experience}
###
"""

class ReponsibilityExtractingAgent(BaseAgent):

    NAME = 'responsibility_extracting_agent'
    def get_messages(self, job_title: str, jd: str, experience: str):
        return [
            {'role': 'system', 'content': SYSTEM_PROMPT_TEMPLATE.format(job_title=job_title)},  # TEMP
            {'role': 'user', 'content': USER_PROMPT_TEMPLATE.format(jd=jd, experience=experience)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)