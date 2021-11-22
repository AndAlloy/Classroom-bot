import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('postgresql://postgres:1@localhost:5432/alchemy')
Session = sessionmaker(bind=engine)

Base = declarative_base()
