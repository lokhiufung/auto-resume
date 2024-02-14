import json
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from auto_resume.db.models import *
from auto_resume.sdk.vector_stores.annoy_vector_store import AnnoyVectorStore
from auto_resume.sdk.embedding_models.sentence_transformer_embedding_model import SentenceTransformerEmbeddingModel



def migrate_job_histories(session, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            
            # Process company
            company_data = data['company']
            company = session.query(Company).filter_by(name=company_data['name']).first()
            if not company:
                company = Company(name=company_data['name'], description=company_data['location'])
                session.add(company)
                session.commit()
            
            # Process job history (ignoring the provided ID and letting the database generate it)
            job_history = JobHistory(
                companyId=company.id,
                title=", ".join(data['titles']),  # Assuming there could be multiple titles
                startDate=company_data['duration'].split('–')[0],
                endDate=company_data['duration'].split('–')[1] if '–' in company_data['duration'] else None,
                des=data['desc'],
                location=company_data['location']
            )
            session.add(job_history)
            session.commit()
            
            # Process titles
            for title_name in data['titles']:
                title = session.query(Title).filter_by(title=title_name).first()
                if not title:
                    title = Title(title=title_name)
                    session.add(title)
                    session.commit()
                
                # Create or update TitleJobHistory relationship
                title_job_history = TitleJobHistory(title_id=title.id, job_history_id=job_history.id)
                session.add(title_job_history)
            session.commit()



def build_annoy_vector_database(session, store_path):
    model_config = {}
    

    companies = session.query(Company).all()
    embedding_model = SentenceTransformerEmbeddingModel(model_config)
    # build a vector database for each company
    for company in companies:
        job_histories = []
        for job_history in company.job_histories:
            job_histories.append({
                'job_history_id': job_history.id,
                'company_id': job_history.companyId,
                'title': job_history.title,
                'start_date': job_history.startDate,
                'end_date': job_history.endDate,
                'des': job_history.des,
                'location': job_history.location,
                'content': job_history.des,  # REMINDER: this is for vector indexing
            })
        standardized_company_name = '_'.join(company.name.lower().strip().split(' '))
        vector_store_config = {
            'store_path': os.path.join(store_path, standardized_company_name),
            'dim': 384,
            'metric': 'angular',
            'n_trees': 10,
        }
        vector_store = AnnoyVectorStore(
            docs=job_histories,
            embedding_model=embedding_model,
            vector_store_config=vector_store_config
        )


def main():
    # inject job histories from jsonl
    cwd = os.getcwd()
    engine = create_engine(f'sqlite:///{cwd}/resume_job_history.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # drop all tables
    Base.metadata.drop_all(engine)
    # recreate
    Base.metadata.create_all(engine)

    # migrate_job_histories(session, file_path='./storage/base/highlight.jsonl')
    print('Creation of tables in the SQLite database has been completed successfully.')

    # build vector stores for each company
    store_file_path = './storage/vector_store'
    if not os.path.exists(store_file_path):
        os.makedirs(store_file_path)
    build_annoy_vector_database(session, store_path=store_file_path)
    print('Creation of vector_stores has been completed successfully.')

    session.close()
    

if __name__ == '__main__':
    main()