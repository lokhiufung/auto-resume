import argparse
import json
import time

# import engine
from auto_resume.engine_v1 import Engine
# import utility functions
from auto_resume.sdk.create_resume import create_resume


LLM_BACKEND = 'openai'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--jd', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--output', type=str, default='resume-updated.docx', help="the file path to your output resume")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="the model name of openai model, i.e gpt-3.5-turbo, gpt-4... etc. default to gpt-3.5-turbo")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.resume, 'r') as f:
        base_resume = json.load(f)
    with open(args.jd, 'r') as f:
        job_description = f.read()

    engine_config = {
        'base_resume': base_resume,
        'job_description': job_description,
    }
    output_file_path = args.output

    # initialize engine
    engine = Engine(
        engine_config=engine_config
    )
    result = engine.start()

    # check metrics
    print(result['metrics'])

    # create resume in doc
    doc = create_resume(resume=result['result'])
    doc.save(output_file_path)


