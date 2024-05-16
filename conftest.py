import pytest
from unittest.mock import MagicMock
from bank import Account, Transaction  
from mock_alchemy.mocking import AlchemyMagicMock

# @pytest.fixture
# def engine():
#     return AlchemyMagicMock()

@pytest.fixture
def account_factory():
    def make_account(balance):
        account = Account(balance)
        # simulation d'une session avec AlchemyMagicMock
        account.session = AlchemyMagicMock()
        account.create_account()
        return account
    return make_account