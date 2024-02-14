from sqlalchemy import Column, Integer, Text

from auto_resume.db.models.base import Base


class Resume(Base):
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobAd = Column(Text, nullable=False)
    createdAt = Column(Text, nullable=False)
    otherInfo = Column(Text)