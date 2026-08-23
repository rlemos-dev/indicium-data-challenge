import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error

connect = create_engine(
    "postgresql+psycopg2://postgres:SUA_SENHA_AQUI@localhost:5432/Indicium"
)

query = """
    SELECT
        o.placed_at::DATE AS data,
        oi.quantity,
        p.id   AS product_id,
        p.name AS product_name,
        pv.id  AS product_variant_id
    FROM products p
    JOIN product_variants pv
        ON pv.product_id = p.id
    JOIN order_items oi
        ON oi.product_variant_id = pv.id
    JOIN orders o
        ON o.id = oi.order_id
    WHERE p.name = 'Bússola de Bordo 702'
      AND o.placed_at::DATE <= '2026-03-31'
    ORDER BY data;
"""

df_vendas = pd.read_sql(query, connect)

if df_vendas.empty:
    raise ValueError("Nenhuma venda encontrada para o produto informado.")

print("Produtos (product_id) encontrados para esse nome:")
print(df_vendas["product_id"].unique())

df_vendas["data"] = pd.to_datetime(df_vendas["data"])
df_vendas["mes"] = df_vendas["data"].dt.to_period("M")

df_mensal = (
    df_vendas
    .groupby("mes")["quantity"]
    .sum()
)

periodo_completo = pd.period_range(
    start=df_mensal.index.min(),
    end="2026-03",
    freq="M"
)

df_mensal = df_mensal.reindex(periodo_completo, fill_value=0).reset_index()
df_mensal.columns = ["mes", "quantity"]

print("\nSérie mensal completa (com meses sem venda = 0):")
print(df_mensal)

treino = df_mensal[df_mensal["mes"] <= "2025-12"].copy()
teste = df_mensal[
    (df_mensal["mes"] >= "2026-01") & (df_mensal["mes"] <= "2026-03")
].copy()

if len(treino) < 3:
    raise ValueError("Menos de 3 meses de histórico antes do teste — "
                     "a média móvel de 3 meses não pode ser calculada.")

dados = pd.concat([treino, teste]).reset_index(drop=True)

inicio_teste = len(treino)
previsoes = []

for i in range(len(teste)):
    indice = inicio_teste + i
    ultimos_3 = dados["quantity"].iloc[indice - 3:indice]
    previsao = ultimos_3.mean()
    previsoes.append(previsao)

resultado = teste.copy()
resultado["previsao"] = previsoes

print("\nPrevisões x Real (1º trimestre de 2026):")
print(resultado)

mae = mean_absolute_error(resultado["quantity"], resultado["previsao"])
print(f"\nMAE: {mae:.2f} unidades")
