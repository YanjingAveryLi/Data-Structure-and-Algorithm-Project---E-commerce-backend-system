from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///products.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)