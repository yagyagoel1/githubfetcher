from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#defining the database location
engine = create_engine('sqlite:///data/github_data.db')
Base = declarative_base()


#creating the schema for the database 
class Repo(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    full_name = Column(String, index=True)
    description = Column(Text)
    language = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


#creating the table in the database if not exists
Base.metadata.create_all(engine)
