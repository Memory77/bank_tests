import pytest 
import datetime
from bank import Account, Transaction
from sqlalchemy import func
from unittest.mock import MagicMock
# Explication de call_args[0][0]
# call_args est une propriété de l'objet MagicMock qui enregistre les arguments avec lesquels la méthode mockée a 
# été appelée pour la dernière fois.
# call_args[0] accède aux arguments positionnels passés à la méthode mockée. Cela retourne un tuple contenant tous
# les arguments positionnels.
# call_args[0][0] accède au premier argument positionnel de la dernière appelée. Dans le cas de session.add(transaction),
# ce premier argument est l'objet Transaction que vous voulez vérifier.

def test_deposit_normal(account_factory):
    account = account_factory(100)
    account.deposit(50)
    assert account.get_balance() == 150 # Vérifier que le solde est mis à jour
    assert account.session.commit.called # Vérifier que le session.commit() a été appelé.
    transaction = account.session.add.call_args[0][0]
    assert transaction.amount == 50 #Vérifier que la transaction est d'un montant de 50.
    assert transaction.type == "deposit" #Vérifier que la transaction est correctement ajoutée avec le type "deposit".
    #assert transaction.timestamp  #Vérifier que le timestamp de la transaction est correctement enregistré.
    #assert account.session.query(Transaction).count() == 1

def test_deposit_negative_amount(account_factory):
    account = account_factory(100)
    #Tenter de déposer un montant négatif.
    account.deposit(-50)
    #Vérifier que le solde du compte n'a pas changé.
    assert account.balance == 100
    #verifier qu'il n'y a pas eu de transaction
    assert account.session.add.call_count == 1 
    #Vérifier que le session.commit() n'a pas été appelé.
    assert account.session.commit.call_count == 1 

def test_deposit_zero_amount(account_factory):
    account = account_factory(100)
    #Tenter de déposer un montant négatif.
    account.deposit(0)
    #Vérifier que le solde du compte n'a pas changé.
    assert account.balance == 100
    #verifier qu'il n'y a pas eu de transaction
    assert account.session.add.call_count == 1 
    #Vérifier que le session.commit() n'a pas été appelé.
    assert account.session.commit.call_count == 1 

def test_withdraw_normal(account_factory):
    account = account_factory(100)
    account.withdraw(50)
    assert account.get_balance() == 50 # Vérifier que le solde est correctement déduit.
    transaction = account.session.add.call_args[0][0]
    assert transaction.type == "withdraw"
    assert account.session.commit.call_count == 2  # Vérifier que le session.commit() a été appelé.


def test_withdraw_insufficient_funds(account_factory):
    account = account_factory(100)
    #Tenter de retirer un montant supérieur au solde disponible.
    account.withdraw(150)
    #Vérifier que le solde reste inchangé.
    assert account.get_balance() == 100
    #Vérifier qu'aucune transaction n'est ajoutée.
    assert account.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé
    assert account.session.commit.call_count == 1

def test_withdraw_negative_amount(account_factory):
    account = account_factory(100)
    #Tenter de retirer un montant négatif.
    account.withdraw(-10)
    #Vérifier que le solde reste inchangé.
    assert account.get_balance() == 100
    #Vérifier qu'aucune transaction n'est ajoutée.
    assert account.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé
    assert account.session.commit.call_count == 1


def test_withdraw_zero_amount(account_factory):
    account = account_factory(100)
    #Tenter de retirer un montant nul.
    account.withdraw(0)
    #Vérifier que le solde reste inchangé.
    assert account.get_balance() == 100
    #Vérifier qu'aucune transaction n'est créée.
    assert account.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé
    assert account.session.commit.call_count == 1

