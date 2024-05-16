from sqlalchemy import create_engine
from bank import Account, Transaction, Base
import pytest
from bank import Account, Transaction  
from mock_alchemy.mocking import AlchemyMagicMock
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

# db_path = 'sqlite:///test_alchemy.db'

# engine = create_engine(db_path)
# Base.metadata.create_all(bind=engine)

@pytest.fixture
def account_factory():
    def make_account(balance):
        account = Account(balance) #ajouter l'argument engine si je test avec la session réelle
        # simulation d'une session avec AlchemyMagicMock 
        account.session = UnifiedAlchemyMagicMock()()
        account.create_account()
        return account
    return make_account

#UnifiedAlchemyMagicMock va servir a simuler une session afin d'éviter de faire des manipulations sur une bdd réelle
#on veut pas toucher a une bdd en production donc on va se servir de l'objet session mockée et de ses methodes pour 
#tester le bon fonctionnement de notre app