SKILL_INJECTING_PROMPT_TEMPLATE = """
You will be given a list of required skills and experiences from one of your job histories.
Your goal is to rewrite the experiences by including the required skills:
Follow the steps below:
1. review the experiences
2. select 1-3 most relevant skills from the required skills
3. rewrite the experiences with the selected skills included

Here is your experiences:
{experiences}

Here is the required skills:
{skills}

You should ONLY return an answer in JSON.
Here is an example of answer.
{{ "experiences": [{{ "selected_skills": ["Python", "SQL"], "experience": "Delivered a real-time Dashboard built with Python and SQL" }}, {{ "selected_skills": ["AWS", "S3"], "experience": "Delivered a serverless web applicaiton on AWS with S3 and Lambda" }}]}}
"""