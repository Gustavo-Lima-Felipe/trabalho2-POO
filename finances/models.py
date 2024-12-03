from datetime import datetime
from typing import List, Optional


class Transaction:
    """
    Representa uma transação financeira.

    Atributos:
        amount (float): Valor da transação.
        date (datetime): Data da transação.
        category (str): Categoria da transação.
        description (str): Descrição da transação.
    """

    def __init__(self, amount: float, category: str, description: str = "") -> None:
        """
        Inicializa uma transação.

        Args:
            amount (float): Valor da transação.
            category (str): Categoria da transação.
            description (str, optional): Descrição da transação. Padrão é "".
        """
        self.amount: float = amount
        self.date: datetime = datetime.now()
        self.category: str = category
        self.description: str = description

    def __str__(self) -> str:
        """
        Retorna uma representação textual da transação.

        Returns:
            str: Descrição formatada da transação.
        """
        return f"Transação: {self.description} R$ {self.amount:.2f} ({self.category})"

    def update(self, **attributes) -> None:
        """
        Atualiza um ou mais atributos da transação.

        Args:
            attributes: Atributos a serem atualizados, passados como argumentos nomeados.
        """
        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Account:
    """
    Representa uma conta bancária.

    Atributos:
        name (str): Nome da conta.
        balance (float): Saldo da conta.
        transactions (List[Transaction]): Lista de transações na conta.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa uma conta.

        Args:
            name (str): Nome da conta.
        """
        self.name: str = name
        self.balance: float = 0.0
        self.transactions: List[Transaction] = []

    def add_transaction(self, amount: float, category: str, description: str = "") -> Transaction:
        """
        Adiciona uma transação à conta e atualiza o saldo.

        Args:
            amount (float): Valor da transação.
            category (str): Categoria da transação.
            description (str, optional): Descrição da transação. Padrão é "".

        Returns:
            Transaction: A transação criada.
        """
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        self.balance += amount
        return transaction

    def get_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None
    ) -> List[Transaction]:
        """
        Retorna uma lista de transações filtradas por data e/ou categoria.

        Args:
            start_date (datetime, optional): Data inicial para filtro. Padrão é None.
            end_date (datetime, optional): Data final para filtro. Padrão é None.
            category (str, optional): Categoria para filtrar. Padrão é None.

        Returns:
            List[Transaction]: Lista de transações filtradas.
        """
        filtered = self.transactions
        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]
        if category:
            filtered = [t for t in filtered if t.category == category]
        return filtered


class Investment:
    """
    Representa um investimento financeiro.

    Atributos:
        type (str): Tipo do investimento.
        initial_amount (float): Valor inicial investido.
        date_purchased (datetime): Data da compra do investimento.
        rate_of_return (float): Taxa mensal de retorno (em decimal).
    """

    def __init__(self, type: str, amount: float, rate_of_return: float) -> None:
        """
        Inicializa um investimento.

        Args:
            type (str): Tipo do investimento.
            amount (float): Valor inicial investido.
            rate_of_return (float): Taxa de retorno mensal (em decimal).
        """
        self.type: str = type
        self.initial_amount: float = amount
        self.date_purchased: datetime = datetime.now()
        self.rate_of_return: float = rate_of_return

    def calculate_value(self) -> float:
        """
        Calcula o valor atual do investimento com base no tempo decorrido.

        Returns:
            float: Valor atual do investimento.
        """
        months_elapsed = (datetime.now() - self.date_purchased).days // 30
        return self.initial_amount * ((1 + self.rate_of_return) ** months_elapsed)

    def sell(self, account: Account) -> None:
        """
        Vende o investimento e deposita o valor em uma conta.

        Args:
            account (Account): Conta para depositar os rendimentos.
        """
        value = self.calculate_value()
        account.add_transaction(value, "Investment Sale", f"Venda do investimento {self.type}")


class Client:
    """
    Representa um cliente com contas e investimentos.

    Atributos:
        name (str): Nome do cliente.
        accounts (List[Account]): Contas do cliente.
        investments (List[Investment]): Investimentos do cliente.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa um cliente.

        Args:
            name (str): Nome do cliente.
        """
        self.name: str = name
        self.accounts: List[Account] = []
        self.investments: List[Investment] = []

    def add_account(self, account_name: str) -> Account:
        """
        Cria uma nova conta para o cliente.

        Args:
            account_name (str): Nome da conta.

        Returns:
            Account: A nova conta criada.
        """
        account = Account(account_name)
        self.accounts.append(account)
        return account

    def add_investment(self, investment: Investment) -> None:
        """
        Adiciona um investimento para o cliente.

        Args:
            investment (Investment): Investimento a ser adicionado.
        """
        self.investments.append(investment)

    def get_net_worth(self) -> float:
        """
        Calcula o patrimônio líquido do cliente (contas + investimentos).

        Returns:
            float: O patrimônio líquido total.
        """
        accounts_total = sum(account.balance for account in self.accounts)
        investments_total = sum(investment.calculate_value() for investment in self.investments)
        return accounts_total + investments_total
