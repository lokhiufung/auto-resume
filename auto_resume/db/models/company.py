from sqlalchemy import Column, Text, String, Integer
from sqlalchemy.orm import relationship


from auto_resume.db.models.base import Base


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    startDate = Column(Text, nullable=False)
    endDate = Column(Text)
    description = Column(Text)
    location = Column(String, nullable=False)
    job_histories = relationship("JobHistory", back_populates="company")
    