def test_transfer_normal(account_factory):
    account_un = account_factory(100)
    account_deux = account_factory(200)

    #Effectuer un transfert entre deux comptes avec des soldes suffisants.
    account_un.transfer(account_deux,50)

    #Vérifier que le montant est déduit du compte source.
    assert account_un.get_balance() == 50
    #Vérifier que le montant est ajouté au compte cible.
    assert account_deux.get_balance() == 250
    #Vérifier que deux transactions sont créées avec les types appropriés.
    assert account_un.session.add.call_count == 2
    assert account_deux.session.add.call_count == 2
    transfer_emetteur = account_un.session.add.call_args[0][0]
    transfer_recepteur = account_deux.session.add.call_args[0][0]
    assert transfer_emetteur.type == "transfer"
    assert transfer_recepteur.type == "transfer"
    #Vérifier que le session.commit() a été appelé.
    assert account_un.session.commit.call_count == 2
    assert account_deux.session.commit.call_count == 2

def test_transfert_insufficient_funds(account_factory):
    account_un = account_factory(50)
    account_deux = account_factory(200)

    #Tenter un transfert avec un solde insuffisant sur le compte source.
    account_un.transfer(account_deux,100)
    #Vérifier que le solde des deux comptes reste inchangé.
    assert account_un.get_balance() == 50
    assert account_deux.get_balance() == 200
    #Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
    assert account_un.session.add.call_count == 1
    assert account_deux.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé.
    assert account_un.session.commit.call_count == 1
    assert account_deux.session.commit.call_count == 1

def test_transfer_negative_amount(account_factory):
    account_un = account_factory(50)
    account_deux = account_factory(200)

    #Tenter de transférer un montant négatif.
    account_un.transfer(account_deux,-10)
    #Vérifier que le solde des deux comptes reste inchangé.
    assert account_un.get_balance() == 50
    assert account_deux.get_balance() == 200
    #Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
    assert account_un.session.add.call_count == 1
    assert account_deux.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé.
    assert account_un.session.commit.call_count == 1
    assert account_deux.session.commit.call_count == 1

def test_transfer_zero_amount(account_factory):
    account_un = account_factory(50)
    account_deux = account_factory(200)

    #Tenter de transférer un montant nul.
    account_un.transfer(account_deux,0)
    #Vérifier que le solde des deux comptes reste inchangé.
    assert account_un.get_balance() == 50
    assert account_deux.get_balance() == 200
    #Vérifier qu'aucune transaction n'est ajoutée pour les deux comptes.
    assert account_un.session.add.call_count == 1
    assert account_deux.session.add.call_count == 1
    #Vérifier que le session.commit() n'a pas été appelé.
    assert account_un.session.commit.call_count == 1
    assert account_deux.session.commit.call_count == 1



def test_get_balance_initial(account_factory):
    account_un = account_factory(50)
    assert account_un.get_balance() == 50
    #verif get_balance apres depot
    account_un.deposit(1)
    assert account_un.get_balance() == 51
    #verif get_balance apres transfer qui fonctionne bien
    account_deux = account_factory(60)
    account_un.transfer(account_deux, 10)
    assert account_un.get_balance() == 41
    assert account_deux.get_balance() == 70
    #verif get_balance apres transfer qui ne fonctionnera pas car montant négatif
    account_un.transfer(account_deux, -10)
    assert account_un.get_balance() == 41
    assert account_deux.get_balance() == 70 #reste inchangé


@pytest.mark.parametrize("amount, expected_balance",
                          [(400,900), (40,540)])
def test_deposit_with_param(account_factory, amount, expected_balance):
    account = account_factory(500)
    account.deposit(amount)
    assert account.get_balance() == expected_balance


@pytest.mark.parametrize("amount, expected_balance",
                          [(400,100), (40,460)])
def test_withdraw_with_param(account_factory, amount, expected_balance):
    account = account_factory(500)
    account.withdraw(amount)
    assert account.get_balance() == expected_balance


@pytest.mark.parametrize("amount, expected_balance_emetteur, expected_balance_recepteur",
                          [(400,100,1400), (40,460,1040), ])
def test_transfer_with_param(account_factory, amount, expected_balance_emetteur, expected_balance_recepteur):
    account_un = account_factory(500)
    account_deux = account_factory(1000)
    account_un.transfer(account_deux,amount)
    assert account_un.get_balance() == expected_balance_emetteur
    assert account_deux.get_balance() == expected_balance_recepteur