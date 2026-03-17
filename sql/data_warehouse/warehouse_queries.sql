-- Ventas totales por región

-- Esto permite identificar qué regiones 
-- generan más ingresos para la empresa.

SELECT
    r.region_nombre,
    SUM(f.precio) AS total_ventas
FROM fact_ventas f

JOIN dim_region r
ON f.region_id = r.region_id

GROUP BY r.region_nombre
ORDER BY total_ventas DESC;


-- Ranking de productos más vendidos

-- Permite identificar qué productos tienen mayor
-- demanda

SELECT
    p.producto_nombre,
    COUNT(*) AS cantidad_vendida
FROM fact_ventas f

JOIN dim_producto p
ON f.producto_id = p.producto_id

GROUP BY p.producto_nombre
ORDER BY cantidad_vendida DESC;


-- Clientes con mayor gasto total

-- Permite detectar clientes de alto valor

SELECT
    c.cliente_nombre,
    SUM(f.precio) AS total_gastado
FROM fact_ventas f

JOIN dim_cliente c
ON f.cliente_id = c.cliente_id

GROUP BY c.cliente_nombre
ORDER BY total_gastado DESC;


-- Ventas mensuales

-- Permite ver tendencias de ventas en el tiempo.

SELECT
    f2.anio,
    f2.mes,
    SUM(f.precio) AS total_ventas
FROM fact_ventas f

JOIN dim_fecha f2
ON f.fecha_id = f2.fecha_id

GROUP BY f2.anio, f2.mes
ORDER BY f2.anio, f2.mes;


-- Ticket promedio por venta

-- Permite estimar el valor promedio de cada venta.

SELECT
    AVG(precio) AS ticket_promedio
FROM fact_ventas;


-- Ventas por producto y región

-- Permite identificar qué productos funcionan 
-- mejor en cada región

SELECT
    p.producto_nombre,
    r.region_nombre,
    SUM(f.precio) AS total_ventas
FROM fact_ventas f

JOIN dim_producto p
ON f.producto_id = p.producto_id

JOIN dim_region r
ON f.region_id = r.region_id

GROUP BY p.producto_nombre, r.region_nombre
ORDER BY total_ventas DESC;