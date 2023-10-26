KEYWORD_INJECTING_PROMPT_TEMPLATE = """
You will be given a list of keywords extracted from a job description and experiences from one of your job histories.
Your goal is to rewrite the experiences by including the keywords:
Follow the steps below:
1. review the experiences
2. select 1-3 most relevant keywords from the job description from the job description from the job description.
3. rewrite the experiences with the selected keywords from the job description included

Here is your experiences:
{experiences}

Here is the keywords from the job description:
{keywords}

You should ONLY return an answer in JSON.
Here is an example of answer.
{{ "experiences": [{{ "selected_keywords": ["payment gateway", "strip"], "experience": "Integrated Strip for user subscripiton" }}, {{ "selected_keywords": ["web automation"], "experience": "Built a LinkedIn scraper for providing web automation services to job applicants" }}]}}
"""