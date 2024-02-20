from sqlalchemy.orm import Session

from auto_resume.db.models import Company, JobHistory, Title


def get_job_histories(db_client: Session, company_name: str):
    """
    Retrieves job histories for a specific company.
    
    :param db_client: The database client (SQLAlchemy session) to use for the query.
    :param company_name: The name of the company whose job histories are to be retrieved.
    :return: A list of job history records.
    """
    # Query the Company table to retrieve the company's ID
    company = db_client.query(Company).filter(Company.name == company_name).first()
    
    # If the company does not exist, return an empty list or raise an error
    if not company:
        return []
        # Alternatively, you can raise an error
        # raise ValueError(f"Company with name {company_name} does not exist.")

    # Query the JobHistory table using the retrieved company ID
    job_histories = db_client.query(JobHistory).filter(JobHistory.companyId == company.id).all()
    
    return job_histories


def create_job_history(db_client: Session, company_name: str, title: str, description: str):
    """
    Creates a new job history record for a company.
    
    :param db_client: The database client (SQLAlchemy session) to use for adding the job history.
    :param company_name: The name of the company for which the job history is being added.
    :param title: The title of the job history.
    :param description: The description of the job history.
    :return: The newly created job history object.
    """
    # Query the Company table to retrieve the company's ID
    company = db_client.query(Company).filter(Company.name == company_name).first()
    
    # If the company does not exist, you can either return None, raise an error, or create the company
    if not company:
        # Option 1: raise an error
        raise ValueError(f"Company with name {company_name} does not exist.")
        
        # Option 2: create the company (if your logic allows it)
        # company = Company(name=company_name)
        # db_client.add(company)
        # db_client.commit()

    title_obj = db_client.query(Title).filter_by(title=title).first()
    if not title_obj:
        title_obj = Title(title=title)
        db_client.add(title_obj)
        db_client.commit()
    # Create a new JobHistory record
    new_job_history = JobHistory(
        companyId=company.id,
        titleId=title_obj.id,
        description=description
    )
    
    # Add the new job history record to the session and commit
    db_client.add(new_job_history)
    db_client.commit()
    
    return new_job_history
