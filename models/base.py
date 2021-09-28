#coding=utf-8

from sqlalchemy import create_engine,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db_example.db')
Session  = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()