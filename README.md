
# API para Geração de PDFs

## Índice
- [Visão Geral](#visão-geral)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Endpoints da API](#endpoints-da-api)
  - [GET /reports/{report_id}](#get-reportsreport_id)
  - [POST /reports](#post-reports)
- [Exemplos de Uso](#exemplos-de-uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Execução e Testes](#execução-e-testes)

---

## Visão Geral

Esta API permite a geração de documentos em PDF com informações extraídas de um banco de dados PostgreSQL. Utilizando o framework FastAPI para a criação dos endpoints, a biblioteca `FPDF` para a formatação e geração de PDFs, e PostgreSQL como banco de dados relacional.

### Tecnologias Utilizadas
- **Python 3.9+**
- **FastAPI**: Framework web para desenvolvimento rápido de APIs REST.
- **FPDF**: Biblioteca para geração de documentos PDF.
- **SQLAlchemy**: ORM para integração com o banco de dados PostgreSQL.
- **PostgreSQL**: Banco de dados relacional para armazenamento de dados.
- **Docker** (opcional): Para contêinerizar a aplicação e simplificar o ambiente de execução.

## Configuração do Ambiente

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/seu-repositorio/nome-do-projeto.git
   cd nome-do-projeto
   ```

2. **Configuração do Banco de Dados**:
   Certifique-se de ter o PostgreSQL instalado e configure o banco:
   ```sql
   CREATE DATABASE nome_do_banco;
   CREATE USER usuario_com_senha PASSWORD 'sua_senha';
   GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO usuario_com_senha;
   ```

3. **Configurar variáveis de ambiente**:
   Crie um arquivo `.env` com as seguintes variáveis:
   ```env
   DATABASE_URL=postgresql://usuario_com_senha:sua_senha@localhost:5432/nome_do_banco
   ```

4. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Iniciar a aplicação**:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints da API

## Exemplos de Uso

Para obter o PDF de um relatório com `report_id = 123`, use:
```bash
curl -X GET "http://localhost:8000/reports/123" -o relatorio_123.pdf
```

Para criar um novo relatório com conteúdo e gerar o PDF imediatamente:
```bash
curl -X POST "http://localhost:8000/reports" -H "Content-Type: application/json" -d '{
  "title": "Relatório de Estoque",
  "content": "Informações detalhadas sobre o estoque atual.",
  "generate_pdf": true
}'
```

## Estrutura do Projeto

```plaintext
nome-do-projeto/
├── app/
│   ├── main.py          # Arquivo principal da aplicação FastAPI
│   ├── connection.py      # Configuração e conexão com o banco de dados
│   ├── pdf_generator.py # Lógica para gerar PDFs com FPDF
│   ├── queries.py          # Funções CRUD para interagir com o banco
├── tests/               # Testes unitários e de integração
│   ├── test_reports.py
├── .env                 # Variáveis de ambiente (não comitar)
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

---

Este é um exemplo de documentação completa para a API de geração de PDFs, que cobre desde a configuração inicial até os detalhes dos endpoints e exemplos de uso.
