from datetime import datetime, timedelta
from finances.models import Client, Account, Investment
from finances.utils import generate_report, future_value_report


def main():
    # Criando um cliente
    print("Criando cliente...")
    client = Client("João Silva")
    print(f"Cliente criado: {client.name}\n")

    # Adicionando contas ao cliente
    print("Adicionando contas...")
    account1 = client.add_account("Conta Corrente")
    account2 = client.add_account("Poupança")
    print(f"Contas adicionadas: {[account.name for account in client.accounts]}\n")

    # Adicionando transações às contas
    print("Adicionando transações...")
    account1.add_transaction(3000.0, "Salary", "Salário recebido")
    account1.add_transaction(-500.0, "Food", "Supermercado")
    account2.add_transaction(1000.0, "Transfer", "Transferência recebida")
    print(f"Saldo de {account1.name}: R$ {account1.balance:.2f}")
    print(f"Saldo de {account2.name}: R$ {account2.balance:.2f}\n")

    # Adicionando investimentos
    print("Adicionando investimentos...")
    investment1 = Investment("Ações", 2000.0, 0.015)  # Retorno de 1,5% ao mês
    investment2 = Investment("CDB", 5000.0, 0.01)  # Retorno de 1% ao mês
    investment1.date_purchased -= timedelta(days=90)  # Investido há 3 meses
    investment2.date_purchased -= timedelta(days=180)  # Investido há 6 meses
    client.add_investment(investment1)
    client.add_investment(investment2)
    print(f"Investimentos adicionados: {[inv.type for inv in client.investments]}\n")

    # Gerando relatório financeiro
    print("Gerando relatório financeiro...")
    report = generate_report(client)
    print(report)

    # Projeção financeira futura
    print("\nGerando projeção financeira futura...")
    future_date = datetime.now() + timedelta(days=365)  # 1 ano no futuro
    projection = future_value_report(client, future_date)
    print(projection)


if __name__ == "__main__":
    main()
