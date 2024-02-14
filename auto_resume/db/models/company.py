from sqlalchemy import Column, Text, String, Integer
from sqlalchemy.orm import relationship


from auto_resume.db.models.base import Base


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    job_histories = relationship("JobHistory", back_populates="company")
    