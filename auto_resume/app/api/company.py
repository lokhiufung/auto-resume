from sqlalchemy.orm import Session
from auto_resume.db.models import Company


def get_companies(db_client: Session, company_name: str=None):
    # Use the session provided by db_client to query companies by name
    # If company_name is None or empty, return all companies
    if company_name:
        return db_client.query(Company).filter(Company.name == company_name).all()
    else:
        return db_client.query(Company).all()

def create_company(db_client: Session, company_name: str, description: str, start_date: str, end_date: str, location: str):
    # Create a new instance of the Company model
    new_company = Company(
        name=company_name,
        startDate=start_date,  # Make sure your model has fields for these attributes
        endDate=end_date,
        description=description,
        location=location
    )
    # Add the new company to the session and commit the transaction
    db_client.add(new_company)
    db_client.commit()

    # Return the newly created company record
    return new_company
