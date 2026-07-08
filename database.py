# import create_engine
from sqlalchemy import create_engine

# import sessionmaker
from sqlalchemy.orm import sessionmaker

# import declarative_base
from sqlalchemy.orm import declarative_base

# copy this from neon and replace the username , password , and host with your own credentials 


DATABASE_URL='postgresql+psycopg2://neondb_owner:npg_dy5wRlcXq7ph@ep-snowy-block-aodturqy-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
# here , we are connecting to a PostgreSQL database hosted on the cloud(neon)

# note : click , "Show Password" and copy the complete connection string

# create SQLAlchemy engine
# the engine is responsible for connecting FastAPI with the cloud PostgreSQL database
engine = create_engine(DATABASE_URL)

# create sessions as every database operation will use this session
SessionLocal = sessionmaker(bind= engine)

# base class as all database tables will inherit from this class
Base = declarative_base()

# dependency injection , this function provides a database 

def get_db():

    db = SessionLocal()

    try :

        yield db

    finally:

        db.close()
