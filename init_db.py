from sqlalchemy import create_engine
from bank import Account, Transaction, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, declarative_base

db_path = 'sqlite:///test_alchemy.db'

engine = create_engine(db_path)

try:
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # account_un = Account(balance=800)
    # session.add(account_un)
    # session.commit()

    # account_deux = Account(balance=1500)
    # session.add(account_deux)
    # session.commit()

    # transaction = Transaction(1,400,"retrait")
    # session.add(transaction)
    # session.commit()

    # print(account_un.get_balance())
    # transaction_1 = account_un.depot(400)
    # session.add(transaction_1)
    # session.commit()

    # transaction_2 = account_un.retrait(800)
    # session.add(transaction_2)
    # session.commit()

    # transaction_2 = account_un.retrait(800)
    # session.add(transaction_2)
    # session.commit()

    # transaction_2 = account_un.transfert(account_deux,50)
    # session.add(transaction_2)
    # session.commit()

    

except Exception as ex:
    print(ex)