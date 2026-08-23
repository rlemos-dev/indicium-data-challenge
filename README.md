# 📊 Indicium Data Challenge

Resolução do case técnico de dados da Indicium. O projeto envolve um pipeline ponta a ponta: desde a modelagem e ingestão de dados em SQL, passando por análises de negócio, até modelos de machine learning e previsão de demanda utilizando Python.

---

## 🏗️ Arquitetura do Projeto

O repositório foi organizado para refletir as etapas lógicas de um projeto de engenharia e ciência de dados no mundo real:

### 📁 `01_data_pipeline` (Engenharia de Dados & Modelagem)
Automação e criação do banco de dados relacional.
*   **`generate_schema.py`:** Script em Python que analisa os arquivos `.csv` brutos, infere os tipos de dados automaticamente (protegendo identificadores como CPF/CNPJ) e gera os comandos DDL de criação das tabelas.
*   **`schema.sql`:** O arquivo final DDL com a estrutura do banco gerado pelo script anterior.
*   **`load_database.py`:** Script de carga (ELT) utilizando `psycopg2`. Ele garante a idempotência (verifica se o banco e as tabelas já existem) e utiliza o comando `COPY` do PostgreSQL para ingestão em alta performance.

### 📁 `02_sql_analysis` (Análise de Negócios)
Resolução de problemas de negócio utilizando SQL avançado.
*   **`01_eda_orders.sql`:** Análise exploratória focada em completude, volumetria, distribuição e identificação de anomalias estatísticas na tabela de pedidos.
*   **`02_categoria_elite.sql`:** Consulta analítica com CTEs (`WITH`) para identificar a categoria de produto mais consumida pelos "clientes de elite" (alta diversidade de compras e maior ticket médio).
*   **`03_vendas_por_dia.sql`:** Análise temporal utilizando `generate_series` para criar um calendário contínuo e calcular a média diária de vendas no canal físico ('pos'), tratando corretamente os dias sem vendas.

### 📁 `03_demand_forecast` (Ciência de Dados / Séries Temporais)
*   **`previsao_vendas.py`:** Extração de dados diretamente do PostgreSQL via SQLAlchemy para construir um modelo de baseline de previsão de demanda (Média Móvel) utilizando `pandas` e validado através da métrica MAE (Scikit-Learn).

### 📁 `04_recommendation_system` (Machine Learning)
*   **`recomendacao_produtos.py`:** Criação de um sistema de recomendação baseado em itens (Filtro Colaborativo). Utiliza a matriz de interações cliente-produto e calcula a similaridade através da técnica de `cosine_similarity`.

---

## 🚀 Como Executar

Para reproduzir este ambiente na sua máquina local:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/rlemos-dev/indicium-data-challenge.git](https://github.com/rlemos-dev/indicium-data-challenge.git)
   cd indicium-data-challenge
   ```

2. **Instale as dependências:**
   É recomendado o uso de um ambiente virtual (venv).
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure os Dados (Não inclusos no repositório):**
   * Crie uma pasta local para armazenar os arquivos `.csv` fornecidos no desafio.
   * *Atenção: Por questões de segurança e boas práticas (conforme o `.gitignore`), os arquivos de dados brutos não foram subidos para o GitHub.*

4. **Inicie o Banco de Dados:**
   * Certifique-se de ter o PostgreSQL rodando localmente (porta 5432).
   * Ajuste as credenciais no arquivo `load_database.py`.
   * Execute o script de carga para criar e popular o banco.

---

*Projeto desenvolvido para o processo seletivo da Indicium.*
