from sqlalchemy import Column, Integer, ForeignKey


from auto_resume.db.models.base import Base


class ResumeJobHistory(Base):
    __tablename__ = 'resume_job_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    resumeId = Column(Integer, ForeignKey('resume.id'), nullable=False)
    jobHistoryId = Column(Integer, ForeignKey('job_history.id'), nullable=False)
