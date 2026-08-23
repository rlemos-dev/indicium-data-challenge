import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

products = pd.read_csv("products.csv")
product_variants = pd.read_csv("product_variants.csv")
orders = pd.read_csv("orders.csv")
order_items = pd.read_csv("order_items.csv")

produto = products[
    products["name"] == "Motor de Popa 1949"
]

produto_id = produto.iloc[0]["id"]

df_compras = (
    order_items
    .merge(
        orders[["id", "customer_id"]],
        left_on="order_id",
        right_on="id",
        how="inner"
    )
    .merge(
        product_variants[["id", "product_id"]],
        left_on="product_variant_id",
        right_on="id",
        how="inner"
    )
    [["customer_id", "product_id"]]
    .drop_duplicates()
)

matriz = pd.crosstab(
    df_compras["customer_id"],
    df_compras["product_id"]
)

similaridade = cosine_similarity(matriz.T)

df_similaridade = pd.DataFrame(
    similaridade,
    index=matriz.columns,
    columns=matriz.columns
)

similaridades_motor = df_similaridade.loc[produto_id]

ranking = (
    similaridades_motor
    .drop(index=produto_id)
    .sort_values(ascending=False)
    .head(5)
)

resultado = pd.DataFrame({
    "product_id": ranking.index,
    "similaridade": ranking.values
})

resultado = resultado.merge(
    products[["id", "name"]],
    left_on="product_id",
    right_on="id",
    how="left"
)

resultado = resultado[[
    "product_id",
    "name",
    "similaridade"
]]

resultado.insert(
    0,
    "ranking",
    range(1, len(resultado) + 1)
)

print("\nProdutos mais similares ao Motor de Popa 1949:")
print(resultado.to_string(index=False))
