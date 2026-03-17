-- =====================================
-- DIMENSION: CLIENTE
-- =====================================

CREATE TABLE dim_cliente (
    cliente_id SERIAL PRIMARY KEY,
    cliente_nombre TEXT UNIQUE
);


-- =====================================
-- DIMENSION: PRODUCTO
-- =====================================

CREATE TABLE dim_producto (
    producto_id SERIAL PRIMARY KEY,
    producto_nombre TEXT UNIQUE
);


-- =====================================
-- DIMENSION: REGION
-- =====================================

CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    region_nombre TEXT UNIQUE
);


-- =====================================
-- DIMENSION: FECHA
-- =====================================

CREATE TABLE dim_fecha (
    fecha_id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE,
    anio INT,
    mes INT,
    dia INT
);


-- =====================================
-- TABLA DE HECHOS: VENTAS
-- =====================================

CREATE TABLE fact_ventas (

    venta_id SERIAL PRIMARY KEY,

    cliente_id INT REFERENCES dim_cliente(cliente_id),

    producto_id INT REFERENCES dim_producto(producto_id),

    region_id INT REFERENCES dim_region(region_id),

    fecha_id INT REFERENCES dim_fecha(fecha_id),

    precio INT
);