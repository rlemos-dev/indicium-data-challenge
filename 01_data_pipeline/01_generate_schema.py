import os
import csv
from datetime import datetime

caminho_csv = "C:/Users/rafae/Code/Indicium AI/1-lh_nautical_csv"
caminho_sql = "C:/Users/rafae/Code/Indicium AI/Desafios/Questão 2/schema.sql"

os.chdir(caminho_csv)

# Colunas que são identificadores/documentos, não números de verdade.
# Mesmo "parecendo" número, nunca fazemos conta com eles, então são texto.
COLUNAS_FORCAR_VARCHAR = [
    "cpf", "cnpj", "tax_id", "phone", "telefone",
    "barcode_ean", "nfe_access_key", "cep", "zip_code", "ncm_code"
]

tabelas = []

for raiz, pastas, arquivos in os.walk("."):
    for arquivo in arquivos:
        if arquivo.endswith(".csv"):
            tabelas.append(os.path.join(raiz, arquivo))

with open(caminho_sql, "w", encoding="utf-8") as schema:
    for caminho_tabela in tabelas:
        with open(caminho_tabela, mode='r', encoding='utf-8') as arquivo_aberto:
            leitor = csv.DictReader(arquivo_aberto)

            dados = {}

            for linha in leitor:
                for nome_coluna in leitor.fieldnames:
                    if nome_coluna not in dados:
                        dados[nome_coluna] = []
                    dados[nome_coluna].append(linha[nome_coluna])

            nome_arquivo = os.path.basename(caminho_tabela)
            tabela = nome_arquivo.removesuffix(".csv")
            sql = f"CREATE TABLE {tabela} (\n"

            for nome_coluna in dados:

                # Se o nome da coluna bate com algo da lista, nem precisa detectar tipo
                if any(termo in nome_coluna.lower() for termo in COLUNAS_FORCAR_VARCHAR):
                    sql += f" {nome_coluna} VARCHAR,\n"
                    continue

                identificador = []

                for valor in dados[nome_coluna]:

                    if valor == "":
                        continue

                    try:
                        int(valor)
                        identificador.append('INTEGER')

                    except ValueError:
                        try:
                            float(valor)
                            identificador.append('NUMERIC')

                        except ValueError:
                            if valor.upper() in ("TRUE", "FALSE"):
                                identificador.append('BOOLEAN')

                            else:
                                try:
                                    datetime.strptime(valor, "%Y-%m-%d")
                                    identificador.append('DATE')

                                except ValueError:
                                    try:
                                        datetime.strptime(
                                            valor, "%Y-%m-%d %H:%M:%S")
                                        identificador.append('TIMESTAMP')

                                    except ValueError:
                                        identificador.append('VARCHAR')

                if set(identificador) == {"INTEGER", "VARCHAR"}:
                    rtype = "VARCHAR"

                elif set(identificador) == {"INTEGER", "NUMERIC"}:
                    rtype = "NUMERIC"

                elif set(identificador) == {"INTEGER"}:
                    rtype = "INTEGER"

                elif set(identificador) == {"NUMERIC"}:
                    rtype = "NUMERIC"

                elif set(identificador) == {"BOOLEAN"}:
                    rtype = "BOOLEAN"

                elif set(identificador) == {"DATE"}:
                    rtype = "DATE"

                elif set(identificador) == {"TIMESTAMP"}:
                    rtype = "TIMESTAMP"

                elif set(identificador) == {"VARCHAR"}:
                    rtype = "VARCHAR"

                elif len(set(identificador)) >= 3:
                    rtype = "VARCHAR"

                elif not identificador:
                    rtype = "VARCHAR"

                else:
                    print(f'Erro em {nome_coluna}: {set(identificador)}')
                    rtype = "VARCHAR"

                sql += f" {nome_coluna} {rtype},\n"

            sql = sql.removesuffix(",\n")
            sql += "\n);"

            schema.write(sql + "\n\n")

            print(' ')
            print(sql)
            print(' ')
            print('>=<' * 30)
