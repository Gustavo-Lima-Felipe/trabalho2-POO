from datetime import datetime, timedelta
from typing import List
from .models import Client, Transaction, Account, Investment


def generate_report(client: Client) -> str:
    """
    Gera um relatório financeiro detalhado para o cliente.

    Args:
        client (Client): O cliente para o qual o relatório será gerado.

    Returns:
        str: Um relatório formatado contendo informações sobre contas, transações e investimentos do cliente.
    """
    report_lines = [f"Relatório Financeiro de {client.name}", "-" * 40]
    
    # Contas
    report_lines.append("\nContas:")
    for account in client.accounts:
        report_lines.append(f" - {account.name}: Saldo R$ {account.balance:.2f}")
        if account.transactions:
            report_lines.append("   Transações:")
            for transaction in account.transactions:
                report_lines.append(f"     {transaction}")

    # Investimentos
    report_lines.append("\nInvestimentos:")
    if client.investments:
        for investment in client.investments:
            current_value = investment.calculate_value()
            report_lines.append(
                f" - {investment.type}: Valor Atual R$ {current_value:.2f} (Taxa de Retorno: {investment.rate_of_return * 100:.2f}%)"
            )
    else:
        report_lines.append(" - Nenhum investimento registrado.")

    # Patrimônio líquido
    net_worth = client.get_net_worth()
    report_lines.append("\nPatrimônio Líquido:")
    report_lines.append(f"R$ {net_worth:.2f}")
    
    return "\n".join(report_lines)


def future_value_report(client: Client, date: datetime) -> str:
    """
    Gera um relatório de projeção de valores futuros para o cliente, incluindo investimentos e saldo das contas.

    Args:
        client (Client): O cliente para o qual o relatório será gerado.
        date (datetime): A data futura para calcular as projeções.

    Returns:
        str: Um relatório formatado contendo projeções de valores futuros.
    """
    report_lines = [f"Projeção Financeira de {client.name} para {date.strftime('%d/%m/%Y')}", "-" * 40]
    
    # Cálculo do número de meses entre agora e a data fornecida
    now = datetime.now()
    if date <= now:
        return "A data fornecida deve ser futura."
    months_to_date = (date.year - now.year) * 12 + (date.month - now.month)
    
    # Contas (Saldo atual, sem projeção de mudanças)
    report_lines.append("\nProjeção de Contas:")
    for account in client.accounts:
        report_lines.append(f" - {account.name}: Saldo Atual R$ {account.balance:.2f}")

    # Investimentos (Projeção com base na taxa de retorno)
    report_lines.append("\nProjeção de Investimentos:")
    if client.investments:
        for investment in client.investments:
            future_value = investment.initial_amount * ((1 + investment.rate_of_return) ** months_to_date)
            report_lines.append(
                f" - {investment.type}: Valor Projetado R$ {future_value:.2f} (Taxa de Retorno: {investment.rate_of_return * 100:.2f}%)"
            )
    else:
        report_lines.append(" - Nenhum investimento registrado.")

    # Patrimônio líquido projetado
    accounts_total = sum(account.balance for account in client.accounts)
    investments_total = sum(
        investment.initial_amount * ((1 + investment.rate_of_return) ** months_to_date)
        for investment in client.investments
    )
    projected_net_worth = accounts_total + investments_total
    report_lines.append("\nPatrimônio Líquido Projetado:")
    report_lines.append(f"R$ {projected_net_worth:.2f}")

    return "\n".join(report_lines)
