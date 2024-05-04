from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# The libraries below are for connecting to postgres via the Psycopg postgres driver
# import psycopg
# from psycopg.rows import dict_row
# import time


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class from which our sqlalchemy models will inherit.
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# The code below is for connecting to postgres via the Psycopg postgres driver
# we want to loop the connection to the database until it's successfull
# while True:
#     try:
        # connect to database
        # conn = psycopg.connect(host='localhost', dbname='postgres', user='postgres',
        #                     password='F5V2h9JfH', row_factory=dict_row)
        # open a cursor to perform database operations
        # cur = conn.cursor()
        # print("Database connection was successfull")
    # except BaseException as error:
    #     print(error)
    #     time.sleep(2)
    # else:
    #     break