EXPERIENCE_ENHANCING_PROMPT_TEMPLATE = """
You will be given some experiences from one of your job histories.
Your goal is to enhance your experiences by following the requirements below:
1. the experiences must use actionable words
2. the experiences must clearly state the job duty
3. the experiences must include key skills
4. the experience are achievement focused and the achievements are quantifiable (e.g 30% improvment, 30% cost reduction, 50% increase in productivity)

Here is your experiences:
{experiences}

You should ONLY return an answer in JSON.
Here is an example of answer.
{{ "experiences": ["Reduced cost of customer service by 30% by building a automated FAQ supporting chatbot with Python, Fastapi, MongoDB", "Ensured code quality and reliability through rigorous testing, resulting in a 99.5% uptime for the chatbot system"] }}
"""