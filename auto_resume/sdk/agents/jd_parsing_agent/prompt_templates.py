JD_PARSING_PROMPT_TEMPLATE = """
You will be given a job description and your goal is to extract the job title, skills, keywords from it.
Here is the job description:
```
{job_description}
```

You should ONLY return an answer in JSON.
Here is an example of answer.
{{ "job_title": "Content Creator", "skills": ["Fluent English", "Typing"], "keywords": ["Lead generation", "Promoting"]}}
"""