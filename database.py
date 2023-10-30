from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

# create .env and add host,port,user....etc and read it via AutoConfig
from decouple import AutoConfig
config = AutoConfig()

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# this is db connection:-

def get_dbURL():
  host =config('HOST') 
  port = config('PORT')
  user = config('USER')
  db = config('DB')
  passwd = config('PASSWD')
  DB_URL="mysql+mysqlconnector://{}:{}@{}:{}/{}?unix_socket=/var/run/mysqld/mysqld.sock".format(user,passwd,host,port,db) 
  
  return DB_URL

engine = create_engine(get_dbURL(),pool_size=10, max_overflow=20)
# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class StoneActivationStatus(Base):
    __tablename__ = "stone_activation_status"

    # id = Column(Integer, primary_key=True, index=True)
    stone_id = Column(String(30), primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    task_id = Column(String(80), index=True)
    activation_start_time = Column(DateTime, default=datetime.now())
    activation_end_time = Column(DateTime, default=datetime.now() + timedelta(seconds=10))

# Create the database tables
Base.metadata.create_all(bind=engine)