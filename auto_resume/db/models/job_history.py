from sqlalchemy import Column, Text, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from auto_resume.db.models.base import Base


class JobHistory(Base):
    __tablename__ = 'job_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    titleId = Column(String, ForeignKey('title.id'), nullable=False)
    description = Column(Text)
    company = relationship("Company", back_populates="job_histories")
    resumes = relationship("Resume", secondary="resume_job_history", back_populates='job_histories')
    title = relationship("Title", back_populates="job_histories")