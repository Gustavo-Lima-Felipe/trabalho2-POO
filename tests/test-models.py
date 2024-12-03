import pytest
from datetime import datetime, timedelta
from finances.models import Transaction, Account, Investment, Client


def test_transaction_initialization():
    """Testa a inicialização de um objeto Transaction."""
    transaction = Transaction(100.0, "Food", "Almoço no restaurante")
    assert transaction.amount == 100.0
    assert transaction.category == "Food"
    assert transaction.description == "Almoço no restaurante"
    assert isinstance(transaction.date, datetime)


def test_transaction_str():
    """Testa o método __str__ de Transaction."""
    transaction = Transaction(100.0, "Food", "Almoço no restaurante")
    assert str(transaction) == "Transação: Almoço no restaurante R$ 100.00 (Food)"


def test_transaction_update():
    """Testa o método update de Transaction."""
    transaction = Transaction(100.0, "Food", "Almoço no restaurante")
    transaction.update(amount=150.0, description="Jantar no restaurante")
    assert transaction.amount == 150.0
    assert transaction.description == "Jantar no restaurante"


def test_account_initialization():
    """Testa a inicialização de um objeto Account."""
    account = Account("Conta Corrente")
    assert account.name == "Conta Corrente"
    assert account.balance == 0.0
    assert account.transactions == []


def test_add_transaction():
    """Testa o método add_transaction de Account."""
    account = Account("Conta Corrente")
    transaction = account.add_transaction(200.0, "Salary", "Salário recebido")
    assert account.balance == 200.0
    assert len(account.transactions) == 1
    assert account.transactions[0] == transaction


def test_get_transactions():
    """Testa o método get_transactions de Account com diferentes filtros."""
    account = Account("Conta Corrente")
    transaction1 = account.add_transaction(200.0, "Salary", "Salário recebido")
    transaction2 = account.add_transaction(-50.0, "Food", "Almoço")
    transaction3 = account.add_transaction(-30.0, "Transport", "Uber")
    
    start_date = transaction1.date - timedelta(days=1)
    end_date = transaction2.date + timedelta(days=1)
    
    # Teste sem filtros
    assert len(account.get_transactions()) == 3
    
    # Teste com filtro por data
    transactions_filtered = account.get_transactions(start_date=start_date, end_date=end_date)
    assert len(transactions_filtered) == 2

    # Teste com filtro por categoria
    transactions_food = account.get_transactions(category="Food")
    assert len(transactions_food) == 1
    assert transactions_food[0].category == "Food"


def test_investment_initialization():
    """Testa a inicialização de um objeto Investment."""
    investment = Investment("Ações", 1000.0, 0.02)
    assert investment.type == "Ações"
    assert investment.initial_amount == 1000.0
    assert isinstance(investment.date_purchased, datetime)
    assert investment.rate_of_return == 0.02


def test_investment_calculate_value():
    """Testa o método calculate_value de Investment."""
    investment = Investment("Ações", 1000.0, 0.02)
    investment.date_purchased -= timedelta(days=90)  # 3 meses atrás
    assert pytest.approx(investment.calculate_value(), rel=1e-2) == 1000.0 * (1.02 ** 3)


def test_investment_sell():
    """Testa o método sell de Investment."""
    account = Account("Conta Corrente")
    investment = Investment("Ações", 1000.0, 0.02)
    investment.date_purchased -= timedelta(days=90)  # 3 meses atrás
    investment.sell(account)
    
    expected_value = investment.calculate_value()
    assert pytest.approx(account.balance, rel=1e-2) == expected_value
    assert len(account.transactions) == 1
    assert account.transactions[0].description == "Venda do investimento Ações"


def test_client_initialization():
    """Testa a inicialização de um objeto Client."""
    client = Client("João")
    assert client.name == "João"
    assert client.accounts == []
    assert client.investments == []


def test_client_add_account():
    """Testa o método add_account de Client."""
    client = Client("João")
    account = client.add_account("Conta Corrente")
    assert len(client.accounts) == 1
    assert client.accounts[0] == account
    assert account.name == "Conta Corrente"


def test_client_add_investment():
    """Testa o método add_investment de Client."""
    client = Client("João")
    investment = Investment("Ações", 1000.0, 0.02)
    client.add_investment(investment)
    assert len(client.investments) == 1
    assert client.investments[0] == investment


def test_client_get_net_worth():
    """Testa o método get_net_worth de Client."""
    client = Client("João")
    account = client.add_account("Conta Corrente")
    account.add_transaction(2000.0, "Salary", "Salário recebido")
    
    investment = Investment("Ações", 1000.0, 0.02)
    client.add_investment(investment)
    investment.date_purchased -= timedelta(days=90)  # 3 meses atrás
    
    expected_net_worth = account.balance + investment.calculate_value()
    assert pytest.approx(client.get_net_worth(), rel=1e-2) == expected_net_worth