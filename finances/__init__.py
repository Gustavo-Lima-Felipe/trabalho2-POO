"""
Pacote NG Finances

Este pacote fornece ferramentas para gerenciamento de finanças pessoais, incluindo 
transações, contas bancárias, investimentos e relatórios financeiros.

Componentes principais:
- Transaction: Representa uma transação financeira.
- Account: Representa uma conta bancária e gerencia transações.
- Investment: Representa um investimento financeiro.
- Client: Representa um cliente e gerencia suas contas e investimentos.
- generate_report: Gera um relatório financeiro detalhado para um cliente.
- future_value_report: Gera projeções financeiras futuras para um cliente.
"""

from .models import Transaction, Account, Investment, Client
from .utils import generate_report, future_value_report

__all__ = [
    "Transaction",
    "Account",
    "Investment",
    "Client",
    "generate_report",
    "future_value_report"
]