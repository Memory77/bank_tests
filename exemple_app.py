from sqlalchemy import create_engine
from bank import Base, Account, Transaction
from sqlalchemy.orm import sessionmaker
from init_db import *


try:
    
    # - Création de deux comptes
    # - Dépôt initial de 100 sur le compte 1, 50 sur le compte 2
    account_un = Account(balance=100, engine=engine)
    account_un.create_account()
    account_deux = Account(balance=50, engine=engine)
    account_deux.create_account()
    
    #Transfer de 50 du compte 1 à 2.
    account_un.transfer(account_deux,50)
    account_un.deposit(1)

except Exception as ex:
    print(ex)