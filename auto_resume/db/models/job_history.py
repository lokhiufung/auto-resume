from sqlalchemy import Column, Text, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from auto_resume.db.models.base import Base


class JobHistory(Base):
    __tablename__ = 'job_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    title = Column(String, nullable=False)
    startDate = Column(Text, nullable=False)
    endDate = Column(Text)
    des = Column(Text)
    location = Column(String, nullable=False)
    company = relationship("Company", back_populates="job_histories")
    resumes = relationship("Resume", secondary="resume_job_history")
    titles = relationship("Title", secondary="title_job_history")