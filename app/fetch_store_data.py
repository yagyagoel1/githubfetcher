import os 
import sys


import requests
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import subprocess

#appending path to able to access the logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
from logger import logger
from api_config import GITHUB_API_URL, GITHUB_USER
from database import engine, Repo

#connecting to the database
Session = sessionmaker(bind=engine)
session = Session()

#fetching of the data from the api 
def fetch_github_repositories(user):
    url = f"{GITHUB_API_URL}/users/{user}/repos"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as err:
        logger.error(f"error : {err}")


def store_repository_data(data):
    
    #editing the date to make it compatible with the database timing
    for repo in data:
        if 'created_at' in repo:
            repo['created_at'] = datetime.fromisoformat(repo['created_at'].replace('Z', '+00:00'))
        if 'updated_at' in repo:
            repo['updated_at'] = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
        
        #check if repository already exists by name
        existing_repo = session.query(Repo).filter_by(name=repo['name']).first()
        
        #creating the repo if the repo with same name does not exist
        if not existing_repo:
            repo_entry = Repo(
                id=repo['id'],
                name=repo['name'],
                full_name=repo['full_name'],
                description=repo['description'],
                language=repo['language'],
                created_at=repo['created_at'],
                updated_at=repo['updated_at']
            )
            #adding the repo to the table
            session.add(repo_entry)
            logger.info(f"Added repository {repo['name']}")
        else:
            logger.info(f"Repository {repo['name']} already exists, skipping.")

    session.commit()
    logger.info(f"Stored {len(data)} repositories for user {GITHUB_USER}")



if __name__ == "__main__":
    data = fetch_github_repositories(GITHUB_USER)
    #if the fetch waas successful store it to the repository  
    if data:
        store_repository_data(data)

    #eun the streamlit process as sub process
    subprocess.run(["streamlit", "run", "dashboard/dashboard.py"])