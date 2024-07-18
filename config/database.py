import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite" 
base_dir = os.path.dirname(os.path.realpath(__file__))
#We read the current directory (__file__) to creathe an URL

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

#Motor of database
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
