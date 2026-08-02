# 🏆 Dundie Rewards System (Dunder Mifflin)

[![CI](https://github.com/GeovaneParedes/dundie-rewards/actions/workflows/main.yml/badge.svg)](https://github.com/GeovaneParedes/dundie-rewards/actions/workflows/main.yml)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)
![Linter: flake8](https://img.shields.io/badge/linter-flake8-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Sistema de recompensas e pontos corporativos desenvolvido para a **Dunder Mifflin Paper Company**.

O sistema permite gerenciar pontos por funcionário, conceder bônus por metas, efetuar transferências entre colaboradores e realizar o resgate de recompensas.

---

## 🚀 Funcionalidades & Módulos

- **Autenticação & Segurança (Issues #4 e #7):** Operações administrativas e de funcionário protegidas por usuário e senha com hash de segurança.
- **Carga de Dados (CLI):** Importação de colaboradores via arquivos CSV, TXT e JSON.
- **Movimentações e Transferências (Issues #5 e #6):** Consulta de saldo/extrato e transferência direta de pontos entre colaboradores.
- **Validação de Regras de Negócio:** Pontuação inicial por cargo (Manager vs Outros), controle de extrato e auditoria de movimentações.

---

## 🛠️ Como Executar o Projeto

```bash
# Clone o repositório
git clone git@github.com:GeovaneParedes/dundie-rewards.git
cd dundie-rewards

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências e o pacote em modo editável
pip install -e .[test,dev]
```

### 💻 Utilizando o CLI (`dundie`)

```bash
# Carregar dados iniciais de funcionários
dundie load assets/sample_data.csv --user admin@dundler.com --password minhasenha

# Visualizar relatório de pontuação
dundie show

# Adicionar pontos a um funcionário
dundie add 100 --email joe@doe.com --user admin@dundler.com --password minhasenha
```

---

## 🧪 Suíte de Testes & Qualidade de Código

O projeto conta com automação completa de testes e linters PEP8:

```bash
# Executar a suíte de testes unitários e integração
pytest

# Verificar padronização de imports e código
isort --check dundie tests integration conftest.py
black --check dundie tests integration conftest.py
flake8 dundie tests integration conftest.py
```

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
