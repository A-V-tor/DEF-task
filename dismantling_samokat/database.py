import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# engine = create_engine('sqlite:///database/database.db')
engine = create_engine('postgresql+psycopg2://admin:admin@db/db')
db = Session(engine)
