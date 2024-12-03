# NG Finances

Um pacote Python para gerenciar finanças pessoais, incluindo transações, contas e investimentos.

## Descrição

O pacote **NG Finances** ajuda os usuários a gerenciar receitas, despesas e investimentos. 
Ele fornece ferramentas para rastreamento de transações, categorização, análise financeira 
e geração de relatórios financeiros e projeções futuras.

## Recursos

- Gerencia de contas e transações financeiras;
- Rastreia investimentos com cálculos de rendimento;
- Gera relatórios financeiros detalhados;
- Mostra projeções futuras de patrimônio.

## Instalação:

1. Clone o repositório:

```bash
git clone https://github.com/Gustavo-Lima-Felipe/trabalho2-POO.git

```

2. Navegue até o diretório do projeto e instale o pacote:

```bash
cd finances
pip install .

```
3. Para instalar as dependências adicionais, execute:

```bash
pip install -r requirements.txt

```

## Uso

Crie um cliente, adicione uma conta e registre transações:

```python
from finances.models import Client

client = Client("Alice")
account = client.add_account("Conta Corrente")
account.add_transaction(5000.0, "Salário", "Recebimento de salário")
```

Gere um relatório financeiro:

```python
from finances.utils import generate_report

print(generate_report(client))
```

## Testes

Para executar os testes, utilize **pytest**:

```bash
pytest
```

## Licença

Este projeto está licenciado sob os termos da Licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

## Contato

Criado por Gustavo Lima Felipe (https://github.com/Gustavo-Lima-Felipe).
