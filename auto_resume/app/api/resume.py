import tempfile

import json

from auto_resume.app.constants import BASE_RESUME_FILE_PATH

from auto_resume.sdk.resume_templates.create_resume_v1 import create_resume
# from auto_resume.sdk.resume_templates.create_resume_v2 import create_resume
# from auto_resume.sdk.resume_templates.create_resume_v3 import create_resume




def export_resume(data):
    with open(BASE_RESUME_FILE_PATH, 'r') as f:
        resume = json.load(f)

    # prepare new work experiences
    # TODO: I should make a better format for the basse resume json
    jobs = []
    for exp in data:
        job = dict()
        job['title'] = exp['experiences'][0]['title']  # TODO: use the first title, change it later
        # TEMP: fix this later
        end_date = exp['end_date']
        if end_date is None:
            end_date = ''
        job['duration'] = exp['start_date'] + end_date
        job['location'] = exp['location']
        job['company'] = exp['company']
        job['desc'] = [experience['description'] for experience in exp['experiences']]
        jobs.append(job)
    
    # update the jobs
    resume['jobs'] = jobs
    # export
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    
    # Export the resume as a .docx file
    docx_resume = create_resume(resume)
    docx_resume.save(temp_file.name)

    # Make sure to close the file after saving
    temp_file.close()

    # Return the path to the saved file
    docx_resume = create_resume(resume)
    docx_resume.save(temp_file.name)
    return temp_file.name
    



        
