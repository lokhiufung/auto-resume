from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def create_db_client(uri):
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
