from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from auto_resume.db.models.base import Base


class Resume(Base):
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobAd = Column(Text, nullable=False)
    createdAt = Column(Text, nullable=False)
    otherInfo = Column(Text)
    job_histories = relationship("JobHistory", secondary="resume_job_history", back_populates='resumes')
