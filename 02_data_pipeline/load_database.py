import psycopg2
from psycopg2 import sql
import os

caminho_csv = "C:/Users/rafae/Code/Indicium AI/1-lh_nautical_csv"
caminho_sql = "C:/Users/rafae/Code/Indicium AI/Desafios/Questão 2/schema.sql"

NOME_BANCO = "Indicium"

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "SUA_SENHA_AQUI"
}

connect = psycopg2.connect(
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database="postgres",
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"]
)

connect.autocommit = True
cursor = connect.cursor()

cursor.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    (NOME_BANCO,)
)

existe = cursor.fetchone()

if not existe:
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(NOME_BANCO)
        )
    )

    print(f"Banco '{NOME_BANCO}' criado com sucesso!")

else:
    print(f"Banco '{NOME_BANCO}' já existe")

cursor.close()
connect.close()

connect = psycopg2.connect(
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=NOME_BANCO,
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"]
)

cursor = connect.cursor()

with open(caminho_sql, "r", encoding="utf-8") as arquivo:
    schema = arquivo.read()

try:
    cursor.execute(schema)
    connect.commit()

    print("Schema criado com sucesso!")

except psycopg2.errors.DuplicateTable:
    connect.rollback()
    print("As tabelas já existem. Schema não foi recriado.")

for raiz, pastas, arquivos in os.walk(caminho_csv):

    for arquivo in arquivos:

        if not arquivo.endswith(".csv"):
            continue

        caminho_arquivo = os.path.join(raiz, arquivo)
        nome_tabela = arquivo.removesuffix(".csv")

        print(f"\nVerificando tabela: {nome_tabela}")

        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            )
            """,
            (nome_tabela,)
        )

        tabela_existe = cursor.fetchone()[0]

        if not tabela_existe:
            print(f"Tabela '{nome_tabela}' não existe. Pulando...")
            continue

        cursor.execute(
            sql.SQL("SELECT COUNT(*) FROM {}").format(
                sql.Identifier(nome_tabela)
            )
        )

        quantidade = cursor.fetchone()[0]

        if quantidade > 0:
            print(
                f"Tabela '{nome_tabela}' já possui "
                f"{quantidade} linhas. Não será carregada novamente."
            )
            continue

        print(f"Carregando {nome_tabela}...")

        try:

            with open(
                caminho_arquivo,
                "r",
                encoding="utf-8"
            ) as arquivo_csv:

                comando_copy = sql.SQL(
                    """
                    COPY {} 
                    FROM STDIN 
                    WITH (
                        FORMAT csv,
                        HEADER true
                    )
                    """
                ).format(
                    sql.Identifier(nome_tabela)
                )

                cursor.copy_expert(
                    comando_copy,
                    arquivo_csv
                )

            connect.commit()

            print(
                f"{nome_tabela} carregada com sucesso!"
            )

        except Exception as e:

            connect.rollback()

            print(
                f"Erro ao carregar {nome_tabela}: {e}"
            )


print("\nTodos os CSVs foram processados!")

print("QUESTÃO 3.2 - VALIDAÇÃO")

tabelas_validacao = [
    "customers",
    "orders",
    "order_items",
    "payments"
]

total_linhas = 0

for tabela in tabelas_validacao:

    cursor.execute(
        sql.SQL("SELECT COUNT(*) FROM {}").format(
            sql.Identifier(tabela)
        )
    )

    quantidade = cursor.fetchone()[0]

    print(f"{tabela}: {quantidade} linhas")

    total_linhas += quantidade


print(f"TOTAL DE LINHAS: {total_linhas}")


cursor.close()
connect.close()
