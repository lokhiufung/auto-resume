import argparse
import json
import time
import os

# import utility functions
from auto_resume.sdk.resume_templates.create_resume_v1 import create_resume


LLM_BACKEND = 'openai'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--jd', type=str, required=True, help="the file path to your json formmated resume")
    parser.add_argument('--output', type=str, default='resume-updated.docx', help="the file path to your output resume")
    # parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="the model name of openai model, i.e gpt-3.5-turbo, gpt-4... etc. default to gpt-3.5-turbo")
    parser.add_argument('--version', '-v', type=str, default='v1', help="the version of engine")
    parser.add_argument('--save', default=True, help='store the job title and jd')
    parser.add_argument('--storage', default='./storage', help='store the job title and jd')
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
    
    if not os.path.exists(args.storage):
        os.mkdir(args.storage)

    # initialize engine
    print(f'Using engine version={args.version}')
    if args.version == 'v1':
        # import engine
        from auto_resume.engine_v1 import Engine
        
        engine = Engine(
            engine_config=engine_config,
            storage=args.storage
        )
    else:
        # import engine
        from auto_resume.engine_v2 import Engine
        
        engine = Engine(
            engine_config=engine_config,
            storage=args.storage
        )

    result = engine.start(save=args.save)

    # check metrics
    print(result['metrics'])

    # create resume in doc
    doc = create_resume(resume=result['result'])
    doc.save(output_file_path)


