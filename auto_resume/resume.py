from typing import List
import json

from auto_resume.sdk.create_resume import create_resume


class Experience:
    def __init__(
            self,
            title,
            duration,
            location,
            highlights
        ):
        self.title = title
        self.duration = duration
        self.location = location
        self.highlights = highlights
    
    def to_json(self):
        return {
            'title': self.title,
            'duration': self.duration,
            'location': self.location,
            'highlights': self.highlights
        }


class Resume:
    def __init__(
            self,
            name,
            title,
            location,
            phone,
            email,
            website,
            github,
            linkedin,
            summary,
            educations,
            experiences: List[Experience],
            skills,
        ):
        self.name = name
        self.title = title
        self.location = location
        self.phone = phone
        self.email = email
        self.website = website
        self.github = github
        self.linkedin = linkedin
        self.summary = summary
        self.educations = educations
        self.experiences = experiences
        self.skills = skills

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, 'r') as f:
            resume_json = json.load(f)
        return cls(**resume_json)
    
    def to_json(self):
        return {
            'name': self.name,
            'title': self.title,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'github': self.github,
            'linkedin': self.linkedin,
            'summary': self.summary,
            'educations': self.educations,
            'experiences': [experience.to_json() for experience in self.experiences],
            'skills': self.skills
        }
    
    def to_docx(self, file_path):
        docx_resume = create_resume(resume=self.to_json())
        docx_resume.save(file_path)
    
    def update_experiences(self, experiences: List[Experience]):
        self.experiences = experiences


    