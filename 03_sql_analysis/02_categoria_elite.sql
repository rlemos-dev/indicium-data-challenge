WITH clientes_orders AS (
	SELECT 
		customer_id, 
		SUM(total) as faturamento_total,
		COUNT(id) as frequencia,
		SUM(total)/COUNT(id) as ticket_medio
	FROM orders
	GROUP BY customer_id
),

clientes_products AS (
	SELECT 
		o.customer_id, 
		COUNT(DISTINCT pr.category_id) as diversidade_categorias
	FROM orders o
	JOIN order_items oi
		ON o.id = oi.order_id

	JOIN product_variants pv
		ON oi.product_variant_id = pv.id

	JOIN products pr
		ON pv.product_id = pr.id
	GROUP BY o.customer_id
),

clientes_elite AS (
	SELECT
		co.customer_id,
		co.faturamento_total,
		co.frequencia,
		co.ticket_medio,
		cp.diversidade_categorias
			FROM clientes_orders co
			JOIN clientes_products cp
				ON co.customer_id = cp.customer_id
			WHERE cp.diversidade_categorias >= 13
			ORDER BY 
				co.ticket_medio DESC,
				co.customer_id ASC
			LIMIT 10
)

SELECT
	c.id AS category_id,
	c.name AS category_name,
	SUM(oi.quantity) AS quantidade_total
FROM clientes_elite ce
JOIN orders o
	ON ce.customer_id = o.customer_id
JOIN order_items oi
	ON o.id = oi.order_id
JOIN product_variants pv
	ON oi.product_variant_id = pv.id
JOIN products p
	ON pv.product_id = p.id
JOIN categories c
	ON p.category_id = c.id
GROUP BY
	c.id,
	c.name
ORDER BY quantidade_total DESC
LIMIT 1;
	
