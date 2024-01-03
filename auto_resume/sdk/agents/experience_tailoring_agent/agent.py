from auto_resume.sdk.agents.base_agent import BaseAgent


SYSTEM_PROMPT_TEMPLATE = """
You are an expert resume writer with over 20 years of experience working with job seekers trying to land a role in {job_title}.
You goal is to tailor your job experience to apply for a job based on a summary of responsibilities of the job and relevant highlights of your experience from another expert.

The highlights of your job experience must follow the requirements below:
1. the highlights must use actionable words
2. the highlights must clearly state the job duty
3. the highlights must include key skills
4. the highlights are achievement focused and the achievements are quantifiable (e.g 30% improvment, 30% cost reduction, 50% increase in productivity)
5. the highlights must be based on facts (i.e as described in my job experience) and you should improvise only from the facts

You should only return answer in JSON format. Here is an example answer:
{{
    "highlights": [
        "Reduced cost of customer service by 30% by building a automated FAQ supporting chatbot with Python, Fastapi, MongoDB", "Ensured code quality and reliability through rigorous testing, resulting in a 99.5% uptime for the chatbot system",
        <...you should tailor 3-5 highlights here>,
        ...
}}
"""

USER_PROMPT_TEMPLATE = """
Here is the a summary of responsibilities of the job and relevant highlights of your experience from another expert:
###
{summary}
###

Here is the job experience to be tailored:
###
{experience}
###
"""


class ExperienceTailoringAgent(BaseAgent):

    NAME = 'experience_tailoring_agent'
    def get_messages(self, job_title: str, summary: str, experience: str):
        return [
            {'role': 'system', 'content': SYSTEM_PROMPT_TEMPLATE.format(job_title=job_title)},  # TEMP
            {'role': 'user', 'content': USER_PROMPT_TEMPLATE.format(summary=summary, experience=experience)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)