WITH periodo AS (
    SELECT
        MIN(placed_at::DATE) AS data_inicio,
        MAX(placed_at::DATE) AS data_fim
    FROM orders
    WHERE channel = 'pos'
),

calendario AS (
    SELECT
        data::DATE AS data,
        EXTRACT(ISODOW FROM data)::INT AS numero_dia,
        CASE EXTRACT(ISODOW FROM data)
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
            WHEN 7 THEN 'Domingo'
        END AS semanal
    FROM periodo,
    generate_series(data_inicio, data_fim, INTERVAL '1 day') AS data
),

vendas_diarias AS (
    SELECT
        c.data,
        c.numero_dia,
        c.semanal,
        COALESCE(SUM(o.total), 0) AS vendas
    FROM calendario c
    LEFT JOIN orders o
        ON c.data = o.placed_at::DATE
        AND o.channel = 'pos'
    GROUP BY
        c.data,
        c.numero_dia,
        c.semanal
)

SELECT
    numero_dia,
    semanal,
    ROUND(AVG(vendas), 2) AS media_vendas
FROM vendas_diarias
GROUP BY
    numero_dia,
    semanal
ORDER BY
    media_vendas;
