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


-- Ticket promedio por cliente

SELECT
    c.cliente_nombre,
    COUNT(*) AS cantidad_compras,
    SUM(f.precio) AS total_gastado,
    ROUND(AVG(f.precio), 2) AS ticket_promedio
FROM fact_ventas f
JOIN dim_cliente c ON f.cliente_id = c.cliente_id
GROUP BY c.cliente_nombre
ORDER BY total_gastado DESC;


-- Ventas por mes con crecimiento

SELECT
    d.anio,
    d.mes,
    SUM(f.precio) AS ventas_mes
FROM fact_ventas f
JOIN dim_fecha d ON f.fecha_id = d.fecha_id
GROUP BY d.anio, d.mes
ORDER BY d.anio, d.mes;


-- Top productos por región

SELECT
    r.region_nombre,
    p.producto_nombre,
    COUNT(*) AS cantidad_vendida
FROM fact_ventas f
JOIN dim_region r ON f.region_id = r.region_id
JOIN dim_producto p ON f.producto_id = p.producto_id
GROUP BY r.region_nombre, p.producto_nombre
ORDER BY cantidad_vendida DESC;


-- Participación de ventas por región (%)

SELECT
    r.region_nombre,
    SUM(f.precio) AS total_ventas,
    ROUND(
        SUM(f.precio) * 100.0 / SUM(SUM(f.precio)) OVER (),
        2
    ) AS porcentaje_participacion
FROM fact_ventas f
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY r.region_nombre
ORDER BY total_ventas DESC;


-- Cliente más importante por región

SELECT
    region_nombre,
    cliente_nombre,
    total_gastado
FROM (
    SELECT
        r.region_nombre,
        c.cliente_nombre,
        SUM(f.precio) AS total_gastado,
        ROW_NUMBER() OVER (
            PARTITION BY r.region_nombre
            ORDER BY SUM(f.precio) DESC
        ) AS ranking
    FROM fact_ventas f
    JOIN dim_region r ON f.region_id = r.region_id
    JOIN dim_cliente c ON f.cliente_id = c.cliente_id
    GROUP BY r.region_nombre, c.cliente_nombre
) sub
WHERE ranking = 1;

-- Análisis de Crecimiento Mes a Mes (MoM) usando Window Functions

-- 1. CTE: Calculamos el total de ingresos por cada mes
WITH VentasMensuales AS (
    SELECT 
        EXTRACT(YEAR FROM d.fecha) AS anio,
        EXTRACT(MONTH FROM d.fecha) AS mes,
        SUM(f.precio) AS ingresos_actuales
    FROM fact_ventas f
    JOIN dim_fecha d ON f.fecha_id = d.fecha_id
    GROUP BY 
        EXTRACT(YEAR FROM d.fecha),
        EXTRACT(MONTH FROM d.fecha)
)

-- 2. Window Function: Comparamos el mes actual con el anterior
SELECT 
    anio,
    mes,
    ingresos_actuales,
    LAG(ingresos_actuales) OVER (ORDER BY anio, mes) AS ingresos_mes_anterior,
    
    -- ::numeric asegura que PostgreSQL respete los decimales
    ROUND(
        ( (ingresos_actuales - LAG(ingresos_actuales) OVER (ORDER BY anio, mes))::numeric * 100.0 ) / 
        LAG(ingresos_actuales) OVER (ORDER BY anio, mes)::numeric
    , 2) AS porcentaje_crecimiento
    
FROM VentasMensuales
ORDER BY anio, mes;