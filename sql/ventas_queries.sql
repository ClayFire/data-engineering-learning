-- =========================================================
-- Proyecto: Pipeline de Ventas
-- Descripción: Consultas analíticas sobre ventas_pipeline
-- =========================================================


-- =========================================
-- Ver todos los registros cargados
-- =========================================
SELECT * FROM ventas_pipeline;


-- =========================================
-- Ventas totales por región
-- =========================================
SELECT region, SUM(precio) AS total_ventas
FROM ventas_pipeline
GROUP BY region
ORDER BY total_ventas DESC;


-- =========================================
-- Producto más vendido
-- =========================================
SELECT producto, COUNT(*) AS cantidad_vendida
FROM ventas_pipeline
GROUP BY producto
ORDER BY cantidad_vendida DESC;


-- =========================================
-- Cliente que más gastó
-- =========================================
SELECT cliente, SUM(precio) AS total_gastado
FROM ventas_pipeline
GROUP BY cliente
ORDER BY total_gastado DESC;


-- =========================================
-- Ventas por mes
-- =========================================
SELECT DATE_TRUNC('month', fecha) AS mes,
SUM(precio) AS ventas
FROM ventas_pipeline
GROUP BY mes
ORDER BY mes;


-- =========================================
-- Venta más cara registrada
-- =========================================
SELECT *
FROM ventas_pipeline
ORDER BY precio DESC
LIMIT 1;


-- =========================================
-- Evitar duplicados en el pipeline
-- =========================================
ALTER TABLE ventas_pipeline
ADD CONSTRAINT unique_venta
UNIQUE (cliente, producto, fecha);