-- QUESTÃO 1 - EDA


-- PARTE 1 - Visão geral da tabela orders

SELECT *
FROM orders
LIMIT 10;

-- Quantidade de registros e valores preenchidos por coluna
SELECT 
    COUNT(*) AS total_linhas,
    COUNT(id) AS id_preenchidos,
    COUNT(order_number) AS order_number_preenchidos,
    COUNT(channel) AS channel_preenchidos,
    COUNT(customer_id) AS customer_id_preenchidos,
    COUNT(salesperson_id) AS salesperson_id_preenchidos,
    COUNT(location_id) AS location_id_preenchidos,
    COUNT(status) AS status_preenchidos,
    COUNT(subtotal) AS subtotal_preenchidos,
    COUNT(discount_amount) AS discount_amount_preenchidos,
    COUNT(total) AS total_preenchidos,
    COUNT(placed_at) AS placed_at_preenchidos,
    COUNT(created_at) AS created_at_preenchidos,
    COUNT(updated_at) AS updated_at_preenchidos
FROM orders;

-- Quantidade de valores nulos em salesperson_id
SELECT 
    COUNT(*) - COUNT(salesperson_id) AS nulos
FROM orders;

/*
Resultado observado:
- Total de registros: 48.998
- A maioria das colunas possui 48.998 valores preenchidos.
- salesperson_id possui 24.867 valores preenchidos,
  indicando 24.131 valores nulos.
*/

-- Quantidade total de colunas
SELECT 
    COUNT(*) AS quantidade_colunas
FROM information_schema.columns
WHERE table_name = 'orders';

-- Intervalo de datas analisado
SELECT 
    MIN(created_at) AS data_minima,
    MAX(created_at) AS data_maxima
FROM orders;


-- PARTE 2 - Análise de valores numéricos (coluna total)

SELECT 
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    ROUND(AVG(total), 2) AS valor_medio
FROM orders;


-- PARTE 3 - Interpretação (evidências estatísticas de apoio)


-- Desvio padrão e percentis para embasar a suspeita de outliers
SELECT
    ROUND(AVG(total), 2) AS media,
    ROUND(STDDEV(total), 2) AS desvio_padrao,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total) AS mediana,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total) AS p95,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY total) AS p99
FROM orders;

-- Verificar valores negativos ou zero em total (inconsistência)
SELECT COUNT(*) AS totais_invalidos
FROM orders
WHERE total <= 0;

