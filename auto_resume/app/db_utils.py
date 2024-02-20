
from auto_resume.db.client import create_db_client

from auto_resume.app.constants import DB_URI



def get_db_client():
    return create_db_client(DB_URI)