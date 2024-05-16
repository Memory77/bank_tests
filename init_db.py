from sqlalchemy import create_engine
from bank import Account, Transaction, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, declarative_base

db_path = 'sqlite:///test_alchemy.db'

engine = create_engine(db_path)

try:
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

   

except Exception as ex:
    print(ex)