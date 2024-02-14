from sqlalchemy import Column, Integer, ForeignKey

from auto_resume.db.models.base import Base


class TitleJobHistory(Base):
    __tablename__ = 'title_job_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title_id = Column(Integer, ForeignKey('title.id'), nullable=False)
    job_history_id = Column(Integer, ForeignKey('job_history.id'), nullable=False)