import pytest
from datetime import datetime, timedelta
from finances.models import Client, Account, Investment
from finances.utils import generate_report, future_value_report


def test_generate_report():
    """
    Testa a função generate_report para gerar um relatório financeiro completo de um cliente.
    """
    # Setup do cliente
    client = Client("Maria")
    account1 = client.add_account("Conta Corrente")
    account2 = client.add_account("Poupança")
    account1.add_transaction(1000.0, "Salary", "Salário recebido")
    account1.add_transaction(-200.0, "Food", "Supermercado")
    account2.add_transaction(500.0, "Transfer", "Transferência recebida")
    
    investment1 = Investment("Ações", 1000.0, 0.02)
    client.add_investment(investment1)
    investment1.date_purchased -= timedelta(days=90)  # 3 meses atrás

    # Geração do relatório
    report = generate_report(client)
    
    # Verificação de conteúdo do relatório
    assert f"Relatório Financeiro de {client.name}" in report
    assert f"- {account1.name}: Saldo R$ {account1.balance:.2f}" in report
    assert f"- {investment1.type}: Valor Atual" in report
    assert f"Patrimônio Líquido:\nR$ {client.get_net_worth():.2f}" in report


def test_future_value_report():
    """
    Testa a função future_value_report para gerar projeções financeiras de um cliente.
    """
    # Setup do cliente
    client = Client("João")
    account1 = client.add_account("Conta Corrente")
    account1.add_transaction(500.0, "Salary", "Salário recebido")
    
    investment1 = Investment("Ações", 1000.0, 0.02)
    investment2 = Investment("CDB", 2000.0, 0.01)
    client.add_investment(investment1)
    client.add_investment(investment2)
    investment1.date_purchased -= timedelta(days=90)  # 3 meses atrás
    investment2.date_purchased -= timedelta(days=30)  # 1 mês atrás

    # Data futura para projeção
    future_date = datetime.now() + timedelta(days=180)  # 6 meses no futuro

    # Geração do relatório de projeção
    report = future_value_report(client, future_date)

    # Cálculos esperados
    months_to_date = 6  # 6 meses
    expected_investment1_value = investment1.initial_amount * ((1 + investment1.rate_of_return) ** months_to_date)
    expected_investment2_value = investment2.initial_amount * ((1 + investment2.rate_of_return) ** months_to_date)
    expected_net_worth = account1.balance + expected_investment1_value + expected_investment2_value

    # Verificação de conteúdo do relatório
    assert f"Projeção Financeira de {client.name} para" in report
    assert f"- {investment1.type}: Valor Projetado R$ {expected_investment1_value:.2f}" in report
    assert f"- {investment2.type}: Valor Projetado R$ {expected_investment2_value:.2f}" in report
    assert f"Patrimônio Líquido Projetado:\nR$ {expected_net_worth:.2f}" in report


def test_future_value_report_invalid_date():
    """
    Testa a função future_value_report para garantir comportamento correto ao receber uma data passada.
    """
    # Setup do cliente
    client = Client("Joana")
    past_date = datetime.now() - timedelta(days=30)  # 30 dias no passado

    # Tentativa de gerar relatório com data passada
    report = future_value_report(client, past_date)

    # Verificação de resposta
    assert report == "A data fornecida deve ser futura."
