from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from auto_resume.db.models.base import Base


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    job_histories = relationship("JobHistory", secondary="title_job_history")