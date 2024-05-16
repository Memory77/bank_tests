from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, scoped_session
from datetime import datetime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id_account = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer)
    transactions = relationship("Transaction", back_populates="accounts")
    
    def __init__(self, balance, engine=None):
        self.balance = balance
        self.session = scoped_session(sessionmaker(bind=engine))
       
    def create_account(self):
        self.session.add(self)
        self.session.commit()
        
    
    def get_balance(self):
        return self.balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            transaction = Transaction(self.id_account, amount, "deposit")
            self.session.add(transaction)
            self.session.commit()
    
    def withdraw(self, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            transaction = Transaction(self.id_account, amount, "withdraw")
            self.session.add(transaction)
            self.session.commit()

    def transfer(self, other_account, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            other_account.balance += amount
            transfer_emetteur = Transaction(self.id_account, amount, "transfer")
            transfer_recepteur = Transaction(self.id_account, amount, "transfer")
            self.session.add(transfer_emetteur)
            self.session.commit()
            other_account.session.add(transfer_recepteur)
            other_account.session.commit()
        


class Transaction(Base):
    __tablename__ = 'transactions'
    id_transaction = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id_account"))
    amount = Column(Float)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
    accounts = relationship("Account", back_populates="transactions")

    def __init__(self, account_id, amount, type):
        self.account_id = account_id
        self.amount = amount
        self.type = type
    
    
       