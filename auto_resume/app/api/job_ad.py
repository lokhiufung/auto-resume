from auto_resume.sdk.agents.jd_parsing_agent.agent import JdParsingAgent


def extract_keywords(job_ad):
    agent = JdParsingAgent.from_llm_config(
        llm_config={
            'model': 'gpt-4-0125-preview',
            'max_tokens': 2000,
            'temperature': 0.1,
        }
    )
    return agent.act(job_description=job_ad)



    
    


